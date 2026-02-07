/**
 * Visual feedback system - stub pour éviter 404 (profil, terminal, monde).
 * Affiche retours visuels (succès, erreur). À étendre si besoin.
 */
(function () {
    'use strict';
    if (typeof window.VisualFeedbackSystem === 'undefined') {
        window.VisualFeedbackSystem = {
            init: function () {},
            showSuccess: function () {},
            showError: function () {},
            showLevelUp: function () {}
        };
    }
    if (typeof window.visualFeedbackSystem === 'undefined') {
        window.visualFeedbackSystem = window.VisualFeedbackSystem;
    }
})();
