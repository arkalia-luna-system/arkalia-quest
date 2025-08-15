#!/usr/bin/env python3
"""
Test du Système d'Analytics et Suivi Utilisateur Data-Driven
Arkalia Quest - Validation complète du système d'analytics

Ce script teste toutes les fonctionnalités du système d'analytics :
- Moteur d'analytics
- Interface JavaScript
- Routes API
- Commandes terminal
- Collecte de données
- Génération d'insights
"""

import json
import os
import sqlite3
import sys
import time
from datetime import datetime

import requests

# Configuration
BASE_URL = "http://localhost:5001"
TEST_USER_ID = "test_analytics_user"
TEST_SESSION_ID = "test_session_" + str(int(time.time()))


class AnalyticsTester:
    """Classe de test pour le système d'analytics"""

    def __init__(self):
        self.results = []
        self.start_time = time.time()

    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Enregistre un résultat de test"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
        self.results.append(result)

        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")

    def test_analytics_engine_import(self):
        """Test l'import du moteur d'analytics"""
        try:
            from core.analytics_engine import AnalyticsEngine

            engine = AnalyticsEngine("test_analytics.db")
            self.log_test(
                "Import Analytics Engine",
                True,
                "Moteur d'analytics importé avec succès",
            )
            return engine
        except Exception as e:
            self.log_test("Import Analytics Engine", False, f"Erreur: {e}")
            return None

    def test_analytics_engine_functionality(self, engine):
        """Test les fonctionnalités du moteur d'analytics"""
        if not engine:
            return

        try:
            # Test de tracking d'événements
            from core.analytics_engine import EventType

            # Événements de test
            test_events = [
                (EventType.SESSION_START, {"session_id": TEST_SESSION_ID}),
                (EventType.COMMAND_EXECUTED, {"command": "test", "success": True}),
                (EventType.MISSION_START, {"mission_id": "test_mission"}),
                (EventType.GAME_START, {"game_type": "logic", "game_id": "test_game"}),
                (EventType.BADGE_EARNED, {"badge_id": "test_badge"}),
                (EventType.EMOTION_TRIGGERED, {"emotion": "excited", "intensity": 0.8}),
                (EventType.SESSION_END, {"session_id": TEST_SESSION_ID}),
            ]

            for event_type, data in test_events:
                engine.track_event(
                    event_type=event_type,
                    user_id=TEST_USER_ID,
                    session_id=TEST_SESSION_ID,
                    data=data,
                    context={"test": True},
                )

            self.log_test(
                "Tracking d'événements", True, f"{len(test_events)} événements trackés"
            )

            # Test de génération d'insights
            insights = engine.get_user_insights(TEST_USER_ID)
            if insights:
                self.log_test(
                    "Génération d'insights", True, "Insights générés avec succès"
                )
            else:
                self.log_test("Génération d'insights", False, "Aucun insight généré")

            # Test d'analytics globaux
            global_analytics = engine.get_global_analytics()
            if global_analytics:
                self.log_test("Analytics globaux", True, "Analytics globaux générés")
            else:
                self.log_test(
                    "Analytics globaux", False, "Erreur génération analytics globaux"
                )

        except Exception as e:
            self.log_test("Fonctionnalités Analytics Engine", False, f"Erreur: {e}")

    def test_api_routes(self):
        """Test les routes API analytics"""

        # Test route de tracking
        try:
            test_events = [
                {
                    "event_type": "session_start",
                    "session_id": TEST_SESSION_ID,
                    "data": {"test": True},
                    "context": {"user_agent": "test"},
                }
            ]

            response = requests.post(
                f"{BASE_URL}/api/analytics/track",
                json={"events": test_events},
                timeout=10,
            )

            if response.status_code == 200:
                self.log_test("API Track Events", True, "Événements trackés via API")
            else:
                self.log_test(
                    "API Track Events",
                    False,
                    f"Erreur {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test("API Track Events", False, f"Erreur: {e}")

        # Test route insights
        try:
            response = requests.get(f"{BASE_URL}/api/analytics/insights", timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("API Insights", True, "Insights récupérés via API")
                else:
                    self.log_test("API Insights", False, "Erreur dans la réponse")
            else:
                self.log_test("API Insights", False, f"Erreur {response.status_code}")
        except Exception as e:
            self.log_test("API Insights", False, f"Erreur: {e}")

        # Test route analytics globaux
        try:
            response = requests.get(f"{BASE_URL}/api/analytics/global", timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test(
                        "API Global Analytics", True, "Analytics globaux récupérés"
                    )
                else:
                    self.log_test(
                        "API Global Analytics", False, "Erreur dans la réponse"
                    )
            else:
                self.log_test(
                    "API Global Analytics", False, f"Erreur {response.status_code}"
                )
        except Exception as e:
            self.log_test("API Global Analytics", False, f"Erreur: {e}")

        # Test route export
        try:
            response = requests.get(f"{BASE_URL}/api/analytics/export", timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("API Export Data", True, "Données exportées via API")
                else:
                    self.log_test("API Export Data", False, "Erreur dans la réponse")
            else:
                self.log_test(
                    "API Export Data", False, f"Erreur {response.status_code}"
                )
        except Exception as e:
            self.log_test("API Export Data", False, f"Erreur: {e}")

    def test_analytics_commands(self):
        """Test les commandes analytics dans le terminal"""
        try:
            from core.command_handler_v2 import CommandHandlerV2

            handler = CommandHandlerV2()
            profile = {"id": TEST_USER_ID, "name": "Test User", "level": 1}

            # Test des commandes analytics
            analytics_commands = [
                "analytics",
                "insights",
                "stats",
                "progress",
                "recommendations",
                "learning_style",
                "engagement",
            ]

            for cmd in analytics_commands:
                if cmd in handler.all_commands:
                    result = handler.handle_command(cmd, profile)
                    if result.get("réussite"):
                        self.log_test(
                            f"Commande {cmd}", True, "Commande exécutée avec succès"
                        )
                    else:
                        self.log_test(
                            f"Commande {cmd}", False, result.get("message", "Erreur")
                        )
                else:
                    self.log_test(f"Commande {cmd}", False, "Commande non trouvée")

        except Exception as e:
            self.log_test("Commandes Analytics", False, f"Erreur: {e}")

    def test_database_integrity(self):
        """Test l'intégrité de la base de données analytics"""
        try:
            # Vérifier que les tables existent
            with sqlite3.connect("arkalia.db") as conn:
                cursor = conn.cursor()

                # Vérifier la table des événements
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='analytics_events'"
                )
                if cursor.fetchone():
                    self.log_test("Table analytics_events", True, "Table existante")
                else:
                    self.log_test("Table analytics_events", False, "Table manquante")

                # Vérifier la table des profils
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='analytics_user_profiles'"
                )
                if cursor.fetchone():
                    self.log_test(
                        "Table analytics_user_profiles", True, "Table existante"
                    )
                else:
                    self.log_test(
                        "Table analytics_user_profiles", False, "Table manquante"
                    )

                # Vérifier la table des sessions
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='analytics_sessions'"
                )
                if cursor.fetchone():
                    self.log_test("Table analytics_sessions", True, "Table existante")
                else:
                    self.log_test("Table analytics_sessions", False, "Table manquante")

                # Vérifier les index
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_events_user_time'"
                )
                if cursor.fetchone():
                    self.log_test("Index events_user_time", True, "Index existant")
                else:
                    self.log_test("Index events_user_time", False, "Index manquant")

        except Exception as e:
            self.log_test("Intégrité Base de Données", False, f"Erreur: {e}")

    def test_data_anonymization(self):
        """Test l'anonymisation des données"""
        try:
            from core.analytics_engine import AnalyticsEngine

            engine = AnalyticsEngine("test_anonymization.db")

            # Tester l'anonymisation
            original_user_id = "user123"
            anonymized_id = engine._anonymize_user_id(original_user_id)

            if anonymized_id != original_user_id and len(anonymized_id) == 16:
                self.log_test(
                    "Anonymisation des données",
                    True,
                    "ID utilisateur anonymisé correctement",
                )
            else:
                self.log_test(
                    "Anonymisation des données", False, "Erreur dans l'anonymisation"
                )

        except Exception as e:
            self.log_test("Anonymisation des données", False, f"Erreur: {e}")

    def test_performance(self):
        """Test les performances du système d'analytics"""
        try:
            from core.analytics_engine import AnalyticsEngine, EventType

            engine = AnalyticsEngine("test_performance.db")

            # Test de performance avec de nombreux événements
            start_time = time.time()

            for i in range(100):
                engine.track_event(
                    event_type=EventType.COMMAND_EXECUTED,
                    user_id=f"user_{i}",
                    session_id=f"session_{i}",
                    data={"command": f"test_cmd_{i}"},
                    context={"test": True},
                )

            end_time = time.time()
            duration = end_time - start_time

            if duration < 5.0:  # Moins de 5 secondes pour 100 événements
                self.log_test(
                    "Performance Tracking",
                    True,
                    f"100 événements trackés en {duration:.2f}s",
                )
            else:
                self.log_test(
                    "Performance Tracking",
                    False,
                    f"Trop lent: {duration:.2f}s pour 100 événements",
                )

        except Exception as e:
            self.log_test("Performance", False, f"Erreur: {e}")

    def test_error_handling(self):
        """Test la gestion d'erreurs"""
        try:
            from core.analytics_engine import AnalyticsEngine

            engine = AnalyticsEngine("test_errors.db")

            # Test avec des données invalides
            try:
                engine.track_event(
                    event_type=None, user_id="", session_id="", data=None, context=None
                )
                self.log_test("Gestion d'erreurs", True, "Erreurs gérées gracieusement")
            except Exception:
                self.log_test("Gestion d'erreurs", False, "Erreur non gérée")

        except Exception as e:
            self.log_test("Gestion d'erreurs", False, f"Erreur: {e}")

    def generate_report(self):
        """Génère un rapport de test complet"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - successful_tests

        duration = time.time() - self.start_time

        report = {
            "test_summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (
                    (successful_tests / total_tests * 100) if total_tests > 0 else 0
                ),
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat(),
            },
            "test_results": self.results,
            "recommendations": self._generate_recommendations(),
        }

        # Sauvegarder le rapport
        with open("test_analytics_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Afficher le résumé
        print("\n" + "=" * 60)
        print("📊 RAPPORT DE TEST DU SYSTÈME ANALYTICS")
        print("=" * 60)
        print(f"🎯 Tests totaux: {total_tests}")
        print(f"✅ Tests réussis: {successful_tests}")
        print(f"❌ Tests échoués: {failed_tests}")
        print(f"📈 Taux de succès: {report['test_summary']['success_rate']:.1f}%")
        print(f"⏱️ Durée totale: {duration:.2f}s")
        print("=" * 60)

        if failed_tests > 0:
            print("\n❌ TESTS ÉCHOUÉS:")
            for result in self.results:
                if not result["success"]:
                    print(f"• {result['test']}: {result['message']}")

        print("\n📄 Rapport détaillé sauvegardé dans: test_analytics_report.json")

        return report

    def _generate_recommendations(self):
        """Génère des recommandations basées sur les résultats"""
        recommendations = []

        failed_tests = [r for r in self.results if not r["success"]]

        if any("Import" in r["test"] for r in failed_tests):
            recommendations.append("Vérifier l'installation des dépendances analytics")

        if any("API" in r["test"] for r in failed_tests):
            recommendations.append("Vérifier que le serveur Flask est démarré")

        if any("Database" in r["test"] for r in failed_tests):
            recommendations.append("Vérifier l'intégrité de la base de données")

        if any("Performance" in r["test"] for r in failed_tests):
            recommendations.append("Optimiser les performances du système d'analytics")

        if not recommendations:
            recommendations.append("Tous les tests sont passés avec succès !")

        return recommendations


def main():
    """Fonction principale de test"""
    print("🔍 DÉMARRAGE DES TESTS DU SYSTÈME ANALYTICS")
    print("=" * 60)

    tester = AnalyticsTester()

    # Tests du moteur d'analytics
    print("\n🧪 TEST DU MOTEUR ANALYTICS")
    print("-" * 40)
    engine = tester.test_analytics_engine_import()
    if engine:
        tester.test_analytics_engine_functionality(engine)

    # Tests des routes API
    print("\n🌐 TEST DES ROUTES API")
    print("-" * 40)
    tester.test_api_routes()

    # Tests des commandes
    print("\n⌨️ TEST DES COMMANDES ANALYTICS")
    print("-" * 40)
    tester.test_analytics_commands()

    # Tests de la base de données
    print("\n🗄️ TEST DE LA BASE DE DONNÉES")
    print("-" * 40)
    tester.test_database_integrity()

    # Tests de sécurité
    print("\n🔒 TEST DE SÉCURITÉ")
    print("-" * 40)
    tester.test_data_anonymization()

    # Tests de performance
    print("\n⚡ TEST DE PERFORMANCE")
    print("-" * 40)
    tester.test_performance()

    # Tests de gestion d'erreurs
    print("\n🛡️ TEST DE GESTION D'ERREURS")
    print("-" * 40)
    tester.test_error_handling()

    # Génération du rapport
    print("\n📊 GÉNÉRATION DU RAPPORT")
    print("-" * 40)
    report = tester.generate_report()

    # Nettoyage des fichiers de test
    test_files = [
        "test_analytics.db",
        "test_anonymization.db",
        "test_performance.db",
        "test_errors.db",
    ]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)

    return report["test_summary"]["success_rate"] >= 80


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
