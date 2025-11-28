import pytest
from httpx import AsyncClient, ASGITransport
from .main import app

@pytest.mark.asyncio
async def test_create_short_url():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://0.0.0.0") as client:

        response = await client.post("/shorten", json={"url": "https://example.com/long/path"})
        assert response.status_code == 200
        data = response.json()
        assert "short_url" in data
        assert len(data["short_url"].split("/")[-1]) == 5

@pytest.mark.asyncio
async def test_redirect_short_url():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://0.0.0.0") as client:

        post_resp = await client.post("/shorten", json={"url": "https://example.com/long/path"})
        short_url = post_resp.json()["short_url"]
        short_code = short_url.split("/")[-1]


        redirect_resp = await client.get(f"/{short_code}", follow_redirects=False)
        assert redirect_resp.status_code in (301, 307, 302)
        assert redirect_resp.headers["location"] == "https://example.com/long/path"
