import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key found: {api_key[:20]}..." if api_key else "No API key!")

if not api_key:
    print("ERROR: OPENAI_API_KEY not set in .env file")
    exit(1)

print("\n=== Testing OpenAI API ===\n")

try:
    client = OpenAI(api_key=api_key, timeout=60.0)
    
    print("1. Testing simple completion...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello World' in Korean"}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    result = response.choices[0].message.content
    print(f"   ✓ Success!")
    print(f"   Response: {result}")
    
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    
    # Check if it's an authentication error
    if "authentication" in str(e).lower() or "api key" in str(e).lower():
        print("\n   → API key is invalid or expired")
        print("   → Please update OPENAI_API_KEY in backend/.env")
    elif "quota" in str(e).lower():
        print("\n   → API quota exceeded")
        print("   → Check your OpenAI account billing")
    elif "rate limit" in str(e).lower():
        print("\n   → Rate limit exceeded")
        print("   → Wait a moment and try again")
