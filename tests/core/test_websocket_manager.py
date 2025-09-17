import pytest

from core.websocket_manager import WebSocketManager


@pytest.fixture
def wm():
    return WebSocketManager()


def test_join_and_leave_challenge_flow(wm):
    room_id = wm.create_challenge_room({"mission": {"id": "m1"}})
    resp_join = wm.handle_join_challenge("s1", {"room_id": room_id, "player_name": "A"})
    assert resp_join["type"] == "join_success"
    assert wm.challenge_rooms[room_id] == ["s1"]
    resp_leave = wm.handle_leave_challenge("s1", {"room_id": room_id})
    assert resp_leave["type"] == "leave_success"


def test_start_complete_and_end_challenge(wm):
    room_id = wm.create_challenge_room({"mission": {"id": "m1"}, "timer": 5})
    wm.handle_join_challenge("s1", {"room_id": room_id, "player_name": "A"})
    wm.handle_join_challenge("s2", {"room_id": room_id, "player_name": "B"})

    start = wm.start_challenge(room_id)
    assert start["type"] == "challenge_started"

    # Complete first player
    r1 = wm.complete_mission(room_id, "s1", {"player_name": "A", "completion_time": 10})
    assert r1["type"] in {"mission_completed", "challenge_ended"}

    # Complete second player triggers end
    r2 = wm.complete_mission(room_id, "s2", {"player_name": "B", "completion_time": 8})
    assert r2["type"] == "challenge_ended"
    assert r2.get("winner") in {"A", "B", None}
