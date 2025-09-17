#!/usr/bin/env python3
"""
🎯 SECONDARY MISSIONS - ARKALIA QUEST
=====================================

Système de missions secondaires et contenu additionnel pour prolonger
l'expérience de jeu et offrir plus de variété.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class SecondaryMissions:
    """Gestionnaire des missions secondaires et contenu additionnel"""

    def __init__(self):
        self.missions = {}
        self.daily_missions = {}
        self.weekly_missions = {}
        self.special_events = {}
        self.player_progress = {}

        # Charger les données
        self.load_mission_data()

    def load_mission_data(self) -> None:
        """Charge les données de missions secondaires"""
        try:
            with open("data/secondary_missions.json", encoding="utf-8") as f:
                data = json.load(f)
                self.missions = data.get("missions", {})
                self.daily_missions = data.get("daily_missions", {})
                self.weekly_missions = data.get("weekly_missions", {})
                self.special_events = data.get("special_events", {})
        except FileNotFoundError:
            logger.info(
                "Fichier de missions secondaires non trouvé, création des données par défaut",
            )
            self._create_default_missions()
        except Exception as e:
            logger.error(f"Erreur chargement missions secondaires: {e}")
            self._create_default_missions()

    def _create_default_missions(self) -> None:
        """Crée les missions secondaires par défaut"""
        self.missions = {
            "hacker_collection": {
                "id": "hacker_collection",
                "title": "Collectionneur de Codes",
                "description": "Collecte 10 fragments de code cachés dans le système",
                "type": "collection",
                "difficulty": "easy",
                "category": "exploration",
                "rewards": {
                    "xp": 200,
                    "badges": ["code_collector"],
                    "unlock": "advanced_hacking_tools",
                },
                "objectives": [
                    {
                        "id": "find_code_1",
                        "description": "Trouve le fragment de code #1",
                        "completed": False,
                    },
                    {
                        "id": "find_code_2",
                        "description": "Trouve le fragment de code #2",
                        "completed": False,
                    },
                    {
                        "id": "find_code_3",
                        "description": "Trouve le fragment de code #3",
                        "completed": False,
                    },
                    {
                        "id": "find_code_4",
                        "description": "Trouve le fragment de code #4",
                        "completed": False,
                    },
                    {
                        "id": "find_code_5",
                        "description": "Trouve le fragment de code #5",
                        "completed": False,
                    },
                    {
                        "id": "find_code_6",
                        "description": "Trouve le fragment de code #6",
                        "completed": False,
                    },
                    {
                        "id": "find_code_7",
                        "description": "Trouve le fragment de code #7",
                        "completed": False,
                    },
                    {
                        "id": "find_code_8",
                        "description": "Trouve le fragment de code #8",
                        "completed": False,
                    },
                    {
                        "id": "find_code_9",
                        "description": "Trouve le fragment de code #9",
                        "completed": False,
                    },
                    {
                        "id": "find_code_10",
                        "description": "Trouve le fragment de code #10",
                        "completed": False,
                    },
                ],
                "prerequisites": ["luna_contact_completed"],
                "unlock_conditions": ["level_2_reached"],
            },
            "luna_memory_core": {
                "id": "luna_memory_core",
                "title": "Cœur de Mémoire de LUNA",
                "description": "Aide LUNA à récupérer ses souvenirs perdus",
                "type": "story",
                "difficulty": "medium",
                "category": "luna_relationship",
                "rewards": {
                    "xp": 500,
                    "badges": ["luna_friend"],
                    "unlock": "luna_backstory",
                    "luna_relationship": 50,
                },
                "objectives": [
                    {
                        "id": "access_memory_bank",
                        "description": "Accède à la banque de mémoire de LUNA",
                        "completed": False,
                    },
                    {
                        "id": "decrypt_memory_1",
                        "description": "Déchiffre le premier souvenir",
                        "completed": False,
                    },
                    {
                        "id": "decrypt_memory_2",
                        "description": "Déchiffre le deuxième souvenir",
                        "completed": False,
                    },
                    {
                        "id": "decrypt_memory_3",
                        "description": "Déchiffre le troisième souvenir",
                        "completed": False,
                    },
                    {
                        "id": "restore_memory",
                        "description": "Restaure la mémoire de LUNA",
                        "completed": False,
                    },
                ],
                "prerequisites": ["luna_relationship_high"],
                "unlock_conditions": ["acte_2_completed"],
            },
            "cyber_security_expert": {
                "id": "cyber_security_expert",
                "title": "Expert en Cybersécurité",
                "description": "Prouve tes compétences en cybersécurité avec 5 défis",
                "type": "challenge",
                "difficulty": "hard",
                "category": "education",
                "rewards": {
                    "xp": 1000,
                    "badges": ["cyber_expert", "security_master"],
                    "unlock": "advanced_security_tools",
                    "skill_points": {"cybersecurity": 25},
                },
                "objectives": [
                    {
                        "id": "firewall_challenge",
                        "description": "Configure un pare-feu robuste",
                        "completed": False,
                    },
                    {
                        "id": "encryption_challenge",
                        "description": "Implémente un système de chiffrement",
                        "completed": False,
                    },
                    {
                        "id": "intrusion_detection",
                        "description": "Détecte et bloque une intrusion",
                        "completed": False,
                    },
                    {
                        "id": "vulnerability_assessment",
                        "description": "Évalue les vulnérabilités d'un système",
                        "completed": False,
                    },
                    {
                        "id": "incident_response",
                        "description": "Gère un incident de sécurité",
                        "completed": False,
                    },
                ],
                "prerequisites": ["hacking_basics_completed"],
                "unlock_conditions": ["level_5_reached", "security_interest_detected"],
            },
            "arkalia_explorer": {
                "id": "arkalia_explorer",
                "title": "Explorateur d'Arkalia",
                "description": "Découvre tous les secrets cachés du monde d'Arkalia",
                "type": "exploration",
                "difficulty": "medium",
                "category": "world_discovery",
                "rewards": {
                    "xp": 750,
                    "badges": ["arkalia_explorer", "world_discoverer"],
                    "unlock": "secret_arkalia_zones",
                    "skill_points": {"exploration": 20},
                },
                "objectives": [
                    {
                        "id": "find_secret_room_1",
                        "description": "Découvre la salle secrète #1",
                        "completed": False,
                    },
                    {
                        "id": "find_secret_room_2",
                        "description": "Découvre la salle secrète #2",
                        "completed": False,
                    },
                    {
                        "id": "find_secret_room_3",
                        "description": "Découvre la salle secrète #3",
                        "completed": False,
                    },
                    {
                        "id": "activate_ancient_terminal",
                        "description": "Active l'ancien terminal",
                        "completed": False,
                    },
                    {
                        "id": "decode_arkalia_secrets",
                        "description": "Déchiffre les secrets d'Arkalia",
                        "completed": False,
                    },
                ],
                "prerequisites": ["world_access_granted"],
                "unlock_conditions": ["acte_3_completed"],
            },
        }

        # Missions quotidiennes
        self.daily_missions = {
            "daily_hack": {
                "id": "daily_hack",
                "title": "Hack Quotidien",
                "description": "Effectue 3 hacks réussis aujourd'hui",
                "type": "daily",
                "difficulty": "easy",
                "rewards": {"xp": 100, "coins": 50},
                "objectives": [
                    {
                        "id": "hack_3_times",
                        "description": "Hack 3 systèmes",
                        "target": 3,
                        "current": 0,
                    },
                ],
                "expires_at": "end_of_day",
            },
            "luna_chat": {
                "id": "luna_chat",
                "title": "Conversation avec LUNA",
                "description": "Parle avec LUNA 5 fois aujourd'hui",
                "type": "daily",
                "difficulty": "easy",
                "rewards": {"xp": 75, "luna_relationship": 10},
                "objectives": [
                    {
                        "id": "chat_5_times",
                        "description": "Parle avec LUNA 5 fois",
                        "target": 5,
                        "current": 0,
                    },
                ],
                "expires_at": "end_of_day",
            },
        }

        # Missions hebdomadaires
        self.weekly_missions = {
            "weekly_challenge": {
                "id": "weekly_challenge",
                "title": "Défi Hebdomadaire",
                "description": "Complète 10 missions cette semaine",
                "type": "weekly",
                "difficulty": "medium",
                "rewards": {"xp": 500, "badges": ["weekly_warrior"]},
                "objectives": [
                    {
                        "id": "complete_10_missions",
                        "description": "Complète 10 missions",
                        "target": 10,
                        "current": 0,
                    },
                ],
                "expires_at": "end_of_week",
            },
        }

    def get_available_missions(self, player_id: str) -> dict[str, list[dict[str, Any]]]:
        """Retourne les missions disponibles pour un joueur"""
        available = {
            "main_missions": [],
            "daily_missions": [],
            "weekly_missions": [],
            "special_events": [],
        }

        # Missions principales
        for _mission_id, mission in self.missions.items():
            if self._check_mission_availability(player_id, mission):
                available["main_missions"].append(self._format_mission(mission))

        # Missions quotidiennes
        for _mission_id, mission in self.daily_missions.items():
            if self._check_daily_mission_availability(player_id, mission):
                available["daily_missions"].append(self._format_mission(mission))

        # Missions hebdomadaires
        for _mission_id, mission in self.weekly_missions.items():
            if self._check_weekly_mission_availability(player_id, mission):
                available["weekly_missions"].append(self._format_mission(mission))

        return available

    def _check_mission_availability(self, player_id: str, mission: dict[str, Any]) -> bool:
        """Vérifie si une mission est disponible pour un joueur"""
        # Vérifier les prérequis
        prerequisites = mission.get("prerequisites", [])
        for prereq in prerequisites:
            if not self._check_prerequisite(player_id, prereq):
                return False

        # Vérifier les conditions de déverrouillage
        unlock_conditions = mission.get("unlock_conditions", [])
        for condition in unlock_conditions:
            if not self._check_unlock_condition(player_id, condition):
                return False

        return True

    def _check_daily_mission_availability(self, player_id: str, mission: dict[str, Any]) -> bool:
        """Vérifie si une mission quotidienne est disponible"""
        # Vérifier si la mission n'a pas déjà été complétée aujourd'hui
        today = datetime.now().date().isoformat()
        player_progress = self.player_progress.get(player_id, {})
        completed_today = player_progress.get("daily_completed", {}).get(mission["id"], [])

        return today not in completed_today

    def _check_weekly_mission_availability(self, player_id: str, mission: dict[str, Any]) -> bool:
        """Vérifie si une mission hebdomadaire est disponible"""
        # Vérifier si la mission n'a pas déjà été complétée cette semaine
        this_week = datetime.now().isocalendar()[1]
        player_progress = self.player_progress.get(player_id, {})
        completed_this_week = player_progress.get("weekly_completed", {}).get(mission["id"], [])

        return this_week not in completed_this_week

    def _check_prerequisite(self, player_id: str, prereq: str) -> bool:
        """Vérifie un prérequis"""
        # Logique simplifiée - à intégrer avec le système de missions principal
        return True

    def _check_unlock_condition(self, player_id: str, condition: str) -> bool:
        """Vérifie une condition de déverrouillage"""
        # Logique simplifiée - à intégrer avec le système de progression
        if condition == "level_2_reached":
            return True  # Valeur par défaut
        if condition == "acte_2_completed" or condition == "level_5_reached" or condition == "security_interest_detected" or condition == "world_access_granted" or condition == "acte_3_completed":
            return True

        return True

    def _format_mission(self, mission: dict[str, Any]) -> dict[str, Any]:
        """Formate une mission pour l'affichage"""
        return {
            "id": mission["id"],
            "title": mission["title"],
            "description": mission["description"],
            "type": mission["type"],
            "difficulty": mission["difficulty"],
            "category": mission.get("category", "general"),
            "rewards": mission.get("rewards", {}),
            "objectives": mission.get("objectives", []),
            "progress": self._calculate_mission_progress(mission),
            "estimated_time": self._estimate_mission_time(mission),
        }

    def _calculate_mission_progress(self, mission: dict[str, Any]) -> dict[str, Any]:
        """Calcule la progression d'une mission"""
        objectives = mission.get("objectives", [])
        if not objectives:
            return {"percentage": 0, "completed": 0, "total": 0}

        completed = sum(1 for obj in objectives if obj.get("completed", False))
        total = len(objectives)
        percentage = (completed / total) * 100 if total > 0 else 0

        return {"percentage": percentage, "completed": completed, "total": total}

    def _estimate_mission_time(self, mission: dict[str, Any]) -> int:
        """Estime le temps nécessaire pour compléter une mission (en minutes)"""
        difficulty_times = {"easy": 5, "medium": 15, "hard": 30}

        base_time = difficulty_times.get(mission.get("difficulty", "medium"), 15)
        objective_count = len(mission.get("objectives", []))

        return base_time + (objective_count * 2)

    def start_mission(self, player_id: str, mission_id: str) -> dict[str, Any]:
        """Démarre une mission secondaire"""
        # Trouver la mission
        mission = None
        mission_type = None

        if mission_id in self.missions:
            mission = self.missions[mission_id]
            mission_type = "main"
        elif mission_id in self.daily_missions:
            mission = self.daily_missions[mission_id]
            mission_type = "daily"
        elif mission_id in self.weekly_missions:
            mission = self.weekly_missions[mission_id]
            mission_type = "weekly"

        if not mission:
            return {"error": "Mission introuvable"}

        # Vérifier la disponibilité
        if not self._check_mission_availability(player_id, mission):
            return {"error": "Mission non disponible"}

        # Initialiser la progression
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {
                "active_missions": {},
                "completed_missions": [],
                "daily_completed": {},
                "weekly_completed": {},
            }

        # Démarrer la mission
        self.player_progress[player_id]["active_missions"][mission_id] = {
            "start_time": datetime.now().isoformat(),
            "objectives": mission["objectives"].copy(),
            "type": mission_type,
        }

        return {
            "success": True,
            "mission": self._format_mission(mission),
            "message": f"Mission '{mission['title']}' démarrée !",
        }

    def update_mission_progress(
        self, player_id: str, mission_id: str, objective_id: str, completed: bool = True,
    ) -> dict[str, Any]:
        """Met à jour la progression d'une mission"""
        if player_id not in self.player_progress:
            return {"error": "Aucune progression trouvée pour ce joueur"}

        active_missions = self.player_progress[player_id]["active_missions"]
        if mission_id not in active_missions:
            return {"error": "Mission non active"}

        mission_progress = active_missions[mission_id]
        objectives = mission_progress["objectives"]

        # Trouver et mettre à jour l'objectif
        for obj in objectives:
            if obj["id"] == objective_id:
                obj["completed"] = completed
                break

        # Vérifier si la mission est terminée
        all_completed = all(obj.get("completed", False) for obj in objectives)

        if all_completed:
            # Mission terminée
            self._complete_mission(player_id, mission_id, mission_progress)

            return {
                "success": True,
                "mission_completed": True,
                "rewards": self._calculate_rewards(player_id, mission_id),
                "message": "Mission terminée ! Félicitations !",
            }
        return {
            "success": True,
            "mission_completed": False,
            "progress": self._calculate_mission_progress({"objectives": objectives}),
            "message": "Progression mise à jour !",
        }

    def _complete_mission(
        self, player_id: str, mission_id: str, mission_progress: dict[str, Any],
    ) -> None:
        """Marque une mission comme terminée"""
        # Ajouter aux missions complétées
        self.player_progress[player_id]["completed_missions"].append(
            {
                "mission_id": mission_id,
                "completed_at": datetime.now().isoformat(),
                "type": mission_progress["type"],
            },
        )

        # Retirer des missions actives
        del self.player_progress[player_id]["active_missions"][mission_id]

        # Marquer comme complétée selon le type
        mission_type = mission_progress["type"]
        if mission_type == "daily":
            today = datetime.now().date().isoformat()
            if mission_id not in self.player_progress[player_id]["daily_completed"]:
                self.player_progress[player_id]["daily_completed"][mission_id] = []
            self.player_progress[player_id]["daily_completed"][mission_id].append(today)
        elif mission_type == "weekly":
            this_week = datetime.now().isocalendar()[1]
            if mission_id not in self.player_progress[player_id]["weekly_completed"]:
                self.player_progress[player_id]["weekly_completed"][mission_id] = []
            self.player_progress[player_id]["weekly_completed"][mission_id].append(this_week)

    def _calculate_rewards(self, player_id: str, mission_id: str) -> dict[str, Any]:
        """Calcule les récompenses d'une mission"""
        # Trouver la mission
        mission = None
        if mission_id in self.missions:
            mission = self.missions[mission_id]
        elif mission_id in self.daily_missions:
            mission = self.daily_missions[mission_id]
        elif mission_id in self.weekly_missions:
            mission = self.weekly_missions[mission_id]

        if not mission:
            return {}

        return mission.get("rewards", {})

    def get_player_progress(self, player_id: str) -> dict[str, Any]:
        """Retourne la progression d'un joueur"""
        if player_id not in self.player_progress:
            return {
                "active_missions": {},
                "completed_missions": [],
                "daily_completed": {},
                "weekly_completed": {},
            }

        return self.player_progress[player_id]

    def generate_daily_missions(self) -> None:
        """Génère de nouvelles missions quotidiennes"""
        # Logique pour générer des missions quotidiennes aléatoires
        # À implémenter selon les besoins

    def generate_weekly_missions(self) -> None:
        """Génère de nouvelles missions hebdomadaires"""
        # Logique pour générer des missions hebdomadaires
        # À implémenter selon les besoins

    def save_mission_data(self) -> bool:
        """Sauvegarde les données de missions"""
        try:
            data = {
                "missions": self.missions,
                "daily_missions": self.daily_missions,
                "weekly_missions": self.weekly_missions,
                "special_events": self.special_events,
                "player_progress": self.player_progress,
            }

            with open("data/secondary_missions.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde missions secondaires: {e}")
            return False


# Instance globale
secondary_missions = SecondaryMissions()
