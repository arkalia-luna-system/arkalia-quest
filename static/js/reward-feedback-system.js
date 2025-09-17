/* ===== ARKALIA QUEST - REWARD FEEDBACK SYSTEM ===== */
/* Système de feedback visuel et sonore pour les récompenses */

class RewardFeedbackSystem {
    constructor() {
        this.audioContext = null;
        this.sounds = {};
        this.init();
    }

    init() {
        this.setupAudioContext();
        this.createRewardContainer();
        this.setupEventListeners();
        // console.log('🎉 Reward Feedback System initialisé');
    }

    setupAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            // console.log('Audio non supporté');
        }
    }

    createRewardContainer() {
        // Créer le conteneur pour les effets de récompense
        if (!document.getElementById('reward-feedback-container')) {
            const container = document.createElement('div');
            container.id = 'reward-feedback-container';
            container.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 9999;
                overflow: hidden;
            `;
            document.body.appendChild(container);
        }
    }

    setupEventListeners() {
        // Écouter les événements de récompense
        document.addEventListener('levelUp', (e) => this.showLevelUpReward(e.detail));
        document.addEventListener('badgeEarned', (e) => this.showBadgeReward(e.detail));
        document.addEventListener('missionComplete', (e) => this.showMissionReward(e.detail));
        document.addEventListener('xpGained', (e) => this.showXPReward(e.detail));
        document.addEventListener('coinEarned', (e) => this.showCoinReward(e.detail));
    }

    showLevelUpReward(data) {
        this.playSound('levelUp');
        this.showConfetti();
        this.showRewardMessage('🎉 NIVEAU SUPÉRIEUR !', `Niveau ${data.level} atteint !`, 'level-up');
    }

    showBadgeReward(data) {
        this.playSound('badge');
        this.showConfetti();
        this.showRewardMessage('🏆 BADGE DÉBLOQUÉ !', data.name, 'badge');
    }

    showMissionReward(data) {
        this.playSound('mission');
        this.showRewardMessage('✅ MISSION TERMINÉE !', data.name, 'mission');
    }

    showXPReward(data) {
        this.showFloatingText(`+${data.amount} XP`, 'xp');
    }

    showCoinReward(data) {
        this.showFloatingText(`+${data.amount} Coins`, 'coin');
    }

    showConfetti() {
        const container = document.getElementById('reward-feedback-container');
        const confetti = document.createElement('div');
        confetti.className = 'confetti-container';
        confetti.innerHTML = this.generateConfettiHTML();

        container.appendChild(confetti);

        // Supprimer après animation
        setTimeout(() => {
            confetti.remove();
        }, 3000);
    }

    generateConfettiHTML() {
        let html = '';
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'];

        for (let i = 0; i < 50; i++) {
            const color = colors[Math.floor(Math.random() * colors.length)];
            const left = Math.random() * 100;
            const delay = Math.random() * 2;
            const duration = 2 + Math.random() * 2;

            html += `
                <div class="confetti-piece" style="
                    left: ${left}%;
                    background-color: ${color};
                    animation-delay: ${delay}s;
                    animation-duration: ${duration}s;
                "></div>
            `;
        }

        return html;
    }

    showRewardMessage(title, subtitle, type) {
        const container = document.getElementById('reward-feedback-container');
        const message = document.createElement('div');
        message.className = `reward-message ${type}`;

        message.innerHTML = `
            <div class="reward-content">
                <div class="reward-title">${title}</div>
                <div class="reward-subtitle">${subtitle}</div>
            </div>
        `;

        container.appendChild(message);

        // Animation d'apparition
        setTimeout(() => {
            message.classList.add('show');
        }, 100);

        // Supprimer après 3 secondes
        setTimeout(() => {
            message.classList.remove('show');
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 3000);
    }

    showFloatingText(text, type) {
        const container = document.getElementById('reward-feedback-container');
        const floatingText = document.createElement('div');
        floatingText.className = `floating-text ${type}`;
        floatingText.textContent = text;

        // Position aléatoire
        const left = 20 + Math.random() * 60;
        const top = 20 + Math.random() * 60;

        floatingText.style.cssText = `
            position: absolute;
            left: ${left}%;
            top: ${top}%;
            color: ${this.getColorForType(type)};
            font-size: 1.5em;
            font-weight: bold;
            text-shadow: 0 0 10px currentColor;
            pointer-events: none;
            z-index: 10000;
        `;

        container.appendChild(floatingText);

        // Animation
        setTimeout(() => {
            floatingText.style.transform = 'translateY(-50px)';
            floatingText.style.opacity = '0';
        }, 100);

        // Supprimer après animation
        setTimeout(() => {
            floatingText.remove();
        }, 2000);
    }

    getColorForType(type) {
        const colors = {
            xp: '#4ecdc4',
            coin: '#feca57',
            badge: '#ff6b6b',
            mission: '#96ceb4',
            level: '#ff9ff3'
        };
        return colors[type] || '#ffffff';
    }

    playSound(type) {
        if (!this.audioContext) return;

        const frequencies = {
            levelUp: [523, 659, 784, 1047],
            badge: [440, 554, 659],
            mission: [392, 494, 587],
            xp: [330, 415],
            coin: [262, 330, 392]
        };

        const freq = frequencies[type] || [440];

        freq.forEach((frequency, index) => {
            setTimeout(() => {
                this.playTone(frequency, 0.1);
            }, index * 100);
        });
    }

    playTone(frequency, duration) {
        if (!this.audioContext) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.value = frequency;
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
}

// CSS pour les animations
const rewardStyles = `
<style>
.confetti-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.confetti-piece {
    position: absolute;
    width: 10px;
    height: 10px;
    animation: confettiFall linear forwards;
}

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

.reward-message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(30, 30, 40, 0.9) 100%);
    border: 2px solid #4ecdc4;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease;
}

.reward-message.show {
    transform: translate(-50%, -50%) scale(1);
}

.reward-title {
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 10px;
    text-shadow: 0 0 20px currentColor;
}

.reward-subtitle {
    font-size: 1.2em;
    opacity: 0.9;
}

.floating-text {
    transition: all 2s ease-out;
    opacity: 1;
}
</style>
`;

// Ajouter les styles au document
document.head.insertAdjacentHTML('beforeend', rewardStyles);

// Initialiser le système
document.addEventListener('DOMContentLoaded', () => {
    window.rewardFeedbackSystem = new RewardFeedbackSystem();
});

// Exporter pour utilisation globale
window.RewardFeedbackSystem = RewardFeedbackSystem;
