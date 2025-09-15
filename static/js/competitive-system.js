/* ===== ARKALIA QUEST - COMPETITIVE SYSTEM ===== */

class CompetitiveSystem {
    constructor() {
        this.challenges = new Map();
        this.badges = new Map();
        this.leaderboard = [];
        this.duels = new Map();
        this.init();
    }

    init() {
        console.log('🏆 Système compétitif initialisé');
        this.loadChallenges();
        this.loadBadges();
        this.loadLeaderboard();
        this.setupEventListeners();
    }

    // Chargement des défis compétitifs
    loadChallenges() {
        const challenges = [
            {
                id: 'speed_challenge',
                name: 'Défi de vitesse',
                description: 'Exécutez 20 commandes en moins de 30 secondes',
                type: 'speed',
                difficulty: 'medium',
                reward: { points: 200, badge: 'speed_demon' },
                requirements: {
                    commandCount: 20,
                    timeLimit: 30000,
                    accuracy: 90
                },
                status: 'available'
            },
            {
                id: 'accuracy_challenge',
                name: 'Défi de précision',
                description: 'Maintenez 100% de précision sur 50 commandes consécutives',
                type: 'accuracy',
                difficulty: 'hard',
                reward: { points: 300, badge: 'accuracy_master' },
                requirements: {
                    commandCount: 50,
                    accuracy: 100,
                    consecutive: true
                },
                status: 'available'
            },
            {
                id: 'efficiency_challenge',
                name: 'Défi d\'efficacité',
                description: 'Atteignez une efficacité de 15+ pendant 5 minutes',
                type: 'efficiency',
                difficulty: 'expert',
                reward: { points: 500, badge: 'efficiency_guru' },
                requirements: {
                    efficiency: 15,
                    duration: 300000,
                    minActions: 100
                },
                status: 'available'
            },
            {
                id: 'streak_challenge',
                name: 'Défi de séquence',
                description: 'Atteignez une séquence de 30 succès consécutifs',
                type: 'streak',
                difficulty: 'legendary',
                reward: { points: 1000, badge: 'streak_legend' },
                requirements: {
                    streak: 30,
                    consecutive: true
                },
                status: 'available'
            }
        ];

        this.challenges = new Map(challenges.map(c => [c.id, c]));
    }

    // Chargement des badges
    loadBadges() {
        const badges = [
            {
                id: 'speed_demon',
                name: 'Démon de vitesse',
                description: 'Exécutez des commandes à la vitesse de l\'éclair',
                rarity: 'common',
                category: 'speed',
                requirements: 'Exécuter 10 commandes en moins de 1 seconde chacune',
                progress: 0,
                maxProgress: 10,
                unlocked: false,
                icon: '⚡',
                color: '#ff6b6b'
            },
            {
                id: 'accuracy_master',
                name: 'Maître de la précision',
                description: 'Une précision chirurgicale dans l\'exécution',
                rarity: 'rare',
                category: 'accuracy',
                requirements: 'Maintenir 95% de précision sur 50 commandes',
                progress: 0,
                maxProgress: 50,
                unlocked: false,
                icon: '🎯',
                color: '#4caf50'
            },
            {
                id: 'efficiency_guru',
                name: 'Guru de l\'efficacité',
                description: 'Optimisation maximale des performances',
                rarity: 'epic',
                category: 'efficiency',
                requirements: 'Maintenir une efficacité supérieure à 10',
                progress: 0,
                maxProgress: 1,
                unlocked: false,
                icon: '🧠',
                color: '#9c27b0'
            },
            {
                id: 'streak_legend',
                name: 'Légende des séquences',
                description: 'Des séquences de succès légendaires',
                rarity: 'legendary',
                category: 'streak',
                requirements: 'Atteindre une séquence de 30 succès consécutifs',
                progress: 0,
                maxProgress: 30,
                unlocked: false,
                icon: '👑',
                color: '#ffc107'
            },
            {
                id: 'first_blood',
                name: 'Premier sang',
                description: 'Votre première victoire compétitive',
                rarity: 'common',
                category: 'pvp',
                requirements: 'Gagner votre premier duel',
                progress: 0,
                maxProgress: 1,
                unlocked: false,
                icon: '🩸',
                color: '#f44336'
            },
            {
                id: 'duel_master',
                name: 'Maître des duels',
                description: 'Dominez l\'arène compétitive',
                rarity: 'epic',
                category: 'pvp',
                requirements: 'Gagner 10 duels',
                progress: 0,
                maxProgress: 10,
                unlocked: false,
                icon: '⚔️',
                color: '#ff9800'
            }
        ];

        this.badges = new Map(badges.map(b => [b.id, b]));
    }

    // Chargement du leaderboard
    loadLeaderboard() {
        // Simuler des données de leaderboard
        this.leaderboard = [
            { rank: 1, name: 'CyberMaster', score: 15420, level: 25, badges: 12 },
            { rank: 2, name: 'MatrixHacker', score: 14230, level: 23, badges: 10 },
            { rank: 3, name: 'LunaElite', score: 13890, level: 22, badges: 9 },
            { rank: 4, name: 'ArkaliaPro', score: 12560, level: 20, badges: 8 },
            { rank: 5, name: 'QuantumGamer', score: 11240, level: 18, badges: 7 }
        ];
    }

    // Démarrer un défi
    startChallenge(challengeId) {
        const challenge = this.challenges.get(challengeId);
        if (!challenge || challenge.status !== 'available') {
            this.showError('Défi non disponible');
            return;
        }

        challenge.status = 'active';
        challenge.startTime = Date.now();
        challenge.progress = 0;

        this.showChallengeStart(challenge);
        this.trackChallengeProgress(challengeId);
    }

    // Suivi de la progression d'un défi
    trackChallengeProgress(challengeId) {
        const challenge = this.challenges.get(challengeId);
        if (!challenge) return;

        const interval = setInterval(() => {
            if (challenge.status !== 'active') {
                clearInterval(interval);
                return;
            }

            // Vérifier les conditions du défi
            const progress = this.checkChallengeProgress(challenge);
            challenge.progress = progress;

            // Mettre à jour l'affichage
            this.updateChallengeDisplay(challengeId);

            // Vérifier si le défi est complété
            if (progress >= 100) {
                this.completeChallenge(challengeId);
                clearInterval(interval);
            }
        }, 1000);
    }

    // Vérifier la progression d'un défi
    checkChallengeProgress(challenge) {
        const now = Date.now();
        const elapsed = now - challenge.startTime;

        switch (challenge.type) {
            case 'speed':
                return this.checkSpeedChallenge(challenge, elapsed);
            case 'accuracy':
                return this.checkAccuracyChallenge(challenge);
            case 'efficiency':
                return this.checkEfficiencyChallenge(challenge, elapsed);
            case 'streak':
                return this.checkStreakChallenge(challenge);
            default:
                return 0;
        }
    }

    // Vérifier le défi de vitesse
    checkSpeedChallenge(challenge, elapsed) {
        const commandCount = this.getCommandCount();
        const progress = (commandCount / challenge.requirements.commandCount) * 100;

        if (elapsed > challenge.requirements.timeLimit) {
            this.failChallenge(challenge.id, 'Temps écoulé');
            return 100;
        }

        return Math.min(progress, 100);
    }

    // Vérifier le défi de précision
    checkAccuracyChallenge(challenge) {
        const accuracy = this.getCurrentAccuracy();
        const commandCount = this.getCommandCount();

        if (accuracy < challenge.requirements.accuracy) {
            this.failChallenge(challenge.id, 'Précision insuffisante');
            return 100;
        }

        const progress = (commandCount / challenge.requirements.commandCount) * 100;
        return Math.min(progress, 100);
    }

    // Vérifier le défi d'efficacité
    checkEfficiencyChallenge(challenge, elapsed) {
        const efficiency = this.getCurrentEfficiency();
        const actionCount = this.getActionCount();

        if (efficiency < challenge.requirements.efficiency) {
            this.failChallenge(challenge.id, 'Efficacité insuffisante');
            return 100;
        }

        if (elapsed > challenge.requirements.duration) {
            this.completeChallenge(challenge.id);
            return 100;
        }

        const progress = (elapsed / challenge.requirements.duration) * 100;
        return Math.min(progress, 100);
    }

    // Vérifier le défi de séquence
    checkStreakChallenge(challenge) {
        const currentStreak = this.getCurrentStreak();
        const progress = (currentStreak / challenge.requirements.streak) * 100;

        if (currentStreak === 0) {
            this.failChallenge(challenge.id, 'Séquence interrompue');
            return 100;
        }

        return Math.min(progress, 100);
    }

    // Compléter un défi
    completeChallenge(challengeId) {
        const challenge = this.challenges.get(challengeId);
        if (!challenge) return;

        challenge.status = 'completed';
        challenge.completionTime = Date.now();

        // Accorder les récompenses
        this.grantReward(challenge.reward);

        // Débloquer le badge si applicable
        if (challenge.reward.badge) {
            this.unlockBadge(challenge.reward.badge);
        }

        this.showChallengeComplete(challenge);
    }

    // Échouer un défi
    failChallenge(challengeId, reason) {
        const challenge = this.challenges.get(challengeId);
        if (!challenge) return;

        challenge.status = 'failed';
        this.showChallengeFailed(challenge, reason);
    }

    // Accorder une récompense
    grantReward(reward) {
        // Mettre à jour le score
        this.updateScore(reward.points);

        // Afficher la notification
        this.showRewardNotification(reward);
    }

    // Débloquer un badge
    unlockBadge(badgeId) {
        const badge = this.badges.get(badgeId);
        if (!badge) return;

        badge.unlocked = true;
        badge.unlockTime = Date.now();

        this.showBadgeUnlocked(badge);
        this.updateBadgeProgress(badgeId);
    }

    // Mettre à jour la progression d'un badge
    updateBadgeProgress(badgeId) {
        const badge = this.badges.get(badgeId);
        if (!badge) return;

        switch (badge.category) {
            case 'speed':
                badge.progress = this.getSpeedProgress();
                break;
            case 'accuracy':
                badge.progress = this.getAccuracyProgress();
                break;
            case 'efficiency':
                badge.progress = this.getEfficiencyProgress();
                break;
            case 'streak':
                badge.progress = this.getStreakProgress();
                break;
            case 'pvp':
                badge.progress = this.getPvPProgress();
                break;
        }

        // Vérifier si le badge est débloqué
        if (badge.progress >= badge.maxProgress && !badge.unlocked) {
            this.unlockBadge(badgeId);
        }
    }

    // Système de duels
    createDuel(opponentId) {
        const duel = {
            id: this.generateDuelId(),
            opponent: opponentId,
            status: 'pending',
            startTime: null,
            endTime: null,
            winner: null,
            score: { player: 0, opponent: 0 }
        };

        this.duels.set(duel.id, duel);
        return duel;
    }

    // Démarrer un duel
    startDuel(duelId) {
        const duel = this.duels.get(duelId);
        if (!duel) return;

        duel.status = 'active';
        duel.startTime = Date.now();

        this.showDuelStart(duel);
        this.trackDuelProgress(duelId);
    }

    // Suivi de la progression d'un duel
    trackDuelProgress(duelId) {
        const duel = this.duels.get(duelId);
        if (!duel) return;

        const interval = setInterval(() => {
            if (duel.status !== 'active') {
                clearInterval(interval);
                return;
            }

            // Mettre à jour les scores
            duel.score.player = this.getCurrentScore();
            duel.score.opponent = this.getOpponentScore(duel.opponent);

            // Vérifier les conditions de fin
            if (this.checkDuelEndConditions(duel)) {
                this.endDuel(duelId);
                clearInterval(interval);
            }
        }, 1000);
    }

    // Vérifier les conditions de fin de duel
    checkDuelEndConditions(duel) {
        const elapsed = Date.now() - duel.startTime;
        const timeLimit = 300000; // 5 minutes

        return elapsed > timeLimit ||
            duel.score.player >= 1000 ||
            duel.score.opponent >= 1000;
    }

    // Terminer un duel
    endDuel(duelId) {
        const duel = this.duels.get(duelId);
        if (!duel) return;

        duel.status = 'completed';
        duel.endTime = Date.now();
        duel.winner = duel.score.player > duel.score.opponent ? 'player' : 'opponent';

        this.showDuelEnd(duel);
        this.updateDuelStats(duel);
    }

    // Affichage des notifications
    showChallengeStart(challenge) {
        this.showNotification(`Défi "${challenge.name}" démarré !`, 'info');
    }

    showChallengeComplete(challenge) {
        this.showNotification(`Défi "${challenge.name}" complété ! +${challenge.reward.points} points`, 'success');
    }

    showChallengeFailed(challenge, reason) {
        this.showNotification(`Défi "${challenge.name}" échoué : ${reason}`, 'error');
    }

    showBadgeUnlocked(badge) {
        this.showNotification(`Badge débloqué : ${badge.name} !`, 'achievement');
    }

    showRewardNotification(reward) {
        this.showNotification(`Récompense : +${reward.points} points`, 'reward');
    }

    showDuelStart(duel) {
        this.showNotification(`Duel contre ${duel.opponent} démarré !`, 'duel');
    }

    showDuelEnd(duel) {
        const result = duel.winner === 'player' ? 'Victoire !' : 'Défaite...';
        this.showNotification(`Duel terminé : ${result}`, duel.winner === 'player' ? 'victory' : 'defeat');
    }

    // Notification générique
    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `competitive-notification ${type}`;
        notification.textContent = message;

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
        }, 3000);
    }

    // Utilitaires
    getCommandCount() {
        return parseInt(localStorage.getItem('arkalia_command_count') || '0');
    }

    getCurrentAccuracy() {
        return parseFloat(localStorage.getItem('arkalia_accuracy') || '0');
    }

    getCurrentEfficiency() {
        return parseFloat(localStorage.getItem('arkalia_efficiency') || '0');
    }

    getCurrentStreak() {
        return parseInt(localStorage.getItem('arkalia_streak') || '0');
    }

    getCurrentScore() {
        return parseInt(localStorage.getItem('arkalia_score') || '0');
    }

    getOpponentScore(opponentId) {
        // Simuler le score de l'opposant
        return Math.floor(Math.random() * 1000);
    }

    updateScore(points) {
        const currentScore = this.getCurrentScore();
        localStorage.setItem('arkalia_score', currentScore + points);
    }

    generateDuelId() {
        return 'duel_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Écouter les commandes du terminal
        document.addEventListener('terminal-command', (e) => {
            this.updateBadgeProgress('speed_demon');
            this.updateBadgeProgress('accuracy_master');
            this.updateBadgeProgress('streak_legend');
        });

        // Écouter les mises à jour de score
        document.addEventListener('score-update', (e) => {
            this.updateBadgeProgress('efficiency_guru');
        });
    }
}

// Initialiser le système compétitif
window.competitiveSystem = new CompetitiveSystem();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CompetitiveSystem;
}
