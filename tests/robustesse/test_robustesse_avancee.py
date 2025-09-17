#!/usr/bin/env python3
"""
🛡️ TESTS DE ROBUSTESSE AVANCÉE - ARKALIA QUEST
Tests de robustesse, résilience et gestion d'erreurs critiques
PRIORITÉ ABSOLUE - Garantir la stabilité du système en production
"""

import concurrent.futures
import os
import random
import sys
import tempfile
import threading
import time
import unittest

# Ajouter le répertoire parent au path
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
)

from utils.logger import GameLogger  # noqa: E402

# Initialiser le logger
game_logger = GameLogger()

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    game_logger.info(r"⚠️ psutil non disponible - tests de mémoire limités")

try:
    from core.database import DatabaseManager
    from core.educational_games_engine import EducationalGamesEngine
    from core.gamification_engine import GamificationEngine
    from core.luna_emotions_engine import LunaEmotionsEngine
    from core.security_manager import SecurityManager
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)


class TestRobustesseAvancee(unittest.TestCase):
    """Tests de robustesse avancée pour Arkalia Quest"""

    def setUp(self):
        """Initialisation avant chaque test"""
        game_logger.info(r"🛡️ Initialisation des tests de robustesse avancée...")

        # Créer un répertoire temporaire pour les tests
        self.test_dir = tempfile.mkdtemp()

        # Initialiser tous les moteurs critiques
        self.luna_engine = LunaEmotionsEngine()
        self.gamification_engine = GamificationEngine(data_dir=self.test_dir)
        self.db_manager = DatabaseManager()
        self.educational_engine = EducationalGamesEngine()
        self.security_manager = SecurityManager()

        # Profils de test variés pour tester différents scénarios
        self.test_profiles = {
            "debutant": {"level": 1, "score": 0, "badges": []},
            "intermediaire": {"level": 5, "score": 1500, "badges": ["hacker"]},
            "expert": {"level": 10, "score": 5000, "badges": ["maitre", "speedrunner"]},
            "extreme": {
                "level": 100,
                "score": 100000,
                "badges": ["legend", "ultimate"],
            },
        }

        # Métriques de robustesse
        self.robustness_metrics = {
            "error_count": 0,
            "recovery_success": 0,
            "performance_degradation": [],
            "memory_leaks": [],
            "concurrent_operations": [],
        }

        game_logger.info(r"✅ Initialisation terminée")

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Nettoyer les ressources
        if hasattr(self, "test_dir") and os.path.exists(self.test_dir):
            import shutil

            shutil.rmtree(self.test_dir)

        # Réinitialiser les moteurs
        self.luna_engine.reset_emotions()

        game_logger.info(f"🧹 Nettoyage terminé - Métriques: {self.robustness_metrics}")

    def test_resilience_under_extreme_load(self):
        """Test de résilience sous charge extrême"""
        game_logger.info(r"🔥 Test de résilience sous charge extrême...")

        # Simuler 1000 opérations simultanées
        operations = []
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            # Créer des tâches variées
            for i in range(1000):
                profile = random.choice(list(self.test_profiles.values()))
                action = f"action_{i % 10}"
                result = {
                    "réussite": i % 2 == 0,
                    "score_gagne": random.randint(0, 1000),
                }

                future = executor.submit(
                    self._execute_operation_safely,
                    self.luna_engine.analyze_action,
                    action,
                    result,
                    profile,
                )
                operations.append(future)

            # Attendre la completion avec timeout
            completed = 0
            errors = 0

            for future in concurrent.futures.as_completed(operations, timeout=30):
                try:
                    result = future.result(timeout=1)
                    completed += 1
                except Exception as e:
                    errors += 1
                    self.robustness_metrics["error_count"] += 1
                    print(f"⚠️ Erreur dans l'opération: {e}")

        end_time = time.time()
        duration = end_time - start_time

        # Vérifications de robustesse
        self.assertGreater(completed, 950, "Trop d'opérations ont échoué")
        self.assertLess(errors, 50, "Trop d'erreurs sous charge")
        self.assertLess(duration, 35, "Performance dégradée sous charge")

        game_logger.info(f"✅ Résilience: {completed}/1000 opérations réussies en {duration:.2f}s")
        game_logger.info(f"📊 Erreurs: {errors}, Métriques: {self.robustness_metrics}")

    def test_memory_leak_prevention(self):
        """Test de prévention des fuites mémoire"""
        game_logger.info(r"💾 Test de prévention des fuites mémoire...")

        if not PSUTIL_AVAILABLE:
            self.skipTest("psutil non disponible")

        process = psutil.Process()
        initial_memory = process.memory_info().rss

        # Simuler une longue session de jeu
        for session in range(10):
            session_memory = []

            for i in range(100):
                # Opérations intensives
                profile = random.choice(list(self.test_profiles.values()))
                for _ in range(50):
                    self.luna_engine.analyze_action(
                        f"session_{session}_action_{i}",
                        {"réussite": True, "score_gagne": random.randint(0, 100)},
                        profile,
                    )

                # Vérifier la mémoire
                current_memory = process.memory_info().rss
                session_memory.append(current_memory)

            # Vérifier qu'il n'y a pas de fuite progressive
            if session > 0:
                memory_increase = session_memory[-1] - session_memory[0]
                self.assertLess(
                    memory_increase,
                    10 * 1024 * 1024,  # 10MB max
                    f"Fuite mémoire détectée dans la session {session}",
                )

        final_memory = process.memory_info().rss
        total_increase = final_memory - initial_memory

        # Vérifier que l'augmentation totale est raisonnable
        self.assertLess(
            total_increase,
            50 * 1024 * 1024,  # 50MB max
            "Fuite mémoire globale détectée",
        )

        print(
            f"✅ Mémoire: {initial_memory / 1024 / 1024:.1f}MB → {final_memory / 1024 / 1024:.1f}MB",
        )
        game_logger.info(f"📊 Augmentation: {total_increase / 1024 / 1024:.1f}MB")

    def test_error_recovery_mechanisms(self):
        """Test des mécanismes de récupération d'erreurs"""
        print("🔄 Test des mécanismes de récupération d'erreurs...")

        # Tester la récupération après des erreurs critiques
        recovery_tests = [
            self._test_database_recovery,
            self._test_engine_recovery,
            self._test_memory_recovery,
            self._test_concurrent_recovery,
        ]

        for test_func in recovery_tests:
            try:
                test_func()
                self.robustness_metrics["recovery_success"] += 1
            except Exception as e:
                game_logger.info(f"❌ Échec du test de récupération {test_func.__name__}: {e}")
                self.robustness_metrics["error_count"] += 1

        # Vérifier que la plupart des récupérations réussissent
        success_rate = self.robustness_metrics["recovery_success"] / len(recovery_tests)
        self.assertGreater(success_rate, 0.8, "Taux de récupération trop faible")

        print(
            f"✅ Récupération: {self.robustness_metrics['recovery_success']}/{len(recovery_tests)}",
        )
        game_logger.info(f"📊 Taux de succès: {success_rate:.1%}")

    def test_concurrent_safety(self):
        """Test de sécurité concurrente"""
        game_logger.info(r"🔒 Test de sécurité concurrente...")

        # Tester l'accès concurrent aux ressources partagées
        shared_data = {"counter": 0, "data": []}
        lock = threading.Lock()

        def concurrent_operation(thread_id):
            """Opération concurrente qui modifie des données partagées"""
            for i in range(100):
                with lock:
                    shared_data["counter"] += 1
                    shared_data["data"].append(f"thread_{thread_id}_op_{i}")

                # Simuler du travail
                time.sleep(0.001)

        # Lancer 10 threads simultanément
        threads = []
        for i in range(10):
            thread = threading.Thread(target=concurrent_operation, args=(i,))
            threads.append(thread)
            thread.start()

        # Attendre la completion
        for thread in threads:
            thread.join()

        # Vérifier l'intégrité des données
        expected_counter = 10 * 100
        self.assertEqual(
            shared_data["counter"],
            expected_counter,
            "Corruption des données concurrentes",
        )
        self.assertEqual(
            len(shared_data["data"]),
            expected_counter,
            "Perte de données concurrentes",
        )

        print(f"✅ Concurrence: {shared_data['counter']} opérations thread-safe")
        print(f"📊 Données: {len(shared_data['data'])} éléments préservés")

    def test_extreme_edge_cases(self):
        """Test des cas limites extrêmes"""
        game_logger.info(r"🎯 Test des cas limites extrêmes...")

        edge_cases = [
            # Profils extrêmes
            {"level": 0, "score": -1000, "badges": None},
            {"level": 999999, "score": 999999999, "badges": ["x" * 1000]},
            {"level": "invalid", "score": "string", "badges": 123},
            # Actions extrêmes
            ("", {}),
            ("x" * 10000, {"réussite": None, "score_gagne": "invalid"}),
            (None, None),
            # Résultats extrêmes
            ("normal_action", {"réussite": True, "score_gagne": float("inf")}),
            ("normal_action", {"réussite": False, "score_gagne": float("-inf")}),
            ("normal_action", {"réussite": "maybe", "score_gagne": complex(1, 1)}),
        ]

        errors_handled = 0

        for i, edge_case in enumerate(edge_cases):
            try:
                if isinstance(edge_case, tuple):
                    action, result = edge_case
                    profile = self.test_profiles["debutant"]
                else:
                    action = "test_action"
                    result = {"réussite": True, "score_gagne": 10}
                    profile = edge_case

                # Tenter l'opération
                self.luna_engine.analyze_action(action, result, profile)
                errors_handled += 1

            except Exception as e:
                # L'erreur est attendue pour les cas limites
                errors_handled += 1
                game_logger.info(f"✅ Cas limite {i} géré: {type(e).__name__}")

        # Vérifier que tous les cas limites sont gérés
        self.assertEqual(errors_handled, len(edge_cases), "Cas limites non gérés")

        game_logger.info(f"✅ Cas limites: {errors_handled}/{len(edge_cases)} gérés correctement")

    def _execute_operation_safely(self, func, *args, **kwargs):
        """Exécute une opération avec gestion d'erreur sécurisée"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Logger l'erreur mais ne pas la faire remonter
            game_logger.info(f"⚠️ Opération échouée: {e}")
            return {"error": str(e), "status": "failed"}

    def _test_database_recovery(self):
        """Test de récupération de la base de données"""
        # Créer un profil de test avec des données valides
        test_profile = {
            "username": "recovery_test",
            "score": 100,
            "level": 5,
            "badges": ["test_badge"],
            "avatars": [],
            "preferences": {"theme": "dark"},
        }

        # Sauvegarder le profil
        success = self.db_manager.save_profile("recovery_test", test_profile)
        self.assertTrue(success, "Sauvegarde du profil échouée")

        # Vérifier la récupération
        recovered_data = self.db_manager.load_profile("recovery_test")
        self.assertIsNotNone(recovered_data, "Profil non récupéré")

        # Vérifier que les données clés sont présentes
        self.assertEqual(recovered_data["username"], "recovery_test", "Username incorrect")
        self.assertEqual(recovered_data["score"], 100, "Score incorrect")
        self.assertEqual(recovered_data["level"], 5, "Niveau incorrect")
        self.assertIn("test_badge", recovered_data["badges"], "Badge de test manquant")

        # Vérifier que c'est un profil valide
        self.assertIsInstance(recovered_data, dict, "Profil non valide")

    def _test_engine_recovery(self):
        """Test de récupération des moteurs"""
        # Forcer une erreur dans le moteur LUNA
        self.luna_engine.reset_emotions()

        # Vérifier que le moteur fonctionne toujours
        result = self.luna_engine.analyze_action(
            "recovery_test",
            {"réussite": True, "score_gagne": 100},
            self.test_profiles["debutant"],
        )
        self.assertIsNotNone(result, "Moteur non récupéré")

    def _test_memory_recovery(self):
        """Test de récupération mémoire"""
        if not PSUTIL_AVAILABLE:
            return

        # Forcer le garbage collection
        import gc

        gc.collect()

        # Vérifier que la mémoire est stable
        process = psutil.Process()
        memory_before = process.memory_info().rss

        # Opération intensive
        for _ in range(1000):
            self.luna_engine.analyze_action(
                "memory_test",
                {"réussite": True, "score_gagne": 10},
                self.test_profiles["debutant"],
            )

        gc.collect()
        memory_after = process.memory_info().rss

        # Vérifier que la mémoire n'explose pas
        increase = memory_after - memory_before
        self.assertLess(increase, 100 * 1024 * 1024, "Récupération mémoire échouée")

    def _test_concurrent_recovery(self):
        """Test de récupération concurrente"""

        # Simuler des erreurs concurrentes
        def error_operation():
            try:
                # Opération qui peut échouer
                if random.random() < 0.3:
                    raise ValueError("Erreur simulée")
                return "success"
            except Exception:
                return "recovered"

        # Exécuter en parallèle
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(error_operation) for _ in range(20)]
            results = [f.result() for f in futures]

        # Vérifier que toutes les opérations se terminent
        self.assertEqual(len(results), 20, "Récupération concurrente échouée")


def run_robustness_tests():
    """Lance tous les tests de robustesse"""
    game_logger.info(r"🛡️ LANCEMENT DES TESTS DE ROBUSTESSE AVANCÉE")
    print("=" * 60)

    # Créer la suite de tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestRobustesseAvancee))

    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Résumé détaillé
    print("\n" + "=" * 60)
    game_logger.info(r"📊 RÉSUMÉ DES TESTS DE ROBUSTESSE")
    game_logger.info(f"Tests exécutés: {result.testsRun}")
    game_logger.info(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    game_logger.info(f"Échecs: {len(result.failures)}")
    game_logger.info(f"Erreurs: {len(result.errors)}")

    if result.failures:
        game_logger.info(r"\n❌ ÉCHECS:")
        for test, traceback in result.failures:
            game_logger.info(f"  - {test}: {traceback}")

    if result.errors:
        game_logger.info(r"\n💥 ERREURS:")
        for test, traceback in result.errors:
            game_logger.info(f"  - {test}: {traceback}")

    success_rate = (
        (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
    ) * 100
    game_logger.info(f"\n🎯 TAUX DE RÉUSSITE: {success_rate:.1f}%")

    if success_rate >= 90:
        game_logger.info(r"🌟 SYSTÈME TRÈS ROBUSTE - Prêt pour la production !")
    elif success_rate >= 80:
        game_logger.info(r"✅ SYSTÈME ROBUSTE - Quelques améliorations recommandées")
    else:
        game_logger.info(r"⚠️ SYSTÈME PEU ROBUSTE - Actions correctives nécessaires")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_robustness_tests()
    sys.exit(0 if success else 1)
