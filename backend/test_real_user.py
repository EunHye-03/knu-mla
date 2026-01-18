import requests
import json

BASE_URL = "http://localhost:8000/api"

print("=== Testing with user 'hoji' ===\n")

# Login
login_data = {"user_id": "hoji", "password": "123456"}
print("1. Logging in...")
login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"   Status: {login_response.status_code}")

if login_response.status_code != 200:
    print(f"   Error: {login_response.text}")
    print("\nTrying with different password...")
    login_data = {"user_id": "hoji", "password": "hoji123"}
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"   ✓ Login successful!")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test translate
    print("\n2. Testing translate...")
    translate_data = {"text": "Hello world", "target_lang": "ko"}
    translate_response = requests.post(f"{BASE_URL}/translate", json=translate_data, headers=headers)
    print(f"   Status: {translate_response.status_code}")
    print(f"   Response: {json.dumps(translate_response.json(), indent=2, ensure_ascii=False)}")
    
    # Check history
    print("\n3. Checking chat history...")
    history_response = requests.get(f"{BASE_URL}/chat", headers=headers)
    print(f"   Status: {history_response.status_code}")
    print(f"   Response: {json.dumps(history_response.json(), indent=2, ensure_ascii=False)}")
else:
    print(f"   Login failed: {login_response.text}")
