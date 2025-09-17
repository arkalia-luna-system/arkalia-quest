#!/usr/bin/env python3
"""
🌳 NARRATIVE BRANCHES - ARKALIA QUEST
====================================

Système de branches narratives avec choix influençant l'histoire
et conséquences à long terme pour une expérience immersive.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class NarrativeBranches:
    """Gestionnaire des branches narratives et choix influençant l'histoire"""

    def __init__(self):
        self.branches = {}
        self.player_choices = {}
        self.consequences = {}
        self.story_states = {}
        self.character_relationships = {}

        # Charger les données de branches
        self.load_branch_data()

    def load_branch_data(self) -> None:
        """Charge les données de branches narratives"""
        try:
            with open("data/narrative_branches.json", encoding="utf-8") as f:
                data = json.load(f)
                # Gérer la structure imbriquée du fichier JSON
                if "branches" in data and isinstance(data["branches"], dict):
                    branches_data = data["branches"]
                    # Vérifier s'il y a une autre couche d'imbrication
                    if "branches" in branches_data and isinstance(branches_data["branches"], dict):
                        self.branches = branches_data["branches"]
                    else:
                        self.branches = branches_data
                else:
                    self.branches = data
        except FileNotFoundError:
            logger.info("Fichier de branches non trouvé, création des données par défaut")
            self._create_default_branches()
        except Exception as e:
            logger.error(f"Erreur chargement branches: {e}")
            self._create_default_branches()

    def _create_default_branches(self) -> None:
        """Crée les branches narratives par défaut"""
        self.branches = {
            "prologue_choice": {
                "id": "prologue_choice",
                "title": "Premier contact avec LUNA",
                "description": "Comment veux-tu interagir avec LUNA lors de votre première rencontre ?",
                "context": "Tu viens de découvrir le SOS d'Althea et LUNA s'éveille dans ton terminal.",
                "choices": [
                    {
                        "id": "friendly",
                        "text": "🌙 Salut LUNA ! Je suis là pour t'aider !",
                        "consequence": "luna_friendly",
                        "effects": {
                            "luna_relationship": 20,
                            "trust_level": "high",
                            "unlock_branch": "luna_trust_path",
                        },
                    },
                    {
                        "id": "cautious",
                        "text": "🤔 Attends... qui es-tu exactement ?",
                        "consequence": "luna_cautious",
                        "effects": {
                            "luna_relationship": 5,
                            "trust_level": "medium",
                            "unlock_branch": "luna_suspicion_path",
                        },
                    },
                    {
                        "id": "aggressive",
                        "text": "⚠️ Je ne fais confiance à aucune IA !",
                        "consequence": "luna_aggressive",
                        "effects": {
                            "luna_relationship": -10,
                            "trust_level": "low",
                            "unlock_branch": "luna_conflict_path",
                        },
                    },
                ],
                "required_mission": "prologue",
                "unlock_conditions": ["luna_contact_completed"],
            },
            "acte_1_approach": {
                "id": "acte_1_approach",
                "title": "Approche pour réparer le site de LUNA",
                "description": "Comment veux-tu procéder pour réparer le site web compromis ?",
                "context": "Le site de LUNA a été hacké par La Corp. Tu dois choisir ta stratégie.",
                "choices": [
                    {
                        "id": "stealth",
                        "text": "🥷 Approche furtive - Infiltration silencieuse",
                        "consequence": "stealth_approach",
                        "effects": {
                            "skill_points": {"stealth": 15, "hacking": 10},
                            "unlock_mission": "stealth_missions",
                            "character_trait": "stealthy",
                        },
                    },
                    {
                        "id": "direct",
                        "text": "💥 Approche directe - Attaque frontale",
                        "consequence": "direct_approach",
                        "effects": {
                            "skill_points": {"combat": 15, "hacking": 5},
                            "unlock_mission": "combat_missions",
                            "character_trait": "aggressive",
                        },
                    },
                    {
                        "id": "diplomatic",
                        "text": "🤝 Approche diplomatique - Négociation",
                        "consequence": "diplomatic_approach",
                        "effects": {
                            "skill_points": {"charisma": 15, "intelligence": 10},
                            "unlock_mission": "diplomatic_missions",
                            "character_trait": "diplomatic",
                        },
                    },
                ],
                "required_mission": "acte_1",
                "unlock_conditions": ["prologue_completed"],
            },
            "luna_relationship_crisis": {
                "id": "luna_relationship_crisis",
                "title": "Crise de confiance avec LUNA",
                "description": "LUNA a caché des informations importantes. Comment réagis-tu ?",
                "context": "Tu découvres que LUNA connaissait l'existence de PANDORA depuis le début.",
                "choices": [
                    {
                        "id": "forgive",
                        "text": "💔 Je comprends, tu avais tes raisons...",
                        "consequence": "luna_forgiven",
                        "effects": {
                            "luna_relationship": 30,
                            "story_path": "redemption_arc",
                            "unlock_ending": "united_ending",
                        },
                    },
                    {
                        "id": "confront",
                        "text": "😡 Tu m'as menti ! Comment puis-je te faire confiance ?",
                        "consequence": "luna_confronted",
                        "effects": {
                            "luna_relationship": -20,
                            "story_path": "conflict_arc",
                            "unlock_ending": "tragic_ending",
                        },
                    },
                    {
                        "id": "analyze",
                        "text": "🧠 Laisse-moi analyser la situation...",
                        "consequence": "luna_analyzed",
                        "effects": {
                            "luna_relationship": 10,
                            "story_path": "logical_arc",
                            "unlock_ending": "logical_ending",
                        },
                    },
                ],
                "required_mission": "acte_4",
                "unlock_conditions": [
                    "luna_relationship_high",
                    "trust_issues_detected",
                ],
            },
        }

    def make_choice(
        self,
        player_id: str,
        branch_id: str,
        choice_id: str,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Enregistre un choix du joueur et retourne les conséquences"""

        if branch_id not in self.branches:
            return {"error": "Branche narrative introuvable"}

        branch = self.branches[branch_id]

        # Vérifier les conditions de déverrouillage
        if not self._check_unlock_conditions(player_id, branch):
            return {"error": "Conditions de déverrouillage non satisfaites"}

        # Trouver le choix
        choice = None
        for c in branch["choices"]:
            if c["id"] == choice_id:
                choice = c
                break

        if not choice:
            return {"error": "Choix introuvable"}

        # Enregistrer le choix
        choice_key = f"{player_id}_{branch_id}"
        if choice_key not in self.player_choices:
            self.player_choices[choice_key] = []

        choice_record = {
            "branch_id": branch_id,
            "choice_id": choice_id,
            "choice_text": choice["text"],
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
        }

        self.player_choices[choice_key].append(choice_record)

        # Appliquer les conséquences
        consequences = self._apply_consequences(player_id, choice, branch)

        # Mettre à jour l'état de l'histoire
        self._update_story_state(player_id, branch_id, choice_id, consequences)

        # Générer la réponse narrative
        narrative_response = self._generate_narrative_response(branch, choice, consequences)

        return {
            "success": True,
            "choice_made": choice_record,
            "consequences": consequences,
            "narrative_response": narrative_response,
            "unlocked_branches": self._check_new_unlocked_branches(player_id),
            "story_state": self.story_states.get(player_id, {}),
        }

    def _check_unlock_conditions(self, player_id: str, branch: dict[str, Any]) -> bool:
        """Vérifie si les conditions de déverrouillage sont satisfaites"""
        conditions = branch.get("unlock_conditions", [])

        for condition in conditions:
            if not self._evaluate_condition(player_id, condition):
                return False

        return True

    def _evaluate_condition(self, player_id: str, condition: str) -> bool:
        """Évalue une condition de déverrouillage"""
        # Logique simplifiée - à étendre selon les besoins
        if condition == "luna_contact_completed":
            return self._has_completed_mission(player_id, "luna_contact")
        if condition == "prologue_completed":
            return self._has_completed_mission(player_id, "prologue")
        if condition == "luna_relationship_high":
            return self._get_luna_relationship(player_id) > 50
        if condition == "trust_issues_detected":
            return self._has_trust_issues(player_id)

        return True  # Condition par défaut

    def _has_completed_mission(self, player_id: str, mission_id: str) -> bool:
        """Vérifie si une mission a été complétée"""
        # Vérifier dans l'état de l'histoire du joueur
        story_state = self.story_states.get(player_id, {})
        completed_events = story_state.get("completed_events", [])
        return f"{mission_id}_completed" in completed_events or mission_id in completed_events

    def _get_luna_relationship(self, player_id: str) -> int:
        """Retourne le niveau de relation avec LUNA"""
        return self.character_relationships.get(player_id, {}).get("luna", 0)

    def _has_trust_issues(self, player_id: str) -> bool:
        """Vérifie s'il y a des problèmes de confiance"""
        return self.character_relationships.get(player_id, {}).get("trust_issues", False)

    def _apply_consequences(
        self,
        player_id: str,
        choice: dict[str, Any],
        branch: dict[str, Any],
    ) -> dict[str, Any]:
        """Applique les conséquences d'un choix"""
        consequences = choice.get("effects", {})

        # Mettre à jour les relations
        if "luna_relationship" in consequences:
            self._update_luna_relationship(player_id, consequences["luna_relationship"])

        # Mettre à jour les compétences
        if "skill_points" in consequences:
            self._update_skills(player_id, consequences["skill_points"])

        # Mettre à jour les traits de caractère
        if "character_trait" in consequences:
            self._update_character_trait(player_id, consequences["character_trait"])

        # Enregistrer les conséquences
        consequence_key = f"{player_id}_{branch['id']}_{choice['id']}"
        self.consequences[consequence_key] = {
            "player_id": player_id,
            "branch_id": branch["id"],
            "choice_id": choice["id"],
            "consequences": consequences,
            "timestamp": datetime.now().isoformat(),
        }

        return consequences

    def _update_luna_relationship(self, player_id: str, change: int) -> None:
        """Met à jour la relation avec LUNA"""
        if player_id not in self.character_relationships:
            self.character_relationships[player_id] = {}

        current = self.character_relationships[player_id].get("luna", 0)
        self.character_relationships[player_id]["luna"] = max(0, min(100, current + change))

    def _update_skills(self, player_id: str, skill_changes: dict[str, int]) -> None:
        """Met à jour les compétences du joueur"""
        if player_id not in self.character_relationships:
            self.character_relationships[player_id] = {}

        if "skills" not in self.character_relationships[player_id]:
            self.character_relationships[player_id]["skills"] = {}

        for skill, change in skill_changes.items():
            current = self.character_relationships[player_id]["skills"].get(skill, 0)
            self.character_relationships[player_id]["skills"][skill] = max(0, current + change)

    def _update_character_trait(self, player_id: str, trait: str) -> None:
        """Met à jour les traits de caractère"""
        if player_id not in self.character_relationships:
            self.character_relationships[player_id] = {}

        if "traits" not in self.character_relationships[player_id]:
            self.character_relationships[player_id]["traits"] = []

        if trait not in self.character_relationships[player_id]["traits"]:
            self.character_relationships[player_id]["traits"].append(trait)

    def _update_story_state(
        self,
        player_id: str,
        branch_id: str,
        choice_id: str,
        consequences: dict[str, Any],
    ) -> None:
        """Met à jour l'état de l'histoire du joueur"""
        if player_id not in self.story_states:
            self.story_states[player_id] = {
                "branches_completed": [],
                "story_path": "default",
                "character_arc": "neutral",
                "unlocked_endings": [],
                "major_choices": [],
            }

        story_state = self.story_states[player_id]
        story_state["branches_completed"].append(branch_id)
        story_state["major_choices"].append(
            {
                "branch_id": branch_id,
                "choice_id": choice_id,
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Mettre à jour le chemin narratif
        if "story_path" in consequences:
            story_state["story_path"] = consequences["story_path"]

        # Mettre à jour l'arc de caractère
        if "character_trait" in consequences:
            story_state["character_arc"] = consequences["character_trait"]

        # Débloquer des fins
        if "unlock_ending" in consequences:
            ending = consequences["unlock_ending"]
            if ending not in story_state["unlocked_endings"]:
                story_state["unlocked_endings"].append(ending)

    def _generate_narrative_response(
        self,
        branch: dict[str, Any],
        choice: dict[str, Any],
        consequences: dict[str, Any],
    ) -> dict[str, Any]:
        """Génère une réponse narrative basée sur le choix"""

        response_templates = {
            "luna_friendly": {
                "title": "🌙 LUNA réagit positivement",
                "message": "LUNA semble ravie de ta réaction amicale. Elle te fait confiance et se sent plus à l'aise pour partager ses secrets.",
                "luna_dialogue": "Merci pour ta confiance, hacker. Ensemble, nous allons sauver l'humanité !",
                "visual_effect": "luna_happy_glow",
            },
            "luna_cautious": {
                "title": "🤔 LUNA comprend ta prudence",
                "message": "LUNA respecte ta méfiance. Elle comprend que la confiance se mérite et se montre plus réservée.",
                "luna_dialogue": "Je comprends ta prudence. Le temps nous dira si nous pouvons nous faire confiance.",
                "visual_effect": "luna_neutral",
            },
            "luna_aggressive": {
                "title": "⚠️ Tension avec LUNA",
                "message": "LUNA semble blessée par ton agressivité. La relation devient tendue et elle se ferme.",
                "luna_dialogue": "Si tu ne veux pas de mon aide, je ne peux rien faire pour toi...",
                "visual_effect": "luna_sad_shake",
            },
            "stealth_approach": {
                "title": "🥷 Approche furtive choisie",
                "message": "Tu décides d'infiltrer silencieusement le système. Tes compétences de furtivité s'améliorent.",
                "luna_dialogue": "Excellente stratégie ! La discrétion est souvent plus efficace que la force brute.",
                "visual_effect": "stealth_mode_activation",
            },
            "direct_approach": {
                "title": "💥 Approche directe choisie",
                "message": "Tu choisis l'attaque frontale. Tes compétences de combat s'améliorent.",
                "luna_dialogue": "Audacieux ! Parfois, la force brute peut être la solution.",
                "visual_effect": "combat_mode_activation",
            },
            "diplomatic_approach": {
                "title": "🤝 Approche diplomatique choisie",
                "message": "Tu optes pour la négociation. Tes compétences sociales s'améliorent.",
                "luna_dialogue": "Sage décision ! Les mots peuvent être plus puissants que les armes.",
                "visual_effect": "diplomatic_aura",
            },
        }

        consequence_id = choice.get("consequence", "default")
        return response_templates.get(
            consequence_id,
            {
                "title": "Choix enregistré",
                "message": "Ton choix a été pris en compte et influencera l'histoire.",
                "luna_dialogue": "Intéressant... Je vois où tu veux en venir.",
                "visual_effect": "choice_confirmed",
            },
        )

    def _check_new_unlocked_branches(self, player_id: str) -> list[dict[str, Any]]:
        """Vérifie les nouvelles branches débloquées"""
        unlocked = []

        for branch_id, branch in self.branches.items():
            if branch_id not in self.story_states.get(player_id, {}).get("branches_completed", []):
                if self._check_unlock_conditions(player_id, branch):
                    unlocked.append(
                        {
                            "branch_id": branch_id,
                            "title": branch["title"],
                            "description": branch["description"],
                        },
                    )

        return unlocked

    def get_available_branches(self, player_id: str) -> list[dict[str, Any]]:
        """Retourne les branches disponibles pour un joueur"""
        available = []

        for branch_id, branch in self.branches.items():
            if self._check_unlock_conditions(player_id, branch):
                available.append(
                    {
                        "id": branch_id,
                        "title": branch["title"],
                        "description": branch["description"],
                        "context": branch.get("context", ""),
                        "choices": [
                            {
                                "id": choice["id"],
                                "text": choice["text"],
                                "preview": choice.get("preview", ""),
                            }
                            for choice in branch["choices"]
                        ],
                    },
                )

        return available

    def get_story_state(self, player_id: str) -> dict[str, Any]:
        """Retourne l'état de l'histoire d'un joueur"""
        return self.story_states.get(
            player_id,
            {
                "branches_completed": [],
                "story_path": "default",
                "character_arc": "neutral",
                "unlocked_endings": [],
                "major_choices": [],
            },
        )

    def get_character_relationships(self, player_id: str) -> dict[str, Any]:
        """Retourne les relations du personnage"""
        return self.character_relationships.get(
            player_id,
            {"luna": 0, "skills": {}, "traits": [], "trust_issues": False},
        )

    def save_branch_data(self) -> bool:
        """Sauvegarde les données de branches"""
        try:
            data = {
                "branches": self.branches,
                "player_choices": self.player_choices,
                "consequences": self.consequences,
                "story_states": self.story_states,
                "character_relationships": self.character_relationships,
            }

            with open("data/narrative_branches.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde branches: {e}")
            return False


# Instance globale
narrative_branches = NarrativeBranches()
