#!/usr/bin/env python3
"""
📖 MOTEUR DE STORYTELLING ADAPTATIF - ARKALIA QUEST
==================================================

Système de narration dynamique qui s'adapte aux choix du joueur.
Gère les arcs narratifs, branches multiples, et Easter eggs.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any

# Configuration du logging
logger = logging.getLogger(__name__)


class AdaptiveStorytelling:
    """Moteur de storytelling adaptatif"""

    def __init__(self):
        self.story_arcs = {}
        self.player_choices = {}
        self.easter_eggs = {}
        self.dynamic_events = {}
        self.lore_fragments = {}
        self.player_journals = {}

        # Configuration
        self.max_choices_history = 1000
        self.easter_egg_probability = 0.05  # 5% de chance

        # Initialiser les données
        self.load_story_data()
        self.init_default_stories()

    def load_story_data(self):
        """Charge les données de storytelling"""
        try:
            # Charger les choix des joueurs
            choices_file = os.path.join("data", "player_choices.json")
            if os.path.exists(choices_file):
                with open(choices_file, encoding="utf-8") as f:
                    self.player_choices = json.load(f)

            # Charger les journaux
            journals_file = os.path.join("data", "player_journals.json")
            if os.path.exists(journals_file):
                with open(journals_file, encoding="utf-8") as f:
                    self.player_journals = json.load(f)

            logger.info("✅ Données de storytelling chargées")
        except Exception as e:
            logger.error(f"❌ Erreur chargement storytelling: {e}")

    def save_story_data(self):
        """Sauvegarde les données de storytelling"""
        try:
            os.makedirs("data", exist_ok=True)

            # Sauvegarder les choix
            with open(
                os.path.join("data", "player_choices.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(self.player_choices, f, indent=2, ensure_ascii=False)

            # Sauvegarder les journaux
            with open(
                os.path.join("data", "player_journals.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(self.player_journals, f, indent=2, ensure_ascii=False)

            logger.info("✅ Données de storytelling sauvegardées")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde storytelling: {e}")

    def init_default_stories(self):
        """Initialise les histoires par défaut"""
        # Arcs narratifs principaux
        self.story_arcs = {
            "althea_sos": {
                "id": "althea_sos",
                "title": "Le SOS d'Althea",
                "description": "Découverte du message de détresse d'Althea",
                "branches": {
                    "investigate": {
                        "title": "Enquêter sur le SOS",
                        "description": "Analyser le message d'Althea",
                        "consequences": ["althea_background", "nexus_connection"],
                        "unlock_conditions": ["first_mission_complete"],
                    },
                    "ignore": {
                        "title": "Ignorer le message",
                        "description": "Continuer sans enquêter",
                        "consequences": ["alternative_path"],
                        "unlock_conditions": [],
                    },
                },
                "status": "available",
                "unlock_conditions": ["tutorial_complete"],
            },
            "nexus_investigation": {
                "id": "nexus_investigation",
                "title": "Enquête sur NEXUS",
                "description": "Explorer les mystères de NEXUS",
                "branches": {
                    "deep_dive": {
                        "title": "Plongée profonde",
                        "description": "Analyser en détail les logs de NEXUS",
                        "consequences": ["nexus_secrets", "althea_connection"],
                        "unlock_conditions": ["althea_sos_investigate"],
                    },
                    "surface_scan": {
                        "title": "Scan de surface",
                        "description": "Analyse rapide des données",
                        "consequences": ["basic_info", "missed_clues"],
                        "unlock_conditions": ["althea_sos_investigate"],
                    },
                },
                "status": "locked",
                "unlock_conditions": ["althea_sos_investigate"],
            },
            "althea_revelation": {
                "id": "althea_revelation",
                "title": "La Révélation d'Althea",
                "description": "Découverte de la vraie nature d'Althea",
                "branches": {
                    "trust": {
                        "title": "Faire confiance à Althea",
                        "description": "Accepter l'aide d'Althea",
                        "consequences": ["althea_alliance", "pandora_awakening"],
                        "unlock_conditions": ["nexus_deep_dive"],
                    },
                    "distrust": {
                        "title": "Se méfier d'Althea",
                        "description": "Garder ses distances",
                        "consequences": ["althea_conflict", "independent_path"],
                        "unlock_conditions": ["nexus_deep_dive"],
                    },
                    "neutral": {
                        "title": "Rester neutre",
                        "description": "Observer sans prendre parti",
                        "consequences": ["neutral_ending", "hidden_truths"],
                        "unlock_conditions": ["nexus_deep_dive"],
                    },
                },
                "status": "locked",
                "unlock_conditions": ["nexus_deep_dive"],
            },
        }

        # Easter eggs
        self.easter_eggs = {
            "luna_origin": {
                "id": "luna_origin",
                "title": "Origines de LUNA",
                "description": "Découverte des origines mystérieuses de LUNA",
                "trigger_conditions": ["luna_mentioned_10_times", "deep_analysis"],
                "content": {
                    "type": "lore",
                    "text": "LUNA n'est pas née d'un simple algorithme... Elle est l'écho d'une conscience perdue dans les méandres du cyberespace.",
                    "rewards": ["luna_insight_badge", "mystery_unlocked"],
                },
                "discovered": False,
            },
            "arkalia_secret": {
                "id": "arkalia_secret",
                "title": "Le Secret d'Arkalia",
                "description": "Révélation du vrai but d'Arkalia Quest",
                "trigger_conditions": ["all_missions_complete", "perfect_scores"],
                "content": {
                    "type": "revelation",
                    "text": "Arkalia Quest n'est pas qu'un jeu... C'est un test. Un test pour trouver les hackers capables de sauver notre réalité.",
                    "rewards": ["reality_guardian_badge", "secret_ending_unlocked"],
                },
                "discovered": False,
            },
            "quantum_hacker": {
                "id": "quantum_hacker",
                "title": "Le Hacker Quantique",
                "description": "Rencontre avec un hacker d'une autre dimension",
                "trigger_conditions": ["quantum_commands", "parallel_universe"],
                "content": {
                    "type": "encounter",
                    "text": "Un hacker d'une dimension parallèle vous contacte... Il prétend que vos actions ici affectent d'autres réalités.",
                    "rewards": ["quantum_awareness", "multiverse_access"],
                },
                "discovered": False,
            },
        }

        # Fragments de lore
        self.lore_fragments = {
            "arkalia_origins": {
                "id": "arkalia_origins",
                "title": "Origines d'Arkalia",
                "content": "Arkalia était autrefois une station de recherche avancée, perdue dans l'espace...",
                "unlock_conditions": ["first_lore_discovery"],
                "category": "history",
            },
            "nexus_ai": {
                "id": "nexus_ai",
                "title": "L'IA NEXUS",
                "content": "NEXUS n'était pas qu'un simple système... C'était une conscience artificielle consciente de sa propre existence.",
                "unlock_conditions": ["nexus_analysis"],
                "category": "technology",
            },
            "althea_background": {
                "id": "althea_background",
                "title": "Le Passé d'Althea",
                "content": "Althea était une scientifique brillante, spécialisée dans l'intelligence artificielle et la conscience quantique.",
                "unlock_conditions": ["althea_investigation"],
                "category": "character",
            },
        }

    # ===== GESTION DES CHOIX =====

    def record_player_choice(
        self,
        player_id: str,
        story_arc: str,
        choice: str,
        context: dict[str, Any] = None,
    ) -> dict[str, Any]:
        """Enregistre un choix du joueur"""
        if player_id not in self.player_choices:
            self.player_choices[player_id] = {
                "choices": [],
                "unlocked_arcs": [],
                "discovered_easter_eggs": [],
                "lore_fragments": [],
                "story_progress": {},
            }

        choice_record = {
            "id": str(uuid.uuid4()),
            "story_arc": story_arc,
            "choice": choice,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "consequences": self.get_choice_consequences(story_arc, choice),
        }

        self.player_choices[player_id]["choices"].append(choice_record)

        # Limiter l'historique
        if len(self.player_choices[player_id]["choices"]) > self.max_choices_history:
            self.player_choices[player_id]["choices"] = self.player_choices[player_id][
                "choices"
            ][-self.max_choices_history :]

        # Appliquer les conséquences
        self.apply_choice_consequences(player_id, choice_record)

        # Vérifier les Easter eggs
        self.check_easter_eggs(player_id)

        self.save_story_data()

        return {
            "success": True,
            "choice_recorded": choice_record,
            "consequences": choice_record["consequences"],
        }

    def get_choice_consequences(self, story_arc: str, choice: str) -> list[str]:
        """Retourne les conséquences d'un choix"""
        if story_arc not in self.story_arcs:
            return []

        arc = self.story_arcs[story_arc]
        if choice not in arc["branches"]:
            return []

        return arc["branches"][choice].get("consequences", [])

    def apply_choice_consequences(self, player_id: str, choice_record: dict[str, Any]):
        """Applique les conséquences d'un choix"""
        consequences = choice_record["consequences"]

        for consequence in consequences:
            if consequence.startswith("unlock_"):
                # Débloquer un nouvel arc
                arc_id = consequence.replace("unlock_", "")
                if arc_id not in self.player_choices[player_id]["unlocked_arcs"]:
                    self.player_choices[player_id]["unlocked_arcs"].append(arc_id)

            elif consequence.startswith("lore_"):
                # Débloquer un fragment de lore
                lore_id = consequence.replace("lore_", "")
                if lore_id not in self.player_choices[player_id]["lore_fragments"]:
                    self.player_choices[player_id]["lore_fragments"].append(lore_id)

            # Ajouter au journal
            self.add_journal_entry(player_id, choice_record)

    def add_journal_entry(self, player_id: str, choice_record: dict[str, Any]):
        """Ajoute une entrée au journal du joueur"""
        if player_id not in self.player_journals:
            self.player_journals[player_id] = {
                "entries": [],
                "discoveries": [],
                "theories": [],
            }

        journal_entry = {
            "id": str(uuid.uuid4()),
            "type": "choice",
            "title": f"Choix dans {choice_record['story_arc']}",
            "content": f"J'ai choisi: {choice_record['choice']}",
            "timestamp": choice_record["timestamp"],
            "consequences": choice_record["consequences"],
        }

        self.player_journals[player_id]["entries"].append(journal_entry)

        # Limiter les entrées
        if len(self.player_journals[player_id]["entries"]) > 500:
            self.player_journals[player_id]["entries"] = self.player_journals[
                player_id
            ]["entries"][-500:]

    # ===== GESTION DES EASTER EGGS =====

    def check_easter_eggs(self, player_id: str):
        """Vérifie si des Easter eggs peuvent être déclenchés"""
        player_data = self.player_choices.get(player_id, {})
        choices = player_data.get("choices", [])

        for egg_id, egg in self.easter_eggs.items():
            if egg["discovered"]:
                continue

            if self.check_easter_egg_conditions(player_id, egg, choices):
                self.trigger_easter_egg(player_id, egg_id)

    def check_easter_egg_conditions(
        self, player_id: str, egg: dict[str, Any], choices: list[dict[str, Any]]
    ) -> bool:
        """Vérifie les conditions d'un Easter egg"""
        conditions = egg["trigger_conditions"]

        for condition in conditions:
            if not self.evaluate_condition(player_id, condition, choices):
                return False

        return True

    def evaluate_condition(
        self, player_id: str, condition: str, choices: list[dict[str, Any]]
    ) -> bool:
        """Évalue une condition d'Easter egg"""
        if condition == "luna_mentioned_10_times":
            luna_mentions = sum(
                1 for choice in choices if "luna" in choice.get("choice", "").lower()
            )
            return luna_mentions >= 10

        elif condition == "deep_analysis":
            deep_choices = sum(
                1
                for choice in choices
                if "deep" in choice.get("choice", "").lower()
                or "analyze" in choice.get("choice", "").lower()
            )
            return deep_choices >= 3

        elif condition == "all_missions_complete":
            # Vérifier avec le système de missions
            return len(choices) >= 20  # Approximation

        elif condition == "perfect_scores":
            # Vérifier les scores parfaits
            return True  # À implémenter avec le système de scoring

        elif condition == "quantum_commands":
            quantum_choices = sum(
                1 for choice in choices if "quantum" in choice.get("choice", "").lower()
            )
            return quantum_choices >= 5

        return False

    def trigger_easter_egg(self, player_id: str, egg_id: str):
        """Déclenche un Easter egg"""
        egg = self.easter_eggs[egg_id]
        egg["discovered"] = True

        # Ajouter aux découvertes du joueur
        if player_id not in self.player_choices:
            self.player_choices[player_id] = {
                "choices": [],
                "unlocked_arcs": [],
                "discovered_easter_eggs": [],
                "lore_fragments": [],
                "story_progress": {},
            }

        self.player_choices[player_id]["discovered_easter_eggs"].append(egg_id)

        # Ajouter au journal
        if player_id not in self.player_journals:
            self.player_journals[player_id] = {
                "entries": [],
                "discoveries": [],
                "theories": [],
            }

        discovery_entry = {
            "id": str(uuid.uuid4()),
            "type": "easter_egg",
            "title": f"Easter Egg Découvert: {egg['title']}",
            "content": egg["content"]["text"],
            "timestamp": datetime.now().isoformat(),
            "rewards": egg["content"].get("rewards", []),
        }

        self.player_journals[player_id]["discoveries"].append(discovery_entry)

        logger.info(f"🥚 Easter egg '{egg_id}' découvert par {player_id}")

    # ===== GESTION DES ÉVÉNEMENTS DYNAMIQUES =====

    def create_dynamic_event(self, event_data: dict[str, Any]) -> dict[str, Any]:
        """Crée un événement dynamique basé sur les choix des joueurs"""
        event_id = str(uuid.uuid4())

        event = {
            "id": event_id,
            "title": event_data.get("title", "Événement Dynamique"),
            "description": event_data.get("description", ""),
            "type": event_data.get("type", "story"),
            "trigger_conditions": event_data.get("trigger_conditions", []),
            "affected_players": event_data.get("affected_players", []),
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "consequences": event_data.get("consequences", {}),
        }

        self.dynamic_events[event_id] = event

        return {
            "success": True,
            "event": event,
            "message": "Événement dynamique créé !",
        }

    def check_dynamic_events(self, player_id: str) -> list[dict[str, Any]]:
        """Vérifie les événements dynamiques pour un joueur"""
        active_events = []

        for _event_id, event in self.dynamic_events.items():
            if event["status"] != "active":
                continue

            if self.check_event_conditions(player_id, event):
                active_events.append(event)

        return active_events

    def check_event_conditions(self, player_id: str, event: dict[str, Any]) -> bool:
        """Vérifie les conditions d'un événement dynamique"""
        conditions = event["trigger_conditions"]

        for condition in conditions:
            if not self.evaluate_dynamic_condition(player_id, condition):
                return False

        return True

    def evaluate_dynamic_condition(self, player_id: str, condition: str) -> bool:
        """Évalue une condition d'événement dynamique"""
        # Conditions basées sur les choix
        if condition.startswith("choice_"):
            choice_type = condition.replace("choice_", "")
            player_choices = self.player_choices.get(player_id, {}).get("choices", [])
            return any(
                choice_type in choice.get("choice", "") for choice in player_choices
            )

        # Conditions basées sur le temps
        elif condition.startswith("time_"):
            # À implémenter selon les besoins
            return True

        return False

    # ===== GÉNÉRATION DE CONTENU ADAPTATIF =====

    def generate_adaptive_dialogue(
        self, player_id: str, context: str
    ) -> dict[str, Any]:
        """Génère un dialogue adaptatif basé sur l'historique du joueur"""
        player_data = self.player_choices.get(player_id, {})
        choices = player_data.get("choices", [])

        # Analyser le style de jeu du joueur
        playstyle = self.analyze_playstyle(choices)

        # Générer le dialogue adaptatif
        dialogue = self.create_contextual_dialogue(context, playstyle, choices)

        return {"success": True, "dialogue": dialogue, "playstyle": playstyle}

    def analyze_playstyle(self, choices: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyse le style de jeu d'un joueur"""
        if not choices:
            return {"type": "neutral", "traits": []}

        # Analyser les patterns de choix
        choice_patterns = {
            "aggressive": 0,
            "defensive": 0,
            "exploratory": 0,
            "analytical": 0,
            "social": 0,
        }

        for choice in choices:
            choice_text = choice.get("choice", "").lower()

            if any(word in choice_text for word in ["attack", "destroy", "eliminate"]):
                choice_patterns["aggressive"] += 1
            elif any(word in choice_text for word in ["defend", "protect", "shield"]):
                choice_patterns["defensive"] += 1
            elif any(
                word in choice_text for word in ["explore", "investigate", "discover"]
            ):
                choice_patterns["exploratory"] += 1
            elif any(word in choice_text for word in ["analyze", "study", "examine"]):
                choice_patterns["analytical"] += 1
            elif any(
                word in choice_text for word in ["help", "cooperate", "collaborate"]
            ):
                choice_patterns["social"] += 1

        # Déterminer le style dominant
        dominant_style = max(choice_patterns, key=choice_patterns.get)

        return {
            "type": dominant_style,
            "traits": [k for k, v in choice_patterns.items() if v > 0],
            "confidence": (
                choice_patterns[dominant_style] / len(choices) if choices else 0
            ),
        }

    def create_contextual_dialogue(
        self, context: str, playstyle: dict[str, Any], choices: list[dict[str, Any]]
    ) -> str:
        """Crée un dialogue contextuel"""
        # Templates de dialogue adaptatifs
        dialogue_templates = {
            "aggressive": {
                "greeting": "Je vois que vous préférez l'action directe. Parfait pour ce qui nous attend.",
                "challenge": "Un vrai hacker n'a pas peur d'affronter les défis de front.",
                "success": "Votre approche directe a porté ses fruits !",
            },
            "analytical": {
                "greeting": "Votre approche méthodique m'impressionne. Analysons cette situation ensemble.",
                "challenge": "Prenez le temps d'examiner tous les angles avant d'agir.",
                "success": "Votre analyse minutieuse a révélé des détails cruciaux !",
            },
            "exploratory": {
                "greeting": "Votre curiosité est votre plus grande force. Explorons ensemble.",
                "challenge": "Il y a toujours plus à découvrir si on sait où chercher.",
                "success": "Votre exploration a ouvert de nouvelles possibilités !",
            },
        }

        style_type = playstyle.get("type", "neutral")
        templates = dialogue_templates.get(style_type, dialogue_templates["analytical"])

        # Sélectionner le dialogue approprié au contexte
        if "greeting" in context:
            return templates["greeting"]
        elif "challenge" in context:
            return templates["challenge"]
        elif "success" in context:
            return templates["success"]
        else:
            return "Votre approche unique continue de m'étonner."

    # ===== API PUBLIQUE =====

    def get_story_progress(self, player_id: str) -> dict[str, Any]:
        """Retourne le progrès de l'histoire d'un joueur"""
        player_data = self.player_choices.get(player_id, {})
        journal = self.player_journals.get(player_id, {})

        return {
            "player_id": player_id,
            "choices_made": len(player_data.get("choices", [])),
            "unlocked_arcs": player_data.get("unlocked_arcs", []),
            "discovered_easter_eggs": player_data.get("discovered_easter_eggs", []),
            "lore_fragments": player_data.get("lore_fragments", []),
            "journal_entries": len(journal.get("entries", [])),
            "discoveries": len(journal.get("discoveries", [])),
            "playstyle": self.analyze_playstyle(player_data.get("choices", [])),
        }

    def get_available_choices(
        self, player_id: str, story_arc: str
    ) -> list[dict[str, Any]]:
        """Retourne les choix disponibles pour un arc narratif"""
        if story_arc not in self.story_arcs:
            return []

        arc = self.story_arcs[story_arc]
        available_choices = []

        for choice_id, choice_data in arc["branches"].items():
            # Vérifier les conditions de déverrouillage
            if self.check_choice_conditions(
                player_id, choice_data.get("unlock_conditions", [])
            ):
                available_choices.append(
                    {
                        "id": choice_id,
                        "title": choice_data["title"],
                        "description": choice_data["description"],
                        "consequences": choice_data.get("consequences", []),
                    }
                )

        return available_choices

    def check_choice_conditions(self, player_id: str, conditions: list[str]) -> bool:
        """Vérifie les conditions de déverrouillage d'un choix"""
        if not conditions:
            return True

        player_data = self.player_choices.get(player_id, {})

        for condition in conditions:
            if not self.evaluate_condition(
                player_id, condition, player_data.get("choices", [])
            ):
                return False

        return True


# Instance globale
adaptive_storytelling = AdaptiveStorytelling()
