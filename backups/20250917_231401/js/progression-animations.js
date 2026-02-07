/**
 * Système d'animations de progression et de récompenses
 * Améliore l'expérience utilisateur avec des effets visuels
 */

class ProgressionAnimationSystem {
    constructor() {
        this.animationQueue = [];
        this.isAnimating = false;
        this.initializeSystem();
    }

    initializeSystem() {
        // Créer les styles d'animation dynamiques
        this.createAnimationStyles();

        // Observer les changements de progression
        this.observeProgressionChanges();

        // Initialiser les effets de chargement
        this.initializeLoadingEffects();
    }

    createAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .progression-animation {
                position: relative;
                overflow: hidden;
            }
            
            .progression-animation::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.3), transparent);
                animation: progression-sweep 2s ease-in-out;
            }
            
            @keyframes progression-sweep {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            .level-up-animation {
                position: relative;
                animation: level-up-glow 1s ease-in-out;
            }
            
            @keyframes level-up-glow {
                0%, 100% { 
                    box-shadow: 0 0 20px #00ff00;
                    transform: scale(1);
                }
                50% { 
                    box-shadow: 0 0 40px #00ff00, 0 0 60px #00ff00;
                    transform: scale(1.05);
                }
            }
            
            .badge-unlock-animation {
                position: relative;
                animation: badge-unlock 1.5s ease-in-out;
            }
            
            @keyframes badge-unlock {
                0% { 
                    transform: scale(0) rotate(0deg);
                    opacity: 0;
                }
                50% { 
                    transform: scale(1.2) rotate(180deg);
                    opacity: 1;
                }
                100% { 
                    transform: scale(1) rotate(360deg);
                    opacity: 1;
                }
            }
            
            .confetti-animation {
                position: relative;
                overflow: hidden;
            }
            
            .confetti-animation::before,
            .confetti-animation::after {
                content: '';
                position: absolute;
                width: 10px;
                height: 10px;
                background: #00ff00;
                animation: confetti-fall 2s ease-in-out infinite;
            }
            
            .confetti-animation::before {
                left: 20%;
                animation-delay: 0s;
            }
            
            .confetti-animation::after {
                left: 80%;
                animation-delay: 1s;
            }
            
            @keyframes confetti-fall {
                0% { 
                    transform: translateY(-100vh) rotate(0deg);
                    opacity: 1;
                }
                100% { 
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    observeProgressionChanges() {
        // Observer les changements dans les éléments de progression
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' || mutation.type === 'attributes') {
                    this.checkForProgressionChanges(mutation);
                }
            });
        });

        // Observer les éléments de progression
        const progressionElements = document.querySelectorAll('.progression, .level, .badge, .score');
        progressionElements.forEach(element => {
            observer.observe(element, {
                attributes: true,
                childList: true,
                subtree: true
            });
        });
    }

    checkForProgressionChanges(mutation) {
        const target = mutation.target;

        // Vérifier si c'est un changement de niveau
        if (target.classList.contains('level') && mutation.type === 'attributes') {
            this.animateLevelUp(target);
        }

        // Vérifier si c'est un nouveau badge
        if (target.classList.contains('badge') && mutation.type === 'childList') {
            this.animateBadgeUnlock(target);
        }

        // Vérifier si c'est une progression
        if (target.classList.contains('progression') && mutation.type === 'attributes') {
            this.animateProgression(target);
        }
    }

    animateLevelUp(element) {
        element.classList.add('level-up-animation');

        // Créer un effet de confetti
        this.createConfettiEffect(element);

        // Afficher un message de félicitations
        this.showCongratulationMessage('Niveau supérieur atteint !', 'success');

        // Supprimer l'animation après 2 secondes
        setTimeout(() => {
            element.classList.remove('level-up-animation');
        }, 2000);
    }

    animateBadgeUnlock(element) {
        element.classList.add('badge-unlock-animation');

        // Créer un effet de particules
        this.createParticleEffect(element);

        // Afficher un message de félicitations
        this.showCongratulationMessage('Nouveau badge débloqué !', 'success');

        // Supprimer l'animation après 2 secondes
        setTimeout(() => {
            element.classList.remove('badge-unlock-animation');
        }, 2000);
    }

    animateProgression(element) {
        element.classList.add('progression-animation');

        // Supprimer l'animation après 2 secondes
        setTimeout(() => {
            element.classList.remove('progression-animation');
        }, 2000);
    }

    createConfettiEffect(element) {
        const rect = element.getBoundingClientRect();
        const colors = ['#00ff00', '#0080ff', '#ff8000', '#ff00ff', '#ffff00'];

        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.position = 'fixed';
                confetti.style.left = rect.left + rect.width / 2 + 'px';
                confetti.style.top = rect.top + 'px';
                confetti.style.width = '10px';
                confetti.style.height = '10px';
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.pointerEvents = 'none';
                confetti.style.zIndex = '9999';
                confetti.style.borderRadius = '50%';

                // Animation de chute
                confetti.style.animation = `confetti-fall ${2 + Math.random() * 2}s ease-in-out forwards`;
                confetti.style.transform = `translateX(${(Math.random() - 0.5) * 200}px)`;

                document.body.appendChild(confetti);

                // Supprimer après l'animation
                setTimeout(() => {
                    if (confetti.parentNode) {
                        confetti.parentNode.removeChild(confetti);
                    }
                }, 4000);
            }, i * 50);
        }
    }

    createParticleEffect(element) {
        const rect = element.getBoundingClientRect();
        const colors = ['#00ff00', '#0080ff', '#ff8000'];

        for (let i = 0; i < 15; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.style.position = 'fixed';
                particle.style.left = rect.left + rect.width / 2 + 'px';
                particle.style.top = rect.top + rect.height / 2 + 'px';
                particle.style.width = '6px';
                particle.style.height = '6px';
                particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                particle.style.pointerEvents = 'none';
                particle.style.zIndex = '9999';
                particle.style.borderRadius = '50%';

                // Animation d'explosion
                const angle = (i / 15) * Math.PI * 2;
                const distance = 100 + Math.random() * 50;
                const endX = Math.cos(angle) * distance;
                const endY = Math.sin(angle) * distance;

                particle.style.animation = `particle-explosion 1s ease-out forwards`;
                particle.style.setProperty('--end-x', endX + 'px');
                particle.style.setProperty('--end-y', endY + 'px');

                document.body.appendChild(particle);

                // Supprimer après l'animation
                setTimeout(() => {
                    if (particle.parentNode) {
                        particle.parentNode.removeChild(particle);
                    }
                }, 1000);
            }, i * 30);
        }
    }

    showCongratulationMessage(message, type = 'success') {
        const messageElement = document.createElement('div');
        messageElement.className = `congratulation-message ${type}`;
        messageElement.textContent = message;

        // Styles
        messageElement.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(45deg, #00ff00, #0080ff);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            z-index: 10000;
            animation: message-appear 0.5s ease-out;
        `;

        // Ajouter l'animation CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes message-appear {
                0% { 
                    opacity: 0; 
                    transform: translate(-50%, -50%) scale(0.5); 
                }
                100% { 
                    opacity: 1; 
                    transform: translate(-50%, -50%) scale(1); 
                }
            }
            
            @keyframes particle-explosion {
                0% { 
                    transform: translate(0, 0) scale(1);
                    opacity: 1;
                }
                100% { 
                    transform: translate(var(--end-x), var(--end-y)) scale(0);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(messageElement);

        // Supprimer après 3 secondes
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 3000);
    }

    initializeLoadingEffects() {
        // Remplacer les "Chargement..." par des animations
        const loadingElements = document.querySelectorAll('[class*="loading"], [class*="chargement"]');
        loadingElements.forEach(element => {
            this.enhanceLoadingElement(element);
        });
    }

    enhanceLoadingElement(element) {
        element.classList.add('loading-animation');

        // Ajouter un spinner animé
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '⏳';
        spinner.style.cssText = `
            display: inline-block;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        `;

        // Ajouter l'animation de rotation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);

        element.insertBefore(spinner, element.firstChild);
    }

    // Méthode publique pour déclencher des animations
    triggerAnimation(type, element, options = {}) {
        switch (type) {
            case 'levelUp':
                this.animateLevelUp(element);
                break;
            case 'badgeUnlock':
                this.animateBadgeUnlock(element);
                break;
            case 'progression':
                this.animateProgression(element);
                break;
            case 'confetti':
                this.createConfettiEffect(element);
                break;
            case 'particles':
                this.createParticleEffect(element);
                break;
            default:
                console.warn('Type d\'animation non reconnu:', type);
        }
    }

    // Méthode pour créer des effets de victoire
    createVictoryEffect(element) {
        // Combiner plusieurs effets
        this.createConfettiEffect(element);
        this.createParticleEffect(element);
        this.showCongratulationMessage('VICTOIRE !', 'success');

        // Effet de vibration (si supporté)
        if (navigator.vibrate) {
            navigator.vibrate([200, 100, 200]);
        }
    }

    // Méthode pour créer des effets de défaite
    createDefeatEffect(element) {
        element.style.animation = 'error-shake 0.5s ease-in-out';
        this.showCongratulationMessage('Essaie encore !', 'error');

        // Supprimer l'animation après 0.5 secondes
        setTimeout(() => {
            element.style.animation = '';
        }, 500);
    }

    // Méthode pour créer des effets de pause
    createPauseEffect(element) {
        element.style.animation = 'pulse 1s ease-in-out infinite';
        this.showCongratulationMessage('Pause détectée', 'info');
    }

    // Méthode pour créer des effets de reprise
    createResumeEffect(element) {
        element.style.animation = 'fadeIn 0.5s ease-in-out';
        this.showCongratulationMessage('Reprise !', 'success');

        // Supprimer l'animation après 0.5 secondes
        setTimeout(() => {
            element.style.animation = '';
        }, 500);
    }
}

// Initialiser le système d'animations
const progressionAnimations = new ProgressionAnimationSystem();

// Exporter pour utilisation globale
window.ProgressionAnimationSystem = ProgressionAnimationSystem;
window.progressionAnimations = progressionAnimations;
