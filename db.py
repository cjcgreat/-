# db.py
import sqlite3
from typing import Optional, List, Tuple, Any

DB_PATH = "bank.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )
        """)
        conn.commit()

def create_account(username: str, initial_balance: float = 0.0) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO accounts (username, balance) VALUES (?, ?)",
            (username, float(initial_balance))
        )
        return cur.lastrowid

def get_account_by_username(username: str) -> Optional[sqlite3.Row]:
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        return cur.fetchone()

def update_balance(account_id: int, new_balance: float) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE accounts SET balance = ? WHERE id = ?", (float(new_balance), account_id))
        conn.commit()

def list_accounts() -> List[sqlite3.Row]:
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM accounts ORDER BY id")
        return cur.fetchall()
