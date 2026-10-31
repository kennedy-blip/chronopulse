# src/database/db_manager.py
import sqlite3
import os

DB_PATH = "chronopulse.db"

def init_db():
    os.makedirs("src/database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            epoch_reached INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_run(score, epoch_reached):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO runs (score, epoch_reached) VALUES (?, ?)", (score, epoch_reached))
    conn.commit()
    conn.close()

def get_high_score():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(score) FROM runs")
    res = cursor.fetchone()
    conn.close()
    return res[0] if res and res[0] else 0