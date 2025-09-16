import pytest

from core.profile_manager import ProfileManager


class DummyDB:
    def __init__(self):
        self.saved = {}
        self.profiles = {}

    def load_profile(self, user_id):
        return self.profiles.get(user_id)

    def save_profile(self, user_id, profile):
        self.saved[user_id] = dict(profile)


@pytest.fixture()
def pm():
    p = ProfileManager()
    p.db_manager = DummyDB()
    return p


def test_create_default_profile_has_required_keys(pm):
    prof = pm.create_default_profile()
    assert prof["level"] == 1
    assert "personnalite" in prof and "progression" in prof


def test_ensure_profile_structure_fills_missing_keys(pm):
    partial = {"username": "u1", "level": 3, "personnalite": {"type": "x"}}
    completed = pm.ensure_profile_structure(partial)
    assert completed["level"] == 3
    assert completed["name"] == "Hacker"
    assert completed["progression"]["niveau"] == 1


def test_add_badge_and_add_score_save(pm):
    # Start with persisted profile
    pm.db_manager.profiles["u1"] = pm.create_default_profile()
    pm.add_badge("u1", "BadgeX")
    assert "BadgeX" in pm.db_manager.saved["u1"]["badges"]
    pm.add_score("u1", 250)
    saved = pm.db_manager.saved["u1"]
    assert saved["score"] >= 250
    assert saved["level"] == (saved["score"] // 100) + 1
