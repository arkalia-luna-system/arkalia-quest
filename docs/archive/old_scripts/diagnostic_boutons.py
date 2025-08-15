#!/usr/bin/env python3
"""
Script de diagnostic des boutons d'interface - Arkalia Quest
Identifie rapidement les problèmes JavaScript et les conflits
"""

import json
import re
from pathlib import Path


class ButtonDiagnostic:
    """Diagnostic des boutons d'interface"""

    def __init__(self):
        self.project_root = Path(".")
        self.issues = []
        self.warnings = []
        self.success = []

    def run_full_diagnostic(self):
        """Lance un diagnostic complet"""
        print("🔍 DIAGNOSTIC COMPLET DES BOUTONS D'INTERFACE")
        print("=" * 50)

        # 1. Analyser les templates HTML
        self.analyze_html_templates()

        # 2. Analyser les fichiers JavaScript
        self.analyze_javascript_files()

        # 3. Vérifier les conflits
        self.check_conflicts()

        # 4. Générer le rapport
        self.generate_report()

    def analyze_html_templates(self):
        """Analyse les templates HTML pour les boutons"""
        print("\n📄 ANALYSE DES TEMPLATES HTML")
        print("-" * 30)

        templates_dir = self.project_root / "templates"
        if not templates_dir.exists():
            self.issues.append("❌ Dossier templates/ non trouvé")
            return

        for html_file in templates_dir.glob("*.html"):
            print(f"\n🔍 Analyse de {html_file.name}:")
            self.analyze_html_file(html_file)

    def analyze_html_file(self, html_file: Path):
        """Analyse un fichier HTML spécifique"""
        try:
            with open(html_file, encoding='utf-8') as f:
                content = f.read()

            # Chercher les boutons
            buttons = re.findall(r'<button[^>]*>', content)
            onclick_buttons = re.findall(r'onclick="([^"]*)"', content)

            print(f"  📊 Boutons trouvés: {len(buttons)}")
            print(f"  🖱️ Boutons avec onclick: {len(onclick_buttons)}")

            # Analyser les onclick
            for i, onclick in enumerate(onclick_buttons):
                print(f"    {i+1}. onclick: {onclick}")

                # Vérifier les fonctions appelées
                if "playSound" in onclick:
                    self.success.append(f"✅ playSound() trouvé dans {html_file.name}")
                if "executeQuickCommand" in onclick:
                    self.success.append(f"✅ executeQuickCommand() trouvé dans {html_file.name}")
                if "executeCommand" in onclick:
                    self.success.append(f"✅ executeCommand() trouvé dans {html_file.name}")

                # Détecter les problèmes potentiels
                if "undefined" in onclick:
                    self.issues.append(f"❌ Fonction undefined dans {html_file.name}: {onclick}")
                if "error" in onclick.lower():
                    self.issues.append(f"⚠️ Possible erreur dans {html_file.name}: {onclick}")

        except Exception as e:
            self.issues.append(f"❌ Erreur lecture {html_file.name}: {e}")

    def analyze_javascript_files(self):
        """Analyse les fichiers JavaScript"""
        print("\n📜 ANALYSE DES FICHIERS JAVASCRIPT")
        print("-" * 35)

        js_dir = self.project_root / "static" / "js"
        if not js_dir.exists():
            self.issues.append("❌ Dossier static/js/ non trouvé")
            return

        for js_file in js_dir.glob("*.js"):
            print(f"\n🔍 Analyse de {js_file.name}:")
            self.analyze_js_file(js_file)

    def analyze_js_file(self, js_file: Path):
        """Analyse un fichier JavaScript spécifique"""
        try:
            with open(js_file, encoding='utf-8') as f:
                content = f.read()

            # Chercher les fonctions importantes
            functions = {
                'playSound': len(re.findall(r'function\s+playSound|playSound\s*=', content)),
                'executeQuickCommand': len(re.findall(r'function\s+executeQuickCommand|executeQuickCommand\s*=', content)),
                'executeCommand': len(re.findall(r'function\s+executeCommand|executeCommand\s*=', content)),
                'addEventListener': len(re.findall(r'addEventListener', content)),
                'DOMContentLoaded': len(re.findall(r'DOMContentLoaded', content))
            }

            print("  📊 Fonctions trouvées:")
            for func, count in functions.items():
                print(f"    {func}: {count} occurrence(s)")

                if count > 1 and func in ['playSound', 'executeQuickCommand', 'executeCommand']:
                    self.warnings.append(f"⚠️ Fonction {func} dupliquée dans {js_file.name} ({count}x)")

            # Chercher les erreurs potentielles
            if 'console.error' in content:
                self.warnings.append(f"⚠️ console.error trouvé dans {js_file.name}")
            if 'throw new Error' in content:
                self.warnings.append(f"⚠️ throw new Error trouvé dans {js_file.name}")

            # Vérifier la syntaxe basique
            if content.count('{') != content.count('}'):
                self.issues.append(f"❌ Parenthèses non équilibrées dans {js_file.name}")
            if content.count('(') != content.count(')'):
                self.issues.append(f"❌ Parenthèses non équilibrées dans {js_file.name}")

        except Exception as e:
            self.issues.append(f"❌ Erreur lecture {js_file.name}: {e}")

    def check_conflicts(self):
        """Vérifie les conflits potentiels"""
        print("\n⚔️ VÉRIFICATION DES CONFLITS")
        print("-" * 25)

        # Vérifier les doublons de fonctions
        js_dir = self.project_root / "static" / "js"
        if js_dir.exists():
            all_js_content = ""
            for js_file in js_dir.glob("*.js"):
                try:
                    with open(js_file, encoding='utf-8') as f:
                        all_js_content += f.read() + "\n"
                except:
                    continue

            # Chercher les fonctions dupliquées
            functions = ['playSound', 'executeQuickCommand', 'executeCommand']
            for func in functions:
                count = len(re.findall(r'function\s+' + func + r'\s*\(', all_js_content))
                if count > 1:
                    self.issues.append(f"❌ CONFLIT: Fonction {func} définie {count} fois")
                elif count == 1:
                    self.success.append(f"✅ Fonction {func} définie une seule fois")
                else:
                    self.warnings.append(f"⚠️ Fonction {func} non trouvée")

    def generate_report(self):
        """Génère le rapport final"""
        print("\n📋 RAPPORT DE DIAGNOSTIC")
        print("=" * 30)

        # Résumé
        print("\n📊 RÉSUMÉ:")
        print(f"  ✅ Succès: {len(self.success)}")
        print(f"  ⚠️ Avertissements: {len(self.warnings)}")
        print(f"  ❌ Problèmes: {len(self.issues)}")

        # Afficher les succès
        if self.success:
            print("\n✅ SUCCÈS:")
            for success in self.success:
                print(f"  {success}")

        # Afficher les avertissements
        if self.warnings:
            print("\n⚠️ AVERTISSEMENTS:")
            for warning in self.warnings:
                print(f"  {warning}")

        # Afficher les problèmes
        if self.issues:
            print("\n❌ PROBLÈMES CRITIQUES:")
            for issue in self.issues:
                print(f"  {issue}")

        # Recommandations
        print("\n🎯 RECOMMANDATIONS:")
        if self.issues:
            print("  🚨 CORRECTION IMMÉDIATE NÉCESSAIRE")
            print("  1. Résoudre les conflits de fonctions")
            print("  2. Corriger les erreurs de syntaxe")
            print("  3. Tester manuellement tous les boutons")
        elif self.warnings:
            print("  ⚠️ AMÉLIORATION RECOMMANDÉE")
            print("  1. Nettoyer les fonctions dupliquées")
            print("  2. Optimiser le code JavaScript")
            print("  3. Tester la performance")
        else:
            print("  ✅ CODE PROPRE - Tests manuels recommandés")
            print("  1. Tester tous les boutons manuellement")
            print("  2. Vérifier la console pour les erreurs")
            print("  3. Tester sur différents navigateurs")

        # Sauvegarder le rapport
        self.save_report()

    def save_report(self):
        """Sauvegarde le rapport dans un fichier"""
        report = {
            "timestamp": "2025-07-09",
            "diagnostic": "Boutons d'interface",
            "summary": {
                "success": len(self.success),
                "warnings": len(self.warnings),
                "issues": len(self.issues)
            },
            "success": self.success,
            "warnings": self.warnings,
            "issues": self.issues
        }

        try:
            with open("diagnostic_boutons_report.json", "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print("\n💾 Rapport sauvegardé: diagnostic_boutons_report.json")
        except Exception as e:
            print(f"\n❌ Erreur sauvegarde rapport: {e}")

def main():
    """Fonction principale"""
    diagnostic = ButtonDiagnostic()
    diagnostic.run_full_diagnostic()

if __name__ == "__main__":
    main()
