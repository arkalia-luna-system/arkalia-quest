# Guide de Contribution — LUNA Hors Connexion

Mise a jour: **26 avril 2026**

Merci de contribuer.

## Setup rapide

```bash
git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Workflow

1. Creer une branche depuis `develop`.
2. Faire une modif ciblee (code + tests + docs si impact fonctionnel).
3. Verifier localement:
   - `python -m pytest -q`
   - `ruff check .`
4. Commit clair (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).
5. Ouvrir PR vers `develop`.

## Standards minimaux

- Respect du style Python (ruff/black).
- Pas de secret dans le repo.
- Toute modif API doit mettre a jour `README.md` et `docs/ARCHITECTURE.md`.
- Toute modif narrative doit rester adaptee a la cible adolescente.

## Quand modifier la documentation

Mettre a jour au minimum:
- `README.md` pour impact produit/global,
- `docs/ARCHITECTURE.md` pour impact technique,
- `docs/CHANGELOG.md` pour impact release.
