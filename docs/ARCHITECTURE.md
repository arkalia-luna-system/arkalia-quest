# Architecture technique — LUNA Hors Connexion

**Version :** 1.0 (Mars 2026)

---

## Vue d'ensemble

Architecture minimaliste. Chaque fichier a un rôle précis. Rien de superflu.

```
arkalia-quest/
├── app.py                          ← point d'entrée Flask
├── routes/
│   ├── pages.py                    ← routes HTML (/, /game, /profil, /leaderboard)
│   └── story.py                    ← API narrative (state, choice, save)
├── core/
│   ├── luna_emotions_engine.py     ← moteur émotions LUNA (GARDÉ + adapté)
│   ├── gamification_engine.py      ← XP, niveaux, badges (GARDÉ)
│   ├── progression_engine.py       ← progression du joueur (GARDÉ + adapté)
│   ├── profile_manager.py          ← profils joueurs (GARDÉ)
│   ├── database.py                 ← SQLite (GARDÉ)
│   ├── security_unified.py         ← sécurité (GARDÉ)
│   ├── ark_logger.py               ← logs (GARDÉ)
│   └── story_engine.py             ← NOUVEAU : moteur narratif principal
├── data/
│   ├── story.json                  ← NOUVEAU : toute la narration + choix + branches
│   ├── profiles/                   ← profils joueurs (GARDÉ)
│   ├── progression.json            ← progression (GARDÉ)
│   └── leaderboard.json            ← classement (GARDÉ)
├── templates/
│   ├── index.html                  ← accueil (RÉÉCRIT)
│   ├── game.html                   ← page principale du jeu (NOUVEAU)
│   ├── profil.html                 ← profil joueur (SIMPLIFIÉ)
│   ├── leaderboard.html            ← classement (SIMPLIFIÉ)
│   └── components/
│       ├── navbar.html             ← navigation (SIMPLIFIÉ)
│       └── luna_avatar.html        ← NOUVEAU : avatar LUNA expressif
├── static/
│   ├── css/
│   │   └── game.css                ← UN SEUL fichier CSS (NOUVEAU)
│   ├── js/
│   │   ├── game.js                 ← moteur de jeu frontend (NOUVEAU)
│   │   ├── audio-manager.js        ← sons (GARDÉ)
│   │   └── service-worker.js       ← PWA (GARDÉ)
│   └── audio/                      ← musique ambiante + effets sonores
└── tests/
    └── (nouveaux tests après réécriture)
```

---

## API Story (3 endpoints)

### `GET /api/story/state`
Retourne l'état courant du joueur dans la narration.

```json
{
  "chapter_id": "chapitre_3",
  "scene_id": "scene_2",
  "luna_emotion": "inquiète",
  "luna_trust": 67,
  "dialogue": "Tu es là ? J'ai besoin que tu sois honnête avec moi.",
  "choices": [
    { "id": "c1", "label": "Je suis là. Dis-moi ce qui se passe." },
    { "id": "c2", "label": "Pourquoi tu m'as caché ça ?" },
    { "id": "c3", "label": "Je ne peux pas te faire confiance." }
  ],
  "chapter_progress": 3,
  "total_chapters": 8
}
```

### `POST /api/story/choice`
Enregistre un choix et retourne la scène suivante.

Payload :
```json
{ "scene_id": "scene_2", "choice_id": "c1" }
```

Réponse :
```json
{
  "next_scene": { ... },
  "trust_delta": +5,
  "xp_gained": 50,
  "luna_reaction": "soulagée",
  "unlock": null
}
```

### `POST /api/story/save`
Sauvegarde manuelle de la progression.

---

## Format de données : story.json

```json
{
  "chapters": [
    {
      "id": "chapitre_0",
      "title": "Signal",
      "scenes": [
        {
          "id": "scene_0_0",
          "luna_emotion": "mystérieuse",
          "dialogue": "...",
          "choices": [
            {
              "id": "c1",
              "label": "...",
              "trust_delta": 5,
              "next_scene": "scene_0_1",
              "luna_reaction": "...",
              "xp": 30
            }
          ]
        }
      ]
    }
  ],
  "endings": {
    "fusion": { "condition": "trust >= 70 AND nexus_helped", "scene": "ending_a" },
    "sacrifice": { "condition": "trust >= 40", "scene": "ending_b" },
    "pandora": { "condition": "pandora_revealed", "scene": "ending_c" }
  }
}
```

---

## Moteur narrative (story_engine.py)

Responsabilités :
- Charger `story.json`
- Calculer la scène suivante selon le choix et l'historique
- Mettre à jour le score de confiance LUNA
- Déclencher l'attribution de XP/badges via `gamification_engine`
- Déterminer quelle fin est accessible

---

## Pages (4 routes HTML)

| Route | Template | Description |
|-------|----------|-------------|
| `/` | `index.html` | Accueil : message LUNA + CTA unique "Répondre au signal" |
| `/game` | `game.html` | Le jeu complet (dialogue + choix + avatar LUNA) |
| `/profil` | `profil.html` | Stats du joueur, fins débloquées, badges |
| `/leaderboard` | `leaderboard.html` | Classement (optionnel, phase 2) |

---

## CSS : un seul fichier

`static/css/game.css` contient :
- Variables CSS (couleurs, typographie, espacements)
- Layout de base (accueil, écran jeu, profil)
- Avatar LUNA et émotions
- Boutons de choix et interactions
- Effet typewriter
- Animations réduites (respect `prefers-reduced-motion`)
- Responsive (mobile first)

**Palette :**
- Fond : `#080c14` (noir bleu profond)
- LUNA accent : `#e07c54` (ambre/corail — chaleur, émotion)
- Actions / choix : `#3dd6f5` (cyan — interaction)
- Texte : `#c9d1d9` (gris clair doux)
- Danger / tension : `#ff4d6d` (rouge rosé)

---

## Ce qu'on supprime (liste complète)

### Templates supprimés
`accessibility_panel.html`, `audio.html`, `dashboard.html`, `explorateur.html`,
`histoire.html`, `mail.html`, `monde.html`, `skill_tree.html`, `technical_tutorials.html`,
`terminal.html`, `tutorial_welcome.html` et tous les composants actuels.

### CSS supprimés (46 fichiers)
Tout `static/css/` sauf ce qu'on crée : `game.css`.

### JS supprimés (66 fichiers)
Tout `static/js/` sauf : `audio-manager.js`, `service-worker.js` + nouveau `game.js`.

### Python supprimés
`command_handler_v2.py`, `core/commands/`, `adaptive_storytelling.py`,
`advanced_achievements.py`, `category_leaderboards.py`, `customization_engine.py`,
`daily_challenges_engine.py`, `database_optimizer.py`, `educational_games_engine.py`,
`game_engine.py`, `micro_interactions.py`, `mission_progress_tracker.py`,
`mission_unified.py`, `narrative_branches.py`, `secondary_missions.py`,
`social_engine.py`, `technical_tutorials.py`, `tutorial_manager.py`,
`websocket_manager.py`, `engines/effects_engine.py`, `engines/luna_ai.py`.

### Data supprimée
`data/missions/`, `data/dark_help.txt`, `data/technical_tutorials.json`,
`data/tutoriel_interactif.json`, `data/narrative_branches.json`,
`data/story_chapters.json`, `data/enhanced_missions.json`, `data/daily_challenges.json`,
`data/tutorial_progress/`, `data/objets_symboliques/`, `data/effects/`.

---

## Ordre de construction

1. `data/story.json` — écrire toute la narration (Chapitre 0–7 + 3 fins)
2. `core/story_engine.py` — moteur narratif
3. `routes/story.py` — 3 endpoints API
4. `templates/game.html` + `templates/index.html` — UI
5. `static/css/game.css` — style complet
6. `static/js/game.js` — logique frontend
7. Nettoyage : supprimer tout ce qui est listé ci-dessus
8. Tests : nouveaux tests pour le story engine
