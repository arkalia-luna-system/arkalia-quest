/**
 * ARKALIA QUEST - SYSTÈME D'ACCESSIBILITÉ WCAG 2.1 AA
 * Gestion complète de l'accessibilité pour tous les utilisateurs
 */

class AccessibilityManager {
    constructor() {
        this.currentMode = 'default';
        this.accessibilitySettings = this.loadSettings();
        this.init();
    }

    init() {
        this.setupSkipLinks();
        this.setupKeyboardNavigation();
        this.setupFocusManagement();
        this.setupAccessibilityPanel();
        this.setupScreenReaderSupport();
        this.setupHapticFeedback();
        this.setupResponsiveAccessibility();
        this.setupAdvancedModes();
        this.applySettings();
        
        console.log('♿ Système d\'accessibilité Arkalia Quest initialisé');
    }

    // ===== GESTION DES PARAMÈTRES =====
    
    loadSettings() {
        const saved = localStorage.getItem('arkalia_accessibility');
        return saved ? JSON.parse(saved) : {
            daltonian: false,
            highContrast: false,
            dyslexia: false,
            reducedMotion: false,
            fontSize: 'normal',
            hapticFeedback: true,
            zoom: 'normal',
            spacing: 'normal',
            highlight: false
        };
    }

    saveSettings() {
        localStorage.setItem('arkalia_accessibility', JSON.stringify(this.accessibilitySettings));
    }

    // ===== SKIP LINKS =====
    
    setupSkipLinks() {
        const skipLinks = `
            <a href="#main-content" class="skip-link">Aller au contenu principal</a>
            <a href="#navigation" class="skip-link">Aller à la navigation</a>
            <a href="#accessibility-panel" class="skip-link">Paramètres d'accessibilité</a>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', skipLinks);
        
        // Gestion des skip links
        document.querySelectorAll('.skip-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.focus();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    // ===== NAVIGATION CLAVIER =====
    
    setupKeyboardNavigation() {
        // Indicateur de navigation clavier
        const navIndicator = document.createElement('div');
        navIndicator.className = 'nav-focus-indicator';
        document.body.appendChild(navIndicator);

        // Détection de navigation clavier
        let isKeyboardNavigation = false;
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                isKeyboardNavigation = true;
                navIndicator.classList.add('active');
            }
        });

        document.addEventListener('mousedown', () => {
            isKeyboardNavigation = false;
            navIndicator.classList.remove('active');
        });

        // Gestion des touches spéciales
        document.addEventListener('keydown', (e) => {
            // Échap pour fermer les modales
            if (e.key === 'Escape') {
                this.closeModals();
            }
            
            // Alt + A pour ouvrir le panneau d'accessibilité
            if (e.altKey && e.key === 'a') {
                e.preventDefault();
                this.toggleAccessibilityPanel();
            }
            
            // Alt + 1-8 pour modes d'accessibilité rapides
            if (e.altKey && ['1', '2', '3', '4', '5', '6', '7', '8'].includes(e.key)) {
                e.preventDefault();
                this.quickAccessibilityMode(e.key);
            }
        });
    }

    // ===== GESTION DU FOCUS =====
    
    setupFocusManagement() {
        // Focus trap pour modales
        this.setupFocusTrap();
        
        // Focus visible renforcé
        document.addEventListener('focusin', (e) => {
            if (e.target.matches('button, input, select, textarea, a, [tabindex]')) {
                e.target.classList.add('focus-visible');
            }
        });

        document.addEventListener('focusout', (e) => {
            e.target.classList.remove('focus-visible');
        });
    }

    setupFocusTrap() {
        // Focus trap pour les modales (à implémenter selon les besoins)
        const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                const modal = document.querySelector('.modal.active');
                if (modal) {
                    const focusable = modal.querySelectorAll(focusableElements);
                    const firstElement = focusable[0];
                    const lastElement = focusable[focusable.length - 1];

                    if (e.shiftKey) {
                        if (document.activeElement === firstElement) {
                            e.preventDefault();
                            lastElement.focus();
                        }
                    } else {
                        if (document.activeElement === lastElement) {
                            e.preventDefault();
                            firstElement.focus();
                        }
                    }
                }
            }
        });
    }

    // ===== MENU D'ACCESSIBILITÉ =====
    
    setupAccessibilityPanel() {
        // Le menu d'accessibilité est maintenant dans le template HTML
        // On gère juste les interactions
        
        // Gestion du bouton toggle
        const toggleBtn = document.getElementById('accessibility-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.toggleAccessibilityMenu();
            });
        }
        
        // Gestion des boutons du menu
        document.querySelectorAll('.accessibility-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mode = btn.dataset.mode;
                const action = btn.dataset.action;
                
                if (mode) {
                    this.toggleMode(mode, btn);
                } else if (action) {
                    this.handleAction(action, btn);
                }
            });
        });
    }

    toggleMode(mode, button) {
        const isActive = button.getAttribute('aria-pressed') === 'true';
        
        if (isActive) {
            this.disableMode(mode);
            button.setAttribute('aria-pressed', 'false');
            button.classList.remove('active');
        } else {
            this.enableMode(mode);
            button.setAttribute('aria-pressed', 'true');
            button.classList.add('active');
        }
        
        this.accessibilitySettings[mode] = !isActive;
        this.saveSettings();
    }

    enableMode(mode) {
        switch (mode) {
            case 'daltonian':
                document.body.classList.add('daltonian');
                this.announceToScreenReader('Mode daltonien activé');
                break;
            case 'highContrast':
                document.body.classList.add('high-contrast');
                this.announceToScreenReader('Mode haut contraste activé');
                break;
            case 'dyslexia':
                document.body.classList.add('dyslexia-friendly');
                this.announceToScreenReader('Police adaptée dyslexie activée');
                break;
            case 'reducedMotion':
                document.body.classList.add('reduced-motion');
                this.announceToScreenReader('Animations réduites activées');
                break;
        }
    }

    disableMode(mode) {
        switch (mode) {
            case 'daltonian':
                document.body.classList.remove('daltonian');
                this.announceToScreenReader('Mode daltonien désactivé');
                break;
            case 'highContrast':
                document.body.classList.remove('high-contrast');
                this.announceToScreenReader('Mode haut contraste désactivé');
                break;
            case 'dyslexia':
                document.body.classList.remove('dyslexia-friendly');
                this.announceToScreenReader('Police adaptée dyslexie désactivée');
                break;
            case 'reducedMotion':
                document.body.classList.remove('reduced-motion');
                this.announceToScreenReader('Animations réduites désactivées');
                break;
        }
    }

    handleAction(action, button) {
        switch (action) {
            case 'fontSize':
                this.cycleFontSize(button);
                break;
            case 'zoom':
                this.cycleZoom(button);
                break;
            case 'spacing':
                this.cycleSpacing(button);
                break;
            case 'highlight':
                this.toggleHighlight(button);
                break;
            case 'hapticFeedback':
                this.toggleHapticFeedback(button);
                break;
        }
    }

    cycleFontSize(button) {
        const sizes = ['small', 'normal', 'large', 'xlarge'];
        const currentIndex = sizes.indexOf(this.accessibilitySettings.fontSize);
        const nextIndex = (currentIndex + 1) % sizes.length;
        const newSize = sizes[nextIndex];
        
        this.setFontSize(newSize);
        this.accessibilitySettings.fontSize = newSize;
        this.saveSettings();
        
        button.textContent = `🔤 ${newSize.charAt(0).toUpperCase() + newSize.slice(1)}`;
        this.announceToScreenReader(`Taille de police : ${newSize}`);
    }

    cycleZoom(button) {
        const zooms = ['normal', '200', '300', '400'];
        const currentIndex = zooms.indexOf(this.accessibilitySettings.zoom);
        const nextIndex = (currentIndex + 1) % zooms.length;
        const newZoom = zooms[nextIndex];
        
        this.setZoom(newZoom);
        this.accessibilitySettings.zoom = newZoom;
        this.saveSettings();
        
        button.textContent = `🔍 ${newZoom === 'normal' ? 'Normal' : newZoom + '%'}`;
        this.announceToScreenReader(`Zoom : ${newZoom === 'normal' ? 'normal' : newZoom + '%'}`);
    }

    cycleSpacing(button) {
        const spacings = ['normal', 'large', 'extra-large'];
        const currentIndex = spacings.indexOf(this.accessibilitySettings.spacing);
        const nextIndex = (currentIndex + 1) % spacings.length;
        const newSpacing = spacings[nextIndex];
        
        this.setSpacing(newSpacing);
        this.accessibilitySettings.spacing = newSpacing;
        this.saveSettings();
        
        button.textContent = `📏 ${newSpacing.charAt(0).toUpperCase() + newSpacing.slice(1)}`;
        this.announceToScreenReader(`Espacement : ${newSpacing}`);
    }

    toggleHighlight(button) {
        this.accessibilitySettings.highlight = !this.accessibilitySettings.highlight;
        const isActive = this.accessibilitySettings.highlight;
        
        if (isActive) {
            document.body.classList.add('highlight-focus', 'highlight-links', 'highlight-buttons');
        } else {
            document.body.classList.remove('highlight-focus', 'highlight-links', 'highlight-buttons');
        }
        
        button.setAttribute('aria-pressed', isActive.toString());
        button.classList.toggle('active', isActive);
        this.saveSettings();
        
        this.announceToScreenReader(
            isActive ? 'Surbrillance activée' : 'Surbrillance désactivée'
        );
    }

    setFontSize(size) {
        const sizes = {
            small: '14px',
            normal: '16px',
            large: '18px',
            xlarge: '20px'
        };
        
        document.documentElement.style.setProperty('--font-size-base', sizes[size]);
    }

    setZoom(zoom) {
        // Retirer les classes de zoom existantes
        document.body.classList.remove('zoom-200', 'zoom-300', 'zoom-400');
        
        if (zoom !== 'normal') {
            document.body.classList.add(`zoom-${zoom}`);
        }
    }

    setSpacing(spacing) {
        // Retirer les classes d'espacement existantes
        document.body.classList.remove('spacing-large', 'spacing-extra-large');
        
        if (spacing !== 'normal') {
            document.body.classList.add(`spacing-${spacing}`);
        }
    }

    toggleHapticFeedback(button) {
        this.accessibilitySettings.hapticFeedback = !this.accessibilitySettings.hapticFeedback;
        const isActive = this.accessibilitySettings.hapticFeedback;
        
        button.setAttribute('aria-pressed', isActive.toString());
        button.classList.toggle('active', isActive);
        this.saveSettings();
        
        this.announceToScreenReader(
            isActive ? 'Feedback haptique activé' : 'Feedback haptique désactivé'
        );
    }

    // ===== SUPPORT LECTEURS D'ÉCRAN =====
    
    setupScreenReaderSupport() {
        // Créer une région pour les annonces
        const announcementRegion = document.createElement('div');
        announcementRegion.id = 'screen-reader-announcements';
        announcementRegion.className = 'sr-only';
        announcementRegion.setAttribute('aria-live', 'polite');
        announcementRegion.setAttribute('aria-atomic', 'true');
        document.body.appendChild(announcementRegion);
        
        // Améliorer les descriptions ARIA
        this.enhanceAriaDescriptions();
    }

    announceToScreenReader(message) {
        const announcementRegion = document.getElementById('screen-reader-announcements');
        if (announcementRegion) {
            announcementRegion.setAttribute('role', 'status');
            announcementRegion.setAttribute('aria-live', 'polite');
            announcementRegion.setAttribute('aria-atomic', 'true');
            announcementRegion.textContent = message;
            setTimeout(() => {
                announcementRegion.textContent = '';
            }, 1000);
        }
    }

    enhanceAriaDescriptions() {
        // Ajouter des descriptions pour les éléments importants
        const elementsToEnhance = [
            { selector: '.main-action-btn', description: 'Bouton d\'action principal' },
            { selector: '.terminal-input', description: 'Zone de saisie des commandes' },
            { selector: '.badge', description: 'Badge de réussite' },
            { selector: '.stats-grid', description: 'Statistiques du joueur' }
        ];
        
        elementsToEnhance.forEach(({ selector, description }) => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (!element.getAttribute('aria-label') && !element.getAttribute('aria-describedby')) {
                    element.setAttribute('aria-label', description);
                }
            });
        });
    }

    // ===== FEEDBACK HAPTIQUE =====
    
    setupHapticFeedback() {
        // Feedback haptique pour les actions importantes
        this.setupHapticTriggers();
    }

    setupHapticTriggers() {
        const hapticTriggers = [
            '.main-action-btn',
            '.badge',
            '.success-message',
            '.error-message',
            'button',
            'a',
            'input[type="submit"]'
        ];
        
        hapticTriggers.forEach(selector => {
            document.addEventListener('click', (e) => {
                if (e.target.matches(selector) && this.accessibilitySettings.hapticFeedback) {
                    this.triggerHapticFeedback('light');
                }
            });
        });

        // Feedback pour navigation clavier
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab' && this.accessibilitySettings.hapticFeedback) {
                this.triggerHapticFeedback('light');
            }
        });
    }

    triggerHapticFeedback(type = 'light') {
        if (!this.accessibilitySettings.hapticFeedback) return;
        
        if ('vibrate' in navigator) {
            const patterns = {
                light: 50,
                medium: [50, 50, 50],
                heavy: [100, 50, 100],
                success: [100, 50, 100, 50, 100],
                error: [200, 100, 200],
                warning: [150, 100, 150]
            };
            
            navigator.vibrate(patterns[type]);
        }
    }

    // ===== ACCESSIBILITÉ RESPONSIVE =====
    
    setupResponsiveAccessibility() {
        // Détecter les préférences utilisateur
        this.detectUserPreferences();
        
        // Optimiser pour les appareils tactiles
        this.optimizeForTouch();
        
        // Gérer les changements d'orientation
        this.handleOrientationChange();
    }

    detectUserPreferences() {
        // Détecter prefers-reduced-motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.body.classList.add('reduced-motion');
        }
        
        // Détecter prefers-color-scheme
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.classList.add('dark-theme');
        }
        
        // Détecter les appareils tactiles
        if ('ontouchstart' in window) {
            document.body.classList.add('touch-device');
        }
    }

    optimizeForTouch() {
        if ('ontouchstart' in window) {
            // Augmenter la taille des éléments tactiles
            const touchElements = document.querySelectorAll('button, input, select, textarea');
            touchElements.forEach(element => {
                element.style.minHeight = '44px';
                element.style.minWidth = '44px';
            });
            
            // Ajouter touch-action: manipulation
            const interactiveElements = document.querySelectorAll('button, a, input');
            interactiveElements.forEach(element => {
                element.style.touchAction = 'manipulation';
            });
        }
    }

    handleOrientationChange() {
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                // Recalculer les tailles après changement d'orientation
                this.optimizeForTouch();
            }, 100);
        });
    }

    // ===== MODES AVANCÉS =====
    
    setupAdvancedModes() {
        // Mode performance réduite
        this.detectLowPerformance();
        
        // Mode contraste automatique
        this.setupAutoContrast();
        
        // Mode focus avancé
        this.setupAdvancedFocus();
    }

    detectLowPerformance() {
        // Détecter les appareils moins puissants
        const isLowPerformance = navigator.hardwareConcurrency < 4 || 
                                navigator.deviceMemory < 4 ||
                                window.innerWidth < 768;
        
        if (isLowPerformance) {
            document.body.classList.add('low-performance');
        }
    }

    setupAutoContrast() {
        // Détecter automatiquement le contraste nécessaire
        const prefersHighContrast = window.matchMedia('(prefers-contrast: high)').matches;
        if (prefersHighContrast) {
            document.body.classList.add('high-contrast');
        }
    }

    setupAdvancedFocus() {
        // Focus avancé avec indicateurs visuels
        document.addEventListener('focusin', (e) => {
            if (e.target.matches('button, input, select, textarea, a')) {
                e.target.classList.add('focus-advanced');
            }
        });

        document.addEventListener('focusout', (e) => {
            e.target.classList.remove('focus-advanced');
        });
    }

    // ===== MODES RAPIDES =====
    
    quickAccessibilityMode(key) {
        const modes = {
            '1': 'daltonian',
            '2': 'highContrast', 
            '3': 'dyslexia',
            '4': 'reducedMotion',
            '5': 'zoom',
            '6': 'spacing',
            '7': 'highlight',
            '8': 'hapticFeedback'
        };
        
        const mode = modes[key];
        if (mode) {
            if (mode === 'zoom' || mode === 'spacing' || mode === 'highlight' || mode === 'hapticFeedback') {
                const button = document.querySelector(`[data-action="${mode}"]`);
                if (button) {
                    this.handleAction(mode, button);
                }
            } else {
                const button = document.querySelector(`[data-mode="${mode}"]`);
                if (button) {
                    this.toggleMode(mode, button);
                }
            }
        }
    }

    // ===== UTILITAIRES =====
    
    closeModals() {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => {
            modal.classList.remove('active');
        });
    }

    toggleAccessibilityMenu() {
        const menu = document.getElementById('accessibility-menu');
        const overlay = document.getElementById('accessibility-overlay');
        const toggleBtn = document.getElementById('accessibility-toggle');
        
        if (menu && overlay && toggleBtn) {
            const isActive = menu.classList.contains('active');
            
            if (isActive) {
                // Fermer le menu
                menu.classList.remove('active');
                overlay.classList.remove('active');
                menu.setAttribute('aria-hidden', 'true');
                toggleBtn.setAttribute('aria-expanded', 'false');
                this.announceToScreenReader('Menu d\'accessibilité fermé');
            } else {
                // Ouvrir le menu
                menu.classList.add('active');
                overlay.classList.add('active');
                menu.setAttribute('aria-hidden', 'false');
                toggleBtn.setAttribute('aria-expanded', 'true');
                this.announceToScreenReader('Menu d\'accessibilité ouvert');
                
                // Focus sur le premier bouton du menu
                const firstButton = menu.querySelector('.accessibility-btn');
                if (firstButton) {
                    setTimeout(() => firstButton.focus(), 100);
                }
            }
        }
    }
    
    toggleAccessibilityPanel() {
        // Alias pour compatibilité
        this.toggleAccessibilityMenu();
    }

    applySettings() {
        // Appliquer les paramètres sauvegardés
        Object.entries(this.accessibilitySettings).forEach(([key, value]) => {
            if (value && key !== 'fontSize' && key !== 'hapticFeedback' && key !== 'zoom' && key !== 'spacing' && key !== 'highlight') {
                this.enableMode(key);
                const button = document.querySelector(`[data-mode="${key}"]`);
                if (button) {
                    button.setAttribute('aria-pressed', 'true');
                    button.classList.add('active');
                }
            }
        });
        
        // Appliquer les paramètres spéciaux
        this.setFontSize(this.accessibilitySettings.fontSize);
        this.setZoom(this.accessibilitySettings.zoom);
        this.setSpacing(this.accessibilitySettings.spacing);
        
        if (this.accessibilitySettings.highlight) {
            document.body.classList.add('highlight-focus', 'highlight-links', 'highlight-buttons');
            const button = document.querySelector('[data-action="highlight"]');
            if (button) {
                button.setAttribute('aria-pressed', 'true');
                button.classList.add('active');
            }
        }
    }

    // ===== API PUBLIQUE =====
    
    // Méthodes publiques pour les autres modules
    announce(message) {
        this.announceToScreenReader(message);
    }

    haptic(type = 'light') {
        this.triggerHapticFeedback(type);
    }

    setMode(mode, enabled) {
        if (enabled) {
            this.enableMode(mode);
        } else {
            this.disableMode(mode);
        }
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.accessibilityManager = new AccessibilityManager();
});

// Fonction globale pour le bouton de fermeture
window.toggleAccessibilityMenu = function() {
    if (window.accessibilityManager) {
        window.accessibilityManager.toggleAccessibilityMenu();
    }
};

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AccessibilityManager;
} 