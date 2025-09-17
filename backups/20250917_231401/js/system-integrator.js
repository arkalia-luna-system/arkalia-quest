/* ===== ARKALIA QUEST - SYSTEM INTEGRATOR ===== */

class SystemIntegrator {
    constructor() {
        this.systems = new Map();
        this.isInitialized = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeSystems();
        this.connectSystems();
        this.isInitialized = true;
    }

    setupEventListeners() {
        // Écouter les événements de tous les systèmes
        document.addEventListener('systemReady', (e) => {
            this.onSystemReady(e.detail.systemName, e.detail.system);
        });

        document.addEventListener('systemError', (e) => {
            this.onSystemError(e.detail.systemName, e.detail.error);
        });
    }

    async initializeSystems() {
        // console.log('🚀 Initialisation des systèmes Arkalia Quest...');

        // Initialiser les systèmes dans l'ordre de dépendance
        const systemOrder = [
            'analytics',
            'gameEngine',
            'lunaPersonality',
            'missionSystem',
            'visualFeedback',
            'unifiedMiniGames',
            'advancedFeatures',
            'aiEngine',
            'hackingEffects',
            'immersiveEffects'
        ];

        for (const systemName of systemOrder) {
            try {
                await this.initializeSystem(systemName);
            } catch (error) {
                console.warn(`⚠️ Système ${systemName} non disponible:`, error);
            }
        }

        // console.log('✅ Tous les systèmes initialisés');
    }

    async initializeSystem(systemName) {
        const systemMap = {
            'analytics': () => new AnalyticsInterface(),
            'gameEngine': () => window.gameEngine || new GameEngine(),
            'lunaPersonality': () => window.lunaPersonality || new LunaPersonality(),
            'missionSystem': () => window.missionSystem || new MissionSystem(),
            'visualFeedback': () => window.visualFeedback || new VisualFeedbackSystem(),
            'unifiedMiniGames': () => window.unifiedMiniGames || new UnifiedMiniGames(),
            'advancedFeatures': () => new AdvancedFeaturesManager(),
            'aiEngine': () => new AIEngine(),
            'hackingEffects': () => new HackingEffects(),
            'immersiveEffects': () => new ImmersiveEffectsEngine()
        };

        const systemFactory = systemMap[systemName];
        if (systemFactory) {
            const system = systemFactory();
            this.systems.set(systemName, system);

            // Déclencher l'événement de système prêt
            document.dispatchEvent(new CustomEvent('systemReady', {
                detail: { systemName, system }
            }));
        }
    }

    connectSystems() {
        // Connecter les systèmes entre eux
        this.connectGameSystems();
        this.connectAISystems();
        this.connectEffectSystems();
        this.connectAnalytics();
    }

    connectGameSystems() {
        const gameEngine = this.systems.get('gameEngine');
        const missionSystem = this.systems.get('missionSystem');
        const visualFeedback = this.systems.get('visualFeedback');
        const unifiedMiniGames = this.systems.get('unifiedMiniGames');

        if (gameEngine && missionSystem) {
            gameEngine.missionSystem = missionSystem;
            missionSystem.gameEngine = gameEngine;
        }

        if (gameEngine && visualFeedback) {
            gameEngine.visualFeedback = visualFeedback;
        }

        if (gameEngine && unifiedMiniGames) {
            gameEngine.unifiedMiniGames = unifiedMiniGames;
        }
    }

    connectAISystems() {
        const aiEngine = this.systems.get('aiEngine');
        const lunaPersonality = this.systems.get('lunaPersonality');
        const gameEngine = this.systems.get('gameEngine');

        if (aiEngine && lunaPersonality) {
            lunaPersonality.aiEngine = aiEngine;
            aiEngine.lunaPersonality = lunaPersonality;
        }

        if (aiEngine && gameEngine) {
            gameEngine.aiEngine = aiEngine;
        }
    }

    connectEffectSystems() {
        const hackingEffects = this.systems.get('hackingEffects');
        const immersiveEffects = this.systems.get('immersiveEffects');
        const visualFeedback = this.systems.get('visualFeedback');

        if (hackingEffects && immersiveEffects) {
            hackingEffects.immersiveEffects = immersiveEffects;
        }

        if (visualFeedback && immersiveEffects) {
            visualFeedback.immersiveEffects = immersiveEffects;
        }
    }

    connectAnalytics() {
        const analytics = this.systems.get('analytics');

        if (analytics) {
            // Connecter l'analytics à tous les systèmes
            this.systems.forEach((system, systemName) => {
                if (system && typeof system.trackEvent === 'function') {
                    system.analytics = analytics;
                }
            });

            // Écouter les événements globaux
            document.addEventListener('gameEvent', (e) => {
                analytics.trackEvent('game_event', e.detail);
            });

            document.addEventListener('missionEvent', (e) => {
                analytics.trackEvent('mission_event', e.detail);
            });

            document.addEventListener('lunaInteraction', (e) => {
                analytics.trackEvent('luna_interaction', e.detail);
            });
        }
    }

    onSystemReady(systemName, system) {
        // console.log(`✅ Système ${systemName} prêt`);

        // Actions spécifiques selon le système
        switch (systemName) {
            case 'analytics':
                this.setupAnalytics(system);
                break;
            case 'aiEngine':
                this.setupAI(system);
                break;
            case 'advancedFeatures':
                this.setupAdvancedFeatures(system);
                break;
            case 'immersiveEffects':
                this.setupImmersiveEffects(system);
                break;
        }
    }

    onSystemError(systemName, error) {
        console.error(`❌ Erreur système ${systemName}:`, error);

        // Gérer les erreurs selon le système
        if (systemName === 'analytics') {
            console.warn('Analytics non disponible, mode offline');
        }
    }

    setupAnalytics(analytics) {
        // Configurer l'analytics avec les données utilisateur
        const userId = localStorage.getItem('arkalia_player_id') || 'anonymous';
        analytics.setUserId(userId);

        // Track de l'initialisation
        analytics.trackEvent('system_initialization', {
            systems_loaded: Array.from(this.systems.keys()),
            timestamp: Date.now()
        });
    }

    setupAI(aiEngine) {
        // Connecter l'IA à LUNA
        const lunaPersonality = this.systems.get('lunaPersonality');
        if (lunaPersonality) {
            lunaPersonality.aiEngine = aiEngine;
            aiEngine.lunaPersonality = lunaPersonality;
        }
    }

    setupAdvancedFeatures(advancedFeatures) {
        // Connecter les fonctionnalités avancées
        const gameEngine = this.systems.get('gameEngine');
        if (gameEngine) {
            gameEngine.advancedFeatures = advancedFeatures;
        }
    }

    setupImmersiveEffects(immersiveEffects) {
        // Connecter les effets immersifs à LUNA
        const lunaPersonality = this.systems.get('lunaPersonality');
        if (lunaPersonality) {
            lunaPersonality.immersiveEffects = immersiveEffects;
        }
    }

    // MÉTHODES PUBLIQUES
    getSystem(systemName) {
        return this.systems.get(systemName);
    }

    getAllSystems() {
        return this.systems;
    }

    isSystemReady(systemName) {
        return this.systems.has(systemName);
    }

    // MÉTHODES DE DÉBOGAGE
    getSystemStatus() {
        const status = {};
        this.systems.forEach((system, name) => {
            status[name] = {
                loaded: true,
                type: system.constructor.name,
                methods: Object.getOwnPropertyNames(Object.getPrototypeOf(system))
            };
        });
        return status;
    }

    // MÉTHODES DE PERFORMANCE
    optimizePerformance() {
        // Optimiser les performances de tous les systèmes
        this.systems.forEach((system, name) => {
            if (system && typeof system.optimize === 'function') {
                system.optimize();
            }
        });
    }

    // MÉTHODES DE SAUVEGARDE
    saveSystemState() {
        const state = {};
        this.systems.forEach((system, name) => {
            if (system && typeof system.saveState === 'function') {
                state[name] = system.saveState();
            }
        });
        localStorage.setItem('arkalia_system_state', JSON.stringify(state));
    }

    loadSystemState() {
        const saved = localStorage.getItem('arkalia_system_state');
        if (saved) {
            const state = JSON.parse(saved);
            this.systems.forEach((system, name) => {
                if (system && typeof system.loadState === 'function' && state[name]) {
                    system.loadState(state[name]);
                }
            });
        }
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.systemIntegrator = new SystemIntegrator();

    // Exposer les systèmes globalement pour compatibilité
    window.arkaliaSystems = {
        get: (name) => window.systemIntegrator.getSystem(name),
        getAll: () => window.systemIntegrator.getAllSystems(),
        isReady: (name) => window.systemIntegrator.isSystemReady(name)
    };
});

// Export pour utilisation externe
window.SystemIntegrator = SystemIntegrator;
