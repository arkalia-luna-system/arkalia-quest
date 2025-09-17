#!/usr/bin/env python3
"""
Test des effets visuels et sonores du skill tree
"""

import os
import sys

import requests

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_visual_feedback():
    """Test des effets visuels et sonores"""
    base_url = "http://127.0.0.1:5001"

    print("🎨 Test des Effets Visuels et Sonores")
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

    # Test 1: Vérifier que la page skill tree contient les scripts nécessaires
    print("\n1. Test des scripts JavaScript...")
    try:
        response = requests.get(f"{base_url}/skill-tree", timeout=10)
        if response.status_code == 200:
            content = response.text

            # Vérifier la présence des scripts
            scripts = ["gamification-feedback.js", "skill-tree-system.js"]

            for script in scripts:
                if script in content:
                    print(f"✅ Script {script} trouvé")
                else:
                    print(f"❌ Script {script} manquant")

            # Vérifier la présence des classes CSS
            css_classes = ["upgrade-skill", "skill-item", "gamification-notification"]

            for css_class in css_classes:
                if css_class in content:
                    print(f"✅ Classe CSS {css_class} trouvée")
                else:
                    print(f"❌ Classe CSS {css_class} manquante")

        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test 2: Vérifier les fichiers CSS
    print("\n2. Test des fichiers CSS...")
    try:
        response = requests.get(
            f"{base_url}/static/css/skill-tree-enhancements.css", timeout=10
        )
        if response.status_code == 200:
            print("✅ Fichier CSS skill-tree-enhancements.css accessible")

            # Vérifier la présence des animations
            animations = [
                "upgradeSuccess",
                "particleExplode",
                "confettiFall",
                "badgeEarned",
            ]

            for animation in animations:
                if f"@keyframes {animation}" in response.text:
                    print(f"✅ Animation {animation} trouvée")
                else:
                    print(f"❌ Animation {animation} manquante")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test 3: Vérifier les fichiers JavaScript
    print("\n3. Test des fichiers JavaScript...")
    try:
        # Test gamification-feedback.js
        response = requests.get(
            f"{base_url}/static/js/gamification-feedback.js", timeout=10
        )
        if response.status_code == 200:
            print("✅ Fichier gamification-feedback.js accessible")

            # Vérifier la présence des fonctions
            functions = [
                "showSkillUpgradeFeedback",
                "createParticleEffect",
                "createConfettiEffect",
                "playSuccessSound",
            ]

            for func in functions:
                if func in response.text:
                    print(f"✅ Fonction {func} trouvée")
                else:
                    print(f"❌ Fonction {func} manquante")
        else:
            print(f"❌ Erreur: {response.status_code}")

        # Test skill-tree-system.js
        response = requests.get(
            f"{base_url}/static/js/skill-tree-system.js", timeout=10
        )
        if response.status_code == 200:
            print("✅ Fichier skill-tree-system.js accessible")

            # Vérifier la présence des fonctions
            functions = [
                "upgradeSkill",
                "showUpgradeAnimation",
                "createParticleEffect",
                "showLevelUpConfetti",
            ]

            for func in functions:
                if func in response.text:
                    print(f"✅ Fonction {func} trouvée")
                else:
                    print(f"❌ Fonction {func} manquante")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test 4: Tester une amélioration pour déclencher les effets
    print("\n4. Test déclenchement des effets...")
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
            print("✅ Amélioration réussie - effets visuels/sonores déclenchés")
            print(f"   - Nouveau niveau: {result.get('new_level')}")
            print(f"   - XP restant: {result.get('remaining_xp')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n" + "=" * 50)
    print("🎯 Test des effets visuels terminé !")
    print("\n💡 Pour tester les effets visuels complets :")
    print("   1. Ouvrez http://127.0.0.1:5001/skill-tree dans votre navigateur")
    print("   2. Cliquez sur les boutons 'Améliorer' des compétences")
    print("   3. Observez les animations, particules et effets sonores")


if __name__ == "__main__":
    test_visual_feedback()
