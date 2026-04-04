# services/billing_service.py
# Atomic billing flow: create order → add items → generate bill → pay

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_connection import call_procedure_with_out, call_procedure, execute_query


def create_order(phone: str, cname: str, staff_id: int, table_no: int):
    """
    Calls sp_create_order. Returns (order_id, message).
    order_id == -1 means failure.
    """
    out = call_procedure_with_out(
        "sp_create_order",
        in_args=[phone, cname, staff_id, table_no],
        out_count=2
    )
    return int(out[0] or -1), str(out[1] or "Unknown error")


def add_item(order_id: int, item_id: int, quantity: int):
    """Calls sp_add_order_item. Returns message string."""
    out = call_procedure_with_out(
        "sp_add_order_item",
        in_args=[order_id, item_id, quantity],
        out_count=1
    )
    return str(out[0])


def generate_bill(order_id: int):
    """Calls sp_generate_bill. Returns (bill_id, message)."""
    out = call_procedure_with_out(
        "sp_generate_bill",
        in_args=[order_id],
        out_count=2
    )
    return int(out[0] or -1), str(out[1] or "Unknown error")


def update_payment(bill_id: int, status: str = "Paid"):
    """Calls sp_update_payment. Returns message."""
    out = call_procedure_with_out(
        "sp_update_payment",
        in_args=[bill_id, status],
        out_count=1
    )
    return str(out[0])


def search_bills(date=None, phone=None, staff_id=None):
    """Calls sp_search_bills with optional filters. Returns list of bill dicts."""
    results = call_procedure("sp_search_bills", args=(date, phone, staff_id))
    return results[0] if results else []


def get_bill_detail(bill_id: int):
    """Returns full bill detail with order items."""
    query = """
        SELECT
            b.bill_id, b.total_amount, b.tax_amount,
            b.discount_applied, b.payment_status, b.generated_at,
            o.order_id, o.table_no,
            c.name AS customer_name, c.phone,
            s.name AS staff_name,
            mi.name AS item_name, oi.quantity, oi.subtotal
        FROM BILL b
        JOIN ORDER_TABLE o  ON b.order_id = o.order_id
        JOIN CUSTOMER c     ON o.customer_phone = c.phone
        JOIN STAFF s        ON o.staff_id = s.staff_id
        JOIN ORDER_ITEM oi  ON o.order_id = oi.order_id
        JOIN MENU_ITEM mi   ON oi.item_id = mi.item_id
        WHERE b.bill_id = %s
    """
    return execute_query(query, (bill_id,), fetch=True)
