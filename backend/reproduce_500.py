
import requests
import json
import sys
import os

BASE_URL = "http://127.0.0.1:8000"

def reproduce():
    # Login first
    login_data = {"user_id": "debug_user", "password": "password123"}
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if resp.status_code != 200:
            print("Login failed, trying to register...", resp.text)
            requests.post(f"{BASE_URL}/auth/register", json={
                "user_id": "debug_user", "email": "debug@example.com", "password": "password123", "nickname": "Debug", "user_lang": "en"
            })
            resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            if resp.status_code != 200:
                print(f"Login failed FATAL: {resp.text}")
                return

        token = resp.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}

        print("Sending chat message...")
        chat_payload = {"message": "Hello AI"}
        resp = requests.post(f"{BASE_URL}/chat/message", json=chat_payload, headers=headers)
        
        print(f"Status: {resp.status_code}")
        try:
            print(f"Response: {json.dumps(resp.json(), indent=2)}")
        except:
            print(f"Response: {resp.text}")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Script Error: {e}")

if __name__ == "__main__":
    reproduce()
