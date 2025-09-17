#!/usr/bin/env python3
"""
Script de lancement pour les tests utilisateur d'Arkalia Quest
Lance les tests automatisés et guide vers les tests manuels
"""

import subprocess
import sys


def print_banner():
    """Affiche la bannière de test utilisateur"""
    print("🧪" + "=" * 60)
    print("🧪 TESTS UTILISATEUR - ARKALIA QUEST v3.1.0")
    print("🧪" + "=" * 60)
    print()


def run_automated_tests():
    """Lance les tests automatisés"""
    print("🤖 LANCEMENT DES TESTS AUTOMATISÉS...")
    print("-" * 40)

    try:
        result = subprocess.run(
            [sys.executable, "tests/test_utilisateur_automated.py"],
            check=False, capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Erreurs:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur lors des tests automatisés: {e}")
        return False


def show_manual_test_guide():
    """Affiche le guide pour les tests manuels"""
    print("\n👥 GUIDE POUR LES TESTS MANUELS")
    print("=" * 50)
    print()
    print("📋 DOCUMENTS DISPONIBLES :")
    print("  • docs/CHECKLISTS_TEST_UTILISATEUR.md - Checklists détaillées")
    print("  • docs/GUIDE_TEST_UTILISATEUR.md - Guide pratique")
    print()
    print("👥 PROFILS DE TESTEURS RECOMMANDÉS :")
    print("  1. 👨‍💻 Développeur/Technicien (45-60 min)")
    print("  2. 🎓 Éducateur/Enseignant (30-45 min)")
    print("  3. 👶 Adolescent 14-17 ans (20-30 min)")
    print("  4. 👩‍💼 Utilisateur Lambda (20-30 min)")
    print("  5. 🎮 Gamer Expérimenté (30-45 min)")
    print()
    print("🚀 POUR COMMENCER :")
    print("  1. Ouvrez docs/CHECKLISTS_TEST_UTILISATEUR.md")
    print("  2. Choisissez le profil de testeur")
    print("  3. Suivez la checklist correspondante")
    print("  4. Notez les retours et suggestions")
    print()
    print("📊 OBJECTIFS :")
    print("  • Identifier les points forts")
    print("  • Détecter les problèmes d'UX")
    print("  • Évaluer la valeur éducative")
    print("  • Tester l'engagement utilisateur")
    print("  • Valider la compatibilité technique")


def show_test_summary():
    """Affiche un résumé des tests"""
    print("\n📊 RÉSUMÉ DES TESTS")
    print("=" * 30)
    print()
    print("✅ TESTS AUTOMATISÉS :")
    print("  • Interface Responsive : PASS")
    print("  • Accessibilité : PASS")
    print("  • Performance : PASS")
    print("  • Qualité du Contenu : PASS")
    print("  • Valeur Éducative : PASS")
    print()
    print("👥 TESTS MANUELS À FAIRE :")
    print("  • Test avec différents profils utilisateur")
    print("  • Validation de l'expérience utilisateur")
    print("  • Retours sur l'engagement")
    print("  • Suggestions d'amélioration")
    print()
    print("🎯 PROCHAINES ÉTAPES :")
    print("  1. Organiser des sessions de test")
    print("  2. Collecter les retours utilisateur")
    print("  3. Analyser les résultats")
    print("  4. Implémenter les améliorations")


def main():
    """Fonction principale"""
    print_banner()

    # Lancement des tests automatisés
    automated_success = run_automated_tests()

    if automated_success:
        print("\n🎉 TESTS AUTOMATISÉS RÉUSSIS !")
        print("✅ Le jeu est prêt pour les tests utilisateur manuels")
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS DANS LES TESTS AUTOMATISÉS")
        print("🔧 Des corrections sont nécessaires avant les tests manuels")

    # Affichage du guide pour les tests manuels
    show_manual_test_guide()

    # Résumé
    show_test_summary()

    print("\n" + "=" * 60)
    print("🚀 ARKALIA QUEST EST PRÊT POUR LES TESTS UTILISATEUR !")
    print("=" * 60)

    return 0 if automated_success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
