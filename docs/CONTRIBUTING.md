# Contribution

Workflow court:

1. Branche depuis `develop`.
2. Fais une modif ciblée.
3. Vérifie:
   - `python -m pytest tests -q`
   - `ruff check .`
   - `black --check .`
4. Ouvre une PR claire.

Règles:

- Pas de secrets committés.
- Si API modifiée: mettre à jour `README.md` et `docs/ARCHITECTURE.md`.
- Si comportement joueur modifié: mettre à jour `docs/VISION.md` ou `docs/ROADMAP.md`.
