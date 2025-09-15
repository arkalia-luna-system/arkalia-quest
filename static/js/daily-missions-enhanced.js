/* ===== ARKALIA QUEST - DAILY MISSIONS ENHANCED ===== */
/* Système de missions du jour amélioré avec variété et motivation */

class DailyMissionsEnhanced {
    constructor() {
        this.missions = this.initializeMissions();
        this.activeMissions = [];
        this.completedMissions = [];
        this.dailyResetTime = this.getNextResetTime();
        this.init();
    }

    init() {
        this.loadMissions();
        this.setupMissionUI();
        this.startMissionTimer();
    }

    initializeMissions() {
        return {
            // Missions sociales
            social: [
                {
                    id: 'social_1',
                    title: '🌐 Connecte-toi avec 3 joueurs',
                    description: 'Envoie des messages à 3 joueurs différents',
                    type: 'social',
                    difficulty: 'easy',
                    xp: 50,
                    coins: 25,
                    requirements: { interactions: 3 },
                    progress: 0,
                    maxProgress: 3,
                    timeLimit: 24, // heures
                    icon: '👥'
                },
                {
                    id: 'social_2',
                    title: '💬 Aide 5 nouveaux joueurs',
                    description: 'Donne des conseils à 5 nouveaux joueurs',
                    type: 'social',
                    difficulty: 'medium',
                    xp: 100,
                    coins: 50,
                    requirements: { help_given: 5 },
                    progress: 0,
                    maxProgress: 5,
                    timeLimit: 24,
                    icon: '🤝'
                }
            ],

            // Missions d'exploration
            exploration: [
                {
                    id: 'explore_1',
                    title: '🗺️ Explore 2 nouvelles zones',
                    description: 'Découvre 2 zones que tu n\'as jamais visitées',
                    type: 'exploration',
                    difficulty: 'easy',
                    xp: 75,
                    coins: 40,
                    requirements: { zones_visited: 2 },
                    progress: 0,
                    maxProgress: 2,
                    timeLimit: 24,
                    icon: '🌍'
                },
                {
                    id: 'explore_2',
                    title: '💎 Trouve 3 secrets cachés',
                    description: 'Découvre 3 secrets dans les zones explorées',
                    type: 'exploration',
                    difficulty: 'medium',
                    xp: 120,
                    coins: 60,
                    requirements: { secrets_found: 3 },
                    progress: 0,
                    maxProgress: 3,
                    timeLimit: 24,
                    icon: '🔍'
                }
            ],

            // Missions de hacking
            hacking: [
                {
                    id: 'hack_1',
                    title: '💻 Utilise 10 commandes différentes',
                    description: 'Exécute 10 commandes différentes dans le terminal',
                    type: 'hacking',
                    difficulty: 'easy',
                    xp: 60,
                    coins: 30,
                    requirements: { commands_used: 10 },
                    progress: 0,
                    maxProgress: 10,
                    timeLimit: 24,
                    icon: '⌨️'
                },
                {
                    id: 'hack_2',
                    title: '🎮 Complète 3 mini-jeux',
                    description: 'Termine 3 mini-jeux avec succès',
                    type: 'hacking',
                    difficulty: 'medium',
                    xp: 150,
                    coins: 75,
                    requirements: { minigames_completed: 3 },
                    progress: 0,
                    maxProgress: 3,
                    timeLimit: 24,
                    icon: '🎯'
                }
            ],

            // Missions de progression
            progression: [
                {
                    id: 'progress_1',
                    title: '⭐ Gagne 500 XP',
                    description: 'Accumule 500 points d\'expérience',
                    type: 'progression',
                    difficulty: 'medium',
                    xp: 100,
                    coins: 50,
                    requirements: { xp_gained: 500 },
                    progress: 0,
                    maxProgress: 500,
                    timeLimit: 24,
                    icon: '📈'
                },
                {
                    id: 'progress_2',
                    title: '🏆 Débloque 2 badges',
                    description: 'Obtiens 2 nouveaux badges',
                    type: 'progression',
                    difficulty: 'hard',
                    xp: 200,
                    coins: 100,
                    requirements: { badges_earned: 2 },
                    progress: 0,
                    maxProgress: 2,
                    timeLimit: 24,
                    icon: '🥇'
                }
            ],

            // Missions spéciales
            special: [
                {
                    id: 'special_1',
                    title: '🌙 Passe 30 minutes avec LUNA',
                    description: 'Interagis avec LUNA pendant 30 minutes',
                    type: 'special',
                    difficulty: 'easy',
                    xp: 80,
                    coins: 40,
                    requirements: { luna_time: 30 },
                    progress: 0,
                    maxProgress: 30,
                    timeLimit: 24,
                    icon: '🌙'
                },
                {
                    id: 'special_2',
                    title: '🎨 Change de thème 3 fois',
                    description: 'Teste 3 thèmes différents',
                    type: 'special',
                    difficulty: 'easy',
                    xp: 40,
                    coins: 20,
                    requirements: { themes_changed: 3 },
                    progress: 0,
                    maxProgress: 3,
                    timeLimit: 24,
                    icon: '🎨'
                }
            ]
        };
    }

    loadMissions() {
        // Charger les missions depuis le localStorage
        const saved = localStorage.getItem('dailyMissions');
        if (saved) {
            const data = JSON.parse(saved);
            this.activeMissions = data.activeMissions || [];
            this.completedMissions = data.completedMissions || [];
        } else {
            this.generateDailyMissions();
        }

        // Vérifier si c'est un nouveau jour
        if (this.isNewDay()) {
            this.resetDailyMissions();
        }
    }

    generateDailyMissions() {
        // Générer 3 missions aléatoires pour la journée
        const allMissions = Object.values(this.missions).flat();
        const selectedMissions = this.selectRandomMissions(allMissions, 3);

        this.activeMissions = selectedMissions.map(mission => ({
            ...mission,
            id: mission.id + '_' + Date.now(),
            startTime: Date.now(),
            progress: 0
        }));

        this.saveMissions();
    }

    selectRandomMissions(allMissions, count) {
        const shuffled = allMissions.sort(() => 0.5 - Math.random());
        return shuffled.slice(0, count);
    }

    isNewDay() {
        const now = new Date();
        const lastReset = new Date(localStorage.getItem('lastMissionReset') || 0);

        return now.getDate() !== lastReset.getDate() ||
            now.getMonth() !== lastReset.getMonth() ||
            now.getFullYear() !== lastReset.getFullYear();
    }

    resetDailyMissions() {
        this.completedMissions = [];
        this.generateDailyMissions();
        localStorage.setItem('lastMissionReset', Date.now().toString());

        // Afficher une notification
        this.showResetNotification();
    }

    showResetNotification() {
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage("Nouvelles missions du jour disponibles !", 4000);
            window.lunaVision.setEmotion('excited');
        }
    }

    setupMissionUI() {
        // Créer l'interface des missions du jour
        this.createMissionPanel();
        this.updateMissionDisplay();
    }

    createMissionPanel() {
        // Vérifier si le panneau existe déjà
        if (document.getElementById('daily-missions-panel')) return;

        const panel = document.createElement('div');
        panel.id = 'daily-missions-panel';
        panel.className = 'daily-missions-panel';
        panel.innerHTML = `
            <div class="missions-header">
                <h3>🎯 Missions du Jour</h3>
                <button class="close-missions-btn" onclick="dailyMissions.togglePanel()">×</button>
            </div>
            <div class="missions-content">
                <div class="missions-list" id="missions-list">
                    <!-- Missions seront chargées ici -->
                </div>
                <div class="missions-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" id="missions-progress-fill"></div>
                    </div>
                    <span class="progress-text" id="missions-progress-text">0/3 complétées</span>
                </div>
                <div class="missions-timer">
                    <span class="timer-text" id="missions-timer">Temps restant: --:--:--</span>
                </div>
            </div>
        `;

        document.body.appendChild(panel);
    }

    updateMissionDisplay() {
        const missionsList = document.getElementById('missions-list');
        if (!missionsList) return;

        missionsList.innerHTML = '';

        if (this.activeMissions.length === 0) {
            missionsList.innerHTML = '<p class="no-missions">Aucune mission active</p>';
            return;
        }

        this.activeMissions.forEach(mission => {
            const missionElement = this.createMissionElement(mission);
            missionsList.appendChild(missionElement);
        });

        this.updateProgressBar();
    }

    createMissionElement(mission) {
        const element = document.createElement('div');
        element.className = `mission-item ${mission.difficulty}`;
        element.innerHTML = `
            <div class="mission-header">
                <span class="mission-icon">${mission.icon}</span>
                <span class="mission-title">${mission.title}</span>
                <span class="mission-reward">+${mission.xp} XP</span>
            </div>
            <div class="mission-description">${mission.description}</div>
            <div class="mission-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${(mission.progress / mission.maxProgress) * 100}%"></div>
                </div>
                <span class="progress-text">${mission.progress}/${mission.maxProgress}</span>
            </div>
            <div class="mission-actions">
                <button class="mission-btn" onclick="dailyMissions.startMission('${mission.id}')">
                    ${mission.progress > 0 ? 'Continuer' : 'Commencer'}
                </button>
            </div>
        `;

        return element;
    }

    updateProgressBar() {
        const completedCount = this.activeMissions.filter(m => m.progress >= m.maxProgress).length;
        const totalCount = this.activeMissions.length;
        const progressFill = document.getElementById('missions-progress-fill');
        const progressText = document.getElementById('missions-progress-text');

        if (progressFill) {
            progressFill.style.width = `${(completedCount / totalCount) * 100}%`;
        }

        if (progressText) {
            progressText.textContent = `${completedCount}/${totalCount} complétées`;
        }
    }

    startMission(missionId) {
        const mission = this.activeMissions.find(m => m.id === missionId);
        if (!mission) return;

        // Rediriger vers la page appropriée selon le type de mission
        switch (mission.type) {
            case 'social':
                window.location.href = '/profil';
                break;
            case 'exploration':
                window.location.href = '/monde';
                break;
            case 'hacking':
                window.location.href = '/terminal';
                break;
            case 'progression':
                window.location.href = '/dashboard';
                break;
            case 'special':
                // Missions spéciales peuvent être faites n'importe où
                this.showMissionGuidance(mission);
                break;
        }
    }

    showMissionGuidance(mission) {
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage(mission.description, 4000);
            window.lunaVision.setEmotion('helpful');
        }
    }

    updateMissionProgress(missionId, increment = 1) {
        const mission = this.activeMissions.find(m => m.id === missionId);
        if (!mission) return;

        mission.progress += increment;
        if (mission.progress > mission.maxProgress) {
            mission.progress = mission.maxProgress;
        }

        // Vérifier si la mission est complétée
        if (mission.progress >= mission.maxProgress) {
            this.completeMission(mission);
        }

        this.updateMissionDisplay();
        this.saveMissions();
    }

    completeMission(mission) {
        // Marquer comme complétée
        mission.completed = true;
        mission.completionTime = Date.now();
        this.completedMissions.push(mission);

        // Retirer de la liste active
        this.activeMissions = this.activeMissions.filter(m => m.id !== mission.id);

        // Donner les récompenses
        this.giveMissionRewards(mission);

        // Afficher l'animation de completion
        this.showMissionCompletion(mission);

        // Vérifier si toutes les missions sont complétées
        if (this.activeMissions.length === 0) {
            this.showAllMissionsCompleted();
        }
    }

    giveMissionRewards(mission) {
        // Donner XP et coins
        if (window.rewardAnimations) {
            window.rewardAnimations.animateXPGain(mission.xp);
            window.rewardAnimations.animateCoinsGained(mission.coins);
        }

        // Mettre à jour le profil (simulation)
        this.updatePlayerProfile(mission);
    }

    updatePlayerProfile(mission) {
        // Simuler la mise à jour du profil
        const profile = JSON.parse(localStorage.getItem('playerProfile') || '{}');
        profile.xp = (profile.xp || 0) + mission.xp;
        profile.coins = (profile.coins || 0) + mission.coins;
        localStorage.setItem('playerProfile', JSON.stringify(profile));
    }

    showMissionCompletion(mission) {
        // Créer une animation de completion
        const completion = document.createElement('div');
        completion.className = 'mission-completion';
        completion.innerHTML = `
            <div class="completion-content">
                <div class="completion-icon">🎉</div>
                <h3>Mission Complétée !</h3>
                <p>${mission.title}</p>
                <div class="completion-rewards">
                    <span>+${mission.xp} XP</span>
                    <span>+${mission.coins} Coins</span>
                </div>
            </div>
        `;

        document.body.appendChild(completion);

        // Animation d'apparition
        setTimeout(() => {
            completion.classList.add('show');
        }, 100);

        // Supprimer après 3 secondes
        setTimeout(() => {
            completion.remove();
        }, 3000);
    }

    showAllMissionsCompleted() {
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage("Félicitations ! Tu as complété toutes les missions du jour !", 5000);
            window.lunaVision.setEmotion('proud');
        }

        // Animation spéciale
        this.createCompletionCelebration();
    }

    createCompletionCelebration() {
        // Créer une célébration spéciale
        const celebration = document.createElement('div');
        celebration.className = 'all-missions-completed';
        celebration.innerHTML = `
            <div class="celebration-content">
                <div class="celebration-icon">🏆</div>
                <h2>Toutes les missions complétées !</h2>
                <p>Tu es un vrai hacker !</p>
            </div>
        `;

        document.body.appendChild(celebration);

        // Animation d'apparition
        setTimeout(() => {
            celebration.classList.add('show');
        }, 100);

        // Supprimer après 5 secondes
        setTimeout(() => {
            celebration.remove();
        }, 5000);
    }

    startMissionTimer() {
        // Mettre à jour le timer toutes les secondes
        setInterval(() => {
            this.updateTimer();
        }, 1000);
    }

    updateTimer() {
        const timerElement = document.getElementById('missions-timer');
        if (!timerElement) return;

        const now = new Date();
        const resetTime = new Date(this.dailyResetTime);
        const timeLeft = resetTime - now;

        if (timeLeft <= 0) {
            timerElement.textContent = 'Nouvelles missions disponibles !';
            this.resetDailyMissions();
            return;
        }

        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        timerElement.textContent = `Temps restant: ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    getNextResetTime() {
        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(0, 0, 0, 0);
        return tomorrow.getTime();
    }

    togglePanel() {
        const panel = document.getElementById('daily-missions-panel');
        if (panel) {
            panel.classList.toggle('show');
        }
    }

    showPanel() {
        const panel = document.getElementById('daily-missions-panel');
        if (panel) {
            panel.classList.add('show');
        }
    }

    hidePanel() {
        const panel = document.getElementById('daily-missions-panel');
        if (panel) {
            panel.classList.remove('show');
        }
    }

    saveMissions() {
        const data = {
            activeMissions: this.activeMissions,
            completedMissions: this.completedMissions
        };
        localStorage.setItem('dailyMissions', JSON.stringify(data));
    }

    // Méthodes publiques pour les interactions
    onCommandUsed(command) {
        this.updateMissionProgress('hack_1', 1);
    }

    onZoneVisited(zoneId) {
        this.updateMissionProgress('explore_1', 1);
    }

    onSecretFound() {
        this.updateMissionProgress('explore_2', 1);
    }

    onMinigameCompleted() {
        this.updateMissionProgress('hack_2', 1);
    }

    onXPGained(amount) {
        this.updateMissionProgress('progress_1', amount);
    }

    onBadgeEarned() {
        this.updateMissionProgress('progress_2', 1);
    }

    onSocialInteraction() {
        this.updateMissionProgress('social_1', 1);
    }

    onHelpGiven() {
        this.updateMissionProgress('social_2', 1);
    }

    onLunaInteraction() {
        this.updateMissionProgress('special_1', 1);
    }

    onThemeChanged() {
        this.updateMissionProgress('special_2', 1);
    }
}

// CSS pour les missions du jour
const style = document.createElement('style');
style.textContent = `
    .daily-missions-panel {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 350px;
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 20px;
        z-index: 10000;
        backdrop-filter: blur(15px);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    }
    
    .daily-missions-panel.show {
        transform: translateX(0);
    }
    
    .missions-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .missions-header h3 {
        color: var(--violet-lunaire);
        margin: 0;
    }
    
    .close-missions-btn {
        background: none;
        border: none;
        color: var(--argent-holographique);
        font-size: 1.5em;
        cursor: pointer;
        transition: color 0.3s ease;
    }
    
    .close-missions-btn:hover {
        color: var(--violet-lunaire);
    }
    
    .mission-item {
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .mission-item:hover {
        border-color: rgba(167, 139, 250, 0.4);
        transform: translateY(-2px);
    }
    
    .mission-item.easy {
        border-left: 4px solid #22c55e;
    }
    
    .mission-item.medium {
        border-left: 4px solid #f59e0b;
    }
    
    .mission-item.hard {
        border-left: 4px solid #ef4444;
    }
    
    .mission-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .mission-icon {
        font-size: 1.2em;
        margin-right: 10px;
    }
    
    .mission-title {
        color: var(--violet-lunaire);
        font-weight: 600;
        flex: 1;
    }
    
    .mission-reward {
        color: var(--bleu-spectre);
        font-size: 0.9em;
        font-weight: 600;
    }
    
    .mission-description {
        color: var(--argent-holographique);
        font-size: 0.9em;
        margin-bottom: 15px;
        line-height: 1.4;
    }
    
    .mission-progress {
        margin-bottom: 15px;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: rgba(167, 139, 250, 0.2);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 5px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .progress-text {
        color: var(--argent-holographique);
        font-size: 0.8em;
        font-family: 'IBM Plex Mono', monospace;
    }
    
    .mission-actions {
        text-align: center;
    }
    
    .mission-btn {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.2), rgba(96, 165, 250, 0.2));
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 6px;
        padding: 8px 16px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9em;
    }
    
    .mission-btn:hover {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.4), rgba(96, 165, 250, 0.4));
        transform: translateY(-1px);
    }
    
    .missions-progress {
        margin: 20px 0;
        padding: 15px;
        background: rgba(167, 139, 250, 0.05);
        border-radius: 8px;
    }
    
    .missions-timer {
        text-align: center;
        margin-top: 15px;
    }
    
    .timer-text {
        color: var(--argent-holographique);
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.9em;
    }
    
    .no-missions {
        text-align: center;
        color: var(--argent-holographique);
        font-style: italic;
    }
    
    .mission-completion {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 30px;
        z-index: 10001;
        text-align: center;
        opacity: 0;
        animation: missionCompletionAppear 3s ease-in-out;
    }
    
    @keyframes missionCompletionAppear {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
        100% { opacity: 0; transform: translate(-50%, -50%) scale(1); }
    }
    
    .completion-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    
    .completion-content h3 {
        color: var(--violet-lunaire);
        margin-bottom: 10px;
    }
    
    .completion-rewards {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 15px;
    }
    
    .completion-rewards span {
        color: var(--bleu-spectre);
        font-weight: 600;
    }
    
    .all-missions-completed {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 40px;
        z-index: 10002;
        text-align: center;
        opacity: 0;
        animation: allMissionsCompletedAppear 5s ease-in-out;
    }
    
    @keyframes allMissionsCompletedAppear {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
        20% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
        80% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        100% { opacity: 0; transform: translate(-50%, -50%) scale(1); }
    }
    
    .celebration-icon {
        font-size: 4em;
        margin-bottom: 20px;
    }
    
    .celebration-content h2 {
        color: var(--violet-lunaire);
        margin-bottom: 15px;
    }
    
    .celebration-content p {
        color: var(--argent-holographique);
        font-size: 1.1em;
    }
`;
document.head.appendChild(style);

// Initialiser le système de missions du jour
document.addEventListener('DOMContentLoaded', () => {
    window.dailyMissions = new DailyMissionsEnhanced();
});

// Exporter pour utilisation globale
window.DailyMissionsEnhanced = DailyMissionsEnhanced;
