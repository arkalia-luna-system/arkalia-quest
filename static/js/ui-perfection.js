/* ===== ARKALIA QUEST - PERFECTION UI/UX 2025 ===== */

class UIPerfection {
    constructor() {
        this.init();
    }

    init() {
        console.log('🎨 UIPerfection initialisé');
        this.setupMicroTransitions();
        this.setupHoverEffects();
        this.setupEmptyStates();
        this.setupFeedbackSystem();
        this.setupLoadingStates();
    }

    /* ===== MICRO-TRANSITIONS LUXUEUSES ===== */
    setupMicroTransitions() {
        // Observer pour les nouveaux éléments
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        this.addTransitionClasses(node);
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Appliquer les transitions aux éléments existants
        this.addTransitionClasses(document.body);
    }

    addTransitionClasses(element) {
        // Boutons et CTA
        const buttons = element.querySelectorAll('button, .btn, .cta-btn, .button, a[role="button"]');
        buttons.forEach(btn => {
            if (!btn.classList.contains('transition-applied')) {
                btn.classList.add('btn-perfect', 'transition-applied');
            }
        });

        // Sections
        const sections = element.querySelectorAll('.section, .card, .panel, .modal, .popup');
        sections.forEach(section => {
            if (!section.classList.contains('transition-applied')) {
                section.classList.add('section-perfect', 'fade-in', 'transition-applied');
            }
        });

        // Icônes
        const icons = element.querySelectorAll('i, .icon, .emoji, [class*="icon"]');
        icons.forEach(icon => {
            if (!icon.classList.contains('transition-applied')) {
                icon.classList.add('icon-perfect', 'transition-applied');
            }
        });
    }

    /* ===== EFFETS DE SURVOL UNIFIÉS ===== */
    setupHoverEffects() {
        // Effet de survol pour tous les éléments interactifs
        document.addEventListener('mouseover', (e) => {
            const element = e.target.closest('.btn-perfect, .cta-perfect, .icon-perfect, .section-perfect');
            if (element) {
                this.addHoverEffect(element);
            }
        });

        document.addEventListener('mouseout', (e) => {
            const element = e.target.closest('.btn-perfect, .cta-perfect, .icon-perfect, .section-perfect');
            if (element) {
                this.removeHoverEffect(element);
            }
        });
    }

    addHoverEffect(element) {
        element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        element.style.transform = 'translateY(-2px) scale(1.02)';
        element.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
    }

    removeHoverEffect(element) {
        element.style.transform = 'translateY(0) scale(1)';
        element.style.boxShadow = '';
    }

    /* ===== ZONES VIDES ÉLÉGANTES ===== */
    setupEmptyStates() {
        // Détecter les zones vides et les styliser
        const emptySelectors = [
            '[data-empty-state]',
            '.empty-state',
            '.no-content',
            '.no-data'
        ];

        emptySelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                this.styleEmptyState(element);
            });
        });
    }

    styleEmptyState(element) {
        element.classList.add('empty-state-perfect');

        // Ajouter une icône si pas déjà présente
        if (!element.querySelector('.empty-state-icon')) {
            const icon = document.createElement('div');
            icon.className = 'empty-state-icon';
            icon.innerHTML = '✨';
            element.insertBefore(icon, element.firstChild);
        }

        // Ajouter un message si pas déjà présent
        if (!element.querySelector('.empty-state-message')) {
            const message = document.createElement('div');
            message.className = 'empty-state-message';
            message.textContent = 'Tout est à jour !';
            element.appendChild(message);
        }
    }

    /* ===== SYSTÈME DE FEEDBACK CONTEXTUEL ===== */
    setupFeedbackSystem() {
        // Système de feedback désactivé - utilise les systèmes universels
        console.log('🎨 Système de feedback UI désactivé - utilise les systèmes universels');
    }

    /* ===== ÉTATS DE CHARGEMENT ÉLÉGANTS ===== */
    setupLoadingStates() {
        // Remplacer les loaders basiques par des versions élégantes
        const loaders = document.querySelectorAll('.loading, .spinner, .loader');
        loaders.forEach(loader => {
            this.replaceWithElegantLoader(loader);
        });
    }

    replaceWithElegantLoader(element) {
        element.classList.add('loading-perfect');
        element.innerHTML = `
            <span class="loading-text">Chargement</span>
            <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
    }

    /* ===== ANIMATIONS D'APPARITION POUR NOUVEAUX ÉLÉMENTS ===== */
    animateNewElement(element) {
        element.classList.add('new-element');

        // Supprimer la classe après l'animation
        setTimeout(() => {
            element.classList.remove('new-element');
        }, 600);
    }

    /* ===== MÉTHODES PUBLIQUES ===== */
    enhanceElement(element) {
        this.addTransitionClasses(element);
        this.styleEmptyState(element);
    }

    showElegantFeedback(type, message) {
        const container = this.createFeedbackContainer();
        this.showFeedback(type, message, container);
    }

    animateContentUpdate(element) {
        element.style.transition = 'all 0.3s ease';
        element.style.transform = 'scale(1.05)';
        element.style.opacity = '0.8';

        setTimeout(() => {
            element.style.transform = 'scale(1)';
            element.style.opacity = '1';
        }, 150);
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.uiPerfection = new UIPerfection();
    console.log('✨ UI Perfection activé - Niveau premium 2025');
});

// Export pour utilisation globale
window.UIPerfection = UIPerfection;
