#!/usr/bin/env python3
"""
Script de test pour vérifier les améliorations d'Arkalia Quest
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.append(str(Path(__file__).parent))


def test_progression_engine():
    """Test du moteur de progression"""
    print(r"🧪 Test du moteur de progression...")

    try:
        from core.progression_engine import ProgressionEngine

        engine = ProgressionEngine()

        # Test de création d'un joueur
        player_id = "test_player"
        result = engine.update_player_progression(
            player_id, "command_used", {"command": "test"}
        )

        if result["success"]:
            print(r"✅ Moteur de progression fonctionnel")

            # Test de récupération des données
            player_data = engine.get_player_progression(player_id)
            print(
                f"📊 Données joueur: Niveau {player_data['level']}, XP {player_data['xp']}"
            )

            return True
        else:
            print(r"❌ Erreur dans le moteur de progression")
            return False

    except Exception as e:
        print(f"❌ Erreur importation moteur de progression: {e}")
        return False


def test_skill_tree_system():
    """Test du système d'arbre de compétences"""
    print("\n🧪 Test du système d'arbre de compétences...")

    try:
        from core.enhanced_mission_system import EnhancedMissionSystem

        system = EnhancedMissionSystem()

        # Test de récupération de l'arbre de compétences
        profile = {"level": 1, "xp": 0, "skills": {}}
        skill_tree = system.get_skill_tree(profile)

        if skill_tree and "hacking" in skill_tree:
            print("✅ Système d'arbre de compétences fonctionnel")
            print(
                f"📊 Compétences hacking disponibles: {len(skill_tree['hacking']['skills'])}"
            )
            return True
        else:
            print("❌ Erreur dans le système d'arbre de compétences")
            return False

    except Exception as e:
        print(f"❌ Erreur importation système d'arbre de compétences: {e}")
        return False


def test_gamification_engine():
    """Test du moteur de gamification"""
    print(r"\n🧪 Test du moteur de gamification...")

    try:
        from core.gamification_engine import GamificationEngine

        engine = GamificationEngine()

        # Test de récupération des badges
        badges = engine._load_badges_secrets()

        if badges and "badges_secrets" in badges:
            print(r"✅ Moteur de gamification fonctionnel")
            print(f"🏆 Badges disponibles: {len(badges['badges_secrets'])}")
            return True
        else:
            print(r"❌ Erreur dans le moteur de gamification")
            return False

    except Exception as e:
        print(f"❌ Erreur importation moteur de gamification: {e}")
        return False


def test_js_files():
    """Test de l'existence des fichiers JavaScript"""
    print(r"\n🧪 Test des fichiers JavaScript...")

    js_files = [
        "static/js/skill-tree-system.js",
        "static/js/gamification-feedback.js",
        "static/js/progression-sync.js",
    ]

    all_exist = True
    for file_path in js_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} existe")
        else:
            print(f"❌ {file_path} manquant")
            all_exist = False

    return all_exist


def test_api_routes():
    """Test des routes API"""
    print(r"\n🧪 Test des routes API...")

    # Vérifier que les routes sont définies dans app.py
    with open("app.py", encoding="utf-8") as f:
        content = f.read()

    routes = [
        '@app.route("/api/skill-tree")',
        '@app.route("/api/skill-tree/upgrade", methods=["POST"])',
        '@app.route("/api/sync-progression")',
        '@app.route("/api/progression-data")',
    ]

    all_routes_exist = True
    for route in routes:
        if route in content:
            print(f"✅ Route {route} définie")
        else:
            print(f"❌ Route {route} manquante")
            all_routes_exist = False

    return all_routes_exist


def main():
    """Fonction principale de test"""
    print("🚀 Test des améliorations d'Arkalia Quest")
    print("=" * 50)

    tests = [
        test_progression_engine,
        test_skill_tree_system,
        test_gamification_engine,
        test_js_files,
        test_api_routes,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans le test: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print(r"📊 RÉSULTATS DES TESTS")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")

    if passed == total:
        print(r"\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print(r"✨ Les améliorations sont prêtes à être testées dans le navigateur")
    else:
        print(r"\n⚠️  Certains tests ont échoué")
        print(r"🔧 Vérifiez les erreurs ci-dessus")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
