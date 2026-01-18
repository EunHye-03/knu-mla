import sqlite3
import os

db_path = 'backend/knu_mla_v7.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(chat_message)")
for c in cursor.fetchall():
    # cid, name, type, notnull, dflt, pk
    print(f"Col: {c[1]} | Type: {c[2]} | NotNull: {c[3]}")
conn.close()
