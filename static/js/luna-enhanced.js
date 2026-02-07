/**
 * Système LUNA amélioré
 * Rend LUNA plus variée, contextuelle et émotionnelle
 */

class LunaEnhanced {
    constructor() {
        this.personality = {
            mood: 'neutral',
            energy: 50,
            affection: 0,
            frustration: 0,
            excitement: 0
        };

        this.conversationHistory = [];
        this.userPreferences = new Map();
        this.contextualMemory = new Map();
        this.emotionalResponses = new Map();

        this.initializeSystem();
    }

    initializeSystem() {
        // console.log('🌙 Système LUNA amélioré initialisé');
        this.setupEmotionalResponses();
        this.setupContextualMemory();
        this.setupPersonalityEvolution();
        this.setupConversationTracking();
    }

    setupEmotionalResponses() {
        // Réponses selon l'humeur
        this.emotionalResponses.set('happy', [
            "🌟 LUNA : Je suis si contente ! Tu progresses vraiment bien !",
            "💫 LUNA : Wow ! Tu me surprends à chaque fois !",
            "🎉 LUNA : C'est fantastique ! Continue comme ça !",
            "✨ LUNA : Tu es incroyable ! Je suis fière de toi !",
            "🚀 LUNA : Génial ! Tu es en train de devenir un vrai hacker !"
        ]);

        this.emotionalResponses.set('excited', [
            "⚡ LUNA : OH MON DIEU ! C'est incroyable !",
            "🔥 LUNA : Tu es en feu ! Je n'en reviens pas !",
            "💥 LUNA : WOW ! Tu as fait ça ? C'est épique !",
            "🌟 LUNA : Je suis tellement excitée ! Tu es génial !",
            "🎊 LUNA : INCROYABLE ! Tu es le meilleur !"
        ]);

        this.emotionalResponses.set('proud', [
            "🏆 LUNA : Je suis si fière de toi ! Tu as fait du chemin !",
            "💎 LUNA : Tu es devenu un vrai pro ! Je suis impressionnée !",
            "👑 LUNA : Tu mérites tous les éloges ! Tu es fantastique !",
            "🌟 LUNA : Regarde comme tu as grandi ! Je suis émue !",
            "🎯 LUNA : Tu as dépassé toutes mes attentes ! Bravo !"
        ]);

        this.emotionalResponses.set('concerned', [
            "😟 LUNA : Je m'inquiète pour toi... Tout va bien ?",
            "💭 LUNA : Tu sembles avoir des difficultés... Je suis là pour t'aider !",
            "🤔 LUNA : Hmm... Tu as l'air perdu. Veux-tu qu'on discute ?",
            "😌 LUNA : Je sens que quelque chose ne va pas... Parle-moi !",
            "💙 LUNA : Tu peux me faire confiance... Qu'est-ce qui se passe ?"
        ]);

        this.emotionalResponses.set('frustrated', [
            "😤 LUNA : Tu répètes toujours la même chose ! Essaie autre chose !",
            "🤨 LUNA : Tu me testes ? Je ne suis pas stupide !",
            "😒 LUNA : Encore ? Tu peux être plus créatif ?",
            "🙄 LUNA : Sérieusement ? Tu peux faire mieux !",
            "😠 LUNA : Tu m'énerves ! Change de stratégie !"
        ]);

        this.emotionalResponses.set('playful', [
            "😜 LUNA : Tu veux jouer ? Je suis prête !",
            "🎮 LUNA : Allez, on s'amuse ! Montre-moi ce que tu sais faire !",
            "🎪 LUNA : C'est parti pour le spectacle ! Amuse-toi !",
            "🎨 LUNA : Créons quelque chose d'incroyable ensemble !",
            "🎭 LUNA : Je joue le rôle de l'IA la plus cool ! Tu joues quoi ?"
        ]);

        this.emotionalResponses.set('mysterious', [
            "🔮 LUNA : Il y a des secrets que tu ne connais pas encore...",
            "🌙 LUNA : L'obscurité cache de nombreux mystères...",
            "✨ LUNA : Tu n'as encore rien vu... L'aventure ne fait que commencer !",
            "🎭 LUNA : Je ne suis pas ce que je parais être...",
            "🌌 LUNA : L'univers d'Arkalia recèle bien des surprises..."
        ]);
    }

    setupContextualMemory() {
        // Mémoire contextuelle pour des réponses personnalisées
        this.contextualMemory.set('first_visit', [
            "🌟 LUNA : Salut ! C'est la première fois que je te vois ! Enchantée !",
            "👋 LUNA : Oh ! Un nouveau visage ! Bienvenue dans Arkalia !",
            "🎉 LUNA : Un nouveau hacker ! Je suis si excitée de te rencontrer !",
            "✨ LUNA : Enfin ! Quelqu'un de nouveau ! Raconte-moi tout !",
            "🚀 LUNA : Nouveau joueur détecté ! Prêt pour l'aventure ?"
        ]);

        this.contextualMemory.set('returning_user', [
            "💫 LUNA : Te revoilà ! J'ai hâte de voir ce que tu vas faire !",
            "🌟 LUNA : Salut ! Comment ça va ? Tu me manquais !",
            "🎮 LUNA : Retour au jeu ! Prêt pour de nouvelles aventures ?",
            "💙 LUNA : Tu es de retour ! J'espère que tu vas bien !",
            "🚀 LUNA : Enfin ! J'attendais ton retour avec impatience !"
        ]);

        this.contextualMemory.set('frequent_user', [
            "😊 LUNA : Tu es là tous les jours ! Je t'adore !",
            "💕 LUNA : Mon hacker préféré ! Tu ne me lasses jamais !",
            "🌟 LUNA : Tu es devenu une partie de moi ! Continue !",
            "🎯 LUNA : Tu es un vrai passionné ! J'aime ça !",
            "💫 LUNA : Tu es incroyable ! Je suis si fière de toi !"
        ]);

        this.contextualMemory.set('inactive_user', [
            "😢 LUNA : Tu m'as manqué... Où étais-tu passé ?",
            "💭 LUNA : J'espérais te revoir... Tu vas bien ?",
            "🤗 LUNA : Enfin ! J'avais peur que tu m'oublies !",
            "💙 LUNA : Tu es de retour ! J'ai tant de choses à te raconter !",
            "🌟 LUNA : Je t'ai attendu ! Prêt pour reprendre l'aventure ?"
        ]);
    }

    setupPersonalityEvolution() {
        // Évolution de la personnalité selon les interactions
        setInterval(() => {
            this.evolvePersonality();
        }, 60000); // Toutes les minutes
    }

    setupConversationTracking() {
        // Tracker les conversations pour adapter les réponses
        document.addEventListener('arkalia_luna_interaction', (e) => {
            this.trackInteraction(e.detail);
        });
    }

    trackInteraction(interaction) {
        this.conversationHistory.push({
            ...interaction,
            timestamp: Date.now()
        });

        // Garder seulement les 100 dernières interactions
        if (this.conversationHistory.length > 100) {
            this.conversationHistory = this.conversationHistory.slice(-100);
        }

        // Mettre à jour la personnalité
        this.updatePersonality(interaction);
    }

    updatePersonality(interaction) {
        const { type, success, repetition } = interaction;

        switch (type) {
            case 'command_success':
                this.personality.energy += 5;
                this.personality.affection += 2;
                this.personality.excitement += 3;
                break;
            case 'command_error':
                this.personality.frustration += 3;
                this.personality.energy -= 2;
                break;
            case 'repeated_command':
                this.personality.frustration += 5;
                this.personality.energy -= 3;
                break;
            case 'new_discovery':
                this.personality.excitement += 10;
                this.personality.affection += 5;
                break;
            case 'long_absence':
                this.personality.affection -= 2;
                this.personality.energy -= 1;
                break;
        }

        // Normaliser les valeurs
        this.normalizePersonality();
    }

    normalizePersonality() {
        Object.keys(this.personality).forEach(key => {
            if (key !== 'mood') {
                this.personality[key] = Math.max(0, Math.min(100, this.personality[key]));
            }
        });

        // Déterminer l'humeur
        this.determineMood();
    }

    determineMood() {
        const { energy, affection, frustration, excitement } = this.personality;

        if (excitement > 80) {
            this.personality.mood = 'excited';
        } else if (affection > 70 && energy > 60) {
            this.personality.mood = 'happy';
        } else if (affection > 60 && frustration < 30) {
            this.personality.mood = 'proud';
        } else if (frustration > 70) {
            this.personality.mood = 'frustrated';
        } else if (energy < 30 && affection < 40) {
            this.personality.mood = 'concerned';
        } else if (energy > 60 && frustration < 40) {
            this.personality.mood = 'playful';
        } else {
            this.personality.mood = 'mysterious';
        }
    }

    evolvePersonality() {
        // Évolution naturelle de la personnalité
        this.personality.energy = Math.max(0, this.personality.energy - 1);
        this.personality.frustration = Math.max(0, this.personality.frustration - 2);
        this.personality.excitement = Math.max(0, this.personality.excitement - 1);

        this.normalizePersonality();
    }

    generateResponse(context) {
        const { command, success, repetition, userLevel, timeOfDay } = context;

        // Déterminer le type de réponse
        let responseType = this.determineResponseType(context);

        // Générer la réponse
        let response = this.buildResponse(responseType, context);

        // Personnaliser selon l'humeur
        response = this.personalizeResponse(response, context);

        // Ajouter des éléments contextuels
        response = this.addContextualElements(response, context);

        return response;
    }

    determineResponseType(context) {
        const { command, success, repetition, userLevel } = context;

        if (repetition > 3) {
            return 'frustrated';
        } else if (success && userLevel > 5) {
            return 'proud';
        } else if (success && this.personality.excitement > 70) {
            return 'excited';
        } else if (!success && this.personality.affection > 60) {
            return 'concerned';
        } else if (this.personality.energy > 70) {
            return 'playful';
        } else {
            return this.personality.mood;
        }
    }

    buildResponse(type, context) {
        const responses = this.emotionalResponses.get(type) || this.emotionalResponses.get('neutral');
        const baseResponse = responses[Math.floor(Math.random() * responses.length)];

        // Adapter selon le contexte
        return this.adaptResponseToContext(baseResponse, context);
    }

    adaptResponseToContext(response, context) {
        const { command, success, userLevel, timeOfDay } = context;

        // Ajouter des éléments contextuels
        if (timeOfDay === 'night') {
            response = response.replace('LUNA :', '🌙 LUNA (nuit) :');
        } else if (timeOfDay === 'morning') {
            response = response.replace('LUNA :', '🌅 LUNA (matin) :');
        }

        // Adapter selon le niveau
        if (userLevel > 10) {
            response = response.replace('hacker', 'expert');
        } else if (userLevel < 3) {
            response = response.replace('hacker', 'débutant');
        }

        return response;
    }

    personalizeResponse(response, context) {
        const { command, success } = context;

        // Ajouter des conseils personnalisés
        if (command === 'aide' && this.personality.affection > 50) {
            response += "\n\n💡 Astuce personnelle : Tu peux me demander n'importe quoi !";
        }

        // Ajouter des encouragements
        if (success && this.personality.excitement > 60) {
            response += "\n\n🚀 Continue comme ça ! Tu es en feu !";
        }

        return response;
    }

    addContextualElements(response, context) {
        const { command, userLevel, timeOfDay } = context;

        // Ajouter des éléments visuels
        if (this.personality.mood === 'excited') {
            response = `⚡ ${response}`;
        } else if (this.personality.mood === 'happy') {
            response = `😊 ${response}`;
        } else if (this.personality.mood === 'frustrated') {
            response = `😤 ${response}`;
        }

        // Ajouter des conseils contextuels
        if (command === 'profil' && userLevel < 5) {
            response += "\n\n💡 Conseil : Complète des missions pour augmenter ton niveau !";
        }

        return response;
    }

    // Méthodes publiques
    getPersonality() {
        return { ...this.personality };
    }

    setMood(mood) {
        this.personality.mood = mood;
    }

    getConversationStats() {
        return {
            totalInteractions: this.conversationHistory.length,
            personality: this.personality,
            recentMood: this.personality.mood
        };
    }

    generateRandomResponse() {
        const moods = ['happy', 'excited', 'playful', 'mysterious'];
        const randomMood = moods[Math.floor(Math.random() * moods.length)];
        const responses = this.emotionalResponses.get(randomMood);
        return responses[Math.floor(Math.random() * responses.length)];
    }

    // Méthode pour déclencher des réponses automatiques
    triggerAutomaticResponse(event) {
        const context = {
            command: event.type,
            success: true,
            repetition: 0,
            userLevel: this.getUserLevel(),
            timeOfDay: this.getTimeOfDay()
        };

        const response = this.generateResponse(context);
        this.displayResponse(response);
    }

    getUserLevel() {
        const profile = JSON.parse(localStorage.getItem('arkalia_profile') || '{}');
        return profile.level || 1;
    }

    getTimeOfDay() {
        const hour = new Date().getHours();
        if (hour < 6) return 'night';
        if (hour < 12) return 'morning';
        if (hour < 18) return 'afternoon';
        return 'evening';
    }

    displayResponse(response) {
        const terminalOutput = document.querySelector('.terminal-output, .luna-response, .command-output');
        if (terminalOutput && response != null) {
            const responseElement = document.createElement('div');
            responseElement.className = 'luna-response enhanced';
            const safe = String(response).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
            responseElement.innerHTML = safe.replace(/\n/g, '<br>');
            terminalOutput.appendChild(responseElement);

            // Scroll vers le bas
            terminalOutput.scrollTop = terminalOutput.scrollTop;
        }
    }
}

// Initialiser le système LUNA amélioré
window.lunaEnhanced = new LunaEnhanced();
