/* ===== ARKALIA QUEST - CASUAL SYSTEM ===== */

class CasualSystem {
    constructor() {
        this.idleRewards = new Map();
        this.welcomeMessages = [];
        this.returnRewards = [];
        this.idleTimer = null;
        this.lastActivity = Date.now();
        this.init();
    }

    init() {
        console.log('😌 Système casual initialisé');
        this.loadIdleRewards();
        this.loadWelcomeMessages();
        this.loadReturnRewards();
        this.setupEventListeners();
        this.startIdleTracking();
    }

    // Chargement des récompenses d'inactivité
    loadIdleRewards() {
        const rewards = [
            {
                id: 'idle_5min',
                name: 'Pause de 5 minutes',
                description: 'Vous avez pris une pause de 5 minutes',
                timeRequired: 300000, // 5 minutes
                reward: { points: 50, message: 'Petite pause bien méritée !' },
                unlocked: false
            },
            {
                id: 'idle_15min',
                name: 'Pause de 15 minutes',
                description: 'Vous avez pris une pause de 15 minutes',
                timeRequired: 900000, // 15 minutes
                reward: { points: 150, message: 'Pause relaxante !' },
                unlocked: false
            },
            {
                id: 'idle_30min',
                name: 'Pause de 30 minutes',
                description: 'Vous avez pris une pause de 30 minutes',
                timeRequired: 1800000, // 30 minutes
                reward: { points: 300, message: 'Longue pause détente !' },
                unlocked: false
            },
            {
                id: 'idle_1hour',
                name: 'Pause d\'une heure',
                description: 'Vous avez pris une pause d\'une heure',
                timeRequired: 3600000, // 1 heure
                reward: { points: 600, message: 'Pause bien méritée !' },
                unlocked: false
            },
            {
                id: 'idle_1day',
                name: 'Retour après une journée',
                description: 'Vous revenez après une journée d\'absence',
                timeRequired: 86400000, // 1 jour
                reward: { points: 1000, message: 'Bienvenue de retour !' },
                unlocked: false
            }
        ];

        this.idleRewards = new Map(rewards.map(r => [r.id, r]));
    }

    // Chargement des messages d'accueil
    loadWelcomeMessages() {
        this.welcomeMessages = [
            'Bienvenue de retour dans Arkalia Quest ! 🌟',
            'Ravie de vous revoir ! Comment s\'est passée votre journée ? 😊',
            'LUNA vous a attendue avec impatience ! 💫',
            'Prêt pour une nouvelle aventure relaxante ? 🚀',
            'Votre progression vous attend sagement... 📚',
            'Envie de continuer votre exploration ? 🗺️',
            'LUNA a préparé quelque chose de spécial pour vous ! 🎁',
            'Votre profil a été mis à jour pendant votre absence ! 📊',
            'Des nouvelles missions vous attendent ! 🎯',
            'Votre score a évolué en douceur... 📈'
        ];
    }

    // Chargement des récompenses de retour
    loadReturnRewards() {
        this.returnRewards = [
            {
                timeAway: 300000, // 5 minutes
                message: 'Petite pause bien méritée !',
                points: 50,
                badge: null
            },
            {
                timeAway: 900000, // 15 minutes
                message: 'Pause relaxante !',
                points: 150,
                badge: null
            },
            {
                timeAway: 1800000, // 30 minutes
                message: 'Longue pause détente !',
                points: 300,
                badge: null
            },
            {
                timeAway: 3600000, // 1 heure
                message: 'Pause bien méritée !',
                points: 600,
                badge: 'relaxed_player'
            },
            {
                timeAway: 86400000, // 1 jour
                message: 'Bienvenue de retour !',
                points: 1000,
                badge: 'returning_hero'
            }
        ];
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Écouter l'activité de l'utilisateur
        ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
            document.addEventListener(event, () => {
                this.updateLastActivity();
            });
        });

        // Écouter la visibilité de la page
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.handlePageHidden();
            } else {
                this.handlePageVisible();
            }
        });

        // Écouter le chargement de la page
        window.addEventListener('load', () => {
            this.handlePageLoad();
        });
    }

    // Démarrer le suivi d'inactivité
    startIdleTracking() {
        this.idleTimer = setInterval(() => {
            this.checkIdleRewards();
        }, 60000); // Vérifier toutes les minutes
    }

    // Mise à jour de la dernière activité
    updateLastActivity() {
        this.lastActivity = Date.now();
    }

    // Gestion de la page cachée
    handlePageHidden() {
        this.lastActivity = Date.now();
    }

    // Gestion de la page visible
    handlePageVisible() {
        const timeAway = Date.now() - this.lastActivity;
        this.handleReturn(timeAway);
    }

    // Gestion du chargement de la page
    handlePageLoad() {
        const lastVisit = this.getLastVisit();
        if (lastVisit) {
            const timeAway = Date.now() - lastVisit;
            this.handleReturn(timeAway);
        }
        this.setLastVisit();
    }

    // Gestion du retour
    handleReturn(timeAway) {
        const reward = this.getReturnReward(timeAway);
        if (reward) {
            this.grantReturnReward(reward);
        }

        this.showWelcomeMessage();
        this.updateIdleRewards(timeAway);
    }

    // Obtenir la récompense de retour
    getReturnReward(timeAway) {
        return this.returnRewards.find(reward => timeAway >= reward.timeAway);
    }

    // Accorder une récompense de retour
    grantReturnReward(reward) {
        this.updateScore(reward.points);
        this.showReturnNotification(reward);

        if (reward.badge) {
            this.unlockBadge(reward.badge);
        }
    }

    // Vérification des récompenses d'inactivité
    checkIdleRewards() {
        const idleTime = Date.now() - this.lastActivity;

        this.idleRewards.forEach((reward, id) => {
            if (!reward.unlocked && idleTime >= reward.timeRequired) {
                this.unlockIdleReward(id);
            }
        });
    }

    // Déblocage d'une récompense d'inactivité
    unlockIdleReward(id) {
        const reward = this.idleRewards.get(id);
        if (!reward) return;

        reward.unlocked = true;
        this.updateScore(reward.reward.points);
        this.showIdleRewardNotification(reward);
        this.saveIdleRewards();
    }

    // Mise à jour des récompenses d'inactivité
    updateIdleRewards(timeAway) {
        this.idleRewards.forEach((reward, id) => {
            if (!reward.unlocked && timeAway >= reward.timeRequired) {
                this.unlockIdleReward(id);
            }
        });
    }

    // Affichage des messages d'accueil
    showWelcomeMessage() {
        const message = this.getRandomWelcomeMessage();
        this.showCasualNotification(message, 'welcome');
    }

    // Obtenir un message d'accueil aléatoire
    getRandomWelcomeMessage() {
        return this.welcomeMessages[Math.floor(Math.random() * this.welcomeMessages.length)];
    }

    // Affichage des notifications de retour
    showReturnNotification(reward) {
        this.showCasualNotification(reward.message, 'return');
    }

    // Affichage des notifications de récompense d'inactivité
    showIdleRewardNotification(reward) {
        this.showCasualNotification(reward.reward.message, 'idle-reward');
    }

    // Notification casual générique
    showCasualNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `casual-notification ${type}`;
        notification.innerHTML = `
            <div class="casual-icon">${this.getIconForType(type)}</div>
            <div class="casual-message">${message}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }

    // Obtenir l'icône pour le type
    getIconForType(type) {
        const icons = {
            'welcome': '🌟',
            'return': '🎉',
            'idle-reward': '🎁',
            'casual': '😊'
        };
        return icons[type] || '😊';
    }

    // Système de progression douce
    enableGentleProgression() {
        // Réduire la fréquence des notifications
        this.setNotificationFrequency('low');

        // Activer les animations douces
        this.enableGentleAnimations();

        // Personnaliser les messages
        this.customizeMessages();
    }

    // Définir la fréquence des notifications
    setNotificationFrequency(frequency) {
        const frequencies = {
            'low': 30000,    // 30 secondes
            'medium': 15000, // 15 secondes
            'high': 5000     // 5 secondes
        };

        if (this.idleTimer) {
            clearInterval(this.idleTimer);
        }

        this.idleTimer = setInterval(() => {
            this.checkIdleRewards();
        }, frequencies[frequency] || 30000);
    }

    // Activer les animations douces
    enableGentleAnimations() {
        document.body.classList.add('gentle-animations');
    }

    // Personnaliser les messages
    customizeMessages() {
        // Remplacer les messages techniques par des messages plus doux
        const gentleMessages = {
            'error': 'Oups, quelque chose ne s\'est pas passé comme prévu...',
            'success': 'Parfait ! Vous y êtes arrivé !',
            'loading': 'LUNA réfléchit...',
            'complete': 'Mission accomplie avec brio !'
        };

        // Appliquer les messages doux
        Object.entries(gentleMessages).forEach(([key, message]) => {
            this.setGentleMessage(key, message);
        });
    }

    // Définir un message doux
    setGentleMessage(key, message) {
        // Remplacer les messages dans l'interface
        const elements = document.querySelectorAll(`[data-message="${key}"]`);
        elements.forEach(element => {
            element.textContent = message;
        });
    }

    // Système de pause automatique
    enableAutoPause() {
        let pauseTimer = null;
        const pauseDelay = 300000; // 5 minutes

        const resetPauseTimer = () => {
            if (pauseTimer) {
                clearTimeout(pauseTimer);
            }
            pauseTimer = setTimeout(() => {
                this.activateAutoPause();
            }, pauseDelay);
        };

        // Réinitialiser le timer à chaque activité
        ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
            document.addEventListener(event, resetPauseTimer);
        });

        resetPauseTimer();
    }

    // Activation de la pause automatique
    activateAutoPause() {
        this.showCasualNotification('LUNA a mis le jeu en pause pour vous... 😴', 'auto-pause');
        this.pauseGame();
    }

    // Mettre le jeu en pause
    pauseGame() {
        // Pause des animations
        document.body.classList.add('game-paused');

        // Pause des timers
        if (this.idleTimer) {
            clearInterval(this.idleTimer);
        }

        // Sauvegarder l'état
        this.saveGameState();
    }

    // Reprendre le jeu
    resumeGame() {
        document.body.classList.remove('game-paused');
        this.startIdleTracking();
        this.showCasualNotification('Bienvenue de retour ! Le jeu reprend... 🎮', 'resume');
    }

    // Système de récompenses progressives
    enableProgressiveRewards() {
        // Récompenses basées sur le temps de jeu
        this.trackPlayTime();

        // Récompenses basées sur la fréquence de retour
        this.trackReturnFrequency();

        // Récompenses basées sur la progression douce
        this.trackGentleProgress();
    }

    // Suivi du temps de jeu
    trackPlayTime() {
        let playTime = 0;
        const startTime = Date.now();

        setInterval(() => {
            if (!document.hidden) {
                playTime += 60000; // 1 minute
                this.checkPlayTimeRewards(playTime);
            }
        }, 60000);
    }

    // Vérification des récompenses de temps de jeu
    checkPlayTimeRewards(playTime) {
        const rewards = [
            { time: 300000, message: '30 minutes de jeu !', points: 100 }, // 5 minutes
            { time: 600000, message: '1 heure de jeu !', points: 200 }, // 10 minutes
            { time: 1800000, message: '30 minutes de jeu !', points: 500 }, // 30 minutes
            { time: 3600000, message: '1 heure de jeu !', points: 1000 } // 1 heure
        ];

        rewards.forEach(reward => {
            if (playTime === reward.time) {
                this.updateScore(reward.points);
                this.showCasualNotification(reward.message, 'play-time');
            }
        });
    }

    // Suivi de la fréquence de retour
    trackReturnFrequency() {
        const returns = this.getReturnCount();
        const rewards = [
            { returns: 5, message: '5 retours ! Vous êtes fidèle !', points: 250 },
            { returns: 10, message: '10 retours ! Vous êtes régulier !', points: 500 },
            { returns: 25, message: '25 retours ! Vous êtes assidu !', points: 1000 }
        ];

        rewards.forEach(reward => {
            if (returns === reward.returns) {
                this.updateScore(reward.points);
                this.showCasualNotification(reward.message, 'return-frequency');
            }
        });
    }

    // Suivi de la progression douce
    trackGentleProgress() {
        // Récompenses pour les petites étapes
        const gentleRewards = [
            { action: 'first_command', message: 'Première commande !', points: 50 },
            { action: 'first_mission', message: 'Première mission !', points: 100 },
            { action: 'first_badge', message: 'Premier badge !', points: 150 },
            { action: 'first_theme', message: 'Premier thème !', points: 75 }
        ];

        gentleRewards.forEach(reward => {
            this.trackGentleAction(reward.action, reward.message, reward.points);
        });
    }

    // Suivi d'une action douce
    trackGentleAction(action, message, points) {
        const key = `gentle_${action}`;
        if (!localStorage.getItem(key)) {
            localStorage.setItem(key, 'true');
            this.updateScore(points);
            this.showCasualNotification(message, 'gentle-progress');
        }
    }

    // Utilitaires
    getLastVisit() {
        return parseInt(localStorage.getItem('arkalia_last_visit') || '0');
    }

    setLastVisit() {
        localStorage.setItem('arkalia_last_visit', Date.now().toString());
    }

    getReturnCount() {
        return parseInt(localStorage.getItem('arkalia_return_count') || '0');
    }

    incrementReturnCount() {
        const count = this.getReturnCount() + 1;
        localStorage.setItem('arkalia_return_count', count.toString());
    }

    updateScore(points) {
        const currentScore = parseInt(localStorage.getItem('arkalia_score') || '0');
        localStorage.setItem('arkalia_score', currentScore + points);
    }

    unlockBadge(badgeId) {
        console.log(`Badge débloqué : ${badgeId}`);
    }

    saveIdleRewards() {
        const rewards = Array.from(this.idleRewards.values());
        localStorage.setItem('arkalia_idle_rewards', JSON.stringify(rewards));
    }

    saveGameState() {
        const state = {
            lastActivity: this.lastActivity,
            idleRewards: Array.from(this.idleRewards.values())
        };
        localStorage.setItem('arkalia_game_state', JSON.stringify(state));
    }
}

// Initialiser le système casual
window.casualSystem = new CasualSystem();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CasualSystem;
}
