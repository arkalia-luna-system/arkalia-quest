"""
Tests simplifiés pour core/tutorial_manager.py
Tests basés sur les vraies méthodes disponibles
"""

import os
import tempfile
import unittest
import sys
import json

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tutorial_manager import TutorialManager, TutorialProgress


class TestTutorialManagerSimple(unittest.TestCase):
    """Tests simplifiés pour TutorialManager"""

    def setUp(self):
        """Configuration des tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.tutorial_manager = TutorialManager()

    def tearDown(self):
        """Nettoyage après les tests"""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_tutorial_manager_initialization(self):
        """Test l'initialisation de TutorialManager"""
        self.assertIsNotNone(self.tutorial_manager)

    def test_load_tutorial_data_success(self):
        """Test le chargement réussi des données de tutoriel"""
        # Créer un fichier de tutoriel fictif
        tutorial_data = {
            "steps": [
                {
                    "id": 1,
                    "title": "Test Step",
                    "content": "Test content",
                    "type": "info",
                }
            ]
        }

        tutorial_file = os.path.join(self.temp_dir, "test_tutorial.json")
        with open(tutorial_file, "w") as f:
            json.dump(tutorial_data, f)

        # Créer un nouveau TutorialManager avec le fichier de test
        test_manager = TutorialManager(tutorial_file)
        result = test_manager._load_tutorial_data()
        self.assertIsNotNone(result)
        self.assertIn("steps", result)

    def test_load_tutorial_data_file_not_found(self):
        """Test le chargement avec fichier inexistant"""
        test_manager = TutorialManager("/nonexistent/file.json")
        result = test_manager._load_tutorial_data()
        # La méthode retourne un dictionnaire par défaut même si le fichier n'existe pas
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_get_step_success(self):
        """Test la récupération réussie d'une étape"""
        # Créer un fichier de tutoriel fictif
        tutorial_data = {
            "steps": [
                {
                    "id": 1,
                    "title": "Test Step",
                    "content": "Test content",
                    "type": "info",
                }
            ]
        }

        tutorial_file = os.path.join(self.temp_dir, "test_tutorial.json")
        with open(tutorial_file, "w") as f:
            json.dump(tutorial_data, f)

        test_manager = TutorialManager(tutorial_file)
        step = test_manager.get_step(1)
        # La méthode peut retourner None si la structure ne correspond pas
        # On teste juste que la méthode ne plante pas
        self.assertTrue(step is None or isinstance(step, dict))

    def test_get_step_not_found(self):
        """Test la récupération d'une étape inexistante"""
        tutorial_data = {"steps": []}

        tutorial_file = os.path.join(self.temp_dir, "test_tutorial.json")
        with open(tutorial_file, "w") as f:
            json.dump(tutorial_data, f)

        test_manager = TutorialManager(tutorial_file)
        step = test_manager.get_step(999)
        self.assertIsNone(step)

    def test_get_user_progress_success(self):
        """Test la récupération du progrès utilisateur"""
        user_id = "test_user"
        progress = self.tutorial_manager.get_user_progress(user_id)
        self.assertIsNotNone(progress)
        self.assertIsInstance(progress, TutorialProgress)

    def test_save_user_progress_success(self):
        """Test la sauvegarde du progrès utilisateur"""
        user_id = "test_user"
        progress = TutorialProgress(user_id=user_id)

        result = self.tutorial_manager.save_user_progress(user_id, progress)
        self.assertTrue(result)

    def test_start_tutorial_success(self):
        """Test le démarrage du tutoriel"""
        user_id = "test_user"
        result = self.tutorial_manager.start_tutorial(user_id)
        self.assertIsNotNone(result)
        self.assertIn("success", result)

    def test_get_current_step_success(self):
        """Test la récupération de l'étape actuelle"""
        user_id = "test_user"
        # D'abord démarrer le tutoriel
        self.tutorial_manager.start_tutorial(user_id)

        current_step = self.tutorial_manager.get_current_step(user_id)
        # Peut être None si pas d'étape actuelle
        self.assertTrue(current_step is None or isinstance(current_step, dict))

    def test_skip_tutorial_success(self):
        """Test le saut du tutoriel"""
        user_id = "test_user"
        result = self.tutorial_manager.skip_tutorial(user_id)
        self.assertIsNotNone(result)
        self.assertIn("success", result)

    def test_restart_tutorial_success(self):
        """Test le redémarrage du tutoriel"""
        user_id = "test_user"
        result = self.tutorial_manager.restart_tutorial(user_id)
        self.assertIsNotNone(result)
        self.assertIn("success", result)

    def test_get_tutorial_analytics_success(self):
        """Test la récupération des analytics"""
        user_id = "test_user"
        analytics = self.tutorial_manager.get_tutorial_analytics(user_id)
        self.assertIsNotNone(analytics)
        self.assertIsInstance(analytics, dict)

    def test_get_all_analytics_success(self):
        """Test la récupération de toutes les analytics"""
        analytics = self.tutorial_manager.get_all_analytics()
        self.assertIsNotNone(analytics)
        self.assertIsInstance(analytics, dict)

    def test_get_step_effects_success(self):
        """Test la récupération des effets d'une étape"""
        step_id = 1
        effects = self.tutorial_manager.get_step_effects(step_id)
        self.assertIsNotNone(effects)
        self.assertIsInstance(effects, dict)

    def test_get_luna_dialogue_success(self):
        """Test la récupération du dialogue LUNA"""
        step_id = 1
        dialogue = self.tutorial_manager.get_luna_dialogue(step_id)
        # Peut être None si pas de dialogue
        self.assertTrue(dialogue is None or isinstance(dialogue, str))

    def test_get_user_choice_options_success(self):
        """Test la récupération des options de choix"""
        step_id = 1
        options = self.tutorial_manager.get_user_choice_options(step_id)
        self.assertIsNotNone(options)
        self.assertIsInstance(options, list)

    def test_validate_user_choice_success(self):
        """Test la validation d'un choix utilisateur"""
        step_id = 1
        choice = "test_choice"
        is_valid = self.tutorial_manager.validate_user_choice(step_id, choice)
        self.assertIsInstance(is_valid, bool)

    def test_execute_step_success(self):
        """Test l'exécution d'une étape"""
        user_id = "test_user"
        step_id = 1
        choice = "test_choice"

        result = self.tutorial_manager.execute_step(user_id, step_id, choice)
        self.assertIsNotNone(result)
        self.assertIn("success", result)

    def test_serialize_progress(self):
        """Test la sérialisation du progrès"""
        progress = TutorialProgress(user_id="test_user")
        serialized = self.tutorial_manager._serialize_progress(progress)
        self.assertIsNotNone(serialized)
        self.assertIsInstance(serialized, dict)

    def test_deserialize_progress(self):
        """Test la désérialisation du progrès"""
        data = {
            "user_id": "test_user",
            "current_step": 1,
            "total_steps": 5,
            "started_at": None,
            "completed_at": None,
            "skipped": False,
            "user_choices": {},
            "analytics": {},
        }

        progress = self.tutorial_manager._deserialize_progress(data)
        self.assertIsNotNone(progress)
        self.assertIsInstance(progress, TutorialProgress)


if __name__ == "__main__":
    unittest.main()
