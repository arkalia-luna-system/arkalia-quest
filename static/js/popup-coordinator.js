/* ===== ARKALIA QUEST - POPUP COORDINATOR ===== */
/* Coordinateur pour éviter les chevauchements de popups automatiques */

class PopupCoordinator {
    constructor() {
        this.autoPopupSystems = new Map();
        this.isInitialized = false;
        this.init();
    }

    init() {
        // Attendre que tous les systèmes soient chargés
        setTimeout(() => {
            this.setupPopupCoordination();
            this.isInitialized = true;
            console.log('🎭 Popup Coordinator initialisé');
        }, 2000);
    }

    setupPopupCoordination() {
        // Désactiver les popups automatiques des systèmes existants
        this.disableAutoPopups();

        // Rediriger les popups vers le PopupManager
        this.redirectPopupsToManager();

        // Coordonner les popups par priorité
        this.setupPrioritySystem();
    }

    disableAutoPopups() {
        // Désactiver les popups automatiques de LUNA Vision
        if (window.lunaVision) {
            const originalShowMessage = window.lunaVision.showLunaMessage;
            window.lunaVision.showLunaMessage = (message, duration) => {
                if (window.popupManager) {
                    window.popupManager.replaceLunaMessage(message, duration);
                } else {
                    originalShowMessage.call(window.lunaVision, message, duration);
                }
            };
        }

        // Désactiver les popups automatiques des missions
        if (window.dailyMissions) {
            const originalShowCompletion = window.dailyMissions.showMissionCompletion;
            if (originalShowCompletion) {
                window.dailyMissions.showMissionCompletion = (mission) => {
                    if (window.popupManager) {
                        window.popupManager.replaceMissionCompletion(mission.name, {
                            xp: mission.xp,
                            coins: mission.coins
                        });
                    } else {
                        originalShowCompletion.call(window.dailyMissions, mission);
                    }
                };
            }
        }

        // Désactiver les popups automatiques de l'exploration des zones
        if (window.zoneExploration) {
            const originalShowNarrative = window.zoneExploration.showZoneNarrative;
            if (originalShowNarrative) {
                window.zoneExploration.showZoneNarrative = (zoneData) => {
                    if (window.popupManager) {
                        window.popupManager.replaceZoneExploration(zoneData);
                    } else {
                        originalShowNarrative.call(window.zoneExploration, zoneData);
                    }
                };
            }
        }

        // Désactiver les popups automatiques des états vides
        if (window.motivationalEmptyStates) {
            const originalShowEmptyState = window.motivationalEmptyStates.showEmptyStateMessage;
            if (originalShowEmptyState) {
                window.motivationalEmptyStates.showEmptyStateMessage = (element, type) => {
                    // Délai pour éviter les popups multiples
                    setTimeout(() => {
                        if (window.popupManager && window.popupManager.getActivePopups().length === 0) {
                            originalShowEmptyState.call(window.motivationalEmptyStates, element, type);
                        }
                    }, 1000);
                };
            }
        }
    }

    redirectPopupsToManager() {
        // Rediriger les notifications vers le PopupManager
        if (window.smartNotifications) {
            const originalShow = window.smartNotifications.showSmartNotification;
            if (originalShow) {
                window.smartNotifications.showSmartNotification = (message, type, duration) => {
                    if (window.popupManager) {
                        window.popupManager.showNotification(message, type, duration);
                    } else {
                        originalShow.call(window.smartNotifications, message, type, duration);
                    }
                };
            }
        }

        // Rediriger les animations de récompenses
        if (window.rewardAnimations) {
            const originalAnimateMission = window.rewardAnimations.animateMissionCompletion;
            if (originalAnimateMission) {
                window.rewardAnimations.animateMissionCompletion = (mission, rewards) => {
                    if (window.popupManager) {
                        window.popupManager.replaceMissionCompletion(mission, rewards);
                    } else {
                        originalAnimateMission.call(window.rewardAnimations, mission, rewards);
                    }
                };
            }
        }
    }

    setupPrioritySystem() {
        // Définir les priorités des systèmes
        this.autoPopupSystems.set('luna_messages', { priority: 'medium', delay: 0 });
        this.autoPopupSystems.set('mission_completion', { priority: 'high', delay: 500 });
        this.autoPopupSystems.set('zone_exploration', { priority: 'medium', delay: 1000 });
        this.autoPopupSystems.set('empty_states', { priority: 'low', delay: 2000 });
        this.autoPopupSystems.set('notifications', { priority: 'low', delay: 0 });
        this.autoPopupSystems.set('challenge_completion', { priority: 'high', delay: 500 });
        this.autoPopupSystems.set('puzzle_completion', { priority: 'medium', delay: 1000 });
    }

    // Méthode pour coordonner les popups avec délai
    coordinatePopup(systemName, popupFunction, delay = 0) {
        const systemConfig = this.autoPopupSystems.get(systemName);
        const actualDelay = delay || (systemConfig ? systemConfig.delay : 0);

        setTimeout(() => {
            // Vérifier qu'aucun popup de priorité plus haute n'est actif
            if (this.canShowPopup(systemName)) {
                popupFunction();
            } else {
                // Réessayer plus tard
                this.coordinatePopup(systemName, popupFunction, 1000);
            }
        }, actualDelay);
    }

    canShowPopup(systemName) {
        if (!window.popupManager) return true;

        const activePopups = window.popupManager.getActivePopups();
        if (activePopups.length === 0) return true;

        const systemConfig = this.autoPopupSystems.get(systemName);
        if (!systemConfig) return true;

        // Vérifier la priorité
        const systemPriority = this.getPriorityValue(systemConfig.priority);

        // Si des popups de priorité plus haute sont actifs, attendre
        for (const popupId of activePopups) {
            const popupElement = document.getElementById(`popup_${popupId}`);
            if (popupElement) {
                const popupPriority = this.getElementPriority(popupElement);
                if (popupPriority > systemPriority) {
                    return false;
                }
            }
        }

        return true;
    }

    getPriorityValue(priority) {
        const priorities = { low: 1, medium: 2, high: 3 };
        return priorities[priority] || 2;
    }

    getElementPriority(element) {
        if (element.classList.contains('popup-priority-high')) return 3;
        if (element.classList.contains('popup-priority-medium')) return 2;
        if (element.classList.contains('popup-priority-low')) return 1;
        return 2;
    }

    // Méthode pour nettoyer les popups en conflit
    cleanupConflictingPopups() {
        if (!window.popupManager) return;

        const activePopups = window.popupManager.getActivePopups();
        if (activePopups.length > 3) {
            // Garder seulement les 3 popups les plus récents
            const popupData = Array.from(window.popupManager.activePopups.values());
            popupData.sort((a, b) => b.created - a.created);

            for (let i = 3; i < popupData.length; i++) {
                window.popupManager.closePopup(popupData[i].config.id);
            }
        }
    }

    // Méthode pour gérer les popups en queue
    processPopupQueue() {
        if (!window.popupManager) return;

        // Nettoyer les popups en conflit
        this.cleanupConflictingPopups();

        // Traiter la queue
        window.popupManager.processQueue();
    }
}

// Initialiser le coordinateur de popups
document.addEventListener('DOMContentLoaded', () => {
    window.popupCoordinator = new PopupCoordinator();

    // Nettoyer les popups toutes les 30 secondes
    setInterval(() => {
        if (window.popupCoordinator) {
            window.popupCoordinator.processPopupQueue();
        }
    }, 30000);
});

// Exporter pour utilisation globale
window.PopupCoordinator = PopupCoordinator;
