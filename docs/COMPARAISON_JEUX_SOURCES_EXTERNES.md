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

---

## Ce que la recherche dit sur le "fun"

| Facteur | Ce que les autres jeux font | Risque si ton jeu ne le fait pas |
| ------- | ---------------------------- | --------------------------------- |
| **Difficulté adaptée** | Niveau intermédiaire, succès possible (Nature 2025). | Trop facile = ennuyeux ; trop dur = frustration. |
| **Attentes + succès** | Le joueur anticipe la difficulté et vit un succès (Nature 2025). | Si l’objectif est flou ou le succès peu visible = "ça ne marche pas". |
| **Musique / ambiance** | La musique est le seul élément avec effet significatif sur le plaisir (meta-analysis). | Pas d’ambiance sonore = expérience plus plate. |
| **Curiosité + compétence** | Le "juicy feedback" motive surtout par curiosité et sentiment de compétence (CHI 2024). | Feedback flou ou rare = "je ne sais pas si j’ai réussi". |

**Appliqué à Arkalia** : Promesse claire, CTA unique, feedback terminal (flash + son + bandeau progression), défi acte_1, navbar simplifiée. **Feedback lisible** (indicateur flottant « +X XP » / « ✓ »), **micro-interactions** (game-feel.css), **ambiance sonore** optionnelle (bouton accueil + page Audio).

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
| **Gameplay immédiat** | Onboarding = partie du jeu (BBC GEL). | Accueil → un CTA "Commencer l’aventure" → Terminal. |
| **Contexte narratif** | Donner du sens aux actions (Inworld). | "LUNA a besoin de toi", promesse 15 mots. |
| **1–3 personnages** | Connexion émotionnelle (Inworld). | LUNA mise en avant (avatar, messages). |
| **Objectif clair** | "Boussole" pour le joueur (Inworld). | "Tape acte_1 pour ta première mission." |
| **Aide contextuelle** | Au moment du besoin, pas en bloc (NNGroup). | Bannière "tape acte_1" sur le terminal, pas de tutoriel long. |

**Appliqué** : Accroche en une ligne sous la promesse ("Tu tapes des commandes, tu débloques des missions. C’est parti."), CTA principal mis en avant avec **micro-interaction** (pulse léger, hover satisfaisant).

---

## Checklist "jeu fun, agréable, fonctionnel, visuel top"

- [x] **Promesse en 15 mots** visible sur l’accueil.
- [x] **Un CTA principal** (Commencer l’aventure).
- [x] **Micro-intro narrative** (LUNA a besoin de toi).
- [x] **Source de vérité** (progression depuis l’API, bandeau terminal).
- [x] **Feedback terminal** : flash succès/échec + son.
- [x] **Première mission claire** : bannière acte_1, défi "Choisis le bon code".
- [x] **Navbar simplifiée** tant qu’acte_1 n’est pas fait.
- [x] **Accroche 30 s** : une ligne "Tu tapes des commandes…" + CTA avec micro-interaction.
- [x] **Game feel** : indicateur flottant succès (+XP/✓), bouton Exécuter et CTA avec hover/transition satisfaisants (game-feel.css).
- [x] **Ambiance sonore** optionnelle : bouton « Ambiance » sur l’accueil + page 🔊 Audio (toggle Musique de fond), préférence sauvegardée.
- [x] **Accessibilité game-feel** : respect `prefers-reduced-motion` et `body.reduced-motion`, focus visible (CTA, bouton Exécuter).
- [x] **Messages d’erreur** : hint « Tape "aide" pour voir les commandes » quand commande inconnue.
- [x] **Modal acte_1** : micro-célébration (scale + glow) avant fermeture au bon code.
- [x] **Prochaine étape** : bannière « tape acte_2 » (puis acte_3… epilogue) après chaque mission.
- [x] **Visuel / UI** : tableau comparatif avec Metaphor, Beastieball, Gnorp Apologue, CHI 2024 (voir section « Ce que les meilleurs jeux font au niveau visuel ») ; game-feel étendu aux boutons de commande rapide (.command-btn), focus-visible et reduced-motion cohérents.
- [ ] **Playtests** avec 2–3 ados (voir [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md)) — guide prêt, à organiser en conditions réelles.

---

## Couverture des pages (game-feel + focus + reduced-motion)

Toutes les pages du jeu ont été alignées sur le même langage visuel et l’accessibilité :

| Page | game-feel.css | Focus visible | Reduced motion |
| ---- | ------------- | ------------- | -------------- |
| Accueil (index) | oui | CTA, cartes, liens | portail, avatar, CTA, cartes |
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

La navbar (composant partagé) a un focus visible via `accessibility.css` (`.nav-link:focus-visible`) et `game-feel.css` (`.burger-btn:focus-visible` pour le menu mobile).

---

## Résumé

Le jeu n’est pas "nul" : il est **solide techniquement** et **déjà aligné** avec une grande partie de la recherche (promesse, onboarding, feedback lié au succès, game feel). Améliorations en place : **feedback lisible** (indicateur flottant « +X XP » / « ✓ » à chaque succès), **micro-interactions** (game-feel.css), **accroche 30 s**, **ambiance sonore** optionnelle (bouton sur l’accueil + toggle sur la page 🔊 Audio), **accessibilité** (reduced-motion, focus visible), **messages d’erreur** amicaux, **célébration** du défi acte_1. Il reste les **playtests** avec ados pour valider et itérer.

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
- **Premier pas (CTA → terminal)** : …
- **Boucle acte_1 (défi code)** : …
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

---

## Référence code (pour mainteneurs)

| Élément | Fichier(s) |
| ------- | ---------- |
| Game feel (CTA, terminal, reduced-motion, focus) | `static/css/game-feel.css` |
| Ambiance sonore + sons succès/erreur | `static/js/audio-manager.js` |
| Terminal : envoi commande, float +XP/✓, flash, modal acte_1 | `templates/terminal.html` (script inline + `sendCommand` / `processCommand`) |
| Accueil : CTA, bouton Ambiance | `templates/index.html` |
| Bandeau progression (niveau, score) | `templates/terminal.html` (`#terminalProgressionStrip`, `refreshProgressionFromServer`) |
| API commande terminal | `app.py` → `POST /api/terminal/command` |
