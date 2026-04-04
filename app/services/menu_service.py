# services/menu_service.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_connection import execute_query


def get_all_items():
    return execute_query("SELECT * FROM MENU_ITEM ORDER BY category, name", fetch=True)

def get_items_by_category(category: str):
    return execute_query(
        "SELECT * FROM MENU_ITEM WHERE category = %s ORDER BY name", (category,), fetch=True
    )

def add_item(name: str, category: str, price: float, tax_rate: float):
    return execute_query(
        "INSERT INTO MENU_ITEM (name, category, price, tax_rate) VALUES (%s, %s, %s, %s)",
        (name, category, price, tax_rate)
    )

def update_price(item_id: int, price: float):
    return execute_query(
        "UPDATE MENU_ITEM SET price = %s WHERE item_id = %s", (price, item_id)
    )

def get_low_selling():
    return execute_query("SELECT * FROM v_low_selling_items", fetch=True)
