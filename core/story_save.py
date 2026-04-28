"""
Sauvegarde persistante de la progression — LUNA Hors Connexion.

Stocke l'état du joueur dans SQLite (data/luna_saves.db).
Chaque joueur est identifié par un player_id (UUID stocké dans un cookie long).
"""

import json
import os
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from heapq import heappop, heappush
from typing import Any, Optional, cast

JsonDict = dict[str, Any]

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "luna_saves.db")
_DB_LOCK_RETRIES = 3


def _get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Crée la table saves si elle n'existe pas."""
    with _get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS story_telemetry (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id    TEXT NOT NULL,
                event_type   TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at   TEXT NOT NULL
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS story_saves (
                player_id   TEXT PRIMARY KEY,
                state_json  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            )
        """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_story_saves_updated_at
            ON story_saves(updated_at)
        """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_story_telemetry_created_at
            ON story_telemetry(created_at)
        """
        )
        conn.commit()


def _is_locked_error(exc: sqlite3.OperationalError) -> bool:
    return "locked" in str(exc).lower()


def _with_db_retry(fn: Any) -> Any:
    for attempt in range(_DB_LOCK_RETRIES):
        try:
            return fn()
        except sqlite3.OperationalError as exc:
            if not _is_locked_error(exc) or attempt >= (_DB_LOCK_RETRIES - 1):
                raise
            time.sleep(0.05 * (attempt + 1))
    raise RuntimeError("Unreachable retry loop")


def _safe_int(value: object, default: int) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def _as_str_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    raw_items = cast(list[object], value)
    return [item for item in raw_items if isinstance(item, str)]


def _safe_str(value: object, default: str = "") -> str:
    if isinstance(value, str):
        clean = value.strip()
        return clean if clean else default
    return default


def generate_player_id() -> str:
    return str(uuid.uuid4())


def save_state(player_id: str, state: JsonDict) -> None:
    """Sauvegarde (upsert) l'état du joueur."""

    def _write() -> None:
        with _get_conn() as conn:
            conn.execute(
                """
                INSERT INTO story_saves (player_id, state_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(player_id) DO UPDATE SET
                    state_json = excluded.state_json,
                    updated_at = excluded.updated_at
            """,
                (
                    player_id,
                    json.dumps(state, ensure_ascii=False),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()

    _with_db_retry(_write)


def load_state(player_id: str) -> Optional[JsonDict]:
    """Charge l'état du joueur. Retourne None si introuvable."""

    def _read() -> Optional[sqlite3.Row]:
        with _get_conn() as conn:
            return conn.execute(
                "SELECT state_json FROM story_saves WHERE player_id = ?", (player_id,)
            ).fetchone()

    try:
        row = _with_db_retry(_read)
    except sqlite3.DatabaseError:
        return None
    if row:
        try:
            loaded = json.loads(row["state_json"])
        except (json.JSONDecodeError, TypeError):
            return None
        if not isinstance(loaded, dict):
            return None
        return cast(JsonDict, loaded)
    return None


def delete_state(player_id: str) -> None:
    """
    Supprime la sauvegarde du joueur (reset).
    Preserve les fins débloquées dans previous_endings pour que LUNA s'en souvienne.
    """
    old = load_state(player_id)
    previous: list[str] = []
    if old:
        previous = cast(list[str], old.get("previous_endings", []))
        for eid in cast(list[str], old.get("endings_unlocked", [])):
            if eid not in previous:
                previous.append(eid)

    def _delete() -> None:
        with _get_conn() as conn:
            conn.execute("DELETE FROM story_saves WHERE player_id = ?", (player_id,))
            conn.commit()

    _with_db_retry(_delete)

    # Réinjecter dans le nouvel état vide si il y a eu des fins
    if previous:
        from core.story_engine import get_story_engine

        new_state = get_story_engine().new_player_state()
        new_state["previous_endings"] = previous
        save_state(player_id, new_state)


def get_save_summary(player_id: str) -> Optional[JsonDict]:
    """Retourne un résumé de la sauvegarde (pour l'accueil)."""
    state = load_state(player_id)
    if not state:
        return None
    chapters_completed = _as_str_list(state.get("chapters_completed", []))
    endings_unlocked = _as_str_list(state.get("endings_unlocked", []))
    flags = _as_str_list(state.get("flags", []))
    secrets_found = _as_str_list(state.get("secrets_found", []))
    return {
        "exists": True,
        "player_name": _safe_str(state.get("player_name"), ""),
        "current_chapter": _safe_str(
            state.get("current_chapter"), "chapitre_0"
        ),
        "luna_trust": _safe_int(state.get("luna_trust", 50), 50),
        "xp": _safe_int(state.get("xp", 0), 0),
        "chapters_completed": len(chapters_completed),
        "endings_unlocked": endings_unlocked,
        "flags": flags,
        "secrets_found": secrets_found,
        "secrets_total": 5,
    }


def get_leaderboard(limit: int = 10) -> list[JsonDict]:
    """
    Retourne le classement des meilleurs joueurs (par XP décroissant).
    Le nom est anonymisé : les 3 premiers caractères + '***' (ou 'Joueur ???' si absent).
    """
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT player_id, state_json FROM story_saves ORDER BY updated_at DESC"
        ).fetchall()

    max_entries = max(1, limit)
    top_entries: list[tuple[int, int, int, JsonDict]] = []
    for idx, row in enumerate(rows):
        try:
            state = cast(JsonDict, json.loads(row["state_json"]))
        except (json.JSONDecodeError, TypeError):
            continue

        xp = _safe_int(state.get("xp", 0), 0)
        if xp == 0:
            continue  # Ignorer les joueurs sans progression

        trust = _safe_int(state.get("luna_trust", 50), 50)

        raw_name = str(state.get("player_name") or "").strip()
        if raw_name:
            # Garder les 3 premiers caractères + *** pour la confidentialité
            display_name = (
                raw_name[:3] + "***" if len(raw_name) > 3 else raw_name + "***"
            )
        else:
            display_name = "Joueur anonyme"

        chapters_done = len(_as_str_list(state.get("chapters_completed", [])))
        endings_unlocked = _as_str_list(state.get("endings_unlocked", []))

        entry = {
            "name": display_name,
            "xp": xp,
            "luna_trust": trust,
            "chapters_done": chapters_done,
            "endings_unlocked": endings_unlocked,
        }
        score = (xp, trust)
        tie_breaker = -idx
        if len(top_entries) < max_entries:
            heappush(top_entries, (score[0], score[1], tie_breaker, entry))
            continue
        worst_xp, worst_trust, worst_tie_breaker, _ = top_entries[0]
        if (score[0], score[1], tie_breaker) > (
            worst_xp,
            worst_trust,
            worst_tie_breaker,
        ):
            heappop(top_entries)
            heappush(top_entries, (score[0], score[1], tie_breaker, entry))

    # Trier final par XP décroissant, puis trust décroissant
    sorted_entries = sorted(
        top_entries,
        key=lambda item: (-item[0], -item[1], -item[2]),
    )
    return [item[3] for item in sorted_entries]


def log_telemetry_event(player_id: str, event_type: str, payload: JsonDict) -> None:
    """Stocke un événement de télémétrie locale non sensible."""

    def _write() -> None:
        with _get_conn() as conn:
            conn.execute(
                """
                INSERT INTO story_telemetry (player_id, event_type, payload_json, created_at)
                VALUES (?, ?, ?, ?)
            """,
                (
                    player_id,
                    event_type,
                    json.dumps(payload, ensure_ascii=False),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()

    _with_db_retry(_write)


# Init au chargement du module
init_db()
