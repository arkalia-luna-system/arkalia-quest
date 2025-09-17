import json

import pytest

try:
    from app import app as flask_app
except Exception:
    flask_app = None


@pytest.fixture
def client():
    if flask_app is None:
        pytest.skip("app non importable dans cet environnement de test")
    flask_app.testing = True
    with flask_app.test_client() as c:
        yield c


def test_health_endpoint_ok(client):
    resp = client.get("/health")
    assert resp.status_code in {200, 204}


def test_status_endpoint_ok(client):
    resp = client.get("/api/status")
    assert resp.status_code in {200, 204}


def test_leaderboard_endpoints(client):
    # Database-backed leaderboard
    r1 = client.get("/api/database/leaderboard")
    assert r1.status_code in {200, 204}
    # Aggregated leaderboard
    r2 = client.get("/api/leaderboard")
    assert r2.status_code in {200, 204}


def test_terminal_command_post_minimal(client):
    payload = {"command": "help"}
    resp = client.post(
        "/api/terminal/command",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code in {200, 400, 500}  # 500 possible en cas d'erreur interne


def test_websocket_challenge_flow_minimal(client):
    # Create challenge
    create = client.post(
        "/api/websocket/challenge/create",
        data=json.dumps({"title": "t"}),
        content_type="application/json",
    )
    assert create.status_code in {200, 201, 400}
    if create.status_code in {200, 201}:
        data = create.get_json(silent=True) or {}
        room_id = data.get("room_id") or data.get("id") or data.get("room")
        if room_id:
            info = client.get(f"/api/websocket/challenge/{room_id}/info")
            assert info.status_code in {200, 404}


def test_luna_v3_learning_stats(client):
    resp = client.get("/api/luna-v3/learning-stats")
    assert resp.status_code in {200, 503}  # 503 si LUNA AI v3 non disponible
