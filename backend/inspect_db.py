
import sqlite3

def inspect():
    try:
        conn = sqlite3.connect('knu_mla_v8.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", tables)

        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='chat_message';")
        schema = cursor.fetchone()
        
        if schema:
            print("Schema for chat_message:")
            print(schema[0])
        else:
            print("Table chat_message not found!")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
