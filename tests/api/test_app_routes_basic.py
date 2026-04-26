"""
Tests de l'ancien système terminal (arkalia-quest v1).
Ces routes n'existent plus dans la version narrative actuelle.
Ce fichier est conservé pour l'historique et ignoré dans la suite CI.
"""

import pytest

pytestmark = pytest.mark.skip(
    reason="Routes de l'ancien système terminal — non implémentées dans LUNA Hors Connexion v2"
)


def test_health_endpoint_ok():
    pass


def test_status_endpoint_ok():
    pass


def test_leaderboard_endpoints():
    pass


def test_terminal_command_post_minimal():
    pass


def test_websocket_challenge_flow_minimal():
    pass


def test_luna_v3_learning_stats():
    pass
