/**
 * Système d'empty states améliorés et motivants
 * Remplace les zones vides par des contenus engageants et animés
 */

class EmptyStatesEnhanced {
    constructor() {
        this.emptyStateTemplates = new Map();
        this.animatedElements = new Set();

        this.initializeSystem();
    }

    initializeSystem() {
        console.log('🌟 Système d\'empty states améliorés initialisé');
        this.createEmptyStateTemplates();
        this.setupEmptyStateDetection();
        this.createEmptyStateStyles();
    }

    createEmptyStateTemplates() {
        // Template pour les missions vides
        this.emptyStateTemplates.set('missions', {
            icon: '🎯',
            title: 'Aucune mission disponible',
            message: 'Les missions apparaîtront ici au fur et à mesure de votre progression !',
            action: 'Commencer l\'aventure',
            actionCommand: 'start_tutorial',
            animation: 'missions-empty',
            encouragement: [
                '🌟 Votre première mission vous attend !',
                '🚀 L\'aventure commence maintenant !',
                '💫 Prêt à découvrir Arkalia ?',
                '🎮 Commencez par le tutoriel !'
            ],
            visualEffects: ['sparkles', 'pulse', 'glow'],
            soundEffect: 'mission_available',
            interactiveElements: [
                { text: '💡 Astuce: Utilisez "aide" pour voir toutes les commandes', type: 'tip' },
                { text: '🌙 Parlez avec LUNA pour des conseils', type: 'suggestion' }
            ]
        });

        // Template pour les badges vides
        this.emptyStateTemplates.set('badges', {
            icon: '🏆',
            title: 'Aucun badge obtenu',
            message: 'Complétez des missions et des défis pour débloquer des badges !',
            action: 'Voir les défis',
            actionCommand: 'daily_challenges',
            animation: 'badges-empty',
            encouragement: [
                '🏅 Votre premier badge vous attend !',
                '⭐ Montrez votre talent !',
                '🎖️ Les récompenses vous attendent !',
                '🏆 Prêt à collectionner ?'
            ],
            visualEffects: ['badge-shine', 'bounce', 'rainbow'],
            soundEffect: 'badge_unlock',
            interactiveElements: [
                { text: '🎯 Complétez votre première mission', type: 'tip' },
                { text: '🎮 Jouez aux mini-jeux pour des points', type: 'suggestion' },
                { text: '🌙 Demandez à LUNA comment obtenir des badges', type: 'help' }
            ]
        });

        // Template pour le profil vide
        this.emptyStateTemplates.set('profil', {
            icon: '👤',
            title: 'Profil en construction',
            message: 'Votre profil se remplira au fur et à mesure de vos aventures !',
            action: 'Commencer à jouer',
            actionCommand: 'start_tutorial',
            animation: 'profil-empty',
            encouragement: [
                '🌟 Créez votre légende !',
                '🚀 Votre histoire commence ici !',
                '💫 Devenez un hacker légendaire !',
                '🎮 L\'aventure vous attend !'
            ]
        });

        // Template pour le leaderboard vide
        this.emptyStateTemplates.set('leaderboard', {
            icon: '📊',
            title: 'Classement en cours',
            message: 'Le classement se met à jour en temps réel !',
            action: 'Voir le profil',
            actionCommand: 'profil',
            animation: 'leaderboard-empty',
            encouragement: [
                '🏆 Montez dans le classement !',
                '⭐ Votre rang vous attend !',
                '🎯 Défiez les autres joueurs !',
                '🚀 Devenez numéro 1 !'
            ]
        });

        // Template pour le dashboard vide
        this.emptyStateTemplates.set('dashboard', {
            icon: '📈',
            title: 'Dashboard en préparation',
            message: 'Vos statistiques apparaîtront ici !',
            action: 'Explorer le monde',
            actionCommand: 'monde',
            animation: 'dashboard-empty',
            encouragement: [
                '📊 Vos données vous attendent !',
                '📈 Suivez votre progression !',
                '📋 Vos stats sont prêtes !',
                '🎯 Analysez vos performances !'
            ]
        });

        // Template pour les mini-jeux vides
        this.emptyStateTemplates.set('mini-games', {
            icon: '🎮',
            title: 'Mini-jeux en chargement',
            message: 'Les mini-jeux se débloquent avec la progression !',
            action: 'Commencer le tutoriel',
            actionCommand: 'start_tutorial',
            animation: 'games-empty',
            encouragement: [
                '🎮 Vos premiers jeux vous attendent !',
                '🎯 Débloquez de nouveaux défis !',
                '🎪 L\'amusement commence !',
                '🎲 Prêt à jouer ?'
            ],
            visualEffects: ['game-controller', 'pixel-art', 'retro-glow'],
            soundEffect: 'game_start',
            interactiveElements: [
                { text: '💻 Tapez "play_game" dans le terminal', type: 'tip' },
                { text: '🎯 Commencez par le tutoriel', type: 'suggestion' }
            ]
        });

        // Template pour le leaderboard vide
        this.emptyStateTemplates.set('leaderboard', {
            icon: '🏆',
            title: 'Classement en construction',
            message: 'Soyez le premier à apparaître ici !',
            action: 'Commencer à jouer',
            actionCommand: 'start_tutorial',
            animation: 'leaderboard-empty',
            encouragement: [
                '🥇 Soyez le numéro 1 !',
                '⭐ Montrez votre talent !',
                '🏆 Grimpez dans le classement !',
                '🎯 Votre nom vous attend !'
            ],
            visualEffects: ['trophy-glow', 'ranking-animation', 'victory-sparkles'],
            soundEffect: 'victory_fanfare',
            interactiveElements: [
                { text: '🎮 Jouez pour gagner des points', type: 'tip' },
                { text: '🌙 Demandez à LUNA comment progresser', type: 'suggestion' }
            ]
        });

        // Template pour les défis quotidiens vides
        this.emptyStateTemplates.set('daily-challenges', {
            icon: '📅',
            title: 'Défis quotidiens en préparation',
            message: 'De nouveaux défis arrivent bientôt !',
            action: 'Explorer le monde',
            actionCommand: 'monde',
            animation: 'challenges-empty',
            encouragement: [
                '📅 De nouveaux défis arrivent !',
                '🎯 Préparez-vous !',
                '⚡ L\'action commence bientôt !',
                '🌟 Soyez prêt !'
            ],
            visualEffects: ['calendar-flip', 'challenge-pulse', 'daily-glow'],
            soundEffect: 'challenge_available',
            interactiveElements: [
                { text: '🔄 Revenez demain pour de nouveaux défis', type: 'tip' },
                { text: '🌙 LUNA peut vous donner des conseils', type: 'suggestion' }
            ]
        });
    }

    createEmptyStateStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .empty-state-enhanced {
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, rgba(0, 255, 0, 0.05), rgba(0, 204, 0, 0.05));
                border: 2px dashed #00ff00;
                border-radius: 12px;
                margin: 20px 0;
                position: relative;
                overflow: hidden;
            }
            
            .empty-state-enhanced::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(0, 255, 0, 0.1), transparent);
                animation: empty-state-shine 3s ease-in-out infinite;
                pointer-events: none;
            }
            
            .empty-state-icon {
                font-size: 48px;
                margin-bottom: 20px;
                animation: empty-state-bounce 2s ease-in-out infinite;
            }
            
            .empty-state-title {
                color: #00ff00;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 15px;
                animation: empty-state-fade-in 1s ease-out;
            }
            
            .empty-state-message {
                color: #cccccc;
                font-size: 16px;
                margin-bottom: 25px;
                line-height: 1.5;
                animation: empty-state-fade-in 1s ease-out 0.2s both;
            }
            
            .empty-state-action {
                background: linear-gradient(45deg, #00ff00, #00cc00);
                color: #000;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s ease;
                animation: empty-state-fade-in 1s ease-out 0.4s both;
                position: relative;
                overflow: hidden;
            }
            
            .empty-state-action:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 15px rgba(0, 255, 0, 0.4);
            }
            
            .empty-state-action:active {
                transform: scale(0.95);
            }
            
            .empty-state-encouragement {
                margin-top: 20px;
                color: #00ff00;
                font-style: italic;
                font-size: 14px;
                animation: empty-state-fade-in 1s ease-out 0.6s both;
            }
            
            .empty-state-particles {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                overflow: hidden;
            }
            
            .empty-state-particle {
                position: absolute;
                width: 4px;
                height: 4px;
                background: #00ff00;
                border-radius: 50%;
                animation: empty-state-particle-float 4s ease-in-out infinite;
            }
            
            @keyframes empty-state-shine {
                0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
                100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            }
            
            @keyframes empty-state-bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            @keyframes empty-state-fade-in {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes empty-state-particle-float {
                0% { transform: translateY(100vh) translateX(0); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(-100px) translateX(50px); opacity: 0; }
            }
            
            /* Nouvelles animations pour les effets visuels */
            .badge-shine {
                animation: badge-shine 2s ease-in-out infinite;
            }
            
            @keyframes badge-shine {
                0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
                50% { box-shadow: 0 0 40px rgba(255, 215, 0, 0.8), 0 0 60px rgba(255, 215, 0, 0.6); }
            }
            
            .rainbow {
                animation: rainbow 3s ease-in-out infinite;
            }
            
            @keyframes rainbow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }
            
            .game-controller {
                animation: game-controller-bounce 2s ease-in-out infinite;
            }
            
            @keyframes game-controller-bounce {
                0%, 100% { transform: scale(1) rotate(0deg); }
                25% { transform: scale(1.1) rotate(5deg); }
                75% { transform: scale(1.1) rotate(-5deg); }
            }
            
            .pixel-art {
                image-rendering: pixelated;
                animation: pixel-art-flicker 1s ease-in-out infinite;
            }
            
            @keyframes pixel-art-flicker {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.8; }
            }
            
            .retro-glow {
                animation: retro-glow 2s ease-in-out infinite;
            }
            
            @keyframes retro-glow {
                0%, 100% { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
                50% { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00; }
            }
            
            .trophy-glow {
                animation: trophy-glow 2s ease-in-out infinite;
            }
            
            @keyframes trophy-glow {
                0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.6); }
                50% { box-shadow: 0 0 40px rgba(255, 215, 0, 0.9), 0 0 60px rgba(255, 215, 0, 0.7); }
            }
            
            .ranking-animation {
                animation: ranking-animation 3s ease-in-out infinite;
            }
            
            @keyframes ranking-animation {
                0% { transform: translateY(0) scale(1); }
                25% { transform: translateY(-5px) scale(1.05); }
                50% { transform: translateY(0) scale(1); }
                75% { transform: translateY(-3px) scale(1.02); }
                100% { transform: translateY(0) scale(1); }
            }
            
            .victory-sparkles {
                position: relative;
            }
            
            .victory-sparkles::before,
            .victory-sparkles::after {
                content: '✨';
                position: absolute;
                animation: victory-sparkles-float 2s ease-in-out infinite;
            }
            
            .victory-sparkles::before {
                top: -10px;
                left: 20px;
                animation-delay: 0s;
            }
            
            .victory-sparkles::after {
                top: -10px;
                right: 20px;
                animation-delay: 1s;
            }
            
            @keyframes victory-sparkles-float {
                0%, 100% { transform: translateY(0) rotate(0deg); opacity: 1; }
                50% { transform: translateY(-15px) rotate(180deg); opacity: 0.7; }
            }
            
            .calendar-flip {
                animation: calendar-flip 2s ease-in-out infinite;
            }
            
            @keyframes calendar-flip {
                0%, 100% { transform: rotateY(0deg); }
                50% { transform: rotateY(180deg); }
            }
            
            .challenge-pulse {
                animation: challenge-pulse 1.5s ease-in-out infinite;
            }
            
            @keyframes challenge-pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .daily-glow {
                animation: daily-glow 2s ease-in-out infinite;
            }
            
            @keyframes daily-glow {
                0%, 100% { box-shadow: 0 0 15px rgba(0, 255, 0, 0.5); }
                50% { box-shadow: 0 0 25px rgba(0, 255, 0, 0.8), 0 0 35px rgba(0, 255, 0, 0.6); }
            }
            
            /* Animations spécifiques par type */
            .missions-empty .empty-state-icon {
                animation: missions-pulse 2s ease-in-out infinite;
            }
            
            .badges-empty .empty-state-icon {
                animation: badges-rotate 3s linear infinite;
            }
            
            .profil-empty .empty-state-icon {
                animation: profil-glow 2s ease-in-out infinite;
            }
            
            .leaderboard-empty .empty-state-icon {
                animation: leaderboard-bounce 1.5s ease-in-out infinite;
            }
            
            .dashboard-empty .empty-state-icon {
                animation: dashboard-pulse 2s ease-in-out infinite;
            }
            
            .games-empty .empty-state-icon {
                animation: games-spin 2s linear infinite;
            }
            
            @keyframes missions-pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            @keyframes badges-rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @keyframes profil-glow {
                0%, 100% { text-shadow: 0 0 10px #00ff00; }
                50% { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; }
            }
            
            @keyframes leaderboard-bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-15px); }
            }
            
            @keyframes dashboard-pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.05); opacity: 0.8; }
            }
            
            @keyframes games-spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }

    setupEmptyStateDetection() {
        // Observer les changements dans le DOM pour détecter les zones vides
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    this.checkForEmptyStates();
                }
            });
        });

        // Observer le document entier
        observer.observe(document.body, { childList: true, subtree: true });

        // Vérifier au chargement
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => this.checkForEmptyStates(), 1000);
        });
    }

    checkForEmptyStates() {
        // Vérifier les sections communes qui peuvent être vides
        const sectionsToCheck = [
            { selector: '.missions, .missions-list', type: 'missions' },
            { selector: '.badges, .badges-list', type: 'badges' },
            { selector: '.profil, .profile', type: 'profil' },
            { selector: '.leaderboard, .ranking', type: 'leaderboard' },
            { selector: '.dashboard, .stats', type: 'dashboard' },
            { selector: '.mini-games, .games-list', type: 'mini-games' }
        ];

        sectionsToCheck.forEach(({ selector, type }) => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (this.isEmpty(element)) {
                    this.enhanceEmptyState(element, type);
                }
            });
        });
    }

    isEmpty(element) {
        // Vérifier si un élément est vide ou ne contient que des éléments vides
        const children = element.children;
        if (children.length === 0) return true;

        // Vérifier si tous les enfants sont vides
        for (let child of children) {
            if (child.textContent.trim() !== '' || child.children.length > 0) {
                return false;
            }
        }

        return true;
    }

    enhanceEmptyState(element, type) {
        // Éviter les doublons
        if (element.querySelector('.empty-state-enhanced')) return;

        const template = this.emptyStateTemplates.get(type);
        if (!template) return;

        // Créer l'empty state
        const emptyState = document.createElement('div');
        emptyState.className = `empty-state-enhanced ${template.animation}`;

        // Choisir un encouragement aléatoire
        const encouragement = template.encouragement[Math.floor(Math.random() * template.encouragement.length)];

        emptyState.innerHTML = `
            <div class="empty-state-particles" id="particles-${Date.now()}"></div>
            <div class="empty-state-icon">${template.icon}</div>
            <div class="empty-state-title">${template.title}</div>
            <div class="empty-state-message">${template.message}</div>
            <button class="empty-state-action" onclick="window.emptyStatesEnhanced.handleEmptyStateAction('${template.actionCommand}')">
                ${template.action}
            </button>
            <div class="empty-state-encouragement">${encouragement}</div>
        `;

        // Remplacer le contenu vide
        element.innerHTML = '';
        element.appendChild(emptyState);

        // Ajouter des particules animées
        this.addParticles(emptyState);

        // Enregistrer l'élément animé
        this.animatedElements.add(emptyState);
    }

    addParticles(container) {
        const particlesContainer = container.querySelector('.empty-state-particles');
        if (!particlesContainer) return;

        // Créer des particules flottantes
        for (let i = 0; i < 10; i++) {
            const particle = document.createElement('div');
            particle.className = 'empty-state-particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 4 + 's';
            particle.style.animationDuration = (Math.random() * 2 + 3) + 's';
            particlesContainer.appendChild(particle);
        }
    }

    handleEmptyStateAction(command) {
        // Exécuter la commande associée
        if (command === 'start_tutorial') {
            window.location.href = '/tutorial';
        } else if (command === 'daily_challenges') {
            // Afficher les défis quotidiens
            this.showDailyChallenges();
        } else if (command === 'profil') {
            window.location.href = '/profil';
        } else if (command === 'monde') {
            window.location.href = '/monde';
        } else {
            // Essayer d'exécuter la commande dans le terminal
            this.executeCommand(command);
        }
    }

    showDailyChallenges() {
        // Créer une modal pour les défis quotidiens
        const modal = document.createElement('div');
        modal.className = 'daily-challenges-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            display: flex;
            justify-content: center;
            align-items: center;
        `;

        modal.innerHTML = `
            <div style="background: linear-gradient(135deg, #001100, #003300); border: 2px solid #00ff00; border-radius: 12px; padding: 20px; max-width: 500px; color: #00ff00;">
                <h3>🎯 Défis Quotidiens</h3>
                <p>Les défis quotidiens vous permettent de gagner de l'XP et des récompenses !</p>
                <button onclick="this.parentElement.parentElement.remove()" style="background: #00ff00; color: #000; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">Fermer</button>
            </div>
        `;

        document.body.appendChild(modal);
    }

    executeCommand(command) {
        // Déclencher l'événement de commande
        document.dispatchEvent(new CustomEvent('arkalia_command', {
            detail: { command }
        }));
    }

    // Méthodes publiques
    refreshEmptyStates() {
        this.checkForEmptyStates();
    }

    addEmptyStateTemplate(type, template) {
        this.emptyStateTemplates.set(type, template);
    }

    getEmptyStateStats() {
        return {
            totalEmptyStates: this.animatedElements.size,
            templates: Array.from(this.emptyStateTemplates.keys())
        };
    }
}

// Initialiser le système d'empty states améliorés
window.emptyStatesEnhanced = new EmptyStatesEnhanced();
