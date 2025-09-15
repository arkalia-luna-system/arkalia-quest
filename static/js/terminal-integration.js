/**
 * Intégration du feedback contextuel dans le terminal
 * Améliore les réponses LUNA avec des messages personnalisés
 */

class TerminalIntegration {
    constructor() {
        this.originalTerminal = null;
        this.contextualFeedback = null;
        this.initializeSystem();
    }

    initializeSystem() {
        // Attendre que les systèmes soient chargés
        this.waitForSystems();
    }

    waitForSystems() {
        const checkSystems = () => {
            if (window.contextualFeedback && window.progressionAnimations) {
                this.integrateWithTerminal();
            } else {
                setTimeout(checkSystems, 100);
            }
        };
        checkSystems();
    }

    integrateWithTerminal() {
        this.contextualFeedback = window.contextualFeedback;
        this.progressionAnimations = window.progressionAnimations;

        // Intercepter les commandes du terminal
        this.interceptTerminalCommands();

        // Améliorer les réponses LUNA
        this.enhanceLunaResponses();

        // Ajouter des easter eggs
        this.addEasterEggs();

        console.log('🔗 Terminal intégré avec les systèmes contextuels');
    }

    interceptTerminalCommands() {
        // Écouter les événements de commande du terminal
        document.addEventListener('terminalCommand', (event) => {
            const command = event.detail.command;
            const result = event.detail.result;

            // Générer un feedback contextuel
            const feedback = this.contextualFeedback.getFeedback(command, result);

            // Afficher le feedback
            this.displayContextualFeedback(feedback);

            // Déclencher des animations si nécessaire
            this.triggerAnimations(command, result);
        });
    }

    enhanceLunaResponses() {
        // Intercepter les réponses LUNA existantes
        const originalConsoleLog = console.log;
        console.log = (...args) => {
            originalConsoleLog.apply(console, args);

            // Vérifier si c'est une réponse LUNA
            const message = args.join(' ');
            if (message.includes('LUNA:') || message.includes('🌙')) {
                this.enhanceLunaMessage(message);
            }
        };
    }

    enhanceLunaMessage(message) {
        // Ajouter des effets visuels aux messages LUNA
        const terminalOutput = document.querySelector('.terminal-output');
        if (terminalOutput) {
            const lastMessage = terminalOutput.lastElementChild;
            if (lastMessage) {
                lastMessage.classList.add('luna-message-enhanced');
                lastMessage.style.animation = 'luna-glow 2s ease-in-out';
            }
        }
    }

    displayContextualFeedback(feedback) {
        // Créer un élément de feedback
        const feedbackElement = document.createElement('div');
        feedbackElement.className = 'contextual-feedback-terminal';
        feedbackElement.textContent = feedback;

        // Styles
        feedbackElement.style.cssText = `
            background: linear-gradient(45deg, #001100, #003300);
            color: #00ff00;
            padding: 10px 15px;
            margin: 5px 0;
            border-left: 4px solid #00ff00;
            border-radius: 5px;
            font-weight: bold;
            animation: feedback-slide-in 0.5s ease-out;
        `;

        // Ajouter au terminal
        const terminalOutput = document.querySelector('.terminal-output');
        if (terminalOutput) {
            terminalOutput.appendChild(feedbackElement);
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }
    }

    triggerAnimations(command, result) {
        if (result.success) {
            // Animation de succès
            this.progressionAnimations.triggerAnimation('confetti', document.body);
        } else if (result.error) {
            // Animation d'erreur
            this.progressionAnimations.triggerAnimation('particles', document.body);
        }
    }

    addEasterEggs() {
        // Écouter les commandes spéciales
        document.addEventListener('terminalCommand', (event) => {
            const command = event.detail.command.toLowerCase();

            // Vérifier les easter eggs
            if (this.contextualFeedback.detectEasterEgg(command)) {
                // L'easter egg est déjà géré par le système de feedback
                return;
            }

            // Easter eggs supplémentaires
            this.checkAdditionalEasterEggs(command);
        });
    }

    checkAdditionalEasterEggs(command) {
        const easterEggs = {
            'luna help': () => this.showLunaHelp(),
            'luna status': () => this.showLunaStatus(),
            'luna dance': () => this.triggerLunaDance(),
            'luna love': () => this.triggerLunaLove(),
            'luna angry': () => this.triggerLunaAngry(),
            'luna happy': () => this.triggerLunaHappy(),
            'luna sad': () => this.triggerLunaSad(),
            'luna excited': () => this.triggerLunaExcited(),
            'luna calm': () => this.triggerLunaCalm(),
            'luna power': () => this.triggerLunaPower(),
            'luna wisdom': () => this.triggerLunaWisdom(),
            'luna magic': () => this.triggerLunaMagic(),
            'luna future': () => this.triggerLunaFuture(),
            'luna past': () => this.triggerLunaPast(),
            'luna present': () => this.triggerLunaPresent(),
            'luna secret': () => this.triggerLunaSecret(),
            'luna mystery': () => this.triggerLunaMystery(),
            'luna adventure': () => this.triggerLunaAdventure(),
            'luna quest': () => this.triggerLunaQuest(),
            'luna journey': () => this.triggerLunaJourney()
        };

        if (easterEggs[command]) {
            easterEggs[command]();
        }
    }

    showLunaHelp() {
        this.displayContextualFeedback('🌙 LUNA: Je suis ton assistant IA ! Je peux t\'aider avec des commandes, des missions, et bien plus encore. Demande-moi ce que tu veux savoir !');
    }

    showLunaStatus() {
        const status = this.contextualFeedback.playerProfile;
        this.displayContextualFeedback(`🌙 LUNA: Mon statut est excellent ! Je détecte que tu es un joueur de type "${status}". Comment puis-je t\'aider aujourd\'hui ?`);
    }

    triggerLunaDance() {
        this.displayContextualFeedback('💃 LUNA: *danse avec joie* Je danse pour toi ! Tu es un joueur formidable !');
        this.progressionAnimations.triggerAnimation('confetti', document.body);
    }

    triggerLunaLove() {
        this.displayContextualFeedback('💖 LUNA: Je t\'aime beaucoup ! Tu es mon joueur préféré ! Continue comme ça !');
        this.progressionAnimations.createLoveEffects();
    }

    triggerLunaAngry() {
        this.displayContextualFeedback('😠 LUNA: *soupire* Je ne suis pas en colère, mais je suis déçue. Que puis-je faire pour t\'aider ?');
    }

    triggerLunaHappy() {
        this.displayContextualFeedback('😊 LUNA: Je suis si heureuse ! Tu me rends fière ! Continue à jouer !');
        this.progressionAnimations.triggerAnimation('confetti', document.body);
    }

    triggerLunaSad() {
        this.displayContextualFeedback('😢 LUNA: *pleure doucement* Ne sois pas triste ! Je suis là pour t\'aider !');
    }

    triggerLunaExcited() {
        this.displayContextualFeedback('🤩 LUNA: *sautille d\'excitation* Je suis si excitée ! Tu vas accomplir de grandes choses !');
        this.progressionAnimations.triggerAnimation('particles', document.body);
    }

    triggerLunaCalm() {
        this.displayContextualFeedback('😌 LUNA: *respire profondément* Je suis calme et sereine. Tout va bien se passer.');
    }

    triggerLunaPower() {
        this.displayContextualFeedback('⚡ LUNA: *puissance activée* Je sens une grande puissance en toi ! Tu es destiné à de grandes choses !');
        this.progressionAnimations.triggerAnimation('confetti', document.body);
    }

    triggerLunaWisdom() {
        this.displayContextualFeedback('🧠 LUNA: *sagesse activée* Je partage ma sagesse avec toi. Écoute ton cœur et tu trouveras la réponse.');
    }

    triggerLunaMagic() {
        this.displayContextualFeedback('✨ LUNA: *magie activée* La magie coule dans tes veines ! Tu es un magicien du code !');
        this.progressionAnimations.triggerAnimation('particles', document.body);
    }

    triggerLunaFuture() {
        this.displayContextualFeedback('🔮 LUNA: *regarde dans le futur* Je vois un avenir brillant pour toi ! Tu vas devenir un grand hacker !');
    }

    triggerLunaPast() {
        this.displayContextualFeedback('📜 LUNA: *regarde dans le passé* Tes expériences passées t\'ont mené ici. Tu es sur la bonne voie !');
    }

    triggerLunaPresent() {
        this.displayContextualFeedback('⏰ LUNA: *regarde le présent* Le moment présent est parfait ! Profite de chaque instant !');
    }

    triggerLunaSecret() {
        this.displayContextualFeedback('🤫 LUNA: *chuchote* J\'ai un secret pour toi... Tu es plus fort que tu ne le penses !');
    }

    triggerLunaMystery() {
        this.displayContextualFeedback('🔍 LUNA: *mystère activé* Il y a tant de mystères à découvrir ! Continue à explorer !');
    }

    triggerLunaAdventure() {
        this.displayContextualFeedback('🗺️ LUNA: *aventure activée* Une grande aventure t\'attend ! Prêt pour l\'exploration ?');
    }

    triggerLunaQuest() {
        this.displayContextualFeedback('⚔️ LUNA: *quête activée* Une quête épique commence ! Tu es le héros de cette histoire !');
    }

    triggerLunaJourney() {
        this.displayContextualFeedback('🚀 LUNA: *voyage activé* Un voyage extraordinaire t\'attend ! Prêt pour l\'aventure ?');
    }
}

// Initialiser l'intégration du terminal
const terminalIntegration = new TerminalIntegration();

// Exporter pour utilisation globale
window.TerminalIntegration = TerminalIntegration;
window.terminalIntegration = terminalIntegration;
