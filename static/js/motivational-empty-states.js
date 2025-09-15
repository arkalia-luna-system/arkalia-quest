/* ===== ARKALIA QUEST - MOTIVATIONAL EMPTY STATES ===== */
/* États vides motivants pour encourager l'engagement */

class MotivationalEmptyStates {
    constructor() {
        this.emptyStateMessages = this.initializeEmptyStateMessages();
        this.currentState = null;
        this.init();
    }

    init() {
        this.setupEmptyStateObserver();
        this.createEmptyStateStyles();
    }

    initializeEmptyStateMessages() {
        return {
            // Messages pour les statistiques vides
            stats: {
                xp: [
                    "🌟 Commence ton aventure ! Chaque action te rapporte de l'XP",
                    "🚀 L'XP, c'est la clé de la progression dans Arkalia !",
                    "💫 Plus tu explores, plus tu gagnes d'XP !",
                    "🎯 Chaque mission complétée te rapporte de l'expérience !"
                ],
                coins: [
                    "💰 Les coins sont ta monnaie dans Arkalia !",
                    "💎 Gagne des coins en complétant des défis !",
                    "🏆 Les coins te permettent d'acheter des améliorations !",
                    "💸 Plus tu joues, plus tu deviens riche !"
                ],
                badges: [
                    "🏅 Les badges montrent tes accomplissements !",
                    "🥇 Chaque badge raconte une partie de ton histoire !",
                    "🎖️ Collectionne tous les badges d'Arkalia !",
                    "🌟 Les badges sont la preuve de tes compétences !"
                ],
                missions: [
                    "🎯 Les missions sont ton chemin vers la gloire !",
                    "📋 Chaque mission te rapproche de la vérité !",
                    "🎪 Les missions révèlent les secrets d'Arkalia !",
                    "🎲 Lance-toi dans ta première mission !"
                ],
                achievements: [
                    "🏆 Les succès marquent tes victoires !",
                    "🎊 Chaque succès est une célébration !",
                    "🌟 Les succès racontent ton parcours !",
                    "🎉 Collectionne tous les succès possibles !"
                ]
            },

            // Messages pour les zones vides
            zones: {
                explored: [
                    "🗺️ Explore le monde d'Arkalia !",
                    "🌍 Chaque zone a ses secrets !",
                    "🔍 Découvre de nouveaux horizons !",
                    "🌟 L'exploration révèle des trésors !"
                ],
                secrets: [
                    "🔍 Les secrets sont partout !",
                    "💎 Cherche bien, tu trouveras !",
                    "🎁 Les secrets récompensent les curieux !",
                    "🌟 Plus tu cherches, plus tu trouves !"
                ]
            },

            // Messages pour les interactions sociales
            social: {
                friends: [
                    "👥 Trouve des alliés dans Arkalia !",
                    "🤝 Les amis rendent l'aventure plus belle !",
                    "💬 Rencontre d'autres hackers !",
                    "🌟 Ensemble, vous êtes plus forts !"
                ],
                messages: [
                    "💬 Commence une conversation !",
                    "📝 Partage tes découvertes !",
                    "🗨️ La communication est la clé !",
                    "💭 Tes pensées comptent !"
                ]
            },

            // Messages pour les mini-jeux
            minigames: [
                "🎮 Teste tes compétences !",
                "🎯 Les mini-jeux sont amusants !",
                "🎪 Chaque jeu est un défi !",
                "🌟 Amuse-toi en apprenant !"
            ],

            // Messages pour les thèmes
            themes: [
                "🎨 Personnalise ton expérience !",
                "🌈 Chaque thème a sa personnalité !",
                "✨ Trouve ton style !",
                "🌟 Laisse libre cours à ta créativité !"
            ]
        };
    }

    setupEmptyStateObserver() {
        // Observer les changements dans le DOM pour détecter les états vides
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    this.checkForEmptyStates();
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Vérifier immédiatement
        this.checkForEmptyStates();
    }

    checkForEmptyStates() {
        // Vérifier les différents types d'états vides
        this.checkStatsEmptyStates();
        this.checkZonesEmptyStates();
        this.checkSocialEmptyStates();
        this.checkMinigamesEmptyStates();
        this.checkThemesEmptyStates();
    }

    checkStatsEmptyStates() {
        // Vérifier les statistiques vides
        const statsElements = document.querySelectorAll('.stat-value, .metric-value, .kpi-value');

        statsElements.forEach(element => {
            const value = element.textContent.trim();
            if (value === '0' || value === '' || value === '--') {
                this.showEmptyStateMessage(element, 'stats');
            }
        });
    }

    checkZonesEmptyStates() {
        // Vérifier les zones d'exploration vides
        const zoneElements = document.querySelectorAll('.zone-list, .exploration-area');

        zoneElements.forEach(element => {
            if (element.children.length === 0) {
                this.showEmptyStateMessage(element, 'zones');
            }
        });
    }

    checkSocialEmptyStates() {
        // Vérifier les zones sociales vides
        const socialElements = document.querySelectorAll('.friends-list, .messages-list, .social-area');

        socialElements.forEach(element => {
            if (element.children.length === 0) {
                this.showEmptyStateMessage(element, 'social');
            }
        });
    }

    checkMinigamesEmptyStates() {
        // Vérifier les mini-jeux vides
        const minigameElements = document.querySelectorAll('.minigames-list, .games-area');

        minigameElements.forEach(element => {
            if (element.children.length === 0) {
                this.showEmptyStateMessage(element, 'minigames');
            }
        });
    }

    checkThemesEmptyStates() {
        // Vérifier les thèmes vides
        const themeElements = document.querySelectorAll('.themes-list, .theme-selection');

        themeElements.forEach(element => {
            if (element.children.length === 0) {
                this.showEmptyStateMessage(element, 'themes');
            }
        });
    }

    showEmptyStateMessage(element, type) {
        // Vérifier si un message est déjà affiché
        if (element.querySelector('.empty-state-message')) return;

        const message = this.getRandomMessage(type);
        const emptyStateElement = this.createEmptyStateElement(message, type);

        element.appendChild(emptyStateElement);

        // Ajouter une animation d'apparition
        setTimeout(() => {
            emptyStateElement.classList.add('show');
        }, 100);
    }

    getRandomMessage(type) {
        const messages = this.emptyStateMessages[type];
        if (!messages) return "Commence ton aventure !";

        const randomIndex = Math.floor(Math.random() * messages.length);
        return messages[randomIndex];
    }

    createEmptyStateElement(message, type) {
        const element = document.createElement('div');
        element.className = 'empty-state-message';
        element.innerHTML = `
            <div class="empty-state-content">
                <div class="empty-state-icon">${this.getIconForType(type)}</div>
                <div class="empty-state-text">${message}</div>
                <div class="empty-state-action">
                    <button class="empty-state-btn" onclick="motivationalEmptyStates.hideEmptyState(this)">
                        Compris !
                    </button>
                </div>
            </div>
        `;

        return element;
    }

    getIconForType(type) {
        const icons = {
            stats: '📊',
            zones: '🗺️',
            social: '👥',
            minigames: '🎮',
            themes: '🎨'
        };

        return icons[type] || '🌟';
    }

    hideEmptyState(button) {
        const emptyStateElement = button.closest('.empty-state-message');
        if (emptyStateElement) {
            emptyStateElement.classList.add('hide');
            setTimeout(() => {
                emptyStateElement.remove();
            }, 300);
        }
    }

    createEmptyStateStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .empty-state-message {
                position: relative;
                background: rgba(167, 139, 250, 0.05);
                border: 2px dashed rgba(167, 139, 250, 0.3);
                border-radius: 15px;
                padding: 30px;
                margin: 20px 0;
                text-align: center;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s ease;
            }
            
            .empty-state-message.show {
                opacity: 1;
                transform: translateY(0);
            }
            
            .empty-state-message.hide {
                opacity: 0;
                transform: translateY(-20px);
            }
            
            .empty-state-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 15px;
            }
            
            .empty-state-icon {
                font-size: 3em;
                animation: emptyStatePulse 2s ease-in-out infinite;
            }
            
            @keyframes emptyStatePulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            .empty-state-text {
                color: var(--violet-lunaire);
                font-size: 1.1em;
                font-weight: 500;
                line-height: 1.4;
                max-width: 300px;
            }
            
            .empty-state-action {
                margin-top: 10px;
            }
            
            .empty-state-btn {
                background: linear-gradient(135deg, rgba(167, 139, 250, 0.2), rgba(96, 165, 250, 0.2));
                border: 1px solid rgba(167, 139, 250, 0.4);
                border-radius: 8px;
                padding: 10px 20px;
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 0.9em;
                font-weight: 500;
            }
            
            .empty-state-btn:hover {
                background: linear-gradient(135deg, rgba(167, 139, 250, 0.4), rgba(96, 165, 250, 0.4));
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(167, 139, 250, 0.3);
            }
            
            .empty-state-btn:active {
                transform: translateY(0);
            }
            
            /* Styles spécifiques pour différents types */
            .empty-state-message[data-type="stats"] {
                border-color: rgba(34, 197, 94, 0.3);
                background: rgba(34, 197, 94, 0.05);
            }
            
            .empty-state-message[data-type="zones"] {
                border-color: rgba(59, 130, 246, 0.3);
                background: rgba(59, 130, 246, 0.05);
            }
            
            .empty-state-message[data-type="social"] {
                border-color: rgba(168, 85, 247, 0.3);
                background: rgba(168, 85, 247, 0.05);
            }
            
            .empty-state-message[data-type="minigames"] {
                border-color: rgba(245, 158, 11, 0.3);
                background: rgba(245, 158, 11, 0.05);
            }
            
            .empty-state-message[data-type="themes"] {
                border-color: rgba(236, 72, 153, 0.3);
                background: rgba(236, 72, 153, 0.05);
            }
            
            /* Animation de particules pour les états vides */
            .empty-state-message::before {
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(45deg, transparent, rgba(167, 139, 250, 0.1), transparent);
                border-radius: 15px;
                animation: emptyStateGlow 3s ease-in-out infinite;
                z-index: -1;
            }
            
            @keyframes emptyStateGlow {
                0%, 100% { opacity: 0; }
                50% { opacity: 1; }
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .empty-state-message {
                    padding: 20px;
                    margin: 15px 0;
                }
                
                .empty-state-text {
                    font-size: 1em;
                    max-width: 250px;
                }
                
                .empty-state-icon {
                    font-size: 2.5em;
                }
            }
        `;

        document.head.appendChild(style);
    }

    // Méthodes publiques pour les interactions
    onStatsEmpty(statType) {
        this.showEmptyStateMessage(document.querySelector(`.${statType}-value`), 'stats');
    }

    onZonesEmpty() {
        this.showEmptyStateMessage(document.querySelector('.zones-area'), 'zones');
    }

    onSocialEmpty() {
        this.showEmptyStateMessage(document.querySelector('.social-area'), 'social');
    }

    onMinigamesEmpty() {
        this.showEmptyStateMessage(document.querySelector('.minigames-area'), 'minigames');
    }

    onThemesEmpty() {
        this.showEmptyStateMessage(document.querySelector('.themes-area'), 'themes');
    }
}

// Initialiser le système d'états vides motivants
document.addEventListener('DOMContentLoaded', () => {
    window.motivationalEmptyStates = new MotivationalEmptyStates();
});

// Exporter pour utilisation globale
window.MotivationalEmptyStates = MotivationalEmptyStates;
