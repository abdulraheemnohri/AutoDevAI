import sqlite3
from backend.config import DATABASE_PATH

def get_knowledge_by_tag(tag):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM knowledge WHERE tags LIKE ?", (f"%{tag}%",))
    knowledge = c.fetchall()
    conn.close()
    return [item[0] for item in knowledge]
