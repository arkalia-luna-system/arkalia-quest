"""
Database Engine - Gestionnaire de base de données SQLite pour Arkalia Quest
"""

import sqlite3
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class DatabaseManager:
    """Gestionnaire de base de données SQLite pour Arkalia Quest"""
    
    def __init__(self, db_path: str = "arkalia.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des profils utilisateurs
            cursor.execute("""
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
            """)
            
            # Table des missions
            cursor.execute("""
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
            """)
            
            # Table des défis sociaux
            cursor.execute("""
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
            """)
            
            # Table des logs d'apprentissage LUNA
            cursor.execute("""
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
            """)
            
            conn.commit()
    
    def migrate_json_to_sqlite(self):
        """Migre les données JSON existantes vers SQLite"""
        # Migrer le profil principal
        try:
            with open('data/profil_joueur.json', 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
                
            self.save_profile('main_user', profile_data)
            print("✅ Migration du profil principal réussie")
        except Exception as e:
            print(f"⚠️ Erreur migration profil: {e}")
        
        # Migrer les missions
        try:
            missions_dir = 'data/missions'
            if os.path.exists(missions_dir):
                for filename in os.listdir(missions_dir):
                    if filename.endswith('.json'):
                        with open(f'{missions_dir}/{filename}', 'r', encoding='utf-8') as f:
                            mission_data = json.load(f)
                            self.save_mission(mission_data)
                print("✅ Migration des missions réussie")
        except Exception as e:
            print(f"⚠️ Erreur migration missions: {e}")
    
    def save_profile(self, username: str, profile_data: Dict[str, Any]) -> bool:
        """Sauvegarde un profil utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Vérifier si le profil existe déjà
                cursor.execute("SELECT id FROM profiles WHERE username = ?", (username,))
                existing = cursor.fetchone()
                
                if existing:
                    # Mettre à jour le profil existant
                    cursor.execute("""
                        UPDATE profiles 
                        SET score = ?, level = ?, badges = ?, avatars = ?, preferences = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE username = ?
                    """, (
                        profile_data.get('score', 0),
                        profile_data.get('niveau', 1),
                        json.dumps(profile_data.get('badges', [])),
                        json.dumps(profile_data.get('avatars', [])),
                        json.dumps(profile_data.get('preferences', {})),
                        username
                    ))
                else:
                    # Créer un nouveau profil
                    cursor.execute("""
                        INSERT INTO profiles (username, score, level, badges, avatars, preferences)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        username,
                        profile_data.get('score', 0),
                        profile_data.get('niveau', 1),
                        json.dumps(profile_data.get('badges', [])),
                        json.dumps(profile_data.get('avatars', [])),
                        json.dumps(profile_data.get('preferences', {}))
                    ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde profil: {e}")
            return False
    
    def load_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Charge un profil utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM profiles WHERE username = ?", (username,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row[0],
                        'username': row[1],
                        'score': row[2],
                        'niveau': row[3],
                        'badges': json.loads(row[4]),
                        'avatars': json.loads(row[5]),
                        'preferences': json.loads(row[6]),
                        'created_at': row[7],
                        'updated_at': row[8]
                    }
                return None
        except Exception as e:
            print(f"❌ Erreur chargement profil: {e}")
            return None
    
    def save_mission(self, mission_data: Dict[str, Any]) -> bool:
        """Sauvegarde une mission"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO missions (mission_id, title, description, difficulty, timer, rewards)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    mission_data.get('id', 'unknown'),
                    mission_data.get('titre', 'Mission'),
                    mission_data.get('description', ''),
                    mission_data.get('difficulte', 'medium'),
                    mission_data.get('timer', 30),
                    json.dumps(mission_data.get('recompenses', {}))
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde mission: {e}")
            return False
    
    def create_challenge(self, challenge_data: Dict[str, Any]) -> Optional[int]:
        """Crée un nouveau défi social"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO challenges (challenge_id, title, description, timer, players)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    challenge_data.get('id', f"challenge_{datetime.now().timestamp()}"),
                    challenge_data.get('title', 'Défi'),
                    challenge_data.get('description', ''),
                    challenge_data.get('timer', 30),
                    json.dumps(challenge_data.get('players', []))
                ))
                
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"❌ Erreur création défi: {e}")
            return None
    
    def log_luna_learning(self, user_id: int, action_type: str, action_data: Dict[str, Any], response: str, success: bool = True):
        """Enregistre une action d'apprentissage de LUNA"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO luna_learning (user_id, action_type, action_data, response, success)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    action_type,
                    json.dumps(action_data),
                    response,
                    success
                ))
                
                conn.commit()
        except Exception as e:
            print(f"❌ Erreur log apprentissage: {e}")
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère le classement des joueurs"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT username, score, level, badges
                    FROM profiles 
                    ORDER BY score DESC 
                    LIMIT ?
                """, (limit,))
                
                return [
                    {
                        'username': row[0],
                        'score': row[1],
                        'level': row[2],
                        'badges_count': len(json.loads(row[3]))
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print(f"❌ Erreur classement: {e}")
            return []


# Instance globale
db_manager = DatabaseManager() 