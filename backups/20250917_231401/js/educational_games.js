// ===== MOTEUR DE MINI-JEUX ÉDUCATIFS - ARKALIA QUEST =====

class EducationalGamesManager {
    constructor() {
        this.currentGame = null;
        this.currentSession = null;
        this.gameContainer = null;
        this.isGameActive = false;
        this.audioManager = window.audioManager;
        this.terminal = window.terminal;

        this.init();
    }

    init() {
        // Créer le conteneur de jeu
        this.createGameContainer();

        // Ajouter les commandes de jeu au terminal
        this.addGameCommands();

        // Moteur de mini-jeux éducatifs initialisé
    }

    createGameContainer() {
        // Créer le conteneur principal
        this.gameContainer = document.createElement('div');
        this.gameContainer.id = 'educational-games-container';
        this.gameContainer.className = 'game-overlay';
        this.gameContainer.style.display = 'none';

        // Structure du conteneur
        this.gameContainer.innerHTML = `
            <div class="game-backdrop"></div>
            <div class="game-modal">
                <div class="game-header">
                    <h2 class="game-title">🎮 Mini-Jeu Éducatif</h2>
                    <button class="game-close-btn" onclick="educationalGames.closeGame()">✕</button>
                </div>
                <div class="game-content">
                    <div class="game-info">
                        <div class="game-description"></div>
                        <div class="game-difficulty"></div>
                        <div class="game-points"></div>
                    </div>
                    <div class="game-area">
                        <div class="game-question"></div>
                        <div class="game-options"></div>
                        <div class="game-input-area"></div>
                        <div class="game-code-editor"></div>
                    </div>
                    <div class="game-controls">
                        <button class="game-submit-btn" onclick="educationalGames.submitAnswer()">🎯 Valider</button>
                        <button class="game-hint-btn" onclick="educationalGames.showHint()">💡 Indice</button>
                        <button class="game-skip-btn" onclick="educationalGames.skipGame()">⏭️ Passer</button>
                    </div>
                    <div class="game-feedback"></div>
                </div>
            </div>
        `;

        // Ajouter au body
        document.body.appendChild(this.gameContainer);

        // Ajouter les styles CSS
        this.addGameStyles();
    }

    addGameStyles() {
        const styles = `
            .game-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .game-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(5px);
            }
            
            .game-modal {
                position: relative;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 20px;
                max-width: 800px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
                animation: gameModalSlideIn 0.5s ease-out;
            }
            
            @keyframes gameModalSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(-50px) scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .game-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid #00ffff;
            }
            
            .game-title {
                color: #00ffff;
                margin: 0;
                font-size: 24px;
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
            }
            
            .game-close-btn {
                background: none;
                border: 1px solid #ff4444;
                color: #ff4444;
                padding: 8px 12px;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .game-close-btn:hover {
                background: #ff4444;
                color: white;
                box-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
            }
            
            .game-info {
                background: rgba(0, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                border-left: 4px solid #00ffff;
            }
            
            .game-description {
                color: #ffffff;
                font-size: 16px;
                margin-bottom: 10px;
            }
            
            .game-difficulty {
                color: #ffff00;
                font-size: 14px;
                margin-bottom: 5px;
            }
            
            .game-points {
                color: #00ff88;
                font-size: 14px;
                font-weight: bold;
            }
            
            .game-area {
                margin-bottom: 20px;
            }
            
            .game-question {
                color: #ffffff;
                font-size: 18px;
                margin-bottom: 15px;
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .game-options {
                display: grid;
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .game-option {
                background: rgba(0, 255, 255, 0.1);
                border: 1px solid #00ffff;
                color: #ffffff;
                padding: 12px 15px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                text-align: left;
            }
            
            .game-option:hover {
                background: rgba(0, 255, 255, 0.2);
                box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
            }
            
            .game-option.selected {
                background: rgba(0, 255, 255, 0.3);
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
            }
            
            .game-input-area {
                margin-bottom: 15px;
            }
            
            .game-input {
                width: 100%;
                background: rgba(0, 0, 0, 0.5);
                border: 1px solid #00ffff;
                color: #ffffff;
                padding: 12px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            
            .game-code-editor {
                margin-bottom: 15px;
            }
            
            .game-code-editor textarea {
                width: 100%;
                height: 200px;
                background: rgba(0, 0, 0, 0.8);
                border: 1px solid #00ffff;
                color: #00ff88;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                resize: vertical;
            }
            
            .game-controls {
                display: flex;
                gap: 10px;
                justify-content: center;
                margin-bottom: 15px;
            }
            
            .game-submit-btn, .game-hint-btn, .game-skip-btn {
                background: linear-gradient(45deg, #00ffff, #0088ff);
                border: none;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
                text-transform: uppercase;
            }
            
            .game-submit-btn:hover {
                background: linear-gradient(45deg, #00ff88, #00ffff);
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
                transform: translateY(-2px);
            }
            
            .game-hint-btn {
                background: linear-gradient(45deg, #ffff00, #ff8800);
            }
            
            .game-hint-btn:hover {
                background: linear-gradient(45deg, #ff8800, #ffff00);
                box-shadow: 0 0 20px rgba(255, 255, 0, 0.5);
            }
            
            .game-skip-btn {
                background: linear-gradient(45deg, #ff4444, #ff0088);
            }
            
            .game-skip-btn:hover {
                background: linear-gradient(45deg, #ff0088, #ff4444);
                box-shadow: 0 0 20px rgba(255, 68, 68, 0.5);
            }
            
            .game-feedback {
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
                text-align: center;
                font-weight: bold;
                font-size: 16px;
                min-height: 20px;
            }
            
            .game-feedback.success {
                background: rgba(0, 255, 136, 0.2);
                border: 1px solid #00ff88;
                color: #00ff88;
                animation: successPulse 0.5s ease-out;
            }
            
            .game-feedback.error {
                background: rgba(255, 68, 68, 0.2);
                border: 1px solid #ff4444;
                color: #ff4444;
                animation: errorShake 0.5s ease-out;
            }
            
            .game-feedback.hint {
                background: rgba(255, 255, 0, 0.2);
                border: 1px solid #ffff00;
                color: #ffff00;
            }
            
            @keyframes successPulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            @keyframes errorShake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            .game-logs {
                background: rgba(0, 0, 0, 0.8);
                border: 1px solid #ff4444;
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: #ff4444;
                margin-bottom: 15px;
                max-height: 150px;
                overflow-y: auto;
            }
            
            .game-logs .log-entry {
                margin-bottom: 5px;
                padding: 2px 0;
            }
            
            .game-passwords {
                display: grid;
                gap: 8px;
            }
            
            .game-password {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                color: #ffffff;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .game-password:hover {
                background: rgba(255, 255, 255, 0.1);
                border-color: #00ffff;
            }
            
            .game-password.selected {
                background: rgba(0, 255, 255, 0.2);
                border-color: #00ffff;
                box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            }
        `;

        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    addGameCommands() {
        // Ajouter les commandes de jeu au terminal
        if (this.terminal && this.terminal.addCommand) {
            this.terminal.addCommand('play_game', this.handlePlayGameCommand.bind(this));
            this.terminal.addCommand('games', this.handleGamesListCommand.bind(this));
            this.terminal.addCommand('game_stats', this.handleGameStatsCommand.bind(this));
            this.terminal.addCommand('game_leaderboard', this.handleGameLeaderboardCommand.bind(this));
        }
    }

    async handlePlayGameCommand(args) {
        if (this.isGameActive) {
            return {
                success: false,
                message: "❌ Un jeu est déjà en cours. Termine-le d'abord !"
            };
        }

        if (!args || args.length === 0) {
            return {
                success: false,
                message: "❌ Usage: play_game <game_id> ou play_game random"
            };
        }

        const gameId = args[0];

        try {
            const response = await fetch('/api/educational-games/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    game_id: gameId === 'random' ? null : gameId
                })
            });

            const data = await response.json();

            if (data.success) {
                this.startGame(data.game, data.session_id);
                return {
                    success: true,
                    message: `🎮 ${data.game.title} démarré !`
                };
            } else {
                return {
                    success: false,
                    message: data.message || "❌ Erreur lors du démarrage du jeu"
                };
            }
        } catch (error) {
            console.error('Erreur démarrage jeu:', error);
            return {
                success: false,
                message: "❌ Erreur de connexion"
            };
        }
    }

    async handleGamesListCommand() {
        try {
            const response = await fetch('/api/educational-games/list');
            const data = await response.json();

            if (data.success) {
                let message = "🎮 MINI-JEUX ÉDUCATIFS DISPONIBLES\n\n";

                const gamesByType = {};
                data.games.forEach(game => {
                    if (!gamesByType[game.type]) {
                        gamesByType[game.type] = [];
                    }
                    gamesByType[game.type].push(game);
                });

                for (const [type, games] of Object.entries(gamesByType)) {
                    const typeEmoji = this.getTypeEmoji(type);
                    const typeName = this.getTypeName(type);
                    message += `${typeEmoji} ${typeName.toUpperCase()}\n`;

                    games.forEach(game => {
                        const difficultyEmoji = this.getDifficultyEmoji(game.difficulty);
                        message += `  • ${game.id}: ${game.title} ${difficultyEmoji} (+${game.points}pts)\n`;
                    });
                    message += "\n";
                }

                message += "💡 Utilise 'play_game <id>' pour jouer !";

                return {
                    success: true,
                    message: message
                };
            } else {
                return {
                    success: false,
                    message: "❌ Erreur lors du chargement des jeux"
                };
            }
        } catch (error) {
            console.error('Erreur liste jeux:', error);
            return {
                success: false,
                message: "❌ Erreur de connexion"
            };
        }
    }

    async handleGameStatsCommand() {
        try {
            const response = await fetch('/api/educational-games/stats');
            const data = await response.json();

            if (data.success) {
                const stats = data.stats;
                let message = "📊 STATISTIQUES DES MINI-JEUX\n\n";
                message += `🎮 Total de jeux: ${stats.total_games}\n`;
                message += `👥 Joueurs actifs: ${stats.total_players}\n`;
                message += `🎯 Sessions jouées: ${stats.total_sessions}\n\n`;

                message += "📈 RÉPARTITION PAR TYPE:\n";
                for (const [type, count] of Object.entries(stats.games_by_type)) {
                    const typeEmoji = this.getTypeEmoji(type);
                    const typeName = this.getTypeName(type);
                    message += `  ${typeEmoji} ${typeName}: ${count} jeux\n`;
                }

                return {
                    success: true,
                    message: message
                };
            } else {
                return {
                    success: false,
                    message: "❌ Erreur lors du chargement des statistiques"
                };
            }
        } catch (error) {
            console.error('Erreur stats jeux:', error);
            return {
                success: false,
                message: "❌ Erreur de connexion"
            };
        }
    }

    async handleGameLeaderboardCommand() {
        try {
            const response = await fetch('/api/educational-games/leaderboard');
            const data = await response.json();

            if (data.success) {
                const leaderboard = data.leaderboard;
                let message = "🏆 CLASSEMENT DES MINI-JEUX\n\n";

                leaderboard.forEach((player, index) => {
                    const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "🏅";
                    message += `${medal} ${player.user_id}: ${player.total_score}pts (${player.games_completed} jeux, ${player.badges_count} badges)\n`;
                });

                return {
                    success: true,
                    message: message
                };
            } else {
                return {
                    success: false,
                    message: "❌ Erreur lors du chargement du classement"
                };
            }
        } catch (error) {
            console.error('Erreur leaderboard jeux:', error);
            return {
                success: false,
                message: "❌ Erreur de connexion"
            };
        }
    }

    startGame(game, sessionId) {
        this.currentGame = game;
        this.currentSession = sessionId;
        this.isGameActive = true;

        // Afficher le conteneur de jeu
        this.gameContainer.style.display = 'flex';

        // Remplir les informations du jeu
        this.gameContainer.querySelector('.game-title').textContent = game.title;
        this.gameContainer.querySelector('.game-description').textContent = game.description;
        this.gameContainer.querySelector('.game-difficulty').textContent = `🎯 Difficulté: ${this.getDifficultyName(game.difficulty)}`;
        this.gameContainer.querySelector('.game-points').textContent = `🏆 Points: ${game.points}`;

        // Préparer l'interface selon le type de jeu
        this.prepareGameInterface(game);

        // Effet sonore
        if (this.audioManager) {
            this.audioManager.playSound('game_start');
        }

        // Animation d'entrée
        this.gameContainer.querySelector('.game-modal').style.animation = 'gameModalSlideIn 0.5s ease-out';
    }

    prepareGameInterface(game) {
        const questionArea = this.gameContainer.querySelector('.game-question');
        const optionsArea = this.gameContainer.querySelector('.game-options');
        const inputArea = this.gameContainer.querySelector('.game-input-area');
        const codeArea = this.gameContainer.querySelector('.game-code-editor');

        // Nettoyer les zones
        questionArea.innerHTML = '';
        optionsArea.innerHTML = '';
        inputArea.innerHTML = '';
        codeArea.innerHTML = '';

        // Préparer selon le type de jeu
        switch (game.type) {
            case 'logic':
                this.prepareLogicGame(game, questionArea, optionsArea);
                break;
            case 'code':
                this.prepareCodeGame(game, questionArea, codeArea);
                break;
            case 'cybersecurity':
                this.prepareCybersecurityGame(game, questionArea, optionsArea);
                break;
            case 'cryptography':
                this.prepareCryptographyGame(game, questionArea, inputArea);
                break;
            case 'network':
                this.prepareNetworkGame(game, questionArea, optionsArea);
                break;
        }
    }

    prepareLogicGame(game, questionArea, optionsArea) {
        if (game.hints) {
            questionArea.innerHTML = `
                <h3>🔍 Indices:</h3>
                <ul>
                    ${game.hints.map(hint => `<li>${hint}</li>`).join('')}
                </ul>
            `;

            // Zone de saisie pour la réponse
            const inputArea = this.gameContainer.querySelector('.game-input-area');
            inputArea.innerHTML = `
                <label>💭 Ta réponse:</label>
                <input type="text" class="game-input" placeholder="Entre ta réponse..." maxlength="50">
            `;
        } else if (game.rules) {
            questionArea.innerHTML = `
                <h3>🧩 Règles:</h3>
                <ul>
                    ${game.rules.map(rule => `<li>${rule}</li>`).join('')}
                </ul>
                <h4>📊 Nombres: ${game.numbers.join(', ')}</h4>
            `;

            // Options pour les portes
            optionsArea.innerHTML = `
                <label>🚪 Sélectionne les portes à ouvrir:</label>
                <div class="game-options">
                    ${game.numbers.map((num, index) => `
                        <div class="game-option" data-value="${index + 1}">
                            Porte ${index + 1} (${num})
                        </div>
                    `).join('')}
                </div>
            `;

            // Gestion des clics sur les options
            optionsArea.querySelectorAll('.game-option').forEach(option => {
                option.addEventListener('click', () => {
                    option.classList.toggle('selected');
                });
            });
        }
    }

    prepareCodeGame(game, questionArea, codeArea) {
        if (game.code) {
            questionArea.innerHTML = `
                <h3>💻 Code à déboguer:</h3>
                <div class="game-logs">
                    ${game.code.split('\n').map(line => `<div class="log-entry">${line}</div>`).join('')}
                </div>
                <p><strong>❌ Problème:</strong> ${game.error}</p>
            `;

            codeArea.innerHTML = `
                <label>🔧 Ta correction:</label>
                <textarea class="game-code-input" placeholder="Écris ta correction ici...">${game.code}</textarea>
            `;
        } else if (game.challenge) {
            questionArea.innerHTML = `
                <h3>🔐 Défi:</h3>
                <p>${game.challenge}</p>
                <p><strong>Test:</strong> Input: "${game.test_input}" → Expected: "${game.expected_output}"</p>
            `;

            codeArea.innerHTML = `
                <label>💻 Ton code:</label>
                <textarea class="game-code-input" placeholder="Écris ta fonction ici..."></textarea>
            `;
        }
    }

    prepareCybersecurityGame(game, questionArea, optionsArea) {
        if (game.logs) {
            questionArea.innerHTML = `
                <h3>🛡️ Logs d'attaque:</h3>
                <div class="game-logs">
                    ${game.logs.map(log => `<div class="log-entry">${log}</div>`).join('')}
                </div>
                <p><strong>❓ Question:</strong> Quel type d'attaque observe-t-on ?</p>
            `;

            optionsArea.innerHTML = `
                <div class="game-options">
                    ${game.options.map(option => `
                        <div class="game-option" data-value="${option}">
                            ${option}
                        </div>
                    `).join('')}
                </div>
            `;
        } else if (game.passwords) {
            questionArea.innerHTML = `
                <h3>🔒 Sécurité des mots de passe:</h3>
                <p>Choisis le mot de passe le plus sécurisé parmi ceux-ci:</p>
            `;

            optionsArea.innerHTML = `
                <div class="game-passwords">
                    ${game.passwords.map((password, index) => `
                        <div class="game-password" data-value="${index}">
                            ${password}
                        </div>
                    `).join('')}
                </div>
            `;
        }

        // Gestion des clics sur les options
        optionsArea.querySelectorAll('.game-option, .game-password').forEach(option => {
            option.addEventListener('click', () => {
                // Désélectionner les autres
                optionsArea.querySelectorAll('.game-option, .game-password').forEach(opt => {
                    opt.classList.remove('selected');
                });
                // Sélectionner celui-ci
                option.classList.add('selected');
            });
        });
    }

    prepareCryptographyGame(game, questionArea, inputArea) {
        if (game.encoded_message) {
            questionArea.innerHTML = `
                <h3>🔐 Message encodé:</h3>
                <div class="game-logs">
                    <div class="log-entry">${game.encoded_message}</div>
                </div>
                <p><strong>💡 Indice:</strong> C'est un encodage Base64</p>
            `;
        } else if (game.encrypted) {
            questionArea.innerHTML = `
                <h3>🔄 Message chiffré (César, décalage ${game.shift}):</h3>
                <div class="game-logs">
                    <div class="log-entry">${game.encrypted}</div>
                </div>
                <p><strong>💡 Indice:</strong> Chaque lettre est décalée de ${game.shift} positions</p>
            `;
        }

        inputArea.innerHTML = `
            <label>🔓 Ta réponse:</label>
            <input type="text" class="game-input" placeholder="Entre le message décodé..." maxlength="100">
        `;
    }

    prepareNetworkGame(game, questionArea, optionsArea) {
        questionArea.innerHTML = `
            <h3>🌐 Analyse réseau:</h3>
            <p>Identifie le type de réseau pour chaque adresse IP:</p>
            <div class="game-logs">
                ${game.ip_addresses.map(ip => `<div class="log-entry">${ip}</div>`).join('')}
            </div>
        `;

        optionsArea.innerHTML = `
            <div class="game-options">
                ${game.options.map(option => `
                    <div class="game-option" data-value="${option}">
                        ${option}
                    </div>
                `).join('')}
            </div>
        `;

        // Gestion des clics sur les options
        optionsArea.querySelectorAll('.game-option').forEach(option => {
            option.addEventListener('click', () => {
                option.classList.toggle('selected');
            });
        });
    }

    async submitAnswer() {
        if (!this.currentGame || !this.currentSession) {
            return;
        }

        // Récupérer la réponse selon le type de jeu
        let answer = this.getCurrentAnswer();

        if (answer === null) {
            this.showFeedback("❌ Veuillez fournir une réponse", 'error');
            return;
        }

        try {
            const response = await fetch('/api/educational-games/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: this.currentSession,
                    answer: answer
                })
            });

            const data = await response.json();

            if (data.success) {
                if (data.correct) {
                    if (window.universalNotifications) {
                        window.universalNotifications.success(`🎉 ${data.message} +${data.score} points !`);
                    }

                    // Effet sonore de succès
                    if (this.audioManager) {
                        this.audioManager.playSound('success');
                    }

                    // Fermer le jeu après 3 secondes
                    setTimeout(() => {
                        this.closeGame();
                    }, 3000);
                } else {
                    this.showFeedback(data.message, 'error');

                    // Effet sonore d'erreur
                    if (this.audioManager) {
                        this.audioManager.playSound('error');
                    }

                    // Afficher l'indice si disponible
                    if (data.hint) {
                        setTimeout(() => {
                            this.showFeedback(data.hint, 'hint');
                        }, 2000);
                    }
                }
            } else {
                this.showFeedback(data.message || "❌ Erreur lors de la soumission", 'error');
            }
        } catch (error) {
            console.error('Erreur soumission réponse:', error);
            this.showFeedback("❌ Erreur de connexion", 'error');
        }
    }

    getCurrentAnswer() {
        const game = this.currentGame;

        switch (game.type) {
            case 'logic':
                if (game.hints) {
                    const input = this.gameContainer.querySelector('.game-input');
                    return input ? input.value.trim() : null;
                } else if (game.rules) {
                    const selected = this.gameContainer.querySelectorAll('.game-option.selected');
                    return selected.length > 0 ? Array.from(selected).map(opt => parseInt(opt.dataset.value)) : null;
                }
                break;

            case 'code':
                const textarea = this.gameContainer.querySelector('.game-code-input');
                return textarea ? textarea.value.trim() : null;

            case 'cybersecurity':
                if (game.logs) {
                    const selected = this.gameContainer.querySelector('.game-option.selected');
                    return selected ? selected.dataset.value : null;
                } else if (game.passwords) {
                    const selected = this.gameContainer.querySelector('.game-password.selected');
                    return selected ? parseInt(selected.dataset.value) : null;
                }
                break;

            case 'cryptography':
                const input = this.gameContainer.querySelector('.game-input');
                return input ? input.value.trim() : null;

            case 'network':
                const selected = this.gameContainer.querySelectorAll('.game-option.selected');
                return selected.length > 0 ? Array.from(selected).map(opt => opt.dataset.value) : null;
        }

        return null;
    }

    showHint() {
        if (!this.currentGame) return;

        const hints = this.currentGame.hints;
        if (hints && hints.length > 0) {
            const randomHint = hints[Math.floor(Math.random() * hints.length)];
            this.showFeedback(`💡 Indice: ${randomHint}`, 'hint');
        } else {
            this.showFeedback("💡 Pas d'indice disponible pour ce jeu", 'hint');
        }
    }

    skipGame() {
        this.showFeedback("⏭️ Jeu passé", 'hint');
        setTimeout(() => {
            this.closeGame();
        }, 2000);
    }

    showFeedback(message, type) {
        const feedback = this.gameContainer.querySelector('.game-feedback');
        feedback.textContent = message;
        feedback.className = `game-feedback ${type}`;

        // Effet visuel
        feedback.style.animation = 'none';
        setTimeout(() => {
            feedback.style.animation = type === 'success' ? 'successPulse 0.5s ease-out' :
                type === 'error' ? 'errorShake 0.5s ease-out' : '';
        }, 10);
    }

    closeGame() {
        this.gameContainer.style.display = 'none';
        this.currentGame = null;
        this.currentSession = null;
        this.isGameActive = false;

        // Effet sonore
        if (this.audioManager) {
            this.audioManager.playSound('game_end');
        }
    }

    getTypeEmoji(type) {
        const emojis = {
            'logic': '🧩',
            'code': '💻',
            'cybersecurity': '🛡️',
            'cryptography': '🔐',
            'network': '🌐'
        };
        return emojis[type] || '🎮';
    }

    getTypeName(type) {
        const names = {
            'logic': 'Logique',
            'code': 'Programmation',
            'cybersecurity': 'Cybersécurité',
            'cryptography': 'Cryptographie',
            'network': 'Réseaux'
        };
        return names[type] || type;
    }

    getDifficultyEmoji(difficulty) {
        const emojis = {
            'beginner': '🟢',
            'intermediate': '🟡',
            'advanced': '🟠',
            'expert': '🔴'
        };
        return emojis[difficulty] || '⚪';
    }

    getDifficultyName(difficulty) {
        const names = {
            'beginner': 'Débutant',
            'intermediate': 'Intermédiaire',
            'advanced': 'Avancé',
            'expert': 'Expert'
        };
        return names[difficulty] || difficulty;
    }
}

// Instance globale
window.educationalGames = new EducationalGamesManager(); 