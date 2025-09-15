/* ===== ARKALIA QUEST - POPUP MANAGER ===== */
/* Gestionnaire centralisé des popups pour éviter les chevauchements */

class PopupManager {
    constructor() {
        this.activePopups = new Map();
        this.popupQueue = [];
        this.isProcessingQueue = false;
        this.zIndexBase = 10000;
        this.currentZIndex = this.zIndexBase;
        this.init();
    }

    init() {
        this.setupGlobalStyles();
        this.setupEventListeners();
        console.log('🎭 Popup Manager initialisé');
    }

    setupGlobalStyles() {
        // Créer les styles globaux pour la gestion des popups
        const style = document.createElement('style');
        style.textContent = `
            .popup-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .popup-overlay.show {
                opacity: 1;
            }
            
            .popup-content {
                background: rgba(9, 9, 11, 0.95);
                border: 2px solid rgba(167, 139, 250, 0.5);
                border-radius: 15px;
                padding: 30px;
                max-width: 90vw;
                max-height: 90vh;
                overflow-y: auto;
                backdrop-filter: blur(15px);
                transform: scale(0.8);
                transition: transform 0.3s ease;
            }
            
            .popup-overlay.show .popup-content {
                transform: scale(1);
            }
            
            .popup-close {
                position: absolute;
                top: 15px;
                right: 15px;
                background: none;
                border: none;
                color: var(--argent-holographique);
                font-size: 1.5em;
                cursor: pointer;
                transition: color 0.3s ease;
                z-index: 1;
            }
            
            .popup-close:hover {
                color: var(--violet-lunaire);
            }
            
            .popup-priority-high {
                z-index: 10050 !important;
            }
            
            .popup-priority-medium {
                z-index: 10030 !important;
            }
            
            .popup-priority-low {
                z-index: 10010 !important;
            }
        `;
        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Gérer la fermeture avec Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeTopPopup();
            }
        });

        // Gérer les clics sur l'overlay
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('popup-overlay')) {
                this.closeTopPopup();
            }
        });
    }

    showPopup(config) {
        const popupConfig = {
            id: config.id || `popup_${Date.now()}`,
            title: config.title || '',
            content: config.content || '',
            priority: config.priority || 'medium', // high, medium, low
            closable: config.closable !== false,
            autoClose: config.autoClose || false,
            autoCloseDelay: config.autoCloseDelay || 5000,
            onClose: config.onClose || null,
            className: config.className || '',
            ...config
        };

        // Vérifier si un popup avec le même ID existe déjà
        if (this.activePopups.has(popupConfig.id)) {
            console.log(`Popup ${popupConfig.id} déjà ouvert`);
            return popupConfig.id;
        }

        // Ajouter à la queue si d'autres popups sont actifs
        if (this.activePopups.size > 0) {
            this.popupQueue.push(popupConfig);
            console.log(`Popup ${popupConfig.id} ajouté à la queue`);
            return popupConfig.id;
        }

        return this.createPopup(popupConfig);
    }

    createPopup(config) {
        const popup = document.createElement('div');
        popup.className = `popup-overlay ${config.className}`;
        popup.id = `popup_${config.id}`;

        // Définir la priorité
        popup.classList.add(`popup-priority-${config.priority}`);

        // Calculer le z-index
        this.currentZIndex += 10;
        popup.style.zIndex = this.currentZIndex;

        popup.innerHTML = `
            <div class="popup-content">
                ${config.closable ? '<button class="popup-close">&times;</button>' : ''}
                ${config.title ? `<h3>${config.title}</h3>` : ''}
                <div class="popup-body">${config.content}</div>
            </div>
        `;

        document.body.appendChild(popup);

        // Ajouter les événements
        if (config.closable) {
            const closeBtn = popup.querySelector('.popup-close');
            closeBtn.addEventListener('click', () => this.closePopup(config.id));
        }

        // Animation d'apparition
        setTimeout(() => {
            popup.classList.add('show');
        }, 100);

        // Auto-close si configuré
        if (config.autoClose) {
            setTimeout(() => {
                this.closePopup(config.id);
            }, config.autoCloseDelay);
        }

        // Stocker le popup
        this.activePopups.set(config.id, {
            element: popup,
            config: config,
            created: Date.now()
        });

        console.log(`Popup ${config.id} créé avec priorité ${config.priority}`);
        return config.id;
    }

    closePopup(id) {
        const popupData = this.activePopups.get(id);
        if (!popupData) return;

        const { element, config } = popupData;

        // Animation de fermeture
        element.classList.remove('show');

        setTimeout(() => {
            element.remove();
            this.activePopups.delete(id);

            // Callback de fermeture
            if (config.onClose) {
                config.onClose();
            }

            // Traiter la queue
            this.processQueue();

            console.log(`Popup ${id} fermé`);
        }, 300);
    }

    closeTopPopup() {
        if (this.activePopups.size === 0) return;

        // Fermer le popup avec la priorité la plus haute
        const popups = Array.from(this.activePopups.values());
        const topPopup = popups.reduce((highest, current) => {
            const highestPriority = this.getPriorityValue(highest.config.priority);
            const currentPriority = this.getPriorityValue(current.config.priority);
            return currentPriority > highestPriority ? current : highest;
        });

        this.closePopup(topPopup.config.id);
    }

    getPriorityValue(priority) {
        const priorities = { low: 1, medium: 2, high: 3 };
        return priorities[priority] || 2;
    }

    processQueue() {
        if (this.isProcessingQueue || this.popupQueue.length === 0) return;

        this.isProcessingQueue = true;

        // Attendre un peu avant de traiter le prochain popup
        setTimeout(() => {
            if (this.activePopups.size === 0 && this.popupQueue.length > 0) {
                const nextPopup = this.popupQueue.shift();
                this.createPopup(nextPopup);
            }
            this.isProcessingQueue = false;
        }, 500);
    }

    closeAllPopups() {
        const popupIds = Array.from(this.activePopups.keys());
        popupIds.forEach(id => this.closePopup(id));
        this.popupQueue = [];
    }

    getActivePopups() {
        return Array.from(this.activePopups.keys());
    }

    // Méthodes utilitaires pour les types de popups courants
    showNotification(message, type = 'info', duration = 3000) {
        return this.showPopup({
            id: `notification_${Date.now()}`,
            content: `<div class="notification ${type}">${message}</div>`,
            priority: 'low',
            autoClose: true,
            autoCloseDelay: duration,
            className: 'notification-popup'
        });
    }

    showConfirmation(message, onConfirm, onCancel = null) {
        return this.showPopup({
            id: `confirmation_${Date.now()}`,
            title: 'Confirmation',
            content: `
                <p>${message}</p>
                <div class="confirmation-buttons">
                    <button class="btn-confirm" onclick="popupManager.confirmPopup('${Date.now()}')">Confirmer</button>
                    <button class="btn-cancel" onclick="popupManager.cancelPopup('${Date.now()}')">Annuler</button>
                </div>
            `,
            priority: 'high',
            className: 'confirmation-popup'
        });
    }

    showLoading(message = 'Chargement...') {
        return this.showPopup({
            id: `loading_${Date.now()}`,
            content: `
                <div class="loading-content">
                    <div class="loading-spinner"></div>
                    <p>${message}</p>
                </div>
            `,
            priority: 'high',
            closable: false,
            className: 'loading-popup'
        });
    }

    // Méthodes pour remplacer les popups existants
    replaceLunaMessage(message, duration = 4000) {
        // Fermer les anciens messages LUNA
        this.closeAllPopups();

        return this.showPopup({
            id: 'luna_message',
            content: `
                <div class="luna-message">
                    <div class="luna-avatar">🌙</div>
                    <div class="luna-text">${message}</div>
                </div>
            `,
            priority: 'medium',
            autoClose: true,
            autoCloseDelay: duration,
            className: 'luna-popup'
        });
    }

    replaceMissionCompletion(mission, rewards = {}) {
        return this.showPopup({
            id: 'mission_completion',
            title: '🎉 Mission Complétée !',
            content: `
                <div class="mission-completion">
                    <h4>${mission}</h4>
                    ${rewards.xp ? `<p>+${rewards.xp} XP</p>` : ''}
                    ${rewards.coins ? `<p>+${rewards.coins} Coins</p>` : ''}
                    ${rewards.badge ? `<p>Badge: ${rewards.badge}</p>` : ''}
                </div>
            `,
            priority: 'high',
            autoClose: true,
            autoCloseDelay: 4000,
            className: 'mission-completion-popup'
        });
    }

    replaceZoneExploration(zoneData) {
        return this.showPopup({
            id: 'zone_exploration',
            title: `🗺️ ${zoneData.name}`,
            content: `
                <div class="zone-exploration">
                    <p>${zoneData.description}</p>
                    <div class="zone-actions">
                        <button onclick="zoneExploration.exploreZone()">🔍 Explorer</button>
                        <button onclick="zoneExploration.playMiniGame()">🎮 Mini-jeux</button>
                        <button onclick="zoneExploration.searchSecrets()">💎 Secrets</button>
                    </div>
                </div>
            `,
            priority: 'medium',
            className: 'zone-exploration-popup'
        });
    }
}

// Initialiser le gestionnaire de popups
document.addEventListener('DOMContentLoaded', () => {
    window.popupManager = new PopupManager();
    console.log('🎭 Popup Manager prêt');
});

// Exporter pour utilisation globale
window.PopupManager = PopupManager;
