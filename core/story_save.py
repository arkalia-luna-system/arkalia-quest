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
    """
    Supprime la sauvegarde du joueur (reset).
    Preserve les fins débloquées dans previous_endings pour que LUNA s'en souvienne.
    """
    old = load_state(player_id)
    previous = []
    if old:
        previous = old.get("previous_endings", [])
        for eid in old.get("endings_unlocked", []):
            if eid not in previous:
                previous.append(eid)

    with _get_conn() as conn:
        conn.execute("DELETE FROM story_saves WHERE player_id = ?", (player_id,))
        conn.commit()

    # Réinjecter dans le nouvel état vide si il y a eu des fins
    if previous:
        from core.story_engine import get_story_engine
        new_state = get_story_engine().new_player_state()
        new_state["previous_endings"] = previous
        save_state(player_id, new_state)


def get_save_summary(player_id: str) -> Optional[dict]:
    """Retourne un résumé de la sauvegarde (pour l'accueil)."""
    state = load_state(player_id)
    if not state:
        return None
    return {
        "exists": True,
        "player_name": state.get("player_name"),
        "current_chapter": state.get("current_chapter", "chapitre_0"),
        "luna_trust": state.get("luna_trust", 50),
        "xp": state.get("xp", 0),
        "chapters_completed": len(state.get("chapters_completed", [])),
        "endings_unlocked": state.get("endings_unlocked", []),
        "flags": state.get("flags", []),
    }


def get_leaderboard(limit: int = 10) -> list[dict]:
    """
    Retourne le classement des meilleurs joueurs (par XP décroissant).
    Le nom est anonymisé : les 3 premiers caractères + '***' (ou 'Joueur ???' si absent).
    """
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT state_json FROM story_saves ORDER BY updated_at DESC"
        ).fetchall()

    entries = []
    for row in rows:
        try:
            state = json.loads(row["state_json"])
        except (json.JSONDecodeError, TypeError):
            continue

        xp = state.get("xp", 0)
        if xp == 0:
            continue  # Ignorer les joueurs sans progression

        raw_name = (state.get("player_name") or "").strip()
        if raw_name:
            # Garder les 3 premiers caractères + *** pour la confidentialité
            display_name = raw_name[:3] + "***" if len(raw_name) > 3 else raw_name + "***"
        else:
            display_name = "Joueur anonyme"

        entries.append({
            "name":             display_name,
            "xp":               xp,
            "luna_trust":       state.get("luna_trust", 50),
            "chapters_done":    len(state.get("chapters_completed", [])),
            "endings_unlocked": state.get("endings_unlocked", []),
        })

    # Trier par XP décroissant, puis par trust en cas d'égalité
    entries.sort(key=lambda e: (-e["xp"], -e["luna_trust"]))
    return entries[:limit]


# Init au chargement du module
init_db()
