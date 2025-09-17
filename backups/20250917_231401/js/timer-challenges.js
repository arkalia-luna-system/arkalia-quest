/* ===== ARKALIA QUEST - TIMER CHALLENGES ===== */
/* Défis à timer et système de scoring */

class TimerChallenges {
    constructor() {
        this.activeChallenges = [];
        this.challengeTypes = this.initializeChallengeTypes();
        this.scoringSystem = this.initializeScoringSystem();
        this.init();
    }

    init() {
        this.setupChallengeUI();
        this.startChallengeTimer();
    }

    initializeChallengeTypes() {
        return {
            speed_hacking: {
                name: 'Hacking Rapide',
                description: 'Utilise 20 commandes en moins de 2 minutes',
                duration: 120, // secondes
                target: 20,
                points: 100,
                difficulty: 'medium'
            },
            memory_master: {
                name: 'Maître de la Mémoire',
                description: 'Mémorise 15 séquences en 3 minutes',
                duration: 180,
                target: 15,
                points: 150,
                difficulty: 'hard'
            },
            zone_explorer: {
                name: 'Explorateur Express',
                description: 'Explore 5 zones en 5 minutes',
                duration: 300,
                target: 5,
                points: 200,
                difficulty: 'easy'
            }
        };
    }

    initializeScoringSystem() {
        return {
            basePoints: 100,
            timeBonus: 0.1, // points par seconde restante
            accuracyBonus: 0.2, // points par pourcentage de précision
            difficultyMultiplier: {
                easy: 1.0,
                medium: 1.5,
                hard: 2.0
            }
        };
    }

    startChallenge(challengeType) {
        const challenge = this.challengeTypes[challengeType];
        if (!challenge) return;

        const challengeInstance = {
            id: Date.now(),
            type: challengeType,
            ...challenge,
            startTime: Date.now(),
            progress: 0,
            completed: false,
            score: 0
        };

        this.activeChallenges.push(challengeInstance);
        this.updateChallengeUI();
        this.showChallengeStart(challengeInstance);
    }

    updateChallengeProgress(challengeId, increment = 1) {
        const challenge = this.activeChallenges.find(c => c.id === challengeId);
        if (!challenge || challenge.completed) return;

        challenge.progress += increment;

        if (challenge.progress >= challenge.target) {
            this.completeChallenge(challenge);
        }

        this.updateChallengeUI();
    }

    completeChallenge(challenge) {
        const timeElapsed = (Date.now() - challenge.startTime) / 1000;
        const timeRemaining = Math.max(0, challenge.duration - timeElapsed);

        // Calculer le score
        const timeBonus = timeRemaining * this.scoringSystem.timeBonus;
        const accuracy = (challenge.progress / challenge.target) * 100;
        const accuracyBonus = accuracy * this.scoringSystem.accuracyBonus;
        const difficultyMultiplier = this.scoringSystem.difficultyMultiplier[challenge.difficulty];

        challenge.score = Math.floor(
            (challenge.points + timeBonus + accuracyBonus) * difficultyMultiplier
        );

        challenge.completed = true;
        challenge.completionTime = timeElapsed;

        this.showChallengeCompletion(challenge);
        this.updateChallengeUI();
    }

    showChallengeStart(challenge) {
        const modal = document.createElement('div');
        modal.className = 'challenge-start-modal';
        modal.innerHTML = `
            <div class="challenge-start-content">
                <div class="challenge-icon">⏱️</div>
                <h3>${challenge.name}</h3>
                <p>${challenge.description}</p>
                <div class="challenge-timer">
                    <span class="timer-display">${this.formatTime(challenge.duration)}</span>
                </div>
                <div class="challenge-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <span class="progress-text">0/${challenge.target}</span>
                </div>
                <button class="challenge-btn" onclick="timerChallenges.startChallengeTimer('${challenge.id}')">
                    Commencer !
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
    }

    startChallengeTimer(challengeId) {
        const challenge = this.activeChallenges.find(c => c.id === challengeId);
        if (!challenge) return;

        const modal = document.querySelector('.challenge-start-modal');
        if (modal) {
            modal.remove();
        }

        // Démarrer le timer
        challenge.timerInterval = setInterval(() => {
            this.updateChallengeTimer(challenge);
        }, 1000);
    }

    updateChallengeTimer(challenge) {
        const timeElapsed = (Date.now() - challenge.startTime) / 1000;
        const timeRemaining = Math.max(0, challenge.duration - timeElapsed);

        if (timeRemaining <= 0) {
            this.endChallenge(challenge);
            return;
        }

        // Mettre à jour l'affichage du timer
        const timerDisplay = document.querySelector(`[data-challenge-id="${challenge.id}"] .timer-display`);
        if (timerDisplay) {
            timerDisplay.textContent = this.formatTime(timeRemaining);
        }
    }

    endChallenge(challenge) {
        clearInterval(challenge.timerInterval);

        if (!challenge.completed) {
            this.showChallengeFailure(challenge);
        }
    }

    showChallengeCompletion(challenge) {
        const modal = document.createElement('div');
        modal.className = 'challenge-completion-modal';
        modal.innerHTML = `
            <div class="challenge-completion-content">
                <div class="completion-icon">🎉</div>
                <h3>Défi Réussi !</h3>
                <p>${challenge.name}</p>
                <div class="completion-stats">
                    <div class="stat">
                        <span class="stat-label">Score:</span>
                        <span class="stat-value">${challenge.score}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Temps:</span>
                        <span class="stat-value">${this.formatTime(challenge.completionTime)}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Précision:</span>
                        <span class="stat-value">${Math.round((challenge.progress / challenge.target) * 100)}%</span>
                    </div>
                </div>
                <button class="challenge-btn" onclick="timerChallenges.closeModal()">
                    Continuer
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
    }

    showChallengeFailure(challenge) {
        const modal = document.createElement('div');
        modal.className = 'challenge-failure-modal';
        modal.innerHTML = `
            <div class="challenge-failure-content">
                <div class="failure-icon">⏰</div>
                <h3>Temps Écoulé !</h3>
                <p>${challenge.name}</p>
                <div class="failure-stats">
                    <div class="stat">
                        <span class="stat-label">Progression:</span>
                        <span class="stat-value">${challenge.progress}/${challenge.target}</span>
                    </div>
                </div>
                <button class="challenge-btn" onclick="timerChallenges.retryChallenge('${challenge.id}')">
                    Réessayer
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
    }

    retryChallenge(challengeId) {
        const challenge = this.activeChallenges.find(c => c.id === challengeId);
        if (!challenge) return;

        // Réinitialiser le défi
        challenge.startTime = Date.now();
        challenge.progress = 0;
        challenge.completed = false;
        challenge.score = 0;

        this.closeModal();
        this.showChallengeStart(challenge);
    }

    closeModal() {
        const modals = document.querySelectorAll('.challenge-start-modal, .challenge-completion-modal, .challenge-failure-modal');
        modals.forEach(modal => modal.remove());
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    setupChallengeUI() {
        // Créer l'interface des défis
        this.createChallengePanel();
    }

    createChallengePanel() {
        if (document.getElementById('challenge-panel')) return;

        const panel = document.createElement('div');
        panel.id = 'challenge-panel';
        panel.className = 'challenge-panel';
        panel.innerHTML = `
            <div class="challenge-header">
                <h3>⏱️ Défis à Timer</h3>
                <button class="close-challenge-btn" onclick="timerChallenges.togglePanel()">×</button>
            </div>
            <div class="challenge-content">
                <div class="challenge-types">
                    ${Object.entries(this.challengeTypes).map(([key, challenge]) => `
                        <div class="challenge-type" onclick="timerChallenges.startChallenge('${key}')">
                            <div class="challenge-type-icon">⏱️</div>
                            <h4>${challenge.name}</h4>
                            <p>${challenge.description}</p>
                            <div class="challenge-info">
                                <span class="difficulty ${challenge.difficulty}">${challenge.difficulty}</span>
                                <span class="points">${challenge.points} pts</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(panel);
    }

    updateChallengeUI() {
        // Mettre à jour l'affichage des défis actifs
        const activeChallenges = document.querySelector('.active-challenges');
        if (!activeChallenges) return;

        activeChallenges.innerHTML = this.activeChallenges.map(challenge => `
            <div class="active-challenge" data-challenge-id="${challenge.id}">
                <div class="challenge-name">${challenge.name}</div>
                <div class="challenge-timer">
                    <span class="timer-display">${this.formatTime(challenge.duration)}</span>
                </div>
                <div class="challenge-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${(challenge.progress / challenge.target) * 100}%"></div>
                    </div>
                    <span class="progress-text">${challenge.progress}/${challenge.target}</span>
                </div>
            </div>
        `).join('');
    }

    togglePanel() {
        const panel = document.getElementById('challenge-panel');
        if (panel) {
            panel.classList.toggle('show');
        }
    }

    startChallengeTimer() {
        // Timer global pour les défis actifs
        setInterval(() => {
            this.activeChallenges.forEach(challenge => {
                if (challenge.timerInterval) {
                    this.updateChallengeTimer(challenge);
                }
            });
        }, 1000);
    }
}

// CSS pour les défis à timer
const style = document.createElement('style');
style.textContent = `
    .challenge-panel {
        position: fixed;
        top: 20px;
        left: 20px;
        width: 400px;
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 20px;
        z-index: 10000;
        backdrop-filter: blur(15px);
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .challenge-panel.show {
        transform: translateX(0);
    }
    
    .challenge-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .challenge-header h3 {
        color: var(--violet-lunaire);
        margin: 0;
    }
    
    .close-challenge-btn {
        background: none;
        border: none;
        color: var(--argent-holographique);
        font-size: 1.5em;
        cursor: pointer;
        transition: color 0.3s ease;
    }
    
    .close-challenge-btn:hover {
        color: var(--violet-lunaire);
    }
    
    .challenge-type {
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .challenge-type:hover {
        border-color: rgba(167, 139, 250, 0.4);
        transform: translateY(-2px);
    }
    
    .challenge-type-icon {
        font-size: 2em;
        margin-bottom: 10px;
    }
    
    .challenge-type h4 {
        color: var(--violet-lunaire);
        margin: 0 0 10px 0;
    }
    
    .challenge-type p {
        color: var(--argent-holographique);
        font-size: 0.9em;
        margin: 0 0 15px 0;
        line-height: 1.4;
    }
    
    .challenge-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .difficulty {
        padding: 4px 8px;
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
    
    .points {
        color: var(--bleu-spectre);
        font-weight: 600;
    }
    
    .challenge-start-modal,
    .challenge-completion-modal,
    .challenge-failure-modal {
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
    
    .challenge-start-modal.show,
    .challenge-completion-modal.show,
    .challenge-failure-modal.show {
        opacity: 1;
    }
    
    .challenge-start-content,
    .challenge-completion-content,
    .challenge-failure-content {
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        max-width: 400px;
        width: 90%;
        backdrop-filter: blur(15px);
    }
    
    .challenge-icon,
    .completion-icon,
    .failure-icon {
        font-size: 3em;
        margin-bottom: 20px;
    }
    
    .challenge-timer {
        margin: 20px 0;
        font-size: 2em;
        font-family: 'IBM Plex Mono', monospace;
        color: var(--violet-lunaire);
    }
    
    .challenge-progress {
        margin: 20px 0;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: rgba(167, 139, 250, 0.2);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 10px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .progress-text {
        color: var(--argent-holographique);
        font-size: 0.9em;
        font-family: 'IBM Plex Mono', monospace;
    }
    
    .challenge-btn {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.2), rgba(96, 165, 250, 0.2));
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 8px;
        padding: 12px 24px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1em;
        font-weight: 500;
        margin-top: 20px;
    }
    
    .challenge-btn:hover {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.4), rgba(96, 165, 250, 0.4));
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(167, 139, 250, 0.3);
    }
    
    .completion-stats,
    .failure-stats {
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
`;
document.head.appendChild(style);

// Initialiser le système de défis à timer
document.addEventListener('DOMContentLoaded', () => {
    window.timerChallenges = new TimerChallenges();
});

// Exporter pour utilisation globale
window.TimerChallenges = TimerChallenges;
