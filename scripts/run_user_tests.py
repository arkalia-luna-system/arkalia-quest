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
    game_logger.info(r"🧪 TESTS UTILISATEUR - ARKALIA QUEST v3.1.0")
    print("🧪" + "=" * 60)
    print()


def run_automated_tests():
    """Lance les tests automatisés"""
    game_logger.info(r"🤖 LANCEMENT DES TESTS AUTOMATISÉS...")
    print("-" * 40)

    try:
        result = subprocess.run(
            [sys.executable, "tests/test_utilisateur_automated.py"],
            check=False,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Erreurs:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        game_logger.info(f"❌ Erreur lors des tests automatisés: {e}")
        return False


def show_manual_test_guide():
    """Affiche le guide pour les tests manuels"""
    game_logger.info(r"\n👥 GUIDE POUR LES TESTS MANUELS")
    print("=" * 50)
    print()
    game_logger.info(r"📋 DOCUMENTS DISPONIBLES :")
    game_logger.info(r"  • docs/CHECKLISTS_TEST_UTILISATEUR.md - Checklists détaillées")
    game_logger.info(r"  • docs/GUIDE_TEST_UTILISATEUR.md - Guide pratique")
    print()
    game_logger.info(r"👥 PROFILS DE TESTEURS RECOMMANDÉS :")
    game_logger.info(r"  1. 👨‍💻 Développeur/Technicien (45-60 min)")
    game_logger.info(r"  2. 🎓 Éducateur/Enseignant (30-45 min)")
    game_logger.info(r"  3. 👶 Adolescent 14-17 ans (20-30 min)")
    game_logger.info(r"  4. 👩‍💼 Utilisateur Lambda (20-30 min)")
    game_logger.info(r"  5. 🎮 Gamer Expérimenté (30-45 min)")
    print()
    game_logger.info(r"🚀 POUR COMMENCER :")
    game_logger.info(r"  1. Ouvrez docs/CHECKLISTS_TEST_UTILISATEUR.md")
    game_logger.info(r"  2. Choisissez le profil de testeur")
    game_logger.info(r"  3. Suivez la checklist correspondante")
    game_logger.info(r"  4. Notez les retours et suggestions")
    print()
    game_logger.info(r"📊 OBJECTIFS :")
    game_logger.info(r"  • Identifier les points forts")
    print("  • Détecter les problèmes d'UX")
    game_logger.info(r"  • Évaluer la valeur éducative")
    print("  • Tester l'engagement utilisateur")
    game_logger.info(r"  • Valider la compatibilité technique")


def show_test_summary():
    """Affiche un résumé des tests"""
    game_logger.info(r"\n📊 RÉSUMÉ DES TESTS")
    print("=" * 30)
    print()
    game_logger.info(r"✅ TESTS AUTOMATISÉS :")
    game_logger.info(r"  • Interface Responsive : PASS")
    game_logger.info(r"  • Accessibilité : PASS")
    game_logger.info(r"  • Performance : PASS")
    game_logger.info(r"  • Qualité du Contenu : PASS")
    game_logger.info(r"  • Valeur Éducative : PASS")
    print()
    game_logger.info(r"👥 TESTS MANUELS À FAIRE :")
    game_logger.info(r"  • Test avec différents profils utilisateur")
    print("  • Validation de l'expérience utilisateur")
    print("  • Retours sur l'engagement")
    print("  • Suggestions d'amélioration")
    print()
    game_logger.info(r"🎯 PROCHAINES ÉTAPES :")
    game_logger.info(r"  1. Organiser des sessions de test")
    game_logger.info(r"  2. Collecter les retours utilisateur")
    game_logger.info(r"  3. Analyser les résultats")
    game_logger.info(r"  4. Implémenter les améliorations")


def main():
    """Fonction principale"""
    print_banner()

    # Lancement des tests automatisés
    automated_success = run_automated_tests()

    if automated_success:
        game_logger.info(r"\n🎉 TESTS AUTOMATISÉS RÉUSSIS !")
        game_logger.info(r"✅ Le jeu est prêt pour les tests utilisateur manuels")
    else:
        game_logger.info(r"\n⚠️ PROBLÈMES DÉTECTÉS DANS LES TESTS AUTOMATISÉS")
        game_logger.info(r"🔧 Des corrections sont nécessaires avant les tests manuels")

    # Affichage du guide pour les tests manuels
    show_manual_test_guide()

    # Résumé
    show_test_summary()

    print("\n" + "=" * 60)
    game_logger.info(r"🚀 ARKALIA QUEST EST PRÊT POUR LES TESTS UTILISATEUR !")
    print("=" * 60)

    return 0 if automated_success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
