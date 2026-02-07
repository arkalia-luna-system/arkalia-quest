# 📋 Changelog - Arkalia Quest

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère à [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.0] - 2025-09-15

## [4.0.3] - 2026-02-07

### Visuel minimal unifié

- **Une seule feuille visuelle** : `static/css/arkalia-minimal.css` (fond `#0d1117`, accent bleu `#58a6ff`, texte lisible) remplace `arkalia-visual-2026.css` sur **toutes** les pages (accueil, histoire, terminal, monde, profil, dashboard, leaderboard, tutoriel, skill-tree, explorateur, mail, audio, accessibilité, tutoriels techniques).
- **Cohérence** : plus de conflits entre refonte 2026 (ambre/cyan) et thèmes Luna/Matrix ; rendu sobre et prévisible.
- **Documentation** : [docs/REPARTIR_SUR_DES_BASES_SANES.md](docs/REPARTIR_SUR_DES_BASES_SANES.md) (diagnostic, plan, questionnaire) ; STATUT, INDEX, REFONTE_VISUELLE_2026, CHEMIN_NULL_VERS_SUPER, POINT_PROJET_2026 mis à jour pour refléter le visuel minimal.

---

## [4.0.2] - 2026-02-07

### Amélioré (Jeu parfait — docs et cohérence)

- **Documentation** : [CHEMIN_NULL_VERS_SUPER.md](docs/CHEMIN_NULL_VERS_SUPER.md) ajouté à l’index ; parcours « null → super » et commandes Git pour push. [PLAYTEST_GUIDE_ADOS.md](docs/PLAYTEST_GUIDE_ADOS.md) aligné sur l’Aventure (Rejoindre LUNA, Continuer, premier chapitre) au lieu du terminal/acte_1. [AUDIT_ET_REVISION_CONCEPT.md](docs/AUDIT_ET_REVISION_CONCEPT.md) Partie 4 complétée (choix, choice_message, aide unifiée). [audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md](docs/audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md) « Prochaines étapes » et tableau « Il manque quoi » mis à jour (parcours Aventure, première session simple ✅). STATUT et COMPARAISON : cohérence navbar (Monde/Profil dès 1er chapitre complété).

### Amélioré (Refonte visuelle 2026)

- **Identité visuelle** : Nouvelle direction « Nuit émotionnelle » — fond bleu nuit (`#0a0e17`), ambre/corail pour LUNA et titres (`#e07c54`), cyan pour les actions (`#67d4e0`), typographie Outfit pour les titres. Fichier `static/css/arkalia-visual-2026.css` (design system + override des variables Luna/Matrix).
- **Pages** : Refonte appliquée à toutes les pages (accueil, aventure, monde, profil, dashboard, leaderboard, tutoriel, skill-tree, terminal, tutoriels techniques, accessibilité, audio, mail, explorateur). Navbar, CTA, bloc LUNA, barre de progression et boutons alignés sur le nouveau visuel.
- **Documentation** : [docs/REFONTE_VISUELLE_2026.md](docs/REFONTE_VISUELLE_2026.md) (audit, jeux de référence, plan et checklist), INDEX_DOCUMENTATION, index.md, README et STATUT mis à jour.

### Amélioré (Audit « pourquoi le jeu semble nul »)

- **Accueil** : CTA principal « Commencer l'aventure » renforcé (taille, bordure, ombre) ; boutons « Explorer le monde » et « Mon profil » en secondaire (classe `secondary`, moins mis en avant). Message LUNA déjà présent (« LUNA a besoin de toi »).
- **Commande aide** : Pour les joueurs intermédiaires, **acte_1** est maintenant en premier dans la liste des missions (aligné avec la bannière du terminal). Fallback statique du terminal : ajout d’un bloc « COMMENCE ICI : acte_1 » en tête de l’aide.
- **Terminal** : Tous les scripts chargés en **defer** pour ne plus bloquer le rendu → premier affichage et clics plus réactifs. Après succès du défi acte_1 (modal), appel à `refreshProgressionFromServer()` pour mettre à jour le bandeau Niveau/Score immédiatement.
- **États vides** : Leaderboard et profil (badges) affichent un message encourageant (« Joue au terminal, tape acte_1… pour apparaître ici / débloquer tes badges »). Composant badges : lien « Aller au terminal » et texte orienté acte_1.
- **Accessibilité (perfs)** : En mode `high-contrast-enhanced`, remplacement du sélecteur global `*` par des sélecteurs ciblés dans `accessibility.css` pour limiter le reflow (recommandation audit visuel).
- **Terminal – bundle CSS** : Les 16 feuilles CSS du terminal sont concaténées en un seul fichier `terminal-bundle.css` via `python scripts/build_terminal_css.py` ; la page terminal ne charge plus qu’une seule feuille.
- **Index – scripts en defer** : Tous les scripts de l’accueil (y compris ceux précédemment « critiques ») sont chargés en **defer** pour ne plus bloquer le parsing → premier affichage (FCP) plus rapide.
- **Terminal – preconnect** : `preconnect` vers Google Fonts pour un chargement plus rapide de la police.

### Références

- [docs/audits/AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md](docs/audits/AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md)
- [docs/AUDIT_VISUEL_ET_PERFORMANCES.md](docs/AUDIT_VISUEL_ET_PERFORMANCES.md)

---

## [4.0.1] - 2026-02-07

### Amélioré (Audit UX 2026)

- **Page d'accueil** : promesse en 15 mots affichée (« Tu es un hacker qui aide LUNA : missions au terminal, actes et mini-jeux »), micro-intro narrative (« LUNA a besoin de toi… »), CTA principal « Commencer l'aventure » mis en avant (classe `primary`). Accueil plus léger : chargement différé réduit à 4 scripts (performance, bug-fixes, audio, service-worker).
- **Terminal** : (1) Source de vérité unique : bandeau « Niveau X | Score Y » rechargé depuis `GET /api/profile/summary` au chargement et après chaque commande. (2) Feedback visuel unifié : flash vert (succès) ou rouge (échec) sur la zone de sortie. (3) Première mission : bannière « tape acte_1 » si acte_1 non complété ; page terminal reçoit `profil` (route `/terminal`). (4) Vrai gameplay acte_1 : après succès de la commande `acte_1`, modal « Défi — Choisis le bon code » (A/B/C) pour valider la mission.
- **Documentation** : README et STATUT mis à jour avec la promesse ; nouvel audit [docs/audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md](docs/audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md) ; [docs/PLAYTEST_GUIDE_ADOS.md](docs/PLAYTEST_GUIDE_ADOS.md) (guide playtest 15 min). INDEX_DOCUMENTATION et audits/README mis à jour.
- **Jeu parfait (suite)** : Navbar simplifiée (Accueil + Terminal + Tutoriel seulement) tant qu’acte_1 n’est pas complété ; code correct du défi acte_1 aléatoire (A, B ou C) ; son succès/échec sur le terminal (playSuccessSound / playErrorSound) ; index reçoit `profil` pour cohérence.
- **Fun & visuel (sources externes)** : Doc [docs/COMPARAISON_JEUX_SOURCES_EXTERNES.md](docs/COMPARAISON_JEUX_SOURCES_EXTERNES.md) (pourquoi le jeu peut sembler nul vs autres jeux, recherche 2024–2025). Accroche 30 s sur l’index (« Tu tapes des commandes, tu débloques des missions. C’est parti. »). CSS [static/css/game-feel.css](static/css/game-feel.css) : micro-interactions CTA principal (pulse, hover), bouton Exécuter terminal (hover/active), indicateur flottant succès (+XP ou ✓), cartes index plus réactives ; respect `prefers-reduced-motion` et focus visible. **Suite** : bouton « Ambiance » sur l’accueil (musique de fond optionnelle, préférence sauvegardée) ; messages d’erreur terminal amicaux (hint « Tape "aide" pour voir les commandes ») ; micro-célébration modal acte_1 (scale + glow) avant fermeture. **Suite** : bannière « Prochaine étape : tape acte_2 » (puis acte_3… epilogue) sur le terminal selon missions complétées, + mise à jour dynamique après défi acte_1.
- **Couverture game-feel sur toutes les pages** : `game-feel.css` chargé sur les 13 pages (accueil, terminal, monde, profil, dashboard, leaderboard, tutoriel, arbre de compétences, explorateur, mail, audio, accessibilité, tutoriels techniques). Sur chaque page : focus visible (boutons, liens, zones/input selon le contexte) et `prefers-reduced-motion` pour désactiver les animations de fond/particules. COMPARAISON : nouvelle section « Couverture des pages » (tableau récap) ; focus burger (menu mobile) dans game-feel.css.
- **Docs playtest & maintenance** : [PLAYTEST_GUIDE_ADOS.md](docs/PLAYTEST_GUIDE_ADOS.md) — checklist rapide avant session (accueil, terminal, acte_1, bannière acte_2). [COMPARAISON_JEUX_SOURCES_EXTERNES.md](docs/COMPARAISON_JEUX_SOURCES_EXTERNES.md) — template « Retours playtest du [date] » à coller dans STATUT ; tableau « Liens utiles » ; section « Référence code » (game-feel.css, audio-manager.js, terminal.html, app.py). STATUT : mention « Prêt pour playtests » + bannière acte_2→epilogue.

---

## [4.0.0] - 2025-09-16

### Ajouté

- API Terminal : `POST /api/terminal/command` (CommandHandlerV2), suggestions et messages « en développement ».
- Popups closables (X, overlay, Escape) via `popup-manager.js` / `popup-coordinator.js`.
- Smart Empty States : stats à zéro masquées, placeholders (`smart-empty-states.js` + CSS).
- Reward Feedback System : effets visuels/sonores (level-up, badges, missions, XP).
- Monde interactif : actions par zone (hack, minage, furtif, puzzle quantique) dans `world-interactions.js`.
- Visual Guidance, Tutorial Celebrations, mini-jeux jouables, Empty States, LUNA Enhanced, Daily Challenges, Terminal Commands Enhanced.

### Modifié

- Responsive : `responsive.css` remplacé par `arkalia-responsive.css` dans tous les templates.
- Démarrage dev : privilégier `python -m flask run`.

### Supprimé

- Fichiers redondants : `instant-feedback-system.js`, `luna_ai.py`, `luna_ai_v2.py` (engines/utils).

### Corrigé

- Sécurité endpoint terminal (validation IP).
- Erreurs JS : `addPersonalizedGreetings`, `undefined.length`, analytics int+str.
- Docs alignées avec l’implémentation.

## [3.2.0] - 2025-09-15

### Ajouté

- 🌙 LUNA AI V3 avec Machine Learning et mémoire à long terme
- 🎯 Système de défis quotidiens avec 6 types de défis
- 🎨 6 thèmes alternatifs (Matrix, Cyberpunk, Neon, Dark, Retro, Ocean)
- 📊 Endpoints API manquants (/api/performance/log, /api/tutorial/data)
- 🚀 Script de démarrage optimisé (start_optimized.sh)
- ⚡ Optimisations de performance (réduction 95% des appels API)

### Amélioré

- 🔧 Correction des erreurs JavaScript critiques
- 📈 Performance monitoring avec throttling
- 🛡️ Gestionnaires d'erreurs unifiés
- 🎮 Interface utilisateur optimisée

### Corrigé

- ❌ Erreur `addPersonalizedGreetings` manquante
- ❌ Erreur de lecture de propriété dans adaptive-guidance.js
- ❌ Gestionnaires d'erreurs dupliqués dans app.py
- ❌ Fuites de semaphore multiprocessing

## [3.1.0] - 2025-09-13

### Ajouté

- 🎮 Nouveau système de gamification avancée
- 🔒 Sécurité renforcée avec rate limiting
- 📊 Monitoring performance en temps réel
- 🧪 Suite de tests complète (179 tests)
- 🤖 Intégration IA LUNA pour recommandations

### Amélioré

- ⚡ Performance optimisée (<100ms response time)
- 🛡️ Architecture sécurisée (Bandit validation)
- 📱 Interface responsive mobile-first
- 🌐 Documentation multilingue

### Corrigé

- 🐛 Correction bugs authentification
- 🔧 Optimisation base de données
- 📝 Amélioration logs et monitoring

## [3.0.0] - 2025-06-01

### Ajouté

- 🏗️ Architecture Flask moderne
- 🔐 Système d'authentification complet
- 🎯 Missions et défis éducatifs
- 📊 Tableau de bord administrateur

### Modifié

- **BREAKING**: Migration Python 3.10+
- **BREAKING**: Nouvelle API REST
- 🔄 Refactoring complet du code base

## [2.0.0] - 2024-12-01

### Ajouté

- 🎮 Interface de jeu intuitive
- 🧠 Moteur IA pour adaptation difficulté
- 📚 Contenu éducatif cybersécurité

## [1.0.0] - 2024-09-01

### Ajouté

- 🌟 Version initiale d'Arkalia Quest
- 📖 Documentation de base
- ⚙️ Configuration CI/CD GitHub Actions

---

## Types de changements

- **Ajouté** pour les nouvelles fonctionnalités
- **Modifié** pour les modifications des fonctionnalités existantes  
- **Déprécié** pour les fonctionnalités qui seront supprimées prochainement
- **Supprimé** pour les fonctionnalités supprimées
- **Corrigé** pour les corrections de bugs
- **Sécurité** pour les améliorations de sécurité

## Liens

- [3.1.0]: https://github.com/arkalia-luna-system/arkalia-quest/compare/v3.0.0...v3.1.0
- [3.0.0]: https://github.com/arkalia-luna-system/arkalia-quest/compare/v2.0.0...v3.0.0
- [2.0.0]: https://github.com/arkalia-luna-system/arkalia-quest/compare/v1.0.0...v2.0.0
- [1.0.0]: https://github.com/arkalia-luna-system/arkalia-quest/releases/tag/v1.0.0

---

*Dernière révision : 7 février 2026*
