import sqlite3
from app.config import DATABASE_URL

def get_conn():
    path = DATABASE_URL.replace("sqlite:///", "")
    return sqlite3.connect(path, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages (
        message_id TEXT PRIMARY KEY,
        from_msisdn TEXT,
        to_msisdn TEXT,
        ts TEXT,
        text TEXT,
        created_at TEXT
    )""")
    conn.commit(); conn.close()
