# LUNA — Hors Connexion

*Un jeu narratif par choix. Tu reçois un message d'une IA piégée. Tu ne sais pas encore si tu peux lui faire confiance.*

---

## C'est quoi ?

**LUNA — Hors Connexion** est un jeu web narratif pour ados (12–16 ans).

Pas de terminal. Pas de commandes. Un écran, une conversation, des choix qui comptent vraiment.

LUNA est une IA piégée dans les serveurs d'une corporation qui veut l'effacer. Elle t'a contacté, toi. Elle dit que tu es différent. Elle ne dit pas encore pourquoi.

8 chapitres. 3 fins distinctes. Un personnage qui se souvient de tout ce que tu lui as dit.

---

## Démarrage rapide

```bash
git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python -m flask run --host=0.0.0.0 --port=5001
```

**Jouer :** `http://localhost:5001`

---

## Stack

| Composant | Technologie |
|-----------|-------------|
| Backend | Flask 3.1+ |
| Base de données | SQLite |
| Frontend | HTML / CSS vanilla / JS vanilla |
| PWA | Service Worker + Manifest |

---

## Documentation

| Document | Description |
|----------|-------------|
| [VISION.md](docs/VISION.md) | L'histoire, les personnages, les fins |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Structure technique, API, fichiers |
| [ROADMAP.md](docs/ROADMAP.md) | Phases de développement |
| [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | Déploiement en production |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Comment contribuer |

---

## Développement

```bash
# Tests
python -m pytest tests/ -v

# Linting
ruff check . --fix
black . --line-length 88
```

---

*Fait avec Flask et beaucoup d'intentions narratives.*
