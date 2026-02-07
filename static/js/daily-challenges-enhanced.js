/**
 * Système de défis quotidiens amélioré et fonctionnel
 * Rend les défis quotidiens vraiment interactifs et engageants
 */

class DailyChallengesEnhanced {
    constructor() {
        this.challenges = new Map();
        this.userProgress = new Map();
        this.activeChallenges = [];
        this.completedToday = new Set();

        this.initializeSystem();
    }

    initializeSystem() {
        // console.log('🎯 Système de défis quotidiens amélioré initialisé');
        this.loadUserProgress();
        this.generateDailyChallenges();
        this.createChallengeInterface();
        this.setupEventListeners();
    }

    loadUserProgress() {
        const saved = localStorage.getItem('arkalia_daily_challenges');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                this.userProgress = new Map(data.progress || []);
                this.completedToday = new Set(data.completedToday || []);
            } catch (e) {
                console.warn('Erreur lors du chargement des défis quotidiens:', e);
            }
        }
    }

    saveUserProgress() {
        const data = {
            progress: Array.from(this.userProgress.entries()),
            completedToday: Array.from(this.completedToday),
            lastUpdate: new Date().toISOString()
        };
        localStorage.setItem('arkalia_daily_challenges', JSON.stringify(data));
    }

    generateDailyChallenges() {
        const today = new Date().toDateString();
        const challenges = [
            {
                id: 'speed_hacker',
                title: '⚡ Speed Hacker',
                description: 'Complète 3 missions en moins de 5 minutes',
                type: 'speed',
                target: 3,
                reward: { xp: 100, badge: 'Speed Demon', coins: 50 },
                condition: 'complete_3_missions_fast',
                timeLimit: 300, // 5 minutes
                difficulty: 'medium'
            },
            {
                id: 'code_master',
                title: '💻 Code Master',
                description: 'Résous 2 mini-jeux de programmation',
                type: 'skill',
                target: 2,
                reward: { xp: 150, badge: 'Code Master', coins: 75 },
                condition: 'solve_2_code_games',
                difficulty: 'hard'
            },
            {
                id: 'social_butterfly',
                title: '🦋 Social Butterfly',
                description: 'Utilise 5 commandes sociales différentes',
                type: 'social',
                target: 5,
                reward: { xp: 80, badge: 'Social Expert', coins: 40 },
                condition: 'use_5_social_commands',
                difficulty: 'easy'
            },
            {
                id: 'night_owl',
                title: '🦉 Night Owl',
                description: 'Joue entre 22h et 6h du matin',
                type: 'time',
                target: 1,
                reward: { xp: 120, badge: 'Night Hacker', coins: 60 },
                condition: 'play_at_night',
                difficulty: 'medium'
            },
            {
                id: 'explorer',
                title: '🗺️ Explorer',
                description: 'Découvre 3 nouvelles zones',
                type: 'exploration',
                target: 3,
                reward: { xp: 90, badge: 'Explorer', coins: 45 },
                condition: 'discover_3_zones',
                difficulty: 'easy'
            },
            {
                id: 'hacker_pro',
                title: '🔐 Hacker Pro',
                description: 'Utilise 10 commandes de hacking',
                type: 'hacking',
                target: 10,
                reward: { xp: 200, badge: 'Hacker Pro', coins: 100 },
                condition: 'use_10_hack_commands',
                difficulty: 'hard'
            }
        ];

        // Sélectionner 3 défis aléatoires pour aujourd'hui
        const selectedChallenges = this.selectRandomChallenges(challenges, 3);

        selectedChallenges.forEach(challenge => {
            this.challenges.set(challenge.id, {
                ...challenge,
                progress: this.userProgress.get(challenge.id) || 0,
                isCompleted: this.completedToday.has(challenge.id),
                startTime: Date.now()
            });
        });

        this.activeChallenges = Array.from(this.challenges.values());
    }

    selectRandomChallenges(challenges, count) {
        const shuffled = [...challenges].sort(() => 0.5 - Math.random());
        return shuffled.slice(0, count);
    }

    createChallengeInterface() {
        // Créer l'interface des défis quotidiens
        const container = document.createElement('div');
        container.id = 'daily-challenges-container';
        container.className = 'daily-challenges-interface';
        container.innerHTML = `
            <div class="challenges-header">
                <h3>🎯 Défis Quotidiens</h3>
                <div class="challenges-timer">
                    <span class="timer-icon">⏰</span>
                    <span class="timer-text">Temps restant: <span id="challenges-timer">--:--:--</span></span>
                </div>
            </div>
            <div class="challenges-list" id="challenges-list">
                <!-- Les défis seront générés ici -->
            </div>
            <div class="challenges-rewards">
                <h4>🏆 Récompenses du jour</h4>
                <div class="rewards-summary" id="rewards-summary">
                    <!-- Résumé des récompenses -->
                </div>
            </div>
        `;

        // Ajouter les styles
        this.addChallengeStyles();

        // Insérer dans la page
        const targetElement = document.querySelector('.daily-challenges, .challenges-section, .sidebar');
        if (targetElement) {
            targetElement.appendChild(container);
        } else {
            // Créer une section dédiée
            const section = document.createElement('div');
            section.className = 'daily-challenges-section';
            section.appendChild(container);
            document.body.appendChild(section);
        }

        this.renderChallenges();
        this.startTimer();
    }

    /** Affiche le panneau des défis (appelé par onclick="dailyChallenges.show()") */
    show() {
        const el = document.getElementById('daily-challenges-container');
        if (el) {
            el.style.display = el.style.display === 'none' ? '' : '';
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    addChallengeStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .daily-challenges-interface {
                background: linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 204, 0, 0.1));
                border: 2px solid #00ff00;
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                font-family: 'Courier New', monospace;
            }
            
            .challenges-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #00ff00;
            }
            
            .challenges-header h3 {
                color: #00ff00;
                margin: 0;
                font-size: 18px;
            }
            
            .challenges-timer {
                display: flex;
                align-items: center;
                gap: 8px;
                color: #00ff00;
                font-size: 14px;
            }
            
            .timer-icon {
                animation: timer-pulse 2s ease-in-out infinite;
            }
            
            @keyframes timer-pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .challenge-item {
                background: rgba(0, 255, 0, 0.05);
                border: 1px solid #00ff00;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .challenge-item:hover {
                background: rgba(0, 255, 0, 0.1);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 255, 0, 0.3);
            }
            
            .challenge-item.completed {
                background: linear-gradient(45deg, rgba(0, 255, 0, 0.2), rgba(0, 204, 0, 0.2));
                border-color: #00cc00;
            }
            
            .challenge-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .challenge-title {
                color: #00ff00;
                font-weight: bold;
                font-size: 16px;
            }
            
            .challenge-difficulty {
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            }
            
            .difficulty-easy { background: #00ff00; color: #000; }
            .difficulty-medium { background: #ffaa00; color: #000; }
            .difficulty-hard { background: #ff4444; color: #fff; }
            
            .challenge-description {
                color: #cccccc;
                margin-bottom: 15px;
                font-size: 14px;
            }
            
            .challenge-progress {
                margin-bottom: 10px;
            }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background: rgba(0, 255, 0, 0.2);
                border-radius: 4px;
                overflow: hidden;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #00ff00, #00cc00);
                transition: width 0.5s ease;
                border-radius: 4px;
            }
            
            .progress-text {
                color: #00ff00;
                font-size: 12px;
                margin-top: 5px;
                text-align: center;
            }
            
            .challenge-reward {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px solid rgba(0, 255, 0, 0.3);
            }
            
            .reward-info {
                color: #00ff00;
                font-size: 14px;
            }
            
            .challenge-action {
                background: #00ff00;
                color: #000;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .challenge-action:hover {
                background: #00cc00;
                transform: scale(1.05);
            }
            
            .challenge-action:disabled {
                background: #666;
                cursor: not-allowed;
                transform: none;
            }
            
            .challenge-completed {
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 24px;
                animation: celebration-bounce 1s ease-out;
            }
            
            @keyframes celebration-bounce {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.2); }
            }
            
            .rewards-summary {
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid #00ff00;
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
            }
            
            .reward-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 5px 0;
                border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            }
            
            .reward-item:last-child {
                border-bottom: none;
            }
        `;
        document.head.appendChild(style);
    }

    renderChallenges() {
        const listContainer = document.getElementById('challenges-list');
        if (!listContainer) return;

        listContainer.innerHTML = '';

        this.activeChallenges.forEach(challenge => {
            const challengeElement = this.createChallengeElement(challenge);
            if (challengeElement && challengeElement.id) listContainer.appendChild(challengeElement);
        });

        this.updateRewardsSummary();
    }

    createChallengeElement(challenge) {
        if (!challenge || typeof challenge !== 'object') return document.createElement('div');
        const target = Number(challenge.target) || 1;
        const progress = Number(challenge.progress) || 0;
        const reward = challenge.reward && typeof challenge.reward === 'object' ? challenge.reward : { xp: 0, coins: 0, badge: '' };
        const element = document.createElement('div');
        element.className = `challenge-item ${challenge.isCompleted ? 'completed' : ''}`;
        element.id = `challenge-${challenge.id || ''}`;

        const progressPercentage = target > 0 ? (progress / target) * 100 : 0;
        const isCompleted = challenge.isCompleted || progress >= target;
        const title = (challenge.title || '').replace(/</g, '&lt;');
        const description = (challenge.description || '').replace(/</g, '&lt;');
        const difficulty = (challenge.difficulty || 'normal').toUpperCase();

        element.innerHTML = `
            <div class="challenge-header">
                <div class="challenge-title">${title}</div>
                <div class="challenge-difficulty difficulty-${challenge.difficulty || 'normal'}">
                    ${difficulty}
                </div>
            </div>
            <div class="challenge-description">${description}</div>
            <div class="challenge-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${progressPercentage}%"></div>
                </div>
                <div class="progress-text">
                    ${progress}/${target} (${Math.round(progressPercentage)}%)
                </div>
            </div>
            <div class="challenge-reward">
                <div class="reward-info">
                    🏆 ${reward.xp ?? 0} XP • ${reward.coins ?? 0} Coins • ${(reward.badge || '').replace(/</g, '&lt;')}
                </div>
                <button class="challenge-action" ${isCompleted ? 'disabled' : ''} 
                        onclick="window.dailyChallengesEnhanced.claimReward('${challenge.id}')">
                    ${isCompleted ? '✅ Complété' : '🎯 Participer'}
                </button>
            </div>
            ${isCompleted ? '<div class="challenge-completed">🎉</div>' : ''}
        `;

        return element;
    }

    updateRewardsSummary() {
        const summaryContainer = document.getElementById('rewards-summary');
        if (!summaryContainer) return;

        const completedChallenges = this.activeChallenges.filter(c => c && c.isCompleted);
        const totalXP = completedChallenges.reduce((sum, c) => sum + (c.reward && c.reward.xp ? c.reward.xp : 0), 0);
        const totalCoins = completedChallenges.reduce((sum, c) => sum + (c.reward && c.reward.coins ? c.reward.coins : 0), 0);
        const badges = completedChallenges.map(c => c.reward && c.reward.badge ? c.reward.badge : '').filter(Boolean);

        summaryContainer.innerHTML = `
            <div class="reward-item">
                <span>Total XP gagné:</span>
                <span class="reward-value">${totalXP} XP</span>
            </div>
            <div class="reward-item">
                <span>Total Coins gagnés:</span>
                <span class="reward-value">${totalCoins} Coins</span>
            </div>
            <div class="reward-item">
                <span>Badges débloqués:</span>
                <span class="reward-value">${badges.length} badges</span>
            </div>
            ${badges.length > 0 ? `
                <div class="reward-item">
                    <span>Badges:</span>
                    <span class="reward-value">${badges.join(', ')}</span>
                </div>
            ` : ''}
        `;
    }

    startTimer() {
        const timerElement = document.getElementById('challenges-timer');
        if (!timerElement) return;

        const updateTimer = () => {
            const now = new Date();
            const tomorrow = new Date(now);
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(0, 0, 0, 0);

            const timeLeft = tomorrow - now;
            const hours = Math.floor(timeLeft / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            timerElement.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

            if (timeLeft <= 0) {
                this.resetDailyChallenges();
            }
        };

        updateTimer();
        setInterval(updateTimer, 1000);
    }

    resetDailyChallenges() {
        // console.log('🔄 Réinitialisation des défis quotidiens');
        this.completedToday.clear();
        this.userProgress.clear();
        this.generateDailyChallenges();
        this.renderChallenges();
        this.saveUserProgress();
    }

    claimReward(challengeId) {
        const challenge = this.challenges.get(challengeId);
        if (!challenge || challenge.isCompleted) return;

        // Vérifier si le défi est complété
        if (challenge.progress >= challenge.target) {
            challenge.isCompleted = true;
            this.completedToday.add(challengeId);

            // Donner les récompenses
            this.giveReward(challenge.reward);

            // Mettre à jour l'affichage
            this.renderChallenges();
            this.saveUserProgress();

            // Célébrer
            this.celebrateCompletion(challenge);
        } else {
            this.showProgressMessage(challenge);
        }
    }

    giveReward(reward) {
        if (!reward || typeof reward !== 'object') return;
        let profile = {};
        try {
            profile = JSON.parse(localStorage.getItem('arkalia_profile') || '{}');
        } catch (e) {
            profile = {};
        }
        profile.xp = (profile.xp || 0) + (reward.xp || 0);
        profile.coins = (profile.coins || 0) + (reward.coins || 0);
        profile.badges = Array.isArray(profile.badges) ? profile.badges : [];
        const badge = reward.badge;
        if (badge && !profile.badges.includes(badge)) {
            profile.badges.push(badge);
        }

        localStorage.setItem('arkalia_profile', JSON.stringify(profile));

        // Afficher la notification
        this.showRewardNotification(reward);
    }

    showRewardNotification(reward) {
        if (!reward || typeof reward !== 'object') return;
        const notification = document.createElement('div');
        notification.className = 'reward-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #00ff00, #00cc00);
            color: #000;
            padding: 15px 20px;
            border-radius: 8px;
            font-weight: bold;
            z-index: 10000;
            animation: slideInRight 0.5s ease-out;
        `;
        notification.innerHTML = `
            <div>🎉 Défi complété !</div>
            <div>+${reward.xp ?? 0} XP • +${reward.coins ?? 0} Coins</div>
            <div>🏆 ${(reward.badge || '').replace(/</g, '&lt;')}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.5s ease-in';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }

    celebrateCompletion(challenge) {
        // Effet de célébration
        const element = document.getElementById(`challenge-${challenge.id}`);
        if (element) {
            element.classList.add('completed');

            // Confetti
            for (let i = 0; i < 10; i++) {
                const confetti = document.createElement('div');
                confetti.style.cssText = `
                    position: absolute;
                    width: 6px;
                    height: 6px;
                    background: #00ff00;
                    top: 50%;
                    left: 50%;
                    animation: confetti-fall 2s ease-out forwards;
                `;
                confetti.style.left = (50 + (Math.random() - 0.5) * 100) + '%';
                confetti.style.top = '50%';
                element.appendChild(confetti);

                setTimeout(() => confetti.remove(), 2000);
            }
        }
    }

    showProgressMessage(challenge) {
        const message = `Progression: ${challenge.progress}/${challenge.target} (${Math.round((challenge.progress / challenge.target) * 100)}%)`;

        // Afficher dans le terminal si disponible
        const terminal = document.querySelector('.terminal-output, .luna-response');
        if (terminal) {
            const progressMsg = document.createElement('div');
            progressMsg.className = 'luna-message progress';
            progressMsg.innerHTML = `🎯 LUNA: ${message}`;
            terminal.appendChild(progressMsg);
        }
    }

    // Méthodes pour mettre à jour la progression
    updateProgress(condition, amount = 1) {
        this.activeChallenges.forEach(challenge => {
            if (challenge.condition === condition && !challenge.isCompleted) {
                challenge.progress = Math.min(challenge.progress + amount, challenge.target);
                this.userProgress.set(challenge.id, challenge.progress);

                // Mettre à jour l'affichage
                this.renderChallenges();
                this.saveUserProgress();
            }
        });
    }

    setupEventListeners() {
        // Écouter les événements de jeu
        document.addEventListener('arkalia_mission_completed', () => {
            this.updateProgress('complete_3_missions_fast', 1);
        });

        document.addEventListener('arkalia_code_game_solved', () => {
            this.updateProgress('solve_2_code_games', 1);
        });

        document.addEventListener('arkalia_social_command_used', () => {
            this.updateProgress('use_5_social_commands', 1);
        });

        document.addEventListener('arkalia_zone_discovered', () => {
            this.updateProgress('discover_3_zones', 1);
        });

        document.addEventListener('arkalia_hack_command_used', () => {
            this.updateProgress('use_10_hack_commands', 1);
        });
    }
}

// Initialiser le système de défis quotidiens
window.dailyChallengesEnhanced = new DailyChallengesEnhanced();
window.dailyChallenges = window.dailyChallengesEnhanced;

/** Fonction globale pour onclick="showDailyChallenges()" (gameplay_enhancements.html) */
window.showDailyChallenges = function () {
    if (window.dailyChallenges && typeof window.dailyChallenges.show === 'function') {
        window.dailyChallenges.show();
    }
};
