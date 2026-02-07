#!/usr/bin/env python3
"""
Test du skill tree après corrections
"""

import os
import sys

import requests

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_skill_tree():
    """Test du skill tree"""
    base_url = "http://127.0.0.1:5001"

    print("🧪 Test du Skill Tree après corrections")
    print("=" * 50)

    # Vérifier que le serveur est en cours d'exécution
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code != 200:
            print(
                "❌ Le serveur n'est pas accessible. Veuillez lancer 'python app.py' d'abord."
            )
            return
    except requests.exceptions.RequestException:
        print(
            "❌ Le serveur n'est pas accessible. Veuillez lancer 'python app.py' d'abord."
        )
        return

    # Test 1: Récupérer les données du skill tree
    print("\n1. Test récupération des données du skill tree...")
    try:
        response = requests.get(f"{base_url}/api/skill-tree", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Données du skill tree récupérées avec succès")
            print(f"   - Succès: {data.get('success')}")
            print(f"   - Compétences disponibles: {len(data.get('skill_tree', {}))}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return

    # Test 2: Tester l'amélioration d'une compétence
    print("\n2. Test amélioration d'une compétence...")
    try:
        upgrade_data = {"category": "hacking", "skill": "code_breaking"}

        response = requests.post(
            f"{base_url}/api/skill-tree/upgrade",
            json=upgrade_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Amélioration de compétence réussie")
            print(f"   - Succès: {result.get('success')}")
            print(f"   - Nouveau niveau: {result.get('new_level')}")
            print(f"   - XP restant: {result.get('remaining_xp')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   - Message: {response.text}")
    except Exception as e:
        print(f"❌ Erreur lors de l'amélioration: {e}")

    # Test 3: Vérifier la synchronisation des données
    print("\n3. Test synchronisation des données...")
    try:
        response = requests.get(f"{base_url}/api/sync-progression", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Synchronisation réussie")
            print(f"   - Succès: {data.get('success')}")
            print(f"   - XP du joueur: {data.get('player_data', {}).get('xp', 0)}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation: {e}")

    # Test 4: Vérifier l'accès à la page skill tree
    print("\n4. Test accès à la page skill tree...")
    try:
        response = requests.get(f"{base_url}/skill-tree", timeout=10)
        if response.status_code == 200:
            print("✅ Page skill tree accessible")
            print(f"   - Taille de la page: {len(response.text)} caractères")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur d'accès à la page: {e}")

    print("\n" + "=" * 50)
    print("🎯 Test terminé !")


if __name__ == "__main__":
    test_skill_tree()
