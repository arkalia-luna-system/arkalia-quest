# Regroupement CSS / JS — Arkalia Quest

Ce document décrit les groupes de fichiers CSS et JS chargés par type de page, pour faciliter la maintenance et d’éventuels bundles.

## Pages « Luna » (dashboard, terminal, profil, leaderboard)

**CSS communs :**  
`arkalia-luna-vision.css`, `accessibility.css`, `arkalia-responsive.css`, `interface-improvements.css`, `empty-states.css`, `game-interface.css`, `mission-interface.css`, `reward-animations.css`, `loading-animations.css`, `progression-animations.css`, `adaptive-guidance.css`, `progression-feedback.css`, `competitive-system.css`, `creative-system.css`, `casual-system.css`.

**JS communs :**  
`navigation.js`, `audio-manager.js`, `effects.js`, `accessibility.js`, `game-engine.js`, `mission-system.js`, `luna-personality.js`, `personalized-messages.js`, `performance-ux-optimizer.js`, `bug-fixes.js`, `reward-system.js`, `system-integrator.js`, `adaptive-guidance.js`, `progression-feedback.js`, `competitive-system.js`, `creative-system.js`, `casual-system.js`.

## Page d’accueil (index)

En plus des styles de base (arkalia-core, arkalia-themes, arkalia-components, arkalia-responsive, accessibility), sont chargés : `smart-empty-states.css`, `interface-improvements.css`, `empty-states.css`, `reward-animations.css`, `loading-animations.css`, `progression-animations.css`, `adaptive-guidance.css`, `adaptive-ui.css`, `instant-feedback.css`, `interactive-zones.css`, `progression-feedback.css`, `casual-system.css`, `contextual-feedback.css`, `mini-games.css`, `animations-optimized.css`, `performance-optimized.css`, `audit-visual-fixes.css`, `theme-selection-enhanced.css`, `zone-exploration-enhanced.css`, `daily-missions-enhanced.css`, `motivational-empty-states.css`, `timer-challenges.css`, `interactive-puzzles.css`, `gameplay-integration.css`, `popup-manager.css`, `command-effects.css`.

## Terminal

Spécifiques : `contextual-feedback.css`, `command-effects.css`, `terminal-enhancements.js`, `terminal.js`, `hacking-effects.js`, `service-worker.js`, `educational_games.js`, `visual-effects.js`, `popup-manager.js`, `popup-coordinator.js`, `terminal-integration.js`, `daily-challenges-enhanced.js`, `mini-games-interactive.js`, `smart-empty-states.js`, `luna-enhanced.js`.

## Monde / Explorateur

Monde : `world-interactions.js`.  
Explorateur : seulement `audio-manager.js`, `navigation.js`.

## Skill tree

`skill-tree-enhancements.css`, `gamification-feedback.js`, `skill-tree-system.js`.

## Bundle disponible

- **static/css/arkalia-bundle-pages.css** : fichier unique qui `@import` les 15 CSS communs des pages Luna. Pour l’utiliser, remplacer dans un template les multiples `<link>` par un seul :  
  `<link rel="stylesheet" href="{{ url_for('static', filename='css/arkalia-bundle-pages.css') }}">`  
  (à tester page par page ; l’ordre des @import peut influencer le rendu.)

## Pistes supplémentaires

- **arkalia-bundle-core.js** : regrouper les JS communs (navigation, accessibility, effects, game-engine, etc.) pour réduire le nombre de requêtes.
- Les templates chargent encore les fichiers individuellement ; le bundle CSS peut être adopté progressivement.
