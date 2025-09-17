/* ===== ARKALIA QUEST - REALTIME FEEDBACK SYSTEM ===== */
/* Système de feedbacks en temps réel pour tous les modules */

class RealtimeFeedback {
    constructor() {
        this.notificationQueue = [];
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createNotificationContainer();
        this.startProgressSync();
        // console.log('⚡ Realtime Feedback System initialisé');
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('arkalia:progression:synced', (e) => {
            this.handleProgressionUpdate(e.detail);
        });

        // Écouter les événements de mission
        document.addEventListener('arkalia:mission:completed', (e) => {
            this.showMissionCompleteFeedback(e.detail);
        });

        // Écouter les événements de badge
        document.addEventListener('arkalia:badge:earned', (e) => {
            this.showBadgeEarnedFeedback(e.detail);
        });

        // Écouter les événements de skill upgrade
        document.addEventListener('arkalia:skill:upgraded', (e) => {
            this.showSkillUpgradeFeedback(e.detail);
        });
    }

    createNotificationContainer() {
        // Créer le conteneur de notifications
        if (!document.getElementById('realtime-notifications')) {
            const container = document.createElement('div');
            container.id = 'realtime-notifications';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                pointer-events: none;
                max-width: 350px;
            `;
            document.body.appendChild(container);
        }
    }

    startProgressSync() {
        // Synchroniser les données de progression toutes les 3 secondes
        setInterval(() => {
            this.syncProgressData();
        }, 3000);
    }

    async syncProgressData() {
        try {
            const response = await fetch('/api/progression-data');
            const data = await response.json();

            if (data.success) {
                this.handleProgressionUpdate(data.progression);
            }
        } catch (error) {
            // console.log('Erreur sync progression:', error);
        }
    }

    handleProgressionUpdate(progressionData) {
        // Mettre à jour tous les éléments d'affichage
        this.updateDashboardStats(progressionData);
        this.updateProfileStats(progressionData);
        this.updateLeaderboardStats(progressionData);
        this.updateMissionStats(progressionData);
    }

    updateDashboardStats(progressionData) {
        // Mettre à jour les stats du dashboard
        const stats = {
            'level': progressionData.level,
            'xp': progressionData.xp,
            'score': progressionData.score,
            'coins': progressionData.coins,
            'badges': progressionData.badges?.length || 0,
            'missions': progressionData.missions_completed?.length || 0
        };

        Object.entries(stats).forEach(([key, value]) => {
            const elements = document.querySelectorAll(`[data-stat="${key}"], .${key}-value, #${key}-value, .player-${key}`);
            elements.forEach(el => {
                const oldValue = el.textContent;
                if (oldValue !== value.toString()) {
                    this.animateValueChange(el, oldValue, value);
                }
            });
        });
    }

    updateProfileStats(progressionData) {
        // Mettre à jour les stats du profil
        this.updateDashboardStats(progressionData);

        // Mettre à jour les compétences
        if (progressionData.skills) {
            this.updateSkillsDisplay(progressionData.skills);
        }
    }

    updateLeaderboardStats(progressionData) {
        // Déclencher une mise à jour du leaderboard
        const event = new CustomEvent('arkalia:leaderboard:update', {
            detail: progressionData
        });
        document.dispatchEvent(event);
    }

    updateMissionStats(progressionData) {
        // Déclencher une mise à jour des missions
        const event = new CustomEvent('arkalia:missions:update', {
            detail: progressionData
        });
        document.dispatchEvent(event);
    }

    updateSkillsDisplay(skills) {
        // Mettre à jour l'affichage des compétences
        Object.entries(skills).forEach(([category, categorySkills]) => {
            Object.entries(categorySkills).forEach(([skill, level]) => {
                const skillElement = document.querySelector(`[data-category="${category}"][data-skill="${skill}"]`);
                if (skillElement) {
                    const levelElement = skillElement.querySelector('.skill-level');
                    if (levelElement) {
                        levelElement.textContent = `Niveau ${level}`;
                    }
                }
            });
        });
    }

    animateValueChange(element, oldValue, newValue) {
        // Animation de changement de valeur
        element.style.transition = 'all 0.3s ease';
        element.style.transform = 'scale(1.1)';
        element.style.color = '#00ff00';

        // Mettre à jour la valeur
        element.textContent = newValue;

        // Retour à la normale
        setTimeout(() => {
            element.style.transform = 'scale(1)';
            element.style.color = '';
        }, 300);
    }

    showMissionCompleteFeedback(missionData) {
        const { mission, xp, coins } = missionData;

        // Créer la notification
        const notification = this.createNotification(
            `🎉 Mission "${mission}" terminée !\n+${xp} XP • +${coins} 🪙`,
            'mission-complete'
        );

        this.showNotification(notification);

        // Effet de confettis
        this.createConfettiEffect();

        // Son de victoire
        this.playVictorySound();
    }

    showBadgeEarnedFeedback(badgeData) {
        const { badge, description } = badgeData;

        // Créer la notification
        const notification = this.createNotification(
            `🏆 NOUVEAU BADGE !\n${badge}\n${description}`,
            'badge-earned'
        );

        this.showNotification(notification);

        // Animation spéciale pour les badges
        this.createBadgeAnimation(badge);

        // Son de badge
        this.playBadgeSound();
    }

    showSkillUpgradeFeedback(skillData) {
        const { category, skill, level } = skillData;

        // Créer la notification
        const notification = this.createNotification(
            `⚡ ${skill} amélioré au niveau ${level} !`,
            'skill-upgrade'
        );

        this.showNotification(notification);

        // Effet de particules
        this.createParticleEffect('skill-upgrade');

        // Son de succès
        this.playSuccessSound();
    }

    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `realtime-notification ${type}`;
        notification.style.cssText = `
            background: ${this.getNotificationColor(type)};
            color: white;
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            border: 2px solid ${this.getNotificationBorderColor(type)};
            font-family: 'IBM Plex Mono', monospace;
            font-size: 14px;
            line-height: 1.4;
            white-space: pre-line;
            text-align: center;
            max-width: 300px;
            animation: slideInRight 0.5s ease-out;
            transform: translateX(100%);
            opacity: 0;
        `;

        notification.textContent = message;
        return notification;
    }

    showNotification(notification) {
        const container = document.getElementById('realtime-notifications');
        if (!container) return;

        container.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        }, 10);

        // Supprimer après 4 secondes
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }

    getNotificationColor(type) {
        const colors = {
            'mission-complete': 'linear-gradient(135deg, #22c55e, #16a34a)',
            'badge-earned': 'linear-gradient(135deg, #ffd700, #ffb700)',
            'skill-upgrade': 'linear-gradient(135deg, #3b82f6, #2563eb)',
            'level-up': 'linear-gradient(135deg, #8b5cf6, #7c3aed)'
        };
        return colors[type] || 'linear-gradient(135deg, #3b82f6, #2563eb)';
    }

    getNotificationBorderColor(type) {
        const colors = {
            'mission-complete': '#00ff00',
            'badge-earned': '#ffd700',
            'skill-upgrade': '#00aaff',
            'level-up': '#8b5cf6'
        };
        return colors[type] || '#00aaff';
    }

    createConfettiEffect() {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        `;

        const colors = ['#00ff00', '#ff00ff', '#ffff00', '#00ffff', '#ff8000'];

        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: absolute;
                width: 8px;
                height: 8px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${Math.random() * 100}%;
                top: -10px;
                border-radius: ${Math.random() > 0.5 ? '50%' : '0'};
                animation: confettiFall ${2 + Math.random() * 3}s linear forwards;
            `;
            container.appendChild(confetti);
        }

        document.body.appendChild(container);

        // Ajouter l'animation CSS
        this.addConfettiAnimation();

        setTimeout(() => {
            if (container.parentNode) {
                container.parentNode.removeChild(container);
            }
        }, 5000);
    }

    createParticleEffect(type) {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 9999;
        `;

        const colors = type === 'skill-upgrade'
            ? ['#00ff00', '#22c55e', '#16a34a']
            : ['#ff00ff', '#a855f7', '#7c3aed'];

        for (let i = 0; i < 15; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 6px;
                height: 6px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                border-radius: 50%;
                left: 0;
                top: 0;
                animation: particleExplode 1s ease-out forwards;
            `;

            const angle = (Math.PI * 2 * i) / 15;
            const distance = 40 + Math.random() * 20;
            const x = Math.cos(angle) * distance;
            const y = Math.sin(angle) * distance;

            particle.style.setProperty('--x', x + 'px');
            particle.style.setProperty('--y', y + 'px');

            container.appendChild(particle);
        }

        document.body.appendChild(container);

        // Ajouter l'animation CSS
        this.addParticleAnimation();

        setTimeout(() => {
            if (container.parentNode) {
                container.parentNode.removeChild(container);
            }
        }, 1000);
    }

    createBadgeAnimation(badgeName) {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 9999;
        `;

        const badge = document.createElement('div');
        badge.style.cssText = `
            font-size: 4em;
            color: #ffd700;
            text-shadow: 0 0 20px #ffd700;
            animation: badgeEarned 2s ease-out forwards;
        `;
        badge.textContent = '🏆';

        container.appendChild(badge);
        document.body.appendChild(container);

        // Ajouter l'animation CSS
        this.addBadgeAnimation();

        setTimeout(() => {
            if (container.parentNode) {
                container.parentNode.removeChild(container);
            }
        }, 2000);
    }

    addConfettiAnimation() {
        if (document.getElementById('confetti-animation-style')) return;

        const style = document.createElement('style');
        style.id = 'confetti-animation-style';
        style.textContent = `
            @keyframes confettiFall {
                to {
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    addParticleAnimation() {
        if (document.getElementById('particle-animation-style')) return;

        const style = document.createElement('style');
        style.id = 'particle-animation-style';
        style.textContent = `
            @keyframes particleExplode {
                to {
                    transform: translate(var(--x), var(--y));
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    addBadgeAnimation() {
        if (document.getElementById('badge-animation-style')) return;

        const style = document.createElement('style');
        style.id = 'badge-animation-style';
        style.textContent = `
            @keyframes badgeEarned {
                0% {
                    transform: scale(0) rotate(0deg);
                    opacity: 0;
                }
                50% {
                    transform: scale(1.2) rotate(180deg);
                    opacity: 1;
                }
                100% {
                    transform: scale(1) rotate(360deg);
                    opacity: 0;
                }
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }

    playSuccessSound() {
        this.playTone([800, 1000, 1200], 0.3);
    }

    playVictorySound() {
        this.playTone([600, 800, 1000, 1200, 1400], 0.5);
    }

    playBadgeSound() {
        this.playTone([1000, 1200, 1400, 1600], 0.4);
    }

    playTone(frequencies, duration) {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            let currentTime = audioContext.currentTime;
            frequencies.forEach((freq, index) => {
                oscillator.frequency.setValueAtTime(freq, currentTime + index * 0.1);
            });

            gainNode.gain.setValueAtTime(0.2, currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, currentTime + duration);

            oscillator.start(currentTime);
            oscillator.stop(currentTime + duration);
        } catch (error) {
            // console.log('Impossible de jouer le son:', error);
        }
    }
}

// Initialiser le système de feedback en temps réel
const realtimeFeedback = new RealtimeFeedback();
