from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_messages():
    r=client.get("/messages")
    assert r.status_code==200
