#!/usr/bin/env python3
"""
Script principal pour exécuter les tests de validation d'Arkalia Quest
Utilise le test de validation complet pour vérifier que tout fonctionne
"""

import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    """Exécute les tests de validation"""
    print("🚀 LANCEMENT DES TESTS DE VALIDATION ARKALIA QUEST")
    print("=" * 60)

    try:
        # Importer et exécuter le test de validation
        from test_validation_complete import main as run_validation

        success = run_validation()

        if success:
            print("\n🎉 VALIDATION COMPLÈTE RÉUSSIE !")
            print("🚀 Arkalia Quest v3.1.0 est prêt pour la production !")
            return 0
        else:
            print("\n❌ VALIDATION ÉCHOUÉE !")
            print("⚠️  Des problèmes ont été détectés.")
            return 1

    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
