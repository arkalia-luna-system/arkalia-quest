#!/usr/bin/env python3
"""
🔍 ANALYSE FINALE COMPLÈTE - ARKALIA QUEST
Analyse complète du projet comme si j'étais ton fils qui vérifie que tout est parfait
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path


class AnalyseurProjet:
    """Analyseur complet du projet Arkalia Quest"""

    def __init__(self):
        self.projet_root = Path(__file__).parent.parent
        self.resultats = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "performance": {},
            "robustesse": {},
            "couverture": {},
            "erreurs": [],
            "recommandations": [],
            "score_global": 0,
        }

    def analyser_structure_projet(self):
        """Analyse la structure générale du projet"""
        game_logger.info(r"📁 ANALYSE DE LA STRUCTURE DU PROJET")
        print("=" * 50)

        # Vérifier les composants critiques
        composants_critiques = [
            "app.py",
            "core/",
            "tests/",
            "static/",
            "templates/",
            "requirements.txt",
        ]

        composants_presents = []
        for composant in composants_critiques:
            if (self.projet_root / composant).exists():
                composants_presents.append(composant)
                game_logger.info(f"✅ {composant}")
            else:
                game_logger.info(f"❌ {composant} - MANQUANT")
                self.resultats["erreurs"].append(f"Composant manquant: {composant}")

        # Vérifier la taille des répertoires
        game_logger.info(r"\n📊 TAILLE DES RÉPERTOIRES:")
        for dir_name in ["core", "tests", "static", "templates"]:
            dir_path = self.projet_root / dir_name
            if dir_path.exists():
                file_count = (
                    len(list(dir_path.rglob("*.py")))
                    if dir_name == "core"
                    else len(list(dir_path.rglob("*")))
                )
                game_logger.info(f"   {dir_name}: {file_count} fichiers")

        self.resultats["structure"] = {
            "composants_presents": len(composants_presents),
            "composants_totaux": len(composants_critiques),
            "score": len(composants_presents) / len(composants_critiques) * 100,
        }

        print(f"\n🎯 Score structure: {self.resultats['structure']['score']:.1f}%")

    def analyser_tests(self):
        """Analyse des tests du projet"""
        game_logger.info(r"\n🧪 ANALYSE DES TESTS")
        print("=" * 50)

        try:
            # Compter les tests
            tests_dir = self.projet_root / "tests"
            test_files = list(tests_dir.rglob("test_*.py"))
            test_count = len(test_files)

            game_logger.info(f"📁 Fichiers de test trouvés: {test_count}")

            # Lister les catégories de tests
            categories = {}
            for test_file in test_files:
                category = test_file.parent.name
                categories[category] = categories.get(category, 0) + 1

            game_logger.info(r"📋 Catégories de tests:")
            for cat, count in categories.items():
                game_logger.info(f"   {cat}: {count} fichiers")

            # Exécuter un test rapide pour vérifier la santé
            game_logger.info(r"\n🔍 Vérification rapide des tests...")
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "--collect-only", "-q"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.projet_root,
            )

            if result.returncode == 0:
                # Compter les tests collectés
                lines = result.stdout.split("\n")
                test_count_collected = 0
                for line in lines:
                    if "collected" in line and "items" in line:
                        test_count_collected = int(line.split()[0])
                        break

                game_logger.info(f"✅ Tests collectés: {test_count_collected}")
                self.resultats["tests"]["collectes"] = test_count_collected
            else:
                game_logger.info(r"❌ Erreur lors de la collecte des tests")
                self.resultats["erreurs"].append("Erreur collecte tests")

            self.resultats["tests"]["fichiers"] = test_count
            self.resultats["tests"]["categories"] = categories

        except Exception as e:
            game_logger.info(f"❌ Erreur analyse tests: {e}")
            self.resultats["erreurs"].append(f"Erreur analyse tests: {e}")

    def analyser_performance(self):
        """Analyse des performances"""
        game_logger.info(r"\n⚡ ANALYSE DES PERFORMANCES")
        print("=" * 50)

        try:
            # Vérifier si l'app tourne
            import requests

            try:
                response = requests.get("http://localhost:5001/", timeout=5)
                if response.status_code == 200:
                    game_logger.info(r"✅ Application accessible sur le port 5001")

                    # Test de performance rapide
                    start_time = time.time()
                    response = requests.get(
                        "http://localhost:5001/api/educational-games/list",
                        timeout=5,
                    )
                    response_time = time.time() - start_time

                    game_logger.info(f"⚡ Temps de réponse API: {response_time:.3f}s")

                    if response_time < 0.1:
                        game_logger.info(r"   🌟 EXCELLENT - Très rapide")
                        self.resultats["performance"]["api_speed"] = "excellent"
                    elif response_time < 0.5:
                        game_logger.info(r"   ✅ BON - Acceptable")
                        self.resultats["performance"]["api_speed"] = "bon"
                    else:
                        game_logger.info(r"   ⚠️  MOYEN - À améliorer")
                        self.resultats["performance"]["api_speed"] = "moyen"

                    self.resultats["performance"]["response_time"] = response_time
                    self.resultats["performance"]["status"] = "accessible"

                else:
                    game_logger.info(
                        f"❌ Application accessible mais erreur {response.status_code}"
                    )
                    self.resultats["performance"]["status"] = "erreur_http"

            except requests.exceptions.RequestException:
                game_logger.info(r"❌ Application non accessible")
                self.resultats["performance"]["status"] = "inaccessible"
                self.resultats["erreurs"].append("Application non accessible")

        except ImportError:
            game_logger.info(r"⚠️  requests non installé - test de performance limité")
            self.resultats["performance"]["status"] = "requests_manquant"

    def analyser_robustesse(self):
        """Analyse de la robustesse"""
        game_logger.info(r"\n🛡️ ANALYSE DE LA ROBUSTESSE")
        print("=" * 50)

        try:
            # Vérifier les tests de robustesse
            robustesse_dir = self.projet_root / "tests" / "robustesse"
            if robustesse_dir.exists():
                robustesse_files = list(robustesse_dir.glob("*.py"))
                game_logger.info(
                    f"📁 Tests de robustesse: {len(robustesse_files)} fichiers"
                )

                # Exécuter un test de robustesse rapide
                game_logger.info(r"🔍 Test de robustesse rapide...")
                result = subprocess.run(
                    ["python", "-m", "pytest", "tests/robustesse/", "-v", "--tb=no"],
                    check=False,
                    capture_output=True,
                    text=True,
                    cwd=self.projet_root,
                    timeout=60,
                )

                if result.returncode == 0:
                    game_logger.info(r"✅ Tests de robustesse passent")
                    self.resultats["robustesse"]["status"] = "succes"
                else:
                    game_logger.info(r"❌ Tests de robustesse échouent")
                    self.resultats["robustesse"]["status"] = "echec"

                    # Analyser les erreurs
                    lines = result.stdout.split("\n")
                    for line in lines:
                        if "FAILED" in line or "ERROR" in line:
                            game_logger.info(f"   ⚠️  {line.strip()}")

            else:
                game_logger.info(r"❌ Répertoire de robustesse manquant")
                self.resultats["robustesse"]["status"] = "manquant"

        except Exception as e:
            game_logger.info(f"❌ Erreur analyse robustesse: {e}")
            self.resultats["erreurs"].append(f"Erreur analyse robustesse: {e}")

    def analyser_couverture(self):
        """Analyse de la couverture de code"""
        game_logger.info(r"\n📊 ANALYSE DE LA COUVERTURE")
        print("=" * 50)

        try:
            # Exécuter la couverture
            game_logger.info(r"🔍 Calcul de la couverture...")
            result = subprocess.run(
                ["python", "-m", "pytest", "--cov=core", "--cov-report=term-missing"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.projet_root,
                timeout=120,
            )

            if result.returncode == 0:
                # Parser la couverture
                lines = result.stdout.split("\n")
                for line in lines:
                    if "TOTAL" in line and "Cover" in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            try:
                                total_statements = int(parts[1])
                                missed_statements = int(parts[2])
                                coverage_percent = float(parts[3].rstrip("%"))

                                game_logger.info(
                                    f"📈 Couverture: {coverage_percent:.1f}%"
                                )
                                game_logger.info(f"   Total: {total_statements} lignes")
                                game_logger.info(
                                    f"   Manquées: {missed_statements} lignes"
                                )

                                if coverage_percent >= 80:
                                    game_logger.info(
                                        r"   🌟 EXCELLENT - Très bonne couverture"
                                    )
                                elif coverage_percent >= 60:
                                    game_logger.info(
                                        r"   ✅ BON - Couverture acceptable"
                                    )
                                elif coverage_percent >= 40:
                                    game_logger.info(r"   ⚠️  MOYEN - À améliorer")
                                else:
                                    game_logger.info(
                                        r"   ❌ FAIBLE - Couverture insuffisante"
                                    )

                                self.resultats["couverture"] = {
                                    "pourcentage": coverage_percent,
                                    "total": total_statements,
                                    "manquees": missed_statements,
                                }

                            except (ValueError, IndexError):
                                game_logger.info(
                                    r"⚠️  Impossible de parser la couverture"
                                )
                                break
                        break
            else:
                game_logger.info(r"❌ Erreur lors du calcul de la couverture")
                self.resultats["erreurs"].append("Erreur calcul couverture")

        except Exception as e:
            game_logger.info(f"❌ Erreur analyse couverture: {e}")
            self.resultats["erreurs"].append(f"Erreur analyse couverture: {e}")

    def calculer_score_global(self):
        """Calcule le score global du projet"""
        game_logger.info(r"\n🎯 CALCUL DU SCORE GLOBAL")
        print("=" * 50)

        score = 0

        # Score structure (25 points)
        if "structure" in self.resultats:
            score += (self.resultats["structure"]["score"] / 100) * 25
            print(
                f"🏗️  Structure: {self.resultats['structure']['score']:.1f}% → {score:.1f}/25"
            )

        # Score tests (25 points)
        if "tests" in self.resultats and "collectes" in self.resultats["tests"]:
            test_score = min(self.resultats["tests"]["collectes"] / 100, 1.0) * 25
            score += test_score
            print(
                f"🧪 Tests: {self.resultats['tests']['collectes']} tests → {test_score:.1f}/25"
            )

        # Score performance (20 points)
        if (
            "performance" in self.resultats
            and "status" in self.resultats["performance"]
        ):
            if self.resultats["performance"]["status"] == "accessible":
                perf_score = 20
                if "response_time" in self.resultats["performance"]:
                    if self.resultats["performance"]["response_time"] < 0.1:
                        perf_score = 20
                    elif self.resultats["performance"]["response_time"] < 0.5:
                        perf_score = 15
                    else:
                        perf_score = 10
            else:
                perf_score = 0
            score += perf_score
            game_logger.info(f"⚡ Performance: {perf_score}/20")

        # Score robustesse (20 points)
        if "robustesse" in self.resultats and "status" in self.resultats["robustesse"]:
            if self.resultats["robustesse"]["status"] == "succes":
                robust_score = 20
            elif self.resultats["robustesse"]["status"] == "echec":
                robust_score = 10
            else:
                robust_score = 0
            score += robust_score
            game_logger.info(f"🛡️  Robustesse: {robust_score}/20")

        # Score couverture (10 points)
        if (
            "couverture" in self.resultats
            and "pourcentage" in self.resultats["couverture"]
        ):
            cov_score = min(self.resultats["couverture"]["pourcentage"] / 10, 10)
            score += cov_score
            print(
                f"📊 Couverture: {self.resultats['couverture']['pourcentage']:.1f}% → {cov_score:.1f}/10",
            )

        self.resultats["score_global"] = score

        game_logger.info(f"\n🎯 SCORE GLOBAL: {score:.1f}/100")

        if score >= 90:
            game_logger.info(r"🌟 EXCELLENT - Projet de très haute qualité !")
            self.resultats["niveau"] = "excellent"
        elif score >= 80:
            game_logger.info(r"✅ TRÈS BON - Projet de bonne qualité")
            self.resultats["niveau"] = "tres_bon"
        elif score >= 70:
            game_logger.info(r"👍 BON - Projet correct avec quelques améliorations")
            self.resultats["niveau"] = "bon"
        elif score >= 60:
            game_logger.info(r"⚠️  MOYEN - Projet fonctionnel mais à améliorer")
            self.resultats["niveau"] = "moyen"
        else:
            game_logger.info(
                r"❌ FAIBLE - Projet nécessite des améliorations importantes"
            )
            self.resultats["niveau"] = "faible"

    def generer_recommandations(self):
        """Génère des recommandations d'amélioration"""
        print("\n💡 RECOMMANDATIONS D'AMÉLIORATION")
        print("=" * 50)

        recommendations = []

        # Recommandations basées sur la couverture
        if (
            "couverture" in self.resultats
            and "pourcentage" in self.resultats["couverture"]
        ):
            if self.resultats["couverture"]["pourcentage"] < 60:
                recommendations.append(
                    "📈 Augmenter la couverture de tests (objectif: 80%+)"
                )

        # Recommandations basées sur les tests
        if "tests" in self.resultats and "collectes" in self.resultats["tests"]:
            if self.resultats["tests"]["collectes"] < 100:
                recommendations.append(
                    "🧪 Ajouter plus de tests unitaires et d'intégration"
                )

        # Recommandations basées sur la robustesse
        if "robustesse" in self.resultats and "status" in self.resultats["robustesse"]:
            if self.resultats["robustesse"]["status"] != "succes":
                recommendations.append(
                    "🛡️  Corriger les tests de robustesse qui échouent"
                )

        # Recommandations basées sur les erreurs
        if self.resultats["erreurs"]:
            recommendations.append("🔧 Résoudre les erreurs détectées dans l'analyse")

        # Recommandations générales
        if self.resultats["score_global"] < 80:
            recommendations.append("🚀 Mettre en place un plan d'amélioration continue")

        if not recommendations:
            recommendations.append(
                "🎉 Aucune recommandation majeure - projet en excellent état !"
            )

        for i, rec in enumerate(recommendations, 1):
            game_logger.info(f"{i}. {rec}")

        self.resultats["recommandations"] = recommendations

    def sauvegarder_rapport(self):
        """Sauvegarde le rapport d'analyse"""
        rapport_file = self.projet_root / "RAPPORT_ANALYSE_FINALE.json"

        with open(rapport_file, "w", encoding="utf-8") as f:
            json.dump(self.resultats, f, indent=2, ensure_ascii=False)

        game_logger.info(f"\n💾 Rapport sauvegardé: {rapport_file}")

    def analyser_completement(self):
        """Lance l'analyse complète du projet"""
        game_logger.info(r"🔍 ANALYSE COMPLÈTE DU PROJET ARKALIA QUEST")
        print("=" * 60)
        print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        game_logger.info(f"📁 Projet: {self.projet_root}")
        print("=" * 60)

        # Analyses
        self.analyser_structure_projet()
        self.analyser_tests()
        self.analyser_performance()
        self.analyser_robustesse()
        self.analyser_couverture()

        # Score et recommandations
        self.calculer_score_global()
        self.generer_recommandations()

        # Sauvegarde
        self.sauvegarder_rapport()

        game_logger.info(r"\n🎯 ANALYSE TERMINÉE")
        print(f"📊 Score final: {self.resultats['score_global']:.1f}/100")
        game_logger.info(r"📁 Rapport: RAPPORT_ANALYSE_FINALE.json")


def main():
    """Fonction principale"""
    try:
        analyseur = AnalyseurProjet()
        analyseur.analyser_completement()

    except KeyboardInterrupt:
        print("\n⏹️  Analyse interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n💥 Erreur lors de l'analyse: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
