# services/report_service.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_connection import execute_query


def get_daily_sales():
    return execute_query("SELECT * FROM v_daily_sales LIMIT 30", fetch=True)

def get_monthly_revenue():
    return execute_query("SELECT * FROM v_monthly_revenue LIMIT 12", fetch=True)

def get_top_staff_view():
    return execute_query("SELECT * FROM v_top_staff", fetch=True)

def get_bill_history():
    return execute_query("SELECT * FROM v_bill_history LIMIT 100", fetch=True)

def get_order_items(order_id: int):
    return execute_query(
        """SELECT mi.name, oi.quantity, mi.price, oi.subtotal
           FROM ORDER_ITEM oi JOIN MENU_ITEM mi ON oi.item_id = mi.item_id
           WHERE oi.order_id = %s""",
        (order_id,), fetch=True
    )
