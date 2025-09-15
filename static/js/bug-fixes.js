/* ===== ARKALIA QUEST - BUG FIXES & STABILITY ===== */

class BugFixes {
    constructor() {
        this.commandHistory = [];
        this.maxHistorySize = 50;
        this.spamProtection = new Map();
        this.lastCommandTime = 0;
        this.minCommandInterval = 200; // 200ms minimum entre les commandes (très tolérant)

        this.init();
    }

    init() {
        this.fixTerminalStability();
        this.fixNavigationIssues();
        this.fixProgressionUpdates();
        this.fixResponsiveIssues();
        this.fixAccessibilityBugs();
        this.fixLunaResponseVariety();

        console.log('🔧 Bug fixes appliqués');
    }

    // ===== STABILITÉ TERMINAL =====
    fixTerminalStability() {
        // Protection contre le spam de commandes
        this.setupSpamProtection();

        // Améliorer les réponses aux commandes invalides
        this.improveInvalidCommandResponses();

        // Optimiser les réponses rapides
        this.optimizeRapidResponses();
    }

    setupSpamProtection() {
        const originalSendCommand = window.sendCommand;
        if (originalSendCommand) {
            window.sendCommand = (command) => {
                if (this.isSpamCommand(command)) {
                    this.showSpamWarning();
                    return;
                }

                this.recordCommand(command);
                return originalSendCommand(command);
            };
        }
    }

    isSpamCommand(command) {
        const now = Date.now();
        const timeSinceLastCommand = now - this.lastCommandTime;

        if (timeSinceLastCommand < this.minCommandInterval) {
            return true;
        }

        // Vérifier les commandes répétitives (plus tolérant)
        const recentCommands = this.commandHistory.slice(-10);
        const duplicateCount = recentCommands.filter(cmd => cmd === command).length;

        if (duplicateCount >= 5) { // Augmenté de 3 à 5
            return true;
        }

        this.lastCommandTime = now;
        return false;
    }

    recordCommand(command) {
        this.commandHistory.push(command);
        if (this.commandHistory.length > this.maxHistorySize) {
            this.commandHistory.shift();
        }
    }

    showSpamWarning() {
        const warning = document.createElement('div');
        warning.className = 'spam-warning';
        warning.innerHTML = `
            <div class="warning-content">
                <div class="warning-icon">⚠️</div>
                <div class="warning-text">Trop rapide ! Attendez un moment...</div>
            </div>
        `;

        warning.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
            color: white;
            padding: 15px 25px;
            border-radius: 25px;
            font-weight: bold;
            text-align: center;
            z-index: 10000;
            animation: spamWarningSlide 3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        `;

        // Ajouter l'animation CSS
        if (!document.getElementById('spam-warning-animation')) {
            const style = document.createElement('style');
            style.id = 'spam-warning-animation';
            style.textContent = `
                @keyframes spamWarningSlide {
                    0% { transform: translateX(-50%) translateY(-100%); opacity: 0; }
                    20% { transform: translateX(-50%) translateY(0); opacity: 1; }
                    80% { transform: translateX(-50%) translateY(0); opacity: 1; }
                    100% { transform: translateX(-50%) translateY(-100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(warning);

        setTimeout(() => {
            if (warning.parentNode) {
                warning.parentNode.removeChild(warning);
            }
        }, 3000);
    }

    improveInvalidCommandResponses() {
        const originalGetCommandResponse = window.getCommandResponse;
        if (originalGetCommandResponse) {
            window.getCommandResponse = (command) => {
                const response = originalGetCommandResponse(command);

                if (response.includes('Commande non reconnue') || response.includes('inconnue')) {
                    return this.getHelpfulInvalidCommandResponse(command);
                }

                return response;
            };
        }
    }

    getHelpfulInvalidCommandResponse(command) {
        const suggestions = this.getCommandSuggestions(command);

        return `❌ Commande "${command}" non reconnue.

💡 Suggestions :
${suggestions.map(s => `• ${s}`).join('\n')}

🔍 Tapez "aide" pour voir toutes les commandes disponibles.`;
    }

    getCommandSuggestions(command) {
        const allCommands = [
            'aide', 'profil', 'missions', 'badges', 'stats', 'monde',
            'terminal', 'dashboard', 'classement', 'tutoriel', 'luna',
            'prologue', 'acte_1', 'acte_2', 'acte_3', 'explorer',
            'games', 'play_game', 'score', 'level', 'xp'
        ];

        const suggestions = allCommands.filter(cmd =>
            cmd.toLowerCase().includes(command.toLowerCase()) ||
            command.toLowerCase().includes(cmd.toLowerCase()) ||
            this.calculateSimilarity(cmd, command) > 0.3
        );

        return suggestions.slice(0, 3);
    }

    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;

        if (longer.length === 0) return 1.0;

        const distance = this.levenshteinDistance(longer, shorter);
        return (longer.length - distance) / longer.length;
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];

        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }

        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }

        return matrix[str2.length][str1.length];
    }

    // ===== PROBLÈMES DE NAVIGATION =====
    fixNavigationIssues() {
        // Corriger les lags visuels lors de la navigation
        this.fixVisualLags();

        // Améliorer les transitions entre pages
        this.improvePageTransitions();

        // Corriger les problèmes de focus
        this.fixFocusIssues();
    }

    fixVisualLags() {
        // Utiliser requestAnimationFrame pour les transitions
        const originalAddEventListener = Element.prototype.addEventListener;
        Element.prototype.addEventListener = function (type, listener, options) {
            if (type === 'transitionend' || type === 'animationend') {
                const wrappedListener = (e) => {
                    requestAnimationFrame(() => listener.call(this, e));
                };
                return originalAddEventListener.call(this, type, wrappedListener, options);
            }
            return originalAddEventListener.call(this, type, listener, options);
        };
    }

    improvePageTransitions() {
        // Ajouter des transitions fluides
        document.addEventListener('DOMContentLoaded', () => {
            document.body.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        });

        // Intercepter les changements de contenu
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    this.animateNewContent(mutation.addedNodes);
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    animateNewContent(nodes) {
        nodes.forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                node.style.opacity = '0';
                node.style.transform = 'translateY(10px)';
                node.style.transition = 'opacity 0.3s ease, transform 0.3s ease';

                requestAnimationFrame(() => {
                    node.style.opacity = '1';
                    node.style.transform = 'translateY(0)';
                });
            }
        });
    }

    fixFocusIssues() {
        // Améliorer la navigation clavier
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                this.enhanceTabNavigation(e);
            }
        });

        // Améliorer le focus visible
        this.enhanceFocusVisibility();
    }

    enhanceTabNavigation(e) {
        const focusableElements = document.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        const currentIndex = Array.from(focusableElements).indexOf(document.activeElement);

        if (e.shiftKey) {
            // Tab vers l'arrière
            if (currentIndex === 0) {
                e.preventDefault();
                focusableElements[focusableElements.length - 1].focus();
            }
        } else {
            // Tab vers l'avant
            if (currentIndex === focusableElements.length - 1) {
                e.preventDefault();
                focusableElements[0].focus();
            }
        }
    }

    enhanceFocusVisibility() {
        // Améliorer la visibilité du focus
        const style = document.createElement('style');
        style.textContent = `
            *:focus {
                outline: 3px solid #00ff00 !important;
                outline-offset: 2px !important;
                box-shadow: 0 0 0 3px rgba(0, 255, 0, 0.3) !important;
            }
            
            .dark-mode *:focus {
                outline: 3px solid #00ffff !important;
                outline-offset: 2px !important;
                box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.3) !important;
            }
        `;
        document.head.appendChild(style);
    }

    // ===== MISE À JOUR DE PROGRESSION =====
    fixProgressionUpdates() {
        // Corriger les compteurs figés
        this.fixFrozenCounters();

        // Améliorer la synchronisation des données
        this.improveDataSynchronization();
    }

    fixFrozenCounters() {
        // Observer les changements de données
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-value') {
                    this.updateCounter(mutation.target);
                }
            });
        });

        // Observer tous les éléments avec des compteurs
        const counters = document.querySelectorAll('[data-counter], [data-value]');
        counters.forEach(counter => {
            observer.observe(counter, { attributes: true });
        });
    }

    updateCounter(element) {
        const newValue = element.dataset.value || element.dataset.counter;
        const currentValue = element.textContent;

        if (newValue && newValue !== currentValue) {
            this.animateCounterUpdate(element, currentValue, newValue);
        }
    }

    animateCounterUpdate(element, from, to) {
        const startValue = parseInt(from) || 0;
        const endValue = parseInt(to) || 0;
        const duration = 500;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const current = Math.round(startValue + (endValue - startValue) * progress);
            element.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    improveDataSynchronization() {
        // Synchroniser les données entre les composants
        this.setupDataSync();

        // Améliorer la mise à jour des états
        this.improveStateUpdates();
    }

    setupDataSync() {
        // Écouter les événements de mise à jour
        document.addEventListener('dataUpdate', (e) => {
            this.syncDataAcrossComponents(e.detail);
        });
    }

    syncDataAcrossComponents(data) {
        // Mettre à jour tous les composants concernés
        const components = document.querySelectorAll('[data-sync]');
        components.forEach(component => {
            if (component.dataset.sync === data.type) {
                this.updateComponent(component, data);
            }
        });
    }

    updateComponent(component, data) {
        // Mettre à jour le composant avec les nouvelles données
        if (data.value !== undefined) {
            component.textContent = data.value;
        }

        if (data.class !== undefined) {
            component.className = data.class;
        }

        if (data.attribute !== undefined) {
            Object.keys(data.attribute).forEach(key => {
                component.setAttribute(key, data.attribute[key]);
            });
        }
    }

    // ===== PROBLÈMES RESPONSIVE =====
    fixResponsiveIssues() {
        // Corriger les problèmes de responsive
        this.fixTableOverflow();

        // Améliorer la navigation sur mobile
        this.improveMobileNavigation();
    }

    fixTableOverflow() {
        // Corriger les débordements de tableaux
        const tables = document.querySelectorAll('table');
        tables.forEach(table => {
            table.style.overflowX = 'auto';
            table.style.width = '100%';

            // Ajouter un wrapper si nécessaire
            if (!table.parentElement.classList.contains('table-wrapper')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-wrapper';
                wrapper.style.overflowX = 'auto';
                wrapper.style.width = '100%';

                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });
    }

    improveMobileNavigation() {
        // Améliorer la navigation sur mobile
        if (window.innerWidth < 768) {
            this.enableMobileOptimizations();
        }

        window.addEventListener('resize', () => {
            if (window.innerWidth < 768) {
                this.enableMobileOptimizations();
            } else {
                this.disableMobileOptimizations();
            }
        });
    }

    enableMobileOptimizations() {
        document.body.classList.add('mobile-optimized');

        // Ajuster les tailles de police
        const smallTexts = document.querySelectorAll('small, .small-text');
        smallTexts.forEach(text => {
            text.style.fontSize = '12px';
        });

        // Ajuster les boutons
        const buttons = document.querySelectorAll('button, .btn');
        buttons.forEach(button => {
            button.style.minHeight = '44px';
            button.style.minWidth = '44px';
        });
    }

    disableMobileOptimizations() {
        document.body.classList.remove('mobile-optimized');
    }

    // ===== BUGS D'ACCESSIBILITÉ =====
    fixAccessibilityBugs() {
        // Corriger les problèmes d'accessibilité
        this.fixAccessibilityIssues();

        // Améliorer la navigation clavier
        this.improveKeyboardNavigation();
    }

    fixAccessibilityIssues() {
        // Ajouter des attributs ARIA manquants
        this.addMissingAriaAttributes();

        // Améliorer les contrastes
        this.improveContrasts();
    }

    addMissingAriaAttributes() {
        // Ajouter des attributs ARIA aux boutons
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (button.textContent) {
                button.setAttribute('aria-label', button.textContent.trim());
            }
        });

        // Ajouter des attributs ARIA aux liens
        const links = document.querySelectorAll('a:not([aria-label])');
        links.forEach(link => {
            if (link.textContent) {
                link.setAttribute('aria-label', link.textContent.trim());
            }
        });
    }

    improveContrasts() {
        // Améliorer les contrastes automatiquement
        const style = document.createElement('style');
        style.textContent = `
            .high-contrast {
                filter: contrast(1.5) brightness(1.2);
            }
            
            .high-contrast * {
                color: #000 !important;
                background-color: #fff !important;
            }
            
            .high-contrast .dark-mode {
                color: #fff !important;
                background-color: #000 !important;
            }
        `;
        document.head.appendChild(style);
    }

    // ===== VARIÉTÉ DES RÉPONSES LUNA =====
    fixLunaResponseVariety() {
        // Améliorer la variété des réponses LUNA
        this.enhanceLunaResponses();

        // Éviter les répétitions
        this.avoidRepetitiveResponses();
    }

    enhanceLunaResponses() {
        // Intercepter les réponses LUNA
        const originalAddMessage = window.addMessage;
        if (originalAddMessage) {
            window.addMessage = (message, type) => {
                if (type === 'luna' || message.includes('LUNA:')) {
                    const enhancedMessage = this.enhanceLunaMessage(message);
                    return originalAddMessage(enhancedMessage, type);
                }
                return originalAddMessage(message, type);
            };
        }
    }

    enhanceLunaMessage(message) {
        // Ajouter de la variété aux messages LUNA
        const enhancements = [
            '🌟 ' + message,
            '✨ ' + message,
            '🚀 ' + message,
            '💫 ' + message,
            '🎯 ' + message
        ];

        const randomEnhancement = enhancements[Math.floor(Math.random() * enhancements.length)];

        // Ajouter des variations de ton
        const toneVariations = [
            'Avec enthousiasme, ',
            'En souriant, ',
            'Avec curiosité, ',
            'En s\'illuminant, ',
            'Avec bienveillance, '
        ];

        const randomTone = toneVariations[Math.floor(Math.random() * toneVariations.length)];

        return randomTone + randomEnhancement;
    }

    avoidRepetitiveResponses() {
        // Éviter les réponses répétitives
        this.responseHistory = [];
        this.maxResponseHistory = 10;

        const originalAddMessage = window.addMessage;
        if (originalAddMessage) {
            window.addMessage = (message, type) => {
                if (type === 'luna' || message.includes('LUNA:')) {
                    if (this.isRepetitiveResponse(message)) {
                        const variedMessage = this.createVariedResponse(message);
                        return originalAddMessage(variedMessage, type);
                    }
                    this.recordResponse(message);
                }
                return originalAddMessage(message, type);
            };
        }
    }

    isRepetitiveResponse(message) {
        return this.responseHistory.includes(message);
    }

    createVariedResponse(message) {
        // Créer une variante du message
        const variations = [
            message.replace('Bienvenue', 'Salut'),
            message.replace('Bonjour', 'Hey'),
            message.replace('Merci', 'Super'),
            message.replace('Parfait', 'Excellent'),
            message.replace('Génial', 'Fantastique')
        ];

        return variations[Math.floor(Math.random() * variations.length)];
    }

    recordResponse(message) {
        this.responseHistory.push(message);
        if (this.responseHistory.length > this.maxResponseHistory) {
            this.responseHistory.shift();
        }
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.bugFixes = new BugFixes();
});

// Export pour utilisation externe
window.BugFixes = BugFixes;
