"""
LUNA — Hors Connexion
Application Flask principale.
"""

import os
import secrets

from flask import Flask, Response, jsonify, render_template
from flask_compress import Compress

from core.story_engine import get_story_engine
from routes.pages import register_pages
from routes.story import story_bp


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
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB max

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
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("404.html"), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=_is_debug_enabled(),
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5001")),
    )
