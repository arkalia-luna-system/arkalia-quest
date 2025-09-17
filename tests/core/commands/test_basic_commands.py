"""
Tests pour core/commands/basic_commands.py
"""

from unittest.mock import patch

import pytest

from core.commands.basic_commands import BasicCommands


@pytest.fixture
def basic_commands():
    with patch("core.commands.basic_commands.CustomizationEngine"):
        return BasicCommands()


@pytest.fixture
def mock_profile():
    return {
        "level": 2,
        "missions_completed": ["intro"],
        "badges": ["first_hack"],
        "score": 150,
        "username": "test_user",
    }


def test_handle_aide_new_player(basic_commands):
    """Test aide pour nouveau joueur"""
    profile = {"level": 1, "missions_completed": []}
    result = basic_commands.handle_aide(profile)
    assert "BIENVENUE HACKER" in result["message"]
    assert "start_tutorial" in result["message"]


def test_handle_aide_experienced_player(basic_commands):
    """Test aide pour joueur expérimenté"""
    profile = {"level": 5, "missions_completed": ["intro", "acte_1"]}
    result = basic_commands.handle_aide(profile)
    assert "HACKER EN PROGRESSION" in result["message"]


def test_handle_profil_display(basic_commands, mock_profile):
    """Test affichage du profil"""
    result = basic_commands.handle_profil(mock_profile)
    assert "PROFIL ARKALIA QUEST" in result["message"]
    assert "150 points" in result["message"]


def test_handle_status_basic(basic_commands, mock_profile):
    """Test commande status"""
    result = basic_commands.handle_status(mock_profile)
    assert "STATUT" in result["message"]


def test_handle_clear(basic_commands):
    """Test commande clear"""
    profile = {"score": 0, "badges": []}
    result = basic_commands.handle_clear(profile)
    assert result["réussite"] is True
    assert "terminal" in result["message"].lower()


def test_handle_badges_display(basic_commands, mock_profile):
    """Test affichage des badges"""
    result = basic_commands.handle_badges(mock_profile)
    assert "badges" in result["message"].lower()


def test_handle_themes_list(basic_commands):
    """Test liste des thèmes"""
    result = basic_commands.handle_themes({})
    assert "thèmes" in result["message"].lower()


def test_handle_theme_set(basic_commands):
    """Test changement de thème"""
    result = basic_commands.handle_theme_set({})
    assert "thème" in result["message"].lower()


def test_handle_simple_hack(basic_commands):
    """Test mini-jeu simple hack"""
    profile = {"score": 0}
    result = basic_commands.handle_simple_hack(profile)
    assert "hack" in result["message"].lower()


def test_handle_sequence_game(basic_commands):
    """Test jeu de séquence"""
    profile = {"score": 0}
    result = basic_commands.handle_sequence_game(profile)
    assert "séquence" in result["message"].lower()


def test_handle_typing_challenge(basic_commands):
    """Test défi de frappe"""
    profile = {"score": 0}
    result = basic_commands.handle_typing_challenge(profile)
    assert (
        "frappe" in result["message"].lower() or "typing" in result["message"].lower()
    )


def test_handle_level_up(basic_commands, mock_profile):
    """Test simulation montée de niveau"""
    result = basic_commands.handle_level_up(mock_profile)
    assert "niveau" in result["message"].lower()


def test_handle_badge_unlock(basic_commands, mock_profile):
    """Test simulation déblocage badge"""
    result = basic_commands.handle_badge_unlock(mock_profile)
    assert "badge" in result["message"].lower()


def test_handle_matrix_mode(basic_commands):
    """Test mode Matrix"""
    profile = {"score": 0}
    result = basic_commands.handle_matrix_mode(profile)
    assert "matrix" in result["message"].lower()


def test_handle_cyberpunk_mode(basic_commands):
    """Test mode Cyberpunk"""
    profile = {"score": 0}
    result = basic_commands.handle_cyberpunk_mode(profile)
    assert "cyberpunk" in result["message"].lower()


def test_handle_debug_mode(basic_commands, mock_profile):
    """Test mode debug"""
    result = basic_commands.handle_debug_mode(mock_profile)
    assert "debug" in result["message"].lower()


def test_handle_check_objects(basic_commands, mock_profile):
    """Test vérification des objets"""
    result = basic_commands.handle_check_objects(mock_profile)
    assert (
        "objets" in result["message"].lower() or "objects" in result["message"].lower()
    )


def test_handle_unlock_universe(basic_commands, mock_profile):
    """Test déverrouillage univers"""
    result = basic_commands.handle_unlock_universe(mock_profile)
    assert (
        "univers" in result["message"].lower()
        or "universe" in result["message"].lower()
    )


def test_handle_scan_persona(basic_commands, mock_profile):
    """Test scan de personnalité"""
    result = basic_commands.handle_scan_persona(mock_profile)
    assert (
        "personnalité" in result["message"].lower()
        or "persona" in result["message"].lower()
    )


def test_handle_missions(basic_commands, mock_profile):
    """Test affichage des missions"""
    result = basic_commands.handle_missions(mock_profile)
    assert (
        "missions" in result["message"].lower()
        or "mission" in result["message"].lower()
    )


def test_handle_leaderboard(basic_commands):
    """Test classement"""
    result = basic_commands.handle_leaderboard({})
    assert (
        "classement" in result["message"].lower()
        or "leaderboard" in result["message"].lower()
    )


def test_handle_play_game(basic_commands):
    """Test lancement de jeu"""
    profile = {"score": 0}
    result = basic_commands.handle_play_game(profile)
    assert "jeu" in result["message"].lower() or "game" in result["message"].lower()


def test_handle_start_tutorial(basic_commands, mock_profile):
    """Test démarrage tutoriel"""
    result = basic_commands.handle_start_tutorial(mock_profile)
    assert (
        "tutorial" in result["message"].lower()
        or "tutorial" in result["message"].lower()
    )
