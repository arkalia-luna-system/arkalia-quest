"""
Tests de couverture pour core/database.py
Améliore la couverture des lignes manquantes
"""

import os
import tempfile
import unittest
from unittest.mock import patch
import sys

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import DatabaseManager


class TestDatabaseCoverage(unittest.TestCase):
    """Tests pour améliorer la couverture de database.py"""

    def setUp(self):
        """Configuration des tests"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)

    def tearDown(self):
        """Nettoyage après les tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_database_initialization(self):
        """Test l'initialisation de la base de données"""
        self.assertIsNotNone(self.db_manager)
        self.assertEqual(self.db_manager.db_path, self.temp_db.name)

    def test_create_tables(self):
        """Test la création des tables"""
        # Cette méthode devrait être appelée dans __init__
        # Vérifier que les tables existent
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn("profiles", tables)
            self.assertIn("missions", tables)
            # Vérifier qu'il y a au moins quelques tables
            self.assertGreaterEqual(len(tables), 2)

    def test_get_connection_success(self):
        """Test la connexion réussie"""
        with self.db_manager.get_connection() as conn:
            self.assertIsNotNone(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_get_connection_error(self):
        """Test la gestion d'erreur de connexion"""
        # Créer un chemin de DB invalide
        invalid_db = DatabaseManager("/invalid/path/database.db")

        # Mock pour simuler une erreur de connexion
        with patch("sqlite3.connect") as mock_connect:
            mock_connect.side_effect = Exception("Connection failed")

            with self.assertRaises(Exception):
                with invalid_db.get_connection():
                    pass

    def test_save_profile_success(self):
        """Test la sauvegarde réussie d'un profil"""
        profile_data = {
            "username": "test_user",
            "level": 1,
            "xp": 100,
            "badges": ["first_badge"],
            "missions_completed": ["intro"],
            "portails_ouverts": [],
        }

        result = self.db_manager.save_profile("test_user", profile_data)
        self.assertTrue(result)

    def test_save_profile_error(self):
        """Test la gestion d'erreur lors de la sauvegarde"""
        # Mock pour simuler une erreur SQL
        with patch.object(self.db_manager, "get_connection") as mock_conn:
            mock_conn.side_effect = Exception("Database error")

            profile_data = {"username": "test", "level": 1}
            result = self.db_manager.save_profile("test", profile_data)
            self.assertFalse(result)

    def test_load_profile_success(self):
        """Test le chargement réussi d'un profil"""
        # D'abord sauvegarder un profil
        profile_data = {
            "username": "test_user",
            "level": 1,
            "xp": 100,
            "badges": ["first_badge"],
            "missions_completed": ["intro"],
            "portails_ouverts": [],
        }
        self.db_manager.save_profile("test_user", profile_data)

        # Puis le charger
        loaded_profile = self.db_manager.load_profile("test_user")
        self.assertIsNotNone(loaded_profile)
        self.assertEqual(loaded_profile["username"], "test_user")

    def test_load_profile_not_found(self):
        """Test le chargement d'un profil inexistant"""
        profile = self.db_manager.load_profile("nonexistent_user")
        self.assertIsNone(profile)

    def test_load_profile_error(self):
        """Test la gestion d'erreur lors du chargement"""
        with patch.object(self.db_manager, "get_connection") as mock_conn:
            mock_conn.side_effect = Exception("Database error")

            profile = self.db_manager.load_profile("test")
            self.assertIsNone(profile)

    def test_save_mission_success(self):
        """Test la sauvegarde réussie d'une mission"""
        mission_data = {
            "mission_id": "test_mission",
            "title": "Test Mission",
            "description": "Test description",
            "difficulty": "medium",
            "timer": 30,
            "rewards": "{}",
            "completed_by": "[]",
        }

        result = self.db_manager.save_mission(mission_data)
        self.assertTrue(result)

    def test_save_mission_error(self):
        """Test la gestion d'erreur lors de la sauvegarde de mission"""
        with patch("sqlite3.connect") as mock_connect:
            mock_connect.side_effect = Exception("Database error")

            mission_data = {"mission_id": "test", "title": "Test"}
            result = self.db_manager.save_mission(mission_data)
            self.assertFalse(result)

    def test_load_mission_success(self):
        """Test le chargement réussi d'une mission"""
        # D'abord sauvegarder une mission
        mission_data = {
            "mission_id": "test_mission",
            "title": "Test Mission",
            "description": "Test description",
            "difficulty": "medium",
            "timer": 30,
            "rewards": "{}",
            "completed_by": "[]",
        }
        self.db_manager.save_mission(mission_data)

        # Puis la charger
        loaded_mission = self.db_manager.load_mission("test_mission")
        self.assertIsNotNone(loaded_mission)
        self.assertEqual(loaded_mission["mission_id"], "test_mission")

    def test_load_mission_not_found(self):
        """Test le chargement d'une mission inexistante"""
        mission = self.db_manager.load_mission("nonexistent_mission")
        self.assertIsNone(mission)

    def test_load_mission_error(self):
        """Test la gestion d'erreur lors du chargement de mission"""
        with patch("sqlite3.connect") as mock_connect:
            mock_connect.side_effect = Exception("Database error")

            mission = self.db_manager.load_mission("test")
            self.assertIsNone(mission)

    def test_cache_functionality(self):
        """Test le système de cache"""
        # Vérifier que le cache est initialisé
        self.assertIsInstance(self.db_manager._profile_cache, dict)
        self.assertIsInstance(self.db_manager._mission_cache, dict)

    def test_database_migration(self):
        """Test la migration de la base de données"""
        # Cette méthode devrait être appelée dans __init__
        # Vérifier que les tables sont créées correctement
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()

            # Vérifier la structure de la table profiles
            cursor.execute("PRAGMA table_info(profiles)")
            columns = [row[1] for row in cursor.fetchall()]
            expected_columns = ["username", "score", "level", "badges"]
            for col in expected_columns:
                self.assertIn(col, columns)


if __name__ == "__main__":
    unittest.main()
