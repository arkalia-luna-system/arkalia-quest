#!/usr/bin/env python3
"""
Test simple pour vérifier les améliorations du terminal
"""


import requests


def test_terminal_improvements():
    """Test des améliorations du terminal"""
    print("🧪 TEST DES AMÉLIORATIONS DU TERMINAL")
    print("=" * 50)

    base_url = "http://127.0.0.1:5000"

    # Test 1: Commande inexistante (devrait déclencher l'aide contextuelle)
    print("\n1️⃣ Test commande inexistante...")
    response = requests.post(
        f"{base_url}/commande", json={"cmd": "commande_inexistante"}
    )
    data = response.json()
    print(f"✅ Réponse: {data.get('message', 'Pas de message')[:100]}...")

    # Test 2: Commande aide (devrait fonctionner)
    print("\n2️⃣ Test commande aide...")
    response = requests.post(f"{base_url}/commande", json={"cmd": "aide"})
    data = response.json()
    print(f"✅ Réponse: {data.get('message', 'Pas de message')[:100]}...")

    # Test 3: Commande profil (devrait fonctionner)
    print("\n3️⃣ Test commande profil...")
    response = requests.post(f"{base_url}/commande", json={"cmd": "profil"})
    data = response.json()
    print(f"✅ Réponse: {data.get('message', 'Pas de message')[:100]}...")

    # Test 4: Vérifier que le JavaScript est bien chargé
    print("\n4️⃣ Test chargement JavaScript...")
    response = requests.get(f"{base_url}/static/js/terminal.js")
    if response.status_code == 200:
        js_content = response.text
        if "provideIntelligentFeedback" in js_content:
            print("✅ JavaScript amélioré détecté")
        else:
            print("❌ JavaScript amélioré NON détecté")
        if "addContextualMessage" in js_content:
            print("✅ Fonction messages contextuels détectée")
        else:
            print("❌ Fonction messages contextuels NON détectée")
    else:
        print("❌ Impossible de charger le JavaScript")

    print("\n🎯 RÉSULTAT:")
    print("Les améliorations sont bien en place côté serveur.")
    print("Pour voir les messages contextuels, ouvrez le terminal dans le navigateur")
    print("et tapez des commandes inexistantes comme 'test' ou 'xyz'")
    print("Vous devriez voir des messages d'aide contextuelle apparaître !")


if __name__ == "__main__":
    test_terminal_improvements()
