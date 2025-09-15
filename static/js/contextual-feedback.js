/**
 * Système de Feedback Contextuel Intelligent
 * Adapte les réponses LUNA selon le profil et le contexte du joueur
 */

class ContextualFeedbackSystem {
    constructor() {
        this.playerProfile = this.detectPlayerProfile();
        this.interactionHistory = this.loadInteractionHistory();
        this.feedbackTemplates = this.initializeFeedbackTemplates();
        this.lastInteractionTime = Date.now();
        this.repetitionCount = {};
        this.successStreak = 0;
        this.errorStreak = 0;
        this.idleTime = 0;

        this.initializeSystem();
    }

    detectPlayerProfile() {
        // Détection basée sur les interactions et préférences
        const interactions = this.loadInteractionHistory();
        const timeSpent = this.calculateTimeSpent();
        const commandPatterns = this.analyzeCommandPatterns();

        if (commandPatterns.includes('aide') && timeSpent < 300000) {
            return 'debutant';
        } else if (commandPatterns.includes('profil') && commandPatterns.includes('badges')) {
            return 'competitif';
        } else if (commandPatterns.includes('accessibility') && commandPatterns.includes('theme')) {
            return 'creatif';
        } else if (timeSpent > 1800000 && commandPatterns.length < 5) {
            return 'casual';
        } else {
            return 'experimente';
        }
    }

    initializeFeedbackTemplates() {
        return {
            debutant: {
                encouragement: [
                    "🌟 Excellent ! Tu apprends vite !",
                    "🎯 Parfait ! Tu maîtrises de mieux en mieux !",
                    "🚀 Bravo ! Tu progresses à chaque étape !",
                    "💫 Super ! Tu deviens un vrai hacker !",
                    "🎮 Génial ! Tu comprends le système !"
                ],
                error: [
                    "🤔 Pas de souci ! Essaie 'aide' pour voir les commandes disponibles",
                    "💡 Astuce : tape 'aide' pour découvrir toutes les possibilités",
                    "🎯 Pas grave ! Chaque erreur t'apprend quelque chose",
                    "🌟 Continue ! Même les meilleurs font des erreurs au début",
                    "💫 Tu y arriveras ! Regarde les suggestions ci-dessous"
                ],
                progression: [
                    "🎉 Félicitations ! Tu as débloqué un nouveau niveau !",
                    "🏆 Bravo ! Tu progresses dans ton aventure !",
                    "⭐ Excellent ! Tu deviens plus fort !",
                    "🎯 Parfait ! Tu maîtrises de nouvelles compétences !",
                    "🚀 Incroyable ! Tu avances à grands pas !"
                ],
                idle: [
                    "👋 Salut ! Prêt pour une nouvelle aventure ?",
                    "🌟 Bienvenue ! Tu veux continuer ton exploration ?",
                    "🎮 Hello ! On reprend où on s'était arrêté ?",
                    "💫 Salut ! Tu veux découvrir de nouvelles choses ?",
                    "🎯 Bonjour ! Prêt pour de nouveaux défis ?"
                ]
            },
            experimente: {
                encouragement: [
                    "⚡ Rapide et efficace ! Tu maîtrises parfaitement !",
                    "🎯 Précision parfaite ! Tu es un expert !",
                    "🚀 Excellente optimisation ! Tu connais tes commandes !",
                    "💫 Parfait ! Tu utilises le système comme un pro !",
                    "🌟 Impressionnant ! Tu es très compétent !"
                ],
                error: [
                    "🔧 Commande inconnue. Tu peux essayer 'aide' pour voir les options",
                    "⚡ Erreur détectée. Vérifie la syntaxe ou consulte 'aide'",
                    "🎯 Commande non reconnue. 'aide' te donnera toutes les possibilités",
                    "💡 Erreur. Tu connais sûrement 'aide' pour les commandes disponibles",
                    "🌟 Commande invalide. 'aide' te montrera tout ce qui est possible"
                ],
                progression: [
                    "🏆 Niveau supérieur atteint ! Tu es un vrai expert !",
                    "⚡ Progression optimale ! Tu maîtrises le système !",
                    "🎯 Excellent ! Tu progresses de manière efficace !",
                    "🚀 Parfait ! Tu es un utilisateur avancé !",
                    "💫 Bravo ! Tu utilises le système comme un pro !"
                ],
                idle: [
                    "⚡ Expert de retour ! Prêt pour de nouveaux défis ?",
                    "🎯 Maître du terminal ! Que veux-tu explorer ?",
                    "🚀 Utilisateur avancé ! Prêt pour l'optimisation ?",
                    "💫 Expert ! Tu veux tester de nouvelles fonctionnalités ?",
                    "🌟 Pro ! Prêt pour des défis techniques ?"
                ]
            },
            competitif: {
                encouragement: [
                    "🏆 CHAMPION ! Tu domines la compétition !",
                    "⚡ VICTOIRE ! Tu es le meilleur !",
                    "🎯 PARFAIT ! Tu écrases la concurrence !",
                    "🚀 GAGNANT ! Tu es imbattable !",
                    "💫 MAÎTRE ! Tu règnes sur le jeu !"
                ],
                error: [
                    "⚔️ Erreur de guerre ! Consulte 'aide' pour les commandes de combat",
                    "🏆 Erreur de champion ! 'aide' te donnera les armes disponibles",
                    "🎯 Erreur de compétition ! 'aide' te montrera tes options de victoire",
                    "🚀 Erreur de leader ! 'aide' te révélera tes pouvoirs",
                    "💫 Erreur de maître ! 'aide' te donnera tes outils de domination"
                ],
                progression: [
                    "👑 COURONNE ! Tu es le roi du jeu !",
                    "🏆 TROPHÉE ! Tu as conquis un nouveau niveau !",
                    "⚡ VICTOIRE ! Tu as écrasé la concurrence !",
                    "🎯 CHAMPION ! Tu as gagné la bataille !",
                    "🚀 MAÎTRE ! Tu as dominé le défi !"
                ],
                idle: [
                    "👑 Roi de retour ! Prêt pour la domination ?",
                    "🏆 Champion ! Tu veux écraser la concurrence ?",
                    "⚡ Maître ! Prêt pour de nouveaux défis de guerre ?",
                    "🎯 Leader ! Tu veux montrer ta supériorité ?",
                    "🚀 Vainqueur ! Prêt pour la victoire totale ?"
                ]
            },
            creatif: {
                encouragement: [
                    "🎨 Créatif ! Tu explores de nouvelles possibilités !",
                    "💫 Artiste ! Tu crées quelque chose d'unique !",
                    "🌟 Inventeur ! Tu découvres des chemins inédits !",
                    "🎯 Visionnaire ! Tu vois au-delà des limites !",
                    "🚀 Innovateur ! Tu repousses les frontières !"
                ],
                error: [
                    "🎨 Erreur créative ! 'aide' te donnera des outils d'expression",
                    "💫 Erreur d'artiste ! 'aide' te révélera tes pinceaux numériques",
                    "🌟 Erreur d'inventeur ! 'aide' te montrera tes instruments",
                    "🎯 Erreur de visionnaire ! 'aide' te donnera tes outils de création",
                    "🚀 Erreur d'innovateur ! 'aide' te révélera tes possibilités"
                ],
                progression: [
                    "🎨 Œuvre d'art ! Tu as créé quelque chose de magnifique !",
                    "💫 Chef-d'œuvre ! Tu as inventé quelque chose d'unique !",
                    "🌟 Innovation ! Tu as repoussé les limites !",
                    "🎯 Création ! Tu as donné vie à quelque chose de nouveau !",
                    "🚀 Révolution ! Tu as changé les règles du jeu !"
                ],
                idle: [
                    "🎨 Artiste de retour ! Prêt pour de nouvelles créations ?",
                    "💫 Créateur ! Tu veux explorer de nouveaux horizons ?",
                    "🌟 Inventeur ! Prêt pour de nouvelles découvertes ?",
                    "🎯 Visionnaire ! Tu veux repousser les limites ?",
                    "🚀 Innovateur ! Prêt pour de nouvelles expérimentations ?"
                ]
            },
            casual: {
                encouragement: [
                    "😊 Doucement mais sûrement ! Tu avances à ton rythme !",
                    "🌟 Parfait ! Tu prends le temps de bien faire !",
                    "🎯 Excellent ! Tu explores tranquillement !",
                    "💫 Super ! Tu profites de chaque moment !",
                    "🚀 Bravo ! Tu avances à ta façon !"
                ],
                error: [
                    "😊 Pas de stress ! 'aide' te guidera gentiment",
                    "🌟 Tranquille ! 'aide' te montrera le chemin",
                    "🎯 Pas de souci ! 'aide' t'aidera à comprendre",
                    "💫 Relax ! 'aide' te donnera les bonnes directions",
                    "🚀 Cool ! 'aide' te fera découvrir les possibilités"
                ],
                progression: [
                    "😊 Douce progression ! Tu avances à ton rythme !",
                    "🌟 Belle avancée ! Tu prends le temps de bien faire !",
                    "🎯 Excellente progression ! Tu explores tranquillement !",
                    "💫 Super avancée ! Tu profites de chaque étape !",
                    "🚀 Bravo ! Tu avances de manière détendue !"
                ],
                idle: [
                    "😊 Salut ! Prêt pour une exploration tranquille ?",
                    "🌟 Bonjour ! Tu veux continuer doucement ?",
                    "🎯 Hello ! Prêt pour une aventure relaxante ?",
                    "💫 Salut ! Tu veux découvrir à ton rythme ?",
                    "🚀 Bonjour ! Prêt pour une exploration cool ?"
                ]
            }
        };
    }

    generateContextualFeedback(action, result, context = {}) {
        const profile = this.playerProfile;
        const templates = this.feedbackTemplates[profile];

        // Analyser le contexte
        const isRepetitive = this.isRepetitiveAction(action);
        const isSuccess = result.success;
        const isError = result.error;
        const isIdle = this.isIdleReturn();

        // Adapter le feedback selon le contexte
        let feedback = '';

        if (isIdle) {
            feedback = this.getRandomTemplate(templates.idle);
        } else if (isSuccess) {
            feedback = this.getRandomTemplate(templates.encouragement);
            this.successStreak++;
            this.errorStreak = 0;
        } else if (isError) {
            feedback = this.getRandomTemplate(templates.error);
            this.errorStreak++;
            this.successStreak = 0;
        } else {
            feedback = this.getRandomTemplate(templates.progression);
        }

        // Ajouter des éléments contextuels
        if (isRepetitive) {
            feedback += this.getRepetitiveContext(profile, action);
        }

        if (this.successStreak > 3) {
            feedback += this.getStreakContext(profile, 'success');
        }

        if (this.errorStreak > 2) {
            feedback += this.getStreakContext(profile, 'error');
        }

        // Enregistrer l'interaction
        this.recordInteraction(action, result, feedback);

        return feedback;
    }

    getRepetitiveContext(profile, action) {
        const contexts = {
            debutant: " Tu répètes cette action, c'est normal d'apprendre !",
            experimente: " Tu répètes cette commande, tu cherches l'optimisation ?",
            competitif: " Tu répètes cette action, tu veux battre un record ?",
            creatif: " Tu répètes cette action, tu explores les possibilités ?",
            casual: " Tu répètes cette action, tu prends ton temps !"
        };
        return contexts[profile] || "";
    }

    getStreakContext(profile, type) {
        if (type === 'success') {
            const contexts = {
                debutant: " 🔥 Tu es en feu ! Continue comme ça !",
                experimente: " ⚡ Série impressionnante ! Tu maîtrises !",
                competitif: " 👑 Tu domines ! Tu es imbattable !",
                creatif: " 🎨 Créativité en série ! Tu es inspiré !",
                casual: " 😊 Belle série ! Tu avances bien !"
            };
            return contexts[profile] || "";
        } else {
            const contexts = {
                debutant: " 💪 Pas de souci ! Tu vas y arriver !",
                experimente: " 🔧 Erreurs en série ? Vérifie la syntaxe !",
                competitif: " ⚔️ Erreurs de guerre ? Consulte 'aide' !",
                creatif: " 🎨 Erreurs créatives ? Explore 'aide' !",
                casual: " 😊 Pas de stress ! 'aide' t'aidera !"
            };
            return contexts[profile] || "";
        }
    }

    getRandomTemplate(templates) {
        return templates[Math.floor(Math.random() * templates.length)];
    }

    isRepetitiveAction(action) {
        this.repetitionCount[action] = (this.repetitionCount[action] || 0) + 1;
        return this.repetitionCount[action] > 2;
    }

    isIdleReturn() {
        const now = Date.now();
        const timeDiff = now - this.lastInteractionTime;
        this.idleTime = timeDiff;
        return timeDiff > 300000; // 5 minutes
    }

    recordInteraction(action, result, feedback) {
        this.lastInteractionTime = Date.now();
        this.interactionHistory.push({
            action,
            result,
            feedback,
            timestamp: new Date().toISOString(),
            profile: this.playerProfile
        });
        this.saveInteractionHistory();
    }

    loadInteractionHistory() {
        try {
            return JSON.parse(localStorage.getItem('arkalia_interaction_history') || '[]');
        } catch {
            return [];
        }
    }

    saveInteractionHistory() {
        try {
            localStorage.setItem('arkalia_interaction_history', JSON.stringify(this.interactionHistory));
        } catch (e) {
            console.warn('Impossible de sauvegarder l\'historique des interactions');
        }
    }

    calculateTimeSpent() {
        const startTime = localStorage.getItem('arkalia_session_start');
        if (startTime) {
            return Date.now() - parseInt(startTime);
        }
        return 0;
    }

    analyzeCommandPatterns() {
        return this.interactionHistory.map(interaction => interaction.action);
    }

    initializeSystem() {
        // Marquer le début de session
        if (!localStorage.getItem('arkalia_session_start')) {
            localStorage.setItem('arkalia_session_start', Date.now().toString());
        }

        // Détecter le retour après absence
        if (this.isIdleReturn()) {
            this.showWelcomeBackMessage();
        }
    }

    showWelcomeBackMessage() {
        const profile = this.playerProfile;
        const welcomeMessages = {
            debutant: "🌟 Salut ! Tu reviens pour continuer ton apprentissage ?",
            experimente: "⚡ Expert de retour ! Prêt pour de nouveaux défis ?",
            competitif: "👑 Champion ! Tu reviens pour dominer ?",
            creatif: "🎨 Artiste ! Tu reviens pour créer ?",
            casual: "😊 Salut ! Tu reviens pour explorer tranquillement ?"
        };

        const message = welcomeMessages[profile] || "🌟 Salut ! Tu reviens pour continuer l'aventure ?";

        // Afficher le message de bienvenue
        this.displayFeedbackMessage(message, 'welcome');
    }

    displayFeedbackMessage(message, type = 'info') {
        // Créer un élément de feedback visuel
        const feedbackElement = document.createElement('div');
        feedbackElement.className = `contextual-feedback ${type}`;
        feedbackElement.textContent = message;

        // Styles selon le type
        const styles = {
            welcome: 'background: linear-gradient(45deg, #00ff00, #0080ff); color: white; padding: 15px; border-radius: 10px; margin: 10px; font-weight: bold;',
            info: 'background: #333; color: #00ff00; padding: 10px; border-radius: 5px; margin: 5px;',
            success: 'background: #00ff00; color: #000; padding: 10px; border-radius: 5px; margin: 5px; font-weight: bold;',
            error: 'background: #ff0000; color: white; padding: 10px; border-radius: 5px; margin: 5px;'
        };

        feedbackElement.style.cssText = styles[type] || styles.info;

        // Ajouter à la page
        const container = document.querySelector('.terminal-output') || document.body;
        container.appendChild(feedbackElement);

        // Supprimer après 5 secondes
        setTimeout(() => {
            if (feedbackElement.parentNode) {
                feedbackElement.parentNode.removeChild(feedbackElement);
            }
        }, 5000);
    }

    // Méthode publique pour générer des feedbacks
    getFeedback(action, result, context = {}) {
        return this.generateContextualFeedback(action, result, context);
    }

    // Méthode pour détecter les easter eggs
    detectEasterEgg(input) {
        const easterEggs = {
            'konami': () => this.triggerKonamiCode(),
            'matrix': () => this.triggerMatrixRain(),
            'luna dance': () => this.triggerLunaDance(),
            'hack the planet': () => this.triggerHackThePlanet(),
            'luna love': () => this.triggerLunaLove()
        };

        const inputLower = input.toLowerCase();
        for (const [trigger, action] of Object.entries(easterEggs)) {
            if (inputLower.includes(trigger)) {
                action();
                return true;
            }
        }
        return false;
    }

    triggerKonamiCode() {
        this.displayFeedbackMessage("🎮 Code Konami activé ! LUNA devient plus puissante !", 'success');
        // Ajouter des effets visuels
        document.body.style.animation = 'konami-glow 2s ease-in-out';
    }

    triggerMatrixRain() {
        this.displayFeedbackMessage("🌧️ Pluie Matrix activée ! Tu es dans la matrice !", 'success');
        // Ajouter l'effet Matrix Rain
        this.createMatrixRain();
    }

    triggerLunaDance() {
        this.displayFeedbackMessage("💃 LUNA danse ! Elle est contente de te voir !", 'success');
        // Animer LUNA
        this.animateLuna();
    }

    triggerHackThePlanet() {
        this.displayFeedbackMessage("🌍 HACK THE PLANET ! Tu es un vrai hacker !", 'success');
        // Effets de hacking
        this.createHackingEffects();
    }

    triggerLunaLove() {
        this.displayFeedbackMessage("💖 LUNA t'aime ! Tu es son joueur préféré !", 'success');
        // Effets d'amour
        this.createLoveEffects();
    }

    createMatrixRain() {
        // Implémentation de l'effet Matrix Rain
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);

        // Animation Matrix Rain
        setTimeout(() => {
            document.body.removeChild(canvas);
        }, 10000);
    }

    animateLuna() {
        const lunaElement = document.querySelector('.luna-avatar');
        if (lunaElement) {
            lunaElement.style.animation = 'luna-dance 2s ease-in-out';
        }
    }

    createHackingEffects() {
        // Effets visuels de hacking
        document.body.style.filter = 'hue-rotate(90deg)';
        setTimeout(() => {
            document.body.style.filter = 'none';
        }, 3000);
    }

    createLoveEffects() {
        // Effets d'amour
        const hearts = ['💖', '💕', '💗', '💝', '💘'];
        for (let i = 0; i < 10; i++) {
            setTimeout(() => {
                const heart = document.createElement('div');
                heart.textContent = hearts[Math.floor(Math.random() * hearts.length)];
                heart.style.position = 'fixed';
                heart.style.left = Math.random() * window.innerWidth + 'px';
                heart.style.top = Math.random() * window.innerHeight + 'px';
                heart.style.fontSize = '2rem';
                heart.style.pointerEvents = 'none';
                heart.style.zIndex = '9999';
                document.body.appendChild(heart);

                setTimeout(() => {
                    if (heart.parentNode) {
                        heart.parentNode.removeChild(heart);
                    }
                }, 2000);
            }, i * 200);
        }
    }
}

// Initialiser le système de feedback contextuel
const contextualFeedback = new ContextualFeedbackSystem();

// Exporter pour utilisation globale
window.ContextualFeedbackSystem = ContextualFeedbackSystem;
window.contextualFeedback = contextualFeedback;
