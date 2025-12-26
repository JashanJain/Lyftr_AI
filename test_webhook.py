from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_live():
    assert client.get("/health/live").status_code==200
