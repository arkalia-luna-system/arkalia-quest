# Architecture — LUNA Hors Connexion

## Stack

- Monolithe Flask
- Templates HTML + JS/CSS vanilla
- SQLite pour sauvegarde + telemetry locale

## Fichiers clés

```text
app.py
routes/story.py
routes/pages.py
core/story_engine.py
core/story_save.py
data/story.json
static/js/game.js
templates/
tests/
```

## Flux runtime

1. `GET /game` sert l’UI.
2. UI appelle `/api/story/state`.
3. Choix joueur via `/api/story/choice` puis `/api/story/advance`.
4. État persistant en SQLite (`story_saves`).
5. Événements gameplay via `/api/story/telemetry`.

## API publique `/api/story`

- `GET /api/story/state`
- `POST /api/story/choice`
- `POST /api/story/advance`
- `POST /api/story/reset`
- `POST /api/story/name`
- `GET /api/story/summary`
- `GET /api/story/leaderboard`
- `GET /api/story/journal`
- `POST /api/story/telemetry`

## Persistance

- DB: `data/luna_saves.db`
- Table `story_saves`: état narratif JSON par `player_id`
- Table `story_telemetry`: événements anonymisés locaux
- Cookie joueur: `luna_player_id`
