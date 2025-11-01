import json

from fastapi.testclient import TestClient

from backend.app import app


def test_simulate():
    c = TestClient(app)
    r = c.post(
        "/simulate/performance", json={"income": 6000, "expenses": 4000, "debt": 10000}
    )
    assert r.status_code == 200
    assert "score" in r.json()
