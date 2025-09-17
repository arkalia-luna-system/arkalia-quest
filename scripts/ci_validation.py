#!/usr/bin/env python3
"""
Script de validation CI pour Arkalia Quest
Vérifie tous les critères de qualité avant le déploiement
"""

import json
import os
import subprocess
import sys


class CIValidator:
    """Validateur CI pour Arkalia Quest"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success = True

    def run_command(self, command, description):
        """Exécute une commande et gère les erreurs"""
        print(f"🔍 {description}...")
        try:
            # Utiliser shlex pour séparer les arguments de manière sécurisée
            import shlex

            if isinstance(command, str):
                command = shlex.split(command)
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"✅ {description} - SUCCÈS")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} - ÉCHEC")
            print(f"   Erreur: {e.stderr}")
            self.errors.append(f"{description}: {e.stderr}")
            self.success = False
            return None

    def validate_ruff(self):
        """Valide le linting avec Ruff"""
        return self.run_command(
            "ruff check . --output-format=concise",
            "Vérification Ruff (Linting)",
        )

    def validate_black(self):
        """Valide le formatage avec Black"""
        return self.run_command(
            "black --check . --diff", "Vérification Black (Formatage)"
        )

    def validate_tests(self):
        """Valide l'exécution des tests"""
        print(r"🔍 Exécution des tests avec couverture...")
        try:
            import shlex

            command = shlex.split(
                "python -m pytest tests/ --tb=short -v --cov=core --cov=engines --cov=utils --cov-report=term-missing --cov-fail-under=10"
            )
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,  # Ne pas échouer sur les erreurs de tests
            )

            if result.returncode == 0:
                print(r"✅ Tests - SUCCÈS")
                return result.stdout
            print(f"❌ Tests - ÉCHEC (code: {result.returncode})")
            if result.stderr:
                print(f"   Erreurs: {result.stderr[:200]}...")
            self.errors.append(f"Tests échoués (code: {result.returncode})")
            self.success = False
            return result.stdout  # Retourner la sortie même en cas d'échec
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution des tests: {e}")
            self.errors.append(f"Erreur d'exécution des tests: {e}")
            self.success = False
            return None

    def validate_coverage(self):
        """Valide la couverture de code"""
        print(r"🔍 Vérification de la couverture...")
        try:
            import shlex

            command = shlex.split(
                "python -m pytest tests/ --cov=core --cov=engines --cov=utils --cov-report=term"
            )
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,  # Ne pas échouer sur les erreurs de tests
            )

            if result.returncode == 0:
                print(r"✅ Couverture - SUCCÈS")
                output = result.stdout
            else:
                print(f"⚠️  Couverture - ÉCHEC (code: {result.returncode})")
                output = result.stdout or result.stderr

            if output:
                # Extraire le pourcentage de couverture
                lines = output.split("\n")
                for line in lines:
                    if "TOTAL" in line and "%" in line:
                        try:
                            coverage = float(line.split()[-1].replace("%", ""))
                            if coverage < 10.0:
                                self.errors.append(
                                    f"Couverture insuffisante: {coverage}% < 10%"
                                )
                                self.success = False
                            else:
                                print(f"✅ Couverture de code: {coverage}% (>= 10%)")
                            break
                        except (ValueError, IndexError):
                            pass

            return output

        except Exception as e:
            print(f"❌ Erreur lors de la vérification de la couverture: {e}")
            self.errors.append(f"Erreur de couverture: {e}")
            self.success = False
            return None

    def validate_dependencies(self):
        """Valide les dépendances"""
        # Vérification simplifiée des dépendances
        print(r"🔍 Vérification des dépendances...")
        try:
            # Test des imports pour vérifier la disponibilité
            import importlib.util

            # Vérifier que les modules sont disponibles
            core_spec = importlib.util.find_spec("core")
            engines_spec = importlib.util.find_spec("engines")
            utils_spec = importlib.util.find_spec("utils")

            if core_spec and engines_spec and utils_spec:
                print(r"✅ Dépendances principales - Disponibles")
                return True
            missing = []
            if not core_spec:
                missing.append("core")
            if not engines_spec:
                missing.append("engines")
            if not utils_spec:
                missing.append("utils")
            error_msg = f"Modules manquants: {', '.join(missing)}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            self.success = False
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des dépendances: {e}")
            self.errors.append(f"Erreur de vérification: {e}")
            self.success = False
            return False

    def validate_imports(self):
        """Valide les imports Python"""
        return self.run_command(
            "python -c 'import core, engines, utils; print(\"✅ Imports valides\")'",
            "Validation des imports",
        )

    def validate_config_files(self):
        """Valide les fichiers de configuration"""
        config_files = [
            "pyproject.toml",
            "requirements.txt",
            "config/load_test_config.json",
        ]

        print(r"🔍 Validation des fichiers de configuration...")
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    if config_file.endswith(".json"):
                        with open(config_file) as f:
                            json.load(f)
                    print(f"✅ {config_file} - Valide")
                except Exception as e:
                    print(f"❌ {config_file} - Invalide: {e}")
                    self.errors.append(f"Configuration invalide: {config_file}")
                    self.success = False
            else:
                print(f"⚠️  {config_file} - Manquant")
                self.warnings.append(f"Fichier manquant: {config_file}")

        return True

    def validate_structure(self):
        """Valide la structure du projet"""
        required_dirs = ["core", "engines", "utils", "tests", "templates", "static"]

        print(r"🔍 Validation de la structure du projet...")
        for directory in required_dirs:
            if os.path.isdir(directory):
                print(f"✅ {directory}/ - Présent")
            else:
                print(f"❌ {directory}/ - Manquant")
                self.errors.append(f"Répertoire manquant: {directory}")
                self.success = False

        return True

    def generate_report(self):
        """Génère un rapport de validation"""
        print("\n" + "=" * 60)
        print(r"📊 RAPPORT DE VALIDATION CI")
        print("=" * 60)

        if self.success:
            print(r"🎉 VALIDATION CI RÉUSSIE !")
            print(r"✅ Tous les critères de qualité sont respectés")
            print(r"🚀 Le projet est prêt pour le déploiement")
        else:
            print(r"❌ VALIDATION CI ÉCHOUÉE !")
            print(r"🔧 Corrections nécessaires avant le déploiement")

        if self.errors:
            print(f"\n❌ ERREURS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")

        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")

        print(f"\n📈 STATUT FINAL: {'SUCCÈS' if self.success else 'ÉCHEC'}")

        return self.success

    def run_full_validation(self):
        """Lance la validation complète"""
        print(r"🚀 DÉMARRAGE DE LA VALIDATION CI COMPLÈTE")
        print("=" * 60)

        # Validation de la structure
        self.validate_structure()

        # Validation des fichiers de configuration
        self.validate_config_files()

        # Validation des dépendances
        self.validate_dependencies()

        # Validation des imports
        self.validate_imports()

        # Validation du code
        self.validate_ruff()
        self.validate_black()

        # Validation des tests
        self.validate_tests()
        self.validate_coverage()

        # Rapport final
        return self.generate_report()


def main():
    """Fonction principale"""
    validator = CIValidator()

    try:
        success = validator.run_full_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Validation interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur lors de la validation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
