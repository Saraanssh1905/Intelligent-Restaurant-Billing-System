# services/customer_service.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_connection import execute_query


def get_customer(phone: str):
    return execute_query("SELECT * FROM CUSTOMER WHERE phone = %s", (phone,), fetch=True)

def add_customer(phone: str, name: str):
    return execute_query(
        "INSERT IGNORE INTO CUSTOMER (phone, name) VALUES (%s, %s)", (phone, name)
    )

def get_all_customers():
    return execute_query("SELECT * FROM CUSTOMER ORDER BY visit_count DESC", fetch=True)

def get_frequent_customers():
    return execute_query("SELECT * FROM v_frequent_customers", fetch=True)

def get_whatsapp_list():
    return execute_query("SELECT * FROM v_whatsapp_customers", fetch=True)

def get_loyalty_discount(phone: str):
    rows = execute_query(
        "SELECT fn_calculate_discount(%s) AS discount", (phone,), fetch=True
    )
    return float(rows[0]["discount"]) if rows else 0.0
