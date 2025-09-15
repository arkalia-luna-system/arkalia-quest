/**
 * Moteur de Tutoriel Ultra-Immersif - Arkalia Quest
 * Tutoriel fun et interactif pour ados de 13 ans
 */

class TutorialEngine {
    constructor() {
        this.currentStep = 0;
        this.tutorialData = null;
        this.isActive = false;
        this.timer = null;
        this.timerElement = null;
        this.choiceContainer = null;
        this.progressContainer = null;
        this.lunaDialogue = null;
        this.playerStyle = null;
        this.init();
    }

    async init() {
        try {
            const response = await fetch('/api/tutorial/data');
            this.tutorialData = await response.json();
            // Tutoriel chargé
        } catch (error) {
            console.error('❌ Erreur chargement tutoriel:', error);
        }
    }

    startTutorial() {
        if (!this.tutorialData) {
            console.error('❌ Données tutoriel non disponibles');
            return;
        }

        this.isActive = true;
        this.currentStep = 0;
        this.showStep(0);
        // Tutoriel démarré
    }

    showStep(stepIndex) {
        if (!this.tutorialData || !this.tutorialData.tutoriel || !this.tutorialData.tutoriel.etapes) {
            console.error('❌ Données tutoriel invalides');
            return;
        }

        const step = this.tutorialData.tutoriel.etapes[stepIndex];
        if (!step) {
            console.error('❌ Étape non trouvée:', stepIndex);
            return;
        }

        this.currentStep = stepIndex;
        this.displayStep(step);
        this.setupStepInteractions(step);
    }

    displayStep(step) {
        // Créer l'interface du tutoriel
        this.createTutorialInterface();

        // Afficher le titre et la description
        const titleElement = document.getElementById('tutorialTitle');
        const descElement = document.getElementById('tutorialDescription');
        const actionElement = document.getElementById('tutorialAction');
        const buttonElement = document.getElementById('tutorialButton');

        if (titleElement) titleElement.innerHTML = step.titre;
        if (descElement) descElement.innerHTML = step.description;
        if (actionElement) actionElement.innerHTML = step.action;
        if (buttonElement) buttonElement.innerHTML = step.bouton;

        // Appliquer les effets visuels
        this.applyVisualEffects(step);

        // Afficher les choix si disponibles
        if (step.choix && step.choix.length > 0) {
            this.displayChoices(step.choix);
        }

        // Afficher le dialogue LUNA
        if (step.luna_dialogue) {
            this.displayLunaDialogue(step.luna_dialogue);
        }

        // Démarrer le timer si défini
        if (step.defi && step.defi.timer) {
            this.startTimer(step.defi.timer, step.defi.type);
        }

        // Jouer les effets sonores
        this.playStepEffects(step);
    }

    createTutorialInterface() {
        // Supprimer l'ancienne interface si elle existe
        const existingInterface = document.getElementById('tutorialInterface');
        if (existingInterface) {
            existingInterface.remove();
        }

        // Créer la nouvelle interface
        const tutorialInterface = document.createElement('div');
        tutorialInterface.id = 'tutorialInterface';
        tutorialInterface.className = 'tutorial-interface';
        tutorialInterface.innerHTML = `
            <div class="tutorial-overlay">
                <div class="tutorial-container">
                    <div class="tutorial-header">
                        <h2 id="tutorialTitle" class="tutorial-title"></h2>
                        <div id="tutorialTimer" class="tutorial-timer" style="display: none;">
                            <span id="timerValue">00:00</span>
                        </div>
                    </div>
                    
                    <div class="tutorial-content">
                        <p id="tutorialDescription" class="tutorial-description"></p>
                        <p id="tutorialAction" class="tutorial-action"></p>
                        
                        <div id="tutorialChoices" class="tutorial-choices"></div>
                        
                        <div id="tutorialProgress" class="tutorial-progress" style="display: none;">
                            <div class="progress-bar">
                                <div class="progress-fill"></div>
                            </div>
                            <div class="progress-text"></div>
                        </div>
                        
                        <div id="lunaDialogue" class="luna-dialogue">
                            <div class="luna-avatar">🌙</div>
                            <div class="luna-message"></div>
                        </div>
                        
                        <button id="tutorialButton" class="tutorial-button"></button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(tutorialInterface);

        // Stocker les références
        this.timerElement = document.getElementById('timerValue');
        this.choiceContainer = document.getElementById('tutorialChoices');
        this.progressContainer = document.getElementById('tutorialProgress');
        this.lunaDialogue = document.getElementById('lunaDialogue');
    }

    applyVisualEffects(step) {
        const tutorialInterface = document.getElementById('tutorialInterface');
        if (!tutorialInterface) return;

        // Appliquer les effets selon l'étape
        if (step.effets) {
            if (step.effets.shake) {
                tutorialInterface.classList.add('shake-effect');
                setTimeout(() => tutorialInterface.classList.remove('shake-effect'), 1000);
            }

            if (step.effets.flash) {
                tutorialInterface.classList.add('flash-effect');
                setTimeout(() => tutorialInterface.classList.remove('flash-effect'), 500);
            }

            // Effet de particules
            if (step.effets.particules) {
                this.createParticles(step.effets.particules, step.effets.couleur);
            }
        }

        // Animation d'entrée
        tutorialInterface.classList.add('fade-in');
    }

    createParticles(count, color) {
        const container = document.getElementById('tutorialInterface');
        if (!container) return;

        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'tutorial-particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: ${color};
                border-radius: 50%;
                pointer-events: none;
                animation: particleFloat 2s ease-out forwards;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            container.appendChild(particle);

            setTimeout(() => particle.remove(), 2000);
        }
    }

    displayChoices(choices) {
        if (!this.choiceContainer) return;

        this.choiceContainer.innerHTML = '';
        this.choiceContainer.style.display = 'flex';

        choices.forEach((choice, index) => {
            const choiceButton = document.createElement('button');
            choiceButton.className = `tutorial-choice choice-${choice.effet} matrix-choice`;
            choiceButton.innerHTML = `
                <div class="choice-text">${choice.texte}</div>
                <div class="choice-description">${choice.description}</div>
                <div class="choice-effect">${this.getChoiceEffectIcon(choice.effet)}</div>
            `;

            // Ajouter des effets Matrix
            choiceButton.style.background = 'linear-gradient(45deg, #00ff00, #00ff88)';
            choiceButton.style.border = '2px solid #00ff00';
            choiceButton.style.boxShadow = '0 0 15px rgba(0, 255, 0, 0.4)';

            choiceButton.addEventListener('click', () => {
                this.handleChoice(choice, index);
            });

            // Animation d'entrée Matrix
            choiceButton.style.opacity = '0';
            choiceButton.style.transform = 'translateY(20px)';
            setTimeout(() => {
                choiceButton.style.transition = 'all 0.3s ease';
                choiceButton.style.opacity = '1';
                choiceButton.style.transform = 'translateY(0)';
            }, index * 100);

            this.choiceContainer.appendChild(choiceButton);
        });
    }

    getChoiceEffectIcon(effect) {
        const icons = {
            'epic': '🚀',
            'stealth': '🕵️',
            'smooth': '✨',
            'hack': '💻',
            'matrix': '🌐'
        };
        return icons[effect] || '🎯';
    }

    handleChoice(choice, index) {
        // Choix sélectionné

        // Effet visuel du choix
        const buttons = this.choiceContainer.querySelectorAll('.tutorial-choice');
        buttons.forEach((btn, i) => {
            if (i === index) {
                btn.classList.add('selected');
            } else {
                btn.classList.add('disabled');
            }
        });

        // Jouer le son selon l'effet
        if (window.audioManager) {
            switch (choice.effet) {
                case 'epic':
                    window.audioManager.playSound('easterSound');
                    break;
                case 'stealth':
                    window.audioManager.playSound('hack');
                    break;
                case 'smooth':
                    window.audioManager.playSound('success');
                    break;
                default:
                    window.audioManager.playSound('buttonSound');
            }
        }

        // Stocker le style du joueur
        if (choice.action.startsWith('mode_')) {
            this.playerStyle = choice.action;
        }

        // Continuer vers l'étape suivante après un délai
        setTimeout(() => {
            this.nextStep();
        }, 1500);
    }

    displayLunaDialogue(dialogue) {
        if (!this.lunaDialogue) return;

        const messageElement = this.lunaDialogue.querySelector('.luna-message');
        if (!messageElement) return;

        // Afficher le message initial
        messageElement.innerHTML = dialogue.avant;

        // Appliquer la personnalité
        this.applyLunaPersonality(dialogue.personnalite);
    }

    applyLunaPersonality(personality) {
        if (!this.lunaDialogue) return;

        const personalityData = this.tutorialData.tutoriel.personnalites[personality];
        if (!personalityData) return;

        // Changer la couleur
        this.lunaDialogue.style.setProperty('--luna-color', personalityData.couleur);

        // Ajouter des emojis aléatoires
        const emoji = personalityData.emojis[Math.floor(Math.random() * personalityData.emojis.length)];
        const avatar = this.lunaDialogue.querySelector('.luna-avatar');
        if (avatar) {
            avatar.textContent = emoji;
        }
    }

    startTimer(duration, type) {
        const timerContainer = document.getElementById('tutorialTimer');
        if (!timerContainer || !this.timerElement) return;

        timerContainer.style.display = 'block';
        let timeLeft = duration;

        this.timer = setInterval(() => {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            this.timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

            // Changement de couleur selon le temps restant
            if (timeLeft <= 5) {
                this.timerElement.style.color = '#ff0000';
                this.timerElement.style.animation = 'pulse 0.5s infinite';
            } else if (timeLeft <= 10) {
                this.timerElement.style.color = '#ff6600';
            }

            if (timeLeft <= 0) {
                this.handleTimerExpired(type);
            }
        }, 1000);
    }

    handleTimerExpired(type) {
        clearInterval(this.timer);

        if (type === 'survie') {
            // Game Over
            this.showGameOver();
        } else {
            // Continuer mais avec pénalité
            this.showTimerExpired();
        }
    }

    showGameOver() {
        const tutorialInterface = document.getElementById('tutorialInterface');
        if (!tutorialInterface) return;

        tutorialInterface.innerHTML = `
            <div class="game-over">
                <h2>💀 GAME OVER</h2>
                <p>La Corp t'a repéré ! Tu dois recommencer !</p>
                <button onclick="tutorialEngine.restartTutorial()" class="restart-button">🔄 RECOMMENCER</button>
            </div>
        `;
    }

    showTimerExpired() {
        const tutorialInterface = document.getElementById('tutorialInterface');
        if (!tutorialInterface) return;

        tutorialInterface.innerHTML = `
            <div class="timer-expired">
                <h2>⏰ TEMPS ÉCOULÉ</h2>
                <p>Tu as été trop lent ! Mais on continue quand même...</p>
                <button onclick="tutorialEngine.nextStep()" class="continue-button">➡️ CONTINUER</button>
            </div>
        `;
    }

    setupStepInteractions(step) {
        const button = document.getElementById('tutorialButton');
        if (!button) return;

        button.onclick = () => {
            this.executeStepCommand(step);
        };
    }

    async executeStepCommand(step) {
        if (!step.commande) return;

        // Exécution commande tutoriel

        try {
            const response = await fetch('/commande', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cmd: step.commande })
            });

            const data = await response.json();

            if (data.reponse && data.reponse.réussite) {
                this.handleStepSuccess(step, data.reponse);
            } else {
                this.handleStepError(step);
            }
        } catch (error) {
            console.error('❌ Erreur commande tutoriel:', error);
            this.handleStepError(step);
        }
    }

    handleStepSuccess(step, response) {
        // Étape réussie

        // Jouer le son de succès
        if (window.audioManager) {
            window.audioManager.playSound('success');
        }

        // Afficher la réponse LUNA
        if (step.luna_dialogue && step.luna_dialogue.apres) {
            const messageElement = this.lunaDialogue.querySelector('.luna-message');
            if (messageElement) {
                messageElement.innerHTML = step.luna_dialogue.apres;
            }
        }

        // Afficher les récompenses
        if (response.badge) {
            this.showReward(response.badge);
        }

        // Continuer vers l'étape suivante
        setTimeout(() => {
            this.nextStep();
        }, 2000);
    }

    handleStepError(step) {
        // Étape échouée

        // Jouer le son d'erreur
        if (window.audioManager) {
            window.audioManager.playSound('error');
        }

        // Afficher le message d'erreur LUNA
        if (step.luna_dialogue && step.luna_dialogue.reactions && step.luna_dialogue.reactions.error) {
            const messageElement = this.lunaDialogue.querySelector('.luna-message');
            if (messageElement) {
                messageElement.innerHTML = step.luna_dialogue.reactions.error;
            }
        }
    }

    showReward(badge) {
        const rewardElement = document.createElement('div');
        rewardElement.className = 'reward-notification';
        rewardElement.innerHTML = `
            <div class="reward-content">
                <div class="reward-icon">🏆</div>
                <div class="reward-text">
                    <h3>Nouveau Badge !</h3>
                    <p>${badge}</p>
                </div>
            </div>
        `;

        document.body.appendChild(rewardElement);

        setTimeout(() => {
            rewardElement.remove();
        }, 3000);
    }

    nextStep() {
        if (!this.tutorialData || !this.tutorialData.tutoriel.etapes) return;

        const nextIndex = this.currentStep + 1;
        if (nextIndex < this.tutorialData.tutoriel.etapes.length) {
            this.showStep(nextIndex);
        } else {
            this.completeTutorial();
        }
    }

    completeTutorial() {
        // Tutoriel terminé

        const tutorialInterface = document.getElementById('tutorialInterface');
        if (!tutorialInterface) return;

        tutorialInterface.innerHTML = `
            <div class="tutorial-complete">
                <h2>🏆 FÉLICITATIONS !</h2>
                <p>Tu as terminé le tutoriel ! Tu es maintenant un vrai hacker !</p>
                <div class="completion-rewards">
                    <div class="reward">🎓 Badge Hacker Débutant</div>
                    <div class="reward">🌙 Badge Contacté</div>
                    <div class="reward">💻 Badge Hack Système</div>
                    <div class="reward">⭐ 500 points</div>
                    <div class="reward">📈 Niveau 2</div>
                </div>
                <button onclick="tutorialEngine.closeTutorial()" class="complete-button">🎮 COMMENCER L'AVENTURE</button>
            </div>
        `;
    }

    closeTutorial() {
        const tutorialInterface = document.getElementById('tutorialInterface');
        if (tutorialInterface) {
            tutorialInterface.remove();
        }
        this.isActive = false;
        // Tutoriel fermé
    }

    restartTutorial() {
        this.startTutorial();
    }

    playStepEffects(step) {
        if (!step.effets || !window.audioManager) return;

        // Jouer le son principal
        if (step.effets.son) {
            window.audioManager.playSound(step.effets.son);
        }
    }
}

// Instance globale - DÉSACTIVÉE
// window.tutorialEngine = new TutorialEngine();

// Fonction pour démarrer le tutoriel depuis l'interface - DÉSACTIVÉE
window.startTutorial = function () {
    console.log('🎓 Tutoriel désactivé - utilise les systèmes universels');
    if (window.universalNotifications) {
        window.universalNotifications.info('🎓 Tutoriel désactivé - explore librement !');
    }
};

// Styles CSS pour le tutoriel
const tutorialStyles = `
<style>
.tutorial-interface {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.5s ease-out;
}

.tutorial-overlay {
    background: linear-gradient(135deg, #000 0%, #001a00 50%, #000 100%);
    border: 2px solid #00ff00;
    border-radius: 15px;
    padding: 30px;
    max-width: 600px;
    width: 90%;
    box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
    position: relative;
    overflow: hidden;
}

.tutorial-overlay::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(0, 255, 0, 0.1) 50%, transparent 70%);
    animation: scan 3s linear infinite;
    pointer-events: none;
}

.tutorial-title {
    color: #00ff00;
    font-size: 2em;
    text-align: center;
    margin-bottom: 20px;
    text-shadow: 0 0 10px #00ff00;
    font-family: 'Orbitron', monospace;
}

.tutorial-description {
    color: #ffffff;
    font-size: 1.2em;
    text-align: center;
    margin-bottom: 15px;
    line-height: 1.5;
}

.tutorial-action {
    color: #00ffff;
    font-size: 1.1em;
    text-align: center;
    margin-bottom: 20px;
    font-weight: bold;
}

.tutorial-button {
    background: linear-gradient(45deg, #00ff00, #00cc00);
    color: #000;
    border: none;
    padding: 15px 30px;
    font-size: 1.2em;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    text-transform: uppercase;
    transition: all 0.3s ease;
    display: block;
    margin: 20px auto;
    font-family: 'Orbitron', monospace;
}

.tutorial-button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.8);
}

.tutorial-choices {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 20px 0;
}

.tutorial-choice {
    background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
    border: 2px solid #333;
    padding: 15px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
}

.tutorial-choice:hover {
    border-color: #00ff00;
    transform: translateX(10px);
}

.tutorial-choice.selected {
    border-color: #00ff00;
    background: linear-gradient(45deg, #003300, #006600);
    transform: scale(1.05);
}

.tutorial-choice.disabled {
    opacity: 0.5;
    pointer-events: none;
}

.choice-text {
    color: #ffffff;
    font-size: 1.1em;
    font-weight: bold;
    margin-bottom: 5px;
}

.choice-description {
    color: #cccccc;
    font-size: 0.9em;
}

.luna-dialogue {
    background: rgba(0, 255, 255, 0.1);
    border: 1px solid var(--luna-color, #00ffff);
    border-radius: 10px;
    padding: 15px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    gap: 15px;
}

.luna-avatar {
    font-size: 2em;
    animation: lunaGlow 2s ease-in-out infinite alternate;
}

.luna-message {
    color: var(--luna-color, #00ffff);
    font-size: 1.1em;
    line-height: 1.4;
}

.tutorial-timer {
    background: rgba(255, 0, 0, 0.2);
    border: 2px solid #ff0000;
    border-radius: 10px;
    padding: 10px 20px;
    text-align: center;
    margin-bottom: 20px;
}

.tutorial-timer span {
    color: #ff0000;
    font-size: 1.5em;
    font-weight: bold;
    font-family: 'Share Tech Mono', monospace;
}

.tutorial-progress {
    margin: 20px 0;
}

.progress-bar {
    background: #333;
    border-radius: 10px;
    height: 20px;
    overflow: hidden;
    border: 1px solid #00ff00;
}

.progress-fill {
    background: linear-gradient(90deg, #00ff00, #00cc00);
    height: 100%;
    width: 0%;
    transition: width 0.3s ease;
    border-radius: 10px;
}

.progress-text {
    color: #00ff00;
    text-align: center;
    margin-top: 10px;
    font-weight: bold;
}

.tutorial-particle {
    position: absolute;
    pointer-events: none;
    z-index: 1000;
}

.game-over, .timer-expired, .tutorial-complete {
    text-align: center;
    color: #ffffff;
}

.game-over h2, .timer-expired h2, .tutorial-complete h2 {
    color: #ff0000;
    font-size: 2.5em;
    margin-bottom: 20px;
}

.timer-expired h2 {
    color: #ff6600;
}

.tutorial-complete h2 {
    color: #00ff00;
}

.restart-button, .continue-button, .complete-button {
    background: linear-gradient(45deg, #00ff00, #00cc00);
    color: #000;
    border: none;
    padding: 15px 30px;
    font-size: 1.2em;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    margin-top: 20px;
    font-family: 'Orbitron', monospace;
}

.completion-rewards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    margin: 20px 0;
}

.reward {
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid #00ff00;
    border-radius: 8px;
    padding: 10px;
    text-align: center;
    color: #00ff00;
    font-weight: bold;
}

.reward-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(45deg, #00ff00, #00cc00);
    color: #000;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    z-index: 10000;
    animation: slideIn 0.5s ease-out;
}

.reward-content {
    display: flex;
    align-items: center;
    gap: 10px;
}

.reward-icon {
    font-size: 2em;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes scan {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes lunaGlow {
    from { text-shadow: 0 0 10px var(--luna-color, #00ffff); }
    to { text-shadow: 0 0 20px var(--luna-color, #00ffff), 0 0 30px var(--luna-color, #00ffff); }
}

@keyframes particleFloat {
    0% { 
        transform: translateY(0) scale(1);
        opacity: 1;
    }
    100% { 
        transform: translateY(-100px) scale(0);
        opacity: 0;
    }
}

@keyframes slideIn {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.shake-effect {
    animation: shake 0.5s ease-in-out;
}

.flash-effect {
    animation: flash 0.5s ease-in-out;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

@keyframes flash {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
    .tutorial-overlay {
        padding: 20px;
        margin: 10px;
    }
    
    .tutorial-title {
        font-size: 1.5em;
    }
    
    .tutorial-description {
        font-size: 1em;
    }
    
    .tutorial-choices {
        flex-direction: column;
    }
}
</style>
`;

// Injecter les styles
document.head.insertAdjacentHTML('beforeend', tutorialStyles);

// Moteur de tutoriel ultra-immersif chargé 