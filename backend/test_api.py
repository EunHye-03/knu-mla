import requests
import json

# Test if backend is running
BASE_URL = "http://localhost:8000/api"

# First, let's try to login
print("=== Testing Backend Connection ===")
try:
    # Test login
    login_data = {
        "user_id": "hoji",
        "password": "123456"  # Adjust if needed
    }
    
    print(f"\n1. Testing login...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        token = token_data.get("access_token")
        print(f"   ✓ Login successful! Token: {token[:20]}...")
        
        # Test translate endpoint
        print(f"\n2. Testing translate endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        translate_data = {
            "text": "Hello world",
            "target_lang": "ko"
        }
        
        translate_response = requests.post(
            f"{BASE_URL}/translate",
            json=translate_data,
            headers=headers
        )
        print(f"   Status: {translate_response.status_code}")
        if translate_response.status_code == 200:
            result = translate_response.json()
            print(f"   ✓ Translation successful!")
            print(f"   Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # Check if chat_session_id is in response
            if result.get("data", {}).get("chat_session_id"):
                print(f"   ✓ chat_session_id returned: {result['data']['chat_session_id']}")
            else:
                print(f"   ✗ chat_session_id NOT in response!")
        else:
            print(f"   Error: {translate_response.text}")
            
        # Test chat history endpoint
        print(f"\n3. Testing chat history endpoint...")
        history_response = requests.get(
            f"{BASE_URL}/chat",
            headers=headers
        )
        print(f"   Status: {history_response.status_code}")
        if history_response.status_code == 200:
            history = history_response.json()
            print(f"   Response: {json.dumps(history, indent=2, ensure_ascii=False)}")
        else:
            print(f"   Error: {history_response.text}")
    else:
        print(f"   Login failed: {login_response.text}")
        
except requests.exceptions.ConnectionError:
    print("   ✗ Cannot connect to backend! Is the server running on port 8000?")
except Exception as e:
    print(f"   Error: {e}")
