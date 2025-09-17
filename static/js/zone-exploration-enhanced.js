/* ===== ARKALIA QUEST - ZONE EXPLORATION ENHANCED ===== */
/* Amélioration de l'exploration des zones avec contenu narratif et mini-jeux */

class ZoneExplorationEnhanced {
    constructor() {
        this.currentZone = null;
        this.zoneData = this.initializeZoneData();
        this.explorationProgress = {};
        this.miniGames = {};
        this.init();
    }

    init() {
        this.setupZoneInteractions();
        this.initializeMiniGames();
        this.setupExplorationFeedback();
    }

    initializeZoneData() {
        return {
            'cyber-city': {
                name: 'Cyber City',
                description: 'Une ville numérique où les données circulent comme des voitures',
                narrative: {
                    entry: "🏙️ Bienvenue dans Cyber City ! Les néons clignotent, les données circulent dans les rues virtuelles. Tu sens l'énergie électrique de cette métropole numérique.",
                    exploration: "🔍 Tu explores les rues de données. Des fragments d'information flottent autour de toi. Chaque coin de rue révèle de nouveaux secrets.",
                    secrets: "💎 Tu découvres un terminal caché ! Il semble contenir des informations sensibles sur le réseau urbain.",
                    completion: "🎉 Excellent travail ! Tu as maîtrisé les secrets de Cyber City. La ville numérique t'appartient maintenant."
                },
                miniGames: ['data_traffic', 'network_infiltration', 'security_breach'],
                rewards: { xp: 150, coins: 75, badge: 'cyber_explorer' },
                secrets: 3,
                difficulty: 'medium'
            },
            'data-center': {
                name: 'Data Center',
                description: 'Le centre de traitement des données avec des serveurs puissants',
                narrative: {
                    entry: "🏢 Tu pénètres dans le Data Center. L'air est chargé d'électricité statique. Des serveurs géants bourdonnent autour de toi.",
                    exploration: "🔍 Tu navigues entre les racks de serveurs. Chaque machine contient des trésors de données. Attention aux systèmes de sécurité !",
                    secrets: "💎 Un serveur isolé attire ton attention. Il contient des archives classifiées !",
                    completion: "🎉 Impressionnant ! Tu as hacké les serveurs les plus sécurisés du Data Center."
                },
                miniGames: ['server_hack', 'data_extraction', 'firewall_breach'],
                rewards: { xp: 200, coins: 100, badge: 'data_master' },
                secrets: 4,
                difficulty: 'hard'
            },
            'underground': {
                name: 'Underground',
                description: 'Les bas-fonds numériques, dangereux mais riches en secrets',
                narrative: {
                    entry: "🕳️ Tu descends dans l'Underground. L'atmosphère est sombre et mystérieuse. Des ombres numériques rôdent dans les tunnels.",
                    exploration: "🔍 Tu explores les tunnels sombres. Chaque recoin peut cacher un secret ou un danger. Reste vigilant !",
                    secrets: "💎 Tu trouves une cache secrète ! Des artefacts numériques rares s'y trouvent.",
                    completion: "🎉 Tu es devenu le maître de l'Underground ! Les ombres te respectent maintenant."
                },
                miniGames: ['shadow_navigation', 'artifact_hunt', 'underground_escape'],
                rewards: { xp: 180, coins: 90, badge: 'underground_king' },
                secrets: 5,
                difficulty: 'hard'
            },
            'training': {
                name: 'Zone d\'Entraînement',
                description: 'Zone sécurisée pour perfectionner tes compétences',
                narrative: {
                    entry: "🎯 Bienvenue dans la zone d'entraînement ! Ici, tu peux pratiquer en toute sécurité.",
                    exploration: "🔍 Tu explores les différents modules d'entraînement. Chaque exercice te rend plus fort.",
                    secrets: "💎 Tu découvres un module d'entraînement avancé !",
                    completion: "🎉 Excellent ! Tu as maîtrisé tous les exercices d'entraînement."
                },
                miniGames: ['basic_hacking', 'command_practice', 'skill_test'],
                rewards: { xp: 100, coins: 50, badge: 'training_master' },
                secrets: 2,
                difficulty: 'easy'
            }
        };
    }

    setupZoneInteractions() {
        // Améliorer les interactions avec les zones
        document.addEventListener('DOMContentLoaded', () => {
            const zones = document.querySelectorAll('.zone');
            zones.forEach(zone => {
                this.enhanceZoneInteraction(zone);
            });
        });
    }

    enhanceZoneInteraction(zone) {
        const zoneId = zone.dataset.zone;
        
        // Ajouter des effets visuels au survol
        zone.addEventListener('mouseenter', () => {
            this.showZonePreview(zoneId);
        });

        // Ajouter des effets de clic
        zone.addEventListener('click', () => {
            this.enterZone(zoneId);
        });

        // Ajouter des effets de proximité
        zone.addEventListener('mouseleave', () => {
            this.hideZonePreview();
        });
    }

    showZonePreview(zoneId) {
        const zoneData = this.zoneData[zoneId];
        if (!zoneData) return;

        // Créer une prévisualisation de zone
        const preview = document.createElement('div');
        preview.className = 'zone-preview';
        preview.innerHTML = `
            <div class="zone-preview-content">
                <h3>${zoneData.name}</h3>
                <p>${zoneData.description}</p>
                <div class="zone-stats">
                    <span>🎮 ${zoneData.miniGames.length} mini-jeux</span>
                    <span>💎 ${zoneData.secrets} secrets</span>
                    <span>⭐ ${zoneData.difficulty}</span>
                </div>
                <button class="enter-zone-btn" onclick="zoneExploration.enterZone('${zoneId}')">
                    Entrer dans la zone
                </button>
            </div>
        `;

        document.body.appendChild(preview);

        // Animation d'apparition
        setTimeout(() => {
            preview.classList.add('show');
        }, 100);
    }

    hideZonePreview() {
        const preview = document.querySelector('.zone-preview');
        if (preview) {
            preview.classList.add('hide');
            setTimeout(() => {
                preview.remove();
            }, 300);
        }
    }

    enterZone(zoneId) {
        const zoneData = this.zoneData[zoneId];
        if (!zoneData) return;

        this.currentZone = zoneId;
        this.showZoneNarrative(zoneData);
        this.startZoneExploration(zoneId);
    }

    showZoneNarrative(zoneData) {
        // Afficher la narration d'entrée
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage(zoneData.narrative.entry, 5000);
            window.lunaVision.setEmotion('curious');
        }

        // Créer une interface d'exploration
        this.createExplorationInterface(zoneData);
    }

    createExplorationInterface(zoneData) {
        // Créer une modale d'exploration
        const modal = document.createElement('div');
        modal.className = 'zone-exploration-modal';
        modal.innerHTML = `
            <div class="zone-modal-content">
                <div class="zone-modal-header">
                    <h2>${zoneData.name}</h2>
                    <button class="close-zone-btn" onclick="zoneExploration.closeZone()">×</button>
                </div>
                <div class="zone-modal-body">
                    <div class="zone-narrative">
                        <p>${zoneData.narrative.exploration}</p>
                    </div>
                    <div class="zone-actions">
                        <button class="action-btn" onclick="zoneExploration.exploreZone()">
                            🔍 Explorer
                        </button>
                        <button class="action-btn" onclick="zoneExploration.playMiniGame()">
                            🎮 Mini-jeux
                        </button>
                        <button class="action-btn" onclick="zoneExploration.searchSecrets()">
                            💎 Chercher des secrets
                        </button>
                    </div>
                    <div class="zone-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" id="zone-progress-fill"></div>
                        </div>
                        <span class="progress-text">Progression: 0%</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Animation d'apparition
        setTimeout(() => {
            modal.classList.add('show');
        }, 100);
    }

    exploreZone() {
        const zoneData = this.zoneData[this.currentZone];
        if (!zoneData) return;

        // Simuler l'exploration
        this.showExplorationFeedback();
        
        // Mettre à jour la progression
        this.updateZoneProgress(10);

        // Afficher la narration d'exploration
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage(zoneData.narrative.exploration, 3000);
        }
    }

    playMiniGame() {
        const zoneData = this.zoneData[this.currentZone];
        if (!zoneData || !zoneData.miniGames.length) return;

        // Sélectionner un mini-jeu aléatoire
        const randomGame = zoneData.miniGames[Math.floor(Math.random() * zoneData.miniGames.length)];
        this.launchMiniGame(randomGame);
    }

    launchMiniGame(gameId) {
        // Créer l'interface du mini-jeu
        const gameModal = document.createElement('div');
        gameModal.className = 'mini-game-modal';
        gameModal.innerHTML = `
            <div class="mini-game-content">
                <div class="mini-game-header">
                    <h3>Mini-jeu: ${this.getGameName(gameId)}</h3>
                    <button class="close-game-btn" onclick="zoneExploration.closeMiniGame()">×</button>
                </div>
                <div class="mini-game-body" id="mini-game-body">
                    ${this.getGameInterface(gameId)}
                </div>
            </div>
        `;

        document.body.appendChild(gameModal);

        // Animation d'apparition
        setTimeout(() => {
            gameModal.classList.add('show');
        }, 100);

        // Initialiser le mini-jeu
        this.initializeMiniGame(gameId);
    }

    getGameName(gameId) {
        const gameNames = {
            'data_traffic': 'Trafic de Données',
            'network_infiltration': 'Infiltration Réseau',
            'security_breach': 'Bréche de Sécurité',
            'server_hack': 'Hack de Serveur',
            'data_extraction': 'Extraction de Données',
            'firewall_breach': 'Bréche de Pare-feu',
            'shadow_navigation': 'Navigation dans l\'Ombre',
            'artifact_hunt': 'Chasse aux Artefacts',
            'underground_escape': 'Évasion Souterraine',
            'basic_hacking': 'Hacking de Base',
            'command_practice': 'Pratique des Commandes',
            'skill_test': 'Test de Compétences'
        };
        return gameNames[gameId] || 'Mini-jeu';
    }

    getGameInterface(gameId) {
        // Retourner l'interface HTML du mini-jeu
        return `
            <div class="game-interface">
                <div class="game-instructions">
                    <p>Utilise les touches pour contrôler le jeu. Objectif: ${this.getGameObjective(gameId)}</p>
                </div>
                <div class="game-area" id="game-area">
                    <canvas id="game-canvas" width="400" height="300"></canvas>
                </div>
                <div class="game-controls">
                    <button class="game-btn" onclick="zoneExploration.startGame()">Commencer</button>
                    <button class="game-btn" onclick="zoneExploration.pauseGame()">Pause</button>
                    <button class="game-btn" onclick="zoneExploration.resetGame()">Recommencer</button>
                </div>
                <div class="game-stats">
                    <span>Score: <span id="game-score">0</span></span>
                    <span>Temps: <span id="game-time">0s</span></span>
                </div>
            </div>
        `;
    }

    getGameObjective(gameId) {
        const objectives = {
            'data_traffic': 'Intercepte les données qui circulent',
            'network_infiltration': 'Pénètre le réseau sans être détecté',
            'security_breach': 'Contourne les systèmes de sécurité',
            'server_hack': 'Hacke les serveurs pour extraire des données',
            'data_extraction': 'Extrais le maximum de données',
            'firewall_breach': 'Traverse le pare-feu',
            'shadow_navigation': 'Navigue dans l\'obscurité',
            'artifact_hunt': 'Trouve tous les artefacts cachés',
            'underground_escape': 'Échappe-toi des tunnels',
            'basic_hacking': 'Maîtrise les commandes de base',
            'command_practice': 'Exécute les commandes rapidement',
            'skill_test': 'Passe tous les tests de compétences'
        };
        return objectives[gameId] || 'Termine le défi';
    }

    initializeMiniGame(gameId) {
        // Initialiser le mini-jeu selon son type
        const canvas = document.getElementById('game-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Logique du mini-jeu basée sur l'ID
        switch(gameId) {
            case 'data_traffic':
                this.initDataTrafficGame(ctx);
                break;
            case 'network_infiltration':
                this.initNetworkInfiltrationGame(ctx);
                break;
            case 'security_breach':
                this.initSecurityBreachGame(ctx);
                break;
            default:
                this.initGenericGame(ctx, gameId);
        }
    }

    initDataTrafficGame(ctx) {
        // Mini-jeu de trafic de données
        let score = 0;
        let time = 0;
        let dataPackets = [];
        let playerY = 150;

        const gameLoop = () => {
            // Effacer le canvas
            ctx.fillStyle = 'rgba(9, 9, 11, 0.8)';
            ctx.fillRect(0, 0, 400, 300);

            // Dessiner les données qui circulent
            dataPackets.forEach((packet, index) => {
                ctx.fillStyle = packet.color;
                ctx.fillRect(packet.x, packet.y, 20, 10);
                packet.x -= 2;

                // Vérifier la collision avec le joueur
                if (packet.x < 50 && packet.x > 30 && Math.abs(packet.y - playerY) < 20) {
                    score += 10;
                    dataPackets.splice(index, 1);
                }
            });

            // Dessiner le joueur
            ctx.fillStyle = '#a78bfa';
            ctx.fillRect(30, playerY - 10, 20, 20);

            // Mettre à jour l'affichage
            document.getElementById('game-score').textContent = score;
            document.getElementById('game-time').textContent = Math.floor(time / 60) + 's';

            // Continuer la boucle
            if (time < 600) { // 10 secondes
                time++;
                requestAnimationFrame(gameLoop);
            } else {
                this.endMiniGame(score);
            }
        };

        // Générer des paquets de données
        setInterval(() => {
            if (time < 600) {
                dataPackets.push({
                    x: 380,
                    y: Math.random() * 280 + 10,
                    color: `hsl(${Math.random() * 360}, 70%, 60%)`
                });
            }
        }, 100);

        // Contrôles
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowUp' && playerY > 20) {
                playerY -= 10;
            } else if (e.key === 'ArrowDown' && playerY < 280) {
                playerY += 10;
            }
        });

        gameLoop();
    }

    initNetworkInfiltrationGame(ctx) {
        // Mini-jeu d'infiltration réseau
        let progress = 0;
        let time = 0;
        let obstacles = [];

        const gameLoop = () => {
            // Effacer le canvas
            ctx.fillStyle = 'rgba(9, 9, 11, 0.8)';
            ctx.fillRect(0, 0, 400, 300);

            // Dessiner le réseau
            ctx.strokeStyle = '#a78bfa';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(50, 150);
            ctx.lineTo(350, 150);
            ctx.stroke();

            // Dessiner la progression
            ctx.fillStyle = '#60a5fa';
            ctx.fillRect(50, 145, progress * 3, 10);

            // Dessiner les obstacles
            obstacles.forEach((obstacle, index) => {
                ctx.fillStyle = '#ef4444';
                ctx.fillRect(obstacle.x, obstacle.y, 20, 20);
                obstacle.x -= 1;

                if (obstacle.x < 0) {
                    obstacles.splice(index, 1);
                }
            });

            // Mettre à jour la progression
            progress += 0.5;
            time++;

            // Mettre à jour l'affichage
            document.getElementById('game-score').textContent = Math.floor(progress);
            document.getElementById('game-time').textContent = Math.floor(time / 60) + 's';

            // Continuer la boucle
            if (progress < 100 && time < 1200) {
                requestAnimationFrame(gameLoop);
            } else {
                this.endMiniGame(Math.floor(progress));
            }
        };

        // Générer des obstacles
        setInterval(() => {
            if (time < 1200) {
                obstacles.push({
                    x: 380,
                    y: Math.random() * 280 + 10
                });
            }
        }, 200);

        gameLoop();
    }

    initSecurityBreachGame(ctx) {
        // Mini-jeu de brèche de sécurité
        let score = 0;
        let time = 0;
        let securityLayers = [];

        const gameLoop = () => {
            // Effacer le canvas
            ctx.fillStyle = 'rgba(9, 9, 11, 0.8)';
            ctx.fillRect(0, 0, 400, 300);

            // Dessiner les couches de sécurité
            securityLayers.forEach((layer, index) => {
                ctx.fillStyle = layer.color;
                ctx.fillRect(layer.x, layer.y, layer.width, layer.height);
            });

            // Dessiner le point d'attaque
            ctx.fillStyle = '#a78bfa';
            ctx.beginPath();
            ctx.arc(200, 150, 10, 0, 2 * Math.PI);
            ctx.fill();

            // Mettre à jour l'affichage
            document.getElementById('game-score').textContent = score;
            document.getElementById('game-time').textContent = Math.floor(time / 60) + 's';

            time++;
            if (time < 900) { // 15 secondes
                requestAnimationFrame(gameLoop);
            } else {
                this.endMiniGame(score);
            }
        };

        // Générer des couches de sécurité
        for (let i = 0; i < 5; i++) {
            securityLayers.push({
                x: Math.random() * 350,
                y: Math.random() * 250,
                width: 50 + Math.random() * 50,
                height: 20 + Math.random() * 30,
                color: `hsl(${Math.random() * 60 + 200}, 70%, 50%)`
            });
        }

        gameLoop();
    }

    initGenericGame(ctx, gameId) {
        // Mini-jeu générique
        let score = 0;
        let time = 0;

        const gameLoop = () => {
            // Effacer le canvas
            ctx.fillStyle = 'rgba(9, 9, 11, 0.8)';
            ctx.fillRect(0, 0, 400, 300);

            // Dessiner un jeu simple
            ctx.fillStyle = '#a78bfa';
            ctx.fillRect(50, 50, 300, 200);

            // Dessiner du texte
            ctx.fillStyle = '#ffffff';
            ctx.font = '16px Arial';
            ctx.fillText(`Mini-jeu: ${this.getGameName(gameId)}`, 100, 100);
            ctx.fillText(`Score: ${score}`, 100, 130);
            ctx.fillText(`Temps: ${Math.floor(time / 60)}s`, 100, 160);

            // Mettre à jour l'affichage
            document.getElementById('game-score').textContent = score;
            document.getElementById('game-time').textContent = Math.floor(time / 60) + 's';

            time++;
            if (time < 600) { // 10 secondes
                requestAnimationFrame(gameLoop);
            } else {
                this.endMiniGame(score);
            }
        };

        gameLoop();
    }

    startGame() {
        // Démarrer le mini-jeu
        // console.log('Mini-jeu démarré');
    }

    pauseGame() {
        // Mettre en pause le mini-jeu
        // console.log('Mini-jeu en pause');
    }

    resetGame() {
        // Recommencer le mini-jeu
        // console.log('Mini-jeu recommencé');
    }

    endMiniGame(score) {
        // Terminer le mini-jeu et donner des récompenses
        const zoneData = this.zoneData[this.currentZone];
        if (!zoneData) return;

        // Calculer les récompenses
        const xpGained = Math.floor(score / 10);
        const coinsGained = Math.floor(score / 20);

        // Afficher les résultats
        this.showGameResults(score, xpGained, coinsGained);

        // Mettre à jour la progression de la zone
        this.updateZoneProgress(20);

        // Fermer le mini-jeu
        setTimeout(() => {
            this.closeMiniGame();
        }, 3000);
    }

    showGameResults(score, xp, coins) {
        const results = document.createElement('div');
        results.className = 'game-results';
        results.innerHTML = `
            <div class="results-content">
                <h3>🎮 Mini-jeu terminé !</h3>
                <p>Score: ${score}</p>
                <p>+${xp} XP</p>
                <p>+${coins} Coins</p>
            </div>
        `;

        document.body.appendChild(results);

        // Animation d'apparition
        setTimeout(() => {
            results.classList.add('show');
        }, 100);

        // Supprimer après 3 secondes
        setTimeout(() => {
            results.remove();
        }, 3000);
    }

    searchSecrets() {
        const zoneData = this.zoneData[this.currentZone];
        if (!zoneData) return;

        // Simuler la recherche de secrets
        const foundSecret = Math.random() < 0.3; // 30% de chance

        if (foundSecret) {
            this.showSecretFound(zoneData);
            this.updateZoneProgress(15);
        } else {
            this.showSecretNotFound();
        }
    }

    showSecretFound(zoneData) {
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage(zoneData.narrative.secrets, 4000);
            window.lunaVision.setEmotion('excited');
        }

        // Animation de secret trouvé
        this.createSecretAnimation();
    }

    showSecretNotFound() {
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage("Rien trouvé cette fois... Continue à chercher !", 2000);
        }
    }

    createSecretAnimation() {
        // Créer une animation de secret trouvé
        const secret = document.createElement('div');
        secret.className = 'secret-found';
        secret.innerHTML = '💎';
        secret.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 3em;
            z-index: 10000;
            animation: secretPulse 2s ease-in-out;
        `;

        document.body.appendChild(secret);

        // Supprimer après l'animation
        setTimeout(() => {
            secret.remove();
        }, 2000);
    }

    updateZoneProgress(increment) {
        if (!this.explorationProgress[this.currentZone]) {
            this.explorationProgress[this.currentZone] = 0;
        }

        this.explorationProgress[this.currentZone] += increment;
        if (this.explorationProgress[this.currentZone] > 100) {
            this.explorationProgress[this.currentZone] = 100;
        }

        // Mettre à jour l'affichage
        const progressFill = document.getElementById('zone-progress-fill');
        const progressText = document.querySelector('.progress-text');
        
        if (progressFill) {
            progressFill.style.width = this.explorationProgress[this.currentZone] + '%';
        }
        
        if (progressText) {
            progressText.textContent = `Progression: ${this.explorationProgress[this.currentZone]}%`;
        }

        // Vérifier si la zone est complétée
        if (this.explorationProgress[this.currentZone] >= 100) {
            this.completeZone();
        }
    }

    completeZone() {
        const zoneData = this.zoneData[this.currentZone];
        if (!zoneData) return;

        // Afficher la narration de completion
        if (window.lunaVision) {
            window.lunaVision.showLunaMessage(zoneData.narrative.completion, 5000);
            window.lunaVision.setEmotion('proud');
        }

        // Donner les récompenses
        this.giveZoneRewards(zoneData.rewards);

        // Animation de completion
        this.createCompletionAnimation();
    }

    giveZoneRewards(rewards) {
        // Donner XP, coins, badge
        if (window.rewardAnimations) {
            window.rewardAnimations.animateXPGain(rewards.xp);
            window.rewardAnimations.animateCoinsGained(rewards.coins);
            if (rewards.badge) {
                window.rewardAnimations.animateBadgeEarned(rewards.badge);
            }
        }
    }

    createCompletionAnimation() {
        // Créer une animation de completion
        const completion = document.createElement('div');
        completion.className = 'zone-completion';
        completion.innerHTML = '🎉';
        completion.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 4em;
            z-index: 10000;
            animation: completionBurst 3s ease-in-out;
        `;

        document.body.appendChild(completion);

        // Supprimer après l'animation
        setTimeout(() => {
            completion.remove();
        }, 3000);
    }

    closeZone() {
        const modal = document.querySelector('.zone-exploration-modal');
        if (modal) {
            modal.classList.add('hide');
            setTimeout(() => {
                modal.remove();
            }, 300);
        }
    }

    closeMiniGame() {
        const modal = document.querySelector('.mini-game-modal');
        if (modal) {
            modal.classList.add('hide');
            setTimeout(() => {
                modal.remove();
            }, 300);
        }
    }

    showExplorationFeedback() {
        // Afficher un feedback d'exploration
        const feedback = document.createElement('div');
        feedback.className = 'exploration-feedback';
        feedback.innerHTML = '🔍 Exploration...';
        feedback.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(167, 139, 250, 0.9);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 10000;
            animation: fadeInOut 2s ease-in-out;
        `;

        document.body.appendChild(feedback);

        // Supprimer après 2 secondes
        setTimeout(() => {
            feedback.remove();
        }, 2000);
    }
}

// CSS pour les animations
const style = document.createElement('style');
style.textContent = `
    @keyframes secretPulse {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.5); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
    }
    
    @keyframes completionBurst {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
    }
    
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateY(-20px); }
        50% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-20px); }
    }
    
    .zone-preview {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 20px;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .zone-preview.show {
        opacity: 1;
    }
    
    .zone-exploration-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .zone-exploration-modal.show {
        opacity: 1;
    }
    
    .zone-modal-content {
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 30px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .zone-actions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .action-btn {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.2), rgba(96, 165, 250, 0.2));
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 8px;
        padding: 15px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .action-btn:hover {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.4), rgba(96, 165, 250, 0.4));
        transform: translateY(-2px);
    }
    
    .mini-game-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        z-index: 10001;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .mini-game-modal.show {
        opacity: 1;
    }
    
    .mini-game-content {
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 30px;
        max-width: 500px;
        width: 90%;
    }
    
    .game-interface {
        text-align: center;
    }
    
    .game-area {
        margin: 20px 0;
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 8px;
        overflow: hidden;
    }
    
    #game-canvas {
        display: block;
        background: rgba(0, 0, 0, 0.5);
    }
    
    .game-controls {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin: 20px 0;
    }
    
    .game-btn {
        background: rgba(167, 139, 250, 0.2);
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 5px;
        padding: 10px 20px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .game-btn:hover {
        background: rgba(167, 139, 250, 0.4);
    }
    
    .game-stats {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        font-family: 'IBM Plex Mono', monospace;
    }
    
    .game-results {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(9, 9, 11, 0.95);
        border: 2px solid rgba(167, 139, 250, 0.5);
        border-radius: 15px;
        padding: 30px;
        z-index: 10002;
        text-align: center;
        opacity: 0;
        animation: fadeInOut 3s ease-in-out;
    }
`;
document.head.appendChild(style);

// Initialiser le système d'exploration de zones
document.addEventListener('DOMContentLoaded', () => {
    window.zoneExploration = new ZoneExplorationEnhanced();
});

// Exporter pour utilisation globale
window.ZoneExplorationEnhanced = ZoneExplorationEnhanced;
