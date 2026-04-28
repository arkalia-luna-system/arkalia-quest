# LUNA — Hors Connexion

Jeu narratif web cyberpunk pour ado: tu aides LUNA, une IA en fuite.

## Démarrage rapide

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

App locale: `http://localhost:5001`

## Commandes utiles

```bash
python -m pytest tests/ -q
ruff check .
black --check .
make build
```

## API story

Base: `/api/story`

- `GET /state`
- `POST /choice` (`scene_id`, `choice_id`)
- `POST /advance` (`scene_id`)
- `POST /reset`
- `POST /name` (`name`)
- `GET /summary`
- `GET /leaderboard`
- `GET /journal`
- `POST /telemetry`

## Variables importantes

- `SECRET_KEY` (obligatoire en production)
- `APP_ENV=production`
- `APP_MAX_CONTENT_LENGTH_BYTES` (défaut `1048576`)
- `STORY_RATE_LIMIT_WINDOW_SECONDS` (défaut `60`)
- `STORY_RATE_LIMIT_MAX_POSTS` (défaut `60`)

## Contribution (résumé)

- Branche depuis `develop`
- Fais une modif ciblée
- Vérifie: `pytest`, `ruff`, `black --check`
- Ouvre une PR claire

## Release (résumé)

- CI verte
- Smoke test gameplay (nouveau joueur, reprise, fin, partage)
- Déploiement puis vérification `/health`

## Assets de démo attendus

- `docs/assets/screenshot-accueil.png`
- `docs/assets/screenshot-game.png`
- `docs/assets/screenshot-profil-leaderboard.png`
- `docs/assets/demo-run.gif`

## Docs projet

Point d’entrée: `docs/index.md`

Docs clés:

- `docs/VISION.md`
- `docs/ARCHITECTURE.md`
- `docs/DEPLOYMENT_GUIDE.md`
