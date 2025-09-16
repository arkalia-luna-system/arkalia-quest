/**
 * LEGACY (DEPRECATED) - Système de guidage visuel pour les débutants
 * Désactivé au profit des notifications unifiées et d'une UX non-intrusive.
 */

class VisualGuidance {
    constructor() {
        this.activeHighlights = new Map();
        this.guidanceQueue = [];
        this.isActive = false;

        this.initializeSystem();
    }

    initializeSystem() {
        console.log('🎯 Système de guidage visuel initialisé');
        this.createGuidanceStyles();
        this.setupEventListeners();
    }

    createGuidanceStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .guidance-highlight {
                position: relative;
                animation: guidance-pulse 2s ease-in-out infinite;
                z-index: 1000;
            }
            
            .guidance-pulse {
                animation: guidance-pulse 1.5s ease-in-out infinite;
            }
            
            .guidance-bounce {
                animation: guidance-bounce 1s ease-in-out infinite;
            }
            
            .guidance-glow {
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5), 0 0 40px rgba(0, 255, 0, 0.3), 0 0 60px rgba(0, 255, 0, 0.2);
                animation: guidance-glow 2s ease-in-out infinite;
            }
            
            .guidance-arrow {
                position: absolute;
                top: -30px;
                left: 50%;
                transform: translateX(-50%);
                font-size: 24px;
                color: rgba(0, 255, 0, 0.8);
                animation: guidance-arrow-bounce 1s ease-in-out infinite;
                z-index: 1001;
            }
            
            .guidance-tooltip {
                position: absolute;
                top: -50px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 255, 0, 0.9);
                color: #000;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                white-space: nowrap;
                z-index: 1002;
                animation: guidance-tooltip-fade 3s ease-in-out;
            }
            
            @keyframes guidance-pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.05); opacity: 0.8; }
            }
            
            @keyframes guidance-bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-5px); }
            }
            
            @keyframes guidance-glow {
                0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.5), 0 0 40px rgba(0, 255, 0, 0.3), 0 0 60px rgba(0, 255, 0, 0.2); }
                50% { box-shadow: 0 0 30px rgba(0, 255, 0, 0.6), 0 0 50px rgba(0, 255, 0, 0.4), 0 0 80px rgba(0, 255, 0, 0.3); }
            }
            
            @keyframes guidance-arrow-bounce {
                0%, 100% { transform: translateX(-50%) translateY(0); }
                50% { transform: translateX(-50%) translateY(-10px); }
            }
            
            @keyframes guidance-tooltip-fade {
                0% { opacity: 0; transform: translateX(-50%) translateY(10px); }
                20% { opacity: 1; transform: translateX(-50%) translateY(0); }
                80% { opacity: 1; transform: translateX(-50%) translateY(0); }
                100% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
            }
            
            .guidance-blink {
                animation: guidance-blink 1s ease-in-out infinite;
            }
            
            @keyframes guidance-blink {
                0%, 50% { opacity: 1; }
                25%, 75% { opacity: 0.3; }
            }
            
            .guidance-attract {
                animation: guidance-attract 2s ease-in-out infinite;
                transform-origin: center;
            }
            
            @keyframes guidance-attract {
                0%, 100% { transform: scale(1) rotate(0deg); }
                25% { transform: scale(1.05) rotate(1deg); }
                50% { transform: scale(1.1) rotate(0deg); }
                75% { transform: scale(1.05) rotate(-1deg); }
            }
            
            .guidance-sparkle {
                position: relative;
                overflow: visible;
            }
            
            .guidance-sparkle::before {
                content: '✨';
                position: absolute;
                top: -20px;
                right: -20px;
                font-size: 20px;
                animation: guidance-sparkle-float 2s ease-in-out infinite;
            }
            
            @keyframes guidance-sparkle-float {
                0%, 100% { transform: translateY(0) rotate(0deg); opacity: 1; }
                50% { transform: translateY(-15px) rotate(180deg); opacity: 0.7; }
            }
        `;
        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Détecter les clics sur les éléments guidés
        document.addEventListener('click', (e) => {
            const guidedElement = e.target.closest('.guidance-highlight');
            if (guidedElement) {
                this.onGuidedElementClick(guidedElement);
            }
        });

        // Détecter les survols
        document.addEventListener('mouseover', (e) => {
            const guidedElement = e.target.closest('.guidance-highlight');
            if (guidedElement) {
                this.onGuidedElementHover(guidedElement);
            }
        });
    }

    // Guider vers un élément spécifique
    highlightElement(selector, options = {}) {
        const element = document.querySelector(selector);
        if (!element) {
            console.warn(`Élément non trouvé: ${selector}`);
            return false;
        }

        const config = {
            duration: 5000,
            type: 'pulse',
            message: 'Cliquez ici pour commencer !',
            showArrow: true,
            showTooltip: true,
            ...options
        };

        // Ajouter les classes de guidage
        element.classList.add('guidance-highlight', `guidance-${config.type}`);

        // Ajouter des effets spéciaux selon le type
        if (config.blink) element.classList.add('guidance-blink');
        if (config.attract) element.classList.add('guidance-attract');
        if (config.sparkle) element.classList.add('guidance-sparkle');

        // Ajouter une flèche si demandé
        if (config.showArrow) {
            const arrow = document.createElement('div');
            arrow.className = 'guidance-arrow';
            arrow.textContent = '↑';
            element.appendChild(arrow);
        }

        // Ajouter un tooltip si demandé
        if (config.showTooltip && config.message) {
            const tooltip = document.createElement('div');
            tooltip.className = 'guidance-tooltip';
            tooltip.textContent = config.message;
            element.appendChild(tooltip);
        }

        // Enregistrer l'highlight actif
        this.activeHighlights.set(selector, {
            element,
            config,
            startTime: Date.now()
        });

        // Programmer la suppression
        setTimeout(() => {
            this.removeHighlight(selector);
        }, config.duration);

        return true;
    }

    // Supprimer un highlight
    removeHighlight(selector) {
        const highlight = this.activeHighlights.get(selector);
        if (!highlight) return;

        const { element } = highlight;

        // Supprimer les classes
        element.classList.remove('guidance-highlight', 'guidance-pulse', 'guidance-bounce', 'guidance-glow');

        // Supprimer les éléments ajoutés
        const arrow = element.querySelector('.guidance-arrow');
        const tooltip = element.querySelector('.guidance-tooltip');

        if (arrow) arrow.remove();
        if (tooltip) tooltip.remove();

        this.activeHighlights.delete(selector);
    }

    // Guider un débutant dans le parcours d'onboarding - DÉSACTIVÉ
    guideBeginner() {
        console.log('🎯 Guidance débutant désactivée - interface propre');
        return; // Sortie immédiate
    }

    // Exécuter une séquence de guidage
    executeGuidanceSequence(sequence, index = 0) {
        if (index >= sequence.length) {
            console.log('✅ Séquence de guidage terminée');
            return;
        }

        const step = sequence[index];
        console.log(`🎯 Étape ${index + 1}/${sequence.length}: ${step.message}`);

        // Attendre un peu avant de commencer
        setTimeout(() => {
            const success = this.highlightElement(step.selector, step);

            if (success) {
                // Passer à l'étape suivante après la durée + un délai
                setTimeout(() => {
                    this.executeGuidanceSequence(sequence, index + 1);
                }, step.duration + 1000);
            } else {
                // Si l'élément n'existe pas, passer à l'étape suivante
                this.executeGuidanceSequence(sequence, index + 1);
            }
        }, 500);
    }

    // Guider vers les défis quotidiens
    guideToDailyChallenges() {
        this.highlightElement('.daily-challenges, [href*="challenges"]', {
            message: '🎯 Défis quotidiens disponibles !',
            type: 'pulse',
            duration: 6000,
            showArrow: true,
            showTooltip: true
        });
    }

    // Guider vers les mini-jeux
    guideToMiniGames() {
        this.highlightElement('.mini-games, [href*="games"]', {
            message: '🎮 Mini-jeux interactifs !',
            type: 'bounce',
            duration: 5000,
            showArrow: true,
            showTooltip: true,
            sparkle: true
        });
    }

    // Guider automatiquement les débutants - DÉSACTIVÉ (trop agressive)
    guideBeginner() {
        console.log('🎯 Guidance automatique désactivée - interface plus propre');
        // Guidance complètement supprimée - les utilisateurs peuvent explorer naturellement
        // Plus de popups agressives ou de highlights automatiques
        return; // Sortie immédiate
    }

    // Guider vers les défis quotidiens
    guideToDailyChallenges() {
        this.highlightElement('.daily-challenges, [href*="challenges"]', {
            message: '🎯 Défis quotidiens disponibles !',
            type: 'attract',
            duration: 5000,
            showArrow: true,
            showTooltip: true,
            sparkle: true
        });
    }

    // Guider vers le profil
    guideToProfile() {
        this.highlightElement('.profile-link, [href*="profil"]', {
            message: '👤 Consultez votre profil et vos badges !',
            type: 'pulse',
            duration: 5000,
            showArrow: true,
            showTooltip: true
        });
    }

    // Callback quand un élément guidé est cliqué
    onGuidedElementClick(element) {
        console.log('✅ Élément guidé cliqué:', element);

        // Supprimer tous les highlights
        this.clearAllHighlights();

        // Feedback positif
        this.showSuccessFeedback('Bien joué ! Vous progressez !');
    }

    // Callback quand un élément guidé est survolé
    onGuidedElementHover(element) {
        // Intensifier l'effet
        element.classList.add('guidance-glow');

        setTimeout(() => {
            element.classList.remove('guidance-glow');
        }, 200);
    }

    // Supprimer tous les highlights
    clearAllHighlights() {
        this.activeHighlights.forEach((_, selector) => {
            this.removeHighlight(selector);
        });
    }

    // Afficher un feedback de succès
    showSuccessFeedback(message) {
        if (window.universalNotifications) {
            window.universalNotifications.info(message);
        }
    }

    // Détecter si l'utilisateur est un débutant
    isBeginner() {
        const profile = JSON.parse(localStorage.getItem('arkalia_profile') || '{}');
        const level = profile.level || 1;
        const missionsCompleted = profile.missions_completed || [];

        return level <= 2 && missionsCompleted.length <= 1;
    }

    // Auto-guidage intelligent
    autoGuide() {
        // Guidance automatique complètement désactivée
        console.log('🎯 Auto-guidance désactivée - interface propre');
        return; // Sortie immédiate
    }
}

// Initialiser le système de guidage
window.visualGuidance = new VisualGuidance();

// Auto-guidage pour les débutants
// Auto-guidance DÉSACTIVÉE - trop agressive
// document.addEventListener('DOMContentLoaded', () => {
//     if (window.visualGuidance.isBeginner()) {
//         window.visualGuidance.autoGuide();
//     }
// });
