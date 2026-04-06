import sqlite3
import os
from backend.config import DATABASE_PATH

def init_db():
    """Initialize the SQLite database and create necessary tables."""
    # Ensure the database directory exists
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    # APIs table
    c.execute("""
    CREATE TABLE IF NOT EXISTS apis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT UNIQUE,
        provider TEXT,
        auth_type TEXT,
        success_rate REAL DEFAULT 0.0,
        latency REAL DEFAULT 0.0,
        last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active'
    )
    """)

    # Knowledge table
    c.execute("""
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        content TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tools table
    c.execute("""
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        capabilities TEXT,
        last_used TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

if __name__ == "__main__":
    init_db()
