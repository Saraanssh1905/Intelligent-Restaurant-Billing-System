# db_config.py
# Edit DB credentials here. Auto-updated by setup_db.py

DB_CONFIG = {
    "host":     "127.0.0.1",
    "port":     3306,
    "user":     "root",
    "password": "Dbms@MIT_26",
    "database": "restaurant_db",
    "autocommit": False,
    "connection_timeout": 10,
}

# Loyalty discount thresholds (mirrors fn_calculate_discount logic)
LOYALTY_TIERS = {
    10: 15.0,
    5:  10.0,
    3:   5.0,
    0:   0.0,
}
