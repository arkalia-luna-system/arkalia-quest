/* ===== ARKALIA QUEST - UNIVERSAL EMPTY STATES SYSTEM ===== */
/* Système unifié pour tous les états vides, placeholders et messages motivants */

class UniversalEmptyStates {
    constructor() {
        this.emptyStates = new Map();
        this.observers = new Map();
        this.settings = this.loadSettings();
        this.init();
    }

    init() {
        this.setupGlobalStyles();
        this.setupIntersectionObserver();
        this.setupEventListeners();
        // console.log('🌟 Universal Empty States System initialisé');
    }

    loadSettings() {
        const defaultSettings = {
            animationDuration: 300,
            autoDetect: true,
            showMotivationalMessages: true,
            theme: 'arkalia',
            position: 'center',
            maxEmptyStates: 5,
            fadeInDelay: 100
        };

        try {
            const saved = localStorage.getItem('arkalia_empty_states_settings');
            return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
        } catch {
            return defaultSettings;
        }
    }

    setupGlobalStyles() {
        if (document.getElementById('universal-empty-states-styles')) return;

        const style = document.createElement('style');
        style.id = 'universal-empty-states-styles';
        style.textContent = `
            .universal-empty-state {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 40px 20px;
                min-height: 200px;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .universal-empty-state.show {
                opacity: 1;
                transform: translateY(0);
            }

            .universal-empty-state-icon {
                font-size: 4em;
                margin-bottom: 20px;
                animation: emptyStateFloat 3s ease-in-out infinite;
                filter: drop-shadow(0 0 20px rgba(167, 139, 250, 0.3));
            }

            @keyframes emptyStateFloat {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }

            .universal-empty-state-title {
                font-family: 'Cormorant', serif;
                font-size: 1.8em;
                font-weight: 600;
                color: var(--violet-lunaire);
                margin-bottom: 12px;
                text-shadow: 0 0 10px rgba(167, 139, 250, 0.5);
            }

            .universal-empty-state-description {
                font-family: 'Inter', sans-serif;
                font-size: 1.1em;
                color: var(--argent-holographique);
                line-height: 1.6;
                margin-bottom: 24px;
                max-width: 400px;
            }

            .universal-empty-state-actions {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
                justify-content: center;
            }

            .universal-empty-state-btn {
                padding: 12px 24px;
                border: 2px solid rgba(167, 139, 250, 0.4);
                border-radius: 8px;
                background: rgba(167, 139, 250, 0.1);
                color: var(--argent-holographique);
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.95em;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }

            .universal-empty-state-btn:hover {
                background: rgba(167, 139, 250, 0.3);
                border-color: var(--violet-lunaire);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(167, 139, 250, 0.3);
            }

            .universal-empty-state-btn.primary {
                background: linear-gradient(135deg, var(--violet-lunaire), var(--bleu-spectre));
                color: #000;
                border-color: var(--violet-lunaire);
            }

            .universal-empty-state-btn.primary:hover {
                background: linear-gradient(135deg, var(--bleu-spectre), var(--violet-lunaire));
                transform: translateY(-2px) scale(1.05);
            }

            .universal-empty-state-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
                transform: scaleX(0);
                transform-origin: left;
                transition: transform 0.3s ease;
            }

            .universal-empty-state-progress.animate {
                transform: scaleX(1);
            }

            .universal-empty-state-particles {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                pointer-events: none;
                overflow: hidden;
            }

            .universal-empty-state-particle {
                position: absolute;
                width: 4px;
                height: 4px;
                background: var(--violet-lunaire);
                border-radius: 50%;
                opacity: 0.6;
                animation: particleFloat 4s ease-in-out infinite;
            }

            @keyframes particleFloat {
                0%, 100% {
                    transform: translateY(0) translateX(0);
                    opacity: 0;
                }
                50% {
                    opacity: 0.6;
                }
                100% {
                    transform: translateY(-100px) translateX(50px);
                    opacity: 0;
                }
            }

            /* Types d'empty states */
            .universal-empty-state.stats {
                background: linear-gradient(135deg, rgba(167, 139, 250, 0.05), rgba(96, 165, 250, 0.05));
                border: 2px dashed rgba(167, 139, 250, 0.3);
                border-radius: 12px;
            }

            .universal-empty-state.missions {
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.05), rgba(167, 139, 250, 0.05));
                border: 2px dashed rgba(34, 197, 94, 0.3);
                border-radius: 12px;
            }

            .universal-empty-state.zones {
                background: linear-gradient(135deg, rgba(96, 165, 250, 0.05), rgba(167, 139, 250, 0.05));
                border: 2px dashed rgba(96, 165, 250, 0.3);
                border-radius: 12px;
            }

            .universal-empty-state.social {
                background: linear-gradient(135deg, rgba(251, 191, 36, 0.05), rgba(167, 139, 250, 0.05));
                border: 2px dashed rgba(251, 191, 36, 0.3);
                border-radius: 12px;
            }

            .universal-empty-state.minigames {
                background: linear-gradient(135deg, rgba(236, 72, 153, 0.05), rgba(167, 139, 250, 0.05));
                border: 2px dashed rgba(236, 72, 153, 0.3);
                border-radius: 12px;
            }

            .universal-empty-state.themes {
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.05), rgba(167, 139, 250, 0.05));
                border: 2px dashed rgba(139, 92, 246, 0.3);
                border-radius: 12px;
            }

            .universal-empty-state.leaderboard {
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.05), rgba(167, 139, 250, 0.05));
                border: 2px dashed rgba(245, 158, 11, 0.3);
                border-radius: 12px;
            }

            .universal-empty-state.achievements {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(167, 139, 250, 0.05));
                border: 2px dashed rgba(16, 185, 129, 0.3);
                border-radius: 12px;
            }

            /* Thèmes */
            .universal-empty-state.matrix {
                background: linear-gradient(135deg, rgba(0, 255, 0, 0.05), rgba(0, 0, 0, 0.1));
                border-color: rgba(0, 255, 0, 0.3);
                color: #00ff00;
            }

            .universal-empty-state.cyberpunk {
                background: linear-gradient(135deg, rgba(255, 0, 255, 0.05), rgba(20, 0, 40, 0.1));
                border-color: rgba(255, 0, 255, 0.3);
                color: #ff00ff;
            }

            .universal-empty-state.ocean {
                background: linear-gradient(135deg, rgba(0, 191, 255, 0.05), rgba(0, 100, 200, 0.1));
                border-color: rgba(0, 191, 255, 0.3);
                color: #00bfff;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .universal-empty-state {
                    padding: 30px 15px;
                    min-height: 150px;
                }

                .universal-empty-state-icon {
                    font-size: 3em;
                    margin-bottom: 15px;
                }

                .universal-empty-state-title {
                    font-size: 1.5em;
                }

                .universal-empty-state-description {
                    font-size: 1em;
                    margin-bottom: 20px;
                }

                .universal-empty-state-actions {
                    flex-direction: column;
                    align-items: center;
                }

                .universal-empty-state-btn {
                    width: 100%;
                    max-width: 200px;
                }
            }

            /* Animations d'apparition */
            @keyframes emptyStateSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(30px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            @keyframes emptyStateFadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }

            .universal-empty-state.slide-in {
                animation: emptyStateSlideIn 0.5s ease-out;
            }

            .universal-empty-state.fade-in {
                animation: emptyStateFadeIn 0.4s ease-out;
            }
        `;
        document.head.appendChild(style);
    }

    setupIntersectionObserver() {
        if (!window.IntersectionObserver) return;

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateEmptyState(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });
    }

    setupEventListeners() {
        // Détecter les changements de contenu
        if (window.MutationObserver) {
            this.mutationObserver = new MutationObserver((mutations) => {
                mutations.forEach(mutation => {
                    if (mutation.type === 'childList') {
                        this.checkForEmptyStates();
                    }
                });
            });
        }
    }

    // Méthodes principales
    showEmptyState(container, type, config = {}) {
        const emptyStateConfig = {
            type: type || 'default',
            title: config.title || this.getDefaultTitle(type),
            description: config.description || this.getDefaultDescription(type),
            icon: config.icon || this.getDefaultIcon(type),
            actions: config.actions || this.getDefaultActions(type),
            theme: config.theme || this.settings.theme,
            animation: config.animation || 'slide-in',
            showParticles: config.showParticles !== false,
            showProgress: config.showProgress !== false,
            ...config
        };

        // Supprimer l'ancien empty state s'il existe
        this.removeEmptyState(container);

        // Créer le nouvel empty state
        const emptyState = this.createEmptyState(emptyStateConfig);
        container.appendChild(emptyState);

        // Stocker la référence
        this.emptyStates.set(container, { element: emptyState, config: emptyStateConfig });

        // Observer pour l'animation
        if (this.observer) {
            this.observer.observe(emptyState);
        }

        return emptyState;
    }

    createEmptyState(config) {
        const emptyState = document.createElement('div');
        emptyState.className = `universal-empty-state ${config.type} ${config.theme} ${config.animation}`;
        emptyState.setAttribute('data-empty-state-type', config.type);

        emptyState.innerHTML = `
            <div class="universal-empty-state-particles">
                ${config.showParticles ? this.generateParticles() : ''}
            </div>
            <div class="universal-empty-state-icon">${config.icon}</div>
            <div class="universal-empty-state-title">${config.title}</div>
            <div class="universal-empty-state-description">${config.description}</div>
            ${config.actions.length > 0 ? `
                <div class="universal-empty-state-actions">
                    ${config.actions.map(action => `
                        <button class="universal-empty-state-btn ${action.primary ? 'primary' : ''}" 
                                data-action="${action.id}">
                            ${action.icon ? `<span>${action.icon}</span>` : ''}
                            ${action.label}
                        </button>
                    `).join('')}
                </div>
            ` : ''}
            ${config.showProgress ? '<div class="universal-empty-state-progress"></div>' : ''}
        `;

        // Ajouter les événements des actions
        config.actions.forEach(action => {
            const btn = emptyState.querySelector(`[data-action="${action.id}"]`);
            if (btn) {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (action.handler) {
                        action.handler(config);
                    }
                    if (action.close !== false) {
                        this.removeEmptyState(emptyState.parentElement);
                    }
                });
            }
        });

        return emptyState;
    }

    animateEmptyState(element) {
        if (!element.classList.contains('show')) {
            element.classList.add('show');

            // Animer la barre de progression
            const progressBar = element.querySelector('.universal-empty-state-progress');
            if (progressBar) {
                setTimeout(() => {
                    progressBar.classList.add('animate');
                }, 200);
            }
        }
    }

    removeEmptyState(container) {
        const emptyStateData = this.emptyStates.get(container);
        if (emptyStateData) {
            emptyStateData.element.remove();
            this.emptyStates.delete(container);
        }
    }

    checkForEmptyStates() {
        if (!this.settings.autoDetect) return;

        const containers = document.querySelectorAll('[data-empty-state]');
        containers.forEach(container => {
            const isEmpty = this.isContainerEmpty(container);
            const hasEmptyState = this.emptyStates.has(container);

            if (isEmpty && !hasEmptyState) {
                const type = container.dataset.emptyState || 'default';
                this.showEmptyState(container, type);
            } else if (!isEmpty && hasEmptyState) {
                this.removeEmptyState(container);
            }
        });
    }

    isContainerEmpty(container) {
        const children = Array.from(container.children);
        return children.length === 0 ||
            children.every(child =>
                child.classList.contains('universal-empty-state') ||
                child.textContent.trim() === '' ||
                child.textContent.trim() === '0' ||
                child.textContent.trim() === '--'
            );
    }

    generateParticles() {
        const particleCount = 8;
        let particles = '';

        for (let i = 0; i < particleCount; i++) {
            const delay = Math.random() * 2;
            const duration = 3 + Math.random() * 2;
            const left = Math.random() * 100;

            particles += `
                <div class="universal-empty-state-particle" 
                     style="left: ${left}%; animation-delay: ${delay}s; animation-duration: ${duration}s;"></div>
            `;
        }

        return particles;
    }

    // Méthodes utilitaires pour les types courants
    showStatsEmpty(container, config = {}) {
        return this.showEmptyState(container, 'stats', {
            title: '📊 Aucune statistique disponible',
            description: 'Commence à jouer pour voir tes statistiques apparaître ici !',
            icon: '📊',
            actions: [
                {
                    id: 'play',
                    label: 'Commencer à jouer',
                    icon: '🎮',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('🎮', 'Redirection vers le jeu...');
                        }
                    }
                }
            ],
            ...config
        });
    }

    showMissionsEmpty(container, config = {}) {
        return this.showEmptyState(container, 'missions', {
            title: '🎯 Aucune mission active',
            description: 'Découvre de nouvelles missions et défis pour progresser !',
            icon: '🎯',
            actions: [
                {
                    id: 'explore',
                    label: 'Explorer les missions',
                    icon: '🔍',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('🔍', 'Ouverture des missions...');
                        }
                    }
                }
            ],
            ...config
        });
    }

    showZonesEmpty(container, config = {}) {
        return this.showEmptyState(container, 'zones', {
            title: '🗺️ Aucune zone découverte',
            description: 'Explore le monde d\'Arkalia pour débloquer de nouvelles zones !',
            icon: '🗺️',
            actions: [
                {
                    id: 'explore',
                    label: 'Explorer le monde',
                    icon: '🌍',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('🌍', 'Ouverture de la carte...');
                        }
                    }
                }
            ],
            ...config
        });
    }

    showSocialEmpty(container, config = {}) {
        return this.showEmptyState(container, 'social', {
            title: '👥 Aucune activité sociale',
            description: 'Connecte-toi avec d\'autres joueurs et partage tes exploits !',
            icon: '👥',
            actions: [
                {
                    id: 'connect',
                    label: 'Se connecter',
                    icon: '🔗',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('🔗', 'Ouverture du social...');
                        }
                    }
                }
            ],
            ...config
        });
    }

    showMinigamesEmpty(container, config = {}) {
        return this.showEmptyState(container, 'minigames', {
            title: '🎮 Aucun mini-jeu disponible',
            description: 'Débloque de nouveaux mini-jeux en progressant dans l\'aventure !',
            icon: '🎮',
            actions: [
                {
                    id: 'play',
                    label: 'Jouer maintenant',
                    icon: '▶️',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('▶️', 'Lancement des mini-jeux...');
                        }
                    }
                }
            ],
            ...config
        });
    }

    showThemesEmpty(container, config = {}) {
        return this.showEmptyState(container, 'themes', {
            title: '🎨 Aucun thème personnalisé',
            description: 'Personnalise ton expérience avec des thèmes uniques !',
            icon: '🎨',
            actions: [
                {
                    id: 'customize',
                    label: 'Personnaliser',
                    icon: '⚙️',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('⚙️', 'Ouverture des paramètres...');
                        }
                    }
                }
            ],
            ...config
        });
    }

    showLeaderboardEmpty(container, config = {}) {
        return this.showEmptyState(container, 'leaderboard', {
            title: '🏆 Classement vide',
            description: 'Sois le premier à apparaître dans le classement !',
            icon: '🏆',
            actions: [
                {
                    id: 'compete',
                    label: 'Relever le défi',
                    icon: '⚡',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('⚡', 'C\'est parti pour la compétition !');
                        }
                    }
                }
            ],
            ...config
        });
    }

    showAchievementsEmpty(container, config = {}) {
        return this.showEmptyState(container, 'achievements', {
            title: '🏅 Aucun achievement',
            description: 'Accomplis des exploits pour débloquer tes premiers achievements !',
            icon: '🏅',
            actions: [
                {
                    id: 'achieve',
                    label: 'Voir les défis',
                    icon: '🎯',
                    primary: true,
                    handler: () => {
                        if (window.universalNotifications) {
                            window.universalNotifications.info('🎯', 'Ouverture des achievements...');
                        }
                    }
                }
            ],
            ...config
        });
    }

    // Méthodes de configuration
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        localStorage.setItem('arkalia_empty_states_settings', JSON.stringify(this.settings));
    }

    getSettings() {
        return { ...this.settings };
    }

    // Méthodes de debug
    getActiveEmptyStates() {
        return Array.from(this.emptyStates.keys());
    }

    clearAllEmptyStates() {
        this.emptyStates.forEach((data, container) => {
            this.removeEmptyState(container);
        });
    }

    // Méthodes utilitaires
    getDefaultTitle(type) {
        const titles = {
            stats: '📊 Aucune donnée',
            missions: '🎯 Aucune mission',
            zones: '🗺️ Aucune zone',
            social: '👥 Aucune activité',
            minigames: '🎮 Aucun jeu',
            themes: '🎨 Aucun thème',
            leaderboard: '🏆 Classement vide',
            achievements: '🏅 Aucun achievement',
            default: '📭 Aucun contenu'
        };
        return titles[type] || titles.default;
    }

    getDefaultDescription(type) {
        const descriptions = {
            stats: 'Les statistiques apparaîtront ici une fois que tu auras commencé à jouer.',
            missions: 'Découvre de nouvelles missions pour progresser dans l\'aventure.',
            zones: 'Explore le monde pour débloquer de nouvelles zones à découvrir.',
            social: 'Connecte-toi avec d\'autres joueurs pour partager ton expérience.',
            minigames: 'Débloque de nouveaux mini-jeux en progressant dans l\'histoire.',
            themes: 'Personnalise ton interface avec des thèmes uniques et colorés.',
            leaderboard: 'Sois le premier à apparaître dans le classement des joueurs.',
            achievements: 'Accomplis des exploits pour débloquer tes premiers achievements.',
            default: 'Le contenu apparaîtra ici une fois disponible.'
        };
        return descriptions[type] || descriptions.default;
    }

    getDefaultIcon(type) {
        const icons = {
            stats: '📊',
            missions: '🎯',
            zones: '🗺️',
            social: '👥',
            minigames: '🎮',
            themes: '🎨',
            leaderboard: '🏆',
            achievements: '🏅',
            default: '📭'
        };
        return icons[type] || icons.default;
    }

    getDefaultActions(type) {
        const actions = {
            stats: [
                { id: 'play', label: 'Commencer à jouer', icon: '🎮', primary: true }
            ],
            missions: [
                { id: 'explore', label: 'Explorer les missions', icon: '🔍', primary: true }
            ],
            zones: [
                { id: 'explore', label: 'Explorer le monde', icon: '🌍', primary: true }
            ],
            social: [
                { id: 'connect', label: 'Se connecter', icon: '🔗', primary: true }
            ],
            minigames: [
                { id: 'play', label: 'Jouer maintenant', icon: '▶️', primary: true }
            ],
            themes: [
                { id: 'customize', label: 'Personnaliser', icon: '⚙️', primary: true }
            ],
            leaderboard: [
                { id: 'compete', label: 'Relever le défi', icon: '⚡', primary: true }
            ],
            achievements: [
                { id: 'achieve', label: 'Voir les défis', icon: '🎯', primary: true }
            ],
            default: [
                { id: 'refresh', label: 'Actualiser', icon: '🔄', primary: true }
            ]
        };
        return actions[type] || actions.default;
    }
}

// Initialiser le système universel
document.addEventListener('DOMContentLoaded', () => {
    window.universalEmptyStates = new UniversalEmptyStates();

    // Démarrer la détection automatique
    setTimeout(() => {
        window.universalEmptyStates.checkForEmptyStates();
    }, 1000);

    // console.log('🌟 Universal Empty States System prêt');
});

// Exporter pour utilisation globale
window.UniversalEmptyStates = UniversalEmptyStates;
