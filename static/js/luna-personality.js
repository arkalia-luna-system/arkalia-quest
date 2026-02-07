/**
 * LUNA Personality - stub pour éviter 404 (profil.html).
 * Personnalité LUNA à étendre si besoin.
 */
(function () {
    'use strict';
    if (typeof window.LunaPersonality === 'undefined') {
        window.LunaPersonality = {
            init: function () {},
            getMood: function () { return 'neutral'; },
            getMessage: function () { return ''; }
        };
    }
})();
