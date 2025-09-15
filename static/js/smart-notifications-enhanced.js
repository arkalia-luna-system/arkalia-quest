/* ===== ARKALIA QUEST - SMART NOTIFICATIONS ENHANCED ===== */

class SmartNotificationsEnhanced {
    constructor() {
        this.notifications = new Map();
        this.messageHistory = [];
        this.maxHistory = 50;
        this.cooldownPeriod = 5000; // 5 secondes entre messages similaires
        this.maxNotifications = 3;
        this.currentNotifications = 0;

        this.messageVariations = {
            'profile_updated': [
                'Profil mis à jour avec succès',
                'Modifications sauvegardées',
                'Profil synchronisé',
                'Données actualisées'
            ],
            'mission_completed': [
                'Mission accomplie !',
                'Excellent travail !',
                'Mission terminée avec succès',
                'Bravo pour cette réussite !'
            ],
            'badge_earned': [
                'Nouveau badge débloqué !',
                'Félicitations pour ce badge !',
                'Badge obtenu avec succès',
                'Nouvelle récompense !'
            ],
            'level_up': [
                'Niveau supérieur atteint !',
                'Félicitations, vous montez de niveau !',
                'Progression remarquable !',
                'Nouveau niveau débloqué !'
            ],
            'loading': [
                'Chargement en cours...',
                'Synchronisation des données...',
                'Mise à jour en cours...',
                'Traitement en cours...'
            ],
            'pause_well_deserved': [
                'Pause bien méritée !',
                'Prenez le temps de vous reposer',
                'Moment de détente apprécié',
                'Pause rafraîchissante !'
            ],
            'luna_waiting': [
                'LUNA vous attend avec impatience',
                'LUNA est prête pour vous',
                'LUNA vous attend patiemment',
                'LUNA est là pour vous'
            ]
        };

        this.init();
    }

    init() {
        this.createNotificationContainer();
        this.setupEventListeners();
        console.log('🔔 Smart Notifications Enhanced initialisé');
    }

    createNotificationContainer() {
        if (document.getElementById('smart-notifications-container')) return;

        const container = document.createElement('div');
        container.id = 'smart-notifications-container';
        container.className = 'smart-notifications-container';
        container.innerHTML = `
            <style>
                .smart-notifications-container {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 10000;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    max-width: 400px;
                    pointer-events: none;
                }
                
                .smart-notification {
                    background: rgba(0, 0, 0, 0.9);
                    border: 1px solid rgba(0, 255, 0, 0.3);
                    border-radius: 12px;
                    padding: 16px 20px;
                    color: white;
                    font-size: 14px;
                    line-height: 1.4;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    backdrop-filter: blur(20px);
                    transform: translateX(100%);
                    opacity: 0;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    pointer-events: auto;
                    position: relative;
                    overflow: hidden;
                }
                
                .smart-notification.show {
                    transform: translateX(0);
                    opacity: 1;
                }
                
                .smart-notification.hide {
                    transform: translateX(100%);
                    opacity: 0;
                }
                
                .smart-notification::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, #00ff00, #00ffff);
                    border-radius: 12px 12px 0 0;
                }
                
                .smart-notification-header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 8px;
                }
                
                .smart-notification-icon {
                    font-size: 18px;
                    margin-right: 8px;
                }
                
                .smart-notification-title {
                    font-weight: 600;
                    color: #00ff00;
                    flex: 1;
                }
                
                .smart-notification-close {
                    background: none;
                    border: none;
                    color: rgba(255, 255, 255, 0.6);
                    cursor: pointer;
                    font-size: 16px;
                    padding: 4px;
                    border-radius: 4px;
                    transition: all 0.2s ease;
                }
                
                .smart-notification-close:hover {
                    color: white;
                    background: rgba(255, 255, 255, 0.1);
                }
                
                .smart-notification-message {
                    color: rgba(255, 255, 255, 0.9);
                    margin: 0;
                }
                
                .smart-notification-progress {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    height: 2px;
                    background: linear-gradient(90deg, #00ff00, #00ffff);
                    border-radius: 0 0 12px 12px;
                    animation: progressBar 4s linear forwards;
                }
                
                @keyframes progressBar {
                    from { width: 100%; }
                    to { width: 0%; }
                }
                
                .smart-notification.success {
                    border-color: rgba(0, 255, 0, 0.5);
                }
                
                .smart-notification.warning {
                    border-color: rgba(255, 193, 7, 0.5);
                }
                
                .smart-notification.error {
                    border-color: rgba(220, 53, 69, 0.5);
                }
                
                .smart-notification.info {
                    border-color: rgba(0, 191, 255, 0.5);
                }
                
                @media (max-width: 768px) {
                    .smart-notifications-container {
                        top: 10px;
                        right: 10px;
                        left: 10px;
                        max-width: none;
                    }
                }
            </style>
        `;

        document.body.appendChild(container);
    }

    setupEventListeners() {
        // Intercepter les messages de LUNA
        if (window.lunaEnhanced) {
            const originalShowMessage = window.lunaEnhanced.showMessage;
            window.lunaEnhanced.showMessage = (message, duration = 3000) => {
                this.showSmartNotification(message, 'info', duration);
            };
        }

        // Intercepter les messages de progression
        if (window.rewardAnimations) {
            const originalShowLevelUp = window.rewardAnimations.showLevelUp;
            window.rewardAnimations.showLevelUp = (level) => {
                this.showSmartNotification(`Niveau ${level} atteint !`, 'success', 4000);
            };
        }
    }

    showSmartNotification(message, type = 'info', duration = 4000) {
        // Vérifier si le message est en cooldown
        if (this.isInCooldown(message)) {
            return;
        }

        // Limiter le nombre de notifications simultanées
        if (this.currentNotifications >= this.maxNotifications) {
            this.removeOldestNotification();
        }

        // Varier le message si possible
        const variedMessage = this.getVariedMessage(message, type);

        // Créer la notification
        const notification = this.createNotification(variedMessage, type, duration);

        // L'afficher
        this.displayNotification(notification);

        // L'enregistrer dans l'historique
        this.recordMessage(message, type);
    }

    isInCooldown(message) {
        const now = Date.now();
        const messageKey = this.getMessageKey(message);

        if (this.messageHistory.has(messageKey)) {
            const lastShown = this.messageHistory.get(messageKey);
            return (now - lastShown) < this.cooldownPeriod;
        }

        return false;
    }

    getMessageKey(message) {
        // Créer une clé basée sur le type de message plutôt que le contenu exact
        if (message.includes('profil') || message.includes('Profil')) return 'profile_updated';
        if (message.includes('mission') || message.includes('Mission')) return 'mission_completed';
        if (message.includes('badge') || message.includes('Badge')) return 'badge_earned';
        if (message.includes('niveau') || message.includes('Niveau')) return 'level_up';
        if (message.includes('pause') || message.includes('Pause')) return 'pause_well_deserved';
        if (message.includes('LUNA') || message.includes('luna')) return 'luna_waiting';
        if (message.includes('chargement') || message.includes('Chargement')) return 'loading';

        return message.toLowerCase().replace(/[^a-z0-9]/g, '');
    }

    getVariedMessage(message, type) {
        const messageKey = this.getMessageKey(message);

        if (this.messageVariations[messageKey]) {
            const variations = this.messageVariations[messageKey];
            const randomIndex = Math.floor(Math.random() * variations.length);
            return variations[randomIndex];
        }

        return message;
    }

    createNotification(message, type, duration) {
        const notification = document.createElement('div');
        notification.className = `smart-notification ${type}`;

        const icon = this.getIconForType(type);
        const id = 'notification-' + Date.now();

        notification.innerHTML = `
            <div class="smart-notification-header">
                <div style="display: flex; align-items: center;">
                    <span class="smart-notification-icon">${icon}</span>
                    <span class="smart-notification-title">${this.getTitleForType(type)}</span>
                </div>
                <button class="smart-notification-close" onclick="window.smartNotifications.removeNotification('${id}')">×</button>
            </div>
            <p class="smart-notification-message">${message}</p>
            <div class="smart-notification-progress"></div>
        `;

        notification.id = id;
        notification.dataset.type = type;
        notification.dataset.message = message;

        return notification;
    }

    getIconForType(type) {
        const icons = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️'
        };
        return icons[type] || 'ℹ️';
    }

    getTitleForType(type) {
        const titles = {
            'success': 'Succès',
            'warning': 'Attention',
            'error': 'Erreur',
            'info': 'Information'
        };
        return titles[type] || 'Notification';
    }

    displayNotification(notification) {
        const container = document.getElementById('smart-notifications-container');
        container.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        this.currentNotifications++;

        // Auto-suppression
        const duration = parseInt(notification.dataset.duration) || 4000;
        setTimeout(() => {
            this.removeNotification(notification.id);
        }, duration);
    }

    removeNotification(id) {
        const notification = document.getElementById(id);
        if (!notification) return;

        notification.classList.add('hide');

        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            this.currentNotifications = Math.max(0, this.currentNotifications - 1);
        }, 400);
    }

    removeOldestNotification() {
        const container = document.getElementById('smart-notifications-container');
        const notifications = container.querySelectorAll('.smart-notification');

        if (notifications.length > 0) {
            this.removeNotification(notifications[0].id);
        }
    }

    recordMessage(message, type) {
        const messageKey = this.getMessageKey(message);
        this.messageHistory.set(messageKey, Date.now());

        // Nettoyer l'historique si nécessaire
        if (this.messageHistory.size > this.maxHistory) {
            const oldestKey = this.messageHistory.keys().next().value;
            this.messageHistory.delete(oldestKey);
        }
    }

    // Méthodes publiques
    showSuccess(message, duration = 4000) {
        this.showSmartNotification(message, 'success', duration);
    }

    showWarning(message, duration = 5000) {
        this.showSmartNotification(message, 'warning', duration);
    }

    showError(message, duration = 6000) {
        this.showSmartNotification(message, 'error', duration);
    }

    showInfo(message, duration = 4000) {
        this.showSmartNotification(message, 'info', duration);
    }

    clearAll() {
        const container = document.getElementById('smart-notifications-container');
        if (container) {
            container.innerHTML = '';
            this.currentNotifications = 0;
        }
    }

    // Méthode pour désactiver temporairement les notifications
    disable(duration = 30000) {
        this.disabled = true;
        setTimeout(() => {
            this.disabled = false;
        }, duration);
    }

    enable() {
        this.disabled = false;
    }
}

// Initialiser le système
window.smartNotifications = new SmartNotificationsEnhanced();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SmartNotificationsEnhanced;
}
