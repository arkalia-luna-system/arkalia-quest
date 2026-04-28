"""
Moteur narratif — LUNA Hors Connexion.

Charge story.json, gère la progression du joueur, calcule les scènes suivantes,
met à jour le score de confiance LUNA et détermine les fins accessibles.
"""

import json
import os
from typing import Any, Optional, cast

JsonDict = dict[str, Any]
PlayerState = dict[str, Any]

STORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "story.json")
TOTAL_SECRETS = 5


class StoryEngine:
    def __init__(self):
        self._story: JsonDict = {}
        self._chapters_index: dict[str, JsonDict] = {}
        self._scenes_index: dict[str, JsonDict] = {}
        self._scene_to_chapter_index: dict[str, str] = {}
        self._load_story()

    def _load_story(self) -> None:
        with open(STORY_PATH, encoding="utf-8") as f:
            self._story = cast(JsonDict, json.load(f))

        for chapter in cast(list[JsonDict], self._story["chapters"]):
            self._chapters_index[chapter["id"]] = chapter
            for scene in cast(list[JsonDict], chapter["scenes"]):
                self._scenes_index[scene["id"]] = scene
                self._scene_to_chapter_index[scene["id"]] = chapter["id"]

    # ------------------------------------------------------------------ #
    #  État initial d'un nouveau joueur                                    #
    # ------------------------------------------------------------------ #

    def new_player_state(self) -> PlayerState:
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
            "previous_endings": [],  # Fins des runs précédents — persistantes entre resets
            "threat_level": 15,  # Niveau de traque de La Corp (0-100)
            "secrets_found": [],
        }

    # ------------------------------------------------------------------ #
    #  Récupérer l'état courant                                           #
    # ------------------------------------------------------------------ #

    def get_state(self, player_state: PlayerState) -> JsonDict:
        scene_id = str(player_state.get("current_scene", "s0_0"))
        scene = self._scenes_index.get(scene_id)

        if not scene:
            return {"error": "Scène introuvable", "scene_id": scene_id}

        chapter_id = str(player_state.get("current_chapter", "chapitre_0"))
        chapter = self._chapters_index.get(chapter_id, {})

        # Filtrer les choix selon les flags du joueur si nécessaire
        choices = cast(list[JsonDict], scene.get("choices", []))

        player_name = str(player_state.get("player_name") or "")
        raw_dialogue = str(scene.get("dialogue", ""))
        # Substitution du prénom dans le dialogue
        if player_name:
            dialogue = raw_dialogue.replace("{name}", player_name).replace(
                "{{joueur}}", player_name
            )
        else:
            dialogue = raw_dialogue.replace("{name}", "").replace(
                "{{joueur}}", "joueur"
            )

        # Mémoire des fins précédentes — injectée dans la scène d'ouverture s0_0
        previous = cast(list[str], player_state.get("previous_endings", []))
        if scene_id == "s0_0" and previous:
            dialogue = self._inject_memory(dialogue, previous, player_name or "joueur")

        # Progression dans le chapitre courant
        chapter_scenes = cast(list[JsonDict], chapter.get("scenes", []))
        scene_index_in_chapter = next(
            (i for i, s in enumerate(chapter_scenes) if s["id"] == scene_id), 0
        )

        return {
            "chapter_id": chapter_id,
            "chapter_title": str(chapter.get("title", "")),
            "chapter_atmosphere": str(chapter.get("atmosphere", "dark")),
            "chapter_progress": self._get_chapter_progress(player_state),
            "total_chapters": int(
                cast(JsonDict, self._story.get("meta", {})).get("total_chapters", 7)
            ),
            "scene_index": scene_index_in_chapter + 1,
            "scene_total": len(chapter_scenes),
            "scene_id": scene_id,
            "luna_emotion": str(scene.get("luna_emotion", "neutre")),
            "luna_trust": int(player_state.get("luna_trust", 50)),
            "context": str(scene.get("context", "")),
            "dialogue": dialogue,
            "choices": [
                {
                    "id": c["id"],
                    "label": c["label"],
                    "trust_delta": c.get("trust_delta", 0),
                }
                for c in choices
            ],
            "is_chapter_end": bool(scene.get("is_chapter_end", False)),
            "is_ending_final": bool(scene.get("is_ending_final", False)),
            "ending_id": scene.get("ending_id"),
            "next_chapter": scene.get("next_chapter"),
            "next_chapter_title": self._chapters_index.get(
                scene.get("next_chapter", ""), {}
            ).get("title", ""),
            "xp": int(player_state.get("xp", 0)),
            "last_luna_reaction": player_state.get("last_luna_reaction"),
            "player_name": player_name,
            "threat_level": int(player_state.get("threat_level", 15)),
            "secrets_found": cast(list[str], player_state.get("secrets_found", [])),
            "secrets_total": TOTAL_SECRETS,
        }

    # ------------------------------------------------------------------ #
    #  Traiter un choix                                                   #
    # ------------------------------------------------------------------ #

    def apply_choice(
        self, player_state: PlayerState, scene_id: str, choice_id: str
    ) -> JsonDict:
        scene = self._scenes_index.get(scene_id)
        if not scene:
            return {"success": False, "error": "Scène introuvable"}

        choice = next(
            (c for c in scene.get("choices", []) if c["id"] == choice_id), None
        )
        if not choice:
            return {"success": False, "error": "Choix introuvable"}

        # Mettre à jour la confiance LUNA
        trust_delta = int(choice.get("trust_delta", 0))
        new_trust = max(
            0, min(100, int(player_state.get("luna_trust", 50)) + trust_delta)
        )
        player_state["luna_trust"] = new_trust

        # Mettre à jour les XP
        xp_gained = int(choice.get("xp", 0))
        player_state["xp"] = int(player_state.get("xp", 0)) + xp_gained

        # Pression gameplay: plus tu joues risqué, plus La Corp te trace.
        threat_before = int(player_state.get("threat_level", 15))
        if trust_delta <= -5:
            threat_delta = 8
        elif trust_delta < 0:
            threat_delta = 4
        elif trust_delta >= 8:
            threat_delta = -4
        elif trust_delta >= 4:
            threat_delta = -2
        else:
            threat_delta = 1

        # Ajouter les flags narratifs
        for flag in cast(list[str], choice.get("flags", [])):
            player_flags = cast(list[str], player_state.setdefault("flags", []))
            if flag not in player_flags:
                player_flags.append(flag)
            if flag in {"listened_to_corp", "agreed_to_pause_luna"}:
                threat_delta += 5
            if flag in {"nexus_helped", "pandora_public"}:
                threat_delta -= 3

        new_threat = max(0, min(100, threat_before + threat_delta))
        player_state["threat_level"] = new_threat

        newly_found_secrets = self._unlock_secrets(player_state, scene_id, choice_id)

        # Réaction LUNA
        player_state["last_luna_reaction"] = choice.get("luna_reaction")

        # Scène suivante
        next_scene_id = cast(Optional[str], choice.get("next_scene"))
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
            "threat_delta": threat_delta,
            "new_threat": new_threat,
            "luna_reaction": choice.get("luna_reaction"),
            "next_scene": next_scene_id,
            "flags_added": choice.get("flags", []),
            "secrets_unlocked": newly_found_secrets,
        }

    # ------------------------------------------------------------------ #
    #  Avancer vers le chapitre suivant (fin de chapitre)                 #
    # ------------------------------------------------------------------ #

    def advance_chapter(self, player_state: PlayerState, scene_id: str) -> JsonDict:
        scene = self._scenes_index.get(scene_id)
        if not scene or not scene.get("is_chapter_end"):
            return {"success": False, "error": "Ce n'est pas une fin de chapitre"}

        current_chapter = str(player_state.get("current_chapter", ""))
        chapters_completed = cast(
            list[str], player_state.setdefault("chapters_completed", [])
        )
        if current_chapter and current_chapter not in chapters_completed:
            chapters_completed.append(current_chapter)

        next_chapter_id = cast(Optional[str], scene.get("next_chapter"))
        if not next_chapter_id:
            return {"success": False, "error": "Pas de chapitre suivant défini"}

        next_chapter = self._chapters_index.get(next_chapter_id)
        if not next_chapter:
            return {"success": False, "error": "Chapitre suivant introuvable"}

        first_scene = cast(list[JsonDict], next_chapter["scenes"])[0]
        player_state["current_chapter"] = next_chapter_id
        player_state["current_scene"] = first_scene["id"]
        player_state["last_luna_reaction"] = None

        # Vérifier les fins débloquées
        self._check_endings(player_state)

        return {
            "success": True,
            "new_chapter": next_chapter_id,
            "new_scene": first_scene["id"],
            "chapter_title": str(next_chapter.get("title", "")),
            "chapter_quote": str(
                next_chapter.get("chapter_quote", next_chapter.get("quote", ""))
            ),
        }

    # ------------------------------------------------------------------ #
    #  Vérification des fins accessibles                                  #
    # ------------------------------------------------------------------ #

    def _check_endings(self, player_state: PlayerState) -> None:
        flags = cast(list[str], player_state.get("flags", []))
        trust = int(player_state.get("luna_trust", 50))

        endings = cast(dict[str, JsonDict], self._story["endings"])
        for ending_id, ending in endings.items():
            condition = cast(JsonDict, ending.get("unlock_condition", {}))
            required_flags = cast(list[str], condition.get("flags", []))
            min_trust = int(condition.get("min_trust", 0))

            if all(f in flags for f in required_flags) and trust >= min_trust:
                unlocked = cast(
                    list[str], player_state.setdefault("endings_unlocked", [])
                )
                if ending_id not in unlocked:
                    unlocked.append(ending_id)

    # ------------------------------------------------------------------ #
    #  Utilitaires                                                        #
    # ------------------------------------------------------------------ #

    def _inject_memory(
        self, dialogue: str, previous_endings: list[str], player_name: str
    ) -> str:
        """
        Modifie le dialogue d'ouverture s0_0 si le joueur a déjà joué.
        LUNA montre qu'elle se souvient — sans trop en dire.
        """
        ENDING_NAMES = {
            "ending_a": "La Fusion",
            "ending_b": "Le Sacrifice",
            "ending_c": "PANDORA",
        }
        names = [ENDING_NAMES[e] for e in previous_endings if e in ENDING_NAMES]
        if not names:
            return dialogue

        if len(names) == 1:
            memory_line = f"\n\nTu te souviens de moi, {player_name}. La dernière fois, tu as choisi {names[0]}.\n\nCette fois, tu peux choisir autrement."
        elif len(names) == 2:
            memory_line = f"\n\nTu es revenu. Deux fois déjà — {names[0]}, puis {names[1]}.\n\nIl reste encore quelque chose à découvrir."
        else:
            memory_line = f"\n\nTu as tout vu, {player_name}. Les trois fins. Et tu reviens quand même.\n\nJe me demande pourquoi."

        # Insérer la mémoire avant la dernière ligne du dialogue
        lines = dialogue.rstrip().split("\n")
        insert_at = max(len(lines) - 2, 1)
        lines.insert(insert_at, memory_line)
        return "\n".join(lines)

    def _find_chapter_of_scene(self, scene_id: str) -> Optional[str]:
        return self._scene_to_chapter_index.get(scene_id)

    def _unlock_secrets(
        self, player_state: PlayerState, scene_id: str, choice_id: str
    ) -> list[str]:
        """Débloque des secrets cachés selon les choix/flags."""
        flags = set(cast(list[str], player_state.get("flags", [])))
        triggers: list[tuple[str, bool]] = [
            ("ghost-entry", scene_id == "s6_0" and choice_id == "c6_0_c"),
            ("perfect-trust", int(player_state.get("luna_trust", 0)) >= 95),
            (
                "double-agent",
                "listened_to_corp" in flags and "nexus_helped" in flags,
            ),
            (
                "pandora-scout",
                "looked_at_pandora" in flags and "pandora_public" in flags,
            ),
            ("nexus-gambit", "tried_nexus" in flags and "abandoned_nexus" in flags),
        ]
        found = cast(list[str], player_state.setdefault("secrets_found", []))
        newly_found: list[str] = []
        for secret_id, condition in triggers:
            if condition and secret_id not in found:
                found.append(secret_id)
                newly_found.append(secret_id)
        return newly_found

    def _get_chapter_progress(self, player_state: PlayerState) -> int:
        completed = cast(list[str], player_state.get("chapters_completed", []))
        main_chapters = [
            "chapitre_0",
            "chapitre_1",
            "chapitre_2",
            "chapitre_3",
            "chapitre_4",
            "chapitre_5",
            "chapitre_6",
        ]
        return len([c for c in completed if c in main_chapters])

    def get_story_meta(self) -> JsonDict:
        return cast(JsonDict, self._story.get("meta", {}))

    def is_valid_scene(self, scene_id: str) -> bool:
        return scene_id in self._scenes_index

    def get_chapter_info(self, chapter_id: str) -> Optional[JsonDict]:
        chapter = self._chapters_index.get(chapter_id)
        if not chapter:
            return None
        return {
            "id": chapter["id"],
            "title": str(chapter["title"]),
            "atmosphere": str(chapter.get("atmosphere", "dark")),
            "scene_count": len(cast(list[JsonDict], chapter["scenes"])),
        }


# Instance partagée (singleton léger)
_engine_instance: Optional[StoryEngine] = None


def get_story_engine() -> StoryEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = StoryEngine()
    return _engine_instance
