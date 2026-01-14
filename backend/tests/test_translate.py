import pytest
import httpx

# Assumption: Backend is running on localhost:8000
BASE_URL = "http://localhost:8000/api/v1"

@pytest.mark.asyncio
async def test_translate_success():
    async with httpx.AsyncClient() as client:
        payload = {
            "text": "Hello world",
            "target_lang": "KR"
        }
        # Verify endpoint path matches your backend
        response = await client.post(f"{BASE_URL}/chat/translate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert isinstance(data["content"], str)

@pytest.mark.asyncio
async def test_translate_empty_input():
    async with httpx.AsyncClient() as client:
        payload = {
            "text": "",
            "target_lang": "KR"
        }
        response = await client.post(f"{BASE_URL}/chat/translate", json=payload)
        # Assuming 400 Bad Request for empty input
        assert response.status_code in [400, 422]

@pytest.mark.asyncio
async def test_translate_invalid_payload():
    async with httpx.AsyncClient() as client:
        payload = {
            "wrong_key": "Hello"
        }
        response = await client.post(f"{BASE_URL}/chat/translate", json=payload)
        assert response.status_code == 422  # Validation Error
