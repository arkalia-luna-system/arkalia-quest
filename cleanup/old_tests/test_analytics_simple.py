#!/usr/bin/env python3
"""
Test simple du système d'analytics pour identifier les erreurs
"""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.analytics_engine import analytics_engine
    print("✅ Import analytics_engine réussi")

    # Test simple d'insights
    try:
        insights = analytics_engine.get_user_insights("test_user")
        print("✅ get_user_insights réussi")
        print(f"Insights: {insights}")
    except Exception as e:
        print(f"❌ Erreur get_user_insights: {e}")
        import traceback
        traceback.print_exc()

    # Test simple d'analytics globaux
    try:
        analytics = analytics_engine.get_global_analytics()
        print("✅ get_global_analytics réussi")
        print(f"Analytics: {analytics}")
    except Exception as e:
        print(f"❌ Erreur get_global_analytics: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Erreur import: {e}")
    import traceback
    traceback.print_exc()
