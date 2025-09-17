#!/usr/bin/env python3
"""
Script de correction manuelle des erreurs Markdown les plus critiques
"""

import glob
import re


def fix_markdown_file(file_path):
    """Corrige les erreurs Markdown les plus importantes dans un fichier"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # 1. Corriger les lignes multiples vides (MD012)
        content = re.sub(r"\n{3,}", "\n\n", content)

        # 2. Ajouter des lignes vides autour des titres (MD022)
        content = re.sub(r"(\n|^)(#{1,6}\s+.+)(\n|$)", r"\1\n\2\n\3", content)

        # 3. Ajouter des lignes vides autour des listes (MD032)
        content = re.sub(r"(\n|^)([-*+]\s+.+)(\n|$)", r"\1\n\2\n\3", content)

        # 4. Ajouter des lignes vides autour des blocs de code (MD031)
        content = re.sub(r"(\n|^)(```.+)(\n|$)", r"\1\n\2\n\3", content)
        content = re.sub(r"(\n|^)(```)(\n|$)", r"\1\n\2\n\3", content)

        # 5. Supprimer les espaces en fin de ligne (MD009)
        content = re.sub(r" +$", "", content, flags=re.MULTILINE)

        # 6. S'assurer qu'il y a une seule nouvelle ligne à la fin (MD047)
        content = content.rstrip() + "\n"

        # 7. Corriger les liens cassés (MD051) - liens vers des ancres
        content = re.sub(r"\[([^\]]+)\]\(#([^)]+)\)", r"[\1](#\2)", content)

        # 8. Supprimer le HTML inline problématique (MD033)
        content = re.sub(r"<div[^>]*>", "", content)
        content = re.sub(r"</div>", "", content)

        # 9. Corriger les titres qui utilisent l'emphase au lieu de # (MD036)
        content = re.sub(r"^(\*\*[^*]+\*\*)$", r"# \1", content, flags=re.MULTILINE)
        content = re.sub(r"^(\*[^*]+\*)$", r"## \1", content, flags=re.MULTILINE)

        # 10. Ajouter un titre H1 au début si manquant (MD041)
        if not content.strip().startswith("#"):
            lines = content.split("\n")
            if lines and lines[0].strip():
                lines.insert(0, "# Document")
                content = "\n".join(lines)

        # 11. Ajouter le langage aux blocs de code (MD040)
        content = re.sub(r"^```$", "```text", content, flags=re.MULTILINE)

        # Écrire le fichier seulement s'il y a eu des changements
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Corrigé: {file_path}")
            return True
        print(f"⏭️  Aucun changement: {file_path}")
        return False

    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")
        return False


def main():
    """Fonction principale"""
    print("🔧 CORRECTION MANUELLE DES ERREURS MARKDOWN")
    print("=" * 50)

    # Trouver tous les fichiers Markdown
    md_files = []
    for pattern in ["**/*.md", "docs/**/*.md", "reports/**/*.md"]:
        md_files.extend(glob.glob(pattern, recursive=True))

    # Supprimer les doublons
    md_files = list(set(md_files))

    print(f"📁 {len(md_files)} fichiers Markdown trouvés")

    corrected_count = 0
    total_count = len(md_files)

    for md_file in md_files:
        if fix_markdown_file(md_file):
            corrected_count += 1

    print("\n" + "=" * 50)
    print("📊 RÉSULTATS:")
    print(f"✅ Fichiers corrigés: {corrected_count}/{total_count}")
    print(f"⏭️  Fichiers inchangés: {total_count - corrected_count}/{total_count}")

    if corrected_count > 0:
        print(f"\n🎉 {corrected_count} fichiers ont été corrigés avec succès !")
    else:
        print("\n✨ Tous les fichiers étaient déjà corrects !")


if __name__ == "__main__":
    main()
