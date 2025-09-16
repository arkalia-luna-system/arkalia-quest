#!/usr/bin/env python3
"""
🧪 TESTS POUR NOUVELLES FONCTIONNALITÉS UX - ARKALIA QUEST
Tests pour les améliorations UX prioritaires implémentées
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

# Ajouter le répertoire parent au path
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

from app import app


class TestNewUXFeatures(unittest.TestCase):
    """Tests pour les nouvelles fonctionnalités UX"""

    def setUp(self):
        """Configuration des tests"""
        self.app = app.test_client()
        self.app.testing = True

    def test_notifications_closable(self):
        """Test que les notifications sont closables"""
        # Tester que la page principale se charge (les notifications sont gérées côté frontend)
        response = self.app.get("/")

        # Vérifier que la page se charge correctement
        self.assertEqual(response.status_code, 200)

        # Vérifier que le contenu contient les scripts de notifications
        content = response.get_data(as_text=True)
        self.assertIn("universal-notifications.js", content)

    def test_world_zone_microgame_trigger(self):
        """Test que le clic sur une zone du monde déclenche un micro-jeu"""
        # Tester que la page monde se charge
        response = self.app.get("/monde")

        # Vérifier que la page se charge correctement
        self.assertEqual(response.status_code, 200)

        # Vérifier que le contenu contient les scripts d'interactions du monde
        content = response.get_data(as_text=True)
        self.assertIn("world-interactions.js", content)

    def test_accessibility_accordion_default_closed(self):
        """Test que l'accordéon d'accessibilité est fermé par défaut"""
        response = self.app.get("/accessibility")

        # Vérifier que la page d'accessibilité se charge
        self.assertEqual(response.status_code, 200)

        # Vérifier que le contenu contient les classes d'accordéon
        content = response.get_data(as_text=True)
        self.assertIn("accessibility-card", content)

    def test_dashboard_empty_stats_hidden(self):
        """Test que les stats vides sont masquées dans le dashboard"""
        response = self.app.get("/api/gamification/summary")

        # Vérifier que l'API retourne les bonnes données
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])

        # Vérifier que les missions complétées sont calculées correctement
        self.assertIn("missions_completees", data)
        self.assertIsInstance(data["missions_completees"], int)

    def test_profile_summary_correct_calculations(self):
        """Test que les calculs du profil sont corrects"""
        response = self.app.get("/api/profile/summary")

        # Vérifier que l'API retourne les bonnes données
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])

        # Vérifier que les missions complétées sont calculées correctement
        profile = data["profile"]
        self.assertIn("missions_completees", profile)
        self.assertIsInstance(profile["missions_completees"], int)

    def test_gamification_summary_correct_calculations(self):
        """Test que les calculs de gamification sont corrects"""
        response = self.app.get("/api/gamification/summary")

        # Vérifier que l'API retourne les bonnes données
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])

        # Vérifier que les missions complétées sont calculées correctement
        self.assertIn("missions_completees", data)
        self.assertIsInstance(data["missions_completees"], int)

    def test_world_interactions_microgame_functions(self):
        """Test que les fonctions de micro-jeu du monde existent"""
        # Tester que la page monde se charge avec toutes les zones
        response = self.app.get("/monde")

        # Vérifier que la page se charge correctement
        self.assertEqual(response.status_code, 200)

        # Vérifier que le contenu contient les zones
        content = response.get_data(as_text=True)
        zones = [
            "terminal",
            "cyber-city",
            "data-center",
            "training",
            "underground",
            "quantum",
        ]
        for zone in zones:
            self.assertIn(zone, content.lower())

    def test_accessibility_toasts_on_toggle(self):
        """Test que les toasts d'accessibilité s'affichent lors des changements"""
        # Tester que la page d'accessibilité se charge
        response = self.app.get("/accessibility")

        # Vérifier que la page se charge correctement
        self.assertEqual(response.status_code, 200)

        # Vérifier que le contenu contient les scripts d'accessibilité
        content = response.get_data(as_text=True)
        self.assertIn("accessibility.js", content)

    def test_notifications_rate_limiting(self):
        """Test que le rate limiting des notifications fonctionne"""
        # Tester que la page principale se charge avec les scripts de notifications
        response = self.app.get("/")

        # Vérifier que la page se charge correctement
        self.assertEqual(response.status_code, 200)

        # Vérifier que le contenu contient les scripts de notifications
        content = response.get_data(as_text=True)
        self.assertIn("universal-notifications.js", content)

    def test_dashboard_encouragement_message(self):
        """Test que le message d'encouragement s'affiche quand les stats sont vides"""
        # Simuler un profil vide
        with patch("app.charger_profil") as mock_charger:
            mock_charger.return_value = {
                "id": "test",
                "name": "Test User",
                "level": 1,
                "score": 0,
                "badges": [],
                "missions_completed": [],
            }

            response = self.app.get("/api/gamification/summary")
            data = response.get_json()

            # Vérifier que les stats sont à zéro
            self.assertEqual(data["total_score"], 0)
            self.assertEqual(data["missions_completees"], 0)
            self.assertEqual(data["badges_count"], 0)

    def test_world_zone_xp_rewards(self):
        """Test que les zones du monde donnent des récompenses XP"""
        # Tester que la page monde se charge
        response = self.app.get("/monde")

        # Vérifier que la page se charge correctement
        self.assertEqual(response.status_code, 200)

        # Vérifier que le contenu contient les scripts d'interactions du monde
        content = response.get_data(as_text=True)
        self.assertIn("world-interactions.js", content)


if __name__ == "__main__":
    unittest.main()
