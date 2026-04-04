
-- FILE: 02_seed_data.sql 

USE restaurant_db;

-- STAFF
INSERT INTO STAFF (name, role, salary) VALUES
('Ravi Kumar',    'Manager',  75000.00),
('Priya Sharma',  'Waiter',   22000.00),
('Anil Mehta',    'Chef',     45000.00),
('Sneha Patel',   'Cashier',  25000.00),
('Raj Nair',      'Waiter',   22000.00),
('Deepa Singh',   'Host',     20000.00);

-- CUSTOMER
INSERT INTO CUSTOMER (phone, name, visit_count, on_whatsapp_list) VALUES
('9876543210', 'Arjun Reddy',   5, 1),
('9123456789', 'Meena Das',     2, 0),
('9988776655', 'Vikram Bose',   8, 1),
('9871234567', 'Sita Rao',      1, 0),
('9000011111', 'Kiran Kumar',   3, 1),
('9555566666', 'Pooja Menon',   0, 0);

-- MENU_ITEM
INSERT INTO MENU_ITEM (name, category, price, tax_rate) VALUES
('Veg Spring Roll',     'Starter',      120.00, 5.00),
('Paneer Tikka',        'Starter',      220.00, 5.00),
('Butter Chicken',      'Main Course',  320.00, 12.00),
('Dal Makhani',         'Main Course',  240.00, 12.00),
('Garlic Naan',         'Main Course',   50.00, 5.00),
('Gulab Jamun',         'Dessert',       80.00, 5.00),
('Mango Lassi',         'Beverage',      90.00, 5.00),
('Cold Coffee',         'Beverage',     110.00, 5.00),
('Masala Fries',        'Snack',         99.00, 5.00),
('Chicken Biryani',     'Main Course',  380.00, 12.00),
('Chocolate Brownie',   'Dessert',      150.00, 5.00),
('Fresh Lime Soda',     'Beverage',      60.00, 5.00);

-- SHIFT
INSERT INTO SHIFT (staff_id, shift_date, start_time, end_time, attendance_status) VALUES
(1, '2026-03-31', '09:00:00', '17:00:00', 'Present'),
(2, '2026-03-31', '11:00:00', '19:00:00', 'Present'),
(3, '2026-03-31', '10:00:00', '18:00:00', 'Present'),
(4, '2026-03-31', '12:00:00', '20:00:00', 'Late'),
(5, '2026-04-01', '11:00:00', '19:00:00', 'Present'),
(6, '2026-04-01', '09:00:00', '17:00:00', 'Absent'),
(1, '2026-04-01', '09:00:00', '17:00:00', 'Present'),
(2, '2026-04-01', '11:00:00', '19:00:00', 'Half-Day');

-- ORDER_TABLE
INSERT INTO ORDER_TABLE (customer_phone, staff_id, table_no, order_datetime, status) VALUES
('9876543210', 2, 3, '2026-03-31 13:00:00', 'Billed'),
('9123456789', 5, 7, '2026-03-31 14:30:00', 'Billed'),
('9988776655', 2, 1, '2026-04-01 12:00:00', 'Billed'),
('9871234567', 5, 5, '2026-04-01 19:00:00', 'Billed'),
('9000011111', 2, 2, '2026-04-01 20:00:00', 'Open');

-- ORDER_ITEM  (subtotal auto-set by trigger; manual values shown as fallback)
INSERT INTO ORDER_ITEM (order_id, item_id, quantity, subtotal) VALUES
(1, 2, 1, 220.00),
(1, 3, 2, 640.00),
(1, 7, 1,  90.00),
(2, 1, 2, 240.00),
(2, 5, 3, 150.00),
(2, 6, 2, 160.00),
(3, 10,1, 380.00),
(3, 4, 1, 240.00),
(3, 8, 2, 220.00),
(4, 9, 2, 198.00),
(4, 11,1, 150.00),
(5, 3, 1, 320.00),
(5, 5, 2, 100.00);

-- BILL
INSERT INTO BILL (order_id, total_amount, tax_amount, discount_applied, payment_status, generated_at) VALUES
(1, 1056.20, 106.20, 10.00, 'Paid',    '2026-03-31 13:45:00'),
(2,  594.50,  44.50, 0.00,  'Paid',    '2026-03-31 15:00:00'),
(3,  924.80,  84.80, 5.00,  'Paid',    '2026-04-01 12:40:00'),
(4,  381.35,  33.35, 0.00,  'Paid',    '2026-04-01 19:30:00');

-- CUSTOMER_RATING
INSERT INTO CUSTOMER_RATING (staff_id, order_id, rating_score) VALUES
(2, 1, 5),
(5, 2, 4),
(2, 3, 5),
(5, 4, 3);
