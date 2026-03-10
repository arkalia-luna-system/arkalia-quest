"""
Sauvegarde persistante de la progression — LUNA Hors Connexion.

Stocke l'état du joueur dans SQLite (data/luna_saves.db).
Chaque joueur est identifié par un player_id (UUID stocké dans un cookie long).
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime
from typing import Optional


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "luna_saves.db")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Crée la table saves si elle n'existe pas."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS story_saves (
                player_id   TEXT PRIMARY KEY,
                state_json  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            )
        """)
        conn.commit()


def generate_player_id() -> str:
    return str(uuid.uuid4())


def save_state(player_id: str, state: dict) -> None:
    """Sauvegarde (upsert) l'état du joueur."""
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO story_saves (player_id, state_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(player_id) DO UPDATE SET
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
        """, (player_id, json.dumps(state, ensure_ascii=False), datetime.utcnow().isoformat()))
        conn.commit()


def load_state(player_id: str) -> Optional[dict]:
    """Charge l'état du joueur. Retourne None si introuvable."""
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT state_json FROM story_saves WHERE player_id = ?", (player_id,)
        ).fetchone()
    if row:
        return json.loads(row["state_json"])
    return None


def delete_state(player_id: str) -> None:
    """Supprime la sauvegarde du joueur (reset)."""
    with _get_conn() as conn:
        conn.execute("DELETE FROM story_saves WHERE player_id = ?", (player_id,))
        conn.commit()


def get_save_summary(player_id: str) -> Optional[dict]:
    """Retourne un résumé de la sauvegarde (pour l'accueil)."""
    state = load_state(player_id)
    if not state:
        return None
    return {
        "exists": True,
        "current_chapter": state.get("current_chapter", "chapitre_0"),
        "luna_trust": state.get("luna_trust", 50),
        "xp": state.get("xp", 0),
        "chapters_completed": len(state.get("chapters_completed", [])),
        "endings_unlocked": state.get("endings_unlocked", []),
        "flags": state.get("flags", []),
    }


# Init au chargement du module
init_db()
