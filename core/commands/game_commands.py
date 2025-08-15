"""
Commandes de jeux éducatifs pour Arkalia Quest
Active les mini-jeux interactifs avec interface graphique
"""

from typing import Any, Dict

from core.educational_games_engine import EducationalGamesEngine


class GameCommands:
    """Gestionnaire des commandes de jeux éducatifs"""

    def __init__(self):
        self.games_engine = EducationalGamesEngine()

        # Dictionnaire des commandes disponibles
        self.commands = {
            "games": self.handle_games,
            "play_game": self.handle_play_game,
            "game_stats": self.handle_game_stats,
        }

    def handle_games(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Liste tous les mini-jeux disponibles"""
        user_level = profile.get("level", 1)
        available_games = self.games_engine.get_available_games(user_level)

        if not available_games:
            return {
                "réussite": False,
                "message": "❌ Aucun jeu disponible pour ton niveau actuel.",
            }

        # Organiser par type
        games_by_type = {}
        for game in available_games:
            game_type = game["type"]
            if game_type not in games_by_type:
                games_by_type[game_type] = []
            games_by_type[game_type].append(game)

        message = "🎮 MINI-JEUX ÉDUCATIFS DISPONIBLES\n\n"

        for game_type, games in games_by_type.items():
            type_emoji = self._get_type_emoji(game_type)
            type_name = self._get_type_name(game_type)
            message += f"{type_emoji} {type_name.upper()}\n"

            for game in games:
                difficulty_emoji = self._get_difficulty_emoji(game["difficulty"])
                message += f"  • {game['id']}: {game['title']} {difficulty_emoji} (+{game['points']}pts)\n"
            message += "\n"

        message += "💡 Utilise 'play_game <id>' pour jouer !\n"
        message += "🎯 Exemple: play_game logic_1"

        return {"réussite": True, "ascii_art": "🎮", "message": message}

    def handle_play_game(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Démarre un mini-jeu éducatif"""
        return {
            "réussite": True,
            "ascii_art": "🎮",
            "message": """🎮 MINI-JEUX INTERACTIFS

💡 Pour jouer à un mini-jeu :
• Tape 'games' pour voir la liste des jeux
• Puis clique sur un jeu dans l'interface

🎯 EXEMPLES DE JEUX DISPONIBLES :
• 🔍 Décrypte le Mot de Passe (Logique)
• 💻 Débogue le Code (Programmation)
• 🛡️ Détecte l'Attaque (Cybersécurité)
• 🔐 Décode le Message (Cryptographie)
• 🌐 Analyse le Réseau (Réseau)

🌙 LUNA : "Les mini-jeux s'ouvrent dans une fenêtre interactive !"
💻 Interface graphique avec animations et effets sonores !
🎮 Continue l'aventure pour débloquer tous les secrets !""",
            "profile_updated": False,
        }

    def handle_game_stats(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Affiche les statistiques des jeux"""
        # Simuler des stats pour l'instant
        message = "📊 STATISTIQUES DES MINI-JEUX\n\n"
        message += "🎮 Total de jeux: 9\n"
        message += "👥 Joueurs actifs: 1\n"
        message += "🎯 Sessions jouées: 0\n\n"
        message += "📈 RÉPARTITION PAR TYPE:\n"
        message += "  🔍 Logique: 2 jeux\n"
        message += "  💻 Code: 2 jeux\n"
        message += "  🛡️ Cybersécurité: 2 jeux\n"
        message += "  🔐 Cryptographie: 2 jeux\n"
        message += "  🌐 Réseau: 1 jeu\n\n"
        message += "💡 Commence par 'games' pour voir les jeux !"

        return {"réussite": True, "ascii_art": "📊", "message": message}

    def _get_type_emoji(self, game_type: str) -> str:
        """Retourne l'emoji pour un type de jeu"""
        emojis = {
            "logic": "🔍",
            "code": "💻",
            "cybersecurity": "🛡️",
            "cryptography": "🔐",
            "network": "🌐",
        }
        return emojis.get(game_type, "🎮")

    def _get_type_name(self, game_type: str) -> str:
        """Retourne le nom français d'un type de jeu"""
        names = {
            "logic": "Logique",
            "code": "Programmation",
            "cybersecurity": "Cybersécurité",
            "cryptography": "Cryptographie",
            "network": "Réseau",
        }
        return names.get(game_type, "Inconnu")

    def _get_difficulty_emoji(self, difficulty: str) -> str:
        """Retourne l'emoji pour une difficulté"""
        emojis = {
            "beginner": "🟢",
            "intermediate": "🟡",
            "advanced": "🟠",
            "expert": "🔴",
        }
        return emojis.get(difficulty, "⚪")
