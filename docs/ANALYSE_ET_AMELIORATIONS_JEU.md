# Analyse du jeu : histoire, gameplay et améliorations

**Date :** 7 février 2026  
**Objectif :** Comprendre pourquoi le jeu peut sembler "nul" et appliquer des corrections ciblées.

---

## 1. Analyse de l’histoire

### Points forts
- **Arc narratif clair** : Prologue → acte_1 à acte_6 → epilogue, avec une vraie continuité (LUNA, NEXUS, PANDORA, Althea).
- **Personnage central** : LUNA est l’IA complice ; le joueur est le "hacker" qui l’aide. La doc prévoit déjà "LUNA a besoin de toi" pour renforcer ce lien.
- **Univers cohérent** : La Corp, SHADOW-13, berceuse d’Althea, fusion LUNA+NEXUS = Arkalia. Les missions (acte_1 = réparer le site, acte_2 = décrypter les logs, etc.) sont logiques.
- **Branches narratives** (`narrative_branches.json`) : Choix (friendly / cautious / aggressive avec LUNA, stealth / direct / diplomatic pour acte_1) avec effets (relation, compétences, missions débloquées).

### Points faibles
- **Double flux au démarrage** : La bannière et le message LUNA disent "tape acte_1", mais l’ancienne aide (ou des fallbacks JS) mettaient "start_tutorial" / "prologue" en premier → confusion.
- **Qui parle à l’accueil ?** Le texte animé disait "J'ai besoin de toi" sans nommer LUNA → lien émotionnel plus faible.
- **Peu de conséquences visibles des choix** : Les branches (friendly, stealth, etc.) existent en données mais ne sont pas toujours visibles dans l’UI (journal, récap par acte).

### Pistes d’amélioration histoire
- Unifier partout "acte_1 d’abord" (bannière, aide, message LUNA, tutoriel) et documenter ce choix.
- Après chaque acte, afficher un court récap "Tu as choisi X, LUNA se souvient" si des branches sont utilisées.
- Renforcer l’épilogue avec un résumé personnalisé (badges, choix majeurs).

---

## 2. Analyse du gameplay

### Points forts
- **Boucle simple** : Terminal → taper une commande → réponse API → message + score/badge. Compréhensible.
- **Défi acte_1** : Modal "Choisis le bon code" (A/B/C) avec micro-célébration → premier succès concret.
- **Feedback** : Flash vert/rouge, son, indicateur flottant "+X XP" / "✓", bandeau progression (niveau, score).
- **Contenu varié** : Mini-jeux (simple_hack, sequence_game, typing_challenge), hack_system en 3 étapes, commandes monde/explorer/naviguer, défis quotidiens (game_engine).
- **Progression** : Score, niveau, badges, missions_completed ; acte_2 débloqué après acte_1, etc.

### Points faibles
- **Premier contact** : Trois CTA au même niveau (Commencer l’aventure, Explorer le monde, Mon profil) → un joueur peut cliquer "Explorer" ou "Profil" et se retrouver sur des écrans vides (leaderboard, badges) sans avoir fait acte_1.
- **Aide trop longue** : Pour un nouveau joueur, l’aide détaillée (40+ lignes, mini-jeux, thèmes, diagnostic) peut être overwhelming ; si en plus l’ordre des commandes ne collait pas à la bannière, sentiment de "le jeu ne sait pas ce qu’il veut".
- **Terminal lourd** : Beaucoup de scripts sur la page terminal → chargement lent, risque de "ça rame".
- **États vides** : Leaderboard / badges vides sans message encourageant ("Joue pour apparaître ici !") → impression de jeu vide.

### Pistes d’amélioration gameplay
- CTA principal unique et mis en avant (déjà fait : "Commencer l’aventure" en pleine largeur, secondaires en dessous).
- Aide nouveau joueur courte (acte_1 + 5–6 commandes), aide détaillée sur "aide_avance" ou après acte_1.
- Réduire le nombre de scripts sur le terminal (bundles ou chargement différé).
- Messages encourageants sur tous les états vides (leaderboard, profil badges, monde).

---

## 3. Améliorations appliquées (ce correctif)

| Priorité | Action | Fichier(s) |
|----------|--------|------------|
| **P0** | Remplacer "J'ai besoin de toi" par "**LUNA** a besoin de toi" dans l’animation du greeting | `templates/index.html` |
| **P0** | Aligner l’aide fallback (terminal.js) sur **acte_1** en premier, comme la bannière et l’API | `static/js/terminal.js` |
| **P1** | Renforcer le CTA principal : bouton "Commencer l’aventure" en pleine largeur, plus grand ; secondaires en dessous, légèrement atténués | `templates/index.html` (CSS) |

L’API (`core/commands/basic_commands.py`) avait déjà une aide "nouveau joueur" avec acte_1 en premier ; seuls le texte d’accueil et les fallbacks JS ont été corrigés pour être cohérents.

---

## 4. Synthèse : pourquoi ça pouvait sembler "nul"

1. **Incohérence** : Bannière "tape acte_1" vs aide (ou fallbacks) qui disaient "commence par start_tutorial / prologue" → le joueur ne savait pas par où commencer.
2. **Accueil flou** : "J'ai besoin de toi" sans dire que c’est LUNA → moins d’attachement au personnage.
3. **Choix pas évident** : Trois boutons au même niveau → risque de cliquer ailleurs et tomber sur des écrans vides.
4. **Technique** : Beaucoup de CSS/JS (terminal, index) → lenteur perçue ; états vides sans message → sentiment de vide.

En alignant **une seule première action** (acte_1), en mettant **LUNA** en avant à l’accueil et en rendant le **CTA principal** visuellement prioritaire, le parcours "accueil → terminal → acte_1" devient clair et cohérent. Les autres pistes (aide courte, allègement terminal, messages états vides) restent documentées dans les audits existants pour la suite.

---

## 5. Références

- [AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md](audits/AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md) — Priorités P0/P1/P2 détaillées.
- [COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md) — Fun, game feel, onboarding (recherche 2024–2025).
- [AUDIT_VISUEL_ET_PERFORMANCES.md](AUDIT_VISUEL_ET_PERFORMANCES.md) — CSS/JS, chargement, performances.
