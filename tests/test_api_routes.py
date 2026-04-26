"""
Tests des routes API — LUNA Hors Connexion.
Vérifie les endpoints /api/story/* en mode test Flask.
"""

import os
import sys
from collections.abc import Generator
from typing import Any, cast

import pytest
from flask.testing import FlaskClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app

COOKIE_NAME = "luna_player_id"


@pytest.fixture(scope="module")
def client() -> Generator[FlaskClient, None, None]:
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def json_obj(resp: Any) -> dict[str, Any]:
    return cast(dict[str, Any], resp.get_json())


# ─────────────────────────────────────────────
# GET /api/story/state
# ─────────────────────────────────────────────


class TestGetState:
    def test_returns_200(self, client: FlaskClient) -> None:
        r = client.get("/api/story/state")
        assert r.status_code == 200

    def test_success_flag(self, client: FlaskClient) -> None:
        r = client.get("/api/story/state")
        data = json_obj(r)
        assert data["success"] is True

    def test_contains_expected_fields(self, client: FlaskClient) -> None:
        r = client.get("/api/story/state")
        data = json_obj(r)
        for field in [
            "scene_id",
            "chapter_id",
            "dialogue",
            "choices",
            "luna_trust",
            "xp",
        ]:
            assert field in data, f"Champ manquant: {field}"

    def test_sets_cookie(self) -> None:
        """Le cookie est bien posé pour un tout nouveau client."""
        from app import create_app

        fresh_app = create_app()
        fresh_app.config["TESTING"] = True
        with fresh_app.test_client() as fresh:
            r = fresh.get("/api/story/state")
            # Cookie present either in Set-Cookie header or accessible via jar
            cookie_set = COOKIE_NAME in r.headers.get("Set-Cookie", "")
            cookie_jar = fresh.get_cookie(COOKIE_NAME)
            assert cookie_set or (cookie_jar is not None)

    def test_cookie_persists_state(self, client: FlaskClient) -> None:
        r1 = client.get("/api/story/state")
        d1 = json_obj(r1)
        r2 = client.get("/api/story/state")
        d2 = json_obj(r2)
        assert d1["scene_id"] == d2["scene_id"]

    def test_scene_progress_present(self, client: FlaskClient) -> None:
        r = client.get("/api/story/state")
        data = json_obj(r)
        assert "scene_index" in data
        assert "scene_total" in data
        assert data["scene_index"] >= 1
        assert data["scene_total"] >= 1


# ─────────────────────────────────────────────
# POST /api/story/choice
# ─────────────────────────────────────────────


class TestApplyChoice:
    def test_valid_choice(self, client: FlaskClient) -> None:
        r = client.post(
            "/api/story/choice", json={"scene_id": "s0_0", "choice_id": "c0_0_a"}
        )
        data = json_obj(r)
        assert data["success"] is True
        assert "choice_result" in data
        assert "next_state" in data

    def test_missing_scene_id_returns_400(self, client: FlaskClient) -> None:
        r = client.post("/api/story/choice", json={"choice_id": "c0_0_a"})
        assert r.status_code == 400

    def test_missing_choice_id_returns_400(self, client: FlaskClient) -> None:
        r = client.post("/api/story/choice", json={"scene_id": "s0_0"})
        assert r.status_code == 400

    def test_invalid_scene_returns_400(self, client: FlaskClient) -> None:
        r = client.post(
            "/api/story/choice", json={"scene_id": "inexistante", "choice_id": "c0_0_a"}
        )
        assert r.status_code == 400

    def test_invalid_choice_returns_400(self, client: FlaskClient) -> None:
        r = client.post(
            "/api/story/choice", json={"scene_id": "s0_0", "choice_id": "inexistant"}
        )
        assert r.status_code == 400

    def test_xp_in_result(self, client: FlaskClient) -> None:
        r = client.post(
            "/api/story/choice", json={"scene_id": "s0_0", "choice_id": "c0_0_a"}
        )
        data = json_obj(r)
        assert "xp_gained" in data["choice_result"]


# ─────────────────────────────────────────────
# POST /api/story/name
# ─────────────────────────────────────────────


class TestSetName:
    def test_valid_name(self, client: FlaskClient) -> None:
        r = client.post("/api/story/name", json={"name": "Athalia"})
        data = json_obj(r)
        assert data["success"] is True
        assert data["player_name"] == "Athalia"

    def test_name_persisted_in_state(self, client: FlaskClient) -> None:
        client.post("/api/story/name", json={"name": "TestJoueur"})
        r = client.get("/api/story/state")
        data = json_obj(r)
        assert data["player_name"] == "TestJoueur"

    def test_empty_name_returns_400(self, client: FlaskClient) -> None:
        r = client.post("/api/story/name", json={"name": ""})
        assert r.status_code == 400

    def test_name_trimmed_to_30_chars(self, client: FlaskClient) -> None:
        long_name = "A" * 50
        r = client.post("/api/story/name", json={"name": long_name})
        data = json_obj(r)
        assert len(data["player_name"]) <= 30


# ─────────────────────────────────────────────
# GET /api/story/summary
# ─────────────────────────────────────────────


class TestGetSummary:
    def test_returns_200(self, client: FlaskClient) -> None:
        r = client.get("/api/story/summary")
        assert r.status_code == 200

    def test_success_flag(self, client: FlaskClient) -> None:
        r = client.get("/api/story/summary")
        data = json_obj(r)
        assert data["success"] is True

    def test_exists_field(self, client: FlaskClient) -> None:
        r = client.get("/api/story/summary")
        data = json_obj(r)
        assert "exists" in data

    def test_flags_field_present(self, client: FlaskClient) -> None:
        r = client.get("/api/story/summary")
        data = json_obj(r)
        assert "flags" in data


# ─────────────────────────────────────────────
# GET /api/story/journal
# ─────────────────────────────────────────────


class TestGetJournal:
    def test_returns_200(self, client: FlaskClient) -> None:
        r = client.get("/api/story/journal")
        assert r.status_code == 200

    def test_success_flag(self, client: FlaskClient) -> None:
        r = client.get("/api/story/journal")
        data = json_obj(r)
        assert data["success"] is True

    def test_moments_is_list(self, client: FlaskClient) -> None:
        r = client.get("/api/story/journal")
        data = json_obj(r)
        assert isinstance(data["moments"], list)

    def test_journal_generated_with_flags(self, client: FlaskClient) -> None:
        from core.story_save import generate_player_id, save_state

        pid = generate_player_id()
        save_state(
            pid,
            {
                "current_chapter": "chapitre_3",
                "current_scene": "s3_1",
                "luna_trust": 75,
                "xp": 150,
                "flags": ["accepted_chapter_0", "nexus_helped"],
                "chapters_completed": ["chapitre_0", "chapitre_1", "chapitre_2"],
                "endings_unlocked": ["ending_a"],
                "player_name": "Tester",
                "previous_endings": [],
            },
        )
        client.set_cookie("luna_player_id", pid)
        r = client.get("/api/story/journal")
        data = json_obj(r)
        assert data["success"] is True
        assert data["journal"] is not None
        assert len(data["moments"]) >= 2
        assert data["player_name"] == "Tester"


# ─────────────────────────────────────────────
# GET /api/story/leaderboard
# ─────────────────────────────────────────────


class TestLeaderboard:
    def test_returns_200(self, client: FlaskClient) -> None:
        r = client.get("/api/story/leaderboard")
        assert r.status_code == 200

    def test_success_flag(self, client: FlaskClient) -> None:
        r = client.get("/api/story/leaderboard")
        data = json_obj(r)
        assert data["success"] is True

    def test_scores_is_list(self, client: FlaskClient) -> None:
        r = client.get("/api/story/leaderboard")
        data = json_obj(r)
        assert isinstance(data["scores"], list)


# ─────────────────────────────────────────────
# POST /api/story/reset
# ─────────────────────────────────────────────


class TestReset:
    def test_reset_returns_success(self, client: FlaskClient) -> None:
        r = client.post("/api/story/reset")
        data = json_obj(r)
        assert data["success"] is True

    def test_reset_restores_initial_state(self, client: FlaskClient) -> None:
        client.post(
            "/api/story/choice", json={"scene_id": "s0_0", "choice_id": "c0_0_a"}
        )
        client.post("/api/story/reset")
        r = client.get("/api/story/state")
        data = json_obj(r)
        assert data["scene_id"] == "s0_0"
        assert data["luna_trust"] == 50
        assert data["xp"] == 0


# ─────────────────────────────────────────────
# Pages HTML
# ─────────────────────────────────────────────


class TestPages:
    def test_index_page(self, client: FlaskClient) -> None:
        r = client.get("/")
        assert r.status_code == 200
        assert b"LUNA" in r.data

    def test_game_page(self, client: FlaskClient) -> None:
        r = client.get("/game")
        assert r.status_code == 200

    def test_profil_page(self, client: FlaskClient) -> None:
        r = client.get("/profil")
        assert r.status_code == 200

    def test_leaderboard_page(self, client: FlaskClient) -> None:
        r = client.get("/leaderboard")
        assert r.status_code == 200

    def test_404_page(self, client: FlaskClient) -> None:
        r = client.get("/cette-page-nexiste-vraiment-pas")
        assert r.status_code == 404
        assert b"404" in r.data or b"perdu" in r.data.lower()
