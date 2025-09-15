#!/usr/bin/env python3
"""
🧪 Tests de couverture pour les modules utils
Tests basiques pour améliorer la couverture de code
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.logger import (
        GameLogger,
        game_logger,
        performance_logger,
        security_logger,
    )
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)


class TestUtilsCoverage(unittest.TestCase):
    """Tests de couverture pour les modules utils"""

    def setUp(self):
        """Initialisation avant chaque test"""
        # Créer un répertoire temporaire pour les logs
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Nettoyage après chaque test"""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_logger_initialization(self):
        """Test d'initialisation des loggers"""
        # Test de création d'un logger
        logger = GameLogger()
        self.assertIsInstance(logger, GameLogger)

        # Test des loggers globaux
        self.assertIsInstance(game_logger, GameLogger)
        # Les loggers spécialisés ont des types différents
        self.assertIsNotNone(performance_logger)
        self.assertIsNotNone(security_logger)

    def test_game_logger_basic_functionality(self):
        """Test des fonctionnalités de base de GameLogger"""
        logger = GameLogger()

        # Test des méthodes de base
        with (
            patch("logging.Logger.info") as mock_info,
            patch("logging.Logger.warning") as mock_warning,
            patch("logging.Logger.error") as mock_error,
            patch("logging.Logger.debug") as mock_debug,
        ):
            logger.info("Test info message")
            logger.warning("Test warning message")
            logger.error("Test error message")
            logger.debug("Test debug message")

            # Vérifier que les méthodes de logging ont été appelées
            self.assertTrue(mock_info.called)
            self.assertTrue(mock_warning.called)
            self.assertTrue(mock_error.called)
            self.assertTrue(mock_debug.called)

    def test_game_logger_with_extra_data(self):
        """Test de logging avec données supplémentaires"""
        logger = GameLogger()

        with patch("logging.Logger.info") as mock_info:
            logger.info("Test message", {"user": "test", "action": "test"})
            self.assertTrue(mock_info.called)

    def test_performance_logger_functionality(self):
        """Test des fonctionnalités du logger de performance"""
        logger = performance_logger

        with patch("logging.Logger.info") as mock_info:
            logger.response_time("test_operation", 0.1)
            logger.memory_usage(50.0)
            logger.database_query("SELECT * FROM users", 0.05)
            self.assertTrue(mock_info.called)

    def test_security_logger_functionality(self):
        """Test des fonctionnalités du logger de sécurité"""
        logger = security_logger

        with (
            patch("logging.Logger.warning") as mock_warning,
            patch("logging.Logger.error") as mock_error,
        ):
            logger.unauthorized_command("admin_command", "192.168.1.1")
            logger.rate_limit_exceeded("api_call", "192.168.1.1")
            logger.suspicious_activity("multiple_failed_logins", "192.168.1.1")
            self.assertTrue(mock_warning.called or mock_error.called)

    def test_luna_ai_v2_initialization(self):
        """Test d'initialisation de LunaAIV2"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        self.assertIsNotNone(luna)
        self.assertIsInstance(luna.personality_traits, dict)
        self.assertIsInstance(luna.learning_data, dict)
        self.assertIsInstance(luna.emotion_states, dict)

    def test_luna_ai_v2_generate_response(self):
        """Test de génération de réponse"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        response = luna.generate_response("Salut LUNA !")

        self.assertIsInstance(response, dict)
        self.assertIn("success", response)
        self.assertIn("response", response)
        self.assertTrue(response["success"])

    def test_luna_ai_v2_analyze_emotion(self):
        """Test d'analyse d'émotion"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        emotion = luna.analyze_emotion("Je suis très content !")

        self.assertIsInstance(emotion, dict)
        self.assertIn("emotion", emotion)
        self.assertIn("intensity", emotion)
        self.assertIn("scores", emotion)

    def test_luna_ai_v2_get_suggestions(self):
        """Test de récupération de suggestions"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        suggestions = luna.get_suggestions({"level": 2})

        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
        self.assertLessEqual(len(suggestions), 5)

    def test_luna_ai_v2_learn_from_interaction(self):
        """Test d'apprentissage à partir d'interactions"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        emotion = {"emotion": "happy", "intensity": 0.8}
        result = luna.learn_from_interaction("Test input", "Test response", emotion)

        self.assertTrue(result)
        self.assertGreater(len(luna.learning_data["interactions"]), 0)

    def test_luna_ai_v2_get_personality_traits(self):
        """Test de récupération des traits de personnalité"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        traits = luna.get_personality_traits()

        self.assertIsInstance(traits, dict)
        self.assertIn("curiosity", traits)
        self.assertIn("empathy", traits)
        self.assertIn("playfulness", traits)

    def test_luna_ai_v2_update_personality(self):
        """Test de mise à jour de la personnalité"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        result = luna.update_personality("curiosity", 0.9)

        self.assertTrue(result)
        self.assertEqual(luna.personality_traits["curiosity"], 0.9)

    def test_luna_ai_v2_error_handling(self):
        """Test de gestion d'erreurs dans LunaAIV2"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()

        # Test avec des données invalides
        result = luna.update_personality("invalid_trait", 0.5)
        self.assertFalse(result)

        # Test avec une valeur invalide
        result = luna.update_personality("curiosity", 1.5)  # Valeur > 1
        self.assertTrue(result)
        self.assertEqual(luna.personality_traits["curiosity"], 1.0)  # Limité à 1.0

    def test_game_logger_error_handling(self):
        """Test de gestion d'erreurs dans GameLogger"""
        logger = GameLogger()

        # Test avec des messages vides
        with (
            patch("logging.Logger.info") as mock_info,
            patch("logging.Logger.warning") as mock_warning,
            patch("logging.Logger.error") as mock_error,
        ):
            logger.info("")
            logger.warning("")
            logger.error("")
            self.assertTrue(mock_info.called or mock_warning.called or mock_error.called)

    def test_logger_with_different_levels(self):
        """Test des différents niveaux de logging"""
        logger = GameLogger()

        with (
            patch("logging.Logger.error") as mock_error,
            patch("logging.Logger.warning") as mock_warning,
            patch("logging.Logger.info") as mock_info,
            patch("logging.Logger.debug") as mock_debug,
        ):
            # Test tous les niveaux disponibles
            logger.error("Error message")
            logger.warning("Warning message")
            logger.info("Info message")
            logger.debug("Debug message")

            # Vérifier que les méthodes de logging ont été appelées
            self.assertTrue(
                mock_error.called and mock_warning.called and mock_info.called and mock_debug.called
            )

    def test_game_logger_specialized_logging(self):
        """Test des loggers spécialisés"""
        logger = game_logger

        with patch("logging.Logger.info") as mock_info:
            # Test des méthodes spécialisées du game_logger
            logger.player_action("move", "player123", x=10, y=20)
            logger.mission_completed("tutorial_1", "player123", score=100)
            logger.personality_detected("hacker_creatif", "player123")
            logger.badge_earned("first_mission", "player123")
            logger.command_executed("help", True, "player123")
            self.assertTrue(mock_info.called)

    def test_luna_ai_v2_context_handling(self):
        """Test de gestion du contexte dans LunaAIV2"""
        from engines.luna_ai_v2 import LunaAIV2

        luna = LunaAIV2()
        context = {"level": 3, "previous_interaction": "test"}
        response = luna.generate_response("Comment ça va ?", context)

        self.assertIsInstance(response, dict)
        self.assertTrue(response["success"])
        self.assertIn("response", response)


if __name__ == "__main__":
    unittest.main()
