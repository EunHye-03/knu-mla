import sqlite3
import os

db_path = 'knu_mla_v7.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Beginning chat_message schema fix...")
    
    # 1. Rename existing table
    cursor.execute("ALTER TABLE chat_message RENAME TO chat_message_old")
    print("Renamed chat_message to chat_message_old")
    
    # 2. Create new table with CORRECT schema (INTEGER PRIMARY KEY) and FK
    create_sql = """
    CREATE TABLE chat_message (
        message_id INTEGER PRIMARY KEY,
        chat_session_id INTEGER NOT NULL,
        role VARCHAR(9) NOT NULL,
        feature_type VARCHAR(13) NOT NULL,
        content TEXT NOT NULL,
        source_lang VARCHAR(2),
        target_lang VARCHAR(2),
        request_id VARCHAR(64),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(chat_session_id) REFERENCES chat_session (chat_session_id) ON DELETE CASCADE
    )
    """
    cursor.execute(create_sql)
    print("Created new chat_message table")
    
    # 3. Copy data
    cursor.execute("""
        INSERT INTO chat_message (message_id, chat_session_id, role, feature_type, content, source_lang, target_lang, request_id, created_at)
        SELECT message_id, chat_session_id, role, feature_type, content, source_lang, target_lang, request_id, created_at FROM chat_message_old
    """)
    print("Copied data to new table")
    
    # 4. Drop old table
    cursor.execute("DROP TABLE chat_message_old")
    print("Dropped old table")
    
    conn.commit()
    print("SUCCESS: chat_message schema fixed!")
    
except Exception as e:
    conn.rollback()
    print(f"ERROR: {e}")
    # print full traceback
    import traceback
    traceback.print_exc()

finally:
    conn.close()
