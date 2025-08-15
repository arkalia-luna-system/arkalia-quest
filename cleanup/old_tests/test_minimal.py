#!/usr/bin/env python3
"""Test minimal pour diagnostiquer le problème"""

print("🚀 Test import minimal...")

try:
    from flask import Flask

    print("✅ Flask OK")
except Exception as e:
    print(f"❌ Flask: {e}")

try:
    print("✅ arkalia_engine OK")
except Exception as e:
    print(f"❌ arkalia_engine: {e}")

try:
    print("✅ command_handler_v2 OK")
except Exception as e:
    print(f"❌ command_handler_v2: {e}")

try:
    print("✅ gamification_engine OK")
except Exception as e:
    print(f"❌ gamification_engine: {e}")

try:
    print("✅ database OK")
except Exception as e:
    print(f"❌ database: {e}")

try:
    print("✅ websocket_manager OK")
except Exception as e:
    print(f"❌ websocket_manager: {e}")

try:
    print("✅ tutorial_manager OK")
except Exception as e:
    print(f"❌ tutorial_manager: {e}")

print("🎯 Test de création minimal Flask...")
try:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "OK"

    print("✅ App Flask créée")
    app.run(debug=True, host="0.0.0.0", port=5001)

except Exception as e:
    print(f"❌ Erreur Flask: {e}")
    import traceback

    traceback.print_exc()
