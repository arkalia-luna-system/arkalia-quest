"""
Tests corrigés pour core/commands/analytics_commands.py
Utilise la vraie structure de retour des méthodes
"""

from unittest.mock import Mock, patch

import pytest

from core.commands.analytics_commands import AnalyticsCommands


class TestAnalyticsCommands:
    """Tests pour AnalyticsCommands avec structure de retour correcte"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.analytics_commands = AnalyticsCommands()

    @patch("core.commands.analytics_commands.requests.get")
    def test_cmd_analytics_success(self, mock_get):
        """Test commande analytics avec succès"""
        # Mock de la réponse API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "analytics": {
                "total_users": 100,
                "total_sessions": 500,
                "total_playtime_hours": 1000,
                "avg_playtime_per_user": 10,
                "recent_sessions_7_days": 50,
                "engagement_metrics": {
                    "retention_rate_7_days": 80,
                    "mission_completion_rate": 75,
                    "avg_engagement_score": 85,
                },
                "popular_events": {"mission_complete": 100, "level_up": 50},
            }
        }
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_analytics()

        assert result["réussite"] is True
        assert "ANALYTICS GLOBAUX" in result["message"]
        assert result["ascii_art"] == "📊"
        assert result["score_gagne"] == 5

    @patch("core.commands.analytics_commands.requests.get")
    def test_cmd_analytics_error(self, mock_get):
        """Test commande analytics avec erreur API"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_analytics()

        assert result["réussite"] is False
        assert "Erreur lors de la récupération" in result["message"]
        assert result["ascii_art"] == "❌"

    @patch("core.commands.analytics_commands.requests.get")
    def test_cmd_analytics_exception(self, mock_get):
        """Test commande analytics avec exception"""
        mock_get.side_effect = Exception("Connection error")

        result = self.analytics_commands.cmd_analytics()

        assert result["réussite"] is False
        assert "Erreur: Connection error" in result["message"]
        assert result["ascii_art"] == "💥"

    @patch("core.commands.analytics_commands.requests.get")
    def test_cmd_insights_success(self, mock_get):
        """Test commande insights avec succès"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "insights": {
                "learning_style": "visual",
                "recommendations": ["Try more visual content"],
                "progress_analysis": "Good progress",
            }
        }
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_insights()

        assert result["réussite"] is True
        assert "INSIGHTS PERSONNALISÉS" in result["message"]
        assert result["ascii_art"] == "🔍"

    @patch("core.commands.analytics_commands.requests.get")
    def test_cmd_insights_error(self, mock_get):
        """Test commande insights avec erreur"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_insights()

        assert result["réussite"] is False
        assert "Erreur lors de la récupération" in result["message"]

    @patch("core.commands.analytics_commands.requests.get")
    def test_cmd_export_data_success(self, mock_get):
        """Test commande export data avec succès"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "export_url": "http://example.com/export.zip",
            "file_size": "2.5MB",
        }
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_export_data()

        assert result["réussite"] is True
        assert "Export réussi" in result["message"]
        assert result["ascii_art"] == "📤"

    @patch("core.commands.analytics_commands.requests.get")
    def test_cmd_export_data_error(self, mock_get):
        """Test commande export data avec erreur"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_export_data()

        assert result["réussite"] is False
        assert "Erreur lors de l'export" in result["message"]

    def test_cmd_analytics_empty_data(self):
        """Test commande analytics avec données vides"""
        with patch("core.commands.analytics_commands.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"analytics": {}}
            mock_get.return_value = mock_response

            result = self.analytics_commands.cmd_analytics()

            assert result["réussite"] is True
            assert "ANALYTICS GLOBAUX" in result["message"]

    def test_cmd_insights_empty_data(self):
        """Test commande insights avec données vides"""
        with patch("core.commands.analytics_commands.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"insights": {}}
            mock_get.return_value = mock_response

            result = self.analytics_commands.cmd_insights()

            # La méthode retourne False pour des données vides
            assert result["réussite"] is False
            assert "Aucun insight disponible" in result["message"]

    def test_timeout_handling(self):
        """Test gestion des timeouts"""
        with patch("core.commands.analytics_commands.requests.get") as mock_get:
            mock_get.side_effect = Exception("Timeout")

            result = self.analytics_commands.cmd_analytics()

            assert result["réussite"] is False
            assert "Erreur: Timeout" in result["message"]

    def test_commands_structure(self):
        """Test structure des commandes"""
        assert isinstance(self.analytics_commands.commands, dict)
        expected_commands = [
            "analytics",
            "insights",
            "stats",
            "progress",
            "recommendations",
            "learning_style",
            "engagement",
            "export_data",
        ]
        for cmd in expected_commands:
            assert cmd in self.analytics_commands.commands

    def test_base_url_configuration(self):
        """Test configuration de l'URL de base"""
        assert self.analytics_commands.base_url == "http://localhost:5001"
