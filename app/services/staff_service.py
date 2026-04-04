# services/staff_service.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_connection import execute_query, call_procedure


def get_all_staff():
    return execute_query("SELECT * FROM STAFF ORDER BY name", fetch=True)

def add_staff(name: str, role: str, salary: float):
    return execute_query(
        "INSERT INTO STAFF (name, role, salary) VALUES (%s, %s, %s)",
        (name, role, salary)
    )

def get_top_staff(month: int, year: int):
    results = call_procedure("sp_get_top_staff", args=(month, year))
    return results[0] if results else []

def get_staff_performance(staff_id: int):
    results = call_procedure("sp_calculate_staff_performance", args=(staff_id,))
    return results[0][0] if results and results[0] else {}

def add_shift(staff_id: int, shift_date: str, start_time: str, end_time: str, status: str):
    return execute_query(
        "INSERT INTO SHIFT (staff_id, shift_date, start_time, end_time, attendance_status) VALUES (%s,%s,%s,%s,%s)",
        (staff_id, shift_date, start_time, end_time, status)
    )

def get_shifts(staff_id: int = None, shift_date: str = None):
    if staff_id:
        return execute_query(
            "SELECT * FROM v_shift_attendance WHERE staff_name IN (SELECT name FROM STAFF WHERE staff_id=%s)",
            (staff_id,), fetch=True
        )
    return execute_query("SELECT * FROM v_shift_attendance", fetch=True)

def add_rating(staff_id: int, order_id: int, rating: int):
    return execute_query(
        "INSERT INTO CUSTOMER_RATING (staff_id, order_id, rating_score) VALUES (%s,%s,%s)",
        (staff_id, order_id, rating)
    )
