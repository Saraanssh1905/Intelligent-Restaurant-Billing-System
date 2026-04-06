# 🍽 Intelligent Restaurant Billing & Management System

> **B.Tech Database Systems Lab — Mini Project**  
> Manipal Institute of Technology, Manipal Academy of Higher Education

A full-stack desktop application that automates restaurant billing, order management, staff scheduling, customer loyalty tracking, and business analytics — powered by a normalized MySQL backend and a modern Python GUI.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Database Design](#-database-design)
- [Stored Procedures & Functions](#-stored-procedures--functions)
- [Triggers](#-triggers)
- [Views](#-views)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Demo Credentials](#-demo-credentials)
- [Application Walkthrough](#-application-walkthrough)
- [Common Pitfalls](#-common-pitfalls)

---

## 🧭 Overview

Managing a restaurant involves juggling orders, bills, customer loyalty, staff schedules, and revenue analytics — all in real-time. This project implements an **Intelligent Restaurant Billing & Management System** that encapsulates critical business logic *inside the database layer* using stored procedures, triggers, and views, while a clean desktop GUI provides an intuitive interface for staff.

The system demonstrates advanced DBMS concepts including:

| Concept | Implementation |
|---|---|
| **Normalization** | 9 tables in 3NF with proper foreign keys and constraints |
| **Stored Procedures** | 7 procedures handling order lifecycle & reporting |
| **User-Defined Functions** | 2 functions for discount calculation & subtotal computation |
| **Triggers** | 9 triggers for auto-computation, validation, and audit logging |
| **Views** | 8 reporting views for analytics dashboards |
| **Transactions** | ACID-compliant order creation & billing with rollback on failure |
| **Indexing** | Strategic indexes on frequently queried columns |

---

## ✨ Key Features

### 🧾 Order Management
- Create new orders linked to customers, staff, and table numbers
- Add multiple menu items with quantities to an existing order
- Automatic subtotal calculation via database triggers
- Order status lifecycle: `Open` → `Ready` → `Billed` → `Cancelled`

### 💳 Billing & Payments
- One-click bill generation with itemized tax computation (per-item tax rates)
- Automatic loyalty discount application based on customer visit history
- Payment status tracking (`Pending` → `Paid` → `Refunded`)
- Duplicate payment prevention via triggers
- Complete audit trail of every payment status change

### 👤 Customer & Loyalty
- Auto-registration of new customers during order creation
- Visit-based loyalty discount tiers:
  - **3+ visits** → 5% discount
  - **5+ visits** → 10% discount
  - **10+ visits** → 15% discount
- Automatic WhatsApp opt-in after 3 paid visits (trigger-driven)
- Frequent customer tracking with total spend analytics

### 👨‍💼 Staff & Shift Management
- Role-based staff records (Manager, Waiter, Chef, Cashier, Host)
- Shift scheduling with attendance tracking (Present, Absent, Late, Half-Day)
- Per-staff performance metrics: orders served, average rating, revenue generated
- Customer rating system (1–5 stars per order)

### 📊 Analytics & Reporting
- **Daily Sales Summary** — bills, revenue, tax, and average bill value per day
- **Monthly Revenue Trends** — month-over-month revenue tracking
- **Top Staff Leaderboard** — ranked by average rating and orders served
- **Low-Selling Items** — menu items ordered 0–1 times (for menu optimization)
- **Shift Attendance Report** — hours worked and attendance breakdown
- **Full Bill History** — searchable by date, customer phone, or staff

### 🔍 Bill Search
- Flexible multi-filter search (date, phone number, staff ID)
- Detailed bill view with order items, tax breakdown, and discount info

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Database** | MySQL 8.0+ | Relational data storage, business logic (procedures, triggers, views) |
| **Backend** | Python 3.10+ | Service layer, database connectivity |
| **GUI** | CustomTkinter 5.2+ | Modern, dark-themed desktop interface |
| **Charting** | Matplotlib 3.8+ | Analytics visualizations |
| **Connector** | mysql-connector-python 8.3+ | Python ↔ MySQL bridge |

---

## 🏗 Architecture

The application follows a clean **3-tier architecture**:

```
┌─────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                │
│    CustomTkinter GUI (Dark Mode, Sidebar Navigation)│
│                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │  Login   │ │  Orders  │ │ Billing  │ │  Menu  │ │
│  ├──────────┤ ├──────────┤ ├──────────┤ ├────────┤ │
│  │Customers │ │  Staff   │ │Analytics │ │ Search │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                    SERVICE LAYER                    │
│          Python modules (app/services/)             │
│                                                     │
│  billing_service · menu_service · customer_service  │
│  staff_service   · report_service                   │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│               DATA ACCESS LAYER                     │
│          db_connection.py + db_config.py            │
│                                                     │
│  execute_query() · call_procedure()                 │
│  call_procedure_with_out() · Transaction()          │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                  DATABASE LAYER                     │
│                    MySQL 8.0                        │
│                                                     │
│  9 Tables · 7 Procedures · 2 Functions              │
│  9 Triggers · 8 Views · 5 Indexes                   │
└─────────────────────────────────────────────────────┘
```

---

## 🗄 Database Design

### Entity-Relationship Summary

The database `restaurant_db` contains **9 tables** in **Third Normal Form (3NF)**:

| # | Table | Description | Primary Key |
|---|---|---|---|
| 1 | `CUSTOMER` | Customer records with loyalty tracking | `phone` (VARCHAR) |
| 2 | `MENU_ITEM` | Food/beverage catalog with per-item tax rates | `item_id` (AUTO_INCREMENT) |
| 3 | `STAFF` | Employee records with roles and salaries | `staff_id` (AUTO_INCREMENT) |
| 4 | `SHIFT` | Staff shift schedules & attendance | `shift_id` (AUTO_INCREMENT) |
| 5 | `ORDER_TABLE` | Orders with customer, staff, and table linkage | `order_id` (AUTO_INCREMENT) |
| 6 | `ORDER_ITEM` | Line items in each order (composite PK) | `(order_id, item_id)` |
| 7 | `BILL` | Generated bills with tax, discount, payment status | `bill_id` (AUTO_INCREMENT) |
| 8 | `CUSTOMER_RATING` | 1–5 star rating per order | `rating_id` (AUTO_INCREMENT) |
| 9 | `BILL_AUDIT_LOG` | Audit trail for payment status changes | `log_id` (AUTO_INCREMENT) |

### Key Constraints & Relationships

```
CUSTOMER (phone)  ◄──────  ORDER_TABLE (customer_phone)
STAFF (staff_id)  ◄──────  ORDER_TABLE (staff_id)
STAFF (staff_id)  ◄──────  SHIFT (staff_id)          [ON DELETE CASCADE]
ORDER_TABLE       ◄──────  ORDER_ITEM (order_id)     [ON DELETE CASCADE]
MENU_ITEM         ◄──────  ORDER_ITEM (item_id)
ORDER_TABLE       ◄──────  BILL (order_id)           [UNIQUE — 1 bill per order]
STAFF             ◄──────  CUSTOMER_RATING (staff_id)
ORDER_TABLE       ◄──────  CUSTOMER_RATING (order_id) [UNIQUE — 1 rating per order]
```

### CHECK Constraints

- Phone numbers must match Indian mobile format: `^[6-9][0-9]{9}$`
- Prices, salaries, and quantities must be positive
- Tax rates bounded between 0% and 28%
- Discount range: 0%–100%
- Rating scores: 1–5
- Shift end time must be after start time

### Indexes

| Index | Table | Column(s) | Purpose |
|---|---|---|---|
| `idx_bill_date` | BILL | `generated_at` | Fast date-range bill searches |
| `idx_order_phone` | ORDER_TABLE | `customer_phone` | Customer order lookups |
| `idx_order_staff` | ORDER_TABLE | `staff_id` | Staff order lookups |
| `idx_shift_date` | SHIFT | `shift_date` | Shift schedule queries |
| `idx_shift_staff` | SHIFT | `staff_id` | Per-staff shift lookups |

---

## ⚙ Stored Procedures & Functions

### User-Defined Functions (2)

| Function | Input | Returns | Description |
|---|---|---|---|
| `fn_calculate_discount(phone)` | Customer phone | DECIMAL(5,2) | Returns loyalty discount % based on visit count tiers |
| `fn_get_order_subtotal(order_id)` | Order ID | DECIMAL(10,2) | Computes total of all order item subtotals |

### Stored Procedures (7)

| Procedure | Parameters | Description |
|---|---|---|
| `sp_create_order` | IN: phone, name, staff_id, table_no; OUT: order_id, message | Creates a new order; auto-inserts customer if not exists; uses transactions with rollback |
| `sp_add_order_item` | IN: order_id, item_id, quantity; OUT: message | Adds item to an open order; validates order status; handles duplicate items via `ON DUPLICATE KEY UPDATE` |
| `sp_generate_bill` | IN: order_id; OUT: bill_id, message | Generates bill with per-item tax calculation and loyalty discount; prevents duplicate billing; marks order as `Billed` |
| `sp_update_payment` | IN: bill_id, new_status; OUT: message | Updates payment status; prevents duplicate payments |
| `sp_search_bills` | IN: date, phone, staff_id (all optional) | Flexible bill search with multi-filter support; returns joined bill+order+customer+staff data |
| `sp_get_top_staff` | IN: month, year | Returns staff leaderboard: orders served, avg rating, revenue generated for a given month |
| `sp_calculate_staff_performance` | IN: staff_id | Single-staff summary: total orders, avg rating, total revenue, shifts worked, days present |

---

## 🔔 Triggers

The system uses **9 triggers** to enforce business rules and automate computations at the database level:

| # | Trigger | Event | Table | Purpose |
|---|---|---|---|---|
| 1 | `trg_auto_subtotal` | BEFORE INSERT | ORDER_ITEM | Auto-calculates `subtotal = price × quantity` |
| 2 | `trg_recalc_subtotal_on_update` | BEFORE UPDATE | ORDER_ITEM | Recalculates subtotal when quantity changes |
| 3 | `trg_no_negative_qty` | BEFORE INSERT | ORDER_ITEM | Blocks zero or negative quantity entries |
| 4 | `trg_no_negative_salary_insert` | BEFORE INSERT | STAFF | Prevents salary ≤ 0 on new staff records |
| 5 | `trg_no_negative_salary_update` | BEFORE UPDATE | STAFF | Prevents salary ≤ 0 on staff updates |
| 6 | `trg_increment_visit_count` | AFTER UPDATE | BILL | Increments customer visit count when bill is marked `Paid` |
| 7 | `trg_whatsapp_optin` | AFTER UPDATE | BILL | Auto opts-in customer to WhatsApp list after 3+ visits |
| 8 | `trg_bill_audit_log` | AFTER UPDATE | BILL | Logs every payment status change to `BILL_AUDIT_LOG` |
| 9 | `trg_prevent_double_payment` | BEFORE UPDATE | BILL | Blocks duplicate `Paid` → `Paid` updates via SIGNAL |

---

## 👁 Views

8 reporting views power the analytics dashboard and search screens:

| View | Purpose |
|---|---|
| `v_daily_sales` | Daily totals: bill count, revenue, tax, avg bill value |
| `v_monthly_revenue` | Monthly aggregated revenue with month names |
| `v_top_staff` | Staff ranked by average rating and orders served |
| `v_frequent_customers` | Customers sorted by visit count with loyalty discount % and total spend |
| `v_low_selling_items` | Menu items ordered ≤ 1 time (underperformers) |
| `v_shift_attendance` | Staff attendance with hours worked per shift |
| `v_whatsapp_customers` | Customers opted into WhatsApp notifications |
| `v_bill_history` | Complete bill history with customer, staff, and order details |

---

## 📁 Project Structure

```
DBS MiniProject/
│
├── db/                              # Database layer (run in order)
│   ├── 01_schema.sql                # Tables, constraints, indexes
│   ├── 02_seed_data.sql             # Sample data (6 staff, 6 customers, 12 menu items)
│   ├── 03_procedures.sql            # 7 stored procedures + 2 functions
│   ├── 04_triggers.sql              # 9 triggers
│   ├── 05_views.sql                 # 8 reporting views
│   └── all_views_compiled.sql       # Consolidated views reference
│
├── app/                             # Application layer
│   ├── main.py                      # Entry point — launches CTk window
│   ├── db_config.py                 # MySQL credentials & loyalty tiers
│   ├── db_connection.py             # Connection manager, query executor, Transaction context manager
│   │
│   ├── services/                    # Business logic / data access
│   │   ├── billing_service.py       # Order creation, item addition, bill generation, payment
│   │   ├── menu_service.py          # CRUD for menu items, low-selling analysis
│   │   ├── customer_service.py      # Customer lookup, loyalty discount, WhatsApp list
│   │   ├── staff_service.py         # Staff CRUD, shifts, ratings, performance
│   │   └── report_service.py        # Daily sales, monthly revenue, bill history
│   │
│   └── ui/                          # GUI screens (CustomTkinter)
│       ├── login_screen.py          # Staff authentication (ID + name-based password)
│       ├── dashboard_screen.py      # Sidebar navigation hub
│       ├── order_screen.py          # New order + add items workflow
│       ├── billing_screen.py        # Bill generation + payment processing
│       ├── menu_screen.py           # Menu catalog management
│       ├── customer_screen.py       # Customer directory + loyalty info
│       ├── staff_screen.py          # Staff management + shift scheduling
│       ├── analytics_screen.py      # Charts & reports (matplotlib)
│       └── bill_search_screen.py    # Multi-filter bill search
│
├── requirements.txt                 # Python dependencies
├── setup_db.py                      # Automated DB setup script
└── README.md                        # This file
```

---

## 📋 Prerequisites

| Requirement | Version |
|---|---|
| **Python** | 3.10 or higher |
| **MySQL Server** | 8.0 or higher |
| **pip** | Latest recommended |

> **Note:** MySQL Workbench is recommended for running the SQL files, as it handles `DELIMITER` changes automatically.

---

## 🚀 Installation & Setup

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Saraanssh1905/Intelligent-Restaurant-Billing-System.git
cd Intelligent-Restaurant-Billing-System
```

### Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `customtkinter` — Modern themed Tkinter widgets
- `mysql-connector-python` — MySQL database connector
- `matplotlib` — Charts and visualizations

### Step 3 — Set Up the Database

Run the SQL files **in order** using MySQL Workbench or CLI:

```bash
mysql -u root -p < db/01_schema.sql       # Tables + constraints + indexes
mysql -u root -p < db/02_seed_data.sql     # Sample data
mysql -u root -p < db/03_procedures.sql    # Stored procedures + functions
mysql -u root -p < db/04_triggers.sql      # All 9 triggers
mysql -u root -p < db/05_views.sql         # Reporting views
```

> ⚠ **Important:** The files must be executed in the numbered order because of foreign key and trigger dependencies.

### Step 4 — Configure Database Credentials

Edit `app/db_config.py` with your MySQL connection details:

```python
DB_CONFIG = {
    "host":     "127.0.0.1",
    "port":     3306,
    "user":     "root",
    "password": "YOUR_MYSQL_PASSWORD",   # ← Change this
    "database": "restaurant_db",
    "autocommit": False,                 # Required for transactions
    "connection_timeout": 10,
}
```

---

## ▶ Running the Application

```bash
cd app
python main.py
```

The application launches a **1280×800** dark-themed desktop window with a sidebar-based navigation interface.

---

## 🔑 Demo Credentials

Authentication uses a simplified scheme: **password = staff's first name** (case-insensitive).

| Staff ID | Name | Password | Role |
|---|---|---|---|
| 1 | Ravi Kumar | `Ravi` | Manager |
| 2 | Priya Sharma | `Priya` | Waiter |
| 3 | Anil Mehta | `Anil` | Chef |
| 4 | Sneha Patel | `Sneha` | Cashier |
| 5 | Raj Nair | `Raj` | Waiter |
| 6 | Deepa Singh | `Deepa` | Host |

---

## 🖥 Application Walkthrough

### 1. Login Screen
- Enter your **Staff ID** and **password** (first name)
- Dark-themed centered card with branding
- Error feedback for invalid credentials

### 2. Dashboard & Navigation
- Left sidebar with 7 sections: New Order, Billing, Menu, Customers, Staff & Shifts, Analytics, Bill Search
- Active section highlighted in accent blue
- Staff name and role displayed at the bottom of the sidebar
- One-click logout functionality

### 3. New Order
- Enter customer phone, name, staff ID, and table number
- System auto-registers new customers via `INSERT IGNORE`
- Add menu items by ID and quantity
- Subtotals auto-computed by `trg_auto_subtotal` trigger

### 4. Billing
- Select an open order to generate a bill
- System calculates: per-item tax → subtotal → loyalty discount → final amount
- Bill generation marks the order as `Billed`
- Process payment to mark as `Paid` (triggers visit count increment + WhatsApp opt-in)

### 5. Menu Management
- View all menu items categorized by type (Starter, Main Course, Dessert, Beverage, Snack)
- Add new items with name, category, price, and tax rate
- Update item prices
- View underperforming items (ordered ≤ 1 time)

### 6. Customer Directory
- Browse all customers sorted by visit count
- View loyalty discount tier and total spend
- Check WhatsApp opt-in list

### 7. Staff & Shifts
- View/add staff members with roles and salaries
- Schedule shifts with attendance tracking
- Submit customer ratings for service
- View individual staff performance summaries

### 8. Analytics Dashboard
- **Daily Sales** — Revenue, bill count, and average bill value per day
- **Monthly Revenue** — Revenue trend across months
- **Top Staff** — Leaderboard by rating and orders
- **Low Sellers** — Underperforming menu items

### 9. Bill Search
- Filter bills by date, customer phone number, or staff ID
- All filters are optional and combinable
- Results show bill details with customer and staff information

---

## ⚠ Common Pitfalls

| Issue | Solution |
|---|---|
| SQL files fail to execute | Run them **in order** (01 → 02 → 03 → 04 → 05) |
| `DELIMITER` errors in MySQL CLI | Use `DELIMITER $$` before procedures/triggers. MySQL Workbench handles this automatically |
| Transactions not working | Ensure `autocommit` is set to `False` in `db_config.py` |
| Login fails | Password = **first name** of the staff member (case-insensitive) |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` and ensure you're in the `app/` directory |
| Connection refused | Verify MySQL is running and credentials in `db_config.py` are correct |
| Duplicate bill error | Each order can only be billed once (enforced by `UNIQUE` constraint on `order_id` in `BILL`) |

---

## 📜 License

This project was developed as an academic mini-project for the Database Systems Lab course at **Manipal Institute of Technology**.

---

<p align="center">
  <i>Built with ❤ using Python, CustomTkinter & MySQL</i>
</p>
