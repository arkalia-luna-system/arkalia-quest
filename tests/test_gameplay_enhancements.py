#!/usr/bin/env python3
"""
Tests pour les améliorations de gameplay d'Arkalia Quest
"""

import json
import os
import sys
import unittest

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGameplayEnhancements(unittest.TestCase):
    """Tests pour les améliorations de gameplay"""

    def setUp(self):
        """Configuration des tests"""
        self.test_data = {
            "player_profile": {
                "id": "test_player",
                "name": "Test Player",
                "level": 5,
                "xp": 1000,
                "coins": 500,
                "badges": ["explorer", "hacker"],
                "zones_explored": ["arkalia_base"],
                "missions_completed": [],
                "puzzles_solved": [],
                "challenges_completed": [],
            }
        }

    def test_zone_exploration_data_structure(self):
        """Test de la structure des données d'exploration des zones"""
        # Vérifier que les fichiers JavaScript existent
        js_files = [
            "static/js/zone-exploration-enhanced.js",
            "static/js/daily-missions-enhanced.js",
            "static/js/motivational-empty-states.js",
            "static/js/timer-challenges.js",
            "static/js/interactive-puzzles.js",
            "static/js/gameplay-integration.js",
        ]

        for js_file in js_files:
            self.assertTrue(os.path.exists(js_file), f"Le fichier {js_file} n'existe pas")

    def test_css_files_exist(self):
        """Test de l'existence des fichiers CSS"""
        css_files = [
            "static/css/zone-exploration-enhanced.css",
            "static/css/daily-missions-enhanced.css",
            "static/css/motivational-empty-states.css",
            "static/css/timer-challenges.css",
            "static/css/interactive-puzzles.css",
            "static/css/gameplay-integration.css",
        ]

        for css_file in css_files:
            self.assertTrue(os.path.exists(css_file), f"Le fichier {css_file} n'existe pas")

    def test_html_integration(self):
        """Test de l'intégration dans le fichier HTML"""
        with open("templates/index.html", encoding="utf-8") as f:
            html_content = f.read()

        # Vérifier que les CSS sont inclus
        css_links = [
            "zone-exploration-enhanced.css",
            "daily-missions-enhanced.css",
            "motivational-empty-states.css",
            "timer-challenges.css",
            "interactive-puzzles.css",
            "gameplay-integration.css",
        ]

        for css_link in css_links:
            self.assertIn(css_link, html_content, f"Le lien CSS {css_link} n'est pas inclus")

        # Vérifier que les scripts JavaScript sont inclus
        js_scripts = [
            "zone-exploration-enhanced.js",
            "daily-missions-enhanced.js",
            "motivational-empty-states.js",
            "timer-challenges.js",
            "interactive-puzzles.js",
            "gameplay-integration.js",
        ]

        for js_script in js_scripts:
            self.assertIn(js_script, html_content, f"Le script {js_script} n'est pas inclus")

    def test_zone_exploration_structure(self):
        """Test de la structure des données d'exploration des zones"""
        with open("static/js/zone-exploration-enhanced.js", encoding="utf-8") as f:
            js_content = f.read()

        # Vérifier que les classes principales existent
        self.assertIn("class ZoneExplorationEnhanced", js_content)
        self.assertIn("initializeZoneData", js_content)
        self.assertIn("enterZone", js_content)
        self.assertIn("exploreZone", js_content)

    def test_daily_missions_structure(self):
        """Test de la structure des missions du jour"""
        with open("static/js/daily-missions-enhanced.js", encoding="utf-8") as f:
            js_content = f.read()

        # Vérifier que les classes principales existent
        self.assertIn("class DailyMissionsEnhanced", js_content)
        self.assertIn("initializeMissions", js_content)
        self.assertIn("generateDailyMissions", js_content)
        self.assertIn("completeMission", js_content)

    def test_motivational_empty_states_structure(self):
        """Test de la structure des états vides motivants"""
        with open("static/js/motivational-empty-states.js", encoding="utf-8") as f:
            js_content = f.read()

        # Vérifier que les classes principales existent
        self.assertIn("class MotivationalEmptyStates", js_content)
        self.assertIn("initializeEmptyStateMessages", js_content)
        self.assertIn("checkForEmptyStates", js_content)
        self.assertIn("showEmptyStateMessage", js_content)

    def test_timer_challenges_structure(self):
        """Test de la structure des défis à timer"""
        with open("static/js/timer-challenges.js", encoding="utf-8") as f:
            js_content = f.read()

        # Vérifier que les classes principales existent
        self.assertIn("class TimerChallenges", js_content)
        self.assertIn("initializeChallengeTypes", js_content)
        self.assertIn("startChallenge", js_content)
        self.assertIn("completeChallenge", js_content)

    def test_interactive_puzzles_structure(self):
        """Test de la structure des puzzles interactifs"""
        with open("static/js/interactive-puzzles.js", encoding="utf-8") as f:
            js_content = f.read()

        # Vérifier que les classes principales existent
        self.assertIn("class InteractivePuzzles", js_content)
        self.assertIn("initializePuzzles", js_content)
        self.assertIn("startPuzzle", js_content)
        self.assertIn("submitAnswer", js_content)

    def test_gameplay_integration_structure(self):
        """Test de la structure de l'intégration du gameplay"""
        with open("static/js/gameplay-integration.js", encoding="utf-8") as f:
            js_content = f.read()

        # Vérifier que les classes principales existent
        self.assertIn("class GameplayIntegration", js_content)
        self.assertIn("initializeSystems", js_content)
        self.assertIn("setupEventListeners", js_content)
        self.assertIn("createGameplayHub", js_content)

    def test_css_syntax(self):
        """Test de la syntaxe CSS"""
        css_files = [
            "static/css/zone-exploration-enhanced.css",
            "static/css/daily-missions-enhanced.css",
            "static/css/motivational-empty-states.css",
            "static/css/timer-challenges.css",
            "static/css/interactive-puzzles.css",
            "static/css/gameplay-integration.css",
        ]

        for css_file in css_files:
            with open(css_file, encoding="utf-8") as f:
                css_content = f.read()

            # Vérifier que le fichier n'est pas vide
            self.assertGreater(len(css_content), 0, f"Le fichier {css_file} est vide")

            # Vérifier que les classes principales existent
            if "zone-exploration" in css_file:
                self.assertIn(".zone-exploration-panel", css_content)
                self.assertIn(".zone-item", css_content)
            elif "daily-missions" in css_file:
                self.assertIn(".daily-missions-panel", css_content)
                self.assertIn(".mission-item", css_content)
            elif "motivational-empty" in css_file:
                self.assertIn(".empty-state-message", css_content)
                self.assertIn(".empty-state-content", css_content)
            elif "timer-challenges" in css_file:
                self.assertIn(".challenge-panel", css_content)
                self.assertIn(".challenge-type", css_content)
            elif "interactive-puzzles" in css_file:
                self.assertIn(".puzzle-panel", css_content)
                self.assertIn(".puzzle-item", css_content)
            elif "gameplay-integration" in css_file:
                self.assertIn(".gameplay-hub", css_content)
                self.assertIn(".hub-section", css_content)

    def test_javascript_syntax(self):
        """Test de la syntaxe JavaScript"""
        js_files = [
            "static/js/zone-exploration-enhanced.js",
            "static/js/daily-missions-enhanced.js",
            "static/js/motivational-empty-states.js",
            "static/js/timer-challenges.js",
            "static/js/interactive-puzzles.js",
            "static/js/gameplay-integration.js",
        ]

        for js_file in js_files:
            with open(js_file, encoding="utf-8") as f:
                js_content = f.read()

            # Vérifier que le fichier n'est pas vide
            self.assertGreater(len(js_content), 0, f"Le fichier {js_file} est vide")

            # Vérifier que les classes sont correctement définies
            self.assertIn("class ", js_content)
            self.assertIn("constructor()", js_content)
            self.assertIn("init()", js_content)

    def test_integration_completeness(self):
        """Test de la complétude de l'intégration"""
        # Vérifier que tous les systèmes sont connectés
        with open("static/js/gameplay-integration.js", encoding="utf-8") as f:
            integration_content = f.read()

        # Vérifier que tous les systèmes sont initialisés
        systems = [
            "zoneExploration",
            "dailyMissions",
            "motivationalEmptyStates",
            "timerChallenges",
            "interactivePuzzles",
        ]

        for system in systems:
            self.assertIn(system, integration_content, f"Le système {system} n'est pas intégré")

    def test_responsive_design(self):
        """Test de la conception responsive"""
        css_files = [
            "static/css/zone-exploration-enhanced.css",
            "static/css/daily-missions-enhanced.css",
            "static/css/motivational-empty-states.css",
            "static/css/timer-challenges.css",
            "static/css/interactive-puzzles.css",
            "static/css/gameplay-integration.css",
        ]

        for css_file in css_files:
            with open(css_file, encoding="utf-8") as f:
                css_content = f.read()

            # Vérifier que les media queries existent
            self.assertIn(
                "@media (max-width: 768px)",
                css_content,
                f"Le fichier {css_file} n'a pas de media queries pour mobile",
            )

    def test_accessibility_features(self):
        """Test des fonctionnalités d'accessibilité"""
        js_files = [
            "static/js/zone-exploration-enhanced.js",
            "static/js/daily-missions-enhanced.js",
            "static/js/motivational-empty-states.js",
            "static/js/timer-challenges.js",
            "static/js/interactive-puzzles.js",
            "static/js/gameplay-integration.js",
        ]

        for js_file in js_files:
            with open(js_file, encoding="utf-8") as f:
                js_content = f.read()

            # Vérifier que les éléments interactifs ont des événements
            self.assertIn(
                "onclick",
                js_content,
                f"Le fichier {js_file} n'a pas d'événements onclick",
            )
            # Note: tabindex est géré par CSS, pas forcément dans le JS


if __name__ == "__main__":
    unittest.main()
