#!/usr/bin/env python3
"""
🧪 TESTS AVANCÉS - ARKALIA QUEST
================================

Tests complets pour tous les nouveaux systèmes avancés :
- Mission Progress Tracker
- Narrative Branches
- Secondary Missions
- Advanced Achievements
- Category Leaderboards
- Technical Tutorials

Auteur: Assistant IA
Version: 1.0
"""

import os
import sys
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports des modules core
from utils.logger import GameLogger  # noqa: E402

# Initialiser le logger
game_logger = GameLogger()

from core.advanced_achievements import AdvancedAchievements  # noqa: E402
from core.category_leaderboards import CategoryLeaderboards  # noqa: E402
from core.mission_progress_tracker import MissionProgressTracker  # noqa: E402
from core.narrative_branches import NarrativeBranches  # noqa: E402
from core.secondary_missions import SecondaryMissions  # noqa: E402
from core.technical_tutorials import TechnicalTutorials  # noqa: E402


class TestMissionProgressTracker(unittest.TestCase):
    """Tests pour le système de suivi de progression des missions"""

    def setUp(self):
        """Configuration initiale"""
        self.tracker = MissionProgressTracker()
        self.player_id = "test_player"
        self.mission_id = "test_mission"

    def test_initialize_mission_progress(self):
        """Test d'initialisation de la progression d'une mission"""
        progress = self.tracker.initialize_mission_progress(self.mission_id, self.player_id)

        self.assertEqual(progress["mission_id"], self.mission_id)
        self.assertEqual(progress["player_id"], self.player_id)
        self.assertEqual(progress["current_step"], 0)
        self.assertEqual(progress["status"], "active")
        self.assertIsInstance(progress["start_time"], str)

    def test_update_mission_progress_step_completed(self):
        """Test de mise à jour de progression - étape complétée"""
        # Initialiser la mission
        self.tracker.initialize_mission_progress(self.mission_id, self.player_id)

        # Mettre à jour la progression
        result = self.tracker.update_mission_progress(
            self.mission_id,
            self.player_id,
            "step_1",
            "step_completed",
            True,
        )

        self.assertTrue(result["success"])
        self.assertIn("visual_indicators", result)
        self.assertIn("achievements", result)
        self.assertIn("feedback", result)

    def test_update_mission_progress_step_failed(self):
        """Test de mise à jour de progression - étape échouée"""
        self.tracker.initialize_mission_progress(self.mission_id, self.player_id)

        result = self.tracker.update_mission_progress(
            self.mission_id,
            self.player_id,
            "step_1",
            "step_failed",
            False,
        )

        self.assertTrue(result["success"])
        self.assertGreater(result["progress"]["failed_attempts"], 0)

    def test_visual_indicators_generation(self):
        """Test de génération des indicateurs visuels"""
        self.tracker.initialize_mission_progress(self.mission_id, self.player_id)

        # Simuler quelques étapes complétées
        for i in range(3):
            self.tracker.update_mission_progress(
                self.mission_id,
                self.player_id,
                f"step_{i}",
                "step_completed",
                True,
            )

        progress_key = f"{self.player_id}_{self.mission_id}"
        progress = self.tracker.mission_states[progress_key]

        indicators = self.tracker._generate_visual_indicators(progress)

        self.assertIn("progress_bar", indicators)
        self.assertIn("step_indicators", indicators)
        self.assertIn("time_indicators", indicators)

    def test_achievement_checking(self):
        """Test de vérification des achievements"""
        self.tracker.initialize_mission_progress(self.mission_id, self.player_id)

        # Simuler une mission terminée rapidement
        progress_key = f"{self.player_id}_{self.mission_id}"
        progress = self.tracker.mission_states[progress_key]
        progress["time_spent"] = 300  # 5 minutes
        progress["status"] = "completed"

        achievements = self.tracker._check_achievements(progress)

        # Vérifier qu'un achievement de vitesse est débloqué
        speed_achievements = [a for a in achievements if "speed" in a["id"]]
        self.assertGreater(len(speed_achievements), 0)

    def test_mission_analytics(self):
        """Test des analytics de mission"""
        # Créer plusieurs missions
        for i in range(3):
            mission_id = f"mission_{i}"
            self.tracker.initialize_mission_progress(mission_id, self.player_id)

            # Compléter quelques étapes
            for j in range(2):
                self.tracker.update_mission_progress(
                    mission_id,
                    self.player_id,
                    f"step_{j}",
                    "step_completed",
                    True,
                )

        analytics = self.tracker.get_mission_analytics(self.player_id)

        self.assertIn("total_missions", analytics)
        self.assertIn("completed_missions", analytics)
        self.assertIn("completion_rate", analytics)
        self.assertEqual(analytics["total_missions"], 3)


class TestNarrativeBranches(unittest.TestCase):
    """Tests pour le système de branches narratives"""

    def setUp(self):
        """Configuration initiale"""
        self.branches = NarrativeBranches()
        self.player_id = "test_player"

        # Configurer les conditions de déverrouillage pour les tests
        self.branches.story_states[self.player_id] = {
            "completed_events": ["luna_contact_completed"],
            "current_mission": "prologue",
            "branches_completed": [],
            "story_path": "default",
            "character_arc": "neutral",
            "unlocked_endings": [],
            "major_choices": [],
        }

    def test_make_choice(self):
        """Test de prise de décision narrative"""
        result = self.branches.make_choice(self.player_id, "prologue_choice", "friendly", {})

        self.assertTrue(result["success"])
        self.assertIn("choice_made", result)
        self.assertIn("consequences", result)
        self.assertIn("narrative_response", result)

    def test_choice_consequences(self):
        """Test des conséquences des choix"""
        # Faire un choix amical
        result = self.branches.make_choice(self.player_id, "prologue_choice", "friendly", {})

        consequences = result["consequences"]
        self.assertIn("luna_relationship", consequences)
        self.assertEqual(consequences["luna_relationship"], 20)

    def test_story_state_tracking(self):
        """Test du suivi de l'état de l'histoire"""
        # Faire plusieurs choix
        self.branches.make_choice(self.player_id, "prologue_choice", "friendly", {})

        # Ajouter les conditions pour la deuxième branche
        self.branches.story_states[self.player_id]["completed_events"].append("prologue_completed")
        self.branches.story_states[self.player_id]["current_mission"] = "acte_1"

        self.branches.make_choice(self.player_id, "acte_1_approach", "stealth", {})

        story_state = self.branches.get_story_state(self.player_id)

        self.assertIn("branches_completed", story_state)
        self.assertIn("major_choices", story_state)
        self.assertEqual(len(story_state["branches_completed"]), 2)

    def test_character_relationships(self):
        """Test des relations de personnage"""
        # Faire un choix qui affecte la relation avec LUNA
        self.branches.make_choice(self.player_id, "prologue_choice", "friendly", {})

        relationships = self.branches.get_character_relationships(self.player_id)

        self.assertIn("luna", relationships)
        self.assertGreater(relationships["luna"], 0)

    def test_available_branches(self):
        """Test de récupération des branches disponibles"""
        branches = self.branches.get_available_branches(self.player_id)

        self.assertIsInstance(branches, list)
        if branches:  # Si des branches sont disponibles
            branch = branches[0]
            self.assertIn("id", branch)
            self.assertIn("title", branch)
            self.assertIn("choices", branch)


class TestSecondaryMissions(unittest.TestCase):
    """Tests pour le système de missions secondaires"""

    def setUp(self):
        """Configuration initiale"""
        self.missions = SecondaryMissions()
        self.player_id = "test_player"

    def test_get_available_missions(self):
        """Test de récupération des missions disponibles"""
        missions = self.missions.get_available_missions(self.player_id)

        self.assertIn("main_missions", missions)
        self.assertIn("daily_missions", missions)
        self.assertIn("weekly_missions", missions)

    def test_start_mission(self):
        """Test de démarrage d'une mission"""
        # D'abord récupérer les missions disponibles
        available = self.missions.get_available_missions(self.player_id)

        if available["main_missions"]:
            mission_id = available["main_missions"][0]["id"]

            result = self.missions.start_mission(self.player_id, mission_id)

            self.assertTrue(result["success"])
            self.assertIn("mission", result)

    def test_update_mission_progress(self):
        """Test de mise à jour de progression de mission"""
        # Démarrer une mission
        available = self.missions.get_available_missions(self.player_id)
        if available["main_missions"]:
            mission_id = available["main_missions"][0]["id"]
            self.missions.start_mission(self.player_id, mission_id)

            # Mettre à jour la progression
            result = self.missions.update_mission_progress(
                self.player_id,
                mission_id,
                "find_code_1",
                True,
            )

            self.assertTrue(result["success"])

    def test_mission_rewards(self):
        """Test du calcul des récompenses"""
        # Démarrer et compléter une mission
        available = self.missions.get_available_missions(self.player_id)
        if available["main_missions"]:
            mission_id = available["main_missions"][0]["id"]
            self.missions.start_mission(self.player_id, mission_id)

            # Compléter tous les objectifs
            mission = self.missions.missions[mission_id]
            for obj in mission["objectives"]:
                self.missions.update_mission_progress(self.player_id, mission_id, obj["id"], True)

            # Vérifier les récompenses
            rewards = self.missions._calculate_rewards(self.player_id, mission_id)
            self.assertIn("xp", rewards)


class TestAdvancedAchievements(unittest.TestCase):
    """Tests pour le système d'achievements avancés"""

    def setUp(self):
        """Configuration initiale"""
        self.achievements = AdvancedAchievements()
        self.player_id = "test_player"

    def test_check_achievement_progress(self):
        """Test de vérification de progression d'achievements"""
        new_achievements = self.achievements.check_achievement_progress(
            self.player_id,
            "hack_system",
            {},
        )

        self.assertIsInstance(new_achievements, list)

    def test_achievement_unlocking(self):
        """Test de déverrouillage d'achievements"""
        # Simuler plusieurs hacks
        for _i in range(5):
            self.achievements.check_achievement_progress(self.player_id, "hack_system", {})

        player_achievements = self.achievements.get_player_achievements(self.player_id)

        self.assertIn("unlocked", player_achievements)
        self.assertIn("statistics", player_achievements)

    def test_achievement_categories(self):
        """Test des catégories d'achievements"""
        categories = self.achievements.get_achievement_categories()

        self.assertIn("hacking", categories)
        self.assertIn("exploration", categories)
        self.assertIn("social", categories)

    def test_achievement_leaderboard(self):
        """Test du classement des achievements"""
        # Ajouter quelques achievements
        self.achievements.check_achievement_progress(self.player_id, "hack_system", {})

        leaderboard = self.achievements.get_achievement_leaderboard()

        self.assertIsInstance(leaderboard, list)

    def test_achievement_statistics(self):
        """Test des statistiques d'achievements"""
        # Débloquer quelques achievements
        self.achievements.check_achievement_progress(self.player_id, "hack_system", {})

        player_data = self.achievements.get_player_achievements(self.player_id)
        stats = player_data["statistics"]

        self.assertIn("total_achievements", stats)
        self.assertIn("total_points", stats)


class TestCategoryLeaderboards(unittest.TestCase):
    """Tests pour le système de classements par catégories"""

    def setUp(self):
        """Configuration initiale"""
        self.leaderboards = CategoryLeaderboards()
        self.player_id = "test_player"

    def test_update_player_metrics(self):
        """Test de mise à jour des métriques d'un joueur"""
        metrics = {
            "hack_success_rate": 85.0,
            "security_knowledge": 70.0,
            "technical_skills": 90.0,
        }

        result = self.leaderboards.update_player_metrics(self.player_id, "hacking", metrics)

        self.assertTrue(result["success"])
        self.assertIn("category_score", result)

    def test_get_leaderboard(self):
        """Test de récupération d'un classement"""
        # Ajouter quelques métriques
        self.leaderboards.update_player_metrics(
            self.player_id,
            "hacking",
            {"hack_success_rate": 85.0},
        )

        leaderboard = self.leaderboards.get_leaderboard("hacking")

        self.assertIn("category", leaderboard)
        self.assertIn("players", leaderboard)

    def test_get_player_rank(self):
        """Test de récupération du rang d'un joueur"""
        # Ajouter des métriques
        self.leaderboards.update_player_metrics(
            self.player_id,
            "hacking",
            {"hack_success_rate": 85.0},
        )

        rank_info = self.leaderboards.get_player_rank(self.player_id, "hacking")

        self.assertIn("rank", rank_info)
        self.assertIn("score", rank_info)
        self.assertIn("percentile", rank_info)

    def test_get_player_overview(self):
        """Test de récupération de l'aperçu d'un joueur"""
        # Ajouter des métriques pour plusieurs catégories
        self.leaderboards.update_player_metrics(
            self.player_id,
            "hacking",
            {"hack_success_rate": 85.0},
        )
        self.leaderboards.update_player_metrics(self.player_id, "speed", {"mission_time": 300.0})

        overview = self.leaderboards.get_player_overview(self.player_id)

        self.assertIn("overall_score", overview)
        self.assertIn("categories", overview)
        self.assertGreater(len(overview["categories"]), 0)

    def test_category_comparison(self):
        """Test de comparaison des performances par catégorie"""
        # Ajouter des métriques
        self.leaderboards.update_player_metrics(
            self.player_id,
            "hacking",
            {"hack_success_rate": 85.0},
        )
        self.leaderboards.update_player_metrics(self.player_id, "speed", {"mission_time": 300.0})

        comparison = self.leaderboards.get_category_comparison(self.player_id)

        self.assertIn("comparison", comparison)
        self.assertIn("strongest_category", comparison)


class TestTechnicalTutorials(unittest.TestCase):
    """Tests pour le système de tutoriels techniques"""

    def setUp(self):
        """Configuration initiale"""
        self.tutorials = TechnicalTutorials()
        self.player_id = "test_player"

    def test_get_available_tutorials(self):
        """Test de récupération des tutoriels disponibles"""
        tutorials = self.tutorials.get_available_tutorials(self.player_id)

        self.assertIsInstance(tutorials, list)
        if tutorials:  # Si des tutoriels sont disponibles
            tutorial = tutorials[0]
            self.assertIn("id", tutorial)
            self.assertIn("title", tutorial)
            self.assertIn("concept", tutorial)

    def test_start_tutorial(self):
        """Test de démarrage d'un tutoriel"""
        available = self.tutorials.get_available_tutorials(self.player_id)

        if available:
            tutorial_id = available[0]["id"]

            result = self.tutorials.start_tutorial(self.player_id, tutorial_id)

            self.assertTrue(result["success"])
            self.assertIn("tutorial", result)

    def test_get_tutorial_content(self):
        """Test de récupération du contenu d'un tutoriel"""
        available = self.tutorials.get_available_tutorials(self.player_id)

        if available:
            tutorial_id = available[0]["id"]
            self.tutorials.start_tutorial(self.player_id, tutorial_id)

            content = self.tutorials.get_tutorial_content(self.player_id, tutorial_id, 0)

            self.assertIn("tutorial_id", content)
            self.assertIn("content", content)

    def test_complete_tutorial_step(self):
        """Test de completion d'une étape de tutoriel"""
        available = self.tutorials.get_available_tutorials(self.player_id)

        if available:
            tutorial_id = available[0]["id"]
            self.tutorials.start_tutorial(self.player_id, tutorial_id)

            result = self.tutorials.complete_tutorial_step(self.player_id, tutorial_id, 0, {})

            self.assertTrue(result["success"])

    def test_tutorial_quiz(self):
        """Test du système de quiz des tutoriels"""
        available = self.tutorials.get_available_tutorials(self.player_id)

        if available:
            tutorial_id = available[0]["id"]

            quiz = self.tutorials.get_quiz(self.player_id, tutorial_id)

            if "error" not in quiz:
                self.assertIn("questions", quiz)
                self.assertIn("time_limit", quiz)

    def test_submit_quiz(self):
        """Test de soumission d'un quiz"""
        available = self.tutorials.get_available_tutorials(self.player_id)

        if available:
            tutorial_id = available[0]["id"]

            # Simuler des réponses
            answers = {"q1": 1, "q2": 0}

            result = self.tutorials.submit_quiz(self.player_id, tutorial_id, answers)

            self.assertTrue(result["success"])
            self.assertIn("score", result)

    def test_get_references(self):
        """Test de récupération des références"""
        references = self.tutorials.get_references()

        self.assertIn("books", references)
        self.assertIn("courses", references)
        self.assertIn("tools", references)

    def test_get_concepts(self):
        """Test de récupération des concepts"""
        concepts = self.tutorials.get_concepts()

        self.assertIn("cryptography", concepts)
        self.assertIn("network_security", concepts)
        self.assertIn("ethical_hacking", concepts)


class TestIntegration(unittest.TestCase):
    """Tests d'intégration entre les systèmes"""

    def setUp(self):
        """Configuration initiale"""
        self.tracker = MissionProgressTracker()
        self.branches = NarrativeBranches()
        self.missions = SecondaryMissions()
        self.achievements = AdvancedAchievements()
        self.leaderboards = CategoryLeaderboards()
        self.tutorials = TechnicalTutorials()
        self.player_id = "integration_test_player"

    def test_full_workflow(self):
        """Test d'un workflow complet"""
        # 1. Démarrer une mission
        mission_id = "prologue"
        self.tracker.initialize_mission_progress(mission_id, self.player_id)

        # 2. Simuler les conditions de déverrouillage
        self.branches.story_states[self.player_id] = {
            "completed_events": ["luna_contact_completed"],
            "current_mission": "prologue",
            "branches_completed": [],
            "story_path": "default",
            "character_arc": "neutral",
            "unlocked_endings": [],
            "major_choices": [],
        }

        # 3. Faire un choix narratif
        choice_result = self.branches.make_choice(self.player_id, "prologue_choice", "friendly", {})
        self.assertTrue(choice_result["success"])

        # 3. Mettre à jour la progression de mission
        progress_result = self.tracker.update_mission_progress(
            mission_id,
            self.player_id,
            "step_1",
            "step_completed",
            True,
        )
        self.assertTrue(progress_result["success"])

        # 4. Vérifier les achievements
        achievements = self.achievements.check_achievement_progress(
            self.player_id,
            "hack_system",
            {},
        )
        self.assertIsInstance(achievements, list)

        # 5. Mettre à jour les métriques de classement
        metrics = {"hack_success_rate": 90.0}
        leaderboard_result = self.leaderboards.update_player_metrics(
            self.player_id,
            "hacking",
            metrics,
        )
        self.assertTrue(leaderboard_result["success"])

        # 6. Démarrer un tutoriel
        available_tutorials = self.tutorials.get_available_tutorials(self.player_id)
        if available_tutorials:
            tutorial_id = available_tutorials[0]["id"]
            tutorial_result = self.tutorials.start_tutorial(self.player_id, tutorial_id)
            self.assertTrue(tutorial_result["success"])

    def test_data_persistence(self):
        """Test de persistance des données"""
        # Modifier des données dans chaque système
        self.tracker.initialize_mission_progress("test_mission", self.player_id)
        self.branches.make_choice(self.player_id, "prologue_choice", "friendly", {})
        self.achievements.check_achievement_progress(self.player_id, "hack_system", {})

        # Sauvegarder
        self.assertTrue(self.tracker.save_progress_data())
        self.assertTrue(self.branches.save_branch_data())
        self.assertTrue(self.achievements.save_achievement_data())
        self.assertTrue(self.leaderboards.save_leaderboard_data())
        self.assertTrue(self.tutorials.save_tutorial_data())


def run_tests():
    """Lance tous les tests"""
    # Créer la suite de tests
    test_suite = unittest.TestSuite()

    # Ajouter tous les tests
    test_classes = [
        TestMissionProgressTracker,
        TestNarrativeBranches,
        TestSecondaryMissions,
        TestAdvancedAchievements,
        TestCategoryLeaderboards,
        TestTechnicalTutorials,
        TestIntegration,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Lancer les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    game_logger.info(r"🧪 Lancement des tests des systèmes avancés...")
    success = run_tests()

    if success:
        game_logger.info(r"\n✅ Tous les tests sont passés avec succès !")
        sys.exit(0)
    else:
        game_logger.info(r"\n❌ Certains tests ont échoué.")
        sys.exit(1)
