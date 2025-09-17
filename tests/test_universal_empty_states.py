#!/usr/bin/env python3
"""
Tests pour le système universel d'empty states
"""

import os
import sys
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestUniversalEmptyStates(unittest.TestCase):
    """Tests pour le système universel d'empty states"""

    def test_universal_empty_states_file_exists(self):
        """Vérifier que le fichier universal-empty-states.js existe"""
        self.assertTrue(os.path.exists("static/js/universal-empty-states.js"))

    def test_universal_empty_states_structure(self):
        """Vérifier la structure de la classe UniversalEmptyStates"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la classe principale
        self.assertIn("class UniversalEmptyStates", content)

        # Vérifier les méthodes principales
        self.assertIn("showEmptyState(", content)
        self.assertIn("removeEmptyState(", content)
        self.assertIn("checkForEmptyStates(", content)
        self.assertIn("createEmptyState(", content)

        # Vérifier les méthodes utilitaires
        self.assertIn("showStatsEmpty(", content)
        self.assertIn("showMissionsEmpty(", content)
        self.assertIn("showZonesEmpty(", content)
        self.assertIn("showSocialEmpty(", content)
        self.assertIn("showMinigamesEmpty(", content)
        self.assertIn("showThemesEmpty(", content)
        self.assertIn("showLeaderboardEmpty(", content)
        self.assertIn("showAchievementsEmpty(", content)

    def test_empty_state_types(self):
        """Vérifier que tous les types d'empty states sont supportés"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les types d'empty states
        types = [
            "stats",
            "missions",
            "zones",
            "social",
            "minigames",
            "themes",
            "leaderboard",
            "achievements",
        ]
        for empty_state_type in types:
            self.assertIn(f"show{empty_state_type.capitalize()}Empty", content)

    def test_icons_system(self):
        """Vérifier le système d'icônes"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la méthode getDefaultIcon
        self.assertIn("getDefaultIcon(", content)

        # Vérifier les icônes définies
        icons = ["📊", "🎯", "🗺️", "👥", "🎮", "🎨", "🏆", "🏅", "📭"]
        for icon in icons:
            self.assertIn(icon, content)

    def test_css_styles(self):
        """Vérifier que les styles CSS sont inclus"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les classes CSS principales
        css_classes = [
            "universal-empty-state",
            "universal-empty-state-icon",
            "universal-empty-state-title",
            "universal-empty-state-description",
            "universal-empty-state-actions",
            "universal-empty-state-btn",
            "universal-empty-state-progress",
            "universal-empty-state-particles",
        ]

        for css_class in css_classes:
            self.assertIn(css_class, content)

    def test_animations(self):
        """Vérifier les animations CSS"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les animations
        animations = [
            "emptyStateFloat",
            "emptyStateSlideIn",
            "emptyStateFadeIn",
            "particleFloat",
        ]

        for animation in animations:
            self.assertIn(animation, content)

    def test_responsive_design(self):
        """Vérifier le design responsive"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les media queries
        self.assertIn("@media (max-width: 768px)", content)
        self.assertIn("flex-direction: column", content)

    def test_intersection_observer(self):
        """Vérifier l'utilisation d'IntersectionObserver"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier IntersectionObserver
        self.assertIn("IntersectionObserver", content)
        self.assertIn("setupIntersectionObserver", content)

    def test_mutation_observer(self):
        """Vérifier l'utilisation de MutationObserver"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier MutationObserver
        self.assertIn("MutationObserver", content)
        self.assertIn("checkForEmptyStates", content)

    def test_settings_system(self):
        """Vérifier le système de paramètres"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les paramètres
        self.assertIn("loadSettings(", content)
        self.assertIn("updateSettings(", content)
        self.assertIn("getSettings(", content)
        self.assertIn("localStorage", content)

    def test_auto_detection(self):
        """Vérifier le système de détection automatique"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la détection automatique
        self.assertIn("autoDetect", content)
        self.assertIn("isContainerEmpty", content)
        self.assertIn("data-empty-state", content)

    def test_particles_system(self):
        """Vérifier le système de particules"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les particules
        self.assertIn("generateParticles", content)
        self.assertIn("showParticles", content)
        self.assertIn("universal-empty-state-particle", content)

    def test_progress_bar(self):
        """Vérifier la barre de progression"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la barre de progression
        self.assertIn("universal-empty-state-progress", content)
        self.assertIn("showProgress", content)
        self.assertIn("animate", content)

    def test_theme_system(self):
        """Vérifier le système de thèmes"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les thèmes
        themes = ["arkalia", "matrix", "cyberpunk", "ocean"]
        for theme in themes:
            self.assertIn(theme, content)

    def test_action_system(self):
        """Vérifier le système d'actions"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les actions
        self.assertIn("actions", content)
        self.assertIn("universal-empty-state-actions", content)
        self.assertIn("universal-empty-state-btn", content)
        self.assertIn("primary", content)

    def test_initialization(self):
        """Vérifier l'initialisation du système"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'initialisation
        self.assertIn("DOMContentLoaded", content)
        self.assertIn("window.universalEmptyStates", content)
        self.assertIn("Universal Empty States System prêt", content)

    def test_global_export(self):
        """Vérifier l'export global"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'export
        self.assertIn("window.UniversalEmptyStates", content)

    def test_debug_methods(self):
        """Vérifier les méthodes de debug"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les méthodes de debug
        self.assertIn("getActiveEmptyStates(", content)
        self.assertIn("clearAllEmptyStates(", content)

    def test_syntax_validation(self):
        """Vérifier la syntaxe JavaScript"""
        import subprocess

        result = subprocess.run(
            ["node", "-c", "static/js/universal-empty-states.js"],
            check=False, capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Erreur de syntaxe: {result.stderr}")

    def test_file_size_reasonable(self):
        """Vérifier que la taille du fichier est raisonnable"""
        file_size = os.path.getsize("static/js/universal-empty-states.js")
        # Le fichier ne devrait pas dépasser 50KB
        self.assertLess(file_size, 50000, "Le fichier est trop volumineux")

    def test_no_console_errors(self):
        """Vérifier qu'il n'y a pas d'erreurs de console évidentes"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier qu'il n'y a pas de console.error ou console.warn
        self.assertNotIn("console.error", content)
        self.assertNotIn("console.warn", content)

        # Vérifier qu'il y a des console.log appropriés
        self.assertIn("console.log", content)

    def test_default_methods(self):
        """Vérifier les méthodes de valeurs par défaut"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les méthodes de défaut
        self.assertIn("getDefaultTitle(", content)
        self.assertIn("getDefaultDescription(", content)
        self.assertIn("getDefaultIcon(", content)
        self.assertIn("getDefaultActions(", content)

    def test_container_detection(self):
        """Vérifier la détection de conteneurs vides"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la détection
        self.assertIn("isContainerEmpty", content)
        self.assertIn("textContent.trim()", content)
        self.assertIn("children.length", content)

    def test_animation_types(self):
        """Vérifier les types d'animations"""
        with open("static/js/universal-empty-states.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les types d'animations
        self.assertIn("slide-in", content)
        self.assertIn("fade-in", content)
        self.assertIn("animation", content)


if __name__ == "__main__":
    unittest.main()
