// DÉLÉGATION: utilise universal-notifications si disponible
window.progressionFeedback = window.progressionFeedback || {
    step: function (title, content) {
        if (window.universalNotifications) {
            window.universalNotifications.info(title || 'Progression', content || 'Étape franchie');
        }
    },
    success: function (title, content) {
        if (window.universalNotifications) {
            window.universalNotifications.success(title || 'Succès', content || 'Bravo !');
        }
    }
};

