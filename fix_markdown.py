#!/usr/bin/env python3
"""
Script pour corriger automatiquement tous les fichiers Markdown
Corrige les erreurs de linting Markdown courantes
"""

import os
import re
import glob


def fix_markdown_file(file_path):
    """Corrige un fichier Markdown"""
    print(f"🔧 Correction de {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # 1. Ajouter des lignes vides autour des titres
        content = re.sub(
            r"^(\n*)(#{1,6}\s+.+)$", r"\1\n\2\n", content, flags=re.MULTILINE
        )

        # 2. Ajouter des lignes vides autour des listes
        content = re.sub(
            r"^(\n*)([-*+]\s+.+)$", r"\1\n\2\n", content, flags=re.MULTILINE
        )

        # 3. Ajouter des lignes vides autour des blocs de code
        content = re.sub(r"^(\n*)(```.+)$", r"\1\n\2\n", content, flags=re.MULTILINE)
        content = re.sub(r"^(\n*)(```)$", r"\1\n\2\n", content, flags=re.MULTILINE)

        # 4. Supprimer les espaces en fin de ligne
        content = re.sub(r" +$", "", content, flags=re.MULTILINE)

        # 5. S'assurer qu'il y a une seule ligne vide à la fin
        content = content.rstrip() + "\n"

        # 6. Corriger les liens cassés (remplacer par des liens valides)
        content = re.sub(r"\[([^\]]+)\]\(#([^)]+)\)", r"[\1](#\2)", content)

        # 7. Supprimer le HTML inline problématique
        content = re.sub(r"<div[^>]*>", "", content)
        content = re.sub(r"</div>", "", content)

        # Écrire le fichier corrigé
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ {file_path} corrigé")
        else:
            print(f"ℹ️  {file_path} déjà correct")

    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")


def main():
    """Fonction principale"""
    print("🚀 Correction automatique des fichiers Markdown")

    # Trouver tous les fichiers .md
    md_files = []
    for pattern in ["**/*.md", "docs/**/*.md", "reports/**/*.md"]:
        md_files.extend(glob.glob(pattern, recursive=True))

    # Supprimer les doublons
    md_files = list(set(md_files))

    print(f"📁 {len(md_files)} fichiers Markdown trouvés")

    # Corriger chaque fichier
    for md_file in md_files:
        if os.path.exists(md_file):
            fix_markdown_file(md_file)

    print("🎉 Correction terminée !")


if __name__ == "__main__":
    main()
