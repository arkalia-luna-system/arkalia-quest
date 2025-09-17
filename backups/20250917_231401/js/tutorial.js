/* ===== ARKALIA QUEST - TUTORIAL SYSTEM ===== */
/* Système de tutoriel interactif pour guider les nouveaux joueurs */

class TutorialSystem {
    constructor() {
        this.currentStep = 0;
        this.steps = [];
        this.isActive = false;
        this.overlay = null;
        this.init();
    }

    init() {
        this.createStyles();
        this.setupEventListeners();
        this.initializeSteps();
        // console.log('🎯 Tutorial System initialisé');
    }

    createStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .tutorial-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                z-index: 10000;
                display: none;
                align-items: center;
                justify-content: center;
            }

            .tutorial-overlay.active {
                display: flex;
            }

            .tutorial-modal {
                background: var(--luna-surface);
                border: 2px solid var(--luna-violet);
                border-radius: 1rem;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                position: relative;
                backdrop-filter: blur(20px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }

            .tutorial-step {
                text-align: center;
            }

            .tutorial-icon {
                font-size: 3rem;
                margin-bottom: 1rem;
                display: block;
                animation: tutorialPulse 2s ease-in-out infinite;
            }

            @keyframes tutorialPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            .tutorial-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--luna-text);
                margin-bottom: 1rem;
            }

            .tutorial-description {
                color: var(--luna-text-secondary);
                margin-bottom: 2rem;
                line-height: 1.6;
            }

            .tutorial-actions {
                display: flex;
                gap: 1rem;
                justify-content: center;
            }

            .tutorial-btn {
                padding: 0.75rem 1.5rem;
                border: none;
                border-radius: 0.5rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .tutorial-btn.primary {
                background: linear-gradient(135deg, var(--luna-violet), var(--luna-cyan));
                color: white;
            }

            .tutorial-btn.secondary {
                background: transparent;
                color: var(--luna-text);
                border: 2px solid var(--luna-violet);
            }

            .tutorial-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
            }

            .tutorial-progress {
                margin-top: 1rem;
                text-align: center;
                color: var(--luna-text-muted);
                font-size: 0.9rem;
            }

            .tutorial-highlight {
                position: relative;
                z-index: 10001;
                box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.5);
                border-radius: 0.5rem;
                animation: tutorialHighlight 2s ease-in-out infinite;
            }

            @keyframes tutorialHighlight {
                0%, 100% { box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.5); }
                50% { box-shadow: 0 0 0 8px rgba(139, 92, 246, 0.3); }
            }
        `;
        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Écouter les clics sur les boutons de tutoriel
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('tutorial-btn')) {
                this.handleButtonClick(e.target);
            }
        });

        // Écouter les événements de fin de tutoriel
        document.addEventListener('tutorialComplete', () => {
            this.completeTutorial();
        });
    }

    initializeSteps() {
        this.steps = [
            {
                icon: '🌙',
                title: 'Bienvenue dans Arkalia Quest !',
                description: 'Je suis LUNA, ton guide dans cette aventure cybernétique. Laisse-moi te montrer les bases.',
                action: 'Commencer'
            },
            {
                icon: '⌨️',
                title: 'Le Terminal LUNA',
                description: 'Utilise le terminal pour communiquer avec moi et exécuter des commandes. C\'est ton interface principale.',
                action: 'Suivant',
                highlight: '.terminal, .cta-btn[href="/terminal"]'
            },
            {
                icon: '🎯',
                title: 'Les Missions',
                description: 'Explore les missions pour progresser dans l\'histoire. Chaque mission te rapproche de la vérité.',
                action: 'Suivant',
                highlight: '.cta-btn[href="/tutorial"]'
            },
            {
                icon: '🏆',
                title: 'Les Achievements',
                description: 'Gagne des badges et des récompenses en accomplissant des défis. Collectionne-les tous !',
                action: 'Suivant',
                highlight: '.cta-btn[href="/profil"]'
            },
            {
                icon: '🌍',
                title: 'Explorer le Monde',
                description: 'Découvre les différentes zones d\'Arkalia. Chaque zone cache ses propres secrets.',
                action: 'Suivant',
                highlight: '.cta-btn[href="/monde"]'
            },
            {
                icon: '🎉',
                title: 'Prêt pour l\'aventure !',
                description: 'Tu connais maintenant les bases. L\'aventure commence ! Bonne chance, hacker.',
                action: 'Commencer l\'aventure'
            }
        ];
    }

    startTutorial() {
        this.isActive = true;
        this.currentStep = 0;
        this.createOverlay();
        this.showStep(0);
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'tutorial-overlay';
        this.overlay.innerHTML = `
            <div class="tutorial-modal">
                <div class="tutorial-step">
                    <span class="tutorial-icon"></span>
                    <h2 class="tutorial-title"></h2>
                    <p class="tutorial-description"></p>
                    <div class="tutorial-actions">
                        <button class="tutorial-btn secondary" data-action="skip">Passer</button>
                        <button class="tutorial-btn primary" data-action="next">Commencer</button>
                    </div>
                    <div class="tutorial-progress"></div>
                </div>
            </div>
        `;
        document.body.appendChild(this.overlay);
    }

    showStep(stepIndex) {
        if (stepIndex >= this.steps.length) {
            this.completeTutorial();
            return;
        }

        const step = this.steps[stepIndex];
        const modal = this.overlay.querySelector('.tutorial-modal');

        modal.querySelector('.tutorial-icon').textContent = step.icon;
        modal.querySelector('.tutorial-title').textContent = step.title;
        modal.querySelector('.tutorial-description').textContent = step.description;

        const nextBtn = modal.querySelector('.tutorial-btn.primary');
        nextBtn.textContent = step.action;
        nextBtn.dataset.action = stepIndex === this.steps.length - 1 ? 'complete' : 'next';

        modal.querySelector('.tutorial-progress').textContent =
            `Étape ${stepIndex + 1} sur ${this.steps.length}`;

        // Mettre en surbrillance l'élément si spécifié
        if (step.highlight) {
            this.highlightElement(step.highlight);
        }

        this.overlay.classList.add('active');
    }

    highlightElement(selector) {
        // Supprimer les surbrillances précédentes
        document.querySelectorAll('.tutorial-highlight').forEach(el => {
            el.classList.remove('tutorial-highlight');
        });

        // Ajouter la surbrillance à l'élément cible
        const element = document.querySelector(selector);
        if (element) {
            element.classList.add('tutorial-highlight');
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    handleButtonClick(button) {
        const action = button.dataset.action;

        switch (action) {
            case 'next':
                this.currentStep++;
                this.showStep(this.currentStep);
                break;
            case 'skip':
                this.completeTutorial();
                break;
            case 'complete':
                this.completeTutorial();
                break;
        }
    }

    completeTutorial() {
        this.isActive = false;

        // Supprimer les surbrillances
        document.querySelectorAll('.tutorial-highlight').forEach(el => {
            el.classList.remove('tutorial-highlight');
        });

        // Supprimer l'overlay
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }

        // Marquer le tutoriel comme complété
        localStorage.setItem('arkalia_tutorial_completed', 'true');

        // Déclencher l'événement de fin de tutoriel
        document.dispatchEvent(new CustomEvent('tutorialComplete'));

        // console.log('🎉 Tutoriel terminé !');
    }

    // Méthode publique pour vérifier si le tutoriel a été complété
    isTutorialCompleted() {
        return localStorage.getItem('arkalia_tutorial_completed') === 'true';
    }

    // Méthode publique pour réinitialiser le tutoriel
    resetTutorial() {
        localStorage.removeItem('arkalia_tutorial_completed');
        // console.log('🔄 Tutoriel réinitialisé');
    }
}

// Initialiser le système
document.addEventListener('DOMContentLoaded', () => {
    window.tutorialSystem = new TutorialSystem();

    // Démarrer automatiquement le tutoriel si c'est la première visite
    if (!window.tutorialSystem.isTutorialCompleted()) {
        // Attendre un peu que la page soit chargée
        setTimeout(() => {
            window.tutorialSystem.startTutorial();
        }, 2000);
    }
});

// Exporter pour utilisation globale
window.TutorialSystem = TutorialSystem;
