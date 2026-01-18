"""
Test script to verify auto title generation
"""
import requests
import json

# Login first
login_response = requests.post(
    "http://127.0.0.1:8000/auth/login",
    json={"user_id": "test_user_v7", "password": "test123456"}
)

if login_response.status_code != 200:
    print(f"Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Send a test message
print("Sending test message...")
chat_response = requests.post(
    "http://127.0.0.1:8000/chat/message",
    headers=headers,
    json={"message": "What is Python programming language?"}
)

if chat_response.status_code != 200:
    print(f"Chat failed: {chat_response.text}")
    exit(1)

result = chat_response.json()
print(f"\nChat response: {json.dumps(result, indent=2)}")

session_id = result.get("data", {}).get("chat_session_id")
if session_id:
    print(f"\nChat session ID: {session_id}")
    
    # Check if title was generated
    import sqlite3
    conn = sqlite3.connect('knu_mla_v7.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, user_lang FROM chat_session WHERE chat_session_id = ?', (session_id,))
    row = cursor.fetchone()
    if row:
        print(f"Title: {row[0]}")
        print(f"Language: {row[1]}")
    conn.close()
else:
    print("No session ID returned!")
