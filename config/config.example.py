# Arkalia Quest - Configuration d'exemple
# Copiez ce fichier vers config.py et configurez vos variables

import os
from pathlib import Path

# Configuration de base
BASE_DIR = Path(__file__).parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")

# Configuration Flask
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 5000))

# Configuration de la base de données
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/arkalia.db")

# Configuration de l'IA LUNA
LUNA_AI_ENABLED = os.environ.get("LUNA_AI_ENABLED", "true").lower() == "true"
LUNA_EMOTIONS_ENABLED = (
    os.environ.get("LUNA_EMOTIONS_ENABLED", "true").lower() == "true"
)

# Configuration des tests
TESTING = os.environ.get("TESTING", "false").lower() == "true"
COVERAGE_ENABLED = os.environ.get("COVERAGE_ENABLED", "false").lower() == "true"

# Configuration des WebSockets
SOCKETIO_ENABLED = os.environ.get("SOCKETIO_ENABLED", "true").lower() == "true"
SOCKETIO_ASYNC_MODE = os.environ.get("SOCKETIO_ASYNC_MODE", "eventlet")

# Configuration de sécurité
CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = 3600

# Configuration des sessions
PERMANENT_SESSION_LIFETIME = 3600  # 1 heure
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True

# Configuration des logs
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "arkalia.log"
