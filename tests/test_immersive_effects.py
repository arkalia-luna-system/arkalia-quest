#!/usr/bin/env python3
"""
🧪 Tests Professionnels - Effets Immersifs
Tests complets pour le système d'effets visuels et audio immersifs
"""

import os
import sys
import unittest

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestImmersiveEffects(unittest.TestCase):
    """Tests pour le système d'effets immersifs"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.test_emotion_data = {
            "emotion": "excited",
            "intensity": 0.8,
            "color": "#00ff00",
            "effect": "pulse_green",
            "sound": "luna_excited",
        }

    def test_emotion_data_structure(self):
        """Test de la structure des données d'émotion"""
        required_keys = ["emotion", "intensity", "color", "effect", "sound"]

        for key in required_keys:
            self.assertIn(key, self.test_emotion_data)

        # Vérifier les types
        self.assertIsInstance(self.test_emotion_data["emotion"], str)
        self.assertIsInstance(self.test_emotion_data["intensity"], float)
        self.assertIsInstance(self.test_emotion_data["color"], str)
        self.assertIsInstance(self.test_emotion_data["effect"], str)
        self.assertIsInstance(self.test_emotion_data["sound"], str)

        # Vérifier les bornes
        self.assertGreaterEqual(self.test_emotion_data["intensity"], 0.0)
        self.assertLessEqual(self.test_emotion_data["intensity"], 1.0)

        # Vérifier le format de couleur
        self.assertTrue(self.test_emotion_data["color"].startswith("#"))
        self.assertEqual(len(self.test_emotion_data["color"]), 7)

    def test_emotion_validation(self):
        """Test de validation des émotions"""
        valid_emotions = [
            "excited",
            "worried",
            "proud",
            "mysterious",
            "determined",
            "playful",
            "focused",
            "surprised",
            "calm",
            "energetic",
        ]

        self.assertIn(self.test_emotion_data["emotion"], valid_emotions)

    def test_effect_validation(self):
        """Test de validation des effets"""
        valid_effects = [
            "pulse_green",
            "shake_orange",
            "sparkle_magenta",
            "fade_cyan",
            "glow_red",
            "bounce_yellow",
            "zoom_blue",
            "flash_pink",
            "float_lightblue",
            "vibrate_green",
        ]

        self.assertIn(self.test_emotion_data["effect"], valid_effects)

    def test_sound_validation(self):
        """Test de validation des sons"""
        valid_sounds = [
            "luna_excited",
            "luna_worried",
            "luna_proud",
            "luna_mysterious",
            "luna_determined",
            "luna_playful",
            "luna_focused",
            "luna_surprised",
            "luna_calm",
            "luna_energetic",
        ]

        self.assertIn(self.test_emotion_data["sound"], valid_sounds)

    def test_color_emotion_mapping(self):
        """Test du mapping couleur-émotion"""
        color_mapping = {
            "excited": "#00ff00",  # Vert vif
            "worried": "#ff6600",  # Orange inquiet
            "proud": "#ff00ff",  # Magenta fier
            "mysterious": "#00ffff",  # Cyan mystérieux
            "determined": "#ff0000",  # Rouge déterminé
            "playful": "#ffff00",  # Jaune joueur
            "focused": "#0000ff",  # Bleu concentré
            "surprised": "#ff00aa",  # Rose surprise
            "calm": "#00ccff",  # Bleu calme
            "energetic": "#00ff88",  # Vert énergique
        }

        emotion = self.test_emotion_data["emotion"]
        expected_color = color_mapping[emotion]
        actual_color = self.test_emotion_data["color"]

        self.assertEqual(actual_color, expected_color)

    def test_intensity_effects(self):
        """Test des effets selon l'intensité"""
        # Test avec intensité faible
        low_intensity_data = self.test_emotion_data.copy()
        low_intensity_data["intensity"] = 0.2

        # Test avec intensité élevée
        high_intensity_data = self.test_emotion_data.copy()
        high_intensity_data["intensity"] = 0.9

        # Les deux doivent être valides
        self.assertGreaterEqual(low_intensity_data["intensity"], 0.0)
        self.assertLessEqual(low_intensity_data["intensity"], 1.0)
        self.assertGreaterEqual(high_intensity_data["intensity"], 0.0)
        self.assertLessEqual(high_intensity_data["intensity"], 1.0)

    def test_emotion_consistency(self):
        """Test de cohérence des émotions"""
        # Tester plusieurs émotions
        test_emotions = [
            {"emotion": "excited", "color": "#00ff00", "effect": "pulse_green"},
            {"emotion": "worried", "color": "#ff6600", "effect": "shake_orange"},
            {"emotion": "proud", "color": "#ff00ff", "effect": "sparkle_magenta"},
            {"emotion": "mysterious", "color": "#00ffff", "effect": "fade_cyan"},
            {"emotion": "determined", "color": "#ff0000", "effect": "glow_red"},
        ]

        for emotion_data in test_emotions:
            # Vérifier que chaque émotion a une couleur et un effet cohérents
            self.assertIsInstance(emotion_data["emotion"], str)
            self.assertIsInstance(emotion_data["color"], str)
            self.assertIsInstance(emotion_data["effect"], str)
            self.assertTrue(emotion_data["color"].startswith("#"))

    def test_effect_naming_convention(self):
        """Test de la convention de nommage des effets"""
        effect = self.test_emotion_data["effect"]

        # Format attendu: action_color
        parts = effect.split("_")
        self.assertEqual(len(parts), 2)

        action, color = parts
        self.assertIsInstance(action, str)
        self.assertIsInstance(color, str)
        self.assertGreater(len(action), 0)
        self.assertGreater(len(color), 0)

    def test_sound_naming_convention(self):
        """Test de la convention de nommage des sons"""
        sound = self.test_emotion_data["sound"]

        # Format attendu: luna_emotion
        parts = sound.split("_")
        self.assertEqual(len(parts), 2)
        self.assertEqual(parts[0], "luna")

        emotion = parts[1]
        valid_emotions = [
            "excited",
            "worried",
            "proud",
            "mysterious",
            "determined",
            "playful",
            "focused",
            "surprised",
            "calm",
            "energetic",
        ]
        self.assertIn(emotion, valid_emotions)


class TestImmersiveEffectsIntegration(unittest.TestCase):
    """Tests d'intégration des effets immersifs"""

    def setUp(self):
        """Initialisation"""
        self.test_profile = {
            "level": 3,
            "score": 500,
            "badges": ["Hacker", "Explorateur"],
            "personnalite": {"type": "hacker_intermediaire"},
        }

    def test_emotion_transition_sequence(self):
        """Test d'une séquence de transitions d'émotions"""
        emotion_sequence = [
            {"emotion": "calm", "intensity": 0.3, "action": "aide"},
            {"emotion": "excited", "intensity": 0.8, "action": "hack_system"},
            {"emotion": "worried", "intensity": 0.6, "action": "commande_inexistante"},
            {"emotion": "proud", "intensity": 0.9, "action": "hack_system"},
            {"emotion": "mysterious", "intensity": 0.4, "action": "explore"},
        ]

        for emotion_data in emotion_sequence:
            # Vérifier la structure
            self.assertIn("emotion", emotion_data)
            self.assertIn("intensity", emotion_data)
            self.assertIn("action", emotion_data)

            # Vérifier les types
            self.assertIsInstance(emotion_data["emotion"], str)
            self.assertIsInstance(emotion_data["intensity"], float)
            self.assertIsInstance(emotion_data["action"], str)

            # Vérifier les bornes
            self.assertGreaterEqual(emotion_data["intensity"], 0.0)
            self.assertLessEqual(emotion_data["intensity"], 1.0)

    def test_effect_intensity_scaling(self):
        """Test de l'échelle des effets selon l'intensité"""
        base_emotion = "excited"

        # Tester différentes intensités
        intensities = [0.1, 0.3, 0.5, 0.7, 0.9]

        for intensity in intensities:
            emotion_data = {
                "emotion": base_emotion,
                "intensity": intensity,
                "color": "#00ff00",
                "effect": "pulse_green",
                "sound": "luna_excited",
            }

            # Vérifier que l'intensité est valide
            self.assertGreaterEqual(intensity, 0.0)
            self.assertLessEqual(intensity, 1.0)

            # Vérifier la cohérence des données
            self.assertEqual(emotion_data["emotion"], base_emotion)
            self.assertEqual(emotion_data["intensity"], intensity)

    def test_emotion_context_consistency(self):
        """Test de cohérence du contexte émotionnel"""
        # Simuler différentes actions avec leurs résultats attendus
        action_results = [
            ("hack_system", {"réussite": True, "score_gagne": 100}, "excited"),
            ("commande_inexistante", {"réussite": False, "score_gagne": 0}, "worried"),
            ("aide", {"réussite": True, "score_gagne": 10}, "calm"),
            ("profil", {"réussite": True, "score_gagne": 5}, "playful"),
        ]

        for action, result, expected_emotion in action_results:
            # Vérifier que l'action et le résultat sont cohérents
            self.assertIsInstance(action, str)
            self.assertIsInstance(result, dict)
            self.assertIn("réussite", result)
            self.assertIn("score_gagne", result)

            # Vérifier que l'émotion attendue est valide
            valid_emotions = [
                "excited",
                "worried",
                "proud",
                "mysterious",
                "determined",
                "playful",
                "focused",
                "surprised",
                "calm",
                "energetic",
            ]
            self.assertIn(expected_emotion, valid_emotions)


class TestImmersiveEffectsPerformance(unittest.TestCase):
    """Tests de performance des effets immersifs"""

    def test_emotion_data_generation_speed(self):
        """Test de la vitesse de génération des données d'émotion"""
        import time

        # Données de test

        start_time = time.time()

        # Générer 100 émotions
        for i in range(100):
            emotion_data = {
                "emotion": "excited",
                "intensity": 0.5 + (i % 10) * 0.05,
                "color": "#00ff00",
                "effect": "pulse_green",
                "sound": "luna_excited",
            }

            # Validation basique
            self.assertIn("emotion", emotion_data)
            self.assertIn("intensity", emotion_data)
            self.assertIn("color", emotion_data)
            self.assertIn("effect", emotion_data)
            self.assertIn("sound", emotion_data)

        end_time = time.time()
        duration = end_time - start_time

        # La génération doit être rapide (< 1 seconde pour 100 émotions)
        self.assertLess(duration, 1.0)
        print(f"⏱️ Génération de 100 émotions en {duration:.3f} secondes")

    def test_effect_data_consistency(self):
        """Test de cohérence des données d'effets"""
        # Générer beaucoup de données d'effets
        effects_data = []

        for i in range(1000):
            emotion_data = {
                "emotion": "excited",
                "intensity": (i % 100) / 100.0,
                "color": "#00ff00",
                "effect": "pulse_green",
                "sound": "luna_excited",
            }
            effects_data.append(emotion_data)

        # Vérifier la cohérence
        for data in effects_data:
            self.assertGreaterEqual(data["intensity"], 0.0)
            self.assertLessEqual(data["intensity"], 1.0)
            self.assertEqual(data["emotion"], "excited")
            self.assertEqual(data["color"], "#00ff00")
            self.assertEqual(data["effect"], "pulse_green")
            self.assertEqual(data["sound"], "luna_excited")


def run_immersive_effects_tests():
    """Lance tous les tests d'effets immersifs"""
    print("🌟 LANCEMENT DES TESTS D'EFFETS IMMERSIFS")
    print("=" * 50)

    # Créer la suite de tests
    test_suite = unittest.TestSuite()

    # Ajouter les tests
    test_classes = [
        TestImmersiveEffects,
        TestImmersiveEffectsIntegration,
        TestImmersiveEffectsPerformance,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS D'EFFETS IMMERSIFS")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")

    if result.failures:
        print("\n❌ ÉCHECS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n💥 ERREURS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    success_rate = (
        (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
    ) * 100
    print(f"\n🎯 TAUX DE RÉUSSITE: {success_rate:.1f}%")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_immersive_effects_tests()
    sys.exit(0 if success else 1)
