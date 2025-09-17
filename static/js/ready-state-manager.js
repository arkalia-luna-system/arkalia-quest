/**
 * Gestionnaire des états "Prêt à commencer !"
 * Fait disparaître les blocs quand l'utilisateur a des données
 */

class ReadyStateManager {
    constructor() {
        this.readyBlocks = new Set();
        this.hiddenBlocks = new Set();
        this.checkInterval = null;
        this.checkFrequency = 2000; // 2 secondes
        
        this.init();
    }

    init() {
        console.log('🚀 Initialisation du gestionnaire d\'états "Prêt à commencer !"...');
        this.findReadyBlocks();
        this.setupEventListeners();
        this.startChecking();
        console.log('✅ Gestionnaire d\'états initialisé');
    }

    findReadyBlocks() {
        // Sélecteurs pour les blocs "Prêt à commencer !"
        const selectors = [
            '.ready-to-start',
            '.prêt-à-commencer',
            '.ready-state',
            '.empty-state',
            '.no-data',
            '.welcome-message',
            '.getting-started',
            '.first-time',
            '.tutorial-prompt'
        ];

        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (this.isReadyBlock(element)) {
                    this.readyBlocks.add(element);
                }
            });
        });

        console.log(`📦 Trouvé ${this.readyBlocks.size} blocs "Prêt à commencer !"`);
    }

    isReadyBlock(element) {
        const text = element.textContent.toLowerCase();
        const readyKeywords = [
            'prêt à commencer',
            'ready to start',
            'commençons',
            'let\'s start',
            'bienvenue',
            'welcome',
            'première fois',
            'first time',
            'débuter',
            'getting started',
            'tutoriel',
            'tutorial',
            'guide',
            'aide',
            'help'
        ];

        return readyKeywords.some(keyword => text.includes(keyword));
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('arkalia:progression:updated', () => {
            this.checkAndHideBlocks();
        });

        document.addEventListener('arkalia:mission:completed', () => {
            this.checkAndHideBlocks();
        });

        document.addEventListener('arkalia:skill:upgraded', () => {
            this.checkAndHideBlocks();
        });

        document.addEventListener('arkalia:badge:earned', () => {
            this.checkAndHideBlocks();
        });

        // Écouter les changements de données
        document.addEventListener('arkalia:unified:synced', (e) => {
            this.checkAndHideBlocks(e.detail.playerData);
        });

        // Observer les changements dans le DOM
        this.setupMutationObserver();
    }

    setupMutationObserver() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (this.isReadyBlock(node)) {
                            this.readyBlocks.add(node);
                        }
                        
                        // Vérifier les enfants
                        const children = node.querySelectorAll ? node.querySelectorAll('*') : [];
                        children.forEach(child => {
                            if (this.isReadyBlock(child)) {
                                this.readyBlocks.add(child);
                            }
                        });
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    startChecking() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }

        this.checkInterval = setInterval(() => {
            this.checkAndHideBlocks();
        }, this.checkFrequency);
    }

    async checkAndHideBlocks(playerData = null) {
        // Récupérer les données si pas fournies
        if (!playerData) {
            try {
                const response = await fetch('/api/progression-data');
                const data = await response.json();
                playerData = data.progression;
            } catch (error) {
                console.warn('⚠️ Impossible de récupérer les données de progression:', error);
                return;
            }
        }

        // Vérifier si l'utilisateur a des données
        const hasData = this.userHasData(playerData);

        if (hasData) {
            this.hideReadyBlocks();
        } else {
            this.showReadyBlocks();
        }
    }

    userHasData(playerData) {
        if (!playerData) return false;

        // Vérifier les critères de données
        const criteria = [
            playerData.xp > 0,
            playerData.score > 0,
            playerData.coins > 0,
            playerData.badges && playerData.badges.length > 0,
            playerData.missions_completed && playerData.missions_completed.length > 0,
            playerData.skills && Object.keys(playerData.skills).length > 0,
            playerData.stats && (
                playerData.stats.total_commands > 0 ||
                playerData.stats.total_luna_commands > 0 ||
                playerData.stats.total_mini_games > 0 ||
                playerData.stats.total_zones_explored > 0
            )
        ];

        return criteria.some(criterion => criterion);
    }

    hideReadyBlocks() {
        this.readyBlocks.forEach(block => {
            if (!this.hiddenBlocks.has(block)) {
                this.hideBlock(block);
                this.hiddenBlocks.add(block);
            }
        });
    }

    showReadyBlocks() {
        this.hiddenBlocks.forEach(block => {
            this.showBlock(block);
            this.hiddenBlocks.delete(block);
        });
    }

    hideBlock(block) {
        // Ajouter une classe pour l'animation
        block.classList.add('hiding-ready-block');
        
        // Animation de sortie
        block.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
        block.style.opacity = '0';
        block.style.transform = 'translateY(-20px)';
        
        // Masquer complètement après l'animation
        setTimeout(() => {
            block.style.display = 'none';
            block.classList.add('ready-block-hidden');
        }, 500);
    }

    showBlock(block) {
        // Retirer les classes de masquage
        block.classList.remove('hiding-ready-block', 'ready-block-hidden');
        
        // Réinitialiser les styles
        block.style.display = '';
        block.style.opacity = '';
        block.style.transform = '';
        block.style.transition = '';
        
        // Animation d'entrée
        setTimeout(() => {
            block.style.transition = 'opacity 0.5s ease-in, transform 0.5s ease-in';
            block.style.opacity = '1';
            block.style.transform = 'translateY(0)';
        }, 10);
    }

    // Méthodes publiques
    forceCheck() {
        this.checkAndHideBlocks();
    }

    reset() {
        this.showReadyBlocks();
        this.hiddenBlocks.clear();
        console.log('🔄 États "Prêt à commencer !" réinitialisés');
    }

    getStats() {
        return {
            totalReadyBlocks: this.readyBlocks.size,
            hiddenBlocks: this.hiddenBlocks.size,
            visibleBlocks: this.readyBlocks.size - this.hiddenBlocks.size
        };
    }

    addReadyBlock(element) {
        if (this.isReadyBlock(element)) {
            this.readyBlocks.add(element);
            console.log('➕ Nouveau bloc "Prêt à commencer !" ajouté');
        }
    }

    removeReadyBlock(element) {
        this.readyBlocks.delete(element);
        this.hiddenBlocks.delete(element);
        console.log('➖ Bloc "Prêt à commencer !" supprimé');
    }
}

// Initialiser le gestionnaire d'états
window.readyStateManager = new ReadyStateManager();

// Exporter pour les modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReadyStateManager;
}
