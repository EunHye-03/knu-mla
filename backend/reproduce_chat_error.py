import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8001/api"

def login(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {"username": email, "password": password} # Changed to username as per OAuth2 spec usually, checking auth router might be needed
    # Let's check auth_router.py to be sure about the payload
    # Actually, often it's form data or json. I'll assume JSON first or check code.
    # Looking at api.ts: body: JSON.stringify({ user_id: userId, password })
    # Wait, api.ts sends user_id, not username? 
    # Let me double check api.ts again.
    # api.ts: body: JSON.stringify({ user_id: userId, password }) -> '/auth/login'
    
    payload = {"user_id": email, "password": password}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Login failed: {response.text}")
        return None

def test_chat(token):
    url = f"{BASE_URL}/chat/message"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": "Hello, this is a test message."}
    
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 500:
        print("Successfully reproduced 500 Error.")
    else:
        print("Did not reproduce 500 Error.")

if __name__ == "__main__":
    # user_id = "testuser" # I need a valid user. 
    # I will try to use a known user or register one. 
    # Let's try to assume there is a user 'test' or 'admin' or just register one.
    # Better to check db or define a user.
    # I'll rely on the user providing one or I'll try to register 'debug_user'.
    
    # Registering a debug user to be sure
    reg_url = f"{BASE_URL}/auth/register"
    reg_payload = {
        "user_id": "debug_user_001",
        "nickname": "Debugger",
        "password": "password123",
        "email": "debug@example.com",
        "user_lang": "en"
    }
    requests.post(reg_url, json=reg_payload) # Ignore error if exists
    
    token_data = login("debug_user_001", "password123")
    if token_data:
        test_chat(token_data["access_token"])
    else:
        print("Could not get token.")
