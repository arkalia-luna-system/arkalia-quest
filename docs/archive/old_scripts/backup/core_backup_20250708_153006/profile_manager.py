"""
Profile Manager - Gestion des profils utilisateur
"""

import json
import os
from typing import Any


class ProfileManager:
    """Gestionnaire des profils utilisateur"""

    def __init__(self, profiles_dir: str = "data/profiles"):
        self.profiles_dir = profiles_dir
        os.makedirs(profiles_dir, exist_ok=True)

    def load_profile(self, user_id: str) -> dict[str, Any]:
        """Charge le profil d'un utilisateur"""

        profile_path = os.path.join(self.profiles_dir, f"{user_id}.json")

        if os.path.exists(profile_path):
            with open(profile_path, encoding="utf-8") as f:
                profile = json.load(f)
        else:
            profile = self.create_default_profile()

        # S'assurer que toutes les clés nécessaires existent
        profile = self.ensure_profile_structure(profile)

        return profile

    def save_profile(self, user_id: str, profile: dict[str, Any]):
        """Sauvegarde le profil d'un utilisateur"""

        profile_path = os.path.join(self.profiles_dir, f"{user_id}.json")

        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

    def create_default_profile(self) -> dict[str, Any]:
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
            "created_at": "2024-01-01T00:00:00",
            "last_login": "2024-01-01T00:00:00",
        }

    def ensure_profile_structure(self, profile: dict[str, Any]) -> dict[str, Any]:
        """S'assure que le profil a toutes les clés nécessaires"""

        default_profile = self.create_default_profile()

        # Ajouter les clés manquantes
        for key, value in default_profile.items():
            if key not in profile:
                profile[key] = value

        # Correction récursive pour les sous-dictionnaires
        if "personnalite" in profile:
            for k, v in default_profile["personnalite"].items():
                if k not in profile["personnalite"]:
                    profile["personnalite"][k] = v

        if "progression" in profile:
            for k, v in default_profile["progression"].items():
                if k not in profile["progression"]:
                    profile["progression"][k] = v

        return profile

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

        self.save_profile(user_id, profile)

    def get_all_profiles(self) -> dict[str, dict[str, Any]]:
        """Retourne tous les profils"""

        profiles = {}

        if os.path.exists(self.profiles_dir):
            for filename in os.listdir(self.profiles_dir):
                if filename.endswith(".json"):
                    user_id = filename.replace(".json", "")
                    profiles[user_id] = self.load_profile(user_id)

        return profiles
