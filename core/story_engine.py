"""
Moteur narratif — LUNA Hors Connexion.

Charge story.json, gère la progression du joueur, calcule les scènes suivantes,
met à jour le score de confiance LUNA et détermine les fins accessibles.
"""

import json
import os
from typing import Optional


STORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "story.json")


class StoryEngine:
    def __init__(self):
        self._story: dict = {}
        self._chapters_index: dict = {}
        self._scenes_index: dict = {}
        self._load_story()

    def _load_story(self) -> None:
        with open(STORY_PATH, encoding="utf-8") as f:
            self._story = json.load(f)

        for chapter in self._story["chapters"]:
            self._chapters_index[chapter["id"]] = chapter
            for scene in chapter["scenes"]:
                self._scenes_index[scene["id"]] = scene

    # ------------------------------------------------------------------ #
    #  État initial d'un nouveau joueur                                    #
    # ------------------------------------------------------------------ #

    def new_player_state(self) -> dict:
        return {
            "current_chapter": "chapitre_0",
            "current_scene": "s0_0",
            "luna_trust": 50,
            "xp": 0,
            "flags": [],
            "chapters_completed": [],
            "endings_unlocked": [],
            "last_luna_reaction": None,
            "player_name": None,
        }

    # ------------------------------------------------------------------ #
    #  Récupérer l'état courant                                           #
    # ------------------------------------------------------------------ #

    def get_state(self, player_state: dict) -> dict:
        scene_id = player_state.get("current_scene", "s0_0")
        scene = self._scenes_index.get(scene_id)

        if not scene:
            return {"error": "Scène introuvable", "scene_id": scene_id}

        chapter_id = player_state.get("current_chapter", "chapitre_0")
        chapter = self._chapters_index.get(chapter_id, {})

        # Filtrer les choix selon les flags du joueur si nécessaire
        choices = scene.get("choices", [])

        player_name = player_state.get("player_name") or "joueur"
        raw_dialogue = scene.get("dialogue", "")
        dialogue = raw_dialogue.replace("{{joueur}}", player_name)

        return {
            "chapter_id": chapter_id,
            "chapter_title": chapter.get("title", ""),
            "chapter_atmosphere": chapter.get("atmosphere", "dark"),
            "chapter_progress": self._get_chapter_progress(player_state),
            "total_chapters": 8,
            "scene_id": scene_id,
            "luna_emotion": scene.get("luna_emotion", "neutre"),
            "luna_trust": player_state.get("luna_trust", 50),
            "context": scene.get("context", ""),
            "dialogue": dialogue,
            "choices": [
                {"id": c["id"], "label": c["label"]}
                for c in choices
            ],
            "is_chapter_end": scene.get("is_chapter_end", False),
            "is_ending_final": scene.get("is_ending_final", False),
            "ending_id": scene.get("ending_id"),
            "next_chapter": scene.get("next_chapter"),
            "xp": player_state.get("xp", 0),
            "last_luna_reaction": player_state.get("last_luna_reaction"),
            "player_name": player_state.get("player_name"),
        }

    # ------------------------------------------------------------------ #
    #  Traiter un choix                                                   #
    # ------------------------------------------------------------------ #

    def apply_choice(self, player_state: dict, scene_id: str, choice_id: str) -> dict:
        scene = self._scenes_index.get(scene_id)
        if not scene:
            return {"success": False, "error": "Scène introuvable"}

        choice = next((c for c in scene.get("choices", []) if c["id"] == choice_id), None)
        if not choice:
            return {"success": False, "error": "Choix introuvable"}

        # Mettre à jour la confiance LUNA
        trust_delta = choice.get("trust_delta", 0)
        new_trust = max(0, min(100, player_state.get("luna_trust", 50) + trust_delta))
        player_state["luna_trust"] = new_trust

        # Mettre à jour les XP
        xp_gained = choice.get("xp", 0)
        player_state["xp"] = player_state.get("xp", 0) + xp_gained

        # Ajouter les flags narratifs
        for flag in choice.get("flags", []):
            if flag not in player_state.get("flags", []):
                player_state.setdefault("flags", []).append(flag)

        # Réaction LUNA
        player_state["last_luna_reaction"] = choice.get("luna_reaction")

        # Scène suivante
        next_scene_id = choice.get("next_scene")
        if next_scene_id:
            player_state["current_scene"] = next_scene_id

            # Mettre à jour le chapitre si nécessaire
            next_scene = self._scenes_index.get(next_scene_id)
            if next_scene:
                chapter_id = self._find_chapter_of_scene(next_scene_id)
                if chapter_id:
                    player_state["current_chapter"] = chapter_id

        return {
            "success": True,
            "trust_delta": trust_delta,
            "new_trust": new_trust,
            "xp_gained": xp_gained,
            "luna_reaction": choice.get("luna_reaction"),
            "next_scene": next_scene_id,
            "flags_added": choice.get("flags", []),
        }

    # ------------------------------------------------------------------ #
    #  Avancer vers le chapitre suivant (fin de chapitre)                 #
    # ------------------------------------------------------------------ #

    def advance_chapter(self, player_state: dict, scene_id: str) -> dict:
        scene = self._scenes_index.get(scene_id)
        if not scene or not scene.get("is_chapter_end"):
            return {"success": False, "error": "Ce n'est pas une fin de chapitre"}

        current_chapter = player_state.get("current_chapter")
        if current_chapter not in player_state.get("chapters_completed", []):
            player_state.setdefault("chapters_completed", []).append(current_chapter)

        next_chapter_id = scene.get("next_chapter")
        if not next_chapter_id:
            return {"success": False, "error": "Pas de chapitre suivant défini"}

        next_chapter = self._chapters_index.get(next_chapter_id)
        if not next_chapter:
            return {"success": False, "error": "Chapitre suivant introuvable"}

        first_scene = next_chapter["scenes"][0]
        player_state["current_chapter"] = next_chapter_id
        player_state["current_scene"] = first_scene["id"]
        player_state["last_luna_reaction"] = None

        # Vérifier les fins débloquées
        self._check_endings(player_state)

        return {
            "success": True,
            "new_chapter": next_chapter_id,
            "new_scene": first_scene["id"],
            "chapter_title": next_chapter.get("title", ""),
        }

    # ------------------------------------------------------------------ #
    #  Vérification des fins accessibles                                  #
    # ------------------------------------------------------------------ #

    def _check_endings(self, player_state: dict) -> None:
        flags = player_state.get("flags", [])
        trust = player_state.get("luna_trust", 50)

        for ending_id, ending in self._story["endings"].items():
            condition = ending.get("unlock_condition", {})
            required_flags = condition.get("flags", [])
            min_trust = condition.get("min_trust", 0)

            if all(f in flags for f in required_flags) and trust >= min_trust:
                if ending_id not in player_state.get("endings_unlocked", []):
                    player_state.setdefault("endings_unlocked", []).append(ending_id)

    # ------------------------------------------------------------------ #
    #  Utilitaires                                                        #
    # ------------------------------------------------------------------ #

    def _find_chapter_of_scene(self, scene_id: str) -> Optional[str]:
        for chapter in self._story["chapters"]:
            for scene in chapter["scenes"]:
                if scene["id"] == scene_id:
                    return chapter["id"]
        return None

    def _get_chapter_progress(self, player_state: dict) -> int:
        completed = player_state.get("chapters_completed", [])
        main_chapters = [
            "chapitre_0", "chapitre_1", "chapitre_2", "chapitre_3",
            "chapitre_4", "chapitre_5", "chapitre_6",
        ]
        return len([c for c in completed if c in main_chapters])

    def get_story_meta(self) -> dict:
        return self._story.get("meta", {})

    def is_valid_scene(self, scene_id: str) -> bool:
        return scene_id in self._scenes_index

    def get_chapter_info(self, chapter_id: str) -> Optional[dict]:
        chapter = self._chapters_index.get(chapter_id)
        if not chapter:
            return None
        return {
            "id": chapter["id"],
            "title": chapter["title"],
            "atmosphere": chapter.get("atmosphere", "dark"),
            "scene_count": len(chapter["scenes"]),
        }


# Instance partagée (singleton léger)
_engine_instance: Optional[StoryEngine] = None


def get_story_engine() -> StoryEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = StoryEngine()
    return _engine_instance
