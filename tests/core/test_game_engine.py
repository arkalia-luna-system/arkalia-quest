import types
from datetime import datetime, timedelta

import pytest

from core.game_engine import GameEngine


class DummyDB:
    def __init__(self):
        self.saved = []
        self.profile = {"xp": 0, "badges": []}

    def load_profile(self, user_id):
        return dict(self.profile)

    def save_profile(self, user_id, profile):
        self.saved.append((user_id, dict(profile)))


class DummyCommandHandler:
    def __init__(self, response):
        self.response = response

    def handle_command(self, command, profile):
        return dict(self.response)


@pytest.fixture()
def engine():
    ge = GameEngine()
    # Monkeypatch DB and command handler to avoid real IO
    ge.db_manager = DummyDB()
    return ge


def test_get_daily_challenges_resets_once_per_day(engine, monkeypatch):
    # Force previous reset to yesterday to trigger a reset
    engine.last_challenge_reset = (datetime.now() - timedelta(days=1)).date()
    # Track that progress resets to 0
    engine.daily_challenges["speed_hacker"]["progress"] = 2
    result = engine.get_daily_challenges("u1")
    assert "challenges" in result
    assert result["challenges"]["speed_hacker"]["progress"] == 0
    # Subsequent call same day should not reset again
    engine.daily_challenges["speed_hacker"]["progress"] = 1
    result2 = engine.get_daily_challenges("u1")
    assert result2["challenges"]["speed_hacker"]["progress"] == 1


def test_check_random_event_triggers_when_under_chance(engine, monkeypatch):
    # Prepare deterministic random
    monkeypatch.setattr("random.random", lambda: 0.0)
    profile = {"xp": 0, "badges": []}
    # Use an event trigger that exists
    result = engine.check_random_event("random_action", profile)
    assert result.get("event_triggered") is True
    assert result.get("profile_updated") is True


def test_execute_random_event_badge_and_random_xp(engine, monkeypatch):
    # Force randint to a fixed number for determinism
    monkeypatch.setattr("random.randint", lambda a, b: 123)
    event = {"effect": {"bonus_xp": "random_50_200", "badge": "Secret Explorer"}}
    profile = {"xp": 0, "badges": []}
    out = engine._execute_random_event(event, profile)
    assert out["effect"]["bonus_xp"] == 123
    assert "Secret Explorer" in profile["badges"]


def test_add_effects_success_adds_matrix_effects_and_rewards(engine, monkeypatch):
    # Stabilize reward calculation timing bonus
    engine.last_action_time = datetime.now()
    profile = {"xp": 0, "current_streak": 3, "level": 1}
    res = engine.add_effects({"réussite": True, "difficulty": "hard", "message": "ok"}, profile)
    eff = res["effect"]
    assert eff["type"] == "success"
    assert eff["color"] == "#00ff00"
    assert eff["reward"]["xp"] >= 10
    assert res.get("instant_rewards") is not None


def test_add_effects_error_branch_has_encouragement(engine, monkeypatch):
    profile = {}
    res = engine.add_effects({"réussite": False, "message": "oops"}, profile)
    eff = res["effect"]
    assert eff["type"] == "error"
    assert "encouragement" in eff


def test_process_command_saves_profile_when_updated(engine, monkeypatch):
    # Inject command handler to set profile_updated
    engine.command_handler = DummyCommandHandler(
        {"profile_updated": True, "réussite": True, "message": "ok"}
    )
    out = engine.process_command("any", user_id="u1")
    # DB save should have been called
    assert engine.db_manager.saved
    assert out.get("effect") is not None
