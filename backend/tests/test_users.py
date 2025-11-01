from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_users_create_and_login():
    # cria usuário
    r = client.post("/users/", json={"name":"Chefao","email":"boss@mind.com","password":"123456"})
    assert r.status_code in (200,201,400)  # 400 se já existir
    # login
    r = client.post("/users/login", json={"email":"boss@mind.com","password":"123456"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token
