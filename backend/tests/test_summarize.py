import pytest
import httpx

BASE_URL = "http://localhost:8000/api/v1"

@pytest.mark.asyncio
async def test_summarize_success():
    async with httpx.AsyncClient() as client:
        payload = {
            "text": "The mitochondria is the powerhouse of the cell. It generates most of the cell's supply of adenosine triphosphate (ATP), used as a source of chemical energy."
        }
        response = await client.post(f"{BASE_URL}/chat/summarize", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) < len(payload["text"])

@pytest.mark.asyncio
async def test_summarize_short_text():
    async with httpx.AsyncClient() as client:
        payload = {
            "text": "Too short"
        }
        response = await client.post(f"{BASE_URL}/chat/summarize", json=payload)
        # Should either work or return 400 depending on logic
        assert response.status_code in [200, 400]

@pytest.mark.asyncio
async def test_summarize_missing_field():
    async with httpx.AsyncClient() as client:
        payload = {}
        response = await client.post(f"{BASE_URL}/chat/summarize", json=payload)
        assert response.status_code == 422
