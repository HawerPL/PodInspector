from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_readyz():
    r = client.get("/readyz")
    assert r.status_code == 200
