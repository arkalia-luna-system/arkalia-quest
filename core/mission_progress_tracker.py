#!/usr/bin/env python3
"""
🎯 MISSION PROGRESS TRACKER - ARKALIA QUEST
==========================================

Système avancé de suivi de progression des missions avec indicateurs visuels
et feedback contextuel pour améliorer l'expérience utilisateur.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class MissionProgressTracker:
    """Gestionnaire avancé de progression des missions"""

    def __init__(self):
        self.mission_states = {}
        self.progress_indicators = {}
        self.visual_feedback = {}
        self.achievement_triggers = {}

    def initialize_mission_progress(
        self,
        mission_id: str,
        player_id: str,
        total_steps: int = 5,
    ) -> dict[str, Any]:
        """Initialise le suivi de progression pour une mission"""
        progress_key = f"{player_id}_{mission_id}"

        if progress_key not in self.mission_states:
            self.mission_states[progress_key] = {
                "mission_id": mission_id,
                "player_id": player_id,
                "start_time": datetime.now().isoformat(),
                "current_step": 0,
                "total_steps": total_steps,
                "completed_steps": [],
                "failed_attempts": 0,
                "hints_used": 0,
                "time_spent": 0,
                "difficulty_level": "medium",
                "progress_percentage": 0.0,
                "status": "active",  # active, completed, failed, paused
                "branches_unlocked": [],
                "choices_made": [],
                "resources_used": [],
                "achievements_earned": [],
                "visual_effects": [],
                "last_activity": datetime.now().isoformat(),
            }

        return self.mission_states[progress_key]

    def update_mission_progress(
        self,
        mission_id: str,
        player_id: str,
        step_id: str,
        action: str,
        success: bool = True,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Met à jour la progression d'une mission avec indicateurs visuels"""
        progress_key = f"{player_id}_{mission_id}"

        if progress_key not in self.mission_states:
            self.initialize_mission_progress(mission_id, player_id)

        progress = self.mission_states[progress_key]
        progress["last_activity"] = datetime.now().isoformat()

        # Calculer le temps écoulé
        start_time = datetime.fromisoformat(progress["start_time"])
        time_spent = (datetime.now() - start_time).total_seconds()
        progress["time_spent"] = time_spent

        # Mettre à jour selon l'action
        if action == "step_completed" and success:
            if step_id not in progress["completed_steps"]:
                progress["completed_steps"].append(step_id)
                progress["current_step"] += 1
                progress["progress_percentage"] = (
                    len(progress["completed_steps"]) / progress["total_steps"]
                ) * 100

                # Déclencher des effets visuels
                self._trigger_progress_effects(progress, "step_completed")

        elif action == "step_failed":
            progress["failed_attempts"] += 1
            self._trigger_progress_effects(progress, "step_failed")

        elif action == "hint_used":
            progress["hints_used"] += 1
            self._trigger_progress_effects(progress, "hint_used")

        elif action == "branch_unlocked":
            branch_id = metadata.get("branch_id") if metadata else "unknown"
            if branch_id not in progress["branches_unlocked"]:
                progress["branches_unlocked"].append(branch_id)
                self._trigger_progress_effects(progress, "branch_unlocked")

        elif action == "choice_made":
            choice_data = metadata or {}
            progress["choices_made"].append(
                {
                    "step_id": step_id,
                    "choice": choice_data.get("choice"),
                    "timestamp": datetime.now().isoformat(),
                    "consequence": choice_data.get("consequence"),
                },
            )
            self._trigger_progress_effects(progress, "choice_made")

        # Vérifier si la mission est terminée
        if progress["progress_percentage"] >= 100:
            progress["status"] = "completed"
            self._trigger_progress_effects(progress, "mission_completed")

        # Générer les indicateurs visuels
        visual_indicators = self._generate_visual_indicators(progress)

        return {
            "success": True,
            "progress": progress,
            "visual_indicators": visual_indicators,
            "achievements": self._check_achievements(progress),
            "feedback": self._generate_contextual_feedback(progress, action, success),
        }

    def _trigger_progress_effects(
        self, progress: dict[str, Any], effect_type: str
    ) -> None:
        """Déclenche des effets visuels selon le type de progression"""
        effects = {
            "step_completed": {
                "type": "success_pulse",
                "color": "#00ff00",
                "animation": "bounce",
                "sound": "success",
                "particles": True,
                "message": "✅ Étape complétée !",
            },
            "step_failed": {
                "type": "error_shake",
                "color": "#ff4444",
                "animation": "shake",
                "sound": "error",
                "particles": False,
                "message": "❌ Essaie encore !",
            },
            "hint_used": {
                "type": "hint_glow",
                "color": "#ffaa00",
                "animation": "glow",
                "sound": "hint",
                "particles": False,
                "message": "💡 Indice utilisé",
            },
            "branch_unlocked": {
                "type": "branch_reveal",
                "color": "#00ffff",
                "animation": "fade_in",
                "sound": "unlock",
                "particles": True,
                "message": "🌟 Nouvelle branche débloquée !",
            },
            "choice_made": {
                "type": "choice_highlight",
                "color": "#aa00ff",
                "animation": "highlight",
                "sound": "choice",
                "particles": False,
                "message": "🎯 Choix enregistré",
            },
            "mission_completed": {
                "type": "celebration",
                "color": "#00ff00",
                "animation": "confetti",
                "sound": "victory",
                "particles": True,
                "message": "🎉 Mission terminée !",
            },
        }

        if effect_type in effects:
            progress["visual_effects"].append(
                {
                    "type": effect_type,
                    "effect": effects[effect_type],
                    "timestamp": datetime.now().isoformat(),
                },
            )

    def _generate_visual_indicators(self, progress: dict[str, Any]) -> dict[str, Any]:
        """Génère les indicateurs visuels de progression"""
        return {
            "progress_bar": {
                "percentage": progress["progress_percentage"],
                "current_step": progress["current_step"],
                "total_steps": progress["total_steps"],
                "color": self._get_progress_color(progress["progress_percentage"]),
                "animation": (
                    "fill_up" if progress["progress_percentage"] > 0 else "idle"
                ),
            },
            "step_indicators": [
                {
                    "step_id": f"step_{i}",
                    "status": (
                        "completed"
                        if i < len(progress["completed_steps"])
                        else "pending"
                    ),
                    "icon": "✅" if i < len(progress["completed_steps"]) else "⏳",
                    "tooltip": f"Étape {i + 1}",
                }
                for i in range(progress["total_steps"])
            ],
            "time_indicators": {
                "time_spent": progress["time_spent"],
                "estimated_remaining": self._estimate_remaining_time(progress),
                "efficiency": self._calculate_efficiency(progress),
            },
            "difficulty_indicators": {
                "current_level": progress["difficulty_level"],
                "adaptive_difficulty": self._calculate_adaptive_difficulty(progress),
                "recommendations": self._get_difficulty_recommendations(progress),
            },
            "achievement_indicators": {
                "unlocked_count": len(progress["achievements_earned"]),
                "available_count": self._count_available_achievements(progress),
                "next_achievement": self._get_next_achievement(progress),
            },
        }

    def _get_progress_color(self, percentage: float) -> str:
        """Retourne la couleur selon le pourcentage de progression"""
        if percentage < 25:
            return "#ff4444"  # Rouge
        if percentage < 50:
            return "#ffaa00"  # Orange
        if percentage < 75:
            return "#ffff00"  # Jaune
        return "#00ff00"  # Vert

    def _estimate_remaining_time(self, progress: dict[str, Any]) -> float:
        """Estime le temps restant pour terminer la mission"""
        if progress["progress_percentage"] == 0:
            return 0

        time_per_step = progress["time_spent"] / len(progress["completed_steps"])
        remaining_steps = progress["total_steps"] - len(progress["completed_steps"])
        return time_per_step * remaining_steps

    def _calculate_efficiency(self, progress: dict[str, Any]) -> str:
        """Calcule l'efficacité du joueur"""
        if progress["time_spent"] == 0:
            return "unknown"

        steps_per_minute = len(progress["completed_steps"]) / (
            progress["time_spent"] / 60
        )

        if steps_per_minute > 2:
            return "excellent"
        if steps_per_minute > 1:
            return "good"
        if steps_per_minute > 0.5:
            return "average"
        return "needs_improvement"

    def _calculate_adaptive_difficulty(self, progress: dict[str, Any]) -> str:
        """Calcule la difficulté adaptative basée sur les performances"""
        if progress["failed_attempts"] == 0 and progress["hints_used"] == 0:
            return "increase"
        if progress["failed_attempts"] > 3 or progress["hints_used"] > 2:
            return "decrease"
        return "maintain"

    def _get_difficulty_recommendations(self, progress: dict[str, Any]) -> list[str]:
        """Retourne des recommandations de difficulté"""
        recommendations = []

        if progress["failed_attempts"] > 5:
            recommendations.append("💡 Essaie de prendre plus de temps pour réfléchir")

        if progress["hints_used"] > 3:
            recommendations.append("🎯 Concentre-toi sur les détails importants")

        if progress["time_spent"] > 1800:  # 30 minutes
            recommendations.append("⏰ Prends une pause si nécessaire")

        return recommendations

    def _count_available_achievements(self, progress: dict[str, Any]) -> int:
        """Compte les achievements disponibles pour cette mission"""
        # Logique pour compter les achievements disponibles
        return 5  # Valeur par défaut

    def _get_next_achievement(
        self, progress: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Retourne le prochain achievement à débloquer"""
        return {
            "id": "speed_demon",
            "name": "Démon de vitesse",
            "description": "Termine une mission en moins de 10 minutes",
            "progress": 0.6,
            "icon": "⚡",
        }

    def _check_achievements(self, progress: dict[str, Any]) -> list[dict[str, Any]]:
        """Vérifie et retourne les nouveaux achievements débloqués"""
        new_achievements = []

        # Achievement de vitesse
        if (
            progress["time_spent"] < 600 and progress["status"] == "completed"
        ):  # 10 minutes
            new_achievements.append(
                {
                    "id": "speed_demon",
                    "name": "Démon de vitesse",
                    "description": "Mission terminée en moins de 10 minutes !",
                    "icon": "⚡",
                    "points": 100,
                },
            )

        # Achievement de précision
        if progress["failed_attempts"] == 0 and progress["status"] == "completed":
            new_achievements.append(
                {
                    "id": "perfect_run",
                    "name": "Course parfaite",
                    "description": "Mission terminée sans erreur !",
                    "icon": "🎯",
                    "points": 150,
                },
            )

        return new_achievements

    def _generate_contextual_feedback(
        self,
        progress: dict[str, Any],
        action: str,
        success: bool,
    ) -> dict[str, Any]:
        """Génère un feedback contextuel basé sur la progression"""
        feedback = {
            "message": "",
            "tone": "neutral",
            "suggestions": [],
            "encouragement": "",
        }

        if action == "step_completed" and success:
            if progress["progress_percentage"] < 25:
                feedback["message"] = "🌟 Excellent début ! Continue comme ça !"
                feedback["tone"] = "encouraging"
            elif progress["progress_percentage"] < 50:
                feedback["message"] = "🚀 Tu es sur la bonne voie !"
                feedback["tone"] = "positive"
            elif progress["progress_percentage"] < 75:
                feedback["message"] = "💪 Plus que quelques étapes !"
                feedback["tone"] = "motivating"
            else:
                feedback["message"] = "🎯 Presque terminé ! Tu y es presque !"
                feedback["tone"] = "exciting"

        elif action == "step_failed":
            if progress["failed_attempts"] == 1:
                feedback["message"] = (
                    "💡 Pas de problème, essaie une approche différente !"
                )
                feedback["tone"] = "supportive"
                feedback["suggestions"] = [
                    "Vérifie tes données",
                    "Relis les instructions",
                ]
            elif progress["failed_attempts"] < 3:
                feedback["message"] = "🤔 Prends ton temps, tu vas y arriver !"
                feedback["tone"] = "patient"
                feedback["suggestions"] = [
                    "Utilise un indice si nécessaire",
                    "Demande de l'aide à LUNA",
                ]
            else:
                feedback["message"] = (
                    "🆘 Besoin d'aide ? LUNA peut te donner des conseils !"
                )
                feedback["tone"] = "helpful"
                feedback["suggestions"] = ["Utilise 'luna_help'", "Demande un indice"]

        return feedback

    def get_mission_analytics(self, player_id: str) -> dict[str, Any]:
        """Retourne les analytics de progression des missions pour un joueur"""
        player_missions = {
            key: progress
            for key, progress in self.mission_states.items()
            if progress["player_id"] == player_id
        }

        if not player_missions:
            return {"error": "Aucune mission trouvée pour ce joueur"}

        total_missions = len(player_missions)
        completed_missions = len(
            [p for p in player_missions.values() if p["status"] == "completed"],
        )
        total_time = sum(p["time_spent"] for p in player_missions.values())
        total_achievements = sum(
            len(p["achievements_earned"]) for p in player_missions.values()
        )

        return {
            "total_missions": total_missions,
            "completed_missions": completed_missions,
            "completion_rate": (
                (completed_missions / total_missions) * 100 if total_missions > 0 else 0
            ),
            "average_time_per_mission": (
                total_time / total_missions if total_missions > 0 else 0
            ),
            "total_achievements": total_achievements,
            "efficiency_rating": self._calculate_overall_efficiency(player_missions),
            "favorite_mission_type": self._get_favorite_mission_type(player_missions),
            "improvement_areas": self._get_improvement_areas(player_missions),
        }

    def _calculate_overall_efficiency(self, missions: dict[str, Any]) -> str:
        """Calcule l'efficacité globale du joueur"""
        if not missions:
            return "unknown"

        total_efficiency = 0
        for mission in missions.values():
            if mission["time_spent"] > 0:
                efficiency = len(mission["completed_steps"]) / (
                    mission["time_spent"] / 60
                )
                total_efficiency += efficiency

        average_efficiency = total_efficiency / len(missions)

        if average_efficiency > 2:
            return "excellent"
        if average_efficiency > 1:
            return "good"
        if average_efficiency > 0.5:
            return "average"
        return "needs_improvement"

    def _get_favorite_mission_type(self, missions: dict[str, Any]) -> str:
        """Détermine le type de mission préféré du joueur"""
        # Logique simplifiée - à étendre selon les types de missions
        return "hacking"  # Valeur par défaut

    def _get_improvement_areas(self, missions: dict[str, Any]) -> list[str]:
        """Identifie les domaines d'amélioration"""
        areas = []

        total_failed_attempts = sum(m["failed_attempts"] for m in missions.values())
        total_hints_used = sum(m["hints_used"] for m in missions.values())

        if total_failed_attempts > len(missions) * 2:
            areas.append("Réduire les tentatives échouées")

        if total_hints_used > len(missions) * 1.5:
            areas.append("Développer l'autonomie")

        return areas

    def save_progress_data(self) -> bool:
        """Sauvegarde les données de progression"""
        try:
            with open("data/mission_progress.json", "w", encoding="utf-8") as f:
                json.dump(self.mission_states, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde progression: {e}")
            return False

    def load_progress_data(self) -> bool:
        """Charge les données de progression"""
        try:
            with open("data/mission_progress.json", encoding="utf-8") as f:
                self.mission_states = json.load(f)
            return True
        except FileNotFoundError:
            logger.info(
                "Fichier de progression non trouvé, initialisation avec données vides"
            )
            return True
        except Exception as e:
            logger.error(f"Erreur chargement progression: {e}")
            return False


# Instance globale
mission_progress_tracker = MissionProgressTracker()
