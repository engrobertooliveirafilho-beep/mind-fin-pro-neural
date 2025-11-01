import pytest, httpx
BASE = "http://127.0.0.1:8002"

@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{BASE}/health")
        assert r.status_code == 200
        j = r.json()
        assert j["status"] == "ok"

@pytest.mark.asyncio
async def test_signup_login_me():
    async with httpx.AsyncClient() as c:
        user = {"name":"Admin","email":"admin@mind.com","password":"123456","bio":"","ai_profile":""}
        await c.post(f"{BASE}/users/", json=user)  # ok se já existir
        r = await c.post(f"{BASE}/users/login", json={"email":"admin@mind.com","password":"123456"})
        assert r.status_code == 200
        tok = r.json()["access_token"]
        me = await c.get(f"{BASE}/users/me", headers={"Authorization": f"Bearer {tok}"})
        assert me.status_code == 200

@pytest.mark.asyncio
async def test_unauthorized_me():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{BASE}/users/me")
        assert r.status_code == 401

@pytest.mark.asyncio
async def test_email_conflict():
    async with httpx.AsyncClient() as c:
        user = {"name":"Dup","email":"admin@mind.com","password":"123456","bio":"","ai_profile":""}
        r = await c.post(f"{BASE}/users/", json=user)
        assert r.status_code in (400, 409)
