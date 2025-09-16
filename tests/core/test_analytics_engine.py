"""
Tests pour core/analytics_engine.py
"""

from unittest.mock import patch

import pytest

from core.analytics_engine import (
    AnalyticsEngine,
    AnalyticsEvent,
    EventType,
    SessionData,
    UserProfile,
)


@pytest.fixture()
def analytics_engine():
    with patch("core.analytics_engine.sqlite3.connect"):
        return AnalyticsEngine(db_path=":memory:")


@pytest.fixture()
def sample_event():
    return AnalyticsEvent(
        event_type=EventType.COMMAND_EXECUTED,
        user_id="test_user",
        timestamp=1234567890.0,
        session_id="session_123",
        data={"command": "help", "success": True},
        context={"level": 2},
    )


@pytest.fixture()
def sample_profile():
    return UserProfile(
        user_id="test_user",
        total_sessions=5,
        total_playtime=3600.0,
        missions_completed=3,
        games_completed=2,
        badges_earned=1,
        current_level=2,
        preferred_games=["hack", "sequence"],
        learning_style="visual",
        engagement_score=0.8,
        last_active=1234567890.0,
        created_at=1234560000.0,
    )


def test_event_type_enum():
    """Test que les types d'événements sont bien définis"""
    assert EventType.SESSION_START.value == "session_start"
    assert EventType.COMMAND_EXECUTED.value == "command_executed"
    assert EventType.MISSION_COMPLETE.value == "mission_complete"


def test_analytics_event_creation(sample_event):
    """Test création d'un événement analytics"""
    assert sample_event.event_type == EventType.COMMAND_EXECUTED
    assert sample_event.user_id == "test_user"
    assert sample_event.anonymized is True


def test_user_profile_creation(sample_profile):
    """Test création d'un profil utilisateur"""
    assert sample_profile.user_id == "test_user"
    assert sample_profile.current_level == 2
    assert sample_profile.engagement_score == 0.8


def test_session_data_creation():
    """Test création de données de session"""
    session = SessionData(
        session_id="session_123",
        user_id="test_user",
        start_time=1234567890.0,
        end_time=None,
        duration=None,
        events_count=0,
        missions_attempted=0,
        games_played=0,
        commands_used=[],
    )
    assert session.session_id == "session_123"
    assert session.end_time is None


def test_analytics_engine_init(analytics_engine):
    """Test initialisation du moteur analytics"""
    assert analytics_engine.db_path == ":memory:"
    assert hasattr(analytics_engine, "user_profiles")


def test_track_event(analytics_engine, sample_event):
    """Test enregistrement d'un événement"""
    analytics_engine.track_event(sample_event, "test_user", "session_123")
    # Vérifier que l'événement a été traité sans erreur
    assert True


def test_user_profiles_storage(analytics_engine, sample_profile):
    """Test stockage des profils utilisateur"""
    analytics_engine.user_profiles["test_user"] = sample_profile
    assert "test_user" in analytics_engine.user_profiles
    assert analytics_engine.user_profiles["test_user"].user_id == "test_user"
