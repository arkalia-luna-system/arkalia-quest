"""
Routes API — Narration LUNA Hors Connexion.

GET  /api/story/state        → état courant du joueur
POST /api/story/choice       → appliquer un choix
POST /api/story/advance      → avancer au chapitre suivant
POST /api/story/reset        → remettre à zéro
GET  /api/story/summary      → résumé de sauvegarde (pour l'accueil)
POST /api/story/name         → enregistrer le prénom du joueur
GET  /api/story/leaderboard  → classement local des joueurs
"""

from flask import Blueprint, jsonify, make_response, request

from core.story_engine import get_story_engine
from core.story_save import (
    delete_state,
    generate_player_id,
    get_leaderboard,
    get_save_summary,
    load_state,
    save_state,
)

story_bp = Blueprint("story", __name__, url_prefix="/api/story")

COOKIE_NAME = "luna_player_id"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 an


# ── Helpers ───────────────────────────────────────────────────────────────

def _get_or_create_player_id() -> tuple[str, bool]:
    """Retourne (player_id, is_new)."""
    pid = request.cookies.get(COOKIE_NAME)
    if pid:
        return pid, False
    return generate_player_id(), True


def _get_player_state(player_id: str) -> dict:
    engine = get_story_engine()
    state = load_state(player_id)
    if not state:
        state = engine.new_player_state()
        save_state(player_id, state)
    return state


def _json_with_cookie(data: dict, player_id: str, is_new: bool):
    resp = make_response(jsonify(data))
    if is_new:
        resp.set_cookie(
            COOKIE_NAME, player_id,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite="Lax",
        )
    return resp


# ── GET /api/story/state ─────────────────────────────────────────────────

@story_bp.route("/state", methods=["GET"])
def get_state():
    try:
        engine = get_story_engine()
        player_id, is_new = _get_or_create_player_id()
        player_state = _get_player_state(player_id)
        state = engine.get_state(player_state)
        return _json_with_cookie({"success": True, **state}, player_id, is_new)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── POST /api/story/choice ────────────────────────────────────────────────

@story_bp.route("/choice", methods=["POST"])
def apply_choice():
    data = request.get_json(silent=True) or {}
    scene_id  = data.get("scene_id")
    choice_id = data.get("choice_id")

    if not scene_id or not choice_id:
        return jsonify({"success": False, "error": "scene_id et choice_id requis"}), 400

    try:
        engine = get_story_engine()
        player_id, is_new = _get_or_create_player_id()
        player_state = _get_player_state(player_id)

        result = engine.apply_choice(player_state, scene_id, choice_id)
        if not result.get("success"):
            return jsonify(result), 400

        save_state(player_id, player_state)
        new_state = engine.get_state(player_state)

        return _json_with_cookie({
            "success": True,
            "choice_result": result,
            "next_state": new_state,
        }, player_id, is_new)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── POST /api/story/advance ───────────────────────────────────────────────

@story_bp.route("/advance", methods=["POST"])
def advance_chapter():
    data = request.get_json(silent=True) or {}
    scene_id = data.get("scene_id")

    if not scene_id:
        return jsonify({"success": False, "error": "scene_id requis"}), 400

    try:
        engine = get_story_engine()
        player_id, is_new = _get_or_create_player_id()
        player_state = _get_player_state(player_id)

        result = engine.advance_chapter(player_state, scene_id)
        if not result.get("success"):
            return jsonify(result), 400

        save_state(player_id, player_state)
        new_state = engine.get_state(player_state)

        return _json_with_cookie({
            "success": True,
            "advance_result": result,
            "next_state": new_state,
        }, player_id, is_new)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── POST /api/story/reset ─────────────────────────────────────────────────

@story_bp.route("/reset", methods=["POST"])
def reset_story():
    try:
        player_id, is_new = _get_or_create_player_id()
        delete_state(player_id)
        engine = get_story_engine()
        new_state = engine.new_player_state()
        save_state(player_id, new_state)
        return _json_with_cookie({"success": True}, player_id, is_new)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── POST /api/story/name ──────────────────────────────────────────────────

@story_bp.route("/name", methods=["POST"])
def set_name():
    """Enregistre le prénom du joueur dans sa sauvegarde."""
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()[:30]  # max 30 chars

    if not name:
        return jsonify({"success": False, "error": "Prénom requis"}), 400

    try:
        player_id, is_new = _get_or_create_player_id()
        player_state = _get_player_state(player_id)
        player_state["player_name"] = name
        save_state(player_id, player_state)
        return _json_with_cookie({"success": True, "player_name": name}, player_id, is_new)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── GET /api/story/summary ────────────────────────────────────────────────

@story_bp.route("/summary", methods=["GET"])
def get_summary():
    """Résumé de sauvegarde pour la page d'accueil."""
    try:
        player_id, is_new = _get_or_create_player_id()
        summary = get_save_summary(player_id)
        if not summary:
            summary = {"exists": False}
        return _json_with_cookie({"success": True, **summary}, player_id, is_new)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── GET /api/story/leaderboard ────────────────────────────────────────────

@story_bp.route("/leaderboard", methods=["GET"])
def leaderboard_view():
    """Classement local — top 10 joueurs par XP."""
    try:
        scores = get_leaderboard(limit=10)
        return jsonify({"success": True, "scores": scores})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
