# Validation visuelle et clics – Arkalia Quest

Checklist pour valider étape par étape que chaque visuel est correct et que chaque clic fonctionne.

## Corrections déjà appliquées

- **Favicons** : Les références aux icônes manquantes (32×32, 16×16) pointent maintenant vers `icon-192x192.png` (templates + `static/css/accessibility.css` + `static/manifest.json`). Plus de 404 sur les favicons.
- **Terminal** : Les commandes saisies par l’utilisateur sont échappées avant affichage (`escapeHtml`) pour éviter les injections HTML/XSS (user-message, command-line, message « Commande non reconnue »).
- **Tests pytest** : Les fichiers macOS `._*` sont exclus de la collecte (`--ignore-glob=**/._*` dans `pyproject.toml`) pour éviter les erreurs d’import.
- **JS manquants** : `static/js/competitive-system.js` et `static/js/creative-system.js` ont été créés en stubs (compatibilité) pour supprimer les 404 sur les pages qui les chargent (terminal, monde, profil, dashboard, leaderboard).
- **Sécurité / erreurs courantes jeu** :
  - **eval() supprimé** : Dans `terminal.js`, les commandes `calc`/`calculate` utilisaient `eval()`. Remplacé par un parser mathématique sécurisé `safeMathEval()` (chiffres et opérateurs uniquement).
  - **XSS** : Données dynamiques échappées avant affichage dans : `luna-enhanced.js` (réponse LUNA), `game-engine.js` (messages terminal), `unified-progression-sync.js` et `progression-sync.js` (badges), `explorateur.html` (contenu JSON), `terminal.html` (réponses API `result.message` / `result.error`), `profil.html` (badges, timeline), `mail.html` (expéditeur, sujet, aperçu), `theme-manager.js` (noms de thèmes).
  - **Null / robustesse** : Vérifications `message != null` et échappement dans `personalized-messages.js` et `luna-enhanced.js`.
- **Erreurs « jeu null » / plantages** :
  - **skill_tree.html** : `skillTreeSystem.init()` remplacé par `window.skillTreeSystem.init()` pour éviter ReferenceError si le script est en mode strict ou ordre de chargement différent.
  - **unified-progression-sync.js** : gardes `if (!playerData || typeof playerData !== 'object') return` dans `updateUI`, `updateStats` et `updateProgressBars` pour éviter les accès sur null/undefined.
  - **leaderboard.html** : vérification que `card.querySelector('.challenge-name')` existe avant d’utiliser `.textContent`.
  - **monde.html** : vérification que `zone.querySelector('.zone-name')` existe avant d’utiliser `.textContent`.
  - **skill-tree-system.js** : utilisation de `skill ? skill.name : skillId` dans la notification d’upgrade pour éviter l’accès à `skill.name` quand `skill` est undefined.
  - **profil.html / dashboard.html** : vérification `response.ok` et `data` valide avant d’utiliser la réponse des APIs de fallback.
  - **technical_tutorials.html** : acceptation des réponses API en tableau ou en objet `{ tutorials: [...] }`.
- **Accès DOM sans garde (éviter plantages)** :
  - **theme-manager.js** : vérification que `theme-select` existe avant d’y attacher l’écouteur.
  - **reward-system.js** : vérification que `reward-notifications` existe avant appendChild.
  - **game-engine.js** : vérification que `modal.querySelector('.game-content')` existe avant innerHTML.
  - **zone-exploration-enhanced.js** : vérification que `game-score` et `game-time` existent avant de mettre à jour (4 mini-jeux).
  - **world-interactions.js** : gardes pour `.world-title`, `.world-subtitle`, `zone-details`, `mission-list`, `world-map`, `player-position`, `modal-content`, `modal-actions`, `btn-start`, `btn-cancel` ; garde pour `zone` et `zone.missions_list` dans updateZoneInfo/updateMissions.
  - **tutorial.js** : garde pour `modal` et tous les sous-éléments (tutorial-icon, title, description, nextBtn, progress) avant affectation.
  - **zone-interactive-challenges.js** : gardes pour `close-modal`, `close-challenge`, `cancel-challenge`, `submit-challenge` avant addEventListener.
- **JSON.parse sans try/catch (localStorage corrompu)** :
  - **accessibility.js** : `loadSettings()` retourne un objet par défaut en cas d’erreur de parse.
  - **system-integrator.js** : `loadSystemState()` encapsulé dans try/catch.
  - **mission-system.js** : `loadMissionProgress()` encapsulé dans try/catch.
  - **interactive-puzzles.js** : `loadPuzzleHistory()` encapsulé dans try/catch.
  - **universal-feedback.js** : `loadSettings()` encapsulé dans try/catch.
- **Autres gardes** :
  - **game-engine.js** : `startGameSession` vérifie que `#game-start`, `#game-quit`, `#game-content` existent ; `showQuestion` vérifie `container`, `game.questions`, et `question` avant d’écrire le HTML.
  - **sticky-progress-bar.js** : vérification de `this.element` et de `.toggle-icon` dans `toggle()`, `show()`, `hide()`.

---

## Checklist manuelle (à exécuter dans le navigateur)

### 1. Accueil (`/`)
- [ ] Page s’affiche correctement (titres, visuels, CTA).
- [ ] Liens de la navbar : Accueil, Terminal, Monde, Profil, Dashboard, Classement, Arbre de compétences, Tutoriel, Tutoriels techniques.
- [ ] Clic sur chaque lien → bonne page.
- [ ] Skip-links (passer au contenu, navigation, accessibilité) ciblent les bons blocs.
- [ ] Menu burger (mobile) : ouverture/fermeture, liens cliquables.

### 2. Terminal (`/terminal`)
- [ ] Interface terminal visible (prompt, zone de commandes, messages).
- [ ] Saisie + Entrée ou bouton d’envoi → commande affichée et réponse (ex. `help`, `profil`, `monde`).
- [ ] Boutons de commande rapide (si présents) déclenchent bien la commande.
- [ ] Pas d’erreur console, pas de 404 (favicon, CSS, JS).

### 3. Monde (`/monde`)
- [ ] Carte / monde s’affiche.
- [ ] Éléments cliquables (zones, boutons) réagissent.

### 4. Profil (`/profil`)
- [ ] Profil utilisateur affiché (ou état non connecté cohérent).
- [ ] Liens et boutons fonctionnels.

### 5. Dashboard (`/dashboard`)
- [ ] Tableau de bord chargé (stats, missions, etc.).
- [ ] Clics sur les widgets/liens → comportement attendu.

### 6. Classement (`/leaderboard`)
- [ ] Classement affiché.
- [ ] Filtres ou onglets (si présents) réactifs.

### 7. Arbre de compétences (`/skill-tree`)
- [ ] Page charge sans erreur.
- [ ] `skillTreeSystem.init()` exécuté (pas d’erreur dans la console).
- [ ] Nœuds / branches interactifs si prévus.

### 8. Tutoriel (`/tutorial`)
- [ ] Page tutoriel (welcome ou étapes) affichée.
- [ ] Boutons « Suivant » / « Commencer » etc. fonctionnent.

### 9. Tutoriels techniques (`/technical-tutorials`)
- [ ] Liste des tutoriels chargée (appel API `/api/technical-tutorials/available`).
- [ ] Clic sur un tutoriel → détail ou ouverture correcte.

### 10. Accessibilité
- [ ] Bouton « Accessibilité » (ou équivalent) ouvre le panneau.
- [ ] Panneau : options (thème, taille, etc.) modifiables.
- [ ] Boutons « Sauvegarder » et « Réinitialiser » fonctionnent.
- [ ] Fermeture : bouton fermer, touche Escape, clic overlay.
- [ ] Préférences persistantes (rechargement de page).

### 11. Navigation globale
- [ ] Navbar : page active soulignée / mise en évidence selon la route.
- [ ] Footer (si présent) : liens valides.
- [ ] Aucun lien cassé (404) sur les pages parcourues.

---

## Tests recommandés

- **Desktop** : Chrome, Firefox ou Safari.
- **Mobile** : vue responsive + menu burger.
- **Console** : pas d’erreurs JavaScript, pas de 404 sur les ressources (images, CSS, JS, favicons).

Si un élément ne s’affiche pas ou un clic ne fait rien, vérifier la console (F12) et les onglets Network / Réseau pour identifier l’erreur (fichier manquant, API, JS).
