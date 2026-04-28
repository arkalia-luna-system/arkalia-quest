# LUNA — Hors Connexion

Jeu narratif web cyberpunk: tu dialogues avec LUNA, une IA en fuite, et tes choix modifient la confiance, la progression et les fins.

## Aperçu

`arkalia-quest` est une application Flask avec:

- une interface narrative (accueil, jeu, profil, classement),
- un moteur d'histoire piloté par `data/story.json`,
- une sauvegarde persistante SQLite par joueur (cookie + `player_id`),
- une progression rejouable avec mémoire des fins déjà débloquées.

Public cible: ado, ton direct, rythme rapide, ambiance néon/hacker.

## Fonctionnalités actuelles

- **Accueil dynamique**: détection de sauvegarde, reprise, reset, saisie prénom.
- **Narration par choix**: contexte, dialogues, choix, réactions de LUNA.
- **Confiance LUNA (0-100)**: impact direct sur le ton et les issues.
- **XP et style de jeu**: progression visible pendant la partie et en fin de run.
- **Fins multiples**: déblocage progressif + mémoire des runs précédents.
- **Profil joueur**: journal personnalisé, moments clés, timeline des chapitres.
- **Classement local**: top joueurs par XP (anonymisé).

## API Story (source de vérité)

Base: `/api/story`

- `GET /state` -> état courant complet du joueur
- `POST /choice` -> applique un choix (`scene_id`, `choice_id`)
- `POST /advance` -> passe au chapitre suivant en fin de chapitre
- `POST /reset` -> reset de la sauvegarde (en conservant la mémoire des fins)
- `POST /name` -> enregistre le prénom joueur
- `GET /summary` -> résumé de sauvegarde pour l'accueil
- `GET /leaderboard` -> top local des joueurs
- `GET /journal` -> journal narratif personnalisé LUNA

## Démarrage local

```bash
git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python app.py
```

Accès local: `http://localhost:5001`

Alternative:

```bash
flask --app app run --host=0.0.0.0 --port=5001
```

## Commandes utiles

```bash
# Tests
python -m pytest tests/ -v

# Lint
ruff check .

# Format
black .
```

## Sécurité (ops)

- `SECRET_KEY` est obligatoire en production.
- Les endpoints `POST /api/story/*` exigent `Content-Type: application/json`.
- Un rate-limit léger est actif sur les `POST` story:
  - `STORY_RATE_LIMIT_WINDOW_SECONDS` (défaut: `60`)
  - `STORY_RATE_LIMIT_MAX_POSTS` (défaut: `60`)
- En cas de dépassement, l'API renvoie `429` avec l'header `Retry-After`.

## Structure principale

- `app.py` -> point d'entrée Flask
- `routes/pages.py` -> routes HTML (`/`, `/game`, `/profil`, `/leaderboard`)
- `routes/story.py` -> API narrative
- `core/story_engine.py` -> logique narrative
- `core/story_save.py` -> persistance SQLite
- `data/story.json` -> chapitres, scènes, choix, fins
- `templates/` -> pages UI
- `static/css/game.css` et `static/js/game.js` -> UX gameplay

## Visibilité du projet

- **Démo live**: [https://arkalia-quest.onrender.com](https://arkalia-quest.onrender.com)
- **Healthcheck**: [https://arkalia-quest.onrender.com/health](https://arkalia-quest.onrender.com/health)

## Documentation complémentaire

- `docs/VISION.md` -> vision narrative
- `docs/ARCHITECTURE.md` -> architecture globale
- `docs/ROADMAP.md` -> roadmap produit
- `docs/DEPLOYMENT_GUIDE.md` -> déploiement
- `docs/CONTRIBUTING.md` -> contribution

## Git flow recommandé

Branche de travail active: `develop`.

Après validation locale:

1. Committer sur `develop`
2. Pousser `develop`
3. Aligner `main` sur l'état validé de `develop` selon la politique du repo

LUNA te parle en premier. Le reste dépend de tes choix.
