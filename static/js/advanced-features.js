/**
 * 🚀 FONCTIONNALITÉS AVANCÉES - ARKALIA QUEST
 * ===========================================
 * 
 * Intégration des nouvelles fonctionnalités :
 * - Interactions sociales et communautaires
 * - Customisation avancée
 * - Storytelling adaptatif
 * - Micro-interactions
 */

class AdvancedFeaturesManager {
    constructor() {
        this.socialEngine = new SocialEngine();
        this.customizationEngine = new CustomizationEngine();
        this.storytellingEngine = new StorytellingEngine();
        this.microInteractions = new MicroInteractionsEngine();

        this.playerId = this.getPlayerId();
        this.isInitialized = false;

        this.init();
    }

    init() {
        this.loadPlayerData();
        this.setupEventListeners();
        this.initializeFeatures();
        this.isInitialized = true;

        console.log('🚀 Fonctionnalités avancées initialisées');
    }

    getPlayerId() {
        // Récupérer l'ID du joueur depuis localStorage ou générer un nouveau
        let playerId = localStorage.getItem('arkalia_player_id');
        if (!playerId) {
            playerId = 'player_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('arkalia_player_id', playerId);
        }
        return playerId;
    }

    async loadPlayerData() {
        try {
            // Charger les données du joueur
            const [socialData, customizationData, storyData, interactionData] = await Promise.all([
                this.socialEngine.getDashboard(this.playerId),
                this.customizationEngine.getPlayerCustomization(this.playerId),
                this.storytellingEngine.getStoryProgress(this.playerId),
                this.microInteractions.getPreferences(this.playerId)
            ]);

            this.playerData = {
                social: socialData,
                customization: customizationData,
                story: storyData,
                interactions: interactionData
            };

            // Appliquer la customisation
            this.applyCustomization(customizationData);

        } catch (error) {
            console.error('❌ Erreur chargement données joueur:', error);
        }
    }

    setupEventListeners() {
        // Écouter les événements de micro-interactions
        document.addEventListener('click', (e) => {
            this.handleMicroInteraction('button_click', e.target);
        });

        document.addEventListener('success', (e) => {
            this.handleMicroInteraction('success_action', e.target);
        });

        document.addEventListener('error', (e) => {
            this.handleMicroInteraction('error_action', e.target);
        });

        // Écouter les événements de progression
        document.addEventListener('level_up', (e) => {
            this.handleMicroInteraction('level_up', e.target);
        });

        document.addEventListener('badge_earned', (e) => {
            this.handleMicroInteraction('badge_earned', e.target);
        });

        document.addEventListener('mission_complete', (e) => {
            this.handleMicroInteraction('mission_complete', e.target);
        });
    }

    initializeFeatures() {
        // Initialiser les fonctionnalités
        this.socialEngine.init();
        this.customizationEngine.init();
        this.storytellingEngine.init();
        this.microInteractions.init();
    }

    // ===== GESTION DES MICRO-INTERACTIONS =====

    async handleMicroInteraction(type, targetElement) {
        try {
            const result = await this.microInteractions.trigger(type, targetElement, {
                player_id: this.playerId,
                timestamp: new Date().toISOString()
            });

            if (result.success) {
                this.processInteractionResult(result);
            }
        } catch (error) {
            console.error('❌ Erreur micro-interaction:', error);
        }
    }

    processInteractionResult(result) {
        // Traiter les animations
        if (result.animations) {
            result.animations.forEach(animation => {
                this.playAnimation(animation);
            });
        }

        // Traiter les sons
        if (result.sounds) {
            result.sounds.forEach(sound => {
                this.playSound(sound);
            });
        }

        // Traiter les notifications
        if (result.notifications) {
            result.notifications.forEach(notification => {
                this.showNotification(notification);
            });
        }
    }

    playAnimation(animation) {
        const element = animation.target_element ?
            document.querySelector(animation.target_element) :
            document.body;

        if (!element) return;

        // Appliquer l'animation CSS
        element.style.animation = `${animation.animation} ${animation.duration}ms ${animation.easing}`;

        // Nettoyer après l'animation
        setTimeout(() => {
            element.style.animation = '';
        }, animation.duration);
    }

    playSound(sound) {
        if (window.audioManager) {
            window.audioManager.playSound(sound.sound, sound.volume);
        }
    }

    showNotification(notification) {
        // Créer la notification
        const notificationElement = document.createElement('div');
        notificationElement.className = `notification ${notification.type} ${notification.style || ''}`;
        notificationElement.innerHTML = `
            <div class="notification-content">
                ${notification.title ? `<h4>${notification.title}</h4>` : ''}
                <p>${notification.message}</p>
            </div>
        `;

        // Positionner la notification
        notificationElement.style.position = 'fixed';
        notificationElement.style.zIndex = '10000';

        switch (notification.position) {
            case 'top-right':
                notificationElement.style.top = '20px';
                notificationElement.style.right = '20px';
                break;
            case 'top-left':
                notificationElement.style.top = '20px';
                notificationElement.style.left = '20px';
                break;
            case 'bottom-right':
                notificationElement.style.bottom = '20px';
                notificationElement.style.right = '20px';
                break;
            case 'bottom-left':
                notificationElement.style.bottom = '20px';
                notificationElement.style.left = '20px';
                break;
            default:
                notificationElement.style.top = '50%';
                notificationElement.style.left = '50%';
                notificationElement.style.transform = 'translate(-50%, -50%)';
        }

        // Ajouter au DOM
        document.body.appendChild(notificationElement);

        // Animation d'entrée
        notificationElement.style.opacity = '0';
        notificationElement.style.transform = 'translateY(-20px)';

        setTimeout(() => {
            notificationElement.style.transition = 'all 0.3s ease';
            notificationElement.style.opacity = '1';
            notificationElement.style.transform = 'translateY(0)';
        }, 10);

        // Supprimer après la durée
        setTimeout(() => {
            notificationElement.style.opacity = '0';
            notificationElement.style.transform = 'translateY(-20px)';

            setTimeout(() => {
                if (notificationElement.parentNode) {
                    notificationElement.parentNode.removeChild(notificationElement);
                }
            }, 300);
        }, notification.duration);
    }

    // ===== GESTION DE LA CUSTOMISATION =====

    applyCustomization(customizationData) {
        if (!customizationData || !customizationData.current_theme) return;

        const theme = customizationData.current_theme;

        // Appliquer les variables CSS
        if (theme.colors) {
            Object.entries(theme.colors).forEach(([key, value]) => {
                document.documentElement.style.setProperty(`--theme-${key}`, value);
            });
        }

        // Appliquer les polices
        if (theme.fonts) {
            Object.entries(theme.fonts).forEach(([key, value]) => {
                document.documentElement.style.setProperty(`--theme-font-${key}`, value);
            });
        }

        // Appliquer les effets
        if (theme.effects) {
            Object.entries(theme.effects).forEach(([key, value]) => {
                document.body.classList.toggle(`effect-${key}`, value);
            });
        }
    }

    async changeTheme(themeId) {
        try {
            const result = await this.customizationEngine.setTheme(this.playerId, themeId);

            if (result.success) {
                // Recharger la customisation
                await this.loadPlayerData();

                // Déclencher une micro-interaction
                this.handleMicroInteraction('success_action', document.body);

                return result;
            }
        } catch (error) {
            console.error('❌ Erreur changement thème:', error);
        }
    }

    async changeAvatar(avatarId) {
        try {
            const result = await this.customizationEngine.setAvatar(this.playerId, avatarId);

            if (result.success) {
                // Mettre à jour l'avatar dans l'interface
                this.updateAvatarDisplay(avatarId);

                // Déclencher une micro-interaction
                this.handleMicroInteraction('success_action', document.body);

                return result;
            }
        } catch (error) {
            console.error('❌ Erreur changement avatar:', error);
        }
    }

    updateAvatarDisplay(avatarId) {
        const avatarElements = document.querySelectorAll('.player-avatar, .avatar-display');
        avatarElements.forEach(element => {
            element.src = `/static/images/avatars/${avatarId}.png`;
            element.alt = `Avatar ${avatarId}`;
        });
    }

    // ===== GESTION DU STORYTELLING =====

    async recordStoryChoice(storyArc, choice, context = {}) {
        try {
            const result = await this.storytellingEngine.recordChoice(
                this.playerId,
                storyArc,
                choice,
                context
            );

            if (result.success) {
                // Vérifier les Easter eggs
                this.checkEasterEggs(result);

                // Mettre à jour l'interface
                this.updateStoryInterface(result);

                return result;
            }
        } catch (error) {
            console.error('❌ Erreur enregistrement choix:', error);
        }
    }

    checkEasterEggs(choiceResult) {
        if (choiceResult.easter_eggs_triggered) {
            choiceResult.easter_eggs_triggered.forEach(egg => {
                this.showEasterEgg(egg);
            });
        }
    }

    showEasterEgg(egg) {
        // Créer une notification spéciale pour l'Easter egg
        const notification = {
            type: 'modal',
            title: `🥚 ${egg.title}`,
            message: egg.content.text,
            duration: 8000,
            style: 'easter-egg'
        };

        this.showNotification(notification);

        // Déclencher une micro-interaction spéciale
        this.handleMicroInteraction('badge_earned', document.body);
    }

    updateStoryInterface(storyResult) {
        // Mettre à jour l'interface selon les conséquences
        if (storyResult.consequences) {
            storyResult.consequences.forEach(consequence => {
                this.handleStoryConsequence(consequence);
            });
        }
    }

    handleStoryConsequence(consequence) {
        switch (consequence) {
            case 'unlock_new_arc':
                this.showNotification({
                    type: 'toast',
                    title: 'Nouveau Chapitre !',
                    message: 'Un nouveau chapitre de l\'histoire est disponible !',
                    duration: 5000,
                    style: 'story'
                });
                break;

            case 'lore_fragment':
                this.showNotification({
                    type: 'toast',
                    title: 'Fragment de Lore',
                    message: 'Vous avez découvert un nouveau fragment de l\'histoire !',
                    duration: 4000,
                    style: 'lore'
                });
                break;
        }
    }

    // ===== GESTION DES FONCTIONNALITÉS SOCIALES =====

    async createGuild(name, description = '') {
        try {
            const result = await this.socialEngine.createGuild(this.playerId, name, description);

            if (result.success) {
                this.showNotification({
                    type: 'toast',
                    title: 'Guilde Créée !',
                    message: `La guilde "${name}" a été créée avec succès !`,
                    duration: 5000,
                    style: 'success'
                });

                return result;
            }
        } catch (error) {
            console.error('❌ Erreur création guilde:', error);
        }
    }

    async joinGuild(guildId) {
        try {
            const result = await this.socialEngine.joinGuild(this.playerId, guildId);

            if (result.success) {
                this.showNotification({
                    type: 'toast',
                    title: 'Guilde Rejointe !',
                    message: 'Vous avez rejoint la guilde avec succès !',
                    duration: 4000,
                    style: 'success'
                });

                return result;
            }
        } catch (error) {
            console.error('❌ Erreur rejoindre guilde:', error);
        }
    }

    async sendGlobalMessage(message) {
        try {
            const result = await this.socialEngine.sendGlobalMessage(this.playerId, message);

            if (result.success) {
                // Ajouter le message à l'interface
                this.addMessageToChat({
                    sender: this.playerId,
                    message: message,
                    timestamp: new Date().toISOString(),
                    type: 'chat'
                });

                return result;
            }
        } catch (error) {
            console.error('❌ Erreur envoi message:', error);
        }
    }

    addMessageToChat(messageData) {
        const chatContainer = document.getElementById('global-chat');
        if (!chatContainer) return;

        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message';
        messageElement.innerHTML = `
            <div class="message-header">
                <span class="sender">${messageData.sender}</span>
                <span class="timestamp">${new Date(messageData.timestamp).toLocaleTimeString()}</span>
            </div>
            <div class="message-content">${messageData.message}</div>
        `;

        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // ===== API PUBLIQUE =====

    async unlockRandomCustomization(category = 'random') {
        try {
            const result = await this.customizationEngine.unlockRandom(this.playerId, category);

            if (result.success) {
                this.showNotification({
                    type: 'modal',
                    title: '🎁 Nouvelle Customisation !',
                    message: `Vous avez débloqué : ${result.unlocked_item.name}`,
                    duration: 6000,
                    style: 'unlock'
                });

                // Recharger les données
                await this.loadPlayerData();

                return result;
            }
        } catch (error) {
            console.error('❌ Erreur déverrouillage:', error);
        }
    }

    getPlayerData() {
        return this.playerData;
    }

    isReady() {
        return this.isInitialized;
    }
}

// ===== MOTEURS SPÉCIALISÉS =====

class SocialEngine {
    async getDashboard(playerId) {
        const response = await fetch(`/api/social/dashboard?player_id=${playerId}`);
        const data = await response.json();
        return data.dashboard;
    }

    async createGuild(playerId, name, description) {
        const response = await fetch('/api/social/guilds', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                creator_id: playerId,
                name: name,
                description: description
            })
        });
        return await response.json();
    }

    async joinGuild(playerId, guildId) {
        const response = await fetch(`/api/social/guilds/${guildId}/join`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_id: playerId })
        });
        return await response.json();
    }

    async sendGlobalMessage(playerId, message) {
        const response = await fetch('/api/social/chat/global', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sender_id: playerId,
                message: message,
                type: 'chat'
            })
        });
        return await response.json();
    }

    init() {
        // Initialisation du moteur social
    }
}

class CustomizationEngine {
    async getPlayerCustomization(playerId) {
        const response = await fetch(`/api/customization/player?player_id=${playerId}`);
        const data = await response.json();
        return data.customization;
    }

    async setTheme(playerId, themeId) {
        const response = await fetch(`/api/customization/themes/${themeId}/set`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_id: playerId })
        });
        return await response.json();
    }

    async setAvatar(playerId, avatarId) {
        const response = await fetch(`/api/customization/avatars/${avatarId}/set`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_id: playerId })
        });
        return await response.json();
    }

    async unlockRandom(playerId, category) {
        const response = await fetch('/api/customization/unlock/random', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                player_id: playerId,
                category: category
            })
        });
        return await response.json();
    }

    init() {
        // Initialisation du moteur de customisation
    }
}

class StorytellingEngine {
    async getStoryProgress(playerId) {
        const response = await fetch(`/api/story/progress?player_id=${playerId}`);
        const data = await response.json();
        return data.progress;
    }

    async recordChoice(playerId, storyArc, choice, context) {
        const response = await fetch('/api/story/choices', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                player_id: playerId,
                story_arc: storyArc,
                choice: choice,
                context: context
            })
        });
        return await response.json();
    }

    init() {
        // Initialisation du moteur de storytelling
    }
}

class MicroInteractionsEngine {
    async trigger(type, targetElement, context) {
        const response = await fetch('/api/interactions/trigger', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                player_id: context.player_id,
                type: type,
                target_element: targetElement ? targetElement.id || targetElement.className : null,
                context: context
            })
        });
        return await response.json();
    }

    async getPreferences(playerId) {
        const response = await fetch(`/api/interactions/preferences?player_id=${playerId}`);
        const data = await response.json();
        return data.preferences;
    }

    init() {
        // Initialisation du moteur de micro-interactions
    }
}

// ===== INITIALISATION GLOBALE =====

// Initialiser les fonctionnalités avancées
let advancedFeatures;

document.addEventListener('DOMContentLoaded', () => {
    advancedFeatures = new AdvancedFeaturesManager();

    // Exposer globalement
    window.advancedFeatures = advancedFeatures;

    console.log('🚀 Arkalia Quest - Fonctionnalités Avancées Chargées');
});

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AdvancedFeaturesManager };
}
