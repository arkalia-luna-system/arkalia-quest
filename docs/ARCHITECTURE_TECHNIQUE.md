# Architecture Technique — Arkalia Quest

Mise a jour: **27 avril 2026**

Ce document remplace l'ancienne version orientee "plateforme educative multi-modules".
Le code actuel est centre sur un **jeu narratif web**.

## Stack

- Backend: Python 3.9+ / Flask
- Stockage: SQLite
- Frontend: HTML + CSS + JS vanilla
- PWA: `manifest.json` + `service-worker.js`
- Tests: `pytest`
- Qualite: `ruff`, `black`

## Composants techniques

### Application Flask

- `app.py` initialise:
  - secret key,
  - compression HTTP (`Flask-Compress`),
  - blueprint API story,
  - routes HTML,
  - pages d'erreur.

### API narrative

`routes/story.py` expose les endpoints de progression:
- state, choice, advance, reset, name, summary, leaderboard, journal.

### Moteur narratif

`core/story_engine.py`:
- charge `data/story.json`,
- calcule les transitions de scene,
- applique confiance/XP/flags,
- gere progression de chapitre et debloquage des fins.

### Persistance

`core/story_save.py`:
- genere un `player_id`,
- stocke et charge l'etat JSON dans SQLite,
- construit resume et leaderboard local.

## Donnees

`data/story.json` contient:
- meta (titre, total chapitres),
- chapitres et scenes,
- choix avec `trust_delta`, `xp`, `flags`, `next_scene`,
- definitions des fins avec conditions.

## Contrat qualite actuel

- `python -m pytest -q` doit passer.
- `ruff check .` doit passer.
- Toute evolution doit mettre a jour:
  - `README.md`
  - `docs/ARCHITECTURE.md`
  - `docs/CHANGELOG.md`

## Points d'attention

- Le projet a encore des traces historiques dans certains fichiers de config.
- La source de verite fonctionnelle est le trio:
  - `routes/story.py`
  - `core/story_engine.py`
  - `data/story.json`
