"""
Testeur d'expérience joueur - Navigation Arkalia Quest
Teste la navigation entre toutes les pages et évalue l'UX
"""

import json
import time
from datetime import datetime

import requests


class NavigationExperienceTester:
    """Testeur d'expérience pour la navigation"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "test_name": "Navigation Experience Test",
            "timestamp": datetime.now().isoformat(),
            "pages_tested": [],
            "overall_score": 0,
            "navigation_issues": [],
            "positive_features": [],
        }

    def test_all_pages(self):
        """Test de toutes les pages principales"""
        game_logger.info(r"🧪 Test de toutes les pages principales...")

        pages = [
            {
                "name": "Accueil",
                "url": "/",
                "expected_elements": ["arkalia", "terminal", "monde"],
            },
            {
                "name": "Terminal",
                "url": "/terminal",
                "expected_elements": ["terminal", "commande", "aide"],
            },
            {
                "name": "Monde",
                "url": "/monde",
                "expected_elements": ["monde", "univers", "portail"],
            },
            {
                "name": "Profil",
                "url": "/profil",
                "expected_elements": ["profil", "score", "badge"],
            },
            {
                "name": "Dashboard",
                "url": "/dashboard",
                "expected_elements": ["dashboard", "statut"],
            },
            {
                "name": "Explorateur",
                "url": "/explorateur",
                "expected_elements": ["explorateur", "fichier"],
            },
            {
                "name": "Mail",
                "url": "/mail",
                "expected_elements": ["mail", "email", "message"],
            },
            {
                "name": "Audio",
                "url": "/audio",
                "expected_elements": ["audio", "son", "musique"],
            },
            {
                "name": "Leaderboard",
                "url": "/leaderboard",
                "expected_elements": ["leaderboard", "classement"],
            },
        ]

        for page in pages:
            page_result = self._test_single_page(page)
            self.results["pages_tested"].append(page_result)

        return self.results["pages_tested"]

    def test_navigation_flow(self):
        """Test du flux de navigation typique"""
        game_logger.info(r"🧪 Test du flux de navigation typique...")

        flow_result = {
            "name": "Flux de navigation",
            "steps": [],
            "total_time": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Flux typique: Accueil -> Terminal -> Monde -> Profil -> Leaderboard
        flow_steps = [
            {"name": "Accueil vers Terminal", "from": "/", "to": "/terminal"},
            {"name": "Terminal vers Monde", "from": "/terminal", "to": "/monde"},
            {"name": "Monde vers Profil", "from": "/monde", "to": "/profil"},
            {
                "name": "Profil vers Leaderboard",
                "from": "/profil",
                "to": "/leaderboard",
            },
            {"name": "Leaderboard vers Accueil", "from": "/leaderboard", "to": "/"},
        ]

        for step in flow_steps:
            step_result = self._test_navigation_step(step)
            flow_result["steps"].append(step_result)

        flow_result["total_time"] = time.time() - start_time
        flow_result["success"] = all(
            step.get("success", False) for step in flow_result["steps"]
        )

        # Évaluer la fluidité
        if flow_result["success"]:
            if flow_result["total_time"] < 5.0:
                flow_result["positives"].append("Navigation très fluide")
            elif flow_result["total_time"] < 10.0:
                flow_result["positives"].append("Navigation fluide")
            else:
                flow_result["issues"].append("Navigation lente")

        self.results["pages_tested"].append(flow_result)
        return flow_result

    def test_mobile_navigation(self):
        """Test de la navigation mobile"""
        game_logger.info(r"🧪 Test de la navigation mobile...")

        mobile_result = {
            "name": "Navigation mobile",
            "tests": [],
            "total_time": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test des pages principales sur mobile (simulation)
        mobile_pages = ["/", "/terminal", "/monde", "/profil"]

        for page in mobile_pages:
            test_result = self._test_mobile_page(page)
            mobile_result["tests"].append(test_result)

        mobile_result["total_time"] = time.time() - start_time
        mobile_result["success"] = any(
            test.get("success", False) for test in mobile_result["tests"]
        )

        if mobile_result["success"]:
            mobile_result["positives"].append("Navigation mobile fonctionnelle")
        else:
            mobile_result["issues"].append("Navigation mobile problématique")

        self.results["pages_tested"].append(mobile_result)
        return mobile_result

    def _test_single_page(self, page_info):
        """Test d'une page individuelle"""
        page_result = {
            "name": page_info["name"],
            "url": page_info["url"],
            "load_time": 0,
            "success": False,
            "elements_found": [],
            "elements_missing": [],
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            response = requests.get(f"{self.base_url}{page_info['url']}", timeout=10)
            page_result["load_time"] = time.time() - start_time

            if response.status_code == 200:
                page_result["success"] = True
                content = response.text.lower()

                # Vérifier les éléments attendus
                for element in page_info["expected_elements"]:
                    if element in content:
                        page_result["elements_found"].append(element)
                    else:
                        page_result["elements_missing"].append(element)

                # Évaluer le temps de chargement
                if page_result["load_time"] < 1.0:
                    page_result["positives"].append("Chargement rapide")
                elif page_result["load_time"] < 3.0:
                    page_result["positives"].append("Chargement acceptable")
                else:
                    page_result["issues"].append("Chargement lent")

                # Évaluer la présence d'éléments clés
                if (
                    len(page_result["elements_found"])
                    >= len(page_info["expected_elements"]) * 0.8
                ):
                    page_result["positives"].append("Contenu complet")
                elif (
                    len(page_result["elements_found"])
                    >= len(page_info["expected_elements"]) * 0.5
                ):
                    page_result["positives"].append("Contenu partiel")
                else:
                    page_result["issues"].append("Contenu incomplet")

                # Vérifier la présence de navigation
                if "nav" in content or "menu" in content or "lien" in content:
                    page_result["positives"].append("Navigation présente")
                else:
                    page_result["issues"].append("Navigation manquante")

            else:
                page_result["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            page_result["issues"].append(f"Erreur de connexion: {e!s}")

        return page_result

    def _test_navigation_step(self, step_info):
        """Test d'une étape de navigation"""
        step_result = {
            "name": step_info["name"],
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de navigation de la page source vers la page destination
            response = requests.get(f"{self.base_url}{step_info['to']}", timeout=5)
            step_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                step_result["success"] = True

                # Vérifier que la page de destination se charge correctement
                content = response.text
                if len(content) > 1000:  # Page avec du contenu
                    step_result["positives"].append("Page de destination chargée")
                else:
                    step_result["issues"].append("Page de destination vide")

                # Évaluer la rapidité de transition
                if step_result["duration"] < 1.0:
                    step_result["positives"].append("Transition rapide")
                elif step_result["duration"] < 3.0:
                    step_result["positives"].append("Transition acceptable")
                else:
                    step_result["issues"].append("Transition lente")

            else:
                step_result["issues"].append(
                    f"Erreur navigation: {response.status_code}"
                )

        except Exception as e:
            step_result["issues"].append(f"Erreur transition: {e!s}")

        return step_result

    def _test_mobile_page(self, page_url):
        """Test d'une page pour mobile"""
        test_result = {
            "page": page_url,
            "success": False,
            "mobile_friendly": False,
            "issues": [],
            "positives": [],
        }

        try:
            response = requests.get(f"{self.base_url}{page_url}", timeout=5)

            if response.status_code == 200:
                test_result["success"] = True
                content = response.text

                # Vérifier les éléments de responsive design
                if "viewport" in content.lower():
                    test_result["mobile_friendly"] = True
                    test_result["positives"].append("Viewport mobile configuré")
                else:
                    test_result["issues"].append("Viewport mobile manquant")

                if "media" in content.lower() and "max-width" in content.lower():
                    test_result["positives"].append("CSS responsive présent")
                else:
                    test_result["issues"].append("CSS responsive manquant")

                if "touch" in content.lower() or "mobile" in content.lower():
                    test_result["positives"].append("Optimisations tactiles")
                else:
                    test_result["issues"].append("Optimisations tactiles manquantes")

            else:
                test_result["issues"].append(f"Erreur page: {response.status_code}")

        except Exception as e:
            test_result["issues"].append(f"Erreur mobile: {e!s}")

        return test_result

    def run_all_tests(self):
        """Lance tous les tests de navigation"""
        print("🎮 ARKALIA QUEST - TESTEUR D'EXPÉRIENCE NAVIGATION")
        print("=" * 60)

        # Test de toutes les pages
        self.test_all_pages()

        # Test du flux de navigation
        self.test_navigation_flow()

        # Test de la navigation mobile
        self.test_mobile_navigation()

        # Calcul du score global
        total_success = 0
        total_tests = 0

        for page in self.results["pages_tested"]:
            if page.get("success", False):
                total_success += 1
            total_tests += 1

        self.results["overall_score"] = (
            (total_success / total_tests * 100) if total_tests > 0 else 0
        )

        # Génération du rapport
        self._generate_report()

        return self.results

    def _generate_report(self):
        """Génère le rapport final"""
        print("\n📊 RAPPORT D'EXPÉRIENCE NAVIGATION")
        print("=" * 60)
        print(f"🎯 Score global: {self.results['overall_score']:.1f}/100")
        print(f"📄 Pages testées: {len(self.results['pages_tested'])}")

        for page in self.results["pages_tested"]:
            print(f"\n📄 {page['name']}:")
            if "load_time" in page:
                print(f"   ⏱️  Temps de chargement: {page['load_time']:.2f}s")
            if "total_time" in page:
                print(f"   ⏱️  Temps total: {page['total_time']:.2f}s")

            if page.get("success", False):
                game_logger.info(r"   ✅ Succès")
            else:
                game_logger.info(r"   ❌ Échec")

            if page.get("elements_found"):
                print(f"   🔍 Éléments trouvés: {len(page['elements_found'])}")
            if page.get("elements_missing"):
                print(f"   ❌ Éléments manquants: {len(page['elements_missing'])}")

            if page.get("issues"):
                print(f"   ⚠️  Problèmes: {len(page['issues'])}")
            if page.get("positives"):
                print(f"   👍 Points positifs: {len(page['positives'])}")

        # Sauvegarde du rapport
        filename = f"navigation_experience_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        game_logger.info(f"\n💾 Rapport sauvegardé: {filename}")


def main():
    """Fonction principale"""
    tester = NavigationExperienceTester()
    results = tester.run_all_tests()

    # Évaluation finale
    if results["overall_score"] >= 80:
        game_logger.info(r"\n🎉 EXPÉRIENCE NAVIGATION EXCELLENTE !")
    elif results["overall_score"] >= 60:
        game_logger.info(r"\n👍 EXPÉRIENCE NAVIGATION BONNE")
    elif results["overall_score"] >= 40:
        game_logger.info(r"\n⚠️  EXPÉRIENCE NAVIGATION MOYENNE")
    else:
        game_logger.info(r"\n❌ EXPÉRIENCE NAVIGATION À AMÉLIORER")


if __name__ == "__main__":
    main()
