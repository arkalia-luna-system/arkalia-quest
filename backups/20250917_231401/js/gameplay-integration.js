/* ===== ARKALIA QUEST - GAMEPLAY INTEGRATION ===== */
/* Intégration de tous les systèmes de gameplay améliorés */

class GameplayIntegration {
    constructor() {
        this.systems = {};
        this.init();
    }

    init() {
        this.initializeSystems();
        this.setupEventListeners();
        this.createMainInterface();
    }

    initializeSystems() {
        // Initialiser tous les systèmes
        this.systems.zoneExploration = new ZoneExplorationEnhanced();
        this.systems.dailyMissions = new DailyMissionsEnhanced();
        this.systems.motivationalEmptyStates = new MotivationalEmptyStates();
        this.systems.timerChallenges = new TimerChallenges();
        this.systems.interactivePuzzles = new InteractivePuzzles();

        // Intégrer avec les systèmes existants
        this.integrateWithExistingSystems();
    }

    integrateWithExistingSystems() {
        // Intégrer avec LUNA Vision
        if (window.lunaVision) {
            this.setupLunaIntegration();
        }

        // Intégrer avec les animations de récompenses
        if (window.rewardAnimations) {
            this.setupRewardIntegration();
        }

        // Intégrer avec le système de commandes
        this.setupCommandIntegration();
    }

    setupLunaIntegration() {
        // Ajouter des commandes LUNA pour les nouveaux systèmes
        const lunaCommands = {
            'zones': () => this.systems.zoneExploration.showZonePanel(),
            'missions': () => this.systems.dailyMissions.showPanel(),
            'puzzles': () => this.systems.interactivePuzzles.togglePanel(),
            'challenges': () => this.systems.timerChallenges.togglePanel()
        };

        // Intégrer avec le système de commandes existant
        if (window.gameEngine) {
            Object.assign(window.gameEngine.commands, lunaCommands);
        }
    }

    setupRewardIntegration() {
        // Connecter les récompenses des nouveaux systèmes
        this.systems.dailyMissions.onMissionCompleted = (mission) => {
            if (window.rewardAnimations) {
                window.rewardAnimations.animateMissionCompletion(mission.name, {
                    xp: mission.xp,
                    coins: mission.coins
                });
            }
        };

        this.systems.timerChallenges.onChallengeCompleted = (challenge) => {
            if (window.rewardAnimations) {
                window.rewardAnimations.animateXPGain(challenge.score);
            }
        };

        this.systems.interactivePuzzles.onPuzzleCompleted = (puzzle) => {
            if (window.rewardAnimations) {
                window.rewardAnimations.animateXPGain(puzzle.score);
            }
        };
    }

    setupCommandIntegration() {
        // Intercepter les commandes pour mettre à jour les systèmes
        const originalHandleCommand = window.gameEngine?.handleCommand;
        if (originalHandleCommand) {
            window.gameEngine.handleCommand = (command, args) => {
                // Traiter la commande normalement
                const result = originalHandleCommand.call(window.gameEngine, command, args);

                // Mettre à jour les systèmes basés sur la commande
                this.updateSystemsFromCommand(command, args, result);

                return result;
            };
        }
    }

    updateSystemsFromCommand(command, args, result) {
        // Mettre à jour les missions du jour
        if (this.systems.dailyMissions) {
            switch (command) {
                case 'hack_system':
                case 'kill_virus':
                case 'find_shadow':
                    this.systems.dailyMissions.onCommandUsed(command);
                    break;
                case 'explorer':
                case 'monde':
                    this.systems.dailyMissions.onZoneVisited(args[0] || 'unknown');
                    break;
                case 'play_game':
                    this.systems.dailyMissions.onMinigameCompleted();
                    break;
            }
        }

        // Mettre à jour l'exploration des zones
        if (this.systems.zoneExploration) {
            if (command === 'explorer' || command === 'monde') {
                this.systems.zoneExploration.onZoneExplored(args[0] || 'unknown');
            }
        }

        // Mettre à jour les états vides
        if (this.systems.motivationalEmptyStates) {
            if (result && result.profile_updated) {
                this.systems.motivationalEmptyStates.checkForEmptyStates();
            }
        }
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('profileUpdated', (event) => {
            this.handleProfileUpdate(event.detail);
        });

        // Écouter les événements de zone
        document.addEventListener('zoneVisited', (event) => {
            this.handleZoneVisited(event.detail);
        });

        // Écouter les événements de mini-jeu
        document.addEventListener('minigameCompleted', (event) => {
            this.handleMinigameCompleted(event.detail);
        });
    }

    handleProfileUpdate(profile) {
        // Mettre à jour tous les systèmes avec les nouvelles données de profil
        Object.values(this.systems).forEach(system => {
            if (system.updateProfile) {
                system.updateProfile(profile);
            }
        });
    }

    handleZoneVisited(zoneData) {
        // Mettre à jour l'exploration des zones
        if (this.systems.zoneExploration) {
            this.systems.zoneExploration.onZoneExplored(zoneData.zoneId);
        }

        // Mettre à jour les missions du jour
        if (this.systems.dailyMissions) {
            this.systems.dailyMissions.onZoneVisited(zoneData.zoneId);
        }
    }

    handleMinigameCompleted(gameData) {
        // Mettre à jour les missions du jour
        if (this.systems.dailyMissions) {
            this.systems.dailyMissions.onMinigameCompleted();
        }

        // Mettre à jour les défis à timer
        if (this.systems.timerChallenges) {
            this.systems.timerChallenges.updateChallengeProgress('hack_2', 1);
        }
    }

    createMainInterface() {
        // Créer l'interface principale qui regroupe tous les systèmes
        this.createGameplayHub();
    }

    createGameplayHub() {
        if (document.getElementById('gameplay-hub')) return;

        const hub = document.createElement('div');
        hub.id = 'gameplay-hub';
        hub.className = 'gameplay-hub';
        hub.innerHTML = `
            <div class="hub-header">
                <h3>🎮 Hub de Gameplay</h3>
                <button class="close-hub-btn" onclick="gameplayIntegration.toggleHub()">×</button>
            </div>
            <div class="hub-content">
                <div class="hub-sections">
                    <div class="hub-section" onclick="gameplayIntegration.openSystem('zones')">
                        <div class="section-icon">🗺️</div>
                        <div class="section-info">
                            <h4>Exploration</h4>
                            <p>Découvre les zones d'Arkalia</p>
                        </div>
                    </div>
                    <div class="hub-section" onclick="gameplayIntegration.openSystem('missions')">
                        <div class="section-icon">🎯</div>
                        <div class="section-info">
                            <h4>Missions</h4>
                            <p>Défis du jour</p>
                        </div>
                    </div>
                    <div class="hub-section" onclick="gameplayIntegration.openSystem('puzzles')">
                        <div class="section-icon">🧩</div>
                        <div class="section-info">
                            <h4>Puzzles</h4>
                            <p>Énigmes interactives</p>
                        </div>
                    </div>
                    <div class="hub-section" onclick="gameplayIntegration.openSystem('challenges')">
                        <div class="section-icon">⏱️</div>
                        <div class="section-info">
                            <h4>Défis</h4>
                            <p>Défis à timer</p>
                        </div>
                    </div>
                </div>
                <div class="hub-stats">
                    <div class="stat-item">
                        <span class="stat-label">Zones explorées</span>
                        <span class="stat-value" id="zones-explored">0</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Missions complétées</span>
                        <span class="stat-value" id="missions-completed">0</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Puzzles résolus</span>
                        <span class="stat-value" id="puzzles-solved">0</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Défis réussis</span>
                        <span class="stat-value" id="challenges-completed">0</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(hub);
    }

    openSystem(systemName) {
        switch (systemName) {
            case 'zones':
                this.systems.zoneExploration?.showZonePanel();
                break;
            case 'missions':
                this.systems.dailyMissions?.showPanel();
                break;
            case 'puzzles':
                this.systems.interactivePuzzles?.togglePanel();
                break;
            case 'challenges':
                this.systems.timerChallenges?.togglePanel();
                break;
        }
    }

    toggleHub() {
        const hub = document.getElementById('gameplay-hub');
        if (hub) {
            hub.classList.toggle('show');
        }
    }

    showHub() {
        const hub = document.getElementById('gameplay-hub');
        if (hub) {
            hub.classList.add('show');
        }
    }

    hideHub() {
        const hub = document.getElementById('gameplay-hub');
        if (hub) {
            hub.classList.remove('show');
        }
    }

    updateStats() {
        // Mettre à jour les statistiques du hub
        const zonesExplored = this.systems.zoneExploration?.getExploredZonesCount() || 0;
        const missionsCompleted = this.systems.dailyMissions?.getCompletedMissionsCount() || 0;
        const puzzlesSolved = this.systems.interactivePuzzles?.getSolvedPuzzlesCount() || 0;
        const challengesCompleted = this.systems.timerChallenges?.getCompletedChallengesCount() || 0;

        document.getElementById('zones-explored').textContent = zonesExplored;
        document.getElementById('missions-completed').textContent = missionsCompleted;
        document.getElementById('puzzles-solved').textContent = puzzlesSolved;
        document.getElementById('challenges-completed').textContent = challengesCompleted;
    }

    // Méthodes publiques pour l'intégration
    onGameStart() {
        // Initialiser tous les systèmes au démarrage du jeu
        Object.values(this.systems).forEach(system => {
            if (system.onGameStart) {
                system.onGameStart();
            }
        });
    }

    onGameEnd() {
        // Nettoyer les systèmes à la fin du jeu
        Object.values(this.systems).forEach(system => {
            if (system.onGameEnd) {
                system.onGameEnd();
            }
        });
    }

    onPlayerAction(action, data) {
        // Diffuser l'action à tous les systèmes
        Object.values(this.systems).forEach(system => {
            if (system.onPlayerAction) {
                system.onPlayerAction(action, data);
            }
        });
    }
}

// CSS pour le hub de gameplay
const style = document.createElement('style');
style.textContent = `
    .gameplay-hub {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 500px;
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 25px;
        z-index: 10000;
        backdrop-filter: blur(15px);
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
    }
    
    .gameplay-hub.show {
        opacity: 1;
        visibility: visible;
    }
    
    .hub-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    
    .hub-header h3 {
        color: var(--violet-lunaire);
        margin: 0;
        font-size: 1.3em;
    }
    
    .close-hub-btn {
        background: none;
        border: none;
        color: var(--argent-holographique);
        font-size: 1.5em;
        cursor: pointer;
        transition: color 0.3s ease;
    }
    
    .close-hub-btn:hover {
        color: var(--violet-lunaire);
    }
    
    .hub-sections {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    .hub-section {
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.2);
        border-radius: 10px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .hub-section:hover {
        border-color: rgba(167, 139, 250, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(167, 139, 250, 0.2);
    }
    
    .section-icon {
        font-size: 2em;
    }
    
    .section-info h4 {
        color: var(--violet-lunaire);
        margin: 0 0 5px 0;
        font-size: 1.1em;
    }
    
    .section-info p {
        color: var(--argent-holographique);
        margin: 0;
        font-size: 0.9em;
    }
    
    .hub-stats {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
    }
    
    .stat-item {
        background: rgba(167, 139, 250, 0.05);
        border: 1px solid rgba(167, 139, 250, 0.1);
        border-radius: 8px;
        padding: 15px;
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
        font-size: 1.5em;
        font-weight: 600;
        font-family: 'IBM Plex Mono', monospace;
    }
    
    @media (max-width: 768px) {
        .gameplay-hub {
            width: 90%;
            max-width: 400px;
        }
        
        .hub-sections {
            grid-template-columns: 1fr;
        }
        
        .hub-stats {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(style);

// Initialiser l'intégration du gameplay
document.addEventListener('DOMContentLoaded', () => {
    window.gameplayIntegration = new GameplayIntegration();
});

// Exporter pour utilisation globale
window.GameplayIntegration = GameplayIntegration;
