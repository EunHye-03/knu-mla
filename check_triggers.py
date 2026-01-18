import sqlite3
conn = sqlite3.connect('backend/knu_mla_v7.db')
cursor = conn.cursor()
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger'")
for row in cursor.fetchall():
    print(f"Trigger: {row[0]}")
    print(f"SQL: {row[1]}")
conn.close()
