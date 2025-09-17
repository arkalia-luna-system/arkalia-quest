/* ===== ARKALIA QUEST - GAMIFICATION FEEDBACK SYSTEM ===== */
/* Système de feedbacks gamifiés pour enrichir l'expérience joueur */

class GamificationFeedback {
    constructor() {
        this.notifications = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createNotificationContainer();
        console.log('🎮 Gamification Feedback System initialisé');
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('arkalia:skill:upgraded', (e) => {
            this.showSkillUpgradeFeedback(e.detail);
        });

        document.addEventListener('arkalia:progression:synced', (e) => {
            this.updateProgressionDisplay(e.detail);
        });

        // Écouter les événements de mission
        document.addEventListener('arkalia:mission:completed', (e) => {
            this.showMissionCompleteFeedback(e.detail);
        });

        // Écouter les événements de badge
        document.addEventListener('arkalia:badge:earned', (e) => {
            this.showBadgeEarnedFeedback(e.detail);
        });
    }

    createNotificationContainer() {
        // Créer le conteneur de notifications
        if (!document.getElementById('gamification-notifications')) {
            const container = document.createElement('div');
            container.id = 'gamification-notifications';
            container.style.position = 'fixed';
            container.style.top = '20px';
            container.style.right = '20px';
            container.style.zIndex = '10000';
            container.style.pointerEvents = 'none';
            document.body.appendChild(container);
        }
    }

    showSkillUpgradeFeedback(detail) {
        const { category, skill, level } = detail;

        // Animation de particules
        this.createParticleEffect('skill-upgrade');

        // Notification
        this.showNotification(
            `🎯 ${skill} amélioré au niveau ${level} !`,
            'success',
            3000
        );

        // Son de succès
        this.playSuccessSound();
    }

    showMissionCompleteFeedback(detail) {
        const { mission, xp, coins } = detail;

        // Confettis
        this.createConfettiEffect();

        // Notification avec récompenses
        this.showNotification(
            `🎉 Mission "${mission}" terminée !\n+${xp} XP • +${coins} 🪙`,
            'success',
            4000
        );

        // Son de victoire
        this.playVictorySound();
    }

    showBadgeEarnedFeedback(detail) {
        const { badge, description } = detail;

        // Animation spéciale pour les badges
        this.createBadgeAnimation(badge);

        // Notification avec style spécial
        this.showNotification(
            `🏆 NOUVEAU BADGE !\n${badge}\n${description}`,
            'badge',
            5000
        );

        // Son de badge
        this.playBadgeSound();
    }

    createParticleEffect(type) {
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.top = '50%';
        container.style.left = '50%';
        container.style.transform = 'translate(-50%, -50%)';
        container.style.pointerEvents = 'none';
        container.style.zIndex = '9999';

        const colors = type === 'skill-upgrade'
            ? ['#00ff00', '#22c55e', '#16a34a']
            : ['#ff00ff', '#a855f7', '#7c3aed'];

        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = '6px';
            particle.style.height = '6px';
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.borderRadius = '50%';
            particle.style.left = '0';
            particle.style.top = '0';

            const angle = (Math.PI * 2 * i) / 20;
            const distance = 50 + Math.random() * 30;
            const x = Math.cos(angle) * distance;
            const y = Math.sin(angle) * distance;

            particle.style.animation = `particleExplode 1s ease-out forwards`;
            particle.style.setProperty('--x', x + 'px');
            particle.style.setProperty('--y', y + 'px');

            container.appendChild(particle);
        }

        document.body.appendChild(container);

        // Ajouter l'animation CSS
        this.addParticleAnimation();

        setTimeout(() => {
            if (container.parentNode) {
                container.parentNode.removeChild(container);
            }
        }, 1000);
    }

    createConfettiEffect() {
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100%';
        container.style.height = '100%';
        container.style.pointerEvents = 'none';
        container.style.zIndex = '9999';

        const colors = ['#00ff00', '#ff00ff', '#ffff00', '#00ffff', '#ff8000'];

        for (let i = 0; i < 100; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'absolute';
            confetti.style.width = '8px';
            confetti.style.height = '8px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.top = '-10px';
            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
            confetti.style.animation = `confettiFall ${2 + Math.random() * 3}s linear forwards`;

            container.appendChild(confetti);
        }

        document.body.appendChild(container);

        // Ajouter l'animation CSS
        this.addConfettiAnimation();

        setTimeout(() => {
            if (container.parentNode) {
                container.parentNode.removeChild(container);
            }
        }, 5000);
    }

    createBadgeAnimation(badgeName) {
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.top = '50%';
        container.style.left = '50%';
        container.style.transform = 'translate(-50%, -50%)';
        container.style.pointerEvents = 'none';
        container.style.zIndex = '9999';

        const badge = document.createElement('div');
        badge.style.fontSize = '4em';
        badge.style.color = '#ffd700';
        badge.style.textShadow = '0 0 20px #ffd700';
        badge.style.animation = 'badgeEarned 2s ease-out forwards';
        badge.textContent = '🏆';

        container.appendChild(badge);
        document.body.appendChild(container);

        // Ajouter l'animation CSS
        this.addBadgeAnimation();

        setTimeout(() => {
            if (container.parentNode) {
                container.parentNode.removeChild(container);
            }
        }, 2000);
    }

    showNotification(message, type = 'info', duration = 3000) {
        const container = document.getElementById('gamification-notifications');
        if (!container) return;

        const notification = document.createElement('div');
        notification.className = `gamification-notification ${type}`;
        notification.style.cssText = `
            background: ${this.getNotificationColor(type)};
            color: white;
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            border: 2px solid ${this.getNotificationBorderColor(type)};
            font-family: 'IBM Plex Mono', monospace;
            font-size: 14px;
            line-height: 1.4;
            white-space: pre-line;
            text-align: center;
            max-width: 300px;
            animation: slideInRight 0.5s ease-out, fadeOut 0.5s ease-in ${duration - 500}ms ${duration - 500}ms;
            animation-fill-mode: both;
        `;

        notification.textContent = message;
        container.appendChild(notification);

        // Supprimer après la durée spécifiée
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, duration);
    }

    getNotificationColor(type) {
        const colors = {
            'success': 'linear-gradient(135deg, #22c55e, #16a34a)',
            'error': 'linear-gradient(135deg, #ef4444, #dc2626)',
            'warning': 'linear-gradient(135deg, #f59e0b, #d97706)',
            'info': 'linear-gradient(135deg, #3b82f6, #2563eb)',
            'badge': 'linear-gradient(135deg, #ffd700, #ffb700)'
        };
        return colors[type] || colors['info'];
    }

    getNotificationBorderColor(type) {
        const colors = {
            'success': '#00ff00',
            'error': '#ff0000',
            'warning': '#ffaa00',
            'info': '#00aaff',
            'badge': '#ffd700'
        };
        return colors[type] || colors['info'];
    }

    playSuccessSound() {
        this.playTone([800, 1000, 1200], 0.3);
    }

    playVictorySound() {
        this.playTone([600, 800, 1000, 1200, 1400], 0.5);
    }

    playBadgeSound() {
        this.playTone([1000, 1200, 1400, 1600], 0.4);
    }

    playTone(frequencies, duration) {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            let currentTime = audioContext.currentTime;
            frequencies.forEach((freq, index) => {
                oscillator.frequency.setValueAtTime(freq, currentTime + index * 0.1);
            });

            gainNode.gain.setValueAtTime(0.2, currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, currentTime + duration);

            oscillator.start(currentTime);
            oscillator.stop(currentTime + duration);
        } catch (error) {
            console.log('Impossible de jouer le son:', error);
        }
    }

    addParticleAnimation() {
        if (document.getElementById('particle-animation-style')) return;

        const style = document.createElement('style');
        style.id = 'particle-animation-style';
        style.textContent = `
            @keyframes particleExplode {
                to {
                    transform: translate(var(--x), var(--y));
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    addConfettiAnimation() {
        if (document.getElementById('confetti-animation-style')) return;

        const style = document.createElement('style');
        style.id = 'confetti-animation-style';
        style.textContent = `
            @keyframes confettiFall {
                to {
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    addBadgeAnimation() {
        if (document.getElementById('badge-animation-style')) return;

        const style = document.createElement('style');
        style.id = 'badge-animation-style';
        style.textContent = `
            @keyframes badgeEarned {
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
                    opacity: 0;
                }
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes fadeOut {
                from {
                    opacity: 1;
                }
                to {
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    updateProgressionDisplay(playerData) {
        // Mettre à jour l'affichage de progression dans tous les modules
        const event = new CustomEvent('arkalia:ui:update-progression', {
            detail: playerData
        });
        document.dispatchEvent(event);
    }
}

// Initialiser le système de feedback gamifié
const gamificationFeedback = new GamificationFeedback();
