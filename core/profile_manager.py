"""
Profile Manager - Gestion des profils utilisateur
"""

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
        else:
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
