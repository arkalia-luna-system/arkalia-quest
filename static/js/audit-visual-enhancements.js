/* ===== ARKALIA QUEST - AUDIT VISUAL ENHANCEMENTS ===== */
/* Améliorations JavaScript basées sur le rapport d'audit visuel */

class AuditVisualEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.enhanceEmptyStates();
        this.enhanceAnimations();
        this.enhanceNotifications();
        this.enhanceThemeSelection();
        this.enhanceResponsive();
        this.addMicroInteractions();
    }

    /* ===== 1. AMÉLIORATION DES ÉTATS VIDES ===== */
    enhanceEmptyStates() {
        // Remplacer les "0 XP", "0 Coins", "0 badges" par des messages motivants
        const emptyStats = document.querySelectorAll('.metric-value');
        emptyStats.forEach(stat => {
            if (stat.textContent === '0' || stat.textContent === 'N/A') {
                this.createMotivationalEmptyState(stat);
            }
        });

        // Améliorer les zones vides existantes
        const emptyStates = document.querySelectorAll('.empty-state');
        emptyStates.forEach(state => {
            this.addEmptyStateEnhancements(state);
        });
    }

    createMotivationalEmptyState(element) {
        const container = element.closest('.widget-content') || element.closest('.metric-display');
        if (!container) return;

        const emptyContainer = document.createElement('div');
        emptyContainer.className = 'empty-stats-container';

        emptyContainer.innerHTML = `
            <div class="empty-stats-icon">🚀</div>
            <div class="empty-stats-title">Prêt à commencer !</div>
            <div class="empty-stats-message">Tes premières récompenses t'attendent...</div>
            <div class="empty-stats-encouragement">Reviens demain pour récupérer tes récompenses !</div>
        `;

        // Remplacer l'élément par le nouveau conteneur
        if (element.parentNode) {
            element.parentNode.replaceChild(emptyContainer, element);
        }
    }

    addEmptyStateEnhancements(emptyState) {
        // Ajouter des animations subtiles
        emptyState.classList.add('fade-in-enhanced');

        // Ajouter des particules de fond
        this.addBackgroundParticles(emptyState);
    }

    /* ===== 2. AMÉLIORATION DES ANIMATIONS ===== */
    enhanceAnimations() {
        // Améliorer les animations d'apparition
        this.enhanceFadeInAnimations();

        // Ajouter des animations de célébration
        this.addCelebrationAnimations();

        // Améliorer les transitions de popup
        this.enhancePopupTransitions();
    }

    enhanceFadeInAnimations() {
        const elements = document.querySelectorAll('.widget, .challenge-item, .feature-card');
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px) scale(0.9)';

            setTimeout(() => {
                element.classList.add('fade-in-enhanced');
            }, index * 100);
        });
    }

    addCelebrationAnimations() {
        // Détecter les actions de succès
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('cta-btn') ||
                e.target.classList.contains('btn-primary') ||
                e.target.closest('.cta-btn') ||
                e.target.closest('.btn-primary')) {
                this.triggerCelebration(e.target);
            }
        });
    }

    triggerCelebration(element) {
        const celebration = document.createElement('div');
        celebration.className = 'celebration-burst';
        celebration.style.position = 'absolute';
        celebration.style.top = '50%';
        celebration.style.left = '50%';
        celebration.style.transform = 'translate(-50%, -50%)';
        celebration.style.pointerEvents = 'none';
        celebration.style.zIndex = '1000';

        element.style.position = 'relative';
        element.appendChild(celebration);

        setTimeout(() => {
            celebration.remove();
        }, 1000);
    }

    enhancePopupTransitions() {
        // Améliorer les transitions des modales
        const modals = document.querySelectorAll('.modal, .popup');
        modals.forEach(modal => {
            modal.addEventListener('show', () => {
                modal.classList.add('scale-in-bounce');
            });

            modal.addEventListener('hide', () => {
                modal.classList.add('fade-out');
            });
        });
    }

    /* ===== 3. AMÉLIORATION DES NOTIFICATIONS ===== */
    enhanceNotifications() {
        // Créer un système de notifications amélioré
        this.createNotificationSystem();

        // Améliorer les notifications existantes
        this.enhanceExistingNotifications();
    }

    createNotificationSystem() {
        // Créer le conteneur de notifications
        const notificationContainer = document.createElement('div');
        notificationContainer.id = 'audit-notification-container';
        notificationContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            pointer-events: none;
        `;
        document.body.appendChild(notificationContainer);
    }

    showEnhancedNotification(message, type = 'info', duration = 4000) {
        const container = document.getElementById('audit-notification-container');
        if (!container) return;

        const notification = document.createElement('div');
        notification.className = `system-notification ${type}`;
        notification.textContent = message;

        container.appendChild(notification);

        // Animation d'apparition
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Animation de disparition
        setTimeout(() => {
            notification.classList.add('hide');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, duration);
    }

    enhanceExistingNotifications() {
        // Améliorer les notifications existantes
        const existingNotifications = document.querySelectorAll('.notification-item');
        existingNotifications.forEach(notification => {
            notification.classList.add('slide-in-left');
        });
    }

    /* ===== 4. AMÉLIORATION DE LA SÉLECTION DE THÈMES ===== */
    enhanceThemeSelection() {
        const themeOptions = document.querySelectorAll('.theme-option, [data-theme]');
        themeOptions.forEach(option => {
            this.addThemeOptionEnhancements(option);
        });
    }

    addThemeOptionEnhancements(option) {
        // Ajouter des effets de survol améliorés
        option.addEventListener('mouseenter', () => {
            option.style.transform = 'translateY(-3px) scale(1.02)';
            option.style.boxShadow = '0 8px 25px rgba(167, 139, 250, 0.3)';
        });

        option.addEventListener('mouseleave', () => {
            option.style.transform = 'translateY(0) scale(1)';
            option.style.boxShadow = '0 4px 15px rgba(167, 139, 250, 0.1)';
        });

        // Ajouter des animations de sélection
        option.addEventListener('click', () => {
            this.triggerThemeSelection(option);
        });
    }

    triggerThemeSelection(option) {
        // Animation de sélection
        option.style.transform = 'scale(0.95)';
        setTimeout(() => {
            option.style.transform = 'scale(1.05)';
            setTimeout(() => {
                option.style.transform = 'scale(1)';
            }, 150);
        }, 100);

        // Notification de confirmation
        this.showEnhancedNotification('Thème appliqué avec succès !', 'success', 2000);
    }

    /* ===== 5. AMÉLIORATION DU RESPONSIVE ===== */
    enhanceResponsive() {
        // Détecter les changements de taille d'écran
        window.addEventListener('resize', () => {
            this.adaptToScreenSize();
        });

        // Adaptation initiale
        this.adaptToScreenSize();
    }

    adaptToScreenSize() {
        const width = window.innerWidth;

        if (width <= 768) {
            this.enableMobileOptimizations();
        } else {
            this.enableDesktopOptimizations();
        }
    }

    enableMobileOptimizations() {
        // Optimisations pour mobile
        const ctaButtons = document.querySelectorAll('.cta-btn');
        ctaButtons.forEach(btn => {
            btn.style.fontSize = '0.9em';
            btn.style.padding = '12px 16px';
        });

        // Réduire les espacements
        const containers = document.querySelectorAll('.widget, .challenge-item');
        containers.forEach(container => {
            container.style.padding = '15px';
            container.style.marginBottom = '15px';
        });
    }

    enableDesktopOptimizations() {
        // Optimisations pour desktop
        const ctaButtons = document.querySelectorAll('.cta-btn');
        ctaButtons.forEach(btn => {
            btn.style.fontSize = '1em';
            btn.style.padding = '16px 24px';
        });
    }

    /* ===== 6. MICRO-INTERACTIONS ===== */
    addMicroInteractions() {
        // Ajouter des micro-interactions subtiles
        this.addHoverEffects();
        this.addClickFeedback();
        this.addScrollAnimations();
    }

    addHoverEffects() {
        const interactiveElements = document.querySelectorAll('.btn, .card, .widget, .challenge-item');
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            });
        });
    }

    addClickFeedback() {
        const clickableElements = document.querySelectorAll('button, .btn, .cta-btn, .theme-option');
        clickableElements.forEach(element => {
            element.addEventListener('click', (e) => {
                // Effet de ripple
                this.createRippleEffect(e.target, e);
            });
        });
    }

    createRippleEffect(element, event) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(167, 139, 250, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;

        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    addScrollAnimations() {
        // Animation au scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-enhanced');
                }
            });
        }, { threshold: 0.1 });

        const animatedElements = document.querySelectorAll('.widget, .challenge-item, .feature-card');
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }

    /* ===== 7. PARTICULES DE FOND ===== */
    addBackgroundParticles(container) {
        const particles = document.createElement('div');
        particles.className = 'background-particles';
        particles.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
            overflow: hidden;
        `;

        // Créer des particules flottantes
        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(167, 139, 250, 0.3);
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: floatParticle ${3 + Math.random() * 2}s ease-in-out infinite;
            `;
            particles.appendChild(particle);
        }

        container.style.position = 'relative';
        container.appendChild(particles);
    }
}

// CSS pour les animations
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes floatParticle {
        0%, 100% {
            transform: translateY(0) translateX(0);
            opacity: 0.3;
        }
        50% {
            transform: translateY(-20px) translateX(10px);
            opacity: 0.8;
        }
    }
`;
document.head.appendChild(style);

// Initialiser les améliorations
document.addEventListener('DOMContentLoaded', () => {
    new AuditVisualEnhancements();
});

// Exporter pour utilisation globale
window.AuditVisualEnhancements = AuditVisualEnhancements;
