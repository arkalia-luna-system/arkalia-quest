/**
 * Système d'animations de récompenses
 * Ajoute des effets visuels spectaculaires pour les badges, XP, et progression
 */

class RewardAnimations {
    constructor() {
        this.activeAnimations = new Set();
        this.rewardQueue = [];
        this.isAnimating = false;

        this.initializeSystem();
    }

    initializeSystem() {
        console.log('🎉 Système d\'animations de récompenses initialisé');
        this.createRewardStyles();
        this.setupRewardListeners();
        this.setupProgressTracking();
    }

    createRewardStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .reward-animation {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10000;
                pointer-events: none;
                font-family: 'Courier New', monospace;
            }
            
            .reward-popup {
                background: linear-gradient(45deg, #00ff00, #00cc00);
                color: #000;
                padding: 20px 30px;
                border-radius: 15px;
                font-weight: bold;
                font-size: 18px;
                text-align: center;
                box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
                animation: reward-popup-appear 0.5s ease-out;
            }
            
            .reward-icon {
                font-size: 48px;
                margin-bottom: 10px;
                animation: reward-icon-bounce 1s ease-in-out infinite;
            }
            
            .reward-text {
                margin: 10px 0;
                animation: reward-text-glow 2s ease-in-out infinite;
            }
            
            .reward-value {
                font-size: 24px;
                font-weight: bold;
                color: #000;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .reward-badge {
                display: inline-block;
                background: linear-gradient(45deg, #ffd700, #ffed4e);
                color: #000;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                margin: 5px;
                animation: reward-badge-spin 2s ease-in-out infinite;
            }
            
            .reward-confetti {
                position: absolute;
                width: 8px;
                height: 8px;
                background: #00ff00;
                animation: reward-confetti-fall 3s ease-out forwards;
            }
            
            .reward-particles {
                position: absolute;
                width: 6px;
                height: 6px;
                background: #00ff00;
                border-radius: 50%;
                animation: reward-particles-burst 2s ease-out forwards;
            }
            
            .reward-stars {
                position: absolute;
                font-size: 24px;
                color: #00ff00;
                animation: reward-stars-burst 2s ease-out forwards;
            }
            
            .xp-gain-animation {
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(45deg, #00ff00, #00cc00);
                color: #000;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: bold;
                font-size: 16px;
                z-index: 10000;
                animation: xp-gain-slide 3s ease-out forwards;
            }
            
            .badge-unlock-animation {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(45deg, #ffd700, #ffed4e);
                color: #000;
                padding: 20px 30px;
                border-radius: 15px;
                font-weight: bold;
                font-size: 20px;
                text-align: center;
                z-index: 10000;
                animation: badge-unlock-pop 1s ease-out;
                box-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
            }
            
            .level-up-animation {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, rgba(0, 255, 0, 0.1), rgba(0, 204, 0, 0.1));
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
                animation: level-up-flash 2s ease-out;
            }
            
            .level-up-text {
                font-size: 48px;
                font-weight: bold;
                color: #00ff00;
                text-align: center;
                animation: level-up-text-grow 2s ease-out;
                text-shadow: 0 0 20px #00ff00;
            }
            
            .progress-bar-animated {
                position: relative;
                width: 100%;
                height: 20px;
                background: rgba(0, 255, 0, 0.2);
                border-radius: 10px;
                overflow: hidden;
                margin: 10px 0;
            }
            
            .progress-fill-animated {
                height: 100%;
                background: linear-gradient(90deg, #00ff00, #00cc00);
                border-radius: 10px;
                transition: width 1s ease-out;
                position: relative;
                overflow: hidden;
            }
            
            .progress-fill-animated::after {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
                animation: progress-shine 2s ease-in-out infinite;
            }
            
            @keyframes reward-popup-appear {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
                50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            }
            
            @keyframes reward-icon-bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            @keyframes reward-text-glow {
                0%, 100% { text-shadow: 0 0 10px #00ff00; }
                50% { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; }
            }
            
            @keyframes reward-badge-spin {
                0% { transform: rotate(0deg) scale(1); }
                50% { transform: rotate(180deg) scale(1.1); }
                100% { transform: rotate(360deg) scale(1); }
            }
            
            @keyframes reward-confetti-fall {
                0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
                100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
            }
            
            @keyframes reward-particles-burst {
                0% { transform: scale(0) rotate(0deg); opacity: 1; }
                50% { transform: scale(1.2) rotate(180deg); opacity: 1; }
                100% { transform: scale(0) rotate(360deg); opacity: 0; }
            }
            
            @keyframes reward-stars-burst {
                0% { transform: scale(0) rotate(0deg); opacity: 1; }
                50% { transform: scale(1.5) rotate(180deg); opacity: 1; }
                100% { transform: scale(0) rotate(360deg); opacity: 0; }
            }
            
            @keyframes xp-gain-slide {
                0% { transform: translateX(100%); opacity: 1; }
                50% { transform: translateX(0); opacity: 1; }
                100% { transform: translateX(0); opacity: 0; }
            }
            
            @keyframes badge-unlock-pop {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
                50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            }
            
            @keyframes level-up-flash {
                0% { background: transparent; }
                50% { background: linear-gradient(45deg, rgba(0, 255, 0, 0.3), rgba(0, 204, 0, 0.3)); }
                100% { background: transparent; }
            }
            
            @keyframes level-up-text-grow {
                0% { transform: scale(0); opacity: 0; }
                50% { transform: scale(1.2); opacity: 1; }
                100% { transform: scale(1); opacity: 1; }
            }
            
            @keyframes progress-shine {
                0% { left: -100%; }
                100% { left: 100%; }
            }
        `;
        document.head.appendChild(style);
    }

    setupRewardListeners() {
        // Écouter les événements de récompense
        document.addEventListener('arkalia_xp_gained', (e) => {
            this.animateXPGain(e.detail.amount, e.detail.source);
        });

        document.addEventListener('arkalia_badge_earned', (e) => {
            this.animateBadgeUnlock(e.detail.badge, e.detail.description);
        });

        document.addEventListener('arkalia_level_up', (e) => {
            this.animateLevelUp(e.detail.newLevel, e.detail.rewards);
        });

        document.addEventListener('arkalia_mission_completed', (e) => {
            this.animateMissionCompletion(e.detail.mission, e.detail.rewards);
        });

        document.addEventListener('arkalia_challenge_completed', (e) => {
            this.animateChallengeCompletion(e.detail.challenge, e.detail.rewards);
        });
    }

    setupProgressTracking() {
        // Observer les changements de progression
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-progress') {
                    this.animateProgressUpdate(mutation.target);
                }
            });
        });

        // Observer les éléments de progression
        document.addEventListener('DOMContentLoaded', () => {
            const progressElements = document.querySelectorAll('[data-progress]');
            progressElements.forEach(element => {
                observer.observe(element, { attributes: true });
            });
        });
    }

    animateXPGain(amount, source = '') {
        if (this.isAnimating) {
            this.rewardQueue.push(() => this.animateXPGain(amount, source));
            return;
        }

        this.isAnimating = true;
        console.log(`🎉 Animation XP: +${amount} (${source})`);

        // Créer l'animation XP
        const xpElement = document.createElement('div');
        xpElement.className = 'xp-gain-animation';
        xpElement.innerHTML = `
            <div>+${amount} XP</div>
            ${source ? `<div style="font-size: 12px;">${source}</div>` : ''}
        `;

        document.body.appendChild(xpElement);

        // Supprimer après l'animation
        setTimeout(() => {
            xpElement.remove();
            this.isAnimating = false;
            this.processRewardQueue();
        }, 3000);
    }

    animateBadgeUnlock(badge, description = '') {
        if (this.isAnimating) {
            this.rewardQueue.push(() => this.animateBadgeUnlock(badge, description));
            return;
        }

        this.isAnimating = true;
        console.log(`🏆 Animation Badge: ${badge}`);

        // Créer l'animation de badge
        const badgeElement = document.createElement('div');
        badgeElement.className = 'badge-unlock-animation';
        badgeElement.innerHTML = `
            <div class="reward-icon">🏆</div>
            <div class="reward-text">Badge débloqué !</div>
            <div class="reward-badge">${badge}</div>
            ${description ? `<div style="font-size: 14px; margin-top: 10px;">${description}</div>` : ''}
        `;

        document.body.appendChild(badgeElement);

        // Ajouter des effets
        this.addConfettiEffect(badgeElement);
        this.addParticleEffect(badgeElement);

        // Supprimer après l'animation
        setTimeout(() => {
            badgeElement.remove();
            this.isAnimating = false;
            this.processRewardQueue();
        }, 3000);
    }

    animateLevelUp(newLevel, rewards = {}) {
        if (this.isAnimating) {
            this.rewardQueue.push(() => this.animateLevelUp(newLevel, rewards));
            return;
        }

        this.isAnimating = true;
        console.log(`🚀 Animation Level Up: ${newLevel}`);

        // Créer l'animation de level up
        const levelUpElement = document.createElement('div');
        levelUpElement.className = 'level-up-animation';
        levelUpElement.innerHTML = `
            <div class="level-up-text">
                <div>🚀 NIVEAU ${newLevel} ! 🚀</div>
                <div style="font-size: 24px; margin-top: 20px;">
                    ${rewards.xp ? `+${rewards.xp} XP` : ''}
                    ${rewards.coins ? ` • +${rewards.coins} Coins` : ''}
                </div>
            </div>
        `;

        document.body.appendChild(levelUpElement);

        // Ajouter des effets
        this.addConfettiEffect(levelUpElement);
        this.addStarEffect(levelUpElement);

        // Supprimer après l'animation
        setTimeout(() => {
            levelUpElement.remove();
            this.isAnimating = false;
            this.processRewardQueue();
        }, 2000);
    }

    animateMissionCompletion(mission, rewards = {}) {
        if (this.isAnimating) {
            this.rewardQueue.push(() => this.animateMissionCompletion(mission, rewards));
            return;
        }

        this.isAnimating = true;
        console.log(`🎯 Animation Mission: ${mission}`);

        // Créer l'animation de mission
        const missionElement = document.createElement('div');
        missionElement.className = 'reward-animation';
        missionElement.innerHTML = `
            <div class="reward-popup">
                <div class="reward-icon">🎯</div>
                <div class="reward-text">Mission accomplie !</div>
                <div class="reward-value">${mission}</div>
                ${rewards.xp ? `<div>+${rewards.xp} XP</div>` : ''}
                ${rewards.coins ? `<div>+${rewards.coins} Coins</div>` : ''}
            </div>
        `;

        document.body.appendChild(missionElement);

        // Ajouter des effets
        this.addConfettiEffect(missionElement);

        // Supprimer après l'animation
        setTimeout(() => {
            missionElement.remove();
            this.isAnimating = false;
            this.processRewardQueue();
        }, 3000);
    }

    animateChallengeCompletion(challenge, rewards = {}) {
        if (this.isAnimating) {
            this.rewardQueue.push(() => this.animateChallengeCompletion(challenge, rewards));
            return;
        }

        this.isAnimating = true;
        console.log(`🎮 Animation Challenge: ${challenge}`);

        // Créer l'animation de défi
        const challengeElement = document.createElement('div');
        challengeElement.className = 'reward-animation';
        challengeElement.innerHTML = `
            <div class="reward-popup">
                <div class="reward-icon">🎮</div>
                <div class="reward-text">Défi relevé !</div>
                <div class="reward-value">${challenge}</div>
                ${rewards.xp ? `<div>+${rewards.xp} XP</div>` : ''}
                ${rewards.badge ? `<div class="reward-badge">${rewards.badge}</div>` : ''}
            </div>
        `;

        document.body.appendChild(challengeElement);

        // Ajouter des effets
        this.addParticleEffect(challengeElement);

        // Supprimer après l'animation
        setTimeout(() => {
            challengeElement.remove();
            this.isAnimating = false;
            this.processRewardQueue();
        }, 3000);
    }

    animateProgressUpdate(element) {
        const progress = element.getAttribute('data-progress');
        const progressFill = element.querySelector('.progress-fill-animated');

        if (progressFill) {
            progressFill.style.width = progress + '%';
        }
    }

    addConfettiEffect(container) {
        const rect = container.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < 20; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'reward-confetti';
            confetti.style.left = centerX + (Math.random() - 0.5) * 200 + 'px';
            confetti.style.top = centerY + 'px';
            confetti.style.background = this.getRandomColor();
            confetti.style.animationDelay = Math.random() * 0.5 + 's';

            document.body.appendChild(confetti);

            setTimeout(() => confetti.remove(), 3000);
        }
    }

    addParticleEffect(container) {
        const rect = container.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < 15; i++) {
            const particle = document.createElement('div');
            particle.className = 'reward-particles';
            particle.style.left = centerX + (Math.random() - 0.5) * 150 + 'px';
            particle.style.top = centerY + (Math.random() - 0.5) * 150 + 'px';
            particle.style.background = this.getRandomColor();
            particle.style.animationDelay = Math.random() * 0.3 + 's';

            document.body.appendChild(particle);

            setTimeout(() => particle.remove(), 2000);
        }
    }

    addStarEffect(container) {
        const rect = container.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < 10; i++) {
            const star = document.createElement('div');
            star.className = 'reward-stars';
            star.textContent = '⭐';
            star.style.left = centerX + (Math.random() - 0.5) * 300 + 'px';
            star.style.top = centerY + (Math.random() - 0.5) * 300 + 'px';
            star.style.animationDelay = Math.random() * 0.4 + 's';

            document.body.appendChild(star);

            setTimeout(() => star.remove(), 2000);
        }
    }

    getRandomColor() {
        const colors = ['#00ff00', '#00cc00', '#ffff00', '#ff6600', '#ff0066', '#6600ff'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    processRewardQueue() {
        if (this.rewardQueue.length > 0) {
            const nextReward = this.rewardQueue.shift();
            nextReward();
        }
    }

    // Méthodes publiques
    triggerReward(type, data) {
        switch (type) {
            case 'xp':
                this.animateXPGain(data.amount, data.source);
                break;
            case 'badge':
                this.animateBadgeUnlock(data.badge, data.description);
                break;
            case 'level':
                this.animateLevelUp(data.level, data.rewards);
                break;
            case 'mission':
                this.animateMissionCompletion(data.mission, data.rewards);
                break;
            case 'challenge':
                this.animateChallengeCompletion(data.challenge, data.rewards);
                break;
        }
    }

    getAnimationStats() {
        return {
            activeAnimations: this.activeAnimations.size,
            queuedRewards: this.rewardQueue.length,
            isAnimating: this.isAnimating
        };
    }
}

// Initialiser le système d'animations de récompenses
window.rewardAnimations = new RewardAnimations();
