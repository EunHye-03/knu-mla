import sqlite3
conn = sqlite3.connect('backend/knu_mla_v7.db')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='chat_message'")
print(cursor.fetchone()[0])
conn.close()
