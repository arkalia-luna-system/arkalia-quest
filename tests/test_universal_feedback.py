#!/usr/bin/env python3
"""
Tests pour le système universel de feedback
"""

import os
import sys
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestUniversalFeedback(unittest.TestCase):
    """Tests pour le système universel de feedback"""

    def test_universal_feedback_file_exists(self):
        """Vérifier que le fichier universal-feedback.js existe"""
        self.assertTrue(os.path.exists("static/js/universal-feedback.js"))

    def test_universal_feedback_structure(self):
        """Vérifier la structure de la classe UniversalFeedback"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la classe principale
        self.assertIn("class UniversalFeedback", content)

        # Vérifier les méthodes principales
        self.assertIn("showFeedback(", content)
        self.assertIn("hideFeedback(", content)
        self.assertIn("clearAllFeedbacks(", content)
        self.assertIn("createFeedback(", content)

        # Vérifier les méthodes utilitaires
        self.assertIn("success(", content)
        self.assertIn("warning(", content)
        self.assertIn("error(", content)
        self.assertIn("info(", content)
        self.assertIn("loading(", content)
        self.assertIn("celebration(", content)
        self.assertIn("achievement(", content)
        self.assertIn("levelUp(", content)
        self.assertIn("badgeEarned(", content)
        self.assertIn("missionComplete(", content)

    def test_feedback_types(self):
        """Vérifier que tous les types de feedback sont supportés"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les types de feedback (vérifier dans les fréquences)
        types = [
            "success",
            "warning",
            "error",
            "info",
            "loading",
            "celebration",
            "achievement",
        ]
        for feedback_type in types:
            self.assertIn(f"{feedback_type}:", content)

    def test_icons_system(self):
        """Vérifier le système d'icônes"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la méthode getDefaultIcon
        self.assertIn("getDefaultIcon(", content)

        # Vérifier les icônes définies
        icons = ["✅", "⚠️", "❌", "ℹ️", "⏳", "🎉", "🏆", "⬆️", "🏅", "🎯"]
        for icon in icons:
            self.assertIn(icon, content)

    def test_css_styles(self):
        """Vérifier que les styles CSS sont inclus"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les classes CSS principales
        css_classes = [
            "universal-feedback-container",
            "universal-feedback",
            "universal-feedback-content",
            "universal-feedback-icon",
            "universal-feedback-text",
            "universal-feedback-progress",
        ]

        for css_class in css_classes:
            self.assertIn(css_class, content)

    def test_animations(self):
        """Vérifier les animations CSS"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les animations
        animations = [
            "feedbackPulse",
            "celebrationBounce",
            "feedbackShake",
            "feedbackGlow",
            "loadingProgress",
        ]

        for animation in animations:
            self.assertIn(animation, content)

    def test_responsive_design(self):
        """Vérifier le design responsive"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les media queries
        self.assertIn("@media (max-width: 768px)", content)
        self.assertIn("max-width: 90vw", content)

    def test_audio_system(self):
        """Vérifier le système audio"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'audio
        self.assertIn("AudioContext", content)
        self.assertIn("playFeedbackSound(", content)
        self.assertIn("setupAudioContext", content)
        self.assertIn("soundVolume", content)

    def test_haptic_system(self):
        """Vérifier le système haptique"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la vibration
        self.assertIn("vibrate(", content)
        self.assertIn("navigator.vibrate", content)
        self.assertIn("hapticFeedback", content)
        self.assertIn("vibrationIntensity", content)

    def test_accessibility_features(self):
        """Vérifier les fonctionnalités d'accessibilité"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les attributs ARIA
        self.assertIn("setAttribute('role', 'alert')", content)
        self.assertIn("aria-live", content)
        self.assertIn("aria-label", content)
        self.assertIn("tabindex", content)

        # Vérifier la gestion du clavier
        self.assertIn("keydown", content)
        self.assertIn("Escape", content)

    def test_settings_system(self):
        """Vérifier le système de paramètres"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les paramètres
        self.assertIn("loadSettings(", content)
        self.assertIn("updateSettings(", content)
        self.assertIn("getSettings(", content)
        self.assertIn("localStorage", content)

    def test_queue_system(self):
        """Vérifier le système de queue"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la gestion de la queue
        self.assertIn("feedbackQueue", content)
        self.assertIn("processQueue(", content)
        self.assertIn("maxConcurrentFeedbacks", content)

    def test_auto_hide_system(self):
        """Vérifier le système d'auto-hide"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'auto-hide
        self.assertIn("startAutoHide(", content)
        self.assertIn("setTimeout", content)
        self.assertIn("duration", content)
        self.assertIn("autoHideDelay", content)

    def test_theme_system(self):
        """Vérifier le système de thèmes"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les thèmes
        themes = ["arkalia", "matrix", "cyberpunk", "ocean"]
        for theme in themes:
            self.assertIn(theme, content)

    def test_animation_types(self):
        """Vérifier les types d'animations"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les types d'animations
        self.assertIn("celebration", content)
        self.assertIn("shake", content)
        self.assertIn("glow", content)
        self.assertIn("animation", content)

    def test_integration_methods(self):
        """Vérifier les méthodes d'intégration"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'intégration
        self.assertIn("integrateWithNotifications(", content)
        self.assertIn("integrateWithEmptyStates(", content)
        self.assertIn("universalNotifications", content)
        self.assertIn("universalEmptyStates", content)

    def test_initialization(self):
        """Vérifier l'initialisation du système"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'initialisation
        self.assertIn("DOMContentLoaded", content)
        self.assertIn("window.universalFeedback", content)
        self.assertIn("Universal Feedback System prêt", content)

    def test_global_export(self):
        """Vérifier l'export global"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'export
        self.assertIn("window.UniversalFeedback", content)

    def test_debug_methods(self):
        """Vérifier les méthodes de debug"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les méthodes de debug
        self.assertIn("getActiveFeedbacks(", content)
        self.assertIn("getQueueLength(", content)
        self.assertIn("clearAll(", content)

    def test_syntax_validation(self):
        """Vérifier la syntaxe JavaScript"""
        import subprocess

        result = subprocess.run(
            ["node", "-c", "static/js/universal-feedback.js"],
            check=False, capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Erreur de syntaxe: {result.stderr}")

    def test_file_size_reasonable(self):
        """Vérifier que la taille du fichier est raisonnable"""
        file_size = os.path.getsize("static/js/universal-feedback.js")
        # Le fichier ne devrait pas dépasser 50KB
        self.assertLess(file_size, 50000, "Le fichier est trop volumineux")

    def test_no_console_errors(self):
        """Vérifier qu'il n'y a pas d'erreurs de console évidentes"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier qu'il n'y a pas de console.error (console.warn est acceptable pour les warnings)
        self.assertNotIn("console.error", content)

        # Vérifier qu'il y a des console.log appropriés
        self.assertIn("console.log", content)

    def test_feedback_frequencies(self):
        """Vérifier les fréquences audio"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les fréquences
        self.assertIn("frequencies", content)
        self.assertIn("success:", content)
        self.assertIn("warning:", content)
        self.assertIn("error:", content)

    def test_vibration_patterns(self):
        """Vérifier les patterns de vibration"""
        with open("static/js/universal-feedback.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les patterns
        self.assertIn("patterns", content)
        self.assertIn("vibrationIntensity", content)
        self.assertIn("multiplier", content)


if __name__ == "__main__":
    unittest.main()
