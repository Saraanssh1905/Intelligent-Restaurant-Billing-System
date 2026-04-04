
-- FILE: 04_triggers.sql  |  Run AFTER 03_procedures.sql

USE restaurant_db;

DELIMITER $$


-- TRIGGER 1: trg_auto_subtotal
-- Auto-calculates subtotal = price * quantity BEFORE INSERT

CREATE TRIGGER trg_auto_subtotal
BEFORE INSERT ON ORDER_ITEM
FOR EACH ROW
BEGIN
    DECLARE v_price DECIMAL(10,2);
    SELECT price INTO v_price FROM MENU_ITEM WHERE item_id = NEW.item_id;
    SET NEW.subtotal = v_price * NEW.quantity;
END$$


-- TRIGGER 2: trg_recalc_subtotal_on_update
-- Recalculates subtotal when quantity is updated

CREATE TRIGGER trg_recalc_subtotal_on_update
BEFORE UPDATE ON ORDER_ITEM
FOR EACH ROW
BEGIN
    DECLARE v_price DECIMAL(10,2);
    IF NEW.quantity != OLD.quantity THEN
        SELECT price INTO v_price FROM MENU_ITEM WHERE item_id = NEW.item_id;
        SET NEW.subtotal = v_price * NEW.quantity;
    END IF;
END$$


-- TRIGGER 3: trg_no_negative_qty
-- Blocks invalid quantity on INSERT

CREATE TRIGGER trg_no_negative_qty
BEFORE INSERT ON ORDER_ITEM
FOR EACH ROW
BEGIN
    IF NEW.quantity <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantity must be greater than zero.';
    END IF;
END$$


-- TRIGGER 4: trg_no_negative_salary
-- Blocks salary <= 0 on INSERT or UPDATE

CREATE TRIGGER trg_no_negative_salary_insert
BEFORE INSERT ON STAFF
FOR EACH ROW
BEGIN
    IF NEW.salary <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary must be greater than zero.';
    END IF;
END$$

CREATE TRIGGER trg_no_negative_salary_update
BEFORE UPDATE ON STAFF
FOR EACH ROW
BEGIN
    IF NEW.salary <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary must be greater than zero.';
    END IF;
END$$

-- TRIGGER 5: trg_no_invalid_rating
-- Blocks out-of-range rating score

CREATE TRIGGER trg_no_invalid_rating
BEFORE INSERT ON CUSTOMER_RATING
FOR EACH ROW
BEGIN
    IF NEW.rating_score < 1 OR NEW.rating_score > 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Rating score must be between 1 and 5.';
    END IF;
END$$


-- TRIGGER 6: trg_increment_visit_count
-- After bill is marked Paid → increment customer visit_count

CREATE TRIGGER trg_increment_visit_count
AFTER UPDATE ON BILL
FOR EACH ROW
BEGIN
    DECLARE v_phone VARCHAR(15);

    IF OLD.payment_status != 'Paid' AND NEW.payment_status = 'Paid' THEN
        SELECT customer_phone INTO v_phone
        FROM ORDER_TABLE WHERE order_id = NEW.order_id;

        UPDATE CUSTOMER
        SET visit_count = visit_count + 1
        WHERE phone = v_phone;
    END IF;
END$$


-- TRIGGER 7: trg_whatsapp_optin
-- After bill paid → auto opt-in customer if visit_count >= 3

CREATE TRIGGER trg_whatsapp_optin
AFTER UPDATE ON BILL
FOR EACH ROW
BEGIN
    DECLARE v_phone  VARCHAR(15);
    DECLARE v_visits INT;

    IF OLD.payment_status != 'Paid' AND NEW.payment_status = 'Paid' THEN
        SELECT customer_phone INTO v_phone
        FROM ORDER_TABLE WHERE order_id = NEW.order_id;

        SELECT visit_count INTO v_visits
        FROM CUSTOMER WHERE phone = v_phone;

        -- visit_count already incremented by trigger 6 (fires first alphabetically)
        -- so check >= 3 after increment
        IF v_visits >= 3 AND NOT (SELECT on_whatsapp_list FROM CUSTOMER WHERE phone = v_phone) THEN
            UPDATE CUSTOMER SET on_whatsapp_list = 1 WHERE phone = v_phone;
        END IF;
    END IF;
END$$


-- TRIGGER 8: trg_bill_audit_log
-- Logs every payment status change in BILL_AUDIT_LOG

CREATE TRIGGER trg_bill_audit_log
AFTER UPDATE ON BILL
FOR EACH ROW
BEGIN
    IF OLD.payment_status != NEW.payment_status THEN
        INSERT INTO BILL_AUDIT_LOG (bill_id, old_status, new_status, changed_by_user)
        VALUES (NEW.bill_id, OLD.payment_status, NEW.payment_status, USER());
    END IF;
END$$


-- TRIGGER 9: trg_prevent_double_payment
-- Blocks updating a Paid bill back to Paid

CREATE TRIGGER trg_prevent_double_payment
BEFORE UPDATE ON BILL
FOR EACH ROW
BEGIN
    IF OLD.payment_status = 'Paid' AND NEW.payment_status = 'Paid' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate payment prevented: Bill is already marked as Paid.';
    END IF;
END$$

DELIMITER ;
