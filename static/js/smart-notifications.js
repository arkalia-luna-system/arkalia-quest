/**
 * Smart Notifications - Système de notifications intelligentes
 * Évite la répétition et contextualise les messages
 */

class SmartNotifications {
    constructor() {
        this.notificationHistory = JSON.parse(localStorage.getItem('arkalia_notifications') || '[]');
        this.lastNotificationTime = 0;
        this.minInterval = 30000; // 30 secondes minimum entre notifications
        this.maxHistory = 50;

        this.init();
    }

    init() {
        // Nettoyer l'historique ancien
        this.cleanOldHistory();
        console.log('✅ Smart Notifications initialisé');
    }

    cleanOldHistory() {
        const oneWeekAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
        this.notificationHistory = this.notificationHistory.filter(
            notif => notif.timestamp > oneWeekAgo
        );
        this.saveHistory();
    }

    shouldShowNotification(type, context = {}) {
        const now = Date.now();

        // Vérifier l'intervalle minimum
        if (now - this.lastNotificationTime < this.minInterval) {
            return false;
        }

        // Vérifier si cette notification a déjà été vue récemment
        const recentSimilar = this.notificationHistory.find(notif =>
            notif.type === type &&
            (now - notif.timestamp) < (5 * 60 * 1000) // 5 minutes
        );

        if (recentSimilar) {
            return false;
        }

        // Vérifier le contexte
        return this.checkContext(type, context);
    }

    checkContext(type, context) {
        switch (type) {
            case 'loading':
                return !context.isFirstLoad && context.hasRealChange;

            case 'profile_update':
                return context.hasRealChanges && !context.isAutomatic;

            case 'mission_available':
                return context.newMissionsCount > 0;

            case 'badge_unlock':
                return context.badgeId && !context.isSimulated;

            case 'level_up':
                return context.newLevel > context.oldLevel;

            default:
                return true;
        }
    }

    showNotification(type, message, options = {}) {
        if (!this.shouldShowNotification(type, options.context)) {
            return false;
        }

        // Enregistrer la notification
        this.recordNotification(type, message, options);

        // Afficher la notification
        this.displayNotification(message, options);

        // Mettre à jour le timestamp
        this.lastNotificationTime = Date.now();

        return true;
    }

    recordNotification(type, message, options) {
        const notification = {
            type,
            message,
            timestamp: Date.now(),
            context: options.context || {}
        };

        this.notificationHistory.push(notification);

        // Garder seulement les 50 dernières
        if (this.notificationHistory.length > this.maxHistory) {
            this.notificationHistory = this.notificationHistory.slice(-this.maxHistory);
        }

        this.saveHistory();
    }

    displayNotification(message, options = {}) {
        // Créer l'élément de notification
        const notification = document.createElement('div');
        notification.className = `smart-notification ${options.type || 'info'}`;
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">${options.icon || '🔔'}</div>
                <div class="notification-message">${message}</div>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Ajouter les styles si pas déjà présents
        this.addNotificationStyles();

        // Ajouter au DOM
        document.body.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Auto-suppression après 5 secondes
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.add('hide');
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, 300);
            }
        }, options.duration || 5000);
    }

    addNotificationStyles() {
        if (document.getElementById('smart-notifications-styles')) return;

        const style = document.createElement('style');
        style.id = 'smart-notifications-styles';
        style.textContent = `
            .smart-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.8));
                color: #fff;
                padding: 15px 20px;
                border-radius: 12px;
                border-left: 4px solid var(--success-color, #00ff00);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
                z-index: 10000;
                max-width: 350px;
                transform: translateX(100%);
                opacity: 0;
                transition: all 0.3s ease;
                font-family: 'Courier New', monospace;
            }

            .smart-notification.show {
                transform: translateX(0);
                opacity: 1;
            }

            .smart-notification.hide {
                transform: translateX(100%);
                opacity: 0;
            }

            .notification-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .notification-icon {
                font-size: 20px;
                flex-shrink: 0;
            }

            .notification-message {
                flex: 1;
                font-size: 14px;
                line-height: 1.4;
            }

            .notification-close {
                background: none;
                border: none;
                color: #fff;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background 0.2s ease;
            }

            .notification-close:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            .smart-notification.success {
                border-left-color: var(--success-color, #00ff00);
            }

            .smart-notification.warning {
                border-left-color: #ff8c00;
            }

            .smart-notification.info {
                border-left-color: #00bfff;
            }

            .smart-notification.error {
                border-left-color: #dc143c;
            }

            @media (max-width: 768px) {
                .smart-notification {
                    top: 10px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    saveHistory() {
        localStorage.setItem('arkalia_notifications', JSON.stringify(this.notificationHistory));
    }

    // Méthodes utilitaires
    showLoading(context = {}) {
        if (context.isFirstLoad) return;

        const messages = [
            "🔄 Mise à jour en cours...",
            "⚡ Synchronisation des données...",
            "🌐 Connexion au serveur...",
            "📡 Actualisation des informations..."
        ];

        const message = messages[Math.floor(Math.random() * messages.length)];
        return this.showNotification('loading', message, {
            type: 'info',
            icon: '🔄',
            context
        });
    }

    showProfileUpdate(context = {}) {
        if (!context.hasRealChanges) return;

        const messages = [
            "✨ Ton profil a été mis à jour !",
            "🎯 Nouvelles données synchronisées !",
            "📊 Statistiques actualisées !"
        ];

        const message = messages[Math.floor(Math.random() * messages.length)];
        return this.showNotification('profile_update', message, {
            type: 'success',
            icon: '✨',
            context
        });
    }

    showMissionAvailable(context = {}) {
        if (context.newMissionsCount <= 0) return;

        const message = `🎯 ${context.newMissionsCount} nouvelle(s) mission(s) disponible(s) !`;
        return this.showNotification('mission_available', message, {
            type: 'info',
            icon: '🎯',
            context
        });
    }

    showBadgeUnlock(context = {}) {
        if (!context.badgeId || context.isSimulated) return;

        const message = `🏆 Badge "${context.badgeName || 'Nouveau'}" débloqué !`;
        return this.showNotification('badge_unlock', message, {
            type: 'success',
            icon: '🏆',
            context
        });
    }

    showLevelUp(context = {}) {
        if (context.newLevel <= context.oldLevel) return;

        const message = `🎊 Niveau ${context.newLevel} atteint !`;
        return this.showNotification('level_up', message, {
            type: 'success',
            icon: '🎊',
            context
        });
    }
}

// Initialiser le système
window.smartNotifications = new SmartNotifications();

// Exporter pour utilisation globale
window.SmartNotifications = SmartNotifications;
