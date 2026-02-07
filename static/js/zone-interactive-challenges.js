/* ===== ARKALIA QUEST - ZONE INTERACTIVE CHALLENGES ===== */
/* Micro-défis interactifs dans chaque zone pour enrichir le gameplay */

class ZoneInteractiveChallenges {
    constructor() {
        this.activeChallenges = new Map();
        this.challengeHistory = [];
        this.init();
    }

    init() {
        this.setupZoneChallenges();
        this.setupEventListeners();
        // console.log('🎯 Zone Interactive Challenges initialisé');
    }

    setupZoneChallenges() {
        // Défis par zone
        this.zoneChallenges = {
            'base': [
                {
                    id: 'memory_sequence',
                    name: 'Séquence de Mémoire',
                    description: 'Mémorisez la séquence de couleurs',
                    type: 'memory',
                    difficulty: 'facile',
                    reward: { xp: 50, coins: 15 }
                },
                {
                    id: 'code_breaker',
                    name: 'Cassage de Code',
                    description: 'Décryptez le code d\'accès',
                    type: 'puzzle',
                    difficulty: 'moyen',
                    reward: { xp: 75, coins: 25 }
                }
            ],
            'station_nexus': [
                {
                    id: 'hacking_mini_game',
                    name: 'Mini-Hack',
                    description: 'Infiltrez le système de sécurité',
                    type: 'hacking',
                    difficulty: 'moyen',
                    reward: { xp: 100, coins: 30 }
                },
                {
                    id: 'pattern_recognition',
                    name: 'Reconnaissance de Motifs',
                    description: 'Trouvez le motif dans les données',
                    type: 'puzzle',
                    difficulty: 'difficile',
                    reward: { xp: 150, coins: 50 }
                }
            ],
            'atelier_luna': [
                {
                    id: 'luna_communication',
                    name: 'Communication avec LUNA',
                    description: 'Résolvez l\'énigme de LUNA',
                    type: 'social',
                    difficulty: 'facile',
                    reward: { xp: 60, coins: 20 }
                },
                {
                    id: 'system_repair',
                    name: 'Réparation Système',
                    description: 'Réparez le système de LUNA',
                    type: 'technical',
                    difficulty: 'moyen',
                    reward: { xp: 120, coins: 40 }
                }
            ],
            'coeur_pandora': [
                {
                    id: 'final_boss_puzzle',
                    name: 'Puzzle Final',
                    description: 'Le défi ultime de Pandora',
                    type: 'puzzle',
                    difficulty: 'expert',
                    reward: { xp: 300, coins: 100 }
                }
            ]
        };
    }

    setupEventListeners() {
        // Écouter les clics sur les zones
        document.addEventListener('click', (e) => {
            const zoneElement = e.target.closest('[data-zone]');
            if (zoneElement) {
                const zoneId = zoneElement.dataset.zone;
                this.showZoneChallenges(zoneId);
            }
        });

        // Écouter les événements de progression
        document.addEventListener('arkalia:progression:update', (e) => {
            this.updateChallengeAvailability();
        });
    }

    showZoneChallenges(zoneId) {
        const challenges = this.zoneChallenges[zoneId] || [];
        if (challenges.length === 0) return;

        // Créer l'interface des défis
        const modal = this.createChallengeModal(zoneId, challenges);
        document.body.appendChild(modal);
        this.showModal(modal);
    }

    createChallengeModal(zoneId, challenges) {
        const modal = document.createElement('div');
        modal.className = 'challenge-modal';
        modal.innerHTML = `
            <div class="challenge-modal-content">
                <div class="challenge-header">
                    <h2>🎯 Défis de la Zone ${zoneId.toUpperCase()}</h2>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="challenges-list">
                    ${challenges.map(challenge => this.createChallengeCard(challenge)).join('')}
                </div>
            </div>
        `;

        // Ajouter les styles
        this.addChallengeStyles();

        // Événements
        const closeBtn = modal.querySelector('.close-modal');
        if (closeBtn) closeBtn.addEventListener('click', () => {
            this.hideModal(modal);
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.hideModal(modal);
            }
        });

        return modal;
    }

    createChallengeCard(challenge) {
        const isCompleted = this.challengeHistory.includes(challenge.id);
        const difficultyClass = `difficulty-${challenge.difficulty}`;

        return `
            <div class="challenge-card ${difficultyClass} ${isCompleted ? 'completed' : ''}" 
                 data-challenge-id="${challenge.id}">
                <div class="challenge-icon">${this.getChallengeIcon(challenge.type)}</div>
                <div class="challenge-info">
                    <h3>${challenge.name}</h3>
                    <p>${challenge.description}</p>
                    <div class="challenge-reward">
                        <span class="xp">+${challenge.reward.xp} XP</span>
                        <span class="coins">+${challenge.reward.coins} Coins</span>
                    </div>
                </div>
                <div class="challenge-actions">
                    ${isCompleted ?
                '<span class="completed-badge">✓ Complété</span>' :
                '<button class="start-challenge">Commencer</button>'
            }
                </div>
            </div>
        `;
    }

    getChallengeIcon(type) {
        const icons = {
            'memory': '🧠',
            'puzzle': '🧩',
            'hacking': '💻',
            'social': '💬',
            'technical': '🔧'
        };
        return icons[type] || '🎯';
    }

    addChallengeStyles() {
        if (document.getElementById('challenge-styles')) return;

        const style = document.createElement('style');
        style.id = 'challenge-styles';
        style.textContent = `
            .challenge-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }

            .challenge-modal.show {
                opacity: 1;
                visibility: visible;
            }

            .challenge-modal-content {
                background: rgba(9, 9, 11, 0.95);
                border: 2px solid rgba(167, 139, 250, 0.5);
                border-radius: 12px;
                padding: 20px;
                max-width: 600px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                backdrop-filter: blur(15px);
            }

            .challenge-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                color: var(--violet-lunaire);
            }

            .challenge-header h2 {
                margin: 0;
                font-family: 'IBM Plex Mono', monospace;
            }

            .close-modal {
                background: none;
                border: none;
                color: var(--argent-holographique);
                font-size: 1.5em;
                cursor: pointer;
                padding: 5px;
                border-radius: 4px;
                transition: all 0.2s ease;
            }

            .close-modal:hover {
                background: rgba(167, 139, 250, 0.2);
                color: var(--violet-lunaire);
            }

            .challenges-list {
                display: grid;
                gap: 15px;
            }

            .challenge-card {
                display: flex;
                align-items: center;
                padding: 15px;
                background: rgba(167, 139, 250, 0.1);
                border: 1px solid rgba(167, 139, 250, 0.3);
                border-radius: 8px;
                transition: all 0.3s ease;
                cursor: pointer;
            }

            .challenge-card:hover {
                background: rgba(167, 139, 250, 0.2);
                border-color: var(--violet-lunaire);
                transform: translateY(-2px);
            }

            .challenge-card.completed {
                opacity: 0.6;
                background: rgba(34, 197, 94, 0.1);
                border-color: rgba(34, 197, 94, 0.3);
            }

            .challenge-icon {
                font-size: 2em;
                margin-right: 15px;
            }

            .challenge-info {
                flex: 1;
            }

            .challenge-info h3 {
                margin: 0 0 5px 0;
                color: var(--argent-holographique);
                font-family: 'IBM Plex Mono', monospace;
            }

            .challenge-info p {
                margin: 0 0 10px 0;
                color: var(--argent-holographique);
                opacity: 0.8;
                font-size: 0.9em;
            }

            .challenge-reward {
                display: flex;
                gap: 10px;
            }

            .challenge-reward span {
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                font-weight: 600;
            }

            .challenge-reward .xp {
                background: rgba(34, 197, 94, 0.2);
                color: #22c55e;
            }

            .challenge-reward .coins {
                background: rgba(245, 158, 11, 0.2);
                color: #f59e0b;
            }

            .challenge-actions {
                margin-left: 15px;
            }

            .start-challenge {
                background: var(--violet-lunaire);
                color: #000;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.2s ease;
            }

            .start-challenge:hover {
                background: var(--bleu-spectre);
                transform: scale(1.05);
            }

            .completed-badge {
                color: #22c55e;
                font-weight: 600;
                font-size: 0.9em;
            }

            .difficulty-facile {
                border-left: 4px solid #22c55e;
            }

            .difficulty-moyen {
                border-left: 4px solid #f59e0b;
            }

            .difficulty-difficile {
                border-left: 4px solid #ef4444;
            }

            .difficulty-expert {
                border-left: 4px solid #8b5cf6;
            }
        `;

        document.head.appendChild(style);
    }

    showModal(modal) {
        modal.classList.add('show');

        // Écouter les clics sur les boutons de défi
        modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('start-challenge')) {
                const challengeCard = e.target.closest('.challenge-card');
                const challengeId = challengeCard.dataset.challengeId;
                this.startChallenge(challengeId);
                this.hideModal(modal);
            }
        });
    }

    hideModal(modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
        }, 300);
    }

    startChallenge(challengeId) {
        // Trouver le défi
        let challenge = null;
        for (const zoneChallenges of Object.values(this.zoneChallenges)) {
            challenge = zoneChallenges.find(c => c.id === challengeId);
            if (challenge) break;
        }

        if (!challenge) return;

        // Créer l'interface de défi
        const challengeInterface = this.createChallengeInterface(challenge);
        document.body.appendChild(challengeInterface);
        this.activeChallenges.set(challengeId, challengeInterface);
    }

    createChallengeInterface(challenge) {
        const interface = document.createElement('div');
        interface.className = 'challenge-interface';
        interface.innerHTML = `
            <div class="challenge-interface-content">
                <div class="challenge-header">
                    <h2>${challenge.name}</h2>
                    <button class="close-challenge">&times;</button>
                </div>
                <div class="challenge-description">
                    <p>${challenge.description}</p>
                </div>
                <div class="challenge-game-area">
                    ${this.createGameArea(challenge)}
                </div>
                <div class="challenge-controls">
                    <button class="submit-challenge">Valider</button>
                    <button class="cancel-challenge">Annuler</button>
                </div>
            </div>
        `;

        // Événements
        const closeCh = interface.querySelector('.close-challenge');
        const cancelCh = interface.querySelector('.cancel-challenge');
        const submitCh = interface.querySelector('.submit-challenge');
        if (closeCh) closeCh.addEventListener('click', () => this.endChallenge(challenge.id));
        if (cancelCh) cancelCh.addEventListener('click', () => this.endChallenge(challenge.id));
        if (submitCh) submitCh.addEventListener('click', () => this.submitChallenge(challenge));

        return interface;
    }

    createGameArea(challenge) {
        switch (challenge.type) {
            case 'memory':
                return this.createMemoryGame();
            case 'puzzle':
                return this.createPuzzleGame();
            case 'hacking':
                return this.createHackingGame();
            case 'social':
                return this.createSocialGame();
            case 'technical':
                return this.createTechnicalGame();
            default:
                return '<div class="game-placeholder">Défi en cours de développement...</div>';
        }
    }

    createMemoryGame() {
        return `
            <div class="memory-game">
                <div class="memory-sequence" id="memory-sequence"></div>
                <div class="memory-input">
                    <input type="text" id="memory-input" placeholder="Entrez la séquence...">
                </div>
                <div class="memory-timer">
                    <span id="memory-timer">10</span> secondes
                </div>
            </div>
        `;
    }

    createPuzzleGame() {
        return `
            <div class="puzzle-game">
                <div class="puzzle-grid" id="puzzle-grid">
                    <div class="puzzle-piece" data-value="1">1</div>
                    <div class="puzzle-piece" data-value="2">2</div>
                    <div class="puzzle-piece" data-value="3">3</div>
                    <div class="puzzle-piece" data-value="4">4</div>
                </div>
                <div class="puzzle-instructions">
                    Cliquez sur les pièces dans l'ordre correct
                </div>
            </div>
        `;
    }

    createHackingGame() {
        return `
            <div class="hacking-game">
                <div class="hacking-terminal">
                    <div class="terminal-line">> Connexion au système...</div>
                    <div class="terminal-line">> Recherche de vulnérabilités...</div>
                    <div class="terminal-line">> Entrez votre exploit:</div>
                    <input type="text" id="hacking-input" placeholder="exploit_command">
                </div>
                <div class="hacking-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" id="hacking-progress"></div>
                    </div>
                </div>
            </div>
        `;
    }

    createSocialGame() {
        return `
            <div class="social-game">
                <div class="character-dialogue">
                    <div class="character-avatar">🌙</div>
                    <div class="dialogue-text">
                        "J'ai besoin de ton aide pour résoudre ce problème..."
                    </div>
                </div>
                <div class="response-options">
                    <button class="response-btn" data-response="helpful">Je vais t'aider</button>
                    <button class="response-btn" data-response="logical">Explique-moi le problème</button>
                    <button class="response-btn" data-response="dismissive">Je suis occupé</button>
                </div>
            </div>
        `;
    }

    createTechnicalGame() {
        return `
            <div class="technical-game">
                <div class="system-diagram">
                    <div class="system-node" data-status="broken">Système A</div>
                    <div class="system-node" data-status="working">Système B</div>
                    <div class="system-node" data-status="broken">Système C</div>
                </div>
                <div class="repair-tools">
                    <button class="repair-btn" data-tool="diagnostic">Diagnostic</button>
                    <button class="repair-btn" data-tool="reset">Reset</button>
                    <button class="repair-btn" data-tool="patch">Patch</button>
                </div>
            </div>
        `;
    }

    submitChallenge(challenge) {
        // Simuler la validation du défi
        const success = Math.random() > 0.3; // 70% de succès

        if (success) {
            this.completeChallenge(challenge);
        } else {
            this.failChallenge(challenge);
        }
    }

    completeChallenge(challenge) {
        // Ajouter à l'historique
        this.challengeHistory.push(challenge.id);

        // Déclencher l'événement de progression
        document.dispatchEvent(new CustomEvent('arkalia:progression:update', {
            detail: {
                type: 'challenge_completed',
                challenge: challenge,
                rewards: challenge.reward
            }
        }));

        // Afficher la notification
        if (window.universalNotifications) {
            window.universalNotifications.success(
                '🎯 Défi Complété !',
                `${challenge.name} terminé avec succès ! +${challenge.reward.xp} XP, +${challenge.reward.coins} Coins`,
                { duration: 4000 }
            );
        }

        this.endChallenge(challenge.id);
    }

    failChallenge(challenge) {
        // Afficher la notification d'échec
        if (window.universalNotifications) {
            window.universalNotifications.warning(
                '❌ Défi Échoué',
                `${challenge.name} échoué. Réessayez !`,
                { duration: 3000 }
            );
        }

        this.endChallenge(challenge.id);
    }

    endChallenge(challengeId) {
        const interface = this.activeChallenges.get(challengeId);
        if (interface && interface.parentNode) {
            interface.parentNode.removeChild(interface);
        }
        this.activeChallenges.delete(challengeId);
    }

    updateChallengeAvailability() {
        // Mettre à jour la disponibilité des défis selon la progression
        // Cette méthode sera appelée quand la progression change
    }
}

// Initialiser le système
document.addEventListener('DOMContentLoaded', () => {
    window.zoneInteractiveChallenges = new ZoneInteractiveChallenges();
});

// Exporter pour utilisation globale
window.ZoneInteractiveChallenges = ZoneInteractiveChallenges;
