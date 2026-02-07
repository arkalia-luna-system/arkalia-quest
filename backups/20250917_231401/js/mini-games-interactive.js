/**
 * Système de mini-jeux vraiment interactifs
 * Remplace les "Chargement..." par de vrais jeux jouables
 */

class MiniGamesInteractive {
    constructor() {
        this.activeGames = new Map();
        this.gameScores = new Map();
        this.gameHistory = [];

        this.initializeSystem();
    }

    initializeSystem() {
        // console.log('🎮 Système de mini-jeux interactifs initialisé');
        this.createGameStyles();
        this.setupGameInterceptors();
        this.initializeGameLibrary();
    }

    createGameStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .mini-game-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: 'Courier New', monospace;
            }
            
            .mini-game-window {
                background: linear-gradient(135deg, #001100, #003300);
                border: 2px solid rgba(0, 255, 0, 0.6);
                border-radius: 12px;
                padding: 20px;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
                position: relative;
            }
            
            .game-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(0, 255, 0, 0.6);
            }
            
            .game-title {
                color: rgba(0, 255, 0, 0.9);
                font-size: 20px;
                font-weight: bold;
                margin: 0;
            }
            
            .game-close {
                background: #ff4444;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
            }
            
            .game-close:hover {
                background: #ff6666;
            }
            
            .game-content {
                color: rgba(0, 255, 0, 0.9);
                margin-bottom: 20px;
            }
            
            .game-description {
                margin-bottom: 15px;
                color: #cccccc;
            }
            
            .game-area {
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid rgba(0, 255, 0, 0.6);
                border-radius: 8px;
                padding: 20px;
                margin: 15px 0;
                min-height: 200px;
            }
            
            .game-controls {
                display: flex;
                gap: 10px;
                margin: 15px 0;
                flex-wrap: wrap;
            }
            
            .game-button {
                background: linear-gradient(45deg, rgba(0, 255, 0, 0.8), rgba(0, 204, 0, 0.8));
                color: #000;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            
            .game-button:hover {
                background: #00cc00;
                transform: scale(1.05);
            }
            
            .game-button:disabled {
                background: #666;
                cursor: not-allowed;
                transform: none;
            }
            
            .game-feedback {
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid rgba(0, 255, 0, 0.6);
                border-radius: 6px;
                padding: 10px;
                margin: 10px 0;
                min-height: 40px;
                display: flex;
                align-items: center;
            }
            
            .game-score {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid rgba(0, 255, 0, 0.6);
                border-radius: 6px;
                padding: 10px;
                margin: 10px 0;
            }
            
            .score-item {
                text-align: center;
            }
            
            .score-value {
                font-size: 18px;
                font-weight: bold;
                color: rgba(0, 255, 0, 0.9);
            }
            
            .score-label {
                font-size: 12px;
                color: #cccccc;
            }
            
            .game-progress {
                margin: 15px 0;
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
                background: linear-gradient(90deg, rgba(0, 255, 0, 0.8), rgba(0, 204, 0, 0.8));
                transition: width 0.3s ease;
                border-radius: 4px;
            }
            
            .progress-text {
                text-align: center;
                margin-top: 5px;
                color: rgba(0, 255, 0, 0.9);
                font-size: 14px;
            }
            
            /* Styles spécifiques aux jeux */
            .logic-puzzle-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin: 20px 0;
            }
            
            .logic-puzzle-cell {
                width: 60px;
                height: 60px;
                background: rgba(0, 255, 0, 0.1);
                border: 2px solid rgba(0, 255, 0, 0.6);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 24px;
                transition: all 0.3s ease;
            }
            
            .logic-puzzle-cell:hover {
                background: rgba(0, 255, 0, 0.2);
                transform: scale(1.05);
            }
            
            .logic-puzzle-cell.selected {
                background: linear-gradient(45deg, rgba(0, 255, 0, 0.8), rgba(0, 204, 0, 0.8));
                color: #000;
            }
            
            .code-debug-editor {
                background: #000;
                border: 1px solid rgba(0, 255, 0, 0.6);
                border-radius: 6px;
                padding: 15px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: rgba(0, 255, 0, 0.9);
                min-height: 200px;
                white-space: pre-wrap;
            }
            
            .code-line {
                margin: 5px 0;
                padding: 2px 5px;
                border-radius: 3px;
            }
            
            .code-line.error {
                background: rgba(255, 0, 0, 0.2);
                border-left: 3px solid #ff0000;
            }
            
            .code-line.correct {
                background: rgba(0, 255, 0, 0.2);
                border-left: 3px solid #00ff00;
            }
            
            .cyber-security-interface {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }
            
            .security-panel {
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid rgba(0, 255, 0, 0.6);
                border-radius: 8px;
                padding: 15px;
            }
            
            .security-threat {
                background: rgba(255, 0, 0, 0.2);
                border: 1px solid #ff0000;
                border-radius: 6px;
                padding: 10px;
                margin: 10px 0;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .security-threat:hover {
                background: rgba(255, 0, 0, 0.3);
                transform: scale(1.02);
            }
            
            .security-threat.eliminated {
                background: rgba(0, 255, 0, 0.2);
                border-color: #00ff00;
                opacity: 0.5;
            }
            
            .memory-game-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
                margin: 20px 0;
            }
            
            .memory-card {
                width: 80px;
                height: 80px;
                background: rgba(0, 255, 0, 0.1);
                border: 2px solid rgba(0, 255, 0, 0.6);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 24px;
                transition: all 0.3s ease;
            }
            
            .memory-card:hover {
                background: rgba(0, 255, 0, 0.2);
                transform: scale(1.05);
            }
            
            .memory-card.flipped {
                background: linear-gradient(45deg, rgba(0, 255, 0, 0.8), rgba(0, 204, 0, 0.8));
                color: #000;
            }
            
            .memory-card.matched {
                background: #00cc00;
                color: #000;
                opacity: 0.7;
            }
        `;
        document.head.appendChild(style);
    }

    setupGameInterceptors() {
        // Intercepter les clics sur les boutons de mini-jeux
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('mini-game-btn') || e.target.dataset.game) {
                e.preventDefault();
                const gameId = e.target.dataset.game || e.target.textContent.trim();
                this.startGame(gameId);
            }
        });

        // Intercepter les commandes de jeu
        document.addEventListener('arkalia_game_command', (e) => {
            const { gameId, action } = e.detail;
            this.handleGameCommand(gameId, action);
        });
    }

    initializeGameLibrary() {
        this.gameLibrary = {
            'logic_puzzle_1': new LogicPuzzle1(),
            'code_debug_1': new CodeDebug1(),
            'cyber_security_1': new CyberSecurity1(),
            'hacking_challenge_1': new HackingChallenge1(),
            'memory_game_1': new MemoryGame1(),
            'simple_hack': new SimpleHackGame(),
            'sequence_game': new SequenceGame(),
            'typing_challenge': new TypingChallenge()
        };
    }

    startGame(gameId) {
        const game = this.gameLibrary[gameId];
        if (!game) {
            console.warn(`Jeu non trouvé: ${gameId}`);
            return;
        }

        // Créer la fenêtre de jeu
        const container = document.createElement('div');
        container.className = 'mini-game-container';
        container.id = `game-${gameId}`;

        container.innerHTML = `
            <div class="mini-game-window">
                <div class="game-header">
                    <h3 class="game-title">${game.title}</h3>
                    <button class="game-close" onclick="window.miniGamesInteractive.closeGame('${gameId}')">✕</button>
                </div>
                <div class="game-content">
                    <div class="game-description">${game.description}</div>
                    <div class="game-area" id="game-area-${gameId}"></div>
                    <div class="game-controls">
                        <button class="game-button" onclick="window.miniGamesInteractive.restartGame('${gameId}')">🔄 Recommencer</button>
                        <button class="game-button" onclick="window.miniGamesInteractive.getHint('${gameId}')">💡 Indice</button>
                    </div>
                    <div class="game-feedback" id="game-feedback-${gameId}"></div>
                    <div class="game-score">
                        <div class="score-item">
                            <div class="score-value" id="score-${gameId}">0</div>
                            <div class="score-label">Score</div>
                        </div>
                        <div class="score-item">
                            <div class="score-value" id="level-${gameId}">1</div>
                            <div class="score-label">Niveau</div>
                        </div>
                        <div class="score-item">
                            <div class="score-value" id="time-${gameId}">60</div>
                            <div class="score-label">Temps</div>
                        </div>
                    </div>
                    <div class="game-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" id="progress-${gameId}" style="width: 0%"></div>
                        </div>
                        <div class="progress-text" id="progress-text-${gameId}">0% complété</div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(container);

        // Initialiser le jeu
        game.init(container);
        this.activeGames.set(gameId, { game, container });

        // Démarrer le timer
        this.startGameTimer(gameId);
    }

    closeGame(gameId) {
        const activeGame = this.activeGames.get(gameId);
        if (activeGame) {
            activeGame.container.remove();
            this.activeGames.delete(gameId);
        }
    }

    restartGame(gameId) {
        const activeGame = this.activeGames.get(gameId);
        if (activeGame) {
            activeGame.game.restart();
            this.updateGameDisplay(gameId);
        }
    }

    getHint(gameId) {
        const activeGame = this.activeGames.get(gameId);
        if (activeGame) {
            const hint = activeGame.game.getHint();
            this.showGameFeedback(gameId, hint);
        }
    }

    startGameTimer(gameId) {
        const activeGame = this.activeGames.get(gameId);
        if (!activeGame) return;

        let timeLeft = 60;
        const timerElement = document.getElementById(`time-${gameId}`);

        const timer = setInterval(() => {
            timeLeft--;
            if (timerElement) {
                timerElement.textContent = timeLeft;
            }

            if (timeLeft <= 0) {
                clearInterval(timer);
                this.endGame(gameId, 'timeout');
            }
        }, 1000);

        activeGame.timer = timer;
    }

    endGame(gameId, reason) {
        const activeGame = this.activeGames.get(gameId);
        if (!activeGame) return;

        if (activeGame.timer) {
            clearInterval(activeGame.timer);
        }

        const score = activeGame.game.getScore();
        this.gameScores.set(gameId, score);

        let message = '';
        if (reason === 'timeout') {
            message = '⏰ Temps écoulé !';
        } else if (reason === 'completed') {
            message = '🎉 Niveau complété !';
        } else {
            message = '🎮 Jeu terminé !';
        }

        this.showGameFeedback(gameId, message);

        // Enregistrer dans l'historique
        this.gameHistory.push({
            gameId,
            score,
            timestamp: Date.now(),
            reason
        });

        // Mettre à jour le profil utilisateur
        this.updateUserProfile(gameId, score);
    }

    updateUserProfile(gameId, score) {
        const profile = JSON.parse(localStorage.getItem('arkalia_profile') || '{}');

        if (!profile.mini_games) {
            profile.mini_games = {};
        }

        if (!profile.mini_games[gameId]) {
            profile.mini_games[gameId] = { bestScore: 0, totalGames: 0, totalScore: 0 };
        }

        profile.mini_games[gameId].totalGames++;
        profile.mini_games[gameId].totalScore += score;
        profile.mini_games[gameId].bestScore = Math.max(profile.mini_games[gameId].bestScore, score);

        // Ajouter de l'XP
        profile.xp = (profile.xp || 0) + Math.floor(score / 10);

        localStorage.setItem('arkalia_profile', JSON.stringify(profile));

        // Déclencher l'événement de mise à jour
        document.dispatchEvent(new CustomEvent('arkalia_profile_updated', { detail: profile }));
    }

    updateGameDisplay(gameId) {
        const activeGame = this.activeGames.get(gameId);
        if (!activeGame) return;

        const score = activeGame.game.getScore();
        const level = activeGame.game.getLevel();
        const progress = activeGame.game.getProgress();

        const scoreElement = document.getElementById(`score-${gameId}`);
        const levelElement = document.getElementById(`level-${gameId}`);
        const progressElement = document.getElementById(`progress-${gameId}`);
        const progressTextElement = document.getElementById(`progress-text-${gameId}`);

        if (scoreElement) scoreElement.textContent = score;
        if (levelElement) levelElement.textContent = level;
        if (progressElement) progressElement.style.width = progress + '%';
        if (progressTextElement) progressTextElement.textContent = progress + '% complété';
    }

    showGameFeedback(gameId, message) {
        const feedbackElement = document.getElementById(`game-feedback-${gameId}`);
        if (feedbackElement) {
            feedbackElement.textContent = message;
            feedbackElement.style.animation = 'fadeIn 0.5s ease-in';
        }
    }

    handleGameCommand(gameId, action) {
        const activeGame = this.activeGames.get(gameId);
        if (activeGame) {
            activeGame.game.handleCommand(action);
            this.updateGameDisplay(gameId);
        }
    }
}

// Classes de jeux individuels
class LogicPuzzle1 {
    constructor() {
        this.title = '🧩 Puzzle Logique';
        this.description = 'Trouve la séquence correcte en cliquant sur les cases !';
        this.score = 0;
        this.level = 1;
        this.sequence = [];
        this.userSequence = [];
        this.isPlaying = false;
    }

    init(container) {
        this.generateSequence();
        this.render(container);
        this.isPlaying = true;
    }

    generateSequence() {
        this.sequence = [];
        for (let i = 0; i < 3 + this.level; i++) {
            this.sequence.push(Math.floor(Math.random() * 9));
        }
    }

    render(container) {
        const gameArea = container.querySelector('.game-area');
        gameArea.innerHTML = `
            <div class="logic-puzzle-grid" id="puzzle-grid">
                ${Array.from({ length: 9 }, (_, i) =>
            `<div class="logic-puzzle-cell" data-index="${i}" onclick="window.miniGamesInteractive.handleCellClick('logic_puzzle_1', ${i})">${i + 1}</div>`
        ).join('')}
            </div>
        `;
    }

    handleCellClick(index) {
        if (!this.isPlaying) return;

        this.userSequence.push(index);

        // Vérifier si la séquence est correcte
        if (this.userSequence.length === this.sequence.length) {
            if (this.userSequence.every((val, i) => val === this.sequence[i])) {
                this.score += 100 * this.level;
                this.level++;
                this.userSequence = [];
                this.generateSequence();
                this.render(document.getElementById('game-logic_puzzle_1'));
                this.showFeedback('🎉 Correct ! Niveau suivant !');
            } else {
                this.showFeedback('❌ Incorrect ! Recommence !');
                this.userSequence = [];
            }
        }
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.userSequence.length / this.sequence.length) * 100; }
    getHint() { return `Séquence de ${this.sequence.length} nombres. Commence par ${this.sequence[0] + 1} !`; }
    restart() { this.score = 0; this.level = 1; this.userSequence = []; this.generateSequence(); }
    showFeedback(message) { // console.log(message); }
}

class CodeDebug1 {
    constructor() {
        this.title = '🐛 Debug de Code';
        this.description = 'Trouve et corrige les erreurs dans le code !';
        this.score = 0;
        this.level = 1;
        this.code = '';
        this.errors = [];
        this.fixedErrors = 0;
    }

    init(container) {
        this.generateCode();
        this.render(container);
    }

    generateCode() {
        this.code = `function calculateSum(a, b) {
    // Erreur: manque return
    a + b;
}

function checkEven(number) {
    // Erreur: mauvais opérateur
    return number % 2 = 0;
}

function greet(name) {
    // Erreur: guillemets manquants
    return Hello + name;
}`;

        this.errors = [
            { line: 2, type: 'missing_return', message: 'Manque return' },
            { line: 6, type: 'wrong_operator', message: 'Utilise == au lieu de =' },
            { line: 10, type: 'missing_quotes', message: 'Ajoute des guillemets' }
        ];
    }

    render(container) {
        const gameArea = container.querySelector('.game-area');
        gameArea.innerHTML = `
            <div class="code-debug-editor" id="code-editor">
                ${this.code.split('\n').map((line, i) =>
            `<div class="code-line" data-line="${i}">${line}</div>`
        ).join('')}
            </div>
            <div class="game-controls">
                <button class="game-button" onclick="window.miniGamesInteractive.fixCode('code_debug_1')">🔧 Corriger</button>
            </div>
        `;
    }

    fixCode() {
        // Logique de correction simplifiée
        this.fixedErrors++;
        this.score += 50;
        this.showFeedback(`Erreur corrigée ! (+50 points)`);

        if (this.fixedErrors >= this.errors.length) {
            this.showFeedback('🎉 Toutes les erreurs corrigées !');
        }
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.fixedErrors / this.errors.length) * 100; }
    getHint() { return `Regarde la ligne ${this.errors[this.fixedErrors]?.line || 1} !`; }
    restart() { this.score = 0; this.fixedErrors = 0; this.generateCode(); }
    showFeedback(message) { // console.log(message); }
}

class CyberSecurity1 {
    constructor() {
        this.title = '🛡️ Cybersécurité';
        this.description = 'Élimine les menaces de sécurité !';
        this.score = 0;
        this.level = 1;
        this.threats = [];
        this.eliminatedThreats = 0;
    }

    init(container) {
        this.generateThreats();
        this.render(container);
    }

    generateThreats() {
        this.threats = [
            { id: 1, name: 'Virus Trojan', type: 'malware', severity: 'high' },
            { id: 2, name: 'Phishing Email', type: 'social', severity: 'medium' },
            { id: 3, name: 'SQL Injection', type: 'injection', severity: 'high' },
            { id: 4, name: 'Brute Force', type: 'attack', severity: 'low' }
        ];
    }

    render(container) {
        const gameArea = container.querySelector('.game-area');
        gameArea.innerHTML = `
            <div class="cyber-security-interface">
                <div class="security-panel">
                    <h4>Menaces détectées</h4>
                    ${this.threats.map(threat =>
            `<div class="security-threat" data-threat="${threat.id}" onclick="window.miniGamesInteractive.eliminateThreat('cyber_security_1', ${threat.id})">
                            ${threat.name} (${threat.severity})
                        </div>`
        ).join('')}
                </div>
                <div class="security-panel">
                    <h4>Actions disponibles</h4>
                    <button class="game-button" onclick="window.miniGamesInteractive.scanSystem('cyber_security_1')">🔍 Scanner</button>
                    <button class="game-button" onclick="window.miniGamesInteractive.quarantine('cyber_security_1')">🚫 Quarantaine</button>
                </div>
            </div>
        `;
    }

    eliminateThreat(threatId) {
        const threat = this.threats.find(t => t.id === threatId);
        if (threat && !threat.eliminated) {
            threat.eliminated = true;
            this.eliminatedThreats++;
            this.score += 100;
            this.showFeedback(`Menace ${threat.name} éliminée ! (+100 points)`);

            if (this.eliminatedThreats >= this.threats.length) {
                this.showFeedback('🎉 Toutes les menaces éliminées !');
            }
        }
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.eliminatedThreats / this.threats.length) * 100; }
    getHint() { return 'Clique sur les menaces pour les éliminer !'; }
    restart() { this.score = 0; this.eliminatedThreats = 0; this.generateThreats(); }
    showFeedback(message) { // console.log(message); }
}

class HackingChallenge1 {
    constructor() {
        this.title = '🔐 Défi de Hacking';
        this.description = 'Percer les défenses du système !';
        this.score = 0;
        this.level = 1;
        this.defenses = [];
        this.breachedDefenses = 0;
    }

    init(container) {
        this.generateDefenses();
        this.render(container);
    }

    generateDefenses() {
        this.defenses = [
            { id: 1, name: 'Firewall', strength: 80, type: 'network' },
            { id: 2, name: 'Antivirus', strength: 60, type: 'software' },
            { id: 3, name: 'Encryption', strength: 90, type: 'data' }
        ];
    }

    render(container) {
        const gameArea = container.querySelector('.game-area');
        gameArea.innerHTML = `
            <div class="cyber-security-interface">
                <div class="security-panel">
                    <h4>Défenses du système</h4>
                    ${this.defenses.map(defense =>
            `<div class="security-threat" data-defense="${defense.id}" onclick="window.miniGamesInteractive.breachDefense('hacking_challenge_1', ${defense.id})">
                            ${defense.name} (Force: ${defense.strength}%)
                        </div>`
        ).join('')}
                </div>
                <div class="security-panel">
                    <h4>Outils de hacking</h4>
                    <button class="game-button" onclick="window.miniGamesInteractive.useTool('hacking_challenge_1', 'exploit')">💥 Exploit</button>
                    <button class="game-button" onclick="window.miniGamesInteractive.useTool('hacking_challenge_1', 'bruteforce')">🔨 Brute Force</button>
                </div>
            </div>
        `;
    }

    breachDefense(defenseId) {
        const defense = this.defenses.find(d => d.id === defenseId);
        if (defense && !defense.breached) {
            defense.breached = true;
            this.breachedDefenses++;
            this.score += defense.strength;
            this.showFeedback(`Défense ${defense.name} percée ! (+${defense.strength} points)`);

            if (this.breachedDefenses >= this.defenses.length) {
                this.showFeedback('🎉 Système compromis ! Mission accomplie !');
            }
        }
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.breachedDefenses / this.defenses.length) * 100; }
    getHint() { return 'Commence par la défense la plus faible !'; }
    restart() { this.score = 0; this.breachedDefenses = 0; this.generateDefenses(); }
    showFeedback(message) { // console.log(message); }
}

class MemoryGame1 {
    constructor() {
        this.title = '🧠 Jeu de Mémoire';
        this.description = 'Retrouve les paires de cartes !';
        this.score = 0;
        this.level = 1;
        this.cards = [];
        this.flippedCards = [];
        this.matchedPairs = 0;
    }

    init(container) {
        this.generateCards();
        this.render(container);
    }

    generateCards() {
        const symbols = ['🌟', '🚀', '💎', '🎯', '⚡', '🔮', '🎮', '🎪'];
        this.cards = [];

        for (let i = 0; i < 8; i++) {
            this.cards.push({ id: i, symbol: symbols[i], matched: false });
            this.cards.push({ id: i + 8, symbol: symbols[i], matched: false });
        }

        // Mélanger les cartes
        this.cards = this.cards.sort(() => Math.random() - 0.5);
    }

    render(container) {
        const gameArea = container.querySelector('.game-area');
        gameArea.innerHTML = `
            <div class="memory-game-grid">
                ${this.cards.map((card, index) =>
            `<div class="memory-card" data-index="${index}" onclick="window.miniGamesInteractive.flipCard('memory_game_1', ${index})">
                        ${card.matched ? card.symbol : '?'}
                    </div>`
        ).join('')}
            </div>
        `;
    }

    flipCard(cardIndex) {
        if (this.flippedCards.length >= 2) return;

        const card = this.cards[cardIndex];
        if (card.matched || this.flippedCards.includes(cardIndex)) return;

        this.flippedCards.push(cardIndex);
        this.updateDisplay();

        if (this.flippedCards.length === 2) {
            setTimeout(() => this.checkMatch(), 1000);
        }
    }

    checkMatch() {
        const [index1, index2] = this.flippedCards;
        const card1 = this.cards[index1];
        const card2 = this.cards[index2];

        if (card1.symbol === card2.symbol) {
            card1.matched = true;
            card2.matched = true;
            this.matchedPairs++;
            this.score += 100;
            this.showFeedback('🎉 Paire trouvée ! (+100 points)');

            if (this.matchedPairs >= 8) {
                this.showFeedback('🎊 Toutes les paires trouvées !');
            }
        } else {
            this.showFeedback('❌ Pas de paire, essaie encore !');
        }

        this.flippedCards = [];
        this.updateDisplay();
    }

    updateDisplay() {
        const cards = document.querySelectorAll('.memory-card');
        cards.forEach((card, index) => {
            const cardData = this.cards[index];
            if (cardData.matched) {
                card.classList.add('matched');
                card.textContent = cardData.symbol;
            } else if (this.flippedCards.includes(index)) {
                card.classList.add('flipped');
                card.textContent = cardData.symbol;
            } else {
                card.classList.remove('flipped');
                card.textContent = '?';
            }
        });
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.matchedPairs / 8) * 100; }
    getHint() { return 'Concentre-toi sur la position des cartes !'; }
    restart() { this.score = 0; this.matchedPairs = 0; this.flippedCards = []; this.generateCards(); }
    showFeedback(message) { // console.log(message); }
}

// Jeu de hack simple
class SimpleHackGame {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.targetCode = '';
        this.userInput = '';
        this.timeLeft = 30;
        this.isActive = false;
    }

    start() {
        this.isActive = true;
        this.generateTargetCode();
        this.timeLeft = 30;
        this.userInput = '';
        this.score = 0;
        this.startTimer();
    }

    generateTargetCode() {
        const patterns = [
            '01010101',
            '11001100',
            '10101010',
            '11110000',
            '00001111',
            '10110110',
            '01101101',
            '11010010'
        ];
        this.targetCode = patterns[Math.floor(Math.random() * patterns.length)];
    }

    startTimer() {
        const timer = setInterval(() => {
            if (!this.isActive) {
                clearInterval(timer);
                return;
            }
            this.timeLeft--;
            if (this.timeLeft <= 0) {
                this.endGame();
                clearInterval(timer);
            }
        }, 1000);
    }

    inputDigit(digit) {
        if (!this.isActive) return;
        this.userInput += digit;
        if (this.userInput.length === this.targetCode.length) {
            this.checkCode();
        }
    }

    checkCode() {
        if (this.userInput === this.targetCode) {
            this.score += 100;
            this.level++;
            this.generateTargetCode();
            this.userInput = '';
            this.timeLeft += 10; // Bonus de temps
        } else {
            this.score = Math.max(0, this.score - 50);
            this.userInput = '';
        }
    }

    endGame() {
        this.isActive = false;
        this.showFeedback(`Hack terminé ! Score: ${this.score}`);
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.userInput.length / this.targetCode.length) * 100; }
    getHint() { return `Code cible: ${this.targetCode}`; }
    restart() { this.start(); }
    showFeedback(message) { // console.log(message); }
}

// Jeu de séquence
class SequenceGame {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.sequence = [];
        this.userSequence = [];
        this.isShowing = false;
        this.isActive = false;
    }

    start() {
        this.isActive = true;
        this.score = 0;
        this.level = 1;
        this.generateSequence();
        this.showSequence();
    }

    generateSequence() {
        this.sequence = [];
        for (let i = 0; i < this.level + 2; i++) {
            this.sequence.push(Math.floor(Math.random() * 4) + 1);
        }
    }

    showSequence() {
        this.isShowing = true;
        let index = 0;
        const showNext = () => {
            if (index < this.sequence.length) {
                this.highlightButton(this.sequence[index]);
                index++;
                setTimeout(showNext, 800);
            } else {
                this.isShowing = false;
            }
        };
        showNext();
    }

    highlightButton(number) {
        // Simulation de highlight - en réalité, cela devrait interagir avec l'UI
        // console.log(`Bouton ${number} clignote`);
    }

    inputButton(number) {
        if (!this.isActive || this.isShowing) return;

        this.userSequence.push(number);

        if (this.userSequence.length === this.sequence.length) {
            this.checkSequence();
        }
    }

    checkSequence() {
        const isCorrect = this.userSequence.every((val, index) => val === this.sequence[index]);

        if (isCorrect) {
            this.score += this.level * 50;
            this.level++;
            this.userSequence = [];
            this.generateSequence();
            setTimeout(() => this.showSequence(), 1000);
        } else {
            this.endGame();
        }
    }

    endGame() {
        this.isActive = false;
        this.showFeedback(`Séquence terminée ! Score: ${this.score}`);
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.userSequence.length / this.sequence.length) * 100; }
    getHint() { return 'Mémorise la séquence et reproduis-la !'; }
    restart() { this.start(); }
    showFeedback(message) { // console.log(message); }
}

// Défi de frappe
class TypingChallenge {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.targetText = '';
        this.userText = '';
        this.timeLeft = 60;
        this.isActive = false;
        this.wpm = 0;
    }

    start() {
        this.isActive = true;
        this.generateTargetText();
        this.userText = '';
        this.score = 0;
        this.timeLeft = 60;
        this.startTimer();
    }

    generateTargetText() {
        const texts = [
            'hack the system',
            'cyber security',
            'digital world',
            'code is power',
            'matrix protocol',
            'neural network',
            'quantum encryption',
            'binary revolution'
        ];
        this.targetText = texts[Math.floor(Math.random() * texts.length)];
    }

    startTimer() {
        const timer = setInterval(() => {
            if (!this.isActive) {
                clearInterval(timer);
                return;
            }
            this.timeLeft--;
            if (this.timeLeft <= 0) {
                this.endGame();
                clearInterval(timer);
            }
        }, 1000);
    }

    inputText(text) {
        if (!this.isActive) return;
        this.userText = text;
        this.calculateWPM();

        if (this.userText === this.targetText) {
            this.completeText();
        }
    }

    calculateWPM() {
        const words = this.userText.split(' ').length;
        const timeElapsed = (60 - this.timeLeft) / 60;
        this.wpm = Math.round(words / timeElapsed);
    }

    completeText() {
        this.score += this.wpm * 10;
        this.level++;
        this.generateTargetText();
        this.userText = '';
        this.timeLeft += 15; // Bonus de temps
    }

    endGame() {
        this.isActive = false;
        this.showFeedback(`Défi terminé ! Score: ${this.score}, WPM: ${this.wpm}`);
    }

    getScore() { return this.score; }
    getLevel() { return this.level; }
    getProgress() { return (this.userText.length / this.targetText.length) * 100; }
    getHint() { return `Tape: "${this.targetText}"`; }
    restart() { this.start(); }
    showFeedback(message) { // console.log(message); }
}

// Initialiser le système de mini-jeux interactifs
window.miniGamesInteractive = new MiniGamesInteractive();
