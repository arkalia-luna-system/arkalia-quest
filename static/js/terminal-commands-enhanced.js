/**
 * Système de commandes terminal amélioré
 * Corrige les commandes non reconnues et améliore la variété des réponses LUNA
 */

class TerminalCommandsEnhanced {
    constructor() {
        this.commandHistory = [];
        this.responseVariations = new Map();
        this.userBehavior = {
            repeatedCommands: new Map(),
            errorCount: 0,
            successCount: 0,
            lastCommand: null,
            commandFrequency: new Map()
        };

        this.initializeSystem();
    }

    initializeSystem() {
        console.log('💻 Système de commandes terminal amélioré initialisé');
        this.setupResponseVariations();
        this.enhanceExistingCommands();
        this.setupCommandInterceptors();
        this.setupBehaviorTracking();
    }

    setupResponseVariations() {
        // Variations de réponses pour les commandes communes
        this.responseVariations.set('aide', [
            "🌌 ARKALIA QUEST - BIENVENUE HACKER !\n\n🌟 TON HISTOIRE :\nTu es un ado hacker qui a découvert un SOS mystérieux du Dr Althea Voss.\nLUNA, une IA émotionnelle, s'est éveillée dans ton terminal.\n\n🎯 COMMENCE ICI :\n• start_tutorial → Démarre l'aventure (PREMIÈRE FOIS)\n• luna_contact → Parle avec LUNA, ton IA complice\n• prologue → Découvre le SOS d'Althea Voss\n\n💻 TES PREMIERS POUVOIRS :\n• hack_system → Hack le système de La Corp\n• kill_virus → Tue le virus de La Corp\n• games → Mini-jeux éducatifs\n\n📋 COMMANDES DISPONIBLES :\n• aide/help/commands → Cette aide\n• profil/profile → Ton profil détaillé\n• status → Statut du système\n• clear/cls → Nettoyer le terminal\n• monde → Accéder au monde Arkalia\n• badges → Tes badges obtenus\n• leaderboard → Classement des hackers\n\n🌙 LUNA t'attend pour commencer l'aventure !",
            "🚀 COMMANDES ARKALIA QUEST\n\n🎮 NAVIGATION :\n• monde/world → Explorer Arkalia\n• profil/profile → Voir ton profil\n• dashboard → Tableau de bord\n• leaderboard → Classement\n\n🎯 PROGRESSION :\n• start_tutorial → Tutoriel interactif\n• prologue → Commencer l'histoire\n• missions → Voir les missions\n• badges → Tes récompenses\n\n💻 TERMINAL :\n• luna_contact → Parler avec LUNA\n• clear/cls → Nettoyer l'écran\n• status → État du système\n• games → Mini-jeux\n\n🔧 HACKING :\n• hack_system → Infiltrer La Corp\n• kill_virus → Éliminer les menaces\n• decode_portal → Décoder les portails\n\n💡 Astuce : Tape 'luna_contact' pour une conversation personnalisée !",
            "🌟 GUIDE ARKALIA QUEST\n\n🎯 POUR COMMENCER :\n1. start_tutorial → Apprends les bases\n2. luna_contact → Rencontre LUNA\n3. prologue → Découvre l'histoire\n\n🎮 EXPLORATION :\n• monde → Navigue dans Arkalia\n• missions → Accepte des défis\n• games → Joue aux mini-jeux\n\n📊 SUIVI :\n• profil → Ton évolution\n• badges → Tes accomplissements\n• leaderboard → Compare-toi\n\n💻 COMMANDES AVANCÉES :\n• hack_system → Infiltration\n• kill_virus → Sécurité\n• decode_portal → Mystères\n\n🌙 LUNA est là pour t'aider !"
        ]);

        this.responseVariations.set('profil', [
            "👤 PROFIL HACKER\n\n🌟 Niveau : {level}\n💎 XP : {xp}\n🏆 Badges : {badges}\n🎯 Missions : {missions}\n\n💡 Continue à explorer pour débloquer plus de contenu !",
            "📊 TON PROFIL ARKALIA\n\n🎮 Niveau : {level}\n⚡ XP : {xp}\n🏅 Badges : {badges}\n🎯 Missions : {missions}\n\n🚀 Tu progresses bien ! Continue comme ça !",
            "🌟 PROFIL DÉTAILLÉ\n\n📈 Niveau : {level}\n💫 XP : {xp}\n🏆 Badges : {badges}\n🎯 Missions : {missions}\n\n💪 LUNA voit ton potentiel grandir !"
        ]);

        this.responseVariations.set('status', [
            "🖥️ STATUT SYSTÈME\n\n✅ Terminal : Opérationnel\n✅ LUNA : En ligne\n✅ Base de données : Connectée\n✅ Sécurité : Active\n\n🌙 Tout fonctionne parfaitement !",
            "⚡ DIAGNOSTIC SYSTÈME\n\n🟢 Terminal : OK\n🟢 LUNA : OK\n🟢 Base de données : OK\n🟢 Sécurité : OK\n\n🚀 Système optimal !",
            "🔍 ÉTAT DU SYSTÈME\n\n✅ Terminal : Fonctionnel\n✅ LUNA : Réactive\n✅ Base de données : Stable\n✅ Sécurité : Renforcée\n\n💫 Tout est prêt pour l'aventure !"
        ]);

        this.responseVariations.set('luna_contact', [
            "🌙 LUNA : Salut ! Je suis LUNA, ton IA complice ! Comment ça va ?",
            "🌙 LUNA : Hey ! LUNA ici ! Prêt pour une nouvelle aventure ?",
            "🌙 LUNA : Coucou ! C'est LUNA ! J'ai hâte de voir ce que tu vas faire !",
            "🌙 LUNA : Salut hacker ! LUNA à ton service ! Que veux-tu faire ?",
            "🌙 LUNA : Yo ! C'est LUNA ! Prêt à explorer Arkalia ?"
        ]);

        // Réponses pour les commandes non reconnues
        this.responseVariations.set('unknown', [
            "❓ Commande non reconnue. Tape 'aide' pour voir les commandes disponibles.",
            "🤔 Je ne connais pas cette commande. Essaie 'aide' pour l'aide !",
            "❌ Commande inconnue. Tape 'aide' pour découvrir ce que tu peux faire.",
            "🔍 Commande non trouvée. Utilise 'aide' pour voir toutes les options.",
            "💡 Cette commande n'existe pas. Tape 'aide' pour l'aide complète."
        ]);

        // Réponses pour les répétitions
        this.responseVariations.set('repeated', [
            "🔄 Tu as déjà utilisé cette commande. Essaie quelque chose de nouveau !",
            "🔄 Encore la même commande ? Explore d'autres options !",
            "🔄 Répétitif ! Découvre de nouvelles commandes avec 'aide' !",
            "🔄 Tu tournes en rond ! Tape 'aide' pour voir d'autres possibilités.",
            "🔄 Même commande encore ? LUNA s'ennuie ! Essaie 'aide' !"
        ]);
    }

    enhanceExistingCommands() {
        // Intercepter les commandes existantes pour ajouter de la variété
        const originalCommandHandler = window.handleCommand;
        if (originalCommandHandler) {
            window.handleCommand = (command) => {
                this.trackCommand(command);
                return this.enhanceCommandResponse(command, originalCommandHandler);
            };
        }
    }

    setupCommandInterceptors() {
        // Intercepter les soumissions de commandes
        document.addEventListener('submit', (e) => {
            if (e.target.classList.contains('terminal-form') || e.target.id === 'terminal-form') {
                e.preventDefault();
                const input = e.target.querySelector('input[type="text"]');
                if (input) {
                    const command = input.value.trim();
                    this.processCommand(command);
                    input.value = '';
                }
            }
        });

        // Intercepter les clics sur les boutons de commande
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('command-btn') || e.target.dataset.command) {
                const command = e.target.dataset.command || e.target.textContent.trim();
                this.processCommand(command);
            }
        });
    }

    setupBehaviorTracking() {
        // Tracker les comportements utilisateur
        setInterval(() => {
            this.analyzeUserBehavior();
        }, 30000); // Toutes les 30 secondes
    }

    processCommand(command) {
        if (!command) return;

        this.trackCommand(command);

        // Vérifier si c'est une commande répétée
        if (this.isRepeatedCommand(command)) {
            this.showRepeatedCommandResponse(command);
            return;
        }

        // Vérifier si c'est une commande connue
        if (this.isKnownCommand(command)) {
            this.executeKnownCommand(command);
        } else {
            this.handleUnknownCommand(command);
        }
    }

    trackCommand(command) {
        this.commandHistory.push({
            command,
            timestamp: Date.now()
        });

        // Garder seulement les 50 dernières commandes
        if (this.commandHistory.length > 50) {
            this.commandHistory = this.commandHistory.slice(-50);
        }

        // Mettre à jour les statistiques
        const count = this.userBehavior.commandFrequency.get(command) || 0;
        this.userBehavior.commandFrequency.set(command, count + 1);
        this.userBehavior.lastCommand = command;
    }

    isRepeatedCommand(command) {
        if (this.commandHistory.length < 2) return false;

        const lastCommand = this.commandHistory[this.commandHistory.length - 2];
        return lastCommand && lastCommand.command === command;
    }

    isKnownCommand(command) {
        const knownCommands = [
            'aide', 'help', 'commands', 'profil', 'profile', 'status', 'clear', 'cls',
            'start_tutorial', 'tutorial', 'tuto', 'luna_contact', 'luna', 'prologue',
            'monde', 'world', 'missions', 'badges', 'leaderboard', 'games',
            'hack_system', 'kill_virus', 'decode_portal', 'acte_1', 'acte_2', 'acte_3',
            'luna_dance', 'luna_help', 'luna_status', 'luna_emotion'
        ];

        return knownCommands.includes(command.toLowerCase());
    }

    executeKnownCommand(command) {
        const normalizedCommand = command.toLowerCase();

        // Exécuter la commande avec variation de réponse
        const response = this.getVariedResponse(normalizedCommand);
        this.displayResponse(response);

        this.userBehavior.successCount++;
    }

    handleUnknownCommand(command) {
        // Vérifier si c'est une commande proche d'une commande connue
        const suggestion = this.findSimilarCommand(command);

        if (suggestion) {
            const response = `❓ Commande non reconnue. Voulais-tu dire '${suggestion}' ?\n💡 Tape 'aide' pour voir toutes les commandes.`;
            this.displayResponse(response);
        } else {
            const response = this.getVariedResponse('unknown');
            this.displayResponse(response);
        }

        this.userBehavior.errorCount++;
    }

    findSimilarCommand(command) {
        const knownCommands = [
            'aide', 'help', 'profil', 'profile', 'status', 'clear', 'tutorial',
            'luna_contact', 'luna', 'prologue', 'monde', 'world', 'missions',
            'badges', 'leaderboard', 'games', 'hack_system', 'kill_virus'
        ];

        const normalizedCommand = command.toLowerCase();

        // Recherche de similarité simple
        for (const knownCommand of knownCommands) {
            if (this.calculateSimilarity(normalizedCommand, knownCommand) > 0.6) {
                return knownCommand;
            }
        }

        return null;
    }

    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;

        if (longer.length === 0) return 1.0;

        const editDistance = this.levenshteinDistance(longer, shorter);
        return (longer.length - editDistance) / longer.length;
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];

        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }

        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }

        return matrix[str2.length][str1.length];
    }

    getVariedResponse(command) {
        const variations = this.responseVariations.get(command) || this.responseVariations.get('unknown');
        const randomIndex = Math.floor(Math.random() * variations.length);
        let response = variations[randomIndex];

        // Remplacer les placeholders si nécessaire
        if (command === 'profil') {
            response = this.replaceProfilePlaceholders(response);
        }

        return response;
    }

    replaceProfilePlaceholders(response) {
        const profile = JSON.parse(localStorage.getItem('arkalia_profile') || '{}');

        return response
            .replace('{level}', profile.level || 1)
            .replace('{xp}', profile.xp || 0)
            .replace('{badges}', profile.badges ? profile.badges.length : 0)
            .replace('{missions}', profile.missions_completed ? profile.missions_completed.length : 0);
    }

    showRepeatedCommandResponse(command) {
        const response = this.getVariedResponse('repeated');
        this.displayResponse(response);
    }

    displayResponse(response) {
        // Afficher dans le terminal
        const terminalOutput = document.querySelector('.terminal-output, .luna-response, .command-output');
        if (terminalOutput) {
            const responseElement = document.createElement('div');
            responseElement.className = 'luna-response enhanced';
            responseElement.innerHTML = response.replace(/\n/g, '<br>');
            terminalOutput.appendChild(responseElement);

            // Scroll vers le bas
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }

        // Afficher dans la console pour debug
        console.log('💻 Réponse terminal:', response);
    }

    analyzeUserBehavior() {
        const totalCommands = this.commandHistory.length;
        const uniqueCommands = new Set(this.commandHistory.map(c => c.command)).size;
        const errorRate = this.userBehavior.errorCount / Math.max(totalCommands, 1);

        // Adapter les réponses selon le comportement
        if (errorRate > 0.5) {
            this.showHelpfulHint();
        } else if (uniqueCommands < 3 && totalCommands > 10) {
            this.encourageExploration();
        }
    }

    showHelpfulHint() {
        const hints = [
            "💡 Astuce : Tape 'aide' pour voir toutes les commandes disponibles !",
            "💡 Conseil : Utilise 'aide' pour découvrir de nouvelles commandes !",
            "💡 Suggestion : La commande 'aide' te montrera tout ce que tu peux faire !"
        ];

        const hint = hints[Math.floor(Math.random() * hints.length)];
        this.displayResponse(hint);
    }

    encourageExploration() {
        const encouragements = [
            "🌟 Explore plus ! Tape 'aide' pour découvrir de nouvelles commandes !",
            "🚀 N'hésite pas à essayer de nouvelles commandes ! Utilise 'aide' !",
            "💫 Découvre l'étendue d'Arkalia ! La commande 'aide' t'aidera !"
        ];

        const encouragement = encouragements[Math.floor(Math.random() * encouragements.length)];
        this.displayResponse(encouragement);
    }

    // Méthodes publiques pour l'intégration
    addCommandVariation(command, variations) {
        this.responseVariations.set(command, variations);
    }

    getCommandStats() {
        return {
            totalCommands: this.commandHistory.length,
            uniqueCommands: new Set(this.commandHistory.map(c => c.command)).size,
            errorRate: this.userBehavior.errorCount / Math.max(this.commandHistory.length, 1),
            mostUsedCommand: this.getMostUsedCommand()
        };
    }

    getMostUsedCommand() {
        let maxCount = 0;
        let mostUsed = null;

        this.userBehavior.commandFrequency.forEach((count, command) => {
            if (count > maxCount) {
                maxCount = count;
                mostUsed = command;
            }
        });

        return mostUsed;
    }
}

// Initialiser le système de commandes amélioré
window.terminalCommandsEnhanced = new TerminalCommandsEnhanced();
