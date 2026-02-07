# Audit complet du projet et révision du concept — Arkalia Quest

**Date :** 7 février 2026  
**Objectif :** Auditer l’ensemble du projet, identifier pourquoi le concept actuel (terminal, promesse, ressenti) ne convient pas, et proposer une **révision complète du concept** sans terminal.

---

## Partie 1 — Audit du projet actuel

### 1.1 Ce qu’est le jeu aujourd’hui

| Élément | Description |
|--------|--------------|
| **Genre annoncé** | Serious game éducatif (cybersécurité / hacking) pour ados |
| **Promesse (15 mots)** | *« Tu es un hacker qui aide LUNA : missions au terminal, actes et mini-jeux. »* |
| **Cœur du gameplay** | **Terminal** : le joueur tape des commandes (`acte_1`, `aide`, `profil`, `monde`, etc.) ; LUNA (IA émotionnelle) répond ; des actes narratifs (prologue, acte_1… acte_6, épilogue) structurent l’histoire |
| **Progression** | XP, niveaux, badges, score, profils persistants, bandeau de progression sur le terminal |
| **Pages** | Accueil → Terminal (central), Monde, Profil, Dashboard, Leaderboard, Tutoriel, Arbre de compétences, Explorateur, Mail, Audio, Accessibilité, Tutoriels techniques |
| **Stack** | Flask, SQLite, templates HTML, CSS (nombreux fichiers), JS (nombreux scripts), API `POST /api/terminal/command` |

En résumé : **tout tourne autour du terminal**. L’accueil envoie vers « Commencer l’aventure » → Terminal. La première mission est « tape acte_1 ». La progression, les récompenses et le récit passent par la frappe de commandes.

---

### 1.2 Pourquoi le terminal pose problème (et ne te plaît pas)

- **Ressenti « dev » plutôt que « jeu »**  
  Taper des commandes dans un faux terminal, c’est proche d’un outil de dev ou d’un tutoriel technique. Pour beaucoup (dont toi), ce n’est pas une fantasy de jeu, ni une expérience immédiatement plaisante.

- **Friction à l’entrée**  
  Il faut savoir *quoi* taper. Même avec « tape acte_1 », le joueur doit lire, comprendre, taper. Pas d’action en un clic, pas de monde à explorer visuellement en premier.

- **Identité floue**  
  Le jeu hésite entre : tutoriel de ligne de commande, histoire narrative, mini-jeux, monde explorable, profil/badges. Le terminal essaie de tout porter → surcharge et manque de clarté.

- **Peu de « game feel » immédiat**  
  Le feedback (flash, +XP, sons) est là, mais l’action de base reste « taper du texte ». Pas de mouvement, pas de choix visuels clairs, pas de découverte spatiale ou d’aventure évidente.

- **Maintenance et coût technique**  
  Beaucoup de logique (CommandHandlerV2, story_commands, basic_commands, etc.) et de scripts/CSS sont dédiés au terminal. Si le concept terminal ne plaît pas, tout ce cœur est mal investi.

En bref : **le terminal n’est pas un bon pilier central** pour une expérience que tu veux aimer. Il faut changer de pilier.

---

### 1.3 Autres points qui ne « plaisent » pas (audit large)

- **Trop de pages pour un concept flou**  
  Monde, Explorateur, Mail, Audio, Dashboard, Leaderboard, Skill tree, Tutoriels techniques… Sans une boucle de jeu claire, ça donne l’impression d’un portail avec des morceaux de jeu, pas d’un jeu unifié.

- **Narratif noyé dans les commandes**  
  Le récit (LUNA, actes, branches narratives) existe en données et en code, mais il est livré via « tape acte_2 », « tape acte_3 ». L’histoire ne se vit pas comme une aventure, mais comme une suite de commandes.

- **LUNA sous-exploitée**  
  LUNA (IA émotionnelle, couleurs, phrases) pourrait être le cœur d’une relation personnage/joueur. Aujourd’hui elle est surtout la « voix du terminal », pas le centre d’une expérience émotionnelle ou narrative claire.

- **Incohérences déjà documentées**  
  Aide qui dit « prologue / start_tutorial » alors que la bannière dit « acte_1 », deux flux (prologue vs acte_1), aide trop longue, terminal très chargé en scripts/CSS. Ça renforce l’impression de confusion.

- **Manque d’une boucle simple et satisfaisante**  
  Une bonne boucle serait : **une action claire → un résultat visible → une récompense ou une suite évidente**. Aujourd’hui la boucle est « taper une commande → lire une réponse → ne pas toujours savoir quoi faire ensuite », ce qui n’est ni simple ni très satisfaisant.

---

### 1.4 Synthèse de l’audit

| Aspect | Constat |
|--------|--------|
| **Concept central** | Terminal = mauvais fit pour le ressenti souhaité et pour une expérience « jeu » immédiate |
| **Identité** | Éclatée entre terminal, récit, mini-jeux, monde, profil ; pas de colonne vertébrale claire |
| **Premier contact** | Pas assez jouable ni visuel ; trop « outil » |
| **Narratif** | Présent mais livré par la commande, pas par l’aventure |
| **Technique** | Beaucoup d’investissement terminal/commandes ; à réorienter si on change de concept |

Conclusion : **il est cohérent de ne plus aimer l’idée du terminal et de vouloir revoir entièrement le concept.** La suite propose une nouvelle direction.

---

## Partie 2 — Nouveau concept : jeu sans terminal

L’idée est de **garder l’univers (Arkalia, LUNA, cybersécurité / aventure)** et la **stack technique (Flask, données, profils, récit)** en changeant **le cœur du gameplay** : plus de terminal comme pilier, une expérience centrée sur **choix, récit et/ou exploration visuelle**.

---

### 2.1 Principes du nouveau concept

1. **Plus de terminal comme cœur**  
   Les commandes type `acte_1` / `aide` ne sont plus le chemin principal. On peut les supprimer ou les garder en option « mode expert » caché, mais pas comme première expérience.

2. **Une boucle de jeu claire et courte**  
   Exemple : **voir une situation → faire un choix (clic / bouton) → voir la conséquence (texte + image/ambiance) → récompense ou prochaine étape**. Pas de saisie de commande pour avancer.

3. **LUNA au centre**  
   LUNA devient le personnage principal avec qui on interagit : dialogues, choix qui influencent la relation, récit qui avance par scènes et choix, pas par commandes.

4. **Une seule entrée évidente**  
   Après l’accueil : **un seul CTA principal** qui mène à l’aventure (ex. « Entrer dans l’histoire » ou « Rejoindre LUNA ») → une page ou un flux unique (histoire / monde / quête) comme colonne vertébrale.

5. **Réutilisation maximale**  
   Réutiliser : récits (actes, branches), données (badges, XP, niveaux), moteurs (gamification, émotions LUNA), pages existantes (Monde, Profil, etc.) en les **subordonnant** à la nouvelle boucle, pas au terminal.

---

### 2.2 Proposition : « Arkalia Quest — L’aventure de LUNA » (narratif + choix)

**En une phrase :**  
*Un jeu narratif par choix (type visual novel / aventure textuelle) où tu aides LUNA à sauver Arkalia en faisant des choix à l’écran ; la progression (XP, badges, niveaux) et le monde restent, mais plus besoin de taper des commandes.*

#### Boucle principale

1. **Accueil**  
   Message court de LUNA (« LUNA a besoin de toi. Notre monde est en danger. ») + **un seul bouton** : « Rejoindre LUNA » (ou « Commencer l’aventure »).

2. **Chapitre / Scène**  
   Une page « histoire » avec :
   - **Texte** (situation, dialogue LUNA, narration).
   - **Illustration ou fond** (CSS/image) pour l’ambiance.
   - **Choix** sous forme de **boutons** (2–4 par écran), ex. :
     - « Infiltrer le serveur en furtif »
     - « Attaquer frontalement »
     - « Demander l’aide d’Althea »
   Clic sur un choix → envoi au backend (ex. `POST /api/story/choice` avec `chapter_id` + `choice_id`) → réponse avec la suite (nouveau texte, prochaine scène, éventuellement mini-jeu ou redirection Monde).

3. **Progression**  
   Les mêmes données qu’aujourd’hui (profil, XP, niveaux, badges) sont mises à jour côté backend selon les choix et les chapitres complétés. **Aucune commande à taper** : tout se fait par clics.

4. **Monde / Profil / Leaderboard**  
   Restent des **écrans secondaires** : après un chapitre on peut « Explorer le monde », « Voir mon profil », « Classement ». Ils restent alimentés par la même gamification (XP, badges), mais ne sont plus le cœur.

5. **LUNA**  
   Chaque scène peut afficher l’émotion LUNA (couleur, phrase courte) calculée par le moteur existant ; les choix peuvent influencer la relation (données déjà en place dans les branches narratives).

#### Ce qu’on garde

- **Récit** : prologue, acte_1… acte_6, épilogue → transformés en **chapitres/scènes** avec boutons de choix au lieu de commandes.
- **Données** : `narrative_branches.json`, missions, badges, profils, progression.
- **Moteurs** : gamification, émotions LUNA, analytics (adaptés aux choix au lieu des commandes).
- **Pages** : Monde, Profil, Dashboard, Leaderboard, etc. en soutien.

#### Ce qu’on change ou retire

- **Terminal** : plus la page centrale ; soit supprimée, soit reléguée en « mode debug / expert ».
- **Commandes** : `acte_1`, `aide`, etc. ne sont plus le flux principal ; l’avancement se fait par **choix (boutons)** et **API histoire**.
- **Promesse** : remplacer par quelque chose comme : *« Aide LUNA à sauver Arkalia : fais des choix, vis l’histoire. »* (sans « terminal »).

---

### 2.3 Variante : monde / exploration comme cœur

Si tu préfères **moins de texte, plus d’exploration** :

- **Accueil** → « Entrer dans le monde ».
- **Page Monde** devient le cœur : carte ou grille de zones (déjà partiellement en place). Chaque zone est un **clic** qui ouvre une **scène** (situation + 2–3 choix) ou un **mini-jeu**.
- La progression (actes, récit) est **débloquée en explorant les zones** au lieu de taper des commandes. LUNA peut donner des indices à l’écran (« Va vers la zone X »).

Même idée : **plus de terminal**, une entrée unique (monde), et tout s’articule autour de **clic + choix**.

---

### 2.4 Étapes concrètes pour la révision

1. **Valider la direction**  
   Choisir : **narratif par choix** (section 2.2) ou **monde/exploration** (section 2.3), ou une combinaison (histoire principale par choix + monde pour side-quests).

2. **Définir la nouvelle promesse**  
   Une phrase courte sans le mot « terminal », ex. : *« Aide LUNA à sauver Arkalia : choisis ton chemin, vis l’aventure. »*

3. **Refonte de l’accueil**  
   Un message LUNA + **un seul CTA** vers la nouvelle entrée (histoire ou monde).

4. **Nouvelle « page cœur »**  
   - Soit une page **Histoire** (chapitres + choix + appels à une API type `POST /api/story/choice`).
   - Soit la page **Monde** enrichie (zones cliquables → scènes/choix ou mini-jeux).

5. **Adapter les données**  
   - Transformer les « commandes d’acte » en **étapes de chapitre** (acte_1 = chapitre 1, etc.).
   - Branches narratives déjà en JSON → mapper vers `chapter_id` + `choice_id` pour les boutons.

6. **Désactiver ou déplacer le terminal**  
   - Retirer le terminal du parcours principal (plus de lien « Terminal » en premier dans la nav, ou plus de CTA « Commencer l’aventure » vers le terminal).
   - Optionnel : garder une route `/terminal` en « mode expert » pour ne pas tout jeter d’un coup.

7. **Mettre à jour la doc**  
   README, STATUT_PROJET_ACTUEL, ARCHITECTURE_TECHNIQUE, COMPARAISON_JEUX_SOURCES_EXTERNES : nouvelle promesse, nouveau flux (accueil → histoire ou monde), plus de terminal comme cœur.

---

## Partie 3 — Résumé et prochaine action

- **Audit** : Le projet actuel est centré sur le terminal et des commandes ; l’identité est éclatée, le premier contact peu « jeu », et le récit est noyé dans la frappe. **Il est logique que ni l’idée du terminal ni le reste ne te plaisent** dans cet état.

- **Révision du concept** : **Abandonner le terminal comme pilier** et baser le jeu sur **choix à l’écran (boutons)** et **récit / exploration**, avec LUNA au centre. Deux options proposées : **(A) narratif par choix (visual novel light)** ou **(B) monde explorable comme cœur**. La stack (Flask, données, gamification, LUNA) est réutilisée.

- **Prochaine action recommandée** : Choisir A ou B (ou A+B), puis mettre à jour la promesse et l’accueil, et implémenter la première « page cœur » (histoire avec choix ou monde enrichi) en s’appuyant sur les données et moteurs existants.

Si tu me dis si tu penches plutôt **histoire/choix** ou **monde/exploration**, je peux détailler la prochaine étape (structure des chapitres, schéma d’API, ou modifications des templates/routes) en conséquence.

---

## Partie 4 — Implémentation réalisée (7 février 2026)

- **API** : `GET /api/story/state` (chapitre en cours + contenu), `POST /api/story/choice` (validation du chapitre, récompenses, chapitre suivant). Données dans `data/story_chapters.json` ; progression dans `progression_engine` (`story_chapters_completed`).
- **Page cœur** : `/histoire` (template `histoire.html`) — affichage du chapitre, bouton « Continuer », puis écran de fin avec liens Monde / Profil / Accueil.
- **Accueil** : CTA principal « Rejoindre LUNA » → `/histoire` ; promesse et textes LUNA mis à jour (sans terminal). Terminal en bouton secondaire « Mode expert ».
- **Navbar** : lien « 📖 AVENTURE » ajouté après Accueil ; Terminal conservé en secondaire.
- **Documentation** : README, STATUT_PROJET_ACTUEL, index.md mis à jour (nouvelle promesse, parcours Accueil → Aventure).
- **Profil** : `charger_profil()` injecte `missions_completed` depuis `story_chapters_completed` pour que la navbar affiche Monde/Profil/etc. après le premier chapitre complété.
