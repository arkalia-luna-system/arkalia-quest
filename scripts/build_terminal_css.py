#!/usr/bin/env python3
"""
Construit terminal-bundle.css en concaténant les feuilles CSS du terminal.
Réduit le nombre de requêtes HTTP (audit visuel/perfs).
Lancer : python scripts/build_terminal_css.py
"""
import os

# Répertoire racine du projet (parent de scripts/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_CSS = os.path.join(ROOT, "static", "css")
BUNDLE_PATH = os.path.join(STATIC_CSS, "terminal-bundle.css")

# Ordre des feuilles (aligné sur templates/terminal.html)
TERMINAL_CSS_FILES = [
    "arkalia-luna-vision.css",
    "accessibility.css",
    "arkalia-responsive.css",
    "interface-improvements.css",
    "empty-states.css",
    "reward-animations.css",
    "loading-animations.css",
    "progression-animations.css",
    "adaptive-guidance.css",
    "progression-feedback.css",
    "competitive-system.css",
    "creative-system.css",
    "casual-system.css",
    "contextual-feedback.css",
    "game-interface.css",
    "mission-interface.css",
]


def main() -> None:
    parts = [
        "/* terminal-bundle.css - Généré par scripts/build_terminal_css.py */",
        "/* Ne pas éditer à la main. Relancer le script après modification des CSS sources. */",
        "",
    ]
    for name in TERMINAL_CSS_FILES:
        path = os.path.join(STATIC_CSS, name)
        if not os.path.isfile(path):
            parts.append(f"/* Fichier manquant: {name} */")
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        parts.append(f"/* ========== {name} ========== */")
        parts.append(content)
        parts.append("")

    with open(BUNDLE_PATH, "w", encoding="utf-8") as out:
        out.write("\n".join(parts))
    print(f"✅ {BUNDLE_PATH}")


if __name__ == "__main__":
    main()
