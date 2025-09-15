/**
 * Système avancé de gestion des profils de joueurs
 * Détection intelligente et adaptation en temps réel
 */

class AdvancedPlayerProfiles {
    constructor() {
        this.profiles = {
            debutant: new DebutantProfile(),
            experimente: new ExperimenteProfile(),
            competitif: new CompetitifProfile(),
            creatif: new CreatifProfile(),
            casual: new CasualProfile()
        };

        this.currentProfile = null;
        this.profileHistory = [];
        this.adaptationLevel = 0;
        this.learningRate = 0.1;

        this.initializeSystem();
    }

    initializeSystem() {
        // Détecter le profil initial
        this.detectInitialProfile();

        // Observer les changements de comportement
        this.observeBehaviorChanges();

        // Initialiser l'adaptation
        this.initializeAdaptation();

        console.log('👤 Système de profils avancés initialisé');
    }

    detectInitialProfile() {
        const interactions = this.loadInteractionHistory();
        const timeSpent = this.calculateTimeSpent();
        const commandPatterns = this.analyzeCommandPatterns(interactions);
        const uiInteractions = this.analyzeUIInteractions();

        // Calculer les scores pour chaque profil
        const scores = {
            debutant: this.calculateDebutantScore(commandPatterns, timeSpent, uiInteractions),
            experimente: this.calculateExperimenteScore(commandPatterns, timeSpent, uiInteractions),
            competitif: this.calculateCompetitifScore(commandPatterns, timeSpent, uiInteractions),
            creatif: this.calculateCreatifScore(commandPatterns, timeSpent, uiInteractions),
            casual: this.calculateCasualScore(commandPatterns, timeSpent, uiInteractions)
        };

        // Sélectionner le profil avec le score le plus élevé
        this.currentProfile = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);

        // Initialiser le profil
        this.profiles[this.currentProfile].activate();

        console.log(`👤 Profil détecté: ${this.currentProfile} (score: ${scores[this.currentProfile]})`);
    }

    calculateDebutantScore(commandPatterns, timeSpent, uiInteractions) {
        let score = 0;

        // Commandes d'aide fréquentes
        if (commandPatterns.includes('aide')) score += 3;
        if (commandPatterns.includes('help')) score += 3;
        if (commandPatterns.includes('tutoriel')) score += 2;

        // Temps de session court
        if (timeSpent < 300000) score += 2; // Moins de 5 minutes

        // Interactions UI basiques
        if (uiInteractions.includes('click_basic_button')) score += 1;
        if (uiInteractions.includes('hover_help')) score += 1;

        // Erreurs fréquentes
        if (this.countErrors() > 3) score += 2;

        return score;
    }

    calculateExperimenteScore(commandPatterns, timeSpent, uiInteractions) {
        let score = 0;

        // Commandes avancées
        if (commandPatterns.includes('profil')) score += 2;
        if (commandPatterns.includes('badges')) score += 2;
        if (commandPatterns.includes('dashboard')) score += 2;

        // Temps de session moyen
        if (timeSpent > 300000 && timeSpent < 1800000) score += 2;

        // Interactions UI avancées
        if (uiInteractions.includes('keyboard_shortcut')) score += 2;
        if (uiInteractions.includes('advanced_navigation')) score += 2;

        // Peu d'erreurs
        if (this.countErrors() < 2) score += 2;

        return score;
    }

    calculateCompetitifScore(commandPatterns, timeSpent, uiInteractions) {
        let score = 0;

        // Commandes compétitives
        if (commandPatterns.includes('leaderboard')) score += 3;
        if (commandPatterns.includes('score')) score += 2;
        if (commandPatterns.includes('badges')) score += 2;

        // Temps de session long
        if (timeSpent > 1800000) score += 2;

        // Interactions UI compétitives
        if (uiInteractions.includes('click_leaderboard')) score += 2;
        if (uiInteractions.includes('check_progress')) score += 2;

        // Recherche de défis
        if (commandPatterns.includes('challenge')) score += 2;
        if (commandPatterns.includes('duel')) score += 2;

        return score;
    }

    calculateCreatifScore(commandPatterns, timeSpent, uiInteractions) {
        let score = 0;

        // Commandes créatives
        if (commandPatterns.includes('theme')) score += 3;
        if (commandPatterns.includes('customize')) score += 2;
        if (commandPatterns.includes('accessibility')) score += 2;

        // Interactions UI créatives
        if (uiInteractions.includes('change_theme')) score += 2;
        if (uiInteractions.includes('customize_ui')) score += 2;

        // Exploration
        if (commandPatterns.includes('explore')) score += 1;
        if (commandPatterns.includes('discover')) score += 1;

        return score;
    }

    calculateCasualScore(commandPatterns, timeSpent, uiInteractions) {
        let score = 0;

        // Commandes casual
        if (commandPatterns.includes('profil')) score += 1;
        if (commandPatterns.includes('missions')) score += 1;

        // Temps de session très long
        if (timeSpent > 3600000) score += 3;

        // Interactions UI casual
        if (uiInteractions.includes('slow_click')) score += 2;
        if (uiInteractions.includes('gentle_navigation')) score += 2;

        // Peu d'activité
        if (commandPatterns.length < 5) score += 2;

        return score;
    }

    observeBehaviorChanges() {
        // Observer les nouvelles interactions
        setInterval(() => {
            this.analyzeRecentBehavior();
        }, 30000); // Toutes les 30 secondes

        // Observer les changements d'UI
        this.observeUIChanges();
    }

    analyzeRecentBehavior() {
        const recentInteractions = this.getRecentInteractions(30000); // 30 secondes
        const behaviorScore = this.calculateBehaviorScore(recentInteractions);

        // Adapter le profil si nécessaire
        if (behaviorScore > 0.7) {
            this.adaptProfile('more_active');
        } else if (behaviorScore < 0.3) {
            this.adaptProfile('less_active');
        }
    }

    calculateBehaviorScore(interactions) {
        if (interactions.length === 0) return 0;

        let score = 0;
        interactions.forEach(interaction => {
            if (interaction.success) score += 1;
            if (interaction.complexity > 0.5) score += 0.5;
            if (interaction.speed > 0.7) score += 0.3;
        });

        return score / interactions.length;
    }

    adaptProfile(direction) {
        this.adaptationLevel += direction === 'more_active' ? this.learningRate : -this.learningRate;
        this.adaptationLevel = Math.max(0, Math.min(1, this.adaptationLevel));

        // Adapter le profil actuel
        this.profiles[this.currentProfile].adapt(this.adaptationLevel);

        console.log(`🔄 Profil adapté: ${this.currentProfile} (niveau: ${this.adaptationLevel.toFixed(2)})`);
    }

    initializeAdaptation() {
        // Adapter l'interface selon le profil
        this.adaptInterface();

        // Adapter les messages
        this.adaptMessages();

        // Adapter les animations
        this.adaptAnimations();
    }

    adaptInterface() {
        const profile = this.profiles[this.currentProfile];

        // Adapter les couleurs
        document.documentElement.style.setProperty('--primary-color', profile.colors.primary);
        document.documentElement.style.setProperty('--secondary-color', profile.colors.secondary);
        document.documentElement.style.setProperty('--accent-color', profile.colors.accent);

        // Adapter les tailles
        document.documentElement.style.setProperty('--font-size', profile.sizes.font);
        document.documentElement.style.setProperty('--button-size', profile.sizes.button);
        document.documentElement.style.setProperty('--spacing', profile.sizes.spacing);

        // Adapter les animations
        document.documentElement.style.setProperty('--animation-speed', profile.animations.speed);
        document.documentElement.style.setProperty('--animation-intensity', profile.animations.intensity);
    }

    adaptMessages() {
        // Adapter les messages selon le profil
        const profile = this.profiles[this.currentProfile];

        // Remplacer les messages génériques
        const genericMessages = document.querySelectorAll('.generic-message');
        genericMessages.forEach(message => {
            message.textContent = profile.getPersonalizedMessage(message.dataset.type);
        });
    }

    adaptAnimations() {
        const profile = this.profiles[this.currentProfile];

        // Adapter les animations selon le profil
        if (profile.animations.enabled) {
            document.body.classList.add('animations-enabled');
        } else {
            document.body.classList.remove('animations-enabled');
        }
    }

    // Méthodes utilitaires
    loadInteractionHistory() {
        try {
            return JSON.parse(localStorage.getItem('arkalia_interaction_history') || '[]');
        } catch {
            return [];
        }
    }

    calculateTimeSpent() {
        const startTime = localStorage.getItem('arkalia_session_start');
        if (startTime) {
            return Date.now() - parseInt(startTime);
        }
        return 0;
    }

    analyzeCommandPatterns(interactions) {
        return interactions.map(interaction => interaction.action);
    }

    analyzeUIInteractions() {
        // Analyser les interactions UI (à implémenter)
        return [];
    }

    countErrors() {
        const interactions = this.loadInteractionHistory();
        return interactions.filter(interaction => !interaction.success).length;
    }

    getRecentInteractions(timeframe) {
        const interactions = this.loadInteractionHistory();
        const now = Date.now();
        return interactions.filter(interaction => {
            const interactionTime = new Date(interaction.timestamp).getTime();
            return now - interactionTime < timeframe;
        });
    }

    // Méthode publique pour changer de profil
    switchProfile(profileName) {
        console.log(`🔄 Tentative de changement vers: ${profileName}`);
        console.log(`📋 Profils disponibles:`, Object.keys(this.profiles));

        if (this.profiles[profileName]) {
            this.currentProfile = profileName;
            this.profiles[profileName].activate();
            this.adaptInterface();
            this.adaptMessages();
            this.adaptAnimations();

            console.log(`✅ Profil changé vers: ${profileName}`);
            return true;
        } else {
            console.error(`❌ Profil ${profileName} non trouvé`);
            return false;
        }
    }

    // Méthode publique pour obtenir le profil actuel
    getCurrentProfile() {
        return {
            name: this.currentProfile,
            level: this.adaptationLevel,
            characteristics: this.profiles[this.currentProfile].getCharacteristics()
        };
    }
}

// Classe de base pour les profils
class BaseProfile {
    constructor(name) {
        this.name = name;
        this.colors = this.getColors();
        this.sizes = this.getSizes();
        this.animations = this.getAnimations();
        this.messages = this.getMessages();
    }

    activate() {
        console.log(`👤 Profil ${this.name} activé`);
    }

    adapt(level) {
        // Adapter le profil selon le niveau d'adaptation
        this.adaptationLevel = level;
    }

    getCharacteristics() {
        return {
            name: this.name,
            colors: this.colors,
            sizes: this.sizes,
            animations: this.animations
        };
    }

    getPersonalizedMessage(type) {
        return this.messages[type] || 'Message personnalisé';
    }
}

// Profil Débutant
class DebutantProfile extends BaseProfile {
    constructor() {
        super('debutant');
    }

    getColors() {
        return {
            primary: '#00ff00',
            secondary: '#0080ff',
            accent: '#ffff00'
        };
    }

    getSizes() {
        return {
            font: '1.1rem',
            button: 'large',
            spacing: 'comfortable'
        };
    }

    getAnimations() {
        return {
            enabled: true,
            speed: 'slow',
            intensity: 'gentle'
        };
    }

    getMessages() {
        return {
            welcome: '🌟 Bienvenue ! Je suis LUNA, ton assistant. Je vais t\'aider à apprendre !',
            help: '💡 N\'hésite pas à demander de l\'aide ! Je suis là pour toi.',
            error: '🤔 Pas de souci ! Chaque erreur est une occasion d\'apprendre.',
            success: '🎉 Bravo ! Tu apprends vite !',
            progress: '📈 Tu progresses bien ! Continue comme ça !'
        };
    }
}

// Profil Expérimenté
class ExperimenteProfile extends BaseProfile {
    constructor() {
        super('experimente');
    }

    getColors() {
        return {
            primary: '#0080ff',
            secondary: '#00ff00',
            accent: '#ff8000'
        };
    }

    getSizes() {
        return {
            font: '1rem',
            button: 'medium',
            spacing: 'balanced'
        };
    }

    getAnimations() {
        return {
            enabled: true,
            speed: 'medium',
            intensity: 'moderate'
        };
    }

    getMessages() {
        return {
            welcome: '⚡ Salut ! Je vois que tu es expérimenté. Prêt pour des défis ?',
            help: '🔧 Tu connais déjà les bases. Que veux-tu explorer ?',
            error: '⚡ Erreur détectée. Vérifie la syntaxe.',
            success: '🎯 Excellent ! Tu maîtrises parfaitement.',
            progress: '📊 Progression optimale ! Tu es efficace.'
        };
    }
}

// Profil Compétitif
class CompetitifProfile extends BaseProfile {
    constructor() {
        super('competitif');
    }

    getColors() {
        return {
            primary: '#ff8000',
            secondary: '#ff0000',
            accent: '#ffff00'
        };
    }

    getSizes() {
        return {
            font: '0.9rem',
            button: 'small',
            spacing: 'compact'
        };
    }

    getAnimations() {
        return {
            enabled: true,
            speed: 'fast',
            intensity: 'high'
        };
    }

    getMessages() {
        return {
            welcome: '🏆 Champion ! Prêt à dominer ?',
            help: '⚔️ Tu veux gagner ? Voici tes armes !',
            error: '⚔️ Erreur de guerre ! Corrige et continue !',
            success: '👑 VICTOIRE ! Tu es le meilleur !',
            progress: '🏆 Tu domines ! Continue à écraser la concurrence !'
        };
    }
}

// Profil Créatif
class CreatifProfile extends BaseProfile {
    constructor() {
        super('creatif');
    }

    getColors() {
        return {
            primary: '#ff00ff',
            secondary: '#00ffff',
            accent: '#ffff00'
        };
    }

    getSizes() {
        return {
            font: '1.2rem',
            button: 'large',
            spacing: 'spacious'
        };
    }

    getAnimations() {
        return {
            enabled: true,
            speed: 'variable',
            intensity: 'artistic'
        };
    }

    getMessages() {
        return {
            welcome: '🎨 Artiste ! Prêt à créer quelque chose d\'unique ?',
            help: '💫 Laisse libre cours à ta créativité !',
            error: '🎨 Erreur créative ! Essaie autre chose !',
            success: '✨ Chef-d\'œuvre ! Tu es un artiste !',
            progress: '🌟 Ta créativité s\'épanouit ! Continue !'
        };
    }
}

// Profil Casual
class CasualProfile extends BaseProfile {
    constructor() {
        super('casual');
    }

    getColors() {
        return {
            primary: '#ffff00',
            secondary: '#00ff00',
            accent: '#0080ff'
        };
    }

    getSizes() {
        return {
            font: '1.1rem',
            button: 'large',
            spacing: 'comfortable'
        };
    }

    getAnimations() {
        return {
            enabled: true,
            speed: 'slow',
            intensity: 'gentle'
        };
    }

    getMessages() {
        return {
            welcome: '😊 Salut ! Prends ton temps, on va bien s\'amuser !',
            help: '🌟 Pas de stress ! Je suis là pour t\'aider.',
            error: '😊 Pas de souci ! On va y arriver ensemble.',
            success: '😊 Super ! Tu avances à ton rythme !',
            progress: '🌟 Belle progression ! Tu prends ton temps, c\'est parfait !'
        };
    }
}

// Initialiser immédiatement et exporter
try {
    window.advancedPlayerProfiles = new AdvancedPlayerProfiles();
    window.AdvancedPlayerProfiles = AdvancedPlayerProfiles;
    console.log('✅ advancedPlayerProfiles initialisé immédiatement');
} catch (error) {
    console.error('❌ Erreur initialisation advancedPlayerProfiles:', error);
    // Créer un objet de fallback
    window.advancedPlayerProfiles = {
        switchProfile: function (profileName) {
            console.log('⚠️ Mode fallback - switchProfile appelé avec:', profileName);
            return true;
        },
        getCurrentProfile: function () {
            return { name: 'fallback', level: 0, characteristics: {} };
        }
    };
}
