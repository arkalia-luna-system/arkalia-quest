import pytest

from core.mission_unified import MissionUnified


class DummyDB:
    def __init__(self, missions):
        self._missions = missions

    def load_all_missions(self):
        return list(self._missions.values())


@pytest.fixture
def handler():
    missions = {
        "prologue": {
            "mission_id": "prologue",
            "etapes": [
                {"id": "s1", "commande": "luna_ping", "recompense": 5},
                {"id": "s2", "commande": "analyser_code", "recompense": 5},
            ],
            "recompense": 20,
            "objet_symbolique": "cle_prologue",
        },
        "acte_1": {
            "mission_id": "acte_1",
            "etapes": [{"id": "a1s1", "commande": "coder_algo", "recompense": 10}],
            "recompense": 30,
        },
    }
    h = MissionUnified()
    h.db_manager = DummyDB(missions)
    h.load_all_data()
    return h


def test_get_current_acte_progression(handler):
    profil = {"missions_completed": ["prologue"]}
    assert handler.get_current_acte(profil) == "acte_1"


def test_execute_mission_step_and_completion(handler):
    profil = {}
    # Step 1
    r1 = handler.execute_mission_step("prologue", "s1", profil)
    assert r1["success"] is True
    assert profil["points"] == 5
    # Step 2 triggers mission complete
    r2 = handler.execute_mission_step("prologue", "s2", profil)
    assert r2["success"] is True
    assert "prologue" in profil.get("missions_completed", [])
    assert "cle_prologue" in profil.get("objets_debloques", [])


def test_get_mission_progress(handler):
    profil = {"etapes_completed": {"prologue": ["s1"]}}
    progress = handler.get_mission_progress("prologue", profil)
    assert progress["etapes_total"] == 2
    assert progress["progress"] == 50.0
