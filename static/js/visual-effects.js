/**
 * Système d'effets visuels pour Arkalia Quest
 * Améliore l'expérience utilisateur avec des animations et effets
 */

class VisualEffects {
    constructor() {
        this.effectsContainer = null;
        this.init();
    }

    init() {
        // Créer le conteneur d'effets
        this.createEffectsContainer();

        // Écouter les événements de récompenses
        this.setupEventListeners();
    }

    createEffectsContainer() {
        // Créer un conteneur pour les effets visuels
        this.effectsContainer = document.createElement('div');
        this.effectsContainer.id = 'visual-effects-container';
        this.effectsContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            overflow: hidden;
        `;

        document.body.appendChild(this.effectsContainer);
    }

    setupEventListeners() {
        // Écouter les événements de récompenses
        document.addEventListener('badgeUnlocked', (e) => {
            this.showBadgeEffect(e.detail);
        });

        document.addEventListener('levelUp', (e) => {
            this.showLevelUpEffect(e.detail);
        });

        document.addEventListener('scoreGained', (e) => {
            this.showScoreEffect(e.detail);
        });

        document.addEventListener('missionComplete', (e) => {
            this.showMissionCompleteEffect(e.detail);
        });
    }

    showBadgeEffect(badgeData) {
        // Effet de confettis pour un badge débloqué
        this.createConfetti();

        // Animation de badge
        const badgeElement = this.createBadgeElement(badgeData);
        this.effectsContainer.appendChild(badgeElement);

        // Animation d'entrée
        badgeElement.style.transform = 'scale(0) translateY(-100px)';
        badgeElement.style.opacity = '0';

        setTimeout(() => {
            badgeElement.style.transition = 'all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            badgeElement.style.transform = 'scale(1) translateY(0)';
            badgeElement.style.opacity = '1';
        }, 100);

        // Supprimer après l'animation
        setTimeout(() => {
            badgeElement.style.transition = 'all 0.4s ease-out';
            badgeElement.style.transform = 'scale(0.8) translateY(50px)';
            badgeElement.style.opacity = '0';
            setTimeout(() => {
                if (badgeElement.parentNode) {
                    badgeElement.parentNode.removeChild(badgeElement);
                }
            }, 400);
        }, 3000);
    }

    showLevelUpEffect(levelData) {
        // Effet de montée de niveau
        this.createLevelUpAnimation(levelData);

        // Particules d'étoiles
        this.createStarParticles();

        // Son de succès (si supporté)
        this.playSuccessSound();
    }

    showScoreEffect(scoreData) {
        // Animation de score gagné
        const scoreElement = this.createScoreElement(scoreData);
        this.effectsContainer.appendChild(scoreElement);

        // Animation flottante
        this.animateFloatingText(scoreElement);
    }

    showMissionCompleteEffect(missionData) {
        // Feux d'artifice pour mission complétée
        this.createFireworks();

        // Message de félicitations
        this.showCongratulationsMessage(missionData);
    }

    createBadgeElement(badgeData) {
        const badgeElement = document.createElement('div');
        badgeElement.className = 'badge-effect';
        badgeElement.innerHTML = `
            <div class="badge-icon">🏆</div>
            <div class="badge-text">Nouveau Badge !</div>
            <div class="badge-name">${badgeData.name || 'Badge Secret'}</div>
        `;

        badgeElement.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            z-index: 10000;
        `;

        return badgeElement;
    }

    createLevelUpAnimation(levelData) {
        const levelElement = document.createElement('div');
        levelElement.className = 'level-up-effect';
        levelElement.innerHTML = `
            <div class="level-up-text">LEVEL UP!</div>
            <div class="level-number">Niveau ${levelData.newLevel || '?'}</div>
        `;

        levelElement.style.cssText = `
            position: absolute;
            top: 30%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px 50px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            text-align: center;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 24px;
            z-index: 10000;
            animation: levelUpPulse 2s ease-in-out;
        `;

        // Ajouter l'animation CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes levelUpPulse {
                0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
                50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        this.effectsContainer.appendChild(levelElement);

        setTimeout(() => {
            if (levelElement.parentNode) {
                levelElement.parentNode.removeChild(levelElement);
            }
        }, 2000);
    }

    createScoreElement(scoreData) {
        const scoreElement = document.createElement('div');
        scoreElement.className = 'score-effect';
        scoreElement.innerHTML = `+${scoreData.amount || 0} points`;

        scoreElement.style.cssText = `
            position: absolute;
            top: 20%;
            right: 20%;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 18px;
            text-shadow: 0 0 10px #00ff00;
            z-index: 10000;
        `;

        return scoreElement;
    }

    createConfetti() {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];
        const confettiCount = 50;

        for (let i = 0; i < confettiCount; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.cssText = `
                    position: absolute;
                    width: 10px;
                    height: 10px;
                    background: ${colors[Math.floor(Math.random() * colors.length)]};
                    top: -10px;
                    left: ${Math.random() * 100}%;
                    animation: confettiFall ${2 + Math.random() * 3}s linear forwards;
                    z-index: 10000;
                `;

                this.effectsContainer.appendChild(confetti);

                setTimeout(() => {
                    if (confetti.parentNode) {
                        confetti.parentNode.removeChild(confetti);
                    }
                }, 5000);
            }, i * 50);
        }

        // Ajouter l'animation CSS pour les confettis
        if (!document.getElementById('confetti-animation')) {
            const style = document.createElement('style');
            style.id = 'confetti-animation';
            style.textContent = `
                @keyframes confettiFall {
                    0% {
                        transform: translateY(-100vh) rotate(0deg);
                        opacity: 1;
                    }
                    100% {
                        transform: translateY(100vh) rotate(720deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    createStarParticles() {
        const starCount = 20;

        for (let i = 0; i < starCount; i++) {
            setTimeout(() => {
                const star = document.createElement('div');
                star.innerHTML = '⭐';
                star.style.cssText = `
                    position: absolute;
                    top: ${Math.random() * 100}%;
                    left: ${Math.random() * 100}%;
                    font-size: ${20 + Math.random() * 20}px;
                    animation: starTwinkle ${1 + Math.random() * 2}s ease-in-out infinite;
                    z-index: 10000;
                `;

                this.effectsContainer.appendChild(star);

                setTimeout(() => {
                    if (star.parentNode) {
                        star.parentNode.removeChild(star);
                    }
                }, 3000);
            }, i * 100);
        }

        // Ajouter l'animation CSS pour les étoiles
        if (!document.getElementById('star-animation')) {
            const style = document.createElement('style');
            style.id = 'star-animation';
            style.textContent = `
                @keyframes starTwinkle {
                    0%, 100% { opacity: 0; transform: scale(0.5); }
                    50% { opacity: 1; transform: scale(1); }
                }
            `;
            document.head.appendChild(style);
        }
    }

    createFireworks() {
        const fireworkCount = 5;

        for (let i = 0; i < fireworkCount; i++) {
            setTimeout(() => {
                this.createSingleFirework();
            }, i * 500);
        }
    }

    createSingleFirework() {
        const firework = document.createElement('div');
        firework.style.cssText = `
            position: absolute;
            top: ${20 + Math.random() * 60}%;
            left: ${20 + Math.random() * 60}%;
            width: 4px;
            height: 4px;
            background: #ff6b6b;
            border-radius: 50%;
            animation: fireworkExplode 1s ease-out forwards;
            z-index: 10000;
        `;

        this.effectsContainer.appendChild(firework);

        setTimeout(() => {
            if (firework.parentNode) {
                firework.parentNode.removeChild(firework);
            }
        }, 1000);

        // Ajouter l'animation CSS pour les feux d'artifice
        if (!document.getElementById('firework-animation')) {
            const style = document.createElement('style');
            style.id = 'firework-animation';
            style.textContent = `
                @keyframes fireworkExplode {
                    0% {
                        transform: scale(0);
                        opacity: 1;
                    }
                    50% {
                        transform: scale(1);
                        opacity: 1;
                    }
                    100% {
                        transform: scale(2);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    animateFloatingText(element) {
        const startY = element.style.top;
        const endY = (parseInt(startY) - 50) + 'px';

        element.style.transition = 'all 2s ease-out';
        element.style.top = endY;
        element.style.opacity = '0';

        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }, 2000);
    }

    showCongratulationsMessage(missionData) {
        const messageElement = document.createElement('div');
        messageElement.className = 'congratulations-message';
        messageElement.innerHTML = `
            <div class="congrats-text">🎉 MISSION ACCOMPLIE ! 🎉</div>
            <div class="mission-name">${missionData.name || 'Mission Secrète'}</div>
        `;

        messageElement.style.cssText = `
            position: absolute;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 40px;
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            text-align: center;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 20px;
            z-index: 10000;
            animation: congratsBounce 3s ease-in-out;
        `;

        this.effectsContainer.appendChild(messageElement);

        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 3000);

        // Ajouter l'animation CSS
        if (!document.getElementById('congrats-animation')) {
            const style = document.createElement('style');
            style.id = 'congrats-animation';
            style.textContent = `
                @keyframes congratsBounce {
                    0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
                    20% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
                    40% { transform: translate(-50%, -50%) scale(0.9); opacity: 1; }
                    60% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
                    80% { transform: translate(-50%, -50%) scale(0.95); opacity: 1; }
                    100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    playSuccessSound() {
        // Créer un son de succès simple (si supporté)
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.1);
            oscillator.frequency.setValueAtTime(1200, audioContext.currentTime + 0.2);

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (e) {
            // Son non supporté, continuer sans
        }
    }
}

// Initialiser le système d'effets visuels
const visualEffects = new VisualEffects();

// Exposer les fonctions pour les autres scripts
window.VisualEffects = VisualEffects;
window.visualEffects = visualEffects;
