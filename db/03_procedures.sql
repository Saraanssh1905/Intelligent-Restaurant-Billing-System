
-- FILE: 03_procedures.sql  

USE restaurant_db;

DELIMITER $$


-- FUNCTION: fn_calculate_discount(phone)
-- Returns discount % based on visit count

CREATE FUNCTION fn_calculate_discount(p_phone VARCHAR(15))
RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_visits INT DEFAULT 0;
    DECLARE v_discount DECIMAL(5,2) DEFAULT 0.00;

    SELECT visit_count INTO v_visits
    FROM CUSTOMER WHERE phone = p_phone;

    IF v_visits >= 10 THEN SET v_discount = 15.00;
    ELSEIF v_visits >= 5 THEN SET v_discount = 10.00;
    ELSEIF v_visits >= 3 THEN SET v_discount = 5.00;
    ELSE SET v_discount = 0.00;
    END IF;

    RETURN v_discount;
END$$


-- FUNCTION: fn_get_order_subtotal(order_id)
-- Computes raw item total for an order

CREATE FUNCTION fn_get_order_subtotal(p_order_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total DECIMAL(10,2) DEFAULT 0.00;
    SELECT COALESCE(SUM(subtotal), 0) INTO v_total
    FROM ORDER_ITEM WHERE order_id = p_order_id;
    RETURN v_total;
END$$


-- PROCEDURE: sp_create_order
-- Creates a new order; inserts customer if not exists

CREATE PROCEDURE sp_create_order(
    IN  p_phone     VARCHAR(15),
    IN  p_cname     VARCHAR(100),
    IN  p_staff_id  INT,
    IN  p_table_no  INT,
    OUT p_order_id  INT,
    OUT p_message   VARCHAR(200)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_order_id = -1;
        SET p_message  = 'ERROR: Order creation failed. Transaction rolled back.';
    END;

    START TRANSACTION;

    -- Insert customer if not exists
    INSERT IGNORE INTO CUSTOMER (phone, name) VALUES (p_phone, p_cname);

    -- Validate staff
    IF NOT EXISTS (SELECT 1 FROM STAFF WHERE staff_id = p_staff_id) THEN
        SET p_order_id = -1;
        SET p_message  = 'ERROR: Staff ID not found.';
        ROLLBACK;
    ELSE
        INSERT INTO ORDER_TABLE (customer_phone, staff_id, table_no)
        VALUES (p_phone, p_staff_id, p_table_no);

        SET p_order_id = LAST_INSERT_ID();
        SET p_message  = CONCAT('Order #', p_order_id, ' created successfully.');
        COMMIT;
    END IF;
END$$


-- PROCEDURE: sp_add_order_item
-- Adds an item to an open order (trigger sets subtotal)

CREATE PROCEDURE sp_add_order_item(
    IN  p_order_id  INT,
    IN  p_item_id   INT,
    IN  p_quantity  INT,
    OUT p_message   VARCHAR(200)
)
BEGIN
    DECLARE v_status VARCHAR(20);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_message = 'ERROR: Could not add item.';
    END;

    SELECT status INTO v_status FROM ORDER_TABLE WHERE order_id = p_order_id;

    IF v_status != 'Open' THEN
        SET p_message = 'ERROR: Cannot add items to a non-Open order.';
    ELSEIF p_quantity <= 0 THEN
        SET p_message = 'ERROR: Quantity must be positive.';
    ELSE
        INSERT INTO ORDER_ITEM (order_id, item_id, quantity, subtotal)
        VALUES (p_order_id, p_item_id, p_quantity, 0.00)
        ON DUPLICATE KEY UPDATE quantity = quantity + p_quantity;
        -- subtotal recalculated by trigger
        SET p_message = 'Item added successfully.';
    END IF;
END$$


-- PROCEDURE: sp_generate_bill
-- Generates bill with tax + loyalty discount

CREATE PROCEDURE sp_generate_bill(
    IN  p_order_id  INT,
    OUT p_bill_id   INT,
    OUT p_message   VARCHAR(200)
)
BEGIN
    DECLARE v_subtotal    DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_tax         DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_discount    DECIMAL(5,2)  DEFAULT 0.00;
    DECLARE v_final       DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_phone       VARCHAR(15);
    DECLARE v_status      VARCHAR(20);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_bill_id = -1;
        SET p_message = 'ERROR: Bill generation failed. Rolled back.';
    END;

    -- Prevent duplicate billing
    IF EXISTS (SELECT 1 FROM BILL WHERE order_id = p_order_id) THEN
        SET p_bill_id = -1;
        SET p_message = 'ERROR: Bill already exists for this order.';
    ELSE
        START TRANSACTION;

        SELECT customer_phone, status INTO v_phone, v_status
        FROM ORDER_TABLE WHERE order_id = p_order_id;

        IF v_status = 'Cancelled' THEN
            SET p_bill_id = -1;
            SET p_message = 'ERROR: Cannot bill a cancelled order.';
            ROLLBACK;
        ELSE
            -- Calculate per-item tax properly
            SELECT
                COALESCE(SUM(oi.subtotal), 0),
                COALESCE(SUM(oi.subtotal * mi.tax_rate / 100), 0)
            INTO v_subtotal, v_tax
            FROM ORDER_ITEM oi
            JOIN MENU_ITEM mi ON oi.item_id = mi.item_id
            WHERE oi.order_id = p_order_id;

            SET v_discount = fn_calculate_discount(v_phone);
            SET v_final    = (v_subtotal + v_tax) * (1 - v_discount / 100);

            INSERT INTO BILL (order_id, total_amount, tax_amount, discount_applied)
            VALUES (p_order_id, v_final, v_tax, v_discount);

            SET p_bill_id = LAST_INSERT_ID();

            UPDATE ORDER_TABLE SET status = 'Billed' WHERE order_id = p_order_id;

            SET p_message = CONCAT('Bill #', p_bill_id, ' generated. Discount: ', v_discount, '%. Total: ₹', v_final);
            COMMIT;
        END IF;
    END IF;
END$$


-- PROCEDURE: sp_update_payment
-- Marks bill as Paid / Refunded; validates no re-payment

CREATE PROCEDURE sp_update_payment(
    IN  p_bill_id    INT,
    IN  p_new_status VARCHAR(10),
    OUT p_message    VARCHAR(200)
)
BEGIN
    DECLARE v_current VARCHAR(20);

    SELECT payment_status INTO v_current FROM BILL WHERE bill_id = p_bill_id;

    IF v_current = 'Paid' AND p_new_status = 'Paid' THEN
        SET p_message = 'ERROR: Payment already recorded. Duplicate prevented.';
    ELSEIF v_current IS NULL THEN
        SET p_message = 'ERROR: Bill not found.';
    ELSE
        UPDATE BILL SET payment_status = p_new_status WHERE bill_id = p_bill_id;
        SET p_message = CONCAT('Bill #', p_bill_id, ' status updated to ', p_new_status);
    END IF;
END$$


-- PROCEDURE: sp_search_bills
-- Flexible search by date / phone / staff (all optional)

CREATE PROCEDURE sp_search_bills(
    IN p_date     DATE,
    IN p_phone    VARCHAR(15),
    IN p_staff_id INT
)
BEGIN
    SELECT
        b.bill_id,
        b.generated_at,
        b.total_amount,
        b.tax_amount,
        b.discount_applied,
        b.payment_status,
        o.order_id,
        o.table_no,
        c.name   AS customer_name,
        c.phone  AS customer_phone,
        s.name   AS staff_name
    FROM BILL b
    JOIN ORDER_TABLE o ON b.order_id = o.order_id
    JOIN CUSTOMER c    ON o.customer_phone = c.phone
    JOIN STAFF s       ON o.staff_id = s.staff_id
    WHERE
        (p_date     IS NULL OR DATE(b.generated_at) = p_date)
        AND (p_phone    IS NULL OR c.phone = p_phone)
        AND (p_staff_id IS NULL OR o.staff_id = p_staff_id)
    ORDER BY b.generated_at DESC;
END$$


-- PROCEDURE: sp_get_top_staff
-- Average rating + orders served per staff for a month/year

CREATE PROCEDURE sp_get_top_staff(
    IN p_month INT,
    IN p_year  INT
)
BEGIN
    SELECT
        s.staff_id,
        s.name,
        s.role,
        COUNT(DISTINCT o.order_id)            AS orders_served,
        COALESCE(AVG(cr.rating_score), 0)     AS avg_rating,
        SUM(b.total_amount)                   AS total_revenue_generated
    FROM STAFF s
    LEFT JOIN ORDER_TABLE o  ON s.staff_id = o.staff_id
              AND MONTH(o.order_datetime) = p_month
              AND YEAR(o.order_datetime)  = p_year
    LEFT JOIN BILL b         ON o.order_id = b.order_id AND b.payment_status = 'Paid'
    LEFT JOIN CUSTOMER_RATING cr ON cr.staff_id = s.staff_id AND cr.order_id = o.order_id
    GROUP BY s.staff_id, s.name, s.role
    ORDER BY avg_rating DESC, orders_served DESC;
END$$


-- PROCEDURE: sp_calculate_staff_performance
-- Single staff performance summary

CREATE PROCEDURE sp_calculate_staff_performance(IN p_staff_id INT)
BEGIN
    SELECT
        s.name,
        s.role,
        COUNT(DISTINCT o.order_id)         AS total_orders,
        COALESCE(AVG(cr.rating_score), 0)  AS avg_rating,
        SUM(b.total_amount)                AS total_revenue,
        COUNT(DISTINCT sh.shift_id)        AS shifts_worked,
        SUM(sh.attendance_status = 'Present') AS days_present
    FROM STAFF s
    LEFT JOIN ORDER_TABLE o  ON s.staff_id = o.staff_id
    LEFT JOIN BILL b         ON o.order_id = b.order_id AND b.payment_status = 'Paid'
    LEFT JOIN CUSTOMER_RATING cr ON cr.staff_id = s.staff_id
    LEFT JOIN SHIFT sh       ON sh.staff_id = s.staff_id
    WHERE s.staff_id = p_staff_id
    GROUP BY s.name, s.role;
END$$

DELIMITER ;
