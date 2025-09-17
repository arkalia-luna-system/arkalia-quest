/* ===== ARKALIA QUEST - REWARD SYSTEM ===== */

class RewardSystem {
    constructor() {
        this.notifications = [];
        this.confettiActive = false;
        this.particlesActive = false;
        this.init();
    }

    init() {
        // Créer le conteneur pour les notifications
        this.createNotificationContainer();

        // Créer le conteneur pour les confettis
        this.createConfettiContainer();

        // Créer le conteneur pour les particules
        this.createParticleContainer();

        // console.log('🎉 Reward System initialisé');
    }

    createNotificationContainer() {
        if (!document.getElementById('reward-notifications')) {
            const container = document.createElement('div');
            container.id = 'reward-notifications';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                pointer-events: none;
            `;
            document.body.appendChild(container);
        }
    }

    createConfettiContainer() {
        if (!document.getElementById('confetti-container')) {
            const container = document.createElement('div');
            container.id = 'confetti-container';
            container.className = 'confetti-container';
            document.body.appendChild(container);
        }
    }

    createParticleContainer() {
        if (!document.getElementById('particle-container')) {
            const container = document.createElement('div');
            container.id = 'particle-container';
            container.className = 'particle-container';
            document.body.appendChild(container);
        }
    }

    // Afficher une notification de récompense
    showRewardNotification(type, title, description, icon = '🎉') {
        const notification = document.createElement('div');
        notification.className = 'reward-notification';
        notification.innerHTML = `
            <div class="reward-icon">${icon}</div>
            <div class="reward-title">${title}</div>
            <div class="reward-description">${description}</div>
        `;

        // Ajouter des styles spécifiques selon le type
        switch (type) {
            case 'level_up':
                notification.style.background = 'linear-gradient(135deg, rgba(34, 197, 94, 0.95), rgba(16, 185, 129, 0.95))';
                notification.style.borderColor = 'rgba(34, 197, 94, 0.8)';
                break;
            case 'badge_earned':
                notification.style.background = 'linear-gradient(135deg, rgba(167, 139, 250, 0.95), rgba(139, 92, 246, 0.95))';
                notification.style.borderColor = 'rgba(167, 139, 250, 0.8)';
                break;
            case 'mission_completed':
                notification.style.background = 'linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(37, 99, 235, 0.95))';
                notification.style.borderColor = 'rgba(59, 130, 246, 0.8)';
                break;
            case 'score_gained':
                notification.style.background = 'linear-gradient(135deg, rgba(245, 158, 11, 0.95), rgba(217, 119, 6, 0.95))';
                notification.style.borderColor = 'rgba(245, 158, 11, 0.8)';
                break;
        }

        document.getElementById('reward-notifications').appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Supprimer après 4 secondes
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 500);
        }, 4000);

        this.notifications.push(notification);
    }

    // Déclencher des confettis
    triggerConfetti(duration = 3000) {
        if (this.confettiActive) return;

        this.confettiActive = true;
        const container = document.getElementById('confetti-container');

        // Créer des confettis
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                this.createConfettiPiece(container);
            }, i * 50);
        }

        // Arrêter après la durée spécifiée
        setTimeout(() => {
            this.confettiActive = false;
        }, duration);
    }

    createConfettiPiece(container) {
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';

        // Position aléatoire
        piece.style.left = Math.random() * 100 + '%';
        piece.style.animationDelay = Math.random() * 2 + 's';
        piece.style.animationDuration = (Math.random() * 2 + 2) + 's';

        // Couleur aléatoire
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43'];
        piece.style.background = colors[Math.floor(Math.random() * colors.length)];

        container.appendChild(piece);

        // Supprimer après l'animation
        setTimeout(() => {
            if (piece.parentNode) {
                piece.parentNode.removeChild(piece);
            }
        }, 4000);
    }

    // Déclencher des particules
    triggerParticles(count = 20, duration = 2000) {
        if (this.particlesActive) return;

        this.particlesActive = true;
        const container = document.getElementById('particle-container');

        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                this.createParticle(container);
            }, i * 100);
        }

        setTimeout(() => {
            this.particlesActive = false;
        }, duration);
    }

    createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';

        // Position aléatoire
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 1 + 's';
        particle.style.animationDuration = (Math.random() * 1 + 1) + 's';

        container.appendChild(particle);

        // Supprimer après l'animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 3000);
    }

    // Animer un élément avec une classe spécifique
    animateElement(element, animationClass, duration = 1000) {
        if (!element) return;

        element.classList.add(animationClass);

        setTimeout(() => {
            element.classList.remove(animationClass);
        }, duration);
    }

    // Afficher un spinner de chargement
    showLoadingSpinner(element) {
        if (!element) return;

        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.id = 'loading-spinner';

        element.appendChild(spinner);
    }

    // Masquer le spinner de chargement
    hideLoadingSpinner(element) {
        if (!element) return;

        const spinner = element.querySelector('#loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }

    // Afficher un skeleton loader
    showSkeletonLoader(element, lines = 3) {
        if (!element) return;

        element.innerHTML = '';

        for (let i = 0; i < lines; i++) {
            const skeleton = document.createElement('div');
            skeleton.className = 'skeleton-loader';
            skeleton.style.height = '20px';
            skeleton.style.marginBottom = '10px';
            skeleton.style.width = (Math.random() * 40 + 60) + '%';
            element.appendChild(skeleton);
        }
    }

    // Masquer le skeleton loader
    hideSkeletonLoader(element) {
        if (!element) return;

        const skeletons = element.querySelectorAll('.skeleton-loader');
        skeletons.forEach(skeleton => skeleton.remove());
    }

    // Célébrer un niveau up
    celebrateLevelUp(newLevel) {
        this.showRewardNotification(
            'level_up',
            'Niveau Atteint !',
            `Félicitations ! Tu es maintenant niveau ${newLevel}`,
            '⭐'
        );

        this.triggerConfetti(4000);
        this.triggerParticles(30, 3000);

        // Animer l'élément de niveau
        const levelElement = document.getElementById('current-level') ||
            document.getElementById('level-current') ||
            document.querySelector('.stat-value');

        if (levelElement) {
            this.animateElement(levelElement, 'level-up-animation');
        }
    }

    // Célébrer un badge obtenu
    celebrateBadgeEarned(badgeName) {
        this.showRewardNotification(
            'badge_earned',
            'Badge Obtenu !',
            `Tu as débloqué le badge "${badgeName}"`,
            '🏆'
        );

        this.triggerParticles(25, 2500);

        // Animer l'élément de badge
        const badgeElements = document.querySelectorAll('.badge-item');
        badgeElements.forEach(badge => {
            if (badge.textContent.includes(badgeName)) {
                this.animateElement(badge, 'badge-earned-animation');
            }
        });
    }

    // Célébrer une mission complétée
    celebrateMissionCompleted(missionName) {
        this.showRewardNotification(
            'mission_completed',
            'Mission Terminée !',
            `Mission "${missionName}" complétée avec succès`,
            '🎯'
        );

        this.triggerParticles(20, 2000);

        // Animer l'élément de mission
        const missionElements = document.querySelectorAll('.mission-item');
        missionElements.forEach(mission => {
            if (mission.textContent.includes(missionName)) {
                this.animateElement(mission, 'mission-completed-animation');
            }
        });
    }

    // Célébrer un score gagné
    celebrateScoreGained(points) {
        this.showRewardNotification(
            'score_gained',
            'Points Gagnés !',
            `+${points} points ajoutés à ton score`,
            '💎'
        );

        this.triggerParticles(15, 1500);

        // Animer l'élément de score
        const scoreElement = document.getElementById('total-score') ||
            document.getElementById('score-current') ||
            document.querySelector('.stat-value');

        if (scoreElement) {
            this.animateElement(scoreElement, 'score-gained-animation');
        }
    }

    // Mettre à jour une barre de progression avec animation
    updateProgressBar(barElement, newValue, maxValue = 100) {
        if (!barElement) return;

        const percentage = (newValue / maxValue) * 100;

        // Afficher un skeleton pendant la mise à jour
        this.showSkeletonLoader(barElement.parentElement);

        setTimeout(() => {
            this.hideSkeletonLoader(barElement.parentElement);

            // Animer la barre de progression
            barElement.style.width = percentage + '%';

            // Ajouter l'effet de shine
            const shine = document.createElement('div');
            shine.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                animation: progressShine 1s ease-in-out;
            `;

            barElement.style.position = 'relative';
            barElement.appendChild(shine);

            setTimeout(() => {
                if (shine.parentNode) {
                    shine.parentNode.removeChild(shine);
                }
            }, 1000);
        }, 500);
    }

    // Nettoyer tous les effets
    cleanup() {
        // Supprimer toutes les notifications
        this.notifications.forEach(notification => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        });
        this.notifications = [];

        // Vider les conteneurs d'effets
        const confettiContainer = document.getElementById('confetti-container');
        const particleContainer = document.getElementById('particle-container');

        if (confettiContainer) {
            confettiContainer.innerHTML = '';
        }

        if (particleContainer) {
            particleContainer.innerHTML = '';
        }
    }
}

// Initialiser et déléguer au nouveau RewardFeedbackSystem si présent
window.rewardSystem = new RewardSystem();
document.addEventListener('DOMContentLoaded', () => {
    if (window.rewardFeedbackSystem) {
        // Shims de délégation
        window.rewardSystem.celebrateLevelUp = (lvl) => {
            document.dispatchEvent(new CustomEvent('levelUp', { detail: { level: lvl } }));
        };
        window.rewardSystem.celebrateBadgeEarned = (name) => {
            document.dispatchEvent(new CustomEvent('badgeEarned', { detail: { name } }));
        };
        window.rewardSystem.celebrateMissionCompleted = (name) => {
            document.dispatchEvent(new CustomEvent('missionComplete', { detail: { name } }));
        };
        window.rewardSystem.celebrateScoreGained = (pts) => {
            document.dispatchEvent(new CustomEvent('xpGained', { detail: { amount: pts } }));
        };
    }
});

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RewardSystem;
}
