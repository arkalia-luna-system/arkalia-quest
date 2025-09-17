/**
 * Gestionnaire de notifications LUNA
 * Corrige les notifications redondantes et améliore l'expérience
 */

class LunaNotificationManager {
    constructor() {
        this.notificationHistory = new Map();
        this.lastNotificationTime = 0;
        this.notificationCooldown = 2000; // 2 secondes entre les notifications
        this.maxHistorySize = 50;
        this.duplicateThreshold = 3000; // 3 secondes pour considérer comme doublon

        this.init();
    }

    init() {
        // console.log('🌙 Initialisation du gestionnaire de notifications LUNA...');
        this.setupEventListeners();
        this.cleanupOldNotifications();
        // console.log('✅ Gestionnaire LUNA initialisé');
    }

    setupEventListeners() {
        // Intercepter les notifications LUNA
        document.addEventListener('arkalia:luna:notification', (e) => {
            this.handleLunaNotification(e.detail);
        });

        // Intercepter les notifications universelles
        document.addEventListener('arkalia:notification:show', (e) => {
            this.handleUniversalNotification(e.detail);
        });

        // Nettoyer les notifications anciennes
        setInterval(() => {
            this.cleanupOldNotifications();
        }, 30000); // Toutes les 30 secondes
    }

    handleLunaNotification(notification) {
        const {
            message,
            type = 'info',
            options = {},
            timestamp = Date.now()
        } = notification;

        // Vérifier si c'est un doublon
        if (this.isDuplicate(message, timestamp)) {
            // console.log('🚫 Notification LUNA dupliquée ignorée:', message);
            return;
        }

        // Vérifier le cooldown
        if (this.isInCooldown(timestamp)) {
            // console.log('⏳ Notification LUNA en cooldown:', message);
            return;
        }

        // Enregistrer la notification
        this.recordNotification(message, timestamp);

        // Afficher la notification
        this.showLunaNotification(message, type, options);
    }

    handleUniversalNotification(notification) {
        const {
            message,
            type = 'info',
            options = {},
            timestamp = Date.now()
        } = notification;

        // Vérifier si c'est une notification LUNA
        if (this.isLunaNotification(message)) {
            this.handleLunaNotification(notification);
            return;
        }

        // Traiter comme notification normale
        this.showUniversalNotification(message, type, options);
    }

    isDuplicate(message, timestamp) {
        const recentNotifications = Array.from(this.notificationHistory.values())
            .filter(notif => timestamp - notif.timestamp < this.duplicateThreshold);

        return recentNotifications.some(notif =>
            this.normalizeMessage(notif.message) === this.normalizeMessage(message)
        );
    }

    isInCooldown(timestamp) {
        return timestamp - this.lastNotificationTime < this.notificationCooldown;
    }

    isLunaNotification(message) {
        const lunaKeywords = [
            'luna', '🌙', 'ia', 'intelligence', 'artificielle',
            'système', 'analyse', 'recommandation', 'suggestion'
        ];

        const normalizedMessage = message.toLowerCase();
        return lunaKeywords.some(keyword => normalizedMessage.includes(keyword));
    }

    normalizeMessage(message) {
        return message
            .toLowerCase()
            .replace(/[^\w\s]/g, '') // Supprimer la ponctuation
            .replace(/\s+/g, ' ') // Normaliser les espaces
            .trim();
    }

    recordNotification(message, timestamp) {
        const id = this.generateId();
        this.notificationHistory.set(id, {
            message,
            timestamp,
            id
        });

        this.lastNotificationTime = timestamp;

        // Limiter la taille de l'historique
        if (this.notificationHistory.size > this.maxHistorySize) {
            const oldestId = this.notificationHistory.keys().next().value;
            this.notificationHistory.delete(oldestId);
        }
    }

    showLunaNotification(message, type, options) {
        // Utiliser le système de feedback universel si disponible
        if (window.universalFeedback) {
            window.universalFeedback.showFeedback(message, type, {
                ...options,
                icon: '🌙',
                className: 'luna-notification',
                animation: 'slideIn'
            });
        } else {
            // Fallback simple
            this.showSimpleNotification(message, type);
        }
    }

    showUniversalNotification(message, type, options) {
        if (window.universalFeedback) {
            window.universalFeedback.showFeedback(message, type, options);
        } else {
            this.showSimpleNotification(message, type);
        }
    }

    showSimpleNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        // Styles de base
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '10px 15px',
            borderRadius: '5px',
            color: 'white',
            zIndex: '10000',
            maxWidth: '300px',
            wordWrap: 'break-word'
        });

        // Couleurs par type
        const colors = {
            success: '#4CAF50',
            error: '#f44336',
            warning: '#ff9800',
            info: '#2196F3'
        };

        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);

        // Auto-remove après 5 secondes
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    cleanupOldNotifications() {
        const now = Date.now();
        const maxAge = 300000; // 5 minutes

        for (const [id, notification] of this.notificationHistory.entries()) {
            if (now - notification.timestamp > maxAge) {
                this.notificationHistory.delete(id);
            }
        }
    }

    generateId() {
        return 'luna_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Méthodes publiques
    clearHistory() {
        this.notificationHistory.clear();
        // console.log('🧹 Historique des notifications LUNA vidé');
    }

    getHistory() {
        return Array.from(this.notificationHistory.values());
    }

    getStats() {
        return {
            totalNotifications: this.notificationHistory.size,
            lastNotificationTime: this.lastNotificationTime,
            cooldownRemaining: Math.max(0, this.notificationCooldown - (Date.now() - this.lastNotificationTime))
        };
    }

    setCooldown(ms) {
        this.notificationCooldown = ms;
        // console.log(`⏱️ Cooldown LUNA défini à ${ms}ms`);
    }

    setDuplicateThreshold(ms) {
        this.duplicateThreshold = ms;
        // console.log(`🔍 Seuil de doublon LUNA défini à ${ms}ms`);
    }
}

// Initialiser le gestionnaire de notifications LUNA
window.lunaNotificationManager = new LunaNotificationManager();

// Exporter pour les modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LunaNotificationManager;
}
