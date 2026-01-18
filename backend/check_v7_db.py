import sqlite3

db_path = 'C:/Users/ASUS/Desktop/knu mla/backend/knu_mla_v7.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"=== Checking database: {db_path} ===\n")

print("EXISTING TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
if tables:
    for table in tables:
        print(f"  - {table[0]}")
else:
    print("  (no tables)")

print("\n=== CHAT SESSIONS ===")
try:
    cursor.execute('SELECT chat_session_id, user_idx, title, created_at FROM chat_sessions ORDER BY created_at DESC LIMIT 10')
    sessions = cursor.fetchall()
    if sessions:
        for row in sessions:
            print(f"ID: {row[0]}, User: {row[1]}, Title: {row[2]}, Created: {row[3]}")
    else:
        print("No chat sessions found")
    
    cursor.execute('SELECT COUNT(*) FROM chat_sessions')
    total = cursor.fetchone()[0]
    print(f"\nTotal sessions: {total}")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

conn.close()
