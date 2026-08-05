import sqlite3
import os
from datetime import datetime, timezone

def get_connection():
    conn = sqlite3.connect("data/data_history.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS data_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_data(data):
    conn = get_connection()
    conn.execute(
        """INSERT OR REPLACE INTO data_history (id, data, timestamp) VALUES (1, ?, ?)""",
        (data, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()

def get_last_data_record():
    conn = get_connection()
    row = conn.execute(""" SELECT * FROM data_history ORDER BY id DESC LIMIT 1""").fetchone()
    conn.close()
    return row