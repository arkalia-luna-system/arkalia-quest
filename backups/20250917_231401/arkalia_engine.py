"""
Arkalia Engine - Moteur principal du jeu Arkalia Quest
Version finale ultra-propre - Juillet 2025
"""

import json
import logging
import os
from datetime import datetime
from typing import Any

from core.database import DatabaseManager

try:
    from utils.logger import game_logger
except ImportError:
    # Fallback si le module utils est en conflit
    game_logger = logging.getLogger("arkalia_game")  # type: ignore


class ProfileManager:
    """Gestionnaire de profils joueurs"""

    def __init__(self):
        self.db_manager = DatabaseManager()

    def load_main_profile(self) -> dict[str, Any]:
        """Charge le profil principal du joueur depuis SQLite"""
        profile = self.db_manager.load_profile("main_user")
        if profile:
            return profile
        return self._create_default_profile()

    def save_main_profile(self, profile: dict[str, Any]) -> bool:
        """Sauvegarde le profil principal dans SQLite avec vérification de structure"""
        # Vérification de structure minimale
        required_keys = [
            "name",
            "score",
            "level",
            "badges",
            "preferences",
            "personnalite",
            "progression",
        ]
        for key in required_keys:
            if key not in profile:
                game_logger.error(
                    f"Erreur sauvegarde profil: clé manquante '{key}' dans le profil !",
                )
                return False
        if not isinstance(profile.get("badges", []), list):
            game_logger.error("Erreur sauvegarde profil: 'badges' doit être une liste !")
            return False
        if not isinstance(profile.get("preferences", {}), dict):
            game_logger.error("Erreur sauvegarde profil: 'preferences' doit être un dictionnaire !")
            return False
        # Vérification de la sous-structure 'personnalite'
        if not isinstance(profile.get("personnalite", {}), dict):
            game_logger.error(
                "Erreur sauvegarde profil: 'personnalite' doit être un dictionnaire !",
            )
            return False
        # Vérification de la sous-structure 'progression'
        if not isinstance(profile.get("progression", {}), dict):
            game_logger.error("Erreur sauvegarde profil: 'progression' doit être un dictionnaire !")
            return False
        return self.db_manager.save_profile("main_user", profile)

    def _create_default_profile(self) -> dict[str, Any]:
        """Crée un profil par défaut"""
        return {
            "id": "default",
            "name": "Hacker",
            "score": 0,
            "level": 1,
            "badges": [],
            "preferences": {},
            "personnalite": {
                "type": "non_detecte",
                "traits": [],
                "missions_completees": [],
                "monde_debloque": "arkalia_base",
            },
            "progression": {
                "niveau": 1,
                "univers_debloques": ["arkalia_base"],
                "portails_ouverts": [],
                "zones_debloquees": [],
            },
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
        }


class LunaAI:
    """IA LUNA pour analyse de personnalité"""

    def analyze_personality(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Analyse la personnalité du joueur"""
        try:
            # Analyse basée sur les actions et préférences
            traits = []
            if profile.get("score", 0) > 100:
                traits.append("expert")
            if len(profile.get("badges", [])) > 5:
                traits.append("collecteur")
            if profile.get("level", 1) > 3:
                traits.append("persévérant")

            return {
                "type": "hacker_" + ("expert" if traits else "débutant"),
                "traits": traits,
                "confiance": min(profile.get("score", 0) / 100, 1.0),
                "analyse_date": datetime.now().isoformat(),
            }
        except Exception as e:
            game_logger.error(f"Erreur analyse personnalité: {e}")
            return {"type": "non_detecte", "traits": [], "confiance": 0.0}


class MissionEngine:
    """Moteur de génération de missions"""

    def generate_personalized_mission(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Génère une mission personnalisée"""
        try:
            level = profile.get("level", 1)
            completed_missions = profile.get("personnalite", {}).get("missions_completees", [])

            # Mission adaptée au niveau
            if level <= 2:
                mission_type = "tutoriel"
                difficulty = "facile"
            elif level <= 4:
                mission_type = "intermédiaire"
                difficulty = "moyen"
            else:
                mission_type = "expert"
                difficulty = "difficile"

            return {
                "id": f"mission_perso_{len(completed_missions) + 1}",
                "type": mission_type,
                "difficulty": difficulty,
                "title": f"Mission personnalisée niveau {level}",
                "description": f"Mission adaptée à ton niveau {level}",
                "objectives": ["Objectif 1", "Objectif 2"],
                "rewards": {"xp": level * 10, "badges": []},
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            game_logger.error(f"Erreur génération mission: {e}")
            return {"id": "error", "type": "erreur", "title": "Erreur de génération"}


class ContentManager:
    """Gestionnaire de contenu disponible"""

    def get_available_content(self) -> dict[str, Any]:
        """Retourne le contenu disponible"""
        try:
            return {
                "missions": self._get_available_missions(),
                "badges": self._get_available_badges(),
                "avatars": self._get_available_avatars(),
                "themes": self._get_available_themes(),
                "updated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            game_logger.error(f"Erreur contenu disponible: {e}")
            return {"error": str(e)}

    def get_mission_info(self, mission_name: str) -> dict[str, Any]:
        """Récupère les infos d'une mission depuis SQLite"""
        try:
            from core.database import DatabaseManager

            db_manager = DatabaseManager()
            mission = db_manager.load_mission(mission_name)
            if mission:
                return mission
            return {"error": f"Mission {mission_name} non trouvée"}
        except Exception as e:
            game_logger.error(f"Erreur mission info: {e}")
            return {"error": str(e)}

    def get_profile_summary(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Résumé du profil pour l'API"""
        try:
            return {
                "id": profile.get("id", "unknown"),
                "name": profile.get("name", "Hacker"),
                "level": profile.get("level", 1),
                "score": profile.get("score", 0),
                "badges_count": len(profile.get("badges", [])),
                "missions_completed": len(
                    profile.get("personnalite", {}).get("missions_completees", []),
                ),
                "last_login": profile.get("last_login", "unknown"),
                "summary_date": datetime.now().isoformat(),
            }
        except Exception as e:
            game_logger.error(f"Erreur résumé profil: {e}")
            return {"error": str(e)}

    def _get_available_missions(self) -> list[str]:
        """Liste des missions disponibles"""
        try:
            missions_dir = "data/missions"
            if os.path.exists(missions_dir):
                return [
                    f.replace(".json", "") for f in os.listdir(missions_dir) if f.endswith(".json")
                ]
            return []
        except Exception:
            return []

    def _get_available_badges(self) -> list[str]:
        """Liste des badges disponibles"""
        try:
            badges_path = "data/badges.json"
            if os.path.exists(badges_path):
                with open(badges_path, encoding="utf-8") as f:
                    badges_data = json.load(f)
                    return list(badges_data.keys())
            return []
        except Exception:
            return []

    def _get_available_avatars(self) -> list[str]:
        """Liste des avatars disponibles"""
        try:
            avatars_path = "data/avatars.json"
            if os.path.exists(avatars_path):
                with open(avatars_path, encoding="utf-8") as f:
                    avatars_data = json.load(f)
                    return list(avatars_data.keys())
            return []
        except Exception:
            return []

    def _get_available_themes(self) -> list[str]:
        """Liste des thèmes disponibles"""
        return ["default", "dark", "hacker", "neon", "retro"]


# Instance principale du moteur Arkalia
arkalia_engine = type(
    "ArkaliaEngine",
    (),
    {
        "profiles": ProfileManager(),
        "luna": LunaAI(),
        "missions": MissionEngine(),
        "content": ContentManager(),
        # Méthodes de compatibilité
        "get_available_content": lambda self: self.content.get_available_content(),
        "get_mission_info": lambda self, mission_name: self.content.get_mission_info(mission_name),
        "get_profile_summary": lambda self, profile: self.content.get_profile_summary(profile),
    },
)()
