"""
Game Engine - Moteur principal d'Arkalia Quest
Orchestre tous les composants du jeu
"""

import json
import os
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
        """Ajoute des effets visuels et audio à la réponse"""

        # Effet de base selon le type de réponse
        if result.get("réussite", False):
            result["effect"] = {
                "type": "success",
                "color": "#00ff88",
                "animation": "pulse_green",
            }
        else:
            result["effect"] = {
                "type": "error",
                "color": "#ff4444",
                "animation": "shake",
            }

        # Effet spécial pour LUNA uniquement si le message commence par 'luna' ou concerne explicitement LUNA
        message = result.get("message", "").lower()
        if "luna" in message and (message.startswith("🌙 luna") or "luna :" in message):
            result["effect"]["type"] = "luna"
            result["effect"]["color"] = "#00ffff"
            result["effect"]["animation"] = "typing_effect"

        return result

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
