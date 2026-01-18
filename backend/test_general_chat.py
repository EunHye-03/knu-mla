import requests
import json

BASE_URL = "http://localhost:8000/api"

print("=== Testing General Chat Endpoint ===\n")

# Login first
login_data = {"user_id": "hoji", "password": "123456"}
print("1. Logging in...")
login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"   ✓ Login successful!")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test general chat
    print("\n2. Testing general chat...")
    chat_data = {"message": "Hello! Can you help me with my studies?"}
    chat_response = requests.post(
        f"{BASE_URL}/chat/message",
        json=chat_data,
        headers=headers
    )
    
    print(f"   Status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        result = chat_response.json()
        print(f"   ✓ Chat successful!")
        print(f"\n   User: {chat_data['message']}")
        print(f"   AI: {result['data']['response']}")
        print(f"   Session ID: {result['data']['chat_session_id']}")
        
        # Test follow-up message
        print("\n3. Testing follow-up message...")
        session_id = result['data']['chat_session_id']
        followup_data = {"message": "What's the best way to study for exams?"}
        followup_response = requests.post(
            f"{BASE_URL}/chat/message?chat_session_id={session_id}",
            json=followup_data,
            headers=headers
        )
        
        if followup_response.status_code == 200:
            result2 = followup_response.json()
            print(f"   ✓ Follow-up successful!")
            print(f"\n   User: {followup_data['message']}")
            print(f"   AI: {result2['data']['response']}")
    else:
        print(f"   Error: {chat_response.text}")
else:
    print(f"   Login failed: {login_response.text}")
