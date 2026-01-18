import sqlite3
import os

db_path = 'backend/knu_mla_v7.db'
if not os.path.exists(db_path):
    if os.path.exists('knu_mla_v7.db'):
        db_path = 'knu_mla_v7.db'
    print(f"Database not found at {db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tables = ["chat_message", "chat_message_v3", "chat_messages"]
for t in tables:
    print(f"\n--- {t} ---")
    try:
        cursor.execute(f"PRAGMA table_info({t})")
        cols = cursor.fetchall()
        print(f"--- Columns for {t} ---")
        col_names = [c[1] for c in cols]
        print(f"Columns: {col_names}")
        print(f"Has request_id: {'request_id' in col_names}")
    except Exception as e:
        print(f"Error checking {t}: {e}")

conn.close()
