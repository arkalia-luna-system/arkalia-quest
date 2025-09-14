/* ===== ARKALIA QUEST - VISUAL FEEDBACK SYSTEM ===== */

class VisualFeedbackSystem {
    constructor() {
        this.notifications = [];
        this.animations = new Map();
        this.soundEnabled = true;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createNotificationContainer();
        this.loadSettings();
    }

    setupEventListeners() {
        // Écouter les événements de jeu
        document.addEventListener('gameEvent', (e) => {
            this.handleGameEvent(e.detail.event, e.detail.data);
        });

        // Écouter les événements de progression
        document.addEventListener('progressionEvent', (e) => {
            this.handleProgressionEvent(e.detail.type, e.detail.data);
        });

        // Écouter les événements de mission
        document.addEventListener('missionEvent', (e) => {
            this.handleMissionEvent(e.detail.type, e.detail.data);
        });
    }

    createNotificationContainer() {
        // Créer le conteneur de notifications
        const container = document.createElement('div');
        container.id = 'visual-feedback-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }

    // GESTION DES ÉVÉNEMENTS DE JEU
    handleGameEvent(event, data) {
        switch (event) {
            case 'game_start':
                this.showGameStartFeedback(data);
                break;
            case 'game_end':
                this.showGameEndFeedback(data);
                break;
            case 'score_update':
                this.showScoreUpdateFeedback(data);
                break;
            case 'level_complete':
                this.showLevelCompleteFeedback(data);
                break;
        }
    }

    handleProgressionEvent(type, data) {
        switch (type) {
            case 'level_up':
                this.showLevelUpAnimation(data);
                break;
            case 'xp_gain':
                this.showXPGainAnimation(data);
                break;
            case 'badge_earned':
                this.showBadgeEarnedAnimation(data);
                break;
            case 'achievement_unlocked':
                this.showAchievementAnimation(data);
                break;
        }
    }

    handleMissionEvent(type, data) {
        switch (type) {
            case 'mission_start':
                this.showMissionStartFeedback(data);
                break;
            case 'mission_complete':
                this.showMissionCompleteAnimation(data);
                break;
            case 'choice_made':
                this.showChoiceFeedback(data);
                break;
        }
    }

    // FEEDBACKS DE JEU
    showGameStartFeedback(data) {
        const notification = this.createNotification({
            type: 'game_start',
            title: '🎮 Jeu Lancé !',
            message: `Prêt pour ${data.gameName || 'ce défi'} ?`,
            duration: 3000,
            animation: 'slideInRight'
        });
        this.showNotification(notification);
    }

    showGameEndFeedback(data) {
        const isWin = data.won || data.score > 0;
        const notification = this.createNotification({
            type: isWin ? 'success' : 'info',
            title: isWin ? '🎉 Victoire !' : '💪 Continue !',
            message: isWin ?
                `Excellent ! Score: ${data.score || 0}` :
                'Pas grave ! Tu feras mieux la prochaine fois !',
            duration: 4000,
            animation: isWin ? 'bounceIn' : 'slideInRight'
        });
        this.showNotification(notification);

        if (isWin) {
            this.createConfettiEffect();
        }
    }

    showScoreUpdateFeedback(data) {
        const scoreElement = document.querySelector('.current-score, .score-value');
        if (scoreElement) {
            this.animateScoreUpdate(scoreElement, data.oldScore, data.newScore);
        }
    }

    showLevelCompleteFeedback(data) {
        const notification = this.createNotification({
            type: 'success',
            title: '🌟 Niveau Complété !',
            message: `Félicitations ! Tu as terminé le niveau ${data.level} !`,
            duration: 5000,
            animation: 'bounceIn'
        });
        this.showNotification(notification);
        this.createLevelCompleteEffect();
    }

    // ANIMATIONS DE PROGRESSION
    showLevelUpAnimation(data) {
        // Notification principale
        const notification = this.createNotification({
            type: 'level_up',
            title: '🚀 NIVEAU SUPÉRIEUR !',
            message: `Niveau ${data.level} atteint ! +${data.xpGained} XP`,
            duration: 6000,
            animation: 'levelUpBounce'
        });
        this.showNotification(notification);

        // Effet de particules
        this.createLevelUpParticles();

        // Animation de l'interface
        this.animateLevelUpInterface(data.level);
    }

    showXPGainAnimation(data) {
        // Animation flottante de XP
        this.createFloatingXP(data.amount, data.source);

        // Mise à jour de la barre de progression
        this.animateProgressBar(data.amount, data.total);
    }

    showBadgeEarnedAnimation(data) {
        const notification = this.createNotification({
            type: 'badge',
            title: '🏆 NOUVEAU BADGE !',
            message: `${data.badge.name} - ${data.badge.description}`,
            duration: 8000,
            animation: 'badgeEarned'
        });
        this.showNotification(notification);

        // Effet spécial de badge
        this.createBadgeEffect(data.badge);
    }

    showAchievementAnimation(data) {
        const notification = this.createNotification({
            type: 'achievement',
            title: '⭐ ACCOMPLISSEMENT !',
            message: `${data.achievement.name} débloqué !`,
            duration: 7000,
            animation: 'achievementUnlock'
        });
        this.showNotification(notification);
    }

    // FEEDBACKS DE MISSION
    showMissionStartFeedback(data) {
        const notification = this.createNotification({
            type: 'mission',
            title: '🎯 Mission Acceptée !',
            message: `${data.missionName} - Prêt à commencer ?`,
            duration: 4000,
            animation: 'slideInLeft'
        });
        this.showNotification(notification);
    }

    showMissionCompleteAnimation(data) {
        const notification = this.createNotification({
            type: 'success',
            title: '✅ Mission Complétée !',
            message: `${data.missionName} - +${data.xpReward} XP`,
            duration: 6000,
            animation: 'missionComplete'
        });
        this.showNotification(notification);

        // Effet de mission complétée
        this.createMissionCompleteEffect();
    }

    showChoiceFeedback(data) {
        const notification = this.createNotification({
            type: 'info',
            title: '🤔 Choix Fait !',
            message: `Tu as choisi: ${data.choiceText}`,
            duration: 3000,
            animation: 'fadeIn'
        });
        this.showNotification(notification);
    }

    // CRÉATION DE NOTIFICATIONS
    createNotification(config) {
        const notification = document.createElement('div');
        notification.className = `visual-notification ${config.type} ${config.animation}`;

        notification.innerHTML = `
            <div class="notification-icon">${this.getNotificationIcon(config.type)}</div>
            <div class="notification-content">
                <div class="notification-title">${config.title}</div>
                <div class="notification-message">${config.message}</div>
            </div>
            <div class="notification-progress"></div>
        `;

        // Styles dynamiques
        notification.style.cssText = `
            background: ${this.getNotificationBackground(config.type)};
            border: 2px solid ${this.getNotificationBorder(config.type)};
            color: ${this.getNotificationColor(config.type)};
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 12px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            max-width: 350px;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        `;

        return {
            element: notification,
            config: config
        };
    }

    showNotification(notification) {
        const container = document.getElementById('visual-feedback-container');
        container.appendChild(notification.element);

        // Animation d'entrée
        this.animateNotificationIn(notification.element, notification.config.animation);

        // Suppression automatique
        setTimeout(() => {
            this.animateNotificationOut(notification.element, () => {
                notification.element.remove();
            });
        }, notification.config.duration);
    }

    // ANIMATIONS
    animateNotificationIn(element, animation) {
        const animations = {
            'slideInRight': 'translateX(100%)',
            'slideInLeft': 'translateX(-100%)',
            'bounceIn': 'scale(0)',
            'fadeIn': 'opacity(0)',
            'levelUpBounce': 'translateY(100px) scale(0)',
            'badgeEarned': 'translateY(100px) rotate(180deg)',
            'achievementUnlock': 'scale(0) rotate(-180deg)',
            'missionComplete': 'translateY(50px) scale(0.8)'
        };

        const initialTransform = animations[animation] || 'translateX(100%)';
        element.style.transform = initialTransform;
        element.style.opacity = '0';

        requestAnimationFrame(() => {
            element.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            element.style.transform = 'translateX(0) scale(1) rotate(0deg)';
            element.style.opacity = '1';
        });
    }

    animateNotificationOut(element, callback) {
        element.style.transition = 'all 0.3s ease-in';
        element.style.transform = 'translateX(100%) scale(0.8)';
        element.style.opacity = '0';

        setTimeout(callback, 300);
    }

    // EFFETS SPÉCIAUX
    createConfettiEffect() {
        const colors = ['#00ff00', '#00ffff', '#ffff00', '#ff00ff'];
        const confettiCount = 50;

        for (let i = 0; i < confettiCount; i++) {
            setTimeout(() => {
                this.createConfettiPiece(colors[Math.floor(Math.random() * colors.length)]);
            }, i * 20);
        }
    }

    createConfettiPiece(color) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 10px;
            height: 10px;
            background: ${color};
            pointer-events: none;
            z-index: 10001;
            animation: confettiFall 3s ease-out forwards;
        `;

        document.body.appendChild(confetti);

        setTimeout(() => confetti.remove(), 3000);
    }

    createLevelUpParticles() {
        const particleCount = 20;
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                left: ${centerX}px;
                top: ${centerY}px;
                width: 6px;
                height: 6px;
                background: #00ff00;
                border-radius: 50%;
                pointer-events: none;
                z-index: 10001;
                animation: levelUpParticle 2s ease-out forwards;
            `;

            // Direction aléatoire
            const angle = (Math.PI * 2 * i) / particleCount;
            const distance = 100 + Math.random() * 100;
            const endX = centerX + Math.cos(angle) * distance;
            const endY = centerY + Math.sin(angle) * distance;

            particle.style.setProperty('--end-x', `${endX}px`);
            particle.style.setProperty('--end-y', `${endY}px`);

            document.body.appendChild(particle);

            setTimeout(() => particle.remove(), 2000);
        }
    }

    createBadgeEffect(badge) {
        const effect = document.createElement('div');
        effect.className = 'badge-effect';
        effect.innerHTML = `
            <div class="badge-icon">${badge.icon || '🏆'}</div>
            <div class="badge-name">${badge.name}</div>
        `;

        effect.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.9), rgba(255, 165, 0, 0.9));
            color: #000;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 1.5em;
            z-index: 10002;
            animation: badgeEffect 3s ease-out forwards;
            box-shadow: 0 0 50px rgba(255, 215, 0, 0.8);
        `;

        document.body.appendChild(effect);

        setTimeout(() => effect.remove(), 3000);
    }

    createFloatingXP(amount, source) {
        const xpElement = document.createElement('div');
        xpElement.textContent = `+${amount} XP`;
        xpElement.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            color: #00ff00;
            font-weight: bold;
            font-size: 1.2em;
            pointer-events: none;
            z-index: 10001;
            animation: floatingXP 2s ease-out forwards;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.8);
        `;

        document.body.appendChild(xpElement);

        setTimeout(() => xpElement.remove(), 2000);
    }

    // MÉTHODES UTILITAIRES
    getNotificationIcon(type) {
        const icons = {
            'game_start': '🎮',
            'success': '✅',
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'level_up': '🚀',
            'badge': '🏆',
            'achievement': '⭐',
            'mission': '🎯'
        };
        return icons[type] || 'ℹ️';
    }

    getNotificationBackground(type) {
        const backgrounds = {
            'game_start': 'linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 255, 255, 0.05))',
            'success': 'linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 255, 0, 0.05))',
            'info': 'linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 255, 255, 0.05))',
            'warning': 'linear-gradient(135deg, rgba(255, 255, 0, 0.1), rgba(255, 255, 0, 0.05))',
            'error': 'linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(255, 0, 0, 0.05))',
            'level_up': 'linear-gradient(135deg, rgba(167, 139, 250, 0.1), rgba(167, 139, 250, 0.05))',
            'badge': 'linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.05))',
            'achievement': 'linear-gradient(135deg, rgba(255, 165, 0, 0.1), rgba(255, 165, 0, 0.05))',
            'mission': 'linear-gradient(135deg, rgba(0, 255, 68, 0.1), rgba(0, 255, 68, 0.05))'
        };
        return backgrounds[type] || backgrounds['info'];
    }

    getNotificationBorder(type) {
        const borders = {
            'game_start': '#00ff00',
            'success': '#00ff00',
            'info': '#00ffff',
            'warning': '#ffff00',
            'error': '#ff0000',
            'level_up': '#a78bfa',
            'badge': '#ffd700',
            'achievement': '#ffa500',
            'mission': '#00ff44'
        };
        return borders[type] || '#00ffff';
    }

    getNotificationColor(type) {
        const colors = {
            'game_start': '#00ff00',
            'success': '#00ff00',
            'info': '#00ffff',
            'warning': '#ffff00',
            'error': '#ff6666',
            'level_up': '#a78bfa',
            'badge': '#ffd700',
            'achievement': '#ffa500',
            'mission': '#00ff44'
        };
        return colors[type] || '#00ffff';
    }

    loadSettings() {
        const settings = localStorage.getItem('arkaliaVisualSettings');
        if (settings) {
            const data = JSON.parse(settings);
            this.soundEnabled = data.soundEnabled !== false;
        }
    }

    saveSettings() {
        const settings = {
            soundEnabled: this.soundEnabled
        };
        localStorage.setItem('arkaliaVisualSettings', JSON.stringify(settings));
    }
}

// CSS pour les animations
const visualFeedbackStyles = document.createElement('style');
visualFeedbackStyles.textContent = `
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

    @keyframes levelUpParticle {
        0% {
            transform: translate(0, 0) scale(1);
            opacity: 1;
        }
        100% {
            transform: translate(var(--end-x), var(--end-y)) scale(0);
            opacity: 0;
        }
    }

    @keyframes badgeEffect {
        0% {
            transform: translate(-50%, -50%) scale(0) rotate(0deg);
            opacity: 0;
        }
        50% {
            transform: translate(-50%, -50%) scale(1.2) rotate(180deg);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -50%) scale(1) rotate(360deg);
            opacity: 0;
        }
    }

    @keyframes floatingXP {
        0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -150px) scale(1.5);
            opacity: 0;
        }
    }

    .notification-progress {
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
        background: currentColor;
        animation: progressBar linear forwards;
    }

    @keyframes progressBar {
        0% { width: 100%; }
        100% { width: 0%; }
    }
`;
document.head.appendChild(visualFeedbackStyles);

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.visualFeedback = new VisualFeedbackSystem();
});

// Export pour utilisation externe
window.VisualFeedbackSystem = VisualFeedbackSystem;
