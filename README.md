# LUNA — Hors Connexion

Jeu narratif web cyberpunk: tu dialogues avec LUNA, une IA en fuite, et tes choix modifient la confiance, la progression et les fins.

Statut de ce README: **audité et mis à jour le 26 avril 2026**.

---

## Ce projet, en vrai

`arkalia-quest` est une application Flask avec:
- une interface narrative (accueil, jeu, profil, classement),
- un moteur d'histoire piloté par `data/story.json`,
- une sauvegarde persistante SQLite par joueur (cookie + `player_id`),
- une progression rejouable avec mémoire des fins déjà débloquées.

Public cible: ado, ton direct, rythme rapide, ambiance néon/hacker.

---

## Audit rapide (26/04/2026)

Points confirmés côté code:
- Backend principal en `Flask` (`app.py`) + blueprint API `routes/story.py`.
- Frontend en `HTML/CSS/JS` vanilla (`templates/` + `static/`).
- Sauvegarde SQLite locale (`core/story_save.py`).
- Moteur narratif central (`core/story_engine.py`).
- PWA partielle (manifest + service worker).

Écarts constatés dans la doc historique:
- Plusieurs docs parlent encore d'un périmètre "éducatif/gamification large" qui ne reflète plus la boucle centrale actuelle.
- Le nombre de chapitres est parfois présenté différemment selon les pages et docs.
- Certains endpoints mentionnés dans les docs ne correspondent pas exactement aux endpoints réellement exposés.

Ce README devient la base de référence opérationnelle.

---

## Fonctionnalités actuelles

- **Accueil dynamique**: détection de sauvegarde, reprise, reset, saisie prénom.
- **Narration par choix**: contexte, dialogues, choix, réactions de LUNA.
- **Confiance LUNA (0-100)**: impact direct sur le ton et les issues.
- **XP et style de jeu**: progression visible pendant la partie et en fin de run.
- **Fins multiples**: déblocage progressif + mémoire des runs précédents.
- **Profil joueur**: journal personnalisé, moments clés, timeline des chapitres.
- **Classement local**: top joueurs par XP (anonymisé).

---

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

---

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

---

## Commandes utiles

```bash
# Tests
python -m pytest tests/ -v

# Lint
ruff check .

# Format
black .
```

---

## Structure principale

- `app.py` -> point d'entrée Flask
- `routes/pages.py` -> routes HTML (`/`, `/game`, `/profil`, `/leaderboard`)
- `routes/story.py` -> API narrative
- `core/story_engine.py` -> logique narrative
- `core/story_save.py` -> persistance SQLite
- `data/story.json` -> chapitres, scènes, choix, fins
- `templates/` -> pages UI
- `static/css/game.css` et `static/js/game.js` -> UX gameplay

---

## Documentation complémentaire

- `docs/VISION.md` -> vision narrative
- `docs/ARCHITECTURE.md` -> architecture globale (à relire avec l'audit ci-dessus)
- `docs/ROADMAP.md` -> roadmap produit
- `docs/DEPLOYMENT_GUIDE.md` -> déploiement
- `docs/CONTRIBUTING.md` -> contribution

---

## Git flow recommandé

Branche de travail active: `develop`.

Après validation locale:
1. Committer sur `develop`
2. Pousser `develop`
3. Aligner `main` et `backup` sur l'état validé de `develop` (merge ou fast-forward selon politique repo)

---

LUNA te parle en premier. Le reste dépend de tes choix.
