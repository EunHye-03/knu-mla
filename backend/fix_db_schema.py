import sqlite3
import os

db_path = 'knu_mla_v7.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Beginning schema fix...")
    
    # 1. Rename existing table
    cursor.execute("ALTER TABLE chat_session RENAME TO chat_session_old")
    print("Renamed chat_session to chat_session_old")
    
    # 2. Create new table with CORRECT schema (INTEGER PRIMARY KEY)
    create_sql = """
    CREATE TABLE chat_session (
        chat_session_id INTEGER PRIMARY KEY,
        user_idx INTEGER NOT NULL,
        project_id INTEGER,
        title VARCHAR(200),
        user_lang VARCHAR(2) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(project_id) REFERENCES project (project_session_id) ON DELETE SET NULL
    )
    """
    cursor.execute(create_sql)
    print("Created new chat_session table")
    
    # 3. Copy data
    # Note: We rely on SQLite to move data correctly. We copy keys as is.
    cursor.execute("""
        INSERT INTO chat_session (chat_session_id, user_idx, project_id, title, user_lang, created_at, updated_at)
        SELECT chat_session_id, user_idx, project_id, title, user_lang, created_at, updated_at FROM chat_session_old
    """)
    print("Copied data to new table")
    
    # 4. Drop old table
    cursor.execute("DROP TABLE chat_session_old")
    print("Dropped old table")
    
    conn.commit()
    print("SUCCESS: Schema fixed!")
    
except Exception as e:
    conn.rollback()
    print(f"ERROR: {e}")
    print("Rolled back changes.")

finally:
    conn.close()
