/**
 * Système de Zones Interactives avec Lore
 * Rend les zones du monde vivantes et immersives
 */

class InteractiveZonesSystem {
    constructor() {
        this.zones = new Map();
        this.currentZone = null;
        this.zoneHistory = [];
        this.init();
    }

    init() {
        console.log('🗺️ Système de zones interactives initialisé');
        this.loadZoneData();
        this.setupEventListeners();
        this.createZoneOverlay();
    }

    loadZoneData() {
        // Données des zones avec lore et interactions
        this.zones.set('terminal', {
            name: 'Terminal Principal',
            description: 'Le cœur de ton opération. Ici, tu communiques avec LUNA et accèdes aux systèmes.',
            lore: 'Ce terminal a été modifié par tes soins. Les circuits brillent d\'une lueur violette, signe de ta maîtrise technique.',
            interactions: [
                {
                    type: 'luna_contact',
                    name: 'Contacter LUNA',
                    description: 'Établir une connexion avec ton IA complice',
                    action: () => this.contactLuna()
                },
                {
                    type: 'hack_system',
                    name: 'Hacker le Système',
                    description: 'Tenter une infiltration dans les réseaux de La Corp',
                    action: () => this.hackSystem()
                }
            ],
            ambiance: 'terminal',
            music: 'ambient_terminal'
        });

        this.zones.set('monde', {
            name: 'Monde d\'Arkalia',
            description: 'Un univers virtuel où chaque zone cache des secrets et des défis.',
            lore: 'Arkalia est un monde en constante évolution. Les données s\'entrelacent pour former des paysages numériques uniques.',
            interactions: [
                {
                    type: 'explore',
                    name: 'Explorer',
                    description: 'Découvrir les secrets cachés de cette zone',
                    action: () => this.exploreZone()
                },
                {
                    type: 'scan',
                    name: 'Scanner',
                    description: 'Analyser l\'environnement pour détecter des anomalies',
                    action: () => this.scanZone()
                }
            ],
            ambiance: 'world',
            music: 'ambient_world'
        });

        this.zones.set('profil', {
            name: 'Profil Personnel',
            description: 'Ton espace personnel où tu peux voir ta progression et tes accomplissements.',
            lore: 'Chaque action que tu poses laisse une trace dans ton profil. C\'est ici que ton histoire se construit.',
            interactions: [
                {
                    type: 'view_stats',
                    name: 'Voir les Statistiques',
                    description: 'Consulter tes performances détaillées',
                    action: () => this.viewStats()
                },
                {
                    type: 'view_badges',
                    name: 'Voir les Badges',
                    description: 'Admirer ta collection de récompenses',
                    action: () => this.viewBadges()
                }
            ],
            ambiance: 'profile',
            music: 'ambient_profile'
        });

        this.zones.set('leaderboard', {
            name: 'Classement Global',
            description: 'Voir où tu te situes parmi les autres hackers du monde.',
            lore: 'La compétition fait rage dans l\'univers d\'Arkalia. Chaque point compte dans cette course effrénée.',
            interactions: [
                {
                    type: 'view_ranking',
                    name: 'Voir le Classement',
                    description: 'Consulter les meilleurs scores',
                    action: () => this.viewRanking()
                },
                {
                    type: 'challenge',
                    name: 'Défier un Joueur',
                    description: 'Lancer un défi à un autre hacker',
                    action: () => this.challengePlayer()
                }
            ],
            ambiance: 'competitive',
            music: 'ambient_competitive'
        });
    }

    setupEventListeners() {
        // Écouter les clics sur les zones
        document.addEventListener('click', (event) => {
            const zoneElement = event.target.closest('[data-zone]');
            if (zoneElement) {
                const zoneId = zoneElement.dataset.zone;
                this.enterZone(zoneId);
            }
        });

        // Écouter les changements de page
        window.addEventListener('popstate', () => {
            this.updateCurrentZone();
        });
    }

    createZoneOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'zone-overlay';
        overlay.className = 'zone-overlay hidden';
        overlay.innerHTML = `
            <div class="zone-content">
                <div class="zone-header">
                    <h2 class="zone-title"></h2>
                    <button class="zone-close">×</button>
                </div>
                <div class="zone-description"></div>
                <div class="zone-lore"></div>
                <div class="zone-interactions"></div>
                <div class="zone-ambiance"></div>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    enterZone(zoneId) {
        const zone = this.zones.get(zoneId);
        if (!zone) return;

        this.currentZone = zoneId;
        this.zoneHistory.push(zoneId);
        this.showZoneOverlay(zone);
        this.playZoneAmbiance(zone);
        this.triggerZoneEvent('enter', zone);
    }

    showZoneOverlay(zone) {
        const overlay = document.getElementById('zone-overlay');
        const title = overlay.querySelector('.zone-title');
        const description = overlay.querySelector('.zone-description');
        const lore = overlay.querySelector('.zone-lore');
        const interactions = overlay.querySelector('.zone-interactions');

        title.textContent = zone.name;
        description.textContent = zone.description;
        lore.textContent = zone.lore;

        // Créer les interactions
        interactions.innerHTML = '';
        zone.interactions.forEach(interaction => {
            const button = document.createElement('button');
            button.className = 'zone-interaction-btn';
            button.innerHTML = `
                <div class="interaction-name">${interaction.name}</div>
                <div class="interaction-description">${interaction.description}</div>
            `;
            button.onclick = () => {
                interaction.action();
                this.hideZoneOverlay();
            };
            interactions.appendChild(button);
        });

        overlay.classList.remove('hidden');
        overlay.classList.add('show');
    }

    hideZoneOverlay() {
        const overlay = document.getElementById('zone-overlay');
        overlay.classList.remove('show');
        overlay.classList.add('hidden');
    }

    playZoneAmbiance(zone) {
        // Jouer l'ambiance sonore de la zone
        if (zone.music) {
            this.playAmbientSound(zone.music);
        }

        // Appliquer les effets visuels
        this.applyZoneEffects(zone.ambiance);
    }

    playAmbientSound(soundId) {
        // Implémentation basique - à étendre avec un vrai système audio
        console.log(`🎵 Lecture de l'ambiance: ${soundId}`);
    }

    applyZoneEffects(ambiance) {
        const body = document.body;
        body.className = body.className.replace(/ambiance-\w+/g, '');
        body.classList.add(`ambiance-${ambiance}`);
    }

    triggerZoneEvent(eventType, zone) {
        const event = new CustomEvent('zoneEvent', {
            detail: {
                type: eventType,
                zone: zone,
                zoneId: this.currentZone
            }
        });
        document.dispatchEvent(event);
    }

    // Actions des zones
    contactLuna() {
        console.log('🌙 Contact avec LUNA...');
        // Déclencher l'événement de contact LUNA
        document.dispatchEvent(new CustomEvent('lunaContact'));
    }

    hackSystem() {
        console.log('💻 Tentative de hack...');
        // Déclencher l'événement de hack
        document.dispatchEvent(new CustomEvent('hackSystem'));
    }

    exploreZone() {
        console.log('🔍 Exploration de la zone...');
        // Déclencher l'événement d'exploration
        document.dispatchEvent(new CustomEvent('zoneExploration'));
    }

    scanZone() {
        console.log('📡 Scan de la zone...');
        // Déclencher l'événement de scan
        document.dispatchEvent(new CustomEvent('zoneScan'));
    }

    viewStats() {
        console.log('📊 Affichage des statistiques...');
        // Déclencher l'événement de visualisation des stats
        document.dispatchEvent(new CustomEvent('viewStats'));
    }

    viewBadges() {
        console.log('🏆 Affichage des badges...');
        // Déclencher l'événement de visualisation des badges
        document.dispatchEvent(new CustomEvent('viewBadges'));
    }

    viewRanking() {
        console.log('🏅 Affichage du classement...');
        // Déclencher l'événement de visualisation du classement
        document.dispatchEvent(new CustomEvent('viewRanking'));
    }

    challengePlayer() {
        console.log('⚔️ Défi d\'un joueur...');
        // Déclencher l'événement de défi
        document.dispatchEvent(new CustomEvent('challengePlayer'));
    }

    updateCurrentZone() {
        const path = window.location.pathname;
        const zoneMap = {
            '/': 'terminal',
            '/terminal': 'terminal',
            '/monde': 'monde',
            '/profil': 'profil',
            '/leaderboard': 'leaderboard'
        };

        const zoneId = zoneMap[path];
        if (zoneId && zoneId !== this.currentZone) {
            this.enterZone(zoneId);
        }
    }

    // Méthodes utilitaires
    getCurrentZone() {
        return this.currentZone;
    }

    getZoneHistory() {
        return this.zoneHistory;
    }

    resetZoneHistory() {
        this.zoneHistory = [];
    }
}

// Initialiser le système de zones interactives
document.addEventListener('DOMContentLoaded', () => {
    window.interactiveZonesSystem = new InteractiveZonesSystem();
    console.log('🗺️ Zones interactives activées');
});

// Export pour utilisation externe
window.InteractiveZonesSystem = InteractiveZonesSystem;
