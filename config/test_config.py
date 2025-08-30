"""
Configuration spécifique pour les tests d'Arkalia Quest
"""

import tempfile
from pathlib import Path


class TestConfig:
    """Configuration optimisée pour les tests"""

    # Base de données de test temporaire
    TESTING = True
    DEBUG = False

    # Utiliser une base de données temporaire
    @property
    def DATABASE_PATH(self):
        """Retourne un chemin de base de données temporaire pour les tests"""
        temp_dir = tempfile.mkdtemp(prefix="arkalia_test_")
        return Path(temp_dir) / "test_arkalia.db"

    # Configuration des tests
    TEST_TIMEOUT = 30
    TEST_COVERAGE_THRESHOLD = 80.0

    # Désactiver les fonctionnalités non nécessaires pour les tests
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

    # Configuration des logs pour les tests
    LOG_LEVEL = "ERROR"  # Réduire le bruit des logs pendant les tests

    # Configuration de l'IA LUNA pour les tests
    LUNA_LEARNING_RATE = 0.5  # Apprentissage plus rapide pour les tests
    LUNA_MEMORY_SIZE = 100  # Mémoire réduite pour les tests
    LUNA_EMOTION_THRESHOLD = 0.3

    # Configuration de la gamification pour les tests
    POINTS_PER_ACTION = 1  # Points réduits pour les tests
    LEVEL_MULTIPLIER = 1.0  # Pas de multiplication pour les tests
    BADGE_UNLOCK_THRESHOLD = 10

    # Configuration des performances pour les tests
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB pour les tests

    def __init__(self):
        # Créer les répertoires temporaires nécessaires
        self._create_test_directories()

    def _create_test_directories(self):
        """Crée les répertoires temporaires nécessaires pour les tests"""
        test_dirs = [
            self.DATABASE_PATH.parent,
            Path(tempfile.gettempdir()) / "arkalia_test_logs",
            Path(tempfile.gettempdir()) / "arkalia_test_reports",
        ]

        for directory in test_dirs:
            directory.mkdir(parents=True, exist_ok=True)

    def cleanup(self):
        """Nettoie les fichiers temporaires créés pendant les tests"""
        import shutil

        # Supprimer la base de données temporaire
        if self.DATABASE_PATH.exists():
            self.DATABASE_PATH.unlink()

        # Supprimer le répertoire temporaire
        if self.DATABASE_PATH.parent.exists():
            shutil.rmtree(self.DATABASE_PATH.parent)

        # Supprimer les autres répertoires temporaires
        temp_dirs = [
            Path(tempfile.gettempdir()) / "arkalia_test_logs",
            Path(tempfile.gettempdir()) / "arkalia_test_reports",
        ]

        for directory in temp_dirs:
            if directory.exists():
                shutil.rmtree(directory)


# Configuration de test par défaut
test_config = TestConfig()
