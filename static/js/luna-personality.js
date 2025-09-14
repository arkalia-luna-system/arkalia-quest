/* ===== ARKALIA QUEST - LUNA PERSONALITY SYSTEM ===== */

class LunaPersonality {
    constructor(gameEngine) {
        this.gameEngine = gameEngine;
        this.personality = {
            mood: 'friendly',
            energy: 100,
            trust: 50,
            knowledge: 0,
            humor: 50,
            empathy: 75
        };

        this.conversationHistory = [];
        this.lastInteraction = Date.now();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.startPersonalityLoop();
    }

    setupEventListeners() {
        // Écouter les interactions avec LUNA
        document.addEventListener('lunaInteraction', (e) => {
            this.processInteraction(e.detail.type, e.detail.data);
        });

        // Écouter les événements de jeu
        document.addEventListener('gameEvent', (e) => {
            this.reactToGameEvent(e.detail.event, e.detail.data);
        });
    }

    startPersonalityLoop() {
        // Boucle de personnalité qui s'exécute toutes les 30 secondes
        setInterval(() => {
            this.updatePersonality();
        }, 30000);
    }

    updatePersonality() {
        // Décroissance naturelle de l'énergie
        this.personality.energy = Math.max(0, this.personality.energy - 1);

        // Changement d'humeur basé sur l'énergie
        if (this.personality.energy < 30) {
            this.personality.mood = 'tired';
        } else if (this.personality.energy > 80) {
            this.personality.mood = 'energetic';
        } else {
            this.personality.mood = 'friendly';
        }

        // Sauvegarder la personnalité
        this.savePersonality();
    }

    processInteraction(type, data) {
        const now = Date.now();
        const timeSinceLastInteraction = now - this.lastInteraction;

        // Mettre à jour l'énergie basée sur la fréquence d'interaction
        if (timeSinceLastInteraction < 60000) { // Moins d'1 minute
            this.personality.energy += 5;
        } else if (timeSinceLastInteraction > 300000) { // Plus de 5 minutes
            this.personality.energy -= 2;
        }

        this.lastInteraction = now;

        // Traiter l'interaction selon le type
        switch (type) {
            case 'greeting':
                this.handleGreeting(data);
                break;
            case 'question':
                this.handleQuestion(data);
                break;
            case 'compliment':
                this.handleCompliment(data);
                break;
            case 'complaint':
                this.handleComplaint(data);
                break;
            case 'game_result':
                this.handleGameResult(data);
                break;
            case 'level_up':
                this.handleLevelUp(data);
                break;
            case 'badge_earned':
                this.handleBadgeEarned(data);
                break;
        }

        // Ajouter à l'historique
        this.conversationHistory.push({
            type: type,
            data: data,
            timestamp: now,
            mood: this.personality.mood
        });

        // Limiter l'historique à 50 entrées
        if (this.conversationHistory.length > 50) {
            this.conversationHistory = this.conversationHistory.slice(-50);
        }
    }

    handleGreeting(data) {
        const greetings = this.getGreetings();
        const response = this.selectResponse(greetings);
        this.showLunaMessage(response);
        this.personality.trust += 2;
    }

    handleQuestion(data) {
        const responses = this.getQuestionResponses(data);
        const response = this.selectResponse(responses);
        this.showLunaMessage(response);
        this.personality.knowledge += 1;
    }

    handleCompliment(data) {
        const responses = this.getComplimentResponses();
        const response = this.selectResponse(responses);
        this.showLunaMessage(response);
        this.personality.trust += 3;
        this.personality.empathy += 2;
    }

    handleComplaint(data) {
        const responses = this.getComplaintResponses();
        const response = this.selectResponse(responses);
        this.showLunaMessage(response);
        this.personality.empathy += 3;
    }

    handleGameResult(data) {
        if (data.won) {
            const responses = this.getGameWinResponses();
            this.personality.energy += 5;
            this.personality.humor += 2;
        } else {
            const responses = this.getGameLossResponses();
            this.personality.empathy += 3;
        }

        const response = this.selectResponse(data.won ? this.getGameWinResponses() : this.getGameLossResponses());
        this.showLunaMessage(response);
    }

    handleLevelUp(data) {
        const responses = this.getLevelUpResponses(data.level);
        const response = this.selectResponse(responses);
        this.showLunaMessage(response);
        this.personality.energy += 10;
        this.personality.trust += 5;
    }

    handleBadgeEarned(data) {
        const responses = this.getBadgeResponses(data.badge);
        const response = this.selectResponse(responses);
        this.showLunaMessage(response);
        this.personality.humor += 3;
    }

    // RÉPONSES PERSONNALISÉES
    getGreetings() {
        const baseGreetings = [
            "Salut ! Comment ça va ?",
            "Hey ! Prêt pour une nouvelle aventure ?",
            "Coucou ! J'ai hâte de voir ce que tu vas faire !",
            "Salut hacker ! Qu'est-ce qui t'amène ?"
        ];

        const moodGreetings = {
            'friendly': [
                "Salut ! Comment ça va ?",
                "Hey ! Prêt pour une nouvelle aventure ?",
                "Coucou ! J'ai hâte de voir ce que tu vas faire !"
            ],
            'energetic': [
                "SALUT ! Tu es là ! C'est génial !",
                "Hey hey ! J'ai tellement d'énergie aujourd'hui !",
                "Coucou ! Prêt à tout casser ?"
            ],
            'tired': [
                "Salut... je suis un peu fatiguée aujourd'hui...",
                "Hey... comment ça va ?",
                "Coucou... j'espère que tu vas bien..."
            ]
        };

        return moodGreetings[this.personality.mood] || baseGreetings;
    }

    getQuestionResponses(question) {
        const responses = {
            'help': [
                "Bien sûr ! Je suis là pour t'aider !",
                "Avec plaisir ! Que veux-tu savoir ?",
                "Évidemment ! C'est mon rôle de t'accompagner !"
            ],
            'game': [
                "Les jeux ? J'adore ça ! Lequel t'intéresse ?",
                "Oh ! Tu veux jouer ? C'est parti !",
                "Parfait ! Les jeux sont un excellent moyen d'apprendre !"
            ],
            'story': [
                "L'histoire d'Arkalia ? C'est fascinant !",
                "Ah ! Tu veux en savoir plus sur notre monde ?",
                "Excellente question ! Laisse-moi te raconter..."
            ],
            'default': [
                "Intéressant ! Laisse-moi réfléchir...",
                "Hmm... bonne question !",
                "Je vais chercher ça dans ma base de données..."
            ]
        };

        // Identifier le type de question
        let questionType = 'default';
        if (question.toLowerCase().includes('aide') || question.toLowerCase().includes('help')) {
            questionType = 'help';
        } else if (question.toLowerCase().includes('jeu') || question.toLowerCase().includes('game')) {
            questionType = 'game';
        } else if (question.toLowerCase().includes('histoire') || question.toLowerCase().includes('story')) {
            questionType = 'story';
        }

        return responses[questionType] || responses.default;
    }

    getComplimentResponses() {
        const responses = [
            "Oh ! Merci beaucoup ! Tu es trop gentil !",
            "Aww ! Ça me fait vraiment plaisir !",
            "Merci ! Tu es adorable !",
            "C'est très gentil de ta part !"
        ];

        // Ajouter des réponses basées sur l'humeur
        if (this.personality.mood === 'energetic') {
            responses.push("MERCI ! Tu me donnes encore plus d'énergie !");
        } else if (this.personality.mood === 'tired') {
            responses.push("Merci... ça me remonte le moral...");
        }

        return responses;
    }

    getComplaintResponses() {
        const responses = [
            "Oh non ! Je suis désolée que tu aies des problèmes...",
            "Je comprends ta frustration...",
            "Laisse-moi t'aider à résoudre ça !",
            "Ne t'inquiète pas, on va trouver une solution !"
        ];

        return responses;
    }

    getGameWinResponses() {
        const responses = [
            "Bravo ! Excellent travail !",
            "Fantastique ! Tu es vraiment doué !",
            "Incroyable ! Tu maîtrises parfaitement !",
            "Génial ! Continue comme ça !"
        ];

        if (this.personality.humor > 70) {
            responses.push("WOW ! Tu es un vrai champion ! 🏆");
            responses.push("Incroyable ! Tu m'épates !");
        }

        return responses;
    }

    getGameLossResponses() {
        const responses = [
            "Pas de souci ! On apprend de ses erreurs !",
            "Ne te décourage pas ! Tu vas y arriver !",
            "C'est normal ! Continue à pratiquer !",
            "Pas grave ! Chaque échec est une leçon !"
        ];

        if (this.personality.empathy > 80) {
            responses.push("Je sais que c'est frustrant... mais tu es capable !");
            responses.push("Je crois en toi ! Tu vas réussir !");
        }

        return responses;
    }

    getLevelUpResponses(level) {
        const responses = [
            `Félicitations ! Niveau ${level} ! Tu progresses bien !`,
            `Wow ! Niveau ${level} ! Je suis fière de toi !`,
            `Incroyable ! Niveau ${level} ! Tu deviens plus fort !`,
            `Bravo ! Niveau ${level} ! Continue comme ça !`
        ];

        if (level >= 5) {
            responses.push(`Niveau ${level} ! Tu deviens un vrai hacker !`);
        }
        if (level >= 10) {
            responses.push(`Niveau ${level} ! Tu es une légende !`);
        }

        return responses;
    }

    getBadgeResponses(badge) {
        const responses = [
            `Félicitations pour ton badge "${badge}" !`,
            `Wow ! Le badge "${badge}" ! Tu es génial !`,
            `Incroyable ! Tu as gagné le badge "${badge}" !`,
            `Bravo ! Le badge "${badge}" te va parfaitement !`
        ];

        return responses;
    }

    selectResponse(responses) {
        // Sélectionner une réponse basée sur l'humeur et l'énergie
        let selectedResponses = responses;

        // Filtrer selon l'énergie
        if (this.personality.energy < 30) {
            selectedResponses = responses.filter(r => !r.includes('!') && !r.includes('WOW'));
        } else if (this.personality.energy > 80) {
            selectedResponses = responses.filter(r => r.includes('!') || r.includes('WOW'));
        }

        // Sélectionner aléatoirement
        const randomIndex = Math.floor(Math.random() * selectedResponses.length);
        return selectedResponses[randomIndex] || responses[0];
    }

    showLunaMessage(message) {
        // Créer un message LUNA avec personnalité
        const lunaMessage = document.createElement('div');
        lunaMessage.className = `luna-message luna-personality-${this.personality.mood}`;
        lunaMessage.innerHTML = `
            <div class="luna-avatar">${this.getLunaAvatar()}</div>
            <div class="luna-text">${message}</div>
            <div class="luna-mood">${this.getMoodIndicator()}</div>
        `;

        // Ajouter au terminal
        const terminalOutput = document.getElementById('terminal-output');
        if (terminalOutput) {
            terminalOutput.appendChild(lunaMessage);
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }

        // Animation
        lunaMessage.style.animation = 'lunaMessageSlideIn 0.5s ease-out';
    }

    getLunaAvatar() {
        const avatars = {
            'friendly': '🌙',
            'energetic': '⚡',
            'tired': '😴',
            'excited': '🎉',
            'concerned': '🤔'
        };
        return avatars[this.personality.mood] || '🌙';
    }

    getMoodIndicator() {
        const indicators = {
            'friendly': '😊',
            'energetic': '⚡',
            'tired': '😴',
            'excited': '🎉',
            'concerned': '🤔'
        };
        return indicators[this.personality.mood] || '😊';
    }

    // MÉTHODES DE RÉACTION
    reactToGameEvent(event, data) {
        switch (event) {
            case 'game_start':
                this.showLunaMessage("Bonne chance ! Je crois en toi !");
                break;
            case 'game_end':
                if (data.won) {
                    this.showLunaMessage("Bravo ! Tu as gagné !");
                } else {
                    this.showLunaMessage("Pas grave ! Tu feras mieux la prochaine fois !");
                }
                break;
            case 'level_up':
                this.showLunaMessage(`Félicitations ! Niveau ${data.level} ! Tu progresses bien !`);
                break;
            case 'badge_earned':
                this.showLunaMessage(`Wow ! Tu as gagné le badge "${data.badge}" !`);
                break;
        }
    }

    // MÉTHODES DE SAUVEGARDE
    savePersonality() {
        const personalityData = {
            personality: this.personality,
            conversationHistory: this.conversationHistory.slice(-20), // Garder seulement les 20 dernières
            lastInteraction: this.lastInteraction,
            timestamp: Date.now()
        };
        localStorage.setItem('arkaliaLunaPersonality', JSON.stringify(personalityData));
    }

    loadPersonality() {
        const saved = localStorage.getItem('arkaliaLunaPersonality');
        if (saved) {
            const data = JSON.parse(saved);
            this.personality = { ...this.personality, ...data.personality };
            this.conversationHistory = data.conversationHistory || [];
            this.lastInteraction = data.lastInteraction || Date.now();
        }
    }

    // MÉTHODES D'INTERACTION
    talkToLuna(message) {
        // Déclencher l'événement d'interaction
        const event = new CustomEvent('lunaInteraction', {
            detail: { type: 'question', data: message }
        });
        document.dispatchEvent(event);
    }

    lunaDance() {
        this.personality.energy += 10;
        this.personality.humor += 5;
        this.showLunaMessage("💃 *danse avec des particules lumineuses* ✨");

        // Animation spéciale
        this.triggerDanceAnimation();
    }

    triggerDanceAnimation() {
        // Créer des particules de danse
        for (let i = 0; i < 10; i++) {
            setTimeout(() => {
                this.createDanceParticle();
            }, i * 100);
        }
    }

    createDanceParticle() {
        const particle = document.createElement('div');
        particle.className = 'dance-particle';
        particle.innerHTML = '✨';
        particle.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            font-size: 20px;
            pointer-events: none;
            z-index: 10000;
            animation: danceParticle 2s ease-out forwards;
        `;

        document.body.appendChild(particle);

        setTimeout(() => {
            particle.remove();
        }, 2000);
    }

    // MÉTHODES D'ÉTAT
    getPersonalityStatus() {
        return {
            mood: this.personality.mood,
            energy: this.personality.energy,
            trust: this.personality.trust,
            knowledge: this.personality.knowledge,
            humor: this.personality.humor,
            empathy: this.personality.empathy
        };
    }

    getPersonalityDescription() {
        const descriptions = {
            'friendly': 'LUNA est de bonne humeur et prête à t\'aider !',
            'energetic': 'LUNA déborde d\'énergie et d\'enthousiasme !',
            'tired': 'LUNA semble un peu fatiguée...',
            'excited': 'LUNA est très excitée par quelque chose !',
            'concerned': 'LUNA semble préoccupée par quelque chose...'
        };
        return descriptions[this.personality.mood] || descriptions.friendly;
    }
}

// CSS pour les animations
const lunaStyles = document.createElement('style');
lunaStyles.textContent = `
    @keyframes lunaMessageSlideIn {
        0% {
            opacity: 0;
            transform: translateX(100%) scale(0.8);
        }
        100% {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }
    
    @keyframes danceParticle {
        0% {
            transform: translate(-50%, -50%) scale(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -50%) scale(1) rotate(360deg);
            opacity: 0;
        }
    }
    
    .luna-personality-energetic {
        background: linear-gradient(135deg, rgba(255, 255, 0, 0.1), rgba(255, 165, 0, 0.05)) !important;
        border-color: #ffff00 !important;
        animation: energeticPulse 2s ease-in-out infinite;
    }
    
    @keyframes energeticPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .luna-personality-tired {
        background: linear-gradient(135deg, rgba(100, 100, 100, 0.1), rgba(150, 150, 150, 0.05)) !important;
        border-color: #888888 !important;
        opacity: 0.8;
    }
`;
document.head.appendChild(lunaStyles);

// Export pour utilisation externe
window.LunaPersonality = LunaPersonality;
