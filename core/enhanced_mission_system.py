#!/usr/bin/env python3
"""
Enhanced Mission System - Système de missions amélioré pour Arkalia Quest
Ajoute des choix multiples, des échecs possibles et des récompenses variables
"""

import random
from datetime import datetime
from typing import Any

from core.database import DatabaseManager


class EnhancedMissionSystem:
    """Système de missions amélioré avec gameplay interactif"""

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.missions = {}
        self.skill_tree = self._init_skill_tree()
        self.daily_challenges = self._init_daily_challenges()
        self.load_missions()

    def _init_skill_tree(self) -> dict[str, Any]:
        """Initialise l'arbre de compétences"""
        return {
            "hacking": {
                "name": "Hacking",
                "levels": ["Débutant", "Intermédiaire", "Avancé", "Expert"],
                "skills": {
                    "code_breaking": {"level": 0, "xp_required": 100, "unlocked": True},
                    "system_penetration": {
                        "level": 0,
                        "xp_required": 200,
                        "unlocked": False,
                    },
                    "cryptography": {"level": 0, "xp_required": 300, "unlocked": False},
                    "social_engineering": {
                        "level": 0,
                        "xp_required": 150,
                        "unlocked": False,
                    },
                },
            },
            "combat": {
                "name": "Combat",
                "levels": ["Débutant", "Intermédiaire", "Avancé", "Expert"],
                "skills": {
                    "defense": {"level": 0, "xp_required": 100, "unlocked": True},
                    "offense": {"level": 0, "xp_required": 200, "unlocked": False},
                    "strategy": {"level": 0, "xp_required": 300, "unlocked": False},
                    "tactics": {"level": 0, "xp_required": 150, "unlocked": False},
                },
            },
            "social": {
                "name": "Social",
                "levels": ["Débutant", "Intermédiaire", "Avancé", "Expert"],
                "skills": {
                    "persuasion": {"level": 0, "xp_required": 100, "unlocked": True},
                    "negotiation": {"level": 0, "xp_required": 200, "unlocked": False},
                    "leadership": {"level": 0, "xp_required": 300, "unlocked": False},
                    "diplomacy": {"level": 0, "xp_required": 150, "unlocked": False},
                },
            },
        }

    def _init_daily_challenges(self) -> dict[str, Any]:
        """Initialise les défis quotidiens"""
        return {
            "hacking_sprint": {
                "name": "Sprint Hacking",
                "description": "Résolvez 3 puzzles de hacking en moins de 5 minutes",
                "reward": {"xp": 150, "coins": 50},
                "difficulty": "moyen",
            },
            "memory_master": {
                "name": "Maître de la Mémoire",
                "description": "Mémorisez une séquence de 10 éléments",
                "reward": {"xp": 100, "coins": 30},
                "difficulty": "facile",
            },
            "speed_typing": {
                "name": "Frappe Rapide",
                "description": "Tapez 200 caractères en moins de 30 secondes",
                "reward": {"xp": 80, "coins": 25},
                "difficulty": "facile",
            },
        }

    def load_missions(self):
        """Charge les missions depuis la base de données"""
        try:
            missions = self.db_manager.load_all_missions()
            for mission in missions:
                self.missions[mission["mission_id"]] = mission
        except Exception as e:
            print(f"Erreur chargement missions: {e}")

    def create_interactive_mission(
        self, mission_id: str, mission_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Crée une mission interactive avec choix multiples"""
        return {
            "id": mission_id,
            "name": mission_data.get("name", "Mission Interactive"),
            "description": mission_data.get("description", ""),
            "type": "interactive",
            "difficulty": mission_data.get("difficulty", "facile"),
            "choices": mission_data.get("choices", []),
            "consequences": mission_data.get("consequences", {}),
            "time_limit": mission_data.get("time_limit", 0),  # 0 = pas de limite
            "failure_conditions": mission_data.get("failure_conditions", []),
            "rewards": mission_data.get("rewards", {"xp": 50, "coins": 10}),
            "skill_requirements": mission_data.get("skill_requirements", {}),
            "status": "available",
        }

    def execute_mission_choice(
        self, mission_id: str, choice_id: str, profile: dict[str, Any],
    ) -> dict[str, Any]:
        """Exécute un choix dans une mission interactive"""
        mission = self.missions.get(mission_id)
        if not mission:
            return {"success": False, "message": "Mission non trouvée"}

        # Vérifier les prérequis de compétences
        if not self._check_skill_requirements(mission, profile):
            return {
                "success": False,
                "message": "Compétences insuffisantes pour cette mission",
                "required_skills": mission.get("skill_requirements", {}),
            }

        # Trouver le choix
        choice = None
        for c in mission.get("choices", []):
            if c["id"] == choice_id:
                choice = c
                break

        if not choice:
            return {"success": False, "message": "Choix non trouvé"}

        # Calculer le succès basé sur les compétences
        success_rate = self._calculate_success_rate(mission, choice, profile)
        success = random.random() < success_rate

        if success:
            # Mission réussie
            result = self._handle_mission_success(mission, choice, profile)
        else:
            # Mission échouée
            result = self._handle_mission_failure(mission, choice, profile)

        return result

    def _check_skill_requirements(self, mission: dict[str, Any], profile: dict[str, Any]) -> bool:
        """Vérifie si le joueur a les compétences requises"""
        requirements = mission.get("skill_requirements", {})
        player_skills = profile.get("skills", {})

        for skill_category, required_level in requirements.items():
            if skill_category not in player_skills:
                return False
            if player_skills[skill_category] < required_level:
                return False

        return True

    def _calculate_success_rate(
        self, mission: dict[str, Any], choice: dict[str, Any], profile: dict[str, Any],
    ) -> float:
        """Calcule le taux de succès basé sur les compétences et le choix"""
        base_rate = 0.7  # 70% de base
        difficulty_modifier = {"facile": 0.2, "moyen": 0.0, "difficile": -0.2}.get(
            mission.get("difficulty", "moyen"), 0.0,
        )
        skill_bonus = self._calculate_skill_bonus(mission, profile)
        choice_modifier = choice.get("success_modifier", 0.0)

        return min(
            0.95,
            max(0.05, base_rate + difficulty_modifier + skill_bonus + choice_modifier),
        )

    def _calculate_skill_bonus(self, mission: dict[str, Any], profile: dict[str, Any]) -> float:
        """Calcule le bonus de compétences"""
        bonus = 0.0
        player_skills = profile.get("skills", {})
        requirements = mission.get("skill_requirements", {})

        for skill_category, required_level in requirements.items():
            player_level = player_skills.get(skill_category, 0)
            if player_level > required_level:
                bonus += (player_level - required_level) * 0.1

        return min(0.3, bonus)  # Maximum 30% de bonus

    def _handle_mission_success(
        self, mission: dict[str, Any], choice: dict[str, Any], profile: dict[str, Any],
    ) -> dict[str, Any]:
        """Gère le succès d'une mission"""
        # Calculer les récompenses variables
        base_rewards = mission.get("rewards", {"xp": 50, "coins": 10})
        choice_bonus = choice.get("reward_bonus", {})

        final_rewards = {
            "xp": base_rewards.get("xp", 0) + choice_bonus.get("xp", 0),
            "coins": base_rewards.get("coins", 0) + choice_bonus.get("coins", 0),
        }

        # Appliquer les récompenses
        profile["xp"] = profile.get("xp", 0) + final_rewards["xp"]
        profile["coins"] = profile.get("coins", 0) + final_rewards["coins"]

        # Mettre à jour les compétences
        self._update_skills(mission, profile)

        # Marquer la mission comme complétée
        if "missions_completed" not in profile:
            profile["missions_completed"] = []
        if mission["id"] not in profile["missions_completed"]:
            profile["missions_completed"].append(mission["id"])

        return {
            "success": True,
            "message": f"Mission '{mission['name']}' réussie !",
            "rewards": final_rewards,
            "consequence": choice.get("consequence", "success"),
            "ascii_art": "success",
        }

    def _handle_mission_failure(
        self, mission: dict[str, Any], choice: dict[str, Any], profile: dict[str, Any],
    ) -> dict[str, Any]:
        """Gère l'échec d'une mission"""
        # Pénalités d'échec
        failure_penalty = choice.get("failure_penalty", {"xp": -10, "coins": -5})

        profile["xp"] = max(0, profile.get("xp", 0) + failure_penalty.get("xp", 0))
        profile["coins"] = max(0, profile.get("coins", 0) + failure_penalty.get("coins", 0))

        return {
            "success": False,
            "message": f"Mission '{mission['name']}' échouée !",
            "penalty": failure_penalty,
            "consequence": choice.get("failure_consequence", "failure"),
            "ascii_art": "failure",
            "retry_available": True,
        }

    def _update_skills(self, mission: dict[str, Any], profile: dict[str, Any]):
        """Met à jour les compétences du joueur"""
        if "skills" not in profile:
            profile["skills"] = {}

        # Gain d'XP dans les compétences utilisées
        skill_xp = mission.get("skill_xp_gain", 10)
        requirements = mission.get("skill_requirements", {})

        for skill_category in requirements.keys():
            if skill_category not in profile["skills"]:
                profile["skills"][skill_category] = 0
            profile["skills"][skill_category] += skill_xp

    def get_available_missions(self, profile: dict[str, Any]) -> list[dict[str, Any]]:
        """Récupère les missions disponibles pour le joueur"""
        available = []

        for mission_id, mission in self.missions.items():
            if self._is_mission_available(mission, profile):
                mission_copy = mission.copy()
                mission_copy["available"] = True
                mission_copy["completed"] = mission_id in profile.get("missions_completed", [])
                available.append(mission_copy)

        return available

    def _is_mission_available(self, mission: dict[str, Any], profile: dict[str, Any]) -> bool:
        """Vérifie si une mission est disponible"""
        # Vérifier les prérequis de niveau
        required_level = mission.get("required_level", 1)
        if profile.get("level", 1) < required_level:
            return False

        # Vérifier les missions prérequises
        required_missions = mission.get("required_missions", [])
        completed_missions = profile.get("missions_completed", [])
        for req_mission in required_missions:
            if req_mission not in completed_missions:
                return False

        return True

    def start_daily_challenge(self, challenge_id: str, profile: dict[str, Any]) -> dict[str, Any]:
        """Démarre un défi quotidien"""
        challenge = self.daily_challenges.get(challenge_id)
        if not challenge:
            return {"success": False, "message": "Défi non trouvé"}

        # Vérifier si le défi a déjà été fait aujourd'hui
        today = datetime.now().date().isoformat()
        daily_challenges = profile.get("daily_challenges", {})
        if daily_challenges.get(challenge_id) == today:
            return {"success": False, "message": "Défi déjà complété aujourd'hui"}

        return {
            "success": True,
            "challenge": challenge,
            "message": f"Défi '{challenge['name']}' démarré !",
        }

    def complete_daily_challenge(
        self, challenge_id: str, profile: dict[str, Any], performance: dict[str, Any],
    ) -> dict[str, Any]:
        """Complète un défi quotidien"""
        challenge = self.daily_challenges.get(challenge_id)
        if not challenge:
            return {"success": False, "message": "Défi non trouvé"}

        # Calculer les récompenses basées sur la performance
        base_rewards = challenge.get("reward", {"xp": 50, "coins": 10})
        performance_multiplier = performance.get("multiplier", 1.0)

        final_rewards = {
            "xp": int(base_rewards.get("xp", 0) * performance_multiplier),
            "coins": int(base_rewards.get("coins", 0) * performance_multiplier),
        }

        # Appliquer les récompenses
        profile["xp"] = profile.get("xp", 0) + final_rewards["xp"]
        profile["coins"] = profile.get("coins", 0) + final_rewards["coins"]

        # Marquer le défi comme complété
        today = datetime.now().date().isoformat()
        if "daily_challenges" not in profile:
            profile["daily_challenges"] = {}
        profile["daily_challenges"][challenge_id] = today

        return {
            "success": True,
            "message": f"Défi '{challenge['name']}' complété !",
            "rewards": final_rewards,
            "performance": performance,
        }

    def get_skill_tree(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Récupère l'arbre de compétences du joueur"""
        player_skills = profile.get("skills", {})

        # Mettre à jour l'arbre avec les compétences du joueur
        skill_tree = self.skill_tree.copy()
        for _category, skills in skill_tree.items():
            for skill_id, skill_data in skills["skills"].items():
                skill_data["level"] = player_skills.get(skill_id, 0)
                skill_data["unlocked"] = skill_data["level"] > 0

        return skill_tree

    def get_daily_challenges(self, profile: dict[str, Any]) -> list[dict[str, Any]]:
        """Récupère les défis quotidiens disponibles"""
        today = datetime.now().date().isoformat()
        daily_challenges = profile.get("daily_challenges", {})

        available = []
        for challenge_id, challenge in self.daily_challenges.items():
            challenge_copy = challenge.copy()
            challenge_copy["id"] = challenge_id
            challenge_copy["completed_today"] = daily_challenges.get(challenge_id) == today
            available.append(challenge_copy)

        return available
