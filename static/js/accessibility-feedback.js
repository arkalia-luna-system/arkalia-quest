/* ===== ARKALIA QUEST - ACCESSIBILITY FEEDBACK SYSTEM ===== */

class AccessibilityFeedback {
    constructor() {
        this.feedbackContainer = null;
        this.currentSettings = {
            fontSize: 'normal',
            contrast: 'normal',
            reducedMotion: false,
            highContrast: false,
            screenReader: false
        };
        this.observers = [];
        this.init();
    }

    init() {
        this.createFeedbackContainer();
        this.detectAccessibilityPreferences();
        this.setupEventListeners();
        this.observeChanges();
        console.log('♿ Accessibility Feedback System initialisé');
    }

    createFeedbackContainer() {
        if (document.getElementById('accessibility-feedback')) return;

        const container = document.createElement('div');
        container.id = 'accessibility-feedback';
        container.className = 'accessibility-feedback-container';
        container.innerHTML = `
            <style>
                .accessibility-feedback-container {
                    position: fixed;
                    bottom: 20px;
                    left: 20px;
                    z-index: 10000;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    max-width: 300px;
                    pointer-events: none;
                }
                
                .accessibility-toast {
                    background: rgba(0, 0, 0, 0.9);
                    border: 2px solid rgba(0, 255, 0, 0.5);
                    border-radius: 12px;
                    padding: 16px 20px;
                    color: white;
                    font-size: 14px;
                    line-height: 1.4;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    backdrop-filter: blur(20px);
                    transform: translateX(-100%);
                    opacity: 0;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    pointer-events: auto;
                    position: relative;
                    overflow: hidden;
                }
                
                .accessibility-toast.show {
                    transform: translateX(0);
                    opacity: 1;
                }
                
                .accessibility-toast.hide {
                    transform: translateX(-100%);
                    opacity: 0;
                }
                
                .accessibility-toast::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, #00ff00, #00ffff);
                    border-radius: 12px 12px 0 0;
                }
                
                .accessibility-toast-header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 8px;
                }
                
                .accessibility-toast-icon {
                    font-size: 18px;
                    margin-right: 8px;
                }
                
                .accessibility-toast-title {
                    font-weight: 600;
                    color: #00ff00;
                    flex: 1;
                }
                
                .accessibility-toast-close {
                    background: none;
                    border: none;
                    color: rgba(255, 255, 255, 0.6);
                    cursor: pointer;
                    font-size: 16px;
                    padding: 4px;
                    border-radius: 4px;
                    transition: all 0.2s ease;
                }
                
                .accessibility-toast-close:hover {
                    color: white;
                    background: rgba(255, 255, 255, 0.1);
                }
                
                .accessibility-toast-message {
                    color: rgba(255, 255, 255, 0.9);
                    margin: 0;
                }
                
                .accessibility-toast.success {
                    border-color: rgba(0, 255, 0, 0.5);
                }
                
                .accessibility-toast.warning {
                    border-color: rgba(255, 193, 7, 0.5);
                }
                
                .accessibility-toast.error {
                    border-color: rgba(220, 53, 69, 0.5);
                }
                
                .accessibility-toast.info {
                    border-color: rgba(0, 191, 255, 0.5);
                }
                
                @media (max-width: 768px) {
                    .accessibility-feedback-container {
                        bottom: 10px;
                        left: 10px;
                        right: 10px;
                        max-width: none;
                    }
                }
            </style>
        `;

        document.body.appendChild(container);
        this.feedbackContainer = container;
    }

    detectAccessibilityPreferences() {
        // Détecter les préférences d'accessibilité
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.currentSettings.reducedMotion = true;
        }

        if (window.matchMedia('(prefers-contrast: high)').matches) {
            this.currentSettings.highContrast = true;
        }

        // Détecter les lecteurs d'écran
        if (navigator.userAgent.includes('NVDA') ||
            navigator.userAgent.includes('JAWS') ||
            navigator.userAgent.includes('VoiceOver')) {
            this.currentSettings.screenReader = true;
        }

        // Détecter la taille de police
        const rootFontSize = parseInt(getComputedStyle(document.documentElement).fontSize);
        if (rootFontSize > 16) {
            this.currentSettings.fontSize = 'large';
        } else if (rootFontSize < 16) {
            this.currentSettings.fontSize = 'small';
        }
    }

    setupEventListeners() {
        // Écouter les changements de préférences
        if (window.matchMedia) {
            const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
            const contrastQuery = window.matchMedia('(prefers-contrast: high)');

            motionQuery.addEventListener('change', (e) => {
                this.currentSettings.reducedMotion = e.matches;
                this.showFeedback('Préférence de mouvement mise à jour', 'info');
            });

            contrastQuery.addEventListener('change', (e) => {
                this.currentSettings.highContrast = e.matches;
                this.showFeedback('Contraste élevé activé', 'info');
            });
        }

        // Écouter les changements de thème
        document.addEventListener('themeChanged', (e) => {
            this.showFeedback(`Thème changé vers ${e.detail.theme}`, 'success');
        });

        // Écouter les changements de taille de police
        document.addEventListener('fontSizeChanged', (e) => {
            this.showFeedback(`Taille de police: ${e.detail.size}`, 'info');
        });

        // Écouter les changements de contraste
        document.addEventListener('contrastChanged', (e) => {
            this.showFeedback(`Contraste: ${e.detail.level}`, 'info');
        });
    }

    observeChanges() {
        // Observer les changements dans les paramètres d'accessibilité
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' &&
                    mutation.attributeName === 'class') {
                    this.checkAccessibilityChanges(mutation.target);
                }
            });
        });

        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['class']
        });

        this.observers.push(observer);
    }

    checkAccessibilityChanges(element) {
        const classes = element.classList;

        // Vérifier les changements de thème
        if (classes.contains('matrix-theme') ||
            classes.contains('neon-theme') ||
            classes.contains('cyberpunk-theme') ||
            classes.contains('ocean-theme') ||
            classes.contains('earth-theme') ||
            classes.contains('dopamine-theme')) {
            const theme = Array.from(classes).find(cls => cls.includes('-theme'));
            this.showFeedback(`Thème ${theme.replace('-theme', '')} activé`, 'success');
        }

        // Vérifier les changements de contraste
        if (classes.contains('high-contrast')) {
            this.showFeedback('Contraste élevé activé', 'info');
        }

        // Vérifier les changements de taille
        if (classes.contains('large-text')) {
            this.showFeedback('Texte agrandi activé', 'info');
        }

        // Vérifier les changements de mouvement
        if (classes.contains('reduced-motion')) {
            this.showFeedback('Mouvements réduits activés', 'info');
        }
    }

    showFeedback(message, type = 'info', duration = 4000) {
        if (!this.feedbackContainer) return;

        // Vérifier si le feedback est déjà affiché
        const existingToast = this.feedbackContainer.querySelector('.accessibility-toast');
        if (existingToast) {
            existingToast.remove();
        }

        const toast = document.createElement('div');
        toast.className = `accessibility-toast ${type}`;

        const icon = this.getIconForType(type);
        const id = 'accessibility-toast-' + Date.now();

        toast.innerHTML = `
            <div class="accessibility-toast-header">
                <div style="display: flex; align-items: center;">
                    <span class="accessibility-toast-icon">${icon}</span>
                    <span class="accessibility-toast-title">Accessibilité</span>
                </div>
                <button class="accessibility-toast-close" onclick="window.accessibilityFeedback.removeToast('${id}')">×</button>
            </div>
            <p class="accessibility-toast-message">${message}</p>
        `;

        toast.id = id;
        this.feedbackContainer.appendChild(toast);

        // Animation d'entrée
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        // Auto-suppression
        setTimeout(() => {
            this.removeToast(id);
        }, duration);
    }

    getIconForType(type) {
        const icons = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️'
        };
        return icons[type] || 'ℹ️';
    }

    removeToast(id) {
        const toast = document.getElementById(id);
        if (!toast) return;

        toast.classList.add('hide');

        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 400);
    }

    // Méthodes publiques
    showSuccess(message, duration = 4000) {
        this.showFeedback(message, 'success', duration);
    }

    showWarning(message, duration = 5000) {
        this.showFeedback(message, 'warning', duration);
    }

    showError(message, duration = 6000) {
        this.showFeedback(message, 'error', duration);
    }

    showInfo(message, duration = 4000) {
        this.showFeedback(message, 'info', duration);
    }

    // Méthodes pour les changements d'accessibilité
    onFontSizeChange(size) {
        this.currentSettings.fontSize = size;
        this.showFeedback(`Taille de police: ${size}`, 'info');

        // Déclencher l'événement personnalisé
        document.dispatchEvent(new CustomEvent('fontSizeChanged', {
            detail: { size }
        }));
    }

    onContrastChange(level) {
        this.currentSettings.contrast = level;
        this.showFeedback(`Contraste: ${level}`, 'info');

        // Déclencher l'événement personnalisé
        document.dispatchEvent(new CustomEvent('contrastChanged', {
            detail: { level }
        }));
    }

    onThemeChange(theme) {
        this.showFeedback(`Thème changé vers ${theme}`, 'success');

        // Déclencher l'événement personnalisé
        document.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme }
        }));
    }

    onReducedMotionToggle(enabled) {
        this.currentSettings.reducedMotion = enabled;
        this.showFeedback(
            enabled ? 'Mouvements réduits activés' : 'Mouvements normaux activés',
            'info'
        );
    }

    onHighContrastToggle(enabled) {
        this.currentSettings.highContrast = enabled;
        this.showFeedback(
            enabled ? 'Contraste élevé activé' : 'Contraste normal activé',
            'info'
        );
    }

    // Méthode pour annoncer les changements importants
    announceChange(message) {
        // Utiliser l'API d'annonce si disponible
        if (window.speechSynthesis) {
            const utterance = new SpeechSynthesisUtterance(message);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            speechSynthesis.speak(utterance);
        }

        // Afficher aussi le feedback visuel
        this.showFeedback(message, 'info', 6000);
    }

    // Méthode pour vérifier l'accessibilité
    checkAccessibility() {
        const issues = [];

        // Vérifier les images sans alt
        const imagesWithoutAlt = document.querySelectorAll('img:not([alt])');
        if (imagesWithoutAlt.length > 0) {
            issues.push(`${imagesWithoutAlt.length} image(s) sans attribut alt`);
        }

        // Vérifier les boutons sans texte
        const buttonsWithoutText = document.querySelectorAll('button:not([aria-label]):empty');
        if (buttonsWithoutText.length > 0) {
            issues.push(`${buttonsWithoutText.length} bouton(s) sans texte`);
        }

        // Vérifier les liens sans texte
        const linksWithoutText = document.querySelectorAll('a:not([aria-label]):empty');
        if (linksWithoutText.length > 0) {
            issues.push(`${linksWithoutText.length} lien(s) sans texte`);
        }

        // Vérifier les formulaires sans labels
        const inputsWithoutLabels = document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])');
        if (inputsWithoutLabels.length > 0) {
            issues.push(`${inputsWithoutLabels.length} champ(s) sans label`);
        }

        if (issues.length > 0) {
            this.showWarning(`Problèmes d'accessibilité détectés: ${issues.join(', ')}`, 8000);
        } else {
            this.showSuccess('Aucun problème d\'accessibilité détecté', 3000);
        }

        return issues;
    }

    // Méthode pour nettoyer
    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        if (this.feedbackContainer) {
            this.feedbackContainer.remove();
        }
    }
}

// Initialiser le système
window.accessibilityFeedback = new AccessibilityFeedback();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AccessibilityFeedback;
}
