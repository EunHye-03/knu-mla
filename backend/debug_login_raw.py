import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def debug_login():
    print("Attempting login...")
    # Use the credentials that we know exist or try to register first
    login_data = {"user_id": "debug_user", "password": "password123"}
    
    try:
        # 1. Try Login
        resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        print(f"Status Code: {resp.status_code}")
        print("Raw Response:")
        print(resp.text)
        
        if resp.status_code == 200:
            print("Login SUCCESS")
        else:
            print("Login FAILED")
            # If 404/401, maybe try to register
            if "User not found" in resp.text or "Invalid credentials" in resp.text:
                print("Registering user...")
                reg_data = {
                    "user_id": "debug_user", 
                    "email": "debug_raw@example.com", 
                    "password": "password123", 
                    "nickname": "DebugRaw", 
                    "user_lang": "en"
                }
                requests.post(f"{BASE_URL}/auth/register", json=reg_data)
                print("Retrying login...")
                resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
                print(f"Retry Status Code: {resp.status_code}")
                print(f"Retry Raw Response: {resp.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_login()
