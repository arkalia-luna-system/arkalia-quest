/**
 * Gestionnaire d'Interface Adaptative Multi-Profils
 * Masque les éléments non pertinents selon le profil utilisateur
 */

class AdaptiveUIManager {
    constructor() {
        this.currentProfile = null;
        this.profileElements = new Map();
        this.hiddenElements = new Set();
        this.init();
    }

    init() {
        console.log('🎨 Adaptive UI Manager initialisé');
        this.detectUserProfile();
        this.setupProfileAdaptation();
        this.observeProfileChanges();
    }

    detectUserProfile() {
        // Utiliser le système de profils existant
        if (window.advancedPlayerProfiles) {
            this.currentProfile = window.advancedPlayerProfiles.currentProfile;
        } else {
            // Détection basique
            this.currentProfile = this.basicProfileDetection();
        }

        console.log(`👤 Profil détecté: ${this.currentProfile}`);
    }

    basicProfileDetection() {
        const interactions = JSON.parse(localStorage.getItem('arkalia_interactions') || '[]');
        const timeSpent = this.getTimeSpent();
        const commandsUsed = this.getCommandsUsed();

        // Logique de détection basique
        if (commandsUsed < 5 && timeSpent < 300) return 'debutant';
        if (commandsUsed > 20 && timeSpent < 600) return 'competitif';
        if (timeSpent > 1800 && commandsUsed < 10) return 'casual';
        if (this.hasCreativeBehavior()) return 'creatif';
        return 'experimente';
    }

    hasCreativeBehavior() {
        const interactions = JSON.parse(localStorage.getItem('arkalia_interactions') || '[]');
        return interactions.some(i =>
            i.command?.includes('theme') ||
            i.command?.includes('color') ||
            i.command?.includes('customize')
        );
    }

    getTimeSpent() {
        const startTime = localStorage.getItem('arkalia_session_start');
        if (!startTime) return 0;
        return Date.now() - parseInt(startTime);
    }

    getCommandsUsed() {
        const interactions = JSON.parse(localStorage.getItem('arkalia_interactions') || '[]');
        return interactions.length;
    }

    setupProfileAdaptation() {
        // Configuration des éléments par profil
        this.profileElements.set('debutant', {
            show: [
                '.tutorial-section',
                '.basic-commands',
                '.luna-section',
                '.simple-missions'
            ],
            hide: [
                '.advanced-stats',
                '.leaderboard-section',
                '.competitive-features',
                '.technical-details',
                '.accessibility-advanced'
            ],
            highlight: [
                '.tutorial-btn',
                '.start-tutorial-btn',
                '.luna-contact-btn'
            ]
        });

        this.profileElements.set('competitif', {
            show: [
                '.leaderboard-section',
                '.stats-section',
                '.missions-section',
                '.badges-section',
                '.competitive-features'
            ],
            hide: [
                '.tutorial-section',
                '.basic-help',
                '.accessibility-advanced'
            ],
            highlight: [
                '.leaderboard-btn',
                '.missions-btn',
                '.stats-btn'
            ]
        });

        this.profileElements.set('casual', {
            show: [
                '.simple-missions',
                '.luna-section',
                '.world-section',
                '.basic-stats'
            ],
            hide: [
                '.advanced-stats',
                '.competitive-features',
                '.technical-details',
                '.accessibility-advanced',
                '.tutorial-section'
            ],
            highlight: [
                '.world-btn',
                '.luna-contact-btn',
                '.simple-missions-btn'
            ]
        });

        this.profileElements.set('creatif', {
            show: [
                '.themes-section',
                '.customization-section',
                '.world-section',
                '.luna-section'
            ],
            hide: [
                '.competitive-features',
                '.advanced-stats',
                '.tutorial-section'
            ],
            highlight: [
                '.themes-btn',
                '.customization-btn',
                '.world-btn'
            ]
        });

        this.profileElements.set('experimente', {
            show: [
                '.all-sections'
            ],
            hide: [
                '.tutorial-section',
                '.basic-help'
            ],
            highlight: []
        });

        // Appliquer l'adaptation
        this.applyProfileAdaptation();
    }

    applyProfileAdaptation() {
        const config = this.profileElements.get(this.currentProfile);
        if (!config) return;

        // Masquer les éléments non pertinents
        config.hide.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.style.display = 'none';
                this.hiddenElements.add(element);
            });
        });

        // Afficher les éléments pertinents
        config.show.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.style.display = '';
                this.hiddenElements.delete(element);
            });
        });

        // Mettre en évidence les éléments importants
        config.highlight.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.classList.add('profile-highlighted');
            });
        });

        // Adapter les messages selon le profil
        this.adaptMessagesForProfile();
    }

    adaptMessagesForProfile() {
        const messages = {
            'debutant': {
                welcome: '🎮 Bienvenue ! Commence par le tutoriel pour apprendre les bases.',
                cta: '🎯 COMMENCER LE TUTORIEL',
                empty: 'Commence ton aventure !'
            },
            'competitif': {
                welcome: '🏆 Prêt pour la compétition ? Vérifie le classement !',
                cta: '🏆 VOIR LE CLASSEMENT',
                empty: 'Aucun défi en cours...'
            },
            'casual': {
                welcome: '😌 Détends-toi et explore le monde d\'Arkalia.',
                cta: '🌍 EXPLORER LE MONDE',
                empty: 'Prends ton temps...'
            },
            'creatif': {
                welcome: '🎨 Personnalise ton expérience et explore !',
                cta: '🎨 PERSONNALISER',
                empty: 'Laisse libre cours à ta créativité...'
            },
            'experimente': {
                welcome: '🚀 Bienvenue, hacker expérimenté !',
                cta: '💻 ACCÉDER AU TERMINAL',
                empty: 'Tout est à ta disposition...'
            }
        };

        const profileMessages = messages[this.currentProfile];
        if (!profileMessages) return;

        // Mettre à jour les messages
        this.updateMessage('.welcome-message', profileMessages.welcome);
        this.updateMessage('.main-cta', profileMessages.cta);
        this.updateMessage('.empty-state-message', profileMessages.empty);
    }

    updateMessage(selector, text) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            if (element.tagName === 'BUTTON') {
                element.textContent = text;
            } else {
                element.innerHTML = text;
            }
        });
    }

    observeProfileChanges() {
        // Observer les changements de profil
        document.addEventListener('profileChanged', (event) => {
            this.currentProfile = event.detail.profile;
            this.applyProfileAdaptation();
        });

        // Observer les interactions pour réadapter
        document.addEventListener('click', (event) => {
            this.analyzeInteraction(event);
        });
    }

    analyzeInteraction(event) {
        const element = event.target;
        const interaction = {
            element: element.tagName,
            class: element.className,
            id: element.id,
            timestamp: Date.now()
        };

        // Enregistrer l'interaction
        this.recordInteraction(interaction);

        // Vérifier si le profil doit changer
        this.checkProfileEvolution();
    }

    recordInteraction(interaction) {
        const interactions = JSON.parse(localStorage.getItem('arkalia_interactions') || '[]');
        interactions.push(interaction);

        // Garder seulement les 100 dernières interactions
        if (interactions.length > 100) {
            interactions.splice(0, interactions.length - 100);
        }

        localStorage.setItem('arkalia_interactions', JSON.stringify(interactions));
    }

    checkProfileEvolution() {
        // Vérifier si le profil doit évoluer
        const newProfile = this.basicProfileDetection();
        if (newProfile !== this.currentProfile) {
            this.currentProfile = newProfile;
            this.applyProfileAdaptation();

            // Notifier le changement
            document.dispatchEvent(new CustomEvent('profileChanged', {
                detail: { profile: newProfile }
            }));
        }
    }

    // Méthodes utilitaires
    showElement(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.style.display = '';
            this.hiddenElements.delete(element);
        });
    }

    hideElement(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.style.display = 'none';
            this.hiddenElements.add(element);
        });
    }

    resetToDefault() {
        // Réinitialiser à l'affichage par défaut
        this.hiddenElements.forEach(element => {
            element.style.display = '';
        });
        this.hiddenElements.clear();
    }
}

// Initialiser le gestionnaire d'interface adaptative
document.addEventListener('DOMContentLoaded', () => {
    window.adaptiveUIManager = new AdaptiveUIManager();
    console.log('🎨 Interface adaptative activée');
});

// Export pour utilisation externe
window.AdaptiveUIManager = AdaptiveUIManager;
