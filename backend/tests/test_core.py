import pytest
from httpx import AsyncClient
from app.temp_app import app

@pytest.mark.asyncio
async def test_healthz_readyz():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/healthz")
        assert res.status_code == 200
        res = await ac.get("/readyz")
        assert res.status_code == 200

@pytest.mark.asyncio
async def test_signup_login_me():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user = {"name":"Admin","email":"admin@mind.com","password":"123456","bio":""}
        await ac.post("/users/", json=user)
        login = await ac.post("/users/login", json={"email":"admin@mind.com","password":"123456"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        me = await ac.get("/users/me", headers=headers)
        assert me.status_code == 200
