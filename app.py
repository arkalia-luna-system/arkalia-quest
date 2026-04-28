"""
LUNA — Hors Connexion
Application Flask principale.
"""

import os
import secrets
from typing import Any

from flask import Flask, Response, jsonify, render_template, request
from flask_compress import Compress
from werkzeug.exceptions import RequestEntityTooLarge

from core.story_engine import get_story_engine
from routes.pages import register_pages
from routes.story import story_bp


def _read_env_int(name: str, default: int, minimum: int = 1) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(minimum, value)


def _is_production() -> bool:
    env = (os.environ.get("FLASK_ENV") or os.environ.get("APP_ENV") or "").lower()
    return env in {"prod", "production"}


def _is_debug_enabled() -> bool:
    raw = (os.environ.get("FLASK_DEBUG") or "").strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return not _is_production()


def create_app() -> Flask:
    app = Flask(__name__)
    is_production = _is_production()

    # Configuration
    secret_key = os.environ.get("SECRET_KEY")
    if is_production and not secret_key:
        raise RuntimeError("SECRET_KEY est obligatoire en production.")
    app.secret_key = secret_key or secrets.token_hex(32)

    app.config["SESSION_COOKIE_NAME"] = "luna_session"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = is_production
    app.config["MAX_CONTENT_LENGTH"] = _read_env_int(
        "APP_MAX_CONTENT_LENGTH_BYTES",
        1 * 1024 * 1024,
        minimum=1024,
    )  # 1 MB max by default

    @app.after_request
    def apply_security_headers(response: Response) -> Response:
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault(
            "Content-Security-Policy",
            (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: blob:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "frame-ancestors 'none'"
            ),
        )
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=()",
        )
        if is_production:
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )
        if request.path.startswith("/api/"):
            response.headers.setdefault("Cache-Control", "no-store")
            response.headers.setdefault("Pragma", "no-cache")
            response.headers.setdefault("Expires", "0")
        return response

    # Compression des réponses
    Compress(app)

    # Pré-chargement du moteur narratif
    get_story_engine()

    # Blueprints
    app.register_blueprint(story_bp)

    # Pages HTML
    register_pages(app)

    @app.get("/health")
    def health():
        """Healthcheck simple pour les plateformes de deploiement."""
        return jsonify({"status": "ok"}), 200

    # Pages d'erreur thématiques
    @app.errorhandler(404)
    def not_found(e: Any):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Endpoint API introuvable."}), 404
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e: Any):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Erreur interne."}), 500
        return render_template("404.html"), 500

    @app.errorhandler(RequestEntityTooLarge)
    def payload_too_large(e: RequestEntityTooLarge):
        if request.path.startswith("/api/"):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Payload trop volumineux. Réduis la taille de la requête.",
                    }
                ),
                413,
            )
        return render_template("404.html"), 413

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=_is_debug_enabled(),
        host=os.environ.get("HOST", "0.0.0.0"),
        port=_read_env_int("PORT", 5001),
    )
