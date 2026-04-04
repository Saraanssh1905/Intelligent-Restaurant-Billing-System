
--Intelligent Restaurant Billing & Management System

-- FILE: 01_schema.sql 

CREATE DATABASE IF NOT EXISTS restaurant_db;
USE restaurant_db;


-- 1. CUSTOMER

CREATE TABLE IF NOT EXISTS CUSTOMER (
    phone           VARCHAR(15)     NOT NULL,
    name            VARCHAR(100)    NOT NULL,
    visit_count     INT             NOT NULL DEFAULT 0,
    on_whatsapp_list TINYINT(1)     NOT NULL DEFAULT 0,
    CONSTRAINT pk_customer PRIMARY KEY (phone),
    CONSTRAINT chk_phone   CHECK (phone REGEXP '^[6-9][0-9]{9}$'),
    CONSTRAINT chk_visit   CHECK (visit_count >= 0)
);


-- 2. MENU_ITEM

CREATE TABLE IF NOT EXISTS MENU_ITEM (
    item_id     INT             NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100)    NOT NULL,
    category    ENUM('Starter','Main Course','Dessert','Beverage','Snack') NOT NULL,
    price       DECIMAL(10,2)   NOT NULL,
    tax_rate    DECIMAL(5,2)    NOT NULL DEFAULT 5.00,
    CONSTRAINT pk_menu      PRIMARY KEY (item_id),
    CONSTRAINT chk_price    CHECK (price > 0),
    CONSTRAINT chk_tax      CHECK (tax_rate >= 0 AND tax_rate <= 28)
);


-- 3. STAFF

CREATE TABLE IF NOT EXISTS STAFF (
    staff_id    INT             NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100)    NOT NULL,
    role        ENUM('Manager','Waiter','Chef','Cashier','Host') NOT NULL,
    salary      DECIMAL(10,2)   NOT NULL,
    CONSTRAINT pk_staff     PRIMARY KEY (staff_id),
    CONSTRAINT chk_salary   CHECK (salary > 0)
);


-- 4. SHIFT

CREATE TABLE IF NOT EXISTS SHIFT (
    shift_id            INT             NOT NULL AUTO_INCREMENT,
    staff_id            INT             NOT NULL,
    shift_date          DATE            NOT NULL,
    start_time          TIME            NOT NULL,
    end_time            TIME            NOT NULL,
    attendance_status   ENUM('Present','Absent','Late','Half-Day') NOT NULL DEFAULT 'Present',
    CONSTRAINT pk_shift     PRIMARY KEY (shift_id),
    CONSTRAINT fk_shift_staff FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id) ON DELETE CASCADE,
    CONSTRAINT chk_shift_time CHECK (end_time > start_time)
);


-- 5. ORDER_TABLE

CREATE TABLE IF NOT EXISTS ORDER_TABLE (
    order_id        INT             NOT NULL AUTO_INCREMENT,
    customer_phone  VARCHAR(15)     NOT NULL,
    staff_id        INT             NOT NULL,
    table_no        INT             NOT NULL,
    order_datetime  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status          ENUM('Open','Ready','Billed','Cancelled') NOT NULL DEFAULT 'Open',
    CONSTRAINT pk_order     PRIMARY KEY (order_id),
    CONSTRAINT fk_order_cust FOREIGN KEY (customer_phone) REFERENCES CUSTOMER(phone),
    CONSTRAINT fk_order_staff FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id),
    CONSTRAINT chk_table    CHECK (table_no > 0)
);


-- 6. ORDER_ITEM

CREATE TABLE IF NOT EXISTS ORDER_ITEM (
    order_id    INT             NOT NULL,
    item_id     INT             NOT NULL,
    quantity    INT             NOT NULL,
    subtotal    DECIMAL(10,2)   NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_order_item PRIMARY KEY (order_id, item_id),
    CONSTRAINT fk_oi_order  FOREIGN KEY (order_id) REFERENCES ORDER_TABLE(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_oi_item   FOREIGN KEY (item_id)  REFERENCES MENU_ITEM(item_id),
    CONSTRAINT chk_qty      CHECK (quantity > 0)
);


-- 7. BILL

CREATE TABLE IF NOT EXISTS BILL (
    bill_id         INT             NOT NULL AUTO_INCREMENT,
    order_id        INT             NOT NULL UNIQUE,
    total_amount    DECIMAL(10,2)   NOT NULL,
    tax_amount      DECIMAL(10,2)   NOT NULL DEFAULT 0.00,
    discount_applied DECIMAL(5,2)  NOT NULL DEFAULT 0.00,
    payment_status  ENUM('Pending','Paid','Refunded') NOT NULL DEFAULT 'Pending',
    generated_at    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_bill      PRIMARY KEY (bill_id),
    CONSTRAINT fk_bill_order FOREIGN KEY (order_id) REFERENCES ORDER_TABLE(order_id),
    CONSTRAINT chk_total    CHECK (total_amount >= 0),
    CONSTRAINT chk_discount CHECK (discount_applied >= 0 AND discount_applied <= 100)
);


-- 8. CUSTOMER_RATING

CREATE TABLE IF NOT EXISTS CUSTOMER_RATING (
    rating_id   INT NOT NULL AUTO_INCREMENT,
    staff_id    INT NOT NULL,
    order_id    INT NOT NULL,
    rating_score TINYINT NOT NULL,
    CONSTRAINT pk_rating    PRIMARY KEY (rating_id),
    CONSTRAINT fk_rating_staff FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id),
    CONSTRAINT fk_rating_order FOREIGN KEY (order_id) REFERENCES ORDER_TABLE(order_id),
    CONSTRAINT chk_score    CHECK (rating_score BETWEEN 1 AND 5),
    CONSTRAINT uq_order_rating UNIQUE (order_id)   -- one rating per order
);


-- 9. BILL_AUDIT_LOG  (for trigger demo)

CREATE TABLE IF NOT EXISTS BILL_AUDIT_LOG (
    log_id          INT             NOT NULL AUTO_INCREMENT,
    bill_id         INT             NOT NULL,
    old_status      VARCHAR(20),
    new_status      VARCHAR(20),
    changed_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by_user VARCHAR(100),
    CONSTRAINT pk_log PRIMARY KEY (log_id)
);


-- INDEXES  (for fast bill search)

CREATE INDEX idx_bill_date       ON BILL(generated_at);
CREATE INDEX idx_order_phone     ON ORDER_TABLE(customer_phone);
CREATE INDEX idx_order_staff     ON ORDER_TABLE(staff_id);
CREATE INDEX idx_shift_date      ON SHIFT(shift_date);
CREATE INDEX idx_shift_staff     ON SHIFT(staff_id);
