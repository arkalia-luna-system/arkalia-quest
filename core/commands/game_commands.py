"""
Commandes de jeux éducatifs pour Arkalia Quest
Active les mini-jeux interactifs avec interface graphique
"""

from typing import Any

from core.educational_games_engine import EducationalGamesEngine


class GameCommands:
    """Gestionnaire des commandes de jeux éducatifs"""

    def __init__(self):
        self.games_engine = EducationalGamesEngine()

        # Dictionnaire des commandes disponibles
        self.commands = {
            "games": self.handle_games,
            "play_game": self.handle_play_game,
            "play": self.handle_play,
            "game_stats": self.handle_game_stats,
            "daily_challenges": self.handle_daily_challenges,
            "random_events": self.handle_random_events,
        }

    def handle_games(self, profile: dict[str, Any]) -> dict[str, Any]:
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
                message += (
                    f"• {game['id']}: {game['title']} {difficulty_emoji}"
                     "(+{game['points']}pts)\n"
                )
            message += "\n"

        message += "💡 Utilise 'play_game <id>' pour jouer !\n"
        message += "🎯 Exemple: play_game logic_1"

        return {"réussite": True, "ascii_art": "🎮", "message": message}

    def handle_play_game(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Démarre un mini-jeu éducatif (ou explique comment)"""
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

    def handle_play(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Lance un mini-jeu spécifique (simulation)"""
        return {
            "réussite": True,
            "ascii_art": "🎮",
            "message": """🎮 LANCEMENT DU MINI-JEU

🌙 LUNA : "Prépare-toi, hacker ! Un défi t'attend !"

💻 Le mini-jeu s'ouvre dans une nouvelle fenêtre interactive...
🎯 Résous le défi pour gagner des points et des badges !

🚀 Bonne chance dans cette aventure éducative !""",
            "profile_updated": False,
        }

    def handle_game_stats(self, profile: dict[str, Any]) -> dict[str, Any]:
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

    def handle_daily_challenges(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Affiche les défis quotidiens engageants pour les ados"""
        # Simuler des défis quotidiens
        challenges = {
            "speed_hacker": {
                "title": "⚡ Speed Hacker",
                "description": "Complète 3 missions en moins de 5 minutes",
                "progress": 1,
                "target": 3,
                "reward": "100 XP + Badge Speed Demon + 50 Coins",
            },
            "code_master": {
                "title": "💻 Code Master",
                "description": "Résous 2 mini-jeux de programmation",
                "progress": 0,
                "target": 2,
                "reward": "150 XP + Badge Code Master + 75 Coins",
            },
            "social_butterfly": {
                "title": "🦋 Social Butterfly",
                "description": "Utilise 5 commandes sociales différentes",
                "progress": 2,
                "target": 5,
                "reward": "80 XP + Badge Social Expert + 40 Coins",
            },
            "night_owl": {
                "title": "🦉 Night Owl",
                "description": "Joue entre 22h et 6h du matin",
                "progress": 0,
                "target": 1,
                "reward": "120 XP + Badge Night Hacker + 60 Coins",
            },
        }

        message = "🎯 DÉFIS QUOTIDIENS - RÉINITIALISÉS CHAQUE JOUR !\n\n"

        for _challenge_id, challenge in challenges.items():
            progress_bar = "█" * challenge["progress"] + "░" * (
                challenge["target"] - challenge["progress"]
            )
            status = (
                "✅ COMPLÉTÉ !"
                if challenge["progress"] >= challenge["target"]
                else f"📊 {challenge['progress']}/{challenge['target']}"
            )

            message += f"🎯 {challenge['title']}\n"
            message += f"   📝 {challenge['description']}\n"
            message += f"   {progress_bar} {status}\n"
            message += f"   🏆 Récompense : {challenge['reward']}\n\n"

        message += "💡 Les défis se réinitialisent chaque jour à minuit !\n"
        message += "🌟 Complète-les tous pour des bonus exclusifs !"

        return {"réussite": True, "ascii_art": "🎯", "message": message}

    def handle_random_events(self) -> dict[str, Any]:
        """Affiche les événements aléatoires et leurs déclencheurs"""
        events = {
            "luna_surprise": {
                "title": "🎁 Surprise LUNA !",
                "description": "LUNA t'offre un bonus XP aléatoire !",
                "trigger": "Actions aléatoires",
                "chance": "10%",
                "effect": "Bonus XP 50-200 + Message spécial",
            },
            "secret_badge": {
                "title": "🔍 Badge Secret Découvert !",
                "description": "Tu as trouvé un badge caché !",
                "trigger": "Exploration du monde",
                "chance": "5%",
                "effect": "Badge 'Secret Explorer' + 100 XP",
            },
            "matrix_glitch": {
                "title": "🌐 Glitch Matrix !",
                "description": "Le système bug, profites-en !",
                "trigger": "Actions système",
                "chance": "8%",
                "effect": "25 Coins bonus + Message glitch",
            },
        }

        message = "🎲 ÉVÉNEMENTS ALÉATOIRES - SURPRISES MATRIX !\n\n"

        for _event_id, event in events.items():
            message += f"🎲 {event['title']}\n"
            message += f"   📝 {event['description']}\n"
            message += f"   🎯 Déclencheur : {event['trigger']}\n"
            message += f"   🎲 Chance : {event['chance']}\n"
            message += f"   ⚡ Effet : {event['effect']}\n\n"

        message += "💡 Ces événements se déclenchent aléatoirement !\n"
        message += "🌟 Plus tu joues, plus tu as de chances !"

        return {"réussite": True, "ascii_art": "🎲", "message": message}

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
