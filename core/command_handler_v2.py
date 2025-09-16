"""
Command Handler Arkalia Quest v2 - Version modulaire
Utilise les modules séparés pour une meilleure organisation
"""

from datetime import datetime
from typing import Any

from .commands.analytics_commands import AnalyticsCommands

# Import des modules de commandes
from .commands.basic_commands import BasicCommands
from .commands.easter_egg_commands import EasterEggCommands
from .commands.game_commands import GameCommands
from .commands.luna_commands import LunaCommands
from .commands.story_commands import StoryCommands
from .commands.system_commands import SystemCommands
from .luna_emotions_engine import luna_emotions


class CommandHandlerV2:
    """Gestionnaire de commandes v2 avec émotions LUNA"""

    def __init__(self):
        # Initialisation des modules de commandes
        self.basic_commands = BasicCommands()
        self.game_commands = GameCommands()
        self.luna_commands = LunaCommands()
        self.system_commands = SystemCommands()
        self.easter_egg_commands = EasterEggCommands()
        self.analytics_commands = AnalyticsCommands()
        self.story_commands = StoryCommands()

        # Fusion de toutes les commandes
        self.all_commands = {}
        self.all_commands.update(self.basic_commands.commands)
        self.all_commands.update(self.game_commands.commands)
        self.all_commands.update(self.luna_commands.commands)
        self.all_commands.update(self.system_commands.commands)
        self.all_commands.update(self.easter_egg_commands.commands)
        self.all_commands.update(self.analytics_commands.commands)
        self.all_commands.update(self.story_commands.commands)

        # Whitelist des commandes autorisées
        self.command_whitelist = set(self.all_commands.keys())

        # Initialiser le moteur d'émotions LUNA
        self.luna_emotions = luna_emotions

    def normalize_command(self, command: str) -> str:
        """Normalise une commande"""
        return command.lower().strip()

    def handle_command(self, command: str, profile: dict[str, Any]) -> dict[str, Any]:
        """
        Traite une commande avec émotions LUNA

        Args:
            command: Commande à traiter
            profile: Profil du joueur

        Returns:
            Dict avec réponse et émotions LUNA
        """
        # Normaliser la commande
        normalized_command = self.normalize_command(command)

        # Vérifier si la commande est autorisée
        if normalized_command not in self.command_whitelist:
            return self._handle_unknown_command(command, profile)

        # Traiter la commande
        result = self._process_command(normalized_command, profile)

        # Analyser l'émotion de LUNA
        luna_emotion_data = self.luna_emotions.analyze_action(
            normalized_command, result, profile
        )

        # Ajouter les données d'émotion à la réponse
        result.update(
            {
                "luna_emotion": luna_emotion_data["emotion"],
                "luna_message": luna_emotion_data["message"],
                "luna_color": luna_emotion_data["color"],
                "luna_effect": luna_emotion_data["effect"],
                "luna_sound": luna_emotion_data["sound"],
                "luna_intensity": luna_emotion_data["intensity"],
                "relationship_change": luna_emotion_data["relationship_change"],
            }
        )

        return result

    def _handle_unknown_command(
        self, command: str, profile: dict[str, Any]
    ) -> dict[str, Any]:
        """Gère une commande inconnue avec émotion LUNA et suggestions intelligentes"""

        # Suggestions intelligentes pour commandes inconnues
        suggestions = self._get_command_suggestions(command)
        suggestion_text = ""
        if suggestions:
            suggestion_text = f"\n\n💡 Suggestions :\n{chr(10).join([f'• {s}' for s in suggestions[:3]])}"

        result = {
            "réussite": False,
            "ascii_art": "❓",
            "message": f"❓ Commande '{command}' non reconnue.{suggestion_text}\n\n🔍 Tape 'aide' pour voir toutes les commandes disponibles !",
            "score_gagne": 0,
            "profile_updated": False,
        }

        # LUNA réagit selon le type de commande
        emotion_type = "unknown_command"
        luna_emotion_data = self.luna_emotions.analyze_action(
            emotion_type, result, profile
        )

        result.update(
            {
                "luna_emotion": luna_emotion_data["emotion"],
                "luna_message": luna_emotion_data["message"],
                "luna_color": luna_emotion_data["color"],
                "luna_effect": luna_emotion_data["effect"],
                "luna_sound": luna_emotion_data["sound"],
                "luna_intensity": luna_emotion_data["intensity"],
                "relationship_change": luna_emotion_data["relationship_change"],
            }
        )

        return result

    def _get_command_suggestions(self, command: str) -> list[str]:
        """Génère des suggestions intelligentes pour une commande inconnue"""
        all_commands = list(self.all_commands.keys())
        suggestions = []

        # Recherche par similarité
        for cmd in all_commands:
            if self._calculate_similarity(command, cmd) > 0.6:
                suggestions.append(cmd)

        # Recherche par préfixe
        for cmd in all_commands:
            if cmd.startswith(command[:3]) and len(command) >= 3:
                suggestions.append(cmd)

        # Supprimer les doublons et limiter
        return list(set(suggestions))[:5]

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calcule la similarité entre deux chaînes"""
        if not str1 or not str2:
            return 0.0

        # Similarité simple basée sur les caractères communs
        common_chars = sum(1 for c in str1 if c in str2)
        max_len = max(len(str1), len(str2))
        return common_chars / max_len if max_len > 0 else 0.0

    def _process_command(self, command: str, profile: dict[str, Any]) -> dict[str, Any]:
        """
        Traite une commande spécifique

        Args:
            command: Commande normalisée
            profile: Profil du joueur

        Returns:
            Dict avec le résultat de la commande
        """
        try:
            # Récupérer la fonction de gestion de la commande
            command_handler = self.all_commands.get(command)

            if command_handler:
                # Exécuter la commande
                result = command_handler(profile)

                # Formater la réponse
                result = self.format_response(result)

                return result
            else:
                # Commande non trouvée
                return {
                    "réussite": False,
                    "ascii_art": "❌",
                    "message": f"❌ Erreur interne : Commande '{command}' non implémentée.",
                    "score_gagne": 0,
                    "profile_updated": False,
                }

        except Exception as e:
            # Gestion d'erreur
            return {
                "réussite": False,
                "ascii_art": "💥",
                "message": f"💥 Erreur lors de l'exécution de '{command}': {e!s}",
                "score_gagne": 0,
                "profile_updated": False,
            }

    def format_response(self, result: dict[str, Any]) -> dict[str, Any]:
        """Formate la réponse"""
        # Ajout de timestamp si pas présent
        if "timestamp" not in result:
            result["timestamp"] = datetime.now().isoformat()

        return result

    def get_available_commands(self) -> list:
        """Retourne la liste des commandes disponibles"""
        return list(self.command_whitelist)

    def get_command_count(self) -> int:
        """Retourne le nombre total de commandes"""
        return len(self.command_whitelist)
