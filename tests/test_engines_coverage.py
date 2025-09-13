#!/usr/bin/env python3
"""
🧪 Tests de couverture pour les modules engines
Tests basiques pour améliorer la couverture de code
"""

import os
import sys
import tempfile
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from engines import EffectsEngine as EffectsEngineImport
    from engines import LunaAI as LunaAIImport
    from engines.effects_engine import EffectsEngine
    from engines.luna_ai import LunaAI
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)


class TestEnginesCoverage(unittest.TestCase):
    """Tests de couverture pour les modules engines"""

    def setUp(self):
        """Initialisation avant chaque test"""
        # Créer un répertoire temporaire pour les effets
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Nettoyage après chaque test"""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_effects_engine_initialization(self):
        """Test d'initialisation de EffectsEngine"""
        # Test avec répertoire par défaut
        engine = EffectsEngine()
        self.assertIsNotNone(engine)
        self.assertIsInstance(engine.effects_dir, str)
        self.assertIsInstance(engine.ascii_arts, dict)
        self.assertIsInstance(engine.sounds, dict)
        self.assertIsInstance(engine.animations, dict)
        self.assertIsInstance(engine.default_effects, dict)

    def test_effects_engine_custom_directory(self):
        """Test d'initialisation avec répertoire personnalisé"""
        engine = EffectsEngine(effects_dir=self.temp_dir)
        self.assertEqual(engine.effects_dir, self.temp_dir)

    def test_effects_engine_load_ascii_arts(self):
        """Test du chargement des arts ASCII"""
        engine = EffectsEngine()
        ascii_arts = engine.load_ascii_arts()
        self.assertIsInstance(ascii_arts, dict)

    def test_effects_engine_load_sounds(self):
        """Test du chargement des sons"""
        engine = EffectsEngine()
        sounds = engine.load_sounds()
        self.assertIsInstance(sounds, dict)

    def test_effects_engine_load_animations(self):
        """Test du chargement des animations"""
        engine = EffectsEngine()
        animations = engine.load_animations()
        self.assertIsInstance(animations, dict)

    def test_effects_engine_get_default_ascii(self):
        """Test de récupération d'ASCII par défaut"""
        engine = EffectsEngine()
        ascii_art = engine.get_default_ascii("success")
        self.assertIsInstance(ascii_art, str)
        self.assertGreater(len(ascii_art), 0)

    def test_effects_engine_generate_effect(self):
        """Test de génération d'effet"""
        engine = EffectsEngine()
        effect = engine.generate_effect("success", {"message": "Test"})
        self.assertIsInstance(effect, dict)
        self.assertIn("ascii_art", effect)
        self.assertIn("sound", effect)
        self.assertIn("animation", effect)

    def test_effects_engine_personalize_effect(self):
        """Test de personnalisation d'effet"""
        engine = EffectsEngine()
        base_effect = engine.default_effects["success"]
        personalized = engine.personalize_effect(base_effect, "hacker_creatif")
        self.assertIsInstance(personalized, dict)

    def test_luna_ai_initialization(self):
        """Test d'initialisation de LunaAI"""
        ai = LunaAI()
        self.assertIsNotNone(ai)
        self.assertIsInstance(ai.personality, str)
        self.assertIsInstance(ai.mood, str)
        self.assertIsInstance(ai.relationship_level, int)

    def test_luna_ai_respond(self):
        """Test de réponse de LunaAI"""
        ai = LunaAI()
        # Utiliser la méthode respond avec les bons paramètres
        response = ai.respond("Hello", {"user_personality": "hacker_creatif"}, {})
        self.assertIsInstance(response, dict)
        self.assertIn("message", response)

    def test_luna_ai_classify_message(self):
        """Test de classification de message"""
        ai = LunaAI()
        message_type = ai.classify_message("Hello")
        self.assertIsInstance(message_type, str)
        self.assertGreater(len(message_type), 0)

    def test_luna_ai_generate_response(self):
        """Test de génération de réponse avec contexte"""
        ai = LunaAI()
        context = {"message_type": "greeting", "user_personality": "hacker_creatif"}
        response = ai.generate_response(context)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_engines_module_imports(self):
        """Test des imports du module engines"""
        # Test que les imports fonctionnent
        self.assertIsNotNone(EffectsEngineImport)
        self.assertIsNotNone(LunaAIImport)

        # Test que les classes sont les mêmes
        self.assertEqual(EffectsEngine, EffectsEngineImport)
        self.assertEqual(LunaAI, LunaAIImport)

    def test_effects_engine_error_handling(self):
        """Test de gestion d'erreurs dans EffectsEngine"""
        engine = EffectsEngine()

        # Test avec un effet inexistant
        effect = engine.generate_effect("nonexistent_effect", {})
        self.assertIsInstance(effect, dict)

        # Test avec des paramètres invalides
        effect = engine.generate_effect("success", None)
        self.assertIsInstance(effect, dict)

    def test_luna_ai_error_handling(self):
        """Test de gestion d'erreurs dans LunaAI"""
        ai = LunaAI()

        # Test avec des entrées vides
        response = ai.respond("", {"user_personality": "hacker_creatif"}, {})
        self.assertIsInstance(response, dict)

        # Test avec des paramètres invalides - utiliser generate_general_response sans paramètres
        response = ai.generate_general_response()
        self.assertIsInstance(response, str)


if __name__ == "__main__":
    unittest.main()
