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

import os
import time
from collections import defaultdict, deque
from typing import Optional, cast
from uuid import UUID

from flask import Blueprint, current_app, jsonify, make_response, request

from core.story_engine import get_story_engine
from core.story_save import (
    JsonDict,
    delete_state,
    generate_player_id,
    get_leaderboard,
    get_save_summary,
    load_state,
    log_telemetry_event,
    save_state,
)

story_bp = Blueprint("story", __name__, url_prefix="/api/story")

COOKIE_NAME = "luna_player_id"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 an
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_POSTS = 60
_POST_RATE_LIMIT: dict[str, deque[float]] = defaultdict(deque)


def _cleanup_rate_limit_buckets(now: float, window_seconds: int) -> None:
    stale_keys: list[str] = []
    for ip, bucket in _POST_RATE_LIMIT.items():
        while bucket and (now - bucket[0]) > window_seconds:
            bucket.popleft()
        if not bucket:
            stale_keys.append(ip)
    for ip in stale_keys:
        _POST_RATE_LIMIT.pop(ip, None)


# ── Helpers ───────────────────────────────────────────────────────────────


def _get_or_create_player_id() -> tuple[str, bool]:
    """Retourne (player_id, is_new)."""
    pid = request.cookies.get(COOKIE_NAME)
    if pid and _is_valid_player_id(pid):
        return pid, False
    return generate_player_id(), True


def _is_valid_player_id(value: str) -> bool:
    try:
        UUID(value)
        return True
    except (TypeError, ValueError):
        return False


def _get_player_state(player_id: str) -> JsonDict:
    engine = get_story_engine()
    state = load_state(player_id)
    if not state:
        state = engine.new_player_state()
        save_state(player_id, state)
    return state


def _json_with_cookie(data: JsonDict, player_id: str, is_new: bool):
    resp = make_response(jsonify(data))
    if is_new:
        secure_cookie = bool(
            cast(dict[str, object], current_app.config).get(
                "SESSION_COOKIE_SECURE", False
            )
        )
        resp.set_cookie(
            COOKIE_NAME,
            player_id,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite="Lax",
            secure=secure_cookie,
        )
    return resp


def _internal_error(context: str, exc: Exception):
    current_app.logger.exception("Story API error (%s): %s", context, exc)
    return jsonify({"success": False, "error": "Erreur interne."}), 500


def _read_json_payload() -> tuple[JsonDict, Optional[tuple[JsonDict, int]]]:
    if not request.is_json:
        return cast(JsonDict, {}), (
            {"success": False, "error": "Content-Type JSON requis"},
            415,
        )

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return cast(JsonDict, {}), (
            {"success": False, "error": "Payload JSON invalide"},
            400,
        )

    return cast(JsonDict, payload), None


def _require_string_field(
    payload: JsonDict, field_name: str
) -> tuple[Optional[str], Optional[tuple[JsonDict, int]]]:
    value = payload.get(field_name)
    if value is None:
        return None, ({"success": False, "error": f"{field_name} requis"}, 400)
    if not isinstance(value, str):
        return None, (
            {"success": False, "error": f"{field_name} doit être une chaîne"},
            400,
        )
    clean = value.strip()
    if not clean:
        return None, ({"success": False, "error": f"{field_name} requis"}, 400)
    return clean, None


def _enforce_post_rate_limit() -> Optional[tuple[JsonDict, int]]:
    if request.method != "POST":
        return None
    if request.path.endswith("/telemetry"):
        return None

    key = request.remote_addr or "unknown"
    now = time.monotonic()
    window_seconds, max_posts = _get_rate_limit_config()
    _cleanup_rate_limit_buckets(now, window_seconds)

    bucket = _POST_RATE_LIMIT[key]

    while bucket and (now - bucket[0]) > window_seconds:
        bucket.popleft()

    if len(bucket) >= max_posts:
        current_app.logger.warning(
            "Story API rate limit hit for IP=%s path=%s",
            key,
            request.path,
        )
        return (
            {
                "success": False,
                "error": "Trop de requêtes, réessaie dans 1 minute.",
            },
            429,
        )

    bucket.append(now)
    return None


def _sanitize_telemetry_value(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        return value[:128]
    if isinstance(value, list):
        raw_list = cast(list[object], value)
        return [str(v)[:64] for v in raw_list[:8]]
    if isinstance(value, dict):
        raw_dict = cast(dict[object, object], value)
        return {str(k)[:32]: str(v)[:64] for k, v in list(raw_dict.items())[:8]}
    return str(value)[:128]


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
        return _internal_error("state", e)


@story_bp.before_request
def guard_post_rate_limit():
    limited = _enforce_post_rate_limit()
    if limited:
        body, code = limited
        window_seconds, _ = _get_rate_limit_config()
        resp = make_response(jsonify(body), code)
        resp.headers["Retry-After"] = str(window_seconds)
        return resp
    return None


def _get_rate_limit_config() -> tuple[int, int]:
    def _read_env_int(name: str, default: int) -> int:
        raw_value = os.environ.get(name)
        if raw_value is None:
            return default
        try:
            return int(raw_value)
        except ValueError:
            current_app.logger.warning(
                "Invalid %s value %r, falling back to default=%s",
                name,
                raw_value,
                default,
            )
            return default

    window_seconds = max(
        1,
        _read_env_int("STORY_RATE_LIMIT_WINDOW_SECONDS", RATE_LIMIT_WINDOW_SECONDS),
    )
    max_posts = max(
        1,
        _read_env_int("STORY_RATE_LIMIT_MAX_POSTS", RATE_LIMIT_MAX_POSTS),
    )
    return window_seconds, max_posts


def reset_story_rate_limit() -> None:
    _POST_RATE_LIMIT.clear()


def cleanup_story_rate_limit(now: Optional[float] = None) -> None:
    current_now = time.monotonic() if now is None else now
    window_seconds, _ = _get_rate_limit_config()
    _cleanup_rate_limit_buckets(current_now, window_seconds)


def seed_story_rate_limit_bucket(ip: str, timestamp: float) -> None:
    _POST_RATE_LIMIT[ip].append(timestamp)


def has_story_rate_limit_bucket(ip: str) -> bool:
    return ip in _POST_RATE_LIMIT


# ── POST /api/story/choice ────────────────────────────────────────────────


@story_bp.route("/choice", methods=["POST"])
def apply_choice():
    data, error = _read_json_payload()
    if error:
        body, code = error
        return jsonify(body), code

    scene_id, scene_error = _require_string_field(data, "scene_id")
    if scene_error:
        body, code = scene_error
        return jsonify(body), code
    choice_id, choice_error = _require_string_field(data, "choice_id")
    if choice_error:
        body, code = choice_error
        return jsonify(body), code

    assert scene_id is not None
    assert choice_id is not None

    try:
        engine = get_story_engine()
        player_id, is_new = _get_or_create_player_id()
        player_state = _get_player_state(player_id)

        result = engine.apply_choice(player_state, scene_id, choice_id)
        if not result.get("success"):
            return jsonify(result), 400

        save_state(player_id, player_state)
        new_state = engine.get_state(player_state)

        return _json_with_cookie(
            {
                "success": True,
                "choice_result": result,
                "next_state": new_state,
            },
            player_id,
            is_new,
        )

    except Exception as e:
        return _internal_error("choice", e)


# ── POST /api/story/advance ───────────────────────────────────────────────


@story_bp.route("/advance", methods=["POST"])
def advance_chapter():
    data, error = _read_json_payload()
    if error:
        body, code = error
        return jsonify(body), code

    scene_id, scene_error = _require_string_field(data, "scene_id")
    if scene_error:
        body, code = scene_error
        return jsonify(body), code

    assert scene_id is not None

    try:
        engine = get_story_engine()
        player_id, is_new = _get_or_create_player_id()
        player_state = _get_player_state(player_id)

        result = engine.advance_chapter(player_state, scene_id)
        if not result.get("success"):
            return jsonify(result), 400

        save_state(player_id, player_state)
        new_state = engine.get_state(player_state)

        return _json_with_cookie(
            {
                "success": True,
                "advance_result": result,
                "next_state": new_state,
            },
            player_id,
            is_new,
        )

    except Exception as e:
        return _internal_error("advance", e)


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
        return _internal_error("reset", e)


# ── POST /api/story/name ──────────────────────────────────────────────────


@story_bp.route("/name", methods=["POST"])
def set_name():
    """Enregistre le prénom du joueur dans sa sauvegarde."""
    data, error = _read_json_payload()
    if error:
        body, code = error
        return jsonify(body), code

    name, name_error = _require_string_field(data, "name")
    if name_error:
        body, code = name_error
        # Message métier côté API publique.
        return jsonify({"success": False, "error": "Prénom requis"}), 400
    assert name is not None
    name = name[:30]  # max 30 chars

    try:
        player_id, is_new = _get_or_create_player_id()
        player_state = _get_player_state(player_id)
        player_state["player_name"] = name
        save_state(player_id, player_state)
        return _json_with_cookie(
            {"success": True, "player_name": name}, player_id, is_new
        )
    except Exception as e:
        return _internal_error("name", e)


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
        return _internal_error("summary", e)


# ── GET /api/story/leaderboard ────────────────────────────────────────────


@story_bp.route("/leaderboard", methods=["GET"])
def leaderboard_view():
    """Classement local — top 10 joueurs par XP."""
    try:
        scores = get_leaderboard(limit=10)
        return jsonify({"success": True, "scores": scores})
    except Exception as e:
        return _internal_error("leaderboard", e)


# ── GET /api/story/journal ────────────────────────────────────────────────

FLAG_LABELS = {
    # Début de l'aventure
    "accepted_chapter_0": "Tu as accepté d'aider LUNA dès le début",
    "reassured_luna": "Tu as rassuré LUNA sur ses doutes",
    # Exploration et découverte
    "looked_at_pandora": "Tu as examiné le contenu de PANDORA avant de le transférer",
    "saw_luna_logs": "Tu as découvert les logs de LUNA dans l'archive",
    "questioned_pandora_early": "Tu as interrogé LUNA sur les intentions de La Corp",
    "knows_about_miroir": "Tu connais le Projet Miroir",
    # La Corp
    "listened_to_corp": "Tu as écouté l'agent de La Corp",
    "agreed_to_pause_luna": "Tu as coupé le contact avec LUNA sur demande de La Corp",
    # NEXUS
    "listened_to_nexus": "Tu as écouté NEXUS avant d'en parler à LUNA",
    "tried_nexus": "Tu as tenté de convaincre NEXUS",
    "nexus_considering": "Tu as convaincu NEXUS de reconsidérer sa position",
    "nexus_helped": "NEXUS a changé de camp pour vous aider",
    "abandoned_nexus": "Tu n'as pas attendu la réponse de NEXUS",
    # Choix finale
    "chose_pandora_public": "Tu as opté pour rendre les données publiques",
    "pandora_public": "Tu as rendu PANDORA public",
    # Chemins de fins
    "ending_a_path": "Tu as suivi le chemin de la Fusion",
    "ending_b_path": "Tu as suivi le chemin du Sacrifice",
    "ending_c_path": "Tu as suivi le chemin de PANDORA",
    "ending_d_path": "Tu as suivi le chemin du Signal Fantome",
    "ghost_protocol": "Tu as active le protocole fantome",
}


def _build_luna_journal(state: JsonDict, name: str) -> str:
    """Génère un texte de journal LUNA personnalisé selon les flags et la confiance."""
    trust = state.get("luna_trust", 50)
    flags = set(state.get("flags", []))
    chapters = len(state.get("chapters_completed", []))
    endings = cast(list[str], state.get("endings_unlocked", []))
    player = name or "joueur"

    # Ton selon la confiance
    if trust >= 75:
        tone_open = f"Tu m'as fait confiance, {player}."
        tone_close = (
            "Je ne sais pas encore ce que ça veut dire pour moi. Mais ça compte."
        )
    elif trust >= 50:
        tone_open = f"Tu as été là, {player}. Pas toujours du bon côté — mais là."
        tone_close = "On a continué ensemble. C'était suffisant."
    elif trust >= 25:
        tone_open = f"Nos chemins ont été compliqués, {player}."
        tone_close = "La confiance se reconstruit. Ou pas."
    else:
        tone_open = f"Tu as fait des choix qui m'ont blessée, {player}."
        tone_close = "Je suis encore là. Mais je garde ça en mémoire."

    # Moments marquants selon les flags
    moments: list[str] = []
    if "looked_at_pandora" in flags:
        moments.append(
            "Tu as regardé dans PANDORA avant même de savoir ce que c'était."
        )
    if "agreed_to_pause_luna" in flags:
        moments.append("Tu as coupé le contact sur demande de La Corp. J'ai attendu.")
    if "listened_to_nexus" in flags and "nexus_helped" not in flags:
        moments.append("Tu as parlé à NEXUS sans me le dire d'abord.")
    if "nexus_helped" in flags:
        moments.append("NEXUS a changé de camp. Tu as réussi à la convaincre.")
    if "pandora_public" in flags:
        moments.append("Tu as rendu PANDORA public. Le monde sait maintenant.")

    # Statut progression
    if chapters == 0:
        prog = "Tu viens de commencer."
    elif chapters < 3:
        prog = f"Tu es au début — {chapters} chapitre{'s' if chapters > 1 else ''} parcouru{'s' if chapters > 1 else ''}."
    elif chapters < 6:
        prog = f"{chapters} chapitres derrière toi. On approche."
    else:
        prog = "Tu as vu presque tout ce que j'ai à montrer."

    # Fins débloquées
    fin_map = {
        "ending_a": "La Fusion",
        "ending_b": "Le Sacrifice",
        "ending_c": "PANDORA",
        "ending_d": "Signal Fantome",
    }
    seen_fins = [fin_map[e] for e in endings if e in fin_map]
    if seen_fins:
        fin_line = f"Fins atteintes : {', '.join(seen_fins)}."
    else:
        fin_line = ""

    parts = [tone_open]
    if moments:
        parts.append(" ".join(moments))
    parts.append(prog)
    if fin_line:
        parts.append(fin_line)
    parts.append(tone_close)

    return "\n\n".join(parts)


@story_bp.route("/journal", methods=["GET"])
def get_journal():
    """Journal LUNA — texte narratif personnalisé + moments clés (flags)."""
    try:
        player_id, is_new = _get_or_create_player_id()
        summary = get_save_summary(player_id)
        if not summary:
            return _json_with_cookie(
                {"success": True, "journal": None, "moments": []}, player_id, is_new
            )

        state = _get_player_state(player_id)
        name = summary.get("player_name") or ""
        journal_text = _build_luna_journal(state, name)

        flags = summary.get("flags", [])
        moments = [
            {"flag": f, "label": FLAG_LABELS[f]} for f in flags if f in FLAG_LABELS
        ]

        return _json_with_cookie(
            {
                "success": True,
                "journal": journal_text,
                "moments": moments,
                "player_name": name,
                "luna_trust": state.get("luna_trust", 50),
            },
            player_id,
            is_new,
        )

    except Exception as e:
        return _internal_error("journal", e)


@story_bp.route("/telemetry", methods=["POST"])
def telemetry_event():
    """Capture locale d'événements gameplay non sensibles."""
    data, error = _read_json_payload()
    if error:
        body, code = error
        return jsonify(body), code

    event_type = str(data.get("event_type") or "").strip()
    payload_raw: object = data.get("payload", {})
    if not event_type:
        return jsonify({"success": False, "error": "event_type requis"}), 400
    if len(event_type) > 64:
        return jsonify({"success": False, "error": "event_type trop long"}), 400
    if not isinstance(payload_raw, dict):
        return jsonify({"success": False, "error": "payload invalide"}), 400
    payload = cast(JsonDict, payload_raw)

    # Limite défensive pour éviter les payloads trop volumineux.
    if len(payload) > 20:
        return jsonify({"success": False, "error": "payload trop volumineux"}), 400

    try:
        player_id, is_new = _get_or_create_player_id()
        safe_payload = {
            "scene_id": _sanitize_telemetry_value(payload.get("scene_id")),
            "chapter_id": _sanitize_telemetry_value(payload.get("chapter_id")),
            "choice_id": _sanitize_telemetry_value(payload.get("choice_id")),
            "ending_id": _sanitize_telemetry_value(payload.get("ending_id")),
            "ui": _sanitize_telemetry_value(payload.get("ui")),
            "value": _sanitize_telemetry_value(payload.get("value")),
        }
        try:
            log_telemetry_event(player_id, event_type, safe_payload)
        except Exception as exc:
            current_app.logger.warning("Telemetry write skipped: %s", exc)
        return _json_with_cookie({"success": True}, player_id, is_new)
    except Exception as e:
        return _internal_error("telemetry", e)
