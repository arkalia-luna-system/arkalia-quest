/**
 * Theme Manager - Gestionnaire de thèmes pour Arkalia Quest
 * Gère le changement de thèmes et la persistance des préférences
 */

class ThemeManager {
    constructor() {
        this.currentTheme = 'matrix';
        this.availableThemes = {
            'matrix': {
                name: 'Matrix',
                description: 'Thème classique vert Matrix',
                icon: '🌌',
                class: 'matrix-theme'
            },
            'cyberpunk': {
                name: 'Cyberpunk',
                description: 'Thème néon rose et cyan',
                icon: '🌆',
                class: 'cyberpunk-theme'
            },
            'neon': {
                name: 'Neon',
                description: 'Thème néon vert et rouge',
                icon: '💚',
                class: 'neon-theme'
            },
            'dark': {
                name: 'Dark Mode',
                description: 'Thème sombre moderne',
                icon: '🌙',
                class: 'dark-theme'
            },
            'retro': {
                name: 'Retro',
                description: 'Thème rétro années 80',
                icon: '🎮',
                class: 'retro-theme'
            },
            'ocean': {
                name: 'Ocean',
                description: 'Thème océan bleu',
                icon: '🌊',
                class: 'ocean-theme'
            },
            'earth': {
                name: 'Earth/Terra',
                description: 'Thème naturel kaki/lilas',
                icon: '🌍',
                class: 'earth-theme'
            },
            'dopamine': {
                name: 'Dopamine Burst',
                description: 'Thème énergisant rose/cyan',
                icon: '🌈',
                class: 'dopamine-theme'
            },
            'neon-electric': {
                name: 'Neon Electric',
                description: 'Thème violet/orange électrique',
                icon: '⚡',
                class: 'neon-theme'
            },
            'frog': {
                name: 'Frog Green',
                description: 'Thème vert moderne + rose/jaune',
                icon: '🐸',
                class: 'frog-theme'
            }
        };

        this.init();
    }

    init() {
        this.loadTheme();
        this.loadThemeFromServer();
        this.createThemeSelector();
        this.setupEventListeners();
        this.applyTheme(this.currentTheme);

        // console.log('🎨 Theme Manager initialisé');
    }

    loadThemeFromServer() {
        fetch('/api/customization/player?player_id=main_user')
            .then((r) => r.ok ? r.json() : null)
            .then((data) => {
                if (data?.success && data?.customization?.current_theme?.id) {
                    const themeId = data.customization.current_theme.id;
                    if (this.availableThemes[themeId]) {
                        this.currentTheme = themeId;
                    }
                }
            })
            .catch(() => {});
    }


    createThemeSelector() {
        // Créer le sélecteur de thème
        const themeSelector = document.createElement('div');
        themeSelector.className = 'theme-selector';
        themeSelector.innerHTML = `
            <select id="theme-select" aria-label="Choisir un thème">
                <option value="">🎨 Choisir un thème</option>
                ${Object.entries(this.availableThemes).map(([key, theme]) =>
            `<option value="${key}">${theme.icon} ${theme.name}</option>`
        ).join('')}
            </select>
        `;

        document.body.appendChild(themeSelector);

        // Définir la valeur actuelle
        const select = document.getElementById('theme-select');
        select.value = this.currentTheme;
    }

    setupEventListeners() {
        // Écouter les changements de thème
        document.getElementById('theme-select').addEventListener('change', (e) => {
            this.changeTheme(e.target.value);
        });

        // Raccourcis clavier
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey) {
                switch (e.key) {
                    case '1': this.changeTheme('matrix'); break;
                    case '2': this.changeTheme('cyberpunk'); break;
                    case '3': this.changeTheme('neon'); break;
                    case '4': this.changeTheme('dark'); break;
                    case '5': this.changeTheme('retro'); break;
                    case '6': this.changeTheme('ocean'); break;
                }
            }
        });
    }

    changeTheme(themeKey) {
        if (!themeKey || !this.availableThemes[themeKey]) {
            return;
        }

        // Supprimer l'ancien thème
        Object.values(this.availableThemes).forEach(theme => {
            document.body.classList.remove(theme.class);
        });

        // Appliquer le nouveau thème
        this.currentTheme = themeKey;
        this.applyTheme(themeKey);
        this.saveTheme();

        // Animation de transition
        this.animateThemeChange();

        // console.log(`🎨 Thème changé vers: ${this.availableThemes[themeKey].name}`);
    }

    applyTheme(themeKey) {
        const theme = this.availableThemes[themeKey];
        if (!theme) return;

        // Ajouter la classe du thème
        document.body.classList.add(theme.class);

        // Mettre à jour les variables CSS personnalisées
        this.updateCSSVariables(themeKey);

        // Mettre à jour les éléments spéciaux
        this.updateSpecialElements(themeKey);
    }

    updateCSSVariables(themeKey) {
        const root = document.documentElement;
        const theme = this.availableThemes[themeKey];

        // Définir les variables CSS selon le thème
        const variables = this.getThemeVariables(themeKey);
        Object.entries(variables).forEach(([property, value]) => {
            root.style.setProperty(property, value);
        });
    }

    getThemeVariables(themeKey) {
        const variables = {
            'matrix': {
                '--primary-color': '#00ff00',
                '--secondary-color': '#00ffff',
                '--accent-color': '#ff00ff',
                '--bg-color': '#000000',
                '--text-color': '#00ff00'
            },
            'cyberpunk': {
                '--primary-color': '#ff0080',
                '--secondary-color': '#00ffff',
                '--accent-color': '#ffff00',
                '--bg-color': '#0a0a0a',
                '--text-color': '#ff0080'
            },
            'neon': {
                '--primary-color': '#00ff41',
                '--secondary-color': '#ff073a',
                '--accent-color': '#00ffff',
                '--bg-color': '#001122',
                '--text-color': '#00ff41'
            },
            'dark': {
                '--primary-color': '#bb86fc',
                '--secondary-color': '#03dac6',
                '--accent-color': '#cf6679',
                '--bg-color': '#121212',
                '--text-color': '#ffffff'
            },
            'retro': {
                '--primary-color': '#ff6b35',
                '--secondary-color': '#f7931e',
                '--accent-color': '#ffd23f',
                '--bg-color': '#2c3e50',
                '--text-color': '#ff6b35'
            },
            'ocean': {
                '--primary-color': '#00bcd4',
                '--secondary-color': '#0097a7',
                '--accent-color': '#26c6da',
                '--bg-color': '#0d47a1',
                '--text-color': '#00bcd4'
            }
        };

        return variables[themeKey] || variables['matrix'];
    }

    updateSpecialElements(themeKey) {
        // Mettre à jour les éléments qui nécessitent une attention spéciale
        const lunaAvatar = document.querySelector('.luna-avatar');
        if (lunaAvatar) {
            lunaAvatar.className = `luna-avatar theme-${themeKey}`;
        }

        // Mettre à jour les boutons
        const buttons = document.querySelectorAll('.cta-btn, .luna-btn, .nav-button');
        buttons.forEach(btn => {
            btn.classList.add(`theme-${themeKey}`);
        });

        // Mettre à jour le terminal
        const terminal = document.querySelector('.terminal');
        if (terminal) {
            terminal.classList.add(`theme-${themeKey}`);
        }
    }

    animateThemeChange() {
        // Animation de transition fluide
        document.body.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';

        // Effet de flash
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.1);
            z-index: 9999;
            pointer-events: none;
            animation: themeFlash 0.5s ease-out;
        `;

        document.body.appendChild(flash);

        setTimeout(() => {
            document.body.removeChild(flash);
            document.body.style.transition = '';
        }, 500);
    }

    saveTheme() {
        localStorage.setItem('arkalia_theme', this.currentTheme);
        fetch(`/api/customization/themes/${encodeURIComponent(this.currentTheme)}/set`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_id: 'main_user' })
        }).then((r) => r.ok ? r.json() : null).catch(() => {});
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('arkalia_theme');
        if (savedTheme && this.availableThemes[savedTheme]) {
            this.currentTheme = savedTheme;
        }
    }

    getCurrentTheme() {
        return {
            key: this.currentTheme,
            ...this.availableThemes[this.currentTheme]
        };
    }

    getAvailableThemes() {
        return this.availableThemes;
    }

    // Méthode pour obtenir des informations sur un thème
    getThemeInfo(themeKey) {
        return this.availableThemes[themeKey] || null;
    }

    // Méthode pour prévisualiser un thème (sans le sauvegarder)
    previewTheme(themeKey) {
        if (!this.availableThemes[themeKey]) return;

        // Supprimer tous les thèmes
        Object.values(this.availableThemes).forEach(theme => {
            document.body.classList.remove(theme.class);
        });

        // Appliquer le thème de prévisualisation
        this.applyTheme(themeKey);

        // Marquer comme prévisualisation
        document.body.classList.add('theme-preview');
    }

    // Méthode pour annuler la prévisualisation
    cancelPreview() {
        document.body.classList.remove('theme-preview');
        this.applyTheme(this.currentTheme);
    }
}

// CSS pour l'animation de flash
const style = document.createElement('style');
style.textContent = `
    @keyframes themeFlash {
        0% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
    
    .theme-preview {
        opacity: 0.9;
        filter: grayscale(0.2);
    }
`;
document.head.appendChild(style);

// Initialiser le gestionnaire de thèmes
const themeManager = new ThemeManager();

// Exporter pour utilisation globale
window.ThemeManager = themeManager;
