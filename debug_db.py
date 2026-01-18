
import sqlite3
import os

db_path = 'backend/knu_mla_v7.db'
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
res = conn.execute("SELECT sql FROM sqlite_master WHERE name='users'").fetchone()
if res:
    print(res[0])
else:
    print("Table 'users' not found")
conn.close()
