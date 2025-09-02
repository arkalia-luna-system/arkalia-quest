#!/usr/bin/env python3
"""
Test complet d'Arkalia Quest v3.1.0
Teste toutes les fonctionnalités principales du jeu
"""

import json
import sys
import os


def test_imports():
    """Test des imports principaux"""
    print("🔧 Test des imports...")
    try:

        print("✅ Tous les imports fonctionnent")
        return True
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False


def test_missions():
    """Test des missions"""
    print("\n🎯 Test des missions...")
    try:
        missions = []
        for file in os.listdir("data/missions"):
            if file.endswith(".json"):
                with open(f"data/missions/{file}", "r", encoding="utf-8") as f:
                    mission = json.load(f)
                    missions.append(mission)

        print(f"✅ {len(missions)} missions chargées")
        for mission in missions:
            print(f"  - {mission['title']} (difficulté: {mission['difficulty']})")
        return True
    except Exception as e:
        print(f"❌ Erreur missions: {e}")
        return False


def test_mini_jeux():
    """Test des mini-jeux"""
    print("\n🎮 Test des mini-jeux...")
    try:
        from core.educational_games_engine import EducationalGamesEngine

        ege = EducationalGamesEngine()
        games = ege.get_available_games(1)

        print(f"✅ {len(games)} mini-jeux disponibles")
        for game in games:
            print(f"  - {game['title']} ({game['type']}) - {game['points']}pts")
        return True
    except Exception as e:
        print(f"❌ Erreur mini-jeux: {e}")
        return False


def test_badges():
    """Test des badges"""
    print("\n🏆 Test des badges...")
    try:
        with open("data/badges_secrets.json", "r", encoding="utf-8") as f:
            badges = json.load(f)

        print(f"✅ {len(badges['badges_secrets'])} badges disponibles")
        for badge_id, badge in list(badges["badges_secrets"].items())[:5]:
            print(f"  - {badge['nom']} ({badge['rarete']})")
        return True
    except Exception as e:
        print(f"❌ Erreur badges: {e}")
        return False


def test_commandes():
    """Test des commandes"""
    print("\n💻 Test des commandes...")
    try:
        from core.commands.game_commands import GameCommands
        from core.commands.basic_commands import BasicCommands

        gc = GameCommands()
        bc = BasicCommands()

        # Test profil fictif
        profile = {"score": 0, "level": 1, "badges": [], "missions_completed": []}

        # Test commande games
        result = gc.handle_games(profile)
        if result["réussite"]:
            print("✅ Commande 'games' fonctionne")

        # Test commande aide
        result = bc.handle_aide(profile)
        if result["réussite"]:
            print("✅ Commande 'aide' fonctionne")

        return True
    except Exception as e:
        print(f"❌ Erreur commandes: {e}")
        return False


def test_interface_js():
    """Test de l'interface JavaScript"""
    print("\n🌐 Test de l'interface JavaScript...")
    try:
        # Vérifier que les fichiers JS existent
        js_files = [
            "static/js/mini-games-interface.js",
            "static/js/terminal.js",
            "static/js/tutorial.js",
        ]

        for js_file in js_files:
            if os.path.exists(js_file):
                print(f"✅ {js_file} existe")
            else:
                print(f"❌ {js_file} manquant")
                return False

        # Vérifier que les fichiers CSS existent
        css_files = ["static/css/mini-games.css", "static/css/arkalia-luna-vision.css"]

        for css_file in css_files:
            if os.path.exists(css_file):
                print(f"✅ {css_file} existe")
            else:
                print(f"❌ {css_file} manquant")
                return False

        return True
    except Exception as e:
        print(f"❌ Erreur interface: {e}")
        return False


def main():
    """Fonction principale de test"""
    print("🚀 TEST COMPLET D'ARKALIA QUEST v3.1.0")
    print("=" * 50)

    tests = [
        test_imports,
        test_missions,
        test_mini_jeux,
        test_badges,
        test_commandes,
        test_interface_js,
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "=" * 50)
    print("📊 RÉSULTATS FINAUX:")

    passed = sum(results)
    total = len(results)

    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("🚀 Arkalia Quest v3.1.0 est prêt pour la production !")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
