#!/usr/bin/env python3
"""
Test complet du système d'arbre de compétences
"""


import requests


def test_complete_system():
    """Test complet du système"""
    base_url = "http://127.0.0.1:5001"
    session = requests.Session()  # Utiliser une session pour maintenir les cookies

    print(r"🧪 Test complet du système Arkalia Quest")
    print("=" * 50)

    # Test 1: Donner de l'XP au joueur via le terminal
    print("1. Donner de l'XP au joueur...")
    response = session.post(
        f"{base_url}/api/terminal/command", json={"command": "stats"}
    )

    if response.status_code == 200:
        print(r"✅ Commande terminal exécutée")
    else:
        print(f"❌ Erreur terminal: {response.status_code}")
        return False

    # Test 2: Vérifier l'arbre de compétences
    print("\n2. Vérification de l'arbre de compétences...")
    response = session.get(f"{base_url}/api/skill-tree")

    if response.status_code == 200:
        data = response.json()
        print(r"✅ Arbre de compétences récupéré")

        # Afficher les données du joueur
        player_data = data.get("player_data", {})
        print(f"📊 XP du joueur: {player_data.get('xp', 0)}")
        print(f"📊 Niveau: {player_data.get('level', 1)}")

        # Vérifier les compétences
        skill_tree = data.get("skill_tree", {})
        if "hacking" in skill_tree:
            code_breaking = skill_tree["hacking"]["skills"]["code_breaking"]
            print(f"🔧 Code Breaking - Niveau: {code_breaking.get('level', 0)}")
            print(
                f"🔧 Code Breaking - Débloqué: {code_breaking.get('unlocked', False)}"
            )
    else:
        print(f"❌ Erreur arbre de compétences: {response.status_code}")
        return False

    # Test 3: Upgrade d'une compétence
    print("\n3. Test d'upgrade de compétence...")
    response = session.post(
        f"{base_url}/api/skill-tree/upgrade",
        json={"category": "hacking", "skill": "code_breaking"},
    )

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(r"✅ Upgrade réussi !")
            print(f"📈 Nouveau niveau: {result.get('new_level')}")
            print(f"💰 XP restant: {result.get('remaining_xp')}")
            print(f"💸 Coût XP: {result.get('xp_cost')}")
        else:
            print(f"❌ Échec upgrade: {result.get('error')}")
            return False
    else:
        print(f"❌ Erreur upgrade: {response.status_code}")
        return False

    # Test 4: Vérifier la synchronisation
    print(r"\n4. Vérification de la synchronisation...")
    response = session.get(f"{base_url}/api/skill-tree")

    if response.status_code == 200:
        data = response.json()
        code_breaking = data["skill_tree"]["hacking"]["skills"]["code_breaking"]

        if code_breaking.get("level") > 0:
            print(r"✅ Synchronisation réussie")
            print(f"🔧 Niveau actuel: {code_breaking.get('level')}")
        else:
            print(r"❌ Problème de synchronisation")
            return False
    else:
        print(r"❌ Erreur vérification")
        return False

    print(r"\n🎉 TOUS LES TESTS SONT PASSÉS !")
    print("✨ Le système d'arbre de compétences fonctionne parfaitement !")
    return True


if __name__ == "__main__":
    try:
        success = test_complete_system()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        exit(1)
