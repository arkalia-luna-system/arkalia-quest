/**
 * Système de synchronisation unifié pour Arkalia Quest
 * Corrige les problèmes de synchronisation des stats
 */

class UnifiedProgressionSync {
    constructor() {
        this.isInitialized = false;
        this.syncInterval = null;
        this.lastSyncTime = 0;
        this.syncFrequency = 3000; // 3 secondes
        this.retryCount = 0;
        this.maxRetries = 3;

        this.init();
    }

    init() {
        // console.log('🔄 Initialisation du système de synchronisation unifié...');
        this.setupEventListeners();
        this.startSyncLoop();
        this.isInitialized = true;
        // console.log('✅ Synchronisation unifiée initialisée');
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('arkalia:progression:updated', (e) => {
            this.forceSync();
        });

        // Écouter les événements de mission
        document.addEventListener('arkalia:mission:completed', (e) => {
            this.forceSync();
        });

        // Écouter les événements de skill tree
        document.addEventListener('arkalia:skill:upgraded', (e) => {
            this.forceSync();
        });

        // Écouter les événements du terminal
        document.addEventListener('arkalia:terminal:command', (e) => {
            this.forceSync();
        });
    }

    startSyncLoop() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
        }

        this.syncInterval = setInterval(() => {
            this.syncProgression();
        }, this.syncFrequency);
    }

    async syncProgression() {
        try {
            const response = await fetch('/api/sync-progression', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.updateUI(data.player_data);
                this.lastSyncTime = Date.now();
                this.retryCount = 0;

                // Déclencher un événement de synchronisation
                this.dispatchSyncEvent(data.player_data);
            }
        } catch (error) {
            console.warn('⚠️ Erreur de synchronisation:', error.message);
            this.handleSyncError(error);
        }
    }

    async forceSync() {
        // console.log('🔄 Synchronisation forcée...');
        await this.syncProgression();
    }

    updateUI(playerData) {
        // Mettre à jour tous les éléments UI avec les nouvelles données
        this.updateStats(playerData);
        this.updateSkillTree(playerData);
        this.updateMissions(playerData);
        this.updateBadges(playerData);
        this.updateProgressBars(playerData);
    }

    updateStats(playerData) {
        // Mettre à jour les stats dans le dashboard
        const elements = {
            'player-level': playerData.level || 1,
            'player-xp': playerData.xp || 0,
            'player-score': playerData.score || 0,
            'player-coins': playerData.coins || 0
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
                element.classList.add('updated');
                setTimeout(() => element.classList.remove('updated'), 1000);
            }
        });
    }

    updateSkillTree(playerData) {
        // Mettre à jour l'arbre de compétences
        if (window.skillTreeSystem) {
            window.skillTreeSystem.updateFromServerData(playerData);
        }
    }

    updateMissions(playerData) {
        // Mettre à jour les missions
        if (window.missionSystem) {
            window.missionSystem.updateFromServerData(playerData);
        }
    }

    updateBadges(playerData) {
        // Mettre à jour les badges
        const badgeContainer = document.querySelector('.badges-container');
        if (badgeContainer && playerData.badges) {
            badgeContainer.innerHTML = playerData.badges
                .filter(badge => badge && badge.trim())
                .map(badge => `<span class="badge">${badge}</span>`)
                .join('');
        }
    }

    updateProgressBars(playerData) {
        // Mettre à jour les barres de progression
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const level = playerData.level || 1;
            const xp = playerData.xp || 0;
            const nextLevelXP = level * 100; // Formule simple
            const progress = Math.min((xp % nextLevelXP) / nextLevelXP * 100, 100);

            bar.style.width = `${progress}%`;
            bar.setAttribute('aria-valuenow', progress);
        });
    }

    dispatchSyncEvent(playerData) {
        // Déclencher un événement personnalisé pour les autres systèmes
        const event = new CustomEvent('arkalia:unified:synced', {
            detail: {
                playerData: playerData,
                timestamp: Date.now()
            }
        });
        document.dispatchEvent(event);
    }

    handleSyncError(error) {
        this.retryCount++;

        if (this.retryCount >= this.maxRetries) {
            console.error('❌ Échec de synchronisation après', this.maxRetries, 'tentatives');
            this.retryCount = 0;

            // Afficher une notification d'erreur
            this.showSyncError();
        } else {
            // Augmenter l'intervalle de retry
            const retryDelay = this.syncFrequency * (this.retryCount + 1);
            setTimeout(() => {
                this.syncProgression();
            }, retryDelay);
        }
    }

    showSyncError() {
        // Afficher une notification d'erreur de synchronisation
        if (window.universalFeedback) {
            window.universalFeedback.showError(
                'Problème de synchronisation des données. Rechargement...',
                { autoHide: false }
            );

            // Recharger la page après 3 secondes
            setTimeout(() => {
                window.location.reload();
            }, 3000);
        }
    }

    // Méthode publique pour forcer la synchronisation
    forceSyncNow() {
        return this.forceSync();
    }

    // Méthode pour arrêter la synchronisation
    stopSync() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
        }
    }

    // Méthode pour redémarrer la synchronisation
    restartSync() {
        this.stopSync();
        this.startSyncLoop();
    }

    // Méthode pour obtenir le statut
    getStatus() {
        return {
            isInitialized: this.isInitialized,
            isRunning: !!this.syncInterval,
            lastSyncTime: this.lastSyncTime,
            retryCount: this.retryCount,
            syncFrequency: this.syncFrequency
        };
    }
}

// Initialiser le système de synchronisation unifié
window.unifiedProgressionSync = new UnifiedProgressionSync();

// Exporter pour les modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UnifiedProgressionSync;
}
