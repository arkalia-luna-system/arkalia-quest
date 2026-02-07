#!/usr/bin/env python3
"""
🔍 AUDIT COMPLET ARKALIA QUEST
=============================

Script d'audit professionnel pour analyser :
- Erreurs de code
- Problèmes de performance
- Bugs potentiels
- Sécurité
- Architecture
- Qualité du code
"""

import ast
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
REPORT_FILE = PROJECT_ROOT / "artifacts" / "audit_complet_jeu.json"
REPORT_MD = PROJECT_ROOT / "docs" / "audits" / "AUDIT_COMPLET_JEU.md"


class GameAuditor:
    """Auditeur complet pour Arkalia Quest"""

    def __init__(self):
        self.issues = {
            "errors": [],
            "warnings": [],
            "performance": [],
            "security": [],
            "architecture": [],
            "bugs": [],
            "code_quality": [],
        }
        self.stats = {
            "files_analyzed": 0,
            "lines_of_code": 0,
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "start_time": time.time(),
        }

    def analyze_file(self, file_path: Path) -> dict[str, Any]:
        """Analyse un fichier Python"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            file_issues = {
                "file": str(file_path),
                "errors": [],
                "warnings": [],
                "performance": [],
                "security": [],
                "bugs": [],
            }

            # Compter les lignes
            lines = content.split("\n")
            self.stats["lines_of_code"] += len(lines)

            # Analyser le contenu
            self._analyze_imports(tree, file_path, file_issues)
            self._analyze_functions(tree, file_path, file_issues)
            self._analyze_classes(tree, file_path, file_issues)
            self._analyze_code_patterns(content, file_path, file_issues)
            self._analyze_security(content, file_path, file_issues)
            self._analyze_performance(content, file_path, file_issues)

            return file_issues

        except Exception as e:
            return {
                "file": str(file_path),
                "error": f"Erreur analyse: {e}",
                "errors": [f"Impossible d'analyser le fichier: {e}"],
            }

    def _analyze_imports(self, tree: ast.AST, file_path: Path, issues: dict):
        """Analyse les imports"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.stats["imports"] += 1
                    # Vérifier les imports problématiques
                    if alias.name.startswith("tkinter"):
                        issues["warnings"].append(
                            f"Import tkinter détecté (ligne {node.lineno})"
                        )
                    if alias.name == "os" and "subprocess" in str(tree):
                        issues["security"].append(
                            f"Utilisation os + subprocess (ligne {node.lineno})"
                        )

    def _analyze_functions(self, tree: ast.AST, file_path: Path, issues: dict):
        """Analyse les fonctions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.stats["functions"] += 1

                # Vérifier les fonctions trop longues
                if hasattr(node, "end_lineno") and node.end_lineno:
                    length = node.end_lineno - node.lineno
                    if length > 50:
                        issues["performance"].append(
                            f"Fonction '{node.name}' trop longue ({length} lignes)"
                        )

                # Vérifier les paramètres trop nombreux
                if len(node.args.args) > 5:
                    issues["warnings"].append(
                        f"Fonction '{node.name}' avec trop de paramètres ({len(node.args.args)})"
                    )

    def _analyze_classes(self, tree: ast.AST, file_path: Path, issues: dict):
        """Analyse les classes"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.stats["classes"] += 1

                # Vérifier les classes trop longues
                if hasattr(node, "end_lineno") and node.end_lineno:
                    length = node.end_lineno - node.lineno
                    if length > 200:
                        issues["performance"].append(
                            f"Classe '{node.name}' trop longue ({length} lignes)"
                        )

    def _analyze_code_patterns(self, content: str, file_path: Path, issues: dict):
        """Analyse les patterns de code problématiques"""
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Vérifier les TODO/FIXME
            if re.search(r"\b(TODO|FIXME|HACK|XXX)\b", line, re.IGNORECASE):
                issues["warnings"].append(
                    f"TODO/FIXME détecté (ligne {i}): {line.strip()}"
                )

            # Vérifier les print de debug
            if re.search(r"\bprint\s*\(", line) and "debug" not in line.lower():
                issues["warnings"].append(f"Print de debug détecté (ligne {i})")

            # Vérifier les except pass
            if re.search(r"except.*:\s*pass", line):
                issues["bugs"].append(f"Except pass silencieux (ligne {i})")

            # Vérifier les variables non utilisées
            if re.search(r"^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*\s*#.*unused", line):
                issues["warnings"].append(f"Variable marquée unused (ligne {i})")

    def _analyze_security(self, content: str, file_path: Path, issues: dict):
        """Analyse les problèmes de sécurité"""
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Vérifier les mots de passe en dur
            if re.search(r'password\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
                issues["security"].append(
                    f"Mot de passe potentiellement en dur (ligne {i})"
                )

            # Vérifier les clés API en dur
            if re.search(r'api[_-]?key\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
                issues["security"].append(f"Clé API potentiellement en dur (ligne {i})")

            # Vérifier les SQL injection
            if re.search(r'execute\s*\(\s*["\'].*%s', line):
                issues["security"].append(f"Possible SQL injection (ligne {i})")

    def _analyze_performance(self, content: str, file_path: Path, issues: dict):
        """Analyse les problèmes de performance"""
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Vérifier les boucles imbriquées
            if re.search(r"for.*:\s*$", line) and i < len(lines) - 1:
                next_line = lines[i] if i < len(lines) else ""
                if re.search(r"for.*:\s*$", next_line):
                    issues["performance"].append(
                        f"Boucles imbriquées détectées (ligne {i})"
                    )

            # Vérifier les imports dans les boucles
            if re.search(r"for.*:\s*$", line):
                for j in range(i + 1, min(i + 10, len(lines))):
                    if re.search(r"^\s*import\s+", lines[j]):
                        issues["performance"].append(
                            f"Import dans une boucle (ligne {j})"
                        )
                        break

    def run_linting_analysis(self):
        """Exécute l'analyse de linting"""
        print("🔍 Exécution de l'analyse de linting...")

        try:
            # Ruff
            result = subprocess.run(
                ["python", "-m", "ruff", "check", ".", "--output-format=json"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
            )

            if result.returncode != 0:
                try:
                    ruff_issues = json.loads(result.stdout)
                    for issue in ruff_issues:
                        self.issues["code_quality"].append(
                            {
                                "type": "ruff",
                                "file": issue.get("filename", ""),
                                "line": issue.get("location", {}).get("row", 0),
                                "message": issue.get("message", ""),
                                "severity": issue.get("code", ""),
                            }
                        )
                except json.JSONDecodeError:
                    pass

            # MyPy
            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "mypy",
                    ".",
                    "--ignore-missing-imports",
                    "--show-error-codes",
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
            )

            if result.returncode != 0:
                for line in result.stdout.split("\n"):
                    if "error:" in line:
                        self.issues["code_quality"].append(
                            {
                                "type": "mypy",
                                "message": line.strip(),
                                "severity": "error",
                            }
                        )

        except Exception as e:
            self.issues["errors"].append(f"Erreur analyse linting: {e}")

    def run_security_analysis(self):
        """Exécute l'analyse de sécurité"""
        print("🔒 Exécution de l'analyse de sécurité...")

        try:
            result = subprocess.run(
                ["python", "-m", "bandit", "-r", ".", "-f", "json"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
            )

            if result.returncode != 0:
                try:
                    bandit_data = json.loads(result.stdout)
                    for issue in bandit_data.get("results", []):
                        if issue.get("issue_severity") == "HIGH":
                            self.issues["security"].append(
                                {
                                    "file": issue.get("filename", ""),
                                    "line": issue.get("line_number", 0),
                                    "message": issue.get("issue_text", ""),
                                    "severity": issue.get("issue_severity", ""),
                                }
                            )
                except json.JSONDecodeError:
                    pass

        except Exception as e:
            self.issues["errors"].append(f"Erreur analyse sécurité: {e}")

    def analyze_architecture(self):
        """Analyse l'architecture du projet"""
        print("🏗️ Analyse de l'architecture...")

        # Vérifier la structure des dossiers
        required_dirs = ["core", "engines", "utils", "tests", "templates", "static"]
        for dir_name in required_dirs:
            if not (PROJECT_ROOT / dir_name).exists():
                self.issues["architecture"].append(f"Dossier manquant: {dir_name}")

        # Vérifier les fichiers de configuration
        config_files = ["requirements.txt", "pyproject.toml", "README.md"]
        for config_file in config_files:
            if not (PROJECT_ROOT / config_file).exists():
                self.issues["architecture"].append(
                    f"Fichier de configuration manquant: {config_file}"
                )

        # Analyser les dépendances
        try:
            with open(PROJECT_ROOT / "requirements.txt") as f:
                requirements = f.read()

            # Vérifier les versions de dépendances
            if "flask" in requirements and "==" not in requirements:
                self.issues["architecture"].append("Version de Flask non spécifiée")

            if "requests" in requirements and "==" not in requirements:
                self.issues["architecture"].append("Version de requests non spécifiée")

        except Exception as e:
            self.issues["architecture"].append(f"Erreur analyse dépendances: {e}")

    def run_performance_tests(self):
        """Exécute des tests de performance"""
        print(r"⚡ Exécution des tests de performance...")

        try:
            # Test d'import de l'application
            start_time = time.time()
            result = subprocess.run(
                ["python", "-c", "from app import app; print('OK')"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
                timeout=30,
            )
            import_time = time.time() - start_time

            if import_time > 5:
                self.issues["performance"].append(
                    f"Import de l'app trop lent: {import_time:.2f}s"
                )

            if result.returncode != 0:
                self.issues["errors"].append(f"Erreur import app: {result.stderr}")

        except subprocess.TimeoutExpired:
            self.issues["performance"].append("Timeout lors de l'import de l'app")
        except Exception as e:
            self.issues["errors"].append(f"Erreur test performance: {e}")

    def analyze_all_files(self):
        """Analyse tous les fichiers Python"""
        print(r"📁 Analyse de tous les fichiers Python...")

        python_files = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Ignorer certains dossiers
            dirs[:] = [
                d
                for d in dirs
                if d not in ["venv", "__pycache__", ".git", "node_modules"]
            ]

            for file in files:
                if file.endswith(".py"):
                    python_files.append(Path(root) / file)

        for file_path in python_files:
            self.stats["files_analyzed"] += 1
            file_issues = self.analyze_file(file_path)

            # Ajouter les issues au rapport global
            for issue_type in ["errors", "warnings", "performance", "security", "bugs"]:
                if issue_type in file_issues:
                    self.issues[issue_type].extend(file_issues[issue_type])

    def generate_report(self):
        """Génère le rapport d'audit"""
        print("📊 Génération du rapport d'audit...")

        # Calculer les statistiques
        self.stats["duration"] = time.time() - self.stats["start_time"]

        # Compter les issues par type
        issue_counts = {}
        for issue_type, issues in self.issues.items():
            issue_counts[issue_type] = len(issues)

        # Générer le rapport JSON
        report = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "issue_counts": issue_counts,
            "issues": self.issues,
            "summary": {
                "total_issues": sum(issue_counts.values()),
                "critical_issues": issue_counts.get("errors", 0)
                + issue_counts.get("security", 0),
                "warnings": issue_counts.get("warnings", 0),
                "performance_issues": issue_counts.get("performance", 0),
            },
        }

        # Sauvegarder le rapport JSON
        os.makedirs(REPORT_FILE.parent, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Générer le rapport Markdown
        self._generate_markdown_report(report)

        return report

    def _generate_markdown_report(self, report: dict[str, Any]):
        """Génère le rapport Markdown"""
        os.makedirs(REPORT_MD.parent, exist_ok=True)

        with open(REPORT_MD, "w", encoding="utf-8") as f:
            f.write("# 🔍 AUDIT COMPLET ARKALIA QUEST\n\n")
            f.write(f"**Date:** {report['timestamp']}\n")
            f.write(f"**Durée:** {report['stats']['duration']:.2f}s\n\n")

            # Résumé
            f.write("## 📊 RÉSUMÉ EXÉCUTIF\n\n")
            f.write(f"- **Fichiers analysés:** {report['stats']['files_analyzed']}\n")
            f.write(f"- **Lignes de code:** {report['stats']['lines_of_code']:,}\n")
            f.write(f"- **Fonctions:** {report['stats']['functions']}\n")
            f.write(f"- **Classes:** {report['stats']['classes']}\n")
            f.write(f"- **Imports:** {report['stats']['imports']}\n\n")

            f.write("### 🚨 PROBLÈMES DÉTECTÉS\n\n")
            f.write(
                f"- **Erreurs critiques:** {report['summary']['critical_issues']}\n"
            )
            f.write(f"- **Avertissements:** {report['summary']['warnings']}\n")
            f.write(
                f"- **Problèmes de performance:** {report['summary']['performance_issues']}\n"
            )
            f.write(f"- **Total:** {report['summary']['total_issues']}\n\n")

            # Détails par catégorie
            for category, issues in report["issues"].items():
                if issues:
                    f.write(f"## {category.upper().replace('_', ' ')}\n\n")
                    for issue in issues[:10]:  # Limiter à 10 par catégorie
                        if isinstance(issue, dict):
                            f.write(
                                f"- **{issue.get('file', 'N/A')}:** {issue.get('message', str(issue))}\n"
                            )
                        else:
                            f.write(f"- {issue}\n")
                    if len(issues) > 10:
                        f.write(f"- ... et {len(issues) - 10} autres\n")
                    f.write("\n")

    def run_complete_audit(self):
        """Exécute l'audit complet"""
        print("🚀 DÉMARRAGE DE L'AUDIT COMPLET ARKALIA QUEST")
        print("=" * 60)

        # Analyser tous les fichiers
        self.analyze_all_files()

        # Exécuter les analyses spécialisées
        self.run_linting_analysis()
        self.run_security_analysis()
        self.analyze_architecture()
        self.run_performance_tests()

        # Générer le rapport
        report = self.generate_report()

        print("\n" + "=" * 60)
        print(r"✅ AUDIT TERMINÉ !")
        print(f"📊 {report['stats']['files_analyzed']} fichiers analysés")
        print(f"🚨 {report['summary']['total_issues']} problèmes détectés")
        print(f"⏱️ Durée: {report['stats']['duration']:.2f}s")
        print(f"📄 Rapport: {REPORT_FILE}")
        print(f"📄 Rapport MD: {REPORT_MD}")

        return report


def main():
    """Fonction principale"""
    auditor = GameAuditor()
    report = auditor.run_complete_audit()

    # Code de sortie basé sur les erreurs critiques
    if report["summary"]["critical_issues"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
