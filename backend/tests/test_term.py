import pytest
import httpx

BASE_URL = "http://localhost:8000/api/v1"

@pytest.mark.asyncio
async def test_explain_term_success():
    async with httpx.AsyncClient() as client:
        payload = {
            "term": "Quantum Entanglement"
        }
        response = await client.post(f"{BASE_URL}/chat/explain", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 10

@pytest.mark.asyncio
async def test_explain_empty_term():
    async with httpx.AsyncClient() as client:
        payload = {
            "term": ""
        }
        response = await client.post(f"{BASE_URL}/chat/explain", json=payload)
        assert response.status_code in [400, 422]

@pytest.mark.asyncio
async def test_explain_malformed_json():
    async with httpx.AsyncClient() as client:
        # Sending raw string instead of JSON
        response = await client.post(
            f"{BASE_URL}/chat/explain", 
            content="Not JSON", 
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]
