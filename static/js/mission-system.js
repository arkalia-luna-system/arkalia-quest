/* ===== ARKALIA QUEST - MISSION SYSTEM ===== */

class MissionSystem {
    constructor(gameEngine) {
        this.gameEngine = gameEngine;
        this.missions = this.initializeMissions();
        this.currentMission = null;
        this.missionHistory = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadMissionProgress();
    }

    initializeMissions() {
        return {
            'prologue': {
                id: 'prologue',
                name: 'Prologue: L\'Appel de LUNA',
                description: 'Découvrez l\'origine de LUNA et l\'appel mystérieux d\'Althea.',
                status: 'available',
                type: 'story',
                difficulty: 1,
                xpReward: 50,
                badgeReward: 'first_contact',
                choices: [
                    {
                        id: 'accept_call',
                        text: 'Accepter l\'appel de LUNA',
                        consequence: 'luna_contact',
                        xp: 25
                    },
                    {
                        id: 'investigate',
                        text: 'Investiguer l\'origine du signal',
                        consequence: 'signal_analysis',
                        xp: 30
                    },
                    {
                        id: 'ignore',
                        text: 'Ignorer l\'appel pour l\'instant',
                        consequence: 'delayed_response',
                        xp: 10
                    }
                ],
                requirements: { level: 1 },
                nextMissions: ['luna_contact', 'signal_analysis', 'delayed_response']
            },
            'luna_contact': {
                id: 'luna_contact',
                name: 'Premier Contact avec LUNA',
                description: 'Établissez une communication avec l\'IA LUNA.',
                status: 'locked',
                type: 'interaction',
                difficulty: 1,
                xpReward: 75,
                badgeReward: 'luna_friend',
                choices: [
                    {
                        id: 'friendly',
                        text: 'Être amical avec LUNA',
                        consequence: 'luna_friendship',
                        xp: 40
                    },
                    {
                        id: 'cautious',
                        text: 'Être prudent avec LUNA',
                        consequence: 'luna_caution',
                        xp: 35
                    },
                    {
                        id: 'direct',
                        text: 'Être direct avec LUNA',
                        consequence: 'luna_direct',
                        xp: 30
                    }
                ],
                requirements: { level: 1, completedMissions: ['prologue'] },
                nextMissions: ['luna_friendship', 'luna_caution', 'luna_direct']
            },
            'first_game': {
                id: 'first_game',
                name: 'Premier Défi',
                description: 'Testez vos compétences avec votre premier mini-jeu.',
                status: 'locked',
                type: 'game',
                difficulty: 1,
                xpReward: 100,
                badgeReward: 'first_gamer',
                gameId: 'logic_puzzle_1',
                requirements: { level: 1, gamesPlayed: 0 },
                nextMissions: ['game_master']
            },
            'cyber_exploration': {
                id: 'cyber_exploration',
                name: 'Exploration Cyber City',
                description: 'Explorez les zones de Cyber City pour découvrir des secrets.',
                status: 'locked',
                type: 'exploration',
                difficulty: 2,
                xpReward: 150,
                badgeReward: 'cyber_explorer',
                choices: [
                    {
                        id: 'data_center',
                        text: 'Explorer le Data Center',
                        consequence: 'data_center_discovery',
                        xp: 50
                    },
                    {
                        id: 'underground',
                        text: 'Descendre dans l\'Underground',
                        consequence: 'underground_secrets',
                        xp: 60
                    },
                    {
                        id: 'quantum_lab',
                        text: 'Visiter le Laboratoire Quantique',
                        consequence: 'quantum_research',
                        xp: 70
                    }
                ],
                requirements: { level: 3, unlockedZones: ['cyber-city'] },
                nextMissions: ['data_center_discovery', 'underground_secrets', 'quantum_research']
            }
        };
    }

    setupEventListeners() {
        // Écouter les événements de mission
        document.addEventListener('missionStart', (e) => {
            this.startMission(e.detail.missionId);
        });

        document.addEventListener('missionChoice', (e) => {
            this.makeChoice(e.detail.missionId, e.detail.choiceId);
        });

        document.addEventListener('missionComplete', (e) => {
            this.completeMission(e.detail.missionId);
        });
    }

    loadMissionProgress() {
        const saved = localStorage.getItem('arkaliaMissionProgress');
        if (saved) {
            const progress = JSON.parse(saved);
            this.missionHistory = progress.history || [];
            this.currentMission = progress.current || null;

            // Mettre à jour le statut des missions
            this.updateMissionStatuses();
        }
    }

    saveMissionProgress() {
        const progress = {
            history: this.missionHistory,
            current: this.currentMission,
            timestamp: Date.now()
        };
        localStorage.setItem('arkaliaMissionProgress', JSON.stringify(progress));
    }

    updateMissionStatuses() {
        Object.values(this.missions).forEach(mission => {
            if (this.missionHistory.includes(mission.id)) {
                mission.status = 'completed';
            } else if (this.checkRequirements(mission)) {
                mission.status = 'available';
            } else {
                mission.status = 'locked';
            }
        });
    }

    checkRequirements(mission) {
        const req = mission.requirements;
        if (!req) return true;

        // Vérifier le niveau
        if (req.level && this.gameEngine.player.level < req.level) {
            return false;
        }

        // Vérifier les missions complétées
        if (req.completedMissions) {
            for (const missionId of req.completedMissions) {
                if (!this.missionHistory.includes(missionId)) {
                    return false;
                }
            }
        }

        // Vérifier les zones débloquées
        if (req.unlockedZones) {
            for (const zone of req.unlockedZones) {
                if (!this.gameEngine.gameState.unlockedZones.includes(zone)) {
                    return false;
                }
            }
        }

        // Vérifier les jeux joués
        if (req.gamesPlayed !== undefined) {
            if (this.gameEngine.player.stats.gamesPlayed < req.gamesPlayed) {
                return false;
            }
        }

        return true;
    }

    startMission(missionId) {
        const mission = this.missions[missionId];
        if (!mission || mission.status !== 'available') {
            this.showError(`Mission "${missionId}" non disponible.`);
            return;
        }

        this.currentMission = mission;
        this.showMissionInterface(mission);
    }

    showMissionInterface(mission) {
        const missionModal = document.createElement('div');
        missionModal.className = 'mission-modal';
        missionModal.innerHTML = `
            <div class="mission-container">
                <div class="mission-header">
                    <h2>${mission.name}</h2>
                    <p class="mission-description">${mission.description}</p>
                    <div class="mission-info">
                        <span class="mission-type">Type: ${this.getMissionTypeLabel(mission.type)}</span>
                        <span class="mission-difficulty">Difficulté: ${'★'.repeat(mission.difficulty)}</span>
                        <span class="mission-reward">Récompense: ${mission.xpReward} XP</span>
                    </div>
                </div>
                <div class="mission-content">
                    ${this.generateMissionContent(mission)}
                </div>
                <div class="mission-controls">
                    <button id="mission-accept" class="btn-primary">Accepter</button>
                    <button id="mission-decline" class="btn-secondary">Refuser</button>
                </div>
            </div>
        `;

        document.body.appendChild(missionModal);
        this.setupMissionEventListeners(missionModal, mission);
    }

    generateMissionContent(mission) {
        if (mission.type === 'story') {
            return this.generateStoryContent(mission);
        } else if (mission.type === 'interaction') {
            return this.generateInteractionContent(mission);
        } else if (mission.type === 'game') {
            return this.generateGameContent(mission);
        } else if (mission.type === 'exploration') {
            return this.generateExplorationContent(mission);
        }
        return '<p>Contenu de mission en cours de développement...</p>';
    }

    generateStoryContent(mission) {
        return `
            <div class="story-content">
                <div class="story-text">
                    <p>Vous recevez un signal mystérieux provenant d'une source inconnue. Le message semble être un appel à l'aide...</p>
                    <p>Que souhaitez-vous faire ?</p>
                </div>
                <div class="story-choices">
                    ${mission.choices.map(choice => `
                        <button class="choice-btn" data-choice="${choice.id}">
                            ${choice.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }

    generateInteractionContent(mission) {
        return `
            <div class="interaction-content">
                <div class="luna-avatar">🌙</div>
                <div class="interaction-text">
                    <p>LUNA apparaît devant vous, ses yeux lumineux vous observant avec curiosité.</p>
                    <p>"Salut ! Je suis LUNA, ton guide dans cette aventure. Comment veux-tu que nous interagissions ?"</p>
                </div>
                <div class="interaction-choices">
                    ${mission.choices.map(choice => `
                        <button class="choice-btn" data-choice="${choice.id}">
                            ${choice.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }

    generateGameContent(mission) {
        return `
            <div class="game-content">
                <div class="game-preview">
                    <h3>🎮 ${mission.name}</h3>
                    <p>Testez vos compétences avec ce mini-jeu !</p>
                    <div class="game-info">
                        <span>Difficulté: ${'★'.repeat(mission.difficulty)}</span>
                        <span>Récompense: ${mission.xpReward} XP</span>
                    </div>
                </div>
                <div class="game-actions">
                    <button class="choice-btn" data-choice="play_game">
                        🎮 Jouer maintenant
                    </button>
                    <button class="choice-btn" data-choice="learn_more">
                        📚 En savoir plus
                    </button>
                </div>
            </div>
        `;
    }

    generateExplorationContent(mission) {
        return `
            <div class="exploration-content">
                <div class="exploration-map">
                    <h3>🗺️ Carte d'Exploration</h3>
                    <p>Choisissez votre destination d'exploration :</p>
                </div>
                <div class="exploration-choices">
                    ${mission.choices.map(choice => `
                        <button class="choice-btn exploration-btn" data-choice="${choice.id}">
                            <span class="choice-icon">${this.getChoiceIcon(choice.id)}</span>
                            <span class="choice-text">${choice.text}</span>
                            <span class="choice-xp">+${choice.xp} XP</span>
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }

    getChoiceIcon(choiceId) {
        const icons = {
            'data_center': '🏢',
            'underground': '🕳️',
            'quantum_lab': '⚛️',
            'friendly': '😊',
            'cautious': '🤔',
            'direct': '💬',
            'play_game': '🎮',
            'learn_more': '📚'
        };
        return icons[choiceId] || '❓';
    }

    getMissionTypeLabel(type) {
        const labels = {
            'story': 'Histoire',
            'interaction': 'Interaction',
            'game': 'Mini-jeu',
            'exploration': 'Exploration'
        };
        return labels[type] || type;
    }

    setupMissionEventListeners(modal, mission) {
        const acceptBtn = modal.querySelector('#mission-accept');
        const declineBtn = modal.querySelector('#mission-decline');
        const choiceBtns = modal.querySelectorAll('.choice-btn');

        acceptBtn.addEventListener('click', () => {
            this.acceptMission(mission);
            modal.remove();
        });

        declineBtn.addEventListener('click', () => {
            this.declineMission(mission);
            modal.remove();
        });

        choiceBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const choiceId = e.target.dataset.choice;
                this.makeChoice(mission.id, choiceId);
                modal.remove();
            });
        });
    }

    acceptMission(mission) {
        this.currentMission = mission;
        this.showSuccess(`Mission "${mission.name}" acceptée !`);

        // Déclencher l'événement de début de mission
        const event = new CustomEvent('missionStart', {
            detail: { missionId: mission.id }
        });
        document.dispatchEvent(event);
    }

    declineMission(mission) {
        this.showInfo(`Mission "${mission.name}" refusée.`);
    }

    makeChoice(missionId, choiceId) {
        const mission = this.missions[missionId];
        if (!mission) return;

        const choice = mission.choices.find(c => c.id === choiceId);
        if (!choice) return;

        // Appliquer les conséquences du choix
        this.applyChoiceConsequence(choice);

        // Marquer la mission comme complétée
        this.completeMission(missionId);
    }

    applyChoiceConsequence(choice) {
        // Ajouter XP
        if (choice.xp) {
            this.gameEngine.addXP(choice.xp, 'choix_mission');
        }

        // Appliquer les conséquences spécifiques
        switch (choice.consequence) {
            case 'luna_contact':
                this.showInfo('Vous avez établi un contact amical avec LUNA.');
                break;
            case 'signal_analysis':
                this.showInfo('Vous analysez le signal mystérieux...');
                break;
            case 'data_center_discovery':
                this.showInfo('Vous découvrez des secrets dans le Data Center !');
                break;
            case 'play_game':
                if (this.currentMission.gameId) {
                    this.gameEngine.playGame(this.currentMission.gameId);
                }
                break;
            default:
                this.showInfo(`Conséquence: ${choice.consequence}`);
        }
    }

    completeMission(missionId) {
        const mission = this.missions[missionId];
        if (!mission) return;

        // Ajouter à l'historique
        this.missionHistory.push(missionId);

        // Récompenses
        if (mission.xpReward) {
            this.gameEngine.addXP(mission.xpReward, 'mission');
        }

        if (mission.badgeReward) {
            this.gameEngine.checkBadges();
        }

        // Mettre à jour le statut
        mission.status = 'completed';
        this.currentMission = null;

        // Débloquer les missions suivantes
        this.updateMissionStatuses();

        // Sauvegarder
        this.saveMissionProgress();

        this.showSuccess(`Mission "${mission.name}" complétée ! +${mission.xpReward} XP`);
    }

    // MÉTHODES D'AFFICHAGE
    showMissions() {
        const availableMissions = Object.values(this.missions).filter(m => m.status === 'available');
        const completedMissions = Object.values(this.missions).filter(m => m.status === 'completed');
        const lockedMissions = Object.values(this.missions).filter(m => m.status === 'locked');

        let missionsText = '🎯 SYSTÈME DE MISSIONS\n\n';

        if (availableMissions.length > 0) {
            missionsText += '📋 MISSIONS DISPONIBLES:\n';
            availableMissions.forEach(mission => {
                missionsText += `• ${mission.name} (${mission.xpReward} XP)\n`;
            });
            missionsText += '\n';
        }

        if (completedMissions.length > 0) {
            missionsText += '✅ MISSIONS COMPLÉTÉES:\n';
            completedMissions.forEach(mission => {
                missionsText += `• ${mission.name} ✓\n`;
            });
            missionsText += '\n';
        }

        if (lockedMissions.length > 0) {
            missionsText += '🔒 MISSIONS VERROUILLÉES:\n';
            lockedMissions.forEach(mission => {
                missionsText += `• ${mission.name} (Niveau ${mission.requirements?.level || 1}+)\n`;
            });
        }

        this.gameEngine.showTerminalMessage(missionsText, 'info');
    }

    showSuccess(message) {
        this.gameEngine.showSuccess(message);
    }

    showError(message) {
        this.gameEngine.showError(message);
    }

    showInfo(message) {
        this.gameEngine.showNotification(message, 'info');
    }
}

// Export pour utilisation externe
window.MissionSystem = MissionSystem;
