import sqlite3

conn = sqlite3.connect('backend/knu_mla.db')
cursor = conn.cursor()

print("=== CHAT SESSIONS ===")
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

print("\n=== CHAT MESSAGES ===")
cursor.execute('SELECT message_id, chat_session_id, role, content FROM chat_messages ORDER BY created_at DESC LIMIT 5')
messages = cursor.fetchall()
if messages:
    for row in messages:
        content_preview = row[3][:50] + '...' if len(row[3]) > 50 else row[3]
        print(f"Msg ID: {row[0]}, Session: {row[1]}, Role: {row[2]}, Content: {content_preview}")
else:
    print("No messages found")

cursor.execute('SELECT COUNT(*) FROM chat_messages')
total_msgs = cursor.fetchone()[0]
print(f"\nTotal messages: {total_msgs}")

conn.close()
