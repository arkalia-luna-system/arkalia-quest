#!/usr/bin/env python3
"""
Mission Handler - Gestionnaire des nouvelles missions Arkalia Quest
Intègre les missions des 7 actes avec le moteur de jeu existant
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional


class MissionHandler:
    """Gestionnaire des missions pour Arkalia Quest"""

    def __init__(self):
        self.missions_path = Path("data/missions")
        self.dialogues_path = Path("data/dialogues_dynamiques.json")
        self.story_path = Path("data/story.json")
        self.missions = {}
        self.dialogues = {}
        self.story = {}
        self.load_all_data()

    def load_all_data(self):
        """Charge toutes les données nécessaires"""
        # Charger les missions (nouvelles missions seulement)
        new_mission_names = [
            "prologue.json",
            "acte_1.json",
            "acte_2.json",
            "acte_3.json",
            "acte_4.json",
            "acte_5.json",
            "acte_6.json",
            "epilogue.json",
        ]

        for mission_file in self.missions_path.glob("*.json"):
            if mission_file.name in new_mission_names:
                try:
                    with open(mission_file, encoding="utf-8") as f:
                        mission_data = json.load(f)
                        self.missions[mission_data["id"]] = mission_data
                except Exception as e:
                    print(f"Erreur chargement {mission_file.name}: {e}")

        # Charger les dialogues
        if self.dialogues_path.exists():
            with open(self.dialogues_path, encoding="utf-8") as f:
                self.dialogues = json.load(f)

        # Charger l'histoire
        if self.story_path.exists():
            with open(self.story_path, encoding="utf-8") as f:
                self.story = json.load(f)

    def get_mission(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une mission par son ID"""
        return self.missions.get(mission_id)

    def get_current_acte(self, profil: Dict[str, Any]) -> str:
        """Détermine l'acte actuel selon la progression du joueur"""
        # Logique pour déterminer l'acte actuel
        # Basé sur les missions complétées, les objets débloqués, etc.
        completed_missions = profil.get("missions_completed", [])

        acte_order = [
            "prologue",
            "acte_1",
            "acte_2",
            "acte_3",
            "acte_4",
            "acte_5",
            "acte_6",
            "epilogue",
        ]

        for acte in acte_order:
            if acte not in completed_missions:
                return acte

        return "epilogue"  # Tous les actes complétés

    def get_dialogue(self, personnage: str, acte: str, contexte: str) -> str:
        """Récupère un dialogue dynamique pour un personnage"""
        try:
            acte_dialogues = self.dialogues["dialogues_par_acte"].get(acte, {})
            personnage_dialogues = acte_dialogues.get(personnage, {})
            contexte_dialogues = personnage_dialogues.get(contexte, [])

            if contexte_dialogues:
                return random.choice(contexte_dialogues)
            else:
                # Dialogue par défaut
                return f"{personnage}: Je n'ai rien à dire pour le moment."
        except Exception:
            return f"{personnage}: ..."

    def get_emotion_reaction(self, personnage: str, emotion: str) -> str:
        """Récupère une réaction émotionnelle"""
        try:
            reactions = self.dialogues["reactions_emotionnelles"].get(personnage, {})
            emotion_reactions = reactions.get(emotion, [])

            if emotion_reactions:
                return random.choice(emotion_reactions)
            else:
                return "..."
        except Exception:
            return "..."

    def execute_mission_step(
        self, mission_id: str, step_id: str, profil: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Exécute une étape de mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {"success": False, "message": "Mission non trouvée"}

        # Trouver l'étape
        step = None
        for s in mission["etapes"]:
            if s["id"] == step_id:
                step = s
                break

        if not step:
            return {"success": False, "message": "Étape non trouvée"}

        # Simuler l'exécution de la commande
        commande = step["commande"]

        # Logique d'exécution selon la commande
        result = self.execute_commande(commande, profil)

        if result["success"]:
            # Ajouter la récompense
            profil["points"] = profil.get("points", 0) + step["recompense"]

            # Marquer l'étape comme complétée
            if "etapes_completed" not in profil:
                profil["etapes_completed"] = {}
            if mission_id not in profil["etapes_completed"]:
                profil["etapes_completed"][mission_id] = []
            profil["etapes_completed"][mission_id].append(step_id)

            # Vérifier si la mission est complétée
            if self.is_mission_completed(mission_id, profil):
                self.complete_mission(mission_id, profil)

        return result

    def execute_commande(self, commande: str, profil: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute une commande de mission"""
        # Simulation des commandes selon le type
        if commande.startswith("luna_"):
            return {
                "success": True,
                "message": "Commande LUNA exécutée",
                "ascii": "luna_contact",
            }
        elif commande.startswith("analyser_"):
            return {"success": True, "message": "Analyse terminée", "ascii": "success"}
        elif commande.startswith("decrypter_"):
            return {"success": True, "message": "Décryptage réussi", "ascii": "success"}
        elif commande.startswith("coder_"):
            return {"success": True, "message": "Code exécuté", "ascii": "success"}
        elif commande.startswith("generer_"):
            return {
                "success": True,
                "message": "Génération terminée",
                "ascii": "success",
            }
        else:
            return {"success": True, "message": f"Commande {commande} exécutée"}

    def is_mission_completed(self, mission_id: str, profil: Dict[str, Any]) -> bool:
        """Vérifie si une mission est complétée"""
        mission = self.get_mission(mission_id)
        if not mission:
            return False

        etapes_completed = profil.get("etapes_completed", {}).get(mission_id, [])
        return len(etapes_completed) >= len(mission["etapes"])

    def complete_mission(self, mission_id: str, profil: Dict[str, Any]):
        """Marque une mission comme complétée"""
        mission = self.get_mission(mission_id)
        if not mission:
            return

        # Ajouter la récompense finale
        profil["points"] = profil.get("points", 0) + mission["recompense"]

        # Marquer la mission comme complétée
        if "missions_completed" not in profil:
            profil["missions_completed"] = []
        if mission_id not in profil["missions_completed"]:
            profil["missions_completed"].append(mission_id)

        # Débloquer l'objet symbolique
        objet = mission.get("objet_symbolique")
        if objet:
            if "objets_debloques" not in profil:
                profil["objets_debloques"] = []
            if objet not in profil["objets_debloques"]:
                profil["objets_debloques"].append(objet)

    def get_available_missions(self, profil: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Récupère les missions disponibles pour le joueur"""
        current_acte = self.get_current_acte(profil)
        acte_order = [
            "prologue",
            "acte_1",
            "acte_2",
            "acte_3",
            "acte_4",
            "acte_5",
            "acte_6",
            "epilogue",
        ]

        available = []
        for acte in acte_order:
            mission = self.get_mission(acte)
            if mission:
                mission["available"] = acte == current_acte
                mission["completed"] = acte in profil.get("missions_completed", [])
                available.append(mission)

        return available

    def get_mission_progress(
        self, mission_id: str, profil: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Récupère la progression d'une mission"""
        mission = self.get_mission(mission_id)
        if not mission:
            return {}

        etapes_completed = profil.get("etapes_completed", {}).get(mission_id, [])
        progress = len(etapes_completed) / len(mission["etapes"]) * 100

        return {
            "mission": mission,
            "progress": progress,
            "etapes_completed": etapes_completed,
            "etapes_total": len(mission["etapes"]),
        }
