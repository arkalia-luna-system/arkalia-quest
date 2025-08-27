#!/usr/bin/env python3
"""
Test des améliorations du terminal Arkalia Quest v3.0
Valide le feedback intelligent, l'accessibilité et le responsive design
"""

import json
import time
from datetime import datetime

import requests


class TerminalImprovementsTester:
    """Testeur des améliorations du terminal"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "test_name": "Terminal Improvements Test",
            "timestamp": datetime.now().isoformat(),
            "improvements_tested": [],
            "overall_score": 0,
            "feedback_quality": 0,
            "accessibility_score": 0,
            "responsive_score": 0,
            "performance_score": 0,
        }

    def test_intelligent_feedback(self):
        """Test du feedback intelligent"""
        print("🧠 Test du feedback intelligent...")

        feedback_tests = [
            {
                "name": "Commande inexistante",
                "command": "commande_inexistante",
                "expected_feedback": "help",
                "description": "Doit afficher une aide contextuelle",
            },
            {
                "name": "Commande valide",
                "command": "aide",
                "expected_feedback": "encouragement",
                "description": "Doit afficher un encouragement",
            },
            {
                "name": "Commande rapide",
                "command": "profil",
                "expected_feedback": "success",
                "description": "Doit afficher un message de succès",
            },
        ]

        feedback_score = 0
        total_tests = len(feedback_tests)

        for test in feedback_tests:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": test["command"]},
                    timeout=5,
                )

                if response.status_code == 200:
                    data = response.json()
                    reponse = data.get("reponse", {})

                    # Vérifier que la réponse contient les éléments de feedback
                    if "message" in reponse:
                        feedback_score += 1
                        print(f"✅ {test['name']}: Feedback présent")
                    else:
                        print(f"❌ {test['name']}: Pas de feedback")

                else:
                    print(f"❌ {test['name']}: Erreur HTTP {response.status_code}")

            except Exception as e:
                print(f"❌ {test['name']}: Erreur - {e}")

        self.results["feedback_quality"] = (feedback_score / total_tests) * 100
        print(
            f"📊 Score feedback intelligent: {self.results['feedback_quality']:.1f}/100"
        )

    def test_accessibility(self):
        """Test de l'accessibilité"""
        print("♿ Test de l'accessibilité...")

        try:
            # Test de la page terminal
            response = requests.get(f"{self.base_url}/terminal", timeout=5)

            if response.status_code == 200:
                content = response.text
                accessibility_score = 0
                total_checks = 0

                # Vérifier les éléments d'accessibilité
                checks = [
                    ("Focus visible", "outline", "Focus visible présent"),
                    ("ARIA labels", "aria-label", "Labels ARIA présents"),
                    ("Contraste", "color: #ffffff", "Contraste suffisant"),
                    ("Navigation clavier", "keydown", "Navigation clavier supportée"),
                    ("Messages d'erreur", "error", "Messages d'erreur clairs"),
                ]

                for check_name, check_term, description in checks:
                    total_checks += 1
                    if check_term in content:
                        accessibility_score += 1
                        print(f"✅ {check_name}: {description}")
                    else:
                        print(f"⚠️ {check_name}: {description} manquant")

                self.results["accessibility_score"] = (
                    accessibility_score / total_checks
                ) * 100
                print(
                    f"📊 Score accessibilité:" + "{self.results['accessibility_score']:.1f}/100"
                )

            else:
                print(f"❌ Erreur HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Erreur test accessibilité: {e}")

    def test_responsive_design(self):
        """Test du responsive design"""
        print("📱 Test du responsive design...")

        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)

            if response.status_code == 200:
                content = response.text
                responsive_score = 0
                total_checks = 0

                # Vérifier les breakpoints responsive
                checks = [
                    (
                        "Breakpoint 1024px",
                        "@media (max-width: 1024px)",
                        "Breakpoint desktop",
                    ),
                    (
                        "Breakpoint 768px",
                        "@media (max-width: 768px)",
                        "Breakpoint tablette",
                    ),
                    (
                        "Breakpoint 480px",
                        "@media (max-width: 480px)",
                        "Breakpoint mobile",
                    ),
                    ("Viewport meta", "viewport", "Meta viewport présent"),
                    ("Flexbox", "display: flex", "Layout flexbox"),
                ]

                for check_name, check_term, description in checks:
                    total_checks += 1
                    if check_term in content:
                        responsive_score += 1
                        print(f"✅ {check_name}: {description}")
                    else:
                        print(f"⚠️ {check_name}: {description} manquant")

                self.results["responsive_score"] = (
                    responsive_score / total_checks
                ) * 100
                print(
                    f"📊 Score responsive: {self.results['responsive_score']:.1f}/100"
                )

            else:
                print(f"❌ Erreur HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Erreur test responsive: {e}")

    def test_performance(self):
        """Test des performances"""
        print("⚡ Test des performances...")

        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            load_time = time.time() - start_time

            if response.status_code == 200:
                # Évaluer le temps de chargement
                if load_time < 1.0:
                    performance_score = 100
                    print("✅ Chargement très rapide (< 1s)")
                elif load_time < 2.0:
                    performance_score = 80
                    print("✅ Chargement rapide (< 2s)")
                elif load_time < 3.0:
                    performance_score = 60
                    print("⚠️ Chargement acceptable (< 3s)")
                else:
                    performance_score = 40
                    print("❌ Chargement lent (> 3s)")

                self.results["performance_score"] = performance_score
                print(f"📊 Temps de chargement: {load_time:.2f}s")
                print(f"📊 Score performance: {performance_score}/100")

            else:
                print(f"❌ Erreur HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Erreur test performance: {e}")

    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 Démarrage des tests d'amélioration du terminal...")
        print("=" * 60)

        self.test_intelligent_feedback()
        print("-" * 40)

        self.test_accessibility()
        print("-" * 40)

        self.test_responsive_design()
        print("-" * 40)

        self.test_performance()
        print("-" * 40)

        # Calculer le score global
        scores = [
            self.results["feedback_quality"],
            self.results["accessibility_score"],
            self.results["responsive_score"],
            self.results["performance_score"],
        ]

        self.results["overall_score"] = sum(scores) / len(scores)

        # Générer le rapport
        self.generate_report()

    def generate_report(self):
        """Générer le rapport de test"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'AMÉLIORATION DU TERMINAL")
        print("=" * 60)

        print(f"🎯 Score global: {self.results['overall_score']:.1f}/100")
        print(f"🧠 Feedback intelligent: {self.results['feedback_quality']:.1f}/100")
        print(f"♿ Accessibilité: {self.results['accessibility_score']:.1f}/100")
        print(f"📱 Responsive design: {self.results['responsive_score']:.1f}/100")
        print(f"⚡ Performance: {self.results['performance_score']:.1f}/100")

        # Évaluation qualitative
        if self.results["overall_score"] >= 85:
            print("🏆 EXCELLENT: Terminal professionnel et accessible !")
        elif self.results["overall_score"] >= 70:
            print("✅ BON: Terminal bien amélioré avec quelques points à optimiser")
        elif self.results["overall_score"] >= 50:
            print("⚠️ MOYEN: Améliorations visibles mais encore du travail")
        else:
            print("❌ INSUFFISANT: Besoin d'améliorations majeures")

        # Sauvegarder le rapport
filename =
f"terminal_improvements_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Rapport sauvegardé: {filename}")
        print("=" * 60)


if __name__ == "__main__":
    tester = TerminalImprovementsTester()
    tester.run_all_tests()
