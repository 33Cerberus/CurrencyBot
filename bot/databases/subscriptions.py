import sqlite3
import os
from datetime import datetime, timezone

def get_connection():
    conn = sqlite3.connect("data/subscriptions.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            currency_code INTEGER,
            created_at TEXT,
            UNIQUE(user_id, currency_code)
        )
    """)
    conn.commit()
    conn.close()

def add_subscription(user_id, currency_code):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO subscriptions (user_id, currency_code, created_at) VALUES (?, ?, ?)",
        (user_id, currency_code, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()

def remove_subscription(user_id, currency_code):
    conn = get_connection()
    conn.execute(
        "delete from subscriptions where user_id = ? and currency_code = ?",
        (user_id, currency_code)
    )
    conn.commit()
    conn.close()

def has_subscription(user_id, currency_code):
    conn = get_connection()
    row = conn.execute("""SELECT 1 FROM subscriptions WHERE user_id = ? AND currency_code = ? LIMIT 1""",
                       (user_id, currency_code)).fetchone()
    conn.close()
    return row is not None

def get_all_subscriptions():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM subscriptions").fetchall()
    conn.close()
    return rows
