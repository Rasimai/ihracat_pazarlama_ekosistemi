from fastapi.testclient import TestClient

from api.server import app


def test_directive_post_returns_message():
    c = TestClient(app)
    r = c.post("/api/directive", json={"text": "Berlin’de 2 km yatak ara"})
    assert r.status_code == 200
    j = r.json()
    assert "message" in j and "intent_guess" in j
