/* ===== ARKALIA QUEST - SKILL TREE SYSTEM ===== */
/* Système d'arbre de compétences non-linéaire pour enrichir le gameplay */

class SkillTreeSystem {
    constructor() {
        this.skillTree = this.initializeSkillTree();
        this.playerSkills = {};
        this.init();
    }

    init() {
        this.loadPlayerSkills();
        this.setupEventListeners();
        this.createSkillTreeUI();
        this.syncWithTerminal();
        this.loadServerData();
        console.log('🌳 Skill Tree System initialisé');
    }

    async loadServerData() {
        // Charger les données depuis le serveur
        try {
            const response = await fetch('/api/skill-tree');
            const data = await response.json();

            if (data.success && data.player_data) {
                // Mettre à jour les données locales avec celles du serveur
                this.updateFromServerData(data.player_data);
            }
        } catch (error) {
            console.log('Impossible de charger les données du serveur:', error);
        }
    }

    updateFromServerData(playerData) {
        // Mettre à jour les compétences avec les données du serveur
        if (playerData.skills) {
            this.playerSkills = playerData.skills;
        }

        // Mettre à jour l'XP total
        if (playerData.xp !== undefined) {
            this.playerTotalXP = playerData.xp;
        }

        // Mettre à jour l'affichage
        this.updatePlayerStats();
        this.updateSkillTreeDisplay();
    }

    async syncPlayerData() {
        // Synchroniser les données du joueur depuis le serveur
        try {
            const response = await fetch('/api/progression-data');
            const data = await response.json();

            if (data.success) {
                this.updateFromServerData(data.progression);
                // Mettre à jour l'affichage des boutons d'amélioration
                this.updateUpgradeButtons();
            }
        } catch (error) {
            console.log('Erreur synchronisation données joueur:', error);
        }
    }

    updateUpgradeButtons() {
        // Mettre à jour l'affichage des boutons d'amélioration
        const skillItems = document.querySelectorAll('.skill-item');
        skillItems.forEach(item => {
            const categoryId = item.dataset.category;
            const skillId = item.dataset.skill;
            const canUpgrade = this.canUpgradeSkill(categoryId, skillId);
            const upgradeButton = item.querySelector('.upgrade-skill');
            const upgradeUnavailable = item.querySelector('.upgrade-unavailable');

            if (canUpgrade) {
                if (upgradeUnavailable) upgradeUnavailable.style.display = 'none';
                if (upgradeButton) upgradeButton.style.display = 'flex';
            } else {
                if (upgradeButton) upgradeButton.style.display = 'none';
                if (upgradeUnavailable) upgradeUnavailable.style.display = 'block';
            }
        });
    }

    initializeSkillTree() {
        return {
            "hacking": {
                "name": "Hacking",
                "icon": "💻",
                "color": "#22c55e",
                "description": "Compétences de piratage et d'infiltration",
                "skills": {
                    "code_breaking": {
                        "name": "Cassage de Code",
                        "description": "Décrypter les codes d'accès",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 100, 250, 500, 1000],
                        "unlocked": true,
                        "prerequisites": [],
                        "effects": {
                            "mission_success_rate": [0, 0.05, 0.10, 0.15, 0.20],
                            "hacking_speed": [0, 0.1, 0.2, 0.3, 0.4]
                        }
                    },
                    "system_penetration": {
                        "name": "Pénétration Système",
                        "description": "Infiltrer les systèmes de sécurité",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 150, 350, 700, 1400],
                        "unlocked": false,
                        "prerequisites": ["code_breaking"],
                        "effects": {
                            "mission_success_rate": [0, 0.08, 0.15, 0.22, 0.30],
                            "stealth_bonus": [0, 0.1, 0.2, 0.3, 0.4]
                        }
                    },
                    "cryptography": {
                        "name": "Cryptographie",
                        "description": "Maîtriser les techniques de chiffrement",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 200, 450, 900, 1800],
                        "unlocked": false,
                        "prerequisites": ["code_breaking", "system_penetration"],
                        "effects": {
                            "mission_success_rate": [0, 0.10, 0.20, 0.30, 0.40],
                            "decryption_speed": [0, 0.2, 0.4, 0.6, 0.8]
                        }
                    },
                    "social_engineering": {
                        "name": "Ingénierie Sociale",
                        "description": "Manipuler les utilisateurs pour obtenir des informations",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 120, 280, 560, 1120],
                        "unlocked": false,
                        "prerequisites": ["code_breaking"],
                        "effects": {
                            "mission_success_rate": [0, 0.06, 0.12, 0.18, 0.25],
                            "social_bonus": [0, 0.15, 0.30, 0.45, 0.60]
                        }
                    }
                }
            },
            "combat": {
                "name": "Combat",
                "icon": "⚔️",
                "color": "#ef4444",
                "description": "Compétences de combat et de défense",
                "skills": {
                    "defense": {
                        "name": "Défense",
                        "description": "Protéger la base et les systèmes",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 100, 250, 500, 1000],
                        "unlocked": true,
                        "prerequisites": [],
                        "effects": {
                            "mission_success_rate": [0, 0.05, 0.10, 0.15, 0.20],
                            "damage_reduction": [0, 0.1, 0.2, 0.3, 0.4]
                        }
                    },
                    "offense": {
                        "name": "Offensive",
                        "description": "Attaquer et repousser les menaces",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 150, 350, 700, 1400],
                        "unlocked": false,
                        "prerequisites": ["defense"],
                        "effects": {
                            "mission_success_rate": [0, 0.08, 0.15, 0.22, 0.30],
                            "attack_power": [0, 0.2, 0.4, 0.6, 0.8]
                        }
                    },
                    "strategy": {
                        "name": "Stratégie",
                        "description": "Planifier et coordonner les actions",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 200, 450, 900, 1800],
                        "unlocked": false,
                        "prerequisites": ["defense", "offense"],
                        "effects": {
                            "mission_success_rate": [0, 0.10, 0.20, 0.30, 0.40],
                            "team_bonus": [0, 0.1, 0.2, 0.3, 0.4]
                        }
                    },
                    "tactics": {
                        "name": "Tactiques",
                        "description": "Techniques de combat avancées",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 120, 280, 560, 1120],
                        "unlocked": false,
                        "prerequisites": ["offense"],
                        "effects": {
                            "mission_success_rate": [0, 0.06, 0.12, 0.18, 0.25],
                            "critical_hit": [0, 0.05, 0.10, 0.15, 0.20]
                        }
                    }
                }
            },
            "social": {
                "name": "Social",
                "icon": "💬",
                "color": "#3b82f6",
                "description": "Compétences sociales et de communication",
                "skills": {
                    "persuasion": {
                        "name": "Persuasion",
                        "description": "Convaincre et influencer les autres",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 100, 250, 500, 1000],
                        "unlocked": true,
                        "prerequisites": [],
                        "effects": {
                            "mission_success_rate": [0, 0.05, 0.10, 0.15, 0.20],
                            "dialogue_options": [0, 1, 2, 3, 4]
                        }
                    },
                    "negotiation": {
                        "name": "Négociation",
                        "description": "Négocier des accords et des compromis",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 150, 350, 700, 1400],
                        "unlocked": false,
                        "prerequisites": ["persuasion"],
                        "effects": {
                            "mission_success_rate": [0, 0.08, 0.15, 0.22, 0.30],
                            "reward_bonus": [0, 0.1, 0.2, 0.3, 0.4]
                        }
                    },
                    "leadership": {
                        "name": "Leadership",
                        "description": "Diriger et motiver les équipes",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 200, 450, 900, 1800],
                        "unlocked": false,
                        "prerequisites": ["persuasion", "negotiation"],
                        "effects": {
                            "mission_success_rate": [0, 0.10, 0.20, 0.30, 0.40],
                            "team_efficiency": [0, 0.15, 0.30, 0.45, 0.60]
                        }
                    },
                    "diplomacy": {
                        "name": "Diplomatie",
                        "description": "Gérer les relations complexes",
                        "level": 0,
                        "max_level": 5,
                        "xp_required": [0, 120, 280, 560, 1120],
                        "unlocked": false,
                        "prerequisites": ["negotiation"],
                        "effects": {
                            "mission_success_rate": [0, 0.06, 0.12, 0.18, 0.25],
                            "conflict_resolution": [0, 0.2, 0.4, 0.6, 0.8]
                        }
                    }
                }
            }
        };
    }

    loadPlayerSkills() {
        // Charger les compétences du joueur depuis le localStorage ou l'API
        const saved = localStorage.getItem('arkalia_player_skills');
        if (saved) {
            try {
                this.playerSkills = JSON.parse(saved);
            } catch (e) {
                console.error('Erreur chargement compétences:', e);
                this.playerSkills = {};
            }
        }
    }

    savePlayerSkills() {
        localStorage.setItem('arkalia_player_skills', JSON.stringify(this.playerSkills));
    }

    setupEventListeners() {
        // Écouter les événements de progression
        document.addEventListener('arkalia:progression:update', (e) => {
            if (e.detail.type === 'skill_xp_gained') {
                this.gainSkillXP(e.detail.skill_category, e.detail.skill_id, e.detail.xp);
            }
        });
    }

    createSkillTreeUI() {
        // Vérifier si on est sur la page dédiée
        if (window.location.pathname === '/skill-tree') {
            this.createDedicatedPageUI();
        } else {
            this.createModalUI();
        }
    }

    createDedicatedPageUI() {
        // Créer l'interface pour la page dédiée
        const skillTreeGrid = document.getElementById('skill-tree-grid');
        if (skillTreeGrid) {
            // Vider le contenu existant
            skillTreeGrid.innerHTML = '';

            // Créer les catégories de compétences
            const categoriesHTML = Object.entries(this.skillTree).map(([categoryId, category]) =>
                this.createCategorySection(categoryId, category)
            ).join('');

            skillTreeGrid.innerHTML = categoriesHTML;

            // Ajouter les événements
            skillTreeGrid.addEventListener('click', (e) => {
                if (e.target.classList.contains('upgrade-skill') || e.target.closest('.upgrade-skill')) {
                    const button = e.target.classList.contains('upgrade-skill') ? e.target : e.target.closest('.upgrade-skill');
                    const skillId = button.dataset.skillId;
                    const categoryId = button.dataset.categoryId;
                    this.upgradeSkill(categoryId, skillId);
                }
            });

            // Mettre à jour les statistiques
            this.updatePlayerStats();

            console.log('🌳 Interface dédiée créée avec succès');
        } else {
            console.error('❌ Élément skill-tree-grid non trouvé');
        }
    }

    createModalUI() {
        // Créer l'interface modale pour les autres pages
        const skillTreeContainer = document.createElement('div');
        skillTreeContainer.id = 'skill-tree-container';
        skillTreeContainer.className = 'skill-tree-container';

        skillTreeContainer.innerHTML = `
            <div class="skill-tree-header">
                <h2>🌳 Arbre de Compétences</h2>
                <button class="close-skill-tree">&times;</button>
            </div>
            <div class="skill-tree-content">
                ${Object.entries(this.skillTree).map(([categoryId, category]) =>
            this.createCategorySection(categoryId, category)
        ).join('')}
            </div>
        `;

        // Ajouter les styles
        this.addSkillTreeStyles();

        // Événements
        skillTreeContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('close-skill-tree')) {
                this.hideSkillTree();
            } else if (e.target.classList.contains('upgrade-skill')) {
                const skillId = e.target.dataset.skillId;
                const categoryId = e.target.dataset.categoryId;
                this.upgradeSkill(categoryId, skillId);
            }
        });

        document.body.appendChild(skillTreeContainer);
    }

    createCategorySection(categoryId, category) {
        return `
            <div class="skill-category" data-category="${categoryId}">
                <div class="category-header">
                    <div class="category-icon">${category.icon}</div>
                    <div class="category-info">
                        <h3 class="category-title">${category.name}</h3>
                        <p class="category-description">${category.description}</p>
                    </div>
                </div>
                <div class="skills-list">
                    ${Object.entries(category.skills).map(([skillId, skill]) =>
            this.createSkillCard(categoryId, skillId, skill)
        ).join('')}
                </div>
            </div>
        `;
    }

    createSkillCard(categoryId, skillId, skill) {
        const playerSkill = this.playerSkills[categoryId]?.[skillId] || { level: 0, xp: 0 };
        const canUpgrade = this.canUpgradeSkill(categoryId, skillId);
        const isUnlocked = this.isSkillUnlocked(categoryId, skillId);
        const upgradeCost = this.getUpgradeCost(categoryId, skillId);
        const currentXP = this.getPlayerTotalXP();

        return `
            <div class="skill-item ${isUnlocked ? 'unlocked' : 'locked'} ${playerSkill.level > 0 ? 'active' : ''}" 
                 data-category="${categoryId}" data-skill="${skillId}">
                <div class="skill-name">${skill.name}</div>
                <div class="skill-description">${skill.description}</div>
                <div class="skill-level">Niveau ${playerSkill.level}/${skill.max_level}</div>
                <div class="skill-cost">${upgradeCost} XP</div>
                <div class="skill-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${this.getSkillProgress(categoryId, skillId)}%"></div>
                    </div>
                    <div class="progress-text">${playerSkill.xp}/${upgradeCost} XP</div>
                </div>
                ${canUpgrade ?
                `<button class="upgrade-skill" data-category="${categoryId}" data-skill="${skillId}">
                        <span class="upgrade-icon">⚡</span>
                        <span class="upgrade-text">Améliorer</span>
                        <span class="upgrade-cost">${upgradeCost} XP</span>
                    </button>` :
                `<div class="upgrade-unavailable">
                        ${playerSkill.level >= skill.max_level ? 'Max niveau' : 'Prérequis non remplis'}
                    </div>`
            }
            </div>
        `;
    }

    addSkillTreeStyles() {
        if (document.getElementById('skill-tree-styles')) return;

        const style = document.createElement('style');
        style.id = 'skill-tree-styles';
        style.textContent = `
            .skill-tree-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                display: flex;
                flex-direction: column;
                z-index: 10000;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }

            .skill-tree-container.show {
                opacity: 1;
                visibility: visible;
            }

            .skill-tree-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px;
                background: rgba(9, 9, 11, 0.95);
                border-bottom: 2px solid rgba(167, 139, 250, 0.5);
            }

            .skill-tree-header h2 {
                margin: 0;
                color: var(--violet-lunaire);
                font-family: 'IBM Plex Mono', monospace;
            }

            .close-skill-tree {
                background: none;
                border: none;
                color: var(--argent-holographique);
                font-size: 1.5em;
                cursor: pointer;
                padding: 5px;
                border-radius: 4px;
                transition: all 0.2s ease;
            }

            .close-skill-tree:hover {
                background: rgba(167, 139, 250, 0.2);
                color: var(--violet-lunaire);
            }

            .skill-tree-content {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }

            .skill-category {
                margin-bottom: 30px;
                background: rgba(167, 139, 250, 0.05);
                border: 1px solid rgba(167, 139, 250, 0.2);
                border-radius: 12px;
                padding: 20px;
            }

            .category-header {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
            }

            .category-icon {
                font-size: 2em;
                margin-right: 15px;
            }

            .category-info h3 {
                margin: 0 0 5px 0;
                color: var(--argent-holographique);
                font-family: 'IBM Plex Mono', monospace;
            }

            .category-info p {
                margin: 0;
                color: var(--argent-holographique);
                opacity: 0.8;
            }

            .skills-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 15px;
            }

            .skill-card {
                background: rgba(9, 9, 11, 0.8);
                border: 2px solid rgba(167, 139, 250, 0.3);
                border-radius: 8px;
                padding: 15px;
                transition: all 0.3s ease;
            }

            .skill-card.unlocked {
                border-color: rgba(34, 197, 94, 0.5);
            }

            .skill-card.active {
                border-color: var(--violet-lunaire);
                box-shadow: 0 0 20px rgba(167, 139, 250, 0.3);
            }

            .skill-card.locked {
                opacity: 0.5;
                border-color: rgba(107, 114, 128, 0.3);
            }

            .skill-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }

            .skill-header h4 {
                margin: 0;
                color: var(--argent-holographique);
                font-family: 'IBM Plex Mono', monospace;
            }

            .skill-level {
                color: var(--violet-lunaire);
                font-weight: 600;
                font-size: 0.9em;
            }

            .skill-description {
                color: var(--argent-holographique);
                opacity: 0.8;
                font-size: 0.9em;
                margin-bottom: 15px;
            }

            .skill-progress {
                margin-bottom: 15px;
            }

            .progress-bar {
                width: 100%;
                height: 6px;
                background: rgba(167, 139, 250, 0.2);
                border-radius: 3px;
                overflow: hidden;
                margin-bottom: 5px;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--violet-lunaire), var(--bleu-spectre));
                border-radius: 3px;
                transition: width 0.3s ease;
            }

            .progress-text {
                color: var(--argent-holographique);
                font-size: 0.8em;
                text-align: center;
            }

            .skill-effects {
                margin-bottom: 15px;
            }

            .skill-effects h5 {
                margin: 0 0 5px 0;
                color: var(--violet-lunaire);
                font-size: 0.9em;
            }

            .skill-effects ul {
                margin: 0;
                padding-left: 15px;
                color: var(--argent-holographique);
                font-size: 0.8em;
            }

            .skill-actions {
                text-align: center;
            }

            .upgrade-skill {
                background: linear-gradient(135deg, #00ff00, #00cc00);
                color: #000;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 700;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 15px rgba(0, 255, 0, 0.3);
                position: relative;
                overflow: hidden;
            }

            .upgrade-skill::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                transition: left 0.5s ease;
            }

            .upgrade-skill:hover::before {
                left: 100%;
            }

            .upgrade-skill:hover {
                background: linear-gradient(135deg, #00cc00, #00ff00);
                transform: translateY(-2px) scale(1.05);
                box-shadow: 0 6px 20px rgba(0, 255, 0, 0.5);
            }

            .upgrade-skill:active {
                transform: translateY(0) scale(0.98);
            }

            .upgrade-icon {
                font-size: 1.2em;
                animation: pulse 2s infinite;
            }

            .upgrade-text {
                font-size: 0.9em;
            }

            .upgrade-cost {
                font-size: 0.8em;
                opacity: 0.8;
            }

            .upgrade-unavailable {
                color: #6b7280;
                font-size: 0.9em;
                text-align: center;
                padding: 8px;
                background: rgba(100, 100, 100, 0.1);
                border-radius: 6px;
            }

            .skill-item.upgrading {
                animation: upgradePulse 1s ease-in-out;
                border-color: #00ff00 !important;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
            }

            @keyframes upgradePulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }

            .skill-progress {
                margin: 10px 0;
            }

            .progress-bar {
                width: 100%;
                height: 8px;
                background: rgba(0, 255, 0, 0.2);
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 5px;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #00ff00, #00cc00);
                border-radius: 4px;
                transition: width 0.5s ease;
            }

            .progress-text {
                color: #00ff00;
                font-size: 0.8em;
                text-align: center;
                font-family: 'IBM Plex Mono', monospace;
            }
        `;

        document.head.appendChild(style);
    }

    show() {
        // Rediriger vers la page dédiée
        window.location.href = '/skill-tree';
    }

    showSkillTree() {
        const container = document.getElementById('skill-tree-container');
        if (container) {
            container.classList.add('show');
            this.updateSkillTreeDisplay();
        }
    }

    hideSkillTree() {
        const container = document.getElementById('skill-tree-container');
        if (container) {
            container.classList.remove('show');
        }
    }

    updateSkillTreeDisplay() {
        // Mettre à jour l'affichage de l'arbre de compétences
        const container = document.getElementById('skill-tree-container');
        if (container) {
            container.innerHTML = `
                <div class="skill-tree-header">
                    <h2>🌳 Arbre de Compétences</h2>
                    <button class="close-skill-tree">&times;</button>
                </div>
                <div class="skill-tree-content">
                    ${Object.entries(this.skillTree).map(([categoryId, category]) =>
                this.createCategorySection(categoryId, category)
            ).join('')}
                </div>
            `;

            // Re-attacher les événements
            container.addEventListener('click', (e) => {
                if (e.target.classList.contains('close-skill-tree')) {
                    this.hideSkillTree();
                } else if (e.target.classList.contains('upgrade-skill')) {
                    const skillId = e.target.dataset.skillId;
                    const categoryId = e.target.dataset.categoryId;
                    this.upgradeSkill(categoryId, skillId);
                }
            });
        }
    }

    canUpgradeSkill(categoryId, skillId) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        if (!skill) return false;

        const playerSkill = this.playerSkills[categoryId]?.[skillId] || { level: 0, xp: 0 };

        // Vérifier si le niveau max est atteint
        if (playerSkill.level >= skill.max_level) return false;

        // Vérifier si les prérequis sont remplis
        for (const prereq of skill.prerequisites) {
            const prereqSkill = this.playerSkills[categoryId]?.[prereq];
            if (!prereqSkill || prereqSkill.level === 0) return false;
        }

        // Vérifier si le joueur a assez d'XP (utiliser les données synchronisées)
        const requiredXP = skill.xp_required[playerSkill.level + 1] || skill.xp_required[playerSkill.level];
        const playerXP = this.getPlayerTotalXP();

        // Si pas d'XP local, vérifier avec les données du serveur
        if (playerXP === 0) {
            // Récupérer les données de progression depuis le serveur
            this.syncPlayerData();
            return false; // Retourner false pour l'instant, sera mis à jour après sync
        }

        return playerXP >= requiredXP;
    }

    isSkillUnlocked(categoryId, skillId) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        if (!skill) return false;

        // Vérifier les prérequis
        for (const prereq of skill.prerequisites) {
            const prereqSkill = this.playerSkills[categoryId]?.[prereq];
            if (!prereqSkill || prereqSkill.level === 0) return false;
        }

        return true;
    }

    getSkillProgress(categoryId, skillId) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const playerSkill = this.playerSkills[categoryId]?.[skillId] || { level: 0, xp: 0 };

        if (!skill || playerSkill.level >= skill.max_level) return 100;

        const currentLevelXP = skill.xp_required[playerSkill.level] || 0;
        const nextLevelXP = skill.xp_required[playerSkill.level + 1] || skill.xp_required[playerSkill.level] || 100;
        const progress = (playerSkill.xp - currentLevelXP) / (nextLevelXP - currentLevelXP) * 100;

        return Math.max(0, Math.min(100, progress));
    }

    getNextLevelXP(categoryId, skillId) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const playerSkill = this.playerSkills[categoryId]?.[skillId] || { level: 0, xp: 0 };

        if (!skill || playerSkill.level >= skill.max_level) return 0;

        return skill.xp_required[playerSkill.level + 1] || skill.xp_required[playerSkill.level] || 100;
    }

    getUpgradeCost(categoryId, skillId) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const playerSkill = this.playerSkills[categoryId]?.[skillId] || { level: 0, xp: 0 };

        if (!skill || playerSkill.level >= skill.max_level) return 0;

        return skill.xp_required[playerSkill.level + 1] || skill.xp_required[playerSkill.level] || 100;
    }

    getSkillEffectsText(categoryId, skillId, level) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        if (!skill || level === 0) return '';

        const effects = skill.effects;
        let text = '<h5>Effets actifs:</h5><ul>';

        for (const [effectName, values] of Object.entries(effects)) {
            const value = values[level] || 0;
            if (value > 0) {
                const effectText = this.getEffectDisplayName(effectName);
                text += `<li>${effectText}: +${(value * 100).toFixed(0)}%</li>`;
            }
        }

        text += '</ul>';
        return text;
    }

    getEffectDisplayName(effectName) {
        const names = {
            'mission_success_rate': 'Taux de succès des missions',
            'hacking_speed': 'Vitesse de hacking',
            'stealth_bonus': 'Bonus de furtivité',
            'decryption_speed': 'Vitesse de décryptage',
            'social_bonus': 'Bonus social',
            'damage_reduction': 'Réduction de dégâts',
            'attack_power': 'Puissance d\'attaque',
            'team_bonus': 'Bonus d\'équipe',
            'critical_hit': 'Coup critique',
            'dialogue_options': 'Options de dialogue',
            'reward_bonus': 'Bonus de récompenses',
            'team_efficiency': 'Efficacité d\'équipe',
            'conflict_resolution': 'Résolution de conflits'
        };
        return names[effectName] || effectName;
    }

    async upgradeSkill(categoryId, skillId) {
        if (!this.canUpgradeSkill(categoryId, skillId)) {
            this.showUpgradeError('Prérequis non remplis ou XP insuffisant');
            return;
        }

        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const requiredXP = this.getUpgradeCost(categoryId, skillId);

        try {
            // Envoyer la requête au serveur
            const response = await fetch('/api/skill-tree/upgrade', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: categoryId,
                    skill: skillId
                })
            });

            const result = await response.json();

            if (result.success) {
                // Mettre à jour localement avec les données du serveur
                if (!this.playerSkills[categoryId]) {
                    this.playerSkills[categoryId] = {};
                }
                if (!this.playerSkills[categoryId][skillId]) {
                    this.playerSkills[categoryId][skillId] = { level: 0, xp: 0 };
                }

                const oldLevel = this.playerSkills[categoryId][skillId].level;
                this.playerSkills[categoryId][skillId].level = result.new_level;
                this.playerSkills[categoryId][skillId].xp = result.remaining_xp || 0;

                // Sauvegarder
                this.savePlayerSkills();

                // Effet visuel d'amélioration
                this.showUpgradeAnimation(categoryId, skillId, oldLevel, result.new_level);

                // Mettre à jour l'affichage
                if (window.location.pathname === '/skill-tree') {
                    this.createDedicatedPageUI();
                    this.updatePlayerStats();
                } else {
                    this.updateSkillTreeDisplay();
                }

                // Notification avec effet sonore
                this.showUpgradeNotification(skill.name, result.new_level);

                // Afficher les confettis si c'est un level up
                if (result.level_up) {
                    this.showLevelUpConfetti();
                    this.showNotification(`🎉 LEVEL UP ! Vous êtes maintenant niveau ${result.new_player_level} !`, 'success');
                }

                // Déclencher un événement personnalisé
                this.triggerUpgradeEvent(categoryId, skillId, result.new_level);

                // Synchroniser avec les autres modules
                this.syncWithOtherModules();
            } else {
                this.showNotification(result.error || 'Erreur lors de l\'amélioration', 'error');
            }
        } catch (error) {
            console.error('Erreur upgrade skill:', error);
            this.showNotification('Erreur de connexion', 'error');
        }
    }

    updatePlayerStats() {
        // Mettre à jour les statistiques affichées
        const totalSkills = this.getTotalSkills();
        const skillPoints = this.getPlayerTotalXP();
        const hackingLevel = this.getCategoryLevel('hacking');
        const combatLevel = this.getCategoryLevel('combat');
        const socialLevel = this.getCategoryLevel('social');

        const totalSkillsEl = document.getElementById('total-skills');
        const skillPointsEl = document.getElementById('skill-points');
        const hackingLevelEl = document.getElementById('hacking-level');
        const combatLevelEl = document.getElementById('combat-level');
        const socialLevelEl = document.getElementById('social-level');

        if (totalSkillsEl) totalSkillsEl.textContent = totalSkills;
        if (skillPointsEl) skillPointsEl.textContent = skillPoints;
        if (hackingLevelEl) hackingLevelEl.textContent = hackingLevel;
        if (combatLevelEl) combatLevelEl.textContent = combatLevel;
        if (socialLevelEl) socialLevelEl.textContent = socialLevel;
    }

    getTotalSkills() {
        let total = 0;
        for (const categorySkills of Object.values(this.playerSkills)) {
            for (const skill of Object.values(categorySkills)) {
                total += skill.level;
            }
        }
        return total;
    }

    getCategoryLevel(categoryId) {
        const categorySkills = this.playerSkills[categoryId] || {};
        let totalLevel = 0;
        for (const skill of Object.values(categorySkills)) {
            totalLevel += skill.level;
        }
        return totalLevel;
    }

    showUpgradeAnimation(categoryId, skillId, oldLevel, newLevel) {
        // Trouver l'élément de la compétence
        const skillElement = document.querySelector(`[data-category="${categoryId}"][data-skill="${skillId}"]`);
        if (!skillElement) return;

        // Animation de pulsation
        skillElement.classList.add('upgrade-success');

        // Effet de particules
        this.createParticleEffect(skillElement);

        // Animation du niveau
        const levelElement = skillElement.querySelector('.skill-level');
        if (levelElement) {
            levelElement.style.transform = 'scale(1.3)';
            levelElement.style.color = '#00ff00';
            levelElement.style.textShadow = '0 0 20px #00ff00';
            setTimeout(() => {
                levelElement.style.transform = 'scale(1)';
                levelElement.style.color = '';
                levelElement.style.textShadow = '';
            }, 800);
        }

        // Animation du bouton d'amélioration
        const upgradeButton = skillElement.querySelector('.upgrade-skill');
        if (upgradeButton) {
            upgradeButton.style.transform = 'scale(1.1)';
            upgradeButton.style.boxShadow = '0 0 30px rgba(0, 255, 0, 0.8)';
            setTimeout(() => {
                upgradeButton.style.transform = 'scale(1)';
                upgradeButton.style.boxShadow = '';
            }, 600);
        }

        // Effet de brillance
        this.createShineEffect(skillElement);

        // Retirer la classe après l'animation
        setTimeout(() => {
            skillElement.classList.remove('upgrade-success');
        }, 1200);
    }

    createShineEffect(element) {
        const shine = document.createElement('div');
        shine.style.cssText = `
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            animation: shine 0.8s ease-in-out;
            pointer-events: none;
            z-index: 10;
        `;

        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(shine);

        // Ajouter l'animation CSS si elle n'existe pas
        if (!document.getElementById('shine-animation')) {
            const style = document.createElement('style');
            style.id = 'shine-animation';
            style.textContent = `
                @keyframes shine {
                    0% { left: -100%; }
                    100% { left: 100%; }
                }
            `;
            document.head.appendChild(style);
        }

        setTimeout(() => {
            if (shine.parentNode) {
                shine.parentNode.removeChild(shine);
            }
        }, 800);
    }

    createParticleEffect(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < 8; i++) {
            const particle = document.createElement('div');
            particle.className = 'skill-particle';
            particle.style.position = 'fixed';
            particle.style.left = centerX + 'px';
            particle.style.top = centerY + 'px';
            particle.style.width = '4px';
            particle.style.height = '4px';
            particle.style.background = '#00ff00';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = '10000';

            document.body.appendChild(particle);

            // Animation de la particule
            const angle = (i / 8) * Math.PI * 2;
            const distance = 50 + Math.random() * 30;
            const endX = centerX + Math.cos(angle) * distance;
            const endY = centerY + Math.sin(angle) * distance;

            particle.animate([
                { transform: 'translate(0, 0) scale(1)', opacity: 1 },
                { transform: `translate(${endX - centerX}px, ${endY - centerY}px) scale(0)`, opacity: 0 }
            ], {
                duration: 800,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            }).onfinish = () => {
                particle.remove();
            };
        }
    }

    showUpgradeNotification(skillName, level) {
        // Notification visuelle
        if (window.universalNotifications) {
            window.universalNotifications.celebration(
                '🌟 Compétence Améliorée !',
                `${skillName} niveau ${level}`,
                {
                    duration: 4000,
                    sound: 'success',
                    animation: 'bounce'
                }
            );
        }

        // Effet sonore (si disponible)
        this.playUpgradeSound();
    }

    showUpgradeError(message) {
        if (window.universalNotifications) {
            window.universalNotifications.error(
                '❌ Impossible d\'améliorer',
                message,
                { duration: 3000 }
            );
        }
    }

    playUpgradeSound() {
        // Créer un son de succès simple
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.1);
        oscillator.frequency.setValueAtTime(1200, audioContext.currentTime + 0.2);

        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    }

    triggerUpgradeEvent(categoryId, skillId, level) {
        // Déclencher un événement personnalisé pour d'autres systèmes
        const event = new CustomEvent('arkalia:skill:upgraded', {
            detail: {
                category: categoryId,
                skill: skillId,
                level: level,
                timestamp: Date.now()
            }
        });
        document.dispatchEvent(event);
    }

    showLevelUpConfetti() {
        // Créer des confettis pour le level up
        const confettiContainer = document.createElement('div');
        confettiContainer.style.position = 'fixed';
        confettiContainer.style.top = '0';
        confettiContainer.style.left = '0';
        confettiContainer.style.width = '100%';
        confettiContainer.style.height = '100%';
        confettiContainer.style.pointerEvents = 'none';
        confettiContainer.style.zIndex = '9999';
        confettiContainer.id = 'confetti-container';

        document.body.appendChild(confettiContainer);

        // Créer des confettis
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'absolute';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = ['#00ff00', '#ff00ff', '#ffff00', '#00ffff', '#ff8000'][Math.floor(Math.random() * 5)];
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.top = '-10px';
            confetti.style.borderRadius = '50%';
            confetti.style.animation = `confettiFall ${2 + Math.random() * 3}s linear forwards`;

            confettiContainer.appendChild(confetti);
        }

        // Ajouter l'animation CSS
        if (!document.getElementById('confetti-style')) {
            const style = document.createElement('style');
            style.id = 'confetti-style';
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

        // Supprimer les confettis après 5 secondes
        setTimeout(() => {
            if (confettiContainer.parentNode) {
                confettiContainer.parentNode.removeChild(confettiContainer);
            }
        }, 5000);
    }

    syncWithOtherModules() {
        // Synchroniser avec les autres modules du jeu
        fetch('/api/sync-progression')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Déclencher un événement de synchronisation
                    const event = new CustomEvent('arkalia:progression:synced', {
                        detail: data.player_data
                    });
                    document.dispatchEvent(event);
                }
            })
            .catch(error => {
                console.log('Erreur synchronisation:', error);
            });
    }

    syncWithTerminal() {
        // Synchroniser avec le terminal pour récupérer l'XP
        this.fetchTerminalXP();

        // Écouter les événements du terminal
        document.addEventListener('arkalia:terminal:xp_gained', (e) => {
            if (e.detail && e.detail.category && e.detail.skill_id && e.detail.xp) {
                this.gainSkillXP(e.detail.category, e.detail.skill_id, e.detail.xp);
            }
        });
    }

    async fetchTerminalXP() {
        try {
            // Récupérer l'XP depuis le terminal
            const response = await fetch('/api/terminal/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: 'skill_tree' })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.data && data.data.message) {
                    // Parser le message pour extraire l'XP
                    this.parseTerminalXP(data.data.message);
                }
            }
        } catch (error) {
            console.log('Impossible de synchroniser avec le terminal:', error);
        }
    }

    parseTerminalXP(message) {
        // Parser le message du terminal pour extraire l'XP
        // Cette méthode peut être améliorée selon le format du message
        const xpMatch = message.match(/(\d+)\s*XP/);
        if (xpMatch) {
            const xp = parseInt(xpMatch[1]);
            // Distribuer l'XP entre les compétences
            this.distributeXP(xp);
        }
    }

    distributeXP(totalXP) {
        // Distribuer l'XP entre les compétences de hacking
        const hackingSkills = ['code_breaking', 'system_penetration', 'cryptography', 'social_engineering'];
        const xpPerSkill = Math.floor(totalXP / hackingSkills.length);

        for (const skillId of hackingSkills) {
            this.gainSkillXP('hacking', skillId, xpPerSkill);
        }
    }

    gainSkillXP(categoryId, skillId, xp) {
        // Initialiser la catégorie si nécessaire
        if (!this.playerSkills[categoryId]) {
            this.playerSkills[categoryId] = {};
        }

        // Initialiser la compétence si nécessaire
        if (!this.playerSkills[categoryId][skillId]) {
            this.playerSkills[categoryId][skillId] = { level: 0, xp: 0 };
        }

        // Ajouter l'XP
        this.playerSkills[categoryId][skillId].xp += xp;

        // Vérifier si on peut améliorer
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        if (skill) {
            const currentLevel = this.playerSkills[categoryId][skillId].level;
            if (currentLevel < skill.max_level) {
                const nextLevelXP = skill.xp_required[currentLevel + 1];
                if (this.playerSkills[categoryId][skillId].xp >= nextLevelXP) {
                    const oldLevel = this.playerSkills[categoryId][skillId].level;
                    this.playerSkills[categoryId][skillId].level++;
                    this.playerSkills[categoryId][skillId].xp = nextLevelXP;

                    // Effet visuel d'amélioration automatique
                    this.showUpgradeAnimation(categoryId, skillId, oldLevel, this.playerSkills[categoryId][skillId].level);

                    // Notification d'amélioration automatique
                    this.showUpgradeNotification(skill.name, this.playerSkills[categoryId][skillId].level);

                    // Déclencher un événement
                    this.triggerUpgradeEvent(categoryId, skillId, this.playerSkills[categoryId][skillId].level);
                }
            }
        }

        // Sauvegarder
        this.savePlayerSkills();

        // Mettre à jour l'affichage si on est sur la page
        if (window.location.pathname === '/skill-tree') {
            this.updatePlayerStats();
            this.createDedicatedPageUI();
        }
    }

    getPlayerTotalXP() {
        // Utiliser l'XP total du joueur depuis les données synchronisées
        if (this.playerTotalXP !== undefined) {
            return this.playerTotalXP;
        }

        // Fallback : calculer l'XP total du joueur
        let totalXP = 0;
        for (const categorySkills of Object.values(this.playerSkills)) {
            for (const skill of Object.values(categorySkills)) {
                totalXP += skill.xp;
            }
        }
        return totalXP;
    }

    getSkillBonus(categoryId, skillId, effectName) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const playerSkill = this.playerSkills[categoryId]?.[skillId];

        if (!skill || !playerSkill || !skill.effects[effectName]) return 0;

        const level = playerSkill.level;
        return skill.effects[effectName][level] || 0;
    }
}

// Initialiser le système
document.addEventListener('DOMContentLoaded', () => {
    window.skillTreeSystem = new SkillTreeSystem();
    console.log('🌳 Skill Tree System initialisé globalement');
});

// Initialiser immédiatement si le DOM est déjà chargé
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.skillTreeSystem = new SkillTreeSystem();
    });
} else {
    window.skillTreeSystem = new SkillTreeSystem();
}

// Exporter pour utilisation globale
window.SkillTreeSystem = SkillTreeSystem;
