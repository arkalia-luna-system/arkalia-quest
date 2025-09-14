/* ===== ARKALIA QUEST - GAME ENGINE ===== */

class GameEngine {
    constructor() {
        this.player = {
            level: 1,
            xp: 0,
            xpToNext: 100,
            score: 0,
            badges: [],
            missions: [],
            completedMissions: [],
            currentMission: null,
            stats: {
                gamesPlayed: 0,
                gamesWon: 0,
                totalScore: 0,
                timePlayed: 0
            }
        };

        this.gameState = {
            currentAct: 'prologue',
            unlockedZones: ['terminal'],
            availableGames: ['logic_puzzle_1'],
            dailyChallenges: [],
            lunaPersonality: 'friendly'
        };

        this.init();
    }

    init() {
        this.loadGameData();
        this.setupEventListeners();
        this.updateUI();
        this.startGameLoop();
    }

    loadGameData() {
        const saved = localStorage.getItem('arkaliaGameData');
        if (saved) {
            const data = JSON.parse(saved);
            this.player = { ...this.player, ...data.player };
            this.gameState = { ...this.gameState, ...data.gameState };
        }
    }

    saveGameData() {
        const data = {
            player: this.player,
            gameState: this.gameState,
            timestamp: Date.now()
        };
        localStorage.setItem('arkaliaGameData', JSON.stringify(data));
    }

    setupEventListeners() {
        // Écouter les commandes du terminal
        document.addEventListener('terminalCommand', (e) => {
            this.handleCommand(e.detail.command, e.detail.args);
        });
    }

    startGameLoop() {
        // Boucle de jeu principale
        setInterval(() => {
            this.updateGameState();
        }, 1000);
    }

    updateGameState() {
        this.player.stats.timePlayed++;
        this.saveGameData();
    }

    // GESTION DES COMMANDES
    handleCommand(command, args = []) {
        const commandMap = {
            'aide': () => this.showHelp(),
            'profil': () => this.showProfile(),
            'stats': () => this.showStats(),
            'missions': () => this.showMissions(),
            'badges': () => this.showBadges(),
            'games': () => this.showGames(),
            'play_game': () => this.playGame(args[0]),
            'story': () => this.showStory(),
            'prologue': () => this.startPrologue(),
            'acte_1': () => this.startAct1(),
            'luna': () => this.talkToLuna(args.join(' ')),
            'luna_dance': () => this.lunaDance(),
            'luna_help': () => this.lunaHelp(),
            'luna_status': () => this.lunaStatus(),
            'daily_challenges': () => this.showDailyChallenges(),
            'leaderboard': () => this.showLeaderboard(),
            'monde': () => this.showWorld(),
            'explorer': () => this.exploreZone(args[0])
        };

        if (commandMap[command]) {
            try {
                commandMap[command]();
                this.showSuccess(`Commande "${command}" exécutée avec succès !`);
            } catch (error) {
                this.showError(`Erreur lors de l'exécution de "${command}": ${error.message}`);
            }
        } else {
            this.showError(`Commande "${command}" non reconnue. Tapez "aide" pour voir les commandes disponibles.`);
        }
    }

    // SYSTÈME DE PROGRESSION
    addXP(amount, source = 'action') {
        this.player.xp += amount;
        this.player.score += amount;
        this.player.stats.totalScore += amount;

        // Vérifier le niveau
        if (this.player.xp >= this.player.xpToNext) {
            this.levelUp();
        }

        this.updateUI();
        this.showXPNotification(amount, source);
    }

    levelUp() {
        this.player.level++;
        this.player.xp -= this.player.xpToNext;
        this.player.xpToNext = Math.floor(this.player.xpToNext * 1.5);

        this.showLevelUpNotification();
        this.unlockNewContent();
    }

    unlockNewContent() {
        const unlocks = {
            2: { zones: ['cyber-city'], games: ['code_debug_1'] },
            3: { zones: ['data-center'], games: ['security_quiz_1'] },
            5: { zones: ['underground'], games: ['hack_simulator_1'] },
            10: { zones: ['quantum'], games: ['ai_challenge_1'] }
        };

        if (unlocks[this.player.level]) {
            const unlock = unlocks[this.player.level];
            if (unlock.zones) {
                this.gameState.unlockedZones.push(...unlock.zones);
            }
            if (unlock.games) {
                this.gameState.availableGames.push(...unlock.games);
            }
            this.showUnlockNotification(unlock);
        }
    }

    // SYSTÈME DE BADGES
    checkBadges() {
        const newBadges = [];

        // Badge premier niveau
        if (this.player.level >= 2 && !this.player.badges.includes('first_level')) {
            newBadges.push({ id: 'first_level', name: 'Premier Pas', icon: '🌟', description: 'Atteint le niveau 2' });
        }

        // Badge premier jeu
        if (this.player.stats.gamesPlayed >= 1 && !this.player.badges.includes('first_game')) {
            newBadges.push({ id: 'first_game', name: 'Gamer', icon: '🎮', description: 'A joué à son premier jeu' });
        }

        // Badge score élevé
        if (this.player.score >= 1000 && !this.player.badges.includes('high_score')) {
            newBadges.push({ id: 'high_score', name: 'Score Master', icon: '🏆', description: 'Atteint 1000 points' });
        }

        // Ajouter les nouveaux badges
        newBadges.forEach(badge => {
            this.player.badges.push(badge.id);
            this.showBadgeEarned(badge);
        });
    }

    // SYSTÈME DE MINI-JEUX
    playGame(gameId) {
        if (!this.gameState.availableGames.includes(gameId)) {
            this.showError(`Jeu "${gameId}" non disponible. Niveau requis: ${this.getRequiredLevel(gameId)}`);
            return;
        }

        const game = this.getGameData(gameId);
        if (!game) {
            this.showError(`Jeu "${gameId}" non trouvé.`);
            return;
        }

        this.showGameInterface(game);
    }

    getGameData(gameId) {
        const games = {
            'logic_puzzle_1': {
                name: 'Puzzle Logique #1',
                description: 'Résolvez ce puzzle de logique pour gagner des points !',
                type: 'logic',
                difficulty: 1,
                maxScore: 100,
                rules: 'Trouvez la séquence logique manquante.',
                questions: [
                    {
                        question: 'Quel est le prochain nombre dans la séquence : 2, 4, 8, 16, ?',
                        options: ['24', '32', '64', '128'],
                        correct: 1,
                        explanation: 'Chaque nombre est multiplié par 2.'
                    },
                    {
                        question: 'Si A = 1, B = 2, C = 3, alors D = ?',
                        options: ['3', '4', '5', '6'],
                        correct: 1,
                        explanation: 'L\'alphabet suit l\'ordre numérique.'
                    }
                ]
            },
            'code_debug_1': {
                name: 'Debug de Code #1',
                description: 'Trouvez et corrigez les erreurs dans ce code Python !',
                type: 'code',
                difficulty: 2,
                maxScore: 150,
                rules: 'Identifiez les erreurs de syntaxe et de logique.',
                questions: [
                    {
                        question: 'Quelle est l\'erreur dans ce code :\nfor i in range(10)\n    print(i)',
                        options: ['Manque les deux points', 'Indentation incorrecte', 'Range incorrect', 'Print incorrect'],
                        correct: 0,
                        explanation: 'Il manque les deux points après range(10).'
                    }
                ]
            }
        };

        return games[gameId];
    }

    showGameInterface(game) {
        const gameModal = document.createElement('div');
        gameModal.className = 'game-modal';
        gameModal.innerHTML = `
            <div class="game-container">
                <div class="game-header">
                    <h2>${game.name}</h2>
                    <p>${game.description}</p>
                    <div class="game-stats">
                        <span>Score: <span id="game-score">0</span>/${game.maxScore}</span>
                        <span>Question: <span id="game-question">1</span>/${game.questions.length}</span>
                    </div>
                </div>
                <div class="game-content" id="game-content">
                    <!-- Le contenu du jeu sera généré ici -->
                </div>
                <div class="game-controls">
                    <button id="game-start" class="btn-primary">Commencer</button>
                    <button id="game-quit" class="btn-secondary">Quitter</button>
                </div>
            </div>
        `;

        document.body.appendChild(gameModal);
        this.startGameSession(game, gameModal);
    }

    startGameSession(game, modal) {
        let currentQuestion = 0;
        let score = 0;
        let startTime = Date.now();

        const startBtn = modal.querySelector('#game-start');
        const quitBtn = modal.querySelector('#game-quit');
        const content = modal.querySelector('#game-content');

        startBtn.addEventListener('click', () => {
            this.showQuestion(game, currentQuestion, content, (isCorrect) => {
                if (isCorrect) {
                    score += Math.floor(game.maxScore / game.questions.length);
                    this.updateGameScore(modal, score);
                }

                currentQuestion++;
                if (currentQuestion < game.questions.length) {
                    this.showQuestion(game, currentQuestion, content, arguments[0]);
                } else {
                    this.finishGame(game, score, Date.now() - startTime, modal);
                }
            });
        });

        quitBtn.addEventListener('click', () => {
            modal.remove();
        });
    }

    showQuestion(game, questionIndex, container, callback) {
        const question = game.questions[questionIndex];
        container.innerHTML = `
            <div class="question-container">
                <h3>Question ${questionIndex + 1}</h3>
                <p class="question-text">${question.question}</p>
                <div class="options-container">
                    ${question.options.map((option, index) => `
                        <button class="option-btn" data-answer="${index}">${option}</button>
                    `).join('')}
                </div>
            </div>
        `;

        container.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const selectedAnswer = parseInt(e.target.dataset.answer);
                const isCorrect = selectedAnswer === question.correct;

                // Feedback visuel
                e.target.style.background = isCorrect ? '#00ff00' : '#ff0000';
                e.target.style.color = '#000000';

                setTimeout(() => {
                    callback(isCorrect);
                }, 1000);
            });
        });
    }

    finishGame(game, score, timePlayed, modal) {
        this.player.stats.gamesPlayed++;
        if (score > 0) {
            this.player.stats.gamesWon++;
        }

        const xpGained = Math.floor(score / 10);
        this.addXP(xpGained, 'mini-jeu');

        modal.querySelector('.game-content').innerHTML = `
            <div class="game-results">
                <h3>🎉 Jeu Terminé !</h3>
                <div class="results-stats">
                    <div class="stat">
                        <span class="stat-label">Score Final:</span>
                        <span class="stat-value">${score}/${game.maxScore}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Temps:</span>
                        <span class="stat-value">${Math.floor(timePlayed / 1000)}s</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">XP Gagné:</span>
                        <span class="stat-value">+${xpGained}</span>
                    </div>
                </div>
                <div class="results-message">
                    ${score >= game.maxScore * 0.8 ?
                '🌟 Excellent travail ! Vous maîtrisez parfaitement ce jeu !' :
                score >= game.maxScore * 0.6 ?
                    '👍 Bon travail ! Continuez à vous améliorer !' :
                    '💪 Continuez à pratiquer pour améliorer votre score !'
            }
                </div>
            </div>
        `;

        this.checkBadges();
        this.updateUI();
    }

    // SYSTÈME DE NOTIFICATIONS
    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `game-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-icon">${this.getNotificationIcon(type)}</div>
            <div class="notification-message">${message}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'notificationSlideOut 0.3s ease-out forwards';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            info: 'ℹ️',
            warning: '⚠️',
            xp: '⚡',
            level: '🌟',
            badge: '🏆'
        };
        return icons[type] || 'ℹ️';
    }

    showXPNotification(amount, source) {
        this.showNotification(`+${amount} XP (${source})`, 'xp');
    }

    showLevelUpNotification() {
        this.showNotification(`🎉 Niveau ${this.player.level} atteint !`, 'level');
    }

    showBadgeEarned(badge) {
        this.showNotification(`🏆 Badge obtenu: ${badge.name}`, 'badge');
    }

    showUnlockNotification(unlock) {
        let message = '🔓 Nouveau contenu débloqué !';
        if (unlock.zones) {
            message += ` Zones: ${unlock.zones.join(', ')}`;
        }
        if (unlock.games) {
            message += ` Jeux: ${unlock.games.join(', ')}`;
        }
        this.showNotification(message, 'info');
    }

    // MÉTHODES D'AFFICHAGE
    showHelp() {
        const helpText = `
📖 COMMANDES DISPONIBLES:

🎮 JEUX:
- games: Liste des mini-jeux disponibles
- play_game [nom]: Jouer à un mini-jeu

👤 PROFIL:
- profil: Afficher votre profil
- stats: Statistiques détaillées
- badges: Vos badges obtenus

🌍 MONDE:
- monde: Explorer le monde d'Arkalia
- explorer [zone]: Explorer une zone spécifique

🌙 LUNA:
- luna [message]: Parler avec LUNA
- luna_help: Aide de LUNA
- luna_status: État de LUNA
- luna_dance: Faire danser LUNA

📚 HISTOIRE:
- story: Récit principal
- prologue: Commencer le prologue
- acte_1: Commencer l'acte 1

🏆 PROGRESSION:
- missions: Vos missions
- daily_challenges: Défis quotidiens
- leaderboard: Classement

💡 TIP: Plus vous jouez, plus vous débloquez de contenu !
        `;
        this.showTerminalMessage(helpText, 'info');
    }

    showProfile() {
        const profileText = `
👤 PROFIL DU JOUEUR:

🌟 Niveau: ${this.player.level}
⚡ XP: ${this.player.xp}/${this.player.xpToNext}
🏆 Score Total: ${this.player.score}
🎮 Jeux Joués: ${this.player.stats.gamesPlayed}
✅ Jeux Gagnés: ${this.player.stats.gamesWon}
⏱️ Temps de Jeu: ${Math.floor(this.player.stats.timePlayed / 60)} minutes

🏆 BADGES (${this.player.badges.length}):
${this.player.badges.map(badgeId => this.getBadgeInfo(badgeId)).join('\n')}

🌍 ZONES DÉBLOQUÉES:
${this.gameState.unlockedZones.join(', ')}

🎮 JEUX DISPONIBLES:
${this.gameState.availableGames.join(', ')}
        `;
        this.showTerminalMessage(profileText, 'info');
    }

    getBadgeInfo(badgeId) {
        const badges = {
            'first_level': '🌟 Premier Pas - Atteint le niveau 2',
            'first_game': '🎮 Gamer - A joué à son premier jeu',
            'high_score': '🏆 Score Master - Atteint 1000 points'
        };
        return badges[badgeId] || `🏆 ${badgeId}`;
    }

    showTerminalMessage(message, type = 'info') {
        const terminalOutput = document.getElementById('terminal-output');
        if (terminalOutput) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `terminal-message ${type}`;
            messageDiv.innerHTML = message.replace(/\n/g, '<br>');
            terminalOutput.appendChild(messageDiv);
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }
    }

    updateUI() {
        // Mettre à jour l'interface utilisateur
        this.updateProfileDisplay();
        this.updateMissionDisplay();
        this.updateBadgeDisplay();
    }

    updateProfileDisplay() {
        const levelElements = document.querySelectorAll('.player-level, .level-value');
        const xpElements = document.querySelectorAll('.player-xp, .xp-value');
        const scoreElements = document.querySelectorAll('.player-score, .score-value');

        levelElements.forEach(el => el.textContent = this.player.level);
        xpElements.forEach(el => el.textContent = this.player.xp);
        scoreElements.forEach(el => el.textContent = this.player.score);
    }

    // MÉTHODES LUNA
    talkToLuna(message) {
        const responses = [
            `🌙 LUNA: ${message} ? Intéressant ! Continue à explorer pour en savoir plus.`,
            `🌙 LUNA: Ah, ${message} ! J'ai des informations sur ce sujet dans ma base de données.`,
            `🌙 LUNA: ${message}... C'est une question profonde. Laisse-moi réfléchir...`,
            `🌙 LUNA: ${message} ? Tu progresses bien ! Tu es maintenant niveau ${this.player.level}.`,
            `🌙 LUNA: ${message}... Je sens que tu deviens plus fort. Continue comme ça !`
        ];

        const response = responses[Math.floor(Math.random() * responses.length)];
        this.showTerminalMessage(response, 'luna');
    }

    lunaDance() {
        this.showTerminalMessage('🌙 LUNA: *danse avec des particules lumineuses* 💃✨', 'luna');
        this.addXP(10, 'luna_dance');
    }

    lunaHelp() {
        this.showTerminalMessage('🌙 LUNA: Je suis là pour t\'aider ! Pose-moi des questions ou explore le monde d\'Arkalia.', 'luna');
    }

    lunaStatus() {
        this.showTerminalMessage(`🌙 LUNA: Système opérationnel. Niveau: ${this.player.level}, XP: ${this.player.xp}. Tout va bien !`, 'luna');
    }

    // MÉTHODES UTILITAIRES
    getRequiredLevel(gameId) {
        const requirements = {
            'logic_puzzle_1': 1,
            'code_debug_1': 2,
            'security_quiz_1': 3,
            'hack_simulator_1': 5,
            'ai_challenge_1': 10
        };
        return requirements[gameId] || 1;
    }

    updateGameScore(modal, score) {
        const scoreElement = modal.querySelector('#game-score');
        if (scoreElement) {
            scoreElement.textContent = score;
        }
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.gameEngine = new GameEngine();
});

// Export pour utilisation externe
window.GameEngine = GameEngine;
