/* ===== ARKALIA QUEST - LOADING MANAGER ===== */

class LoadingManager {
    constructor() {
        this.activeLoaders = new Map();
        this.loaderTypes = {
            'matrix': 'matrix-loader',
            'cyber': 'cyber-loader',
            'luna': 'luna-loader',
            'terminal': 'terminal-loader',
            'progressive': 'progressive-loader',
            'section': 'section-loader',
            'data': 'data-loader',
            'game': 'game-loader',
            'success': 'success-loader',
            'error': 'error-loader'
        };
        this.init();
    }

    init() {
        console.log('🔄 Loading Manager initialisé');
        this.setupGlobalStyles();
    }

    setupGlobalStyles() {
        // Ajouter les styles globaux pour les loaders
        const style = document.createElement('style');
        style.textContent = `
            .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                backdrop-filter: blur(5px);
            }
            
            .loading-container {
                background: rgba(0, 0, 0, 0.9);
                border: 2px solid var(--violet-lunaire);
                border-radius: 12px;
                padding: 30px;
                text-align: center;
                box-shadow: 0 0 30px rgba(167, 139, 250, 0.5);
            }
            
            .loading-text {
                color: var(--violet-lunaire);
                font-family: 'IBM Plex Mono', monospace;
                font-size: 1.2em;
                margin-top: 20px;
                animation: loadingPulse 2s ease-in-out infinite;
            }
            
            @keyframes loadingPulse {
                0%, 100% { opacity: 0.7; }
                50% { opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    // Afficher un loader
    showLoader(elementId, type = 'matrix', message = 'Chargement...', options = {}) {
        const element = document.getElementById(elementId);
        if (!element) {
            console.error(`Élément ${elementId} non trouvé`);
            return;
        }

        // Créer le loader
        const loader = this.createLoader(type, message, options);
        loader.id = `loader-${elementId}`;

        // Masquer le contenu original
        element.style.position = 'relative';
        element.style.overflow = 'hidden';

        // Ajouter le loader
        element.appendChild(loader);

        // Enregistrer le loader actif
        this.activeLoaders.set(elementId, {
            element: element,
            loader: loader,
            type: type,
            message: message,
            options: options
        });

        // Animation d'entrée
        setTimeout(() => {
            loader.classList.add('loader-fade-in');
        }, 10);

        return loader;
    }

    // Masquer un loader
    hideLoader(elementId) {
        const loaderData = this.activeLoaders.get(elementId);
        if (!loaderData) {
            console.warn(`Aucun loader actif pour ${elementId}`);
            return;
        }

        const { element, loader } = loaderData;

        // Animation de sortie
        loader.classList.add('loader-fade-out');

        setTimeout(() => {
            if (loader.parentNode) {
                loader.parentNode.removeChild(loader);
            }
            this.activeLoaders.delete(elementId);
        }, 300);
    }

    // Créer un loader selon le type
    createLoader(type, message, options) {
        const loader = document.createElement('div');
        loader.className = `loader-container ${this.loaderTypes[type] || 'matrix-loader'}`;

        switch (type) {
            case 'matrix':
                loader.innerHTML = `
                    <div class="matrix-loader"></div>
                    <div class="loading-text">${message}</div>
                `;
                break;

            case 'cyber':
                loader.innerHTML = `
                    <div class="cyber-loader">
                        <div class="cyber-ring"></div>
                        <div class="cyber-ring"></div>
                        <div class="cyber-ring"></div>
                    </div>
                    <div class="loading-text">${message}</div>
                `;
                break;

            case 'luna':
                loader.innerHTML = `
                    <div class="luna-loader">
                        <div class="luna-core"></div>
                        <div class="luna-orbit"></div>
                        <div class="luna-orbit"></div>
                        <div class="luna-orbit"></div>
                    </div>
                    <div class="loading-text">${message}</div>
                `;
                break;

            case 'terminal':
                loader.innerHTML = `
                    <div class="terminal-loader">
                        <div class="terminal-text">${message}</div>
                        <div class="terminal-cursor"></div>
                    </div>
                `;
                break;

            case 'progressive':
                loader.innerHTML = `
                    <div class="progressive-loader">
                        <div class="progress-bar"></div>
                    </div>
                    <div class="loading-text">${message}</div>
                `;
                break;

            case 'section':
                loader.innerHTML = `
                    <div class="section-loader">
                        <div class="loader-icon">${options.icon || '🔄'}</div>
                        <div class="loader-text">${message}</div>
                    </div>
                `;
                break;

            case 'data':
                loader.innerHTML = `
                    <div class="data-loader">
                        <div class="data-dots">
                            <div class="data-dot"></div>
                            <div class="data-dot"></div>
                            <div class="data-dot"></div>
                        </div>
                        <div class="loading-text">${message}</div>
                    </div>
                `;
                break;

            case 'game':
                loader.innerHTML = `
                    <div class="game-loader">
                        <div class="game-icon">${options.icon || '🎮'}</div>
                        <div class="game-text">${message}</div>
                    </div>
                `;
                break;

            case 'success':
                loader.innerHTML = `
                    <div class="success-loader">
                        <div class="success-check"></div>
                    </div>
                    <div class="loading-text">${message}</div>
                `;
                break;

            case 'error':
                loader.innerHTML = `
                    <div class="error-loader">
                        <div class="error-x"></div>
                    </div>
                    <div class="loading-text">${message}</div>
                `;
                break;

            default:
                loader.innerHTML = `
                    <div class="matrix-loader"></div>
                    <div class="loading-text">${message}</div>
                `;
        }

        return loader;
    }

    // Afficher un loader en overlay
    showOverlayLoader(type = 'luna', message = 'Chargement...', options = {}) {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.id = 'loading-overlay';

        const container = document.createElement('div');
        container.className = 'loading-container';

        const loader = this.createLoader(type, message, options);
        container.appendChild(loader);
        overlay.appendChild(container);

        document.body.appendChild(overlay);

        // Animation d'entrée
        setTimeout(() => {
            overlay.style.opacity = '1';
        }, 10);

        return overlay;
    }

    // Masquer le loader overlay
    hideOverlayLoader() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => {
                if (overlay.parentNode) {
                    overlay.parentNode.removeChild(overlay);
                }
            }, 300);
        }
    }

    // Afficher un loader de progression
    showProgressLoader(elementId, message = 'Chargement...', duration = 3000) {
        const loader = this.showLoader(elementId, 'progressive', message);

        // Simuler la progression
        const progressBar = loader.querySelector('.progress-bar');
        if (progressBar) {
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 100) progress = 100;

                progressBar.style.width = progress + '%';

                if (progress >= 100) {
                    clearInterval(interval);
                    setTimeout(() => {
                        this.hideLoader(elementId);
                    }, 500);
                }
            }, 100);
        }

        return loader;
    }

    // Afficher un loader de succès
    showSuccessLoader(elementId, message = 'Succès !') {
        const loader = this.showLoader(elementId, 'success', message);

        setTimeout(() => {
            this.hideLoader(elementId);
        }, 2000);

        return loader;
    }

    // Afficher un loader d'erreur
    showErrorLoader(elementId, message = 'Erreur !') {
        const loader = this.showLoader(elementId, 'error', message);

        setTimeout(() => {
            this.hideLoader(elementId);
        }, 3000);

        return loader;
    }

    // Remplacer automatiquement les messages "Chargement..."
    replaceLoadingMessages() {
        const loadingElements = document.querySelectorAll('[class*="loading"], [id*="loading"]');

        loadingElements.forEach(element => {
            if (element.textContent.includes('Chargement') || element.textContent.includes('Loading')) {
                const parent = element.closest('[id]');
                if (parent) {
                    this.showLoader(parent.id, 'matrix', 'Chargement...');
                }
            }
        });
    }

    // Afficher un loader contextuel selon la section
    showContextualLoader(section, message) {
        const contextualMessages = {
            'dashboard': 'Analyse des données...',
            'profil': 'Chargement du profil...',
            'monde': 'Exploration des zones...',
            'terminal': 'Initialisation du terminal...',
            'leaderboard': 'Mise à jour du classement...',
            'tutorial': 'Préparation du tutoriel...',
            'mini-games': 'Chargement des mini-jeux...',
            'missions': 'Synchronisation des missions...'
        };

        const contextualTypes = {
            'dashboard': 'data',
            'profil': 'luna',
            'monde': 'cyber',
            'terminal': 'terminal',
            'leaderboard': 'progressive',
            'tutorial': 'section',
            'mini-games': 'game',
            'missions': 'matrix'
        };

        const loaderMessage = message || contextualMessages[section] || 'Chargement...';
        const loaderType = contextualTypes[section] || 'matrix';

        return this.showOverlayLoader(loaderType, loaderMessage, {
            icon: this.getContextualIcon(section)
        });
    }

    // Obtenir l'icône contextuelle
    getContextualIcon(section) {
        const icons = {
            'dashboard': '📊',
            'profil': '👤',
            'monde': '🌍',
            'terminal': '💻',
            'leaderboard': '🏆',
            'tutorial': '🎯',
            'mini-games': '🎮',
            'missions': '🎯'
        };

        return icons[section] || '🔄';
    }

    // Nettoyer tous les loaders
    cleanup() {
        this.activeLoaders.forEach((loaderData, elementId) => {
            this.hideLoader(elementId);
        });
        this.hideOverlayLoader();
    }
}

// Initialiser le gestionnaire de chargement
window.loadingManager = new LoadingManager();

// Remplacer automatiquement les messages de chargement au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Attendre un peu pour que tous les éléments soient chargés
    setTimeout(() => {
        window.loadingManager.replaceLoadingMessages();
    }, 1000);
});

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LoadingManager;
}
