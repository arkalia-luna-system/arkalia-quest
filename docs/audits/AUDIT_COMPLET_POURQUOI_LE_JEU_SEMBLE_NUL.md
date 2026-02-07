# Audit complet — Pourquoi le jeu peut sembler "nul" (et comment le rendre fun)

**Date :** 7 février 2026  
**Objectif :** Identifier tout ce qui donne l’impression que le jeu est "très nul" et proposer des corrections **priorisées**.

---

## Résumé en 3 lignes

1. **Le jeu n’est pas nul techniquement** : récit (actes 1–6, epilogue), commandes, API, feedback visuel/sonore sont en place.
2. **Ce qui le fait paraître nul** : incohérences (bannière dit "acte_1", l’aide dit "prologue / start_tutorial"), surcharge (38 scripts sur le terminal, dizaines de CSS), et premier contact pas assez direct.
3. **Leviers prioritaires** : aligner aide + bannière sur **une seule** première action (acte_1), alléger le chargement du terminal, renforcer la promesse et le CTA sur l’accueil.

---

## 1. Parcours joueur (accueil → terminal → première mission)

### ✅ Ce qui va bien

- Promesse 15 mots sur l’accueil.
- CTA principal "Commencer l’aventure" → Terminal.
- Bannière "Première mission : tape **acte_1**" sur le terminal.
- Message LUNA dans le terminal : "Pour commencer, tape **acte_1**. Sinon tape **aide**."
- Modal acte_1 "Choisis le bon code" (A/B/C) avec micro-célébration.
- Bannière "Prochaine étape : tape acte_2" (puis acte_3… epilogue) après chaque mission.

### ❌ Ce qui casse l’impression

| Problème | Où | Impact |
|----------|-----|--------|
| **Incohérence première action** | Bannière + message terminal disent "tape **acte_1**", mais la commande **aide** pour un nouveau joueur dit "COMMENCE ICI : **start_tutorial**, **prologue**, luna_contact" sans mentionner acte_1. | Le joueur qui tape "aide" croit qu’il doit faire prologue d’abord → confusion, sentiment que "le jeu ne sait pas ce qu’il veut". |
| **Accueil : qui parle ?** | Texte actuel : *"J'ai besoin de toi. Ensemble on va débloquer cette histoire. Tu es prêt ?"* — la doc (COMPARAISON) prévoit "**LUNA** a besoin de toi". | Moins clair que c’est LUNA qui s’adresse au joueur → lien émotionnel plus faible. |
| **Trop de CTA sur l’accueil** | 3 boutons au même niveau : "Commencer l’aventure", "Explorer le monde", "Mon profil". | Un ado peut cliquer "Explorer le monde" ou "Mon profil" en premier → pas la boucle voulue (terminal → acte_1). |

### Recommandations (parcours)

- **P0** : Dans **aide** (nouveau joueur), mettre **acte_1** en premier dans "COMMENCE ICI" et raccourcir la liste (ex. "acte_1 → Ta première mission" puis "aide / profil / monde"). Garder prologue/start_tutorial plus bas ou après acte_1.
- **P0** : Sur l’accueil, remplacer "J'ai besoin de toi" par "**LUNA** a besoin de toi" (ou "LUNA a besoin de toi. Tu es prêt ?").
- **P1** : Renforcer visuellement le CTA principal (taille, contraste) et dégrader un peu "Explorer le monde" / "Mon profil" (secondaires) pour que "Commencer l’aventure" soit le choix évident.

---

## 2. Contenu et clarté (messages, commandes, feedback)

### ✅ Ce qui va bien

- Récit structuré (prologue, acte_1 à acte_6, epilogue) avec vrais textes dans `story_commands.py`.
- Messages d’erreur avec hint "Tape 'aide' pour voir les commandes" en cas de commande inconnue.
- Indicateur flottant "+X XP" / "✓" sur succès au terminal.
- Flash vert/rouge + son sur succès/échec.

### ❌ Ce qui casse l’impression

| Problème | Où | Impact |
|----------|-----|--------|
| **Aide trop longue pour un débutant** | Premier bloc "aide" = ~40 lignes (histoire, mini-jeux, thèmes, diagnostic…). | Overwhelming → "trop compliqué", le joueur abandonne ou ne lit pas. |
| **Deux flux narratifs** | Certaines commandes supposent "prologue fait" (aide avancé), mais la bannière pousse à acte_1 sans prologue. | Incohérence narrative et mécanique. |
| **Peu de récompense visible après acte_1** | Modal se ferme, message "Défi réussi", bannière acte_2. Pas de "+XP" ou "Niveau 2" clairement mis en avant dans le bandeau tout de suite. | Le joueur ne "sent" pas la progression. |

### Recommandations (contenu)

- **P0** : Aide nouveau joueur : un bloc court "COMMENCE ICI : **acte_1** (ta première mission). Puis **aide** pour plus de commandes." + 5–6 commandes essentielles max. Déplacer le gros bloc actuel en "Aide détaillée" (après acte_1 ou commande "aide_avance").
- **P1** : Après succès acte_1 (modal), s’assurer que le bandeau "Niveau | Score" se met à jour immédiatement (déjà prévu via `refreshProgressionFromServer`) et éventuellement afficher un court message "+X points !" dans le bandeau.
- **P2** : Unifier le flux : soit "acte_1 d’abord" partout (bannière + aide + message LUNA), soit "prologue puis acte_1" partout ; documenter le choix dans STATUT / COMPARAISON.

---

## 3. Technique et ressenti (performance, erreurs, vide)

### ✅ Ce qui va bien

- API `/api/terminal/command` fiable, game_engine + CommandHandlerV2 cohérents.
- game-feel.css sur les pages, reduced-motion et focus visible.
- Empty states prévus (leaderboard, profil, monde, tutoriels).

### ❌ Ce qui casse l’impression

| Problème | Où | Impact |
|----------|-----|--------|
| **Terminal très lourd** | **38 scripts** chargés sur la page terminal (`templates/terminal.html`). | Temps de chargement long, risque de freeze ou latence au premier clic → "le jeu rame", "c’est nul". |
| **Beaucoup de CSS par page** | Profil, dashboard, leaderboard : 15+ feuilles CSS (arkalia, accessibility, empty-states, game-interface, mission-interface, reward, loading, progression, adaptive, competitive, creative, casual, game-feel…). | Temps de rendu, maintenance difficile, incohérences possibles. |
| **Pages "vides" au début** | Leaderboard, profil badges, monde missions : états vides "Aucun joueur", "Aucun badge". | Normal pour un nouveau joueur, mais si pas de message encourageant ("Joue pour apparaître ici !") ça fait "jeu vide". |
| **Double logique terminal ?** | Template terminal a son propre `sendCommand` / `processCommand` (fetch `/api/terminal/command`). terminal.js a `executeCommand` (fetch `/commande`). Le bouton n’a pas d’id `sendButton` donc seul le script inline tourne → une seule source d’envoi, mais **deux APIs** différentes selon les pages/scripts. | Risque de confusion en maintenance ; tests qui ciblent `/commande` alors que le flux principal utilise `/api/terminal/command`. |

### Recommandations (technique)

- **P0** : Réduire le nombre de scripts sur le terminal : regrouper en 2–3 bundles (ex. terminal-core.js, terminal-games.js) ou charger en différé tout ce qui n’est pas nécessaire au premier envoi de commande (mini-jeux, hacking effects, etc.). Viser **&lt; 15 scripts** en chargement critique.
- **P1** : Vérifier que les états vides (leaderboard, badges) affichent un court message motivant ("Joue au terminal pour gagner des points et apparaître ici !").
- **P2** : Documenter clairement : "Flux principal = template terminal + `/api/terminal/command` ; terminal.js = legacy ou autres contextes" (ou migrer tout vers une seule API et un seul script d’envoi).

---

## 4. Synthèse : priorités pour ne plus avoir l’impression que "c’est nul"

### Priorité 0 (rapide, fort impact)

1. **Alignement aide + bannière** : Pour un nouveau joueur, la commande **aide** doit dire en premier "COMMENCE ICI : **acte_1** (ta première mission)." comme la bannière et le message LUNA.
2. **Accueil** : Remplacer "J'ai besoin de toi" par "**LUNA** a besoin de toi" (ou formulation équivalente mettant LUNA en avant).
3. **Alléger le terminal** : Réduire le nombre de scripts chargés sur la page terminal (bundles ou chargement différé) pour améliorer le temps de chargement et la réactivité.

### Priorité 1 (moyen terme)

4. ~~Aide nouveau joueur : version courte~~ — **fait** (acte_1 en premier dans aide).
5. ~~Renforcer le CTA principal sur l’accueil~~ — **fait** (ligne « 👉 Clique ici pour lancer ta première mission » au-dessus du CTA).
6. Message de progression immédiat après acte_1 (bandeau à jour + éventuel "+X points" visible) — déjà en place via `refreshProgressionFromServer` ; optionnel : message "+X points !" dans le bandeau.
7. ~~États vides : message encourageant sur leaderboard / badges~~ — **fait** (leaderboard : les deux emplacements ont le message ; profil : déjà en place).

### Priorité 2 (long terme)

8. Unifier le flux narratif (acte_1 first vs prologue first) et le documenter.
9. Rationaliser les CSS (moins de fichiers par page, thèmes/design system).
10. Une seule API terminal côté front (tout passer par `/api/terminal/command` ou tout par `/commande`) et documenter.

---

## 5. Références croisées

- **Checklist fun/visuel** : [COMPARAISON_JEUX_SOURCES_EXTERNES.md](../COMPARAISON_JEUX_SOURCES_EXTERNES.md)
- **Audit bonnes pratiques 2026** : [AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md](AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md)
- **Playtests** : [PLAYTEST_GUIDE_ADOS.md](../PLAYTEST_GUIDE_ADOS.md) — les retours ados valideront ou infléchiront ces priorités.

---

*Audit réalisé à partir du code (routes, templates, core/commands), de la doc existante et des critères "fun / game feel / onboarding" des références 2024–2025.*
