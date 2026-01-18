import requests

print("=== Testing endpoints ===\n")

# Test root
print("1. Testing http://localhost:8000/")
try:
    response = requests.get("http://localhost:8000/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Test /docs
print("\n2. Testing http://localhost:8000/docs")
try:
    response = requests.get("http://localhost:8000/docs")
    print(f"   Status: {response.status_code}")
except Exception as e:
    print(f"   Error: {e}")

# Test /api/docs
print("\n3. Testing http://localhost:8000/api/docs")
try:
    response = requests.get("http://localhost:8000/api/docs")
    print(f"   Status: {response.status_code}")
except Exception as e:
    print(f"   Error: {e}")

# Test /health
print("\n4. Testing http://localhost:8000/health")
try:
    response = requests.get("http://localhost:8000/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test /api/health
print("\n5. Testing http://localhost:8000/api/health")
try:
    response = requests.get("http://localhost:8000/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test /auth/login
print("\n6. Testing http://localhost:8000/auth/login")
try:
    response = requests.post("http://localhost:8000/auth/login", json={"user_id": "test", "password": "test"})
    print(f"   Status: {response.status_code}")
except Exception as e:
    print(f"   Error: {e}")
