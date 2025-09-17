/* ===== ARKALIA QUEST - UNIVERSAL NOTIFICATIONS SYSTEM ===== */
/* Système unifié pour toutes les notifications, feedbacks et états vides */

class UniversalNotifications {
    constructor() {
        this.notifications = new Map();
        this.queue = [];
        this.isProcessing = false;
        this.recentNotifications = new Map(); // anti-spam/déduplication
        this.settings = this.loadSettings();
        this.init();
    }

    init() {
        this.setupGlobalStyles();
        this.setupEventListeners();
        this.setupAccessibility();
        console.log('🔔 Universal Notifications System initialisé');
    }

    loadSettings() {
        const defaultSettings = {
            maxNotifications: 2,        // Réduit pour éviter le spam
            defaultDuration: 3000,      // Durée optimale
            position: 'bottom-right',
            theme: 'arkalia',
            animations: true,
            sound: false,
            vibration: false,
            rateLimitMs: 5000,          // Augmenté pour réduire le spam
            dedupeWindowMs: 10000,      // Augmenté pour mieux dédupliquer
            autoClose: true,            // Nouveau: fermeture automatique
            dismissible: true,          // Nouveau: toutes les notifications sont dismissibles
            groupSimilar: true,         // Nouveau: grouper les notifications similaires
            maxGroupSize: 3,            // Réduit pour éviter l'encombrement
            smartFiltering: true,       // Nouveau: filtrage intelligent
            priorityOnly: false,        // Nouveau: afficher seulement les prioritaires
            minImportance: 1            // Nouveau: importance minimale (1-5)
        };

        try {
            const saved = localStorage.getItem('arkalia_notifications_settings');
            return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
        } catch {
            return defaultSettings;
        }
    }

    setupGlobalStyles() {
        if (document.getElementById('universal-notifications-styles')) return;

        const style = document.createElement('style');
        style.id = 'universal-notifications-styles';
        style.textContent = `
            .universal-notifications-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 400px;
                pointer-events: none;
            }

            .universal-notification {
                background: rgba(9, 9, 11, 0.95);
                border: 2px solid rgba(167, 139, 250, 0.5);
                border-radius: 12px;
                padding: 16px 20px;
                color: var(--argent-holographique);
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.95em;
                line-height: 1.4;
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                transform: translateX(100%);
                opacity: 0;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                pointer-events: auto;
                position: relative;
                overflow: hidden;
            }

            .universal-notification.show {
                transform: translateX(0);
                opacity: 1;
            }

            .universal-notification.hide {
                transform: translateX(100%);
                opacity: 0;
            }

            .universal-notification::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
            }

            .universal-notification.success::before {
                background: linear-gradient(90deg, #22c55e, #16a34a);
            }

            .universal-notification.warning::before {
                background: linear-gradient(90deg, #f59e0b, #d97706);
            }

            .universal-notification.error::before {
                background: linear-gradient(90deg, #ef4444, #dc2626);
            }

            .universal-notification.info::before {
                background: linear-gradient(90deg, var(--bleu-spectre), #3b82f6);
            }

            .universal-notification-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 8px;
            }

            .universal-notification-icon {
                font-size: 1.2em;
                margin-right: 8px;
            }

            .universal-notification-title {
                font-weight: 600;
                color: var(--violet-lunaire);
                flex: 1;
            }

            .universal-notification-close {
                background: none;
                border: none;
                color: var(--argent-holographique);
                font-size: 1.2em;
                cursor: pointer;
                padding: 4px;
                border-radius: 4px;
                transition: all 0.2s ease;
                opacity: 0.7;
            }

            .universal-notification-close:hover {
                opacity: 1;
                background: rgba(167, 139, 250, 0.2);
                color: var(--violet-lunaire);
            }

            .universal-notification-content {
                margin-bottom: 8px;
            }

            .universal-notification-actions {
                display: flex;
                gap: 8px;
                margin-top: 12px;
            }

            .universal-notification-btn {
                padding: 6px 12px;
                border: 1px solid rgba(167, 139, 250, 0.3);
                border-radius: 6px;
                background: rgba(167, 139, 250, 0.1);
                color: var(--argent-holographique);
                font-size: 0.85em;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .universal-notification-btn:hover {
                background: rgba(167, 139, 250, 0.3);
                border-color: var(--violet-lunaire);
            }

            .universal-notification-btn.primary {
                background: var(--violet-lunaire);
                color: #000;
                border-color: var(--violet-lunaire);
            }

            .universal-notification-btn.primary:hover {
                background: var(--bleu-spectre);
                border-color: var(--bleu-spectre);
            }

            .universal-notification-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 2px;
                background: var(--violet-lunaire);
                transition: width linear;
            }

            /* Animations */
            @keyframes notificationSlideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes notificationSlideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }

            @keyframes notificationPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }

            .universal-notification.pulse {
                animation: notificationPulse 0.6s ease-in-out;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .universal-notifications-container {
                    top: 10px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }

                .universal-notification {
                    font-size: 0.9em;
                    padding: 14px 16px;
                }
            }

            /* Thèmes */
            .universal-notification.matrix {
                border-color: rgba(0, 255, 0, 0.5);
                background: rgba(0, 0, 0, 0.9);
            }

            .universal-notification.matrix::before {
                background: linear-gradient(90deg, #00ff00, #00ffff);
            }

            .universal-notification.cyberpunk {
                border-color: rgba(255, 0, 255, 0.5);
                background: rgba(20, 0, 40, 0.95);
            }

            .universal-notification.cyberpunk::before {
                background: linear-gradient(90deg, #ff00ff, #00ffff);
            }
        `;
        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Gérer les clics sur l'overlay pour fermer les notifications
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('universal-notification')) {
                this.closeNotification(e.target.dataset.id);
            }
        });

        // Gérer les touches clavier
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllNotifications();
            }
        });
    }

    setupAccessibility() {
        // Ajouter les attributs ARIA pour l'accessibilité
        const container = this.getContainer();
        container.setAttribute('role', 'region');
        container.setAttribute('aria-label', 'Notifications');
        container.setAttribute('aria-live', 'polite');
    }

    getContainer() {
        let container = document.getElementById('universal-notifications-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'universal-notifications-container';
            container.className = 'universal-notifications-container';

            // Ajouter un bouton "Fermer toutes les notifications"
            const closeAllBtn = document.createElement('button');
            closeAllBtn.id = 'close-all-notifications';
            closeAllBtn.className = 'close-all-notifications-btn';
            closeAllBtn.innerHTML = '❌ Fermer toutes';
            closeAllBtn.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 10001;
                background: rgba(239, 68, 68, 0.9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 0.8em;
                cursor: pointer;
                display: none;
                backdrop-filter: blur(10px);
            `;
            closeAllBtn.addEventListener('click', () => this.closeAllNotifications());

            document.body.appendChild(container);
            document.body.appendChild(closeAllBtn);
        }
        return container;
    }

    // Méthodes principales
    show(config) {
        const notificationConfig = {
            id: config.id || `notification_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type: config.type || 'info',
            title: config.title || '',
            content: config.content || '',
            duration: config.duration || this.settings.defaultDuration,
            closable: config.closable !== false,
            actions: config.actions || [],
            theme: config.theme || this.settings.theme,
            priority: config.priority || 'normal',
            importance: config.importance || 1,
            onClose: config.onClose || null,
            onClick: config.onClick || null,
            ...config
        };

        // Filtrage intelligent
        if (this.settings.smartFiltering && !this.shouldShowNotification(notificationConfig)) {
            return notificationConfig.id;
        }

        // Anti-spam / déduplication amélioré
        const now = Date.now();
        const rateKey = this.getRateKey(notificationConfig);
        if (this.isRateLimited(rateKey, now)) {
            // Au lieu d'ignorer, grouper avec la notification existante
            if (this.settings.groupSimilar) {
                this.groupWithExisting(notificationConfig, rateKey);
            }
            return notificationConfig.id;
        }
        this.recentNotifications.set(rateKey, now);
        this.pruneRecent(now);

        // Vérifier la limite de notifications
        if (this.notifications.size >= this.settings.maxNotifications) {
            this.queue.push(notificationConfig);
            return notificationConfig.id;
        }

        return this.createNotification(notificationConfig);
    }

    getRateKey(config) {
        // Clé basée sur type + titre + début du contenu
        const contentSnippet = (config.content || '').toString().slice(0, 120);
        return `${config.type}|${config.title}|${contentSnippet}`;
    }

    isRateLimited(key, now) {
        const last = this.recentNotifications.get(key);
        if (last == null) return false;
        return (now - last) < (this.settings.rateLimitMs || 1500);
    }

    pruneRecent(now) {
        const windowMs = this.settings.dedupeWindowMs || 3000;
        for (const [key, ts] of this.recentNotifications.entries()) {
            if (now - ts > windowMs) this.recentNotifications.delete(key);
        }
    }

    // Nouvelle méthode pour grouper les notifications similaires
    groupWithExisting(newConfig, rateKey) {
        // Trouver la notification existante avec la même clé
        for (const [id, notification] of this.notifications.entries()) {
            const existingKey = this.getRateKey(notification.config);
            if (existingKey === rateKey) {
                // Incrémenter le compteur de groupe
                if (!notification.config.groupCount) {
                    notification.config.groupCount = 1;
                }
                notification.config.groupCount++;

                // Mettre à jour l'affichage
                this.updateGroupedNotification(notification);

                // Réinitialiser le timer
                this.resetNotificationTimer(id);
                break;
            }
        }
    }

    updateGroupedNotification(notification) {
        const titleElement = notification.element.querySelector('.universal-notification-title');
        if (titleElement && notification.config.groupCount > 1) {
            const originalTitle = notification.config.title.replace(/ \(\d+\)$/, '');
            titleElement.textContent = `${originalTitle} (${notification.config.groupCount})`;
        }
    }

    resetNotificationTimer(id) {
        // Annuler le timer existant
        const notification = this.notifications.get(id);
        if (notification && notification.timeoutId) {
            clearTimeout(notification.timeoutId);
        }

        // Redémarrer le timer
        if (notification && notification.config.duration > 0) {
            notification.timeoutId = setTimeout(() => {
                this.closeNotification(id);
            }, notification.config.duration);
        }
    }

    updateCloseAllButton() {
        const closeAllBtn = document.getElementById('close-all-notifications');
        if (closeAllBtn) {
            if (this.notifications.size > 0) {
                closeAllBtn.style.display = 'block';
                closeAllBtn.textContent = `❌ Fermer toutes (${this.notifications.size})`;
            } else {
                closeAllBtn.style.display = 'none';
            }
        }
    }

    shouldShowNotification(config) {
        // Filtrage intelligent des notifications
        const content = (config.content || '').toLowerCase();
        const title = (config.title || '').toLowerCase();

        // Filtrer les notifications peu utiles
        const spamPatterns = [
            'petite pause bien méritée',
            'progression attendue',
            'score a évolué en douceur',
            'votre progression vous attend',
            'pause bien méritée',
            'progression en douceur',
            'chargement',
            'loading',
            'veuillez patienter',
            'en cours de traitement'
        ];

        for (const pattern of spamPatterns) {
            if (content.includes(pattern) || title.includes(pattern)) {
                return false;
            }
        }

        // Vérifier l'importance minimale
        if (config.importance < this.settings.minImportance) {
            return false;
        }

        // Mode priorité uniquement
        if (this.settings.priorityOnly && config.priority !== 'high') {
            return false;
        }

        // Filtrer les notifications trop fréquentes
        const now = Date.now();
        const recentCount = Array.from(this.recentNotifications.values())
            .filter(timestamp => now - timestamp < 30000) // 30 secondes
            .length;

        if (recentCount > 3) {
            return false;
        }

        return true;
    }

    createNotification(config) {
        const container = this.getContainer();
        const notification = document.createElement('div');
        notification.className = `universal-notification ${config.type} ${config.theme}`;
        notification.dataset.id = config.id;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'assertive');

        notification.innerHTML = `
            <div class="universal-notification-header">
                <div style="display: flex; align-items: center;">
                    <span class="universal-notification-icon">${this.getIcon(config.type)}</span>
                    <span class="universal-notification-title">${config.title}</span>
                </div>
                ${config.closable ? '<button class="universal-notification-close" aria-label="Fermer">&times;</button>' : ''}
            </div>
            <div class="universal-notification-content">${config.content}</div>
            ${config.actions.length > 0 ? `
                <div class="universal-notification-actions">
                    ${config.actions.map(action => `
                        <button class="universal-notification-btn ${action.primary ? 'primary' : ''}" 
                                data-action="${action.id}">
                            ${action.label}
                        </button>
                    `).join('')}
                </div>
            ` : ''}
            <div class="universal-notification-progress" style="width: 100%;"></div>
        `;

        // Ajouter les événements
        if (config.closable) {
            const closeBtn = notification.querySelector('.universal-notification-close');
            closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.closeNotification(config.id);
            });
        }

        if (config.onClick) {
            notification.addEventListener('click', () => config.onClick(config));
        }

        // Ajouter les événements des actions
        config.actions.forEach(action => {
            const btn = notification.querySelector(`[data-action="${action.id}"]`);
            if (btn) {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (action.handler) action.handler(config);
                    if (action.close !== false) this.closeNotification(config.id);
                });
            }
        });

        container.appendChild(notification);
        this.notifications.set(config.id, { element: notification, config });

        // Afficher le bouton "Fermer toutes" s'il y a des notifications
        this.updateCloseAllButton();

        // Animation d'entrée
        requestAnimationFrame(() => {
            notification.classList.add('show');
            if (config.pulse) {
                notification.classList.add('pulse');
            }
        });

        // Auto-close
        if (config.duration > 0) {
            this.startAutoClose(config.id, config.duration);
        }

        // Son et vibration
        this.playNotificationSound(config.type);
        this.vibrate(config.type);

        return config.id;
    }

    startAutoClose(id, duration) {
        const notification = this.notifications.get(id);
        if (!notification) return;

        const progressBar = notification.element.querySelector('.universal-notification-progress');
        if (progressBar) {
            progressBar.style.transition = `width ${duration}ms linear`;
            progressBar.style.width = '0%';
        }

        setTimeout(() => {
            this.closeNotification(id);
        }, duration);
    }

    closeNotification(id) {
        const notification = this.notifications.get(id);
        if (!notification) return;

        const { element, config } = notification;

        element.classList.add('hide');
        element.classList.remove('show');

        setTimeout(() => {
            element.remove();
            this.notifications.delete(id);

            // Mettre à jour le bouton "Fermer toutes"
            this.updateCloseAllButton();

            if (config.onClose) {
                config.onClose(config);
            }

            this.processQueue();
        }, 400);
    }

    closeAllNotifications() {
        const ids = Array.from(this.notifications.keys());
        ids.forEach(id => this.closeNotification(id));
        this.queue = [];

        // Masquer le bouton "Fermer toutes"
        const closeAllBtn = document.getElementById('close-all-notifications');
        if (closeAllBtn) {
            closeAllBtn.style.display = 'none';
        }
    }

    processQueue() {
        if (this.isProcessing || this.queue.length === 0) return;

        this.isProcessing = true;
        setTimeout(() => {
            if (this.notifications.size < this.settings.maxNotifications && this.queue.length > 0) {
                const nextNotification = this.queue.shift();
                this.createNotification(nextNotification);
            }
            this.isProcessing = false;
        }, 500);
    }

    getIcon(type) {
        const icons = {
            success: '✅',
            warning: '⚠️',
            error: '❌',
            info: 'ℹ️',
            loading: '⏳',
            celebration: '🎉',
            achievement: '🏆',
            levelup: '⬆️',
            badge: '🏅',
            mission: '🎯',
            luna: '🌙',
            hack: '💻',
            security: '🛡️'
        };
        return icons[type] || icons.info;
    }

    playNotificationSound(type) {
        if (!this.settings.sound) return;

        // Implémentation simple de son (peut être étendue)
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        const frequencies = {
            success: 800,
            warning: 600,
            error: 400,
            info: 500
        };

        oscillator.frequency.setValueAtTime(frequencies[type] || 500, audioContext.currentTime);
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);

        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.2);
    }

    vibrate(type) {
        if (!this.settings.vibration || !navigator.vibrate) return;

        const patterns = {
            success: [100, 50, 100],
            warning: [200, 100, 200],
            error: [300, 150, 300],
            info: [100]
        };

        navigator.vibrate(patterns[type] || [100]);
    }

    // Méthodes utilitaires pour les types courants
    success(title, content, options = {}) {
        return this.show({
            type: 'success',
            title,
            content,
            ...options
        });
    }

    warning(title, content, options = {}) {
        return this.show({
            type: 'warning',
            title,
            content,
            ...options
        });
    }

    error(title, content, options = {}) {
        return this.show({
            type: 'error',
            title,
            content,
            duration: 6000, // Plus long pour les erreurs
            ...options
        });
    }

    info(title, content, options = {}) {
        return this.show({
            type: 'info',
            title,
            content,
            ...options
        });
    }

    loading(title, content, options = {}) {
        return this.show({
            type: 'loading',
            title,
            content,
            duration: 0, // Pas d'auto-close
            closable: false,
            ...options
        });
    }

    celebration(title, content, options = {}) {
        return this.show({
            type: 'celebration',
            title,
            content,
            duration: 5000,
            pulse: true,
            ...options
        });
    }

    achievement(title, content, options = {}) {
        return this.show({
            type: 'achievement',
            title,
            content,
            duration: 6000,
            pulse: true,
            ...options
        });
    }

    lunaMessage(message, duration = 4000) {
        return this.show({
            type: 'luna',
            title: '🌙 LUNA',
            content: message,
            duration,
            theme: 'arkalia'
        });
    }

    missionComplete(missionName, rewards = {}) {
        const content = `
            <div style="text-align: center;">
                <div style="font-size: 1.2em; margin-bottom: 8px;">${missionName}</div>
                ${rewards.xp ? `<div>+${rewards.xp} XP</div>` : ''}
                ${rewards.coins ? `<div>+${rewards.coins} Coins</div>` : ''}
                ${rewards.badge ? `<div>Badge: ${rewards.badge}</div>` : ''}
            </div>
        `;

        return this.celebration('🎯 Mission Complétée !', content, {
            duration: 5000,
            pulse: true
        });
    }

    // Méthodes de configuration
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        localStorage.setItem('arkalia_notifications_settings', JSON.stringify(this.settings));
    }

    getSettings() {
        return { ...this.settings };
    }

    // Méthodes de debug
    getActiveNotifications() {
        return Array.from(this.notifications.keys());
    }

    getQueueLength() {
        return this.queue.length;
    }

    clearAll() {
        this.closeAllNotifications();
        this.queue = [];
    }
}

// Initialiser le système universel
document.addEventListener('DOMContentLoaded', () => {
    window.universalNotifications = new UniversalNotifications();
    console.log('🔔 Universal Notifications System prêt');
});

// Exporter pour utilisation globale
window.UniversalNotifications = UniversalNotifications;
