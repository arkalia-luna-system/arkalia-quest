#!/usr/bin/env python3
"""
Script pour identifier les fichiers CSS/JS inutiles dans Arkalia Quest
"""

import os
import re
from pathlib import Path


def find_css_js_references():
    """Trouve toutes les références CSS/JS dans les templates"""
    references = set()
    templates_dir = Path("templates")

    for template_file in templates_dir.glob("*.html"):
        try:
            with open(template_file, encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(template_file, encoding="latin-1") as f:
                    content = f.read()
            except Exception as e:
                print(f"⚠️  Impossible de lire {template_file}: {e}")
                continue

        # Chercher les références CSS
        css_matches = re.findall(r'css/([^"\']+\.css)', content)
        for match in css_matches:
            references.add(f"static/css/{match}")

        # Chercher les références JS
        js_matches = re.findall(r'js/([^"\']+\.js)', content)
        for match in js_matches:
            references.add(f"static/js/{match}")

    return references


def find_existing_files():
    """Trouve tous les fichiers CSS/JS existants"""
    existing_files = set()

    # Fichiers CSS
    css_dir = Path("static/css")
    if css_dir.exists():
        for css_file in css_dir.glob("*.css"):
            existing_files.add(str(css_file))

    # Fichiers JS
    js_dir = Path("static/js")
    if js_dir.exists():
        for js_file in js_dir.glob("*.js"):
            existing_files.add(str(js_file))

    return existing_files


def main():
    print("🔍 Analyse des fichiers CSS/JS inutiles...")

    # Trouver les références et fichiers existants
    referenced_files = find_css_js_references()
    existing_files = find_existing_files()

    # Fichiers consolidés (à ne pas supprimer)
    consolidated_files = {
        "static/css/arkalia-core.css",
        "static/css/arkalia-themes.css",
        "static/css/arkalia-components.css",
        "static/css/arkalia-responsive.css",
    }

    # Fichiers critiques (à ne pas supprimer)
    critical_files = {
        "static/css/accessibility.css",
        "static/css/mini-games.css",
        "static/css/popup-manager.css",
        "static/js/universal-notifications.js",
        "static/js/universal-empty-states.js",
        "static/js/universal-feedback.js",
        "static/js/tutorial.js",
        "static/js/motivational-empty-states.js",
    }

    # Fichiers potentiellement inutiles
    potentially_unused = existing_files - referenced_files - consolidated_files - critical_files

    print("\n📊 STATISTIQUES:")
    print(f"   Fichiers CSS/JS existants: {len(existing_files)}")
    print(f"   Fichiers référencés: {len(referenced_files)}")
    print(f"   Fichiers consolidés: {len(consolidated_files)}")
    print(f"   Fichiers critiques: {len(critical_files)}")
    print(f"   Fichiers potentiellement inutiles: {len(potentially_unused)}")

    print("\n🗑️  FICHIERS POTENTIELLEMENT INUTILES:")
    for file in sorted(potentially_unused):
        print(f"   ❌ {file}")

    print("\n✅ FICHIERS CONSOLIDÉS (à conserver):")
    for file in sorted(consolidated_files):
        if file in existing_files:
            print(f"   ✅ {file}")

    print("\n🔒 FICHIERS CRITIQUES (à conserver):")
    for file in sorted(critical_files):
        if file in existing_files:
            print(f"   🔒 {file}")

    # Vérifier les fichiers manquants
    missing_files = referenced_files - existing_files
    if missing_files:
        print("\n⚠️  FICHIERS RÉFÉRENCÉS MAIS MANQUANTS:")
        for file in sorted(missing_files):
            print(f"   ⚠️  {file}")

    return potentially_unused


if __name__ == "__main__":
    unused_files = main()
