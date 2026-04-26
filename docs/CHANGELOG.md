# Changelog — LUNA Hors Connexion

## [Unreleased] — Mars 2026

### Refonte complète du concept
- Abandon du terminal et des commandes comme mécanique centrale
- Nouveau concept : jeu narratif par choix, LUNA comme personnage principal
- Nouveau public cible : ados 12–16 ans, fans de vrais jeux
- Suppression de 100+ fichiers CSS/JS/templates obsolètes
- Suppression de 80+ fichiers MD d'anciens audits et rapports
- Nouveaux docs : VISION.md, ARCHITECTURE.md, ROADMAP.md
- README entièrement réécrit

### Architecture ciblée
- 4 routes HTML (/, /game, /profil, /leaderboard)
- 3 endpoints API (/api/story/state, /api/story/choice, /api/story/save)
- 1 fichier CSS (game.css)
- 1 fichier JS principal (game.js)
- Nouveau moteur narratif (story_engine.py)
- Nouveau format de données (story.json)
