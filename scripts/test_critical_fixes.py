#!/usr/bin/env python3
"""
Test des corrections critiques d'Arkalia Quest
"""

import os
import sys
import time

import requests

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def test_critical_fixes():
    """Test des corrections critiques"""
    base_url = "http://127.0.0.1:5001"
    session = requests.Session()

    game_logger.info(r"🔧 TEST DES CORRECTIONS CRITIQUES")
    print("=" * 50)

    # Test 1: Vérifier la synchronisation des stats
    game_logger.info(r"1. 🔄 Test de synchronisation des stats...")

    # Donner de l'XP via le terminal
    print("   📊 Donner de l'XP via le terminal...")
    terminal_commands = ["stats", "progression", "help", "luna"]

    for command in terminal_commands:
        response = session.post(
            f"{base_url}/api/terminal/command", json={"command": command}
        )
        if response.status_code == 200:
            print(f"   ✅ Commande '{command}' exécutée")
        else:
            print(f"   ❌ Erreur commande '{command}': {response.status_code}")
        time.sleep(0.5)

    # Vérifier les données de progression
    game_logger.info(r"   📈 Vérification des données de progression...")
    response = session.get(f"{base_url}/api/progression-data")

    if response.status_code == 200:
        data = response.json()
        progression = data.get("progression", {})

        print(f"   📊 XP: {progression.get('xp', 0)}")
        print(f"   📊 Score: {progression.get('score', 0)}")
        print(f"   📊 Niveau: {progression.get('level', 1)}")
        print(f"   📊 Badges: {len(progression.get('badges', []))}")

        if progression.get("xp", 0) > 0:
            game_logger.info(r"   ✅ Synchronisation des stats fonctionnelle")
        else:
            game_logger.info(r"   ❌ Problème de synchronisation des stats")
            return False
    else:
        game_logger.info(f"   ❌ Erreur API progression: {response.status_code}")
        return False

    # Test 2: Vérifier l'arbre de compétences
    print("\n2. 🔧 Test de l'arbre de compétences...")

    response = session.get(f"{base_url}/api/skill-tree")
    if response.status_code == 200:
        data = response.json()
        player_data = data.get("player_data", {})
        xp = player_data.get("xp", 0)

        print(f"   📊 XP dans l'arbre: {xp}")

        if xp > 0:
            # Tester l'upgrade d'une compétence
            print("   🔧 Test d'upgrade de compétence...")
            response = session.post(
                f"{base_url}/api/skill-tree/upgrade",
                json={"category": "hacking", "skill": "code_breaking"},
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    game_logger.info(r"   ✅ Upgrade de compétence réussi")
                    print(f"   📈 Nouveau niveau: {result.get('new_level')}")
                    print(f"   💰 XP restant: {result.get('remaining_xp')}")
                else:
                    print(f"   ❌ Échec upgrade: {result.get('error')}")
                    return False
            else:
                game_logger.info(f"   ❌ Erreur upgrade: {response.status_code}")
                return False
        else:
            print("   ❌ Pas d'XP pour tester l'upgrade")
            return False
    else:
        game_logger.info(f"   ❌ Erreur API skill-tree: {response.status_code}")
        return False

    # Test 3: Vérifier les systèmes JavaScript
    game_logger.info(r"\n3. 🌐 Test des systèmes JavaScript...")

    # Vérifier que les nouveaux scripts sont chargés
    response = session.get(f"{base_url}/")
    if response.status_code == 200:
        content = response.text

        scripts_to_check = [
            "unified-progression-sync.js",
            "luna-notification-manager.js",
            "ready-state-manager.js",
        ]

        for script in scripts_to_check:
            if script in content:
                game_logger.info(f"   ✅ Script {script} chargé")
            else:
                game_logger.info(f"   ❌ Script {script} manquant")
                return False
    else:
        game_logger.info(f"   ❌ Erreur chargement page: {response.status_code}")
        return False

    # Test 4: Vérifier la cohérence des données
    game_logger.info(r"\n4. 🔍 Test de cohérence des données...")

    # Récupérer les données de plusieurs sources
    progression_response = session.get(f"{base_url}/api/progression-data")
    skill_tree_response = session.get(f"{base_url}/api/skill-tree")

    if (
        progression_response.status_code == 200
        and skill_tree_response.status_code == 200
    ):
        progression_data = progression_response.json().get("progression", {})
        skill_tree_data = skill_tree_response.json().get("player_data", {})

        # Comparer les données
        xp_progression = progression_data.get("xp", 0)
        xp_skill_tree = skill_tree_data.get("xp", 0)

        game_logger.info(f"   📊 XP progression: {xp_progression}")
        game_logger.info(f"   📊 XP skill-tree: {xp_skill_tree}")

        if xp_progression == xp_skill_tree:
            game_logger.info(r"   ✅ Données cohérentes entre les APIs")
        else:
            game_logger.info(r"   ❌ Incohérence des données entre les APIs")
            return False
    else:
        game_logger.info(r"   ❌ Erreur récupération des données")
        return False

    game_logger.info(r"\n🎉 TOUS LES TESTS SONT PASSÉS !")
    game_logger.info(r"✅ Les corrections critiques fonctionnent parfaitement !")
    return True


def main():
    """Fonction principale"""
    try:
        success = test_critical_fixes()
        if success:
            game_logger.info(r"\n🚀 Les corrections critiques sont opérationnelles !")
            game_logger.info(r"📋 Prochaines étapes recommandées :")
            print("   1. Tester l'interface web manuellement")
            game_logger.info(
                r"   2. Vérifier que les notifications LUNA ne sont plus redondantes"
            )
            print("   3. Confirmer que les blocs 'Prêt à commencer !' disparaissent")
            game_logger.info(r"   4. Valider la synchronisation en temps réel")
        else:
            game_logger.info(
                r"\n❌ Des problèmes persistent dans les corrections critiques"
            )
            game_logger.info(r"📋 Actions recommandées :")
            game_logger.info(r"   1. Vérifier les logs du serveur")
            game_logger.info(r"   2. Contrôler la console du navigateur")
            game_logger.info(r"   3. Tester les APIs individuellement")

        return 0 if success else 1
    except Exception as e:
        game_logger.info(f"\n❌ Erreur lors du test: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
