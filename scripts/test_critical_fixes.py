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

    print("🔧 TEST DES CORRECTIONS CRITIQUES")
    print("=" * 50)

    # Test 1: Vérifier la synchronisation des stats
    print("1. 🔄 Test de synchronisation des stats...")

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
    print("   📈 Vérification des données de progression...")
    response = session.get(f"{base_url}/api/progression-data")

    if response.status_code == 200:
        data = response.json()
        progression = data.get("progression", {})

        print(f"   📊 XP: {progression.get('xp', 0)}")
        print(f"   📊 Score: {progression.get('score', 0)}")
        print(f"   📊 Niveau: {progression.get('level', 1)}")
        print(f"   📊 Badges: {len(progression.get('badges', []))}")

        if progression.get("xp", 0) > 0:
            print("   ✅ Synchronisation des stats fonctionnelle")
        else:
            print("   ❌ Problème de synchronisation des stats")
            return False
    else:
        print(f"   ❌ Erreur API progression: {response.status_code}")
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
                    print("   ✅ Upgrade de compétence réussi")
                    print(f"   📈 Nouveau niveau: {result.get('new_level')}")
                    print(f"   💰 XP restant: {result.get('remaining_xp')}")
                else:
                    print(f"   ❌ Échec upgrade: {result.get('error')}")
                    return False
            else:
                print(f"   ❌ Erreur upgrade: {response.status_code}")
                return False
        else:
            print("   ❌ Pas d'XP pour tester l'upgrade")
            return False
    else:
        print(f"   ❌ Erreur API skill-tree: {response.status_code}")
        return False

    # Test 3: Vérifier les systèmes JavaScript
    print("\n3. 🌐 Test des systèmes JavaScript...")

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
                print(f"   ✅ Script {script} chargé")
            else:
                print(f"   ❌ Script {script} manquant")
                return False
    else:
        print(f"   ❌ Erreur chargement page: {response.status_code}")
        return False

    # Test 4: Vérifier la cohérence des données
    print("\n4. 🔍 Test de cohérence des données...")

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

        print(f"   📊 XP progression: {xp_progression}")
        print(f"   📊 XP skill-tree: {xp_skill_tree}")

        if xp_progression == xp_skill_tree:
            print("   ✅ Données cohérentes entre les APIs")
        else:
            print("   ❌ Incohérence des données entre les APIs")
            return False
    else:
        print("   ❌ Erreur récupération des données")
        return False

    print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
    print("✅ Les corrections critiques fonctionnent parfaitement !")
    return True


def main():
    """Fonction principale"""
    try:
        success = test_critical_fixes()
        if success:
            print("\n🚀 Les corrections critiques sont opérationnelles !")
            print("📋 Prochaines étapes recommandées :")
            print("   1. Tester l'interface web manuellement")
            print("   2. Vérifier que les notifications LUNA ne sont plus redondantes")
            print("   3. Confirmer que les blocs 'Prêt à commencer !' disparaissent")
            print("   4. Valider la synchronisation en temps réel")
        else:
            print("\n❌ Des problèmes persistent dans les corrections critiques")
            print("📋 Actions recommandées :")
            print("   1. Vérifier les logs du serveur")
            print("   2. Contrôler la console du navigateur")
            print("   3. Tester les APIs individuellement")

        return 0 if success else 1
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
