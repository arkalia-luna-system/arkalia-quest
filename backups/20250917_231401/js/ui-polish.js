/* ===== ARKALIA QUEST - UI POLISH SYSTEM ===== */
/* Système de polish UI pour corriger les micro-frictions */

class UIPolish {
    constructor() {
        this.notificationHistory = new Set();
        this.lastNotificationTime = 0;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.optimizeNotifications();
        this.improveEmptyStates();
        this.enhanceInteractions();
        // console.log('✨ UI Polish System initialisé');
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('arkalia:progression:synced', (e) => {
            this.updateEmptyStates(e.detail);
        });

        // Écouter les événements de notification
        document.addEventListener('arkalia:notification:show', (e) => {
            this.handleNotification(e.detail);
        });
    }

    optimizeNotifications() {
        // Intercepter les notifications pour éviter les doublons
        const originalConsoleLog = console.log;
        console.log = (...args) => {
            const message = args.join(' ');
            if (this.isRedundantNotification(message)) {
                return; // Ignorer les notifications redondantes
            }
            originalConsoleLog.apply(console, args);
        };
    }

    isRedundantNotification(message) {
        const now = Date.now();
        const timeSinceLastNotification = now - this.lastNotificationTime;

        // Ignorer les notifications trop rapprochées (moins de 2 secondes)
        if (timeSinceLastNotification < 2000) {
            return true;
        }

        // Ignorer les messages répétitifs
        if (this.notificationHistory.has(message)) {
            return true;
        }

        // Ajouter à l'historique
        this.notificationHistory.add(message);
        this.lastNotificationTime = now;

        // Nettoyer l'historique après 30 secondes
        setTimeout(() => {
            this.notificationHistory.delete(message);
        }, 30000);

        return false;
    }

    handleNotification(notificationData) {
        const { message, type, duration } = notificationData;

        // Vérifier si c'est une notification redondante
        if (this.isRedundantNotification(message)) {
            return;
        }

        // Afficher la notification avec un style amélioré
        this.showPolishedNotification(message, type, duration);
    }

    showPolishedNotification(message, type = 'info', duration = 3000) {
        const container = document.getElementById('realtime-notifications') || this.createNotificationContainer();

        const notification = document.createElement('div');
        notification.className = `polished-notification ${type}`;
        notification.style.cssText = `
            background: ${this.getNotificationColor(type)};
            color: white;
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 12px;
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(15px);
            border: 2px solid ${this.getNotificationBorderColor(type)};
            font-family: 'IBM Plex Mono', monospace;
            font-size: 14px;
            line-height: 1.4;
            white-space: pre-line;
            text-align: center;
            max-width: 350px;
            animation: slideInRight 0.5s ease-out;
            transform: translateX(100%);
            opacity: 0;
            position: relative;
            overflow: hidden;
        `;

        // Ajouter un effet de brillance
        const shine = document.createElement('div');
        shine.style.cssText = `
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            animation: shine 1s ease-in-out;
            pointer-events: none;
        `;

        notification.appendChild(shine);
        notification.textContent = message;
        container.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        }, 10);

        // Supprimer après la durée spécifiée
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, duration);
    }

    createNotificationContainer() {
        const container = document.createElement('div');
        container.id = 'realtime-notifications';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            pointer-events: none;
            max-width: 350px;
        `;
        document.body.appendChild(container);
        return container;
    }

    getNotificationColor(type) {
        const colors = {
            'success': 'linear-gradient(135deg, #22c55e, #16a34a)',
            'error': 'linear-gradient(135deg, #ef4444, #dc2626)',
            'warning': 'linear-gradient(135deg, #f59e0b, #d97706)',
            'info': 'linear-gradient(135deg, #3b82f6, #2563eb)',
            'badge': 'linear-gradient(135deg, #ffd700, #ffb700)',
            'mission': 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
            'skill': 'linear-gradient(135deg, #06b6d4, #0891b2)'
        };
        return colors[type] || colors['info'];
    }

    getNotificationBorderColor(type) {
        const colors = {
            'success': '#00ff00',
            'error': '#ff0000',
            'warning': '#ffaa00',
            'info': '#00aaff',
            'badge': '#ffd700',
            'mission': '#8b5cf6',
            'skill': '#06b6d4'
        };
        return colors[type] || colors['info'];
    }

    updateEmptyStates(progressionData) {
        // Mettre à jour les états vides selon la progression
        this.updateDashboardEmptyState(progressionData);
        this.updateProfileEmptyState(progressionData);
        this.updateMissionEmptyState(progressionData);
    }

    updateDashboardEmptyState(progressionData) {
        const dashboard = document.querySelector('.dashboard-container, #dashboard');
        if (!dashboard) return;

        // Masquer les messages "Prêt à commencer !" si il y a de la progression
        const readyMessages = dashboard.querySelectorAll('.ready-to-start, .no-progress');
        if (progressionData.xp > 0 || progressionData.badges?.length > 0) {
            readyMessages.forEach(msg => {
                msg.style.display = 'none';
            });
        }

        // Mettre à jour les compteurs
        this.updateCounters(dashboard, progressionData);
    }

    updateProfileEmptyState(progressionData) {
        const profile = document.querySelector('.profile-container, #profile');
        if (!profile) return;

        // Mettre à jour les compteurs
        this.updateCounters(profile, progressionData);
    }

    updateMissionEmptyState(progressionData) {
        const missions = document.querySelector('.missions-container, #missions');
        if (!missions) return;

        // Mettre à jour les compteurs
        this.updateCounters(missions, progressionData);
    }

    updateCounters(container, progressionData) {
        const counters = {
            'level': progressionData.level,
            'xp': progressionData.xp,
            'score': progressionData.score,
            'coins': progressionData.coins,
            'badges': progressionData.badges?.length || 0,
            'missions': progressionData.missions_completed?.length || 0
        };

        Object.entries(counters).forEach(([key, value]) => {
            const elements = container.querySelectorAll(`[data-stat="${key}"], .${key}-value, #${key}-value, .player-${key}`);
            elements.forEach(el => {
                if (el.textContent !== value.toString()) {
                    this.animateCounter(el, value);
                }
            });
        });
    }

    animateCounter(element, newValue) {
        const oldValue = parseInt(element.textContent) || 0;
        const difference = newValue - oldValue;

        if (difference === 0) return;

        // Animation de compteur
        element.style.transition = 'all 0.3s ease';
        element.style.transform = 'scale(1.1)';
        element.style.color = difference > 0 ? '#00ff00' : '#ff6b6b';

        // Mettre à jour la valeur
        element.textContent = newValue;

        // Retour à la normale
        setTimeout(() => {
            element.style.transform = 'scale(1)';
            element.style.color = '';
        }, 300);
    }

    improveEmptyStates() {
        // Améliorer l'affichage des états vides
        const emptyStates = document.querySelectorAll('.empty-state, .no-data, .no-progress');
        emptyStates.forEach(state => {
            this.enhanceEmptyState(state);
        });
    }

    enhanceEmptyState(element) {
        // Ajouter des animations subtiles aux états vides
        element.style.transition = 'all 0.3s ease';
        element.style.opacity = '0.8';

        // Ajouter un effet de pulsation subtile
        element.style.animation = 'subtlePulse 3s ease-in-out infinite';
    }

    enhanceInteractions() {
        // Améliorer les interactions avec les boutons et éléments cliquables
        const interactiveElements = document.querySelectorAll('button, .clickable, .interactive');
        interactiveElements.forEach(element => {
            this.enhanceInteractiveElement(element);
        });
    }

    enhanceInteractiveElement(element) {
        // Ajouter des effets de hover améliorés
        element.addEventListener('mouseenter', () => {
            element.style.transform = 'translateY(-2px)';
            element.style.boxShadow = '0 4px 15px rgba(0, 255, 0, 0.3)';
        });

        element.addEventListener('mouseleave', () => {
            element.style.transform = 'translateY(0)';
            element.style.boxShadow = '';
        });

        element.addEventListener('click', () => {
            element.style.transform = 'scale(0.95)';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 150);
        });
    }

    // Méthode pour ajouter des animations CSS
    addAnimations() {
        if (document.getElementById('ui-polish-animations')) return;

        const style = document.createElement('style');
        style.id = 'ui-polish-animations';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes shine {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            @keyframes subtlePulse {
                0%, 100% { opacity: 0.8; }
                50% { opacity: 1; }
            }
            
            .polished-notification {
                position: relative;
                overflow: hidden;
            }
            
            .polished-notification::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                animation: shine 1s ease-in-out;
                pointer-events: none;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialiser le système de polish UI
const uiPolish = new UIPolish();
