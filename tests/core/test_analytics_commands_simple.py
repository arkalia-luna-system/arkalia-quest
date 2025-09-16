"""
Tests simplifiés pour analytics_commands.py
"""

from unittest.mock import Mock, patch

import pytest

from core.commands.analytics_commands import AnalyticsCommands


class TestAnalyticsCommands:
    """Tests pour la classe AnalyticsCommands"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.analytics_commands = AnalyticsCommands()

    def test_init(self):
        """Test de l'initialisation"""
        assert hasattr(self.analytics_commands, "base_url")
        assert self.analytics_commands.base_url == "http://localhost:5001"
        assert hasattr(self.analytics_commands, "commands")

    @patch("requests.get")
    def test_cmd_analytics_success(self, mock_get):
        """Test de cmd_analytics avec succès"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "analytics": {"total_users": 100, "active_users": 50}
        }
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_analytics()

        assert isinstance(result, dict)
        assert "réussite" in result
        assert "message" in result
        assert "ANALYTICS GLOBAUX" in result["message"]
        mock_get.assert_called_once_with(
            "http://localhost:5001/api/analytics/global", timeout=10
        )

    @patch("requests.get")
    def test_cmd_analytics_error(self, mock_get):
        """Test de cmd_analytics avec erreur"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_analytics()

        assert isinstance(result, dict)
        assert "réussite" in result
        assert "message" in result
        assert "Erreur" in result["message"]

    @patch("requests.get")
    def test_cmd_insights_success(self, mock_get):
        """Test de cmd_insights avec succès"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "insights": {"learning_patterns": ["pattern1"]}
        }
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_insights()

        assert isinstance(result, dict)
        assert "réussite" in result
        assert "message" in result
        assert "INSIGHTS" in result["message"]

    @patch("requests.get")
    def test_cmd_export_data_success(self, mock_get):
        """Test de cmd_export_data avec succès"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.analytics_commands.cmd_export_data()

        assert isinstance(result, dict)
        assert "réussite" in result
        assert "message" in result
        assert "EXPORT" in result["message"]

    def test_commands_dict(self):
        """Test du dictionnaire des commandes"""
        commands = self.analytics_commands.commands
        assert isinstance(commands, dict)
        assert "analytics" in commands
        assert "insights" in commands
        assert "export_data" in commands
