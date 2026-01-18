
import requests
import json
import sys
import os

BASE_URL = "http://127.0.0.1:8001/api"

def test_endpoint(name, method, url, data, headers):
    print(f"\n--- Testing {name} ---")
    try:
        if method == "POST":
            resp = requests.post(url, json=data, headers=headers)
        else:
            resp = requests.get(url, headers=headers)
        
        print(f"Status: {resp.status_code}")
        try:
            print(f"Response: {json.dumps(resp.json(), indent=2)}")
        except:
            print(f"Response (Text): {resp.text}")
            
        return resp.status_code == 200
    except Exception as e:
        print(f"Error testing {name}: {e}")
        return False

def run_tests():
    # Login
    print("--- Login ---")
    login_data = {"user_id": "debug_user", "password": "password123"}
    resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if resp.status_code != 200:
        print("Login failed, trying to register...")
        requests.post(f"{BASE_URL}/auth/register", json={
            "user_id": "debug_user", "email": "debug@example.com", "password": "password123", "nickname": "Debug", "user_lang": "en"
        })
        resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if resp.status_code != 200:
            print("FATAL: Could not login")
            return

    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Chat
    test_endpoint("Chat", "POST", f"{BASE_URL}/chat/message", {"message": "Hello"}, headers)
    
    # 2. Translate
    test_endpoint("Translate", "POST", f"{BASE_URL}/translate", {"text": "Hello world", "target_lang": "ko"}, headers)
    
    # 3. Summarize
    test_endpoint("Summarize", "POST", f"{BASE_URL}/summarize", {"text": "This is a long text to summarize."}, headers)

if __name__ == "__main__":
    run_tests()
