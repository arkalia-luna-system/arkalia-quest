/* ===== ARKALIA QUEST - TERMINAL ENHANCEMENTS ===== */

class TerminalEnhancer {
    constructor() {
        this.terminalOutput = null;
        this.commandHistory = [];
        this.historyIndex = -1;
        this.init();
    }

    init() {
        this.terminalOutput = document.getElementById('terminal-output');
        if (!this.terminalOutput) return;

        this.setupEventListeners();
        this.addWelcomeMessage();
        this.addPageTransition();
    }

    setupEventListeners() {
        // Écouter les commandes rapides
        document.querySelectorAll('.command-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.animateCommandButton(e.target);
                this.executeCommand(e.target.getAttribute('onclick'));
            });
        });

        // Écouter les commandes du terminal
        const terminalInput = document.getElementById('terminal-input');
        if (terminalInput) {
            terminalInput.addEventListener('keydown', (e) => {
                this.handleTerminalInput(e);
            });
        }
    }

    addWelcomeMessage() {
        if (!this.terminalOutput) return;

        const welcomeMessage = this.createMessage('info', '🌙 LUNA: Bienvenue dans le terminal Arkalia Quest. Tapez "aide" pour voir les commandes disponibles.');
        this.addMessageToTerminal(welcomeMessage);
    }

    addPageTransition() {
        const container = document.querySelector('.terminal-container');
        if (container) {
            container.classList.add('page-transition');
        }
    }

    animateCommandButton(button) {
        button.classList.add('command-executed');
        setTimeout(() => {
            button.classList.remove('command-executed');
        }, 500);
    }

    executeCommand(onclickAttr) {
        if (!onclickAttr) return;

        // Extraire la commande de l'attribut onclick
        const commandMatch = onclickAttr.match(/quickCommand\('([^']+)'\)/);
        if (commandMatch) {
            const command = commandMatch[1];
            this.addCommandToTerminal(command);
            this.simulateCommandExecution(command);
        }
    }

    addCommandToTerminal(command) {
        const commandLine = document.createElement('div');
        commandLine.className = 'command-line';
        commandLine.innerHTML = `
            <span class="command-prompt">arkalia@luna:~$</span>
            <span class="command-input">${command}</span>
            <span class="command-cursor"></span>
        `;

        this.addMessageToTerminal(commandLine);

        // Ajouter à l'historique
        this.commandHistory.push(command);
        this.historyIndex = this.commandHistory.length;
    }

    simulateCommandExecution(command) {
        setTimeout(() => {
            let response = this.getCommandResponse(command);
            this.addMessageToTerminal(response);
        }, 300);
    }

    getCommandResponse(command) {
        const responses = {
            'aide': this.createMessage('info', '📖 Commandes disponibles: profil, monde, status, badges, missions, clear, luna'),
            'profil': this.createMessage('success', '👤 Profil chargé. Niveau: 1, XP: 0/100, Badges: 0'),
            'monde': this.createMessage('success', '🌍 Monde ouvert. Zones disponibles: Terminal, Cyber City, Data Center'),
            'status': this.createMessage('info', '📊 Status: Connecté, Système: Opérationnel, LUNA: Active'),
            'badges': this.createMessage('warning', '🏆 Aucun badge obtenu. Complétez des missions pour débloquer des récompenses!'),
            'missions': this.createMessage('info', '🎯 Missions disponibles: Tutoriel (En cours), Première mission (Verrouillée)'),
            'clear': () => {
                this.clearTerminal();
                return null;
            },
            'luna': this.createMessage('luna', '🌙 LUNA: Salut! Comment puis-je t\'aider aujourd\'hui?')
        };

        const response = responses[command];
        if (typeof response === 'function') {
            response();
            return null;
        }
        return response || this.createMessage('error', `❌ Commande "${command}" non reconnue. Tapez "aide" pour voir les commandes disponibles.`);
    }

    createMessage(type, text) {
        const message = document.createElement('div');
        message.className = `terminal-message ${type}`;
        message.textContent = text;
        return message;
    }

    addMessageToTerminal(message) {
        if (!message) return;

        this.terminalOutput.appendChild(message);
        this.scrollToBottom();
    }

    clearTerminal() {
        if (this.terminalOutput) {
            this.terminalOutput.innerHTML = '';
            this.addWelcomeMessage();
        }
    }

    scrollToBottom() {
        if (this.terminalOutput) {
            this.terminalOutput.scrollTop = this.terminalOutput.scrollHeight;
        }
    }

    handleTerminalInput(e) {
        if (e.key === 'Enter') {
            const input = e.target;
            const command = input.value.trim();

            if (command) {
                this.addCommandToTerminal(command);
                this.simulateCommandExecution(command);
                input.value = '';
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            this.navigateHistory(-1);
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            this.navigateHistory(1);
        }
    }

    navigateHistory(direction) {
        if (this.commandHistory.length === 0) return;

        this.historyIndex += direction;

        if (this.historyIndex < 0) {
            this.historyIndex = 0;
        } else if (this.historyIndex >= this.commandHistory.length) {
            this.historyIndex = this.commandHistory.length;
        }

        const terminalInput = document.getElementById('terminal-input');
        if (terminalInput) {
            if (this.historyIndex === this.commandHistory.length) {
                terminalInput.value = '';
            } else {
                terminalInput.value = this.commandHistory[this.historyIndex];
            }
        }
    }
}

// Classe pour les animations de badges
class BadgeAnimator {
    static showBadgeEarned(badgeName, badgeIcon) {
        const notification = document.createElement('div');
        notification.className = 'badge-notification badge-earned';
        notification.innerHTML = `
            <div class="badge-icon">${badgeIcon}</div>
            <div class="badge-text">
                <div class="badge-title">Badge Obtenu!</div>
                <div class="badge-name">${badgeName}</div>
            </div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Classe pour les notifications LUNA
class LunaNotifier {
    static showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `luna-notification luna-notification-${type}`;
        notification.innerHTML = `
            <div class="luna-icon">🌙</div>
            <div class="luna-message">${message}</div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Classe pour les transitions de pages
class PageTransition {
    static addTransition(element) {
        if (element) {
            element.classList.add('page-transition');
        }
    }

    static removeTransition(element) {
        if (element) {
            element.classList.remove('page-transition');
        }
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    // Initialiser l'améliorateur de terminal
    new TerminalEnhancer();

    // Ajouter des transitions de page
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        PageTransition.addTransition(mainContent);
    }

    // Ajouter des effets hover
    document.querySelectorAll('button, .btn, .cta-btn, .nav-button').forEach(btn => {
        btn.classList.add('hover-effect');
    });

    // Ajouter des effets focus
    document.querySelectorAll('input, select, textarea, button, a').forEach(el => {
        el.classList.add('focus-effect');
    });
});

// Export pour utilisation externe
window.TerminalEnhancer = TerminalEnhancer;
window.BadgeAnimator = BadgeAnimator;
window.LunaNotifier = LunaNotifier;
window.PageTransition = PageTransition;
