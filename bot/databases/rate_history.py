import sqlite3
import os
from datetime import datetime, timezone

def get_connection():
    conn = sqlite3.connect("data/rate_history.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rate_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code INTEGER,
            rate_buy REAL,
            rate_sell REAL,
            rate_cross REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_rate(currency_code, rate_buy, rate_sell, rate_cross):
    conn = get_connection()
    conn.execute(
        "INSERT INTO rate_history (currency_code, rate_buy, rate_sell, rate_cross, timestamp) VALUES (?, ?, ?, ?, ?)",
        (currency_code, rate_buy, rate_sell, rate_cross, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()

def get_last_rates(currency_code, limit=5):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM rate_history WHERE currency_code = ? ORDER BY timestamp DESC LIMIT ?",
        (currency_code, limit)
    ).fetchall()
    conn.close()
    return rows