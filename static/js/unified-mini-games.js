/* ===== ARKALIA QUEST - UNIFIED MINI-GAMES SYSTEM ===== */

class UnifiedMiniGames {
    constructor() {
        this.availableGames = {
            'logic_puzzle_1': {
                name: 'Puzzle Logique #1',
                description: 'Résolvez des puzzles de logique pour gagner des points !',
                type: 'logic',
                difficulty: 1,
                maxScore: 100,
                icon: '🧩',
                color: '#00ff00'
            },
            'code_debug_1': {
                name: 'Debug de Code #1',
                description: 'Trouvez et corrigez les erreurs dans ce code Python !',
                type: 'code',
                difficulty: 2,
                maxScore: 150,
                icon: '🐍',
                color: '#00ffff'
            },
            'security_quiz_1': {
                name: 'Quiz Cybersécurité #1',
                description: 'Testez vos connaissances en sécurité informatique !',
                type: 'security',
                difficulty: 3,
                maxScore: 200,
                icon: '🔒',
                color: '#ff6600'
            },
            'hack_simulator_1': {
                name: 'Simulateur de Hack #1',
                description: 'Simulez des attaques et défenses en cybersécurité !',
                type: 'hacking',
                difficulty: 4,
                maxScore: 250,
                icon: '⚡',
                color: '#ff0066'
            }
        };

        this.gameInstances = new Map();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createGameButtons();
        this.loadGameProgress();
    }

    setupEventListeners() {
        // Écouter les événements de jeu
        document.addEventListener('gameRequest', (e) => {
            this.handleGameRequest(e.detail.gameId, e.detail.context);
        });

        // Écouter les événements de progression
        document.addEventListener('gameComplete', (e) => {
            this.handleGameComplete(e.detail);
        });
    }

    createGameButtons() {
        // Créer des boutons de jeu dans les pages appropriées
        this.addGameButtonsToDashboard();
        this.addGameButtonsToProfile();
        this.addGameButtonsToWorld();
    }

    addGameButtonsToDashboard() {
        const dashboard = document.querySelector('.dashboard-grid, .dashboard-container');
        if (dashboard) {
            const gamesSection = this.createGamesSection();
            dashboard.appendChild(gamesSection);
        }
    }

    addGameButtonsToProfile() {
        const profile = document.querySelector('.profile-stats, .profile-container');
        if (profile) {
            const gamesSection = this.createGamesSection();
            profile.appendChild(gamesSection);
        }
    }

    addGameButtonsToWorld() {
        const world = document.querySelector('.world-zones, .zones-container');
        if (world) {
            const gamesSection = this.createGamesSection();
            world.appendChild(gamesSection);
        }
    }

    createGamesSection() {
        const section = document.createElement('div');
        section.className = 'mini-games-section';
        section.innerHTML = `
            <div class="games-header">
                <h3>🎮 Mini-Jeux Disponibles</h3>
                <p>Testez vos compétences et gagnez des points !</p>
            </div>
            <div class="games-grid" id="games-grid">
                <!-- Les jeux seront ajoutés dynamiquement -->
            </div>
        `;

        // Styles
        section.style.cssText = `
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 255, 255, 0.05));
            border: 2px solid rgba(0, 255, 0, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
        `;

        // Ajouter les jeux
        this.populateGamesGrid(section.querySelector('#games-grid'));

        return section;
    }

    populateGamesGrid(container) {
        Object.entries(this.availableGames).forEach(([gameId, game]) => {
            const gameCard = this.createGameCard(gameId, game);
            container.appendChild(gameCard);
        });
    }

    createGameCard(gameId, game) {
        const card = document.createElement('div');
        card.className = 'game-card';
        card.innerHTML = `
            <div class="game-icon">${game.icon}</div>
            <div class="game-info">
                <h4>${game.name}</h4>
                <p>${game.description}</p>
                <div class="game-stats">
                    <span class="difficulty">${'★'.repeat(game.difficulty)}</span>
                    <span class="max-score">Max: ${game.maxScore} pts</span>
                </div>
            </div>
            <div class="game-actions">
                <button class="play-btn" data-game="${gameId}">Jouer</button>
                <button class="info-btn" data-game="${gameId}">Info</button>
            </div>
        `;

        // Styles
        card.style.cssText = `
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(0, 17, 0, 0.6));
            border: 2px solid ${game.color}40;
            border-radius: 12px;
            padding: 20px;
            margin: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
            cursor: pointer;
        `;

        // Hover effect
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px) scale(1.02)';
            card.style.boxShadow = `0 10px 30px ${game.color}40`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.boxShadow = 'none';
        });

        // Event listeners
        const playBtn = card.querySelector('.play-btn');
        const infoBtn = card.querySelector('.info-btn');

        playBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.launchGame(gameId);
        });

        infoBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.showGameInfo(gameId);
        });

        return card;
    }

    launchGame(gameId) {
        if (window.gameEngine) {
            window.gameEngine.playGame(gameId);
        } else {
            this.showError('Système de jeu non disponible');
        }
    }

    showGameInfo(gameId) {
        const game = this.availableGames[gameId];
        if (!game) return;

        const modal = document.createElement('div');
        modal.className = 'game-info-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${game.icon} ${game.name}</h2>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <p>${game.description}</p>
                    <div class="game-details">
                        <div class="detail">
                            <strong>Type:</strong> ${this.getGameTypeLabel(game.type)}
                        </div>
                        <div class="detail">
                            <strong>Difficulté:</strong> ${'★'.repeat(game.difficulty)}
                        </div>
                        <div class="detail">
                            <strong>Score Maximum:</strong> ${game.maxScore} points
                        </div>
                        <div class="detail">
                            <strong>Récompenses:</strong> XP, Badges, Progression
                        </div>
                    </div>
                    <div class="modal-actions">
                        <button class="play-btn-modal" data-game="${gameId}">Jouer Maintenant</button>
                        <button class="close-btn-modal">Fermer</button>
                    </div>
                </div>
            </div>
        `;

        // Styles
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;

        modal.querySelector('.modal-content').style.cssText = `
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.95), rgba(0, 17, 0, 0.9));
            border: 3px solid ${game.color};
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            color: var(--matrix-green);
        `;

        document.body.appendChild(modal);

        // Event listeners
        modal.querySelector('.close-btn').addEventListener('click', () => modal.remove());
        modal.querySelector('.close-btn-modal').addEventListener('click', () => modal.remove());
        modal.querySelector('.play-btn-modal').addEventListener('click', () => {
            modal.remove();
            this.launchGame(gameId);
        });

        // Fermer en cliquant à l'extérieur
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
    }

    getGameTypeLabel(type) {
        const labels = {
            'logic': 'Logique',
            'code': 'Programmation',
            'security': 'Cybersécurité',
            'hacking': 'Hacking'
        };
        return labels[type] || type;
    }

    // GESTION DES ÉVÉNEMENTS
    handleGameRequest(gameId, context) {
        this.launchGame(gameId);
    }

    handleGameComplete(data) {
        // Mettre à jour l'interface
        this.updateGameStats(data.gameId, data.score);

        // Déclencher des événements de feedback
        if (window.visualFeedback) {
            window.visualFeedback.handleGameEvent('game_end', data);
        }
    }

    updateGameStats(gameId, score) {
        // Mettre à jour les statistiques du jeu
        const gameCard = document.querySelector(`[data-game="${gameId}"]`);
        if (gameCard) {
            const stats = gameCard.querySelector('.game-stats');
            if (stats) {
                const scoreElement = stats.querySelector('.current-score');
                if (scoreElement) {
                    scoreElement.textContent = `Score: ${score}`;
                } else {
                    const scoreSpan = document.createElement('span');
                    scoreSpan.className = 'current-score';
                    scoreSpan.textContent = `Score: ${score}`;
                    scoreSpan.style.color = '#00ff00';
                    stats.appendChild(scoreSpan);
                }
            }
        }
    }

    // MÉTHODES UTILITAIRES
    showError(message) {
        if (window.visualFeedback) {
            window.visualFeedback.showNotification({
                type: 'error',
                title: 'Erreur',
                message: message,
                duration: 3000
            });
        } else {
            alert(message);
        }
    }

    loadGameProgress() {
        const progress = localStorage.getItem('arkaliaGameProgress');
        if (progress) {
            const data = JSON.parse(progress);
            this.gameInstances = new Map(data.gameInstances || []);
        }
    }

    saveGameProgress() {
        const progress = {
            gameInstances: Array.from(this.gameInstances.entries()),
            timestamp: Date.now()
        };
        localStorage.setItem('arkaliaGameProgress', JSON.stringify(progress));
    }

    // MÉTHODES PUBLIQUES
    getAvailableGames() {
        return this.availableGames;
    }

    getGameStats(gameId) {
        return this.gameInstances.get(gameId) || {
            timesPlayed: 0,
            bestScore: 0,
            totalScore: 0,
            lastPlayed: null
        };
    }

    updateGameStats(gameId, score) {
        const stats = this.getGameStats(gameId);
        stats.timesPlayed++;
        stats.bestScore = Math.max(stats.bestScore, score);
        stats.totalScore += score;
        stats.lastPlayed = new Date().toISOString();

        this.gameInstances.set(gameId, stats);
        this.saveGameProgress();
    }

    // Ouvrir la modal de jeu
    openGameModal(gameId) {
        const game = this.games[gameId];

        // Créer la modal
        const modal = document.createElement('div');
        modal.className = 'game-modal';
        modal.id = `game-modal-${gameId}`;
        modal.innerHTML = `
            <div class="game-modal-content">
                <div class="game-header">
                    <h3 class="game-title">${game.name}</h3>
                    <button class="game-close" onclick="window.unifiedMiniGames.closeGameModal('${gameId}')">&times;</button>
                </div>
                <div class="game-content">
                    <div class="game-description">${game.description}</div>
                    <div class="game-area" id="game-area-${gameId}">
                        ${this.generateGameContent(gameId)}
                    </div>
                    <div class="game-controls">
                        <button class="game-button" onclick="window.unifiedMiniGames.startGame('${gameId}')">Commencer</button>
                        <button class="game-button" onclick="window.unifiedMiniGames.resetGame('${gameId}')">Recommencer</button>
                    </div>
                    <div class="game-feedback" id="game-feedback-${gameId}"></div>
                    <div class="game-progress" id="game-progress-${gameId}">
                        <div class="progress-bar">
                            <div class="progress-fill" id="progress-fill-${gameId}"></div>
                        </div>
                        <div class="progress-text" id="progress-text-${gameId}">0%</div>
                    </div>
                    <div class="game-score" id="game-score-${gameId}">
                        Score: <span id="score-value-${gameId}">0</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Afficher la modal avec animation
        setTimeout(() => {
            modal.style.opacity = '1';
            modal.style.transform = 'scale(1)';
        }, 10);

        // Initialiser le jeu
        this.initializeGame(gameId);
    }

    // Fermer la modal de jeu
    closeGameModal(gameId) {
        const modal = document.getElementById(`game-modal-${gameId}`);
        if (modal) {
            modal.style.opacity = '0';
            modal.style.transform = 'scale(0.8)';
            setTimeout(() => {
                modal.remove();
            }, 300);
        }
    }

    // Générer le contenu du jeu selon le type
    generateGameContent(gameId) {
        const game = this.games[gameId];

        switch (game.type) {
            case 'logic':
                return this.generateLogicGame(gameId);
            case 'code':
                return this.generateCodeGame(gameId);
            case 'cybersecurity':
                return this.generateCybersecurityGame(gameId);
            case 'hacking':
                return this.generateHackingGame(gameId);
            default:
                return '<p>Type de jeu non supporté</p>';
        }
    }

    // Générer un jeu de logique
    generateLogicGame(gameId) {
        return `
            <div class="logic-puzzle">
                <div class="puzzle-question" id="puzzle-question-${gameId}">
                    <h4>Question de logique</h4>
                    <p id="question-text-${gameId}">Chargement...</p>
                </div>
                <div class="puzzle-options" id="puzzle-options-${gameId}">
                    <!-- Les options seront générées dynamiquement -->
                </div>
                <div class="puzzle-hint" id="puzzle-hint-${gameId}">
                    <button class="hint-button" onclick="window.unifiedMiniGames.showHint('${gameId}')">Indice</button>
                </div>
            </div>
        `;
    }

    // Générer un jeu de code
    generateCodeGame(gameId) {
        return `
            <div class="code-puzzle">
                <div class="code-question" id="code-question-${gameId}">
                    <h4>Débogage de code</h4>
                    <p id="code-problem-${gameId}">Chargement...</p>
                </div>
                <div class="code-editor">
                    <textarea id="code-input-${gameId}" placeholder="Tapez votre solution ici..."></textarea>
                </div>
                <div class="code-actions">
                    <button class="game-button" onclick="window.unifiedMiniGames.checkCode('${gameId}')">Vérifier</button>
                    <button class="game-button" onclick="window.unifiedMiniGames.runCode('${gameId}')">Exécuter</button>
                </div>
                <div class="code-output" id="code-output-${gameId}"></div>
            </div>
        `;
    }

    // Générer un jeu de cybersécurité
    generateCybersecurityGame(gameId) {
        return `
            <div class="cybersecurity-puzzle">
                <div class="security-scenario" id="security-scenario-${gameId}">
                    <h4>Scénario de cybersécurité</h4>
                    <p id="scenario-text-${gameId}">Chargement...</p>
                </div>
                <div class="security-options" id="security-options-${gameId}">
                    <!-- Les options seront générées dynamiquement -->
                </div>
                <div class="security-explanation" id="security-explanation-${gameId}">
                    <!-- L'explication apparaîtra après la réponse -->
                </div>
            </div>
        `;
    }

    // Générer un jeu de hacking
    generateHackingGame(gameId) {
        return `
            <div class="hacking-puzzle">
                <div class="hack-scenario" id="hack-scenario-${gameId}">
                    <h4>Défi de hacking</h4>
                    <p id="hack-text-${gameId}">Chargement...</p>
                </div>
                <div class="hack-terminal">
                    <div class="terminal-output" id="hack-output-${gameId}"></div>
                    <div class="terminal-input">
                        <input type="text" id="hack-input-${gameId}" placeholder="Tapez votre commande...">
                        <button onclick="window.unifiedMiniGames.executeHackCommand('${gameId}')">Exécuter</button>
                    </div>
                </div>
                <div class="hack-progress" id="hack-progress-${gameId}">
                    <div class="progress-steps">
                        <div class="step" id="step-1-${gameId}">1. Reconnaissance</div>
                        <div class="step" id="step-2-${gameId}">2. Exploitation</div>
                        <div class="step" id="step-3-${gameId}">3. Accès</div>
                    </div>
                </div>
            </div>
        `;
    }

    // Initialiser un jeu
    initializeGame(gameId) {
        const game = this.games[gameId];

        switch (game.type) {
            case 'logic':
                this.initializeLogicGame(gameId);
                break;
            case 'code':
                this.initializeCodeGame(gameId);
                break;
            case 'cybersecurity':
                this.initializeCybersecurityGame(gameId);
                break;
            case 'hacking':
                this.initializeHackingGame(gameId);
                break;
        }
    }

    // Initialiser un jeu de logique
    initializeLogicGame(gameId) {
        const questions = [
            {
                question: "Si tous les chats sont des animaux et que Félix est un chat, que peut-on conclure ?",
                options: ["Félix est un animal", "Félix n'est pas un animal", "Tous les animaux sont des chats", "Aucune des réponses"],
                correct: 0,
                explanation: "Si tous les chats sont des animaux et que Félix est un chat, alors Félix est nécessairement un animal."
            },
            {
                question: "Dans une séquence : 2, 4, 8, 16, ? Quel est le prochain nombre ?",
                options: ["20", "24", "32", "28"],
                correct: 2,
                explanation: "La séquence double à chaque étape : 2×2=4, 4×2=8, 8×2=16, 16×2=32."
            },
            {
                question: "Si A = 1, B = 2, C = 3, alors D = ?",
                options: ["3", "4", "5", "6"],
                correct: 1,
                explanation: "L'alphabet suit l'ordre numérique : A=1, B=2, C=3, D=4."
            }
        ];

        const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
        this.currentGameData[gameId] = {
            question: randomQuestion,
            score: 0,
            attempts: 0
        };

        this.displayLogicQuestion(gameId, randomQuestion);
    }

    // Afficher une question de logique
    displayLogicQuestion(gameId, question) {
        const questionElement = document.getElementById(`question-text-${gameId}`);
        const optionsElement = document.getElementById(`puzzle-options-${gameId}`);

        if (questionElement) {
            questionElement.textContent = question.question;
        }

        if (optionsElement) {
            optionsElement.innerHTML = '';
            question.options.forEach((option, index) => {
                const optionButton = document.createElement('button');
                optionButton.className = 'game-choice';
                optionButton.textContent = option;
                optionButton.onclick = () => this.selectLogicAnswer(gameId, index);
                optionsElement.appendChild(optionButton);
            });
        }
    }

    // Sélectionner une réponse de logique
    selectLogicAnswer(gameId, selectedIndex) {
        const gameData = this.currentGameData[gameId];
        const question = gameData.question;

        gameData.attempts++;

        if (selectedIndex === question.correct) {
            gameData.score += 100;
            this.showGameFeedback(gameId, "Correct ! +100 points", "success");
            this.updateGameScore(gameId, gameData.score);

            // Célébrer avec le système de récompense
            if (window.rewardSystem) {
                window.rewardSystem.celebrateScoreGained(100);
            }

            // Passer à la question suivante
            setTimeout(() => {
                this.initializeLogicGame(gameId);
            }, 2000);
        } else {
            this.showGameFeedback(gameId, "Incorrect. Essayez encore !", "error");
        }
    }

    // Initialiser un jeu de code
    initializeCodeGame(gameId) {
        const problems = [
            {
                problem: "Corrigez ce code JavaScript qui ne fonctionne pas :\n\nfunction add(a, b) {\n  return a + b\n}\n\nconsole.log(add(2, 3));",
                solution: "function add(a, b) {\n  return a + b;\n}\n\nconsole.log(add(2, 3));",
                hint: "Il manque un point-virgule"
            },
            {
                problem: "Ce code Python a une erreur. Trouvez-la :\n\ndef greet(name):\n    print('Hello, ' + name)\n\ngreet('World')",
                solution: "def greet(name):\n    print('Hello, ' + name)\n\ngreet('World')",
                hint: "Le code semble correct, vérifiez l'indentation"
            }
        ];

        const randomProblem = problems[Math.floor(Math.random() * problems.length)];
        this.currentGameData[gameId] = {
            problem: randomProblem,
            score: 0,
            attempts: 0
        };

        this.displayCodeProblem(gameId, randomProblem);
    }

    // Afficher un problème de code
    displayCodeProblem(gameId, problem) {
        const problemElement = document.getElementById(`code-problem-${gameId}`);
        if (problemElement) {
            problemElement.innerHTML = `<pre>${problem.problem}</pre>`;
        }
    }

    // Vérifier le code
    checkCode(gameId) {
        const codeInput = document.getElementById(`code-input-${gameId}`);
        const gameData = this.currentGameData[gameId];

        if (!codeInput || !gameData) return;

        const userCode = codeInput.value.trim();
        const solution = gameData.problem.solution.trim();

        gameData.attempts++;

        if (userCode === solution) {
            gameData.score += 150;
            this.showGameFeedback(gameId, "Code correct ! +150 points", "success");
            this.updateGameScore(gameId, gameData.score);

            if (window.rewardSystem) {
                window.rewardSystem.celebrateScoreGained(150);
            }
        } else {
            this.showGameFeedback(gameId, "Code incorrect. Essayez encore !", "error");
        }
    }

    // Exécuter le code
    runCode(gameId) {
        const codeInput = document.getElementById(`code-input-${gameId}`);
        const outputElement = document.getElementById(`code-output-${gameId}`);

        if (!codeInput || !outputElement) return;

        const code = codeInput.value;

        try {
            // Simulation d'exécution (en réalité, on ne devrait pas exécuter du code utilisateur)
            outputElement.innerHTML = `<div class="code-result">Exécution simulée : ${code}</div>`;
        } catch (error) {
            outputElement.innerHTML = `<div class="code-error">Erreur : ${error.message}</div>`;
        }
    }

    // Initialiser un jeu de cybersécurité
    initializeCybersecurityGame(gameId) {
        const scenarios = [
            {
                scenario: "Vous recevez un email suspect avec une pièce jointe. Que faites-vous ?",
                options: [
                    "Ouvrir la pièce jointe pour voir ce que c'est",
                    "Supprimer l'email immédiatement",
                    "Répondre à l'expéditeur pour demander des précisions",
                    "Transférer l'email à vos collègues"
                ],
                correct: 1,
                explanation: "Il faut toujours supprimer les emails suspects avec des pièces jointes pour éviter les malwares."
            },
            {
                scenario: "Votre mot de passe a été compromis. Quelle est la première chose à faire ?",
                options: [
                    "Changer le mot de passe immédiatement",
                    "Attendre de voir si quelque chose se passe",
                    "Changer seulement quelques caractères",
                    "Utiliser le même mot de passe partout"
                ],
                correct: 0,
                explanation: "Il faut changer le mot de passe compromis immédiatement pour sécuriser le compte."
            }
        ];

        const randomScenario = scenarios[Math.floor(Math.random() * scenarios.length)];
        this.currentGameData[gameId] = {
            scenario: randomScenario,
            score: 0,
            attempts: 0
        };

        this.displayCybersecurityScenario(gameId, randomScenario);
    }

    // Afficher un scénario de cybersécurité
    displayCybersecurityScenario(gameId, scenario) {
        const scenarioElement = document.getElementById(`scenario-text-${gameId}`);
        const optionsElement = document.getElementById(`security-options-${gameId}`);

        if (scenarioElement) {
            scenarioElement.textContent = scenario.scenario;
        }

        if (optionsElement) {
            optionsElement.innerHTML = '';
            scenario.options.forEach((option, index) => {
                const optionButton = document.createElement('button');
                optionButton.className = 'game-choice';
                optionButton.textContent = option;
                optionButton.onclick = () => this.selectCybersecurityAnswer(gameId, index);
                optionsElement.appendChild(optionButton);
            });
        }
    }

    // Sélectionner une réponse de cybersécurité
    selectCybersecurityAnswer(gameId, selectedIndex) {
        const gameData = this.currentGameData[gameId];
        const scenario = gameData.scenario;

        gameData.attempts++;

        if (selectedIndex === scenario.correct) {
            gameData.score += 120;
            this.showGameFeedback(gameId, "Bonne réponse ! +120 points", "success");
            this.updateGameScore(gameId, gameData.score);

            if (window.rewardSystem) {
                window.rewardSystem.celebrateScoreGained(120);
            }
        } else {
            this.showGameFeedback(gameId, "Mauvaise réponse. Apprenez de vos erreurs !", "error");
        }

        // Afficher l'explication
        this.showCybersecurityExplanation(gameId, scenario.explanation);
    }

    // Afficher l'explication de cybersécurité
    showCybersecurityExplanation(gameId, explanation) {
        const explanationElement = document.getElementById(`security-explanation-${gameId}`);
        if (explanationElement) {
            explanationElement.innerHTML = `<div class="explanation">${explanation}</div>`;
        }
    }

    // Initialiser un jeu de hacking
    initializeHackingGame(gameId) {
        const challenges = [
            {
                challenge: "Trouvez le mot de passe caché dans ce fichier système",
                commands: ["ls", "cat password.txt", "grep password", "find . -name '*.txt'"],
                solution: "cat password.txt",
                explanation: "La commande 'cat' permet de lire le contenu d'un fichier."
            }
        ];

        const randomChallenge = challenges[Math.floor(Math.random() * challenges.length)];
        this.currentGameData[gameId] = {
            challenge: randomChallenge,
            score: 0,
            attempts: 0,
            currentStep: 0
        };

        this.displayHackingChallenge(gameId, randomChallenge);
    }

    // Afficher un défi de hacking
    displayHackingChallenge(gameId, challenge) {
        const challengeElement = document.getElementById(`hack-text-${gameId}`);
        if (challengeElement) {
            challengeElement.textContent = challenge.challenge;
        }
    }

    // Exécuter une commande de hacking
    executeHackCommand(gameId) {
        const inputElement = document.getElementById(`hack-input-${gameId}`);
        const outputElement = document.getElementById(`hack-output-${gameId}`);

        if (!inputElement || !outputElement) return;

        const command = inputElement.value.trim();
        const gameData = this.currentGameData[gameId];

        if (!command) return;

        gameData.attempts++;

        // Simuler la sortie de la commande
        let output = `$ ${command}\n`;

        if (command === gameData.challenge.solution) {
            gameData.score += 200;
            gameData.currentStep++;
            output += "Mot de passe trouvé : 'Arkalia2024!'\n";
            output += "Accès autorisé !\n";
            this.showGameFeedback(gameId, "Excellent ! +200 points", "success");
            this.updateGameScore(gameId, gameData.score);

            if (window.rewardSystem) {
                window.rewardSystem.celebrateScoreGained(200);
            }
        } else {
            output += "Commande non reconnue ou accès refusé.\n";
            this.showGameFeedback(gameId, "Commande incorrecte. Essayez autre chose !", "error");
        }

        outputElement.innerHTML += `<div class="terminal-line">${output}</div>`;
        inputElement.value = '';

        // Faire défiler vers le bas
        outputElement.scrollTop = outputElement.scrollHeight;
    }

    // Afficher le feedback du jeu
    showGameFeedback(gameId, message, type) {
        const feedbackElement = document.getElementById(`game-feedback-${gameId}`);
        if (feedbackElement) {
            feedbackElement.innerHTML = `<div class="feedback ${type}">${message}</div>`;
            feedbackElement.style.display = 'block';

            setTimeout(() => {
                feedbackElement.style.display = 'none';
            }, 3000);
        }
    }

    // Mettre à jour le score du jeu
    updateGameScore(gameId, score) {
        const scoreElement = document.getElementById(`score-value-${gameId}`);
        if (scoreElement) {
            scoreElement.textContent = score;
        }
    }

    // Démarrer un jeu
    startGame(gameId) {
        console.log(`Démarrage du jeu ${gameId}`);
        // Le jeu est déjà initialisé, on peut ajouter des actions de démarrage ici
    }

    // Réinitialiser un jeu
    resetGame(gameId) {
        console.log(`Réinitialisation du jeu ${gameId}`);
        this.initializeGame(gameId);

        // Réinitialiser le score
        const scoreElement = document.getElementById(`score-value-${gameId}`);
        if (scoreElement) {
            scoreElement.textContent = '0';
        }

        // Réinitialiser la progression
        const progressElement = document.getElementById(`progress-fill-${gameId}`);
        if (progressElement) {
            progressElement.style.width = '0%';
        }
    }

    // Afficher un indice
    showHint(gameId) {
        const gameData = this.currentGameData[gameId];
        if (gameData && gameData.question && gameData.question.hint) {
            this.showGameFeedback(gameId, `Indice : ${gameData.question.hint}`, "hint");
        } else if (gameData && gameData.problem && gameData.problem.hint) {
            this.showGameFeedback(gameId, `Indice : ${gameData.problem.hint}`, "hint");
        }
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.unifiedMiniGames = new UnifiedMiniGames();
});

// Export pour utilisation externe
window.UnifiedMiniGames = UnifiedMiniGames;
