# Legacy JS (déprécié)

Ces modules sont conservés pour compatibilité historique/tests mais ne sont plus utilisés en production.

- adaptive-guidance.js → coachmarks désactivés
- visual-guidance.js → guidage visuel désactivé
- progression-feedback.js / universal-feedback.js → délèguent vers universal-notifications.js

Merci de ne plus référencer ces fichiers dans les templates. Utiliser à la place:
- universal-notifications.js (+ popup-manager.js)
- reward-feedback-system.js
- smart-empty-states.js
