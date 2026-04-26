# Architecture — LUNA Hors Connexion

Mise a jour: **26 avril 2026**

## Vue d'ensemble

Le projet est une application Flask monolithique legere:
- rendu HTML cote serveur pour les pages principales,
- API JSON pour la progression narrative,
- moteur d'histoire base sur `data/story.json`,
- persistance SQLite par joueur via cookie `luna_player_id`.

## Structure reelle

```text
app.py
routes/
  pages.py        # routes HTML
  story.py        # API /api/story/*
core/
  story_engine.py # logique narrative
  story_save.py   # persistance sqlite
data/
  story.json      # chapitres, scenes, choix, fins
templates/
  index.html
  game.html
  profil.html
  leaderboard.html
static/
  css/game.css
  js/game.js
  js/service-worker.js
tests/
  test_story_engine.py
  test_api_routes.py
  api/test_app_routes_basic.py
```

## Routes HTML

- `GET /` -> page d'accueil narrative
- `GET /game` -> interface de jeu
- `GET /profil` -> progression et recap joueur
- `GET /leaderboard` -> classement local

## API Story

Base: `/api/story`

- `GET /state` -> etat courant joueur
- `POST /choice` -> appliquer un choix de scene
- `POST /advance` -> passer au chapitre suivant
- `POST /reset` -> reset de sauvegarde (memoire des fins conservee)
- `POST /name` -> enregistrer le prenom
- `GET /summary` -> resume de sauvegarde
- `GET /leaderboard` -> classement local
- `GET /journal` -> journal narratif personnalise

## Persistance

- DB: `data/luna_saves.db`
- Table: `story_saves(player_id, state_json, updated_at)`
- Le `state_json` contient notamment:
  - chapitre/scene courants
  - confiance LUNA
  - XP
  - flags narratifs
  - fins debloquees
  - fins precedentes (memoire inter-runs)

## Flux principal

1. Chargement initial: `GET /api/story/state`
2. Choix joueur: `POST /api/story/choice`
3. Fin de chapitre: `POST /api/story/advance`
4. Sauvegarde auto a chaque action serveur
5. Reprise via cookie + sauvegarde SQLite

## Qualite

- Tests: `pytest`
- Lint: `ruff`
- Le projet est volontairement sans framework frontend lourd.
