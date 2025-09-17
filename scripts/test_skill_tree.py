#!/usr/bin/env python3
"""
Test spécifique pour l'arbre de compétences
"""

import time

import requests


def test_skill_tree_api():
    """Test de l'API de l'arbre de compétences"""
    base_url = "http://127.0.0.1:5001"

    print("🧪 Test de l'API Skill Tree")
    print("=" * 40)

    # Test 1: Récupérer l'arbre de compétences
    print("1. Récupération de l'arbre de compétences...")
    response = requests.get(f"{base_url}/api/skill-tree")
    if response.status_code == 200:
        data = response.json()
        game_logger.info(r"✅ API skill-tree fonctionne")

        # Vérifier la structure
        if "skill_tree" in data and "hacking" in data["skill_tree"]:
            game_logger.info(r"✅ Structure de données correcte")

            # Vérifier les compétences
            hacking_skills = data["skill_tree"]["hacking"]["skills"]
            game_logger.info(f"📊 Compétences hacking: {list(hacking_skills.keys())}")

            # Vérifier code_breaking
            code_breaking = hacking_skills.get("code_breaking", {})
            print(f"🔧 Code Breaking - Niveau: {code_breaking.get('level', 0)}")
            print(
                f"🔧 Code Breaking - Débloqué: {code_breaking.get('unlocked', False)}"
            )
        else:
            game_logger.info(r"❌ Structure de données incorrecte")
            return False
    else:
        game_logger.info(f"❌ Erreur API: {response.status_code}")
        return False

    # Test 2: Upgrade d'une compétence
    print("\n2. Test d'upgrade de compétence...")
    upgrade_data = {"category": "hacking", "skill": "code_breaking"}

    response = requests.post(
        f"{base_url}/api/skill-tree/upgrade",
        json=upgrade_data,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            game_logger.info(r"✅ Upgrade réussi !")
            print(f"📈 Nouveau niveau: {result.get('new_level')}")
            print(f"💰 XP restant: {result.get('remaining_xp')}")
            print(f"💸 Coût XP: {result.get('xp_cost')}")
        else:
            print(f"❌ Échec upgrade: {result.get('error')}")
            return False
    else:
        game_logger.info(f"❌ Erreur upgrade: {response.status_code}")
        return False

    # Test 3: Vérifier la synchronisation
    game_logger.info(r"\n3. Vérification de la synchronisation...")
    time.sleep(1)  # Attendre un peu

    response = requests.get(f"{base_url}/api/skill-tree")
    if response.status_code == 200:
        data = response.json()
        code_breaking = data["skill_tree"]["hacking"]["skills"]["code_breaking"]

        if code_breaking.get("level") > 0:
            game_logger.info(r"✅ Synchronisation réussie")
            print(f"🔧 Niveau actuel: {code_breaking.get('level')}")
        else:
            game_logger.info(r"❌ Problème de synchronisation")
            return False
    else:
        game_logger.info(r"❌ Erreur vérification")
        return False

    # Test 4: Test des données de progression
    game_logger.info(r"\n4. Test des données de progression...")
    response = requests.get(f"{base_url}/api/progression-data")
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            progression = data.get("progression", {})
            game_logger.info(r"✅ Données de progression récupérées")
            print(f"📊 Niveau joueur: {progression.get('level')}")
            print(f"⭐ XP total: {progression.get('xp')}")
            print(f"🏆 Badges: {len(progression.get('badges', []))}")
        else:
            game_logger.info(r"❌ Erreur données de progression")
            return False
    else:
        game_logger.info(r"❌ Erreur API progression")
        return False

    game_logger.info(r"\n🎉 TOUS LES TESTS SONT PASSÉS !")
    print("✨ L'arbre de compétences fonctionne parfaitement !")
    return True


if __name__ == "__main__":
    try:
        success = test_skill_tree_api()
        exit(0 if success else 1)
    except Exception as e:
        game_logger.info(f"❌ Erreur lors du test: {e}")
        exit(1)
