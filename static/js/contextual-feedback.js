/* ===== ARKALIA QUEST - CONTEXTUAL FEEDBACK ===== */
/* Système de feedback contextuel selon la page et les actions */

class ContextualFeedback {
    constructor() {
        this.currentPage = this.getCurrentPage();
        this.userActions = [];
        this.feedbackHistory = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupPageSpecificFeedback();
        console.log('💬 Contextual Feedback initialisé');
    }

    getCurrentPage() {
        const path = window.location.pathname;
        const pageMap = {
            '/': 'accueil',
            '/terminal': 'terminal',
            '/monde': 'monde',
            '/profil': 'profil',
            '/dashboard': 'dashboard',
            '/leaderboard': 'leaderboard'
        };
        return pageMap[path] || 'unknown';
    }

    setupEventListeners() {
        // Écouter les changements de page
        document.addEventListener('arkalia:navigation:change', (event) => {
            this.currentPage = this.getCurrentPage();
            this.setupPageSpecificFeedback();
        });

        // Écouter les actions utilisateur
        document.addEventListener('click', (event) => {
            this.handleUserAction('click', event.target);
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                this.handleUserAction('enter', event.target);
            }
        });
    }

    setupPageSpecificFeedback() {
        // Feedback spécifique à chaque page
        switch (this.currentPage) {
            case 'terminal':
                this.setupTerminalFeedback();
                break;
            case 'monde':
                this.setupMondeFeedback();
                break;
            case 'profil':
                this.setupProfilFeedback();
                break;
            case 'dashboard':
                this.setupDashboardFeedback();
                break;
        }
    }

    setupTerminalFeedback() {
        // Feedback pour le terminal
        const input = document.getElementById('commandInput');
        if (input) {
            input.addEventListener('input', () => {
                this.showTypingFeedback();
            });
        }
    }

    setupMondeFeedback() {
        // Feedback pour le monde
        const zones = document.querySelectorAll('.zone');
        zones.forEach(zone => {
            zone.addEventListener('mouseenter', () => {
                this.showZoneHoverFeedback(zone);
            });
        });
    }

    setupProfilFeedback() {
        // Feedback pour le profil
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.showStatHoverFeedback(card);
            });
        });
    }

    setupDashboardFeedback() {
        // Feedback pour le dashboard
        const widgets = document.querySelectorAll('.widget');
        widgets.forEach(widget => {
            widget.addEventListener('mouseenter', () => {
                this.showWidgetHoverFeedback(widget);
            });
        });
    }

    handleUserAction(action, element) {
        this.userActions.push({
            action,
            element: element.tagName,
            timestamp: Date.now(),
            page: this.currentPage
        });

        // Limiter l'historique
        if (this.userActions.length > 50) {
            this.userActions = this.userActions.slice(-50);
        }

        // Générer un feedback contextuel
        this.generateContextualFeedback(action, element);
    }

    generateContextualFeedback(action, element) {
        const feedback = this.getFeedbackForAction(action, element);
        if (feedback) {
            this.showFeedback(feedback);
        }
    }

    getFeedbackForAction(action, element) {
        const elementType = element.tagName.toLowerCase();
        const elementClass = element.className;
        const elementId = element.id;

        // Feedback selon l'action et l'élément
        if (action === 'click') {
            if (elementType === 'button') {
                return this.getButtonFeedback(element);
            } else if (elementType === 'a') {
                return this.getLinkFeedback(element);
            }
        } else if (action === 'enter') {
            if (elementType === 'input') {
                return this.getInputFeedback(element);
            }
        }

        return null;
    }

    getButtonFeedback(element) {
        const buttonText = element.textContent.toLowerCase();

        if (buttonText.includes('commencer') || buttonText.includes('start')) {
            return {
                type: 'encouragement',
                message: '🚀 Excellente décision ! Commençons l\'aventure !',
                duration: 3000
            };
        } else if (buttonText.includes('aide') || buttonText.includes('help')) {
            return {
                type: 'info',
                message: '💡 Je suis là pour t\'aider !',
                duration: 2000
            };
        } else if (buttonText.includes('luna')) {
            return {
                type: 'luna',
                message: '🌙 LUNA est ravie de te voir !',
                duration: 3000
            };
        }

        return null;
    }

    getLinkFeedback(element) {
        const href = element.getAttribute('href');
        const linkText = element.textContent.toLowerCase();

        if (href === '/terminal') {
            return {
                type: 'info',
                message: '⌨️ Accès au terminal de hacking...',
                duration: 2000
            };
        } else if (href === '/monde') {
            return {
                type: 'info',
                message: '🌍 Exploration du monde d\'Arkalia...',
                duration: 2000
            };
        } else if (href === '/profil') {
            return {
                type: 'info',
                message: '👤 Consultation de ton profil...',
                duration: 2000
            };
        }

        return null;
    }

    getInputFeedback(element) {
        if (element.id === 'commandInput') {
            return {
                type: 'info',
                message: '⌨️ Commande en cours d\'exécution...',
                duration: 2000
            };
        }

        return null;
    }

    showTypingFeedback() {
        // Feedback de frappe
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage('💭 Je vois que tu écris...', 1000);
        }
    }

    showZoneHoverFeedback(zone) {
        const zoneName = zone.querySelector('.zone-name')?.textContent;
        if (zoneName && window.lunaVision) {
            window.lunaVision.showLunaMessage(`🔍 Zone ${zoneName} - Explore ses secrets...`, 2000);
        }
    }

    showStatHoverFeedback(card) {
        const statLabel = card.querySelector('.stat-label')?.textContent;
        if (statLabel && window.lunaVision) {
            window.lunaVision.showLunaMessage(`📊 ${statLabel} - Ta progression est excellente !`, 2000);
        }
    }

    showWidgetHoverFeedback(widget) {
        const widgetTitle = widget.querySelector('.widget-title')?.textContent;
        if (widgetTitle && window.lunaVision) {
            window.lunaVision.showLunaMessage(`📈 ${widgetTitle} - Analyse en cours...`, 2000);
        }
    }

    showFeedback(feedback) {
        if (window.universalNotifications) {
            window.universalNotifications.show({
                type: feedback.type,
                title: feedback.message,
                duration: feedback.duration || 3000,
                importance: 2
            });
        }
    }

    // Méthodes publiques
    getCurrentPage() {
        return this.currentPage;
    }

    getUserActions() {
        return this.userActions;
    }

    getFeedbackHistory() {
        return this.feedbackHistory;
    }

    clearHistory() {
        this.userActions = [];
        this.feedbackHistory = [];
    }
}

// Initialiser le système de feedback contextuel
document.addEventListener('DOMContentLoaded', () => {
    window.contextualFeedback = new ContextualFeedback();
});

// Exporter pour utilisation globale
window.ContextualFeedback = ContextualFeedback;
