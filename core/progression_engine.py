"""
Progression Engine - Moteur de progression fonctionnel pour Arkalia Quest
"""

import json
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class ProgressionEngine:
    """Moteur de progression qui fonctionne vraiment"""

    def __init__(self):
        self.progression_file = "data/progression.json"
        self.achievements_file = "data/achievements.json"
        self.daily_challenges_file = "data/daily_challenges.json"

        # Charger les données existantes
        self.progression_data = self.load_progression_data()
        self.achievements_data = self.load_achievements_data()
        self.daily_challenges_data = self.load_daily_challenges_data()

        # Initialiser les défis quotidiens
        self.initialize_daily_challenges()

    def load_progression_data(self) -> dict[str, Any]:
        """Charge les données de progression"""
        try:
            with open(self.progression_file, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"players": {}, "global_stats": {}}
        except Exception as e:
            logger.error(f"Erreur chargement progression: {e}")
            return {"players": {}, "global_stats": {}}

    def load_achievements_data(self) -> dict[str, Any]:
        """Charge les données d'achievements"""
        try:
            with open(self.achievements_file, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"achievements": [], "unlocked": {}}
        except Exception as e:
            logger.error(f"Erreur chargement achievements: {e}")
            return {"achievements": [], "unlocked": {}}

    def load_daily_challenges_data(self) -> dict[str, Any]:
        """Charge les données de défis quotidiens"""
        try:
            with open(self.daily_challenges_file, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"challenges": {}, "last_reset": None}
        except Exception as e:
            logger.error(f"Erreur chargement défis quotidiens: {e}")
            return {"challenges": {}, "last_reset": None}

    def save_progression_data(self):
        """Sauvegarde les données de progression"""
        try:
            with open(self.progression_file, "w", encoding="utf-8") as f:
                json.dump(self.progression_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde progression: {e}")

    def save_achievements_data(self):
        """Sauvegarde les données d'achievements"""
        try:
            with open(self.achievements_file, "w", encoding="utf-8") as f:
                json.dump(self.achievements_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde achievements: {e}")

    def save_daily_challenges_data(self):
        """Sauvegarde les données de défis quotidiens"""
        try:
            with open(self.daily_challenges_file, "w", encoding="utf-8") as f:
                json.dump(self.daily_challenges_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde défis quotidiens: {e}")

    def initialize_daily_challenges(self):
        """Initialise les défis quotidiens"""
        today = datetime.now().date().isoformat()

        # Vérifier si les défis doivent être réinitialisés
        if self.daily_challenges_data.get("last_reset") != today:
            self.daily_challenges_data = {
                "challenges": self.generate_daily_challenges(),
                "last_reset": today,
            }
            self.save_daily_challenges_data()

    def generate_daily_challenges(self) -> dict[str, Any]:
        """Génère les défis quotidiens"""
        return {
            "hacker_speed": {
                "id": "hacker_speed",
                "name": "⚡ Speed Hacker",
                "description": "Complète 5 commandes en 3 minutes",
                "target": 5,
                "reward": {"xp": 100, "coins": 50, "badge": "Speed Demon"},
                "type": "command_count",
                "time_limit": 180,  # 3 minutes
                "active": True,
            },
            "luna_friend": {
                "id": "luna_friend",
                "name": "🌙 Ami de LUNA",
                "description": "Utilise 3 commandes LUNA différentes",
                "target": 3,
                "reward": {"xp": 150, "coins": 75, "badge": "LUNA Friend"},
                "type": "luna_commands",
                "active": True,
            },
            "explorer": {
                "id": "explorer",
                "name": "🔍 Explorateur",
                "description": "Explore 2 zones différentes",
                "target": 2,
                "reward": {"xp": 200, "coins": 100, "badge": "Explorer"},
                "type": "zones_explored",
                "active": True,
            },
            "code_master": {
                "id": "code_master",
                "name": "💻 Code Master",
                "description": "Résous 2 mini-jeux de programmation",
                "target": 2,
                "reward": {"xp": 250, "coins": 125, "badge": "Code Master"},
                "type": "mini_games",
                "active": True,
            },
        }

    def update_player_progression(
        self,
        player_id: str,
        action: str,
        metadata: dict[str, Any] = None,
    ) -> dict[str, Any]:
        """Met à jour la progression d'un joueur"""
        if player_id not in self.progression_data["players"]:
            self.progression_data["players"][player_id] = {
                "score": 0,
                "level": 1,
                "xp": 0,
                "coins": 0,
                "badges": [],
                "zones_explored": [],
                "commands_used": [],
                "luna_commands_used": [],
                "mini_games_completed": [],
                "daily_challenges_progress": {},
                "achievements_unlocked": [],
                "last_activity": datetime.now().isoformat(),
                "stats": {
                    "total_commands": 0,
                    "total_luna_commands": 0,
                    "total_zones_explored": 0,
                    "total_mini_games": 0,
                    "total_play_time": 0,
                },
            }

        player = self.progression_data["players"][player_id]
        player["last_activity"] = datetime.now().isoformat()

        # Mettre à jour selon l'action
        if action == "command_used":
            command = metadata.get("command", "")
            player["commands_used"].append(
                {"command": command, "timestamp": datetime.now().isoformat()},
            )
            player["stats"]["total_commands"] += 1

            # Vérifier si c'est une commande LUNA
            if "luna" in command.lower():
                player["luna_commands_used"].append(command)
                player["stats"]["total_luna_commands"] += 1

            # Mettre à jour les défis quotidiens automatiquement
            self.update_daily_challenges_progress(player_id, action, metadata)

            # Vérifier si des défis sont complétés
            self.check_daily_challenges_completion(player_id)

        elif action == "zone_explored":
            zone = metadata.get("zone", "")
            if zone not in player["zones_explored"]:
                player["zones_explored"].append(zone)
                player["stats"]["total_zones_explored"] += 1

            # Mettre à jour les défis quotidiens automatiquement
            self.update_daily_challenges_progress(player_id, action, metadata)

            # Vérifier si des défis sont complétés
            self.check_daily_challenges_completion(player_id)

        elif action == "mini_game_completed":
            game = metadata.get("game", "")
            player["mini_games_completed"].append(
                {"game": game, "timestamp": datetime.now().isoformat()},
            )
            player["stats"]["total_mini_games"] += 1

            # Mettre à jour les défis quotidiens automatiquement
            self.update_daily_challenges_progress(player_id, action, metadata)

            # Vérifier si des défis sont complétés
            self.check_daily_challenges_completion(player_id)

        elif action == "score_earned":
            points = metadata.get("points", 0)
            player["score"] += points
            player["xp"] += points

            # Vérifier le niveau
            new_level = (player["xp"] // 1000) + 1
            if new_level > player["level"]:
                player["level"] = new_level
                # Débloquer des zones selon le niveau
                self.unlock_zones_for_level(player_id, new_level)

        elif action == "coins_earned":
            coins = metadata.get("coins", 0)
            player["coins"] += coins

        elif action == "badge_earned":
            badge = metadata.get("badge", "")
            if badge not in player["badges"]:
                player["badges"].append(badge)

        elif action == "skill_upgrade":
            category = metadata.get("category", "")
            skill = metadata.get("skill", "")
            new_level = metadata.get("new_level", 1)
            xp_cost = metadata.get("xp_cost", 0)

            # Dépenser l'XP
            player["xp"] = max(0, player["xp"] - xp_cost)

            # Mettre à jour les compétences
            if "skills" not in player:
                player["skills"] = {}
            if category not in player["skills"]:
                player["skills"][category] = {}
            player["skills"][category][skill] = new_level

            # Vérifier si le niveau du joueur a changé
            new_player_level = self.calculate_level_from_xp(player["xp"])
            if new_player_level > player["level"]:
                player["level"] = new_player_level
                self.unlock_zones_for_level(player_id, new_player_level)

        # Vérifier les achievements
        self.check_achievements(player_id)

        # Sauvegarder
        self.save_progression_data()

        return {
            "success": True,
            "player": player,
            "level_up": (
                new_level > player["level"] if action == "score_earned" else False
            ),
        }

    def update_daily_challenges_progress(
        self,
        player_id: str,
        action: str,
        metadata: dict[str, Any] = None,
    ):
        """Met à jour la progression des défis quotidiens"""
        player = self.progression_data["players"][player_id]

        if "daily_challenges_progress" not in player:
            player["daily_challenges_progress"] = {}

        challenges = self.daily_challenges_data["challenges"]

        for challenge_id, challenge in challenges.items():
            if not challenge.get("active", True):
                continue

            if challenge_id not in player["daily_challenges_progress"]:
                player["daily_challenges_progress"][challenge_id] = {
                    "progress": 0,
                    "completed": False,
                    "reward_claimed": False,
                }

            progress = player["daily_challenges_progress"][challenge_id]

            # Mettre à jour selon le type de défi
            if (
                (challenge["type"] == "command_count" and action == "command_used")
                or (
                    challenge["type"] == "luna_commands"
                    and action == "command_used"
                    and "luna" in metadata.get("command", "").lower()
                )
                or (challenge["type"] == "zones_explored" and action == "zone_explored")
                or (
                    challenge["type"] == "mini_games"
                    and action == "mini_game_completed"
                )
            ):
                progress["progress"] += 1

            # Vérifier si le défi est complété
            if (
                progress["progress"] >= challenge["target"]
                and not progress["completed"]
            ):
                progress["completed"] = True
                # Donner la récompense
                reward = challenge["reward"]
                if "xp" in reward:
                    self.update_player_progression(
                        player_id,
                        "score_earned",
                        {"points": reward["xp"]},
                    )
                if "coins" in reward:
                    self.update_player_progression(
                        player_id,
                        "coins_earned",
                        {"coins": reward["coins"]},
                    )
                if "badge" in reward:
                    self.update_player_progression(
                        player_id,
                        "badge_earned",
                        {"badge": reward["badge"]},
                    )

    def check_daily_challenges_completion(self, player_id: str):
        """Vérifie et notifie les défis quotidiens complétés"""
        if player_id not in self.progression_data["players"]:
            return None

        player = self.progression_data["players"][player_id]
        challenges = self.daily_challenges_data["challenges"]
        completed_today = []

        for challenge_id, challenge in challenges.items():
            if not challenge.get("active", True):
                continue

            if challenge_id not in player["daily_challenges_progress"]:
                continue

            progress = player["daily_challenges_progress"][challenge_id]

            if progress["completed"] and not progress.get("notified", False):
                completed_today.append(
                    {
                        "id": challenge_id,
                        "title": challenge.get("title", f"Défi {challenge_id}"),
                        "reward": challenge.get("reward", {}),
                    },
                )
                progress["notified"] = True

        # Sauvegarder les changements
        if completed_today:
            self.save_progression_data()

        return completed_today

    def unlock_zones_for_level(self, player_id: str, level: int):
        """Débloque des zones selon le niveau"""
        player = self.progression_data["players"][player_id]

        zones_to_unlock = []
        if level >= 2 and "arkalia_forest" not in player["zones_explored"]:
            zones_to_unlock.append("arkalia_forest")
        if level >= 3 and "arkalia_city" not in player["zones_explored"]:
            zones_to_unlock.append("arkalia_city")
        if level >= 5 and "arkalia_lab" not in player["zones_explored"]:
            zones_to_unlock.append("arkalia_lab")

        for zone in zones_to_unlock:
            if zone not in player["zones_explored"]:
                player["zones_explored"].append(zone)

    def check_achievements(self, player_id: str):
        """Vérifie et débloque les achievements"""
        player = self.progression_data["players"][player_id]

        # Achievement: Premier pas
        if (
            player["stats"]["total_commands"] >= 1
            and "first_step" not in player["achievements_unlocked"]
        ):
            self.unlock_achievement(
                player_id,
                "first_step",
                "Premier pas",
                "Vous avez utilisé votre première commande !",
            )

        # Achievement: Speed Demon
        if (
            player["stats"]["total_commands"] >= 10
            and "speed_demon" not in player["achievements_unlocked"]
        ):
            self.unlock_achievement(
                player_id,
                "speed_demon",
                "Speed Demon",
                "10 commandes utilisées !",
            )

        # Achievement: LUNA Friend
        if (
            player["stats"]["total_luna_commands"] >= 5
            and "luna_friend" not in player["achievements_unlocked"]
        ):
            self.unlock_achievement(
                player_id,
                "luna_friend",
                "LUNA Friend",
                "5 commandes LUNA utilisées !",
            )

        # Achievement: Explorer
        if (
            player["stats"]["total_zones_explored"] >= 3
            and "explorer" not in player["achievements_unlocked"]
        ):
            self.unlock_achievement(
                player_id, "explorer", "Explorer", "3 zones explorées !"
            )

    def calculate_level_from_xp(self, xp: int) -> int:
        """Calcule le niveau du joueur basé sur son XP"""
        # Formule de progression : niveau = sqrt(xp / 100) + 1
        level = int((xp / 100) ** 0.5) + 1
        return max(1, level)  # Niveau minimum de 1

    def unlock_achievement(
        self, player_id: str, achievement_id: str, name: str, description: str
    ):
        """Débloque un achievement"""
        player = self.progression_data["players"][player_id]

        if achievement_id not in player["achievements_unlocked"]:
            player["achievements_unlocked"].append(achievement_id)

            # Ajouter le badge correspondant
            self.update_player_progression(player_id, "badge_earned", {"badge": name})

            # Donner des points
            self.update_player_progression(player_id, "score_earned", {"points": 100})

    def get_player_progression(self, player_id: str) -> dict[str, Any]:
        """Récupère la progression d'un joueur"""
        if player_id not in self.progression_data["players"]:
            return self.update_player_progression(player_id, "command_used", {})[
                "player"
            ]
        return self.progression_data["players"][player_id]

    def get_daily_challenges(self, player_id: str) -> dict[str, Any]:
        """Récupère les défis quotidiens d'un joueur"""
        player = self.get_player_progression(player_id)
        challenges = self.daily_challenges_data["challenges"]

        result = {}
        for challenge_id, challenge in challenges.items():
            if not challenge.get("active", True):
                continue

            progress = player.get("daily_challenges_progress", {}).get(
                challenge_id,
                {"progress": 0, "completed": False, "reward_claimed": False},
            )

            result[challenge_id] = {
                **challenge,
                "progress": progress["progress"],
                "completed": progress["completed"],
                "reward_claimed": progress["reward_claimed"],
            }

        return result

    def get_leaderboard(self, limit: int = 10) -> list[dict[str, Any]]:
        """Récupère le classement des joueurs"""
        players = list(self.progression_data["players"].values())
        players.sort(key=lambda x: x["score"], reverse=True)
        return players[:limit]

    def get_achievements(self, player_id: str) -> list[dict[str, Any]]:
        """Récupère les achievements d'un joueur"""
        player = self.get_player_progression(player_id)
        unlocked = player.get("achievements_unlocked", [])

        all_achievements = [
            {
                "id": "first_step",
                "name": "Premier pas",
                "description": "Utilisez votre première commande",
            },
            {
                "id": "speed_demon",
                "name": "Speed Demon",
                "description": "Utilisez 10 commandes",
            },
            {
                "id": "luna_friend",
                "name": "LUNA Friend",
                "description": "Utilisez 5 commandes LUNA",
            },
            {"id": "explorer", "name": "Explorer", "description": "Explorez 3 zones"},
        ]

        result = []
        for achievement in all_achievements:
            achievement["unlocked"] = achievement["id"] in unlocked
            result.append(achievement)

        return result


# Instance globale
progression_engine = ProgressionEngine()
