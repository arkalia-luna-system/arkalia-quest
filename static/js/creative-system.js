/* ===== ARKALIA QUEST - CREATIVE SYSTEM ===== */

class CreativeSystem {
    constructor() {
        this.easterEggs = new Map();
        this.customThemes = new Map();
        this.creativeSettings = this.loadCreativeSettings();
        this.init();
    }

    init() {
        console.log('🎨 Système créatif initialisé');
        this.loadEasterEggs();
        this.loadCustomThemes();
        this.setupEventListeners();
        this.detectCreativeBehavior();
    }

    // Chargement des easter eggs
    loadEasterEggs() {
        const easterEggs = [
            {
                id: 'konami_code',
                name: 'Code Konami',
                description: 'Le code secret classique',
                trigger: 'ArrowUp,ArrowUp,ArrowDown,ArrowDown,ArrowLeft,ArrowRight,ArrowLeft,ArrowRight,KeyB,KeyA',
                action: () => this.activateKonamiCode(),
                discovered: false
            },
            {
                id: 'matrix_rain',
                name: 'Pluie Matrix',
                description: 'Active la pluie de code Matrix',
                trigger: 'KeyM,KeyA,KeyT,KeyR,KeyI,KeyX',
                action: () => this.activateMatrixRain(),
                discovered: false
            },
            {
                id: 'luna_dance',
                name: 'Danse de LUNA',
                description: 'LUNA fait une danse spéciale',
                trigger: 'KeyL,KeyU,KeyN,KeyA,KeyD,KeyA,KeyN,KeyC,KeyE',
                action: () => this.activateLunaDance(),
                discovered: false
            },
            {
                id: 'cyber_punk',
                name: 'Mode Cyberpunk',
                description: 'Active le thème cyberpunk extrême',
                trigger: 'KeyC,KeyY,KeyB,KeyE,KeyR,KeyP,KeyU,KeyN,KeyK',
                action: () => this.activateCyberpunkMode(),
                discovered: false
            },
            {
                id: 'debug_mode',
                name: 'Mode Debug',
                description: 'Active le mode développeur',
                trigger: 'KeyD,KeyE,KeyB,KeyU,KeyG,KeyM,KeyO,KeyD,KeyE',
                action: () => this.activateDebugMode(),
                discovered: false
            },
            {
                id: 'rainbow_mode',
                name: 'Mode Arc-en-ciel',
                description: 'Active le mode arc-en-ciel',
                trigger: 'KeyR,KeyA,KeyI,KeyN,KeyB,KeyO,KeyW',
                action: () => this.activateRainbowMode(),
                discovered: false
            }
        ];

        this.easterEggs = new Map(easterEggs.map(e => [e.id, e]));
    }

    // Chargement des thèmes personnalisés
    loadCustomThemes() {
        const themes = [
            {
                id: 'matrix_classic',
                name: 'Matrix Classique',
                description: 'Le thème Matrix original',
                colors: {
                    primary: '#00ff00',
                    secondary: '#00ffff',
                    accent: '#ff00ff',
                    background: '#000000',
                    text: '#00ff00'
                },
                effects: ['matrix_rain', 'glitch_effect'],
                unlocked: true
            },
            {
                id: 'cyber_punk',
                name: 'Cyberpunk',
                description: 'Thème cyberpunk futuriste',
                colors: {
                    primary: '#ff0080',
                    secondary: '#00ffff',
                    accent: '#ffff00',
                    background: '#0a0a0a',
                    text: '#ff0080'
                },
                effects: ['neon_glow', 'scan_lines'],
                unlocked: false
            },
            {
                id: 'retro_wave',
                name: 'Retro Wave',
                description: 'Thème synthwave rétro',
                colors: {
                    primary: '#ff00ff',
                    secondary: '#00ffff',
                    accent: '#ffff00',
                    background: '#0a0a0a',
                    text: '#ff00ff'
                },
                effects: ['vaporwave', 'grid_lines'],
                unlocked: false
            },
            {
                id: 'hacker_green',
                name: 'Hacker Vert',
                description: 'Thème hacker classique',
                colors: {
                    primary: '#00ff00',
                    secondary: '#00aa00',
                    accent: '#00ffff',
                    background: '#001100',
                    text: '#00ff00'
                },
                effects: ['terminal_glow', 'ascii_art'],
                unlocked: false
            }
        ];

        this.customThemes = new Map(themes.map(t => [t.id, t]));
    }

    // Détection du comportement créatif
    detectCreativeBehavior() {
        let creativeScore = 0;
        const interactions = this.getStoredInteractions();

        // Analyser les interactions créatives
        interactions.forEach(interaction => {
            if (interaction.command.includes('theme') ||
                interaction.command.includes('color') ||
                interaction.command.includes('customize')) {
                creativeScore += 2;
            }
            if (interaction.command.includes('debug') ||
                interaction.command.includes('secret') ||
                interaction.command.includes('hidden')) {
                creativeScore += 3;
            }
        });

        // Si le score créatif est élevé, débloquer des fonctionnalités
        if (creativeScore >= 10) {
            this.unlockCreativeFeatures();
        }
    }

    // Déblocage des fonctionnalités créatives
    unlockCreativeFeatures() {
        this.customThemes.get('cyber_punk').unlocked = true;
        this.customThemes.get('retro_wave').unlocked = true;
        this.customThemes.get('hacker_green').unlocked = true;

        this.showCreativeUnlock('Fonctionnalités créatives débloquées !');
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Écouter les séquences de touches
        let keySequence = [];
        document.addEventListener('keydown', (e) => {
            keySequence.push(e.code);
            if (keySequence.length > 20) {
                keySequence.shift();
            }

            this.checkEasterEggs(keySequence);
        });

        // Écouter les commandes créatives
        document.addEventListener('terminal-command', (e) => {
            this.handleCreativeCommand(e.detail.command);
        });

        // Écouter les changements de thème
        document.addEventListener('theme-change', (e) => {
            this.handleThemeChange(e.detail.theme);
        });
    }

    // Vérification des easter eggs
    checkEasterEggs(keySequence) {
        this.easterEggs.forEach((easterEgg, id) => {
            if (!easterEgg.discovered && keySequence.join(',').includes(easterEgg.trigger)) {
                this.activateEasterEgg(id);
            }
        });
    }

    // Activation d'un easter egg
    activateEasterEgg(id) {
        const easterEgg = this.easterEggs.get(id);
        if (!easterEgg) return;

        easterEgg.discovered = true;
        easterEgg.action();

        this.showEasterEggNotification(easterEgg);
        this.saveCreativeSettings();
    }

    // Code Konami
    activateKonamiCode() {
        this.showEasterEggMessage('Code Konami activé ! 🎮');
        this.activateMatrixRain();
        this.grantReward({ points: 1000, badge: 'konami_master' });
    }

    // Pluie Matrix
    activateMatrixRain() {
        const rain = document.createElement('div');
        rain.id = 'matrix-rain';
        rain.className = 'matrix-rain';
        document.body.appendChild(rain);

        // Générer la pluie de code
        this.generateMatrixRain();

        // Supprimer après 30 secondes
        setTimeout(() => {
            if (rain.parentNode) {
                rain.parentNode.removeChild(rain);
            }
        }, 30000);
    }

    // Génération de la pluie Matrix
    generateMatrixRain() {
        const rain = document.getElementById('matrix-rain');
        if (!rain) return;

        const characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';

        for (let i = 0; i < 50; i++) {
            const column = document.createElement('div');
            column.className = 'matrix-column';
            column.style.left = Math.random() * 100 + '%';
            column.style.animationDelay = Math.random() * 5 + 's';
            column.style.animationDuration = (Math.random() * 3 + 2) + 's';

            for (let j = 0; j < 20; j++) {
                const char = document.createElement('div');
                char.className = 'matrix-char';
                char.textContent = characters[Math.floor(Math.random() * characters.length)];
                char.style.animationDelay = (j * 0.1) + 's';
                column.appendChild(char);
            }

            rain.appendChild(column);
        }
    }

    // Danse de LUNA
    activateLunaDance() {
        this.showEasterEggMessage('LUNA danse ! 💃');

        // Animer LUNA
        const luna = document.querySelector('.luna-avatar, .luna-icon');
        if (luna) {
            luna.classList.add('luna-dancing');
            setTimeout(() => {
                luna.classList.remove('luna-dancing');
            }, 5000);
        }

        this.grantReward({ points: 500, badge: 'luna_dancer' });
    }

    // Mode Cyberpunk
    activateCyberpunkMode() {
        this.showEasterEggMessage('Mode Cyberpunk activé ! 🤖');
        this.applyTheme('cyber_punk');
        this.activateNeonEffects();
        this.grantReward({ points: 750, badge: 'cyberpunk_master' });
    }

    // Mode Debug
    activateDebugMode() {
        this.showEasterEggMessage('Mode Debug activé ! 🐛');
        this.showDebugPanel();
        this.grantReward({ points: 1000, badge: 'debug_master' });
    }

    // Mode Arc-en-ciel
    activateRainbowMode() {
        this.showEasterEggMessage('Mode Arc-en-ciel activé ! 🌈');
        this.activateRainbowEffects();
        this.grantReward({ points: 600, badge: 'rainbow_master' });
    }

    // Application d'un thème
    applyTheme(themeId) {
        const theme = this.customThemes.get(themeId);
        if (!theme || !theme.unlocked) return;

        const root = document.documentElement;
        root.style.setProperty('--matrix-green', theme.colors.primary);
        root.style.setProperty('--matrix-accent', theme.colors.secondary);
        root.style.setProperty('--violet-lunaire', theme.colors.accent);
        root.style.setProperty('--background-dark', theme.colors.background);
        root.style.setProperty('--argent-holographique', theme.colors.text);

        // Appliquer les effets
        theme.effects.forEach(effect => {
            this.activateEffect(effect);
        });

        this.showThemeNotification(theme);
    }

    // Activation des effets
    activateEffect(effectId) {
        switch (effectId) {
            case 'matrix_rain':
                this.activateMatrixRain();
                break;
            case 'glitch_effect':
                this.activateGlitchEffect();
                break;
            case 'neon_glow':
                this.activateNeonGlow();
                break;
            case 'scan_lines':
                this.activateScanLines();
                break;
            case 'vaporwave':
                this.activateVaporwave();
                break;
            case 'grid_lines':
                this.activateGridLines();
                break;
            case 'terminal_glow':
                this.activateTerminalGlow();
                break;
            case 'ascii_art':
                this.activateAsciiArt();
                break;
        }
    }

    // Effet de glitch
    activateGlitchEffect() {
        document.body.classList.add('glitch-effect');
        setTimeout(() => {
            document.body.classList.remove('glitch-effect');
        }, 2000);
    }

    // Effet néon
    activateNeonGlow() {
        document.body.classList.add('neon-glow');
    }

    // Lignes de balayage
    activateScanLines() {
        const scanLines = document.createElement('div');
        scanLines.className = 'scan-lines';
        document.body.appendChild(scanLines);
    }

    // Effet vaporwave
    activateVaporwave() {
        document.body.classList.add('vaporwave-effect');
    }

    // Lignes de grille
    activateGridLines() {
        const grid = document.createElement('div');
        grid.className = 'grid-lines';
        document.body.appendChild(grid);
    }

    // Lueur du terminal
    activateTerminalGlow() {
        document.body.classList.add('terminal-glow');
    }

    // Art ASCII
    activateAsciiArt() {
        const ascii = document.createElement('div');
        ascii.className = 'ascii-art';
        ascii.innerHTML = `
            <pre>
    ██████╗  ██████╗ ██████╗ ███████╗
    ██╔══██╗██╔═══██╗██╔══██╗██╔════╝
    ██████╔╝██║   ██║██████╔╝█████╗  
    ██╔══██╗██║   ██║██╔══██╗██╔══╝  
    ██║  ██║╚██████╔╝██║  ██║███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
            </pre>
        `;
        document.body.appendChild(ascii);

        setTimeout(() => {
            if (ascii.parentNode) {
                ascii.parentNode.removeChild(ascii);
            }
        }, 5000);
    }

    // Effets arc-en-ciel
    activateRainbowEffects() {
        document.body.classList.add('rainbow-mode');
    }

    // Effets néon
    activateNeonEffects() {
        document.body.classList.add('neon-mode');
    }

    // Panneau de debug
    showDebugPanel() {
        const panel = document.createElement('div');
        panel.id = 'debug-panel';
        panel.className = 'debug-panel';
        panel.innerHTML = `
            <div class="debug-header">
                <h3>Debug Panel</h3>
                <button onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="debug-content">
                <div class="debug-section">
                    <h4>Performance</h4>
                    <div id="debug-fps">FPS: <span id="fps-value">0</span></div>
                    <div id="debug-memory">Memory: <span id="memory-value">0</span> MB</div>
                </div>
                <div class="debug-section">
                    <h4>Easter Eggs</h4>
                    <div id="debug-easter-eggs">
                        ${Array.from(this.easterEggs.values()).map(egg =>
            `<div class="debug-egg ${egg.discovered ? 'discovered' : 'locked'}">
                                ${egg.name}: ${egg.discovered ? '✓' : '✗'}
                            </div>`
        ).join('')}
                    </div>
                </div>
                <div class="debug-section">
                    <h4>Themes</h4>
                    <div id="debug-themes">
                        ${Array.from(this.customThemes.values()).map(theme =>
            `<div class="debug-theme ${theme.unlocked ? 'unlocked' : 'locked'}">
                                ${theme.name}: ${theme.unlocked ? '✓' : '✗'}
                            </div>`
        ).join('')}
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(panel);

        // Mise à jour des métriques
        this.updateDebugMetrics();
    }

    // Mise à jour des métriques de debug
    updateDebugMetrics() {
        const fpsValue = document.getElementById('fps-value');
        const memoryValue = document.getElementById('memory-value');

        if (fpsValue) {
            setInterval(() => {
                fpsValue.textContent = Math.round(1000 / (performance.now() - (window.lastTime || performance.now())));
                window.lastTime = performance.now();
            }, 1000);
        }

        if (memoryValue && performance.memory) {
            setInterval(() => {
                memoryValue.textContent = Math.round(performance.memory.usedJSHeapSize / 1024 / 1024);
            }, 1000);
        }
    }

    // Gestion des commandes créatives
    handleCreativeCommand(command) {
        const creativeCommands = {
            'theme': () => this.showThemeSelector(),
            'colors': () => this.showColorPicker(),
            'customize': () => this.showCustomizationPanel(),
            'debug': () => this.showDebugPanel(),
            'secret': () => this.showSecretMenu(),
            'hidden': () => this.showHiddenFeatures()
        };

        const handler = creativeCommands[command.toLowerCase()];
        if (handler) {
            handler();
        }
    }

    // Sélecteur de thèmes
    showThemeSelector() {
        const selector = document.createElement('div');
        selector.className = 'theme-selector-modal';
        selector.innerHTML = `
            <div class="theme-selector-content">
                <h3>Sélecteur de Thèmes</h3>
                <div class="theme-grid">
                    ${Array.from(this.customThemes.values()).map(theme => `
                        <div class="theme-card ${theme.unlocked ? 'unlocked' : 'locked'}" 
                             onclick="${theme.unlocked ? `creativeSystem.applyTheme('${theme.id}')` : ''}">
                            <div class="theme-preview" style="background: ${theme.colors.background}; color: ${theme.colors.text};">
                                <div class="theme-sample" style="border-color: ${theme.colors.primary};">
                                    <div class="theme-accent" style="background: ${theme.colors.accent};"></div>
                                </div>
                            </div>
                            <div class="theme-name">${theme.name}</div>
                            <div class="theme-status">${theme.unlocked ? '✓' : '🔒'}</div>
                        </div>
                    `).join('')}
                </div>
                <button onclick="this.parentElement.parentElement.remove()">Fermer</button>
            </div>
        `;

        document.body.appendChild(selector);
    }

    // Affichage des notifications
    showEasterEggNotification(easterEgg) {
        this.showNotification(`Easter Egg découvert : ${easterEgg.name} !`, 'easter-egg');
    }

    showCreativeUnlock(message) {
        this.showNotification(message, 'creative-unlock');
    }

    showThemeNotification(theme) {
        this.showNotification(`Thème "${theme.name}" appliqué !`, 'theme-change');
    }

    showEasterEggMessage(message) {
        this.showNotification(message, 'easter-egg-message');
    }

    // Notification générique
    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `creative-notification ${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // Accorder une récompense
    grantReward(reward) {
        // Mettre à jour le score
        this.updateScore(reward.points);

        // Débloquer le badge si applicable
        if (reward.badge) {
            this.unlockBadge(reward.badge);
        }
    }

    // Utilitaires
    getStoredInteractions() {
        return JSON.parse(localStorage.getItem('arkalia_interactions') || '[]');
    }

    loadCreativeSettings() {
        return JSON.parse(localStorage.getItem('arkalia_creative_settings') || JSON.stringify({
            themes: [],
            easterEggs: [],
            customizations: {}
        }));
    }

    saveCreativeSettings() {
        localStorage.setItem('arkalia_creative_settings', JSON.stringify(this.creativeSettings));
    }

    updateScore(points) {
        const currentScore = parseInt(localStorage.getItem('arkalia_score') || '0');
        localStorage.setItem('arkalia_score', currentScore + points);
    }

    unlockBadge(badgeId) {
        // Logique de déblocage de badge
        console.log(`Badge débloqué : ${badgeId}`);
    }
}

// Initialiser le système créatif
window.creativeSystem = new CreativeSystem();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CreativeSystem;
}
