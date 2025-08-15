#!/usr/bin/env python3
"""
Script de vérification complète d'Arkalia Quest
Détecte et corrige automatiquement les erreurs courantes
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from core.database import DatabaseManager


class ArkaliaChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.fixes = []
        self.project_root = Path(".")

    def log_error(self, message: str, file: str = "", line: int = 0):
        """Enregistre une erreur"""
        error = f"❌ ERREUR: {message}"
        if file:
            error += f" (fichier: {file}"
            if line:
                error += f", ligne: {line}"
            error += ")"
        self.errors.append(error)
        print(error)

    def log_warning(self, message: str, file: str = ""):
        """Enregistre un avertissement"""
        warning = f"⚠️ ATTENTION: {message}"
        if file:
            warning += f" (fichier: {file})"
        self.warnings.append(warning)
        print(warning)

    def log_fix(self, message: str):
        """Enregistre une correction"""
        fix = f"🔧 CORRECTION: {message}"
        self.fixes.append(fix)
        print(fix)

    def check_python_syntax(self):
        """Vérifie la syntaxe Python de tous les fichiers"""
        print("\n🔍 Vérification de la syntaxe Python...")

        python_files = list(self.project_root.rglob("*.py"))
        python_files = [
            f for f in python_files if ".venv" not in str(f) and ".git" not in str(f)
        ]

        for py_file in python_files:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    self.log_error(f"Erreur de syntaxe dans {py_file}", str(py_file))
                else:
                    print(f"✅ {py_file}")
            except Exception as e:
                self.log_error(f"Impossible de vérifier {py_file}: {e}", str(py_file))

    def check_json_files(self):
        """Vérifie la validité des fichiers JSON"""
        print("\n🔍 Vérification des fichiers JSON...")

        json_files = list(self.project_root.rglob("*.json"))
        json_files = [
            f for f in json_files if ".venv" not in str(f) and ".git" not in str(f)
        ]

        for json_file in json_files:
            try:
                with open(json_file, encoding="utf-8") as f:
                    json.load(f)
                print(f"✅ {json_file}")
            except json.JSONDecodeError as e:
                self.log_error(f"JSON invalide dans {json_file}: {e}", str(json_file))
            except Exception as e:
                self.log_error(f"Impossible de lire {json_file}: {e}", str(json_file))

    def check_imports(self):
        """Vérifie les imports Python"""
        print("\n🔍 Vérification des imports...")

        try:
            # Test des imports principaux
            imports_to_test = [
                ("app", "app.py"),
                ("arkalia_engine", "arkalia_engine.py"),
                ("core.command_handler", "core/command_handler.py"),
                ("core.database", "core/database.py"),
                ("core.websocket_manager", "core/websocket_manager.py"),
                ("engines.luna_ai", "engines/luna_ai.py"),
                ("engines.effects_engine", "engines/effects_engine.py"),
                ("mission_utils.meme_engine", "mission_utils/meme_engine.py"),
                ("utils.logger", "utils/logger.py"),
            ]

            for module_name, file_path in imports_to_test:
                try:
                    __import__(module_name)
                    print(f"✅ Import {module_name}")
                except ImportError as e:
                    self.log_error(f"Import échoué pour {module_name}: {e}", file_path)
                except Exception as e:
                    self.log_error(
                        f"Erreur lors de l'import de {module_name}: {e}", file_path
                    )

        except Exception as e:
            self.log_error(f"Erreur lors de la vérification des imports: {e}")

    def check_file_permissions(self):
        """Vérifie les permissions des fichiers"""
        print("\n🔍 Vérification des permissions...")

        # Scripts qui doivent être exécutables
        executable_files = ["run.sh", "start_gunicorn.sh", "activate-quest.sh"]

        for script in executable_files:
            script_path = self.project_root / script
            if script_path.exists():
                if not os.access(script_path, os.X_OK):
                    self.log_warning(
                        f"Script {script} n'est pas exécutable", str(script_path)
                    )
                    # Corriger automatiquement
                    try:
                        os.chmod(script_path, 0o755)
                        self.log_fix(f"Permissions corrigées pour {script}")
                    except Exception as e:
                        self.log_error(
                            f"Impossible de corriger les permissions de {script}: {e}"
                        )
                else:
                    print(f"✅ {script} (exécutable)")

    def check_required_files(self):
        """Vérifie la présence des fichiers requis"""
        print("\n🔍 Vérification des fichiers requis...")

        required_files = [
            "app.py",
            "arkalia_engine.py",
            "requirements.txt",
            "pyproject.toml",
            "render.yaml",
            "Procfile",
            "runtime.txt",
            "data/profil_joueur.json",
            "data/badges.json",
            "data/avatars.json",
            "templates/terminal.html",
            "static/style.css",
            "static/js/terminal.js",
        ]

        for file_path in required_files:
            if (self.project_root / file_path).exists():
                print(f"✅ {file_path}")
            else:
                self.log_error(f"Fichier requis manquant: {file_path}")

    def check_data_integrity(self):
        """Vérifie l'intégrité des données"""
        print("\n🔍 Vérification de l'intégrité des données...")

        # Vérifier le profil joueur via SQLite
        try:
            db_manager = DatabaseManager()
            profil = db_manager.load_profile("main_user")

            if profil:
                required_fields = ["username", "score", "level", "badges"]
                for field in required_fields:
                    if field not in profil:
                        self.log_warning(f"Champ manquant dans profil SQLite: {field}")
                        # Corriger automatiquement
                        if field == "badges":
                            profil[field] = []
                        elif field == "level":
                            profil[field] = 1
                        elif field == "score":
                            profil[field] = 0
                        elif field == "username":
                            profil[field] = "main_user"

                # Sauvegarder les corrections
                db_manager.save_profile("main_user", profil)
                self.log_fix("Profil joueur corrigé")
            else:
                self.log_warning("Profil principal non trouvé en base")

        except Exception as e:
            self.log_error(f"Erreur lors de la vérification du profil: {e}")

    def check_configuration_files(self):
        """Vérifie les fichiers de configuration"""
        print("\n🔍 Vérification des fichiers de configuration...")

        # Vérifier requirements.txt
        try:
            with open("requirements.txt") as f:
                requirements = f.read()

            required_packages = ["Flask", "gunicorn", "Werkzeug"]
            for package in required_packages:
                if package not in requirements:
                    self.log_warning(
                        f"Package requis manquant dans requirements.txt: {package}"
                    )

            print("✅ requirements.txt")
        except Exception as e:
            self.log_error(f"Erreur lors de la vérification de requirements.txt: {e}")

        # Vérifier pyproject.toml
        try:
            with open("pyproject.toml") as f:
                pyproject = f.read()

            if "arkalia-quest" not in pyproject:
                self.log_warning("Nom du projet manquant dans pyproject.toml")

            print("✅ pyproject.toml")
        except Exception as e:
            self.log_error(f"Erreur lors de la vérification de pyproject.toml: {e}")

    def check_web_files(self):
        """Vérifie les fichiers web"""
        print("\n🔍 Vérification des fichiers web...")

        # Vérifier les templates HTML
        html_files = list(self.project_root.rglob("*.html"))
        for html_file in html_files:
            if ".venv" not in str(html_file) and ".git" not in str(html_file):
                try:
                    with open(html_file, encoding="utf-8") as f:
                        content = f.read()

                    # Vérifications basiques
                    if "<!DOCTYPE html>" not in content and "<html" in content:
                        self.log_warning(
                            f"DOCTYPE manquant dans {html_file}", str(html_file)
                        )

                    if "charset" not in content:
                        self.log_warning(
                            f"Charset manquant dans {html_file}", str(html_file)
                        )

                    print(f"✅ {html_file}")
                except Exception as e:
                    self.log_error(
                        f"Erreur lors de la vérification de {html_file}: {e}",
                        str(html_file),
                    )

        # Vérifier les fichiers CSS
        css_files = list(self.project_root.rglob("*.css"))
        for css_file in css_files:
            if ".venv" not in str(css_file) and ".git" not in str(css_file):
                try:
                    with open(css_file, encoding="utf-8") as f:
                        content = f.read()

                    # Vérifications basiques CSS
                    if "{" in content and "}" in content:
                        print(f"✅ {css_file}")
                    else:
                        self.log_warning(
                            f"CSS potentiellement vide ou invalide: {css_file}",
                            str(css_file),
                        )
                except Exception as e:
                    self.log_error(
                        f"Erreur lors de la vérification de {css_file}: {e}",
                        str(css_file),
                    )

    def run_all_checks(self):
        """Exécute toutes les vérifications"""
        print("🚀 DÉMARRAGE DE LA VÉRIFICATION COMPLÈTE D'ARKALIA QUEST")
        print("=" * 60)

        self.check_required_files()
        self.check_python_syntax()
        self.check_json_files()
        self.check_imports()
        self.check_file_permissions()
        self.check_data_integrity()
        self.check_configuration_files()
        self.check_web_files()

        # Résumé
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DE LA VÉRIFICATION")
        print("=" * 60)
        print(f"❌ Erreurs trouvées: {len(self.errors)}")
        print(f"⚠️ Avertissements: {len(self.warnings)}")
        print(f"🔧 Corrections appliquées: {len(self.fixes)}")

        if self.errors:
            print("\n❌ ERREURS CRITIQUES:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print("\n⚠️ AVERTISSEMENTS:")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.fixes:
            print("\n🔧 CORRECTIONS APPLIQUÉES:")
            for fix in self.fixes:
                print(f"  {fix}")

        if not self.errors:
            print(
                "\n🎉 Aucune erreur critique trouvée ! Le projet est prêt pour le déploiement."
            )
        else:
            print(
                "\n⚠️ Des erreurs critiques ont été trouvées. Corrigez-les avant le déploiement."
            )

        return len(self.errors) == 0


if __name__ == "__main__":
    checker = ArkaliaChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
