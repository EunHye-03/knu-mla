import sqlite3

conn = sqlite3.connect('backend/knu_mla_v7.db')
cursor = conn.cursor()

print("=== EXISTING TABLES ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f"  - {table[0]}")

conn.close()
