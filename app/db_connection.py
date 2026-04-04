# db_connection.py
# Central DB connection manager with transaction wrapper

import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG


def get_connection():
    """Returns a new MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise ConnectionError(f"DB Connection failed: {e}")


def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """
    Execute a single SQL query.
    - fetch=True  → returns list of dicts (SELECT)
    - fetch=False → returns (rows_affected, last_insert_id)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = (cursor.rowcount, cursor.lastrowid)
    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Query error: {e}\nSQL: {query}")
    finally:
        cursor.close()
        conn.close()
    return result


def call_procedure(proc_name: str, args: tuple = ()):
    """
    Call a stored procedure that returns result sets (SELECT inside procedure).
    Returns list of result sets (each is a list of dicts).
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    results = []
    try:
        cursor.callproc(proc_name, args)
        conn.commit()
        for rs in cursor.stored_results():
            results.append(rs.fetchall())
    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Procedure error [{proc_name}]: {e}")
    finally:
        cursor.close()
        conn.close()
    return results


def call_procedure_with_out(proc_name: str, in_args: list, out_count: int):
    """
    Call a stored procedure that has OUT parameters.
    Uses SET @var = NULL → CALL proc(in_args..., @var...) → SELECT @var pattern.

    in_args  : list of IN parameter values
    out_count: number of OUT params

    Returns list of OUT values in order.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Named session variables for OUT params
        out_vars = [f"@_out_{proc_name}_{i}" for i in range(out_count)]

        # Initialize OUT vars to NULL
        for var in out_vars:
            cursor.execute(f"SET {var} = NULL")

        # Build CALL statement: CALL proc(%s, %s, @var1, @var2)
        in_placeholders  = ", ".join(["%s"] * len(in_args))
        out_placeholders = ", ".join(out_vars)
        if in_args and out_vars:
            all_placeholders = f"{in_placeholders}, {out_placeholders}"
        elif in_args:
            all_placeholders = in_placeholders
        else:
            all_placeholders = out_placeholders

        call_sql = f"CALL {proc_name}({all_placeholders})"
        cursor.execute(call_sql, tuple(in_args))
        conn.commit()

        # Consume any implicit result sets the procedure may have returned
        try:
            while cursor.nextset():
                pass
        except Exception:
            pass

        # Fetch OUT values
        out_vals = []
        for var in out_vars:
            cursor.execute(f"SELECT {var} AS val")
            row = cursor.fetchone()
            out_vals.append(row["val"] if row else None)

        return out_vals
    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Procedure OUT error [{proc_name}]: {e}")
    finally:
        cursor.close()
        conn.close()


class Transaction:
    """
    Context manager for manual atomic transactions.
    Usage:
        with Transaction() as (conn, cur):
            cur.execute(...)
    Commits on exit, rolls back on exception.
    """
    def __init__(self):
        self.conn   = None
        self.cursor = None

    def __enter__(self):
        self.conn = get_connection()
        self.conn.autocommit = False
        self.cursor = self.conn.cursor(dictionary=True)
        return self.conn, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return False   # re-raise exceptions
