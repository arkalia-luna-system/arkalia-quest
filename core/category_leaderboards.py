#!/usr/bin/env python3
"""
🏆 CATEGORY LEADERBOARDS - ARKALIA QUEST
========================================

Système de classements par catégories (vitesse, créativité, etc.)
pour motiver les joueurs selon leurs compétences spécifiques.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CategoryLeaderboards:
    """Gestionnaire des classements par catégories"""

    def __init__(self):
        self.categories = {}
        self.leaderboards = {}
        self.player_stats = {}
        self.ranking_periods = {}

        # Charger les données
        self.load_leaderboard_data()

    def load_leaderboard_data(self) -> None:
        """Charge les données de classements"""
        try:
            with open("data/category_leaderboards.json", encoding="utf-8") as f:
                data = json.load(f)
                self.categories = data.get("categories", {})
                self.leaderboards = data.get("leaderboards", {})
                self.player_stats = data.get("player_stats", {})
                self.ranking_periods = data.get("ranking_periods", {})
        except FileNotFoundError:
            logger.info(
                "Fichier de classements non trouvé, création des données par défaut"
            )
            self._create_default_categories()
        except Exception as e:
            logger.error(f"Erreur chargement classements: {e}")
            self._create_default_categories()

    def _create_default_categories(self) -> None:
        """Crée les catégories de classement par défaut"""
        self.categories = {
            "speed": {
                "name": "Vitesse",
                "description": "Rapidité d'exécution et efficacité",
                "icon": "⚡",
                "color": "#ff4444",
                "metrics": ["mission_time", "hack_speed", "response_time"],
                "weight": {
                    "mission_time": 0.4,
                    "hack_speed": 0.4,
                    "response_time": 0.2,
                },
            },
            "creativity": {
                "name": "Créativité",
                "description": "Solutions innovantes et approches créatives",
                "icon": "🎨",
                "color": "#aa44ff",
                "metrics": [
                    "creative_solutions",
                    "unexpected_approaches",
                    "artistic_score",
                ],
                "weight": {
                    "creative_solutions": 0.5,
                    "unexpected_approaches": 0.3,
                    "artistic_score": 0.2,
                },
            },
            "hacking": {
                "name": "Hacking",
                "description": "Compétences techniques et de sécurité",
                "icon": "💻",
                "color": "#00ff00",
                "metrics": [
                    "hack_success_rate",
                    "security_knowledge",
                    "technical_skills",
                ],
                "weight": {
                    "hack_success_rate": 0.4,
                    "security_knowledge": 0.3,
                    "technical_skills": 0.3,
                },
            },
            "social": {
                "name": "Social",
                "description": "Interactions et leadership communautaire",
                "icon": "👥",
                "color": "#ff00ff",
                "metrics": ["interactions_count", "guild_leadership", "help_provided"],
                "weight": {
                    "interactions_count": 0.3,
                    "guild_leadership": 0.4,
                    "help_provided": 0.3,
                },
            },
            "education": {
                "name": "Éducation",
                "description": "Apprentissage et développement des compétences",
                "icon": "📚",
                "color": "#ffff00",
                "metrics": ["games_completed", "knowledge_gained", "skill_progression"],
                "weight": {
                    "games_completed": 0.3,
                    "knowledge_gained": 0.4,
                    "skill_progression": 0.3,
                },
            },
            "exploration": {
                "name": "Exploration",
                "description": "Découverte et curiosité",
                "icon": "🌍",
                "color": "#00ffff",
                "metrics": ["zones_discovered", "secrets_found", "exploration_time"],
                "weight": {
                    "zones_discovered": 0.4,
                    "secrets_found": 0.4,
                    "exploration_time": 0.2,
                },
            },
            "luna_relationship": {
                "name": "Relation LUNA",
                "description": "Développement de la relation avec l'IA",
                "icon": "🌙",
                "color": "#ffaa00",
                "metrics": ["luna_interactions", "trust_level", "emotional_connection"],
                "weight": {
                    "luna_interactions": 0.3,
                    "trust_level": 0.4,
                    "emotional_connection": 0.3,
                },
            },
            "persistence": {
                "name": "Persévérance",
                "description": "Détermination et résilience",
                "icon": "💪",
                "color": "#44aa44",
                "metrics": ["retry_count", "comeback_success", "difficulty_overcome"],
                "weight": {
                    "retry_count": 0.3,
                    "comeback_success": 0.4,
                    "difficulty_overcome": 0.3,
                },
            },
        }

    def update_player_metrics(
        self,
        player_id: str,
        category: str,
        metrics: dict[str, float],
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Met à jour les métriques d'un joueur pour une catégorie"""

        if category not in self.categories:
            return {"error": "Catégorie invalide"}

        if player_id not in self.player_stats:
            self.player_stats[player_id] = {
                "categories": {},
                "overall_score": 0,
                "last_updated": datetime.now().isoformat(),
            }

        if category not in self.player_stats[player_id]["categories"]:
            self.player_stats[player_id]["categories"][category] = {
                "metrics": {},
                "score": 0,
                "rank": 0,
                "last_updated": datetime.now().isoformat(),
            }

        # Mettre à jour les métriques
        category_data = self.player_stats[player_id]["categories"][category]
        for metric, value in metrics.items():
            if metric in self.categories[category]["metrics"]:
                category_data["metrics"][metric] = value

        # Recalculer le score de la catégorie
        category_score = self._calculate_category_score(player_id, category)
        category_data["score"] = category_score
        category_data["last_updated"] = datetime.now().isoformat()

        # Recalculer le score global
        overall_score = self._calculate_overall_score(player_id)
        self.player_stats[player_id]["overall_score"] = overall_score
        self.player_stats[player_id]["last_updated"] = datetime.now().isoformat()

        # Mettre à jour les classements
        self._update_leaderboards()

        return {
            "success": True,
            "category_score": category_score,
            "overall_score": overall_score,
            "message": f"Métriques mises à jour pour {self.categories[category]['name']}",
        }

    def _calculate_category_score(self, player_id: str, category: str) -> float:
        """Calcule le score d'une catégorie pour un joueur"""
        if player_id not in self.player_stats:
            return 0.0

        if category not in self.player_stats[player_id]["categories"]:
            return 0.0

        category_data = self.player_stats[player_id]["categories"][category]
        metrics = category_data.get("metrics", {})
        weights = self.categories[category]["weight"]

        total_score = 0.0
        total_weight = 0.0

        for metric, weight in weights.items():
            if metric in metrics:
                # Normaliser la valeur (0-100)
                normalized_value = min(100, max(0, metrics[metric]))
                total_score += normalized_value * weight
                total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0.0

    def _calculate_overall_score(self, player_id: str) -> float:
        """Calcule le score global d'un joueur"""
        if player_id not in self.player_stats:
            return 0.0

        category_scores = []
        for category_data in self.player_stats[player_id]["categories"].values():
            category_scores.append(category_data.get("score", 0))

        if not category_scores:
            return 0.0

        return sum(category_scores) / len(category_scores)

    def _update_leaderboards(self) -> None:
        """Met à jour tous les classements"""
        for category in self.categories.keys():
            self._update_category_leaderboard(category)

    def _update_category_leaderboard(self, category: str) -> None:
        """Met à jour le classement d'une catégorie"""
        players = []

        for player_id, player_data in self.player_stats.items():
            if category in player_data["categories"]:
                score = player_data["categories"][category]["score"]
                players.append(
                    {
                        "player_id": player_id,
                        "score": score,
                        "last_updated": player_data["categories"][category][
                            "last_updated"
                        ],
                    },
                )

        # Trier par score décroissant
        players.sort(key=lambda x: x["score"], reverse=True)

        # Assigner les rangs
        for rank, player in enumerate(players, 1):
            player_id = player["player_id"]
            self.player_stats[player_id]["categories"][category]["rank"] = rank

        # Sauvegarder le classement
        self.leaderboards[category] = {
            "players": players[:100],  # Top 100
            "last_updated": datetime.now().isoformat(),
            "total_players": len(players),
        }

    def get_leaderboard(
        self,
        category: str,
        period: str = "all_time",
        limit: int = 50,
    ) -> dict[str, Any]:
        """Retourne le classement d'une catégorie"""

        if category not in self.categories:
            return {"error": "Catégorie invalide"}

        if category not in self.leaderboards:
            return {"error": "Classement non disponible"}

        leaderboard_data = self.leaderboards[category]
        players = leaderboard_data["players"][:limit]

        # Ajouter des informations supplémentaires
        for player in players:
            player_id = player["player_id"]
            if player_id in self.player_stats:
                player["overall_score"] = self.player_stats[player_id]["overall_score"]
                player["total_categories"] = len(
                    self.player_stats[player_id]["categories"]
                )

        return {
            "category": self.categories[category],
            "period": period,
            "players": players,
            "total_players": leaderboard_data["total_players"],
            "last_updated": leaderboard_data["last_updated"],
        }

    def get_player_rank(self, player_id: str, category: str) -> dict[str, Any]:
        """Retourne le rang d'un joueur dans une catégorie"""

        if player_id not in self.player_stats:
            return {"error": "Joueur non trouvé"}

        if category not in self.player_stats[player_id]["categories"]:
            return {"error": "Joueur non classé dans cette catégorie"}

        player_data = self.player_stats[player_id]["categories"][category]
        rank = player_data["rank"]
        score = player_data["score"]

        # Calculer le percentile
        if category in self.leaderboards:
            total_players = self.leaderboards[category]["total_players"]
            percentile = (
                ((total_players - rank + 1) / total_players) * 100
                if total_players > 0
                else 0
            )
        else:
            percentile = 0

        return {
            "player_id": player_id,
            "category": category,
            "rank": rank,
            "score": score,
            "percentile": percentile,
            "category_info": self.categories[category],
        }

    def get_player_overview(self, player_id: str) -> dict[str, Any]:
        """Retourne un aperçu des performances d'un joueur"""

        if player_id not in self.player_stats:
            return {"error": "Joueur non trouvé"}

        player_data = self.player_stats[player_id]
        categories = []

        for category, category_data in player_data["categories"].items():
            categories.append(
                {
                    "category": category,
                    "name": self.categories[category]["name"],
                    "icon": self.categories[category]["icon"],
                    "color": self.categories[category]["color"],
                    "score": category_data["score"],
                    "rank": category_data["rank"],
                    "metrics": category_data["metrics"],
                },
            )

        # Trier par score décroissant
        categories.sort(key=lambda x: x["score"], reverse=True)

        return {
            "player_id": player_id,
            "overall_score": player_data["overall_score"],
            "categories": categories,
            "best_category": categories[0] if categories else None,
            "total_categories": len(categories),
            "last_updated": player_data["last_updated"],
        }

    def get_category_comparison(self, player_id: str) -> dict[str, Any]:
        """Retourne une comparaison des performances par catégorie"""

        if player_id not in self.player_stats:
            return {"error": "Joueur non trouvé"}

        player_data = self.player_stats[player_id]
        comparison = []

        for category, category_data in player_data["categories"].items():
            category_info = self.categories[category]
            score = category_data["score"]
            rank = category_data["rank"]

            # Calculer le percentile
            if category in self.leaderboards:
                total_players = self.leaderboards[category]["total_players"]
                percentile = (
                    ((total_players - rank + 1) / total_players) * 100
                    if total_players > 0
                    else 0
                )
            else:
                percentile = 0

            # Déterminer le niveau de performance
            if percentile >= 90:
                performance_level = "excellent"
            elif percentile >= 75:
                performance_level = "good"
            elif percentile >= 50:
                performance_level = "average"
            else:
                performance_level = "needs_improvement"

            comparison.append(
                {
                    "category": category,
                    "name": category_info["name"],
                    "icon": category_info["icon"],
                    "color": category_info["color"],
                    "score": score,
                    "rank": rank,
                    "percentile": percentile,
                    "performance_level": performance_level,
                },
            )

        # Trier par percentile décroissant
        comparison.sort(key=lambda x: x["percentile"], reverse=True)

        return {
            "player_id": player_id,
            "comparison": comparison,
            "strongest_category": comparison[0] if comparison else None,
            "weakest_category": comparison[-1] if comparison else None,
        }

    def get_global_leaderboard(self, limit: int = 50) -> dict[str, Any]:
        """Retourne le classement global"""

        players = []
        for player_id, player_data in self.player_stats.items():
            players.append(
                {
                    "player_id": player_id,
                    "overall_score": player_data["overall_score"],
                    "categories_count": len(player_data["categories"]),
                    "last_updated": player_data["last_updated"],
                },
            )

        # Trier par score global décroissant
        players.sort(key=lambda x: x["overall_score"], reverse=True)

        return {
            "type": "global",
            "players": players[:limit],
            "total_players": len(players),
            "last_updated": datetime.now().isoformat(),
        }

    def get_achievement_leaderboard(
        self, category: str, limit: int = 50
    ) -> dict[str, Any]:
        """Retourne le classement des achievements par catégorie"""

        if category not in self.categories:
            return {"error": "Catégorie invalide"}

        # Logique pour calculer les achievements par catégorie
        # À implémenter selon les besoins
        return {
            "category": self.categories[category],
            "players": [],
            "total_players": 0,
            "last_updated": datetime.now().isoformat(),
        }

    def get_weekly_leaderboard(self, category: str, limit: int = 50) -> dict[str, Any]:
        """Retourne le classement hebdomadaire d'une catégorie"""

        if category not in self.categories:
            return {"error": "Catégorie invalide"}

        # Logique pour calculer le classement hebdomadaire
        # À implémenter selon les besoins
        return {
            "category": self.categories[category],
            "period": "weekly",
            "players": [],
            "total_players": 0,
            "last_updated": datetime.now().isoformat(),
        }

    def get_monthly_leaderboard(self, category: str, limit: int = 50) -> dict[str, Any]:
        """Retourne le classement mensuel d'une catégorie"""

        if category not in self.categories:
            return {"error": "Catégorie invalide"}

        # Logique pour calculer le classement mensuel
        # À implémenter selon les besoins
        return {
            "category": self.categories[category],
            "period": "monthly",
            "players": [],
            "total_players": 0,
            "last_updated": datetime.now().isoformat(),
        }

    def get_categories(self) -> dict[str, Any]:
        """Retourne toutes les catégories disponibles"""
        return self.categories

    def save_leaderboard_data(self) -> bool:
        """Sauvegarde les données de classements"""
        try:
            data = {
                "categories": self.categories,
                "leaderboards": self.leaderboards,
                "player_stats": self.player_stats,
                "ranking_periods": self.ranking_periods,
            }

            with open("data/category_leaderboards.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde classements: {e}")
            return False


# Instance globale
category_leaderboards = CategoryLeaderboards()
