import sys
sys.path.append('.')
from app import app
import pytest

@pytest.fixture
def client():
    return app.test_client()

def test_oracle_get(client):
    r = client.get("/oracle")
    assert r.status_code == 200
    assert b"Oracle d" in r.data

def test_oracle_reply(client):
    r = client.post("/oracle", data={"question": "Quel est mon dragon ?"})
    assert b"dragon" in r.data or b"myst" in r.data 