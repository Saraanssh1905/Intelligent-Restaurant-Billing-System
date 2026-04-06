<br/>
<div align="center">

# MANIPAL INSTITUTE OF TECHNOLOGY
### (A Constituent Institution of Manipal Academy of Higher Education)

**Department of Computer Science and Engineering**

---

## DATABASE SYSTEMS LAB — MINI PROJECT REPORT

### **Intelligent Restaurant Billing & Management System**

---

**Submitted in partial fulfillment of the requirements for the degree of**
**Bachelor of Technology (B.Tech) in Computer Science and Engineering**

---

| | |
|---|---|
| **Subject** | Database Systems Lab (CSE 2272) |
| **Semester** | IV |
| **Section** | __________ |

---

| **Name** | **Roll Number** | **Registration Number** |
|:---:|:---:|:---:|
| _Student Name 1_ | _Roll No. 1_ | _Reg. No. 1_ |
| _Student Name 2_ | _Roll No. 2_ | _Reg. No. 2_ |

---

**Faculty Guide:** _Prof. _______________

**Date of Submission:** April 2026

</div>

---

<div align="center">

# CERTIFICATE

</div>

This is to certify that the mini project entitled **"Intelligent Restaurant Billing & Management System"** is a bonafide work carried out by the above-mentioned students in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science and Engineering at Manipal Institute of Technology, Manipal Academy of Higher Education, during the academic year 2025–2026.

This project has been completed under the guidance of the Department of Computer Science and Engineering and has been found satisfactory. The work presented in this report is original and has not been submitted elsewhere for the award of any other degree or diploma.

<br/>

| | |
|---|---|
| **Signature of Faculty Guide** | **Signature of HOD** |
| Prof. _______________ | Dr. _______________ |
| Department of CSE | Department of CSE |
| MIT, Manipal | MIT, Manipal |

**Date:** April 2026 &emsp;&emsp;&emsp; **Place:** Manipal

---

<div align="center">

# TABLE OF CONTENTS

</div>

| Chapter | Title | Page |
|:---:|---|:---:|
| | Certificate | ii |
| | Table of Contents | iii |
| | List of Figures | iv |
| 1 | Introduction | 1 |
| 1.1 | Problem Domain | 1 |
| 1.2 | Need for Database Systems | 2 |
| 1.3 | Limitations of Existing Systems | 2 |
| 1.4 | Proposed Solution | 3 |
| 2 | Problem Statement and Objectives | 4 |
| 2.1 | Problem Statement | 4 |
| 2.2 | Existing Challenges | 4 |
| 2.3 | Project Objectives | 5 |
| 3 | Methodology | 6 |
| 3.1 | Schema Design Approach | 6 |
| 3.2 | Normalization | 7 |
| 3.3 | Frontend–Backend Architecture | 8 |
| 3.4 | Trigger-Based Automation | 8 |
| 3.5 | Stored Procedures and Functions | 9 |
| 3.6 | User Workflow | 9 |
| 4 | ER Diagram and Relational Tables | 10 |
| 4.1 | Entity–Relationship Model | 10 |
| 4.2 | Relational Schema | 11 |
| 4.3 | Sample Data | 13 |
| 5 | SQL Implementation | 14 |
| 5.1 | Table Creation | 14 |
| 5.2 | Indexes | 15 |
| 5.3 | Triggers | 16 |
| 5.4 | Stored Procedures | 17 |
| 5.5 | Functions | 19 |
| 5.6 | Views | 19 |
| 5.7 | Reporting Queries | 20 |
| 6 | Results and Snapshots | 21 |
| 7 | Conclusion, Limitations and Future Work | 23 |
| 8 | References | 25 |

---

<div align="center">

# LIST OF FIGURES

</div>

| Figure | Description | Page |
|:---:|---|:---:|
| Fig 1 | Login Screen | 21 |
| Fig 2 | Dashboard with Sidebar Navigation | 21 |
| Fig 3 | New Order Creation | 21 |
| Fig 4 | Bill Generation with Loyalty Discount | 21 |
| Fig 5 | Trigger Execution — Auto Subtotal | 22 |
| Fig 6 | Bill Audit Log | 22 |
| Fig 7 | Analytics Dashboard — Daily Sales | 22 |
| Fig 8 | Customer Loyalty & WhatsApp Opt-In | 22 |
| Fig 9 | Staff Performance Report | 22 |
| Fig 10 | Bill Search with Filters | 22 |
| Fig 11 | Error Handling — Duplicate Payment | 23 |
| Fig 12 | Data Integrity — CHECK Constraint | 23 |

---

# CHAPTER 1: INTRODUCTION

## 1.1 Problem Domain

The restaurant industry is a high-throughput, operationally intensive domain where multiple concurrent processes—order placement, billing, inventory awareness, staff scheduling, and customer relationship management—must operate in unison with minimal latency. A mid-scale restaurant typically handles 100–300 orders per day, each involving menu lookups, tax computation, discount application, and payment reconciliation. Managing these workflows manually or through flat-file systems introduces computational overhead, data redundancy, and a significant risk of human error.

The **Intelligent Restaurant Billing & Management System** addresses these challenges by implementing a fully normalized relational database backend (MySQL 8.x) coupled with a rich graphical user interface (Python CustomTkinter) that together automate the end-to-end lifecycle of restaurant operations—from customer walk-in to payment settlement and post-service analytics.

## 1.2 Need for Database Systems

Traditional paper-based or spreadsheet-driven restaurant management approaches suffer from several critical deficiencies:

- **Data Redundancy:** Customer information, menu prices, and staff details are replicated across multiple ledgers, leading to inconsistencies when updates are not propagated uniformly.
- **Lack of Referential Integrity:** In file-based systems, there is no mechanism to enforce that an order references a valid customer or that a bill references a valid order, resulting in orphan records.
- **No Concurrency Control:** Multiple waiters simultaneously adding items to orders can lead to lost updates when flat files are used.
- **Absence of Atomicity:** Bill generation—which involves reading order items, computing tax, applying discounts, and inserting a bill record—must succeed or fail as a single unit. File-based systems offer no transactional guarantees.
- **Limited Querying Capability:** Generating reports such as "top-selling items this month" or "staff with highest average ratings" requires complex programmatic iteration over raw files rather than declarative SQL queries.

A Relational Database Management System (RDBMS) solves all of these problems through ACID-compliant transactions, declarative query processing, constraint enforcement, and trigger-based automation.

## 1.3 Limitations of Existing Systems

Existing small-scale restaurant management solutions often exhibit the following shortcomings:

1. **No Loyalty Tracking:** Customer visit counts and tiered discount programs are not tracked, leading to missed retention opportunities.
2. **Manual Tax Computation:** Per-item tax rates (GST slabs of 5%, 12%, 18%) are computed manually, introducing calculation errors.
3. **No Audit Trail:** Payment status changes are not logged, making dispute resolution difficult.
4. **Static Staffing Reports:** Staff performance metrics (orders served, average customer rating, attendance) are not aggregated automatically.
5. **No Duplicate Payment Prevention:** Without database-level enforcement, a bill may be marked "Paid" multiple times, causing revenue accounting discrepancies.

## 1.4 Proposed Solution

This project implements a **9-table normalized relational schema** with:
- **9 triggers** for automated subtotal calculation, data validation, audit logging, loyalty tracking, and duplicate prevention
- **6 stored procedures** with IN/OUT parameters and transaction management for atomic order-to-bill workflows
- **2 user-defined functions** for discount computation and order subtotal aggregation
- **8 reporting views** for real-time analytics without application-layer computation
- A **Python CustomTkinter GUI** with role-based login, 7 functional screens, and full CRUD capabilities interfacing with the MySQL backend via the `mysql-connector-python` driver

---

# CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES

## 2.1 Problem Statement

Design and implement a relational database system for an intelligent restaurant billing and management platform that automates the complete order-to-payment lifecycle, enforces data integrity through constraints and triggers, provides real-time analytics through views, and offers a graphical user interface for operational staff.

## 2.2 Existing Challenges

The following challenges are observed in conventional restaurant operations:

1. **Order–Bill Integrity Gap:** Orders and their corresponding bills are tracked independently, with no foreign-key linkage guaranteeing one-to-one correspondence.
2. **Tax Rate Inconsistency:** Different food categories attract different GST slabs (5% for beverages, 12% for main courses), and manual computation leads to under-billing or over-billing.
3. **Normalization Deficiency:** Unnormalized schemas store redundant customer and menu information within each order record, inflating storage requirements and complicating updates.
4. **Absence of Role-Based Access:** Waiters, cashiers, and managers have identical access levels, creating security and operational risks.
5. **No Automated Loyalty Program:** Visit-count-based discount tiers require manual tracking, leading to inconsistent customer experiences.
6. **Reporting Latency:** Generating end-of-day sales summaries or monthly revenue reports requires manual SQL execution rather than pre-computed views.
7. **Staff Performance Opacity:** Correlating orders served, customer ratings, shift attendance, and revenue generated per staff member is not feasible without dedicated analytical queries.

## 2.3 Project Objectives

1. Design a **normalized relational schema in Third Normal Form (3NF)** comprising 9 interrelated tables with appropriate primary keys, foreign keys, CHECK constraints, and UNIQUE constraints.
2. Implement **9 database triggers** covering subtotal auto-calculation, data validation, audit logging, loyalty visit-count increment, WhatsApp opt-in automation, and duplicate payment prevention.
3. Develop **6 stored procedures** with IN/OUT parameters supporting transactional order creation, item addition, bill generation, payment processing, bill search, and staff performance analysis.
4. Create **2 user-defined functions** for visit-count-based discount calculation and order subtotal aggregation.
5. Build **8 reporting views** for daily sales, monthly revenue, top staff, frequent customers, low-selling items, shift attendance, WhatsApp subscriber lists, and bill history.
6. Implement a **role-based login system** where authentication is performed against the STAFF table, and the user interface adapts based on the staff member's role.
7. Develop a **Python CustomTkinter GUI** with 7 screens (Order, Billing, Menu, Customers, Staff & Shifts, Analytics, Bill Search) connected to the MySQL backend.
8. Enforce **data integrity** through CHECK constraints (phone format validation, non-negative quantities, rating range 1–5, salary > 0) and trigger-based SIGNAL statements.
9. Establish **performance indexing** on high-cardinality search columns (bill date, customer phone, staff ID, shift date) to optimize query execution plans.
10. Provide a **complete audit trail** via the BILL_AUDIT_LOG table, populated automatically by triggers upon any payment status change.

---

# CHAPTER 3: METHODOLOGY

## 3.1 Schema Design Approach

The database schema was designed using a **top-down entity identification** approach:

1. **Core Entities Identified:** CUSTOMER, MENU_ITEM, STAFF, ORDER_TABLE, ORDER_ITEM, BILL
2. **Support Entities Added:** SHIFT (staff scheduling), CUSTOMER_RATING (service feedback), BILL_AUDIT_LOG (change tracking)
3. **Relationship Mapping:** Each entity's relationships were mapped with appropriate cardinality constraints:
   - One CUSTOMER → Many ORDERS (1:N)
   - One STAFF → Many ORDERS (1:N)
   - One ORDER → Many ORDER_ITEMS (1:N, composite PK)
   - One ORDER → One BILL (1:1, enforced via UNIQUE constraint on `order_id`)
   - One STAFF → Many SHIFTS (1:N)
   - One STAFF → Many RATINGS (1:N)

## 3.2 Normalization

The schema adheres to **Third Normal Form (3NF)**:

**First Normal Form (1NF):** All attributes contain atomic values. The MENU_ITEM category uses an ENUM type ensuring a single categorical value per row. Multi-valued attributes (e.g., order items) are decomposed into the separate ORDER_ITEM table.

**Second Normal Form (2NF):** All non-key attributes are fully functionally dependent on the entire primary key. In ORDER_ITEM (composite PK: `order_id, item_id`), `quantity` and `subtotal` depend on both components of the key, not on either individually.

**Third Normal Form (3NF):** There are no transitive dependencies. For example, in ORDER_TABLE, `customer_phone` references the CUSTOMER table rather than storing the customer's name redundantly. Similarly, `staff_id` references STAFF rather than duplicating staff details within each order.

## 3.3 Frontend–Backend Architecture

The system follows a **three-tier architecture**:

| Layer | Technology | Responsibility |
|---|---|---|
| **Presentation** | Python CustomTkinter | 7 GUI screens with dark theme, form validation |
| **Business Logic** | Python service modules | 5 service modules mediating between UI and database |
| **Data** | MySQL 8.x | Schema, constraints, triggers, procedures, views |

The `db_connection.py` module acts as the **Data Access Layer (DAL)**, providing three core functions:
- `execute_query()` — for direct SQL statements (SELECT, INSERT, UPDATE)
- `call_procedure()` — for stored procedures returning result sets
- `call_procedure_with_out()` — for procedures with OUT parameters using session variables
- `Transaction` — a context manager for explicit multi-statement transactions with automatic commit/rollback

## 3.4 Trigger-Based Automation

Nine triggers automate critical business rules at the database level, ensuring enforcement regardless of the client application:

| # | Trigger Name | Event | Purpose |
|---|---|---|---|
| 1 | `trg_auto_subtotal` | BEFORE INSERT on ORDER_ITEM | Computes `subtotal = price × quantity` |
| 2 | `trg_recalc_subtotal_on_update` | BEFORE UPDATE on ORDER_ITEM | Recomputes subtotal when quantity changes |
| 3 | `trg_no_negative_qty` | BEFORE INSERT on ORDER_ITEM | Blocks quantity ≤ 0 via SIGNAL |
| 4 | `trg_no_negative_salary_insert` | BEFORE INSERT on STAFF | Blocks salary ≤ 0 |
| 5 | `trg_no_negative_salary_update` | BEFORE UPDATE on STAFF | Blocks salary ≤ 0 |
| 6 | `trg_no_invalid_rating` | BEFORE INSERT on CUSTOMER_RATING | Enforces rating ∈ [1, 5] |
| 7 | `trg_increment_visit_count` | AFTER UPDATE on BILL | Increments customer visit count on payment |
| 8 | `trg_whatsapp_optin` | AFTER UPDATE on BILL | Auto opts-in customer to WhatsApp list after 3 visits |
| 9 | `trg_bill_audit_log` | AFTER UPDATE on BILL | Logs payment status changes |
| 10 | `trg_prevent_double_payment` | BEFORE UPDATE on BILL | Blocks duplicate "Paid" transitions |

## 3.5 Stored Procedures and Functions

**Stored Procedures:**

| Procedure | Parameters | Description |
|---|---|---|
| `sp_create_order` | IN: phone, name, staff_id, table_no; OUT: order_id, message | Atomic order creation with customer auto-insert |
| `sp_add_order_item` | IN: order_id, item_id, qty; OUT: message | Adds item with status check |
| `sp_generate_bill` | IN: order_id; OUT: bill_id, message | Computes tax + discount, generates bill |
| `sp_update_payment` | IN: bill_id, status; OUT: message | Updates payment status with validation |
| `sp_search_bills` | IN: date, phone, staff_id | Flexible bill search with optional filters |
| `sp_get_top_staff` | IN: month, year | Ranks staff by rating and orders served |
| `sp_calculate_staff_performance` | IN: staff_id | Comprehensive single-staff performance summary |

**User-Defined Functions:**

| Function | Returns | Description |
|---|---|---|
| `fn_calculate_discount(phone)` | DECIMAL(5,2) | Returns tiered discount %: 15% (≥10 visits), 10% (≥5), 5% (≥3), 0% (else) |
| `fn_get_order_subtotal(order_id)` | DECIMAL(10,2) | Returns SUM of order item subtotals |

## 3.6 User Workflow

The end-to-end user workflow proceeds as follows:

1. **Login:** Staff member authenticates via Staff ID and password (first name).
2. **Order Creation:** Waiter selects customer phone, table number → `sp_create_order` creates order and auto-inserts new customer.
3. **Item Addition:** Waiter adds menu items → `sp_add_order_item` validates order status and inserts items; `trg_auto_subtotal` computes subtotal.
4. **Bill Generation:** Cashier generates bill → `sp_generate_bill` computes per-item tax, applies `fn_calculate_discount`, inserts bill atomically.
5. **Payment:** Cashier marks bill as Paid → `sp_update_payment` validates; `trg_increment_visit_count` updates loyalty; `trg_whatsapp_optin` auto-enrolls; `trg_bill_audit_log` records change.
6. **Analytics:** Manager views daily sales, monthly revenue, top staff, frequent customers via precomputed views.

---

# CHAPTER 4: ER DIAGRAM AND RELATIONAL TABLES

## 4.1 Entity–Relationship Model

The ER diagram for the Intelligent Restaurant Billing & Management System consists of **9 entities** with the following relationships:

### Entities and Their Key Attributes

| Entity | Primary Key | Key Attributes |
|---|---|---|
| **CUSTOMER** | phone (VARCHAR 15) | name, visit_count, on_whatsapp_list |
| **MENU_ITEM** | item_id (INT, AUTO_INCREMENT) | name, category (ENUM), price, tax_rate |
| **STAFF** | staff_id (INT, AUTO_INCREMENT) | name, role (ENUM), salary |
| **SHIFT** | shift_id (INT, AUTO_INCREMENT) | staff_id (FK), shift_date, start_time, end_time, attendance_status |
| **ORDER_TABLE** | order_id (INT, AUTO_INCREMENT) | customer_phone (FK), staff_id (FK), table_no, order_datetime, status |
| **ORDER_ITEM** | (order_id, item_id) — Composite | quantity, subtotal |
| **BILL** | bill_id (INT, AUTO_INCREMENT) | order_id (FK, UNIQUE), total_amount, tax_amount, discount_applied, payment_status |
| **CUSTOMER_RATING** | rating_id (INT, AUTO_INCREMENT) | staff_id (FK), order_id (FK, UNIQUE), rating_score |
| **BILL_AUDIT_LOG** | log_id (INT, AUTO_INCREMENT) | bill_id, old_status, new_status, changed_at, changed_by_user |

### Relationships and Cardinalities

```
CUSTOMER (1) ──────── (N) ORDER_TABLE
STAFF    (1) ──────── (N) ORDER_TABLE
STAFF    (1) ──────── (N) SHIFT
STAFF    (1) ──────── (N) CUSTOMER_RATING
ORDER_TABLE (1) ───── (N) ORDER_ITEM
MENU_ITEM   (1) ───── (N) ORDER_ITEM
ORDER_TABLE (1) ───── (1) BILL           [UNIQUE on order_id]
ORDER_TABLE (1) ───── (1) CUSTOMER_RATING [UNIQUE on order_id]
BILL        (1) ───── (N) BILL_AUDIT_LOG
```

## 4.2 Relational Schema with Constraints

### Table: CUSTOMER
| Column | Type | Constraints |
|---|---|---|
| phone | VARCHAR(15) | **PK**, CHECK (Indian 10-digit format) |
| name | VARCHAR(100) | NOT NULL |
| visit_count | INT | NOT NULL, DEFAULT 0, CHECK ≥ 0 |
| on_whatsapp_list | TINYINT(1) | NOT NULL, DEFAULT 0 |

### Table: MENU_ITEM
| Column | Type | Constraints |
|---|---|---|
| item_id | INT AUTO_INCREMENT | **PK** |
| name | VARCHAR(100) | NOT NULL |
| category | ENUM('Starter','Main Course','Dessert','Beverage','Snack') | NOT NULL |
| price | DECIMAL(10,2) | NOT NULL, CHECK > 0 |
| tax_rate | DECIMAL(5,2) | NOT NULL, DEFAULT 5.00, CHECK [0, 28] |

### Table: STAFF
| Column | Type | Constraints |
|---|---|---|
| staff_id | INT AUTO_INCREMENT | **PK** |
| name | VARCHAR(100) | NOT NULL |
| role | ENUM('Manager','Waiter','Chef','Cashier','Host') | NOT NULL |
| salary | DECIMAL(10,2) | NOT NULL, CHECK > 0 |

### Table: SHIFT
| Column | Type | Constraints |
|---|---|---|
| shift_id | INT AUTO_INCREMENT | **PK** |
| staff_id | INT | NOT NULL, **FK → STAFF** (ON DELETE CASCADE) |
| shift_date | DATE | NOT NULL |
| start_time | TIME | NOT NULL |
| end_time | TIME | NOT NULL, CHECK end > start |
| attendance_status | ENUM('Present','Absent','Late','Half-Day') | NOT NULL, DEFAULT 'Present' |

### Table: ORDER_TABLE
| Column | Type | Constraints |
|---|---|---|
| order_id | INT AUTO_INCREMENT | **PK** |
| customer_phone | VARCHAR(15) | NOT NULL, **FK → CUSTOMER** |
| staff_id | INT | NOT NULL, **FK → STAFF** |
| table_no | INT | NOT NULL, CHECK > 0 |
| order_datetime | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| status | ENUM('Open','Ready','Billed','Cancelled') | NOT NULL, DEFAULT 'Open' |

### Table: ORDER_ITEM
| Column | Type | Constraints |
|---|---|---|
| order_id | INT | **PK** (composite), **FK → ORDER_TABLE** (CASCADE) |
| item_id | INT | **PK** (composite), **FK → MENU_ITEM** |
| quantity | INT | NOT NULL, CHECK > 0 |
| subtotal | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 |

### Table: BILL
| Column | Type | Constraints |
|---|---|---|
| bill_id | INT AUTO_INCREMENT | **PK** |
| order_id | INT | NOT NULL, **FK → ORDER_TABLE**, UNIQUE |
| total_amount | DECIMAL(10,2) | NOT NULL, CHECK ≥ 0 |
| tax_amount | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 |
| discount_applied | DECIMAL(5,2) | NOT NULL, DEFAULT 0.00, CHECK [0, 100] |
| payment_status | ENUM('Pending','Paid','Refunded') | NOT NULL, DEFAULT 'Pending' |
| generated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

### Table: CUSTOMER_RATING
| Column | Type | Constraints |
|---|---|---|
| rating_id | INT AUTO_INCREMENT | **PK** |
| staff_id | INT | NOT NULL, **FK → STAFF** |
| order_id | INT | NOT NULL, **FK → ORDER_TABLE**, UNIQUE |
| rating_score | TINYINT | NOT NULL, CHECK BETWEEN 1 AND 5 |

### Table: BILL_AUDIT_LOG
| Column | Type | Constraints |
|---|---|---|
| log_id | INT AUTO_INCREMENT | **PK** |
| bill_id | INT | NOT NULL |
| old_status | VARCHAR(20) | — |
| new_status | VARCHAR(20) | — |
| changed_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| changed_by_user | VARCHAR(100) | — |

## 4.3 Sample INSERT Statements

```sql
-- Staff
INSERT INTO STAFF (name, role, salary) VALUES
('Ravi Kumar', 'Manager', 75000.00),
('Priya Sharma', 'Waiter', 22000.00),
('Anil Mehta', 'Chef', 45000.00);

-- Customers
INSERT INTO CUSTOMER (phone, name, visit_count, on_whatsapp_list) VALUES
('9876543210', 'Arjun Reddy', 5, 1),
('9123456789', 'Meena Das', 2, 0);

-- Menu Items
INSERT INTO MENU_ITEM (name, category, price, tax_rate) VALUES
('Butter Chicken', 'Main Course', 320.00, 12.00),
('Mango Lassi', 'Beverage', 90.00, 5.00);

-- Orders
INSERT INTO ORDER_TABLE (customer_phone, staff_id, table_no) VALUES
('9876543210', 2, 3);

-- Order Items (subtotal auto-set by trg_auto_subtotal)
INSERT INTO ORDER_ITEM (order_id, item_id, quantity) VALUES
(1, 3, 2);
```


---

# CHAPTER 5: SQL IMPLEMENTATION

This chapter details the core database elements implemented in MySQL.

## 5.1 Table Creation

```sql
CREATE TABLE IF NOT EXISTS CUSTOMER (
    phone           VARCHAR(15)     NOT NULL,
    name            VARCHAR(100)    NOT NULL,
    visit_count     INT             NOT NULL DEFAULT 0,
    on_whatsapp_list TINYINT(1)     NOT NULL DEFAULT 0,
    CONSTRAINT pk_customer PRIMARY KEY (phone),
    CONSTRAINT chk_phone   CHECK (phone REGEXP '^[6-9][0-9]{9}$'),
    CONSTRAINT chk_visit   CHECK (visit_count >= 0)
);

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
```

## 5.2 Indexes

To optimize lookup operations for reporting and bill search screens, secondary indexes are explicitly defined:

```sql
CREATE INDEX idx_bill_date       ON BILL(generated_at);
CREATE INDEX idx_order_phone     ON ORDER_TABLE(customer_phone);
CREATE INDEX idx_order_staff     ON ORDER_TABLE(staff_id);
CREATE INDEX idx_shift_date      ON SHIFT(shift_date);
CREATE INDEX idx_shift_staff     ON SHIFT(staff_id);
```

## 5.3 Triggers

Triggers autonomously maintain business logic consistency.

**Trigger: Auto Subtotal Calculation**
```sql
CREATE TRIGGER trg_auto_subtotal
BEFORE INSERT ON ORDER_ITEM
FOR EACH ROW
BEGIN
    DECLARE v_price DECIMAL(10,2);
    SELECT price INTO v_price FROM MENU_ITEM WHERE item_id = NEW.item_id;
    SET NEW.subtotal = v_price * NEW.quantity;
END$$
```

**Trigger: Automated Audit Logging**
```sql
CREATE TRIGGER trg_bill_audit_log
AFTER UPDATE ON BILL
FOR EACH ROW
BEGIN
    IF OLD.payment_status != NEW.payment_status THEN
        INSERT INTO BILL_AUDIT_LOG (bill_id, old_status, new_status, changed_by_user)
        VALUES (NEW.bill_id, OLD.payment_status, NEW.payment_status, USER());
    END IF;
END$$
```

## 5.4 Stored Procedures

Stored Procedures encapsulate complex transactions spanning multiple tables.

**Procedure: Bill Generation**
Computes individual taxes and cross-references loyalty discount function before committing.
```sql
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

    -- Exception handler with rollback omitted for brevity
    START TRANSACTION;

    SELECT customer_phone, status INTO v_phone, v_status 
    FROM ORDER_TABLE WHERE order_id = p_order_id;
    
    -- Calculate per-item tax
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

    COMMIT;
END$$
```

## 5.5 Functions

**Function: Loyalty Discount Calculation**
```sql
CREATE FUNCTION fn_calculate_discount(p_phone VARCHAR(15))
RETURNS DECIMAL(5,2)
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_visits INT DEFAULT 0;
    DECLARE v_discount DECIMAL(5,2) DEFAULT 0.00;
    SELECT visit_count INTO v_visits FROM CUSTOMER WHERE phone = p_phone;

    IF v_visits >= 10 THEN SET v_discount = 15.00;
    ELSEIF v_visits >= 5 THEN SET v_discount = 10.00;
    ELSEIF v_visits >= 3 THEN SET v_discount = 5.00;
    END IF;

    RETURN v_discount;
END$$
```

## 5.6 Views

Views provide encapsulated reporting logic for real-time dashboard analytics.

**View: Top Performing Staff**
```sql
CREATE OR REPLACE VIEW v_top_staff AS
SELECT 
    s.staff_id, s.name AS staff_name, s.role,
    COUNT(DISTINCT o.order_id)                AS orders_served,
    COALESCE(ROUND(AVG(cr.rating_score),2),0) AS avg_rating,
    COALESCE(SUM(b.total_amount),0)           AS revenue_generated
FROM STAFF s
LEFT JOIN ORDER_TABLE o      ON s.staff_id = o.staff_id
LEFT JOIN BILL b             ON o.order_id = b.order_id AND b.payment_status = 'Paid'
LEFT JOIN CUSTOMER_RATING cr ON cr.staff_id = s.staff_id
GROUP BY s.staff_id, s.name, s.role
ORDER BY avg_rating DESC, orders_served DESC;
```

---

# CHAPTER 6: RESULTS AND SNAPSHOTS

The resulting system is a fully functional Desktop application backed by a normalized MySQL instance.

_Note: The student should replace these placeholders with actual screenshots from the application._

#### Figure 1: Login Screen (Role-Based Authentication)
[PLACEHOLDER: Insert screenshot of the dark-themed Login Screen]

#### Figure 2: Dashboard and Active Orders
[PLACEHOLDER: Insert screenshot of Dashboard with sidebar nav and "New Order" interface]

#### Figure 3: Interactive Bill Search
[PLACEHOLDER: Insert screenshot of the "Bill Search" screen with filters applied]

#### Figure 4: Analytics and Reporting View
[PLACEHOLDER: Insert screenshot of the "Analytics" screen showing Daily Sales and Top Staff tables]

#### Figure 5: Customer Loyalty and WhatsApp Opt-in
[PLACEHOLDER: Insert screenshot of the "Customer Management" screen]

#### Figure 6: Successful Trigger Compilation & View Output in MySQL CLI
[PLACEHOLDER: Insert screenshot showing `SHOW TRIGGERS` and `SELECT * FROM v_top_staff`]

#### Figure 7: Duplicate Payment Prevention Error
[PLACEHOLDER: Insert screenshot of an error dialog triggered by `trg_prevent_double_payment`]

---

# CHAPTER 7: CONCLUSION, LIMITATIONS AND FUTURE WORK

## 7.1 Conclusion
The **Intelligent Restaurant Billing & Management System** was successfully implemented and meets all the operational requirements outlined in the objectives. Moving from a manual or flat-file-based approach to a fully normalized relational schema ensures 100% data integrity, atomicity of financial transactions, and scalable reporting capabilities. The utilization of triggers and stored procedures shifted the heavy-lifting of complex aggregations and data-validation constraints securely into the database layer, decoupling it completely from the frontend UI framework.

The integration of Python CustomTkinter provides a visually appealing, contemporary dark-themed interface, making the database highly accessible and usable for an end-user such as a waiter or store manager.

## 7.2 Core Strengths
- **Data Consistency**: Strict enforcement of domain, entity, and referential integrity via Foreign Keys, UNIQUE constraints, and CHECK constraints.
- **Robust Exception Handling**: Multi-step transactions spanning customers, orders, menu items, and bills roll back entirely to maintain financial accuracy upon failure.
- **Automated Operations**: System auto-calculates taxes/discounts, increments loyalty status, and preserves an unalterable audit log entirely through autonomous triggers.

## 7.3 Limitations
1. **Concurrency Constraints**: Currently runs optimally on a local network; concurrent large-scale read/write operations from multiple distant nodes might experience latency due to row-level locks on heavy transaction tables.
2. **Static Configurations**: Core configurations such as specific tax slabs (e.g., 5%, 12%) or percentage constraints for the loyalty program (3/5/10 visits) are hardcoded into triggers/functions instead of a dedicated configuration table.
3. **Absence of Real-time Web Synching**: Desktop-bound GUI limits mobile accessibility for floor-staff waitressing applications.

## 7.4 Future Work
- **Cloud Database Hosting**: Migrating the MySQL footprint to AWS RDS or Azure SQL Database for centralized, multi-branch processing capability.
- **Dynamic Variable Table**: Constructing a distinct `SYS_CONFIG` table for dynamically configuring thresholds (such as minimum visits for loyalty rewards or current GST rates) without altering trigger definitions.
- **Inventory Management Module**: Introducing tables for `RAW_MATERIALS` and `RECIPES` with cascade triggers that deduct stock corresponding dynamically to the ordered menu items.
- **Predictive Analytics**: Using historical reporting view outputs as datasets for simple machine learning models predicting peak hour volumes.

---

# CHAPTER 8: REFERENCES

1. Elmasri, R., & Navathe, S. B. (2015). _Fundamentals of Database Systems_ (7th ed.). Pearson.
2. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019). _Database System Concepts_ (7th ed.). McGraw-Hill Education. 
3. MySQL 8.0 Reference Manual. Oracle Corporation. Retrieved from https://dev.mysql.com/doc/refman/8.0/en/
4. Python Software Foundation (2025). _MySQL Connector/Python Developer Guide_.
5. Date, C. J. (2003). _An Introduction to Database Systems_ (8th ed.). Addison-Wesley Longman Publishing Co., Inc.
6. Ramakrishnan, R., & Gehrke, J. (2002). _Database Management Systems_ (3rd ed.). McGraw-Hill.
