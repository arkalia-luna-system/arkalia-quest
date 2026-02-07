"""
Commandes de progression fonctionnelles pour Arkalia Quest
"""

from typing import Any

from core.progression_engine import progression_engine


class ProgressionCommands:
    """Commandes qui fonctionnent vraiment avec la progression"""

    def __init__(self):
        self.commands = {
            "progression": self.handle_progression,
            "stats": self.handle_stats,
            "achievements": self.handle_achievements,
            "leaderboard": self.handle_leaderboard,
            "daily_challenges": self.handle_daily_challenges,
            "explore_zone": self.handle_explore_zone,
            "play_mini_game": self.handle_play_mini_game,
            "claim_reward": self.handle_claim_reward,
        }

    def handle_progression(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Affiche la progression du joueur"""
        player_id = profile.get("id", "default")
        player = progression_engine.get_player_progression(player_id)

        message = f"""🎯 PROGRESSION DU JOUEUR

📊 STATISTIQUES :
• Niveau : {player['level']}
• Score : {player['score']} points
• XP : {player['xp']} XP
• Coins : {player['coins']} 🪙
• Badges : {len(player['badges'])} 🏆

📈 ACTIVITÉ :
• Commandes utilisées : {player['stats']['total_commands']}
• Commandes LUNA : {player['stats']['total_luna_commands']}
• Zones explorées : {player['stats']['total_zones_explored']}
• Mini-jeux : {player['stats']['total_mini_games']}

🌍 ZONES DÉBLOQUÉES :
{chr(10).join([f"• {zone}" for zone in player['zones_explored']]) if player['zones_explored'] else "• Aucune zone explorée"}

🏆 BADGES OBTENUS :
{chr(10).join([f"• {badge}" for badge in player['badges']]) if player['badges'] else "• Aucun badge obtenu"}

💡 Utilisez 'daily_challenges' pour voir vos défis quotidiens !"""

        return {
            "réussite": True,
            "ascii_art": "🎯",
            "message": message,
            "score_gagne": 0,
            "profile_updated": False,
        }

    def handle_stats(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Affiche les statistiques détaillées"""
        player_id = profile.get("id", "default")
        player = progression_engine.get_player_progression(player_id)

        message = f"""📊 STATISTIQUES DÉTAILLÉES

🎮 ACTIVITÉ GÉNÉRALE :
• Total commandes : {player['stats']['total_commands']}
• Commandes LUNA : {player['stats']['total_luna_commands']}
• Zones explorées : {player['stats']['total_zones_explored']}
• Mini-jeux complétés : {player['stats']['total_mini_games']}

💰 RESSOURCES :
• Score total : {player['score']} points
• XP actuel : {player['xp']} XP
• Coins : {player['coins']} 🪙
• Niveau : {player['level']}

🏆 ACHIEVEMENTS :
• Badges obtenus : {len(player['badges'])}
• Achievements débloqués : {len(player['achievements_unlocked'])}

📅 DERNIÈRE ACTIVITÉ :
• {player['last_activity']}"""

        return {
            "réussite": True,
            "ascii_art": "📊",
            "message": message,
            "score_gagne": 0,
            "profile_updated": False,
        }

    def handle_achievements(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Affiche les achievements"""
        player_id = profile.get("id", "default")
        achievements = progression_engine.get_achievements(player_id)

        message = "🏆 ACHIEVEMENTS\n\n"

        for achievement in achievements:
            status = "✅" if achievement["unlocked"] else "🔒"
            message += (
                f"{status} {achievement['name']}\n   {achievement['description']}\n\n"
            )

        message += "💡 Continuez à jouer pour débloquer plus d'achievements !"

        return {
            "réussite": True,
            "ascii_art": "🏆",
            "message": message,
            "score_gagne": 0,
            "profile_updated": False,
        }

    def handle_leaderboard(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Affiche le classement"""
        leaderboard = progression_engine.get_leaderboard(10)

        message = "🏆 CLASSEMENT GLOBAL\n\n"

        for i, player in enumerate(leaderboard, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
            message += f"{emoji} #{i} {player.get('name', 'Joueur')} - {player['score']} points (Niveau {player['level']})\n"

        if not leaderboard:
            message += "Aucun joueur dans le classement pour le moment."

        return {
            "réussite": True,
            "ascii_art": "🏆",
            "message": message,
            "score_gagne": 0,
            "profile_updated": False,
        }

    def handle_daily_challenges(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Affiche les défis quotidiens"""
        player_id = profile.get("id", "default")
        challenges = progression_engine.get_daily_challenges(player_id)

        message = "🎯 DÉFIS QUOTIDIENS\n\n"

        for _challenge_id, challenge in challenges.items():
            status = "✅" if challenge["completed"] else "⏳"
            progress_bar = "█" * (
                challenge["progress"] * 10 // challenge["target"]
            ) + "░" * (10 - (challenge["progress"] * 10 // challenge["target"]))

            message += f"{status} {challenge['name']}\n"
            message += f"   {challenge['description']}\n"
            message += f"   Progression: [{progress_bar}] {challenge['progress']}/{challenge['target']}\n"
            message += f"   Récompense: {challenge['reward']['xp']} XP + {challenge['reward']['coins']} 🪙 + {challenge['reward']['badge']}\n\n"

        message += "💡 Continuez à jouer pour compléter vos défis !"

        return {
            "réussite": True,
            "ascii_art": "🎯",
            "message": message,
            "score_gagne": 0,
            "profile_updated": False,
        }

    def handle_explore_zone(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Explore une zone"""
        player_id = profile.get("id", "default")
        player = progression_engine.get_player_progression(player_id)

        # Zones disponibles selon le niveau
        available_zones = ["arkalia_base"]
        if player["level"] >= 2:
            available_zones.append("arkalia_forest")
        if player["level"] >= 3:
            available_zones.append("arkalia_city")
        if player["level"] >= 5:
            available_zones.append("arkalia_lab")

        # Trouver une zone non explorée
        unexplored_zones = [
            zone for zone in available_zones if zone not in player["zones_explored"]
        ]

        if not unexplored_zones:
            message = "🌍 EXPLORATION\n\nToutes les zones disponibles ont été explorées !\n\nMontez de niveau pour débloquer de nouvelles zones."
            return {
                "réussite": True,
                "ascii_art": "🌍",
                "message": message,
                "score_gagne": 0,
                "profile_updated": False,
            }

        # Explorer la première zone disponible
        zone = unexplored_zones[0]
        progression_engine.update_player_progression(
            player_id, "zone_explored", {"zone": zone}
        )

        zone_descriptions = {
            "arkalia_base": "Base d'Arkalia - Votre point de départ dans cette aventure cyberpunk",
            "arkalia_forest": "Forêt d'Arkalia - Une zone mystérieuse pleine de secrets",
            "arkalia_city": "Ville d'Arkalia - Le cœur urbain de cette dimension",
            "arkalia_lab": "Laboratoire d'Arkalia - Où la science rencontre la magie",
        }

        message = f"""🌍 EXPLORATION RÉUSSIE !

Vous avez exploré : {zone.upper()}
{zone_descriptions.get(zone, 'Une nouvelle zone mystérieuse')}

🎉 +50 XP pour cette exploration !
🏆 Zone ajoutée à votre collection !

Utilisez 'progression' pour voir vos zones explorées."""

        return {
            "réussite": True,
            "ascii_art": "🌍",
            "message": message,
            "score_gagne": 50,
            "profile_updated": True,
        }

    def handle_play_mini_game(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Joue à un mini-jeu"""
        player_id = profile.get("id", "default")

        # Simuler un mini-jeu simple
        mini_games = [
            "Code Breaker",
            "Memory Matrix",
            "Logic Puzzle",
            "Pattern Recognition",
        ]

        import random

        game = random.choice(mini_games)

        # Simuler la réussite (90% de chance)
        if random.random() < 0.9:
            progression_engine.update_player_progression(
                player_id,
                "mini_game_completed",
                {"game": game},
            )

            message = f"""🎮 MINI-JEU TERMINÉ !

Jeu : {game}
Résultat : VICTOIRE ! 🎉

🎉 +100 XP pour cette victoire !
🏆 Mini-jeu ajouté à votre collection !

Utilisez 'progression' pour voir vos statistiques."""

            return {
                "réussite": True,
                "ascii_art": "🎮",
                "message": message,
                "score_gagne": 100,
                "profile_updated": True,
            }
        message = f"""🎮 MINI-JEU ÉCHOUÉ !

Jeu : {game}
Résultat : ÉCHEC ! 😔

💡 Réessayez ! La pratique rend parfait !

Utilisez 'play_mini_game' pour réessayer."""

        return {
            "réussite": False,
            "ascii_art": "🎮",
            "message": message,
            "score_gagne": 0,
            "profile_updated": False,
        }

    def handle_claim_reward(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Récupère les récompenses des défis complétés"""
        player_id = profile.get("id", "default")
        player = progression_engine.get_player_progression(player_id)

        # Vérifier les défis complétés non réclamés
        challenges = progression_engine.get_daily_challenges(player_id)
        rewards_claimed = 0

        for challenge_id, challenge in challenges.items():
            if challenge["completed"] and not challenge["reward_claimed"]:
                # Marquer comme réclamé
                player["daily_challenges_progress"][challenge_id][
                    "reward_claimed"
                ] = True
                rewards_claimed += 1

        if rewards_claimed > 0:
            message = f"""🎁 RÉCOMPENSES RÉCLAMÉES !

Vous avez réclamé {rewards_claimed} récompense(s) !

🎉 Félicitations pour avoir complété vos défis !
💡 Continuez à jouer pour plus de récompenses !"""

            return {
                "réussite": True,
                "ascii_art": "🎁",
                "message": message,
                "score_gagne": 0,
                "profile_updated": True,
            }
        message = """🎁 RÉCOMPENSES

Aucune récompense à réclamer pour le moment.

💡 Complétez vos défis quotidiens pour débloquer des récompenses !
Utilisez 'daily_challenges' pour voir vos défis."""

        return {
            "réussite": True,
            "ascii_art": "🎁",
            "message": message,
            "score_gagne": 0,
            "profile_updated": False,
        }
