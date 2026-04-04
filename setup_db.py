"""
setup_db.py — Run this ONCE to set up the entire database.
Prompts for MySQL credentials, runs all 5 SQL files, then updates db_config.py.

Usage:   python setup_db.py
"""
import subprocess
import sys
import os
import re
import getpass

MYSQL_BIN = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
SQL_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
APP_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")

SQL_FILES = [
    "01_schema.sql",
    "02_seed_data.sql",
    "03_procedures.sql",
    "04_triggers.sql",
    "05_views.sql",
]


def run_sql_file(fpath, user, password, host, port):
    """Execute a .sql file via mysql CLI using 'source' command."""
    # Use forward slashes — MySQL CLI requires them in 'source' paths
    fpath_fwd = fpath.replace("\\", "/")
    cmd = [
        MYSQL_BIN,
        f"-u{user}",
        f"-p{password}",
        f"-h{host}",
        f"-P{port}",
        "--default-character-set=utf8mb4",
        "-e", f"source {fpath_fwd}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def update_config(user, password, host, port):
    config_path = os.path.join(APP_DIR, "db_config.py")
    with open(config_path, "r") as f:
        content = f.read()

    content = re.sub(r'"user":\s*"[^"]*"',     f'"user":     "{user}"',     content)
    content = re.sub(r'"password":\s*"[^"]*"', f'"password": "{password}"', content)
    content = re.sub(r'"host":\s*"[^"]*"',     f'"host":     "{host}"',     content)
    content = re.sub(r'"port":\s*\d+',         f'"port":     {port}',       content)

    with open(config_path, "w") as f:
        f.write(content)
    print(f"  ✅ app/db_config.py updated with your credentials.")


def main():
    print("=" * 60)
    print("  🍽  Restaurant DB Setup")
    print("=" * 60)

    if not os.path.exists(MYSQL_BIN):
        print(f"\n❌ MySQL not found at:\n   {MYSQL_BIN}")
        print("   Update MYSQL_BIN in setup_db.py to your mysql.exe path.")
        sys.exit(1)

    user     = input("\nMySQL username [root]: ").strip() or "root"
    password = getpass.getpass("MySQL password: ")
    host     = input("MySQL host [127.0.0.1]: ").strip() or "127.0.0.1"
    port     = input("MySQL port [3306]: ").strip() or "3306"

    print()
    all_ok = True
    for fname in SQL_FILES:
        fpath = os.path.join(SQL_DIR, fname)
        print(f"  ▶  {fname} ...", end=" ", flush=True)
        code, out, err = run_sql_file(fpath, user, password, host, port)

        # Filter out MySQL warnings (they're printed to stderr but don't indicate failure)
        real_errors = [
            line for line in err.splitlines()
            if line.strip()
            and "Warning" not in line
            and "warning" not in line
            and "mysqldump" not in line
        ]

        if code == 0 or not real_errors:
            print("✅")
        else:
            print("❌")
            for e in real_errors[:8]:
                print(f"     {e}")
            all_ok = False
            print("\n⚠  Fix the error above, then rerun setup_db.py")
            sys.exit(1)

    print()
    if all_ok:
        update_config(user, password, host, port)
        print()
        print("✅  All done! Database is ready.")
        print()
        print("  Run the app:")
        print("    cd app")
        print("    python main.py")
        print()
        print("  Demo Login:")
        print("    Staff ID : 1    Password : Ravi   (Manager)")
        print("    Staff ID : 2    Password : Priya  (Waiter)")
        print()
    print("=" * 60)


if __name__ == "__main__":
    main()
