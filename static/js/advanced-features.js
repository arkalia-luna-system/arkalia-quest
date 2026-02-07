/**
 * Advanced features - stub pour éviter 404 (profil, terminal, monde).
 * Fonctionnalités avancées optionnelles.
 */
(function () {
    'use strict';
    if (typeof window.AdvancedFeatures === 'undefined') {
        window.AdvancedFeatures = {
            init: function () {},
            isEnabled: function () { return false; }
        };
    }
})();
