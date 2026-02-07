"""
Testeur d'expérience joueur - PWA et Mobile Arkalia Quest
Teste l'installation PWA, le mode offline, et la réactivité mobile
"""

import json
import os
import sys
import time
from datetime import datetime

import requests

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import du logger
from utils.logger import game_logger


class PWAMobileExperienceTester:
    """Testeur d'expérience pour PWA et mobile"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "test_name": "PWA Mobile Experience Test",
            "timestamp": datetime.now().isoformat(),
            "tests_performed": [],
            "overall_score": 0,
            "pwa_issues": [],
            "mobile_issues": [],
            "positive_features": [],
        }

    def test_pwa_manifest(self):
        """Test du manifest PWA"""
        game_logger.info(r"🧪 Test du manifest PWA...")

        manifest_result = {
            "name": "Manifest PWA",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test du manifest.json
            response = requests.get(f"{self.base_url}/static/manifest.json", timeout=5)
            manifest_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                try:
                    manifest_data = response.json()
                    manifest_result["success"] = True

                    # Vérifier les éléments essentiels du manifest
                    required_fields = [
                        "name",
                        "short_name",
                        "start_url",
                        "display",
                        "icons",
                    ]
                    present_fields = 0

                    for field in required_fields:
                        if field in manifest_data:
                            present_fields += 1

                    if present_fields >= 4:
                        manifest_result["positives"].append("Manifest complet")
                    elif present_fields >= 3:
                        manifest_result["positives"].append("Manifest partiel")
                    else:
                        manifest_result["issues"].append("Manifest incomplet")

                    # Vérifier les icônes
                    if "icons" in manifest_data and len(manifest_data["icons"]) >= 3:
                        manifest_result["positives"].append(
                            "Icônes multiples présentes"
                        )
                    else:
                        manifest_result["issues"].append("Icônes insuffisantes")

                    # Vérifier le nom
                    if "name" in manifest_data and len(manifest_data["name"]) > 0:
                        manifest_result["positives"].append("Nom PWA défini")
                    else:
                        manifest_result["issues"].append("Nom PWA manquant")

                except json.JSONDecodeError:
                    manifest_result["issues"].append("Manifest JSON invalide")

            else:
                manifest_result["issues"].append(
                    f"Manifest inaccessible: {response.status_code}"
                )

        except Exception as e:
            manifest_result["issues"].append(f"Erreur manifest: {e!s}")

        self.results["tests_performed"].append(manifest_result)
        return manifest_result

    def test_service_worker(self):
        """Test du service worker"""
        game_logger.info(r"🧪 Test du service worker...")

        sw_result = {
            "name": "Service Worker",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test du service worker
            response = requests.get(
                f"{self.base_url}/static/js/service-worker.js", timeout=5
            )
            sw_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                sw_result["success"] = True
                content = response.text

                # Vérifier la présence de fonctionnalités PWA
                if "install" in content.lower():
                    sw_result["positives"].append("Installation PWA supportée")
                else:
                    sw_result["issues"].append("Installation PWA non supportée")

                if "cache" in content.lower():
                    sw_result["positives"].append("Cache PWA configuré")
                else:
                    sw_result["issues"].append("Cache PWA non configuré")

                if "fetch" in content.lower():
                    sw_result["positives"].append("Interception fetch configurée")
                else:
                    sw_result["issues"].append("Interception fetch manquante")

                if "offline" in content.lower():
                    sw_result["positives"].append("Mode offline supporté")
                else:
                    sw_result["issues"].append("Mode offline non supporté")

            else:
                sw_result["issues"].append(
                    f"Service worker inaccessible: {response.status_code}"
                )

        except Exception as e:
            sw_result["issues"].append(f"Erreur service worker: {e!s}")

        self.results["tests_performed"].append(sw_result)
        return sw_result

    def test_pwa_installation(self):
        """Test de l'installation PWA"""
        print("🧪 Test de l'installation PWA...")

        install_result = {
            "name": "Installation PWA",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de la page d'accueil pour vérifier l'installation PWA
            response = requests.get(f"{self.base_url}/", timeout=5)
            install_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                content = response.text
                install_result["success"] = True

                # Vérifier les éléments d'installation PWA
                if "manifest.json" in content:
                    install_result["positives"].append("Manifest référencé")
                else:
                    install_result["issues"].append("Manifest non référencé")

                if "service-worker" in content:
                    install_result["positives"].append("Service worker référencé")
                else:
                    install_result["issues"].append("Service worker non référencé")

                if "beforeinstallprompt" in content.lower():
                    install_result["positives"].append(
                        "Prompt d'installation configuré"
                    )
                else:
                    install_result["issues"].append("Prompt d'installation manquant")

                if (
                    "add to home screen" in content.lower()
                    or "install" in content.lower()
                ):
                    install_result["positives"].append(
                        "Interface d'installation présente"
                    )
                else:
                    install_result["issues"].append(
                        "Interface d'installation manquante"
                    )

            else:
                install_result["issues"].append(
                    f"Page d'accueil inaccessible: {response.status_code}",
                )

        except Exception as e:
            install_result["issues"].append(f"Erreur installation: {e!s}")

        self.results["tests_performed"].append(install_result)
        return install_result

    def test_offline_functionality(self):
        """Test du mode offline"""
        game_logger.info(r"🧪 Test du mode offline...")

        offline_result = {
            "name": "Mode Offline",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de la disponibilité des ressources essentielles
            essential_resources = [
                "/static/manifest.json",
                "/static/js/service-worker.js",
                "/static/css/style.css",
                "/static/js/terminal.js",
                "/favicon.ico",
            ]

            available_resources = 0

            for resource in essential_resources:
                try:
                    response = requests.get(f"{self.base_url}{resource}", timeout=3)
                    if response.status_code == 200:
                        available_resources += 1
                except Exception:
                    pass

            offline_result["duration"] = time.time() - start_time
            offline_result["success"] = available_resources > 0

            if available_resources >= 4:
                offline_result["positives"].append("Ressources offline complètes")
            elif available_resources >= 2:
                offline_result["positives"].append("Ressources offline partielles")
            else:
                offline_result["issues"].append("Ressources offline insuffisantes")

            # Vérifier la présence de cache dans le service worker
            sw_response = requests.get(
                f"{self.base_url}/static/js/service-worker.js", timeout=3
            )
            if sw_response.status_code == 200:
                if "cache" in sw_response.text.lower():
                    offline_result["positives"].append("Cache configuré pour offline")
                else:
                    offline_result["issues"].append("Cache offline non configuré")

        except Exception as e:
            offline_result["issues"].append(f"Erreur mode offline: {e!s}")

        self.results["tests_performed"].append(offline_result)
        return offline_result

    def test_mobile_responsiveness(self):
        """Test de la réactivité mobile"""
        game_logger.info(r"🧪 Test de la réactivité mobile...")

        mobile_result = {
            "name": "Réactivité Mobile",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de la page d'accueil pour vérifier le responsive
            response = requests.get(f"{self.base_url}/", timeout=5)
            mobile_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                content = response.text
                mobile_result["success"] = True

                # Vérifier les éléments de responsive design
                if "viewport" in content.lower():
                    mobile_result["positives"].append("Viewport mobile configuré")
                else:
                    mobile_result["issues"].append("Viewport mobile manquant")

                if "media" in content.lower() and "max-width" in content.lower():
                    mobile_result["positives"].append("CSS responsive présent")
                else:
                    mobile_result["issues"].append("CSS responsive manquant")

                if "touch" in content.lower() or "mobile" in content.lower():
                    mobile_result["positives"].append("Optimisations tactiles")
                else:
                    mobile_result["issues"].append("Optimisations tactiles manquantes")

                # Vérifier la présence de CSS mobile
                css_response = requests.get(
                    f"{self.base_url}/static/css/style.css", timeout=3
                )
                if css_response.status_code == 200:
                    css_content = css_response.text
                    if "@media" in css_content:
                        mobile_result["positives"].append("Media queries présentes")
                    else:
                        mobile_result["issues"].append("Media queries manquantes")

            else:
                mobile_result["issues"].append(
                    f"Page inaccessible: {response.status_code}"
                )

        except Exception as e:
            mobile_result["issues"].append(f"Erreur mobile: {e!s}")

        self.results["tests_performed"].append(mobile_result)
        return mobile_result

    def test_mobile_performance(self):
        """Test de la performance mobile"""
        game_logger.info(r"🧪 Test de la performance mobile...")

        performance_result = {
            "name": "Performance Mobile",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de performance avec des requêtes rapides
            pages_to_test = ["/", "/terminal", "/monde", "/profil"]
            load_times = []

            for page in pages_to_test:
                page_start = time.time()
                try:
                    response = requests.get(f"{self.base_url}{page}", timeout=3)
                    if response.status_code == 200:
                        load_times.append(time.time() - page_start)
                except Exception:
                    load_times.append(5.0)  # Timeout

            performance_result["duration"] = time.time() - start_time
            performance_result["success"] = len(load_times) > 0

            if performance_result["success"]:
                avg_load_time = sum(load_times) / len(load_times)

                if avg_load_time < 1.0:
                    performance_result["positives"].append(
                        "Performance mobile excellente"
                    )
                elif avg_load_time < 2.0:
                    performance_result["positives"].append("Performance mobile bonne")
                elif avg_load_time < 3.0:
                    performance_result["positives"].append(
                        "Performance mobile acceptable"
                    )
                else:
                    performance_result["issues"].append("Performance mobile lente")

            else:
                performance_result["issues"].append("Performance mobile insuffisante")

        except Exception as e:
            performance_result["issues"].append(f"Erreur performance: {e!s}")

        self.results["tests_performed"].append(performance_result)
        return performance_result

    def test_mobile_accessibility(self):
        """Test de l'accessibilité mobile"""
        print("🧪 Test de l'accessibilité mobile...")

        accessibility_result = {
            "name": "Accessibilité Mobile",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test d'accessibilité mobile (simulation)
            response = requests.get(f"{self.base_url}/", timeout=5)
            accessibility_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                content = response.text
                accessibility_result["success"] = True

                # Vérifier les éléments d'accessibilité
                if "aria" in content.lower():
                    accessibility_result["positives"].append("Attributs ARIA présents")
                else:
                    accessibility_result["issues"].append("Attributs ARIA manquants")

                if "alt=" in content.lower():
                    accessibility_result["positives"].append(
                        "Textes alternatifs présents"
                    )
                else:
                    accessibility_result["issues"].append(
                        "Textes alternatifs manquants"
                    )

                if "tabindex" in content.lower():
                    accessibility_result["positives"].append(
                        "Navigation clavier configurée"
                    )
                else:
                    accessibility_result["issues"].append(
                        "Navigation clavier manquante"
                    )

                # Vérifier la taille des éléments tactiles
                if "min-height: 44px" in content or "min-width: 44px" in content:
                    accessibility_result["positives"].append(
                        "Taille tactile appropriée"
                    )
                else:
                    accessibility_result["issues"].append("Taille tactile insuffisante")

            else:
                accessibility_result["issues"].append(
                    f"Page inaccessible: {response.status_code}"
                )

        except Exception as e:
            accessibility_result["issues"].append(f"Erreur accessibilité: {e!s}")

        self.results["tests_performed"].append(accessibility_result)
        return accessibility_result

    def test_notifications(self):
        """Test des notifications PWA"""
        game_logger.info(r"🧪 Test des notifications PWA...")

        notifications_result = {
            "name": "Notifications PWA",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de la configuration des notifications
            response = requests.get(f"{self.base_url}/", timeout=5)
            notifications_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                content = response.text
                notifications_result["success"] = True

                # Vérifier la présence de code de notifications
                if "notification" in content.lower():
                    notifications_result["positives"].append(
                        "Notifications configurées"
                    )
                else:
                    notifications_result["issues"].append(
                        "Notifications non configurées"
                    )

                if "permission" in content.lower():
                    notifications_result["positives"].append(
                        "Demande de permission configurée"
                    )
                else:
                    notifications_result["issues"].append(
                        "Demande de permission manquante"
                    )

                if "push" in content.lower():
                    notifications_result["positives"].append(
                        "Notifications push supportées"
                    )
                else:
                    notifications_result["issues"].append(
                        "Notifications push non supportées"
                    )

            else:
                notifications_result["issues"].append(
                    f"Page inaccessible: {response.status_code}"
                )

        except Exception as e:
            notifications_result["issues"].append(f"Erreur notifications: {e!s}")

        self.results["tests_performed"].append(notifications_result)
        return notifications_result

    def run_all_tests(self):
        """Lance tous les tests PWA et mobile"""
        print("🎮 ARKALIA QUEST - TESTEUR D'EXPÉRIENCE PWA ET MOBILE")
        print("=" * 60)

        # Tests PWA
        self.test_pwa_manifest()
        self.test_service_worker()
        self.test_pwa_installation()
        self.test_offline_functionality()
        self.test_notifications()

        # Tests Mobile
        self.test_mobile_responsiveness()
        self.test_mobile_performance()
        self.test_mobile_accessibility()

        # Calcul du score global
        total_success = 0
        total_tests = 0

        for test in self.results["tests_performed"]:
            if test.get("success", False):
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
        print("\n📊 RAPPORT D'EXPÉRIENCE PWA ET MOBILE")
        print("=" * 60)
        print(f"🎯 Score global: {self.results['overall_score']:.1f}/100")
        print(f"🧪 Tests effectués: {len(self.results['tests_performed'])}")

        for test in self.results["tests_performed"]:
            print(f"\n🧪 {test['name']}:")
            print(f"   ⏱️  Durée: {test['duration']:.2f}s")

            if test.get("success", False):
                game_logger.info(r"   ✅ Succès")
            else:
                game_logger.info(r"   ❌ Échec")

            if test.get("issues"):
                print(f"   ⚠️  Problèmes: {len(test['issues'])}")
            if test.get("positives"):
                print(f"   👍 Points positifs: {len(test['positives'])}")

        # Sauvegarde du rapport
        filename = f"pwa_mobile_experience_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        game_logger.info(f"\n💾 Rapport sauvegardé: {filename}")


def main():
    """Fonction principale"""
    tester = PWAMobileExperienceTester()
    results = tester.run_all_tests()

    # Évaluation finale
    if results["overall_score"] >= 80:
        game_logger.info(r"\n🎉 EXPÉRIENCE PWA ET MOBILE EXCELLENTE !")
    elif results["overall_score"] >= 60:
        game_logger.info(r"\n👍 EXPÉRIENCE PWA ET MOBILE BONNE")
    elif results["overall_score"] >= 40:
        game_logger.info(r"\n⚠️  EXPÉRIENCE PWA ET MOBILE MOYENNE")
    else:
        game_logger.info(r"\n❌ EXPÉRIENCE PWA ET MOBILE À AMÉLIORER")


if __name__ == "__main__":
    main()
