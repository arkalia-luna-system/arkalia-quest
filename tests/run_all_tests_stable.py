#!/usr/bin/env python3
"""
🎮 ARKALIA QUEST - LANCEUR DE TESTS VERSION STABLE
==================================================

Ce script lance TOUS les tests pour valider la version stable :
- Tests de fonctionnalités complètes
- Tests de performance et stress
- Tests de sécurité
- Tests d'accessibilité
- Tests de base de données
- Tests PWA

Auteur: Assistant IA
Version: 1.0
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from typing import Any


class StableVersionTestRunner:
    """Lanceur de tests pour la version stable"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {},
            "recommendations": [],
        }

        # Liste des tests à exécuter
        self.test_modules = [
            {
                "name": "Version Stable Complète",
                "file": "test_stable_version_complete.py",
                "description": "Tests complets de toutes les fonctionnalités",
            },
            {
                "name": "Performance & Stress",
                "file": "test_performance_stress.py",
                "description": "Tests de performance et de charge",
            },
            {
                "name": "Sécurité",
                "file": "test_security_complete.py",
                "description": "Tests de sécurité et vulnérabilités",
            },
            {
                "name": "Gamification",
                "file": "test_gamification_complete.py",
                "description": "Tests du système de gamification",
            },
        ]

    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def check_server_status(self) -> bool:
        """Vérifie que le serveur est démarré"""
        self.log("🔍 Vérification du serveur...")

        try:
            import requests

            response = requests.get("http://localhost:5001/", timeout=5)
            if response.status_code == 200:
                self.log("✅ Serveur accessible", "SUCCESS")
                return True
            self.log(f"❌ Serveur répond avec code {response.status_code}", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Serveur inaccessible: {e}", "ERROR")
            return False

    def run_test_module(self, module: dict[str, str]) -> dict[str, Any]:
        """Exécute un module de test"""
        self.log(f"🚀 Lancement du test: {module['name']}")

        start_time = time.time()

        try:
            # Exécuter le test
            result = subprocess.run(
                [sys.executable, f"tests/{module['file']}"],
                check=False,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max par test
            )

            end_time = time.time()
            duration = end_time - start_time

            # Analyser le résultat
            success = result.returncode == 0
            output = result.stdout
            error = result.stderr

            self.log(f"⏱️ Durée: {duration:.2f}s", "INFO")

            if success:
                self.log(f"✅ {module['name']} - RÉUSSI", "SUCCESS")
            else:
                self.log(f"❌ {module['name']} - ÉCHOUÉ", "ERROR")
                if error:
                    self.log(f"Erreur: {error[:200]}...", "ERROR")

            return {
                "name": module["name"],
                "file": module["file"],
                "description": module["description"],
                "success": success,
                "duration": duration,
                "return_code": result.returncode,
                "output": output,
                "error": error,
            }

        except subprocess.TimeoutExpired:
            self.log(f"⏰ {module['name']} - TIMEOUT", "ERROR")
            return {
                "name": module["name"],
                "file": module["file"],
                "description": module["description"],
                "success": False,
                "duration": 300,
                "return_code": -1,
                "output": "",
                "error": "Timeout après 5 minutes",
            }
        except Exception as e:
            self.log(f"❌ Erreur exécution {module['name']}: {e}", "ERROR")
            return {
                "name": module["name"],
                "file": module["file"],
                "description": module["description"],
                "success": False,
                "duration": 0,
                "return_code": -1,
                "output": "",
                "error": str(e),
            }

    def generate_summary(self) -> dict[str, Any]:
        """Génère un résumé des résultats"""
        total_tests = len(self.test_modules)
        successful_tests = sum(
            1 for result in self.results["tests"].values() if result["success"]
        )
        failed_tests = total_tests - successful_tests

        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0

        total_duration = sum(
            result["duration"] for result in self.results["tests"].values()
        )

        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "total_duration": total_duration,
            "timestamp": self.results["timestamp"],
        }

    def generate_recommendations(self) -> list[str]:
        """Génère des recommandations basées sur les résultats"""
        recommendations = []
        summary = self.results["summary"]

        if summary["success_rate"] >= 90:
            recommendations.append(
                "🎉 Version stable excellente ! Prête pour la production."
            )
        elif summary["success_rate"] >= 80:
            recommendations.append(
                "✅ Version stable correcte. Quelques améliorations mineures"
                + "recommandées.",
            )
        elif summary["success_rate"] >= 60:
            recommendations.append(
                "⚠️ Version stable avec des problèmes. Corrections"
                + "nécessaires avant production.",
            )
        else:
            recommendations.append(
                "❌ Version instable. Corrections majeures requises."
            )

        # Recommandations spécifiques basées sur les tests
        for test_name, result in self.results["tests"].items():
            if not result["success"]:
                recommendations.append(f"🔧 Corriger les problèmes dans {test_name}")

        if summary["total_duration"] > 600:  # Plus de 10 minutes
            recommendations.append("⚡ Optimiser les temps d'exécution des tests")

        return recommendations

    def generate_report(self) -> str:
        """Génère un rapport complet"""
        summary = self.results["summary"]

        report = f"""
🎮 RAPPORT DE TESTS VERSION STABLE - ARKALIA QUEST
==================================================

📊 RÉSUMÉ GLOBAL
----------------
✅ Tests réussis: {summary["successful_tests"]}/{summary["total_tests"]}
❌ Tests échoués: {summary["failed_tests"]}/{summary["total_tests"]}
📈 Taux de réussite: {summary["success_rate"]:.1f}%
⏱️ Durée totale: {summary["total_duration"]:.2f} secondes
🕐 Timestamp: {summary["timestamp"]}

🔍 DÉTAIL PAR TEST
------------------
"""

        for test_name, result in self.results["tests"].items():
            status = "✅ RÉUSSI" if result["success"] else "❌ ÉCHOUÉ"
            report += f"{status} - {test_name}\n"
            report += f"   Durée: {result['duration']:.2f}s\n"
            report += f"   Description: {result['description']}\n"

            if result["error"]:
                report += f"   Erreur: {result['error'][:100]}...\n"

            report += "\n"

        # Recommandations
        if self.results["recommendations"]:
            report += "🎯 RECOMMANDATIONS\n"
            report += "------------------\n"
            for rec in self.results["recommendations"]:
                report += f"{rec}\n"
            report += "\n"

        # Conclusion
        report += "🏁 CONCLUSION\n"
        report += "-------------\n"

        if summary["success_rate"] >= 90:
            report += "🌟 VERSION STABLE VALIDÉE ! Prête pour la production.\n"
        elif summary["success_rate"] >= 80:
            report += (
                "✅ VERSION STABLE ACCEPTABLE. Quelques améliorations recommandées.\n"
            )
        elif summary["success_rate"] >= 60:
            report += "⚠️ VERSION STABLE AVEC RÉSERVES. Corrections nécessaires.\n"
        else:
            report += "❌ VERSION NON STABLE. Corrections majeures requises.\n"

        return report

    def run_all_tests(self):
        """Exécute tous les tests"""
        self.log("🚀 DÉMARRAGE DES TESTS VERSION STABLE ARKALIA QUEST")
        self.log("=" * 60)

        # Vérifier le serveur
        if not self.check_server_status():
            self.log("❌ Serveur non disponible, arrêt des tests", "ERROR")
            return False

        # Exécuter tous les tests
        for module in self.test_modules:
            result = self.run_test_module(module)
            self.results["tests"][module["name"]] = result

        # Générer le résumé
        self.results["summary"] = self.generate_summary()

        # Générer les recommandations
        self.results["recommendations"] = self.generate_recommendations()

        # Afficher le rapport
        report = self.generate_report()
        print(report)

        # Sauvegarder les résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"stable_version_test_report_{timestamp}.json"

        with open(report_file, encoding="utf-8", mode="w") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        self.log(f"📄 Rapport sauvegardé: {report_file}")

        # Retourner le succès global
        return self.results["summary"]["success_rate"] >= 80


def main():
    """Fonction principale"""
    print("🎮 ARKALIA QUEST - LANCEUR DE TESTS VERSION STABLE")
    print("=" * 60)

    runner = StableVersionTestRunner()
    success = runner.run_all_tests()

    if success:
        print("\n🎉 VERSION STABLE VALIDÉE !")
        return 0
    print("\n⚠️ VERSION NÉCESSITE DES CORRECTIONS")
    return 1


if __name__ == "__main__":
    exit(main())
