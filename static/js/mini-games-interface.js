/**
 * Interface des Mini-Jeux Interactifs - Arkalia Quest
 * Interface graphique pour les 9 mini-jeux éducatifs
 */

class MiniGamesInterface {
    constructor() {
        this.currentGame = null;
        this.gameContainer = null;
        this.isGameActive = false;
        this.audioManager = window.audioManager;
        this.init();
    }

    init() {
        this.createGameContainer();
        this.bindEvents();
    }

    createGameContainer() {
        // Créer le conteneur principal des mini-jeux
        this.gameContainer = document.createElement('div');
        this.gameContainer.id = 'mini-games-container';
        this.gameContainer.className = 'mini-games-container';
        this.gameContainer.innerHTML = `
            <div class="mini-games-overlay"></div>
            <div class="mini-games-modal">
                <div class="mini-games-header">
                    <h2 id="game-title">🎮 Mini-Jeu</h2>
                    <button class="close-game-btn" aria-label="Fermer le jeu">×</button>
                </div>
                <div class="mini-games-content">
                    <div id="game-description" class="game-description"></div>
                    <div id="game-area" class="game-area"></div>
                    <div id="game-controls" class="game-controls"></div>
                    <div id="game-feedback" class="game-feedback"></div>
                </div>
                <div class="mini-games-footer">
                    <div id="game-progress" class="game-progress"></div>
                    <div id="game-score" class="game-score">Score: 0</div>
                </div>
            </div>
        `;

        document.body.appendChild(this.gameContainer);
    }

    bindEvents() {
        // Fermer le jeu
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('close-game-btn') ||
                e.target.classList.contains('mini-games-overlay')) {
                this.closeGame();
            }
        });

        // Échapper pour fermer
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isGameActive) {
                this.closeGame();
            }
        });
    }

    openGame(gameId) {
        this.currentGame = gameId;
        this.isGameActive = true;
        this.gameContainer.style.display = 'flex';

        // Charger le jeu spécifique
        this.loadGame(gameId);

        // Focus sur le jeu
        const gameArea = document.getElementById('game-area');
        if (gameArea) {
            gameArea.focus();
        }
    }

    closeGame() {
        this.isGameActive = false;
        this.currentGame = null;
        this.gameContainer.style.display = 'none';

        // Nettoyer l'interface
        this.clearGameArea();
    }

    loadGame(gameId) {
        const gameData = this.getGameData(gameId);
        if (!gameData) return;

        // Mettre à jour l'interface
        document.getElementById('game-title').textContent = gameData.title;
        document.getElementById('game-description').textContent = gameData.description;

        // Charger le jeu spécifique
        switch (gameData.type) {
            case 'logic':
                this.loadLogicGame(gameData);
                break;
            case 'code':
                this.loadCodeGame(gameData);
                break;
            case 'cybersecurity':
                this.loadCybersecurityGame(gameData);
                break;
            case 'cryptography':
                this.loadCryptographyGame(gameData);
                break;
            case 'network':
                this.loadNetworkGame(gameData);
                break;
        }
    }

    loadLogicGame(gameData) {
        const gameArea = document.getElementById('game-area');

        if (gameData.id === 'logic_1') {
            // Jeu de décryptage de mot de passe
            gameArea.innerHTML = `
                <div class="logic-game">
                    <h3>🔍 Décrypte le Mot de Passe</h3>
                    <div class="hints">
                        <h4>Indices :</h4>
                        <ul>
                            ${gameData.hints.map(hint => `<li>${hint}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="input-area">
                        <input type="text" id="password-input" placeholder="Tape le mot de passe..." maxlength="10">
                        <button id="check-password">Vérifier</button>
                    </div>
                    <div id="password-feedback" class="feedback"></div>
                </div>
            `;

            this.bindPasswordGame(gameData);
        } else if (gameData.id === 'logic_2') {
            // Jeu de puzzle de portes
            gameArea.innerHTML = `
                <div class="logic-game">
                    <h3>🧩 Puzzle de Portes</h3>
                    <div class="rules">
                        <h4>Règles :</h4>
                        <ul>
                            ${gameData.rules.map(rule => `<li>${rule}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="numbers">
                        <h4>Nombres à analyser :</h4>
                        <div class="number-grid">
                            ${gameData.numbers.map(num => `<span class="number-item" data-number="${num}">${num}</span>`).join('')}
                        </div>
                    </div>
                    <div class="doors">
                        <h4>Sélectionne les portes à ouvrir :</h4>
                        <div class="door-grid">
                            <button class="door-btn" data-door="1">Porte 1</button>
                            <button class="door-btn" data-door="2">Porte 2</button>
                            <button class="door-btn" data-door="3">Porte 3</button>
                        </div>
                    </div>
                    <button id="check-doors">Vérifier</button>
                    <div id="doors-feedback" class="feedback"></div>
                </div>
            `;

            this.bindDoorsGame(gameData);
        }
    }

    loadCodeGame(gameData) {
        const gameArea = document.getElementById('game-area');

        if (gameData.id === 'code_1') {
            // Jeu de débogage
            gameArea.innerHTML = `
                <div class="code-game">
                    <h3>💻 Débogue le Code</h3>
                    <div class="code-display">
                        <h4>Code à corriger :</h4>
                        <pre><code>${gameData.code}</code></pre>
                    </div>
                    <div class="error-info">
                        <h4>Erreur identifiée :</h4>
                        <p>${gameData.error}</p>
                    </div>
                    <div class="code-editor">
                        <h4>Corrige le code :</h4>
                        <textarea id="code-editor" rows="10" cols="50">${gameData.code}</textarea>
                    </div>
                    <button id="check-code">Vérifier</button>
                    <div id="code-feedback" class="feedback"></div>
                </div>
            `;

            this.bindCodeGame(gameData);
        }
    }

    loadCybersecurityGame(gameData) {
        const gameArea = document.getElementById('game-area');

        if (gameData.id === 'cyber_1') {
            // Jeu de détection d'attaque
            gameArea.innerHTML = `
                <div class="cybersecurity-game">
                    <h3>🛡️ Détecte l'Attaque</h3>
                    <div class="logs-display">
                        <h4>Logs à analyser :</h4>
                        <div class="logs">
                            ${gameData.logs.map(log => `<div class="log-entry">${log}</div>`).join('')}
                        </div>
                    </div>
                    <div class="attack-options">
                        <h4>Quel type d'attaque détectes-tu ?</h4>
                        <div class="options-grid">
                            ${gameData.options.map(option => `
                                <button class="attack-option" data-option="${option}">${option}</button>
                            `).join('')}
                        </div>
                    </div>
                    <div id="cyber-feedback" class="feedback"></div>
                </div>
            `;

            this.bindCybersecurityGame(gameData);
        }
    }

    loadCryptographyGame(gameData) {
        const gameArea = document.getElementById('game-area');

        if (gameData.id === 'crypto_1') {
            // Jeu de décodage Base64
            gameArea.innerHTML = `
                <div class="cryptography-game">
                    <h3>🔐 Décode le Message</h3>
                    <div class="encoded-message">
                        <h4>Message crypté :</h4>
                        <div class="encoded-text">${gameData.encoded_message}</div>
                    </div>
                    <div class="decode-area">
                        <h4>Message décodé :</h4>
                        <input type="text" id="decoded-input" placeholder="Tape le message décodé...">
                        <button id="check-decode">Vérifier</button>
                    </div>
                    <div id="crypto-feedback" class="feedback"></div>
                </div>
            `;

            this.bindCryptographyGame(gameData);
        }
    }

    loadNetworkGame(gameData) {
        const gameArea = document.getElementById('game-area');

        if (gameData.id === 'network_1') {
            // Jeu d'analyse d'adresses IP
            gameArea.innerHTML = `
                <div class="network-game">
                    <h3>🌐 Analyse le Réseau</h3>
                    <div class="ip-display">
                        <h4>Adresses IP à analyser :</h4>
                        <div class="ip-list">
                            ${gameData.ips.map(ip => `<div class="ip-item">${ip}</div>`).join('')}
                        </div>
                    </div>
                    <div class="analysis-area">
                        <h4>Analyse :</h4>
                        <div class="analysis-options">
                            <label><input type="radio" name="analysis" value="public"> IP Publique</label>
                            <label><input type="radio" name="analysis" value="private"> IP Privée</label>
                            <label><input type="radio" name="analysis" value="localhost"> Localhost</label>
                        </div>
                        <button id="check-analysis">Vérifier</button>
                    </div>
                    <div id="network-feedback" class="feedback"></div>
                </div>
            `;

            this.bindNetworkGame(gameData);
        }
    }

    // Méthodes de liaison des événements pour chaque jeu
    bindPasswordGame(gameData) {
        const checkBtn = document.getElementById('check-password');
        const input = document.getElementById('password-input');
        const feedback = document.getElementById('password-feedback');

        checkBtn.addEventListener('click', () => {
            const answer = input.value.trim().toUpperCase();
            if (answer === gameData.solution) {
                feedback.innerHTML = '✅ Correct ! ' + gameData.explanation;
                feedback.className = 'feedback success';
                this.gameComplete(gameData);
            } else {
                feedback.innerHTML = '❌ Incorrect. Essaie encore !';
                feedback.className = 'feedback error';
            }
        });
    }

    bindDoorsGame(gameData) {
        const checkBtn = document.getElementById('check-doors');
        const feedback = document.getElementById('doors-feedback');
        let selectedDoors = [];

        document.querySelectorAll('.door-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                btn.classList.toggle('selected');
                const doorNum = parseInt(btn.dataset.door);
                if (selectedDoors.includes(doorNum)) {
                    selectedDoors = selectedDoors.filter(d => d !== doorNum);
                } else {
                    selectedDoors.push(doorNum);
                }
            });
        });

        checkBtn.addEventListener('click', () => {
            const isCorrect = JSON.stringify(selectedDoors.sort()) === JSON.stringify(gameData.solution);
            if (isCorrect) {
                feedback.innerHTML = '✅ Correct ! ' + gameData.explanation;
                feedback.className = 'feedback success';
                this.gameComplete(gameData);
            } else {
                feedback.innerHTML = '❌ Incorrect. Analyse mieux les règles !';
                feedback.className = 'feedback error';
            }
        });
    }

    bindCodeGame(gameData) {
        const checkBtn = document.getElementById('check-code');
        const feedback = document.getElementById('code-feedback');

        checkBtn.addEventListener('click', () => {
            const userCode = document.getElementById('code-editor').value;
            // Vérification simplifiée - en réalité, on ferait une analyse plus poussée
            if (userCode.includes('if not nombres:') && userCode.includes('return 0')) {
                feedback.innerHTML = '✅ Correct ! Tu as ajouté la vérification de liste vide.';
                feedback.className = 'feedback success';
                this.gameComplete(gameData);
            } else {
                feedback.innerHTML = '❌ Pas tout à fait. Pense à vérifier si la liste est vide !';
                feedback.className = 'feedback error';
            }
        });
    }

    bindCybersecurityGame(gameData) {
        const feedback = document.getElementById('cyber-feedback');

        document.querySelectorAll('.attack-option').forEach(btn => {
            btn.addEventListener('click', () => {
                const selectedOption = btn.dataset.option;
                if (selectedOption === gameData.solution) {
                    feedback.innerHTML = '✅ Correct ! ' + gameData.explanation;
                    feedback.className = 'feedback success';
                    this.gameComplete(gameData);
                } else {
                    feedback.innerHTML = '❌ Incorrect. Analyse mieux les patterns !';
                    feedback.className = 'feedback error';
                }
            });
        });
    }

    bindCryptographyGame(gameData) {
        const checkBtn = document.getElementById('check-decode');
        const feedback = document.getElementById('crypto-feedback');

        checkBtn.addEventListener('click', () => {
            const answer = document.getElementById('decoded-input').value.trim();
            if (answer === gameData.decoded_message) {
                feedback.innerHTML = '✅ Correct ! Message décodé avec succès.';
                feedback.className = 'feedback success';
                this.gameComplete(gameData);
            } else {
                feedback.innerHTML = '❌ Incorrect. Essaie de décoder le Base64 !';
                feedback.className = 'feedback error';
            }
        });
    }

    bindNetworkGame(gameData) {
        const checkBtn = document.getElementById('check-analysis');
        const feedback = document.getElementById('network-feedback');

        checkBtn.addEventListener('click', () => {
            const selectedAnalysis = document.querySelector('input[name="analysis"]:checked');
            if (selectedAnalysis && selectedAnalysis.value === gameData.solution) {
                feedback.innerHTML = '✅ Correct ! ' + gameData.explanation;
                feedback.className = 'feedback success';
                this.gameComplete(gameData);
            } else {
                feedback.innerHTML = '❌ Incorrect. Analyse mieux les adresses IP !';
                feedback.className = 'feedback error';
            }
        });
    }

    gameComplete(gameData) {
        // Mettre à jour le score
        const scoreElement = document.getElementById('game-score');
        const currentScore = parseInt(scoreElement.textContent.split(': ')[1]) || 0;
        scoreElement.textContent = `Score: ${currentScore + gameData.points}`;

        // Afficher le badge
        if (gameData.badge) {
            this.showBadge(gameData.badge);
        }

        // Son de succès
        if (this.audioManager) {
            this.audioManager.playSound('success');
        }

        // Fermer le jeu après 3 secondes
        setTimeout(() => {
            this.closeGame();
        }, 3000);
    }

    showBadge(badgeName) {
        const badgeElement = document.createElement('div');
        badgeElement.className = 'badge-notification';
        badgeElement.innerHTML = `
            <div class="badge-content">
                <span class="badge-icon">🏆</span>
                <span class="badge-text">Badge débloqué: ${badgeName}</span>
            </div>
        `;

        document.body.appendChild(badgeElement);

        // Animation d'apparition
        setTimeout(() => {
            badgeElement.classList.add('show');
        }, 100);

        // Supprimer après 5 secondes
        setTimeout(() => {
            badgeElement.remove();
        }, 5000);
    }

    clearGameArea() {
        const gameArea = document.getElementById('game-area');
        if (gameArea) {
            gameArea.innerHTML = '';
        }
    }

    getGameData(gameId) {
        // Données des jeux (en réalité, on les récupérerait depuis l'API)
        const gamesData = {
            'logic_1': {
                id: 'logic_1',
                title: '🔍 Décrypte le Mot de Passe',
                description: 'Trouve le mot de passe en analysant les indices',
                type: 'logic',
                hints: [
                    'Le mot fait 6 lettres',
                    'Il contient 2 voyelles',
                    'C\'est un animal',
                    'Il commence par \'C\''
                ],
                solution: 'CHAT',
                explanation: 'C = première lettre, HAT = 3 lettres restantes, animal = CHAT',
                points: 50,
                badge: 'Déducteur'
            },
            'logic_2': {
                id: 'logic_2',
                title: '🧩 Puzzle de Portes',
                description: 'Ouvre la bonne porte en suivant la logique',
                type: 'logic',
                rules: [
                    'Porte 1 : Ouverte si nombre pair',
                    'Porte 2 : Ouverte si nombre > 10',
                    'Porte 3 : Ouverte si nombre divisible par 3'
                ],
                numbers: [6, 15, 9, 12, 7],
                solution: [1, 2, 3],
                explanation: '6 (pair), 15 (>10 et divisible par 3), 9 (divisible par 3)',
                points: 75,
                badge: 'Logique'
            },
            'code_1': {
                id: 'code_1',
                title: '💻 Débogue le Code',
                description: 'Trouve et corrige l\'erreur dans ce code Python',
                type: 'code',
                code: `def calculer_moyenne(nombres):
    total = 0
    for nombre in nombres:
        total += nombre
    return total / len(nombres)

# Test
resultat = calculer_moyenne([10, 20, 30])
print(f"Moyenne: {resultat}")`,
                error: 'Division par zéro si liste vide',
                solution: 'Ajouter une vérification de liste vide',
                points: 60,
                badge: 'Débogueur'
            },
            'cyber_1': {
                id: 'cyber_1',
                title: '🛡️ Détecte l\'Attaque',
                description: 'Identifie le type d\'attaque dans ces logs',
                type: 'cybersecurity',
                logs: [
                    '192.168.1.100 - - [GET /admin HTTP/1.1] 404',
                    '192.168.1.100 - - [GET /admin.php HTTP/1.1] 404',
                    '192.168.1.100 - - [GET /administrator HTTP/1.1] 404',
                    '192.168.1.100 - - [GET /wp-admin HTTP/1.1] 404'
                ],
                options: ['DDoS', 'Brute Force', 'Directory Traversal', 'SQL Injection'],
                solution: 'Directory Traversal',
                explanation: 'L\'attaquant teste différents chemins d\'administration',
                points: 70,
                badge: 'Détective'
            },
            'crypto_1': {
                id: 'crypto_1',
                title: '🔐 Décode le Message',
                description: 'Décode ce message crypté en Base64',
                type: 'cryptography',
                encoded_message: 'SGVsbG8gQXJrYWxpYQ==',
                decoded_message: 'Hello Arkalia',
                points: 80,
                badge: 'Cryptographe'
            },
            'network_1': {
                id: 'network_1',
                title: '🌐 Analyse le Réseau',
                description: 'Analyse ces adresses IP et identifie leur type',
                type: 'network',
                ips: ['192.168.1.1', '8.8.8.8', '127.0.0.1', '10.0.0.1'],
                solution: 'private',
                explanation: 'La plupart sont des IP privées (192.168.x.x, 10.x.x.x)',
                points: 65,
                badge: 'Analyste Réseau'
            }
        };

        return gamesData[gameId];
    }
}

// Initialiser l'interface des mini-jeux
document.addEventListener('DOMContentLoaded', () => {
    window.miniGamesInterface = new MiniGamesInterface();
});

// Fonction globale pour ouvrir un mini-jeu
function openMiniGame(gameId) {
    if (window.miniGamesInterface) {
        window.miniGamesInterface.openGame(gameId);
    }
}
