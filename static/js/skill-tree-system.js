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
        console.log('🌳 Skill Tree System initialisé');
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
        // Créer l'interface de l'arbre de compétences
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
                        <h3>${category.name}</h3>
                        <p>${category.description}</p>
                    </div>
                </div>
                <div class="skills-grid">
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

        return `
            <div class="skill-card ${isUnlocked ? 'unlocked' : 'locked'} ${playerSkill.level > 0 ? 'active' : ''}" 
                 data-category="${categoryId}" data-skill="${skillId}">
                <div class="skill-header">
                    <h4>${skill.name}</h4>
                    <div class="skill-level">Niveau ${playerSkill.level}/${skill.max_level}</div>
                </div>
                <div class="skill-description">${skill.description}</div>
                <div class="skill-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${this.getSkillProgress(categoryId, skillId)}%"></div>
                    </div>
                    <div class="progress-text">${playerSkill.xp}/${this.getNextLevelXP(categoryId, skillId)} XP</div>
                </div>
                <div class="skill-effects">
                    ${this.getSkillEffectsText(categoryId, skillId, playerSkill.level)}
                </div>
                <div class="skill-actions">
                    ${canUpgrade ?
                `<button class="upgrade-skill" data-category="${categoryId}" data-skill="${skillId}">
                            Améliorer (${this.getUpgradeCost(categoryId, skillId)} XP)
                        </button>` :
                '<span class="upgrade-unavailable">Prérequis non remplis</span>'
            }
                </div>
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
                background: var(--violet-lunaire);
                color: #000;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.2s ease;
            }

            .upgrade-skill:hover {
                background: var(--bleu-spectre);
                transform: scale(1.05);
            }

            .upgrade-unavailable {
                color: #6b7280;
                font-size: 0.9em;
            }
        `;

        document.head.appendChild(style);
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

        // Vérifier si le joueur a assez d'XP
        const requiredXP = skill.xp_required[playerSkill.level];
        const playerXP = this.getPlayerTotalXP();
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

        const currentLevelXP = skill.xp_required[playerSkill.level];
        const nextLevelXP = skill.xp_required[playerSkill.level + 1];
        const progress = (playerSkill.xp - currentLevelXP) / (nextLevelXP - currentLevelXP) * 100;

        return Math.max(0, Math.min(100, progress));
    }

    getNextLevelXP(categoryId, skillId) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const playerSkill = this.playerSkills[categoryId]?.[skillId] || { level: 0, xp: 0 };

        if (!skill || playerSkill.level >= skill.max_level) return 0;

        return skill.xp_required[playerSkill.level + 1];
    }

    getUpgradeCost(categoryId, skillId) {
        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const playerSkill = this.playerSkills[categoryId]?.[skillId] || { level: 0, xp: 0 };

        if (!skill || playerSkill.level >= skill.max_level) return 0;

        return skill.xp_required[playerSkill.level + 1];
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

    upgradeSkill(categoryId, skillId) {
        if (!this.canUpgradeSkill(categoryId, skillId)) return;

        const skill = this.skillTree[categoryId]?.skills?.[skillId];
        const requiredXP = this.getUpgradeCost(categoryId, skillId);

        // Initialiser la catégorie si nécessaire
        if (!this.playerSkills[categoryId]) {
            this.playerSkills[categoryId] = {};
        }

        // Initialiser la compétence si nécessaire
        if (!this.playerSkills[categoryId][skillId]) {
            this.playerSkills[categoryId][skillId] = { level: 0, xp: 0 };
        }

        // Améliorer la compétence
        this.playerSkills[categoryId][skillId].level++;
        this.playerSkills[categoryId][skillId].xp = requiredXP;

        // Sauvegarder
        this.savePlayerSkills();

        // Mettre à jour l'affichage
        this.updateSkillTreeDisplay();

        // Notification
        if (window.universalNotifications) {
            window.universalNotifications.success(
                '🌟 Compétence Améliorée !',
                `${skill.name} niveau ${this.playerSkills[categoryId][skillId].level}`,
                { duration: 3000 }
            );
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
                    this.playerSkills[categoryId][skillId].level++;
                    this.playerSkills[categoryId][skillId].xp = nextLevelXP;

                    // Notification d'amélioration automatique
                    if (window.universalNotifications) {
                        window.universalNotifications.celebration(
                            '🌟 Compétence Améliorée !',
                            `${skill.name} niveau ${this.playerSkills[categoryId][skillId].level}`,
                            { duration: 4000 }
                        );
                    }
                }
            }
        }

        // Sauvegarder
        this.savePlayerSkills();
    }

    getPlayerTotalXP() {
        // Calculer l'XP total du joueur
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
});

// Exporter pour utilisation globale
window.SkillTreeSystem = SkillTreeSystem;
