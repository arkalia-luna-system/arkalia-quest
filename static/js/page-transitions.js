/* ===== ARKALIA QUEST - PAGE TRANSITIONS ===== */
/* Système d'animations de transition entre les pages */

class PageTransitions {
    constructor() {
        this.transitionDuration = 500;
        this.isTransitioning = false;
        this.transitionQueue = [];
        this.currentTransition = null;
        this.init();
    }

    init() {
        this.createTransitionOverlay();
        this.setupEventListeners();
        this.setupNavigationInterception();
        // console.log('🎬 Page Transitions initialisé');
    }

    createTransitionOverlay() {
        // Créer l'overlay de transition
        this.overlay = document.createElement('div');
        this.overlay.id = 'page-transition-overlay';
        this.overlay.className = 'page-transition-overlay';

        this.overlay.innerHTML = `
            <div class="transition-content">
                <div class="transition-logo">ARKALIA QUEST</div>
                <div class="transition-loading">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">Chargement...</div>
                </div>
                <div class="transition-progress">
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                </div>
            </div>
        `;

        // Ajouter les styles
        this.addStyles();

        // Ajouter au DOM
        document.body.appendChild(this.overlay);
    }

    addStyles() {
        if (document.getElementById('page-transitions-styles')) return;

        const style = document.createElement('style');
        style.id = 'page-transitions-styles';
        style.textContent = `
            .page-transition-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, rgba(9, 9, 11, 0.98) 0%, rgba(30, 30, 40, 0.98) 100%);
                backdrop-filter: blur(20px);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .page-transition-overlay.show {
                opacity: 1;
                visibility: visible;
            }

            .transition-content {
                text-align: center;
                color: var(--argent-holographique);
                font-family: 'IBM Plex Mono', monospace;
            }

            .transition-logo {
                font-size: 2.5em;
                font-weight: 700;
                color: var(--violet-lunaire);
                text-shadow: 0 0 30px rgba(167, 139, 250, 0.6);
                margin-bottom: 30px;
                animation: logoGlow 2s ease-in-out infinite;
            }

            @keyframes logoGlow {
                0%, 100% {
                    text-shadow: 0 0 30px rgba(167, 139, 250, 0.6);
                }
                50% {
                    text-shadow: 0 0 40px rgba(167, 139, 250, 0.8);
                }
            }

            .transition-loading {
                margin-bottom: 30px;
            }

            .loading-spinner {
                width: 50px;
                height: 50px;
                border: 3px solid rgba(167, 139, 250, 0.3);
                border-top: 3px solid var(--violet-lunaire);
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .loading-text {
                font-size: 1.1em;
                color: var(--argent-holographique);
                animation: textPulse 1.5s ease-in-out infinite;
            }

            @keyframes textPulse {
                0%, 100% {
                    opacity: 0.7;
                }
                50% {
                    opacity: 1;
                }
            }

            .transition-progress {
                width: 300px;
                margin: 0 auto;
            }

            .progress-bar {
                width: 100%;
                height: 4px;
                background: rgba(167, 139, 250, 0.2);
                border-radius: 2px;
                overflow: hidden;
                border: 1px solid rgba(167, 139, 250, 0.3);
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
                border-radius: 2px;
                width: 0%;
                transition: width 0.3s ease;
                position: relative;
                box-shadow: 0 0 10px rgba(167, 139, 250, 0.5);
            }

            .progress-fill::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                animation: progressShine 1.5s ease-in-out infinite;
            }

            @keyframes progressShine {
                0% { transform: translateX(-100%); }
                50% { transform: translateX(100%); }
                100% { transform: translateX(100%); }
            }

            /* Animations de transition */
            .page-transition-overlay.slide-in {
                animation: slideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .page-transition-overlay.slide-out {
                animation: slideOut 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            }

            @keyframes slideIn {
                from {
                    transform: translateY(-100%);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }

            @keyframes slideOut {
                from {
                    transform: translateY(0);
                    opacity: 1;
                }
                to {
                    transform: translateY(100%);
                    opacity: 0;
                }
            }

            /* Responsive */
            @media (max-width: 768px) {
                .transition-logo {
                    font-size: 2em;
                }

                .transition-progress {
                    width: 250px;
                }
            }

            @media (max-width: 480px) {
                .transition-logo {
                    font-size: 1.8em;
                }

                .transition-progress {
                    width: 200px;
                }
            }
        `;

        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Écouter les changements de page
        window.addEventListener('beforeunload', () => {
            this.hideTransition();
        });

        // Écouter les événements de navigation
        document.addEventListener('arkalia:navigation:change', (event) => {
            this.handleNavigationChange(event.detail);
        });
    }

    setupNavigationInterception() {
        // Intercepter les clics sur les liens de navigation
        document.addEventListener('click', (event) => {
            const link = event.target.closest('a[href]');
            if (link && this.isInternalLink(link.href)) {
                event.preventDefault();
                this.navigateTo(link.href);
            }
        });

        // Intercepter les changements d'historique
        window.addEventListener('popstate', () => {
            this.handlePopState();
        });
    }

    isInternalLink(url) {
        try {
            const linkUrl = new URL(url, window.location.origin);
            return linkUrl.origin === window.location.origin;
        } catch {
            return false;
        }
    }

    async navigateTo(url) {
        if (this.isTransitioning) {
            this.transitionQueue.push(url);
            return;
        }

        this.isTransitioning = true;
        this.currentTransition = url;

        try {
            // Afficher la transition
            await this.showTransition();

            // Charger la nouvelle page
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // Extraire le contenu principal
            const newContent = doc.querySelector('main, #main-content, .main-content');
            const currentContent = document.querySelector('main, #main-content, .main-content');

            if (newContent && currentContent) {
                // Mettre à jour le contenu
                currentContent.innerHTML = newContent.innerHTML;
            }

            // Mettre à jour l'URL
            window.history.pushState({}, '', url);

            // Déclencher l'événement de changement de page
            this.dispatchNavigationEvent(url);

        } catch (error) {
            console.error('❌ Erreur navigation:', error);
            // Rediriger vers la page en cas d'erreur
            window.location.href = url;
        } finally {
            // Masquer la transition
            await this.hideTransition();
            this.isTransitioning = false;
            this.currentTransition = null;

            // Traiter la queue
            this.processQueue();
        }
    }

    async showTransition() {
        this.overlay.classList.add('show', 'slide-in');
        this.overlay.classList.remove('slide-out');

        // Animation de progression
        await this.animateProgress();

        return new Promise(resolve => {
            setTimeout(resolve, this.transitionDuration);
        });
    }

    async hideTransition() {
        this.overlay.classList.add('slide-out');
        this.overlay.classList.remove('slide-in');

        return new Promise(resolve => {
            setTimeout(() => {
                this.overlay.classList.remove('show', 'slide-out');
                resolve();
            }, this.transitionDuration);
        });
    }

    async animateProgress() {
        const progressFill = this.overlay.querySelector('.progress-fill');
        if (!progressFill) return;

        // Animation de progression
        for (let i = 0; i <= 100; i += 10) {
            progressFill.style.width = `${i}%`;
            await new Promise(resolve => setTimeout(resolve, 50));
        }
    }

    handleNavigationChange(detail) {
        // Mettre à jour le texte de chargement selon la page
        const loadingText = this.overlay.querySelector('.loading-text');
        if (loadingText) {
            const pageNames = {
                '/': 'Accueil',
                '/terminal': 'Terminal',
                '/monde': 'Monde',
                '/profil': 'Profil',
                '/dashboard': 'Dashboard',
                '/leaderboard': 'Classement'
            };

            const pageName = pageNames[detail.url] || 'Page';
            loadingText.textContent = `Chargement ${pageName}...`;
        }
    }

    handlePopState() {
        // Gérer le retour en arrière
        this.hideTransition();
    }

    dispatchNavigationEvent(url) {
        const event = new CustomEvent('arkalia:navigation:change', {
            detail: { url, timestamp: Date.now() }
        });
        document.dispatchEvent(event);
    }

    processQueue() {
        if (this.transitionQueue.length > 0) {
            const nextUrl = this.transitionQueue.shift();
            this.navigateTo(nextUrl);
        }
    }

    // Méthodes publiques
    showTransitionOverlay() {
        this.overlay.classList.add('show');
    }

    hideTransitionOverlay() {
        this.overlay.classList.remove('show');
    }

    setTransitionDuration(duration) {
        this.transitionDuration = duration;
    }

    // Méthode pour forcer une transition
    forceTransition(url) {
        this.navigateTo(url);
    }

    // Méthode pour détruire le système
    destroy() {
        if (this.overlay && this.overlay.parentNode) {
            this.overlay.parentNode.removeChild(this.overlay);
        }
    }
}

// Initialiser le système de transitions
document.addEventListener('DOMContentLoaded', () => {
    window.pageTransitions = new PageTransitions();
});

// Exporter pour utilisation globale
window.PageTransitions = PageTransitions;
