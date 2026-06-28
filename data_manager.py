import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
DB_PATH = "data/assistant.db"

def _get_conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_input TEXT,
            action TEXT,
            response TEXT,
            error TEXT
        )
    """)
    conn.commit()
    return conn

def save_interaction(user_input: str, action: str, response: str, error: str):
    """Ulozi interakci do databaze."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO history (timestamp, user_input, action, response, error) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), user_input or "", action or "", response or "", error or "")
    )
    conn.commit()
    conn.close()
    logger.debug(f"Interakce ulozena: {user_input} -> {action}")

def get_last_history(n: int = 10) -> list:
    """Vrati poslednich n interakci."""
    conn = _get_conn()
    cursor = conn.execute(
        "SELECT timestamp, user_input, action, response, error FROM history ORDER BY id DESC LIMIT ?",
        (n,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_history():
    """Smaze celou historii."""
    conn = _get_conn()
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    logger.info("Historie smazana.")
