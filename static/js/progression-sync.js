/* ===== ARKALIA QUEST - PROGRESSION SYNC SYSTEM ===== */
/* Système de synchronisation automatique des données de progression */

class ProgressionSync {
    constructor() {
        this.updateInterval = 5000; // Mise à jour toutes les 5 secondes
        this.lastUpdate = 0;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.startAutoSync();
        // console.log('🔄 Progression Sync System initialisé');
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('arkalia:progression:synced', (e) => {
            this.updateAllModules(e.detail);
        });

        // Écouter les événements de mise à jour UI
        document.addEventListener('arkalia:ui:update-progression', (e) => {
            this.updateAllModules(e.detail);
        });

        // Synchroniser au chargement de la page
        document.addEventListener('DOMContentLoaded', () => {
            this.syncProgression();
        });
    }

    startAutoSync() {
        setInterval(() => {
            this.syncProgression();
        }, this.updateInterval);
    }

    async syncProgression() {
        try {
            const response = await fetch('/api/progression-data');
            const data = await response.json();

            if (data.success) {
                this.updateAllModules(data.progression);
                this.lastUpdate = Date.now();
            }
        } catch (error) {
            // console.log('Erreur synchronisation progression:', error);
        }
    }

    updateAllModules(progressionData) {
        // Mettre à jour le dashboard
        this.updateDashboard(progressionData);

        // Mettre à jour le profil
        this.updateProfile(progressionData);

        // Mettre à jour le leaderboard
        this.updateLeaderboard(progressionData);

        // Mettre à jour l'arbre de compétences
        this.updateSkillTree(progressionData);

        // Mettre à jour les missions
        this.updateMissions(progressionData);
    }

    updateDashboard(progressionData) {
        if (!progressionData || typeof progressionData !== 'object') return;
        const levelElement = document.querySelector('.player-level, .level-value, #player-level');
        if (levelElement) {
            levelElement.textContent = progressionData.level ?? 1;
        }

        const xpElement = document.querySelector('.player-xp, .xp-value, #player-xp');
        if (xpElement) {
            xpElement.textContent = progressionData.xp ?? 0;
        }

        const scoreElement = document.querySelector('.player-score, .score-value, #player-score');
        if (scoreElement) {
            scoreElement.textContent = progressionData.score ?? 0;
        }

        const coinsElement = document.querySelector('.player-coins, .coins-value, #player-coins');
        if (coinsElement) {
            coinsElement.textContent = progressionData.coins ?? 0;
        }

        const badgesContainer = document.querySelector('.badges-container, .player-badges, #player-badges');
        if (badgesContainer && Array.isArray(progressionData.badges)) {
            const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
            badgesContainer.innerHTML = progressionData.badges.map(badge =>
                `<span class="badge">${badge != null ? esc(badge) : ''}</span>`
            ).join('');
        }

        if (progressionData.stats) {
            this.updateStats(progressionData.stats);
        }
    }

    updateProfile(progressionData) {
        if (!progressionData || typeof progressionData !== 'object') return;
        const profileElements = {
            'level': progressionData.level ?? 1,
            'xp': progressionData.xp ?? 0,
            'score': progressionData.score ?? 0,
            'coins': progressionData.coins ?? 0,
            'badges': Array.isArray(progressionData.badges) ? progressionData.badges.length : 0,
            'missions': Array.isArray(progressionData.missions_completed) ? progressionData.missions_completed.length : 0
        };

        Object.entries(profileElements).forEach(([key, value]) => {
            const elements = document.querySelectorAll(`[data-stat="${key}"], .${key}-value, #${key}-value`);
            elements.forEach(el => {
                el.textContent = value;
            });
        });
    }

    updateLeaderboard(progressionData) {
        // Mettre à jour le leaderboard si nécessaire
        const leaderboardContainer = document.querySelector('.leaderboard-container, #leaderboard');
        if (leaderboardContainer) {
            // Déclencher une mise à jour du leaderboard
            const event = new CustomEvent('arkalia:leaderboard:update');
            document.dispatchEvent(event);
        }
    }

    updateSkillTree(progressionData) {
        // Mettre à jour l'arbre de compétences
        if (progressionData.skills) {
            const event = new CustomEvent('arkalia:skill-tree:update', {
                detail: progressionData.skills
            });
            document.dispatchEvent(event);
        }
    }

    updateMissions(progressionData) {
        // Mettre à jour les missions
        const missionsContainer = document.querySelector('.missions-container, #missions');
        if (missionsContainer) {
            const event = new CustomEvent('arkalia:missions:update', {
                detail: progressionData
            });
            document.dispatchEvent(event);
        }
    }

    updateStats(stats) {
        if (!stats) return;

        const statsElements = {
            'total_commands': stats.total_commands || 0,
            'total_luna_commands': stats.total_luna_commands || 0,
            'total_zones_explored': stats.total_zones_explored || 0,
            'total_mini_games': stats.total_mini_games || 0
        };

        Object.entries(statsElements).forEach(([key, value]) => {
            const elements = document.querySelectorAll(`[data-stat="${key}"], .${key}-value, #${key}-value`);
            elements.forEach(el => {
                el.textContent = value;
            });
        });
    }

    // Méthode pour forcer une synchronisation
    forceSync() {
        this.syncProgression();
    }

    // Méthode pour obtenir les données actuelles
    async getCurrentProgression() {
        try {
            const response = await fetch('/api/progression-data');
            const data = await response.json();
            return data.success ? data.progression : null;
        } catch (error) {
            console.error('Erreur récupération progression:', error);
            return null;
        }
    }
}

// Initialiser le système de synchronisation
const progressionSync = new ProgressionSync();

// Exposer globalement pour utilisation dans d'autres scripts
window.progressionSync = progressionSync;
