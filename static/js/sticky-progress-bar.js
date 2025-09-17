/* ===== ARKALIA QUEST - STICKY PROGRESS BAR ===== */
/* Barre de progression sticky visible sur toutes les pages */

class StickyProgressBar {
    constructor() {
        this.element = null;
        this.isVisible = true;
        this.animationDuration = 300;
        this.lastUpdate = 0;
        this.updateThrottle = 1000; // 1 seconde
        this.init();
    }

    init() {
        this.createStickyBar();
        this.setupEventListeners();
        this.updateProgress();
        console.log('📊 Sticky Progress Bar initialisé');
    }

    createStickyBar() {
        // Créer l'élément sticky
        this.element = document.createElement('div');
        this.element.id = 'sticky-progress-bar';
        this.element.className = 'sticky-progress-bar';

        this.element.innerHTML = `
            <div class="sticky-progress-content">
                <div class="sticky-progress-left">
                    <div class="sticky-progress-item">
                        <span class="sticky-progress-icon">⭐</span>
                        <span class="sticky-progress-value" data-stat-type="level">1</span>
                    </div>
                    <div class="sticky-progress-item">
                        <span class="sticky-progress-icon">🏆</span>
                        <span class="sticky-progress-value" data-stat-type="score">0</span>
                    </div>
                    <div class="sticky-progress-item">
                        <span class="sticky-progress-icon">🏅</span>
                        <span class="sticky-progress-value" data-stat-type="badges">0</span>
                    </div>
                </div>
                <div class="sticky-progress-center">
                    <div class="sticky-progress-bar-container">
                        <div class="sticky-progress-bar-bg">
                            <div class="sticky-progress-bar-fill" data-progress-type="level"></div>
                        </div>
                        <span class="sticky-progress-text">Niveau</span>
                    </div>
                </div>
                <div class="sticky-progress-right">
                    <div class="sticky-progress-item">
                        <span class="sticky-progress-icon">💰</span>
                        <span class="sticky-progress-value" data-stat-type="coins">0</span>
                    </div>
                    <div class="sticky-progress-item">
                        <span class="sticky-progress-icon">🎯</span>
                        <span class="sticky-progress-value" data-stat-type="achievements">0</span>
                    </div>
                    <button class="sticky-progress-toggle" title="Masquer/Afficher la barre">
                        <span class="toggle-icon">−</span>
                    </button>
                </div>
            </div>
        `;

        // Ajouter les styles
        this.addStyles();

        // Ajouter au DOM
        document.body.appendChild(this.element);
    }

    addStyles() {
        if (document.getElementById('sticky-progress-bar-styles')) return;

        const style = document.createElement('style');
        style.id = 'sticky-progress-bar-styles';
        style.textContent = `
            .sticky-progress-bar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 1000;
                background: rgba(9, 9, 11, 0.95);
                border-bottom: 2px solid rgba(167, 139, 250, 0.3);
                backdrop-filter: blur(15px);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                transform: translateY(0);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }

            .sticky-progress-bar.hidden {
                transform: translateY(-100%);
            }

            .sticky-progress-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 8px 20px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .sticky-progress-left,
            .sticky-progress-right {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            .sticky-progress-center {
                flex: 1;
                max-width: 300px;
                margin: 0 20px;
            }

            .sticky-progress-item {
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 4px 8px;
                background: rgba(167, 139, 250, 0.1);
                border: 1px solid rgba(167, 139, 250, 0.2);
                border-radius: 6px;
                transition: all 0.2s ease;
            }

            .sticky-progress-item:hover {
                background: rgba(167, 139, 250, 0.2);
                border-color: rgba(167, 139, 250, 0.4);
            }

            .sticky-progress-icon {
                font-size: 0.9em;
                filter: drop-shadow(0 0 4px rgba(167, 139, 250, 0.6));
            }

            .sticky-progress-value {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.85em;
                font-weight: 600;
                color: var(--violet-lunaire);
                text-shadow: 0 0 8px rgba(167, 139, 250, 0.6);
            }

            .sticky-progress-bar-container {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .sticky-progress-bar-bg {
                flex: 1;
                height: 8px;
                background: rgba(167, 139, 250, 0.2);
                border-radius: 4px;
                overflow: hidden;
                border: 1px solid rgba(167, 139, 250, 0.3);
            }

            .sticky-progress-bar-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
                border-radius: 4px;
                transition: width 0.8s ease;
                position: relative;
                box-shadow: 0 0 8px rgba(167, 139, 250, 0.5);
            }

            .sticky-progress-bar-fill::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                animation: progressShine 2s ease-in-out infinite;
            }

            @keyframes progressShine {
                0% { transform: translateX(-100%); }
                50% { transform: translateX(100%); }
                100% { transform: translateX(100%); }
            }

            .sticky-progress-text {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.8em;
                color: var(--argent-holographique);
                font-weight: 600;
                min-width: 50px;
            }

            .sticky-progress-toggle {
                background: rgba(167, 139, 250, 0.1);
                border: 1px solid rgba(167, 139, 250, 0.3);
                border-radius: 4px;
                color: var(--argent-holographique);
                cursor: pointer;
                padding: 4px 8px;
                font-size: 0.8em;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 24px;
                height: 24px;
            }

            .sticky-progress-toggle:hover {
                background: rgba(167, 139, 250, 0.3);
                border-color: var(--violet-lunaire);
                color: var(--violet-lunaire);
            }

            .toggle-icon {
                font-size: 0.9em;
                font-weight: bold;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .sticky-progress-content {
                    padding: 6px 15px;
                }

                .sticky-progress-left,
                .sticky-progress-right {
                    gap: 10px;
                }

                .sticky-progress-center {
                    margin: 0 10px;
                    max-width: 200px;
                }

                .sticky-progress-item {
                    padding: 3px 6px;
                }

                .sticky-progress-icon {
                    font-size: 0.8em;
                }

                .sticky-progress-value {
                    font-size: 0.8em;
                }

                .sticky-progress-text {
                    font-size: 0.7em;
                    min-width: 40px;
                }
            }

            @media (max-width: 480px) {
                .sticky-progress-content {
                    padding: 4px 10px;
                }

                .sticky-progress-left,
                .sticky-progress-right {
                    gap: 8px;
                }

                .sticky-progress-center {
                    margin: 0 8px;
                    max-width: 150px;
                }

                .sticky-progress-item {
                    padding: 2px 4px;
                }

                .sticky-progress-icon {
                    font-size: 0.7em;
                }

                .sticky-progress-value {
                    font-size: 0.7em;
                }
            }
        `;

        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Toggle de la barre
        const toggleBtn = this.element.querySelector('.sticky-progress-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.toggle();
            });
        }

        // Écouter les mises à jour de progression
        if (window.globalProgressionSync) {
            window.globalProgressionSync.onProgressionUpdate((data) => {
                this.updateProgress(data);
            });
        }

        // Écouter les changements de page
        document.addEventListener('arkalia:navigation:change', () => {
            this.updateProgress();
        });
    }

    updateProgress(data = null) {
        const now = Date.now();
        if (now - this.lastUpdate < this.updateThrottle) return;

        this.lastUpdate = now;

        if (!data && window.globalProgressionSync) {
            data = window.globalProgressionSync.getProgressionData();
        }

        if (!data) return;

        // Mettre à jour les valeurs
        const statElements = this.element.querySelectorAll('[data-stat-type]');
        statElements.forEach(element => {
            const type = element.dataset.statType;
            const value = this.getStatValue(data, type);
            if (value !== null) {
                this.animateValueChange(element, value);
            }
        });

        // Mettre à jour la barre de progression
        const progressBar = this.element.querySelector('[data-progress-type]');
        if (progressBar) {
            const level = data.level || 1;
            const xp = data.xp || 0;
            const xpForNextLevel = level * 1000;
            const currentLevelXp = xp % 1000;
            const percentage = (currentLevelXp / 1000) * 100;

            this.updateProgressBar(progressBar, percentage);
        }
    }

    getStatValue(data, type) {
        switch (type) {
            case 'level':
                return data.level || 1;
            case 'score':
                return data.score || 0;
            case 'xp':
                return data.xp || 0;
            case 'coins':
                return data.coins || 0;
            case 'badges':
                return data.badges ? data.badges.length : 0;
            case 'achievements':
                return data.achievements_unlocked ? data.achievements_unlocked.length : 0;
            default:
                return null;
        }
    }

    animateValueChange(element, newValue) {
        const oldValue = parseInt(element.textContent) || 0;
        if (oldValue === newValue) return;

        // Animation de changement de valeur
        element.style.transform = 'scale(1.1)';
        element.style.color = '#00ff00';

        setTimeout(() => {
            element.textContent = newValue;
            element.style.transform = 'scale(1)';
            element.style.color = '';
        }, 150);
    }

    updateProgressBar(element, percentage) {
        const fill = element.querySelector('.sticky-progress-bar-fill');
        if (fill) {
            fill.style.width = `${Math.min(percentage, 100)}%`;
        }
    }

    toggle() {
        this.isVisible = !this.isVisible;

        if (this.isVisible) {
            this.element.classList.remove('hidden');
            this.element.querySelector('.toggle-icon').textContent = '−';
        } else {
            this.element.classList.add('hidden');
            this.element.querySelector('.toggle-icon').textContent = '+';
        }
    }

    show() {
        this.isVisible = true;
        this.element.classList.remove('hidden');
        this.element.querySelector('.toggle-icon').textContent = '−';
    }

    hide() {
        this.isVisible = false;
        this.element.classList.add('hidden');
        this.element.querySelector('.toggle-icon').textContent = '+';
    }

    // Méthode pour forcer une mise à jour
    forceUpdate() {
        this.updateProgress();
    }

    // Méthode pour détruire la barre
    destroy() {
        if (this.element && this.element.parentNode) {
            this.element.parentNode.removeChild(this.element);
        }
    }
}

// Initialiser la barre sticky
document.addEventListener('DOMContentLoaded', () => {
    // Attendre que le système de progression soit prêt
    setTimeout(() => {
        window.stickyProgressBar = new StickyProgressBar();
    }, 1000);
});

// Exporter pour utilisation globale
window.StickyProgressBar = StickyProgressBar;
