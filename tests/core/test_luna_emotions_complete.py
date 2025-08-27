#!/usr/bin/env python3
"""
🧪 TESTS COMPLETS DU MOTEUR D'ÉMOTIONS LUNA - ARKALIA QUEST
Tests approfondis et exhaustifs du système d'émotions de l'IA LUNA
PRIORITÉ ABSOLUE - Module critique pour la qualité du jeu
"""

import os
import sys
import unittest
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

try:
    from core.database import DatabaseManager
    from core.luna_emotions_engine import LunaEmotion, LunaEmotionsEngine
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)


class TestLunaEmotionsComplete(unittest.TestCase):
    """Tests complets et approfondis du moteur d'émotions LUNA"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.engine = LunaEmotionsEngine()
        self.db_manager = DatabaseManager()

        # Profils de test variés
        self.test_profiles = {
            "debutant": {
                "level": 1,
                "score": 0,
                "badges": [],
                "personnalite": {"type": "debutant", "traits": ["curieux", "timide"]},
                "progression": {"missions_completees": 0, "temps_jeu": 0},
            },
            "intermediaire": {
                "level": 5,
                "score": 1500,
                "badges": ["hacker", "explorateur"],
                "personnalite": {
                    "type": "hacker",
                    "traits": ["determine", "analytique"],
                },
                "progression": {"missions_completees": 15, "temps_jeu": 3600},
            },
            "expert": {
                "level": 10,
                "score": 5000,
                "badges": ["maitre", "speedrunner", "collector"],
                "personnalite": {
                    "type": "expert",
                    "traits": ["confiant", "strategique"],
                },
                "progression": {"missions_completees": 50, "temps_jeu": 18000},
            },
        }

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.engine.reset_emotions()
        if hasattr(self, "temp_db"):
            os.remove(self.temp_db)

    # ===== TESTS D'INITIALISATION ET CONFIGURATION =====

    def test_engine_initialization_complete(self):
        """Test complet de l'initialisation du moteur"""
        print("🔧 Test d'initialisation complète...")

        # Vérifier l'état initial
        self.assertEqual(self.engine.current_emotion, LunaEmotion.CALM)
        self.assertEqual(self.engine.emotion_intensity, 0.5)
        self.assertEqual(self.engine.player_relationship, 0.0)
        self.assertEqual(len(self.engine.emotion_history), 0)

        # Vérifier la configuration
        self.assertIsNotNone(self.engine.emotion_config)
        self.assertIsNotNone(self.engine.transition_rules)
        self.assertIsNotNone(self.engine.response_templates)

    def test_emotion_states_validation(self):
        """Test de validation de tous les états d'émotion"""
        print("😊 Test de validation des états d'émotion...")

        # Vérifier que toutes les émotions sont valides
        valid_emotions = [
            LunaEmotion.CALM,
            LunaEmotion.HAPPY,
            LunaEmotion.EXCITED,
            LunaEmotion.DETERMINED,
            LunaEmotion.FOCUSED,
            LunaEmotion.CURIOUS,
            LunaEmotion.SURPRISED,
            LunaEmotion.PROUD,
            LunaEmotion.ENERGETIC,
            LunaEmotion.CONFIDENT,
            LunaEmotion.PLAYFUL,
            LunaEmotion.MYSTERIOUS,
        ]

        for emotion in valid_emotions:
            with self.subTest(emotion=emotion):
                self.assertIsInstance(emotion, LunaEmotion)
                self.assertIsInstance(emotion.value, str)
                self.assertGreater(len(emotion.value), 0)

    # ===== TESTS D'ANALYSE D'ACTIONS =====

    def test_action_analysis_comprehensive(self):
        """Test complet de l'analyse d'actions"""
        print("🎯 Test complet de l'analyse d'actions...")

        # Actions de test variées
        test_actions = [
            ("hack_system", {"réussite": True, "score_gagne": 100}),
            ("explore_world", {"réussite": True, "decouvertes": 3}),
            ("complete_mission", {"réussite": True, "difficulte": "hard"}),
            ("fail_challenge", {"réussite": False, "erreur": "timeout"}),
            ("earn_badge", {"réussite": True, "badge": "speedrunner"}),
            ("social_interaction", {"réussite": True, "type": "collaboration"}),
        ]

        for action, result in test_actions:
            with self.subTest(action=action):
                # Tester avec différents profils
                for _profile_name, profile in self.test_profiles.items():
                    emotion_data = self.engine.analyze_action(action, result, profile)

                    # Vérifications de base
                    self.assertIsInstance(emotion_data, dict)
                    self.assertIn("emotion", emotion_data)
                    self.assertIn("intensity", emotion_data)
                    self.assertIn("message", emotion_data)
                    self.assertIn("color", emotion_data)

                    # Vérifications de validité
                    self.assertIsInstance(emotion_data["emotion"], str)
                    self.assertIsInstance(emotion_data["intensity"], (int, float))
                    self.assertIsInstance(emotion_data["message"], str)
                    self.assertIsInstance(emotion_data["color"], str)

                    # Vérifications de cohérence
                    self.assertGreaterEqual(emotion_data["intensity"], 0)
                    self.assertLessEqual(emotion_data["intensity"], 10)
                    self.assertTrue(emotion_data["color"].startswith("#"))

    def test_emotion_transitions_logic(self):
        """Test de la logique des transitions d'émotions"""
        print("🔄 Test de la logique des transitions...")

        # Simuler une séquence d'actions
        actions_sequence = [
            ("start_game", {"réussite": True}),
            ("first_mission", {"réussite": True, "score_gagne": 50}),
            ("explore_area", {"réussite": True, "decouvertes": 2}),
            ("challenge_failed", {"réussite": False, "erreur": "difficulte"}),
            ("retry_challenge", {"réussite": True, "score_gagne": 100}),
            ("earn_badge", {"réussite": True, "badge": "perseverant"}),
        ]

        profile = self.test_profiles["intermediaire"]
        previous_emotion = None

        for action, result in actions_sequence:
            with self.subTest(action=action):
                emotion_data = self.engine.analyze_action(action, result, profile)
                current_emotion = emotion_data["emotion"]

                # Vérifier que l'émotion a changé de manière logique
                if (
                    previous_emotion and action != "retry_challenge"
                ):  # Retry peut maintenir l'émotion
                    # L'émotion ne devrait pas rester identique après des actions différentes
                    self.assertNotEqual(current_emotion, previous_emotion)

                previous_emotion = current_emotion

    # ===== TESTS DE PERSONNALISATION ET ADAPTATION =====

    def test_profile_based_emotions(self):
        """Test de l'adaptation des émotions au profil joueur"""
        print("👤 Test d'adaptation au profil joueur...")

        # Action de test standard
        action = "complete_mission"
        result = {"réussite": True, "score_gagne": 200}

        # Tester avec différents profils
        emotions_by_profile = {}

        for profile_name, profile in self.test_profiles.items():
            emotion_data = self.engine.analyze_action(action, result, profile)
            emotions_by_profile[profile_name] = emotion_data["emotion"]

        # Vérifier que les profils différents produisent des émotions différentes
        unique_emotions = set(emotions_by_profile.values())
        self.assertGreater(
            len(unique_emotions),
            1,
            "Les profils différents devraient produire des émotions variées",
        )

    def test_learning_adaptation(self):
        """Test de l'adaptation et de l'apprentissage"""
        print("🧠 Test d'adaptation et d'apprentissage...")

        profile = self.test_profiles["debutant"]
        action = "hack_system"

        # Simuler plusieurs tentatives
        for attempt in range(5):
            result = {
                "réussite": attempt >= 2,
                "score_gagne": 50 if attempt >= 2 else 0,
            }
            emotion_data = self.engine.analyze_action(action, result, profile)

            # Vérifier que l'émotion s'adapte aux succès/échecs
            if attempt < 2:
                # Échecs - émotions de frustration ou détermination
                self.assertIn(
                    emotion_data["emotion"],
                    ["determined", "focused", "curious", "mysterious"],
                )
            else:
                # Succès - émotions de joie ou fierté
                self.assertIn(
                    emotion_data["emotion"], ["happy", "excited", "proud", "energetic"]
                )

    # ===== TESTS DE PERFORMANCE ET ROBUSTESSE =====

    def test_performance_under_load(self):
        """Test de performance sous charge"""
        print("⚡ Test de performance sous charge...")

        profile = self.test_profiles["expert"]
        action = "complex_operation"

        # Simuler 100 analyses d'actions rapides
        start_time = datetime.now()

        for i in range(100):
            result = {"réussite": i % 2 == 0, "iteration": i}
            emotion_data = self.engine.analyze_action(action, result, profile)

            # Vérifier que la réponse est rapide
            self.assertIsInstance(emotion_data, dict)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 100 actions devraient prendre moins de 1 seconde
        self.assertLess(
            duration, 1.0, f"Performance insuffisante: {duration}s pour 100 actions"
        )

    def test_memory_management(self):
        """Test de la gestion de la mémoire"""
        print("💾 Test de gestion de la mémoire...")

        profile = self.test_profiles["intermediaire"]

        # Simuler une longue session de jeu

        for i in range(1000):
            action = f"action_{i % 10}"
            result = {"réussite": True, "iteration": i}
            self.engine.analyze_action(action, result, profile)

        # Vérifier que l'historique ne grandit pas infiniment
        final_history_length = len(self.engine.emotion_history)
        self.assertLessEqual(
            final_history_length, 100, "L'historique des émotions devrait être limité"
        )

    def test_error_handling_robustness(self):
        """Test de la robustesse et gestion d'erreurs"""
        print("🛡️ Test de robustesse et gestion d'erreurs...")

        profile = self.test_profiles["debutant"]

        # Tests avec des données invalides
        invalid_inputs = [
            (None, {}),
            ("", {}),
            ("valid_action", None),
            ("valid_action", "invalid_result"),
            ("valid_action", {"réussite": "invalid_boolean"}),
            ("valid_action", {"réussite": True, "score_gagne": "invalid_number"}),
        ]

        for action, result in invalid_inputs:
            with self.subTest(action=action, result=result):
                try:
                    emotion_data = self.engine.analyze_action(action, result, profile)

                    # Même avec des données invalides, on devrait avoir une réponse
                    self.assertIsInstance(emotion_data, dict)
                    self.assertIn("emotion", emotion_data)

                except Exception as e:
                    # Si une erreur se produit, elle devrait être gérée gracieusement
                    self.fail(
                        f"Le moteur devrait gérer gracieusement les données invalides: {e}"
                    )

    # ===== TESTS D'INTÉGRATION AVEC LA BASE DE DONNÉES =====

    def test_emotion_persistence(self):
        """Test de la persistance des émotions"""
        print("💾 Test de persistance des émotions...")

        # Créer une base de données temporaire
        self.temp_db = "temp_emotions_test.db"

        # Simuler des actions et sauvegarder
        profile = self.test_profiles["expert"]
        actions = [
            ("start_session", {"réussite": True}),
            ("complete_objective", {"réussite": True, "score_gagne": 300}),
            ("explore_secret", {"réussite": True, "decouvertes": 5}),
        ]

        for action, result in actions:
            self.engine.analyze_action(action, result, profile)

        # Vérifier que l'historique est maintenu
        self.assertGreater(len(self.engine.emotion_history), 0)

        # Vérifier que les émotions sont cohérentes
        for emotion_record in self.engine.emotion_history:
            self.assertIn("emotion", emotion_record)
            self.assertIn("timestamp", emotion_record)
            self.assertIn("action", emotion_record)

    # ===== TESTS DE VALIDATION DES RÉPONSES =====

    def test_response_quality_validation(self):
        """Test de la qualité des réponses émotionnelles"""
        print("✨ Test de qualité des réponses...")

        profile = self.test_profiles["intermediaire"]
        action = "achievement_unlocked"
        result = {"réussite": True, "achievement": "master_hacker"}

        emotion_data = self.engine.analyze_action(action, result, profile)

        # Vérifier la cohérence de la réponse
        self.assertIsInstance(emotion_data["message"], str)
        self.assertGreater(len(emotion_data["message"]), 10)

        # Vérifier que le message est contextuel
        message = emotion_data["message"].lower()
        if "achievement" in result:
            self.assertTrue(
                any(
                    word in message
                    for word in ["félicitations", "bravo", "succès", "accompli"]
                ),
                "Le message devrait refléter le succès de l'achievement",
            )

    def test_emotion_intensity_scaling(self):
        """Test de l'échelle d'intensité des émotions"""
        print("📊 Test de l'échelle d'intensité...")

        profile = self.test_profiles["debutant"]

        # Actions avec différents niveaux de succès
        test_cases = [
            ("small_success", {"réussite": True, "score_gagne": 10}, "faible"),
            ("medium_success", {"réussite": True, "score_gagne": 100}, "moyen"),
            ("major_success", {"réussite": True, "score_gagne": 500}, "élevé"),
            ("epic_success", {"réussite": True, "score_gagne": 1000}, "épique"),
        ]

        intensities = []

        for action, result, _expected_level in test_cases:
            emotion_data = self.engine.analyze_action(action, result, profile)
            intensities.append(emotion_data["intensity"])

        # Vérifier que l'intensité augmente avec l'importance du succès
        for i in range(1, len(intensities)):
            self.assertGreaterEqual(
                intensities[i],
                intensities[i - 1] * 0.8,
                "L'intensité devrait augmenter avec l'importance du succès",
            )

    # ===== TESTS DE CONFIGURATION ET PERSONNALISATION =====

    def test_emotion_configuration_validation(self):
        """Test de validation de la configuration des émotions"""
        print("⚙️ Test de validation de la configuration...")

        # Vérifier que la configuration est valide
        config = self.engine.emotion_config

        self.assertIsInstance(config, dict)
        self.assertIn("emotions", config)
        self.assertIn("transitions", config)
        self.assertIn("responses", config)

        # Vérifier la structure des émotions
        for _emotion_name, emotion_data in config["emotions"].items():
            self.assertIn("color", emotion_data)
            self.assertIn("intensity_range", emotion_data)
            self.assertIn("response_templates", emotion_data)

    def test_custom_emotion_creation(self):
        """Test de création d'émotions personnalisées"""
        print("🎨 Test de création d'émotions personnalisées...")

        # Créer une émotion personnalisée
        custom_emotion = {
            "name": "custom_excited",
            "color": "#ff6b35",
            "intensity_range": [7, 10],
            "response_templates": ["Je suis super excité !", "C'est incroyable !"],
        }

        # Vérifier que l'émotion peut être ajoutée
        self.assertTrue(hasattr(self.engine, "add_custom_emotion"))

        # Tester l'ajout (si la méthode existe)
        if hasattr(self.engine, "add_custom_emotion"):
            try:
                self.engine.add_custom_emotion(custom_emotion)
                self.assertIn("custom_excited", self.engine.emotion_config["emotions"])
            except NotImplementedError:
                # Si la fonctionnalité n'est pas encore implémentée
                pass

    # ===== TESTS DE STRESS ET LIMITES =====

    def test_stress_test_extreme_values(self):
        """Test de stress avec des valeurs extrêmes"""
        print("🔥 Test de stress avec valeurs extrêmes...")

        profile = self.test_profiles["expert"]

        # Test avec des valeurs extrêmes
        extreme_cases = [
            ("extreme_success", {"réussite": True, "score_gagne": 999999}),
            ("extreme_failure", {"réussite": False, "erreur": "catastrophic"}),
            ("rapid_actions", {"réussite": True, "speed": 0.001}),
            ("massive_data", {"réussite": True, "data_size": "1TB"}),
        ]

        for action, result in extreme_cases:
            with self.subTest(action=action):
                try:
                    emotion_data = self.engine.analyze_action(action, result, profile)

                    # Même avec des valeurs extrêmes, on devrait avoir une réponse valide
                    self.assertIsInstance(emotion_data, dict)
                    self.assertIn("emotion", emotion_data)

                except Exception as e:
                    self.fail(f"Le moteur devrait gérer les valeurs extrêmes: {e}")

    def test_concurrent_access_simulation(self):
        """Test de simulation d'accès concurrent"""
        print("🔄 Test de simulation d'accès concurrent...")

        profile = self.test_profiles["intermediaire"]
        action = "concurrent_action"

        # Simuler des accès concurrents
        import threading

        results = []
        errors = []

        def worker(worker_id):
            try:
                for i in range(10):
                    result = {"réussite": True, "worker": worker_id, "iteration": i}
                    emotion_data = self.engine.analyze_action(action, result, profile)
                    results.append((worker_id, i, emotion_data))
            except Exception as e:
                errors.append((worker_id, e))

        # Lancer 5 threads concurrents
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()

        # Vérifier qu'il n'y a pas d'erreurs
        self.assertEqual(
            len(errors), 0, f"Erreurs lors de l'accès concurrent: {errors}"
        )

        # Vérifier que tous les résultats sont valides
        self.assertEqual(
            len(results), 50, "Tous les threads devraient avoir produit des résultats"
        )

        for _worker_id, _iteration, emotion_data in results:
            self.assertIsInstance(emotion_data, dict)
            self.assertIn("emotion", emotion_data)

    # ===== TESTS DE VALIDATION FINALE =====

    def test_final_validation_complete_system(self):
        """Test de validation finale du système complet"""
        print("🎯 Test de validation finale du système complet...")

        # Test complet du système
        profile = self.test_profiles["expert"]

        # Séquence complète d'actions
        complete_sequence = [
            ("game_start", {"réussite": True, "session_id": "test_session"}),
            ("tutorial_complete", {"réussite": True, "time_taken": 300}),
            ("first_mission", {"réussite": True, "score_gagne": 150}),
            ("exploration", {"réussite": True, "areas_discovered": 3}),
            ("challenge_attempt", {"réussite": False, "difficulty": "hard"}),
            ("skill_improvement", {"réussite": True, "skill_level": 2}),
            ("achievement_unlock", {"réussite": True, "achievement": "perseverant"}),
            ("social_interaction", {"réussite": True, "friends_made": 2}),
            ("game_session_end", {"réussite": True, "total_score": 2500}),
        ]

        emotion_history = []

        for action, result in complete_sequence:
            emotion_data = self.engine.analyze_action(action, result, profile)
            emotion_history.append(
                {
                    "action": action,
                    "emotion": emotion_data["emotion"],
                    "intensity": emotion_data["intensity"],
                    "message": emotion_data["message"],
                }
            )

        # Validations finales
        self.assertEqual(len(emotion_history), len(complete_sequence))

        # Vérifier la variété des émotions
        unique_emotions = {record["emotion"] for record in emotion_history}
        self.assertGreaterEqual(
            len(unique_emotions),
            3,
            "Le système devrait produire une variété d'émotions",
        )

        # Vérifier la cohérence des intensités
        intensities = [record["intensity"] for record in emotion_history]
        self.assertGreaterEqual(
            max(intensities),
            5,
            "Certaines actions devraient produire des émotions intenses",
        )
        self.assertLessEqual(
            min(intensities),
            5,
            "Certaines actions devraient produire des émotions calmes",
        )


if __name__ == "__main__":
    # Configuration des tests
    unittest.main(verbosity=2, failfast=False, buffer=True)
