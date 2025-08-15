#!/usr/bin/env python3
"""
Test de debug pour identifier l'erreur dans charger_profil
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from arkalia_engine import arkalia_engine
    print("✅ Import arkalia_engine réussi")

    try:
        profil = arkalia_engine.profiles.load_main_profile()
        print("✅ load_main_profile réussi")
        print(f"Profil: {profil}")

        # Test de l'ID utilisateur
        user_id = profil.get("id", "default")
        print(f"User ID: {user_id} (type: {type(user_id)})")

    except Exception as e:
        print(f"❌ Erreur load_main_profile: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Erreur import arkalia_engine: {e}")
    import traceback
    traceback.print_exc()
