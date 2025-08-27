"""
Moteur d'Analytics et Suivi Utilisateur Data-Driven
Arkalia Quest - Système d'analyse comportementale éthique

Ce module implémente un système d'analytics avancé pour :
- Collecter des données d'engagement et d'apprentissage
- Analyser les patterns comportementaux
- Personnaliser l'expérience utilisateur
- Générer des insights pour l'amélioration du jeu
"""

import hashlib
import json
import logging
import sqlite3
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types d'événements analytics"""

    SESSION_START = "session_start"
    SESSION_END = "session_end"
    COMMAND_EXECUTED = "command_executed"
    MISSION_START = "mission_start"
    MISSION_COMPLETE = "mission_complete"
    MISSION_FAIL = "mission_fail"
    TUTORIAL_START = "tutorial_start"
    TUTORIAL_COMPLETE = "tutorial_complete"
    GAME_START = "game_start"
    GAME_COMPLETE = "game_complete"
    GAME_FAIL = "game_fail"
    BADGE_EARNED = "badge_earned"
    LEVEL_UP = "level_up"
    ERROR_OCCURRED = "error_occurred"
    HELP_REQUESTED = "help_requested"
    HINT_USED = "hint_used"
    TIME_SPENT = "time_spent"
    INTERACTION = "interaction"
    EMOTION_TRIGGERED = "emotion_triggered"


@dataclass
class AnalyticsEvent:
    """Structure d'un événement analytics"""

    event_type: EventType
    user_id: str
    timestamp: float
    session_id: str
    data: Dict[str, Any]
    context: Dict[str, Any]
    anonymized: bool = True


@dataclass
class UserProfile:
    """Profil analytics utilisateur"""

    user_id: str
    total_sessions: int
    total_playtime: float
    missions_completed: int
    games_completed: int
    badges_earned: int
    current_level: int
    preferred_games: List[str]
    learning_style: str
    engagement_score: float
    last_active: float
    created_at: float


@dataclass
class SessionData:
    """Données de session"""

    session_id: str
    user_id: str
    start_time: float
    end_time: Optional[float]
    duration: Optional[float]
    events_count: int
    missions_attempted: int
    games_played: int
    commands_used: List[str]


class AnalyticsEngine:
    """Moteur principal d'analytics"""

    def __init__(self, db_path: str = "arkalia.db"):
        self.db_path = db_path
        self.session_data = {}
        self.user_profiles = {}
        self.event_buffer = []
        self.buffer_lock = threading.Lock()
        self.anonymization_salt = "arkalia_quest_2024"

        # Initialiser la base de données
        self._init_database()
        self._load_user_profiles()

        # Configuration
        self.buffer_size = 50
        self.flush_interval = 300  # 5 minutes
        self.retention_days = 90

        # Démarrer le thread de flush automatique
        self._start_flush_thread()

    def _init_database(self):
        """Initialiser les tables analytics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Table des événements
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS analytics_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    session_id TEXT NOT NULL,
                    data TEXT NOT NULL,
                    context TEXT NOT NULL,
                    anonymized BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Table des profils utilisateurs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS analytics_user_profiles (
                    user_id TEXT PRIMARY KEY,
                    total_sessions INTEGER DEFAULT 0,
                    total_playtime REAL DEFAULT 0,
                    missions_completed INTEGER DEFAULT 0,
                    games_completed INTEGER DEFAULT 0,
                    badges_earned INTEGER DEFAULT 0,
                    current_level INTEGER DEFAULT 1,
                    preferred_games TEXT DEFAULT '[]',
                    learning_style TEXT DEFAULT 'unknown',
                    engagement_score REAL DEFAULT 0,
                    last_active REAL,
                    created_at REAL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Table des sessions
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS analytics_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    start_time REAL NOT NULL,
                    end_time REAL,
                    duration REAL,
                    events_count INTEGER DEFAULT 0,
                    missions_attempted INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    commands_used TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Index pour optimiser les requêtes
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_events_user_time ON analytics_events(user_id, timestamp)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_events_type ON analytics_events(event_type)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_sessions_user ON analytics_sessions(user_id)"
            )

            conn.commit()

    def _anonymize_user_id(self, user_id: str) -> str:
        """Anonymiser l'ID utilisateur"""
        return hashlib.sha256((user_id + self.anonymization_salt).encode()).hexdigest()[
            :16
        ]

    def track_event(
        self,
        event_type: EventType,
        user_id: str,
        session_id: str,
        data: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Tracker un événement"""
        try:
            # Anonymiser l'ID utilisateur
            anonymized_user_id = self._anonymize_user_id(user_id)

            event = AnalyticsEvent(
                event_type=event_type,
                user_id=anonymized_user_id,
                timestamp=time.time(),
                session_id=session_id,
                data=data or {},
                context=context or {},
                anonymized=True,
            )

            # Ajouter au buffer
            with self.buffer_lock:
                self.event_buffer.append(event)

                # Flush si le buffer est plein
                if len(self.event_buffer) >= self.buffer_size:
                    self._flush_buffer()

            # Mettre à jour les données de session
            self._update_session_data(event)

        except Exception as e:
            logger.error(f"Erreur lors du tracking d'événement: {e}")

    def _update_session_data(self, event: AnalyticsEvent):
        """Mettre à jour les données de session"""
        if event.session_id not in self.session_data:
            self.session_data[event.session_id] = SessionData(
                session_id=event.session_id,
                user_id=event.user_id,
                start_time=event.timestamp,
                end_time=None,
                duration=None,
                events_count=0,
                missions_attempted=0,
                games_played=0,
                commands_used=[],
            )

        session = self.session_data[event.session_id]
        session.events_count += 1

        # Compter les types d'événements spécifiques
        if event.event_type == EventType.MISSION_START:
            session.missions_attempted += 1
        elif event.event_type == EventType.GAME_START:
            session.games_played += 1
        elif event.event_type == EventType.COMMAND_EXECUTED:
            command = event.data.get("command", "")
            if command and command not in session.commands_used:
                session.commands_used.append(command)

    def start_session(
        self, user_id: str, session_id: str, context: Optional[Dict[str, Any]] = None
    ):
        """Démarrer une session"""
        self.track_event(
            EventType.SESSION_START,
            user_id,
            session_id,
            data={"session_id": session_id},
            context=context or {},
        )

    def end_session(self, user_id: str, session_id: str):
        """Terminer une session"""
        if session_id in self.session_data:
            session = self.session_data[session_id]
            session.end_time = time.time()
            session.duration = session.end_time - session.start_time

            # Sauvegarder la session
            self._save_session(session)

            # Mettre à jour le profil utilisateur
            self._update_user_profile(user_id, session)

        self.track_event(
            EventType.SESSION_END, user_id, session_id, data={"session_id": session_id}
        )

    def _save_session(self, session: SessionData):
        """Sauvegarder une session dans la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO analytics_sessions
                    (session_id, user_id, start_time, end_time, duration,
                     events_count, missions_attempted, games_played, commands_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        session.session_id,
                        session.user_id,
                        session.start_time,
                        session.end_time,
                        session.duration,
                        session.events_count,
                        session.missions_attempted,
                        session.games_played,
                        json.dumps(session.commands_used),
                    ),
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de session: {e}")

    def _update_user_profile(self, user_id: str, session: SessionData):
        """Mettre à jour le profil utilisateur"""
        anonymized_user_id = self._anonymize_user_id(user_id)

        if anonymized_user_id not in self.user_profiles:
            self.user_profiles[anonymized_user_id] = UserProfile(
                user_id=anonymized_user_id,
                total_sessions=0,
                total_playtime=0,
                missions_completed=0,
                games_completed=0,
                badges_earned=0,
                current_level=1,
                preferred_games=[],
                learning_style="unknown",
                engagement_score=0,
                last_active=time.time(),
                created_at=time.time(),
            )

        profile = self.user_profiles[anonymized_user_id]
        profile.total_sessions += 1
        profile.total_playtime += session.duration or 0
        profile.last_active = time.time()

        # Sauvegarder le profil
        self._save_user_profile(profile)

    def _save_user_profile(self, profile: UserProfile):
        """Sauvegarder un profil utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO analytics_user_profiles
                    (user_id, total_sessions, total_playtime, missions_completed,
                     games_completed, badges_earned, current_level, preferred_games,
                     learning_style, engagement_score, last_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        profile.user_id,
                        profile.total_sessions,
                        profile.total_playtime,
                        profile.missions_completed,
                        profile.games_completed,
                        profile.badges_earned,
                        profile.current_level,
                        json.dumps(profile.preferred_games),
                        profile.learning_style,
                        profile.engagement_score,
                        profile.last_active,
                        profile.created_at,
                    ),
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du profil: {e}")

    def _load_user_profiles(self):
        """Charger les profils utilisateurs depuis la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM analytics_user_profiles")
                rows = cursor.fetchall()

                for row in rows:
                    profile = UserProfile(
                        user_id=row[0],
                        total_sessions=row[1],
                        total_playtime=row[2],
                        missions_completed=row[3],
                        games_completed=row[4],
                        badges_earned=row[5],
                        current_level=row[6],
                        preferred_games=json.loads(row[7]),
                        learning_style=row[8],
                        engagement_score=row[9],
                        last_active=row[10],
                        created_at=row[11],
                    )
                    self.user_profiles[profile.user_id] = profile
        except Exception as e:
            logger.error(f"Erreur lors du chargement des profils: {e}")

    def _flush_buffer(self):
        """Vider le buffer d'événements"""
        if not self.event_buffer:
            return

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for event in self.event_buffer:
                    cursor.execute(
                        """
                        INSERT INTO analytics_events
                        (event_type, user_id, timestamp, session_id, data, context, anonymized)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            event.event_type.value,
                            event.user_id,
                            event.timestamp,
                            event.session_id,
                            json.dumps(event.data),
                            json.dumps(event.context),
                            event.anonymized,
                        ),
                    )

                conn.commit()

                # Vider le buffer
                self.event_buffer.clear()

        except Exception as e:
            logger.error(f"Erreur lors du flush du buffer: {e}")

    def _start_flush_thread(self):
        """Démarrer le thread de flush automatique"""

        def flush_worker():
            while True:
                time.sleep(self.flush_interval)
                with self.buffer_lock:
                    self._flush_buffer()

        thread = threading.Thread(target=flush_worker, daemon=True)
        thread.start()

    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Obtenir des insights pour un utilisateur"""
        anonymized_user_id = self._anonymize_user_id(user_id)

        if anonymized_user_id not in self.user_profiles:
            return {}

        profile = self.user_profiles[anonymized_user_id]

        # Calculer des métriques avancées
        avg_session_duration = (
            profile.total_playtime / profile.total_sessions
            if profile.total_sessions > 0
            else 0
        )
        engagement_rate = min(profile.engagement_score / 100, 1.0)

        # Analyser les préférences
        preferred_games = profile.preferred_games[:5] if profile.preferred_games else []

        # Déterminer le style d'apprentissage
        learning_style = self._analyze_learning_style(anonymized_user_id)

        return {
            "user_id": user_id,
            "total_sessions": profile.total_sessions,
            "total_playtime_hours": round(profile.total_playtime / 3600, 2),
            "avg_session_duration_minutes": round(avg_session_duration / 60, 2),
            "missions_completed": profile.missions_completed,
            "games_completed": profile.games_completed,
            "badges_earned": profile.badges_earned,
            "current_level": profile.current_level,
            "engagement_rate": round(engagement_rate, 2),
            "preferred_games": preferred_games,
            "learning_style": learning_style,
            "last_active_days": round((time.time() - profile.last_active) / 86400, 1),
            "recommendations": self._generate_recommendations(profile, learning_style),
        }

    def _analyze_learning_style(self, user_id: str) -> str:
        """Analyser le style d'apprentissage d'un utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Analyser les types d'événements
                cursor.execute(
                    """
                    SELECT event_type, COUNT(*) as count
                    FROM analytics_events
                    WHERE user_id = ?
                    GROUP BY event_type
                """,
                    (user_id,),
                )

                event_counts = dict(cursor.fetchall())

                # Déterminer le style basé sur les patterns
                tutorial_events = event_counts.get(EventType.TUTORIAL_START.value, 0)
                game_events = event_counts.get(EventType.GAME_START.value, 0)
                help_events = event_counts.get(EventType.HELP_REQUESTED.value, 0)
                hint_events = event_counts.get(EventType.HINT_USED.value, 0)

                if tutorial_events > game_events:
                    return "guided_learner"
                elif help_events > 0 or hint_events > 0:
                    return "support_seeker"
                elif game_events > tutorial_events:
                    return "hands_on_learner"
                else:
                    return "balanced_learner"

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du style d'apprentissage: {e}")
            return "unknown"

    def _generate_recommendations(
        self, profile: UserProfile, learning_style: str
    ) -> List[str]:
        """Générer des recommandations personnalisées"""
        recommendations = []

        # Recommandations basées sur le niveau
        if profile.current_level <= 3:
            recommendations.append("Commencer par les tutoriels de base")
            recommendations.append("Explorer les mini-jeux de logique")

        # Recommandations basées sur le style d'apprentissage
        if learning_style == "guided_learner":
            recommendations.append("Suivre les tutoriels étape par étape")
        elif learning_style == "hands_on_learner":
            recommendations.append("Essayer les défis pratiques")
            recommendations.append("Expérimenter avec les commandes")
        elif learning_style == "support_seeker":
            recommendations.append("Utiliser les indices quand nécessaire")
            recommendations.append("Demander de l'aide via le chat")

        # Recommandations basées sur l'engagement
        if profile.engagement_score < 50:
            recommendations.append("Essayer de nouveaux types de missions")
            recommendations.append("Participer aux défis communautaires")

        return recommendations[:5]  # Limiter à 5 recommandations

    def get_global_analytics(self) -> Dict[str, Any]:
        """Obtenir des analytics globaux"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Statistiques générales
                cursor.execute(
                    "SELECT COUNT(DISTINCT user_id) FROM analytics_user_profiles"
                )
                total_users = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT SUM(total_sessions) FROM analytics_user_profiles"
                )
                total_sessions = cursor.fetchone()[0] or 0

                cursor.execute(
                    "SELECT SUM(total_playtime) FROM analytics_user_profiles"
                )
                total_playtime = cursor.fetchone()[0] or 0

                # Événements populaires
                cursor.execute(
                    """
                    SELECT event_type, COUNT(*) as count
                    FROM analytics_events
                    GROUP BY event_type
                    ORDER BY count DESC
                    LIMIT 10
                """
                )
                popular_events = dict(cursor.fetchall())

                # Sessions récentes (7 derniers jours)
                week_ago = time.time() - (7 * 24 * 3600)
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM analytics_sessions
                    WHERE start_time > ?
                """,
                    (week_ago,),
                )
                recent_sessions = cursor.fetchone()[0]

                return {
                    "total_users": total_users,
                    "total_sessions": total_sessions,
                    "total_playtime_hours": round(total_playtime / 3600, 2),
                    "avg_playtime_per_user": (
                        round(total_playtime / total_users / 3600, 2)
                        if total_users > 0
                        else 0
                    ),
                    "recent_sessions_7_days": recent_sessions,
                    "popular_events": popular_events,
                    "engagement_metrics": self._calculate_engagement_metrics(),
                }

        except Exception as e:
            logger.error(f"Erreur lors du calcul des analytics globaux: {e}")
            return {}

    def _calculate_engagement_metrics(self) -> Dict[str, float]:
        """Calculer les métriques d'engagement"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Taux de rétention (utilisateurs actifs dans les 7 derniers jours)
                week_ago = time.time() - (7 * 24 * 3600)
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM analytics_user_profiles
                    WHERE last_active > ?
                """,
                    (week_ago,),
                )
                active_users = cursor.fetchone()[0] or 0

                cursor.execute("SELECT COUNT(*) FROM analytics_user_profiles")
                total_users = cursor.fetchone()[0] or 0

                retention_rate = (
                    (active_users / total_users * 100) if total_users > 0 else 0.0
                )

                # Taux de complétion des missions
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM analytics_events
                    WHERE event_type = ?
                """,
                    (EventType.MISSION_COMPLETE.value,),
                )
                completed_missions = cursor.fetchone()[0] or 0

                cursor.execute(
                    """
                    SELECT COUNT(*) FROM analytics_events
                    WHERE event_type IN (?, ?)
                """,
                    (EventType.MISSION_START.value, EventType.MISSION_COMPLETE.value),
                )
                total_missions = cursor.fetchone()[0] or 0

                completion_rate = (
                    (completed_missions / (total_missions / 2) * 100)
                    if total_missions > 0
                    else 0.0
                )

                return {
                    "retention_rate_7_days": round(float(retention_rate), 2),
                    "mission_completion_rate": round(float(completion_rate), 2),
                    "avg_engagement_score": self._get_avg_engagement_score(),
                }

        except Exception as e:
            logger.error(f"Erreur lors du calcul des métriques d'engagement: {e}")
            return {
                "retention_rate_7_days": 0.0,
                "mission_completion_rate": 0.0,
                "avg_engagement_score": 0.0,
            }

    def _get_avg_engagement_score(self) -> float:
        """Obtenir le score d'engagement moyen"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT AVG(engagement_score) FROM analytics_user_profiles"
                )
                result = cursor.fetchone()[0]
                return round(result or 0, 2)
        except Exception as e:
            logger.error(f"Erreur lors du calcul du score d'engagement moyen: {e}")
            return 0.0

    def cleanup_old_data(self):
        """Nettoyer les anciennes données"""
        try:
            cutoff_time = time.time() - (self.retention_days * 24 * 3600)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Supprimer les anciens événements
                cursor.execute(
                    "DELETE FROM analytics_events WHERE timestamp < ?", (cutoff_time,)
                )

                # Supprimer les anciennes sessions
                cursor.execute(
                    "DELETE FROM analytics_sessions WHERE start_time < ?",
                    (cutoff_time,),
                )

                conn.commit()

                logger.info(
                    f"Nettoyage des données antérieures à {self.retention_days} jours effectué"
                )

        except Exception as e:
            logger.error(f"Erreur lors du nettoyage des données: {e}")

    def export_data(self, user_id: Optional[str] = None, format: str = "json") -> str:
        """Exporter les données analytics"""
        try:
            if user_id:
                # Export pour un utilisateur spécifique
                # anonymized_user_id = self._anonymize_user_id(user_id)  # Variable non utilisée
                data = self.get_user_insights(user_id)

                if format == "json":
                    return json.dumps(data, indent=2, ensure_ascii=False)
                else:
                    return str(data)
            else:
                # Export global
                data = self.get_global_analytics()

                if format == "json":
                    return json.dumps(data, indent=2, ensure_ascii=False)
                else:
                    return str(data)

        except Exception as e:
            logger.error(f"Erreur lors de l'export des données: {e}")
            return "{}"


# Instance globale du moteur d'analytics
analytics_engine = AnalyticsEngine()
