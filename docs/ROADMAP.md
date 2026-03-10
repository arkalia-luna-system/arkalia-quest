# Roadmap — LUNA Hors Connexion

*Mars 2026*

---

## Phase 0 — Nettoyage (EN COURS)

- [x] Supprimer les docs obsolètes (terminal, vieux audits, vieux rapports)
- [x] Audit complet du code existant
- [x] Écrire les nouveaux docs (VISION, ARCHITECTURE, ROADMAP)
- [ ] Supprimer les fichiers code obsolètes (CSS, JS, templates, Python)
- [ ] Garder le squelette utile propre

---

## Phase 1 — Le squelette du jeu

**Objectif :** avoir quelque chose de jouable, même avec un seul chapitre.

- [ ] Écrire `data/story.json` — Chapitre 0 complet (Signal) avec 3 scènes et vrais choix
- [ ] Créer `core/story_engine.py` — charge la narration, calcule la scène suivante, gère la confiance
- [ ] Créer `routes/story.py` — `GET /api/story/state` et `POST /api/story/choice`
- [ ] Créer `templates/game.html` — écran de jeu (avatar LUNA + dialogue + choix)
- [ ] Créer `static/css/game.css` — style complet (palette, layout, avatar, boutons)
- [ ] Créer `static/js/game.js` — typewriter, appels API, transitions

**Résultat :** Le Chapitre 0 est jouable de bout en bout.

---

## Phase 2 — L'histoire complète

**Objectif :** 8 chapitres jouables, 3 fins différentes.

- [ ] Écrire les Chapitres 1–7 dans `data/story.json`
- [ ] Implémenter les 3 fins dans `story_engine.py`
- [ ] Système de confiance LUNA visible dans l'UI
- [ ] Sauvegardes automatiques entre chapitres
- [ ] Adapter `luna_emotions_engine.py` au nouveau système

**Résultat :** Le jeu est complet de la première à la dernière scène.

---

## Phase 3 — Le polish

**Objectif :** ça doit *vraiment* avoir l'air d'un jeu.

- [ ] Avatar LUNA animé (CSS pur, 5–6 expressions)
- [ ] Effets sonores sur les choix importants
- [ ] Musique ambiante par chapitre (3 atmosphères)
- [ ] Transitions entre scènes (fondu, glissement)
- [ ] Micro-animations sur les boutons de choix
- [ ] Écran de fin mémorable (animation CSS)

**Résultat :** Quelqu'un qui ne connaît pas le projet peut jouer et trouver ça cool.

---

## Phase 4 — Tests et corrections

**Objectif :** playtest avec 2–3 ados (dont ton fils).

- [ ] Session de jeu complète (~1h30)
- [ ] Observer sans intervenir : où est-ce qu'il accroche, hésite, sourit
- [ ] Identifier les 3 plus grands problèmes
- [ ] Corriger, rejouer

---

## Phase 5 — Profil et rejouabilité

- [ ] Page `/profil` : fins débloquées, badges, stats de confiance LUNA
- [ ] Badges pour chaque fin obtenue
- [ ] "Souvenir" : LUNA se rappelle de ton nom si tu joues une 2e fois
- [ ] Indices subtils sur les fins non encore débloquées

---

## Ce qu'on ne fait PAS (pour l'instant)

- Pas de mode multijoueur
- Pas de leaderboard (inutile pour un jeu narratif solo)
- Pas de système de points complexe
- Pas d'internationalisation
- Pas d'app mobile native

Ces choses peuvent venir plus tard si le jeu fonctionne. Pas avant.
