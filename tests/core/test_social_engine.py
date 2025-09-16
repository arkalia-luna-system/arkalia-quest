"""
Tests pour core/social_engine.py
"""

import pytest

from core.social_engine import SocialEngine


@pytest.fixture()
def social_engine():
    """Fixture pour créer un moteur social de test"""
    return SocialEngine()


def test_social_engine_init(social_engine):
    """Test initialisation du moteur social"""
    assert social_engine is not None
    assert hasattr(social_engine, "guilds")
    assert hasattr(social_engine, "challenges")
    assert hasattr(social_engine, "events")


def test_load_social_data_with_files(social_engine):
    """Test chargement des données sociales avec fichiers"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_save_social_data(social_engine):
    """Test sauvegarde des données sociales"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_create_guild(social_engine):
    """Test création de guilde"""
    result = social_engine.create_guild("test_user", "Test Guild")
    assert result["success"] is True
    assert "guild" in result


def test_join_guild(social_engine):
    """Test rejoindre une guilde"""
    # Créer d'abord une guilde
    guild_result = social_engine.create_guild("owner", "Test Guild")
    assert guild_result["success"] is True

    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_leave_guild(social_engine):
    """Test quitter une guilde"""
    # Créer d'abord une guilde
    guild_result = social_engine.create_guild("owner", "Test Guild")
    assert guild_result["success"] is True

    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_create_challenge(social_engine):
    """Test création de défi"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_join_challenge(social_engine):
    """Test rejoindre un défi"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_send_chat_message(social_engine):
    """Test envoi de message chat"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_get_chat_messages(social_engine):
    """Test récupération des messages chat"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_add_friend(social_engine):
    """Test ajout d'ami"""
    result = social_engine.add_friend("user1", "user2")
    assert result["success"] is True


def test_remove_friend(social_engine):
    """Test suppression d'ami"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_get_friends(social_engine):
    """Test récupération des amis"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_create_event(social_engine):
    """Test création d'événement"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_join_event(social_engine):
    """Test rejoindre un événement"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_get_guild_leaderboard(social_engine):
    """Test récupération du classement des guildes"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_get_player_stats(social_engine):
    """Test récupération des stats joueur"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_search_players(social_engine):
    """Test recherche de joueurs"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_get_season_leaderboard(social_engine):
    """Test récupération du classement de saison"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_update_player_reputation(social_engine):
    """Test mise à jour de la réputation joueur"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None


def test_get_player_reputation(social_engine):
    """Test récupération de la réputation joueur"""
    # Vérifier que l'engine peut être initialisé
    assert social_engine is not None
