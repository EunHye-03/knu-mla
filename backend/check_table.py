import sqlite3
import os

db_path = 'knu_mla_v7.db'
if not os.path.exists(db_path):
    print(f"Database {db_path} not found")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password_reset_token'")
    if cursor.fetchone():
        print("Table 'password_reset_token' exists")
    else:
        print("Table 'password_reset_token' is MISSING")
    conn.close()
