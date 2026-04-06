import sqlite3
from backend.config import DATABASE_PATH

def get_all_apis():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM apis")
    apis = c.fetchall()
    conn.close()
    return apis

def update_api_status(api_id, status, latency=None, success_rate=None):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    update_query = "UPDATE apis SET status = ?" 
    params = [status]
    if latency is not None:
        update_query += ", latency = ?"
        params.append(latency)
    if success_rate is not None:
        update_query += ", success_rate = ?"
        params.append(success_rate)
    update_query += " WHERE id = ?"
    params.append(api_id)
    c.execute(update_query, tuple(params))
    conn.commit()
    conn.close()
