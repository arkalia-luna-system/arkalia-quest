/**
 * Système d'animations de célébration pour le tutoriel
 * Ajoute des micro-animations pour fêter chaque étape franchie
 */

class TutorialCelebrations {
    constructor() {
        this.celebrationQueue = [];
        this.isAnimating = false;

        this.initializeSystem();
    }

    initializeSystem() {
        console.log('🎉 Système de célébrations tutoriel initialisé');
        this.createCelebrationStyles();
        this.setupTutorialListeners();
    }

    createCelebrationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .tutorial-celebration {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10000;
                pointer-events: none;
            }
            
            .celebration-confetti {
                position: absolute;
                width: 10px;
                height: 10px;
                background: #00ff00;
                opacity: 0.7;
                animation: confetti-fall 3s ease-out forwards;
            }
            
            .celebration-star {
                position: absolute;
                font-size: 24px;
                color: rgba(0, 255, 0, 0.9);
                opacity: 0.8;
                text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
                animation: star-burst 2s ease-out forwards;
            }
            
            .celebration-text {
                position: absolute;
                top: -60px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(45deg, rgba(0, 255, 0, 0.8), rgba(0, 204, 0, 0.8));
                color: #000;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: bold;
                font-size: 16px;
                animation: celebration-text-pop 2s ease-out forwards;
                white-space: nowrap;
            }
            
            .tutorial-step-completed {
                animation: step-completed 1s ease-out;
                background: linear-gradient(45deg, rgba(0, 255, 0, 0.2), rgba(0, 204, 0, 0.2));
                border: 2px solid rgba(0, 255, 0, 0.6);
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0;
            }
            
            .tutorial-progress-bar {
                width: 100%;
                height: 8px;
                background: rgba(0, 255, 0, 0.2);
                border-radius: 4px;
                overflow: hidden;
                margin: 10px 0;
            }
            
            .tutorial-progress-fill {
                height: 100%;
                background: linear-gradient(90deg, rgba(0, 255, 0, 0.8), rgba(0, 204, 0, 0.8));
                width: 0%;
                transition: width 0.5s ease-out;
                border-radius: 4px;
            }
            
            .tutorial-xp-gain {
                position: absolute;
                top: -30px;
                right: 10px;
                color: rgba(0, 255, 0, 0.9);
                font-weight: bold;
                font-size: 14px;
                animation: xp-gain-float 2s ease-out forwards;
            }
            
            @keyframes confetti-fall {
                0% {
                    transform: translateY(-100px) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }
            
            @keyframes star-burst {
                0% {
                    transform: scale(0) rotate(0deg);
                    opacity: 1;
                }
                50% {
                    transform: scale(1.2) rotate(180deg);
                    opacity: 1;
                }
                100% {
                    transform: scale(0) rotate(360deg);
                    opacity: 0;
                }
            }
            
            @keyframes celebration-text-pop {
                0% {
                    transform: translateX(-50%) scale(0);
                    opacity: 0;
                }
                50% {
                    transform: translateX(-50%) scale(1.1);
                    opacity: 1;
                }
                100% {
                    transform: translateX(-50%) scale(1);
                    opacity: 0;
                }
            }
            
            @keyframes step-completed {
                0% {
                    transform: scale(1);
                    background: transparent;
                }
                50% {
                    transform: scale(1.05);
                    background: linear-gradient(45deg, rgba(0, 255, 0, 0.3), rgba(0, 204, 0, 0.3));
                }
                100% {
                    transform: scale(1);
                    background: linear-gradient(45deg, rgba(0, 255, 0, 0.2), rgba(0, 204, 0, 0.2));
                }
            }
            
            @keyframes xp-gain-float {
                0% {
                    transform: translateY(0);
                    opacity: 1;
                }
                100% {
                    transform: translateY(-50px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    setupTutorialListeners() {
        // Écouter les changements dans le tutoriel
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    this.checkForTutorialProgress();
                }
            });
        });

        // Observer les changements dans le contenu du tutoriel
        const tutorialContainer = document.querySelector('.tutorial-content, .tutorial-steps, .tutorial-container');
        if (tutorialContainer) {
            observer.observe(tutorialContainer, { childList: true, subtree: true });
        }

        // Observer les changements d'attributs (pour les classes de progression)
        document.addEventListener('DOMContentLoaded', () => {
            const tutorialElements = document.querySelectorAll('[class*="tutorial"], [class*="step"]');
            tutorialElements.forEach(element => {
                observer.observe(element, { attributes: true, attributeFilter: ['class'] });
            });
        });
    }

    // Vérifier les progrès du tutoriel
    checkForTutorialProgress() {
        // Chercher les éléments de progression
        const progressElements = document.querySelectorAll('.tutorial-step, .step, .tutorial-item');
        const completedElements = document.querySelectorAll('.completed, .tutorial-completed, .step-completed');

        // Si on trouve des éléments complétés, célébrer
        if (completedElements.length > 0) {
            this.celebrateStepCompletion(completedElements[completedElements.length - 1]);
        }

        // Mettre à jour la barre de progression
        this.updateProgressBar(completedElements.length, progressElements.length);
    }

    // Célébrer la complétion d'une étape
    celebrateStepCompletion(element) {
        if (this.isAnimating) {
            this.celebrationQueue.push(() => this.celebrateStepCompletion(element));
            return;
        }

        this.isAnimating = true;
        console.log('🎉 Célébration d\'étape tutoriel');

        // Ajouter la classe de célébration à l'élément
        element.classList.add('tutorial-step-completed');

        // Créer l'effet de confetti
        this.createConfettiEffect(element);

        // Créer l'effet d'étoiles
        this.createStarBurstEffect(element);

        // Afficher le texte de célébration
        this.showCelebrationText(element, this.getRandomCelebrationMessage());

        // Afficher le gain d'XP
        this.showXPGain(element, this.calculateXPGain());

        // Son de célébration (si supporté)
        this.playCelebrationSound();

        // Terminer l'animation
        setTimeout(() => {
            this.isAnimating = false;
            this.processCelebrationQueue();
        }, 2000);
    }

    // Créer l'effet de confetti
    createConfettiEffect(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < 20; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'celebration-confetti';
            confetti.style.left = centerX + (Math.random() - 0.5) * 100 + 'px';
            confetti.style.top = centerY + 'px';
            confetti.style.background = this.getRandomColor();
            confetti.style.animationDelay = Math.random() * 0.5 + 's';

            document.body.appendChild(confetti);

            setTimeout(() => confetti.remove(), 3000);
        }
    }

    // Créer l'effet d'étoiles
    createStarBurstEffect(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < 8; i++) {
            const star = document.createElement('div');
            star.className = 'celebration-star';
            star.textContent = '⭐';
            star.style.left = centerX + (Math.random() - 0.5) * 200 + 'px';
            star.style.top = centerY + (Math.random() - 0.5) * 200 + 'px';
            star.style.animationDelay = Math.random() * 0.3 + 's';

            document.body.appendChild(star);

            setTimeout(() => star.remove(), 2000);
        }
    }

    // Afficher le texte de célébration
    showCelebrationText(element, message) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const text = document.createElement('div');
        text.className = 'celebration-text';
        text.textContent = message;
        text.style.left = centerX + 'px';
        text.style.top = centerY + 'px';

        document.body.appendChild(text);

        setTimeout(() => text.remove(), 2000);
    }

    // Afficher le gain d'XP
    showXPGain(element, xp) {
        const rect = element.getBoundingClientRect();
        const xpElement = document.createElement('div');
        xpElement.className = 'tutorial-xp-gain';
        xpElement.textContent = `+${xp} XP`;
        xpElement.style.left = rect.right + 'px';
        xpElement.style.top = rect.top + 'px';

        element.appendChild(xpElement);

        setTimeout(() => xpElement.remove(), 2000);
    }

    // Mettre à jour la barre de progression
    updateProgressBar(completed, total) {
        let progressBar = document.querySelector('.tutorial-progress-fill');

        if (!progressBar) {
            // Créer la barre de progression si elle n'existe pas
            const container = document.querySelector('.tutorial-content, .tutorial-steps, .tutorial-container');
            if (container) {
                const progressContainer = document.createElement('div');
                progressContainer.className = 'tutorial-progress-bar';
                progressContainer.innerHTML = '<div class="tutorial-progress-fill"></div>';
                container.insertBefore(progressContainer, container.firstChild);
                progressBar = progressContainer.querySelector('.tutorial-progress-fill');
            }
        }

        if (progressBar) {
            const percentage = total > 0 ? (completed / total) * 100 : 0;
            progressBar.style.width = percentage + '%';

            // Célébrer si 100% complété
            if (percentage >= 100) {
                this.celebrateTutorialCompletion();
            }
        }
    }

    // Célébrer la complétion du tutoriel
    celebrateTutorialCompletion() {
        console.log('🎊 Tutoriel complété !');

        // Effet de célébration majeur
        this.createConfettiEffect(document.body);
        this.createStarBurstEffect(document.body);

        // Message de félicitations
        this.showCelebrationText(document.body, '🎉 Tutoriel terminé ! Félicitations !');

        // Récompense spéciale
        this.showXPGain(document.body, 500);

        // Notification LUNA
        this.showLunaCongratulation();
    }

    // Afficher les félicitations de LUNA
    showLunaCongratulation() {
        const lunaMessages = [
            "🌟 Incroyable ! Tu as maîtrisé les bases !",
            "🚀 LUNA est fière de toi !",
            "💫 Tu es prêt pour l'aventure !",
            "🎯 Excellent travail, jeune hacker !",
            "✨ LUNA détecte un grand potentiel !"
        ];

        const message = lunaMessages[Math.floor(Math.random() * lunaMessages.length)];

        // Afficher dans le terminal si disponible
        const terminal = document.querySelector('.terminal-output, .luna-response');
        if (terminal) {
            const lunaResponse = document.createElement('div');
            lunaResponse.className = 'luna-message celebration';
            lunaResponse.innerHTML = `🌙 LUNA: ${message}`;
            terminal.appendChild(lunaResponse);
        }
    }

    // Obtenir un message de célébration aléatoire
    getRandomCelebrationMessage() {
        const messages = [
            "Excellent !",
            "Bravo !",
            "Parfait !",
            "Génial !",
            "Super !",
            "Fantastique !",
            "Incroyable !",
            "Magnifique !",
            "Formidable !",
            "Impressionnant !"
        ];

        return messages[Math.floor(Math.random() * messages.length)];
    }

    // Calculer le gain d'XP
    calculateXPGain() {
        return Math.floor(Math.random() * 50) + 25; // 25-75 XP
    }

    // Obtenir une couleur aléatoire
    getRandomColor() {
        const colors = ['#00ff00', '#00cc00', '#ffff00', '#ff6600', '#ff0066', '#6600ff'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    // Jouer un son de célébration
    playCelebrationSound() {
        // Créer un son simple avec Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);

            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
        } catch (e) {
            console.log('Audio non supporté');
        }
    }

    // Traiter la file d'attente des célébrations
    processCelebrationQueue() {
        if (this.celebrationQueue.length > 0) {
            const nextCelebration = this.celebrationQueue.shift();
            nextCelebration();
        }
    }

    // Détecter automatiquement les progrès
    detectProgress() {
        // Chercher les patterns de progression dans le DOM
        const progressIndicators = document.querySelectorAll('[class*="progress"], [class*="step"], [class*="tutorial"]');

        progressIndicators.forEach(indicator => {
            if (indicator.textContent.includes('complété') ||
                indicator.textContent.includes('terminé') ||
                indicator.classList.contains('completed')) {
                this.celebrateStepCompletion(indicator);
            }
        });
    }
}

// Initialiser le système de célébrations
window.tutorialCelebrations = new TutorialCelebrations();

// Détecter les progrès au chargement
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.tutorialCelebrations.detectProgress();
    }, 1000);
});
