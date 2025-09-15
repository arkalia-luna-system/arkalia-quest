/**
 * Système d'amélioration des empty states
 * Transforme les états vides en expériences engageantes
 */

class EnhancedEmptyStates {
    constructor() {
        this.playerProfile = this.detectPlayerProfile();
        this.emptyStateTemplates = this.initializeEmptyStateTemplates();
        this.initializeSystem();
    }

    detectPlayerProfile() {
        // Détection basée sur les interactions
        const interactions = JSON.parse(localStorage.getItem('arkalia_interaction_history') || '[]');
        const timeSpent = this.calculateTimeSpent();
        const commandPatterns = interactions.map(i => i.action);

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

    initializeEmptyStateTemplates() {
        return {
            debutant: {
                noMissions: {
                    title: "🌟 Aucune mission disponible",
                    message: "Tu n'as pas encore de missions ! Commence par explorer le monde pour découvrir de nouvelles aventures.",
                    action: "Explorer le monde",
                    icon: "🎯",
                    animation: "bounce"
                },
                noBadges: {
                    title: "🏆 Aucun badge débloqué",
                    message: "Tu n'as pas encore de badges ! Complète des missions et des défis pour gagner tes premiers badges.",
                    action: "Voir les missions",
                    icon: "⭐",
                    animation: "pulse"
                },
                noProgress: {
                    title: "📈 Aucune progression",
                    message: "Tu n'as pas encore de progression ! Commence à jouer pour voir tes statistiques s'améliorer.",
                    action: "Commencer à jouer",
                    icon: "🚀",
                    animation: "glow"
                },
                noLeaderboard: {
                    title: "🏆 Classement vide",
                    message: "Le classement est vide ! Sois le premier à marquer des points et à dominer le jeu.",
                    action: "Jouer maintenant",
                    icon: "👑",
                    animation: "sparkle"
                }
            },
            experimente: {
                noMissions: {
                    title: "⚡ Aucune mission disponible",
                    message: "Aucune mission active. Tu peux en créer une nouvelle ou explorer d'autres zones.",
                    action: "Créer une mission",
                    icon: "🎯",
                    animation: "fadeIn"
                },
                noBadges: {
                    title: "🏆 Aucun badge débloqué",
                    message: "Aucun badge obtenu. Les défis avancés t'attendent pour débloquer des récompenses.",
                    action: "Voir les défis",
                    icon: "⭐",
                    animation: "slideIn"
                },
                noProgress: {
                    title: "📊 Aucune donnée",
                    message: "Aucune donnée de progression. Lance une mission pour commencer à collecter des statistiques.",
                    action: "Lancer une mission",
                    icon: "📈",
                    animation: "zoomIn"
                },
                noLeaderboard: {
                    title: "🏆 Classement vide",
                    message: "Le classement est vide. Sois le premier à établir un record et à montrer tes compétences.",
                    action: "Établir un record",
                    icon: "🏅",
                    animation: "scaleIn"
                }
            },
            competitif: {
                noMissions: {
                    title: "⚔️ Aucune mission de combat",
                    message: "Aucune mission de combat disponible ! Crée une mission pour défier d'autres joueurs.",
                    action: "Créer un défi",
                    icon: "⚔️",
                    animation: "shake"
                },
                noBadges: {
                    title: "👑 Aucun badge de champion",
                    message: "Aucun badge de champion ! Gagne des duels et des compétitions pour débloquer des récompenses.",
                    action: "Rejoindre un duel",
                    icon: "🏆",
                    animation: "bounce"
                },
                noProgress: {
                    title: "📊 Aucune statistique de victoire",
                    message: "Aucune statistique de victoire ! Commence à jouer pour établir ton record de victoires.",
                    action: "Commencer à dominer",
                    icon: "📈",
                    animation: "glow"
                },
                noLeaderboard: {
                    title: "🏆 Aucun classement de guerre",
                    message: "Aucun classement de guerre ! Sois le premier à établir ta domination sur le jeu.",
                    action: "Conquérir le jeu",
                    icon: "👑",
                    animation: "sparkle"
                }
            },
            creatif: {
                noMissions: {
                    title: "🎨 Aucune mission créative",
                    message: "Aucune mission créative disponible ! Crée ta propre aventure et explore de nouvelles possibilités.",
                    action: "Créer une aventure",
                    icon: "🎨",
                    animation: "rainbow"
                },
                noBadges: {
                    title: "💫 Aucun badge d'artiste",
                    message: "Aucun badge d'artiste ! Exprime ta créativité et débloque des récompenses uniques.",
                    action: "Exprimer ma créativité",
                    icon: "💫",
                    animation: "float"
                },
                noProgress: {
                    title: "🌟 Aucune progression créative",
                    message: "Aucune progression créative ! Commence à créer pour voir tes œuvres s'améliorer.",
                    action: "Commencer à créer",
                    icon: "🌟",
                    animation: "twinkle"
                },
                noLeaderboard: {
                    title: "🎭 Aucun classement d'artiste",
                    message: "Aucun classement d'artiste ! Sois le premier à montrer ta créativité au monde.",
                    action: "Montrer ma créativité",
                    icon: "🎭",
                    animation: "dance"
                }
            },
            casual: {
                noMissions: {
                    title: "😊 Aucune mission tranquille",
                    message: "Aucune mission tranquille disponible ! Prends ton temps pour explorer et découvrir de nouvelles choses.",
                    action: "Explorer tranquillement",
                    icon: "😊",
                    animation: "gentle"
                },
                noBadges: {
                    title: "🌟 Aucun badge de détente",
                    message: "Aucun badge de détente ! Profite du jeu à ton rythme et débloque des récompenses douces.",
                    action: "Profiter du jeu",
                    icon: "🌟",
                    animation: "soft"
                },
                noProgress: {
                    title: "📊 Aucune progression douce",
                    message: "Aucune progression douce ! Commence à jouer tranquillement pour voir tes progrès.",
                    action: "Jouer tranquillement",
                    icon: "📊",
                    animation: "breathe"
                },
                noLeaderboard: {
                    title: "🏆 Aucun classement relaxant",
                    message: "Aucun classement relaxant ! Prends ton temps pour établir ton propre rythme.",
                    action: "Prendre mon temps",
                    icon: "🏆",
                    animation: "calm"
                }
            }
        };
    }

    initializeSystem() {
        // Observer les changements dans les éléments vides
        this.observeEmptyElements();

        // Améliorer les empty states existants
        this.enhanceExistingEmptyStates();

        // Créer des animations CSS
        this.createAnimationStyles();
    }

    observeEmptyElements() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    this.checkForEmptyElements(mutation.target);
                }
            });
        });

        // Observer les conteneurs principaux
        const containers = document.querySelectorAll('.missions, .badges, .progress, .leaderboard, .dashboard');
        containers.forEach(container => {
            observer.observe(container, {
                childList: true,
                subtree: true
            });
        });
    }

    checkForEmptyElements(container) {
        // Vérifier si le conteneur est vide
        if (container.children.length === 0 || this.isEmpty(container)) {
            this.enhanceEmptyState(container);
        }
    }

    isEmpty(element) {
        const text = element.textContent.trim();
        return text === '' || text === 'Aucune donnée' || text === 'N/A' || text === '--';
    }

    enhanceEmptyState(container) {
        const containerType = this.getContainerType(container);
        const template = this.getEmptyStateTemplate(containerType);

        if (template) {
            this.createEnhancedEmptyState(container, template);
        }
    }

    getContainerType(container) {
        if (container.classList.contains('missions') || container.querySelector('.mission')) {
            return 'noMissions';
        } else if (container.classList.contains('badges') || container.querySelector('.badge')) {
            return 'noBadges';
        } else if (container.classList.contains('progress') || container.querySelector('.progress')) {
            return 'noProgress';
        } else if (container.classList.contains('leaderboard') || container.querySelector('.leaderboard')) {
            return 'noLeaderboard';
        }
        return 'noProgress';
    }

    getEmptyStateTemplate(containerType) {
        const profile = this.playerProfile;
        return this.emptyStateTemplates[profile]?.[containerType] || this.emptyStateTemplates.debutant[containerType];
    }

    createEnhancedEmptyState(container, template) {
        // Supprimer le contenu existant
        container.innerHTML = '';

        // Créer l'empty state amélioré
        const emptyState = document.createElement('div');
        emptyState.className = `enhanced-empty-state ${template.animation}`;
        emptyState.innerHTML = `
            <div class="empty-state-icon">${template.icon}</div>
            <h3 class="empty-state-title">${template.title}</h3>
            <p class="empty-state-message">${template.message}</p>
            <button class="empty-state-action" onclick="enhancedEmptyStates.handleEmptyStateAction('${template.action}')">
                ${template.action}
            </button>
        `;

        // Styles
        emptyState.style.cssText = `
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #001100, #003300);
            border: 2px dashed #00ff00;
            border-radius: 15px;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        `;

        // Ajouter l'animation
        this.addAnimation(emptyState, template.animation);

        container.appendChild(emptyState);
    }

    addAnimation(element, animationType) {
        const animations = {
            bounce: 'bounce 2s ease-in-out infinite',
            pulse: 'pulse 2s ease-in-out infinite',
            glow: 'glow 2s ease-in-out infinite',
            sparkle: 'sparkle 2s ease-in-out infinite',
            fadeIn: 'fadeIn 1s ease-in-out',
            slideIn: 'slideIn 1s ease-in-out',
            zoomIn: 'zoomIn 1s ease-in-out',
            scaleIn: 'scaleIn 1s ease-in-out',
            shake: 'shake 0.5s ease-in-out infinite',
            rainbow: 'rainbow 3s ease-in-out infinite',
            float: 'float 2s ease-in-out infinite',
            twinkle: 'twinkle 1.5s ease-in-out infinite',
            dance: 'dance 2s ease-in-out infinite',
            gentle: 'gentle 2s ease-in-out infinite',
            soft: 'soft 2s ease-in-out infinite',
            breathe: 'breathe 3s ease-in-out infinite',
            calm: 'calm 2s ease-in-out infinite'
        };

        if (animations[animationType]) {
            element.style.animation = animations[animationType];
        }
    }

    createAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.05); opacity: 0.8; }
            }
            
            @keyframes glow {
                0%, 100% { box-shadow: 0 0 20px #00ff00; }
                50% { box-shadow: 0 0 40px #00ff00, 0 0 60px #00ff00; }
            }
            
            @keyframes sparkle {
                0%, 100% { transform: scale(1) rotate(0deg); }
                25% { transform: scale(1.1) rotate(90deg); }
                50% { transform: scale(1.2) rotate(180deg); }
                75% { transform: scale(1.1) rotate(270deg); }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-50px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            @keyframes zoomIn {
                from { opacity: 0; transform: scale(0.5); }
                to { opacity: 1; transform: scale(1); }
            }
            
            @keyframes scaleIn {
                from { opacity: 0; transform: scale(0.8); }
                to { opacity: 1; transform: scale(1); }
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            @keyframes rainbow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-10px) rotate(5deg); }
            }
            
            @keyframes twinkle {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.5; transform: scale(1.1); }
            }
            
            @keyframes dance {
                0%, 100% { transform: rotate(0deg) scale(1); }
                25% { transform: rotate(-5deg) scale(1.05); }
                75% { transform: rotate(5deg) scale(1.05); }
            }
            
            @keyframes gentle {
                0%, 100% { transform: translateY(0) scale(1); }
                50% { transform: translateY(-5px) scale(1.02); }
            }
            
            @keyframes soft {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.8; transform: scale(1.01); }
            }
            
            @keyframes breathe {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.02); opacity: 0.9; }
            }
            
            @keyframes calm {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-3px) rotate(1deg); }
            }
            
            .enhanced-empty-state .empty-state-icon {
                font-size: 4rem;
                margin-bottom: 20px;
                display: block;
            }
            
            .enhanced-empty-state .empty-state-title {
                color: #00ff00;
                font-size: 1.5rem;
                margin-bottom: 15px;
                font-weight: bold;
            }
            
            .enhanced-empty-state .empty-state-message {
                color: #ccc;
                font-size: 1rem;
                margin-bottom: 25px;
                line-height: 1.5;
            }
            
            .enhanced-empty-state .empty-state-action {
                background: linear-gradient(45deg, #00ff00, #0080ff);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 1rem;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 255, 0, 0.3);
            }
            
            .enhanced-empty-state .empty-state-action:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 255, 0, 0.5);
            }
            
            .enhanced-empty-state .empty-state-action:active {
                transform: translateY(0);
                box-shadow: 0 2px 10px rgba(0, 255, 0, 0.3);
            }
        `;
        document.head.appendChild(style);
    }

    enhanceExistingEmptyStates() {
        // Améliorer les empty states existants
        const emptyElements = document.querySelectorAll('.empty-state, .no-data, .no-content');
        emptyElements.forEach(element => {
            this.enhanceEmptyState(element);
        });
    }

    handleEmptyStateAction(action) {
        // Gérer les actions des empty states
        switch (action) {
            case 'Explorer le monde':
                window.location.href = '/monde';
                break;
            case 'Voir les missions':
                window.location.href = '/monde';
                break;
            case 'Commencer à jouer':
                window.location.href = '/terminal';
                break;
            case 'Jouer maintenant':
                window.location.href = '/terminal';
                break;
            case 'Créer une mission':
                this.showCreateMissionModal();
                break;
            case 'Voir les défis':
                this.showChallengesModal();
                break;
            case 'Lancer une mission':
                this.showMissionModal();
                break;
            case 'Établir un record':
                this.showRecordModal();
                break;
            case 'Créer un défi':
                this.showCreateChallengeModal();
                break;
            case 'Rejoindre un duel':
                this.showDuelModal();
                break;
            case 'Commencer à dominer':
                this.showDominationModal();
                break;
            case 'Conquérir le jeu':
                this.showConquestModal();
                break;
            case 'Créer une aventure':
                this.showCreateAdventureModal();
                break;
            case 'Exprimer ma créativité':
                this.showCreativityModal();
                break;
            case 'Commencer à créer':
                this.showCreateModal();
                break;
            case 'Montrer ma créativité':
                this.showShowcaseModal();
                break;
            case 'Explorer tranquillement':
                this.showGentleExplorationModal();
                break;
            case 'Profiter du jeu':
                this.showRelaxModal();
                break;
            case 'Jouer tranquillement':
                this.showCasualPlayModal();
                break;
            case 'Prendre mon temps':
                this.showTakeTimeModal();
                break;
            default:
                console.log('Action non reconnue:', action);
        }
    }

    showCreateMissionModal() {
        this.showModal('Créer une mission', 'Fonctionnalité à venir...');
    }

    showChallengesModal() {
        this.showModal('Défis disponibles', 'Fonctionnalité à venir...');
    }

    showMissionModal() {
        this.showModal('Lancer une mission', 'Fonctionnalité à venir...');
    }

    showRecordModal() {
        this.showModal('Établir un record', 'Fonctionnalité à venir...');
    }

    showCreateChallengeModal() {
        this.showModal('Créer un défi', 'Fonctionnalité à venir...');
    }

    showDuelModal() {
        this.showModal('Rejoindre un duel', 'Fonctionnalité à venir...');
    }

    showDominationModal() {
        this.showModal('Commencer à dominer', 'Fonctionnalité à venir...');
    }

    showConquestModal() {
        this.showModal('Conquérir le jeu', 'Fonctionnalité à venir...');
    }

    showCreateAdventureModal() {
        this.showModal('Créer une aventure', 'Fonctionnalité à venir...');
    }

    showCreativityModal() {
        this.showModal('Exprimer ma créativité', 'Fonctionnalité à venir...');
    }

    showCreateModal() {
        this.showModal('Commencer à créer', 'Fonctionnalité à venir...');
    }

    showShowcaseModal() {
        this.showModal('Montrer ma créativité', 'Fonctionnalité à venir...');
    }

    showGentleExplorationModal() {
        this.showModal('Explorer tranquillement', 'Fonctionnalité à venir...');
    }

    showRelaxModal() {
        this.showModal('Profiter du jeu', 'Fonctionnalité à venir...');
    }

    showCasualPlayModal() {
        this.showModal('Jouer tranquillement', 'Fonctionnalité à venir...');
    }

    showTakeTimeModal() {
        this.showModal('Prendre mon temps', 'Fonctionnalité à venir...');
    }

    showModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'enhanced-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close" onclick="this.parentElement.parentElement.parentElement.remove()">×</button>
                </div>
                <div class="modal-body">
                    <p>${content}</p>
                </div>
            </div>
        `;

        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;

        const modalContent = modal.querySelector('.modal-content');
        modalContent.style.cssText = `
            background: linear-gradient(135deg, #001100, #003300);
            border: 2px solid #00ff00;
            border-radius: 15px;
            padding: 20px;
            max-width: 500px;
            width: 90%;
            text-align: center;
        `;

        document.body.appendChild(modal);
    }

    calculateTimeSpent() {
        const startTime = localStorage.getItem('arkalia_session_start');
        if (startTime) {
            return Date.now() - parseInt(startTime);
        }
        return 0;
    }
}

// Initialiser le système d'empty states améliorés
const enhancedEmptyStates = new EnhancedEmptyStates();

// Exporter pour utilisation globale
window.EnhancedEmptyStates = EnhancedEmptyStates;
window.enhancedEmptyStates = enhancedEmptyStates;
