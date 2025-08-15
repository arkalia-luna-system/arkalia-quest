#!/usr/bin/env python3
"""
Test de debug pour identifier l'erreur exacte dans analytics
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.analytics_engine import analytics_engine
    print("✅ Import analytics_engine réussi")

    # Test avec un ID utilisateur simple
    user_id = "2"
    print(f"Testing with user_id: {user_id} (type: {type(user_id)})")

    try:
        insights = analytics_engine.get_user_insights(user_id)
        print("✅ get_user_insights réussi")
        print(f"Insights: {insights}")
    except Exception as e:
        print(f"❌ Erreur get_user_insights: {e}")
        import traceback
        traceback.print_exc()

        # Test de la fonction d'anonymisation
        try:
            anonymized = analytics_engine._anonymize_user_id(user_id)
            print(f"✅ Anonymisation réussie: {anonymized}")
        except Exception as e2:
            print(f"❌ Erreur anonymisation: {e2}")

        # Test de l'analyse du style d'apprentissage
        try:
            style = analytics_engine._analyze_learning_style(user_id)
            print(f"✅ Analyse style réussie: {style}")
        except Exception as e3:
            print(f"❌ Erreur analyse style: {e3}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"❌ Erreur import: {e}")
    import traceback
    traceback.print_exc()
