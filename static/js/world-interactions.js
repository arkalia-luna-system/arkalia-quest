/* ===== ARKALIA QUEST - WORLD INTERACTIONS ===== */
/* Système d'interactions pour la page Monde */

class WorldInteractions {
    constructor() {
        this.currentZone = 'training';
        this.playerPosition = { x: 45, y: 45 };
        this.zones = this.initializeZones();
        this.lunaMessages = this.initializeLunaMessages();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createStyles();
        this.initializeWorld();
        // console.log('🌍 World Interactions initialisé');
    }

    initializeZones() {
        return {
            terminal: {
                name: 'Terminal Central',
                description: 'Le cœur du système. Accède aux commandes principales et aux outils de hacking.',
                missions: 3,
                progress: 100,
                status: 'completed',
                icon: '⌨️',
                color: '#8b5cf6',
                missions_list: [
                    { title: 'Premier Contact', status: 'completed', description: 'Connexion initiale au système' },
                    { title: 'Commandes de Base', status: 'available', description: 'Apprends les commandes essentielles' },
                    { title: 'Hacking Avancé', status: 'locked', description: 'Techniques de hacking avancées' }
                ]
            },
            'cyber-city': {
                name: 'Cyber City',
                description: 'Une ville numérique où les données circulent comme des voitures. Infiltre les réseaux urbains.',
                missions: 5,
                progress: 60,
                status: 'available',
                icon: '🏙️',
                color: '#06b6d4',
                missions_list: [
                    { title: 'Infiltration Réseau', status: 'completed', description: 'Pénètre le réseau urbain' },
                    { title: 'Trafic de Données', status: 'available', description: 'Intercepte les communications' },
                    { title: 'Sécurité Urbaine', status: 'locked', description: 'Contourne les systèmes de sécurité' }
                ]
            },
            'data-center': {
                name: 'Data Center',
                description: 'Le centre de traitement des données. Ici, chaque bit compte et chaque accès est surveillé.',
                missions: 4,
                progress: 30,
                status: 'available',
                icon: '🏢',
                color: '#a855f7',
                missions_list: [
                    { title: 'Accès Sécurisé', status: 'available', description: 'Trouve un moyen d\'entrer' },
                    { title: 'Extraction de Données', status: 'locked', description: 'Récupère des informations sensibles' }
                ]
            },
            underground: {
                name: 'Underground',
                description: 'Les bas-fonds du cyberespace. Un endroit dangereux mais riche en secrets.',
                missions: 6,
                progress: 0,
                status: 'locked',
                icon: '🕳️',
                color: '#6366f1',
                missions_list: [
                    { title: 'Exploration', status: 'locked', description: 'Découvre les secrets cachés' }
                ]
            },
            training: {
                name: 'Zone d\'Entraînement',
                description: 'Parfait pour commencer. Ici, tu peux t\'exercer en toute sécurité.',
                missions: 2,
                progress: 100,
                status: 'completed',
                icon: '🎯',
                color: '#10b981',
                missions_list: [
                    { title: 'Exercices de Base', status: 'completed', description: 'Maîtrise les fondamentaux' },
                    { title: 'Défis Avancés', status: 'completed', description: 'Perfectionne tes compétences' }
                ]
            },
            quantum: {
                name: 'Quantum Lab',
                description: 'Le laboratoire quantique. Un endroit mystérieux où les lois de la physique sont différentes.',
                missions: 0,
                progress: 0,
                status: 'locked',
                icon: '⚛️',
                color: '#f59e0b',
                missions_list: [
                    { title: 'Découverte Quantique', status: 'locked', description: 'Explore les mystères quantiques' }
                ]
            }
        };
    }

    initializeLunaMessages() {
        return {
            welcome: [
                "🌙 Bienvenue dans le monde d'Arkalia ! Chaque zone cache ses secrets...",
                "🌙 Explore les zones pour découvrir de nouvelles missions et défis !",
                "🌙 Le monde d'Arkalia t'attend. Commence par cliquer sur une zone !"
            ],
            zone_selected: [
                "🌙 Excellente zone ! Cette région regorge de possibilités...",
                "🌙 Un choix judicieux ! Cette zone te réserve des surprises...",
                "🌙 Parfait ! Cette zone est idéale pour progresser..."
            ],
            zone_completed: [
                "🌙 Félicitations ! Tu as maîtrisé cette zone !",
                "🌙 Bravo ! Cette zone n'a plus de secrets pour toi !",
                "🌙 Excellent travail ! Tu progresses remarquablement !"
            ],
            zone_locked: [
                "🌙 Cette zone est verrouillée. Continue à explorer pour la débloquer !",
                "🌙 Patience... Cette zone se déverrouillera bientôt !",
                "🌙 Cette zone attend que tu sois plus expérimenté..."
            ],
            all_completed: [
                "🌙 Incroyable ! Tu as exploré tout ce qui est accessible !",
                "🌙 Bravo ! Tu es devenu un vrai maître d'Arkalia !",
                "🌙 Félicitations ! Reviens demain pour de nouveaux défis !"
            ]
        };
    }

    setupEventListeners() {
        // Écouter les clics sur les zones
        document.addEventListener('click', (e) => {
            if (e.target.closest('.zone')) {
                const zone = e.target.closest('.zone');
                const zoneId = zone.dataset.zone;
                this.selectZone(zoneId);
            }
        });

        // Écouter les clics sur les missions
        document.addEventListener('click', (e) => {
            if (e.target.closest('.mission-item')) {
                const mission = e.target.closest('.mission-item');
                this.selectMission(mission);
            }
        });

        // Écouter les clics sur les boutons de navigation
        document.addEventListener('click', (e) => {
            if (e.target.closest('.direction-btn')) {
                const btn = e.target.closest('.direction-btn');
                const direction = btn.onclick.toString().match(/movePlayer\('(\w+)'\)/)[1];
                this.movePlayer(direction);
            }
        });
    }

    createStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Animations d'interaction */
            .zone {
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .zone::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                transition: left 0.6s ease;
            }

            .zone:hover::before {
                left: 100%;
            }

            .zone.selected {
                border-color: var(--luna-cyan) !important;
                background: rgba(6, 182, 212, 0.3) !important;
                box-shadow: 0 0 40px rgba(6, 182, 212, 0.6) !important;
                transform: scale(1.1) !important;
            }

            .zone.completed.selected {
                border-color: var(--luna-success) !important;
                background: rgba(16, 185, 129, 0.3) !important;
                box-shadow: 0 0 40px rgba(16, 185, 129, 0.6) !important;
            }

            .zone.locked {
                cursor: not-allowed;
                opacity: 0.5;
            }

            .zone.locked:hover {
                transform: none !important;
                box-shadow: none !important;
            }

            /* Animations de récompense */
            .reward-animation {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10000;
                pointer-events: none;
            }

            .confetti {
                position: absolute;
                width: 10px;
                height: 10px;
                background: var(--luna-cyan);
                animation: confetti-fall 3s ease-out forwards;
            }

            @keyframes confetti-fall {
                0% {
                    transform: translateY(0) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(100vh) rotate(720deg);
                    opacity: 0;
                }
            }

            .mission-item {
                cursor: pointer;
                transition: all 0.3s ease;
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0;
            }

            .mission-item:hover {
                background: rgba(139, 92, 246, 0.1);
                transform: translateX(5px);
            }

            .mission-item.available {
                border-left: 4px solid var(--luna-cyan);
            }

            .mission-item.completed {
                border-left: 4px solid var(--luna-success);
                opacity: 0.7;
            }

            .mission-item.locked {
                border-left: 4px solid var(--luna-text-muted);
                opacity: 0.5;
            }

            /* Messages LUNA dynamiques */
            .luna-message {
                position: fixed;
                bottom: 20px;
                left: 20px;
                background: rgba(139, 92, 246, 0.1);
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 10px;
                padding: 15px;
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.9em;
                color: var(--luna-text);
                backdrop-filter: blur(10px);
                max-width: 350px;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s ease;
                z-index: 1000;
            }

            .luna-message.show {
                opacity: 1;
                transform: translateY(0);
            }

            .luna-message::before {
                content: '🌙 LUNA:';
                font-weight: bold;
                color: var(--luna-violet);
                margin-right: 8px;
            }

            /* Zone info dynamique */
            .zone-info-card {
                background: rgba(26, 26, 46, 0.9);
                border: 2px solid var(--luna-violet);
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
                backdrop-filter: blur(15px);
                animation: slideInUp 0.5s ease-out;
            }

            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .zone-title {
                font-size: 1.4em;
                font-weight: 600;
                color: var(--luna-violet);
                margin-bottom: 10px;
            }

            .zone-description {
                color: var(--luna-text-secondary);
                line-height: 1.6;
                margin-bottom: 15px;
            }

            .zone-stats {
                display: flex;
                gap: 20px;
                margin-bottom: 15px;
            }

            .zone-stat {
                text-align: center;
            }

            .zone-stat-value {
                font-size: 1.2em;
                font-weight: bold;
                color: var(--luna-cyan);
            }

            .zone-stat-label {
                font-size: 0.8em;
                color: var(--luna-text-muted);
            }

            /* Boutons d'action */
            .zone-action-btn {
                background: linear-gradient(135deg, var(--luna-violet), var(--luna-cyan));
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                margin: 5px;
            }

            .zone-action-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
            }

            .zone-action-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
        `;
        document.head.appendChild(style);
    }

    initializeWorld() {
        // Initialiser la zone par défaut
        this.selectZone('training');
        this.updateLunaMessage('welcome');

        // Animer l'entrée
        setTimeout(() => {
            document.querySelector('.world-title').style.animation = 'fadeInUp 1.5s ease-out forwards';
            document.querySelector('.world-subtitle').style.animation = 'fadeInUp 1.5s ease-out 0.3s forwards';
        }, 500);
    }

    selectZone(zoneId) {
        // Désélectionner toutes les zones
        document.querySelectorAll('.zone').forEach(zone => {
            zone.classList.remove('selected');
        });

        // Sélectionner la nouvelle zone
        const zoneElement = document.querySelector(`[data-zone="${zoneId}"]`);
        if (zoneElement) {
            zoneElement.classList.add('selected');
            this.currentZone = zoneId;
            this.updateZoneInfo(zoneId);
            this.updateMissions(zoneId);
            this.updatePlayerPosition(zoneId);

            // Effet sonore et visuel
            this.playZoneSound(zoneId);
            this.showZoneEffect(zoneElement);

            // Message LUNA
            const zone = this.zones[zoneId];
            if (zone.status === 'completed') {
                this.updateLunaMessage('zone_completed');
            } else if (zone.status === 'locked') {
                this.updateLunaMessage('zone_locked');
            } else {
                this.updateLunaMessage('zone_selected');
            }
        }
    }

    updateZoneInfo(zoneId) {
        const zone = this.zones[zoneId];
        const zoneDetails = document.getElementById('zone-details');

        zoneDetails.innerHTML = `
            <div class="zone-info-card">
                <div class="zone-title">${zone.icon} ${zone.name}</div>
                <div class="zone-description">${zone.description}</div>
                <div class="zone-stats">
                    <div class="zone-stat">
                        <div class="zone-stat-value">${zone.missions}</div>
                        <div class="zone-stat-label">Missions</div>
                    </div>
                    <div class="zone-stat">
                        <div class="zone-stat-value">${zone.progress}%</div>
                        <div class="zone-stat-label">Progression</div>
                    </div>
                    <div class="zone-stat">
                        <div class="zone-stat-value">${zone.status}</div>
                        <div class="zone-stat-label">Statut</div>
                    </div>
                </div>
                <div>
                    <button class="zone-action-btn" onclick="worldInteractions.exploreZone('${zoneId}')">
                        ${zone.status === 'locked' ? '🔒 Verrouillé' : '🔍 Explorer'}
                    </button>
                    ${zone.status === 'completed' ? '<button class="zone-action-btn" onclick="worldInteractions.celebrateZone(\'' + zoneId + '\')">🎉 Célébrer</button>' : ''}
                </div>
            </div>
        `;
    }

    updateMissions(zoneId) {
        const zone = this.zones[zoneId];
        const missionList = document.getElementById('mission-list');

        if (zone.missions_list.length === 0) {
            missionList.innerHTML = '<div class="zone-description">Aucune mission disponible dans cette zone.</div>';
            return;
        }

        missionList.innerHTML = `
            <h4 style="color: var(--luna-violet); margin-bottom: 15px;">Missions de ${zone.name}</h4>
            ${zone.missions_list.map(mission => `
                <div class="mission-item ${mission.status}" onclick="worldInteractions.selectMission('${zoneId}', '${mission.title}')">
                    <div style="font-weight: 600; color: var(--luna-text);">${mission.title}</div>
                    <div style="font-size: 0.9em; color: var(--luna-text-secondary);">${mission.description}</div>
                </div>
            `).join('')}
        `;
    }

    updatePlayerPosition(zoneId) {
        const zoneElement = document.querySelector(`[data-zone="${zoneId}"]`);
        if (zoneElement) {
            const rect = zoneElement.getBoundingClientRect();
            const mapRect = document.getElementById('world-map').getBoundingClientRect();

            const x = ((rect.left - mapRect.left + rect.width / 2) / mapRect.width) * 100;
            const y = ((rect.top - mapRect.top + rect.height / 2) / mapRect.height) * 100;

            const playerPosition = document.getElementById('player-position');
            playerPosition.style.left = x + '%';
            playerPosition.style.top = y + '%';

            // Animation de déplacement
            playerPosition.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
        }
    }

    exploreZone(zoneId) {
        const zone = this.zones[zoneId];
        if (zone.status === 'locked') {
            this.showNotification('Cette zone est verrouillée !', 'warning');
            return;
        }

        // Lancer un micro‑jeu simple selon la zone
        switch (zoneId) {
            case 'terminal':
                this.launchTerminalHack();
                break;
            case 'cyber-city':
            case 'cyber_city':
                this.launchDataMining();
                break;
            case 'data-center':
            case 'data_center':
                this.launchServerHack();
                break;
            case 'training':
                this.launchTrainingChallenge();
                break;
            case 'underground':
                this.launchStealthMission();
                break;
            case 'quantum':
                this.launchQuantumPuzzle();
                break;
            default:
                this.showNotification(`Exploration de ${zone.name}...`, 'info');
                setTimeout(() => {
                    this.showNotification(`Tu as découvert de nouvelles informations dans ${zone.name} !`, 'success');
                    this.createExplorationEffect();
                }, 2000);
        }
    }

    celebrateZone(zoneId) {
        const zone = this.zones[zoneId];
        this.showNotification(`🎉 Félicitations ! Tu as maîtrisé ${zone.name} !`, 'success');
        this.createConfettiEffect();
        this.updateLunaMessage('zone_completed');
    }

    selectMission(zoneId, missionTitle) {
        const zone = this.zones[zoneId];
        const mission = zone.missions_list.find(m => m.title === missionTitle);

        if (mission.status === 'locked') {
            this.showNotification('Cette mission est verrouillée !', 'warning');
            return;
        }

        if (mission.status === 'completed') {
            this.showNotification('Cette mission est déjà terminée !', 'info');
            return;
        }

        this.showNotification(`Mission "${missionTitle}" lancée !`, 'success');
        this.updateLunaMessage('zone_selected');
    }

    movePlayer(direction) {
        const directions = {
            up: { x: 0, y: -10 },
            down: { x: 0, y: 10 },
            left: { x: -10, y: 0 },
            right: { x: 10, y: 0 }
        };

        const delta = directions[direction];
        if (delta) {
            this.playerPosition.x = Math.max(0, Math.min(100, this.playerPosition.x + delta.x));
            this.playerPosition.y = Math.max(0, Math.min(100, this.playerPosition.y + delta.y));

            const playerPosition = document.getElementById('player-position');
            playerPosition.style.left = this.playerPosition.x + '%';
            playerPosition.style.top = this.playerPosition.y + '%';

            this.showNotification(`Déplacement vers ${direction.toUpperCase()}`, 'info');
        }
    }

    updateLunaMessage(type) {
        const messages = this.lunaMessages[type];
        if (messages && messages.length > 0) {
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            this.showLunaMessage(randomMessage);
        }
    }

    showLunaMessage(message) {
        // Supprimer l'ancien message
        const oldMessage = document.querySelector('.luna-message');
        if (oldMessage) {
            oldMessage.remove();
        }

        // Créer le nouveau message
        const messageElement = document.createElement('div');
        messageElement.className = 'luna-message';
        messageElement.textContent = message;
        document.body.appendChild(messageElement);

        // Afficher avec animation
        setTimeout(() => {
            messageElement.classList.add('show');
        }, 100);

        // Masquer après 5 secondes
        setTimeout(() => {
            messageElement.classList.remove('show');
            setTimeout(() => {
                messageElement.remove();
            }, 300);
        }, 5000);
    }

    showNotification(message, type = 'info') {
        // Créer une notification
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
        `;

        // Couleurs selon le type
        const colors = {
            success: 'background: linear-gradient(135deg, #10b981, #059669);',
            warning: 'background: linear-gradient(135deg, #f59e0b, #d97706);',
            info: 'background: linear-gradient(135deg, #06b6d4, #0891b2);',
            error: 'background: linear-gradient(135deg, #ef4444, #dc2626);'
        };

        notification.style.cssText += colors[type] || colors.info;
        document.body.appendChild(notification);

        // Supprimer après 3 secondes
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    createConfettiEffect() {
        const confettiContainer = document.createElement('div');
        confettiContainer.className = 'reward-animation';
        document.body.appendChild(confettiContainer);

        // Créer des confettis
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.background = ['#8b5cf6', '#06b6d4', '#a855f7', '#10b981', '#f59e0b'][Math.floor(Math.random() * 5)];
            confetti.style.animationDelay = Math.random() * 2 + 's';
            confettiContainer.appendChild(confetti);
        }

        // Supprimer après l'animation
        setTimeout(() => {
            confettiContainer.remove();
        }, 5000);
    }

    createExplorationEffect() {
        const effect = document.createElement('div');
        effect.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100px;
            height: 100px;
            border: 3px solid var(--luna-cyan);
            border-radius: 50%;
            z-index: 10000;
            animation: explorationPulse 1s ease-out;
        `;
        document.body.appendChild(effect);

        setTimeout(() => {
            effect.remove();
        }, 1000);
    }

    playZoneSound(zoneId) {
        // Simuler un son (dans une vraie implémentation, on utiliserait l'audio)
        // console.log(`🔊 Son de zone: ${zoneId}`);
    }

    showZoneEffect(zoneElement) {
        // Effet de surbrillance
        zoneElement.style.boxShadow = '0 0 50px rgba(139, 92, 246, 0.8)';
        setTimeout(() => {
            zoneElement.style.boxShadow = '';
        }, 1000);
    }

    // Nouvelles actions jouables pour les zones
    exploreZone(zoneId) {
        const zoneData = this.zones[zoneId];
        if (!zoneData) return;

        if (zoneData.status === 'locked') {
            this.showNotification('Cette zone est verrouillée. Progressez ailleurs pour la débloquer.', 'error');
            return;
        }

        this.launchZoneAction(zoneId, zoneData);
    }

    launchZoneAction(zoneId, zoneData) {
        const actions = {
            terminal: () => this.launchTerminalHack(),
            cyber_city: () => this.launchDataMining(),
            data_center: () => this.launchServerHack(),
            underground: () => this.launchStealthMission(),
            training: () => this.launchTrainingChallenge(),
            quantum: () => this.launchQuantumPuzzle()
        };

        if (actions[zoneId]) {
            actions[zoneId]();
        }
    }

    launchTerminalHack() {
        this.showActionModal('💻 HACK TERMINAL', 'Décodez le système de sécurité', () => {
            this.simulateHackSequence();
        });
    }

    launchDataMining() {
        this.showActionModal('🏙️ MINAGE DE DONNÉES', 'Extrayez des informations sensibles', () => {
            this.simulateDataMining();
        });
    }

    launchServerHack() {
        this.showActionModal('💾 HACK SERVEUR', 'Infiltrer le centre de données', () => {
            this.simulateServerHack();
        });
    }

    launchStealthMission() {
        this.showActionModal('🚇 MISSION FURTIVE', 'Naviguez dans les bas-fonds', () => {
            this.simulateStealthMission();
        });
    }

    launchTrainingChallenge() {
        this.showActionModal('💡 DÉFI D\'ENTRAÎNEMENT', 'Perfectionnez vos compétences', () => {
            this.simulateTrainingChallenge();
        });
    }

    launchQuantumPuzzle() {
        this.showActionModal('⚛️ PUZZLE QUANTIQUE', 'Résolvez l\'énigme quantique', () => {
            this.simulateQuantumPuzzle();
        });
    }

    showActionModal(title, description, onStart) {
        const modal = document.createElement('div');
        modal.className = 'zone-action-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>${title}</h3>
                <p>${description}</p>
                <div class="modal-actions">
                    <button class="btn-start">🚀 COMMENCER</button>
                    <button class="btn-cancel">❌ ANNULER</button>
                </div>
            </div>
        `;

        // Styles pour le modal
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;

        const content = modal.querySelector('.modal-content');
        content.style.cssText = `
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(30, 30, 40, 0.95) 100%);
            border: 2px solid var(--luna-violet, #8b5cf6);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            color: white;
            max-width: 400px;
            width: 90%;
        `;

        const actions = modal.querySelector('.modal-actions');
        actions.style.cssText = `
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 20px;
        `;

        const buttons = modal.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.style.cssText = `
                padding: 10px 20px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            `;
        });

        const startBtn = modal.querySelector('.btn-start');
        startBtn.style.cssText += `
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
            color: white;
        `;

        const cancelBtn = modal.querySelector('.btn-cancel');
        cancelBtn.style.cssText += `
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            color: white;
        `;

        document.body.appendChild(modal);

        // Événements
        startBtn.addEventListener('click', () => {
            modal.remove();
            onStart();
        });

        cancelBtn.addEventListener('click', () => {
            modal.remove();
        });

        // Fermer en cliquant sur l'overlay
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    simulateHackSequence() {
        this.showNotification('🔐 Séquence de hack en cours...', 'info');

        setTimeout(() => {
            this.showNotification('✅ Système hacké avec succès !', 'success');
            this.triggerRewardAnimation('Hack réussi ! +50 XP');
            this.addXP(50);
        }, 2000);
    }

    simulateDataMining() {
        this.showNotification('📊 Extraction de données...', 'info');

        setTimeout(() => {
            this.showNotification('💎 Données sensibles récupérées !', 'success');
            this.triggerRewardAnimation('Données extraites ! +75 XP');
            this.addXP(75);
        }, 2500);
    }

    simulateServerHack() {
        this.showNotification('🖥️ Infiltration du serveur...', 'info');

        setTimeout(() => {
            this.showNotification('🎯 Serveur compromis !', 'success');
            this.triggerRewardAnimation('Serveur hacké ! +100 XP');
            this.addXP(100);
        }, 3000);
    }

    simulateStealthMission() {
        this.showNotification('🥷 Mission furtive en cours...', 'info');

        setTimeout(() => {
            this.showNotification('👻 Mission accomplie sans être détecté !', 'success');
            this.triggerRewardAnimation('Mission furtive réussie ! +125 XP');
            this.addXP(125);
        }, 3500);
    }

    simulateTrainingChallenge() {
        this.showNotification('💪 Défi d\'entraînement...', 'info');

        setTimeout(() => {
            this.showNotification('🏆 Compétences améliorées !', 'success');
            this.triggerRewardAnimation('Entraînement terminé ! +25 XP');
            this.addXP(25);
        }, 1500);
    }

    simulateQuantumPuzzle() {
        this.showNotification('⚛️ Résolution du puzzle quantique...', 'info');

        setTimeout(() => {
            this.showNotification('🌟 Puzzle quantique résolu !', 'success');
            this.triggerRewardAnimation('Puzzle résolu ! +200 XP');
            this.addXP(200);
        }, 4000);
    }

    addXP(amount) {
        // Déclencher l'événement XP
        const event = new CustomEvent('xpGained', {
            detail: { amount: amount }
        });
        document.dispatchEvent(event);
    }
}

// Initialiser le système
document.addEventListener('DOMContentLoaded', () => {
    window.worldInteractions = new WorldInteractions();
});

// Exporter pour utilisation globale (onclick="movePlayer('up')" dans monde.html)
window.WorldInteractions = WorldInteractions;
window.movePlayer = function (direction) {
    if (window.worldInteractions && typeof window.worldInteractions.movePlayer === 'function') {
        window.worldInteractions.movePlayer(direction);
    }
};
