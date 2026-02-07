# Pourquoi Arkalia peut sembler "nul" vs les autres jeux (sources externes)

Comparaison avec la recherche et les bonnes pratiques 2024–2025 pour rendre le jeu **fun, agréable, fonctionnel et visuellement au top**.

*Dernière mise à jour : 7 février 2026.*

---

## Sources utilisées

- **Fun / psychologie** : *Player Enjoyment in Video Games* (meta-analysis), *Leveling up fun* (Nature 2025), *7 psychology principles game designers learn too late* (Medium).
- **Game feel / juice** : *Juicy Game Feedback* (CHI 2024), *Good Game Feel: Empirically Grounded Framework for Juicy Design*, Deepnight Game Feel Demo (2024).
- **Onboarding** : Inworld.ai *Best practices for video game onboarding*, BBC GEL *How to design onboarding for games*, NNGroup *Onboarding Tutorials vs. Contextual Help*, Moldstud *Engaging Onboarding 2024*.
- **Micro-interactions** : Sitepoint *Button micro-interactions*, Codrops *CSS button hover animations*, *Button glow & pulse*.
- **Visuel / UI des meilleurs jeux** : *Metaphor: ReFantazio* (Best Art Direction TGA 2024), *Beastieball* (langage visuel cohérent, Gamedeveloper.com), *Twilight Oracle* (clarté visuelle), *(the) Gnorp Apologue* (design minimal à fort impact), *How does Juicy Game Feedback Motivate?* (curiosité, compétence, CHI 2024).
- **Visuel** : En production, visuel minimal unifié ([REPARTIR_SUR_DES_BASES_SANES.md](REPARTIR_SUR_DES_BASES_SANES.md), `arkalia-minimal.css`). Référence historique : [REFONTE_VISUELLE_2026.md](REFONTE_VISUELLE_2026.md) (Solace State, Neurodiver, Hades).

---

## Ce que la recherche dit sur le "fun"

| Facteur | Ce que les autres jeux font | Risque si ton jeu ne le fait pas |
| ------- | ---------------------------- | --------------------------------- |
| **Difficulté adaptée** | Niveau intermédiaire, succès possible (Nature 2025). | Trop facile = ennuyeux ; trop dur = frustration. |
| **Attentes + succès** | Le joueur anticipe la difficulté et vit un succès (Nature 2025). | Si l’objectif est flou ou le succès peu visible = "ça ne marche pas". |
| **Musique / ambiance** | La musique est le seul élément avec effet significatif sur le plaisir (meta-analysis). | Pas d’ambiance sonore = expérience plus plate. |
| **Curiosité + compétence** | Le "juicy feedback" motive surtout par curiosité et sentiment de compétence (CHI 2024). | Feedback flou ou rare = "je ne sais pas si j’ai réussi". |

**Appliqué à Arkalia** : Promesse claire, CTA unique « Rejoindre LUNA » → Aventure, feedback sur la page Histoire (son + indicateur flottant +XP, barre de progression, célébration bouton). **Feedback lisible** (indicateur flottant « +X pts » à chaque chapitre validé), **micro-interactions** (game-feel.css), **ambiance sonore** optionnelle (bouton accueil + page Audio). Terminal en mode expert pour les joueurs avancés.

---

## Ce que les meilleurs jeux font au niveau visuel (sources 2024–2025)

| Principe | Exemple (jeu / source) | Application Arkalia |
| -------- | ---------------------- | -------------------- |
| **Langage visuel cohérent** | Beastieball : UI = représentation organisée des systèmes, même direction artistique partout. | Thèmes Luna (arkalia-themes.css), variables CSS (--violet-lunaire, --matrix-green), game-feel.css pour CTA + terminal. |
| **Clarté > complexité** | Twilight Oracle : lisibilité et logique des puzzles priment sur le détail. Metaphor : chaque écran a un design unique mais lisible. | Messages terminal typés (success/error/info), bandeau progression, bannière acte_1. |
| **Détail et polish** | Metaphor: ReFantazio : écrans de victoire animés, menus pause style aquarelle, temps passé = qualité perçue. | Flash succès/échec terminal, indicateur flottant +XP/✓, transitions game-feel (hover, active). |
| **Design minimal à fort impact** | Gnorp Apologue : visuels simples, impact par la répétition et l’échelle (milliers d’éléments). | Un seul feedback par action (zone terminal + son), pas de surcharge d’effets. |
| **Feedback lié au succès réel** | CHI 2024 Juicy : curiosité et compétence passent par un **lien action–résultat** lisible ; trop d’amplification peut réduire la motivation. | Flash et son uniquement sur vraie réussite/échec API ; indicateur flottant sur succès. |

**Résumé visuel** : Arkalia vise un **langage visuel cohérent** (couleurs, transitions), une **lisibilité** maximale (feedback immédiat, états succès/erreur), et un **polish** mesuré (micro-interactions, reduced-motion respecté) sans surcharge.

---

## Ce que la recherche dit sur le "game feel" (juicy)

| Principe | Bonne pratique | Chez nous |
| -------- | -------------- | --------- |
| **Feedback immédiat** | Réponse visuelle/audio dès l’action (framework Juicy Design). | Flash vert/rouge + son sur le terminal. |
| **Lien action–résultat** | Le feedback doit être **lié au succès réel** (CHI 2024). | Flash et son uniquement sur vraie réussite/échec API. |
| **Pas que "plus d’effets"** | Trop d’amplification peut réduire la motivation ; la **lisibilité** compte plus. | Un seul type de feedback par action (zone terminal + son). |
| **Curiosité** | Principal moteur de plaisir et de temps de jeu (CHI 2024). | Missions, actes, défi acte_1 pour garder la curiosité. |

**Appliqué** : Ajout d’un **indicateur flottant** (ex. "+XP" / "✓") sur succès de commande, **boutons avec hover satisfaisant** (scale, glow), **transitions douces** (game-feel.css).

---

## Ce que la recherche dit sur les 30 premières secondes

| Principe | Source | Application Arkalia |
| -------- | ------ | -------------------- |
| **Gameplay immédiat** | Onboarding = partie du jeu (BBC GEL). | Accueil → CTA « Rejoindre LUNA » → page Aventure (/histoire). |
| **Contexte narratif** | Donner du sens aux actions (Inworld). | "LUNA a besoin de toi", promesse 15 mots. |
| **1–3 personnages** | Connexion émotionnelle (Inworld). | LUNA mise en avant (avatar, bloc LUNA sur la page Aventure). |
| **Objectif clair** | "Boussole" pour le joueur (Inworld). | "Clique Continuer pour valider chaque chapitre." |
| **Aide contextuelle** | Au moment du besoin, pas en bloc (NNGroup). | Hint « Clique sur Continuer pour le prochain chapitre » sur la page Aventure ; tutoriel welcome pointe vers /histoire. |

**Appliqué** : Accroche sous la promesse ("Aide LUNA à sauver Arkalia : choisis ton chemin, vis l’aventure."), CTA principal mis en avant avec **micro-interaction** (pulse léger, hover satisfaisant).

---

## Checklist "jeu fun, agréable, fonctionnel, visuel top"

- [x] **Promesse en 15 mots** visible sur l’accueil.
- [x] **Un CTA principal** (Rejoindre LUNA → page Aventure /histoire).
- [x] **Micro-intro narrative** (LUNA a besoin de toi).
- [x] **Source de vérité** (progression depuis l’API ; page Aventure avec barre de progression par chapitre).
- [x] **Feedback Aventure** : son succès + indicateur flottant +XP + célébration bouton « Continuer » à chaque chapitre validé.
- [x] **Première mission claire** : page Aventure, lire le chapitre puis cliquer « Continuer » ; tutoriel welcome pointe vers /histoire.
- [x] **Navbar** : lien « Aventure » visible ; Monde/Profil etc. débloqués après le premier chapitre.
- [x] **Accroche 30 s** : « Aide LUNA à sauver Arkalia… » + CTA avec micro-interaction.
- [x] **Game feel** : indicateur flottant +X pts sur la page Aventure, bouton Continuer avec classe .celebrate au clic ; game-feel.css sur CTA et terminal.
- [x] **Ambiance sonore** optionnelle : bouton « Ambiance » sur l’accueil + page 🔊 Audio (toggle Musique de fond), préférence sauvegardée.
- [x] **Accessibilité game-feel** : respect `prefers-reduced-motion` et `body.reduced-motion`, focus visible (CTA, bouton Continuer, Exécuter terminal).
- [x] **Messages d’erreur** : messages encourageants sur la page Aventure (« Réessaie ou reviens à l’accueil ») ; terminal : hint « Tape "aide" » si commande inconnue.
- [x] **Célébration** : bouton « Continuer » avec pulse/glow après validation de chapitre (page Aventure).
- [x] **Prochaine étape** : hint « Clique sur Continuer pour le prochain chapitre » ; écran de fin avec liens Monde / Profil / Accueil.
- [x] **Visuel / UI** : tableau comparatif avec Metaphor, Beastieball, Gnorp Apologue, CHI 2024 ; game-feel étendu ; page Aventure avec bloc LUNA et barre de progression.
- [x] **Aide unifiée** : terminal (commande inconnue) indique « tape aide » + « Va au Tutoriel ou à l’Aventure (menu) ».
- [ ] **Playtests** avec 2–3 ados (voir [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md)) — seule action restante pour un jeu « parfait ».

---

## Couverture des pages (game-feel + focus + reduced-motion)

Toutes les pages du jeu ont été alignées sur le même langage visuel et l’accessibilité :

| Page | game-feel.css | Focus visible | Reduced motion |
| ---- | ------------- | ------------- | -------------- |
| Accueil (index) | oui | CTA, cartes, liens | portail, avatar, CTA, cartes |
| Aventure (/histoire) | oui (reward-animations, styles inline) | bouton Continuer, liens | barre progression, float XP |
| Terminal | oui | input, Exécuter, commandes rapides, modal acte_1 | (dans game-feel global) |
| Monde | oui | zones, boutons direction | fond, grille, zones, joueur |
| Profil | oui | boutons, liens | fond, titres |
| Dashboard | oui | boutons, liens | fond, titres |
| Classement (leaderboard) | oui | cartes défis, refresh | fond, titres, lignes, couronne, spinner |
| Tutoriel (welcome) | oui | boutons, liens | fond |
| Arbre de compétences | oui | boutons, liens | — |
| Explorateur | oui | boutons, liens | grille, particules |
| Mail | oui | boutons, liens | grille, particules |
| Audio | oui | boutons, liens | grille, particules |
| Accessibilité | oui | boutons, liens | fond, titre |
| Tutoriels techniques | oui | boutons, liens, cartes | — |

La navbar (composant partagé) a un focus visible via `accessibility.css` (`.nav-link:focus-visible`) et `game-feel.css` (`.burger-btn:focus-visible` pour le menu mobile). **Cohérence** : toutes les pages (accueil, aventure, terminal, monde, profil, dashboard, leaderboard, skill-tree, etc.) utilisent le même composant `navbar.html` avec `active_page` et `profil` ; le lien « Aventure » est le parcours principal recommandé.

---

## Résumé

Le jeu n’est pas "nul" : il est **solide techniquement** et **aligné** avec la recherche (promesse, onboarding par l’Aventure, feedback lié au succès, game feel). En place : **parcours principal** Accueil → Aventure (chapitres + bouton Continuer), **feedback lisible** (indicateur flottant +X pts, son, célébration bouton), **micro-interactions** (game-feel.css), **accroche 30 s**, **ambiance sonore** optionnelle, **accessibilité** (reduced-motion, focus visible), **messages d’erreur** encourageants. Il reste les **playtests** avec ados pour valider et itérer.

---

## Refonte visuelle 2026 (7 février 2026)

Une **refonte complète du visuel** a été documentée et implémentée :

- **Problème** : Palette violet + vert matrix trop générique, peu d’identité, ressenti « outil » plutôt qu’« aventure ».
- **Références ajoutées** : Solace State, Read Only Memories: Neurodiver, Metaphor: ReFantazio, Hades/Supergiant pour principes (langage cohérent, clarté, émotion).
- **Nouvelle direction** : « Arkalia — Nuit émotionnelle » — fond bleu nuit, ambre/corail pour LUNA et chaleur, cyan pour actions, design system dans `arkalia-visual-2026.css`. Détail : [REFONTE_VISUELLE_2026.md](REFONTE_VISUELLE_2026.md).
- **Checklist** : Accueil, /histoire, navbar, contraste WCAG, reduced-motion, pas de régression sur les autres pages.

---

## Prochaines étapes

1. **Organiser les playtests** avec 2–3 ados (scénario 15 min dans [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md)).
2. **Synthétiser les retours** : points communs, blocages récurrents, idées (grille d’observation du guide).
3. **Prioriser 1–2 changements** (ex. texte d’aide, placement d’un bouton, difficulté du défi acte_1) et mettre à jour ce doc + [STATUT_PROJET_ACTUEL.md](STATUT_PROJET_ACTUEL.md) avec « Retours playtest du [date] ».
4. **Itérer** : réappliquer la checklist après chaque vague de playtests si besoin.

---

## Template « Retours playtest du [date] »

À coller dans [STATUT_PROJET_ACTUEL.md](STATUT_PROJET_ACTUEL.md) après une session :

```markdown
### Retours playtest du [JJ/MM/AAAA] (2–3 ados)

- **Clarté** : …
- **Premier pas (CTA → Aventure, clic Continuer)** : …
- **Boucle chapitres (lire → Continuer)** : …
- **Points à améliorer** : …
- **Note moyenne /10** : …
- **Changements priorisés** : 1) … 2) …
```

---

## Liens utiles

| Doc | Rôle |
| --- | ---- |
| [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md) | Scénario 15 min, grille d’observation, checklist avant session |
| [STATUT_PROJET_ACTUEL.md](STATUT_PROJET_ACTUEL.md) | Vue d’ensemble, métriques, où coller les retours playtest |
| [audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md](audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md) | Audit UX / bonnes pratiques détaillé |
| [audits/AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md](audits/AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md) | Audit complet "pourquoi le jeu semble nul" + corrections P0/P1/P2 |

---

## Référence code (pour mainteneurs)

| Élément | Fichier(s) |
| ------- | ---------- |
| Game feel (CTA, terminal, reduced-motion, focus) | `static/css/game-feel.css` |
| Ambiance sonore + sons succès/erreur | `static/js/audio-manager.js` |
| Terminal : envoi commande, float +XP/✓, flash, modal acte_1 | `templates/terminal.html` (script inline + `sendCommand` / `processCommand`) |
| Accueil : CTA, bouton Ambiance | `templates/index.html` |
| Aventure : chapitres, choix (acte_5) + message narratif par choix, barre progression, fonds/émotions, transition, badge Nouveau, « Tu as choisi », toggle Ambiance, float +XP, son | `templates/histoire.html`, `data/story_chapters.json` |
| API état / choix histoire | `app.py` → `GET /api/story/state`, `POST /api/story/choice` |
| Bandeau progression (niveau, score) | `templates/terminal.html` (`#terminalProgressionStrip`, `refreshProgressionFromServer`) |
| API commande terminal | `app.py` → `POST /api/terminal/command` |
