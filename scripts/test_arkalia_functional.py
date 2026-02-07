#!/usr/bin/env python3
"""
Script de test fonctionnel Arkalia Quest (sans serveur).
Fusionne : test_improvements, vérifications progression/skill-tree/gamification, fichiers, routes.
"""

import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
os.chdir(_root)


def test_progression_engine():
    """Test du moteur de progression."""
    print("🧪 Test du moteur de progression...")
    try:
        from core.progression_engine import ProgressionEngine

        engine = ProgressionEngine()
        result = engine.update_player_progression(
            "test_player", "command_used", {"command": "test"}
        )
        if result.get("success"):
            player_data = engine.get_player_progression("test_player")
            print(f"  ✅ Niveau {player_data.get('level')}, XP {player_data.get('xp')}")
            return True
        return False
    except Exception as e:
        print(f"  ❌ {e}")
        return False


def test_skill_tree_system():
    """Test du système d'arbre de compétences (mission_unified)."""
    print("🧪 Test du système d'arbre de compétences...")
    try:
        from core.mission_unified import mission_unified

        profile = {"level": 1, "xp": 0, "skills": {}}
        skill_tree = mission_unified.get_skill_tree(profile)
        if skill_tree and "hacking" in skill_tree:
            n = len(skill_tree["hacking"]["skills"])
            print(f"  ✅ Compétences hacking: {n}")
            return True
        return False
    except Exception as e:
        print(f"  ❌ {e}")
        return False


def test_gamification_engine():
    """Test du moteur de gamification."""
    print("🧪 Test du moteur de gamification...")
    try:
        from core.gamification_engine import GamificationEngine

        engine = GamificationEngine()
        badges = engine._load_badges_secrets()
        if badges and "badges_secrets" in badges:
            print(f"  ✅ Badges: {len(badges['badges_secrets'])}")
            return True
        return False
    except Exception as e:
        print(f"  ❌ {e}")
        return False


def test_js_files():
    """Test de l'existence des fichiers JavaScript critiques."""
    print("🧪 Test des fichiers JavaScript...")
    js_files = [
        "static/js/skill-tree-system.js",
        "static/js/gamification-feedback.js",
        "static/js/progression-sync.js",
    ]
    ok = all(Path(f).exists() for f in js_files)
    for f in js_files:
        print(f"  {'✅' if Path(f).exists() else '❌'} {f}")
    return ok


def test_api_routes_defined():
    """Vérifie que les routes API critiques sont définies dans app.py."""
    print("🧪 Test des routes API (définies)...")
    app_py = _root / "app.py"
    content = app_py.read_text(encoding="utf-8")
    routes = [
        '@app.route("/api/skill-tree")',
        '@app.route("/api/skill-tree/upgrade", methods=["POST"])',
        '@app.route("/api/sync-progression")',
        '@app.route("/api/progression-data")',
    ]
    ok = all(r in content for r in routes)
    for r in routes:
        print(f"  {'✅' if r in content else '❌'} {r.split(')')[0]})")
    return ok


def main():
    print("🚀 Test fonctionnel Arkalia Quest")
    print("=" * 50)
    tests = [
        test_progression_engine,
        test_skill_tree_system,
        test_gamification_engine,
        test_js_files,
        test_api_routes_defined,
    ]
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:
            print(f"  ❌ {e}")
            results.append(False)
    passed = sum(results)
    total = len(results)
    print("=" * 50)
    print(f"📊 Résultats: {passed}/{total}")
    return passed == total


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
