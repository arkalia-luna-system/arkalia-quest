"""
Game Engine - Moteur principal d'Arkalia Quest
Orchestre tous les composants du jeu
"""

import json
import os
import random
from datetime import datetime
from typing import Any, Dict

from core.database import DatabaseManager

from .command_handler_v2 import CommandHandlerV2 as CommandHandler
from .profile_manager import ProfileManager


class GameEngine:
    """Moteur principal du jeu Arkalia Quest"""

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.profile_manager = ProfileManager()
        self.command_handler = CommandHandler()
        self.current_missions = {}
        self.game_state = {
            "luna_relationship": 0,
            "universe_unlocked": False,
            "personality_detected": False,
        }

    def process_command(self, command: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Traite une commande utilisateur et retourne la réponse

        Args:
            command: Commande saisie par l'utilisateur
            user_id: Identifiant unique de l'utilisateur

        Returns:
            Dict contenant la réponse et les effets
        """
        # Charger le profil utilisateur
        profile = self.db_manager.load_profile(user_id)
        if not profile:
            profile = self.profile_manager.create_default_profile()

        # Traiter la commande
        result = self.command_handler.handle_command(command, profile)

        # Mettre à jour le profil si nécessaire
        if result.get("profile_updated", False):
            self.db_manager.save_profile(user_id, profile)

        # Ajouter des effets visuels/audio
        result = self.add_effects(result, profile)

        return result

    def add_effects(
        self, result: Dict[str, Any], profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ajoute des effets visuels et audio à la réponse - OPTIMISÉ ADOLESCENT"""

        # Effet de base selon le type de réponse - THÈME MATRIX
        if result.get("réussite", False):
            result["effect"] = {
                "type": "success",
                "color": "#00ff00",  # Vert Matrix
                "animation": "matrix_pulse",
                "sound": "success_matrix",
                "particles": True,
                "reward": self._calculate_reward(profile, result),
            }
        else:
            result["effect"] = {
                "type": "error",
                "color": "#ff4444",
                "animation": "matrix_shake",
                "sound": "error_matrix",
                "particles": False,
                "encouragement": self._get_encouragement(profile),
            }

        # Effet spécial pour LUNA - THÈME MATRIX
        message = result.get("message", "").lower()
        if "luna" in message and (message.startswith("🌙 luna") or "luna :" in message):
            result["effect"]["type"] = "luna_matrix"
            result["effect"]["color"] = "#00ffff"  # Cyan Matrix
            result["effect"]["animation"] = "matrix_typing"
            result["effect"]["sound"] = "luna_matrix"

        # Ajouter des récompenses instantanées pour l'engagement
        if result.get("réussite", False):
            result["instant_rewards"] = self._generate_instant_rewards(profile, result)

        return result

    def _calculate_reward(
        self, profile: Dict[str, Any], result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calcule les récompenses pour l'engagement adolescent"""
        base_xp = 10
        bonus_multiplier = 1.0

        # Bonus pour actions rapides
        if hasattr(self, "last_action_time"):
            time_diff = (datetime.now() - self.last_action_time).total_seconds()
            if time_diff < 5:  # Action rapide
                bonus_multiplier += 0.5

        # Bonus pour difficulté
        if result.get("difficulty", "easy") == "hard":
            bonus_multiplier += 0.3

        xp_gained = int(base_xp * bonus_multiplier)

        return {
            "xp": xp_gained,
            "coins": int(xp_gained / 2),
            "streak_bonus": self._check_streak_bonus(profile),
            "level_progress": self._calculate_level_progress(profile, xp_gained),
        }

    def _get_encouragement(self, profile: Dict[str, Any]) -> str:
        """Génère des encouragements personnalisés pour les ados"""
        encouragements = [
            "💪 Ne lâche pas ! Chaque échec te rapproche du succès !",
            "🌟 Tu y es presque ! Essaie une approche différente !",
            "🚀 C'est normal de se tromper, c'est comme ça qu'on apprend !",
            "🎯 Garde la tête haute, tu vas y arriver !",
            "⚡ Un petit pas en arrière, deux pas en avant !",
        ]
        return random.choice(encouragements)

    def _generate_instant_rewards(
        self, profile: Dict[str, Any], result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Génère des récompenses instantanées visuelles"""
        rewards = {"badge": None, "achievement": None, "special_effect": None}

        # Vérifier les badges
        if profile.get("total_actions", 0) == 10:
            rewards["badge"] = "🎖️ Débutant Hacker"
        elif profile.get("total_actions", 0) == 50:
            rewards["badge"] = "🏆 Hacker Confirmé"
        elif profile.get("total_actions", 0) == 100:
            rewards["badge"] = "👑 Maître Hacker"

        # Vérifier les achievements
        if profile.get("missions_completed", 0) == 5:
            rewards["achievement"] = "🎯 Missionnaire"
        elif profile.get("missions_completed", 0) == 10:
            rewards["achievement"] = "🚀 Explorateur"

        # Effets spéciaux
        if rewards["badge"] or rewards["achievement"]:
            rewards["special_effect"] = "matrix_celebration"

        return rewards

    def _check_streak_bonus(self, profile: Dict[str, Any]) -> int:
        """Vérifie les bonus de série"""
        current_streak = profile.get("current_streak", 0)
        if current_streak >= 7:
            return 50  # Bonus hebdomadaire
        elif current_streak >= 3:
            return 20  # Bonus de série
        return 0

    def _calculate_level_progress(
        self, profile: Dict[str, Any], xp_gained: int
    ) -> Dict[str, Any]:
        """Calcule la progression de niveau"""
        current_xp = profile.get("xp", 0) + xp_gained
        current_level = profile.get("level", 1)
        xp_needed = current_level * 100

        if current_xp >= xp_needed:
            new_level = current_level + 1
            return {
                "level_up": True,
                "new_level": new_level,
                "old_level": current_level,
                "bonus_xp": current_xp - xp_needed,
            }

        return {
            "level_up": False,
            "progress": (current_xp / xp_needed) * 100,
            "xp_remaining": xp_needed - current_xp,
        }

    def start_mission(
        self, mission_id: str, user_id: str = "default"
    ) -> Dict[str, Any]:
        """Démarre une mission pour un utilisateur"""

        profile = self.profile_manager.load_profile(user_id)

        # Vérifier les prérequis
        if not self.can_start_mission(mission_id, profile):
            return {
                "réussite": False,
                "message": "❌ Prérequis non satisfaits pour cette mission.",
            }

        # Créer le contexte de mission
        mission_context = {
            "mission_id": mission_id,
            "start_time": datetime.now().isoformat(),
            "choices_made": [],
            "current_step": 0,
        }

        self.current_missions[user_id] = mission_context

        return {
            "réussite": True,
            "message": f"🎯 Mission '{mission_id}' démarrée !",
            "mission_context": mission_context,
        }

    def can_start_mission(self, mission_id: str, profile: Dict[str, Any]) -> bool:
        """Vérifie si l'utilisateur peut démarrer une mission"""

        # Charger la mission
        mission_file = f"data/missions/{mission_id}.json"
        if not os.path.exists(mission_file):
            return False

        with open(mission_file, encoding="utf-8") as f:
            mission = json.load(f)

        # Vérifier les prérequis
        prerequis = mission.get("prerequis", [])

        for prerequis_item in prerequis:
            if prerequis_item == "unlock_universe":
                if not self.game_state["universe_unlocked"]:
                    return False
            elif prerequis_item == "complete_tutorial":
                if not self.game_state["tutorial_completed"]:
                    return False

        return True

    def get_available_missions(self, user_id: str = "default") -> list:
        """Retourne les missions disponibles pour l'utilisateur"""

        profile = self.profile_manager.load_profile(user_id)
        available_missions = []

        # Parcourir tous les fichiers de mission
        missions_dir = "data/missions"
        if os.path.exists(missions_dir):
            for filename in os.listdir(missions_dir):
                if filename.endswith(".json"):
                    mission_id = filename.replace(".json", "")
                    if self.can_start_mission(mission_id, profile):
                        available_missions.append(mission_id)

        return available_missions

    def get_game_state(self) -> Dict[str, Any]:
        """Retourne l'état actuel du jeu"""
        return self.game_state.copy()

    def update_game_state(self, updates: Dict[str, Any]):
        """Met à jour l'état du jeu"""
        self.game_state.update(updates)
