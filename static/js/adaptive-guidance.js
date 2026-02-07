// Stub : délègue vers universal-notifications si disponible (évite 404 si chargé)
window.adaptiveGuidance = window.adaptiveGuidance || {
    hint: function (message) {
        if (window.universalNotifications) {
            window.universalNotifications.info('Aide', message || '');
        }
    },
    show: function (title, content) {
        if (window.universalNotifications) {
            window.universalNotifications.info(title || 'Guide', content || '');
        }
    }
};
