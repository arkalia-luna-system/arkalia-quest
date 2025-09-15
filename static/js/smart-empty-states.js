/**
 * Smart Empty States - Gestion intelligente des zones vides
 * Masque ou stylise les zones vides pour éviter l'effet "zéro"
 */

class SmartEmptyStates {
    constructor() {
        this.emptyStateTemplates = {
            badges: {
                hidden: true, // Masquer complètement si vide
                placeholder: "🎖️ Tes badges apparaîtront ici...",
                hint: "💡 Complète des missions pour débloquer des badges !"
            },
            missions: {
                hidden: false,
                placeholder: "🎯 Aucune mission en cours",
                hint: "💡 Explore le monde pour découvrir de nouvelles missions !",
                action: "Explorer le monde"
            },
            leaderboard: {
                hidden: false,
                placeholder: "🏆 Classement en cours de chargement...",
                hint: "💡 Joue pour apparaître dans le classement !",
                action: "Commencer à jouer"
            },
            stats: {
                hidden: true, // Masquer les stats vides
                placeholder: "📊 Statistiques en cours de calcul...",
                hint: "💡 Tes statistiques apparaîtront ici !"
            },
            challenges: {
                hidden: false,
                placeholder: "🎮 Défis quotidiens disponibles",
                hint: "💡 Reviens demain pour de nouveaux défis !",
                action: "Voir les défis"
            }
        };

        this.init();
    }

    init() {
        this.observeEmptyStates();
        console.log('✅ Smart Empty States initialisé');
    }

    observeEmptyStates() {
        // Observer les changements dans le DOM
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    this.processNewElements(mutation.addedNodes);
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Traiter les éléments existants
        this.processExistingElements();
    }

    processNewElements(nodes) {
        nodes.forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                this.processElement(node);
            }
        });
    }

    processExistingElements() {
        // Traiter tous les éléments existants
        const elements = document.querySelectorAll('[data-empty-state]');
        elements.forEach(element => this.processElement(element));
    }

    processElement(element) {
        const emptyStateType = element.getAttribute('data-empty-state');
        if (!emptyStateType) return;

        const config = this.emptyStateTemplates[emptyStateType];
        if (!config) return;

        // Vérifier si l'élément est vide
        if (this.isEmpty(element)) {
            this.handleEmptyElement(element, config, emptyStateType);
        } else {
            this.handleNonEmptyElement(element, emptyStateType);
        }
    }

    isEmpty(element) {
        const text = element.textContent.trim();
        const hasContent = text.length > 0 && !text.match(/^(0|--|aucun|vide|null)$/i);
        const hasChildren = element.children.length > 0;

        return !hasContent && !hasChildren;
    }

    handleEmptyElement(element, config, type) {
        if (config.hidden) {
            // Masquer complètement l'élément
            element.style.display = 'none';
            element.classList.add('empty-hidden');
        } else {
            // Afficher un état vide stylisé
            this.showEmptyState(element, config, type);
        }
    }

    handleNonEmptyElement(element, type) {
        // Restaurer l'élément s'il était masqué
        element.style.display = '';
        element.classList.remove('empty-hidden');

        // Supprimer les états vides
        const emptyState = element.querySelector('.smart-empty-state');
        if (emptyState) {
            emptyState.remove();
        }
    }

    showEmptyState(element, config, type) {
        // Supprimer l'ancien état vide s'il existe
        const existingEmptyState = element.querySelector('.smart-empty-state');
        if (existingEmptyState) {
            existingEmptyState.remove();
        }

        // Créer le nouvel état vide
        const emptyState = document.createElement('div');
        emptyState.className = 'smart-empty-state';
        emptyState.innerHTML = `
            <div class="empty-state-content">
                <div class="empty-state-icon">${this.getEmptyStateIcon(type)}</div>
                <div class="empty-state-message">${config.placeholder}</div>
                <div class="empty-state-hint">${config.hint}</div>
                ${config.action ? `<button class="empty-state-action" onclick="this.handleEmptyStateAction('${type}')">${config.action}</button>` : ''}
            </div>
        `;

        // Ajouter les styles si pas déjà présents
        this.addEmptyStateStyles();

        // Ajouter à l'élément
        element.appendChild(emptyState);
    }

    getEmptyStateIcon(type) {
        const icons = {
            badges: '🎖️',
            missions: '🎯',
            leaderboard: '🏆',
            stats: '📊',
            challenges: '🎮',
            default: '📭'
        };
        return icons[type] || icons.default;
    }

    addEmptyStateStyles() {
        if (document.getElementById('smart-empty-states-styles')) return;

        const style = document.createElement('style');
        style.id = 'smart-empty-states-styles';
        style.textContent = `
            .smart-empty-state {
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 120px;
                padding: 20px;
                text-align: center;
                background: linear-gradient(135deg, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.05));
                border-radius: 12px;
                border: 2px dashed rgba(255, 255, 255, 0.2);
                margin: 10px 0;
            }

            .empty-state-content {
                max-width: 300px;
            }

            .empty-state-icon {
                font-size: 48px;
                margin-bottom: 16px;
                opacity: 0.7;
                animation: emptyStatePulse 2s ease-in-out infinite;
            }

            @keyframes emptyStatePulse {
                0%, 100% { opacity: 0.7; transform: scale(1); }
                50% { opacity: 1; transform: scale(1.05); }
            }

            .empty-state-message {
                font-size: 16px;
                font-weight: 600;
                color: var(--text, #e0e0e0);
                margin-bottom: 8px;
            }

            .empty-state-hint {
                font-size: 14px;
                color: var(--text-secondary, #b0b0b0);
                margin-bottom: 16px;
                line-height: 1.4;
            }

            .empty-state-action {
                background: linear-gradient(45deg, var(--primary, #00ff00), var(--secondary, #00ffff));
                color: #000;
                border: none;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 14px;
            }

            .empty-state-action:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }

            .empty-hidden {
                display: none !important;
            }

            /* Thèmes spécifiques */
            .earth-theme .smart-empty-state {
                background: linear-gradient(135deg, rgba(139, 69, 19, 0.1), rgba(139, 69, 19, 0.05));
                border-color: rgba(139, 69, 19, 0.3);
            }

            .dopamine-theme .smart-empty-state {
                background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(78, 205, 196, 0.05));
                border-color: rgba(255, 107, 107, 0.3);
            }

            .neon-theme .smart-empty-state {
                background: linear-gradient(135deg, rgba(157, 78, 221, 0.1), rgba(255, 133, 0, 0.05));
                border-color: rgba(157, 78, 221, 0.3);
            }

            .frog-theme .smart-empty-state {
                background: linear-gradient(135deg, rgba(124, 179, 66, 0.1), rgba(255, 107, 157, 0.05));
                border-color: rgba(124, 179, 66, 0.3);
            }
        `;
        document.head.appendChild(style);
    }

    // Méthode pour gérer les actions des états vides
    handleEmptyStateAction(type) {
        switch (type) {
            case 'missions':
                window.location.href = '/monde';
                break;
            case 'leaderboard':
                window.location.href = '/leaderboard';
                break;
            case 'challenges':
                window.location.href = '/dashboard';
                break;
            default:
                console.log(`Action pour ${type} non définie`);
        }
    }
}

// Initialiser le système
window.smartEmptyStates = new SmartEmptyStates();

// Exporter pour utilisation globale
window.SmartEmptyStates = SmartEmptyStates;
