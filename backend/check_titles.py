import sqlite3

conn = sqlite3.connect('knu_mla_v7.db')
cursor = conn.cursor()

cursor.execute('SELECT chat_session_id, title, user_lang, created_at FROM chat_session ORDER BY created_at DESC LIMIT 5')
print('Chat Sessions:')
for row in cursor.fetchall():
    print(f'  ID: {row[0]}, Title: {row[1]}, Lang: {row[2]}, Created: {row[3]}')

cursor.execute('SELECT COUNT(*) FROM chat_message')
print(f'\nTotal messages: {cursor.fetchone()[0]}')

conn.close()
