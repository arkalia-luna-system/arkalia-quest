"""
Database Engine - Gestionnaire de base de données SQLite pour Arkalia Quest
"""

import json
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime
from typing import Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from utils.logger import game_logger
except ImportError:
    # Fallback si le module utils est en conflit
    game_logger = logging.getLogger("arkalia_game")


class DatabaseManager:
    """Gestionnaire de base de données SQLite pour Arkalia Quest"""

    def __init__(self, db_path: str = "arkalia.db"):
        self.db_path = db_path
        # Cache simple pour améliorer les performances
        self._profile_cache = {}
        self._mission_cache = {}
        self._cache_ttl = 300  # 5 minutes
        self._cache_timestamps = {}
        self.init_database()

    def init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Table des profils utilisateurs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    score INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    badges TEXT DEFAULT '[]',
                    avatars TEXT DEFAULT '[]',
                    preferences TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            )

            # Table des missions
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS missions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mission_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    difficulty TEXT DEFAULT 'medium',
                    timer INTEGER DEFAULT 30,
                    rewards TEXT DEFAULT '{}',
                    completed_by TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            )

            # Table des défis sociaux
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    challenge_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    timer INTEGER DEFAULT 30,
                    players TEXT DEFAULT '[]',
                    winner TEXT,
                    status TEXT DEFAULT 'waiting',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """,
            )

            # Table des logs d'apprentissage LUNA
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS luna_learning (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action_type TEXT NOT NULL,
                    action_data TEXT,
                    response TEXT,
                    success BOOLEAN DEFAULT TRUE,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES profiles (id)
                )
            """,
            )

            # Créer des index pour optimiser les performances
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_profiles_username ON profiles(username)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_profiles_score ON profiles(score)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_profiles_level ON profiles(level)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_missions_difficulty ON missions(difficulty)",
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_challenges_status ON challenges(status)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_luna_learning_user_time ON luna_learning(user_id, timestamp)",
            )

            conn.commit()

    def get_connection(self):
        """Obtient une connexion à la base de données avec optimisations"""
        conn = sqlite3.connect(self.db_path)
        # Optimisations SQLite
        conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        conn.execute("PRAGMA synchronous=NORMAL")  # Performance vs sécurité
        conn.execute("PRAGMA cache_size=10000")  # Cache de 10MB
        conn.execute("PRAGMA temp_store=MEMORY")  # Tables temporaires en mémoire
        return conn

    def _is_cache_valid(self, key: str) -> bool:
        """Vérifie si un élément du cache est encore valide"""
        if key not in self._cache_timestamps:
            return False
        return time.time() - self._cache_timestamps[key] < self._cache_ttl

    def _get_from_cache(self, cache_type: str, key: str) -> Optional[Any]:
        """Récupère un élément du cache"""
        cache_key = f"{cache_type}:{key}"
        if self._is_cache_valid(cache_key):
            return (
                self._profile_cache.get(cache_key)
                if cache_type == "profile"
                else self._mission_cache.get(cache_key)
            )
        return None

    def _set_cache(self, cache_type: str, key: str, value: Any):
        """Met en cache un élément"""
        cache_key = f"{cache_type}:{key}"
        if cache_type == "profile":
            self._profile_cache[cache_key] = value
        else:
            self._mission_cache[cache_key] = value
        self._cache_timestamps[cache_key] = time.time()

    def migrate_json_to_sqlite(self):
        """Migre les données JSON existantes vers SQLite"""
        # Migrer le profil principal
        try:
            profile_file = "data/profil_joueur.json"
            if os.path.exists(profile_file):
                with open(profile_file, encoding="utf-8") as f:
                    profile_data = json.load(f)

                self.save_profile("main_user", profile_data)
                game_logger.info("Migration du profil principal réussie")
        except Exception as e:
            game_logger.warning(f"Erreur migration profil: {e}")

        # Migrer les missions
        try:
            missions_dir = "data/missions"
            if os.path.exists(missions_dir):
                for filename in os.listdir(missions_dir):
                    if filename.endswith(".json"):
                        with open(f"{missions_dir}/{filename}", encoding="utf-8") as f:
                            mission_data = json.load(f)
                            self.save_mission(mission_data)
                game_logger.info("Migration des missions réussie")
        except Exception as e:
            game_logger.warning(f"Erreur migration missions: {e}")

    def save_profile(self, username: str, profile_data: dict[str, Any]) -> bool:
        """Sauvegarde un profil utilisateur"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Vérifier si le profil existe déjà
                cursor.execute(
                    "SELECT id FROM profiles WHERE username = ?", (username,)
                )
                existing = cursor.fetchone()

                if existing:
                    # Mettre à jour le profil existant
                    cursor.execute(
                        """
                        UPDATE profiles
                        SET score = ?, level = ?, badges = ?, avatars = ?,
                            preferences = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE username = ?
                    """,
                        (
                            profile_data.get("score", 0),
                            profile_data.get("level", profile_data.get("niveau", 1)),
                            json.dumps(profile_data.get("badges", [])),
                            json.dumps(profile_data.get("avatars", [])),
                            json.dumps(profile_data.get("preferences", {})),
                            username,
                        ),
                    )
                else:
                    # Créer un nouveau profil
                    cursor.execute(
                        """
                        INSERT INTO profiles (username, score, level, badges, avatars,
                                            preferences)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            username,
                            profile_data.get("score", 0),
                            profile_data.get("level", profile_data.get("niveau", 1)),
                            json.dumps(profile_data.get("badges", [])),
                            json.dumps(profile_data.get("avatars", [])),
                            json.dumps(profile_data.get("preferences", {})),
                        ),
                    )

                conn.commit()
                return True
        except Exception as e:
            game_logger.error(f"Erreur sauvegarde profil: {e}")
            return False

    def load_profile(self, username: str) -> Optional[dict[str, Any]]:
        """Charge un profil utilisateur"""
        # Vérifier le cache d'abord
        cached_profile = self._get_from_cache("profile", username)
        if cached_profile:
            return cached_profile

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM profiles WHERE username = ?", (username,))
                row = cursor.fetchone()

                if row:
                    profile_data = {
                        "id": row[0],
                        "username": row[1],
                        "name": row[1],  # Ajout de la clé 'name'
                        "score": row[2],
                        "level": row[3],  # Correction de 'niveau' vers 'level'
                        "niveau": row[3],  # Garder pour compatibilité
                        "badges": json.loads(row[4]),
                        "avatars": json.loads(row[5]),
                        "preferences": json.loads(row[6]),
                        "created_at": row[7],
                        "updated_at": row[8],
                    }
                    # Mettre en cache le profil récupéré
                    self._set_cache("profile", username, profile_data)
                    return profile_data
                return None
        except Exception as e:
            game_logger.error(f"Erreur chargement profil: {e}")
            return None

    def save_mission(self, mission_data: dict[str, Any]) -> bool:
        """Sauvegarde une mission"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO missions (mission_id, title, description,
                                                    difficulty, timer, rewards)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        mission_data.get("id", "unknown"),
                        mission_data.get("titre", "Mission"),
                        mission_data.get("description", ""),
                        mission_data.get("difficulte", "medium"),
                        mission_data.get("timer", 30),
                        json.dumps(mission_data.get("recompenses", {})),
                    ),
                )

                conn.commit()
                return True
        except Exception as e:
            game_logger.error(f"Erreur sauvegarde mission: {e}")
            return False

    def create_challenge(self, challenge_data: dict[str, Any]) -> Optional[int]:
        """Crée un nouveau défi social"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO challenges (challenge_id, title, description, timer,
                                          players)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        challenge_data.get(
                            "id", f"challenge_{datetime.now().timestamp()}"
                        ),
                        challenge_data.get("title", "Défi"),
                        challenge_data.get("description", ""),
                        challenge_data.get("timer", 30),
                        json.dumps(challenge_data.get("players", [])),
                    ),
                )

                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            game_logger.error(f"Erreur création défi: {e}")
            return None

    def log_luna_learning(
        self,
        user_id: int,
        action_type: str,
        action_data: dict[str, Any],
        response: str,
        success: bool = True,
    ):
        """Enregistre une action d'apprentissage de LUNA"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO luna_learning (user_id, action_type, action_data,
                                              response, success)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (user_id, action_type, json.dumps(action_data), response, success),
                )

                conn.commit()
        except Exception as e:
            game_logger.error(f"Erreur log apprentissage: {e}")

    def get_leaderboard(self, limit: int = 10) -> list[dict[str, Any]]:
        """Récupère le classement des joueurs"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT username, score, level, badges
                    FROM profiles
                    ORDER BY score DESC
                    LIMIT ?
                """,
                    (limit,),
                )

                return [
                    {
                        "username": row[0],
                        "score": row[1],
                        "level": row[2],
                        "badges_count": len(json.loads(row[3])),
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            game_logger.error(f"Erreur classement: {e}")
            return []

    def load_all_missions(self) -> list[dict[str, Any]]:
        """Charge toutes les missions depuis la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM missions")
                rows = cursor.fetchall()

                missions = []
                for row in rows:
                    missions.append(
                        {
                            "id": row[0],
                            "mission_id": row[1],
                            "title": row[2],
                            "description": row[3],
                            "difficulty": row[4],
                            "timer": row[5],
                            "rewards": json.loads(row[6]),
                            "completed_by": json.loads(row[7]),
                            "created_at": row[8],
                        },
                    )
                return missions
        except Exception as e:
            game_logger.error(f"Erreur chargement missions: {e}")
            return []

    def load_mission(self, mission_id: str) -> Optional[dict[str, Any]]:
        """Charge une mission spécifique par son ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM missions WHERE mission_id = ?", (mission_id,)
                )
                row = cursor.fetchone()

                if row:
                    return {
                        "id": row[0],
                        "mission_id": row[1],
                        "title": row[2],
                        "description": row[3],
                        "difficulty": row[4],
                        "timer": row[5],
                        "rewards": json.loads(row[6]),
                        "completed_by": json.loads(row[7]),
                        "created_at": row[8],
                    }
                return None
        except Exception as e:
            game_logger.error(f"Erreur chargement mission {mission_id}: {e}")
            return None

    def load_all_profiles(self) -> list[dict[str, Any]]:
        """Charge tous les profils utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM profiles")
                rows = cursor.fetchall()

                profiles = []
                for row in rows:
                    profiles.append(
                        {
                            "id": row[0],
                            "username": row[1],
                            "score": row[2],
                            "level": row[3],
                            "badges": json.loads(row[4]),
                            "avatars": json.loads(row[5]),
                            "preferences": json.loads(row[6]),
                            "created_at": row[7],
                            "updated_at": row[8],
                        },
                    )
                return profiles
        except Exception as e:
            game_logger.error(f"Erreur chargement profils: {e}")
            return []


# Instance globale
db_manager = DatabaseManager()
