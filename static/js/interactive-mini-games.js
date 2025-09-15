/**
 * Système de mini-jeux interactifs
 * Transforme les mini-jeux listés en vrais jeux jouables
 */

class InteractiveMiniGames {
    constructor() {
        this.games = {
            'logic_puzzle_1': new LogicPuzzle1(),
            'code_debug_1': new CodeDebug1(),
            'cyber_security_1': new CyberSecurity1(),
            'hacking_challenge_1': new HackingChallenge1(),
            'memory_game_1': new MemoryGame1()
        };
        
        this.currentGame = null;
        this.score = 0;
        this.level = 1;
        this.lives = 3;
        
        this.initializeSystem();
    }

    initializeSystem() {
        // Créer l'interface des mini-jeux
        this.createGameInterface();
        
        // Écouter les commandes de jeu
        this.listenForGameCommands();
        
        // Initialiser les jeux
        this.initializeGames();
    }

    createGameInterface() {
        // Créer le conteneur principal des mini-jeux
        const gameContainer = document.createElement('div');
        gameContainer.id = 'mini-games-container';
        gameContainer.className = 'mini-games-container';
        gameContainer.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            max-width: 800px;
            height: 80%;
            max-height: 600px;
            background: linear-gradient(135deg, #001100, #003300);
            border: 2px solid #00ff00;
            border-radius: 15px;
            padding: 20px;
            z-index: 10000;
            display: none;
            flex-direction: column;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        `;

        // Créer l'en-tête du jeu
        const gameHeader = document.createElement('div');
        gameHeader.className = 'game-header';
        gameHeader.innerHTML = `
            <div class="game-title">Mini-Jeu</div>
            <div class="game-stats">
                <span class="score">Score: <span id="game-score">0</span></span>
                <span class="level">Niveau: <span id="game-level">1</span></span>
                <span class="lives">Vies: <span id="game-lives">3</span></span>
            </div>
            <button class="close-game" onclick="interactiveMiniGames.closeGame()">×</button>
        `;
        gameHeader.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #00ff00;
        `;

        // Créer la zone de jeu
        const gameArea = document.createElement('div');
        gameArea.id = 'game-area';
        gameArea.className = 'game-area';
        gameArea.style.cssText = `
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #000;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        `;

        // Créer les contrôles
        const gameControls = document.createElement('div');
        gameControls.className = 'game-controls';
        gameControls.innerHTML = `
            <button onclick="interactiveMiniGames.pauseGame()">Pause</button>
            <button onclick="interactiveMiniGames.restartGame()">Recommencer</button>
            <button onclick="interactiveMiniGames.hint()">Indice</button>
        `;
        gameControls.style.cssText = `
            display: flex;
            gap: 10px;
            justify-content: center;
        `;

        // Assembler l'interface
        gameContainer.appendChild(gameHeader);
        gameContainer.appendChild(gameArea);
        gameContainer.appendChild(gameControls);
        
        document.body.appendChild(gameContainer);
    }

    listenForGameCommands() {
        // Écouter les commandes de jeu dans le terminal
        document.addEventListener('terminalCommand', (event) => {
            const command = event.detail.command.toLowerCase();
            
            if (command.startsWith('play_game ')) {
                const gameName = command.replace('play_game ', '');
                this.startGame(gameName);
            } else if (command === 'games') {
                this.showAvailableGames();
            } else if (command === 'close_game') {
                this.closeGame();
            }
        });
    }

    showAvailableGames() {
        const gameList = Object.keys(this.games).map(gameName => {
            const game = this.games[gameName];
            return `🎮 ${gameName}: ${game.description}`;
        }).join('\n');
        
        // Afficher la liste dans le terminal
        this.displayInTerminal(`Jeux disponibles:\n${gameList}`);
    }

    startGame(gameName) {
        if (!this.games[gameName]) {
            this.displayInTerminal(`❌ Jeu "${gameName}" non trouvé.`);
            return;
        }

        this.currentGame = this.games[gameName];
        this.currentGameName = gameName;
        
        // Afficher l'interface
        const container = document.getElementById('mini-games-container');
        container.style.display = 'flex';
        
        // Initialiser le jeu
        this.currentGame.init();
        this.updateGameStats();
        
        // Afficher le message de démarrage
        this.displayInTerminal(`🎮 Démarrage de ${gameName}...`);
    }

    closeGame() {
        const container = document.getElementById('mini-games-container');
        container.style.display = 'none';
        
        if (this.currentGame) {
            this.currentGame.cleanup();
            this.currentGame = null;
        }
        
        this.displayInTerminal('🎮 Jeu fermé.');
    }

    pauseGame() {
        if (this.currentGame) {
            this.currentGame.pause();
            this.displayInTerminal('⏸️ Jeu en pause.');
        }
    }

    restartGame() {
        if (this.currentGame) {
            this.currentGame.restart();
            this.updateGameStats();
            this.displayInTerminal('🔄 Jeu redémarré.');
        }
    }

    hint() {
        if (this.currentGame) {
            const hint = this.currentGame.getHint();
            this.displayInTerminal(`💡 Indice: ${hint}`);
        }
    }

    updateGameStats() {
        document.getElementById('game-score').textContent = this.score;
        document.getElementById('game-level').textContent = this.level;
        document.getElementById('game-lives').textContent = this.lives;
    }

    displayInTerminal(message) {
        // Afficher le message dans le terminal
        const terminal = document.querySelector('.terminal-output');
        if (terminal) {
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            messageElement.style.color = '#00ff00';
            terminal.appendChild(messageElement);
            terminal.scrollTop = terminal.scrollHeight;
        }
    }
}

// Classe de base pour les mini-jeux
class BaseMiniGame {
    constructor(name, description) {
        this.name = name;
        this.description = description;
        this.isRunning = false;
        this.isPaused = false;
    }

    init() {
        this.isRunning = true;
        this.isPaused = false;
    }

    pause() {
        this.isPaused = !this.isPaused;
    }

    restart() {
        this.cleanup();
        this.init();
    }

    cleanup() {
        this.isRunning = false;
        this.isPaused = false;
    }

    getHint() {
        return "Utilise ton intelligence pour résoudre ce défi !";
    }
}

// Jeu de puzzle logique
class LogicPuzzle1 extends BaseMiniGame {
    constructor() {
        super('logic_puzzle_1', 'Puzzle logique: Trouve la séquence correcte');
        this.sequence = [];
        this.userSequence = [];
        this.currentStep = 0;
    }

    init() {
        super.init();
        this.generateSequence();
        this.displayPuzzle();
    }

    generateSequence() {
        this.sequence = [];
        for (let i = 0; i < 5; i++) {
            this.sequence.push(Math.floor(Math.random() * 4) + 1);
        }
    }

    displayPuzzle() {
        const gameArea = document.getElementById('game-area');
        gameArea.innerHTML = `
            <h3>Puzzle Logique</h3>
            <p>Mémorise la séquence et reproduis-la :</p>
            <div class="sequence-display" id="sequence-display"></div>
            <div class="user-input" id="user-input">
                <button onclick="interactiveMiniGames.currentGame.selectNumber(1)">1</button>
                <button onclick="interactiveMiniGames.currentGame.selectNumber(2)">2</button>
                <button onclick="interactiveMiniGames.currentGame.selectNumber(3)">3</button>
                <button onclick="interactiveMiniGames.currentGame.selectNumber(4)">4</button>
            </div>
            <div class="game-status" id="game-status">Clique sur les boutons pour reproduire la séquence</div>
        `;

        // Afficher la séquence
        this.showSequence();
    }

    showSequence() {
        const display = document.getElementById('sequence-display');
        display.innerHTML = this.sequence.map(num => `<span class="sequence-number">${num}</span>`).join(' ');
        
        // Masquer après 3 secondes
        setTimeout(() => {
            display.innerHTML = 'Mémorisez la séquence...';
        }, 3000);
    }

    selectNumber(number) {
        this.userSequence.push(number);
        
        // Vérifier si c'est correct
        if (this.userSequence[this.currentStep] === this.sequence[this.currentStep]) {
            this.currentStep++;
            
            if (this.currentStep === this.sequence.length) {
                this.win();
            } else {
                this.updateStatus(`Correct ! Étape ${this.currentStep}/${this.sequence.length}`);
            }
        } else {
            this.lose();
        }
    }

    win() {
        this.updateStatus('🎉 Félicitations ! Vous avez gagné !');
        interactiveMiniGames.score += 100;
        interactiveMiniGames.updateGameStats();
        
        // Effet de victoire
        if (window.progressionAnimations) {
            window.progressionAnimations.createVictoryEffect(document.getElementById('game-area'));
        }
    }

    lose() {
        this.updateStatus('❌ Mauvaise séquence ! Recommencez.');
        interactiveMiniGames.lives--;
        interactiveMiniGames.updateGameStats();
        
        if (interactiveMiniGames.lives <= 0) {
            this.gameOver();
        } else {
            this.restart();
        }
    }

    gameOver() {
        this.updateStatus('💀 Game Over ! Plus de vies.');
        interactiveMiniGames.lives = 3;
        interactiveMiniGames.score = Math.max(0, interactiveMiniGames.score - 50);
        interactiveMiniGames.updateGameStats();
    }

    updateStatus(message) {
        const status = document.getElementById('game-status');
        if (status) {
            status.textContent = message;
        }
    }

    getHint() {
        return `La séquence contient ${this.sequence.length} nombres entre 1 et 4.`;
    }
}

// Jeu de débogage de code
class CodeDebug1 extends BaseMiniGame {
    constructor() {
        super('code_debug_1', 'Débogage de code: Trouve et corrige les erreurs');
        this.code = '';
        this.errors = [];
        this.userCorrections = [];
    }

    init() {
        super.init();
        this.generateCode();
        this.displayCode();
    }

    generateCode() {
        this.code = `
function calculerMoyenne(nombres) {
    let somme = 0;
    for (let i = 0; i < nombres.length; i++) {
        somme += nombres[i];
    }
    return somme / nombres.length;
}

// Erreur: variable non déclarée
console.log(calculerMoyenne([1, 2, 3, 4, 5]));
        `;
        
        this.errors = [
            { line: 2, error: 'Variable "somme" non déclarée', fix: 'let somme = 0;' },
            { line: 8, error: 'Variable "nombres" non définie', fix: 'let nombres = [1, 2, 3, 4, 5];' }
        ];
    }

    displayCode() {
        const gameArea = document.getElementById('game-area');
        gameArea.innerHTML = `
            <h3>Débogage de Code</h3>
            <p>Trouve et corrige les erreurs dans ce code :</p>
            <pre class="code-display">${this.code}</pre>
            <div class="error-list" id="error-list"></div>
            <div class="correction-input">
                <input type="text" id="correction-input" placeholder="Entrez votre correction...">
                <button onclick="interactiveMiniGames.currentGame.submitCorrection()">Corriger</button>
            </div>
            <div class="game-status" id="game-status">Trouvez les erreurs et corrigez-les !</div>
        `;

        this.displayErrors();
    }

    displayErrors() {
        const errorList = document.getElementById('error-list');
        errorList.innerHTML = this.errors.map((error, index) => 
            `<div class="error-item" data-line="${error.line}">
                Ligne ${error.line}: ${error.error}
                <span class="error-status" id="error-${index}">❌</span>
            </div>`
        ).join('');
    }

    submitCorrection() {
        const input = document.getElementById('correction-input');
        const correction = input.value.trim();
        
        if (correction) {
            // Vérifier si la correction est correcte
            const correctError = this.errors.find(error => error.fix === correction);
            
            if (correctError) {
                this.correctError(correctError);
            } else {
                this.updateStatus('❌ Correction incorrecte. Essayez encore.');
            }
            
            input.value = '';
        }
    }

    correctError(error) {
        const errorIndex = this.errors.indexOf(error);
        const errorStatus = document.getElementById(`error-${errorIndex}`);
        errorStatus.textContent = '✅';
        errorStatus.style.color = '#00ff00';
        
        this.userCorrections.push(error);
        this.updateStatus(`✅ Erreur corrigée ! ${this.userCorrections.length}/${this.errors.length}`);
        
        if (this.userCorrections.length === this.errors.length) {
            this.win();
        }
    }

    win() {
        this.updateStatus('🎉 Toutes les erreurs ont été corrigées !');
        interactiveMiniGames.score += 150;
        interactiveMiniGames.updateGameStats();
        
        if (window.progressionAnimations) {
            window.progressionAnimations.createVictoryEffect(document.getElementById('game-area'));
        }
    }

    getHint() {
        return 'Cherchez les variables non déclarées et les erreurs de syntaxe.';
    }
}

// Jeu de cybersécurité
class CyberSecurity1 extends BaseMiniGame {
    constructor() {
        super('cyber_security_1', 'Cybersécurité: Défends le système contre les attaques');
        this.threats = [];
        this.defenses = [];
        this.currentThreat = null;
    }

    init() {
        super.init();
        this.generateThreats();
        this.displayThreats();
    }

    generateThreats() {
        this.threats = [
            { name: 'Virus', description: 'Malware détecté', defense: 'Antivirus' },
            { name: 'Phishing', description: 'Email suspect', defense: 'Filtre anti-spam' },
            { name: 'DDoS', description: 'Attaque par déni de service', defense: 'Pare-feu' },
            { name: 'SQL Injection', description: 'Injection SQL détectée', defense: 'Validation des entrées' }
        ];
        
        this.defenses = ['Antivirus', 'Filtre anti-spam', 'Pare-feu', 'Validation des entrées'];
    }

    displayThreats() {
        const gameArea = document.getElementById('game-area');
        gameArea.innerHTML = `
            <h3>Cybersécurité</h3>
            <p>Défends le système contre les menaces :</p>
            <div class="threat-display" id="threat-display"></div>
            <div class="defense-options" id="defense-options"></div>
            <div class="game-status" id="game-status">Sélectionnez la bonne défense !</div>
        `;

        this.showRandomThreat();
    }

    showRandomThreat() {
        this.currentThreat = this.threats[Math.floor(Math.random() * this.threats.length)];
        const threatDisplay = document.getElementById('threat-display');
        threatDisplay.innerHTML = `
            <div class="threat-info">
                <h4>🚨 ${this.currentThreat.name}</h4>
                <p>${this.currentThreat.description}</p>
            </div>
        `;

        this.displayDefenseOptions();
    }

    displayDefenseOptions() {
        const defenseOptions = document.getElementById('defense-options');
        const shuffledDefenses = [...this.defenses].sort(() => Math.random() - 0.5);
        
        defenseOptions.innerHTML = shuffledDefenses.map(defense => 
            `<button onclick="interactiveMiniGames.currentGame.selectDefense('${defense}')">${defense}</button>`
        ).join('');
    }

    selectDefense(defense) {
        if (defense === this.currentThreat.defense) {
            this.updateStatus('✅ Menace neutralisée !');
            interactiveMiniGames.score += 75;
            interactiveMiniGames.updateGameStats();
            
            setTimeout(() => {
                this.showRandomThreat();
            }, 1000);
        } else {
            this.updateStatus('❌ Mauvaise défense ! La menace persiste.');
            interactiveMiniGames.lives--;
            interactiveMiniGames.updateGameStats();
            
            if (interactiveMiniGames.lives <= 0) {
                this.gameOver();
            }
        }
    }

    gameOver() {
        this.updateStatus('💀 Système compromis ! Game Over.');
        interactiveMiniGames.lives = 3;
        interactiveMiniGames.score = Math.max(0, interactiveMiniGames.score - 100);
        interactiveMiniGames.updateGameStats();
    }

    updateStatus(message) {
        const status = document.getElementById('game-status');
        if (status) {
            status.textContent = message;
        }
    }

    getHint() {
        return 'Chaque type de menace a une défense spécifique.';
    }
}

// Jeu de défi de hacking
class HackingChallenge1 extends BaseMiniGame {
    constructor() {
        super('hacking_challenge_1', 'Défi de hacking: Brise le code d\'accès');
        this.password = '';
        this.attempts = 0;
        this.maxAttempts = 5;
    }

    init() {
        super.init();
        this.generatePassword();
        this.displayChallenge();
    }

    generatePassword() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        this.password = '';
        for (let i = 0; i < 6; i++) {
            this.password += chars.charAt(Math.floor(Math.random() * chars.length));
        }
    }

    displayChallenge() {
        const gameArea = document.getElementById('game-area');
        gameArea.innerHTML = `
            <h3>Défi de Hacking</h3>
            <p>Brise le code d'accès de 6 caractères :</p>
            <div class="password-display" id="password-display">_ _ _ _ _ _</div>
            <div class="hacking-input">
                <input type="text" id="hacking-input" maxlength="6" placeholder="Entrez le code...">
                <button onclick="interactiveMiniGames.currentGame.submitPassword()">Hacker</button>
            </div>
            <div class="attempts">Tentatives: <span id="attempts-left">${this.maxAttempts - this.attempts}</span></div>
            <div class="game-status" id="game-status">Trouvez le code d'accès !</div>
        `;
    }

    submitPassword() {
        const input = document.getElementById('hacking-input');
        const guess = input.value.toUpperCase();
        
        if (guess.length !== 6) {
            this.updateStatus('❌ Le code doit faire 6 caractères.');
            return;
        }
        
        this.attempts++;
        
        if (guess === this.password) {
            this.win();
        } else {
            this.updatePasswordDisplay(guess);
            this.updateStatus(`❌ Code incorrect. ${this.maxAttempts - this.attempts} tentatives restantes.`);
            
            if (this.attempts >= this.maxAttempts) {
                this.lose();
            }
        }
        
        input.value = '';
    }

    updatePasswordDisplay(guess) {
        const display = document.getElementById('password-display');
        let displayText = '';
        
        for (let i = 0; i < 6; i++) {
            if (guess[i] === this.password[i]) {
                displayText += `<span style="color: #00ff00;">${guess[i]}</span> `;
            } else if (this.password.includes(guess[i])) {
                displayText += `<span style="color: #ffff00;">${guess[i]}</span> `;
            } else {
                displayText += `<span style="color: #ff0000;">${guess[i]}</span> `;
            }
        }
        
        display.innerHTML = displayText;
    }

    win() {
        this.updateStatus('🎉 Code d\'accès brisé ! Accès autorisé !');
        interactiveMiniGames.score += 200;
        interactiveMiniGames.updateGameStats();
        
        if (window.progressionAnimations) {
            window.progressionAnimations.createVictoryEffect(document.getElementById('game-area'));
        }
    }

    lose() {
        this.updateStatus('💀 Échec ! Le système a détecté l\'intrusion.');
        interactiveMiniGames.lives--;
        interactiveMiniGames.updateGameStats();
        
        if (interactiveMiniGames.lives <= 0) {
            this.gameOver();
        } else {
            this.restart();
        }
    }

    gameOver() {
        this.updateStatus('💀 Game Over ! Système verrouillé.');
        interactiveMiniGames.lives = 3;
        interactiveMiniGames.score = Math.max(0, interactiveMiniGames.score - 150);
        interactiveMiniGames.updateGameStats();
    }

    updateStatus(message) {
        const status = document.getElementById('game-status');
        if (status) {
            status.textContent = message;
        }
    }

    getHint() {
        return 'Les caractères corrects sont en vert, les caractères présents mais mal placés en jaune.';
    }
}

// Jeu de mémoire
class MemoryGame1 extends BaseMiniGame {
    constructor() {
        super('memory_game_1', 'Jeu de mémoire: Mémorise et reproduis la séquence');
        this.sequence = [];
        this.userSequence = [];
        this.currentStep = 0;
        this.showingSequence = false;
    }

    init() {
        super.init();
        this.generateSequence();
        this.displayGame();
    }

    generateSequence() {
        this.sequence = [];
        for (let i = 0; i < 4; i++) {
            this.sequence.push(Math.floor(Math.random() * 4) + 1);
        }
    }

    displayGame() {
        const gameArea = document.getElementById('game-area');
        gameArea.innerHTML = `
            <h3>Jeu de Mémoire</h3>
            <p>Mémorisez la séquence de couleurs :</p>
            <div class="memory-grid" id="memory-grid">
                <button class="memory-button" data-color="1" style="background: #ff0000;">1</button>
                <button class="memory-button" data-color="2" style="background: #00ff00;">2</button>
                <button class="memory-button" data-color="3" style="background: #0000ff;">3</button>
                <button class="memory-button" data-color="4" style="background: #ffff00;">4</button>
            </div>
            <div class="game-status" id="game-status">Préparez-vous à mémoriser !</div>
        `;

        this.showSequence();
    }

    showSequence() {
        this.showingSequence = true;
        this.updateStatus('Mémorisez la séquence...');
        
        let step = 0;
        const interval = setInterval(() => {
            if (step < this.sequence.length) {
                this.highlightButton(this.sequence[step]);
                step++;
            } else {
                clearInterval(interval);
                this.showingSequence = false;
                this.updateStatus('Reproduisez la séquence !');
            }
        }, 1000);
    }

    highlightButton(color) {
        const button = document.querySelector(`[data-color="${color}"]`);
        if (button) {
            button.style.transform = 'scale(1.2)';
            button.style.boxShadow = '0 0 20px #fff';
            
            setTimeout(() => {
                button.style.transform = 'scale(1)';
                button.style.boxShadow = 'none';
            }, 500);
        }
    }

    selectButton(color) {
        if (this.showingSequence) return;
        
        this.userSequence.push(color);
        
        if (this.userSequence[this.currentStep] === this.sequence[this.currentStep]) {
            this.currentStep++;
            
            if (this.currentStep === this.sequence.length) {
                this.win();
            } else {
                this.updateStatus(`Correct ! Étape ${this.currentStep}/${this.sequence.length}`);
            }
        } else {
            this.lose();
        }
    }

    win() {
        this.updateStatus('🎉 Séquence correcte ! Niveau suivant...');
        interactiveMiniGames.score += 125;
        interactiveMiniGames.level++;
        interactiveMiniGames.updateGameStats();
        
        setTimeout(() => {
            this.nextLevel();
        }, 2000);
    }

    lose() {
        this.updateStatus('❌ Mauvaise séquence ! Recommencez.');
        interactiveMiniGames.lives--;
        interactiveMiniGames.updateGameStats();
        
        if (interactiveMiniGames.lives <= 0) {
            this.gameOver();
        } else {
            this.restart();
        }
    }

    nextLevel() {
        this.sequence.push(Math.floor(Math.random() * 4) + 1);
        this.userSequence = [];
        this.currentStep = 0;
        this.showSequence();
    }

    gameOver() {
        this.updateStatus('💀 Game Over ! Plus de vies.');
        interactiveMiniGames.lives = 3;
        interactiveMiniGames.score = Math.max(0, interactiveMiniGames.score - 75);
        interactiveMiniGames.updateGameStats();
    }

    updateStatus(message) {
        const status = document.getElementById('game-status');
        if (status) {
            status.textContent = message;
        }
    }

    getHint() {
        return 'Concentrez-vous sur l\'ordre des couleurs qui s\'allument.';
    }
}

// Initialiser le système de mini-jeux
const interactiveMiniGames = new InteractiveMiniGames();

// Exporter pour utilisation globale
window.InteractiveMiniGames = InteractiveMiniGames;
window.interactiveMiniGames = interactiveMiniGames;
