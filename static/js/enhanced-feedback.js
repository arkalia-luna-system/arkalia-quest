/**
 * Enhanced Feedback - Système de feedback visuel et auditif renforcé
 * Améliore la sensation d'action/réaction pour chaque interaction
 */

class EnhancedFeedback {
    constructor() {
        this.soundEnabled = true;
        this.hapticEnabled = 'vibrate' in navigator;
        this.feedbackHistory = [];

        this.init();
    }

    init() {
        this.loadPreferences();
        this.setupEventListeners();
        this.addFeedbackStyles();
        console.log('✅ Enhanced Feedback initialisé');
    }

    loadPreferences() {
        const prefs = JSON.parse(localStorage.getItem('arkalia_feedback_prefs') || '{}');
        this.soundEnabled = prefs.soundEnabled !== false;
        this.hapticEnabled = prefs.hapticEnabled !== false && 'vibrate' in navigator;
    }

    savePreferences() {
        const prefs = {
            soundEnabled: this.soundEnabled,
            hapticEnabled: this.hapticEnabled
        };
        localStorage.setItem('arkalia_feedback_prefs', JSON.stringify(prefs));
    }

    setupEventListeners() {
        // Boutons principaux
        document.addEventListener('click', (e) => {
            if (e.target.matches('.cta-btn, .primary-btn, .action-btn')) {
                this.triggerFeedback('button_click', e.target);
            }
        });

        // Liens de navigation
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href]')) {
                this.triggerFeedback('navigation', e.target);
            }
        });

        // Formulaires
        document.addEventListener('submit', (e) => {
            this.triggerFeedback('form_submit', e.target);
        });

        // Inputs
        document.addEventListener('input', (e) => {
            if (e.target.matches('input, textarea, select')) {
                this.triggerFeedback('input_change', e.target);
            }
        });

        // Commandes terminal
        document.addEventListener('keydown', (e) => {
            if (e.target.matches('#commandInput') && e.key === 'Enter') {
                this.triggerFeedback('command_execute', e.target);
            }
        });
    }

    triggerFeedback(type, element, options = {}) {
        const feedback = {
            type,
            element,
            timestamp: Date.now(),
            options
        };

        this.feedbackHistory.push(feedback);
        this.cleanHistory();

        // Feedback visuel
        this.visualFeedback(type, element, options);

        // Feedback auditif
        if (this.soundEnabled) {
            this.audioFeedback(type, options);
        }

        // Feedback haptique
        if (this.hapticEnabled) {
            this.hapticFeedback(type, options);
        }
    }

    visualFeedback(type, element, options = {}) {
        const config = this.getVisualConfig(type, options);

        // Créer l'effet visuel
        const effect = document.createElement('div');
        effect.className = `feedback-effect ${config.class}`;
        effect.style.cssText = config.styles;

        // Positionner l'effet
        if (element) {
            const rect = element.getBoundingClientRect();
            effect.style.left = `${rect.left + rect.width / 2}px`;
            effect.style.top = `${rect.top + rect.height / 2}px`;
        }

        document.body.appendChild(effect);

        // Animation
        requestAnimationFrame(() => {
            effect.classList.add('active');
        });

        // Supprimer après animation
        setTimeout(() => {
            effect.classList.add('fade-out');
            setTimeout(() => {
                if (effect.parentElement) {
                    effect.remove();
                }
            }, 300);
        }, config.duration || 1000);
    }

    getVisualConfig(type, options) {
        const configs = {
            button_click: {
                class: 'ripple-effect',
                styles: `
                    position: fixed;
                    width: 20px;
                    height: 20px;
                    background: radial-gradient(circle, rgba(0, 255, 0, 0.6) 0%, transparent 70%);
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 1000;
                    transform: translate(-50%, -50%) scale(0);
                `,
                duration: 600
            },
            navigation: {
                class: 'slide-effect',
                styles: `
                    position: fixed;
                    width: 4px;
                    height: 40px;
                    background: linear-gradient(to bottom, var(--primary, #00ff00), transparent);
                    pointer-events: none;
                    z-index: 1000;
                    transform: translate(-50%, -50%) scaleY(0);
                `,
                duration: 400
            },
            command_execute: {
                class: 'terminal-effect',
                styles: `
                    position: fixed;
                    width: 100px;
                    height: 2px;
                    background: linear-gradient(90deg, transparent, var(--terminal-accent, #00ff00), transparent);
                    pointer-events: none;
                    z-index: 1000;
                    transform: translate(-50%, -50%) scaleX(0);
                `,
                duration: 500
            },
            success: {
                class: 'success-effect',
                styles: `
                    position: fixed;
                    width: 60px;
                    height: 60px;
                    background: radial-gradient(circle, rgba(0, 255, 0, 0.3) 0%, transparent 70%);
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 1000;
                    transform: translate(-50%, -50%) scale(0);
                `,
                duration: 800
            },
            error: {
                class: 'error-effect',
                styles: `
                    position: fixed;
                    width: 60px;
                    height: 60px;
                    background: radial-gradient(circle, rgba(255, 0, 0, 0.3) 0%, transparent 70%);
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 1000;
                    transform: translate(-50%, -50%) scale(0);
                `,
                duration: 800
            }
        };

        return configs[type] || configs.button_click;
    }

    audioFeedback(type, options = {}) {
        const sounds = {
            button_click: { frequency: 800, duration: 100, type: 'sine' },
            navigation: { frequency: 600, duration: 150, type: 'sine' },
            command_execute: { frequency: 1000, duration: 200, type: 'square' },
            success: { frequency: 1200, duration: 300, type: 'sine' },
            error: { frequency: 400, duration: 400, type: 'sawtooth' },
            notification: { frequency: 900, duration: 250, type: 'triangle' }
        };

        const sound = sounds[type];
        if (!sound) return;

        this.playTone(sound.frequency, sound.duration, sound.type);
    }

    playTone(frequency, duration, type = 'sine') {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
            oscillator.type = type;

            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration / 1000);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration / 1000);
        } catch (error) {
            console.log('Audio non disponible:', error);
        }
    }

    hapticFeedback(type, options = {}) {
        const patterns = {
            button_click: [10],
            navigation: [20],
            command_execute: [15, 10, 15],
            success: [50, 100, 50],
            error: [100, 50, 100],
            notification: [30, 20, 30]
        };

        const pattern = patterns[type];
        if (!pattern) return;

        try {
            navigator.vibrate(pattern);
        } catch (error) {
            console.log('Vibration non disponible:', error);
        }
    }

    addFeedbackStyles() {
        if (document.getElementById('enhanced-feedback-styles')) return;

        const style = document.createElement('style');
        style.id = 'enhanced-feedback-styles';
        style.textContent = `
            .feedback-effect {
                transition: all 0.3s ease;
            }

            .feedback-effect.active {
                transform: translate(-50%, -50%) scale(1) !important;
            }

            .feedback-effect.fade-out {
                opacity: 0;
                transform: translate(-50%, -50%) scale(1.2) !important;
            }

            .ripple-effect.active {
                animation: ripple 0.6s ease-out;
            }

            @keyframes ripple {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(3); opacity: 0; }
            }

            .slide-effect.active {
                animation: slide 0.4s ease-out;
            }

            @keyframes slide {
                0% { transform: translate(-50%, -50%) scaleY(0); }
                100% { transform: translate(-50%, -50%) scaleY(1); }
            }

            .terminal-effect.active {
                animation: terminal 0.5s ease-out;
            }

            @keyframes terminal {
                0% { transform: translate(-50%, -50%) scaleX(0); }
                100% { transform: translate(-50%, -50%) scaleX(1); }
            }

            .success-effect.active {
                animation: success 0.8s ease-out;
            }

            @keyframes success {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 1; }
                50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
                100% { transform: translate(-50%, -50%) scale(2); opacity: 0; }
            }

            .error-effect.active {
                animation: error 0.8s ease-out;
            }

            @keyframes error {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 1; }
                25% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.9; }
                50% { transform: translate(-50%, -50%) scale(0.9); opacity: 0.8; }
                75% { transform: translate(-50%, -50%) scale(1.05); opacity: 0.6; }
                100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
            }

            /* Amélioration des boutons */
            .cta-btn, .primary-btn, .action-btn {
                transition: all 0.2s ease;
                position: relative;
                overflow: hidden;
            }

            .cta-btn:active, .primary-btn:active, .action-btn:active {
                transform: scale(0.95);
            }

            /* Amélioration des liens */
            a[href] {
                transition: all 0.2s ease;
            }

            a[href]:hover {
                transform: translateY(-1px);
            }

            /* Amélioration des inputs */
            input, textarea, select {
                transition: all 0.2s ease;
            }

            input:focus, textarea:focus, select:focus {
                transform: scale(1.02);
                box-shadow: 0 0 0 2px var(--primary, #00ff00);
            }
        `;
        document.head.appendChild(style);
    }

    cleanHistory() {
        const oneHourAgo = Date.now() - (60 * 60 * 1000);
        this.feedbackHistory = this.feedbackHistory.filter(
            feedback => feedback.timestamp > oneHourAgo
        );
    }

    // Méthodes publiques
    enableSound() {
        this.soundEnabled = true;
        this.savePreferences();
    }

    disableSound() {
        this.soundEnabled = false;
        this.savePreferences();
    }

    enableHaptic() {
        this.hapticEnabled = true;
        this.savePreferences();
    }

    disableHaptic() {
        this.hapticEnabled = false;
        this.savePreferences();
    }

    // Méthodes pour déclencher des feedbacks spécifiques
    showSuccess(message, element = null) {
        this.triggerFeedback('success', element, { message });
    }

    showError(message, element = null) {
        this.triggerFeedback('error', element, { message });
    }

    showNotification(message, element = null) {
        this.triggerFeedback('notification', element, { message });
    }
}

// Initialiser le système
window.enhancedFeedback = new EnhancedFeedback();

// Exporter pour utilisation globale
window.EnhancedFeedback = EnhancedFeedback;
