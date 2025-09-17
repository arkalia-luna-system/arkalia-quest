/**
 * Système de feedback universel pour Arkalia Quest
 * Gère les notifications, animations et retours utilisateur
 */

class UniversalFeedback {
    constructor() {
        this.container = null;
        this.animations = new Map();
        this.audioEnabled = true;
        this.autoHideDelay = 5000;
        this.debugMode = false;

        this.init();
    }

    init() {
        this.createContainer();
        this.setupEventListeners();
        this.loadAnimations();
        this.debug('UniversalFeedback initialisé');
    }

    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'universal-feedback-container';
        this.container.className = 'universal-feedback-container';
        this.container.setAttribute('role', 'region');
        this.container.setAttribute('aria-live', 'polite');
        this.container.setAttribute('aria-label', 'Notifications système');

        document.body.appendChild(this.container);
    }

    setupEventListeners() {
        // Auto-hide des notifications
        this.container.addEventListener('click', (e) => {
            if (e.target.classList.contains('feedback-close')) {
                this.hideFeedback(e.target.closest('.feedback-item'));
            }
        });

        // Raccourcis clavier
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideAllFeedback();
            }
        });
    }

    loadAnimations() {
        this.animations.set('fadeIn', {
            keyframes: [
                { opacity: 0, transform: 'translateY(-20px)' },
                { opacity: 1, transform: 'translateY(0)' }
            ],
            duration: 300,
            easing: 'ease-out'
        });

        this.animations.set('slideIn', {
            keyframes: [
                { transform: 'translateX(-100%)' },
                { transform: 'translateX(0)' }
            ],
            duration: 400,
            easing: 'ease-out'
        });

        this.animations.set('bounce', {
            keyframes: [
                { transform: 'scale(0.8)' },
                { transform: 'scale(1.1)' },
                { transform: 'scale(1)' }
            ],
            duration: 600,
            easing: 'ease-out'
        });

        this.animations.set('shake', {
            keyframes: [
                { transform: 'translateX(0)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(10px)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(10px)' },
                { transform: 'translateX(0)' }
            ],
            duration: 500,
            easing: 'ease-in-out'
        });

        this.animations.set('feedbackPulse', {
            keyframes: [
                { transform: 'scale(1)' },
                { transform: 'scale(1.05)' },
                { transform: 'scale(1)' }
            ],
            duration: 200,
            easing: 'ease-out'
        });
    }

    showFeedback(message, type = 'info', options = {}) {
        const feedbackItem = this.createFeedbackItem(message, type, options);
        this.container.appendChild(feedbackItem);

        this.animateIn(feedbackItem, options.animation || 'fadeIn');
        this.playAudio(type);

        if (options.autoHide !== false) {
            this.scheduleAutoHide(feedbackItem);
        }

        this.debug(`Feedback affiché: ${type} - ${message}`);
        return feedbackItem;
    }

    createFeedbackItem(message, type, options) {
        const item = document.createElement('div');
        item.className = `feedback-item feedback-${type}`;
        item.setAttribute('role', 'alert');
        item.setAttribute('aria-live', 'assertive');

        const icon = this.getIcon(type);
        const closeBtn = options.closable !== false ? '<button class="feedback-close" aria-label="Fermer">&times;</button>' : '';

        item.innerHTML = `
            <div class="feedback-content universal-feedback-content">
                <span class="feedback-icon">${icon}</span>
                <span class="feedback-message">${message}</span>
                ${closeBtn}
            </div>
            <div class="feedback-progress"></div>
        `;

        // Accessibilité
        item.setAttribute('tabindex', '0');

        return item;
    }

    getIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️',
            loading: '⏳',
            celebration: '🎉',
            achievement: '🏆'
        };
        return icons[type] || icons.info;
    }

    getDefaultIcon() {
        return 'ℹ️';
    }

    animateIn(element, animationName) {
        const animation = this.animations.get(animationName);
        if (!animation) return;

        element.animate(animation.keyframes, {
            duration: animation.duration,
            easing: animation.easing,
            fill: 'forwards'
        });
    }

    playAudio(type) {
        if (!this.audioEnabled) return;

        // Utiliser AudioContext pour les fréquences
        if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
            const AudioContextClass = AudioContext || webkitAudioContext;
            const audioContext = new AudioContextClass();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(this.frequencies[type] || 500, audioContext.currentTime);
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.2);
        } else {
            // Fallback audio files
            const audioMap = {
                success: 'success.mp3',
                error: 'error.mp3',
                warning: 'warning.mp3',
                info: 'info.mp3'
            };

            const audioFile = audioMap[type];
            if (audioFile) {
                const audio = new Audio(`/static/audio/${audioFile}`);
                audio.volume = 0.3;
                audio.play().catch(() => {
                    // Ignore les erreurs audio
                });
            }
        }
    }

    scheduleAutoHide(element) {
        setTimeout(() => {
            this.hideFeedback(element);
        }, this.autoHideDelay);
    }

    hideFeedback(element) {
        if (!element || !element.parentNode) return;

        element.animate([
            { opacity: 1, transform: 'translateY(0)' },
            { opacity: 0, transform: 'translateY(-20px)' }
        ], {
            duration: 200,
            easing: 'ease-in',
            fill: 'forwards'
        }).onfinish = () => {
            element.remove();
        };
    }

    hideAllFeedback() {
        const items = this.container.querySelectorAll('.feedback-item');
        items.forEach(item => this.hideFeedback(item));
    }

    clearAllFeedbacks() {
        this.hideAllFeedback();
    }

    setAudioEnabled(enabled) {
        this.audioEnabled = enabled;
        this.debug(`Audio ${enabled ? 'activé' : 'désactivé'}`);
    }

    setAutoHideDelay(delay) {
        this.autoHideDelay = delay;
        this.debug(`Auto-hide delay: ${delay}ms`);
    }

    setDebugMode(enabled) {
        this.debugMode = enabled;
        this.debug('Mode debug activé');
    }

    debug(message) {
        if (this.debugMode) {
            // console.log(`[UniversalFeedback] ${message}`);
        }
    }

    // Méthodes de feedback spécialisées
    showSuccess(message, options = {}) {
        return this.showFeedback(message, 'success', options);
    }

    showError(message, options = {}) {
        return this.showFeedback(message, 'error', { ...options, autoHide: false });
    }

    showWarning(message, options = {}) {
        return this.showFeedback(message, 'warning', options);
    }

    showInfo(message, options = {}) {
        return this.showFeedback(message, 'info', options);
    }

    showLoading(message, options = {}) {
        return this.showFeedback(message, 'loading', { ...options, autoHide: false });
    }

    showCelebration(message, options = {}) {
        return this.showFeedback(message, 'celebration', { ...options, animation: 'bounce' });
    }

    // Statistiques
    getStats() {
        return {
            totalFeedbacks: this.container.children.length,
            audioEnabled: this.audioEnabled,
            autoHideDelay: this.autoHideDelay,
            debugMode: this.debugMode
        };
    }

    getActiveFeedbacks() {
        return this.container.querySelectorAll('.feedback-item');
    }

    // Système de vibration
    vibrate(pattern = [200]) {
        if ('vibrate' in navigator) {
            navigator.vibrate(pattern);
        }
    }

    // Patterns de vibration
    vibrationPatterns = {
        success: [100, 50, 100],
        error: [200, 100, 200],
        warning: [150],
        info: [100]
    };

    // Fréquences audio
    frequencies = {
        success: 800,
        error: 400,
        warning: 600,
        info: 500
    };

    // Système de queue
    feedbackQueue = [];
    isProcessingQueue = false;

    // Méthodes d'intégration
    integrateWithNotifications() {
        this.debug('Intégration avec le système de notifications');
    }

    // Système de paramètres
    loadSettings() {
        const settings = localStorage.getItem('universalFeedbackSettings');
        if (settings) {
            const parsed = JSON.parse(settings);
            this.audioEnabled = parsed.audioEnabled || true;
            this.autoHideDelay = parsed.autoHideDelay || 5000;
            this.debugMode = parsed.debugMode || false;
        }
    }

    saveSettings() {
        const settings = {
            audioEnabled: this.audioEnabled,
            autoHideDelay: this.autoHideDelay,
            debugMode: this.debugMode
        };
        localStorage.setItem('universalFeedbackSettings', JSON.stringify(settings));
    }

    // Auto-hide amélioré
    startAutoHide(element) {
        this.scheduleAutoHide(element);
    }
}

// Instance globale
window.UniversalFeedback = UniversalFeedback;

// Auto-initialisation
document.addEventListener('DOMContentLoaded', () => {
    window.feedback = new UniversalFeedback();
    window.universalFeedback = window.feedback;
});

// Export pour les modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UniversalFeedback;
}
