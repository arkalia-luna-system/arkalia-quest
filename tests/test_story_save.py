"""
Tests de robustesse de la couche de sauvegarde SQLite.
"""

import sqlite3
from typing import Any
from unittest.mock import patch

from core import story_save


def _point_db_to_temp(tmp_path: Any) -> None:
    story_save.DB_PATH = str(tmp_path / "luna_saves_test.db")
    story_save.init_db()


class TestStorySaveRobustness:
    def test_load_state_returns_none_on_invalid_json(self, tmp_path: Any) -> None:
        _point_db_to_temp(tmp_path)
        player_id = "player-invalid-json"
        with sqlite3.connect(story_save.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO story_saves (player_id, state_json, updated_at) VALUES (?, ?, ?)",
                (player_id, "{not-json", "2026-01-01T00:00:00+00:00"),
            )
            conn.commit()

        assert story_save.load_state(player_id) is None

    def test_load_state_returns_none_on_non_object_json(self, tmp_path: Any) -> None:
        _point_db_to_temp(tmp_path)
        player_id = "player-non-object-json"
        with sqlite3.connect(story_save.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO story_saves (player_id, state_json, updated_at) VALUES (?, ?, ?)",
                (player_id, '"just-a-string"', "2026-01-01T00:00:00+00:00"),
            )
            conn.commit()

        assert story_save.load_state(player_id) is None

    def test_get_save_summary_returns_none_on_corrupted_state(
        self, tmp_path: Any
    ) -> None:
        _point_db_to_temp(tmp_path)
        player_id = "player-bad-summary"
        with sqlite3.connect(story_save.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO story_saves (player_id, state_json, updated_at) VALUES (?, ?, ?)",
                (player_id, "{broken-json", "2026-01-01T00:00:00+00:00"),
            )
            conn.commit()

        assert story_save.get_save_summary(player_id) is None

    def test_init_db_creates_missing_parent_directory(self, tmp_path: Any) -> None:
        nested = tmp_path / "nested" / "dir"
        story_save.DB_PATH = str(nested / "luna_saves_test.db")
        story_save.init_db()
        assert nested.exists() is True
        assert (nested / "luna_saves_test.db").exists() is True

    def test_load_state_returns_none_when_database_is_invalid(
        self, tmp_path: Any
    ) -> None:
        db_path = tmp_path / "broken.db"
        db_path.write_text("not-a-sqlite-file", encoding="utf-8")
        story_save.DB_PATH = str(db_path)
        assert story_save.load_state("any-player") is None

    def test_init_db_creates_expected_indexes(self, tmp_path: Any) -> None:
        _point_db_to_temp(tmp_path)
        with sqlite3.connect(story_save.DB_PATH) as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' ORDER BY name"
            ).fetchall()
        index_names = {row[0] for row in rows}
        assert "idx_story_saves_updated_at" in index_names
        assert "idx_story_telemetry_created_at" in index_names

    def test_save_state_retries_when_database_is_locked(self, tmp_path: Any) -> None:
        _point_db_to_temp(tmp_path)
        player_id = "retry-player"
        state = {"current_scene": "s0_0", "luna_trust": 50}

        original_connect = story_save.sqlite3.connect
        attempts = {"count": 0}

        def flaky_connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
            attempts["count"] += 1
            if attempts["count"] == 1:
                raise sqlite3.OperationalError("database is locked")
            return original_connect(*args, **kwargs)

        with patch("core.story_save.sqlite3.connect", side_effect=flaky_connect):
            story_save.save_state(player_id, state)

        loaded = story_save.load_state(player_id)
        assert loaded is not None
        assert loaded["current_scene"] == "s0_0"
        assert attempts["count"] >= 2

    def test_get_leaderboard_ignores_malformed_entries(self, tmp_path: Any) -> None:
        _point_db_to_temp(tmp_path)
        with sqlite3.connect(story_save.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO story_saves (player_id, state_json, updated_at) VALUES (?, ?, ?)",
                (
                    "bad-xp",
                    '{"player_name":"Bad","xp":"oops","luna_trust":"nan"}',
                    "2026-01-01T00:00:00+00:00",
                ),
            )
            conn.execute(
                "INSERT INTO story_saves (player_id, state_json, updated_at) VALUES (?, ?, ?)",
                (
                    "good",
                    '{"player_name":"Alex","xp":120,"luna_trust":"70","chapters_completed":"bad","endings_unlocked":"ending_a"}',
                    "2026-01-02T00:00:00+00:00",
                ),
            )
            conn.commit()

        board = story_save.get_leaderboard(limit=10)
        assert len(board) == 1
        assert board[0]["name"] == "Ale***"
        assert board[0]["xp"] == 120
        assert board[0]["luna_trust"] == 70
        assert board[0]["chapters_done"] == 0
        assert board[0]["endings_unlocked"] == []
