/* ===== ARKALIA QUEST - PERFORMANCE & UX OPTIMIZER ===== */

class PerformanceUXOptimizer {
    constructor() {
        this.loadingStates = new Map();
        this.buttonStates = new Map();
        this.animationQueue = [];
        this.isProcessing = false;
        this.debounceTimers = new Map();
        this.rafId = null;

        this.init();
    }

    init() {
        this.setupLoadingStates();
        this.setupButtonFeedback();
        this.setupAccessibilityOptimizations();
        this.setupLunaResponseVariety();
        this.setupVisualOptimizations();
        this.setupResponsiveOptimizations();
        this.setupProgressionUpdates();
        this.setupMicroAnimations();

        console.log('🚀 Performance & UX Optimizer initialisé');
    }

    // ===== LOADING STATES & ANIMATIONS =====
    setupLoadingStates() {
        // Créer les spinners de chargement
        this.createLoadingSpinners();

        // Intercepter les changements de page
        this.interceptPageChanges();

        // Optimiser les transitions
        this.optimizeTransitions();
    }

    createLoadingSpinners() {
        const spinnerHTML = `
            <div id="arkalia-loading-overlay" class="loading-overlay hidden">
                <div class="loading-spinner">
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                    <div class="loading-text">Chargement...</div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', spinnerHTML);

        // Styles pour le spinner
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
                justify-content: center;
                align-items: center;
                z-index: 10000;
                transition: opacity 0.3s ease;
            }
            
            .loading-overlay.hidden {
                opacity: 0;
                pointer-events: none;
            }
            
            .loading-spinner {
                text-align: center;
                color: #00ff00;
            }
            
            .spinner-ring {
                width: 40px;
                height: 40px;
                border: 4px solid rgba(0, 255, 0, 0.3);
                border-top: 4px solid #00ff00;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 10px auto;
            }
            
            .spinner-ring:nth-child(2) {
                animation-delay: 0.2s;
                width: 30px;
                height: 30px;
            }
            
            .spinner-ring:nth-child(3) {
                animation-delay: 0.4s;
                width: 20px;
                height: 20px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .loading-text {
                margin-top: 20px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: #00ff00;
                text-shadow: 0 0 10px #00ff00;
            }
        `;
        document.head.appendChild(style);
    }

    showLoading(message = 'Chargement...') {
        const overlay = document.getElementById('arkalia-loading-overlay');
        const text = overlay.querySelector('.loading-text');

        if (text) text.textContent = message;
        overlay.classList.remove('hidden');
    }

    hideLoading() {
        const overlay = document.getElementById('arkalia-loading-overlay');
        overlay.classList.add('hidden');
    }

    interceptPageChanges() {
        // Intercepter les changements de page
        const originalPushState = history.pushState;
        const originalReplaceState = history.replaceState;

        history.pushState = (...args) => {
            this.showLoading('Chargement de la page...');
            originalPushState.apply(history, args);
            setTimeout(() => this.hideLoading(), 300);
        };

        history.replaceState = (...args) => {
            this.showLoading('Mise à jour...');
            originalReplaceState.apply(history, args);
            setTimeout(() => this.hideLoading(), 200);
        };
    }

    // ===== BOUTON FEEDBACK & CONFIRMATION =====
    setupButtonFeedback() {
        // Améliorer le feedback des boutons
        document.addEventListener('click', (e) => {
            if (e.target.matches('button, .btn, .quick-btn, [role="button"]')) {
                this.enhanceButtonFeedback(e.target);
            }
        });

        // Feedback visuel pour les changements d'état
        this.setupStateChangeFeedback();
    }

    enhanceButtonFeedback(button) {
        // Éviter le spam de clics
        if (button.dataset.processing === 'true') return;

        button.dataset.processing = 'true';

        // Animation de pression
        button.style.transform = 'scale(0.95)';
        button.style.transition = 'transform 0.1s ease';

        // Feedback sonore si disponible
        if (window.hackingEffects) {
            window.hackingEffects.playClickSound();
        }

        // Restaurer l'état
        setTimeout(() => {
            button.style.transform = 'scale(1)';
            button.dataset.processing = 'false';
        }, 150);

        // Confirmation visuelle
        this.showButtonConfirmation(button);
    }

    showButtonConfirmation(button) {
        const confirmation = document.createElement('div');
        confirmation.className = 'button-confirmation';
        confirmation.textContent = '✓';
        confirmation.style.cssText = `
            position: absolute;
            top: -10px;
            right: -10px;
            background: #00ff00;
            color: #000;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            animation: confirmationPulse 0.5s ease;
            z-index: 1000;
        `;

        // Ajouter l'animation CSS
        if (!document.getElementById('confirmation-animation')) {
            const style = document.createElement('style');
            style.id = 'confirmation-animation';
            style.textContent = `
                @keyframes confirmationPulse {
                    0% { transform: scale(0); opacity: 0; }
                    50% { transform: scale(1.2); opacity: 1; }
                    100% { transform: scale(1); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        button.style.position = 'relative';
        button.appendChild(confirmation);

        setTimeout(() => {
            if (confirmation.parentNode) {
                confirmation.parentNode.removeChild(confirmation);
            }
        }, 500);
    }

    // ===== OPTIMISATIONS ACCESSIBILITÉ =====
    setupAccessibilityOptimizations() {
        // Optimiser les changements de mode sombre
        this.optimizeDarkModeTransitions();

        // Améliorer les changements de contraste
        this.optimizeContrastChanges();

        // Optimiser les changements de taille de texte
        this.optimizeTextSizeChanges();
    }

    optimizeDarkModeTransitions() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const target = mutation.target;
                    if (target.classList.contains('dark-mode')) {
                        this.smoothDarkModeTransition(target);
                    }
                }
            });
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
        });
    }

    smoothDarkModeTransition(element) {
        // Ajouter une transition fluide
        element.style.transition = 'background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease';

        // Forcer un reflow
        element.offsetHeight;

        // Supprimer la transition après l'animation
        setTimeout(() => {
            element.style.transition = '';
        }, 300);
    }

    optimizeContrastChanges() {
        // Détecter les changements de contraste
        const contrastObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const target = mutation.target;
                    if (target.classList.contains('high-contrast')) {
                        this.smoothContrastTransition(target);
                    }
                }
            });
        });

        contrastObserver.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
        });
    }

    smoothContrastTransition(element) {
        // Transition fluide pour le contraste
        element.style.transition = 'filter 0.3s ease, contrast 0.3s ease';

        // Forcer un reflow
        element.offsetHeight;

        // Supprimer la transition après l'animation
        setTimeout(() => {
            element.style.transition = '';
        }, 300);
    }

    // ===== VARIÉTÉ DES RÉPONSES LUNA =====
    setupLunaResponseVariety() {
        this.lunaResponseHistory = [];
        this.maxHistorySize = 10;

        // Intercepter les réponses LUNA
        this.interceptLunaResponses();
    }

    interceptLunaResponses() {
        // Écouter les événements de réponse LUNA
        document.addEventListener('lunaResponse', (e) => {
            this.enhanceLunaResponse(e.detail);
        });

        // Intercepter les réponses du terminal
        this.interceptTerminalResponses();
    }

    interceptTerminalResponses() {
        const originalAddMessage = window.addMessage;
        if (originalAddMessage) {
            window.addMessage = (message, type = 'system') => {
                if (type === 'luna' || message.includes('LUNA:')) {
                    this.enhanceLunaResponse(message);
                }
                return originalAddMessage(message, type);
            };
        }
    }

    enhanceLunaResponse(message) {
        // Ajouter de la variété aux réponses
        const enhancedMessage = this.addResponseVariety(message);

        // Ajouter des émotions
        this.addEmotionalContext(enhancedMessage);

        // Historique pour éviter les répétitions
        this.lunaResponseHistory.push(message);
        if (this.lunaResponseHistory.length > this.maxHistorySize) {
            this.lunaResponseHistory.shift();
        }
    }

    addResponseVariety(message) {
        // Ajouter des variations subtiles
        const variations = [
            '🌟 ' + message,
            '✨ ' + message,
            '🚀 ' + message,
            '💫 ' + message
        ];

        // Choisir une variation aléatoire
        const randomVariation = variations[Math.floor(Math.random() * variations.length)];

        return randomVariation;
    }

    addEmotionalContext(message) {
        // Ajouter du contexte émotionnel
        const emotionalPrefixes = [
            'Avec enthousiasme, ',
            'En souriant, ',
            'Avec curiosité, ',
            'En s\'illuminant, ',
            'Avec bienveillance, '
        ];

        const randomPrefix = emotionalPrefixes[Math.floor(Math.random() * emotionalPrefixes.length)];

        return randomPrefix + message;
    }

    // ===== OPTIMISATIONS VISUELLES =====
    setupVisualOptimizations() {
        // Optimiser les transitions de page
        this.optimizePageTransitions();

        // Réduire les lags visuels
        this.reduceVisualLags();

        // Optimiser les animations
        this.optimizeAnimations();
    }

    optimizePageTransitions() {
        // Ajouter des transitions fluides entre les pages
        document.addEventListener('DOMContentLoaded', () => {
            document.body.style.transition = 'opacity 0.3s ease';
        });

        // Intercepter les changements de contenu
        this.interceptContentChanges();
    }

    interceptContentChanges() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    this.animateNewContent(mutation.addedNodes);
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    animateNewContent(nodes) {
        nodes.forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                node.style.opacity = '0';
                node.style.transform = 'translateY(20px)';
                node.style.transition = 'opacity 0.3s ease, transform 0.3s ease';

                requestAnimationFrame(() => {
                    node.style.opacity = '1';
                    node.style.transform = 'translateY(0)';
                });
            }
        });
    }

    // ===== OPTIMISATIONS RESPONSIVE =====
    setupResponsiveOptimizations() {
        // Améliorer le responsive sur tailles extrêmes
        this.optimizeExtremeSizes();

        // Améliorer la navigation clavier
        this.optimizeKeyboardNavigation();
    }

    optimizeExtremeSizes() {
        // Détecter les tailles extrêmes
        const checkSize = () => {
            const width = window.innerWidth;
            const height = window.innerHeight;

            if (width < 320 || height < 480) {
                this.enableMobileOptimizations();
            } else if (width > 1920 || height > 1080) {
                this.enableLargeScreenOptimizations();
            }
        };

        window.addEventListener('resize', this.debounce(checkSize, 250));
        checkSize();
    }

    enableMobileOptimizations() {
        document.body.classList.add('mobile-optimized');

        // Ajuster les tableaux pour mobile
        const tables = document.querySelectorAll('table');
        tables.forEach(table => {
            table.style.fontSize = '12px';
            table.style.overflowX = 'auto';
        });
    }

    enableLargeScreenOptimizations() {
        document.body.classList.add('large-screen-optimized');

        // Ajuster pour les grands écrans
        const containers = document.querySelectorAll('.container, .content');
        containers.forEach(container => {
            container.style.maxWidth = '1400px';
            container.style.margin = '0 auto';
        });
    }

    // ===== MISE À JOUR DE PROGRESSION =====
    setupProgressionUpdates() {
        // Optimiser la mise à jour des compteurs
        this.optimizeCounterUpdates();

        // Améliorer la synchronisation des données
        this.improveDataSynchronization();
    }

    optimizeCounterUpdates() {
        // Utiliser requestAnimationFrame pour les mises à jour
        this.updateCounters = this.throttle(() => {
            this.updateAllCounters();
        }, 100);

        // Écouter les changements de progression
        document.addEventListener('progressionUpdate', this.updateCounters);
    }

    updateAllCounters() {
        // Mettre à jour tous les compteurs de manière optimisée
        const counters = document.querySelectorAll('[data-counter]');
        counters.forEach(counter => {
            this.animateCounter(counter);
        });
    }

    animateCounter(counter) {
        const targetValue = parseInt(counter.dataset.counter);
        const currentValue = parseInt(counter.textContent) || 0;

        if (targetValue !== currentValue) {
            this.animateNumber(counter, currentValue, targetValue, 500);
        }
    }

    animateNumber(element, start, end, duration) {
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const current = Math.round(start + (end - start) * progress);
            element.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    // ===== MICRO-ANIMATIONS =====
    setupMicroAnimations() {
        // Ajouter des micro-animations pour les récompenses
        this.addRewardAnimations();

        // Améliorer les animations de badge
        this.enhanceBadgeAnimations();
    }

    addRewardAnimations() {
        // Écouter les événements de récompense
        document.addEventListener('rewardEarned', (e) => {
            this.showRewardAnimation(e.detail);
        });

        document.addEventListener('badgeUnlocked', (e) => {
            this.showBadgeAnimation(e.detail);
        });
    }

    showRewardAnimation(reward) {
        const animation = document.createElement('div');
        animation.className = 'reward-animation';
        animation.innerHTML = `
            <div class="reward-content">
                <div class="reward-icon">${reward.icon || '🎉'}</div>
                <div class="reward-text">${reward.text || 'Récompense obtenue!'}</div>
            </div>
        `;

        animation.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(45deg, #00ff00, #00ffff);
            color: #000;
            padding: 20px;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
            z-index: 10000;
            animation: rewardPulse 2s ease;
        `;

        // Ajouter l'animation CSS
        if (!document.getElementById('reward-animation')) {
            const style = document.createElement('style');
            style.id = 'reward-animation';
            style.textContent = `
                @keyframes rewardPulse {
                    0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
                    50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
                    100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(animation);

        setTimeout(() => {
            if (animation.parentNode) {
                animation.parentNode.removeChild(animation);
            }
        }, 2000);
    }

    showBadgeAnimation(badge) {
        const animation = document.createElement('div');
        animation.className = 'badge-animation';
        animation.innerHTML = `
            <div class="badge-content">
                <div class="badge-icon">${badge.icon || '🏆'}</div>
                <div class="badge-text">${badge.name || 'Badge débloqué!'}</div>
            </div>
        `;

        animation.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #ffa500, #ffff00);
            color: #000;
            padding: 15px;
            border-radius: 50px;
            font-weight: bold;
            text-align: center;
            z-index: 10000;
            animation: badgeSlide 3s ease;
        `;

        // Ajouter l'animation CSS
        if (!document.getElementById('badge-animation')) {
            const style = document.createElement('style');
            style.id = 'badge-animation';
            style.textContent = `
                @keyframes badgeSlide {
                    0% { transform: translateX(100%); opacity: 0; }
                    20% { transform: translateX(0); opacity: 1; }
                    80% { transform: translateX(0); opacity: 1; }
                    100% { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(animation);

        setTimeout(() => {
            if (animation.parentNode) {
                animation.parentNode.removeChild(animation);
            }
        }, 3000);
    }

    // ===== UTILITAIRES =====
    debounce(func, wait) {
        return (...args) => {
            clearTimeout(this.debounceTimers.get(func));
            this.debounceTimers.set(func, setTimeout(() => func.apply(this, args), wait));
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return (...args) => {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // ===== MÉTHODES PUBLIQUES =====
    showLoading(message) {
        this.showLoading(message);
    }

    hideLoading() {
        this.hideLoading();
    }

    triggerReward(reward) {
        document.dispatchEvent(new CustomEvent('rewardEarned', { detail: reward }));
    }

    triggerBadge(badge) {
        document.dispatchEvent(new CustomEvent('badgeUnlocked', { detail: badge }));
    }

    updateProgression(data) {
        document.dispatchEvent(new CustomEvent('progressionUpdate', { detail: data }));
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.performanceUXOptimizer = new PerformanceUXOptimizer();
});

// Export pour utilisation externe
window.PerformanceUXOptimizer = PerformanceUXOptimizer;
