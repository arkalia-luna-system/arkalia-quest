"""
Gamification Engine - Moteur de gamification avancée pour Arkalia Quest
"""

import json
import math
import os
from datetime import datetime
from typing import Any, Dict, List


class GamificationEngine:
    """Moteur de gamification avancée"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.leaderboard_file = os.path.join(data_dir, "leaderboard.json")
        self.badges_secrets_file = os.path.join(data_dir, "badges_secrets.json")
        self.achievements_file = os.path.join(data_dir, "achievements.json")

        # Initialiser les fichiers
        self._init_files()

    def _init_files(self):
        """Initialise les fichiers de données"""

        # Leaderboard
        if not os.path.exists(self.leaderboard_file):
            self._save_leaderboard(
                {
                    "last_updated": datetime.now().isoformat(),
                    "players": [],
                    "top_players": [],
                    "statistics": {
                        "total_players": 0,
                        "total_score": 0,
                        "average_score": 0,
                    },
                }
            )

        # Badges secrets
        if not os.path.exists(self.badges_secrets_file):
            self._save_badges_secrets(
                {
                    "badges_secrets": {
                        "speed_demon": {
                            "nom": "Speed Demon",
                            "description": "Complète 5 missions en moins de 2 minutes",
                            "icone": "⚡",
                            "rarete": "legendaire",
                            "couleur": "#ffff00",
                            "animation": "flash",
                            "condition": "speed_missions",
                            "seuil": 5,
                            "temps_limite": 120,
                        },
                        "social_butterfly": {
                            "nom": "Social Butterfly",
                            "description": "Utilise toutes les commandes sociales",
                            "icone": "🦋",
                            "rarete": "epique",
                            "couleur": "#ff00ff",
                            "animation": "rainbow",
                            "condition": "social_commands",
                            "seuil": 10,
                        },
                        "night_owl": {
                            "nom": "Night Owl",
                            "description": "Joue entre 22h et 6h du matin",
                            "icone": "🦉",
                            "rarete": "rare",
                            "couleur": "#800080",
                            "animation": "glow",
                            "condition": "night_play",
                            "seuil": 3,
                        },
                        "perfectionist": {
                            "nom": "Perfectionist",
                            "description": "Complète une mission sans erreur",
                            "icone": "💎",
                            "rarete": "mythique",
                            "couleur": "#ffd700",
                            "animation": "star",
                            "condition": "perfect_mission",
                            "seuil": 1,
                        },
                        "explorer_master": {
                            "nom": "Explorer Master",
                            "description": "Découvre tous les modules (explorateur, mail, audio)",
                            "icone": "🗺️",
                            "rarete": "epique",
                            "couleur": "#00ffff",
                            "animation": "pulse",
                            "condition": "all_modules",
                            "seuil": 3,
                        },
                    }
                }
            )

        # Achievements
        if not os.path.exists(self.achievements_file):
            self._save_achievements(
                {
                    "achievements": {
                        "first_mission": {
                            "nom": "Première Mission",
                            "description": "Complète ta première mission",
                            "points": 50,
                            "icone": "🎯",
                        },
                        "score_1000": {
                            "nom": "Score 1000",
                            "description": "Atteins 1000 points",
                            "points": 100,
                            "icone": "🏆",
                        },
                        "badge_collector": {
                            "nom": "Collectionneur",
                            "description": "Obtiens 5 badges",
                            "points": 200,
                            "icone": "📜",
                        },
                        "speed_runner": {
                            "nom": "Speed Runner",
                            "description": "Complète 3 missions rapidement",
                            "points": 150,
                            "icone": "⚡",
                        },
                        "social_expert": {
                            "nom": "Expert Social",
                            "description": "Utilise toutes les commandes sociales",
                            "points": 300,
                            "icone": "🤝",
                        },
                    }
                }
            )

    def _load_leaderboard(self) -> Dict[str, Any]:
        """Charge le leaderboard"""
        with open(self.leaderboard_file, encoding="utf-8") as f:
            return json.load(f)

    def _save_leaderboard(self, data: Dict[str, Any]):
        """Sauvegarde le leaderboard"""
        with open(self.leaderboard_file, encoding="utf-8", mode="w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_badges_secrets(self) -> Dict[str, Any]:
        """Charge les badges secrets"""
        with open(self.badges_secrets_file, encoding="utf-8") as f:
            return json.load(f)

    def _save_badges_secrets(self, data: Dict[str, Any]):
        """Sauvegarde les badges secrets"""
        with open(self.badges_secrets_file, encoding="utf-8", mode="w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_achievements(self) -> Dict[str, Any]:
        """Charge les achievements"""
        with open(self.achievements_file, encoding="utf-8") as f:
            return json.load(f)

    def _save_achievements(self, data: Dict[str, Any]):
        """Sauvegarde les achievements"""
        with open(self.achievements_file, encoding="utf-8", mode="w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def update_leaderboard(self, user_id: str, profile: Dict[str, Any]):
        """Met à jour le leaderboard avec un profil"""

        leaderboard = self._load_leaderboard()

        # Trouver ou créer l'entrée du joueur
        player_entry = None
        for player in leaderboard["players"]:
            if player["user_id"] == user_id:
                player_entry = player
                break

        if not player_entry:
            player_entry = {
                "user_id": user_id,
                "name": profile.get("name", "Hacker"),
                "score": 0,
                "level": 1,
                "badges_count": 0,
                "missions_completed": 0,
                "last_activity": datetime.now().isoformat(),
                "join_date": datetime.now().isoformat(),
            }
            leaderboard["players"].append(player_entry)

        # Mettre à jour les données
        player_entry.update(
            {
                "name": profile.get("name", "Hacker"),
                "score": profile.get("score", 0),
                "level": profile.get("level", 1),
                "badges_count": len(profile.get("badges", [])),
                "missions_completed": len(
                    profile.get("personnalite", {}).get("missions_completees", [])
                ),
                "last_activity": datetime.now().isoformat(),
            }
        )

        # Trier par score décroissant
        leaderboard["players"].sort(key=lambda x: x["score"], reverse=True)

        # Mettre à jour les top players (top 10)
        leaderboard["top_players"] = leaderboard["players"][:10]

        # Mettre à jour les statistiques
        total_players = len(leaderboard["players"])
        total_score = sum(p["score"] for p in leaderboard["players"])
        average_score = total_score / total_players if total_players > 0 else 0

        leaderboard["statistics"] = {
            "total_players": total_players,
            "total_score": total_score,
            "average_score": round(average_score, 2),
        }

        leaderboard["last_updated"] = datetime.now().isoformat()

        self._save_leaderboard(leaderboard)

        return player_entry

    def get_leaderboard(self, limit: int = 10) -> Dict[str, Any]:
        """Récupère le leaderboard"""
        leaderboard = self._load_leaderboard()
        return {
            "top_players": leaderboard["top_players"][:limit],
            "statistics": leaderboard["statistics"],
            "last_updated": leaderboard["last_updated"],
        }

    def check_badges_secrets(
        self, profile: Dict[str, Any], action: str, **kwargs
    ) -> List[str]:
        """Vérifie et débloque les badges secrets"""

        badges_secrets = self._load_badges_secrets()
        unlocked_badges = []

        for badge_id, badge_data in badges_secrets["badges_secrets"].items():
            if badge_id not in profile.get(
                "badges", []
            ) and self._check_badge_condition(badge_data, profile, action, **kwargs):
                unlocked_badges.append(badge_id)

        return unlocked_badges

    def _check_badge_condition(
        self, badge_data: Dict[str, Any], profile: Dict[str, Any], action: str, **kwargs
    ) -> bool:
        """Vérifie si une condition de badge est remplie"""

        condition = badge_data.get("condition")
        seuil = badge_data.get("seuil", 1)

        if condition == "speed_missions":
            # Missions rapides
            missions_completees = profile.get("personnalite", {}).get(
                "missions_completees", []
            )
            if len(missions_completees) >= seuil:
                return True

        elif condition == "social_commands":
            # Commandes sociales utilisées
            social_commands = ["aide", "profil", "monde", "status"]
            commands_used = profile.get("commands_used", [])
            social_used = [cmd for cmd in commands_used if cmd in social_commands]
            return len(social_used) >= seuil

        elif condition == "night_play":
            # Jeu de nuit
            current_hour = datetime.now().hour
            if current_hour >= 22 or current_hour <= 6:
                return True

        elif condition == "perfect_mission":
            # Mission parfaite
            if action == "mission_complete" and kwargs.get("perfect", False):
                return True

        elif condition == "all_modules":
            # Tous les modules visités
            modules_visited = profile.get("modules_visited", [])
            required_modules = ["explorateur", "mail", "audio"]
            return all(module in modules_visited for module in required_modules)

        return False

    def check_achievements(
        self, profile: Dict[str, Any]
    ) -> List[str]:
        """Vérifie et débloque les achievements"""

        achievements = self._load_achievements()
        unlocked_achievements = []

        for achievement_id, _achievement_data in achievements["achievements"].items():
            if achievement_id not in profile.get(
                "achievements", []
            ) and self._check_achievement_condition(achievement_id, profile):
                unlocked_achievements.append(achievement_id)

        return unlocked_achievements

    def _check_achievement_condition(
        self, achievement_id: str, profile: Dict[str, Any]
    ) -> bool:
        """Vérifie si une condition d'achievement est remplie"""

        if achievement_id == "first_mission":
            missions = profile.get("personnalite", {}).get("missions_completees", [])
            return len(missions) >= 1

        elif achievement_id == "score_1000":
            return profile.get("score", 0) >= 1000

        elif achievement_id == "badge_collector":
            return len(profile.get("badges", [])) >= 5

        elif achievement_id == "speed_runner":
            missions = profile.get("personnalite", {}).get("missions_completees", [])
            return len(missions) >= 3

        elif achievement_id == "social_expert":
            social_commands = ["aide", "profil", "monde", "status"]
            commands_used = profile.get("commands_used", [])
            return all(cmd in commands_used for cmd in social_commands)

        return False

    def calculate_xp_gain(self, action: str, **kwargs) -> int:
        """Calcule le gain d'XP pour une action"""

        xp_table = {
            "mission_complete": 100,
            "badge_unlocked": 50,
            "achievement_unlocked": 200,
            "command_used": 5,
            "portal_decoded": 75,
            "coffre_hacked": 150,
            "social_interaction": 25,
        }

        base_xp = xp_table.get(action, 10)

        # Bonus pour actions spéciales
        if kwargs.get("perfect", False):
            base_xp *= 2  # Bonus parfait
        if kwargs.get("speed", False):
            base_xp *= 1.5  # Bonus vitesse
        if kwargs.get("first_time", False):
            base_xp *= 1.2  # Bonus première fois

        return int(base_xp)

    def calculate_level(self, xp: int) -> int:
        """Calcule le niveau basé sur l'XP"""
        return int(math.sqrt(xp / 100)) + 1

    def get_level_progress(self, xp: int) -> Dict[str, Any]:
        """Calcule la progression du niveau"""

        current_level = self.calculate_level(xp)
        xp_for_current = (current_level - 1) ** 2 * 100
        xp_for_next = current_level**2 * 100
        xp_in_level = int(xp - xp_for_current)
        xp_needed = int(xp_for_next - xp_for_current)

        progress_percentage = (xp_in_level / xp_needed) * 100 if xp_needed > 0 else 100

        return {
            "current_level": current_level,
            "xp_current": xp,
            "xp_in_level": xp_in_level,
            "xp_needed": xp_needed,
            "progress_percentage": round(progress_percentage, 1),
        }

    def get_gamification_summary(
        self, user_id: str, profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Récupère un résumé complet de la gamification"""

        leaderboard = self.get_leaderboard()
        player_rank = None

        # Trouver le rang du joueur
        for i, player in enumerate(leaderboard["top_players"]):
            if player["user_id"] == user_id:
                player_rank = i + 1
                break

        level_progress = self.get_level_progress(profile.get("score", 0))

        return {
            "player_rank": player_rank,
            "total_players": leaderboard["statistics"]["total_players"],
            "level_progress": level_progress,
            "badges_count": len(profile.get("badges", [])),
            "missions_completed": len(
                profile.get("personnalite", {}).get("missions_completees", [])
            ),
            "achievements_count": len(profile.get("achievements", [])),
            "total_score": profile.get("score", 0),
            "leaderboard_stats": leaderboard["statistics"],
        }
