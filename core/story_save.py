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
_SCORES_INDEX_NAME = "idx_story_saves_scores"


def _get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    # WAL: meilleures lectures concurrentes (API Flask + écritures saves).
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Crée la table saves si elle n'existe pas."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS story_telemetry (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id    TEXT NOT NULL,
                event_type   TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at   TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS story_saves (
                player_id   TEXT PRIMARY KEY,
                state_json  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_story_saves_updated_at
            ON story_saves(updated_at)
        """)
        _ensure_story_save_schema(conn)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_story_telemetry_created_at
            ON story_telemetry(created_at)
        """)
        conn.commit()


def _ensure_story_save_schema(conn: sqlite3.Connection) -> None:
    columns = {
        str(row["name"])
        for row in conn.execute("PRAGMA table_info(story_saves)").fetchall()
    }

    if "xp_cache" not in columns:
        conn.execute(
            "ALTER TABLE story_saves ADD COLUMN xp_cache INTEGER NOT NULL DEFAULT 0"
        )
    if "luna_trust_cache" not in columns:
        conn.execute(
            "ALTER TABLE story_saves ADD COLUMN luna_trust_cache INTEGER NOT NULL DEFAULT 50"
        )

    conn.execute(f"""
        CREATE INDEX IF NOT EXISTS {_SCORES_INDEX_NAME}
        ON story_saves(xp_cache DESC, luna_trust_cache DESC, updated_at DESC)
    """)
    # Backfill idempotent: utile après migration d'une base existante.
    conn.execute("""
        UPDATE story_saves
        SET
            xp_cache = CAST(COALESCE(json_extract(state_json, '$.xp'), '0') AS INTEGER),
            luna_trust_cache = CAST(COALESCE(json_extract(state_json, '$.luna_trust'), '50') AS INTEGER)
    """)


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


def _state_scores(state: JsonDict) -> tuple[int, int]:
    xp = _safe_int(state.get("xp", 0), 0)
    trust = _safe_int(state.get("luna_trust", 50), 50)
    return xp, trust


def save_state(player_id: str, state: JsonDict) -> None:
    """Sauvegarde (upsert) l'état du joueur."""

    def _write() -> None:
        with _get_conn() as conn:
            xp, trust = _state_scores(state)
            conn.execute(
                """
                INSERT INTO story_saves (
                    player_id, state_json, updated_at, xp_cache, luna_trust_cache
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(player_id) DO UPDATE SET
                    state_json = excluded.state_json,
                    updated_at = excluded.updated_at,
                    xp_cache = excluded.xp_cache,
                    luna_trust_cache = excluded.luna_trust_cache
            """,
                (
                    player_id,
                    json.dumps(state, ensure_ascii=False),
                    datetime.now(timezone.utc).isoformat(),
                    xp,
                    trust,
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
        "current_chapter": _safe_str(state.get("current_chapter"), "chapitre_0"),
        "luna_trust": _safe_int(state.get("luna_trust", 50), 50),
        "xp": _safe_int(state.get("xp", 0), 0),
        "chapters_completed": len(chapters_completed),
        "endings_unlocked": endings_unlocked,
        "flags": flags,
        "secrets_found": secrets_found,
        "secrets_total": 5,
    }


def _leaderboard_entry_from_state(state: JsonDict) -> Optional[JsonDict]:
    """Construit une entrée leaderboard depuis un état déjà parsé (xp > 0 attendu)."""
    xp = _safe_int(state.get("xp", 0), 0)
    if xp == 0:
        return None

    trust = _safe_int(state.get("luna_trust", 50), 50)

    raw_name = str(state.get("player_name") or "").strip()
    if raw_name:
        display_name = raw_name[:3] + "***" if len(raw_name) > 3 else raw_name + "***"
    else:
        display_name = "Joueur anonyme"

    chapters_done = len(_as_str_list(state.get("chapters_completed", [])))
    endings_unlocked = _as_str_list(state.get("endings_unlocked", []))

    return {
        "name": display_name,
        "xp": xp,
        "luna_trust": trust,
        "chapters_done": chapters_done,
        "endings_unlocked": endings_unlocked,
    }


def _get_leaderboard_legacy(limit: int) -> list[JsonDict]:
    """Parcourt toutes les lignes (chemins SQLite sans extension JSON1)."""
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

        entry = _leaderboard_entry_from_state(state)
        if entry is None:
            continue

        xp = cast(int, entry["xp"])
        trust = cast(int, entry["luna_trust"])
        tie_breaker = -idx
        if len(top_entries) < max_entries:
            heappush(top_entries, (xp, trust, tie_breaker, entry))
            continue
        worst_xp, worst_trust, worst_tie_breaker, _ = top_entries[0]
        if (xp, trust, tie_breaker) > (worst_xp, worst_trust, worst_tie_breaker):
            heappop(top_entries)
            heappush(top_entries, (xp, trust, tie_breaker, entry))

    sorted_entries = sorted(
        top_entries,
        key=lambda item: (-item[0], -item[1], -item[2]),
    )
    return [item[3] for item in sorted_entries]


def get_leaderboard(limit: int = 10) -> list[JsonDict]:
    """
    Retourne le classement des meilleurs joueurs (par XP décroissant).
    Le nom est anonymisé : les 3 premiers caractères + '***' (ou 'Joueur ???' si absent).

    Utilise les colonnes cache indexées pour éviter de parser toute la table.
    Repli automatique vers la stratégie legacy si la requête optimisée échoue.
    """
    max_entries = max(1, limit)
    fetch_cap = max(max_entries * 25, 64)

    try:
        with _get_conn() as conn:
            rows = conn.execute(
                """
                SELECT state_json FROM story_saves
                WHERE xp_cache > 0
                ORDER BY
                  xp_cache DESC,
                  luna_trust_cache DESC,
                  updated_at DESC
                LIMIT ?
                """,
                (fetch_cap,),
            ).fetchall()
    except sqlite3.OperationalError:
        return _get_leaderboard_legacy(limit)

    if not rows:
        return _get_leaderboard_legacy(limit)

    result: list[JsonDict] = []
    for row in rows:
        try:
            state = cast(JsonDict, json.loads(row["state_json"]))
        except (json.JSONDecodeError, TypeError):
            continue
        entry = _leaderboard_entry_from_state(state)
        if entry is None:
            continue
        result.append(entry)
        if len(result) >= max_entries:
            break

    # Plein écran de candidats mais trop de lignes invalides au parse → repli sûr.
    if len(rows) == fetch_cap and len(result) < max_entries:
        return _get_leaderboard_legacy(limit)

    return result


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
