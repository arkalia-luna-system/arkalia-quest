# Roadmap — LUNA Hors Connexion

*Mise à jour : Mars 2026*

---

## ✅ Phase 0 — Nettoyage (TERMINÉ)

- [x] Supprimer les docs obsolètes (terminal, vieux audits, vieux rapports)
- [x] Audit complet du code existant
- [x] Écrire les nouveaux docs (VISION, ARCHITECTURE, ROADMAP)
- [x] Supprimer les fichiers code obsolètes (CSS, JS, templates, Python)
- [x] Squelette propre — 0 dette technique

---

## ✅ Phase 1 — Le squelette du jeu (TERMINÉ)

- [x] Écrire `data/story.json` — 8 chapitres + 3 fins avec vrais choix
- [x] Créer `core/story_engine.py` — moteur narratif complet
- [x] Créer `routes/story.py` — 5 endpoints API
- [x] Créer `templates/game.html` — écran de jeu
- [x] Créer `static/css/game.css` — style complet
- [x] Créer `static/js/game.js` — typewriter, appels API, transitions

---

## ✅ Phase 2 — L'histoire complète (TERMINÉ)

- [x] 8 chapitres jouables + 3 fins distinctes (fin_a, fin_b, fin_c)
- [x] Les 3 fins sont toutes atteignables (bug fin_b corrigé)
- [x] Système de confiance LUNA visible dans l'UI
- [x] Sauvegardes automatiques SQLite (persistance par UUID)
- [x] LUNA se souvient du prénom du joueur (`{{joueur}}` dans les dialogues)

---

## ✅ Phase 3 — Le polish (TERMINÉ)

- [x] Avatar LUNA animé (CSS pur, 8 expressions)
- [x] Effets sonores Web Audio API (typing, choix, trust, transitions)
- [x] Atmosphères visuelles par chapitre (dark, tense, revelations, confrontation…)
- [x] Transitions cinématiques entre chapitres
- [x] Micro-animations sur les boutons de choix
- [x] Écran de fin avec animation CSS
- [x] Effet CRT scanlines en arrière-plan

---

## 🔜 Phase 4 — Tests et corrections

**Objectif :** playtest avec 2–3 ados (dont ton fils).

- [ ] Session de jeu complète (~1h30)
- [ ] Observer sans intervenir : où est-ce qu'il accroche, hésite, sourit
- [ ] Identifier les 3 plus grands problèmes
- [ ] Corriger, rejouer

---

## 🔜 Phase 5 — Profil et rejouabilité

- [ ] Badges visuels pour chaque fin obtenue (avec illustration)
- [ ] "Souvenir" : LUNA mentionne les choix passés si tu rejoues
- [ ] Indices subtils sur les fins non encore débloquées
- [ ] Statistiques de confiance et de choix dans le profil

---

## Ce qu'on ne fait PAS (pour l'instant)

- Pas de mode multijoueur
- Pas de leaderboard (inutile pour un jeu narratif solo)
- Pas de système de points complexe
- Pas d'internationalisation
- Pas d'app mobile native

Ces choses peuvent venir plus tard si le jeu fonctionne. Pas avant.
