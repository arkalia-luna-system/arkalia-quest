/* ===== ARKALIA QUEST - PROGRESSION FEEDBACK SYSTEM ===== */

class ProgressionFeedbackSystem {
    constructor() {
        this.userStats = this.loadUserStats();
        this.performanceMetrics = new Map();
        this.achievements = new Map();
        this.leaderboard = [];
        this.init();
    }

    init() {
        console.log('📊 Système de feedback de progression initialisé');
        this.setupEventListeners();
        this.startPerformanceTracking();
        this.loadAchievements();
    }

    // Suivi des performances en temps réel
    startPerformanceTracking() {
        this.trackCommandSpeed();
        this.trackAccuracy();
        this.trackEfficiency();
        this.trackStreaks();
    }

    // Vitesse des commandes
    trackCommandSpeed() {
        let commandStartTime = null;
        let commandCount = 0;
        let totalTime = 0;

        document.addEventListener('terminal-command-start', () => {
            commandStartTime = Date.now();
        });

        document.addEventListener('terminal-command-end', (e) => {
            if (commandStartTime) {
                const duration = Date.now() - commandStartTime;
                commandCount++;
                totalTime += duration;

                const avgSpeed = totalTime / commandCount;
                this.performanceMetrics.set('commandSpeed', avgSpeed);

                // Feedback pour vitesse exceptionnelle
                if (duration < 1000) {
                    this.showSpeedFeedback('Rapide !', 'green');
                } else if (duration < 2000) {
                    this.showSpeedFeedback('Bien !', 'blue');
                }

                commandStartTime = null;
            }
        });
    }

    // Précision des commandes
    trackAccuracy() {
        let totalCommands = 0;
        let successfulCommands = 0;

        document.addEventListener('terminal-command', (e) => {
            totalCommands++;
            if (e.detail.success) {
                successfulCommands++;
            }

            const accuracy = (successfulCommands / totalCommands) * 100;
            this.performanceMetrics.set('accuracy', accuracy);

            // Feedback pour précision
            if (accuracy >= 95) {
                this.showAccuracyFeedback('Précision parfaite !', 'gold');
            } else if (accuracy >= 90) {
                this.showAccuracyFeedback('Très précis !', 'green');
            } else if (accuracy >= 80) {
                this.showAccuracyFeedback('Bon niveau !', 'blue');
            }
        });
    }

    // Efficacité globale
    trackEfficiency() {
        const startTime = Date.now();
        let actionsPerformed = 0;
        let scoreGained = 0;

        setInterval(() => {
            const timeElapsed = (Date.now() - startTime) / 1000; // en secondes
            const efficiency = (actionsPerformed + scoreGained) / timeElapsed;
            this.performanceMetrics.set('efficiency', efficiency);

            // Feedback pour efficacité
            if (efficiency > 10) {
                this.showEfficiencyFeedback('Efficacité maximale !', 'purple');
            } else if (efficiency > 5) {
                this.showEfficiencyFeedback('Très efficace !', 'green');
            }
        }, 30000); // Vérifier toutes les 30 secondes
    }

    // Séquences de succès
    trackStreaks() {
        let currentStreak = 0;
        let bestStreak = 0;
        let lastSuccess = true;

        document.addEventListener('terminal-command', (e) => {
            if (e.detail.success) {
                if (lastSuccess) {
                    currentStreak++;
                } else {
                    currentStreak = 1;
                }
                lastSuccess = true;
            } else {
                currentStreak = 0;
                lastSuccess = false;
            }

            if (currentStreak > bestStreak) {
                bestStreak = currentStreak;
            }

            this.performanceMetrics.set('currentStreak', currentStreak);
            this.performanceMetrics.set('bestStreak', bestStreak);

            // Feedback pour les séquences
            if (currentStreak === 5) {
                this.showStreakFeedback('Séquence de 5 !', 'orange');
            } else if (currentStreak === 10) {
                this.showStreakFeedback('Séquence de 10 !', 'red');
            } else if (currentStreak === 20) {
                this.showStreakFeedback('Séquence de 20 !', 'purple');
            }
        });
    }

    // Affichage des feedbacks de vitesse
    showSpeedFeedback(message, color) {
        this.showFloatingFeedback(message, color, 'speed');
    }

    // Affichage des feedbacks de précision
    showAccuracyFeedback(message, color) {
        this.showFloatingFeedback(message, color, 'accuracy');
    }

    // Affichage des feedbacks d'efficacité
    showEfficiencyFeedback(message, color) {
        this.showFloatingFeedback(message, color, 'efficiency');
    }

    // Affichage des feedbacks de séquence
    showStreakFeedback(message, color) {
        this.showFloatingFeedback(message, color, 'streak');
    }

    // Affichage des feedbacks flottants
    showFloatingFeedback(message, color, type) {
        const feedback = document.createElement('div');
        feedback.className = `floating-feedback ${type} ${color}`;
        feedback.textContent = message;

        // Position aléatoire
        const x = Math.random() * (window.innerWidth - 200) + 100;
        const y = Math.random() * (window.innerHeight - 100) + 50;

        feedback.style.left = `${x}px`;
        feedback.style.top = `${y}px`;

        document.body.appendChild(feedback);

        // Animation d'apparition
        setTimeout(() => {
            feedback.classList.add('show');
        }, 100);

        // Suppression automatique
        setTimeout(() => {
            feedback.classList.remove('show');
            setTimeout(() => {
                if (feedback.parentNode) {
                    feedback.parentNode.removeChild(feedback);
                }
            }, 300);
        }, 3000);
    }

    // Système d'achievements
    loadAchievements() {
        const achievements = [
            {
                id: 'speed_demon',
                name: 'Démon de vitesse',
                description: 'Exécutez 10 commandes en moins de 1 seconde chacune',
                condition: () => this.performanceMetrics.get('commandSpeed') < 1000,
                reward: { points: 100, badge: 'speed_demon' }
            },
            {
                id: 'accuracy_master',
                name: 'Maître de la précision',
                description: 'Maintenez 95% de précision sur 50 commandes',
                condition: () => this.performanceMetrics.get('accuracy') >= 95,
                reward: { points: 150, badge: 'accuracy_master' }
            },
            {
                id: 'streak_king',
                name: 'Roi des séquences',
                description: 'Atteignez une séquence de 20 succès consécutifs',
                condition: () => this.performanceMetrics.get('bestStreak') >= 20,
                reward: { points: 200, badge: 'streak_king' }
            },
            {
                id: 'efficiency_guru',
                name: 'Guru de l\'efficacité',
                description: 'Maintenez une efficacité supérieure à 10',
                condition: () => this.performanceMetrics.get('efficiency') > 10,
                reward: { points: 250, badge: 'efficiency_guru' }
            }
        ];

        this.achievements = new Map(achievements.map(a => [a.id, a]));
    }

    // Vérification des achievements
    checkAchievements() {
        this.achievements.forEach((achievement, id) => {
            if (!this.userStats.achievements.includes(id) && achievement.condition()) {
                this.unlockAchievement(achievement);
            }
        });
    }

    // Déblocage d'un achievement
    unlockAchievement(achievement) {
        this.userStats.achievements.push(achievement.id);
        this.userStats.points += achievement.reward.points;

        // Affichage de l'achievement
        this.showAchievementNotification(achievement);

        // Sauvegarde
        this.saveUserStats();
    }

    // Notification d'achievement
    showAchievementNotification(achievement) {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div class="achievement-icon">🏆</div>
            <div class="achievement-content">
                <div class="achievement-title">${achievement.name}</div>
                <div class="achievement-description">${achievement.description}</div>
                <div class="achievement-reward">+${achievement.reward.points} points</div>
            </div>
        `;

        document.body.appendChild(notification);

        // Animation d'apparition
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Suppression automatique
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 500);
        }, 5000);
    }

    // Tableau de bord des performances
    createPerformanceDashboard() {
        const dashboard = document.createElement('div');
        dashboard.className = 'performance-dashboard';
        dashboard.innerHTML = `
            <div class="performance-title">Tableau de bord des performances</div>
            <div class="performance-metrics">
                <div class="metric">
                    <div class="metric-label">Vitesse moyenne</div>
                    <div class="metric-value" id="speed-value">${this.performanceMetrics.get('commandSpeed') || 0}ms</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Précision</div>
                    <div class="metric-value" id="accuracy-value">${this.performanceMetrics.get('accuracy') || 0}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Efficacité</div>
                    <div class="metric-value" id="efficiency-value">${this.performanceMetrics.get('efficiency') || 0}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Meilleure séquence</div>
                    <div class="metric-value" id="streak-value">${this.performanceMetrics.get('bestStreak') || 0}</div>
                </div>
            </div>
        `;

        return dashboard;
    }

    // Mise à jour du tableau de bord
    updatePerformanceDashboard() {
        const speedValue = document.getElementById('speed-value');
        const accuracyValue = document.getElementById('accuracy-value');
        const efficiencyValue = document.getElementById('efficiency-value');
        const streakValue = document.getElementById('streak-value');

        if (speedValue) {
            speedValue.textContent = `${Math.round(this.performanceMetrics.get('commandSpeed') || 0)}ms`;
        }
        if (accuracyValue) {
            accuracyValue.textContent = `${Math.round(this.performanceMetrics.get('accuracy') || 0)}%`;
        }
        if (efficiencyValue) {
            efficiencyValue.textContent = `${Math.round(this.performanceMetrics.get('efficiency') || 0)}`;
        }
        if (streakValue) {
            streakValue.textContent = `${this.performanceMetrics.get('bestStreak') || 0}`;
        }
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Écouter les commandes du terminal
        document.addEventListener('terminal-command', (e) => {
            this.trackCommand(e.detail);
        });

        // Écouter les changements de score
        document.addEventListener('score-update', (e) => {
            this.trackScoreUpdate(e.detail);
        });

        // Écouter les missions complétées
        document.addEventListener('mission-completed', (e) => {
            this.trackMissionCompletion(e.detail);
        });

        // Vérifier les achievements périodiquement
        setInterval(() => {
            this.checkAchievements();
        }, 5000);
    }

    // Suivi des commandes
    trackCommand(detail) {
        // Mise à jour des métriques
        this.updatePerformanceMetrics();

        // Vérification des achievements
        this.checkAchievements();

        // Mise à jour du tableau de bord
        this.updatePerformanceDashboard();
    }

    // Suivi des mises à jour de score
    trackScoreUpdate(detail) {
        this.userStats.totalScore += detail.points;
        this.userStats.scoreHistory.push({
            points: detail.points,
            timestamp: Date.now(),
            source: detail.source
        });

        // Feedback pour les gains de score
        if (detail.points >= 100) {
            this.showScoreFeedback(`+${detail.points} points !`, 'gold');
        } else if (detail.points >= 50) {
            this.showScoreFeedback(`+${detail.points} points !`, 'green');
        } else if (detail.points >= 10) {
            this.showScoreFeedback(`+${detail.points} points !`, 'blue');
        }

        this.saveUserStats();
    }

    // Suivi des missions complétées
    trackMissionCompletion(detail) {
        this.userStats.missionsCompleted++;
        this.userStats.missionHistory.push({
            mission: detail.mission,
            timestamp: Date.now(),
            points: detail.points
        });

        // Feedback pour les missions
        this.showMissionFeedback(`Mission "${detail.mission}" complétée !`, 'green');

        this.saveUserStats();
    }

    // Affichage des feedbacks de score
    showScoreFeedback(message, color) {
        this.showFloatingFeedback(message, color, 'score');
    }

    // Affichage des feedbacks de mission
    showMissionFeedback(message, color) {
        this.showFloatingFeedback(message, color, 'mission');
    }

    // Mise à jour des métriques de performance
    updatePerformanceMetrics() {
        // Calculer les métriques basées sur l'historique
        const recentCommands = this.userStats.commandHistory.slice(-50);
        const successfulCommands = recentCommands.filter(c => c.success);

        if (recentCommands.length > 0) {
            const accuracy = (successfulCommands.length / recentCommands.length) * 100;
            this.performanceMetrics.set('accuracy', accuracy);
        }

        // Calculer la vitesse moyenne
        const recentSpeeds = recentCommands.map(c => c.duration).filter(d => d > 0);
        if (recentSpeeds.length > 0) {
            const avgSpeed = recentSpeeds.reduce((a, b) => a + b, 0) / recentSpeeds.length;
            this.performanceMetrics.set('commandSpeed', avgSpeed);
        }
    }

    // Utilitaires
    loadUserStats() {
        return JSON.parse(localStorage.getItem('arkalia_user_stats') || JSON.stringify({
            totalScore: 0,
            missionsCompleted: 0,
            achievements: [],
            commandHistory: [],
            scoreHistory: [],
            missionHistory: []
        }));
    }

    saveUserStats() {
        localStorage.setItem('arkalia_user_stats', JSON.stringify(this.userStats));
    }
}

// Initialiser le système de feedback de progression
window.progressionFeedback = new ProgressionFeedbackSystem();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProgressionFeedbackSystem;
}
