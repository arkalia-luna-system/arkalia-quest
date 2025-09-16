/* ===== LEGACY (DEPRECATED) - ADAPTIVE GUIDANCE SYSTEM ===== */
/* Ce fichier est conservé pour compatibilité. Toutes les fonctionnalités
   d'overlay/coachmarks sont désactivées. */

class AdaptiveGuidanceSystem {
    constructor() {
        this.userProfile = this.detectUserProfile();
        this.interactionHistory = [];
        this.guidanceLevel = 'beginner';
        this.highlightedElements = new Set();
        this.tooltips = new Map();
        this.init();
    }

    init() {
        console.log('🎯 Système de guidance adaptative initialisé');
        this.setupEventListeners();
        // Désactivé: ne plus créer d'overlay/coachmark
        // this.createGuidanceOverlay();
        this.startProfileDetection();
    }

    // Détection du profil utilisateur
    detectUserProfile() {
        const interactions = this.getStoredInteractions();
        const timeSpent = this.getTimeSpent();
        const commandsUsed = this.getCommandsUsed();
        const errorsMade = this.getErrorsMade();

        // Analyse des patterns
        if (errorsMade > 10 && commandsUsed < 5) {
            return 'beginner';
        } else if (commandsUsed > 20 && timeSpent < 300) {
            return 'experienced';
        } else if (this.hasCompetitiveBehavior()) {
            return 'competitive';
        } else if (this.hasCreativeBehavior()) {
            return 'creative';
        } else if (timeSpent > 600 && commandsUsed < 10) {
            return 'casual';
        }

        return 'beginner'; // Par défaut
    }

    hasCompetitiveBehavior() {
        const interactions = this.getStoredInteractions();
        return interactions.some(i =>
            i.command.includes('score') ||
            i.command.includes('badge') ||
            i.command.includes('leaderboard')
        );
    }

    hasCreativeBehavior() {
        const interactions = this.getStoredInteractions();
        return interactions.some(i =>
            i.command.includes('theme') ||
            i.command.includes('color') ||
            i.command.includes('customize')
        );
    }

    // Création de l'overlay de guidance (désactivée)
    createGuidanceOverlay() {
        // Intentionnellement vide pour désactiver toute création d'overlay/tooltip
        return;
    }

    // Mise en évidence des éléments importants (désactivée)
    highlightElement(selector, message, options = {}) {
        // Ne rien faire: désactivation complète des coachmarks/overlays
        return;
    }

    // Affichage du tooltip
    showTooltip(element, message, options = {}) {
        const tooltip = document.getElementById('guidance-tooltip');
        const title = tooltip.querySelector('.guidance-title');
        const description = tooltip.querySelector('.guidance-description');

        title.textContent = message.title || 'Conseil';
        description.textContent = message.description || message;

        // Positionner le tooltip
        const rect = element.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();

        let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
        let top = rect.bottom + 10;

        // Ajuster si le tooltip sort de l'écran
        if (left < 10) left = 10;
        if (left + tooltipRect.width > window.innerWidth - 10) {
            left = window.innerWidth - tooltipRect.width - 10;
        }
        if (top + tooltipRect.height > window.innerHeight - 10) {
            top = rect.top - tooltipRect.height - 10;
        }

        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
        tooltip.style.display = 'block';

        // Animation d'apparition
        tooltip.classList.add('guidance-tooltip-show');
    }

    // Masquer le tooltip
    hideTooltip() {
        const tooltip = document.getElementById('guidance-tooltip');
        const highlight = document.getElementById('guidance-highlight');

        tooltip.classList.remove('guidance-tooltip-show');
        highlight.style.display = 'none';

        setTimeout(() => {
            tooltip.style.display = 'none';
        }, 300);
    }

    // Guidance adaptative selon le profil
    provideAdaptiveGuidance() {
        switch (this.userProfile) {
            case 'beginner':
                this.provideBeginnerGuidance();
                break;
            case 'experienced':
                this.provideExperiencedGuidance();
                break;
            case 'competitive':
                this.provideCompetitiveGuidance();
                break;
            case 'creative':
                this.provideCreativeGuidance();
                break;
            case 'casual':
                this.provideCasualGuidance();
                break;
        }
    }

    // Guidance pour débutants - DÉSACTIVÉE (trop agressive)
    provideBeginnerGuidance() {
        const currentPage = this.getCurrentPage();

        switch (currentPage) {
            case 'index':
                // Guidance supprimée - trop agressive et inutile
                // Les utilisateurs peuvent découvrir l'interface naturellement
                break;
            case 'tutorial':
                this.highlightElement('.tutorial-step.active', {
                    title: '📚 Étape en cours',
                    description: 'Suivez les instructions étape par étape. Prenez votre temps !'
                });
                break;
            case 'terminal':
                this.highlightElement('#terminal-input', {
                    title: '💻 Tapez votre commande',
                    description: 'Commencez par taper "aide" pour voir toutes les commandes disponibles.'
                });
                break;
            case 'monde':
                this.highlightElement('.zone:first-child', {
                    title: '🌍 Explorez les zones',
                    description: 'Cliquez sur une zone pour découvrir ses missions et défis.'
                });
                break;
            case 'profil':
                this.highlightElement('.stat-card:first-child', {
                    title: '👤 Votre progression',
                    description: 'Ici vous verrez votre score et votre niveau évoluer au fil du temps.'
                });
                break;
        }
    }

    // Guidance pour joueurs expérimentés
    provideExperiencedGuidance() {
        const currentPage = this.getCurrentPage();

        switch (currentPage) {
            case 'terminal':
                this.highlightElement('.terminal-advanced-commands', {
                    title: '⚡ Commandes avancées',
                    description: 'Utilisez les commandes avancées pour optimiser votre progression.'
                });
                break;
            case 'dashboard':
                this.highlightElement('.performance-metrics', {
                    title: '📊 Métriques de performance',
                    description: 'Analysez vos performances pour optimiser votre stratégie.'
                });
                break;
        }
    }

    // Guidance pour esprits compétitifs
    provideCompetitiveGuidance() {
        const currentPage = this.getCurrentPage();

        switch (currentPage) {
            case 'leaderboard':
                this.highlightElement('.leaderboard-table', {
                    title: '🏆 Classement',
                    description: 'Montez dans le classement en complétant des missions et en gagnant des points.'
                });
                break;
            case 'profil':
                this.highlightElement('.badges-section', {
                    title: '🎖️ Badges',
                    description: 'Débloquez des badges en accomplissant des défis spécifiques.'
                });
                break;
        }
    }

    // Guidance pour explorateurs créatifs
    provideCreativeGuidance() {
        const currentPage = this.getCurrentPage();

        switch (currentPage) {
            case 'accessibility':
                this.highlightElement('.theme-selector', {
                    title: '🎨 Personnalisation',
                    description: 'Personnalisez l\'apparence du jeu selon vos préférences.'
                });
                break;
            case 'terminal':
                this.highlightElement('.terminal-customization', {
                    title: '⚙️ Personnalisation avancée',
                    description: 'Explorez les options de personnalisation avancées.'
                });
                break;
        }
    }

    // Guidance pour joueurs casual
    provideCasualGuidance() {
        const currentPage = this.getCurrentPage();

        switch (currentPage) {
            case 'index':
                this.highlightElement('.cta-btn:nth-child(2)', {
                    title: '🚀 Commencez l\'aventure',
                    description: 'Prenez votre temps, explorez à votre rythme. Il n\'y a pas de pression !'
                });
                break;
            case 'monde':
                this.highlightElement('.zone', {
                    title: '🌍 Explorez librement',
                    description: 'Découvrez les zones à votre rythme. Chaque zone a ses propres secrets !'
                });
                break;
        }
    }

    // Système d'aide contextuelle
    provideContextualHelp(command, context) {
        const helpMessages = {
            'aide': {
                beginner: 'La commande "aide" vous montre toutes les commandes disponibles. C\'est un bon point de départ !',
                experienced: 'Utilisez "aide [commande]" pour obtenir des détails sur une commande spécifique.',
                competitive: 'Les commandes avancées peuvent vous donner un avantage. Explorez-les !',
                creative: 'Certaines commandes cachées peuvent révéler des fonctionnalités secrètes.',
                casual: 'Prenez votre temps pour explorer les commandes. Il n\'y a pas de course !'
            },
            'profil': {
                beginner: 'Votre profil montre votre progression. C\'est motivant de voir vos statistiques évoluer !',
                experienced: 'Analysez vos métriques pour optimiser votre stratégie de jeu.',
                competitive: 'Comparez vos statistiques avec les autres joueurs pour identifier vos forces.',
                creative: 'Personnalisez votre profil pour refléter votre style unique.',
                casual: 'Votre profil grandit avec vous. C\'est agréable de voir votre évolution !'
            }
        };

        const message = helpMessages[command]?.[this.userProfile];
        if (message) {
            this.showContextualMessage(message);
        }
    }

    // Affichage de messages contextuels
    showContextualMessage(message) {
        const notification = document.createElement('div');
        notification.className = 'contextual-help-notification';
        notification.innerHTML = `
            <div class="help-icon">💡</div>
            <div class="help-message">${message}</div>
        `;

        document.body.appendChild(notification);

        // Animation d'apparition
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Suppression automatique
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }

    // Détection des interactions
    trackInteraction(command, success, context) {
        this.interactionHistory.push({
            command,
            success,
            context,
            timestamp: Date.now(),
            userProfile: this.userProfile
        });

        // Mettre à jour le profil si nécessaire
        this.updateUserProfile();

        // Fournir une guidance adaptative
        this.provideAdaptiveGuidance();
    }

    // Mise à jour du profil utilisateur
    updateUserProfile() {
        const newProfile = this.detectUserProfile();
        if (newProfile !== this.userProfile) {
            this.userProfile = newProfile;
            this.guidanceLevel = this.getGuidanceLevel();
            console.log(`🔄 Profil utilisateur mis à jour: ${newProfile}`);
        }
    }

    // Niveau de guidance
    getGuidanceLevel() {
        const interactions = (this.interactionHistory && Array.isArray(this.interactionHistory)) ? this.interactionHistory.length : 0;
        const errors = (this.interactionHistory && Array.isArray(this.interactionHistory)) ? this.interactionHistory.filter(i => !i.success).length : 0;

        if (interactions < 5 || errors > interactions * 0.5) {
            return 'high';
        } else if (interactions < 20) {
            return 'medium';
        } else {
            return 'low';
        }
    }

    // Utilitaires
    getCurrentPage() {
        const path = window.location.pathname;
        if (path === '/') return 'index';
        if (path.includes('tutorial')) return 'tutorial';
        if (path.includes('terminal')) return 'terminal';
        if (path.includes('monde')) return 'monde';
        if (path.includes('profil')) return 'profil';
        if (path.includes('dashboard')) return 'dashboard';
        if (path.includes('leaderboard')) return 'leaderboard';
        if (path.includes('accessibility')) return 'accessibility';
        return 'unknown';
    }

    getStoredInteractions() {
        return JSON.parse(localStorage.getItem('arkalia_interactions') || '[]');
    }

    getTimeSpent() {
        return parseInt(localStorage.getItem('arkalia_time_spent') || '0');
    }

    getCommandsUsed() {
        return (this.interactionHistory && Array.isArray(this.interactionHistory)) ? this.interactionHistory.length : 0;
    }

    getErrorsMade() {
        return (this.interactionHistory && Array.isArray(this.interactionHistory)) ? this.interactionHistory.filter(i => !i.success).length : 0;
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Écouter les clics sur les éléments importants
        document.addEventListener('click', (e) => {
            const element = e.target.closest('[data-guidance]');
            if (element) {
                const guidance = element.dataset.guidance;
                this.provideContextualHelp(guidance, { element });
            }
        });

        // Écouter les commandes du terminal
        document.addEventListener('terminal-command', (e) => {
            this.trackInteraction(e.detail.command, e.detail.success, e.detail.context);
        });

        // Écouter les changements de page
        window.addEventListener('popstate', () => {
            setTimeout(() => this.provideAdaptiveGuidance(), 100);
        });
    }

    // Démarrer la détection de profil
    startProfileDetection() {
        // Détecter le profil initial
        this.provideAdaptiveGuidance();

        // Mettre à jour périodiquement (optimisé)
        setInterval(() => {
            this.updateUserProfile();
        }, 120000); // Toutes les 2 minutes
    }
}

// Initialiser le système de guidance
window.adaptiveGuidance = new AdaptiveGuidanceSystem();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdaptiveGuidanceSystem;
}
