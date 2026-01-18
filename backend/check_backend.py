import requests
import json

BASE_URL = "http://localhost:8000/api"

print("=== Checking Backend Status ===\n")

# 1. Check health
print("1. Checking /api/health...")
try:
    health = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {health.status_code}")
    if health.status_code == 200:
        print(f"   ✓ Backend is running!")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# 2. Check if chat endpoint exists
print("\n2. Checking if /api/chat/message exists...")
try:
    # This will fail with 401 (auth required) but that's OK - it means endpoint exists
    response = requests.post(f"{BASE_URL}/chat/message", json={"message": "test"})
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print(f"   ✓ Endpoint exists (requires auth)")
    elif response.status_code == 404:
        print(f"   ✗ Endpoint NOT FOUND!")
        print(f"   Response: {response.text}")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# 3. Check OpenAPI docs
print("\n3. Checking OpenAPI docs...")
try:
    docs = requests.get("http://localhost:8000/openapi.json")
    if docs.status_code == 200:
        openapi = docs.json()
        paths = openapi.get("paths", {})
        
        # Check if our endpoint is registered
        if "/api/chat/message" in paths:
            print(f"   ✓ /api/chat/message is registered!")
        else:
            print(f"   ✗ /api/chat/message NOT in OpenAPI schema")
            print(f"   Available endpoints:")
            for path in sorted(paths.keys()):
                if "chat" in path.lower():
                    print(f"     - {path}")
except Exception as e:
    print(f"   Error: {e}")

print("\n=== Summary ===")
print("If endpoint is NOT FOUND, the server needs to be restarted.")
print("The --reload flag should have auto-reloaded, but sometimes it doesn't catch new files.")
