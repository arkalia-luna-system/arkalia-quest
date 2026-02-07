/* ===== ARKALIA QUEST - SMART EMPTY STATES ===== */
/* Système intelligent pour masquer les stats à zéro et afficher des placeholders motivants */

class SmartEmptyStates {
    constructor() {
        this.motivationalMessages = {
            badges: [
                "🎯 Tes premiers badges t'attendent !",
                "🏆 Commence l'aventure pour débloquer des récompenses !",
                "⭐ Chaque action compte pour ta légende !"
            ],
            missions: [
                "🚀 Prêt pour ta première mission ?",
                "🎮 L'aventure commence maintenant !",
                "💫 Tes exploits t'attendent !"
            ],
            coins: [
                "💰 Tes premiers coins arrivent bientôt !",
                "💎 L'aventure récompense les courageux !",
                "✨ Chaque victoire compte !"
            ],
            xp: [
                "⚡ Ton XP grandira avec l'aventure !",
                "🌟 Chaque action te rend plus fort !",
                "🔥 Prêt à monter en niveau ?"
            ],
            score: [
                "🎯 Ton score grandira avec tes exploits !",
                "🏆 Chaque victoire compte !",
                "⭐ L'aventure te récompensera !"
            ]
        };

        this.init();
    }

    init() {
        this.hideZeroStats();
        this.addMotivationalPlaceholders();
        this.enhanceEmptyWidgets();
        // console.log('🎯 Smart Empty States initialisé');
    }

    hideZeroStats() {
        // Masquer les stats à zéro
        const zeroStats = document.querySelectorAll('.metric-value, .stat-value, .badge-count, .mission-count, .coin-count, .xp-value');

        zeroStats.forEach(stat => {
            const value = stat.textContent.trim();
            if (value === '0' || value === 'N/A' || value === '') {
                const container = stat.closest('.widget, .metric, .stat-card, .badge-widget, .mission-widget');
                if (container) {
                    container.style.display = 'none';
                }
            }
        });
    }

    addMotivationalPlaceholders() {
        // Ajouter des placeholders motivants pour les sections vides
        this.createMotivationalWidget('badges', '🏆 MES BADGES', this.getRandomMessage('badges'));
        this.createMotivationalWidget('missions', '🎯 MES MISSIONS', this.getRandomMessage('missions'));
        this.createMotivationalWidget('coins', '💰 MES COINS', this.getRandomMessage('coins'));
        this.createMotivationalWidget('xp', '⚡ MON XP', this.getRandomMessage('xp'));
        this.createMotivationalWidget('score', '🎯 MON SCORE', this.getRandomMessage('score'));
    }

    createMotivationalWidget(type, title, message) {
        // Vérifier si le widget existe déjà
        const existingWidget = document.querySelector(`[data-widget-type="${type}"]`);
        if (existingWidget) return;

        // Vérifier si la section parent existe
        const parentSection = document.querySelector('.dashboard-grid, .profile-stats, .leaderboard-stats');
        if (!parentSection) return;

        const widget = document.createElement('div');
        widget.className = 'motivational-widget';
        widget.setAttribute('data-widget-type', type);

        widget.innerHTML = `
            <div class="motivational-content">
                <div class="motivational-icon">${this.getIconForType(type)}</div>
                <h3 class="motivational-title">${title}</h3>
                <p class="motivational-message">${message}</p>
                <a href="/terminal" class="cta-motivational">🚀 COMMENCER L'AVENTURE</a>
            </div>
        `;

        parentSection.appendChild(widget);
    }

    getIconForType(type) {
        const icons = {
            badges: '🏆',
            missions: '🎯',
            coins: '💰',
            xp: '⚡',
            score: '🎯'
        };
        return icons[type] || '🌟';
    }

    getRandomMessage(type) {
        const messages = this.motivationalMessages[type] || this.motivationalMessages.score;
        return messages[Math.floor(Math.random() * messages.length)];
    }

    enhanceEmptyWidgets() {
        // Améliorer les widgets vides existants
        const emptyWidgets = document.querySelectorAll('.widget:empty, .metric:empty, .stat-card:empty');

        emptyWidgets.forEach(widget => {
            widget.innerHTML = `
                <div class="empty-widget-content">
                    <span class="empty-icon">🌟</span>
                    <p class="empty-message">Commence l'aventure pour remplir cette section !</p>
                </div>
            `;
        });
    }

    // Méthode pour afficher un widget quand une stat devient > 0
    showWidgetWhenReady(type, value) {
        if (value > 0) {
            const motivationalWidget = document.querySelector(`[data-widget-type="${type}"]`);
            if (motivationalWidget) {
                motivationalWidget.style.display = 'none';
            }

            // Afficher le widget réel
            const realWidget = document.querySelector(`[data-real-widget="${type}"]`);
            if (realWidget) {
                realWidget.style.display = 'block';
            }
        }
    }
}

// Initialiser le système
document.addEventListener('DOMContentLoaded', () => {
    window.smartEmptyStates = new SmartEmptyStates();
});

// Exporter pour utilisation globale
window.SmartEmptyStates = SmartEmptyStates;
