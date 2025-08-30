"""
Core module pour Arkalia Quest
Contient les modules avancés : database, websocket_manager, tutorial_manager
"""

# Import des modules principaux
try:
    from .database import db_manager
    from .tutorial_manager import tutorial_manager
    from .websocket_manager import websocket_manager

    __all__ = ["db_manager", "tutorial_manager", "websocket_manager"]

except ImportError as e:
    print(f"⚠️ Erreur import module core: {e}")

    # Créer des objets factices pour éviter les erreurs
    class DummyManager:
        def __getattr__(self, name):
            return lambda *_args, **_kwargs: {"error": "Module not available"}

    db_manager = DummyManager()
    websocket_manager = DummyManager()
    tutorial_manager = DummyManager()

    __all__ = ["db_manager", "tutorial_manager", "websocket_manager"]
