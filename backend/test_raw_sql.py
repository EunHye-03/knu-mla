import sqlite3
import uuid

conn = sqlite3.connect('backend/knu_mla_v7.db')
cursor = conn.cursor()

try:
    print("Attempting raw insert...")
    # Get max session
    cursor.execute("SELECT MAX(chat_session_id) FROM chat_session")
    sid = cursor.fetchone()[0]
    if not sid: sid = 1
    
    req_id = str(uuid.uuid4())
    
    # Insert
    sql = """
    INSERT INTO chat_message (chat_session_id, role, feature_type, content, source_lang, target_lang, request_id, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """
    params = (sid, "user", "translate", "Raw Content", "en", "ko", req_id)
    
    cursor.execute(sql, params)
    conn.commit()
    print("Raw insert SUCCESS!")
except Exception as e:
    print(f"Raw insert FAILED: {e}")
finally:
    conn.close()
