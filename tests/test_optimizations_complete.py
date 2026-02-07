#!/usr/bin/env python3
"""
Test complet des optimisations d'Arkalia Quest
"""

import os
import sys
import time

# Ajouter le répertoire racine du projet au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import du logger (après sys.path pour résoudre utils)
from utils.logger import game_logger  # noqa: E402


def test_performance_optimizations():
    """Test des optimisations de performance"""
    game_logger.info(r"⚡ Test des optimisations de performance...")

    tests_passed = 0
    total_tests = 0

    # Test 1: Vérifier que les fichiers d'optimisation existent
    total_tests += 1
    optimization_files = [
        "core/cache_manager.py",
        "core/security_unified.py",
        "core/performance_optimizer.py",
        "core/database_optimizer.py",
        "static/js/performance-ux-optimizer.js",
        "static/css/performance-optimized.css",
        "static/js/real-time-monitor.js",
    ]

    all_files_exist = True
    for file_path in optimization_files:
        if not os.path.exists(file_path):
            game_logger.info(f"❌ Fichier manquant: {file_path}")
            all_files_exist = False

    if all_files_exist:
        print("✅ Tous les fichiers d'optimisation sont présents")
        tests_passed += 1
    else:
        print("❌ Certains fichiers d'optimisation sont manquants")

    # Test 2: Vérifier la syntaxe Python
    total_tests += 1
    python_files = [
        "core/cache_manager.py",
        "core/security_unified.py",
        "core/performance_optimizer.py",
        "core/database_optimizer.py",
    ]

    syntax_ok = True
    for file_path in python_files:
        try:
            full_path = os.path.join(project_root, file_path)
            with open(full_path, encoding="utf-8") as f:
                compile(f.read(), full_path, "exec")
        except SyntaxError as e:
            game_logger.info(f"❌ Erreur de syntaxe dans {file_path}: {e}")
            syntax_ok = False

    if syntax_ok:
        game_logger.info(r"✅ Syntaxe Python correcte")
        tests_passed += 1
    else:
        game_logger.info(r"❌ Erreurs de syntaxe Python détectées")

    # Test 3: Vérifier les imports (garder project_root en premier pour résoudre core.*)
    total_tests += 1
    try:
        if sys.path[0] != project_root:
            sys.path.insert(0, project_root)
        # Vérification que les modules core sont importables
        import core.cache_manager  # noqa: F401
        import core.performance_optimizer  # noqa: F401

        print("✅ Imports des modules d'optimisation réussis")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")

    assert (
        tests_passed == total_tests
    ), f"Seulement {tests_passed}/{total_tests} tests de performance ont réussi"
    return (tests_passed, total_tests)


def test_security_enhancements():
    """Test des améliorations de sécurité"""
    game_logger.info(r"\n🛡️ Test des améliorations de sécurité...")

    tests_passed = 0
    total_tests = 0

    # Test 1: Validation des entrées
    total_tests += 1
    try:
        from core.security_unified import SecurityUnified

        security = SecurityUnified()

        # Test validation username
        is_valid, _ = security.validate_input("username", "testuser123")
        if is_valid:
            game_logger.info(r"✅ Validation username fonctionne")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Validation username échoue")

        # Test validation email
        is_valid, _ = security.validate_input("email", "arkalia.luna.system@gmail.com")
        if is_valid:
            game_logger.info(r"✅ Validation email fonctionne")
        else:
            game_logger.info(r"❌ Validation email échoue")

        # Test validation commande
        is_valid, _ = security.validate_input("command", "help")
        if is_valid:
            game_logger.info(r"✅ Validation commande fonctionne")
        else:
            game_logger.info(r"❌ Validation commande échoue")

    except Exception as e:
        game_logger.info(f"❌ Erreur test sécurité: {e}")

    # Test 2: Rate limiting
    total_tests += 1
    try:
        from core.security_unified import SecurityUnified

        security = SecurityUnified()

        # Test rate limiting
        allowed = security.check_rate_limit("127.0.0.1")
        if allowed:
            game_logger.info(r"✅ Rate limiting fonctionne")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Rate limiting échoue")

    except Exception as e:
        game_logger.info(f"❌ Erreur test rate limiting: {e}")

    # Test 3: Génération de tokens sécurisés (simulé)
    total_tests += 1
    try:
        from core.security_unified import SecurityUnified

        security = SecurityUnified()

        # Simuler la génération de token (pas implémentée dans SecurityUnified)
        # Vérifier que la classe fonctionne
        report = security.get_security_report()
        if report and "security_status" in report:
            game_logger.info(r"✅ Système de sécurité fonctionne")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Système de sécurité échoue")

    except Exception as e:
        game_logger.info(f"❌ Erreur test tokens: {e}")

    assert (
        tests_passed == total_tests
    ), f"Seulement {tests_passed}/{total_tests} tests de performance ont réussi"
    return (tests_passed, total_tests)


def test_cache_system():
    """Test du système de cache"""
    game_logger.info(r"\n💾 Test du système de cache...")

    tests_passed = 0
    total_tests = 0

    # Test 1: Opérations de base du cache
    total_tests += 1
    try:
        from core.cache_manager import cache_manager

        # Test set/get
        cache_manager.set("test_key", "test_value", 60)
        value = cache_manager.get("test_key")

        if value == "test_value":
            game_logger.info(r"✅ Opérations de base du cache fonctionnent")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Opérations de base du cache échouent")

    except Exception as e:
        game_logger.info(f"❌ Erreur test cache: {e}")

    # Test 2: Cache des profils utilisateur
    total_tests += 1
    try:
        from core.cache_manager import cache_manager

        test_profile = {"id": "test", "username": "testuser", "score": 100}
        cache_manager.set_user_profile("test", test_profile)
        retrieved_profile = cache_manager.get_user_profile("test")

        if retrieved_profile == test_profile:
            game_logger.info(r"✅ Cache des profils utilisateur fonctionne")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Cache des profils utilisateur échoue")

    except Exception as e:
        game_logger.info(f"❌ Erreur test cache profils: {e}")

    # Test 3: Statistiques du cache
    total_tests += 1
    try:
        from core.cache_manager import cache_manager

        stats = cache_manager.get_stats()
        if isinstance(stats, dict) and "cache_size" in stats:
            game_logger.info(r"✅ Statistiques du cache fonctionnent")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Statistiques du cache échouent")

    except Exception as e:
        game_logger.info(f"❌ Erreur test stats cache: {e}")

    assert (
        tests_passed == total_tests
    ), f"Seulement {tests_passed}/{total_tests} tests de performance ont réussi"
    return (tests_passed, total_tests)


def test_performance_monitoring():
    """Test du monitoring de performance"""
    game_logger.info(r"\n📊 Test du monitoring de performance...")

    tests_passed = 0
    total_tests = 0

    # Test 1: Décorateur de monitoring
    total_tests += 1
    try:
        from core.performance_optimizer import performance_optimizer

        @performance_optimizer.monitor_performance("test_function")
        def test_function():
            time.sleep(0.1)
            return "test"

        result = test_function()
        if result == "test":
            game_logger.info(r"✅ Décorateur de monitoring fonctionne")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Décorateur de monitoring échoue")

    except Exception as e:
        game_logger.info(f"❌ Erreur test monitoring: {e}")

    # Test 2: Statistiques de performance
    total_tests += 1
    try:
        from core.performance_optimizer import performance_optimizer

        stats = performance_optimizer.get_performance_stats()
        if isinstance(stats, dict) and "total_api_calls" in stats:
            game_logger.info(r"✅ Statistiques de performance fonctionnent")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Statistiques de performance échouent")

    except Exception as e:
        game_logger.info(f"❌ Erreur test stats performance: {e}")

    # Test 3: Suggestions d'optimisation
    total_tests += 1
    try:
        from core.performance_optimizer import performance_optimizer

        suggestions = performance_optimizer.suggest_optimizations()
        if isinstance(suggestions, list):
            print("✅ Suggestions d'optimisation fonctionnent")
            tests_passed += 1
        else:
            print("❌ Suggestions d'optimisation échouent")

    except Exception as e:
        game_logger.info(f"❌ Erreur test suggestions: {e}")

    assert (
        tests_passed == total_tests
    ), f"Seulement {tests_passed}/{total_tests} tests de performance ont réussi"
    return (tests_passed, total_tests)


def test_database_optimizations():
    """Test des optimisations de base de données"""
    game_logger.info(r"\n🗄️ Test des optimisations de base de données...")

    tests_passed = 0
    total_tests = 0

    # Test 1: Création de l'optimiseur
    total_tests += 1
    try:
        from core.database_optimizer import database_optimizer

        if database_optimizer:
            game_logger.info(r"✅ Optimiseur de base de données créé")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Échec création optimiseur de base de données")

    except Exception as e:
        game_logger.info(f"❌ Erreur test optimiseur DB: {e}")

    # Test 2: Pool de connexions
    total_tests += 1
    try:
        from core.database_optimizer import database_optimizer

        with database_optimizer.get_connection() as conn:
            if conn:
                game_logger.info(r"✅ Pool de connexions fonctionne")
                tests_passed += 1
            else:
                game_logger.info(r"❌ Pool de connexions échoue")

    except Exception as e:
        game_logger.info(f"❌ Erreur test pool connexions: {e}")

    # Test 3: Statistiques de base de données
    total_tests += 1
    try:
        from core.database_optimizer import database_optimizer

        stats = database_optimizer.get_performance_stats()
        if isinstance(stats, dict) and "connection_pool_size" in stats:
            game_logger.info(r"✅ Statistiques de base de données fonctionnent")
            tests_passed += 1
        else:
            game_logger.info(r"❌ Statistiques de base de données échouent")

    except Exception as e:
        game_logger.info(f"❌ Erreur test stats DB: {e}")

    assert (
        tests_passed == total_tests
    ), f"Seulement {tests_passed}/{total_tests} tests de performance ont réussi"
    return (tests_passed, total_tests)


def test_application_integration():
    """Test de l'intégration dans l'application"""
    # S'assurer que project_root est en premier pour résoudre app et core.*
    if sys.path[0] != project_root:
        sys.path.insert(0, project_root)
    print("\n🔗 Test de l'intégration dans l'application...")

    tests_passed = 0
    total_tests = 0

    # Test 1: Vérifier que l'application peut être importée
    total_tests += 1
    try:
        import app as app_module  # noqa: F401

        game_logger.info(r"✅ Application peut être importée")
        tests_passed += 1
    except Exception as e:
        game_logger.info(f"❌ Erreur import application: {e}")

    # Test 2: Vérifier les nouveaux endpoints
    total_tests += 1
    try:
        # Vérifier que les nouveaux endpoints sont définis
        from app import app as flask_app

        endpoints = [rule.rule for rule in flask_app.url_map.iter_rules()]
        required_endpoints = [
            "/api/performance/stats",
            "/api/security/stats",
            "/api/cache/clear",
        ]

        missing_endpoints = [ep for ep in required_endpoints if ep not in endpoints]
        if not missing_endpoints:
            game_logger.info(r"✅ Nouveaux endpoints présents")
            tests_passed += 1
        else:
            game_logger.info(f"❌ Endpoints manquants: {missing_endpoints}")

    except Exception as e:
        game_logger.info(f"❌ Erreur test endpoints: {e}")

    # Test 3: Vérifier les fichiers statiques
    total_tests += 1
    static_files = [
        "static/js/performance-ux-optimizer.js",
        "static/css/performance-optimized.css",
        "static/js/real-time-monitor.js",
    ]

    all_static_exist = True
    for file_path in static_files:
        if not os.path.exists(file_path):
            game_logger.info(f"❌ Fichier statique manquant: {file_path}")
            all_static_exist = False

    if all_static_exist:
        game_logger.info(r"✅ Fichiers statiques présents")
        tests_passed += 1
    else:
        game_logger.info(r"❌ Certains fichiers statiques sont manquants")

    assert (
        tests_passed == total_tests
    ), f"Seulement {tests_passed}/{total_tests} tests de performance ont réussi"
    return (tests_passed, total_tests)


def main():
    """Fonction principale"""
    game_logger.info(r"🚀 TEST COMPLET DES OPTIMISATIONS ARKALIA QUEST")
    print("=" * 60)

    total_passed = 0
    total_tests = 0

    # Exécuter tous les tests
    test_functions = [
        test_performance_optimizations,
        test_security_enhancements,
        test_cache_system,
        test_performance_monitoring,
        test_database_optimizations,
        test_application_integration,
    ]

    for test_func in test_functions:
        try:
            passed, tests = test_func()
            total_passed += passed
            total_tests += tests
        except Exception as e:
            game_logger.info(f"❌ Erreur dans {test_func.__name__}: {e}")

    # Résumé final
    print("\n" + "=" * 60)
    game_logger.info(r"📊 RÉSULTATS FINAUX")
    print("=" * 60)
    game_logger.info(f"✅ Tests réussis: {total_passed}/{total_tests}")
    game_logger.info(f"❌ Tests échoués: {total_tests - total_passed}/{total_tests}")
    game_logger.info(f"📈 Taux de réussite: {(total_passed / total_tests) * 100:.1f}%")

    if total_passed == total_tests:
        game_logger.info(r"\n🎉 TOUTES LES OPTIMISATIONS SONT FONCTIONNELLES !")
        game_logger.info(r"🚀 Arkalia Quest est prêt pour la production !")
        return 0
    game_logger.info(f"\n⚠️ {total_tests - total_passed} test(s) ont échoué")
    game_logger.info(r"🔧 Des corrections sont nécessaires")
    return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
