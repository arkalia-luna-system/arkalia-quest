/* ===== ARKALIA QUEST - INTERACTIVE PUZZLES ===== */
/* Énigmes et puzzles interactifs pour enrichir le gameplay */

class InteractivePuzzles {
    constructor() {
        this.puzzles = this.initializePuzzles();
        this.activePuzzle = null;
        this.puzzleHistory = [];
        this.init();
    }

    init() {
        this.setupPuzzleUI();
        this.loadPuzzleHistory();
    }

    initializePuzzles() {
        return {
            // Puzzles de logique
            logic: {
                binary_sequence: {
                    name: 'Séquence Binaire',
                    description: 'Trouve la prochaine valeur dans la séquence binaire',
                    type: 'sequence',
                    difficulty: 'medium',
                    data: {
                        sequence: [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
                        answer: 0,
                        explanation: 'Chaque groupe de 1 est suivi d\'un 0, et le nombre de 1 augmente de 1 à chaque groupe'
                    }
                },
                pattern_recognition: {
                    name: 'Reconnaissance de Motif',
                    description: 'Identifie le motif dans la grille',
                    type: 'pattern',
                    difficulty: 'hard',
                    data: {
                        grid: [
                            ['A', 'B', 'C', 'D'],
                            ['B', 'C', 'D', 'A'],
                            ['C', 'D', 'A', 'B'],
                            ['D', 'A', 'B', 'C']
                        ],
                        answer: 'D',
                        explanation: 'Chaque ligne est décalée d\'une position vers la droite par rapport à la précédente'
                    }
                }
            },

            // Puzzles de cryptographie
            cryptography: {
                caesar_cipher: {
                    name: 'Chiffre de César',
                    description: 'Déchiffre le message avec un décalage de 3',
                    type: 'cipher',
                    difficulty: 'easy',
                    data: {
                        encrypted: 'KDUH',
                        shift: 3,
                        answer: 'HACK',
                        explanation: 'Chaque lettre est décalée de 3 positions vers la gauche dans l\'alphabet'
                    }
                },
                substitution: {
                    name: 'Substitution',
                    description: 'Trouve la clé de substitution',
                    type: 'cipher',
                    difficulty: 'hard',
                    data: {
                        encrypted: 'XLI GSQI',
                        key: { 'X': 'T', 'L': 'H', 'I': 'E', 'G': 'A', 'S': 'R', 'Q': 'O' },
                        answer: 'THE HERO',
                        explanation: 'Chaque lettre est remplacée par une autre selon une table de substitution'
                    }
                }
            },

            // Puzzles de réseau
            network: {
                routing: {
                    name: 'Routage de Paquets',
                    description: 'Trouve le chemin le plus court entre deux nœuds',
                    type: 'graph',
                    difficulty: 'medium',
                    data: {
                        nodes: ['A', 'B', 'C', 'D', 'E'],
                        connections: [
                            ['A', 'B', 4],
                            ['A', 'C', 2],
                            ['B', 'D', 5],
                            ['C', 'D', 1],
                            ['C', 'E', 3],
                            ['D', 'E', 2]
                        ],
                        start: 'A',
                        end: 'E',
                        answer: ['A', 'C', 'E'],
                        explanation: 'Le chemin le plus court passe par C avec un coût total de 5'
                    }
                }
            },

            // Puzzles de cybersécurité
            cybersecurity: {
                password_cracking: {
                    name: 'Cracking de Mot de Passe',
                    description: 'Trouve le mot de passe en analysant les indices',
                    type: 'password',
                    difficulty: 'medium',
                    data: {
                        hints: [
                            'Contient 8 caractères',
                            'Commence par une majuscule',
                            'Se termine par un chiffre',
                            'Contient le mot "HACK"',
                            'Le 5ème caractère est un symbole'
                        ],
                        answer: 'HACK3R!',
                        explanation: 'Le mot de passe respecte tous les critères de sécurité'
                    }
                }
            }
        };
    }

    startPuzzle(category, puzzleId) {
        const puzzle = this.puzzles[category]?.[puzzleId];
        if (!puzzle) return;

        this.activePuzzle = {
            ...puzzle,
            id: puzzleId,
            category: category,
            startTime: Date.now(),
            attempts: 0,
            hints: 0,
            completed: false
        };

        this.showPuzzleInterface();
    }

    showPuzzleInterface() {
        const modal = document.createElement('div');
        modal.className = 'puzzle-modal';
        modal.innerHTML = `
            <div class="puzzle-content">
                <div class="puzzle-header">
                    <h3>${this.activePuzzle.name}</h3>
                    <button class="close-puzzle-btn" onclick="interactivePuzzles.closePuzzle()">×</button>
                </div>
                <div class="puzzle-body">
                    <div class="puzzle-description">
                        ${this.activePuzzle.description}
                    </div>
                    <div class="puzzle-area" id="puzzle-area">
                        ${this.renderPuzzleContent()}
                    </div>
                    <div class="puzzle-actions">
                        <button class="puzzle-btn" onclick="interactivePuzzles.submitAnswer()">
                            Vérifier
                        </button>
                        <button class="puzzle-btn secondary" onclick="interactivePuzzles.getHint()">
                            Indice (${this.activePuzzle.hints}/3)
                        </button>
                        <button class="puzzle-btn secondary" onclick="interactivePuzzles.resetPuzzle()">
                            Recommencer
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
    }

    renderPuzzleContent() {
        switch (this.activePuzzle.type) {
            case 'sequence':
                return this.renderSequencePuzzle();
            case 'pattern':
                return this.renderPatternPuzzle();
            case 'cipher':
                return this.renderCipherPuzzle();
            case 'graph':
                return this.renderGraphPuzzle();
            case 'password':
                return this.renderPasswordPuzzle();
            default:
                return '<p>Type de puzzle non supporté</p>';
        }
    }

    renderSequencePuzzle() {
        const sequence = this.activePuzzle.data.sequence;
        return `
            <div class="sequence-puzzle">
                <div class="sequence-display">
                    ${sequence.map((item, index) => `
                        <span class="sequence-item ${index === sequence.length - 1 ? 'last' : ''}">${item}</span>
                    `).join('')}
                    <span class="sequence-item answer">?</span>
                </div>
                <div class="sequence-input">
                    <input type="text" id="sequence-answer" placeholder="Votre réponse" maxlength="1">
                </div>
            </div>
        `;
    }

    renderPatternPuzzle() {
        const grid = this.activePuzzle.data.grid;
        return `
            <div class="pattern-puzzle">
                <div class="pattern-grid">
                    ${grid.map(row => `
                        <div class="pattern-row">
                            ${row.map(cell => `
                                <span class="pattern-cell">${cell}</span>
                            `).join('')}
                        </div>
                    `).join('')}
                </div>
                <div class="pattern-question">
                    <p>Quelle lettre devrait remplacer le "?" dans la case vide ?</p>
                    <input type="text" id="pattern-answer" placeholder="Votre réponse" maxlength="1">
                </div>
            </div>
        `;
    }

    renderCipherPuzzle() {
        const encrypted = this.activePuzzle.data.encrypted;
        return `
            <div class="cipher-puzzle">
                <div class="cipher-display">
                    <div class="encrypted-text">${encrypted}</div>
                    <div class="cipher-info">
                        <p>Décalage: ${this.activePuzzle.data.shift || 'Inconnu'}</p>
                    </div>
                </div>
                <div class="cipher-input">
                    <input type="text" id="cipher-answer" placeholder="Texte déchiffré">
                </div>
            </div>
        `;
    }

    renderGraphPuzzle() {
        const { nodes, connections, start, end } = this.activePuzzle.data;
        return `
            <div class="graph-puzzle">
                <div class="graph-display">
                    <div class="graph-nodes">
                        ${nodes.map(node => `
                            <div class="graph-node ${node === start ? 'start' : node === end ? 'end' : ''}">
                                ${node}
                            </div>
                        `).join('')}
                    </div>
                    <div class="graph-connections">
                        ${connections.map(([from, to, weight]) => `
                            <div class="connection" data-from="${from}" data-to="${to}" data-weight="${weight}">
                                ${weight}
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div class="graph-question">
                    <p>Trouve le chemin le plus court de ${start} à ${end}</p>
                    <input type="text" id="graph-answer" placeholder="Ex: A,C,E">
                </div>
            </div>
        `;
    }

    renderPasswordPuzzle() {
        const hints = this.activePuzzle.data.hints;
        return `
            <div class="password-puzzle">
                <div class="password-hints">
                    <h4>Indices :</h4>
                    <ul>
                        ${hints.map(hint => `<li>${hint}</li>`).join('')}
                    </ul>
                </div>
                <div class="password-input">
                    <input type="text" id="password-answer" placeholder="Mot de passe">
                </div>
            </div>
        `;
    }

    submitAnswer() {
        const answer = this.getAnswer();
        if (!answer) return;

        this.activePuzzle.attempts++;

        if (this.checkAnswer(answer)) {
            this.completePuzzle();
        } else {
            this.showIncorrectAnswer();
        }
    }

    getAnswer() {
        const input = document.querySelector('#sequence-answer, #pattern-answer, #cipher-answer, #graph-answer, #password-answer');
        return input ? input.value.trim() : '';
    }

    checkAnswer(answer) {
        const correctAnswer = this.activePuzzle.data.answer;

        if (Array.isArray(correctAnswer)) {
            return answer.split(',').map(a => a.trim()).join(',') === correctAnswer.join(',');
        }

        return answer.toUpperCase() === correctAnswer.toUpperCase();
    }

    completePuzzle() {
        const timeElapsed = (Date.now() - this.activePuzzle.startTime) / 1000;
        const score = this.calculateScore();

        this.activePuzzle.completed = true;
        this.activePuzzle.completionTime = timeElapsed;
        this.activePuzzle.score = score;

        this.puzzleHistory.push({ ...this.activePuzzle });
        this.savePuzzleHistory();

        this.showPuzzleCompletion();
    }

    calculateScore() {
        const baseScore = 100;
        const timeBonus = Math.max(0, 60 - this.activePuzzle.completionTime) * 2;
        const attemptPenalty = this.activePuzzle.attempts * 10;
        const hintPenalty = this.activePuzzle.hints * 15;

        return Math.max(0, baseScore + timeBonus - attemptPenalty - hintPenalty);
    }

    showPuzzleCompletion() {
        const modal = document.createElement('div');
        modal.className = 'puzzle-completion-modal';
        modal.innerHTML = `
            <div class="puzzle-completion-content">
                <div class="completion-icon">🎉</div>
                <h3>Puzzle Résolu !</h3>
                <p>${this.activePuzzle.name}</p>
                <div class="completion-stats">
                    <div class="stat">
                        <span class="stat-label">Score:</span>
                        <span class="stat-value">${this.activePuzzle.score}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Temps:</span>
                        <span class="stat-value">${this.formatTime(this.activePuzzle.completionTime)}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Tentatives:</span>
                        <span class="stat-value">${this.activePuzzle.attempts}</span>
                    </div>
                </div>
                <div class="explanation">
                    <h4>Explication :</h4>
                    <p>${this.activePuzzle.data.explanation}</p>
                </div>
                <button class="puzzle-btn" onclick="interactivePuzzles.closePuzzle()">
                    Continuer
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
    }

    showIncorrectAnswer() {
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage("Réponse incorrecte. Essaie encore !", 3000);
            window.lunaVision.setEmotion('thinking');
        }
    }

    getHint() {
        if (this.activePuzzle.hints >= 3) return;

        this.activePuzzle.hints++;

        // Afficher un indice basé sur le type de puzzle
        let hint = '';
        switch (this.activePuzzle.type) {
            case 'sequence':
                hint = 'Regarde la progression des nombres...';
                break;
            case 'pattern':
                hint = 'Observe comment les lettres se déplacent...';
                break;
            case 'cipher':
                hint = 'Chaque lettre est décalée de la même valeur...';
                break;
            case 'graph':
                hint = 'Utilise l\'algorithme de Dijkstra...';
                break;
            case 'password':
                hint = 'Combine tous les indices pour former le mot de passe...';
                break;
        }

        if (window.lunaVision) {
            window.lunaVision.showLunaMessage(hint, 4000);
            window.lunaVision.setEmotion('helpful');
        }
    }

    resetPuzzle() {
        this.activePuzzle.attempts = 0;
        this.activePuzzle.hints = 0;
        this.activePuzzle.startTime = Date.now();

        // Réinitialiser l'interface
        const puzzleArea = document.getElementById('puzzle-area');
        if (puzzleArea) {
            puzzleArea.innerHTML = this.renderPuzzleContent();
        }
    }

    closePuzzle() {
        const modals = document.querySelectorAll('.puzzle-modal, .puzzle-completion-modal');
        modals.forEach(modal => modal.remove());

        this.activePuzzle = null;
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    setupPuzzleUI() {
        this.createPuzzlePanel();
    }

    createPuzzlePanel() {
        if (document.getElementById('puzzle-panel')) return;

        const panel = document.createElement('div');
        panel.id = 'puzzle-panel';
        panel.className = 'puzzle-panel';
        panel.innerHTML = `
            <div class="puzzle-header">
                <h3>🧩 Puzzles Interactifs</h3>
                <button class="close-puzzle-btn" onclick="interactivePuzzles.togglePanel()">×</button>
            </div>
            <div class="puzzle-content">
                ${Object.entries(this.puzzles).map(([category, puzzles]) => `
                    <div class="puzzle-category">
                        <h4>${this.getCategoryName(category)}</h4>
                        <div class="puzzle-list">
                            ${Object.entries(puzzles).map(([id, puzzle]) => `
                                <div class="puzzle-item" onclick="interactivePuzzles.startPuzzle('${category}', '${id}')">
                                    <div class="puzzle-icon">${this.getPuzzleIcon(puzzle.type)}</div>
                                    <div class="puzzle-info">
                                        <h5>${puzzle.name}</h5>
                                        <p>${puzzle.description}</p>
                                        <span class="difficulty ${puzzle.difficulty}">${puzzle.difficulty}</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        document.body.appendChild(panel);
    }

    getCategoryName(category) {
        const names = {
            logic: 'Logique',
            cryptography: 'Cryptographie',
            network: 'Réseau',
            cybersecurity: 'Cybersécurité'
        };
        return names[category] || category;
    }

    getPuzzleIcon(type) {
        const icons = {
            sequence: '🔢',
            pattern: '🔍',
            cipher: '🔐',
            graph: '🕸️',
            password: '🔑'
        };
        return icons[type] || '🧩';
    }

    togglePanel() {
        const panel = document.getElementById('puzzle-panel');
        if (panel) {
            panel.classList.toggle('show');
        }
    }

    loadPuzzleHistory() {
        const saved = localStorage.getItem('puzzleHistory');
        if (saved) {
            this.puzzleHistory = JSON.parse(saved);
        }
    }

    savePuzzleHistory() {
        localStorage.setItem('puzzleHistory', JSON.stringify(this.puzzleHistory));
    }
}

// CSS pour les puzzles interactifs
const style = document.createElement('style');
style.textContent = `
    .puzzle-panel {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 400px;
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 20px;
        z-index: 10000;
        backdrop-filter: blur(15px);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .puzzle-panel.show {
        transform: translateX(0);
    }
    
    .puzzle-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .puzzle-header h3 {
        color: var(--violet-lunaire);
        margin: 0;
    }
    
    .close-puzzle-btn {
        background: none;
        border: none;
        color: var(--argent-holographique);
        font-size: 1.5em;
        cursor: pointer;
        transition: color 0.3s ease;
    }
    
    .close-puzzle-btn:hover {
        color: var(--violet-lunaire);
    }
    
    .puzzle-category {
        margin-bottom: 25px;
    }
    
    .puzzle-category h4 {
        color: var(--bleu-spectre);
        margin: 0 0 15px 0;
        font-size: 1.1em;
    }
    
    .puzzle-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .puzzle-item {
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.2);
        border-radius: 8px;
        padding: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .puzzle-item:hover {
        border-color: rgba(167, 139, 250, 0.4);
        transform: translateY(-2px);
    }
    
    .puzzle-icon {
        font-size: 1.5em;
    }
    
    .puzzle-info {
        flex: 1;
    }
    
    .puzzle-info h5 {
        color: var(--violet-lunaire);
        margin: 0 0 5px 0;
        font-size: 1em;
    }
    
    .puzzle-info p {
        color: var(--argent-holographique);
        font-size: 0.9em;
        margin: 0 0 8px 0;
        line-height: 1.3;
    }
    
    .difficulty {
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .difficulty.easy {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    
    .difficulty.medium {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
    }
    
    .difficulty.hard {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .puzzle-modal,
    .puzzle-completion-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10001;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .puzzle-modal.show,
    .puzzle-completion-modal.show {
        opacity: 1;
    }
    
    .puzzle-content,
    .puzzle-completion-content {
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 30px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        backdrop-filter: blur(15px);
    }
    
    .puzzle-body {
        margin-top: 20px;
    }
    
    .puzzle-description {
        color: var(--argent-holographique);
        font-size: 1.1em;
        margin-bottom: 25px;
        line-height: 1.4;
    }
    
    .puzzle-area {
        margin: 25px 0;
        padding: 20px;
        background: rgba(167, 139, 250, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(167, 139, 250, 0.1);
    }
    
    .sequence-puzzle {
        text-align: center;
    }
    
    .sequence-display {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.2em;
    }
    
    .sequence-item {
        padding: 8px 12px;
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 6px;
        color: var(--violet-lunaire);
    }
    
    .sequence-item.last {
        border-color: rgba(167, 139, 250, 0.6);
        background: rgba(167, 139, 250, 0.2);
    }
    
    .sequence-item.answer {
        background: rgba(96, 165, 250, 0.1);
        border-color: rgba(96, 165, 250, 0.3);
        color: var(--bleu-spectre);
    }
    
    .sequence-input input,
    .pattern-input input,
    .cipher-input input,
    .graph-input input,
    .password-input input {
        width: 100%;
        padding: 10px;
        background: rgba(9, 9, 11, 0.8);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 6px;
        color: white;
        font-size: 1em;
        text-align: center;
    }
    
    .pattern-puzzle {
        text-align: center;
    }
    
    .pattern-grid {
        display: inline-block;
        margin-bottom: 20px;
    }
    
    .pattern-row {
        display: flex;
        gap: 5px;
        margin-bottom: 5px;
    }
    
    .pattern-cell {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 4px;
        color: var(--violet-lunaire);
        font-weight: 600;
    }
    
    .cipher-puzzle {
        text-align: center;
    }
    
    .cipher-display {
        margin-bottom: 20px;
    }
    
    .encrypted-text {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.5em;
        color: var(--violet-lunaire);
        margin-bottom: 10px;
    }
    
    .cipher-info {
        color: var(--argent-holographique);
        font-size: 0.9em;
    }
    
    .graph-puzzle {
        text-align: center;
    }
    
    .graph-display {
        margin-bottom: 20px;
    }
    
    .graph-nodes {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .graph-node {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(167, 139, 250, 0.1);
        border: 2px solid rgba(167, 139, 250, 0.3);
        border-radius: 50%;
        color: var(--violet-lunaire);
        font-weight: 600;
    }
    
    .graph-node.start {
        border-color: #22c55e;
        background: rgba(34, 197, 94, 0.1);
    }
    
    .graph-node.end {
        border-color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }
    
    .password-puzzle {
        text-align: left;
    }
    
    .password-hints {
        margin-bottom: 20px;
    }
    
    .password-hints h4 {
        color: var(--violet-lunaire);
        margin-bottom: 10px;
    }
    
    .password-hints ul {
        color: var(--argent-holographique);
        padding-left: 20px;
    }
    
    .password-hints li {
        margin-bottom: 5px;
    }
    
    .puzzle-actions {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin-top: 25px;
    }
    
    .puzzle-btn {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.2), rgba(96, 165, 250, 0.2));
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 8px;
        padding: 10px 20px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9em;
        font-weight: 500;
    }
    
    .puzzle-btn:hover {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.4), rgba(96, 165, 250, 0.4));
        transform: translateY(-2px);
    }
    
    .puzzle-btn.secondary {
        background: rgba(167, 139, 250, 0.1);
        border-color: rgba(167, 139, 250, 0.2);
    }
    
    .puzzle-btn.secondary:hover {
        background: rgba(167, 139, 250, 0.2);
    }
    
    .completion-icon {
        font-size: 3em;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .completion-stats {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    
    .stat {
        text-align: center;
    }
    
    .stat-label {
        display: block;
        color: var(--argent-holographique);
        font-size: 0.9em;
        margin-bottom: 5px;
    }
    
    .stat-value {
        display: block;
        color: var(--violet-lunaire);
        font-size: 1.2em;
        font-weight: 600;
    }
    
    .explanation {
        margin: 20px 0;
        padding: 15px;
        background: rgba(167, 139, 250, 0.05);
        border-radius: 8px;
        border-left: 4px solid var(--violet-lunaire);
    }
    
    .explanation h4 {
        color: var(--violet-lunaire);
        margin: 0 0 10px 0;
    }
    
    .explanation p {
        color: var(--argent-holographique);
        margin: 0;
        line-height: 1.4;
    }
`;
document.head.appendChild(style);

// Initialiser le système de puzzles interactifs
document.addEventListener('DOMContentLoaded', () => {
    window.interactivePuzzles = new InteractivePuzzles();
});

// Exporter pour utilisation globale
window.InteractivePuzzles = InteractivePuzzles;
