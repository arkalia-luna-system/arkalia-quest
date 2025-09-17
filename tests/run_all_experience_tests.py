"""
Lanceur principal des tests d'expérience joueur Arkalia Quest
Exécute tous les testeurs d'expérience et génère un rapport global
"""

import json
import subprocess
import sys
import time
from datetime import datetime


class ExperienceTestRunner:
    """Lanceur principal des tests d'expérience"""

    def __init__(self):
        self.results = {
            "test_suite": "Arkalia Quest Experience Tests",
            "timestamp": datetime.now().isoformat(),
            "tests_run": [],
            "overall_score": 0,
            "summary": {},
            "recommendations": [],
        }

    def run_tutoriel_test(self):
        """Lance le test d'expérience tutoriel"""
        print("🎮 LANCEMENT TEST EXPÉRIENCE TUTORIEL")
        print("=" * 50)

        try:
            result = subprocess.run(
                [sys.executable, "tests/test_ui_tutoriel_experience.py"],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )

            test_result = {
                "name": "Tutoriel Experience",
                "success": result.returncode == 0,
                "duration": 0,
                "output": result.stdout,
                "errors": result.stderr,
                "score": 0,
            }

            # Extraire le score du rapport JSON généré
            try:
                import glob

                report_files = glob.glob("tutoriel_experience_report_*.json")
                if report_files:
                    latest_report = max(report_files, key=lambda x: x.split("_")[-1].split(".")[0])
                    with open(latest_report, encoding="utf-8") as f:
                        report_data = json.load(f)
                        test_result["score"] = report_data.get("overall_score", 0)
            except Exception:
                pass

            self.results["tests_run"].append(test_result)
            return test_result

        except subprocess.TimeoutExpired:
            test_result = {
                "name": "Tutoriel Experience",
                "success": False,
                "duration": 60,
                "output": "",
                "errors": "Timeout après 60 secondes",
                "score": 0,
            }
            self.results["tests_run"].append(test_result)
            return test_result

    def run_terminal_test(self):
        """Lance le test d'expérience terminal"""
        print("🎮 LANCEMENT TEST EXPÉRIENCE TERMINAL")
        print("=" * 50)

        try:
            result = subprocess.run(
                [sys.executable, "tests/test_ui_terminal_experience.py"],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )

            test_result = {
                "name": "Terminal Experience",
                "success": result.returncode == 0,
                "duration": 0,
                "output": result.stdout,
                "errors": result.stderr,
                "score": 0,
            }

            # Extraire le score du rapport JSON généré
            try:
                import glob

                report_files = glob.glob("terminal_experience_report_*.json")
                if report_files:
                    latest_report = max(report_files, key=lambda x: x.split("_")[-1].split(".")[0])
                    with open(latest_report, encoding="utf-8") as f:
                        report_data = json.load(f)
                        test_result["score"] = report_data.get("overall_score", 0)
            except Exception:
                pass

            self.results["tests_run"].append(test_result)
            return test_result

        except subprocess.TimeoutExpired:
            test_result = {
                "name": "Terminal Experience",
                "success": False,
                "duration": 60,
                "output": "",
                "errors": "Timeout après 60 secondes",
                "score": 0,
            }
            self.results["tests_run"].append(test_result)
            return test_result

    def run_navigation_test(self):
        """Lance le test d'expérience navigation"""
        print("🎮 LANCEMENT TEST EXPÉRIENCE NAVIGATION")
        print("=" * 50)

        try:
            result = subprocess.run(
                [sys.executable, "tests/test_ui_navigation_experience.py"],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )

            test_result = {
                "name": "Navigation Experience",
                "success": result.returncode == 0,
                "duration": 0,
                "output": result.stdout,
                "errors": result.stderr,
                "score": 0,
            }

            # Extraire le score du rapport JSON généré
            try:
                import glob

                report_files = glob.glob("navigation_experience_report_*.json")
                if report_files:
                    latest_report = max(report_files, key=lambda x: x.split("_")[-1].split(".")[0])
                    with open(latest_report, encoding="utf-8") as f:
                        report_data = json.load(f)
                        test_result["score"] = report_data.get("overall_score", 0)
            except Exception:
                pass

            self.results["tests_run"].append(test_result)
            return test_result

        except subprocess.TimeoutExpired:
            test_result = {
                "name": "Navigation Experience",
                "success": False,
                "duration": 60,
                "output": "",
                "errors": "Timeout après 60 secondes",
                "score": 0,
            }
            self.results["tests_run"].append(test_result)
            return test_result

    def run_boutons_test(self):
        """Lance le test d'expérience boutons et actions"""
        print("🎮 LANCEMENT TEST EXPÉRIENCE BOUTONS ET ACTIONS")
        print("=" * 50)

        try:
            result = subprocess.run(
                [sys.executable, "tests/test_ui_boutons_actions_experience.py"],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )

            test_result = {
                "name": "Boutons Actions Experience",
                "success": result.returncode == 0,
                "duration": 0,
                "output": result.stdout,
                "errors": result.stderr,
                "score": 0,
            }

            # Extraire le score du rapport JSON généré
            try:
                import glob

                report_files = glob.glob("boutons_actions_experience_report_*.json")
                if report_files:
                    latest_report = max(report_files, key=lambda x: x.split("_")[-1].split(".")[0])
                    with open(latest_report, encoding="utf-8") as f:
                        report_data = json.load(f)
                        test_result["score"] = report_data.get("overall_score", 0)
            except Exception:
                pass

            self.results["tests_run"].append(test_result)
            return test_result

        except subprocess.TimeoutExpired:
            test_result = {
                "name": "Boutons Actions Experience",
                "success": False,
                "duration": 60,
                "output": "",
                "errors": "Timeout après 60 secondes",
                "score": 0,
            }
            self.results["tests_run"].append(test_result)
            return test_result

    def run_pwa_mobile_test(self):
        """Lance le test d'expérience PWA et mobile"""
        print("🎮 LANCEMENT TEST EXPÉRIENCE PWA ET MOBILE")
        print("=" * 50)

        try:
            result = subprocess.run(
                [sys.executable, "tests/test_ui_pwa_mobile_experience.py"],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )

            test_result = {
                "name": "PWA Mobile Experience",
                "success": result.returncode == 0,
                "duration": 0,
                "output": result.stdout,
                "errors": result.stderr,
                "score": 0,
            }

            # Extraire le score du rapport JSON généré
            try:
                import glob

                report_files = glob.glob("pwa_mobile_experience_report_*.json")
                if report_files:
                    latest_report = max(report_files, key=lambda x: x.split("_")[-1].split(".")[0])
                    with open(latest_report, encoding="utf-8") as f:
                        report_data = json.load(f)
                        test_result["score"] = report_data.get("overall_score", 0)
            except Exception:
                pass

            self.results["tests_run"].append(test_result)
            return test_result

        except subprocess.TimeoutExpired:
            test_result = {
                "name": "PWA Mobile Experience",
                "success": False,
                "duration": 60,
                "output": "",
                "errors": "Timeout après 60 secondes",
                "score": 0,
            }
            self.results["tests_run"].append(test_result)
            return test_result

    def run_all_tests(self):
        """Lance tous les tests d'expérience"""
        print("🎮 ARKALIA QUEST - LANCEUR DE TESTS D'EXPÉRIENCE COMPLETS")
        print("=" * 70)
        print("🚀 Démarrage de la batterie complète de tests d'expérience joueur...")
        print()

        start_time = time.time()

        # Lancement de tous les tests
        self.run_tutoriel_test()
        self.run_terminal_test()
        self.run_navigation_test()
        self.run_boutons_test()
        self.run_pwa_mobile_test()

        total_time = time.time() - start_time

        # Calcul du score global
        total_score = 0
        successful_tests = 0

        for test in self.results["tests_run"]:
            total_score += test["score"]
            if test["success"]:
                successful_tests += 1

        self.results["overall_score"] = (
            total_score / len(self.results["tests_run"]) if self.results["tests_run"] else 0
        )

        # Génération du résumé
        self.results["summary"] = {
            "total_tests": len(self.results["tests_run"]),
            "successful_tests": successful_tests,
            "success_rate": (
                (successful_tests / len(self.results["tests_run"]) * 100)
                if self.results["tests_run"]
                else 0
            ),
            "total_time": total_time,
            "average_score": self.results["overall_score"],
        }

        # Génération des recommandations
        self._generate_recommendations()

        # Affichage du rapport final
        self._display_final_report()

        return self.results

    def _generate_recommendations(self):
        """Génère des recommandations basées sur les résultats"""
        recommendations = []

        # Analyser les scores par test
        test_scores = {test["name"]: test["score"] for test in self.results["tests_run"]}

        for test_name, score in test_scores.items():
            if score < 40:
                recommendations.append(
                    f"❌ {test_name}: Nécessite une amélioration majeure (score:"
                    "{score:.1f}/100)",
                )
            elif score < 60:
                recommendations.append(
                    f"⚠️ {test_name}: Amélioration recommandée (score:" + "{score:.1f}/100)",
                )
            elif score < 80:
                recommendations.append(
                    f"👍 {test_name}: Bon, peut être optimisé (score: {score:.1f}/100)",
                )
            else:
                recommendations.append(f"🎉 {test_name}: Excellent (score: {score:.1f}/100)")

        # Recommandations générales
        if self.results["overall_score"] < 50:
            recommendations.append("🚨 EXPÉRIENCE GLOBALE: Amélioration majeure nécessaire")
        elif self.results["overall_score"] < 70:
            recommendations.append("⚠️  EXPÉRIENCE GLOBALE: Amélioration recommandée")
        elif self.results["overall_score"] < 85:
            recommendations.append("👍 EXPÉRIENCE GLOBALE: Bonne, optimisations possibles")
        else:
            recommendations.append("🎉 EXPÉRIENCE GLOBALE: Excellente !")

        self.results["recommendations"] = recommendations

    def _display_final_report(self):
        """Affiche le rapport final"""
        print("\n" + "=" * 70)
        print("📊 RAPPORT FINAL - TESTS D'EXPÉRIENCE ARKALIA QUEST")
        print("=" * 70)

        print(f"\n🎯 SCORE GLOBAL: {self.results['overall_score']:.1f}/100")
        print(f"⏱️  Temps total: {self.results['summary']['total_time']:.2f} secondes")
        print(f"🧪 Tests effectués: {self.results['summary']['total_tests']}")
        print(f"✅ Tests réussis: {self.results['summary']['successful_tests']}")
        print(f"📈 Taux de réussite: {self.results['summary']['success_rate']:.1f}%")

        print("\n📋 DÉTAIL PAR TEST:")
        print("-" * 50)

        for test in self.results["tests_run"]:
            status = "✅" if test["success"] else "❌"
            print(f"{status} {test['name']}: {test['score']:.1f}/100")

        print("\n💡 RECOMMANDATIONS:")
        print("-" * 50)

        for recommendation in self.results["recommendations"]:
            print(f"  {recommendation}")

        # Évaluation finale
        print("\n🏁 CONCLUSION:")
        print("-" * 50)

        if self.results["overall_score"] >= 85:
            print("🎉 EXPÉRIENCE UTILISATEUR EXCELLENTE !")
            print("   Le jeu offre une expérience immersive et fluide.")
        elif self.results["overall_score"] >= 70:
            print("👍 EXPÉRIENCE UTILISATEUR BONNE")
            print("   Quelques améliorations peuvent optimiser l'expérience.")
        elif self.results["overall_score"] >= 50:
            print("⚠️  EXPÉRIENCE UTILISATEUR MOYENNE")
            print("   Des améliorations sont nécessaires pour une meilleure expérience.")
        else:
            print("❌ EXPÉRIENCE UTILISATEUR À AMÉLIORER")
            print("   Des améliorations majeures sont nécessaires.")

        # Sauvegarde du rapport
        filename = f"experience_tests_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Rapport complet sauvegardé: {filename}")


def main():
    """Fonction principale"""
    runner = ExperienceTestRunner()
    results = runner.run_all_tests()

    return results


if __name__ == "__main__":
    main()
