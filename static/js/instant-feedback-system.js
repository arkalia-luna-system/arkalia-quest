/**
 * Système de Feedback Instantané et Gratifiant
 * Répond aux besoins de chaque profil utilisateur
 */

class InstantFeedbackSystem {
    constructor() {
        this.feedbackQueue = [];
        this.isProcessing = false;
        this.soundEnabled = true;
        this.vibrationEnabled = true;
        this.init();
    }

    init() {
        console.log('🎉 Système de feedback instantané initialisé');
        this.setupEventListeners();
        this.createFeedbackContainer();
        this.setupSoundSystem();
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('levelUp', (event) => {
            this.showLevelUpFeedback(event.detail);
        });

        document.addEventListener('badgeEarned', (event) => {
            this.showBadgeFeedback(event.detail);
        });

        document.addEventListener('missionComplete', (event) => {
            this.showMissionCompleteFeedback(event.detail);
        });

        document.addEventListener('scoreGained', (event) => {
            this.showScoreFeedback(event.detail);
        });

        document.addEventListener('achievementUnlocked', (event) => {
            this.showAchievementFeedback(event.detail);
        });
    }

    createFeedbackContainer() {
        const container = document.createElement('div');
        container.id = 'instant-feedback-container';
        container.className = 'instant-feedback-container';
        container.innerHTML = `
            <div class="feedback-overlay"></div>
            <div class="feedback-messages"></div>
            <div class="feedback-particles"></div>
        `;
        document.body.appendChild(container);
    }

    setupSoundSystem() {
        // Créer le contexte audio
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('⚠️ AudioContext non supporté');
            this.soundEnabled = false;
        }
    }

    // Feedback de montée de niveau
    showLevelUpFeedback(data) {
        const feedback = {
            type: 'levelUp',
            title: `🎉 NIVEAU ${data.level} !`,
            message: `Félicitations ! Tu as atteint le niveau ${data.level} !`,
            duration: 4000,
            sound: 'levelUp',
            vibration: [200, 100, 200],
            animation: 'levelUpBurst'
        };

        this.queueFeedback(feedback);
    }

    // Feedback de badge obtenu
    showBadgeFeedback(data) {
        const feedback = {
            type: 'badgeEarned',
            title: `🏆 BADGE OBTENU !`,
            message: `${data.badgeName}`,
            description: data.description || 'Nouveau badge débloqué !',
            duration: 3000,
            sound: 'badgeEarned',
            vibration: [300, 100, 300],
            animation: 'badgeUnlock'
        };

        this.queueFeedback(feedback);
    }

    // Feedback de mission complétée
    showMissionCompleteFeedback(data) {
        const feedback = {
            type: 'missionComplete',
            title: `✅ MISSION TERMINÉE !`,
            message: `${data.missionName}`,
            description: `+${data.xp} XP • +${data.coins} pièces`,
            duration: 3000,
            sound: 'missionComplete',
            vibration: [150, 100, 150],
            animation: 'missionComplete'
        };

        this.queueFeedback(feedback);
    }

    // Feedback de score gagné
    showScoreFeedback(data) {
        const feedback = {
            type: 'scoreGained',
            title: `+${data.score} POINTS !`,
            message: data.message || 'Score gagné !',
            duration: 2000,
            sound: 'scoreGained',
            vibration: [100],
            animation: 'scoreGained'
        };

        this.queueFeedback(feedback);
    }

    // Feedback d'achievement débloqué
    showAchievementFeedback(data) {
        const feedback = {
            type: 'achievementUnlocked',
            title: `🎯 ACHIEVEMENT !`,
            message: data.achievementName,
            description: data.description || 'Nouvel achievement débloqué !',
            duration: 4000,
            sound: 'achievementUnlocked',
            vibration: [200, 100, 200, 100, 200],
            animation: 'achievementUnlock'
        };

        this.queueFeedback(feedback);
    }

    queueFeedback(feedback) {
        this.feedbackQueue.push(feedback);
        this.processQueue();
    }

    async processQueue() {
        if (this.isProcessing || this.feedbackQueue.length === 0) return;

        this.isProcessing = true;
        const feedback = this.feedbackQueue.shift();

        try {
            await this.displayFeedback(feedback);
            await this.playFeedbackSound(feedback.sound);
            await this.playFeedbackVibration(feedback.vibration);
            await this.createParticleEffect(feedback.animation);
        } catch (error) {
            console.error('Erreur feedback:', error);
        }

        this.isProcessing = false;
        this.processQueue();
    }

    async displayFeedback(feedback) {
        const container = document.getElementById('instant-feedback-container');
        const messagesContainer = container.querySelector('.feedback-messages');

        const feedbackElement = document.createElement('div');
        feedbackElement.className = `feedback-message feedback-${feedback.type}`;
        feedbackElement.innerHTML = `
            <div class="feedback-content">
                <div class="feedback-title">${feedback.title}</div>
                <div class="feedback-message-text">${feedback.message}</div>
                ${feedback.description ? `<div class="feedback-description">${feedback.description}</div>` : ''}
            </div>
            <div class="feedback-close" onclick="this.parentElement.remove()">×</div>
        `;

        messagesContainer.appendChild(feedbackElement);

        // Animation d'entrée
        setTimeout(() => {
            feedbackElement.classList.add('show');
        }, 100);

        // Auto-suppression
        setTimeout(() => {
            feedbackElement.classList.add('hide');
            setTimeout(() => {
                if (feedbackElement.parentNode) {
                    feedbackElement.remove();
                }
            }, 300);
        }, feedback.duration);
    }

    async playFeedbackSound(soundType) {
        if (!this.soundEnabled || !this.audioContext) return;

        const frequencies = {
            levelUp: [800, 1000, 1200],
            badgeEarned: [600, 800, 1000, 1200],
            missionComplete: [500, 700, 900],
            scoreGained: [1000],
            achievementUnlocked: [400, 600, 800, 1000, 1200]
        };

        const freq = frequencies[soundType] || [800];

        for (let i = 0; i < freq.length; i++) {
            setTimeout(() => {
                this.createSoundEffect(freq[i], 0.2);
            }, i * 100);
        }
    }

    createSoundEffect(frequency, duration) {
        if (!this.audioContext) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }

    async playFeedbackVibration(pattern) {
        if (!this.vibrationEnabled || !navigator.vibrate) return;

        try {
            navigator.vibrate(pattern);
        } catch (error) {
            console.warn('Vibration non supportée');
        }
    }

    async createParticleEffect(animationType) {
        const container = document.getElementById('instant-feedback-container');
        const particlesContainer = container.querySelector('.feedback-particles');

        const particleCount = 20;
        const colors = ['#00ff00', '#00ffff', '#ff00ff', '#ffff00', '#ff6600'];

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'feedback-particle';
            particle.style.cssText = `
                position: absolute;
                width: 6px;
                height: 6px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                border-radius: 50%;
                pointer-events: none;
                z-index: 10000;
                left: 50%;
                top: 50%;
                animation: ${animationType} 2s ease-out forwards;
            `;

            particlesContainer.appendChild(particle);

            // Supprimer la particule après l'animation
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, 2000);
        }
    }

    // Méthodes utilitaires
    enableSound() {
        this.soundEnabled = true;
    }

    disableSound() {
        this.soundEnabled = false;
    }

    enableVibration() {
        this.vibrationEnabled = true;
    }

    disableVibration() {
        this.vibrationEnabled = false;
    }

    clearAllFeedback() {
        const container = document.getElementById('instant-feedback-container');
        const messagesContainer = container.querySelector('.feedback-messages');
        messagesContainer.innerHTML = '';
        this.feedbackQueue = [];
    }
}

// Initialiser le système de feedback instantané
document.addEventListener('DOMContentLoaded', () => {
    window.instantFeedbackSystem = new InstantFeedbackSystem();
    console.log('🎉 Feedback instantané activé');
});

// Export pour utilisation externe
window.InstantFeedbackSystem = InstantFeedbackSystem;
