"""
Configuration principale d'Arkalia Quest
Centralise tous les paramètres de l'application
"""

import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
TESTS_DIR = BASE_DIR / "tests"


# Configuration de l'application
class Config:
    """Configuration de base"""

    # Informations de base
    APP_NAME = "Arkalia Quest"
    APP_VERSION = "3.0.0"
    APP_DESCRIPTION = "Jeu éducatif immersif avec IA émotionnelle LUNA"

    # Configuration du serveur
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5001))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Configuration de la base de données
    DATABASE_PATH = DATA_DIR / "database" / "arkalia.db"
    DATABASE_BACKUP_DIR = DATA_DIR / "database" / "backups"

    # Configuration des logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "arkalia.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5

    # Configuration de la sécurité
    SECRET_KEY = os.getenv("SECRET_KEY", "arkalia-secret-key-change-in-production")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Configuration des performances
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    UPLOAD_FOLDER = DATA_DIR / "uploads"

    # Configuration de l'IA LUNA
    LUNA_LEARNING_RATE = float(os.getenv("LUNA_LEARNING_RATE", "0.1"))
    LUNA_MEMORY_SIZE = int(os.getenv("LUNA_MEMORY_SIZE", "1000"))
    LUNA_EMOTION_THRESHOLD = float(os.getenv("LUNA_EMOTION_THRESHOLD", "0.5"))

    # Configuration de la gamification
    POINTS_PER_ACTION = int(os.getenv("POINTS_PER_ACTION", "10"))
    LEVEL_MULTIPLIER = float(os.getenv("LEVEL_MULTIPLIER", "1.5"))
    BADGE_UNLOCK_THRESHOLD = int(os.getenv("BADGE_UNLOCK_THRESHOLD", "100"))

    # Configuration des tests
    TEST_DATABASE_PATH = DATA_DIR / "database" / "test_arkalia.db"
    TEST_TIMEOUT = int(os.getenv("TEST_TIMEOUT", "30"))
    TEST_COVERAGE_THRESHOLD = float(os.getenv("TEST_COVERAGE_THRESHOLD", "80.0"))

    # Configuration du déploiement
    DEPLOYMENT_ENV = os.getenv("DEPLOYMENT_ENV", "development")
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "False").lower() == "true"
    METRICS_PORT = int(os.getenv("METRICS_PORT", "9090"))


class DevelopmentConfig(Config):
    """Configuration pour le développement"""

    DEBUG = True
    LOG_LEVEL = "DEBUG"
    DATABASE_PATH = DATA_DIR / "database" / "dev_arkalia.db"


class TestingConfig(Config):
    """Configuration pour les tests"""

    TESTING = True
    DEBUG = False
    DATABASE_PATH = DATA_DIR / "database" / "test_arkalia.db"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configuration pour la production"""

    DEBUG = False
    LOG_LEVEL = "WARNING"
    SESSION_COOKIE_SECURE = True
    ENABLE_METRICS = True


# Mapping des configurations
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config() -> Config:
    """Retourne la configuration appropriée selon l'environnement"""
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)()


def get_database_url() -> str:
    """Retourne l'URL de la base de données"""
    config = get_config()
    return f"sqlite:///{config.DATABASE_PATH}"


def ensure_directories():
    """Crée les répertoires nécessaires s'ils n'existent pas"""
    directories = [
        DATA_DIR,
        DATA_DIR / "database",
        DATA_DIR / "uploads",
        LOGS_DIR,
        REPORTS_DIR,
        TESTS_DIR / "results",
        TESTS_DIR / "reports",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Configuration par défaut
config = get_config()

# Créer les répertoires au chargement du module
ensure_directories()
