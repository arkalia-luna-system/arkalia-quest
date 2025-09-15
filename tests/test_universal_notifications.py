#!/usr/bin/env python3
"""
Tests pour le système universel de notifications
"""

import os
import sys
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestUniversalNotifications(unittest.TestCase):
    """Tests pour le système universel de notifications"""

    def test_universal_notifications_file_exists(self):
        """Vérifier que le fichier universal-notifications.js existe"""
        self.assertTrue(os.path.exists("static/js/universal-notifications.js"))

    def test_universal_notifications_structure(self):
        """Vérifier la structure de la classe UniversalNotifications"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la classe principale
        self.assertIn("class UniversalNotifications", content)

        # Vérifier les méthodes principales
        self.assertIn("show(", content)
        self.assertIn("closeNotification(", content)
        self.assertIn("closeAllNotifications(", content)
        self.assertIn("processQueue(", content)

        # Vérifier les méthodes utilitaires
        self.assertIn("success(", content)
        self.assertIn("warning(", content)
        self.assertIn("error(", content)
        self.assertIn("info(", content)
        self.assertIn("loading(", content)
        self.assertIn("celebration(", content)
        self.assertIn("achievement(", content)
        self.assertIn("lunaMessage(", content)
        self.assertIn("missionComplete(", content)

    def test_notification_types(self):
        """Vérifier que tous les types de notifications sont supportés"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les types de notifications (vérifier dans les icônes)
        types = [
            "success",
            "warning",
            "error",
            "info",
            "loading",
            "celebration",
            "achievement",
            "luna",
            "hack",
            "security",
        ]
        for notification_type in types:
            self.assertIn(f"{notification_type}:", content)

    def test_icons_system(self):
        """Vérifier le système d'icônes"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la méthode getIcon
        self.assertIn("getIcon(", content)

        # Vérifier les icônes définies
        icons = ["✅", "⚠️", "❌", "ℹ️", "⏳", "🎉", "🏆", "⬆️", "🏅", "🎯", "🌙", "💻", "🛡️"]
        for icon in icons:
            self.assertIn(icon, content)

    def test_css_styles(self):
        """Vérifier que les styles CSS sont inclus"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les classes CSS principales
        css_classes = [
            "universal-notifications-container",
            "universal-notification",
            "universal-notification-header",
            "universal-notification-content",
            "universal-notification-close",
            "universal-notification-progress",
        ]

        for css_class in css_classes:
            self.assertIn(css_class, content)

    def test_animations(self):
        """Vérifier les animations CSS"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les animations
        animations = ["notificationSlideIn", "notificationSlideOut", "notificationPulse"]

        for animation in animations:
            self.assertIn(animation, content)

    def test_responsive_design(self):
        """Vérifier le design responsive"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les media queries
        self.assertIn("@media (max-width: 768px)", content)
        self.assertIn("max-width: none", content)

    def test_accessibility_features(self):
        """Vérifier les fonctionnalités d'accessibilité"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les attributs ARIA
        self.assertIn("setAttribute('role', 'alert')", content)
        self.assertIn("aria-live", content)
        self.assertIn("aria-label", content)

        # Vérifier la gestion du clavier
        self.assertIn("keydown", content)
        self.assertIn("Escape", content)

    def test_settings_system(self):
        """Vérifier le système de paramètres"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les paramètres
        self.assertIn("loadSettings(", content)
        self.assertIn("updateSettings(", content)
        self.assertIn("getSettings(", content)
        self.assertIn("localStorage", content)

    def test_queue_system(self):
        """Vérifier le système de queue"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la gestion de la queue
        self.assertIn("queue", content)
        self.assertIn("processQueue(", content)
        self.assertIn("maxNotifications", content)

    def test_auto_close_system(self):
        """Vérifier le système d'auto-fermeture"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'auto-fermeture
        self.assertIn("startAutoClose(", content)
        self.assertIn("setTimeout", content)
        self.assertIn("duration", content)

    def test_sound_vibration(self):
        """Vérifier les fonctionnalités son et vibration"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier le son
        self.assertIn("playNotificationSound(", content)
        self.assertIn("AudioContext", content)

        # Vérifier la vibration
        self.assertIn("vibrate(", content)
        self.assertIn("navigator.vibrate", content)

    def test_theme_system(self):
        """Vérifier le système de thèmes"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les thèmes
        themes = ["arkalia", "matrix", "cyberpunk"]
        for theme in themes:
            self.assertIn(theme, content)

    def test_priority_system(self):
        """Vérifier le système de priorité"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la priorité
        self.assertIn("priority", content)

    def test_actions_system(self):
        """Vérifier le système d'actions"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les actions
        self.assertIn("actions", content)
        self.assertIn("universal-notification-actions", content)
        self.assertIn("universal-notification-btn", content)

    def test_initialization(self):
        """Vérifier l'initialisation du système"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'initialisation
        self.assertIn("DOMContentLoaded", content)
        self.assertIn("window.universalNotifications", content)
        self.assertIn("Universal Notifications System prêt", content)

    def test_global_export(self):
        """Vérifier l'export global"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'export
        self.assertIn("window.UniversalNotifications", content)

    def test_debug_methods(self):
        """Vérifier les méthodes de debug"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les méthodes de debug
        self.assertIn("getActiveNotifications(", content)
        self.assertIn("getQueueLength(", content)
        self.assertIn("clearAll(", content)

    def test_syntax_validation(self):
        """Vérifier la syntaxe JavaScript"""
        import subprocess

        result = subprocess.run(
            ["node", "-c", "static/js/universal-notifications.js"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, f"Erreur de syntaxe: {result.stderr}")

    def test_file_size_reasonable(self):
        """Vérifier que la taille du fichier est raisonnable"""
        file_size = os.path.getsize("static/js/universal-notifications.js")
        # Le fichier ne devrait pas dépasser 50KB
        self.assertLess(file_size, 50000, "Le fichier est trop volumineux")

    def test_no_console_errors(self):
        """Vérifier qu'il n'y a pas d'erreurs de console évidentes"""
        with open("static/js/universal-notifications.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier qu'il n'y a pas de console.error ou console.warn
        self.assertNotIn("console.error", content)
        self.assertNotIn("console.warn", content)

        # Vérifier qu'il y a des console.log appropriés
        self.assertIn("console.log", content)


if __name__ == "__main__":
    unittest.main()
