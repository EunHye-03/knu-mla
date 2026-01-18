import sqlite3
import os

db_path = 'backend/knu_mla_v7.db'
if not os.path.exists(db_path):
    print(f"DB not found: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("PRAGMA table_info(chat_message)")
    cols = cursor.fetchall()
    col_names = [c[1] for c in cols]
    
    if "request_id" not in col_names:
        print("Adding request_id column...")
        cursor.execute("ALTER TABLE chat_message ADD COLUMN request_id TEXT")
        conn.commit()
        print("Column added.")
    else:
        print("request_id column already exists.")

except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
