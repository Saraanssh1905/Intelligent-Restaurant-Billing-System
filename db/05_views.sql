
-- FILE: 05_views.sql  
-- Reporting views for GUI analytics screens

USE restaurant_db;


-- Daily Sales Summary

CREATE OR REPLACE VIEW v_daily_sales AS
SELECT
    DATE(b.generated_at)             AS sale_date,
    COUNT(b.bill_id)                 AS total_bills,
    SUM(b.total_amount)              AS total_revenue,
    SUM(b.tax_amount)                AS total_tax,
    AVG(b.total_amount)              AS avg_bill_value
FROM BILL b
WHERE b.payment_status = 'Paid'
GROUP BY DATE(b.generated_at)
ORDER BY sale_date DESC;


-- Monthly Revenue

CREATE OR REPLACE VIEW v_monthly_revenue AS
SELECT
    YEAR(b.generated_at)             AS year,
    MONTH(b.generated_at)            AS month,
    MONTHNAME(b.generated_at)        AS month_name,
    COUNT(b.bill_id)                 AS total_bills,
    SUM(b.total_amount)              AS total_revenue
FROM BILL b
WHERE b.payment_status = 'Paid'
GROUP BY YEAR(b.generated_at), MONTH(b.generated_at), MONTHNAME(b.generated_at)
ORDER BY year DESC, month DESC;


-- Top Staff (by rating + orders)

CREATE OR REPLACE VIEW v_top_staff AS
SELECT
    s.staff_id,
    s.name                                    AS staff_name,
    s.role,
    COUNT(DISTINCT o.order_id)                AS orders_served,
    COALESCE(ROUND(AVG(cr.rating_score),2),0) AS avg_rating,
    COALESCE(SUM(b.total_amount),0)           AS revenue_generated
FROM STAFF s
LEFT JOIN ORDER_TABLE o  ON s.staff_id = o.staff_id
LEFT JOIN BILL b         ON o.order_id = b.order_id AND b.payment_status = 'Paid'
LEFT JOIN CUSTOMER_RATING cr ON cr.staff_id = s.staff_id
GROUP BY s.staff_id, s.name, s.role
ORDER BY avg_rating DESC, orders_served DESC;


-- Frequent Customers

CREATE OR REPLACE VIEW v_frequent_customers AS
SELECT
    c.phone,
    c.name,
    c.visit_count,
    c.on_whatsapp_list,
    fn_calculate_discount(c.phone) AS loyalty_discount_pct,
    COALESCE(SUM(b.total_amount),0) AS total_spent
FROM CUSTOMER c
LEFT JOIN ORDER_TABLE o ON c.phone = o.customer_phone
LEFT JOIN BILL b        ON o.order_id = b.order_id AND b.payment_status = 'Paid'
GROUP BY c.phone, c.name, c.visit_count, c.on_whatsapp_list
ORDER BY c.visit_count DESC;


-- Low Selling Items (0 or 1 orders)

CREATE OR REPLACE VIEW v_low_selling_items AS
SELECT
    mi.item_id,
    mi.name,
    mi.category,
    mi.price,
    COALESCE(COUNT(oi.order_id), 0) AS times_ordered,
    COALESCE(SUM(oi.quantity), 0)   AS total_qty_sold
FROM MENU_ITEM mi
LEFT JOIN ORDER_ITEM oi ON mi.item_id = oi.item_id
GROUP BY mi.item_id, mi.name, mi.category, mi.price
HAVING times_ordered <= 1
ORDER BY times_ordered ASC;


-- Shift Attendance Summary

CREATE OR REPLACE VIEW v_shift_attendance AS
SELECT
    s.name             AS staff_name,
    s.role,
    sh.shift_date,
    sh.start_time,
    sh.end_time,
    sh.attendance_status,
    TIMEDIFF(sh.end_time, sh.start_time) AS hours_worked
FROM SHIFT sh
JOIN STAFF s ON sh.staff_id = s.staff_id
ORDER BY sh.shift_date DESC, s.name;


-- WhatsApp Opt-In List

CREATE OR REPLACE VIEW v_whatsapp_customers AS
SELECT phone, name, visit_count
FROM CUSTOMER
WHERE on_whatsapp_list = 1
ORDER BY visit_count DESC;


-- Full Bill History (for search screen)

CREATE OR REPLACE VIEW v_bill_history AS
SELECT
    b.bill_id,
    b.generated_at,
    b.total_amount,
    b.tax_amount,
    b.discount_applied,
    b.payment_status,
    o.order_id,
    o.table_no,
    o.order_datetime,
    c.name           AS customer_name,
    c.phone          AS customer_phone,
    st.name          AS staff_name,
    st.role          AS staff_role
FROM BILL b
JOIN ORDER_TABLE o  ON b.order_id = o.order_id
JOIN CUSTOMER c     ON o.customer_phone = c.phone
JOIN STAFF st       ON o.staff_id = st.staff_id
ORDER BY b.generated_at DESC;
