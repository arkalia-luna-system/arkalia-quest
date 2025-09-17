"""
Profile Manager - Gestion des profils utilisateur
"""

from datetime import datetime
from typing import Any

from core.database import DatabaseManager


class ProfileManager:
    """Gestionnaire des profils utilisateur"""

    def __init__(self):
        self.db_manager = DatabaseManager()

    def load_profile(self, user_id: str) -> dict[str, Any]:
        profile = self.db_manager.load_profile(user_id)
        if profile:
            # S'assurer que le profil a toutes les clés nécessaires
            return self.ensure_profile_structure(profile)
        return self.create_default_profile()

    def save_profile(self, user_id: str, profile: dict[str, Any]):
        # S'assurer que le profil a la structure complète avant sauvegarde
        complete_profile = self.ensure_profile_structure(profile)
        self.db_manager.save_profile(user_id, complete_profile)

    def create_default_profile(self) -> dict[str, Any]:
        """Crée un profil par défaut avec toutes les clés nécessaires"""

        return {
            "id": "default",
            "name": "Hacker",
            "username": "Hacker",
            "score": 0,
            "level": 1,
            "niveau": 1,  # Compatibilité
            "badges": [],
            "avatars": [],
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
                "chapitres_completes": [],
                "etape_actuelle": "tutorial_etape_1",
            },
            "created_at": "2025-01-01T00:00:00",
            "last_login": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00",
        }

    def ensure_profile_structure(self, profile: dict[str, Any]) -> dict[str, Any]:
        """S'assure que le profil a toutes les clés nécessaires"""

        default_profile = self.create_default_profile()

        # Créer une copie pour éviter les modifications inattendues
        complete_profile = {}

        # Ajouter toutes les clés du profil par défaut
        for key, value in default_profile.items():
            complete_profile[key] = profile.get(key, value)

        # Correction spécifique pour les sous-dictionnaires
        if "personnalite" in profile and isinstance(profile["personnalite"], dict):
            complete_profile["personnalite"] = {}
            for k, v in default_profile["personnalite"].items():
                if k in profile["personnalite"]:
                    complete_profile["personnalite"][k] = profile["personnalite"][k]
                else:
                    complete_profile["personnalite"][k] = v

        if "progression" in profile and isinstance(profile["progression"], dict):
            complete_profile["progression"] = {}
            for k, v in default_profile["progression"].items():
                if k in profile["progression"]:
                    complete_profile["progression"][k] = profile["progression"][k]
                else:
                    complete_profile["progression"][k] = v

        return complete_profile

    def update_profile(self, user_id: str, updates: dict[str, Any]):
        """Met à jour le profil d'un utilisateur"""

        profile = self.load_profile(user_id)
        profile.update(updates)
        self.save_profile(user_id, profile)

    def add_badge(self, user_id: str, badge: str):
        """Ajoute un badge au profil"""

        profile = self.load_profile(user_id)
        if badge not in profile["badges"]:
            profile["badges"].append(badge)
            self.save_profile(user_id, profile)

    def add_score(self, user_id: str, points: int):
        """Ajoute des points au score"""

        profile = self.load_profile(user_id)
        profile["score"] += points

        # Calculer le niveau basé sur le score
        profile["level"] = (profile["score"] // 100) + 1
        profile["niveau"] = profile["level"]  # Compatibilité

        self.save_profile(user_id, profile)

    def get_all_profiles(self) -> dict[str, dict[str, Any]]:
        """Retourne tous les profils"""

        profiles = {}

        # This method will need to be adapted to use DatabaseManager
        # For now, it will return an empty dict as per the original logic
        # which relied on file system access.
        # If the intent was to fetch from DB, this method would need to be
        # refactored to use db_manager.get_all_profiles()

        return profiles

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
                print(
                    f"Erreur sauvegarde profil: clé manquante '{key}' dans le profil !"
                )
                return False
        if not isinstance(profile.get("badges", []), list):
            print("Erreur sauvegarde profil: 'badges' doit être une liste !")
            return False
        if not isinstance(profile.get("preferences", {}), dict):
            print("Erreur sauvegarde profil: 'preferences' doit être un dictionnaire !")
            return False
        # Vérification de la sous-structure 'personnalite'
        if not isinstance(profile.get("personnalite", {}), dict):
            print(
                "Erreur sauvegarde profil: 'personnalite' doit être un dictionnaire !"
            )
            return False
        # Vérification de la sous-structure 'progression'
        if not isinstance(profile.get("progression", {}), dict):
            print("Erreur sauvegarde profil: 'progression' doit être un dictionnaire !")
            return False
        return self.db_manager.save_profile("main_user", profile)

    def analyze_personality(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Analyse la personnalité du joueur"""
        try:
            from datetime import datetime

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
            print(f"Erreur analyse personnalité: {e}")
            return {"type": "non_detecte", "traits": [], "confiance": 0.0}

    def generate_personalized_mission(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Génère une mission personnalisée"""
        try:
            level = profile.get("level", 1)

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
                "id": f"mission_{mission_type}_{level}",
                "type": mission_type,
                "title": f"Mission {mission_type.title()} Niveau {level}",
                "difficulty": difficulty,
                "description": f"Mission adaptée à votre niveau {level}",
                "rewards": {"xp": level * 50, "coins": level * 25},
                "created_at": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Erreur génération mission: {e}")
            return {"id": "error", "type": "erreur", "title": "Erreur de génération"}

    def get_available_content(self) -> dict[str, Any]:
        """Retourne le contenu disponible"""
        try:
            from datetime import datetime

            return {
                "missions": self._get_available_missions(),
                "badges": self._get_available_badges(),
                "avatars": self._get_available_avatars(),
                "themes": self._get_available_themes(),
                "updated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Erreur contenu disponible: {e}")
            return {"error": str(e)}

    def get_mission_info(self, mission_name: str) -> dict[str, Any]:
        """Récupère les infos d'une mission depuis SQLite"""
        try:
            mission = self.db_manager.load_mission(mission_name)
            if mission:
                return mission
            return {"error": f"Mission {mission_name} non trouvée"}
        except Exception as e:
            print(f"Erreur mission info: {e}")
            return {"error": str(e)}

    def _get_available_missions(self) -> list[dict[str, Any]]:
        """Récupère les missions disponibles"""
        try:
            return [
                {"id": "intro", "name": "Introduction", "difficulty": "facile"},
                {"id": "hack_basic", "name": "Hack Basique", "difficulty": "moyen"},
                {
                    "id": "crypto_challenge",
                    "name": "Défi Crypto",
                    "difficulty": "difficile",
                },
            ]
        except Exception as e:
            print(f"Erreur missions disponibles: {e}")
            return []

    def _get_available_badges(self) -> list[dict[str, Any]]:
        """Récupère les badges disponibles"""
        try:
            return [
                {
                    "id": "first_step",
                    "name": "Premier Pas",
                    "description": "Première mission",
                },
                {"id": "hacker", "name": "Hacker", "description": "Hack réussi"},
                {"id": "expert", "name": "Expert", "description": "Niveau expert"},
            ]
        except Exception as e:
            print(f"Erreur badges disponibles: {e}")
            return []

    def _get_available_avatars(self) -> list[dict[str, Any]]:
        """Récupère les avatars disponibles"""
        try:
            return [
                {"id": "hacker1", "name": "Hacker 1", "image": "hacker1.png"},
                {"id": "hacker2", "name": "Hacker 2", "image": "hacker2.png"},
            ]
        except Exception as e:
            print(f"Erreur avatars disponibles: {e}")
            return []

    def _get_available_themes(self) -> list[dict[str, Any]]:
        """Récupère les thèmes disponibles"""
        try:
            return [
                {"id": "matrix", "name": "Matrix", "description": "Thème Matrix"},
                {
                    "id": "cyberpunk",
                    "name": "Cyberpunk",
                    "description": "Thème Cyberpunk",
                },
            ]
        except Exception as e:
            print(f"Erreur thèmes disponibles: {e}")
            return []
