/**
 * Daily Challenges - Système de défis quotidiens
 * Gère les défis quotidiens et les récompenses
 */

class DailyChallenges {
    constructor() {
        this.challenges = [];
        this.completed = [];
        this.streak = 0;
        this.totalPoints = 0;
        this.isLoaded = false;

        this.init();
    }

    async init() {
        await this.loadChallenges();
        this.createUI();
        this.setupEventListeners();
        this.updateDisplay();

        console.log('🎯 Daily Challenges initialisé');
    }

    async loadChallenges() {
        try {
            const response = await fetch('/api/daily-challenges');
            if (!response.ok) throw new Error('Erreur de chargement');

            const data = await response.json();
            this.challenges = data.challenges || [];
            this.completed = data.completed || [];
            this.streak = data.streak || 0;
            this.totalPoints = data.total_points || 0;
            this.isLoaded = true;

            console.log(`📊 ${this.challenges.length} défis chargés`);
        } catch (error) {
            console.error('❌ Erreur chargement défis:', error);
            this.showError('Impossible de charger les défis quotidiens');
        }
    }

    createUI() {
        // Créer le conteneur principal
        const container = document.createElement('div');
        container.id = 'daily-challenges-container';
        container.className = 'daily-challenges-overlay';
        container.style.display = 'none';

        container.innerHTML = `
            <div class="daily-challenges-backdrop"></div>
            <div class="daily-challenges-modal">
                <div class="daily-challenges-header">
                    <h2>🎯 Défis Quotidiens</h2>
                    <button class="daily-challenges-close" onclick="dailyChallenges.close()">✕</button>
                </div>
                
                <div class="daily-challenges-stats">
                    <div class="stat-item">
                        <span class="stat-label">Série actuelle</span>
                        <span class="stat-value streak-value">${this.streak}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Points du jour</span>
                        <span class="stat-value points-value">${this.totalPoints}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Défis complétés</span>
                        <span class="stat-value completed-value">${this.completed.length}/${this.challenges.length}</span>
                    </div>
                </div>
                
                <div class="daily-challenges-list" id="challenges-list">
                    <!-- Les défis seront chargés ici -->
                </div>
                
                <div class="daily-challenges-footer">
                    <button class="btn-secondary" onclick="dailyChallenges.close()">Fermer</button>
                    <button class="btn-primary" onclick="dailyChallenges.refresh()">🔄 Actualiser</button>
                </div>
            </div>
        `;

        document.body.appendChild(container);
        this.addStyles();
    }

    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .daily-challenges-overlay {
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
            
            .daily-challenges-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(5px);
            }
            
            .daily-challenges-modal {
                position: relative;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border: 2px solid var(--primary-color, #00ff00);
                border-radius: 15px;
                padding: 20px;
                max-width: 800px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
                animation: dailyChallengesSlideIn 0.5s ease-out;
            }
            
            @keyframes dailyChallengesSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(-50px) scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .daily-challenges-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 1px solid var(--primary-color, #00ff00);
            }
            
            .daily-challenges-header h2 {
                color: var(--primary-color, #00ff00);
                margin: 0;
                font-size: 24px;
                text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
            }
            
            .daily-challenges-close {
                background: none;
                border: 1px solid #ff4444;
                color: #ff4444;
                padding: 8px 12px;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .daily-challenges-close:hover {
                background: #ff4444;
                color: white;
                box-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
            }
            
            .daily-challenges-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .stat-item {
                background: rgba(0, 255, 0, 0.1);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid var(--primary-color, #00ff00);
                text-align: center;
            }
            
            .stat-label {
                display: block;
                color: var(--text-color, #ffffff);
                font-size: 14px;
                margin-bottom: 5px;
            }
            
            .stat-value {
                display: block;
                color: var(--primary-color, #00ff00);
                font-size: 24px;
                font-weight: bold;
                text-shadow: 0 0 8px rgba(0, 255, 0, 0.5);
            }
            
            .daily-challenges-list {
                margin-bottom: 20px;
            }
            
            .challenge-item {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                transition: all 0.3s;
            }
            
            .challenge-item:hover {
                background: rgba(0, 255, 0, 0.1);
                border-color: var(--primary-color, #00ff00);
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
            }
            
            .challenge-item.completed {
                background: rgba(0, 255, 136, 0.1);
                border-color: #00ff88;
            }
            
            .challenge-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            
            .challenge-title {
                color: var(--primary-color, #00ff00);
                font-size: 18px;
                font-weight: bold;
                margin: 0;
            }
            
            .challenge-difficulty {
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }
            
            .challenge-difficulty.easy {
                background: rgba(0, 255, 0, 0.2);
                color: #00ff00;
            }
            
            .challenge-difficulty.medium {
                background: rgba(255, 255, 0, 0.2);
                color: #ffff00;
            }
            
            .challenge-difficulty.hard {
                background: rgba(255, 0, 0, 0.2);
                color: #ff4444;
            }
            
            .challenge-description {
                color: var(--text-color, #ffffff);
                margin-bottom: 10px;
                line-height: 1.5;
            }
            
            .challenge-objective {
                color: var(--secondary-color, #00ffff);
                font-style: italic;
                margin-bottom: 15px;
                padding: 10px;
                background: rgba(0, 255, 255, 0.1);
                border-radius: 5px;
                border-left: 3px solid var(--secondary-color, #00ffff);
            }
            
            .challenge-rewards {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .reward-item {
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid var(--primary-color, #00ff00);
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                color: var(--primary-color, #00ff00);
            }
            
            .challenge-actions {
                display: flex;
                gap: 10px;
            }
            
            .challenge-btn {
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
                text-transform: uppercase;
                font-size: 12px;
            }
            
            .challenge-btn.primary {
                background: linear-gradient(45deg, #00ff00, #00ffff);
                color: #000;
            }
            
            .challenge-btn.primary:hover {
                background: linear-gradient(45deg, #00ffff, #00ff00);
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
                transform: translateY(-2px);
            }
            
            .challenge-btn.secondary {
                background: transparent;
                border: 1px solid var(--primary-color, #00ff00);
                color: var(--primary-color, #00ff00);
            }
            
            .challenge-btn.secondary:hover {
                background: var(--primary-color, #00ff00);
                color: #000;
            }
            
            .challenge-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .daily-challenges-footer {
                display: flex;
                justify-content: space-between;
                gap: 10px;
            }
            
            .btn-primary, .btn-secondary {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }
            
            .btn-primary {
                background: linear-gradient(45deg, #00ff00, #00ffff);
                color: #000;
            }
            
            .btn-primary:hover {
                background: linear-gradient(45deg, #00ffff, #00ff00);
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            }
            
            .btn-secondary {
                background: transparent;
                border: 1px solid var(--primary-color, #00ff00);
                color: var(--primary-color, #00ff00);
            }
            
            .btn-secondary:hover {
                background: var(--primary-color, #00ff00);
                color: #000;
            }
            
            @media (max-width: 768px) {
                .daily-challenges-modal {
                    width: 95%;
                    padding: 15px;
                }
                
                .daily-challenges-stats {
                    grid-template-columns: 1fr;
                }
                
                .challenge-actions {
                    flex-direction: column;
                }
            }
        `;
        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Fermer avec Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen()) {
                this.close();
            }
        });

        // Fermer en cliquant sur le backdrop
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('daily-challenges-backdrop')) {
                this.close();
            }
        });
    }

    show() {
        const container = document.getElementById('daily-challenges-container');
        if (container) {
            container.style.display = 'flex';
            this.updateDisplay();
        }
    }

    close() {
        const container = document.getElementById('daily-challenges-container');
        if (container) {
            container.style.display = 'none';
        }
    }

    isOpen() {
        const container = document.getElementById('daily-challenges-container');
        return container && container.style.display === 'flex';
    }

    async refresh() {
        await this.loadChallenges();
        this.updateDisplay();
        this.showNotification('Défis actualisés !', 'success');
    }

    updateDisplay() {
        if (!this.isLoaded) return;

        // Mettre à jour les statistiques
        document.querySelector('.streak-value').textContent = this.streak;
        document.querySelector('.points-value').textContent = this.totalPoints;
        document.querySelector('.completed-value').textContent = `${this.completed.length}/${this.challenges.length}`;

        // Mettre à jour la liste des défis
        const challengesList = document.getElementById('challenges-list');
        if (challengesList) {
            challengesList.innerHTML = this.challenges.map(challenge =>
                this.createChallengeHTML(challenge)
            ).join('');
        }
    }

    createChallengeHTML(challenge) {
        const isCompleted = this.completed.includes(challenge.daily_id);
        const difficultyClass = challenge.difficulty || 'easy';

        return `
            <div class="challenge-item ${isCompleted ? 'completed' : ''}">
                <div class="challenge-header">
                    <h3 class="challenge-title">${challenge.title}</h3>
                    <span class="challenge-difficulty ${difficultyClass}">${difficultyClass}</span>
                </div>
                
                <div class="challenge-description">${challenge.description}</div>
                
                <div class="challenge-objective">
                    <strong>Objectif:</strong> ${challenge.objective}
                </div>
                
                <div class="challenge-rewards">
                    <span class="reward-item">${challenge.reward_points} points</span>
                    <span class="reward-item">${challenge.reward_badge}</span>
                </div>
                
                <div class="challenge-actions">
                    ${isCompleted ?
                '<button class="challenge-btn secondary" disabled>✅ Complété</button>' :
                `<button class="challenge-btn primary" onclick="dailyChallenges.attemptChallenge('${challenge.daily_id}')">
                            🎯 Tenter
                        </button>`
            }
                    <button class="challenge-btn secondary" onclick="dailyChallenges.showHints('${challenge.daily_id}')">
                        💡 Indices
                    </button>
                </div>
            </div>
        `;
    }

    async attemptChallenge(challengeId) {
        const challenge = this.challenges.find(c => c.daily_id === challengeId);
        if (!challenge) return;

        // Ouvrir une modal pour la réponse
        const answer = await this.promptAnswer(challenge);
        if (!answer) return;

        try {
            const response = await fetch('/api/daily-challenges/attempt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    challenge_id: challengeId,
                    answer: answer
                })
            });

            const result = await response.json();

            if (result.success) {
                if (result.correct) {
                    this.showNotification(result.message, 'success');
                    this.completed.push(challengeId);
                    this.totalPoints += result.rewards.points;
                    this.streak = result.streak;
                    this.updateDisplay();
                } else {
                    this.showNotification(result.message, 'error');
                }
            } else {
                this.showNotification(result.error || 'Erreur inconnue', 'error');
            }
        } catch (error) {
            console.error('❌ Erreur tentative défi:', error);
            this.showNotification('Erreur de connexion', 'error');
        }
    }

    async promptAnswer(challenge) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'answer-modal-overlay';
            modal.innerHTML = `
                <div class="answer-modal">
                    <h3>${challenge.title}</h3>
                    <p>${challenge.objective}</p>
                    <textarea id="challenge-answer" placeholder="Votre réponse..." rows="4"></textarea>
                    <div class="answer-modal-actions">
                        <button onclick="this.closest('.answer-modal-overlay').remove()">Annuler</button>
                        <button onclick="this.submitAnswer()">Valider</button>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            const textarea = modal.querySelector('#challenge-answer');
            textarea.focus();

            const submitBtn = modal.querySelector('button:last-child');
            submitBtn.onclick = () => {
                const answer = textarea.value.trim();
                modal.remove();
                resolve(answer);
            };

            // Fermer avec Escape
            const handleKeydown = (e) => {
                if (e.key === 'Escape') {
                    modal.remove();
                    document.removeEventListener('keydown', handleKeydown);
                    resolve(null);
                }
            };
            document.addEventListener('keydown', handleKeydown);
        });
    }

    showHints(challengeId) {
        const challenge = this.challenges.find(c => c.daily_id === challengeId);
        if (!challenge || !challenge.hints) return;

        const hints = challenge.hints.join('\n• ');
        this.showNotification(`💡 Indices:\n• ${hints}`, 'info');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            z-index: 10001;
            max-width: 300px;
            word-wrap: break-word;
            animation: notificationSlideIn 0.3s ease-out;
        `;

        const colors = {
            success: '#00ff88',
            error: '#ff4444',
            info: '#00ffff',
            warning: '#ffff00'
        };

        notification.style.background = colors[type] || colors.info;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'notificationSlideOut 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// CSS pour les notifications
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes notificationSlideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes notificationSlideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyle);

// Initialiser les défis quotidiens
const dailyChallenges = new DailyChallenges();

// Exporter pour utilisation globale
window.DailyChallenges = dailyChallenges;
