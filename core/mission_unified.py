#!/usr/bin/env python3
"""
Système de missions unifié pour Arkalia Quest
Combine les fonctionnalités de mission_handler.py et enhanced_mission_system.py
"""

import random
from datetime import datetime
from typing import Any, Optional

from core.database import DatabaseManager


class MissionUnified:
    """Système de missions unifié avec toutes les fonctionnalités"""

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
                    "code_breaking": {"level": 0, "unlocked": True, "xp_required": 100},
                    "cryptography": {"level": 0, "unlocked": False, "xp_required": 300},
                    "social_engineering": {
                        "level": 0,
                        "unlocked": False,
                        "xp_required": 150,
                    },
                    "system_penetration": {
                        "level": 0,
                        "unlocked": False,
                        "xp_required": 200,
                    },
                },
            },
            "combat": {
                "name": "Combat",
                "levels": ["Débutant", "Intermédiaire", "Avancé", "Expert"],
                "skills": {
                    "defense": {"level": 0, "unlocked": False, "xp_required": 100},
                    "offense": {"level": 0, "unlocked": False, "xp_required": 200},
                    "strategy": {"level": 0, "unlocked": False, "xp_required": 300},
                    "tactics": {"level": 0, "unlocked": False, "xp_required": 150},
                },
            },
            "social": {
                "name": "Social",
                "levels": ["Débutant", "Intermédiaire", "Avancé", "Expert"],
                "skills": {
                    "diplomacy": {"level": 0, "unlocked": False, "xp_required": 150},
                    "leadership": {"level": 0, "unlocked": False, "xp_required": 300},
                    "negotiation": {"level": 0, "unlocked": False, "xp_required": 200},
                    "persuasion": {"level": 0, "unlocked": False, "xp_required": 100},
                },
            },
        }

    def _init_daily_challenges(self) -> dict[str, Any]:
        """Initialise les défis quotidiens"""
        return {
            "code_master": {
                "name": "Maître du Code",
                "description": "Résolvez 5 problèmes de programmation",
                "target": 5,
                "reward": {"xp": 100, "coins": 50},
                "type": "programming",
            },
            "explorer": {
                "name": "Explorateur",
                "description": "Explorez 3 nouvelles zones",
                "target": 3,
                "reward": {"xp": 75, "coins": 25},
                "type": "exploration",
            },
            "hacker_speed": {
                "name": "Hacker Rapide",
                "description": "Terminez 3 missions de hacking en moins de 10 minutes",
                "target": 3,
                "reward": {"xp": 150, "coins": 75},
                "type": "hacking",
            },
            "luna_friend": {
                "name": "Ami de LUNA",
                "description": "Interagissez avec LUNA 5 fois",
                "target": 5,
                "reward": {"xp": 50, "coins": 25},
                "type": "social",
            },
        }

    def load_missions(self):
        """Charge toutes les missions depuis SQLite"""
        missions = self.db_manager.load_all_missions()
        for mission in missions:
            self.missions[mission["mission_id"]] = mission

    def load_all_data(self):
        """Charge toutes les données nécessaires"""
        self.load_missions()

    # Méthodes de mission_handler
    def get_mission(self, mission_id: str) -> Optional[dict[str, Any]]:
        """Récupère une mission par son ID"""
        return self.missions.get(mission_id)

    def get_all_missions(self) -> list[dict[str, Any]]:
        """Récupère toutes les missions disponibles"""
        return list(self.missions.values())

    def get_missions_by_act(self, act: int) -> list[dict[str, Any]]:
        """Récupère les missions d'un acte spécifique"""
        return [
            mission for mission in self.missions.values() if mission.get("act") == act
        ]

    def get_missions_by_difficulty(self, difficulty: str) -> list[dict[str, Any]]:
        """Récupère les missions par difficulté"""
        return [
            mission
            for mission in self.missions.values()
            if mission.get("difficulty") == difficulty
        ]

    def get_random_mission(
        self, difficulty: Optional[str] = None
    ) -> Optional[dict[str, Any]]:
        """Récupère une mission aléatoire"""
        missions = self.missions.values()
        if difficulty:
            missions = [m for m in missions if m.get("difficulty") == difficulty]

        if not missions:
            return None

        return random.choice(list(missions))

    def complete_mission(
        self, mission_id: str, player_id: str, success: bool = True
    ) -> dict[str, Any]:
        """Marque une mission comme terminée"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {"success": False, "error": "Mission non trouvée"}

        # Logique de completion
        result = {
            "success": success,
            "mission_id": mission_id,
            "player_id": player_id,
            "completed_at": datetime.now().isoformat(),
        }

        # Calculer les récompenses
        if success:
            result["rewards"] = mission.get("rewards", {"xp": 50, "coins": 25})
        else:
            result["rewards"] = {"xp": 10, "coins": 5}

        return result

    # Méthodes de enhanced_mission_system
    def get_skill_tree(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Récupère l'arbre de compétences pour un profil"""
        # Mettre à jour les compétences basées sur le profil
        updated_skill_tree = self.skill_tree.copy()

        # Appliquer les compétences du joueur
        player_skills = profile.get("skills", {})
        for category, skills in player_skills.items():
            if category in updated_skill_tree:
                for skill_name, level in skills.items():
                    if skill_name in updated_skill_tree[category]["skills"]:
                        updated_skill_tree[category]["skills"][skill_name]["level"] = (
                            level
                        )
                        updated_skill_tree[category]["skills"][skill_name][
                            "unlocked"
                        ] = level > 0

        return updated_skill_tree

    def get_available_missions(self, profile: dict[str, Any]) -> list[dict[str, Any]]:
        """Récupère les missions disponibles pour un profil"""
        level = profile.get("level", 1)
        completed_missions = profile.get("missions_completed", [])

        available = []
        for mission in self.missions.values():
            # Vérifier le niveau requis
            required_level = mission.get("required_level", 1)
            if level >= required_level:
                # Vérifier si pas déjà terminée
                if mission["mission_id"] not in completed_missions:
                    available.append(mission)

        return available

    def get_mission_details(self, mission_id: str) -> Optional[dict[str, Any]]:
        """Récupère les détails d'une mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return None

        # Enrichir avec des détails supplémentaires
        enhanced_mission = mission.copy()
        enhanced_mission["choices"] = self._generate_mission_choices(mission)
        enhanced_mission["consequences"] = self._generate_mission_consequences(mission)

        return enhanced_mission

    def _generate_mission_choices(
        self, mission: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Génère des choix pour une mission"""
        choices = []

        # Choix basés sur le type de mission
        mission_type = mission.get("type", "standard")

        if mission_type == "hacking":
            choices = [
                {"id": "stealth", "text": "Approche furtive", "difficulty": "hard"},
                {"id": "brute_force", "text": "Force brute", "difficulty": "medium"},
                {"id": "social", "text": "Ingénierie sociale", "difficulty": "easy"},
            ]
        elif mission_type == "exploration":
            choices = [
                {"id": "careful", "text": "Exploration prudente", "difficulty": "easy"},
                {
                    "id": "aggressive",
                    "text": "Exploration agressive",
                    "difficulty": "hard",
                },
                {
                    "id": "stealth",
                    "text": "Exploration furtive",
                    "difficulty": "medium",
                },
            ]
        else:
            choices = [
                {"id": "standard", "text": "Approche standard", "difficulty": "medium"}
            ]

        return choices

    def _generate_mission_consequences(self, mission: dict[str, Any]) -> dict[str, Any]:
        """Génère les conséquences possibles d'une mission"""
        return {
            "success": {
                "xp_bonus": mission.get("xp_reward", 50),
                "coin_bonus": mission.get("coin_reward", 25),
                "unlock_mission": mission.get("unlocks", []),
            },
            "failure": {"xp_penalty": 10, "coin_penalty": 5, "retry_available": True},
            "partial_success": {
                "xp_bonus": mission.get("xp_reward", 50) // 2,
                "coin_bonus": mission.get("coin_reward", 25) // 2,
                "retry_available": True,
            },
        }

    def get_daily_challenges(self) -> dict[str, Any]:
        """Récupère les défis quotidiens"""
        return self.daily_challenges

    def complete_daily_challenge(
        self, challenge_id: str, player_id: str
    ) -> dict[str, Any]:
        """Termine un défi quotidien"""
        challenge = self.daily_challenges.get(challenge_id)
        if not challenge:
            return {"success": False, "error": "Défi non trouvé"}

        return {
            "success": True,
            "challenge_id": challenge_id,
            "player_id": player_id,
            "rewards": challenge["reward"],
            "completed_at": datetime.now().isoformat(),
        }

    def get_mission_progress(self, mission_id: str, player_id: str) -> dict[str, Any]:
        """Récupère le progrès d'une mission"""
        # Cette méthode devrait interroger la base de données
        # Pour l'instant, retourner un progrès par défaut
        return {
            "mission_id": mission_id,
            "player_id": player_id,
            "progress": 0,
            "status": "not_started",
            "last_updated": datetime.now().isoformat(),
        }

    def get_current_acte(self, profil: dict[str, Any]) -> str:
        """Détermine l'acte actuel basé sur les missions complétées"""
        completed_missions = profil.get("missions_completed", [])

        # Logique de progression des actes
        if "prologue" in completed_missions:
            if "acte_1" in completed_missions:
                return "acte_2"
            return "acte_1"
        return "prologue"

    def execute_mission_step(
        self, mission_id: str, step_id: str, profil: dict[str, Any]
    ) -> dict[str, Any]:
        """Exécute une étape de mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {"success": False, "error": "Mission non trouvée"}

        # Trouver l'étape
        etapes = mission.get("etapes", [])
        step = next((s for s in etapes if s["id"] == step_id), None)
        if not step:
            return {"success": False, "error": "Étape non trouvée"}

        # Initialiser les structures si nécessaire
        if "points" not in profil:
            profil["points"] = 0
        if "missions_completed" not in profil:
            profil["missions_completed"] = []
        if "objets_debloques" not in profil:
            profil["objets_debloques"] = []
        if "etapes_completed" not in profil:
            profil["etapes_completed"] = {}

        # Ajouter les points
        recompense = step.get("recompense", 0)
        profil["points"] += recompense

        # Marquer l'étape comme complétée
        if mission_id not in profil["etapes_completed"]:
            profil["etapes_completed"][mission_id] = []
        profil["etapes_completed"][mission_id].append(step_id)

        # Vérifier si la mission est complète
        completed_steps = profil["etapes_completed"].get(mission_id, [])
        if len(completed_steps) >= len(etapes):
            profil["missions_completed"].append(mission_id)
            # Ajouter l'objet symbolique si présent
            objet = mission.get("objet_symbolique")
            if objet:
                profil["objets_debloques"].append(objet)

        return {
            "success": True,
            "step_id": step_id,
            "recompense": recompense,
            "mission_complete": len(completed_steps) >= len(etapes),
        }

    def update_mission_progress(
        self, mission_id: str, player_id: str, progress: int
    ) -> dict[str, Any]:
        """Met à jour le progrès d'une mission"""
        return {
            "success": True,
            "mission_id": mission_id,
            "player_id": player_id,
            "progress": progress,
            "updated_at": datetime.now().isoformat(),
        }


# Instance globale
mission_unified = MissionUnified()
