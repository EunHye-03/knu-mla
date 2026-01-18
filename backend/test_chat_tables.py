import sqlite3

db_path = 'C:/Users/ASUS/Desktop/knu mla/backend/knu_mla_v7.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== CHAT SESSION TABLE (singular) ===")
try:
    cursor.execute('SELECT chat_session_id, user_idx, title, created_at FROM chat_session ORDER BY created_at DESC LIMIT 10')
    sessions = cursor.fetchall()
    if sessions:
        for row in sessions:
            print(f"ID: {row[0]}, User: {row[1]}, Title: {row[2]}, Created: {row[3]}")
    else:
        print("No chat sessions found (table is empty)")
    
    cursor.execute('SELECT COUNT(*) FROM chat_session')
    total = cursor.fetchone()[0]
    print(f"\nTotal sessions: {total}")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

print("\n=== CHAT MESSAGE TABLE ===")
try:
    cursor.execute('SELECT message_id, chat_session_id, role, content FROM chat_message ORDER BY created_at DESC LIMIT 5')
    messages = cursor.fetchall()
    if messages:
        for row in messages:
            content_preview = row[3][:50] + '...' if len(row[3]) > 50 else row[3]
            print(f"Msg ID: {row[0]}, Session: {row[1]}, Role: {row[2]}, Content: {content_preview}")
    else:
        print("No messages found (table is empty)")
    
    cursor.execute('SELECT COUNT(*) FROM chat_message')
    total_msgs = cursor.fetchone()[0]
    print(f"\nTotal messages: {total_msgs}")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

print("\n=== USERS TABLE ===")
try:
    cursor.execute('SELECT user_idx, user_id, nickname FROM users LIMIT 5')
    users = cursor.fetchall()
    if users:
        for row in users:
            print(f"User IDX: {row[0]}, User ID: {row[1]}, Nickname: {row[2]}")
    else:
        print("No users found")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

conn.close()
