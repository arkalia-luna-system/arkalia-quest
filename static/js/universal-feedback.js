// DÉLÉGATION: redirige vers universal-notifications s'il est présent
(function () {
    function delegate(type, title, content, options) {
        if (window.universalNotifications) {
            return window.universalNotifications.show({ type, title, content, ...(options || {}) });
        }
    }
    window.universalFeedback = {
        success: (t, c, o) => delegate('success', t, c, o),
        warning: (t, c, o) => delegate('warning', t, c, o),
        error: (t, c, o) => delegate('error', t, c, o),
        info: (t, c, o) => delegate('info', t, c, o)
    };
})();
/* ===== ARKALIA QUEST - UNIVERSAL FEEDBACK SYSTEM ===== */
/* Système unifié pour tous les feedbacks visuels, auditifs et haptiques */

class UniversalFeedback {
    constructor() {
        this.activeFeedbacks = new Map();
        this.feedbackQueue = [];
        this.isProcessing = false;
        this.settings = this.loadSettings();
        this.audioContext = null;
        this.init();
    }

    init() {
        this.setupGlobalStyles();
        this.setupAudioContext();
        this.setupEventListeners();
        this.setupAccessibility();
        console.log('⚡ Universal Feedback System initialisé');
    }

    loadSettings() {
        const defaultSettings = {
            visualFeedback: true,
            audioFeedback: false,
            hapticFeedback: false,
            animationDuration: 300,
            soundVolume: 0.3,
            vibrationIntensity: 'medium',
            theme: 'arkalia',
            position: 'center',
            maxConcurrentFeedbacks: 3,
            autoHideDelay: 2000
        };

        try {
            const saved = localStorage.getItem('arkalia_feedback_settings');
            return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
        } catch {
            return defaultSettings;
        }
    }

    setupGlobalStyles() {
        if (document.getElementById('universal-feedback-styles')) return;

        const style = document.createElement('style');
        style.id = 'universal-feedback-styles';
        style.textContent = `
            .universal-feedback-container {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10000;
                pointer-events: none;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }

            .universal-feedback {
                background: rgba(9, 9, 11, 0.95);
                border: 2px solid rgba(167, 139, 250, 0.6);
                border-radius: 12px;
                padding: 16px 24px;
                color: var(--argent-holographique);
                font-family: 'IBM Plex Mono', monospace;
                font-size: 1em;
                text-align: center;
                backdrop-filter: blur(15px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                transform: scale(0.8) translateY(20px);
                opacity: 0;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                pointer-events: auto;
                position: relative;
                overflow: hidden;
                min-width: 200px;
                max-width: 400px;
            }

            .universal-feedback.show {
                transform: scale(1) translateY(0);
                opacity: 1;
            }

            .universal-feedback.hide {
                transform: scale(0.8) translateY(-20px);
                opacity: 0;
            }

            .universal-feedback::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
            }

            .universal-feedback.success::before {
                background: linear-gradient(90deg, #22c55e, #16a34a);
            }

            .universal-feedback.warning::before {
                background: linear-gradient(90deg, #f59e0b, #d97706);
            }

            .universal-feedback.error::before {
                background: linear-gradient(90deg, #ef4444, #dc2626);
            }

            .universal-feedback.info::before {
                background: linear-gradient(90deg, var(--bleu-spectre), #3b82f6);
            }

            .universal-feedback.loading::before {
                background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
                animation: loadingProgress 2s linear infinite;
            }

            @keyframes loadingProgress {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }

            .universal-feedback-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .universal-feedback-icon {
                font-size: 1.5em;
                animation: feedbackPulse 0.6s ease-in-out;
            }

            @keyframes feedbackPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.2); }
            }

            .universal-feedback-text {
                flex: 1;
                font-weight: 500;
            }

            .universal-feedback-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: var(--violet-lunaire);
                transform: scaleX(0);
                transform-origin: left;
                transition: transform linear;
            }

            .universal-feedback-progress.animate {
                transform: scaleX(1);
            }

            /* Types de feedback */
            .universal-feedback.success {
                border-color: rgba(34, 197, 94, 0.6);
                background: rgba(34, 197, 94, 0.1);
            }

            .universal-feedback.warning {
                border-color: rgba(245, 158, 11, 0.6);
                background: rgba(245, 158, 11, 0.1);
            }

            .universal-feedback.error {
                border-color: rgba(239, 68, 68, 0.6);
                background: rgba(239, 68, 68, 0.1);
            }

            .universal-feedback.info {
                border-color: rgba(59, 130, 246, 0.6);
                background: rgba(59, 130, 246, 0.1);
            }

            .universal-feedback.loading {
                border-color: rgba(167, 139, 250, 0.6);
                background: rgba(167, 139, 250, 0.1);
            }

            /* Animations spéciales */
            .universal-feedback.celebration {
                animation: celebrationBounce 0.8s ease-in-out;
            }

            @keyframes celebrationBounce {
                0%, 100% { transform: scale(1) translateY(0); }
                25% { transform: scale(1.1) translateY(-10px); }
                50% { transform: scale(1.05) translateY(-5px); }
                75% { transform: scale(1.08) translateY(-8px); }
            }

            .universal-feedback.shake {
                animation: feedbackShake 0.5s ease-in-out;
            }

            @keyframes feedbackShake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }

            .universal-feedback.glow {
                animation: feedbackGlow 1s ease-in-out;
            }

            @keyframes feedbackGlow {
                0%, 100% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); }
                50% { box-shadow: 0 8px 32px rgba(167, 139, 250, 0.6); }
            }

            /* Thèmes */
            .universal-feedback.matrix {
                border-color: rgba(0, 255, 0, 0.6);
                background: rgba(0, 0, 0, 0.9);
                color: #00ff00;
            }

            .universal-feedback.matrix::before {
                background: linear-gradient(90deg, #00ff00, #00ffff);
            }

            .universal-feedback.cyberpunk {
                border-color: rgba(255, 0, 255, 0.6);
                background: rgba(20, 0, 40, 0.95);
                color: #ff00ff;
            }

            .universal-feedback.cyberpunk::before {
                background: linear-gradient(90deg, #ff00ff, #00ffff);
            }

            .universal-feedback.ocean {
                border-color: rgba(0, 191, 255, 0.6);
                background: rgba(0, 100, 200, 0.1);
                color: #00bfff;
            }

            .universal-feedback.ocean::before {
                background: linear-gradient(90deg, #00bfff, #0066cc);
            }

            /* Responsive */
            @media (max-width: 768px) {
                .universal-feedback {
                    font-size: 0.9em;
                    padding: 14px 20px;
                    min-width: 180px;
                    max-width: 90vw;
                }

                .universal-feedback-content {
                    gap: 10px;
                }

                .universal-feedback-icon {
                    font-size: 1.3em;
                }
            }

            /* Accessibilité */
            .universal-feedback[aria-live="polite"] {
                animation: none;
            }

            .universal-feedback[aria-live="assertive"] {
                animation: feedbackPulse 0.6s ease-in-out;
            }

            /* États de focus */
            .universal-feedback:focus {
                outline: 3px solid var(--violet-lunaire);
                outline-offset: 2px;
            }
        `;
        document.head.appendChild(style);
    }

    setupAudioContext() {
        if (!this.settings.audioFeedback) return;

        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (error) {
            console.warn('AudioContext non supporté:', error);
        }
    }

    setupEventListeners() {
        // Gérer les touches clavier pour l'accessibilité
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.clearAllFeedbacks();
            }
        });
    }

    setupAccessibility() {
        // Ajouter les attributs ARIA pour l'accessibilité
        const container = this.getContainer();
        container.setAttribute('role', 'status');
        container.setAttribute('aria-live', 'polite');
        container.setAttribute('aria-label', 'Feedback');
    }

    getContainer() {
        let container = document.getElementById('universal-feedback-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'universal-feedback-container';
            container.className = 'universal-feedback-container';
            document.body.appendChild(container);
        }
        return container;
    }

    // Méthodes principales
    showFeedback(config) {
        const feedbackConfig = {
            id: config.id || `feedback_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type: config.type || 'info',
            message: config.message || '',
            icon: config.icon || this.getDefaultIcon(config.type),
            duration: config.duration || this.settings.autoHideDelay,
            animation: config.animation || 'default',
            theme: config.theme || this.settings.theme,
            priority: config.priority || 'normal',
            onShow: config.onShow || null,
            onHide: config.onHide || null,
            ...config
        };

        // Vérifier la limite de feedbacks
        if (this.activeFeedbacks.size >= this.settings.maxConcurrentFeedbacks) {
            this.feedbackQueue.push(feedbackConfig);
            return feedbackConfig.id;
        }

        return this.createFeedback(feedbackConfig);
    }

    createFeedback(config) {
        const container = this.getContainer();
        const feedback = document.createElement('div');
        feedback.className = `universal-feedback ${config.type} ${config.theme} ${config.animation}`;
        feedback.dataset.id = config.id;
        feedback.setAttribute('role', 'alert');
        feedback.setAttribute('aria-live', 'assertive');
        feedback.setAttribute('tabindex', '-1');

        feedback.innerHTML = `
            <div class="universal-feedback-content">
                <span class="universal-feedback-icon">${config.icon}</span>
                <span class="universal-feedback-text">${config.message}</span>
            </div>
            <div class="universal-feedback-progress"></div>
        `;

        container.appendChild(feedback);
        this.activeFeedbacks.set(config.id, { element: feedback, config });

        // Animation d'entrée
        requestAnimationFrame(() => {
            feedback.classList.add('show');
            feedback.focus();
        });

        // Auto-hide
        if (config.duration > 0) {
            this.startAutoHide(config.id, config.duration);
        }

        // Feedback audio et haptique
        this.playFeedbackSound(config.type);
        this.vibrate(config.type);

        // Callback onShow
        if (config.onShow) {
            config.onShow(config);
        }

        return config.id;
    }

    startAutoHide(id, duration) {
        const feedback = this.activeFeedbacks.get(id);
        if (!feedback) return;

        const progressBar = feedback.element.querySelector('.universal-feedback-progress');
        if (progressBar) {
            progressBar.style.transition = `transform ${duration}ms linear`;
            progressBar.classList.add('animate');
        }

        setTimeout(() => {
            this.hideFeedback(id);
        }, duration);
    }

    hideFeedback(id) {
        const feedback = this.activeFeedbacks.get(id);
        if (!feedback) return;

        const { element, config } = feedback;

        element.classList.add('hide');
        element.classList.remove('show');

        setTimeout(() => {
            element.remove();
            this.activeFeedbacks.delete(id);

            if (config.onHide) {
                config.onHide(config);
            }

            this.processQueue();
        }, 300);
    }

    clearAllFeedbacks() {
        const ids = Array.from(this.activeFeedbacks.keys());
        ids.forEach(id => this.hideFeedback(id));
        this.feedbackQueue = [];
    }

    processQueue() {
        if (this.isProcessing || this.feedbackQueue.length === 0) return;

        this.isProcessing = true;
        setTimeout(() => {
            if (this.activeFeedbacks.size < this.settings.maxConcurrentFeedbacks && this.feedbackQueue.length > 0) {
                const nextFeedback = this.feedbackQueue.shift();
                this.createFeedback(nextFeedback);
            }
            this.isProcessing = false;
        }, 500);
    }

    // Méthodes utilitaires pour les types courants
    success(message, options = {}) {
        return this.showFeedback({
            type: 'success',
            message,
            icon: '✅',
            animation: 'celebration',
            ...options
        });
    }

    warning(message, options = {}) {
        return this.showFeedback({
            type: 'warning',
            message,
            icon: '⚠️',
            animation: 'shake',
            ...options
        });
    }

    error(message, options = {}) {
        return this.showFeedback({
            type: 'error',
            message,
            icon: '❌',
            animation: 'shake',
            duration: 4000, // Plus long pour les erreurs
            ...options
        });
    }

    info(message, options = {}) {
        return this.showFeedback({
            type: 'info',
            message,
            icon: 'ℹ️',
            ...options
        });
    }

    loading(message, options = {}) {
        return this.showFeedback({
            type: 'loading',
            message,
            icon: '⏳',
            duration: 0, // Pas d'auto-hide
            ...options
        });
    }

    celebration(message, options = {}) {
        return this.showFeedback({
            type: 'success',
            message,
            icon: '🎉',
            animation: 'celebration',
            duration: 3000,
            ...options
        });
    }

    achievement(message, options = {}) {
        return this.showFeedback({
            type: 'success',
            message,
            icon: '🏆',
            animation: 'glow',
            duration: 4000,
            ...options
        });
    }

    levelUp(newLevel, options = {}) {
        return this.showFeedback({
            type: 'success',
            message: `Niveau ${newLevel} atteint !`,
            icon: '⬆️',
            animation: 'celebration',
            duration: 3000,
            ...options
        });
    }

    badgeEarned(badgeName, options = {}) {
        return this.showFeedback({
            type: 'success',
            message: `Badge "${badgeName}" débloqué !`,
            icon: '🏅',
            animation: 'glow',
            duration: 3000,
            ...options
        });
    }

    missionComplete(missionName, options = {}) {
        return this.showFeedback({
            type: 'success',
            message: `Mission "${missionName}" complétée !`,
            icon: '🎯',
            animation: 'celebration',
            duration: 3000,
            ...options
        });
    }

    // Méthodes de feedback audio
    playFeedbackSound(type) {
        if (!this.settings.audioFeedback || !this.audioContext) return;

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            const frequencies = {
                success: [800, 1000, 1200],
                warning: [600, 400],
                error: [400, 300, 200],
                info: [500],
                loading: [600, 700, 600],
                celebration: [800, 1000, 1200, 1000, 800],
                achievement: [1000, 1200, 1400, 1200, 1000]
            };

            const freqArray = frequencies[type] || frequencies.info;
            let currentFreq = 0;

            const playTone = (freq) => {
                oscillator.frequency.setValueAtTime(freq, this.audioContext.currentTime + currentFreq * 0.1);
                currentFreq++;
            };

            freqArray.forEach(playTone);

            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(this.settings.soundVolume, this.audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + freqArray.length * 0.1);

            oscillator.start();
            oscillator.stop(this.audioContext.currentTime + freqArray.length * 0.1);
        } catch (error) {
            console.warn('Erreur audio:', error);
        }
    }

    vibrate(type) {
        if (!this.settings.hapticFeedback || !navigator.vibrate) return;

        const patterns = {
            success: [100, 50, 100],
            warning: [200, 100, 200],
            error: [300, 150, 300, 150, 300],
            info: [100],
            loading: [50, 50, 50],
            celebration: [100, 50, 100, 50, 100, 50, 100],
            achievement: [200, 100, 200, 100, 200]
        };

        const intensity = this.settings.vibrationIntensity;
        const multiplier = intensity === 'low' ? 0.5 : intensity === 'high' ? 1.5 : 1;
        const pattern = patterns[type] || patterns.info;
        const adjustedPattern = pattern.map(duration => Math.round(duration * multiplier));

        navigator.vibrate(adjustedPattern);
    }

    // Méthodes de configuration
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        localStorage.setItem('arkalia_feedback_settings', JSON.stringify(this.settings));

        // Reconfigurer l'audio si nécessaire
        if (newSettings.audioFeedback && !this.audioContext) {
            this.setupAudioContext();
        }
    }

    getSettings() {
        return { ...this.settings };
    }

    // Méthodes de debug
    getActiveFeedbacks() {
        return Array.from(this.activeFeedbacks.keys());
    }

    getQueueLength() {
        return this.feedbackQueue.length;
    }

    clearAll() {
        this.clearAllFeedbacks();
        this.feedbackQueue = [];
    }

    // Méthodes utilitaires
    getDefaultIcon(type) {
        const icons = {
            success: '✅',
            warning: '⚠️',
            error: '❌',
            info: 'ℹ️',
            loading: '⏳',
            celebration: '🎉',
            achievement: '🏆',
            levelup: '⬆️',
            badge: '🏅',
            mission: '🎯'
        };
        return icons[type] || icons.info;
    }

    // Méthodes d'intégration avec d'autres systèmes
    integrateWithNotifications() {
        if (window.universalNotifications) {
            // Rediriger certains types de notifications vers le feedback
            const originalSuccess = window.universalNotifications.success;
            window.universalNotifications.success = (title, content, options) => {
                this.success(`${title}: ${content}`, options);
                return originalSuccess.call(window.universalNotifications, title, content, options);
            };
        }
    }

    integrateWithEmptyStates() {
        if (window.universalEmptyStates) {
            // Ajouter des feedbacks aux actions d'empty states
            const originalShowEmptyState = window.universalEmptyStates.showEmptyState;
            window.universalEmptyStates.showEmptyState = (container, type, config) => {
                const result = originalShowEmptyState.call(window.universalEmptyStates, container, type, config);
                this.info(`État vide affiché: ${type}`, { duration: 1000 });
                return result;
            };
        }
    }
}

// Initialiser le système universel
document.addEventListener('DOMContentLoaded', () => {
    window.universalFeedback = new UniversalFeedback();

    // Intégrer avec les autres systèmes
    setTimeout(() => {
        window.universalFeedback.integrateWithNotifications();
        window.universalFeedback.integrateWithEmptyStates();
    }, 1000);

    console.log('⚡ Universal Feedback System prêt');
});

// Exporter pour utilisation globale
window.UniversalFeedback = UniversalFeedback;
