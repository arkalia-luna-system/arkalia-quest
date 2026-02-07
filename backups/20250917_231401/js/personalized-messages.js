/* ===== ARKALIA QUEST - MESSAGES PERSONNALISÉS ===== */

class PersonalizedMessages {
    constructor() {
        this.userLevel = 1;
        this.userXP = 0;
        this.completedMissions = 0;
        this.badgesEarned = 0;
        this.init();
    }

    init() {
        this.loadUserData();
        this.setupMessageSystem();
        // Les messages personnalisés sont déjà ajoutés dans setupMessageSystem
        // console.log('✅ Messages personnalisés initialisés');
    }

    loadUserData() {
        // Simuler le chargement des données utilisateur
        // En réalité, cela viendrait de l'API
        this.userLevel = parseInt(localStorage.getItem('userLevel')) || 1;
        this.userXP = parseInt(localStorage.getItem('userXP')) || 0;
        this.completedMissions = parseInt(localStorage.getItem('completedMissions')) || 0;
        this.badgesEarned = parseInt(localStorage.getItem('badgesEarned')) || 0;
    }

    setupMessageSystem() {
        // Remplacer les messages génériques par des messages personnalisés
        this.replaceGenericMessages();
        this.addContextualMessages();
    }

    replaceGenericMessages() {
        // Messages d'accueil personnalisés
        const greetings = [
            `🌙 LUNA: Salut hacker ! Niveau ${this.userLevel}, ${this.userXP} XP. Prêt pour l'aventure ?`,
            `🌙 LUNA: Bienvenue de retour ! Tu as ${this.completedMissions} missions complétées. Continue !`,
            `🌙 LUNA: Hey ! ${this.badgesEarned} badges obtenus. Tu progresses bien !`,
            `🌙 LUNA: Salut ! Tu es niveau ${this.userLevel}. Prêt pour de nouveaux défis ?`
        ];

        const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
        this.updateLunaMessage(randomGreeting);

        // Messages de progression personnalisés
        this.updateProgressMessages();
    }

    updateLunaMessage(message) {
        const lunaElements = document.querySelectorAll('.luna-greeting, .luna-message');
        lunaElements.forEach(element => {
            if (element.textContent.includes('Bienvenue') || element.textContent.includes('LUNA:')) {
                element.innerHTML = message;
                element.classList.add('luna-notification');
            }
        });
    }

    updateProgressMessages() {
        // Messages de progression dans le profil
        const progressElements = document.querySelectorAll('.progress-message, .status-message');
        progressElements.forEach(element => {
            if (element.textContent.includes('Chargement') || element.textContent.includes('N/A')) {
                element.innerHTML = this.getPersonalizedProgressMessage();
            }
        });
    }

    getPersonalizedProgressMessage() {
        if (this.userLevel === 1 && this.userXP === 0) {
            return `🚀 Nouveau hacker détecté ! Commence par le tutoriel pour débloquer ton potentiel.`;
        } else if (this.userLevel < 5) {
            return `⚡ Tu progresses bien ! Niveau ${this.userLevel}, ${this.userXP} XP. Continue l'aventure !`;
        } else if (this.userLevel < 10) {
            return `🔥 Excellent travail ! Niveau ${this.userLevel}, tu deviens un vrai hacker !`;
        } else {
            return `👑 Maître hacker ! Niveau ${this.userLevel}, tu es une légende !`;
        }
    }

    addContextualMessages() {
        // Messages contextuels selon la page
        const currentPage = window.location.pathname;

        switch (currentPage) {
            case '/tutorial':
                this.addTutorialMessages();
                break;
            case '/terminal':
                this.addTerminalMessages();
                break;
            case '/monde':
                this.addWorldMessages();
                break;
            case '/profil':
                this.addProfileMessages();
                break;
            case '/dashboard':
                this.addDashboardMessages();
                break;
        }
    }

    addTutorialMessages() {
        const tutorialSteps = document.querySelectorAll('.tutorial-step');
        tutorialSteps.forEach((step, index) => {
            const stepNumber = index + 1;
            const personalizedText = this.getTutorialStepMessage(stepNumber);

            if (step.querySelector('.step-description')) {
                step.querySelector('.step-description').innerHTML = personalizedText;
            }
        });
    }

    getTutorialStepMessage(stepNumber) {
        const messages = {
            1: `🎯 Étape ${stepNumber}: Bienvenue ! Je suis LUNA, ton guide IA. Commençons par explorer l'interface.`,
            2: `⌨️ Étape ${stepNumber}: Voici le terminal. Tape "aide" pour voir les commandes disponibles.`,
            3: `🌍 Étape ${stepNumber}: Explore le monde d'Arkalia. Chaque zone cache des secrets !`,
            4: `👤 Étape ${stepNumber}: Ton profil suit ta progression. Plus tu joues, plus tu progresses !`,
            5: `🏆 Étape ${stepNumber}: Gagne des badges en complétant des missions. Collectionne-les tous !`
        };

        return messages[stepNumber] || `📚 Étape ${stepNumber}: Continue l'apprentissage !`;
    }

    addTerminalMessages() {
        const terminalOutput = document.getElementById('terminal-output');
        if (terminalOutput) {
            const personalizedWelcome = this.getTerminalWelcomeMessage();
            const welcomeElement = document.createElement('div');
            welcomeElement.className = 'terminal-message luna';
            welcomeElement.innerHTML = personalizedWelcome;
            terminalOutput.appendChild(welcomeElement);
        }
    }

    getTerminalWelcomeMessage() {
        const messages = [
            `🌙 LUNA: Terminal activé ! Niveau ${this.userLevel}, ${this.userXP} XP. Que veux-tu faire ?`,
            `🌙 LUNA: Système prêt ! ${this.completedMissions} missions complétées. Tape "aide" pour commencer.`,
            `🌙 LUNA: Interface chargée ! ${this.badgesEarned} badges obtenus. Prêt pour de nouveaux défis ?`
        ];

        return messages[Math.floor(Math.random() * messages.length)];
    }

    addWorldMessages() {
        const worldDescription = document.querySelector('.world-subtitle');
        if (worldDescription) {
            worldDescription.innerHTML = `Explore les zones mystérieuses d'Arkalia. Niveau ${this.userLevel}, tu peux accéder à ${this.getAvailableZones()} zones.`;
        }
    }

    getAvailableZones() {
        if (this.userLevel >= 5) return 'toutes les';
        if (this.userLevel >= 3) return 'la plupart des';
        return 'certaines';
    }

    addProfileMessages() {
        // Messages de motivation dans le profil
        const motivationSection = document.querySelector('.profile-motivation');
        if (!motivationSection) {
            this.createProfileMotivation();
        }
    }

    createProfileMotivation() {
        const profileContainer = document.querySelector('.profil-container, .profile-container');
        if (profileContainer) {
            const motivationDiv = document.createElement('div');
            motivationDiv.className = 'dashboard-motivation';
            motivationDiv.innerHTML = `
                <h3>🌟 Ton Progrès Hacker</h3>
                <p>Tu es niveau ${this.userLevel} avec ${this.userXP} XP. Continue l'aventure pour débloquer de nouveaux pouvoirs !</p>
                <div class="motivation-stats">
                    <div class="motivation-stat">
                        <div class="stat-icon">🎯</div>
                        <div class="stat-label">Missions</div>
                        <div class="stat-value">${this.completedMissions}</div>
                    </div>
                    <div class="motivation-stat">
                        <div class="stat-icon">🏆</div>
                        <div class="stat-label">Badges</div>
                        <div class="stat-value">${this.badgesEarned}</div>
                    </div>
                    <div class="motivation-stat">
                        <div class="stat-icon">⚡</div>
                        <div class="stat-label">Niveau</div>
                        <div class="stat-value">${this.userLevel}</div>
                    </div>
                </div>
            `;
            profileContainer.appendChild(motivationDiv);
        }
    }

    addDashboardMessages() {
        // Messages de motivation pour le dashboard
        const dashboardContainer = document.querySelector('.dashboard-container, .dashboard-grid');
        if (dashboardContainer) {
            const motivationDiv = document.createElement('div');
            motivationDiv.className = 'dashboard-motivation';
            motivationDiv.innerHTML = `
                <h3>🚀 Tableau de Bord Hacker</h3>
                <p>Bienvenue dans ton centre de contrôle ! Ici tu peux suivre ta progression et accéder à toutes les fonctionnalités.</p>
                <div class="motivation-stats">
                    <div class="motivation-stat">
                        <div class="stat-icon">📊</div>
                        <div class="stat-label">Statistiques</div>
                        <div class="stat-value">En cours</div>
                    </div>
                    <div class="motivation-stat">
                        <div class="stat-icon">🎮</div>
                        <div class="stat-label">Jeux</div>
                        <div class="stat-value">Disponibles</div>
                    </div>
                    <div class="motivation-stat">
                        <div class="stat-icon">🌙</div>
                        <div class="stat-label">LUNA</div>
                        <div class="stat-value">Active</div>
                    </div>
                </div>
            `;
            dashboardContainer.appendChild(motivationDiv);
        }
    }

    // Méthode pour mettre à jour les données utilisateur
    updateUserData(level, xp, missions, badges) {
        this.userLevel = level;
        this.userXP = xp;
        this.completedMissions = missions;
        this.badgesEarned = badges;

        // Sauvegarder dans localStorage
        localStorage.setItem('userLevel', level);
        localStorage.setItem('userXP', xp);
        localStorage.setItem('completedMissions', missions);
        localStorage.setItem('badgesEarned', badges);

        // Mettre à jour les messages
        this.replaceGenericMessages();
    }
}

// Classe pour les feedbacks d'accessibilité améliorés
class AccessibilityFeedback {
    constructor() {
        this.setupFeedbackSystem();
    }

    setupFeedbackSystem() {
        // Écouter les changements d'accessibilité
        document.addEventListener('change', (e) => {
            if (e.target.matches('input[type="checkbox"], select, input[type="range"]')) {
                this.showAccessibilityFeedback(e.target);
            }
        });
    }

    showAccessibilityFeedback(element) {
        const feedback = this.getAccessibilityFeedback(element);
        this.displayFeedback(feedback);
    }

    getAccessibilityFeedback(element) {
        const setting = element.name || element.id;
        const value = element.checked || element.value;

        const feedbacks = {
            'contrast': value ?
                '✅ Contraste renforcé activé ! Les textes sont maintenant plus visibles.' :
                'ℹ️ Contraste standard restauré.',
            'font-size': `📏 Taille de police ajustée à ${value}px.`,
            'dark-mode': value ?
                '🌙 Mode sombre activé ! Interface optimisée pour la nuit.' :
                '☀️ Mode clair activé ! Interface optimisée pour le jour.',
            'spacing': value ?
                '📐 Espacement augmenté ! Interface plus aérée.' :
                '📐 Espacement standard restauré.',
            'animations': value ?
                '🎬 Animations activées ! Interface plus dynamique.' :
                '⏸️ Animations désactivées pour une navigation plus calme.',
            'keyboard-nav': value ?
                '⌨️ Navigation clavier activée ! Utilise Tab pour naviguer.' :
                '🖱️ Navigation clavier désactivée.'
        };

        return feedbacks[setting] || '⚙️ Paramètre d\'accessibilité modifié.';
    }

    displayFeedback(message) {
        // Créer une notification de feedback
        const notification = document.createElement('div');
        notification.className = 'accessibility-feedback';
        notification.innerHTML = `
            <div class="feedback-icon">🔧</div>
            <div class="feedback-message">${message}</div>
        `;

        // Styles pour la notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.9), rgba(0, 255, 255, 0.8));
            color: var(--matrix-dark);
            padding: 15px 20px;
            border-radius: 10px;
            border: 2px solid var(--matrix-green);
            box-shadow: 0 8px 25px rgba(0, 255, 0, 0.4);
            z-index: 10000;
            font-weight: 600;
            animation: feedbackSlideIn 0.5s ease-out;
            max-width: 300px;
        `;

        document.body.appendChild(notification);

        // Supprimer après 3 secondes
        setTimeout(() => {
            notification.style.animation = 'feedbackSlideOut 0.3s ease-in forwards';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// CSS pour les animations de feedback
const feedbackStyles = document.createElement('style');
feedbackStyles.textContent = `
    @keyframes feedbackSlideIn {
        0% {
            transform: translateX(100%);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes feedbackSlideOut {
        0% {
            transform: translateX(0);
            opacity: 1;
        }
        100% {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(feedbackStyles);

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    new PersonalizedMessages();
    new AccessibilityFeedback();
});

// Export pour utilisation externe
window.PersonalizedMessages = PersonalizedMessages;
window.AccessibilityFeedback = AccessibilityFeedback;
