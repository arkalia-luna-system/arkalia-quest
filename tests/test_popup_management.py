#!/usr/bin/env python3
"""
Tests pour le système de gestion des popups
"""

import os
import sys
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPopupManagement(unittest.TestCase):
    """Tests pour le système de gestion des popups"""

    def test_popup_manager_file_exists(self):
        """Vérifier que le fichier popup-manager.js existe"""
        self.assertTrue(os.path.exists("static/js/popup-manager.js"))

    def test_popup_coordinator_file_exists(self):
        """Vérifier que le fichier popup-coordinator.js existe"""
        self.assertTrue(os.path.exists("static/js/popup-coordinator.js"))

    def test_popup_manager_css_exists(self):
        """Vérifier que le fichier popup-manager.css existe"""
        self.assertTrue(os.path.exists("static/css/popup-manager.css"))

    def test_popup_manager_structure(self):
        """Vérifier la structure du PopupManager"""
        with open("static/js/popup-manager.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les classes principales
        self.assertIn("class PopupManager", content)
        self.assertIn("showPopup", content)
        self.assertIn("closePopup", content)
        self.assertIn("closeAllPopups", content)
        self.assertIn("processQueue", content)

    def test_popup_coordinator_structure(self):
        """Vérifier la structure du PopupCoordinator"""
        with open("static/js/popup-coordinator.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les classes principales
        self.assertIn("class PopupCoordinator", content)
        self.assertIn("disableAutoPopups", content)
        self.assertIn("redirectPopupsToManager", content)
        self.assertIn("coordinatePopup", content)

    def test_popup_priority_system(self):
        """Vérifier le système de priorité des popups"""
        with open("static/js/popup-manager.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les priorités
        self.assertIn("popup-priority-high", content)
        self.assertIn("popup-priority-medium", content)
        self.assertIn("popup-priority-low", content)
        self.assertIn("getPriorityValue", content)

    def test_popup_queue_system(self):
        """Vérifier le système de queue des popups"""
        with open("static/js/popup-manager.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier la gestion de la queue
        self.assertIn("popupQueue", content)
        self.assertIn("processQueue", content)
        self.assertIn("isProcessingQueue", content)

    def test_popup_types(self):
        """Vérifier les types de popups supportés"""
        with open("static/js/popup-manager.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les types de popups
        self.assertIn("showNotification", content)
        self.assertIn("showConfirmation", content)
        self.assertIn("showLoading", content)
        self.assertIn("replaceLunaMessage", content)
        self.assertIn("replaceMissionCompletion", content)

    def test_popup_css_styles(self):
        """Vérifier les styles CSS des popups"""
        with open("static/css/popup-manager.css", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les styles principaux
        self.assertIn(".popup-overlay", content)
        self.assertIn(".popup-content", content)
        self.assertIn(".popup-close", content)
        self.assertIn(".popup-priority-high", content)
        self.assertIn(".popup-priority-medium", content)
        self.assertIn(".popup-priority-low", content)

    def test_popup_animations(self):
        """Vérifier les animations des popups"""
        with open("static/css/popup-manager.css", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les animations
        self.assertIn("@keyframes popupFadeIn", content)
        self.assertIn("@keyframes popupFadeOut", content)
        self.assertIn("@keyframes spin", content)
        self.assertIn("@keyframes lunaFloat", content)

    def test_popup_responsive_design(self):
        """Vérifier le design responsive des popups"""
        with open("static/css/popup-manager.css", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les media queries
        self.assertIn("@media (max-width: 768px)", content)
        self.assertIn("max-width: 95vw", content)
        self.assertIn("flex-direction: column", content)

    def test_popup_event_handlers(self):
        """Vérifier les gestionnaires d'événements"""
        with open("static/js/popup-manager.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier les événements
        self.assertIn("addEventListener", content)
        self.assertIn("keydown", content)
        self.assertIn("Escape", content)
        self.assertIn("click", content)

    def test_popup_cleanup_system(self):
        """Vérifier le système de nettoyage des popups"""
        with open("static/js/popup-coordinator.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier le nettoyage
        self.assertIn("cleanupConflictingPopups", content)
        self.assertIn("processPopupQueue", content)

        # Vérifier que closeAllPopups est dans le PopupManager
        with open("static/js/popup-manager.js", encoding="utf-8") as f:
            manager_content = f.read()
        self.assertIn("closeAllPopups", manager_content)

    def test_popup_integration_with_existing_systems(self):
        """Vérifier l'intégration avec les systèmes existants"""
        with open("static/js/popup-coordinator.js", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'intégration
        self.assertIn("lunaVision", content)
        self.assertIn("dailyMissions", content)
        self.assertIn("zoneExploration", content)
        self.assertIn("motivationalEmptyStates", content)
        self.assertIn("smartNotifications", content)

    def test_popup_html_integration(self):
        """Vérifier l'intégration dans le HTML"""
        with open("templates/index.html", encoding="utf-8") as f:
            content = f.read()

        # Vérifier l'inclusion des fichiers
        self.assertIn("popup-manager.js", content)
        self.assertIn("popup-coordinator.js", content)
        self.assertIn("popup-manager.css", content)

    def test_popup_initialization_logs(self):
        """Vérifier que les scripts popup sont chargés sur la page d'accueil"""
        with open("templates/index.html", encoding="utf-8") as f:
            content = f.read()

        # Vérifier que les scripts sont inclus (pas les logs console, retirés en prod)
        self.assertIn("popup-manager.js", content)
        self.assertIn("popup-coordinator.js", content)


if __name__ == "__main__":
    unittest.main()
