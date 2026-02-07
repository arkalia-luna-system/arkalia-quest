/* ===== ARKALIA QUEST - MOTIVATIONAL EMPTY STATES ===== */
/* Système d'états vides motivants pour encourager l'engagement */

class MotivationalEmptyStates {
    constructor() {
        this.messages = {
            no_missions: [
                "🎯 Aucune mission en cours... C'est le moment parfait pour en commencer une nouvelle !",
                "🌟 Prêt pour une nouvelle aventure ? Découvre les missions disponibles !",
                "🚀 L'espace est vide, mais plein de possibilités ! Explore les défis qui t'attendent."
            ],
            no_achievements: [
                "🏆 Tes succès arrivent ! Continue à jouer pour débloquer de nouveaux badges.",
                "⭐ Chaque action compte ! Tes achievements se construisent au fil du temps.",
                "🎖️ La route vers la gloire commence par un premier pas. Continue !"
            ],
            no_friends: [
                "👥 L'aventure est plus belle à plusieurs ! Invite des amis à rejoindre Arkalia.",
                "🤝 Trouve ta tribu ! Les hackers solitaires deviennent des légendes ensemble.",
                "🌟 Partage l'expérience ! Montre à tes amis le monde de LUNA."
            ],
            empty_inventory: [
                "🎒 Ton inventaire est vide... Parfait pour le remplir de trésors !",
                "💎 L'espace attend d'être rempli de découvertes extraordinaires !",
                "🔍 Explore plus pour découvrir des objets uniques et rares."
            ]
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createStyles();
        // console.log('🌟 Motivational Empty States initialisé');
    }

    setupEventListeners() {
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

        // Vérifier au chargement initial
        document.addEventListener('DOMContentLoaded', () => {
            this.checkForEmptyStates();
        });
    }

    createStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .motivational-empty-state {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
                border: 2px dashed rgba(139, 92, 246, 0.3);
                border-radius: 1rem;
                margin: 1rem 0;
                position: relative;
                overflow: hidden;
            }

            .motivational-empty-state::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.1), transparent);
                animation: motivationalShine 3s ease-in-out infinite;
            }

            @keyframes motivationalShine {
                0% { left: -100%; }
                50% { left: 100%; }
                100% { left: 100%; }
            }

            .motivational-message {
                font-size: 1.1rem;
                color: var(--luna-text);
                margin-bottom: 1rem;
                font-weight: 500;
            }

            .motivational-icon {
                font-size: 3rem;
                margin-bottom: 1rem;
                display: block;
                animation: motivationalPulse 2s ease-in-out infinite;
            }

            @keyframes motivationalPulse {
                0%, 100% { transform: scale(1); opacity: 0.8; }
                50% { transform: scale(1.1); opacity: 1; }
            }

            .motivational-action {
                background: linear-gradient(135deg, var(--luna-violet), var(--luna-cyan));
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 0.5rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }

            .motivational-action:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
            }
        `;
        document.head.appendChild(style);
    }

    checkForEmptyStates() {
        // Vérifier les missions
        this.checkMissionsEmpty();

        // Vérifier les achievements
        this.checkAchievementsEmpty();

        // Vérifier les amis
        this.checkFriendsEmpty();

        // Vérifier l'inventaire
        this.checkInventoryEmpty();
    }

    checkMissionsEmpty() {
        const missionsContainer = document.querySelector('.missions-container, .missions-list, #missions');
        if (missionsContainer && missionsContainer.children.length === 0) {
            this.showMotivationalState(missionsContainer, 'no_missions', '🎯', 'Découvrir les missions');
        }
    }

    checkAchievementsEmpty() {
        const achievementsContainer = document.querySelector('.achievements-container, .badges-list, #achievements');
        if (achievementsContainer && achievementsContainer.children.length === 0) {
            this.showMotivationalState(achievementsContainer, 'no_achievements', '🏆', 'Voir les défis');
        }
    }

    checkFriendsEmpty() {
        const friendsContainer = document.querySelector('.friends-container, .friends-list, #friends');
        if (friendsContainer && friendsContainer.children.length === 0) {
            this.showMotivationalState(friendsContainer, 'no_friends', '👥', 'Inviter des amis');
        }
    }

    checkInventoryEmpty() {
        const inventoryContainer = document.querySelector('.inventory-container, .items-list, #inventory');
        if (inventoryContainer && inventoryContainer.children.length === 0) {
            this.showMotivationalState(inventoryContainer, 'empty_inventory', '🎒', 'Explorer');
        }
    }

    showMotivationalState(container, type, icon, actionText) {
        // Vérifier si un état motivant existe déjà
        if (container.querySelector('.motivational-empty-state')) {
            return;
        }

        const message = this.getRandomMessage(type);
        const motivationalState = document.createElement('div');
        motivationalState.className = 'motivational-empty-state';
        motivationalState.innerHTML = `
            <span class="motivational-icon">${icon}</span>
            <div class="motivational-message">${message}</div>
            <button class="motivational-action" onclick="this.parentElement.remove()">${actionText}</button>
        `;

        container.appendChild(motivationalState);

        // Auto-suppression après 10 secondes
        setTimeout(() => {
            if (motivationalState.parentElement) {
                motivationalState.remove();
            }
        }, 10000);
    }

    getRandomMessage(type) {
        const messages = this.messages[type] || ['🌟 Continue ton aventure !'];
        return messages[Math.floor(Math.random() * messages.length)];
    }

    initializeEmptyStateMessages() {
        // Initialiser les messages d'états vides
        this.messages = {
            no_missions: [
                "🎯 Aucune mission en cours... C'est le moment parfait pour en commencer une nouvelle !",
                "🌟 Prêt pour une nouvelle aventure ? Découvre les missions disponibles !",
                "🚀 L'espace est vide, mais plein de possibilités ! Explore les défis qui t'attendent."
            ],
            no_achievements: [
                "🏆 Tes succès arrivent ! Continue à jouer pour débloquer de nouveaux badges.",
                "⭐ Chaque action compte ! Tes achievements se construisent au fil du temps.",
                "🎖️ La route vers la gloire commence par un premier pas. Continue !"
            ],
            no_friends: [
                "👥 L'aventure est plus belle à plusieurs ! Invite des amis à rejoindre Arkalia.",
                "🤝 Trouve ta tribu ! Les hackers solitaires deviennent des légendes ensemble.",
                "🌟 Partage l'expérience ! Montre à tes amis le monde de LUNA."
            ],
            empty_inventory: [
                "🎒 Ton inventaire est vide... Parfait pour le remplir de trésors !",
                "💎 L'espace attend d'être rempli de découvertes extraordinaires !",
                "🔍 Explore plus pour découvrir des objets uniques et rares."
            ]
        };
    }

    // Méthode publique pour forcer l'affichage d'un état motivant
    showCustomEmptyState(container, message, icon = '🌟', actionText = 'Continuer') {
        const motivationalState = document.createElement('div');
        motivationalState.className = 'motivational-empty-state';
        motivationalState.innerHTML = `
            <span class="motivational-icon">${icon}</span>
            <div class="motivational-message">${message}</div>
            <button class="motivational-action" onclick="this.parentElement.remove()">${actionText}</button>
        `;

        container.appendChild(motivationalState);
    }

    // Alias pour la compatibilité avec les tests
    showEmptyStateMessage(container, message, icon = '🌟', actionText = 'Continuer') {
        this.showCustomEmptyState(container, message, icon, actionText);
    }
}

// Initialiser le système
document.addEventListener('DOMContentLoaded', () => {
    window.motivationalEmptyStates = new MotivationalEmptyStates();
});

// Exporter pour utilisation globale
window.MotivationalEmptyStates = MotivationalEmptyStates;
