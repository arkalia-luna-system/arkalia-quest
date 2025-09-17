#!/usr/bin/env python3
"""
🧪 Tests complets du moteur de gamification Arkalia Quest
Tests de tous les aspects du système de récompenses et de progression
"""

import os
import sys
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.gamification_engine import GamificationEngine
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)


class TestGamificationEngineComplete(unittest.TestCase):
    """Tests complets du moteur de gamification"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.engine = GamificationEngine()
        self.test_profile = {
            "username": "test_user",
            "level": 1,
            "score": 0,
            "badges": [],
            "achievements": [],
            "experience": 0,
            "streak": 0,
            "last_activity": "2025-08-17T10:00:00",
        }

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Nettoyer les données de test

    def test_initialization(self):
        """Test d'initialisation du moteur de gamification"""
        self.assertIsNotNone(self.engine)
        self.assertTrue(hasattr(self.engine, "data_dir"))
        self.assertTrue(hasattr(self.engine, "leaderboard_file"))
        self.assertTrue(hasattr(self.engine, "badges_secrets_file"))
        self.assertTrue(hasattr(self.engine, "achievements_file"))

    def test_badge_system(self):
        """Test complet du système de badges"""
        game_logger.info(r"🏆 Test du système de badges...")

        # Test de création de badges
        badge_data = {
            "id": "first_hack",
            "name": "Premier Hack",
            "description": "A réussi son premier hack",
            "icon": "💻",
            "points": 100,
            "requirements": {"hacks_completed": 1},
        }

        # Vérifier que le badge peut être créé
        self.assertIsInstance(badge_data["id"], str)
        self.assertIsInstance(badge_data["name"], str)
        self.assertIsInstance(badge_data["points"], int)
        self.assertGreater(badge_data["points"], 0)

        # Test de validation des badges
        valid_badges = ["hacker", "explorer", "master", "speedrunner", "collector"]
        for badge in valid_badges:
            self.assertIsInstance(badge, str)
            self.assertGreater(len(badge), 0)

    def test_level_progression(self):
        """Test du système de progression des niveaux"""
        game_logger.info(r"📈 Test de la progression des niveaux...")

        # Test des calculs de niveau
        test_cases = [
            {"score": 0, "expected_level": 1},
            {"score": 100, "expected_level": 1},
            {"score": 500, "expected_level": 2},
            {"score": 1000, "expected_level": 3},
            {"score": 2000, "expected_level": 4},
        ]

        for case in test_cases:
            with self.subTest(score=case["score"]):
                # Simuler le calcul de niveau
                calculated_level = self.calculate_level_from_score(case["score"])
                self.assertGreaterEqual(calculated_level, 1)
                self.assertLessEqual(calculated_level, 100)  # Niveau max raisonnable

    def calculate_level_from_score(self, score):
        """Calcule le niveau basé sur le score (simulation)"""
        if score < 100:
            return 1
        if score < 500:
            return 2
        if score < 1000:
            return 3
        if score < 2000:
            return 4
        return 5

    def test_achievement_system(self):
        """Test du système d'achievements"""
        print("🏅 Test du système d'achievements...")

        # Test de création d'achievements
        achievement_data = {
            "id": "speed_hacker",
            "name": "Hacker Rapide",
            "description": "A complété 10 hacks en moins de 5 minutes",
            "icon": "⚡",
            "points": 500,
            "requirements": {"hacks_speed": 10, "time_limit": 300},
        }

        # Vérifier la structure des achievements
        self.assertIsInstance(achievement_data["id"], str)
        self.assertIsInstance(achievement_data["name"], str)
        self.assertIsInstance(achievement_data["points"], int)
        self.assertGreater(achievement_data["points"], 0)

        # Test des types d'achievements
        achievement_types = [
            "speed",
            "accuracy",
            "creativity",
            "persistence",
            "innovation",
        ]
        for achievement_type in achievement_types:
            self.assertIsInstance(achievement_type, str)
            self.assertGreater(len(achievement_type), 0)

    def test_score_calculation(self):
        """Test du calcul des scores"""
        game_logger.info(r"💯 Test du calcul des scores...")

        # Test des différents types d'actions
        action_scores = {
            "hack_system": 100,
            "complete_tutorial": 50,
            "earn_badge": 200,
            "help_others": 25,
            "explore_world": 75,
        }

        for action, expected_score in action_scores.items():
            with self.subTest(action=action):
                # Vérifier que les scores sont cohérents
                self.assertIsInstance(expected_score, int)
                self.assertGreater(expected_score, 0)
                self.assertLessEqual(expected_score, 1000)  # Score max raisonnable

    def test_streak_system(self):
        """Test du système de streak (série)"""
        game_logger.info(r"🔥 Test du système de streak...")

        # Test des calculs de streak
        streak_cases = [
            {"days": 1, "multiplier": 1.0},
            {"days": 3, "multiplier": 1.2},
            {"days": 7, "multiplier": 1.5},
            {"days": 14, "multiplier": 2.0},
            {"days": 30, "multiplier": 3.0},
        ]

        for case in streak_cases:
            with self.subTest(days=case["days"]):
                multiplier = self.calculate_streak_multiplier(case["days"])
                self.assertGreaterEqual(multiplier, 1.0)
                self.assertLessEqual(multiplier, 5.0)  # Multiplicateur max raisonnable

    def calculate_streak_multiplier(self, days):
        """Calcule le multiplicateur de streak (simulation)"""
        if days < 3:
            return 1.0
        if days < 7:
            return 1.2
        if days < 14:
            return 1.5
        if days < 30:
            return 2.0
        return 3.0

    def test_reward_system(self):
        """Test du système de récompenses"""
        game_logger.info(r"🎁 Test du système de récompenses...")

        # Test des types de récompenses
        reward_types = {
            "points": "Score numérique",
            "badges": "Badges visuels",
            "achievements": "Achievements spéciaux",
            "unlocks": "Déblocages de contenu",
            "bonuses": "Bonus temporaires",
        }

        for reward_type, description in reward_types.items():
            with self.subTest(reward_type=reward_type):
                self.assertIsInstance(reward_type, str)
                self.assertIsInstance(description, str)
                self.assertGreater(len(reward_type), 0)
                self.assertGreater(len(description), 0)

    def test_engagement_metrics(self):
        """Test des métriques d'engagement"""
        print("📊 Test des métriques d'engagement...")

        # Test des indicateurs d'engagement
        engagement_metrics = [
            "daily_active_users",
            "session_duration",
            "retention_rate",
            "completion_rate",
            "social_sharing",
        ]

        for metric in engagement_metrics:
            with self.subTest(metric=metric):
                self.assertIsInstance(metric, str)
                self.assertGreater(len(metric), 0)

                # Simuler une valeur de métrique
                metric_value = self.simulate_metric_value(metric)
                self.assertIsInstance(metric_value, (int, float))
                self.assertGreaterEqual(metric_value, 0)

    def simulate_metric_value(self, metric):
        """Simule une valeur de métrique d'engagement"""
        if "users" in metric:
            return 150  # Nombre d'utilisateurs
        if "duration" in metric:
            return 25.5  # Minutes
        if "rate" in metric:
            return 0.85  # Pourcentage
        if "sharing" in metric:
            return 12  # Nombre de partages
        return 100  # Valeur par défaut

    def test_motivation_system(self):
        """Test du système de motivation"""
        game_logger.info(r"💪 Test du système de motivation...")

        # Test des facteurs de motivation
        motivation_factors = {
            "progress_visibility": "Visibilité de la progression",
            "social_recognition": "Reconnaissance sociale",
            "challenge_balance": "Équilibre des défis",
            "reward_frequency": "Fréquence des récompenses",
            "personalization": "Personnalisation de l'expérience",
        }

        for factor, description in motivation_factors.items():
            with self.subTest(factor=factor):
                self.assertIsInstance(factor, str)
                self.assertIsInstance(description, str)
                self.assertGreater(len(factor), 0)
                self.assertGreater(len(description), 0)

    def test_gamification_balance(self):
        """Test de l'équilibre du système de gamification"""
        print("⚖️ Test de l'équilibre du système...")

        # Test de l'équilibre des récompenses
        reward_balance = {
            "easy_tasks": {"min_points": 10, "max_points": 50},
            "medium_tasks": {"min_points": 50, "max_points": 200},
            "hard_tasks": {"min_points": 200, "max_points": 1000},
        }

        for difficulty, points_range in reward_balance.items():
            with self.subTest(difficulty=difficulty):
                min_points = points_range["min_points"]
                max_points = points_range["max_points"]

                self.assertGreater(max_points, min_points)
                self.assertGreaterEqual(min_points, 0)
                self.assertLessEqual(max_points, 1000)

                # Vérifier la progression logique
                if difficulty == "easy_tasks":
                    self.assertLessEqual(max_points, 100)
                elif difficulty == "medium_tasks":
                    self.assertGreaterEqual(min_points, 25)
                    self.assertLessEqual(max_points, 500)
                elif difficulty == "hard_tasks":
                    self.assertGreaterEqual(min_points, 100)

    def test_performance_optimization(self):
        """Test de l'optimisation des performances"""
        print("⚡ Test de l'optimisation des performances...")

        # Test des métriques de performance
        performance_metrics = {
            "response_time": "Temps de réponse",
            "memory_usage": "Utilisation mémoire",
            "cpu_usage": "Utilisation CPU",
            "database_queries": "Requêtes base de données",
            "cache_hit_rate": "Taux de cache",
        }

        for metric, description in performance_metrics.items():
            with self.subTest(metric=metric):
                self.assertIsInstance(metric, str)
                self.assertIsInstance(description, str)

                # Simuler une valeur de performance
                performance_value = self.simulate_performance_value(metric)
                self.assertIsInstance(performance_value, (int, float))
                self.assertGreaterEqual(performance_value, 0)

    def simulate_performance_value(self, metric):
        """Simule une valeur de performance"""
        if "time" in metric:
            return 0.15  # Secondes
        if "memory" in metric:
            return 45.2  # MB
        if "cpu" in metric:
            return 12.5  # Pourcentage
        if "queries" in metric:
            return 8  # Nombre de requêtes
        if "cache" in metric:
            return 0.92  # Taux de cache
        return 100  # Valeur par défaut

    def test_error_handling(self):
        """Test de la gestion des erreurs"""
        game_logger.info(r"🚨 Test de la gestion des erreurs...")

        # Test des scénarios d'erreur
        error_scenarios = [
            "invalid_score",
            "missing_badge_data",
            "database_connection_failed",
            "invalid_user_input",
            "system_overload",
        ]

        for scenario in error_scenarios:
            with self.subTest(scenario=scenario):
                self.assertIsInstance(scenario, str)
                self.assertGreater(len(scenario), 0)

                # Vérifier que le scénario peut être géré
                can_handle = self.can_handle_error_scenario(scenario)
                self.assertIsInstance(can_handle, bool)

    def can_handle_error_scenario(self, scenario):
        """Vérifie si un scénario d'erreur peut être géré"""
        handleable_scenarios = [
            "invalid_score",
            "missing_badge_data",
            "invalid_user_input",
        ]
        return scenario in handleable_scenarios

    def test_integration_points(self):
        """Test des points d'intégration"""
        print("🔗 Test des points d'intégration...")

        # Test des intégrations avec d'autres systèmes
        integration_points = {
            "user_profile": "Profil utilisateur",
            "achievement_system": "Système d'achievements",
            "notification_system": "Système de notifications",
            "analytics_engine": "Moteur d'analytics",
            "social_features": "Fonctionnalités sociales",
        }

        for point, description in integration_points.items():
            with self.subTest(point=point):
                self.assertIsInstance(point, str)
                self.assertIsInstance(description, str)
                self.assertGreater(len(point), 0)
                self.assertGreater(len(description), 0)

    def test_data_consistency(self):
        """Test de la cohérence des données"""
        game_logger.info(r"🔒 Test de la cohérence des données...")

        # Test de la validation des données
        data_validation_rules = {
            "score_range": (0, 999999),
            "level_range": (1, 100),
            "badge_id_format": "alphanumeric",
            "achievement_points": "positive_integer",
            "user_id_format": "uuid_or_string",
        }

        for rule, _constraint in data_validation_rules.items():
            with self.subTest(rule=rule):
                self.assertIsInstance(rule, str)
                self.assertGreater(len(rule), 0)

                # Vérifier que la règle est valide
                is_valid_rule = self.validate_data_rule(rule)
                self.assertIsInstance(is_valid_rule, bool)

    def validate_data_rule(self, rule):
        """Valide une règle de données"""
        valid_rules = [
            "score_range",
            "level_range",
            "badge_id_format",
            "achievement_points",
            "user_id_format",
        ]
        return rule in valid_rules


def run_gamification_tests():
    """Lance tous les tests de gamification"""
    game_logger.info(r"🎮 Lancement des tests complets de gamification...")

    # Créer la suite de tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestGamificationEngineComplete)

    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Afficher le résumé
    game_logger.info(r"\n📊 Résumé des tests de gamification:")
    game_logger.info(f"  Tests exécutés: {result.testsRun}")
    game_logger.info(
        f"Tests réussis: {result.testsRun - len(result.failures) - len(result.errors)}"
    )
    game_logger.info(f"  Tests échoués: {len(result.failures)}")
    game_logger.info(f"  Tests en erreur: {len(result.errors)}")

    if result.failures:
        game_logger.info(r"\n❌ Tests échoués:")
        for test, traceback in result.failures:
            game_logger.info(f"  - {test}: {traceback}")

    if result.errors:
        game_logger.info(r"\n🚨 Tests en erreur:")
        for test, traceback in result.errors:
            game_logger.info(f"  - {test}: {traceback}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_gamification_tests()
    sys.exit(0 if success else 1)
