#!/usr/bin/env python3
"""
🎨 AUDIT VISUEL ET NETTOYAGE ARKALIA QUEST
==========================================

Script spécialisé pour détecter :
- Problèmes visuels (CSS, HTML, JS)
- Fichiers inutilisés
- Code dupliqué
- Assets orphelins
- Problèmes d'interface utilisateur
"""

import ast
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
REPORT_FILE = PROJECT_ROOT / "artifacts" / "audit_visuel_nettoyage.json"
REPORT_MD = PROJECT_ROOT / "docs" / "audits" / "AUDIT_VISUEL_NETTOYAGE.md"


class VisualAuditor:
    """Auditeur spécialisé pour les problèmes visuels et le nettoyage"""

    def __init__(self):
        self.issues = {
            "fichiers_inutilises": [],
            "code_duplique": [],
            "assets_orphelins": [],
            "problemes_css": [],
            "problemes_html": [],
            "problemes_js": [],
            "imports_manquants": [],
            "fichiers_vides": [],
            "fichiers_trop_gros": [],
            "dependances_inutilisees": [],
        }
        self.stats = {
            "fichiers_analyses": 0,
            "lignes_css": 0,
            "lignes_html": 0,
            "lignes_js": 0,
            "assets_trouves": 0,
            "start_time": 0,
        }

    def find_unused_files(self):
        """Trouve les fichiers inutilisés"""
        print("🔍 Recherche des fichiers inutilisés...")

        # Fichiers Python
        python_files = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [
                d
                for d in dirs
                if d
                not in ["venv", "__pycache__", ".git", "node_modules", "build", "dist"]
            ]
            for file in files:
                if file.endswith(".py"):
                    python_files.append(Path(root) / file)

        # Analyser les imports
        all_imports = set()
        for file_path in python_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                # Extraire les imports
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            all_imports.add(alias.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            all_imports.add(node.module.split(".")[0])
            except Exception:
                continue

        # Vérifier les fichiers non importés
        for file_path in python_files:
            module_name = file_path.stem
            if module_name not in ["__init__", "app", "arkalia_engine"]:
                if module_name not in all_imports:
                    # Vérifier si c'est un fichier de test
                    if "test" not in str(file_path) and "script" not in str(file_path):
                        self.issues["fichiers_inutilises"].append(
                            {
                                "fichier": str(file_path),
                                "raison": "Module non importé",
                                "taille": file_path.stat().st_size,
                            }
                        )

    def find_duplicate_code(self):
        """Trouve le code dupliqué"""
        print("🔍 Recherche du code dupliqué...")

        python_files = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [
                d
                for d in dirs
                if d
                not in ["venv", "__pycache__", ".git", "node_modules", "build", "dist"]
            ]
            for file in files:
                if file.endswith(".py"):
                    python_files.append(Path(root) / file)

        # Extraire les fonctions
        functions = {}
        for file_path in python_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        func_code = ast.get_source_segment(content, node)
                        if func_code:
                            if func_name in functions:
                                self.issues["code_duplique"].append(
                                    {
                                        "fonction": func_name,
                                        "fichier1": functions[func_name],
                                        "fichier2": str(file_path),
                                        "lignes": len(func_code.split("\n")),
                                    }
                                )
                            else:
                                functions[func_name] = str(file_path)
            except Exception:
                continue

    def find_orphaned_assets(self):
        """Trouve les assets orphelins"""
        print("🔍 Recherche des assets orphelins...")

        # Trouver tous les assets
        assets = []
        for root, _dirs, files in os.walk(PROJECT_ROOT / "static"):
            for file in files:
                if file.endswith(
                    (".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico")
                ):
                    assets.append(Path(root) / file)

        self.stats["assets_trouves"] = len(assets)

        # Trouver toutes les références dans les templates et le code
        references = set()

        # Analyser les templates HTML
        for root, _dirs, files in os.walk(PROJECT_ROOT / "templates"):
            for file in files:
                if file.endswith(".html"):
                    try:
                        with open(Path(root) / file, encoding="utf-8") as f:
                            content = f.read()

                        # Extraire les références aux assets
                        css_refs = re.findall(r'href=["\']([^"\']*\.css)["\']', content)
                        js_refs = re.findall(r'src=["\']([^"\']*\.js)["\']', content)
                        img_refs = re.findall(
                            r'src=["\']([^"\']*\.(?:png|jpg|jpeg|gif|svg|ico))["\']',
                            content,
                        )

                        references.update(css_refs)
                        references.update(js_refs)
                        references.update(img_refs)
                    except Exception:
                        continue

        # Analyser le code Python
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [
                d
                for d in dirs
                if d
                not in ["venv", "__pycache__", ".git", "node_modules", "build", "dist"]
            ]
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(Path(root) / file, encoding="utf-8") as f:
                            content = f.read()

                        # Extraire les références aux assets
                        asset_refs = re.findall(
                            r'["\']([^"\']*\.(?:css|js|png|jpg|jpeg|gif|svg|ico))["\']',
                            content,
                        )
                        references.update(asset_refs)
                    except Exception:
                        continue

        # Vérifier les assets orphelins
        for asset in assets:
            asset_name = asset.name
            asset_relative = str(asset.relative_to(PROJECT_ROOT))

            is_referenced = False
            for ref in references:
                if asset_name in ref or asset_relative in ref:
                    is_referenced = True
                    break

            if not is_referenced:
                self.issues["assets_orphelins"].append(
                    {
                        "fichier": str(asset),
                        "taille": asset.stat().st_size,
                        "type": asset.suffix,
                    }
                )

    def analyze_css_issues(self):
        """Analyse les problèmes CSS"""
        print("🔍 Analyse des problèmes CSS...")

        css_files = []
        for root, _dirs, files in os.walk(PROJECT_ROOT / "static"):
            for file in files:
                if file.endswith(".css"):
                    css_files.append(Path(root) / file)

        for css_file in css_files:
            try:
                with open(css_file, encoding="utf-8") as f:
                    content = f.read()

                lines = content.split("\n")
                self.stats["lignes_css"] += len(lines)

                # Vérifier les problèmes CSS
                for i, line in enumerate(lines, 1):
                    line = line.strip()

                    # CSS non utilisé
                    if re.match(r"^\.[a-zA-Z][a-zA-Z0-9_-]*\s*\{", line):
                        class_name = re.match(
                            r"^\.([a-zA-Z][a-zA-Z0-9_-]*)\s*\{", line
                        ).group(1)
                        if not self._is_css_class_used(class_name):
                            self.issues["problemes_css"].append(
                                {
                                    "fichier": str(css_file),
                                    "ligne": i,
                                    "probleme": f"Classe CSS non utilisée: .{class_name}",
                                    "severite": "warning",
                                }
                            )

                    # Propriétés CSS obsolètes
                    if re.search(r"\b(zoom|filter|behavior)\b", line):
                        self.issues["problemes_css"].append(
                            {
                                "fichier": str(css_file),
                                "ligne": i,
                                "probleme": "Propriété CSS obsolète détectée",
                                "severite": "warning",
                            }
                        )

                    # CSS non optimisé
                    if re.search(r"!important", line):
                        self.issues["problemes_css"].append(
                            {
                                "fichier": str(css_file),
                                "ligne": i,
                                "probleme": "Utilisation de !important (à éviter)",
                                "severite": "info",
                            }
                        )

            except Exception as e:
                self.issues["problemes_css"].append(
                    {
                        "fichier": str(css_file),
                        "probleme": f"Erreur lecture fichier: {e}",
                        "severite": "error",
                    }
                )

    def analyze_html_issues(self):
        """Analyse les problèmes HTML"""
        print("🔍 Analyse des problèmes HTML...")

        html_files = []
        for root, _dirs, files in os.walk(PROJECT_ROOT / "templates"):
            for file in files:
                if file.endswith(".html"):
                    html_files.append(Path(root) / file)

        for html_file in html_files:
            try:
                with open(html_file, encoding="utf-8") as f:
                    content = f.read()

                lines = content.split("\n")
                self.stats["lignes_html"] += len(lines)

                # Vérifier les problèmes HTML
                for i, line in enumerate(lines, 1):
                    line = line.strip()

                    # Balises HTML obsolètes
                    if re.search(
                        r"<(center|font|marquee|blink|applet|embed|object)\b",
                        line,
                        re.IGNORECASE,
                    ):
                        self.issues["problemes_html"].append(
                            {
                                "fichier": str(html_file),
                                "ligne": i,
                                "probleme": "Balise HTML obsolète détectée",
                                "severite": "warning",
                            }
                        )

                    # Attributs manquants
                    if re.search(r"<img[^>]*(?!alt=)", line) and "alt=" not in line:
                        self.issues["problemes_html"].append(
                            {
                                "fichier": str(html_file),
                                "ligne": i,
                                "probleme": "Image sans attribut alt",
                                "severite": "error",
                            }
                        )

                    # Liens sans texte
                    if re.search(r"<a[^>]*>\s*</a>", line):
                        self.issues["problemes_html"].append(
                            {
                                "fichier": str(html_file),
                                "ligne": i,
                                "probleme": "Lien sans texte",
                                "severite": "warning",
                            }
                        )

            except Exception as e:
                self.issues["problemes_html"].append(
                    {
                        "fichier": str(html_file),
                        "probleme": f"Erreur lecture fichier: {e}",
                        "severite": "error",
                    }
                )

    def analyze_js_issues(self):
        """Analyse les problèmes JavaScript"""
        print("🔍 Analyse des problèmes JavaScript...")

        js_files = []
        for root, _dirs, files in os.walk(PROJECT_ROOT / "static"):
            for file in files:
                if file.endswith(".js"):
                    js_files.append(Path(root) / file)

        for js_file in js_files:
            try:
                with open(js_file, encoding="utf-8") as f:
                    content = f.read()

                lines = content.split("\n")
                self.stats["lignes_js"] += len(lines)

                # Vérifier les problèmes JavaScript
                for i, line in enumerate(lines, 1):
                    line = line.strip()

                    # Variables non déclarées
                    if re.search(r"\bvar\b", line):
                        self.issues["problemes_js"].append(
                            {
                                "fichier": str(js_file),
                                "ligne": i,
                                "probleme": "Utilisation de 'var' (utiliser 'let' ou 'const')",
                                "severite": "warning",
                            }
                        )

                    # Fonctions non utilisées
                    if re.match(r"function\s+(\w+)", line):
                        func_name = re.match(r"function\s+(\w+)", line).group(1)
                        if not self._is_js_function_used(func_name, content):
                            self.issues["problemes_js"].append(
                                {
                                    "fichier": str(js_file),
                                    "ligne": i,
                                    "probleme": f"Fonction JavaScript non utilisée: {func_name}",
                                    "severite": "warning",
                                }
                            )

                    # Console.log en production
                    if re.search(r"console\.log", line):
                        self.issues["problemes_js"].append(
                            {
                                "fichier": str(js_file),
                                "ligne": i,
                                "probleme": "Console.log détecté (à supprimer en production)",
                                "severite": "info",
                            }
                        )

            except Exception as e:
                self.issues["problemes_js"].append(
                    {
                        "fichier": str(js_file),
                        "probleme": f"Erreur lecture fichier: {e}",
                        "severite": "error",
                    }
                )

    def find_empty_files(self):
        """Trouve les fichiers vides"""
        print("🔍 Recherche des fichiers vides...")

        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [
                d
                for d in dirs
                if d
                not in ["venv", "__pycache__", ".git", "node_modules", "build", "dist"]
            ]
            for file in files:
                file_path = Path(root) / file
                if file_path.stat().st_size == 0:
                    self.issues["fichiers_vides"].append(
                        {"fichier": str(file_path), "taille": 0}
                    )

    def find_large_files(self):
        """Trouve les fichiers trop gros"""
        print("🔍 Recherche des fichiers trop gros...")

        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [
                d
                for d in dirs
                if d
                not in ["venv", "__pycache__", ".git", "node_modules", "build", "dist"]
            ]
            for file in files:
                file_path = Path(root) / file
                size = file_path.stat().st_size

                # Fichiers > 1MB
                if size > 1024 * 1024:
                    self.issues["fichiers_trop_gros"].append(
                        {
                            "fichier": str(file_path),
                            "taille": size,
                            "taille_mb": round(size / (1024 * 1024), 2),
                        }
                    )

    def find_unused_dependencies(self):
        """Trouve les dépendances inutilisées"""
        print("🔍 Recherche des dépendances inutilisées...")

        try:
            # Lire requirements.txt
            with open(PROJECT_ROOT / "requirements.txt") as f:
                requirements = f.read()

            # Extraire les noms des packages
            packages = []
            for line in requirements.split("\n"):
                if line.strip() and not line.startswith("#"):
                    package_name = line.split(">=")[0].split("==")[0].strip()
                    packages.append(package_name)

            # Vérifier l'utilisation dans le code
            for package in packages:
                if not self._is_package_used(package):
                    self.issues["dependances_inutilisees"].append(
                        {"package": package, "raison": "Non utilisé dans le code"}
                    )

        except Exception as e:
            self.issues["dependances_inutilisees"].append(
                {"package": "unknown", "raison": f"Erreur analyse: {e}"}
            )

    def _is_css_class_used(self, class_name: str) -> bool:
        """Vérifie si une classe CSS est utilisée"""
        # Rechercher dans les templates HTML
        for root, _dirs, files in os.walk(PROJECT_ROOT / "templates"):
            for file in files:
                if file.endswith(".html"):
                    try:
                        with open(Path(root) / file, encoding="utf-8") as f:
                            content = f.read()
                        if (
                            f'class="{class_name}"' in content
                            or f"class='{class_name}'" in content
                        ):
                            return True
                    except Exception:
                        continue
        return False

    def _is_js_function_used(self, func_name: str, content: str) -> bool:
        """Vérifie si une fonction JavaScript est utilisée"""
        # Compter les occurrences (définition + utilisation)
        occurrences = content.count(func_name)
        return occurrences > 1

    def _is_package_used(self, package_name: str) -> bool:
        """Vérifie si un package Python est utilisé"""
        # Rechercher dans tous les fichiers Python
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [
                d
                for d in dirs
                if d
                not in ["venv", "__pycache__", ".git", "node_modules", "build", "dist"]
            ]
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(Path(root) / file, encoding="utf-8") as f:
                            content = f.read()
                        if (
                            f"import {package_name}" in content
                            or f"from {package_name}" in content
                        ):
                            return True
                    except Exception:
                        continue
        return False

    def generate_report(self):
        """Génère le rapport d'audit visuel"""
        print("📊 Génération du rapport d'audit visuel...")

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
                "fichiers_inutilises": issue_counts.get("fichiers_inutilises", 0),
                "assets_orphelins": issue_counts.get("assets_orphelins", 0),
                "problemes_visuels": issue_counts.get("problemes_css", 0)
                + issue_counts.get("problemes_html", 0)
                + issue_counts.get("problemes_js", 0),
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
            f.write("# 🎨 AUDIT VISUEL ET NETTOYAGE ARKALIA QUEST\n\n")
            f.write(f"**Date:** {report['timestamp']}\n")
            f.write(f"**Durée:** {report['stats']['duration']:.2f}s\n\n")

            # Résumé
            f.write("## 📊 RÉSUMÉ EXÉCUTIF\n\n")
            f.write(
                f"- **Fichiers analysés:** {report['stats']['fichiers_analyses']}\n"
            )
            f.write(f"- **Lignes CSS:** {report['stats']['lignes_css']:,}\n")
            f.write(f"- **Lignes HTML:** {report['stats']['lignes_html']:,}\n")
            f.write(f"- **Lignes JS:** {report['stats']['lignes_js']:,}\n")
            f.write(f"- **Assets trouvés:** {report['stats']['assets_trouves']}\n\n")

            f.write("### 🚨 PROBLÈMES DÉTECTÉS\n\n")
            f.write(
                f"- **Fichiers inutilisés:** {report['summary']['fichiers_inutilises']}\n"
            )
            f.write(
                f"- **Assets orphelins:** {report['summary']['assets_orphelins']}\n"
            )
            f.write(
                f"- **Problèmes visuels:** {report['summary']['problemes_visuels']}\n"
            )
            f.write(f"- **Total:** {report['summary']['total_issues']}\n\n")

            # Détails par catégorie
            for category, issues in report["issues"].items():
                if issues:
                    f.write(f"## {category.upper().replace('_', ' ')}\n\n")
                    for issue in issues[:10]:  # Limiter à 10 par catégorie
                        if isinstance(issue, dict):
                            f.write(
                                f"- **{issue.get('fichier', 'N/A')}:** {issue.get('probleme', str(issue))}\n"
                            )
                        else:
                            f.write(f"- {issue}\n")
                    if len(issues) > 10:
                        f.write(f"- ... et {len(issues) - 10} autres\n")
                    f.write("\n")

    def run_complete_audit(self):
        """Exécute l'audit visuel complet"""
        print("🚀 DÉMARRAGE DE L'AUDIT VISUEL ET NETTOYAGE")
        print("=" * 60)

        self.stats["start_time"] = time.time()

        # Exécuter toutes les analyses
        self.find_unused_files()
        self.find_duplicate_code()
        self.find_orphaned_assets()
        self.analyze_css_issues()
        self.analyze_html_issues()
        self.analyze_js_issues()
        self.find_empty_files()
        self.find_large_files()
        self.find_unused_dependencies()

        # Générer le rapport
        report = self.generate_report()

        print("\n" + "=" * 60)
        print("✅ AUDIT VISUEL TERMINÉ !")
        print(f"📊 {report['summary']['total_issues']} problèmes détectés")
        print(f"⏱️ Durée: {report['stats']['duration']:.2f}s")
        print(f"📄 Rapport: {REPORT_FILE}")
        print(f"📄 Rapport MD: {REPORT_MD}")

        return report


def main():
    """Fonction principale"""
    auditor = VisualAuditor()
    report = auditor.run_complete_audit()

    # Code de sortie basé sur les problèmes critiques
    if report["summary"]["total_issues"] > 0:
        print(f"\n⚠️  {report['summary']['total_issues']} problèmes détectés")
        return 1
    else:
        print("\n✅ Aucun problème détecté")
        return 0


if __name__ == "__main__":
    import sys
    import time

    sys.exit(main())
