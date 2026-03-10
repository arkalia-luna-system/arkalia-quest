"""
LUNA — Hors Connexion
Application Flask principale.
"""

import os
import secrets

from flask import Flask
from flask_compress import Compress

from core.story_engine import get_story_engine
from routes.pages import register_pages
from routes.story import story_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Configuration
    app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB max

    # Compression des réponses
    Compress(app)

    # Pré-chargement du moteur narratif
    get_story_engine()

    # Blueprints
    app.register_blueprint(story_bp)

    # Pages HTML
    register_pages(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
