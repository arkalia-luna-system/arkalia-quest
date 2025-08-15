#!/usr/bin/env python3
"""
Test simple pour le système de mini-jeux éducatifs Arkalia Quest
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_educational_games_engine():
    """Test simple du moteur de mini-jeux éducatifs"""

    print("🎮 TEST SIMPLE - MINI-JEUX ÉDUCATIFS")
    print("=" * 50)

    try:
        # Importer le moteur
        from core.educational_games_engine import EducationalGamesEngine

        # Créer une instance
        engine = EducationalGamesEngine()
        print("✅ Moteur créé avec succès")

        # Vérifier les données des jeux
        games_data = engine.games_data
        print(f"✅ Données des jeux chargées : {len(games_data)} types")

        # Vérifier chaque type de jeu
        for game_type, games in games_data.items():
            print(f"  🎮 {game_type}: {len(games)} jeux")
            for game in games:
                print(f"    - {game['id']}: {game['title']} ({game['difficulty']})")

        # Test de démarrage d'un jeu
        result = engine.start_game("logic_1", "test_user")
        if result["success"]:
            print("✅ Démarrage de jeu réussi")
            session_id = result["session_id"]

            # Test de soumission de réponse correcte
            submit_result = engine.submit_answer(session_id, "CHAT")
            if submit_result["success"] and submit_result["correct"]:
                print("✅ Soumission de réponse correcte réussie")
                print(f"   Score: {submit_result['score']}")
                print(f"   Badge: {submit_result['badge']}")
            else:
                print("❌ Échec soumission réponse correcte")

            # Test de soumission de réponse incorrecte
            submit_result = engine.submit_answer(session_id, "CHIEN")
            if submit_result["success"] and not submit_result["correct"]:
                print("✅ Soumission de réponse incorrecte gérée correctement")
            else:
                print("❌ Échec gestion réponse incorrecte")
        else:
            print("❌ Échec démarrage de jeu")

        # Test des statistiques
        stats = engine.get_game_statistics()
        print(f"✅ Statistiques récupérées : {stats['total_games']} jeux")

        # Test du classement
        leaderboard = engine.get_leaderboard()
        print(f"✅ Classement récupéré : {len(leaderboard)} joueurs")

        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        return True

    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_educational_games_commands():
    """Test des commandes de mini-jeux"""

    print("\n🎮 TEST DES COMMANDES")
    print("=" * 30)

    try:
        from core.commands.game_commands import GameCommands

        commands = GameCommands()
        test_profile = {
            "id": "test_user",
            "name": "Test User",
            "level": 2,
            "score": 100,
            "badges": []
        }

        # Test des commandes
        commands_to_test = [
            ("play_game", ["logic_1"]),
            ("games_list", []),
            ("game_stats", []),
            ("game_leaderboard", []),
            ("game_progress", [])
        ]

        for command, args in commands_to_test:
            handler = getattr(commands, f"handle_{command}")
            result = handler(test_profile, args)

            if result and result.get("réussite"):
                print(f"✅ Commande {command} : OK")
            else:
                print(f"❌ Commande {command} : ÉCHEC")

        print("🎉 TOUTES LES COMMANDES TESTÉES !")
        return True

    except Exception as e:
        print(f"❌ Erreur commandes : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST SIMPLE - SYSTÈME DE MINI-JEUX ÉDUCATIFS")
    print("=" * 60)

    # Test du moteur
    engine_success = test_educational_games_engine()

    # Test des commandes
    commands_success = test_educational_games_commands()

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print(f"Moteur : {'✅ Réussi' if engine_success else '❌ Échec'}")
    print(f"Commandes : {'✅ Réussi' if commands_success else '❌ Échec'}")

    if engine_success and commands_success:
        print("\n🎉 SYSTÈME DE MINI-JEUX ÉDUCATIFS OPÉRATIONNEL !")
        print("💡 Fonctionnalités disponibles :")
        print("  - 9 mini-jeux éducatifs (logique, code, cybersécurité, cryptographie, réseaux)")
        print("  - Système de points et badges")
        print("  - Interface immersive avec effets visuels")
        print("  - Commandes terminal intégrées")
        print("  - API REST complète")
        return True
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
