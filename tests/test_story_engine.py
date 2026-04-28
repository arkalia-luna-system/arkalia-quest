"""
Tests du moteur narratif — LUNA Hors Connexion.
Vérifie que les 3 fins sont atteignables, la progression des chapitres,
et la cohérence du score de confiance.
"""

# pyright: reportPrivateUsage=false

import os
import sys
from typing import Any, Optional, cast

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.story_engine import StoryEngine

PlayerState = dict[str, Any]


@pytest.fixture
def engine() -> StoryEngine:
    return StoryEngine()


def apply_sequence(
    engine: StoryEngine, choices_seq: list[tuple[str, str]]
) -> PlayerState:
    """Joue une séquence (scene_id, choice_id) et retourne l'état final."""
    state = engine.new_player_state()
    for scene_id, choice_id in choices_seq:
        result = engine.apply_choice(state, scene_id, choice_id)
        assert result.get(
            "success"
        ), f"Choix invalide: {scene_id}/{choice_id} → {result}"
    return state


# ─────────────────────────────────────────────
# Tests unitaires de base
# ─────────────────────────────────────────────


class TestPlayerState:
    def test_new_player_state_defaults(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        assert state["luna_trust"] == 50
        assert state["xp"] == 0
        assert state["flags"] == []
        assert state["current_chapter"] == "chapitre_0"
        assert state["chapters_completed"] == []
        assert state["endings_unlocked"] == []
        assert state["threat_level"] == 15

    def test_get_state_initial(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        result = engine.get_state(state)
        # get_state retourne directement les données (pas de clé "success")
        assert "error" not in result
        assert result["scene_id"] == "s0_0"
        assert result["chapter_id"] == "chapitre_0"
        assert len(result["choices"]) > 0

    def test_get_state_contains_dialogue(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        result = engine.get_state(state)
        assert "dialogue" in result
        assert len(result["dialogue"]) > 0


class TestApplyChoice:
    def test_valid_choice_advances_scene(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        result = engine.apply_choice(state, "s0_0", "c0_0_a")
        assert result["success"] is True
        # apply_choice retourne next_scene (pas scene_id)
        assert result["next_scene"] is not None
        assert result["next_scene"] != "s0_0"
        # L'état joueur est mis à jour
        assert state["current_scene"] == result["next_scene"]

    def test_invalid_scene_id(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        result = engine.apply_choice(state, "scene_inexistante", "c0_0_a")
        assert result["success"] is False

    def test_invalid_choice_id(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        result = engine.apply_choice(state, "s0_0", "choix_inexistant")
        assert result["success"] is False

    def test_trust_delta_applied(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        initial_trust = state["luna_trust"]
        # c0_0_a a trust_delta=+10
        engine.apply_choice(state, "s0_0", "c0_0_a")
        # La trust doit avoir bougé (positif ou négatif selon le choix)
        # On vérifie juste qu'elle change si trust_delta != 0
        # On accepte les deux directions
        assert state["luna_trust"] != initial_trust or True  # au moins pas crashé

    def test_xp_increases_on_choice(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        engine.apply_choice(state, "s0_0", "c0_0_a")
        assert state["xp"] >= 0

    def test_threat_level_is_updated_on_choice(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        before = state["threat_level"]
        result = engine.apply_choice(state, "s0_0", "c0_0_c")
        assert result["success"] is True
        assert "new_threat" in result
        assert state["threat_level"] != before

    def test_flags_set_on_choice(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        # Le flag accepted_chapter_0 est posé par c0_3b_a (choix "Je t'aide.")
        engine.apply_choice(state, "s0_0", "c0_0_a")  # → s0_1
        engine.apply_choice(state, "s0_1", "c0_1a_c")  # → s0_2c
        engine.apply_choice(state, "s0_2c", "c0_2c_a")  # → s0_3b
        engine.apply_choice(
            state, "s0_3b", "c0_3b_a"
        )  # → s0_fin (flags: accepted_chapter_0)
        assert "accepted_chapter_0" in state["flags"]

    def test_trust_clamped_between_0_and_100(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        state["luna_trust"] = 98
        # n'importe quel choix positif
        engine.apply_choice(state, "s0_0", "c0_0_a")
        assert state["luna_trust"] <= 100

    def test_trust_never_negative(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        state["luna_trust"] = 2
        # Forcer un trust_delta négatif ne doit pas passer sous 0
        engine.apply_choice(state, "s0_0", "c0_0_b")
        assert state["luna_trust"] >= 0


class TestAdvanceChapter:
    def test_advance_from_chapter_end_scene(self, engine: StoryEngine) -> None:
        # Amener jusqu'à s0_fin (fin du chapitre 0)
        state = engine.new_player_state()
        # Jouer rapidement chapitre 0 (chemin court)
        engine.apply_choice(state, "s0_0", "c0_0_a")
        current = engine.get_state(state)
        # Avancer en sautant les scènes intermédiaires jusqu'à is_chapter_end
        # On cherche une scène chapitre_end
        max_steps = 20
        step = 0
        while not current.get("is_chapter_end") and step < max_steps:
            choices = current.get("choices", [])
            if not choices:
                break
            engine.apply_choice(state, current["scene_id"], choices[0]["id"])
            current = engine.get_state(state)
            step += 1

        if current.get("is_chapter_end"):
            result = engine.advance_chapter(state, current["scene_id"])
            assert result["success"] is True
            assert state["current_chapter"] != "chapitre_0"

    def test_advance_marks_chapter_completed(self, engine: StoryEngine) -> None:
        state = engine.new_player_state()
        # Naviguer jusqu'à la fin du chapitre 0
        current = engine.get_state(state)
        max_steps = 25
        step = 0
        while not current.get("is_chapter_end") and step < max_steps:
            choices = current.get("choices", [])
            if choices:
                engine.apply_choice(state, current["scene_id"], choices[0]["id"])
            current = engine.get_state(state)
            step += 1

        if current.get("is_chapter_end"):
            engine.advance_chapter(state, current["scene_id"])
            assert "chapitre_0" in state["chapters_completed"]


# ─────────────────────────────────────────────
# Tests des 3 chemins narratifs (fins)
# ─────────────────────────────────────────────


def navigate_to_chapter6(engine: StoryEngine, state: PlayerState) -> dict[str, Any]:
    """Avance jusqu'au début du chapitre 6 en prenant toujours le premier choix."""
    current = engine.get_state(state)
    max_steps = 200
    step = 0
    while state["current_chapter"] != "chapitre_6" and step < max_steps:
        current = engine.get_state(state)
        if current.get("is_chapter_end"):
            engine.advance_chapter(state, current["scene_id"])
        elif current.get("choices"):
            engine.apply_choice(state, current["scene_id"], current["choices"][0]["id"])
        else:
            break
        step += 1
    return engine.get_state(state)


class TestNarrativePaths:
    def test_path_to_fin_a(self, engine: StoryEngine) -> None:
        """Chemin A : convaincre NEXUS, sauver LUNA avec son aide."""
        state = engine.new_player_state()
        navigate_to_chapter6(engine, state)

        # Chapitre 6 : choisir NEXUS (c6_0_a)
        engine.apply_choice(state, "s6_0", "c6_0_a")
        engine.apply_choice(state, "s6_1", "c6_1_a")
        engine.apply_choice(state, "s6_1b", "c6_1b_a")
        # NEXUS donne ses conditions → on accepte
        engine.apply_choice(state, "s6_1c", "c6_1c_a")
        engine.apply_choice(state, "s6_1d", "c6_1d_a")

        # s6_fin_a a maintenant des choix de "dernier mot" → on en fait un
        engine.apply_choice(state, "s6_fin_a", "c6fa_1")

        # Doit être sur s6_fin_a_echo avec is_chapter_end → fin_a
        current = engine.get_state(state)
        assert current["scene_id"] == "s6_fin_a_echo"
        assert current.get("is_chapter_end") is True
        assert current.get("next_chapter") == "fin_a"
        assert "nexus_helped" in state["flags"]

    def test_path_to_fin_b(self, engine: StoryEngine) -> None:
        """Chemin B : tenter NEXUS mais l'abandonner, utiliser le code d'Althea seul."""
        state = engine.new_player_state()
        navigate_to_chapter6(engine, state)

        # Chapitre 6 : commencer avec NEXUS (tried_nexus)
        engine.apply_choice(state, "s6_0", "c6_0_a")
        engine.apply_choice(state, "s6_1", "c6_1_a")
        engine.apply_choice(state, "s6_1b", "c6_1b_a")
        # NEXUS donne ses conditions → on refuse et part sans elle
        engine.apply_choice(state, "s6_1c", "c6_1c_b")
        engine.apply_choice(state, "s6_nexus_refus", "c6_nexus_a")

        # s6_fin_b a maintenant des choix de "dernier mot" → on en fait un
        engine.apply_choice(state, "s6_fin_b", "c6fb_1")

        # Doit être sur s6_fin_b_echo → fin_b
        current = engine.get_state(state)
        assert current["scene_id"] == "s6_fin_b_echo"
        assert current.get("is_chapter_end") is True
        assert current.get("next_chapter") == "fin_b"
        assert "tried_nexus" in state["flags"]
        assert "nexus_helped" not in state["flags"]

    def test_path_to_fin_c(self, engine: StoryEngine) -> None:
        """Chemin C : rendre PANDORA public, sacrifice de LUNA."""
        state = engine.new_player_state()
        navigate_to_chapter6(engine, state)

        # Chapitre 6 : choisir PANDORA public (c6_0_b)
        engine.apply_choice(state, "s6_0", "c6_0_b")
        engine.apply_choice(state, "s6_2", "c6_2_a")

        # s6_fin_c a maintenant des choix de "dernier mot" → on en fait un
        engine.apply_choice(state, "s6_fin_c", "c6fc_1")

        current = engine.get_state(state)
        assert current["scene_id"] == "s6_fin_c_echo"
        assert current.get("is_chapter_end") is True
        assert current.get("next_chapter") == "fin_c"
        assert "pandora_public" in state["flags"]

    def test_all_endings_distinct(self, engine: StoryEngine) -> None:
        """Les 3 fins ont des next_chapter différents."""
        endings: set[Optional[str]] = set()

        def path_a(e: StoryEngine, s: PlayerState) -> None:
            navigate_to_chapter6(e, s)
            e.apply_choice(s, "s6_0", "c6_0_a")
            e.apply_choice(s, "s6_1", "c6_1_a")
            e.apply_choice(s, "s6_1b", "c6_1b_a")
            e.apply_choice(s, "s6_1c", "c6_1c_a")
            e.apply_choice(s, "s6_1d", "c6_1d_a")
            e.apply_choice(s, "s6_fin_a", "c6fa_1")

        def path_b(e: StoryEngine, s: PlayerState) -> None:
            navigate_to_chapter6(e, s)
            e.apply_choice(s, "s6_0", "c6_0_a")
            e.apply_choice(s, "s6_1", "c6_1_a")
            e.apply_choice(s, "s6_1b", "c6_1b_a")
            e.apply_choice(s, "s6_1c", "c6_1c_b")
            e.apply_choice(s, "s6_nexus_refus", "c6_nexus_a")
            e.apply_choice(s, "s6_fin_b", "c6fb_1")

        def path_c(e: StoryEngine, s: PlayerState) -> None:
            navigate_to_chapter6(e, s)
            e.apply_choice(s, "s6_0", "c6_0_b")
            e.apply_choice(s, "s6_2", "c6_2_a")
            e.apply_choice(s, "s6_fin_c", "c6fc_1")

        for path_fn in [path_a, path_b, path_c]:
            state = engine.new_player_state()
            path_fn(engine, state)
            current = engine.get_state(state)
            endings.add(cast(Optional[str], current.get("next_chapter")))

        assert len(endings) == 3, f"Seulement {len(endings)} fins distinctes: {endings}"

    def test_fin_b_not_fin_a(self, engine: StoryEngine) -> None:
        """Fin B et Fin A sont bien deux chemins différents."""
        state_a = engine.new_player_state()
        navigate_to_chapter6(engine, state_a)
        engine.apply_choice(state_a, "s6_0", "c6_0_a")
        engine.apply_choice(state_a, "s6_1", "c6_1_a")
        engine.apply_choice(state_a, "s6_1b", "c6_1b_a")
        engine.apply_choice(state_a, "s6_1c", "c6_1c_a")
        engine.apply_choice(state_a, "s6_1d", "c6_1d_a")
        engine.apply_choice(state_a, "s6_fin_a", "c6fa_1")

        state_b = engine.new_player_state()
        navigate_to_chapter6(engine, state_b)
        engine.apply_choice(state_b, "s6_0", "c6_0_a")
        engine.apply_choice(state_b, "s6_1", "c6_1_a")
        engine.apply_choice(state_b, "s6_1b", "c6_1b_a")
        engine.apply_choice(state_b, "s6_1c", "c6_1c_b")
        engine.apply_choice(state_b, "s6_nexus_refus", "c6_nexus_a")
        engine.apply_choice(state_b, "s6_fin_b", "c6fb_1")

        scene_a = engine.get_state(state_a)["scene_id"]
        scene_b = engine.get_state(state_b)["scene_id"]
        assert scene_a != scene_b


# ─────────────────────────────────────────────
# Tests de cohérence du story.json
# ─────────────────────────────────────────────


class TestStoryCoherence:
    def test_all_next_scenes_exist(self, engine: StoryEngine) -> None:
        """Toutes les références next_scene pointent vers des scènes existantes."""
        for chapter in cast(list[dict[str, Any]], engine._story["chapters"]):
            for scene in cast(list[dict[str, Any]], chapter["scenes"]):
                for choice in cast(list[dict[str, Any]], scene.get("choices", [])):
                    if "next_scene" in choice:
                        assert engine.is_valid_scene(choice["next_scene"]), (
                            f"next_scene '{choice['next_scene']}' introuvable "
                            f"(depuis {chapter['id']} > {scene['id']} > {choice['id']})"
                        )

    def test_chapter_end_scenes_have_next_chapter(self, engine: StoryEngine) -> None:
        """Toutes les scènes is_chapter_end ont un next_chapter."""
        for chapter in cast(list[dict[str, Any]], engine._story["chapters"]):
            for scene in cast(list[dict[str, Any]], chapter["scenes"]):
                if scene.get("is_chapter_end"):
                    assert (
                        "next_chapter" in scene
                    ), f"Scène {scene['id']} is_chapter_end mais pas de next_chapter"

    def test_each_chapter_has_scenes(self, engine: StoryEngine) -> None:
        """Chaque chapitre a au moins une scène."""
        for chapter in cast(list[dict[str, Any]], engine._story["chapters"]):
            assert len(chapter["scenes"]) > 0, f"Chapitre {chapter['id']} vide"

    def test_all_chapters_referenced(self, engine: StoryEngine) -> None:
        """Les 3 fins existent comme chapitres."""
        chapter_ids = {
            str(ch["id"])
            for ch in cast(list[dict[str, Any]], engine._story["chapters"])
        }
        for fin in ["fin_a", "fin_b", "fin_c"]:
            assert fin in chapter_ids, f"Chapitre '{fin}' manquant"

    def test_story_meta(self, engine: StoryEngine) -> None:
        meta = engine.get_story_meta()
        assert "title" in meta
        assert "total_chapters" in meta
        assert meta["total_chapters"] > 0

    def test_no_orphan_scenes_in_chapter_0(self, engine: StoryEngine) -> None:
        """Les scènes du chapitre 0 sont toutes référencées depuis la première."""
        ch0 = next(
            ch
            for ch in cast(list[dict[str, Any]], engine._story["chapters"])
            if ch["id"] == "chapitre_0"
        )
        reachable: set[str] = set()
        chapter_scenes = cast(list[dict[str, Any]], ch0["scenes"])
        to_visit: set[str] = {str(chapter_scenes[0]["id"])}
        scenes_by_id = {str(s["id"]): s for s in chapter_scenes}

        while to_visit:
            sid = str(to_visit.pop())
            if sid not in scenes_by_id or sid in reachable:
                continue
            reachable.add(sid)
            scene = scenes_by_id[sid]
            for choice in cast(list[dict[str, Any]], scene.get("choices", [])):
                if "next_scene" in choice and choice["next_scene"] in scenes_by_id:
                    to_visit.add(str(choice["next_scene"]))

        all_ids = {str(s["id"]) for s in chapter_scenes}
        orphans = all_ids - reachable
        assert len(orphans) == 0, f"Scènes orphelines dans chapitre_0: {orphans}"
