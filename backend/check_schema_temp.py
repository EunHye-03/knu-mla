import sqlite3
import os

db_path = 'knu_mla_v7.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n--- chat_message schema ---")
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='chat_message'")
row = cursor.fetchone()
if row:
    print(row[0])
else:
    print("Table chat_session not found")

cursor.execute("PRAGMA table_info(chat_session)")
cols = cursor.fetchall()
for c in cols:
    print(c)

conn.close()
