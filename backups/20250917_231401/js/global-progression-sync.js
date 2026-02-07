/* ===== ARKALIA QUEST - GLOBAL PROGRESSION SYNC ===== */
/* Système de synchronisation des données de progression entre toutes les pages */

class GlobalProgressionSync {
    constructor() {
        this.progressionData = null;
        this.updateInterval = null;
        this.lastUpdate = 0;
        this.updateFrequency = 5000; // 5 secondes
        this.isUpdating = false;
        this.callbacks = new Set();
        this.cache = new Map();
        this.init();
    }

    init() {
        // console.log('🔄 Global Progression Sync initialisé');
        this.loadProgressionData();
        this.startAutoUpdate();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Écouter les changements de page
        window.addEventListener('beforeunload', () => {
            this.stopAutoUpdate();
        });

        // Écouter les actions de progression
        document.addEventListener('arkalia:progression:update', (event) => {
            this.handleProgressionUpdate(event.detail);
        });

        // Écouter les actions de navigation
        document.addEventListener('arkalia:navigation:change', (event) => {
            this.handlePageChange(event.detail);
        });
    }

    async loadProgressionData() {
        try {
            const response = await fetch('/api/progression/data');
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.progressionData = data.progression;
                    this.cache.set('progression', this.progressionData);
                    this.notifyCallbacks();
                    // console.log('📊 Données de progression chargées');
                }
            }
        } catch (error) {
            console.error('❌ Erreur chargement progression:', error);
        }
    }

    startAutoUpdate() {
        if (this.updateInterval) return;

        this.updateInterval = setInterval(() => {
            this.updateProgressionData();
        }, this.updateFrequency);
    }

    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    async updateProgressionData() {
        if (this.isUpdating) return;

        this.isUpdating = true;
        try {
            const response = await fetch('/api/progression/data');
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    const newData = data.progression;

                    // Vérifier s'il y a des changements
                    if (this.hasProgressionChanged(newData)) {
                        this.progressionData = newData;
                        this.cache.set('progression', this.progressionData);
                        this.notifyCallbacks();
                        this.detectChanges(newData);
                    }
                }
            }
        } catch (error) {
            console.error('❌ Erreur mise à jour progression:', error);
        } finally {
            this.isUpdating = false;
        }
    }

    hasProgressionChanged(newData) {
        if (!this.progressionData) return true;

        const oldData = this.progressionData;
        return (
            oldData.score !== newData.score ||
            oldData.level !== newData.level ||
            oldData.xp !== newData.xp ||
            oldData.coins !== newData.coins ||
            JSON.stringify(oldData.badges) !== JSON.stringify(newData.badges) ||
            JSON.stringify(oldData.achievements_unlocked) !== JSON.stringify(newData.achievements_unlocked)
        );
    }

    detectChanges(newData) {
        if (!this.progressionData) return;

        const oldData = this.progressionData;

        // Détecter les changements de score
        if (newData.score > oldData.score) {
            this.showScoreChange(newData.score - oldData.score);
        }

        // Détecter les changements de niveau
        if (newData.level > oldData.level) {
            this.showLevelUp(newData.level);
        }

        // Détecter les nouveaux badges
        const newBadges = newData.badges.filter(badge => !oldData.badges.includes(badge));
        newBadges.forEach(badge => {
            this.showBadgeUnlock(badge);
        });

        // Détecter les nouveaux achievements
        const newAchievements = newData.achievements_unlocked.filter(
            achievement => !oldData.achievements_unlocked.includes(achievement)
        );
        newAchievements.forEach(achievement => {
            this.showAchievementUnlock(achievement);
        });
    }

    showScoreChange(points) {
        if (window.universalNotifications) {
            window.universalNotifications.success(
                '📈 Score mis à jour !',
                `+${points} points gagnés !`,
                { duration: 3000, importance: 2 }
            );
        }
    }

    showLevelUp(newLevel) {
        if (window.universalNotifications) {
            window.universalNotifications.celebration(
                '🌟 Niveau supérieur !',
                `Félicitations ! Tu es maintenant niveau ${newLevel} !`,
                { duration: 5000, importance: 5 }
            );
        }
    }

    showBadgeUnlock(badge) {
        if (window.universalNotifications) {
            window.universalNotifications.achievement(
                '🏅 Nouveau badge !',
                `Badge "${badge}" débloqué !`,
                { duration: 4000, importance: 4 }
            );
        }
    }

    showAchievementUnlock(achievement) {
        if (window.universalNotifications) {
            window.universalNotifications.achievement(
                '🎯 Achievement débloqué !',
                `Achievement "${achievement}" débloqué !`,
                { duration: 4000, importance: 4 }
            );
        }
    }

    handleProgressionUpdate(detail) {
        // Mettre à jour immédiatement les données locales
        if (detail.type === 'score_earned') {
            this.progressionData.score += detail.points || 0;
            this.progressionData.xp += detail.points || 0;
        } else if (detail.type === 'level_up') {
            this.progressionData.level = detail.newLevel;
        } else if (detail.type === 'badge_earned') {
            if (!this.progressionData.badges.includes(detail.badge)) {
                this.progressionData.badges.push(detail.badge);
            }
        }

        this.notifyCallbacks();
    }

    handlePageChange(detail) {
        // Mettre à jour les données lors du changement de page
        this.updateProgressionData();
    }

    // Méthodes publiques
    getProgressionData() {
        return this.progressionData;
    }

    getCachedData(key) {
        return this.cache.get(key);
    }

    setCachedData(key, value) {
        this.cache.set(key, value);
    }

    onProgressionUpdate(callback) {
        this.callbacks.add(callback);
        return () => this.callbacks.delete(callback);
    }

    notifyCallbacks() {
        this.callbacks.forEach(callback => {
            try {
                callback(this.progressionData);
            } catch (error) {
                console.error('❌ Erreur callback progression:', error);
            }
        });
    }

    // Méthodes de mise à jour des éléments UI
    updateAllProgressBars() {
        const progressBars = document.querySelectorAll('[data-progress-type]');
        progressBars.forEach(bar => {
            const type = bar.dataset.progressType;
            const value = this.getProgressValue(type);
            if (value !== null) {
                this.updateProgressBar(bar, value);
            }
        });
    }

    getProgressValue(type) {
        if (!this.progressionData) return null;

        switch (type) {
            case 'level':
                return this.progressionData.level || 1;
            case 'score':
                return this.progressionData.score || 0;
            case 'xp':
                return this.progressionData.xp || 0;
            case 'coins':
                return this.progressionData.coins || 0;
            case 'badges':
                return this.progressionData.badges ? this.progressionData.badges.length : 0;
            default:
                return null;
        }
    }

    updateProgressBar(element, value) {
        const maxValue = element.dataset.maxValue || 100;
        const percentage = Math.min((value / maxValue) * 100, 100);

        const fill = element.querySelector('.progress-fill, .progress-bar-fill');
        if (fill) {
            fill.style.width = `${percentage}%`;
        }

        const text = element.querySelector('.progress-text, .progress-percentage');
        if (text) {
            text.textContent = `${Math.round(percentage)}%`;
        }
    }

    updateAllStats() {
        // Mettre à jour tous les éléments de stats
        const statElements = document.querySelectorAll('[data-stat-type]');
        statElements.forEach(element => {
            const type = element.dataset.statType;
            const value = this.getStatValue(type);
            if (value !== null) {
                element.textContent = value;
            }
        });
    }

    getStatValue(type) {
        if (!this.progressionData) return null;

        switch (type) {
            case 'level':
                return this.progressionData.level || 1;
            case 'score':
                return this.progressionData.score || 0;
            case 'xp':
                return this.progressionData.xp || 0;
            case 'coins':
                return this.progressionData.coins || 0;
            case 'badges':
                return this.progressionData.badges ? this.progressionData.badges.length : 0;
            case 'achievements':
                return this.progressionData.achievements_unlocked ? this.progressionData.achievements_unlocked.length : 0;
            default:
                return null;
        }
    }

    // Méthode pour forcer une mise à jour
    forceUpdate() {
        this.updateProgressionData();
    }

    // Méthode pour arrêter le système
    destroy() {
        this.stopAutoUpdate();
        this.callbacks.clear();
        this.cache.clear();
    }
}

// Initialiser le système global
document.addEventListener('DOMContentLoaded', () => {
    window.globalProgressionSync = new GlobalProgressionSync();

    // Mettre à jour les éléments UI au chargement
    setTimeout(() => {
        if (window.globalProgressionSync) {
            window.globalProgressionSync.updateAllStats();
            window.globalProgressionSync.updateAllProgressBars();
        }
    }, 1000);
});

// Exporter pour utilisation globale
window.GlobalProgressionSync = GlobalProgressionSync;
