# Intelligent Restaurant Billing & Management System
## MIT Manipal DBMS Mini Project

### Quick Start (3 commands)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Set up database (run in MySQL Workbench or CLI in order)
#    mysql -u root -p < db/01_schema.sql
#    mysql -u root -p < db/02_seed_data.sql
#    mysql -u root -p < db/03_procedures.sql
#    mysql -u root -p < db/04_triggers.sql
#    mysql -u root -p < db/05_views.sql

# 3. Edit credentials & run GUI
#    Edit app/db_config.py → set your MySQL password
cd app
python main.py
```

### Login Credentials (demo)
| Staff ID | Password (first name) | Role |
|---|---|---|
| 1 | Ravi | Manager |
| 2 | Priya | Waiter |
| 4 | Sneha | Cashier |

### File Execution Order
```
db/01_schema.sql    → tables + constraints + indexes
db/02_seed_data.sql → sample data
db/03_procedures.sql → stored procedures + functions
db/04_triggers.sql  → all 9 triggers
db/05_views.sql     → reporting views
```

### Team Split (2-person)
**Person A:** db/ folder (all SQL files) + viva Q&A preparation  
**Person B:** app/ folder (Python GUI + services) + demo rehearsal

### Common Mistakes to Avoid
- Run SQL files **in order** (schema first, triggers last)
- Set `DELIMITER $$` before procedures/triggers in raw CLI
- MySQL Workbench handles DELIMITER automatically
- `autocommit` must be `False` for transactions to work
- PASSWORD in demo = first name of staff (case-insensitive)
