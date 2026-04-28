"""
Tests de robustesse de la couche de sauvegarde SQLite.
"""

import sqlite3
from typing import Any

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
