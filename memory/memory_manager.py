import sqlite3
import os
import logging

logger = logging.getLogger(__name__)
DB_PATH = "data/assistant.db"

def _get_conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def remember_fact(fact: str):
    """Ulozi fakt do pameti."""
    conn = _get_conn()
    conn.execute("INSERT INTO memory (key, value) VALUES (?, ?)", ("fact", fact))
    conn.commit()
    conn.close()
    logger.info(f"Zapamatovano: {fact}")

def forget_fact(fact: str):
    """Smaze fakt z pameti."""
    conn = _get_conn()
    conn.execute("DELETE FROM memory WHERE value LIKE ?", (f"%{fact}%",))
    conn.commit()
    conn.close()
    logger.info(f"Zapomenuto: {fact}")

def show_all_memory() -> list:
    """Vrati vsechny zapamatovane fakty."""
    conn = _get_conn()
    cursor = conn.execute("SELECT value FROM memory ORDER BY created_at DESC")
    rows = [row[0] for row in cursor.fetchall()]
    conn.close()
    return rows

def get_user_name() -> str:
    """Zkusi najit jmeno uzivatele v pameti."""
    conn = _get_conn()
    cursor = conn.execute(
        "SELECT value FROM memory WHERE value LIKE '%jmenuji se%' OR value LIKE '%jmeno%' ORDER BY created_at DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        val = row[0]
        for word in ["jmenuji se", "jmeno je", "moje jmeno"]:
            if word in val:
                return val.replace(word, "").strip()
        return val
    return ""

def clear_memory():
    """Smaze celou pamet."""
    conn = _get_conn()
    conn.execute("DELETE FROM memory")
    conn.commit()
    conn.close()
    logger.info("Pamet smazana.")
