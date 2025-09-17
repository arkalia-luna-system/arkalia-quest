#!/usr/bin/env python3
"""
Script pour donner de l'XP au joueur pour tester l'arbre de compétences
"""

import os
import sys

import requests

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def give_xp_directly():
    """Donne directement de l'XP au joueur via le moteur de progression"""
    print("🎮 Donner de l'XP directement au joueur...")

    try:
        from core.progression_engine import ProgressionEngine

        # Créer une instance du moteur de progression
        engine = ProgressionEngine()

        # Donner de l'XP au joueur
        player_id = "default"

        # Utiliser plusieurs actions pour gagner de l'XP
        actions = [
            ("command_used", {"command": "test"}),
            ("mission_completed", {"mission_id": "test_mission", "xp": 50}),
            ("achievement_unlocked", {"achievement_id": "test_achievement", "xp": 25}),
            ("badge_earned", {"badge_id": "test_badge", "xp": 25}),
        ]

        total_xp_given = 0
        for action, metadata in actions:
            result = engine.update_player_progression(player_id, action, metadata)
            if result.get("success"):
                xp_gained = metadata.get("xp", 10)
                total_xp_given += xp_gained
                print(f"✅ Action '{action}' - +{xp_gained} XP")
            else:
                print(f"❌ Erreur action '{action}': {result.get('error')}")

        # Vérifier l'XP final
        player_data = engine.get_player_progression(player_id)
        final_xp = player_data.get("xp", 0)
        level = player_data.get("level", 1)

        game_logger.info(f"\n📊 XP total: {final_xp}")
        game_logger.info(f"📊 Niveau: {level}")
        game_logger.info(f"📈 XP donné: {total_xp_given}")

        if final_xp >= 100:
            print("✅ Le joueur a assez d'XP pour tester l'arbre de compétences !")
            return True
        else:
            print("❌ Pas assez d'XP")
            return False

    except Exception as e:
        game_logger.info(f"❌ Erreur: {e}")
        return False


def test_skill_tree_with_xp():
    """Teste l'arbre de compétences avec l'XP donné"""
    base_url = "http://127.0.0.1:5001"
    session = requests.Session()

    print("\n🧪 Test de l'arbre de compétences...")

    # Test 1: Vérifier l'arbre de compétences
    response = session.get(f"{base_url}/api/skill-tree")
    if response.status_code == 200:
        data = response.json()
        player_data = data.get("player_data", {})
        xp = player_data.get("xp", 0)
        game_logger.info(f"📊 XP du joueur: {xp}")

        if xp >= 100:
            # Test 2: Upgrade d'une compétence
            print("🔧 Test d'upgrade de compétence...")
            response = session.post(
                f"{base_url}/api/skill-tree/upgrade",
                json={"category": "hacking", "skill": "code_breaking"},
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    game_logger.info(r"✅ Upgrade réussi !")
                    print(f"📈 Nouveau niveau: {result.get('new_level')}")
                    print(f"💰 XP restant: {result.get('remaining_xp')}")
                    return True
                else:
                    print(f"❌ Échec upgrade: {result.get('error')}")
                    return False
            else:
                game_logger.info(f"❌ Erreur upgrade: {response.status_code}")
                return False
        else:
            print("❌ Pas assez d'XP pour tester l'upgrade")
            return False
    else:
        game_logger.info(f"❌ Erreur récupération arbre: {response.status_code}")
        return False


if __name__ == "__main__":
    print("🚀 Test du système d'arbre de compétences")
    print("=" * 50)

    # Étape 1: Donner de l'XP
    if give_xp_directly():
        # Étape 2: Tester l'arbre de compétences
        if test_skill_tree_with_xp():
            game_logger.info(r"\n🎉 TOUS LES TESTS SONT PASSÉS !")
            print("✨ Le système d'arbre de compétences fonctionne parfaitement !")
        else:
            print("\n❌ Échec du test de l'arbre de compétences")
    else:
        print("\n❌ Échec de l'attribution d'XP")
