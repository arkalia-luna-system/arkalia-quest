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
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.unifiedMiniGames = new UnifiedMiniGames();
});

// Export pour utilisation externe
window.UnifiedMiniGames = UnifiedMiniGames;
