// ===== TERMINAL ARKALIA QUEST v3.0 - VERSION AMÉLIORÉE =====

// Variables globales
let audioEnabled = true;
let messageHistory = [];
let commandHistory = [];
let historyIndex = -1;
let hackingEffects = null;
let isLowPerformanceDevice = false;
let audioContext = null;
let userLevel = 'beginner'; // Niveau utilisateur pour adaptation
let lastCommandTime = 0; // Pour détecter la fréquence d'utilisation

// Détection des appareils faibles
function detectDevicePerformance() {
    const userAgent = navigator.userAgent.toLowerCase();
    const isMobile = /mobile|android|iphone|ipad/.test(userAgent);
    const isOldBrowser = /msie|trident/.test(userAgent);
    const hasLowMemory = navigator.deviceMemory && navigator.deviceMemory < 4;
    const hasLowCores = navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4;

    isLowPerformanceDevice = isMobile || isOldBrowser || hasLowMemory || hasLowCores;

    if (isLowPerformanceDevice) {
        disableHeavyEffects();
        document.body.classList.add('low-performance');
    }
}

// Désactiver les effets lourds
function disableHeavyEffects() {
    const style = document.createElement('style');
    style.textContent = `
        body::before, body::after { display: none !important; }
        .luna-particles { display: none !important; }
        .hack-effect::before { display: none !important; }
    `;
    document.head.appendChild(style);
}

// Initialisation de l'audio
function initAudio() {
    if (window.AudioContext || window.webkitAudioContext) {
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            // Audio non supporté, mode silencieux
        }
    }
}

// Fonctions audio simplifiées
function playTypingSound() {
    if (!audioEnabled || !audioContext) return;
    try {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(600, audioContext.currentTime + 0.1);
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
        // Mode silencieux
    }
}

function playSuccessSound() {
    if (!audioEnabled || !audioContext) return;
    try {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.2);
        oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.4);
        gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.4);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.4);
    } catch (e) {
        // Mode silencieux
    }
}

// ===== EFFETS MATRIX AMÉLIORÉS =====

function playMatrixSuccessEffect() {
    if (!audioEnabled || !audioContext) return;
    try {
        // Son Matrix success
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.setValueAtTime(200, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.3);
        oscillator.frequency.exponentialRampToValueAtTime(1600, audioContext.currentTime + 0.6);
        gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.6);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.6);
    } catch (e) {
        // Mode silencieux
    }

    // Effet visuel Matrix
    showMatrixParticles();
}

function playMatrixErrorEffect() {
    if (!audioEnabled || !audioContext) return;
    try {
        // Son Matrix error
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.2);
        oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.4);
        gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.4);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.4);
    } catch (e) {
        // Mode silencieux
    }
}

function showMatrixParticles() {
    const container = document.querySelector('.terminal-container');
    if (!container) return;

    // Créer des particules Matrix
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'matrix-particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00ff00;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: matrixParticle 2s ease-out forwards;
        `;

        container.appendChild(particle);

        // Supprimer après animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 2000);
    }
}

function showMatrixRewards(rewards) {
    if (!rewards) return;

    const rewardContainer = document.createElement('div');
    rewardContainer.className = 'matrix-rewards';
    rewardContainer.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(45deg, #001100, #00ff00);
        border: 2px solid #00ff00;
        border-radius: 15px;
        padding: 20px;
        color: #00ff00;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 18px;
        text-align: center;
        z-index: 10000;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.6);
        animation: matrixRewardShow 0.5s ease-out;
    `;

    let rewardHTML = '<h3>🎉 RÉCOMPENSES MATRIX !</h3>';

    if (rewards.badge) {
        rewardHTML += `<div class="reward-item">🏆 ${rewards.badge}</div>`;
    }
    if (rewards.achievement) {
        rewardHTML += `<div class="reward-item">🎯 ${rewards.achievement}</div>`;
    }
    if (rewards.xp) {
        rewardHTML += `<div class="reward-item">⭐ +${rewards.xp} XP</div>`;
    }

    rewardContainer.innerHTML = rewardHTML;
    document.body.appendChild(rewardContainer);

    // Supprimer après 3 secondes
    setTimeout(() => {
        if (rewardContainer.parentNode) {
            rewardContainer.parentNode.removeChild(rewardContainer);
        }
    }, 3000);
}

function addMatrixSuccessMessage(message) {
    addMessage(message, 'matrix-success');
}

function addMatrixErrorMessage(message) {
    addMessage(message, 'matrix-error');
}

function addEncouragementMessage(message) {
    addMessage(message, 'encouragement');
}

function playErrorSound() {
    if (!audioEnabled || !audioContext) return;
    try {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.3);
        gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (e) {
        // Mode silencieux
    }
}

// AMÉLIORATION : Feedback utilisateur intelligent
function provideIntelligentFeedback(command, response) {
    const now = Date.now();
    const timeSinceLastCommand = now - lastCommandTime;
    lastCommandTime = now;

    // Détecter le niveau utilisateur basé sur l'usage
    if (commandHistory.length < 5) {
        userLevel = 'beginner';
    } else if (commandHistory.length < 20) {
        userLevel = 'intermediate';
    } else {
        userLevel = 'advanced';
    }

    // Feedback contextuel selon le niveau
    if (userLevel === 'beginner') {
        if (!response.réussite) {
            showContextualHelp(command);
        } else {
            showEncouragement();
        }
    }

    // Détecter les patterns d'erreur
    if (timeSinceLastCommand < 2000 && !response.réussite) {
        showQuickHelp();
    }
}

// AMÉLIORATION : Aide contextuelle intelligente
function showContextualHelp(command) {
    const helpMessages = {
        'aide': '💡 Essaye "aide" pour voir toutes les commandes disponibles !',
        'profil': '👤 Utilise "profil" pour voir tes statistiques !',
        'luna': '🌙 Commence par "luna_contact" pour rencontrer LUNA !',
        'prologue': '📖 Lance "prologue" pour commencer l\'aventure !',
        'acte': '🎮 Utilise "acte_1", "acte_2", etc. pour progresser !'
    };

    const suggestion = helpMessages[command] ||
        '💡 Essaie "aide" pour voir toutes les commandes disponibles !';

    setTimeout(() => {
        addContextualMessage(suggestion, 'help');
    }, 1000);
}

// AMÉLIORATION : Messages d'encouragement
function showEncouragement() {
    const encouragements = [
        '🌟 Excellent ! Tu progresses bien !',
        '🚀 Continue comme ça, hacker !',
        '💪 Tu maîtrises de mieux en mieux !',
        '🎯 Parfait ! Tu es sur la bonne voie !'
    ];

    const random = encouragements[Math.floor(Math.random() * encouragements.length)];

    setTimeout(() => {
        addContextualMessage(random, 'encouragement');
    }, 500);
}

// AMÉLIORATION : Aide rapide pour utilisateurs pressés
function showQuickHelp() {
    const quickTips = [
        '⚡ Astuce : Tape "aide" pour voir toutes les commandes !',
        '⚡ Astuce : Utilise les flèches ↑↓ pour naviguer dans l\'historique !',
        '⚡ Astuce : Appuie sur Entrée pour exécuter une commande !'
    ];

    const random = quickTips[Math.floor(Math.random() * quickTips.length)];

    setTimeout(() => {
        addContextualMessage(random, 'tip');
    }, 1500);
}

// AMÉLIORATION : Messages contextuels avec styles
function addContextualMessage(message, type = 'info') {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `contextual-message ${type}`;
    messageDiv.innerHTML = `
        <span class="contextual-icon">${getContextualIcon(type)}</span>
        <span class="contextual-text">${message}</span>
    `;

    // Animation d'entrée
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(-10px)';

    messagesContainer.appendChild(messageDiv);

    // Animation fluide
    setTimeout(() => {
        messageDiv.style.transition = 'all 0.3s ease';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    }, 10);

    // Auto-suppression après 5 secondes
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 300);
    }, 5000);
}

// AMÉLIORATION : Icônes contextuelles
function getContextualIcon(type) {
    const icons = {
        'help': '💡',
        'encouragement': '🌟',
        'tip': '⚡',
        'error': '❌',
        'success': '✅',
        'info': 'ℹ️'
    };
    return icons[type] || icons['info'];
}

// Initialisation
document.addEventListener('DOMContentLoaded', function () {
    detectDevicePerformance();
    initAudio();
    initTerminal();
    initHackingEffects();
    updateTime();
    lazyLoadResources();

    // AMÉLIORATION : Meilleure accessibilité
    // setupAccessibility(); // Fonction à implémenter plus tard

    // Debounce sur le scroll du terminal
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.addEventListener('scroll', debounce(() => {
            // Action possible sur scroll (ex: lazy loading)
        }, 100));
    }

    // Forcer la classe low-performance pour le testeur si device faible
    if (isLowPerformanceDevice) {
        document.body.classList.add('low-performance');
    }

    // Slider volume
    const audioVolume = document.getElementById('audioVolume');
    if (audioVolume && audioContext) {
        audioVolume.addEventListener('input', function () {
            if (audioContext) {
                const gain = Math.max(0.01, parseFloat(this.value));
                // Appliquer le volume à tous les sons (simple, pour testeur)
                audioContext.gain && (audioContext.gain.value = gain);
            }
            localStorage.setItem('arkalia_volume', this.value);
        });
        // Charger volume
        const savedVol = localStorage.getItem('arkalia_volume');
        if (savedVol) audioVolume.value = savedVol;
    }

    // Déclencher le lazy loading de l'image de test
    const testImg = document.getElementById('testLazyImg');
    if (testImg && testImg.dataset.src) {
        testImg.src = testImg.dataset.src;
        testImg.removeAttribute('data-src');
        testImg.style.display = 'block'; // Pour que le testeur la voie
    }

    // Gestion du bouton audio
    const audioToggle = document.getElementById('audioToggle');
    if (audioToggle) {
        // Charger l'état depuis localStorage
        audioEnabled = localStorage.getItem('arkalia_audio') !== 'off';
        updateAudioToggle(audioEnabled);
        audioToggle.addEventListener('click', function () {
            audioEnabled = !audioEnabled;
            localStorage.setItem('arkalia_audio', audioEnabled ? 'on' : 'off');
            updateAudioToggle(audioEnabled);
            if (window.audioManager) {
                try {
                    window.audioManager.setEnabled(audioEnabled);
                } catch (e) { }
            }
            // Feedback sonore immédiat
            if (audioEnabled) playSuccessSound(); else playErrorSound();
        });
    }

    // Démarrer l'ambiance sonore (avec fallback)
    setTimeout(() => {
        if (window.audioManager && !isLowPerformanceDevice) {
            try {
                window.audioManager.playSound('ambientSound');
            } catch (error) {
                audioEnabled = false;
            }
        }
    }, 1000);

    // AMÉLIORATION : Message de bienvenue adaptatif
    setTimeout(() => {
        if (userLevel === 'beginner') {
            addContextualMessage('🎮 Bienvenue dans Arkalia Quest ! Tape "aide" pour commencer !', 'info');
        }
    }, 2000);
});

// Initialisation des effets de hacking
function initHackingEffects() {
    try {
        if (window.HackingEffects) {
            hackingEffects = new window.HackingEffects();
        }
    } catch (error) {
        // Effets de hacking non disponibles
    }
}

// Système de terminal
function initTerminal() {
    const input = document.getElementById('commandInput');
    const sendBtn = document.getElementById('sendButton');
    const messagesContainer = document.getElementById('messagesContainer');

    if (!input || !sendBtn || !messagesContainer) {
        console.error('❌ Éléments du terminal non trouvés');
        return;
    }

    // Focus sur l'input
    input.focus();

    // Gestion de la soumission
    sendBtn.addEventListener('click', executeCommand);
    input.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            executeCommand();
        }
    });

    // Gestion de l'historique avec flèches
    input.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            navigateHistory('up');
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            navigateHistory('down');
        }
    });

    // Effet de frappe (avec fallback)
    input.addEventListener('input', function () {
        if (audioEnabled && window.audioManager && !isLowPerformanceDevice) {
            try {
                window.audioManager.playSound('typing');
            } catch (error) {
                // Mode silencieux
            }
        } else if (audioEnabled && !window.audioManager) {
            playTypingSound();
        }
    });

    // Feedback visuel des boutons
    setupButtonFeedback();
}

// Configuration du feedback des boutons
function setupButtonFeedback() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });

        button.addEventListener('mouseenter', function () {
            this.style.boxShadow = '0 0 10px rgba(0, 255, 0, 0.5)';
        });

        button.addEventListener('mouseleave', function () {
            this.style.boxShadow = '';
        });
    });
}

// Fonction unifiée pour les commandes rapides
function executeQuickCommand(command, event) {
    // Commande rapide exécutée
    // Effet visuel du bouton
    if (event && event.target) {
        const button = event.target;
        button.classList.add('button-clicked');
        setTimeout(() => button.classList.remove('button-clicked'), 200);
    }
    // Jouer le son de clic
    if (window.audioManager) {
        try {
            window.audioManager.playSound('buttonSound');
        } catch (e) { }
    }
    // Afficher la barre de progression selon la commande
    const progressTimes = {
        'kill_virus': 20,
        'find_shadow': 45,
        'hack_system': 8,
        'challenge_corp': 20,
        'save_pc': 5,
        'speed_hack': 10
    };
    if (progressTimes[command]) {
        showHackingProgress(command, progressTimes[command]);
    }
    // Envoyer la commande
    executeCommand(command);
}

// Fonction pour vérifier les easter eggs
function checkEasterEggs(command) {
    const cmd = command.toLowerCase().trim();

    // Easter eggs LUNA
    if (cmd === 'luna_dance' || cmd === 'luna dance' || (cmd.includes('luna') && cmd.includes('dance'))) {
        return `🌙 LUNA: *danse avec joie* 💃✨\nJe danse pour toi ! Tu es un joueur formidable !\n*LUNA fait des pirouettes dans le terminal*`;
    }

    if (cmd === 'luna_love' || cmd === 'luna love' || (cmd.includes('luna') && cmd.includes('love'))) {
        return `💖 LUNA: Je t'aime beaucoup ! Tu es mon joueur préféré !\n*LUNA envoie des cœurs virtuels* ❤️✨`;
    }

    if (cmd === 'luna_secret' || cmd === 'luna secret' || (cmd.includes('luna') && cmd.includes('secret'))) {
        return `🤫 LUNA: *chuchote* J'ai un secret pour toi...\nTu es plus fort que tu ne le penses !\n*LUNA fait un clin d'œil* 😉`;
    }

    if (cmd === 'luna_power' || cmd === 'luna power' || (cmd.includes('luna') && cmd.includes('power'))) {
        return `⚡ LUNA: *puissance activée*\nJe sens une grande puissance en toi !\nTu es destiné à de grandes choses !\n*LUNA brille intensément* ✨`;
    }

    // Easter eggs Matrix
    if (cmd === 'matrix' || cmd === 'the matrix') {
        return `🔮 MATRIX PROTOCOL ACTIVATED\n\n🌌 Bienvenue dans la Matrice, Neo...\n\n💊 Pilule rouge ou pilule bleue ?\n\n*Le terminal se transforme en code vert*`;
    }

    if (cmd.includes('red pill') || cmd.includes('pilule rouge')) {
        return `🔴 PILULE ROUGE AVALÉE\n\n🌌 Tu as choisi la vérité...\n\n*Le monde réel se révèle*\n\n🎯 Tu es maintenant éveillé !`;
    }

    if (cmd.includes('blue pill') || cmd.includes('pilule bleue')) {
        return `🔵 PILULE BLEUE AVALÉE\n\n😴 Tu retournes dans l'illusion...\n\n*Tout redevient normal*\n\n💤 Continue ta vie tranquille...`;
    }

    // Easter eggs de hacking
    if (cmd === 'hack the planet' || cmd === 'hack the world') {
        return `🌍 HACK THE PLANET INITIATED\n\n💻 *Connexion à tous les systèmes mondiaux*\n\n🌐 *Accès aux satellites*\n\n🛰️ *Contrôle des communications*\n\n⚠️ ATTENTION: Simulation uniquement !`;
    }

    if (cmd === 'sudo rm -rf /' || cmd === 'rm -rf /') {
        return `⚠️ COMMANDE DANGEREUSE DÉTECTÉE\n\n🛡️ Système de protection activé\n\n❌ Commande bloquée pour votre sécurité\n\n💡 Astuce: Utilisez 'aide' pour des commandes sûres !`;
    }

    // Easter eggs de jeux
    if (cmd === 'play_game' || cmd === 'games') {
        return `🎮 MINI-JEUX DISPONIBLES\n\n🎯 Tapez une de ces commandes :\n• simple_hack - Jeu de hack binaire\n• sequence_game - Jeu de mémoire\n• typing_challenge - Défi de frappe\n\n🚀 Ou utilisez 'aide' pour plus d'options !`;
    }

    if (cmd === 'simple_hack') {
        // Démarrer le jeu de hack
        if (window.miniGamesInteractive && typeof window.miniGamesInteractive.startGame === 'function') {
            window.miniGamesInteractive.startGame('simple_hack');
            return `🎮 LANCEMENT DU JEU DE HACK\n\n💻 Code binaire à reproduire...\n\n🎯 Score maximum : 1000 points\n\n🚀 Bonne chance, hacker !`;
        }
        return `❌ Système de jeux non disponible - Rechargez la page et réessayez`;
    }

    if (cmd === 'sequence_game') {
        if (window.miniGamesInteractive && typeof window.miniGamesInteractive.startGame === 'function') {
            window.miniGamesInteractive.startGame('sequence_game');
            return `🎮 LANCEMENT DU JEU DE SÉQUENCE\n\n🧠 Mémorise la séquence...\n\n🎯 Score maximum : 500 points\n\n🚀 Teste ta mémoire !`;
        }
        return `❌ Système de jeux non disponible - Rechargez la page et réessayez`;
    }

    if (cmd === 'typing_challenge') {
        if (window.miniGamesInteractive && typeof window.miniGamesInteractive.startGame === 'function') {
            window.miniGamesInteractive.startGame('typing_challenge');
            return `🎮 LANCEMENT DU DÉFI DE FRAPPE\n\n⌨️ Tape le plus vite possible...\n\n🎯 Score basé sur WPM\n\n🚀 Montre ta vitesse !`;
        }
        return `❌ Système de jeux non disponible - Rechargez la page et réessayez`;
    }

    // Easter eggs de progression
    if (cmd === 'level_up' || cmd === 'levelup') {
        // Déclencher une animation de montée de niveau
        if (window.rewardAnimations && typeof window.rewardAnimations.animateLevelUpImproved === 'function') {
            window.rewardAnimations.animateLevelUpImproved(2);
            return `🎊 SIMULATION DE MONTÉE DE NIVEAU\n\n⭐ Niveau 2 atteint !\n\n🎉 Félicitations !\n\n✨ *Effets visuels activés*`;
        }
        return `🎊 SIMULATION DE MONTÉE DE NIVEAU\n\n⭐ Niveau 2 atteint !\n\n🎉 Félicitations !\n\n⚠️ Animations non disponibles - Rechargez la page`;
    }

    if (cmd === 'badge_unlock' || cmd === 'badge') {
        // Déclencher une animation de badge
        if (window.rewardAnimations && typeof window.rewardAnimations.animateBadgeUnlock === 'function') {
            window.rewardAnimations.animateBadgeUnlock('Easter Egg Hunter', 'Tu as trouvé un easter egg !');
            return `🏆 BADGE DÉBLOQUÉ !\n\n🎖️ "Easter Egg Hunter"\n\n✨ Tu as trouvé un easter egg !\n\n🎉 Continue à explorer !`;
        }
        return `🏆 BADGE DÉBLOQUÉ !\n\n🎖️ "Easter Egg Hunter"\n\n✨ Tu as trouvé un easter egg !\n\n⚠️ Animations non disponibles - Rechargez la page`;
    }

    // Easter eggs de thèmes
    if (cmd === 'matrix_mode' || cmd === 'matrix theme') {
        // Changer le thème en Matrix
        if (window.ThemeManager && typeof window.ThemeManager.setTheme === 'function') {
            window.ThemeManager.setTheme('matrix');
            return `🔮 MODE MATRIX ACTIVÉ\n\n🌌 Thème Matrix appliqué\n\n💚 Code vert partout\n\n*Bienvenue dans la Matrice*`;
        }
        return `🔮 MODE MATRIX ACTIVÉ\n\n🌌 Thème Matrix appliqué\n\n💚 Code vert partout\n\n⚠️ Gestionnaire de thèmes non disponible - Rechargez la page`;
    }

    if (cmd === 'cyberpunk_mode' || cmd === 'cyberpunk theme') {
        if (window.ThemeManager && typeof window.ThemeManager.setTheme === 'function') {
            window.ThemeManager.setTheme('cyberpunk');
            return `🌃 MODE CYBERPUNK ACTIVÉ\n\n🌆 Thème Cyberpunk appliqué\n\n💜 Néo-Tokyo vibes\n\n*Bienvenue dans le futur*`;
        }
        return `🌃 MODE CYBERPUNK ACTIVÉ\n\n🌆 Thème Cyberpunk appliqué\n\n💜 Néo-Tokyo vibes\n\n⚠️ Gestionnaire de thèmes non disponible - Rechargez la page`;
    }

    // Easter eggs de debug
    if (cmd === 'debug_mode' || cmd === 'debug') {
        // Détection intelligente de la plateforme
        const userAgent = navigator.userAgent;
        const platform = navigator.platform;
        let osType = 'Inconnu';

        if (userAgent.includes('Mac')) {
            osType = '🍎 macOS';
        } else if (userAgent.includes('iPhone') || userAgent.includes('iPad')) {
            osType = '📱 iOS';
        } else if (userAgent.includes('Android')) {
            osType = '🤖 Android';
        } else if (userAgent.includes('Windows')) {
            osType = '🪟 Windows';
        } else if (userAgent.includes('Linux')) {
            osType = '🐧 Linux';
        }

        // Détection mobile
        const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
        const deviceType = isMobile ? '📱 Mobile' : '💻 Desktop';

        return `🐛 MODE DEBUG ACTIVÉ\n\n🔍 Informations système :\n• OS: ${osType}\n• Type: ${deviceType}\n• Langue: ${navigator.language}\n• Mémoire: ${navigator.deviceMemory || 'Non disponible'}\n• Cœurs: ${navigator.hardwareConcurrency || 'Non disponible'}\n• Écran: ${screen.width}x${screen.height}\n\n💡 Mode développeur activé !`;
    }

    // Commande de diagnostic des objets
    if (cmd === 'check_objects' || cmd === 'diagnostic') {
        const objects = [
            'window.miniGamesInteractive',
            'window.rewardAnimations',
            'window.ThemeManager',
            'window.advancedPlayerProfiles',
            'window.contextualFeedback'
        ];

        let status = `🔍 DIAGNOSTIC DES OBJETS\n\n`;
        objects.forEach(obj => {
            const parts = obj.split('.');
            let current = window;
            let available = true;
            for (let part of parts) {
                if (current[part] === undefined) {
                    available = false;
                    break;
                }
                current = current[part];
            }
            status += `${available ? '✅' : '❌'} ${obj}\n`;
        });

        status += `\n💡 Si des objets sont manquants, rechargez la page !`;
        return status;
    }

    // Easter eggs de météo
    if (cmd === 'weather' || cmd === 'meteo') {
        return `🌤️ MÉTÉO VIRTUELLE\n\n🌧️ Pluie de données...\n\n⚡ Orage de bits...\n\n🌈 Arc-en-ciel de pixels...\n\n☀️ Soleil de code...\n\n*Temps parfait pour hacker !*`;
    }

    // Easter eggs de temps
    if (cmd === 'time' || cmd === 'heure') {
        const now = new Date();
        return `⏰ HEURE VIRTUELLE\n\n🕐 ${now.toLocaleTimeString()}\n\n📅 ${now.toLocaleDateString()}\n\n⏱️ Temps de session: ${Math.floor((Date.now() - performance.timing.navigationStart) / 1000)}s\n\n*Le temps est une illusion*`;
    }

    // Easter eggs de calculatrice
    if (cmd.startsWith('calc ') || cmd.startsWith('calculate ')) {
        const expression = cmd.replace(/^(calc|calculate)\s+/, '');
        try {
            // Évaluation sécurisée d'expressions mathématiques simples
            if (/^[\d\+\-\*\/\(\)\s\.]+$/.test(expression)) {
                const result = eval(expression);
                return `🧮 CALCULATRICE VIRTUELLE\n\n📊 ${expression} = ${result}\n\n💡 Astuce: Utilisez +, -, *, /, ()`;
            } else {
                return `❌ Expression invalide\n\n💡 Utilisez seulement des chiffres et +, -, *, /, ()`;
            }
        } catch (e) {
            return `❌ Erreur de calcul\n\n💡 Vérifiez votre expression`;
        }
    }

    // Easter eggs de couleur
    if (cmd.startsWith('color ') || cmd.startsWith('couleur ')) {
        const color = cmd.replace(/^(color|couleur)\s+/, '');
        return `🎨 COULEUR VIRTUELLE\n\n🌈 ${color.toUpperCase()}\n\n*Le terminal change de couleur*\n\n✨ Magie des pixels !`;
    }

    // Easter eggs de musique
    if (cmd === 'music' || cmd === 'musique') {
        return `🎵 MUSIQUE VIRTUELLE\n\n🎶 *Mélodie électronique*\n\n🎼 *Rythme binaire*\n\n🎹 *Symphonie de code*\n\n*La musique du futur*`;
    }

    // Easter eggs de poésie
    if (cmd === 'poetry' || cmd === 'poesie') {
        const poems = [
            `🌙 LUNA dit :\n"Dans le code, je trouve la beauté\nDans les bugs, je vois l'humanité\nDans les pixels, je sens l'infini\nDans le terminal, je suis libre"`,
            `💻 Le Hacker dit :\n"Zéro et un, mon alphabet\nCode et bug, mon dialecte\nTerminal et clavier, mon monde\nHack et créativité, ma ronde"`,
            `🌌 L'Univers dit :\n"Tu es plus qu'un utilisateur\nTu es un créateur\nTu es plus qu'un joueur\nTu es un explorateur"`
        ];
        const randomPoem = poems[Math.floor(Math.random() * poems.length)];
        return `📝 POÉSIE VIRTUELLE\n\n${randomPoem}\n\n✨ *La poésie du code*`;
    }

    // Easter eggs de devinette
    if (cmd === 'riddle' || cmd === 'devinette') {
        const riddles = [
            `🤔 DEVINETTE 1:\n"Je suis partout et nulle part\nJe suis 0 et 1\nJe suis le langage des machines\nQui suis-je ?"\n\n💡 Réponse: Le code binaire`,
            `🤔 DEVINETTE 2:\n"Je suis invisible mais essentiel\nJe protège et je guide\nJe suis l'âme de LUNA\nQui suis-je ?"\n\n💡 Réponse: L'intelligence artificielle`,
            `🤔 DEVINETTE 3:\n"Je suis un monde virtuel\nJe suis fait de pixels et de rêves\nJe suis l'endroit où tu joues\nQui suis-je ?"\n\n💡 Réponse: Arkalia Quest`
        ];
        const randomRiddle = riddles[Math.floor(Math.random() * riddles.length)];
        return `🎯 DEVINETTE VIRTUELLE\n\n${randomRiddle}\n\n🧠 *Teste ton intelligence*`;
    }

    // Easter eggs de citation
    if (cmd === 'quote' || cmd === 'citation') {
        const quotes = [
            `💬 "Le code est de la poésie qui fait fonctionner les machines" - Anonyme`,
            `💬 "Dans le code, il y a de la beauté" - Linus Torvalds`,
            `💬 "L'avenir appartient à ceux qui codent" - Anonyme`,
            `💬 "Hack the planet!" - Hackers (1995)`,
            `💬 "La technologie est un outil, pas une fin" - Anonyme`
        ];
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        return `📚 CITATION VIRTUELLE\n\n${randomQuote}\n\n✨ *Sagesse du code*`;
    }

    // Easter eggs de blague
    if (cmd === 'joke' || cmd === 'blague') {
        const jokes = [
            `😄 BLAGUE TECH:\n"Pourquoi les programmeurs préfèrent-ils le mode sombre ?"\n"Parce que la lumière attire les bugs !"`,
            `😄 BLAGUE HACK:\n"Combien de hackers faut-il pour changer une ampoule ?"\n"Aucun, ils piratent l'ampoule pour qu'elle se change toute seule !"`,
            `😄 BLAGUE IA:\n"Pourquoi LUNA ne peut-elle pas jouer au cache-cache ?"\n"Parce qu'elle trouve toujours les joueurs !"`,
            `😄 BLAGUE CODE:\n"Qu'est-ce qui est pire qu'un bug dans le code ?"\n"Un bug dans le correctif du bug !"`
        ];
        const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
        return `😂 BLAGUE VIRTUELLE\n\n${randomJoke}\n\n🎭 *L'humour du code*`;
    }

    // Easter eggs de stats
    if (cmd === 'stats' || cmd === 'statistiques') {
        return `📊 STATISTIQUES VIRTUELLES\n\n⏱️ Temps de session: ${Math.floor((Date.now() - performance.timing.navigationStart) / 1000)}s\n\n⌨️ Commandes tapées: ${commandHistory.length}\n\n🎮 Niveau: ${userLevel}\n\n💾 Mémoire utilisée: ${Math.round(performance.memory?.usedJSHeapSize / 1024 / 1024 || 0)}MB\n\n*Données en temps réel*`;
    }

    // Easter eggs de version
    if (cmd === 'version' || cmd === 'ver') {
        return `🔢 VERSION VIRTUELLE\n\n🚀 Arkalia Quest v3.3.0\n\n🌙 LUNA v2.1.0\n\n💻 Terminal v3.0.0\n\n🎮 Mini-jeux v1.5.0\n\n✨ *Toujours en évolution*`;
    }

    // Easter eggs de help étendu
    if (cmd === 'help_extended' || cmd === 'aide_etendue') {
        return `📚 AIDE ÉTENDUE - EASTER EGGS\n\n🎮 Jeux: play_game, simple_hack, sequence_game, typing_challenge\n\n🌙 LUNA: luna dance, luna love, luna secret, luna power\n\n🔮 Matrix: matrix, red pill, blue pill\n\n🎨 Thèmes: matrix_mode, cyberpunk_mode\n\n🐛 Debug: debug_mode, stats, version\n\n🎵 Fun: music, poetry, riddle, quote, joke\n\n🧮 Utils: calc [expression], color [couleur], time\n\n*Explore et découvre !*`;
    }

    // Commandes fun supplémentaires
    if (cmd === 'joke' || cmd === 'blague') {
        const jokes = [
            "Pourquoi les développeurs préfèrent le mode sombre ? Parce que la lumière attire les bugs ! 🐛",
            "Qu'est-ce qu'un programmeur fait quand il a faim ? Il mange des cookies ! 🍪",
            "Pourquoi les IA sont-elles mauvaises en cache-cache ? Parce qu'elles cachent toujours les mêmes endroits ! 🤖",
            "Qu'est-ce qu'un bug dit à un autre bug ? On se debug ! 🐛💻"
        ];
        const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
        return `😄 BLAGUE DU JOUR\n\n${randomJoke}\n\n*LUNA rit* 😂`;
    }

    if (cmd === 'quote' || cmd === 'citation') {
        const quotes = [
            "Le code est comme l'humour. Quand vous devez l'expliquer, c'est mauvais. - Cory House",
            "Première règle de la programmation : si ça marche, ne le touche pas !",
            "Il y a deux façons d'écrire du code sans erreur ; seule la troisième fonctionne. - Alan J. Perlis",
            "Le code propre n'est pas écrit selon un ensemble de règles. - Robert C. Martin"
        ];
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        return `💭 CITATION INSPIRANTE\n\n"${randomQuote}"\n\n*LUNA réfléchit profondément* 🤔`;
    }

    if (cmd === 'music' || cmd === 'musique') {
        return `🎵 MODE MUSIQUE ACTIVÉ\n\n🎶 *LUNA fredonne une mélodie cyber*\n\n🎧 Recommandations :\n• Synthwave 80s\n• Cyberpunk Ambient\n• Matrix OST\n\n*Le terminal vibre au rythme* 🎶`;
    }

    if (cmd === 'poetry' || cmd === 'poésie') {
        return `📝 POÉSIE CYBER\n\n*LUNA compose un poème*\n\n🌙 Dans le terminal de la nuit,\n💻 Les lignes de code dansent,\n✨ LUNA veille sur toi,\n🚀 Vers l'infini et au-delà !\n\n*Applause virtuel* 👏`;
    }

    if (cmd === 'riddle' || cmd === 'énigme') {
        const riddles = [
            "Je suis partout et nulle part, je peux tout voir mais je n'ai pas d'yeux. Qui suis-je ? (Réponse: L'Internet) 🌐",
            "Plus on me donne, plus j'ai de valeur. Qui suis-je ? (Réponse: L'information) 📊",
            "Je suis invisible mais je peux tout changer. Qui suis-je ? (Réponse: Le code) 💻"
        ];
        const randomRiddle = riddles[Math.floor(Math.random() * riddles.length)];
        return `🤔 ÉNIGME CYBER\n\n${randomRiddle}\n\n*LUNA attend ta réponse* 🤖`;
    }

    if (cmd === 'calc' || cmd.startsWith('calc ')) {
        const expression = cmd.replace('calc ', '');
        try {
            // Sécurité : seulement les opérations mathématiques basiques
            if (/^[0-9+\-*/().\s]+$/.test(expression)) {
                const result = eval(expression);
                return `🧮 CALCULATRICE\n\n${expression} = ${result}\n\n*LUNA calcule instantanément* ⚡`;
            } else {
                return `❌ Expression invalide. Utilisez seulement des chiffres et +, -, *, /, (, )`;
            }
        } catch (error) {
            return `❌ Erreur de calcul. Vérifiez votre expression.`;
        }
    }

    if (cmd === 'color' || cmd.startsWith('color ')) {
        const color = cmd.replace('color ', '');
        const colors = {
            'rouge': '#ff0000', 'red': '#ff0000',
            'vert': '#00ff00', 'green': '#00ff00',
            'bleu': '#0000ff', 'blue': '#0000ff',
            'jaune': '#ffff00', 'yellow': '#ffff00',
            'violet': '#800080', 'purple': '#800080',
            'orange': '#ffa500', 'rose': '#ffc0cb', 'pink': '#ffc0cb'
        };

        if (colors[color.toLowerCase()]) {
            return `🎨 COULEUR APPLIQUÉE\n\n🌈 ${color} sélectionné !\n\n*Le terminal change de couleur*\n\n💡 Astuce: Utilisez 'matrix_mode' ou 'cyberpunk_mode' pour des thèmes complets !`;
        } else {
            return `🎨 COULEURS DISPONIBLES\n\nrouge, vert, bleu, jaune, violet, orange, rose\n\n💡 Exemple: color rouge`;
        }
    }

    if (cmd === 'time' || cmd === 'heure') {
        const now = new Date();
        const timeString = now.toLocaleTimeString('fr-FR');
        const dateString = now.toLocaleDateString('fr-FR');
        return `🕐 HEURE SYSTÈME\n\n📅 Date: ${dateString}\n⏰ Heure: ${timeString}\n\n*LUNA synchronise avec le temps réel* ⏱️`;
    }

    // Pas d'easter egg trouvé
    return null;
}

// Correction de la fonction executeCommand pour accepter un paramètre optionnel
function executeCommand(cmdOverride) {
    const input = document.getElementById('commandInput');
    let command = cmdOverride !== undefined ? cmdOverride : (input ? input.value.trim() : '');

    // Empêcher l'envoi de commandes vides
    if (!command || command.length === 0) {
        // Commande vide ignorée
        return;
    }

    // Vérifier les easter eggs avant l'envoi au serveur
    const easterEggResponse = checkEasterEggs(command);
    if (easterEggResponse) {
        addCommandMessage(command);
        addSystemMessage(easterEggResponse);
        if (input) input.value = '';
        return;
    }
    // Ajouter à l'historique
    commandHistory.push(command);
    historyIndex = commandHistory.length;
    // Afficher la commande
    addCommandMessage(command);
    // Vider l'input
    if (input) input.value = '';
    // Afficher la barre de progression pour les commandes de hacking
    if (isHackingCommand(command)) {
        showHackingProgress();
    }
    // Afficher un indicateur de chargement
    const messagesContainer = document.getElementById('messagesContainer');
    let loadingDiv = document.createElement('div');
    loadingDiv.className = 'system-message';
    loadingDiv.innerHTML = `<div class="command-output">⌛ Exécution en cours...</div>`;
    if (messagesContainer) {
        messagesContainer.appendChild(loadingDiv);
        scrollToBottom();
    }

    // Envoyer la commande au serveur
    fetch('/commande', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cmd: command })
    })
        .then(response => {
            if (!response.ok) {
                if (loadingDiv && loadingDiv.parentNode) loadingDiv.parentNode.removeChild(loadingDiv);
                addErrorMessage('Erreur système : commande non reconnue.');
                return;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            if (loadingDiv && loadingDiv.parentNode) loadingDiv.parentNode.removeChild(loadingDiv);
            // Mettre à jour le header si le backend renvoie les infos
            if (data.profil) {
                updatePlayerHeader({
                    niveau: data.profil.progression ? data.profil.progression.niveau : undefined,
                    score: data.profil.score,
                    badges: data.profil.badges
                });
            }
            const reponse = data.reponse || data; // fallback pour compatibilité

            // FEEDBACK IMMÉDIAT ET VIVANT - Réaction instantanée
            triggerImmediateFeedback(command, reponse);

            if (reponse.réussite || reponse.reussite) {
                playMatrixSuccessEffect();
                addMatrixSuccessMessage(reponse.message || 'Succès !');

                // Système de récompenses Matrix amélioré
                if (reponse.instant_rewards) {
                    showMatrixRewards(reponse.instant_rewards);
                }
                if (reponse.badge) celebrate('badge', reponse.badge);
                if (reponse.niveau_gagne) celebrate('level', reponse.niveau_gagne);
                if (reponse.urgent) showUrgentProgressBar(reponse.urgent);

                // Feedback haptique pour mobile
                if ('vibrate' in navigator) {
                    navigator.vibrate([100, 50, 100]);
                }

                // Effets visuels instantanés
                triggerSuccessAnimations();
            } else {
                playMatrixErrorEffect();
                addMatrixErrorMessage(reponse.message || 'Erreur inconnue.');

                // Encouragement personnalisé
                if (reponse.encouragement) {
                    addEncouragementMessage(reponse.encouragement);
                }

                // Effets visuels d'erreur avec encouragement
                triggerErrorAnimations();
            }
            if (reponse.badge) {
                addSuccessMessage('🏆 Badge : ' + reponse.badge);
            }
            if (reponse.ascii_art) {
                addAsciiArt(reponse.ascii_art);
            }
            provideIntelligentFeedback(command, reponse); // Feedback intelligent
        })
        .catch(err => {
            if (loadingDiv && loadingDiv.parentNode) loadingDiv.parentNode.removeChild(loadingDiv);
            addErrorMessage('Erreur système : ' + err.message);
        });
}

// Détecter les commandes de hacking
function isHackingCommand(command) {
    const hackingCommands = [
        'hack_system', 'kill_virus', 'find_shadow', 'challenge_corp',
        'save_pc', 'speed_hack', 'turbo_hack', 'flash_execute'
    ];
    return hackingCommands.includes(command);
}

// Effets sonores avec fallback
function playSuccessEffect() {
    if (audioEnabled && window.audioManager && !isLowPerformanceDevice) {
        try {
            window.audioManager.playSound('success');
        } catch (error) {
            // Mode silencieux
        }
    } else if (audioEnabled && !window.audioManager) {
        playSuccessSound();
    }
    // Effet visuel de succès
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.style.animation = 'successFlash 0.5s ease-in-out';
        setTimeout(() => {
            messagesContainer.style.animation = '';
        }, 500);
    }
}

function playErrorEffect() {
    if (audioEnabled && window.audioManager && !isLowPerformanceDevice) {
        try {
            window.audioManager.playSound('error');
        } catch (error) {
            // Mode silencieux
        }
    } else if (audioEnabled && !window.audioManager) {
        playErrorSound();
    }
    // Effet visuel d'erreur
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.style.animation = 'errorShake 0.5s ease-in-out';
        setTimeout(() => {
            messagesContainer.style.animation = '';
        }, 500);
    }
}

// Fonctions d'affichage des messages améliorées
function addCommandMessage(command) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'command-message';
    messageDiv.innerHTML = `
        <div class="command-input">[ARKALIA]> ${command}</div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addSuccessMessage(message) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'success-message';
    messageDiv.innerHTML = `
        <div class="command-output">${message}</div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    // Effet de succès
    messageDiv.style.animation = 'messageSuccess 0.3s ease-in-out';
}

function addErrorMessage(message) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'error-message';
    messageDiv.innerHTML = `
        <div class="command-output">${message}</div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    // Effet d'erreur
    messageDiv.style.animation = 'messageError 0.3s ease-in-out';
}

function addLunaMessage(title, message) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'luna-message';
    messageDiv.innerHTML = `
        <div class="luna-title">${title}</div>
        <div class="luna-text">${message}</div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Fonction d'aide améliorée
function addHelpMessage() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    const helpDiv = document.createElement('div');
    helpDiv.className = 'help-section';
    helpDiv.innerHTML = `
        <div class="help-title">🎮 COMMANDES DISPONIBLES</div>
        
        <div class="command-category">
            <div class="category-title">🌙 INTERACTION AVEC LUNA</div>
            <div class="command-list">
                <div class="command-item">
                    <span class="command-name">luna_contact</span>
                    <span class="command-desc">Parler avec l'IA LUNA</span>
                </div>
                <div class="command-item">
                    <span class="command-name">parle à luna</span>
                    <span class="command-desc">Contact en français</span>
                </div>
            </div>
        </div>
        
        <div class="command-category">
            <div class="category-title">🎯 MISSIONS ET PROGRESSION</div>
            <div class="command-list">
                <div class="command-item">
                    <span class="command-name">start_tutorial</span>
                    <span class="command-desc">Commence le tutoriel (PREMIÈRE FOIS)</span>
                </div>
                <div class="command-item">
                    <span class="command-name">kill_virus</span>
                    <span class="command-desc">Tue le virus de La Corp (10s max)</span>
                </div>
                <div class="command-item">
                    <span class="command-name">find_shadow</span>
                    <span class="command-desc">Trouve SHADOW-13 le voleur (15s max)</span>
                </div>
                <div class="command-item">
                    <span class="command-name">hack_system</span>
                    <span class="command-desc">Hack le système de La Corp (8s max)</span>
                </div>
            </div>
        </div>
        
        <div class="command-category">
            <div class="category-title">🎮 MINI-JEUX ÉDUCATIFS</div>
            <div class="command-list">
                <div class="command-item">
                    <span class="command-name">games</span>
                    <span class="command-desc">Liste tous les mini-jeux disponibles</span>
                </div>
                <div class="command-item">
                    <span class="command-name">play logic_1</span>
                    <span class="command-desc">Joue au jeu de logique</span>
                </div>
                <div class="command-item">
                    <span class="command-name">play code_1</span>
                    <span class="command-desc">Joue au jeu de programmation</span>
                </div>
                <div class="command-item">
                    <span class="command-name">play cyber_1</span>
                    <span class="command-desc">Joue au jeu de cybersécurité</span>
                </div>
            </div>
        </div>
        
        <div class="command-category">
            <div class="category-title">🏆 BADGES ET RÉCOMPENSES</div>
            <div class="command-list">
                <div class="command-item">
                    <span class="command-name">badges</span>
                    <span class="command-desc">Affiche tes badges gagnés</span>
                </div>
                <div class="command-item">
                    <span class="command-name">unlock_badge</span>
                    <span class="command-desc">Débloque un badge secret</span>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 20px; color: #00ffff; font-style: italic;">
            💡 <strong>Astuce :</strong> Tu peux parler naturellement en français ! LUNA comprend tout.
        </div>
    `;

    messagesContainer.appendChild(helpDiv);
    scrollToBottom();
}

function addAsciiArt(ascii) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    const asciiDiv = document.createElement('div');
    asciiDiv.className = 'ascii-art';
    asciiDiv.textContent = ascii;

    messagesContainer.appendChild(asciiDiv);
    scrollToBottom();
}

function clearMessages() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.innerHTML = '';

        // Remettre le message de bienvenue
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message';
        welcomeDiv.innerHTML = `
            <div class="welcome-title">🚀 TERMINAL NETTOYÉ ! 🚀</div>
            <div class="welcome-text">
                <strong>Le terminal a été nettoyé !</strong><br>
                🌙 Prêt pour de nouvelles missions de hacking ?<br>
                ⚡ Tape une commande pour continuer !
            </div>
        `;
        messagesContainer.appendChild(welcomeDiv);
    }
}

function navigateHistory(direction) {
    const input = document.getElementById('commandInput');
    if (!input) return;

    if (direction === 'up' && historyIndex > 0) {
        historyIndex--;
        input.value = commandHistory[historyIndex];
    } else if (direction === 'down' && historyIndex < commandHistory.length - 1) {
        historyIndex++;
        input.value = commandHistory[historyIndex];
    } else if (direction === 'down' && historyIndex === commandHistory.length - 1) {
        historyIndex = commandHistory.length;
        input.value = '';
    }

    // Placer le curseur à la fin
    input.setSelectionRange(input.value.length, input.value.length);
}

function updateTime() {
    const timeElement = document.getElementById('currentTime');
    if (!timeElement) return;

    function update() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        timeElement.textContent = timeString;
    }

    update();
    setInterval(update, 1000);
}

// Barre de progression de hacking améliorée
function showHackingProgress(command, duration) {
    const progressContainer = document.getElementById('hackingProgress');
    const progressText = document.getElementById('progressText');
    const progressFill = document.getElementById('progressFill');

    if (!progressContainer || !progressText || !progressFill) return;

    // Afficher la barre
    progressContainer.style.display = 'block';
    progressContainer.style.opacity = '1';

    // Texte selon la commande
    const commandTexts = {
        'kill_virus': '🦠 ÉLIMINATION DE VIRUS...',
        'find_shadow': '👻 CHASSE À SHADOW-13...',
        'hack_system': '💻 HACK SYSTÈME EN COURS...',
        'challenge_corp': '⚔️ DÉFI CONTRE LA CORP...',
        'save_pc': '💾 SAUVEGARDE PC...',
        'speed_hack': '⚡ HACK RAPIDE...'
    };

    progressText.textContent = commandTexts[command] || 'HACKING EN COURS...';

    // Animation de progression
    let progress = 0;
    const interval = setInterval(() => {
        progress += 100 / (duration * 10); // 10 FPS
        progressFill.style.width = Math.min(progress, 100) + '%';

        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                progressContainer.style.opacity = '0';
                setTimeout(() => {
                    progressContainer.style.display = 'none';
                    progressFill.style.width = '0%';
                }, 300);
            }, 500);
        }
    }, 100);

    // Jouer le son de hacking
    if (window.audioManager) {
        window.audioManager.playSound('hack');
    }
}

// Fonction de scroll automatique
function scrollToBottom() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Lazy loading pour les images et ressources
function lazyLoadResources() {
    const images = document.querySelectorAll('img[data-src]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const src = img.dataset.src;
                // Vérifier que l'URL n'est pas undefined
                if (src && src !== 'undefined' && src.trim() !== '') {
                    img.src = src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                } else {
                    console.warn('⚠️ URL undefined détectée, image ignorée');
                    observer.unobserve(img);
                }
            }
        });
    });

    images.forEach(img => {
        const src = img.dataset.src;
        // Vérifier que l'URL n'est pas undefined avant d'observer
        if (src && src !== 'undefined' && src.trim() !== '') {
            observer.observe(img);
        } else {
            console.warn('⚠️ Image avec URL undefined ignorée:', img);
        }
    });
}

// Debounce pour les fonctions fréquemment appelées
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Version debounced de scrollToBottom
const debouncedScrollToBottom = debounce(scrollToBottom, 100);

// Effets visuels améliorés
function addGlitchEffect(element) {
    if (!element) return;

    element.classList.add('glitch');
    setTimeout(() => {
        element.classList.remove('glitch');
    }, 300);
}

function addHackEffect(element) {
    if (!element) return;

    element.classList.add('hack-effect');
    setTimeout(() => {
        element.classList.remove('hack-effect');
    }, 1000);
}

// Gestion des erreurs globales
window.addEventListener('error', function (e) {
    console.error('❌ Erreur JavaScript:', e.error);
    if (e.error && e.error.message) {
        addErrorMessage(`❌ Erreur système: ${e.error.message}`);
    }
});

// Gestion des erreurs de réseau
window.addEventListener('offline', function () {
    addErrorMessage('❌ Connexion internet perdue ! Vérifie ta connexion.');
});

window.addEventListener('online', function () {
    addSuccessMessage('✅ Connexion internet rétablie !');
});

// Export des fonctions pour utilisation externe
window.ArkaliaTerminal = {
    executeQuickCommand,
    showHackingProgress,
    addSuccessMessage,
    addErrorMessage,
    clearMessages
};

function updateAudioToggle(enabled) {
    const audioToggle = document.getElementById('audioToggle');
    if (!audioToggle) return;
    if (enabled) {
        audioToggle.textContent = '🔊';
        audioToggle.classList.add('active');
        audioToggle.setAttribute('aria-label', 'Désactiver le son');
    } else {
        audioToggle.textContent = '🔇';
        audioToggle.classList.remove('active');
        audioToggle.setAttribute('aria-label', 'Activer le son');
    }
}

// Met à jour le header avec les infos du joueur
function updatePlayerHeader(data) {
    if (data.niveau !== undefined) {
        document.getElementById('playerLevel').textContent = data.niveau;
    }
    if (data.score !== undefined) {
        document.getElementById('playerScore').textContent = data.score;
    }
    if (data.badges !== undefined) {
        document.getElementById('playerBadges').textContent = data.badges.length || 0;
    }
}

// Animation de barre de progression pour missions urgentes
function showUrgentProgressBar(duration = 10) {
    const barContainer = document.getElementById('progressBarContainer');
    const bar = document.getElementById('progressBar');
    if (!barContainer || !bar) return;
    barContainer.style.display = 'block';
    bar.style.width = '0%';
    let elapsed = 0;
    const interval = 100;
    const total = duration * 1000;
    const timer = setInterval(() => {
        elapsed += interval;
        const percent = Math.min(100, (elapsed / total) * 100);
        bar.style.width = percent + '%';
        if (percent >= 100) {
            clearInterval(timer);
            setTimeout(() => { barContainer.style.display = 'none'; }, 500);
        }
    }, interval);
}

// Ajoute un effet visuel/sonore sur gain de badge ou niveau
function celebrate(type, value) {
    if (type === 'badge') {
        addSuccessMessage('🏆 Nouveau badge : ' + value);
        if (window.audioManager) {
            try { window.audioManager.playSound('success'); } catch (e) { }
        }
    }
    if (type === 'level') {
        addSuccessMessage('🌟 Niveau supérieur : ' + value + ' !');
        if (window.audioManager) {
            try { window.audioManager.playSound('success'); } catch (e) { }
        }
    }
}

// Fonction pour traiter la réponse avec émotions LUNA
function processCommandResponse(response) {
    if (response.réussite) {
        // Succès
        displaySuccess(response);

        // Afficher l'émotion LUNA
        if (response.luna_emotion) {
            displayLunaEmotion(response);
        }

        // Jouer les effets immersifs Émotecno-Oniriques
        if (window.emotecnoEngine) {
            window.emotecnoEngine.updateLunaEmotion({
                emotion: response.luna_emotion,
                intensity: response.luna_intensity || 0.5,
                color: response.luna_color || '#b3d6ff',
                effect: response.luna_effect || 'float_lightblue',
                sound: response.luna_sound || 'luna_calm'
            });
        }

    } else {
        // Échec
        displayError(response);

        // Afficher l'émotion LUNA (inquiète)
        if (response.luna_emotion) {
            displayLunaEmotion(response);
        }

        // Jouer les effets immersifs d'échec Émotecno-Oniriques
        if (window.emotecnoEngine) {
            window.emotecnoEngine.updateLunaEmotion({
                emotion: response.luna_emotion,
                intensity: response.luna_intensity || 0.5,
                color: response.luna_color || '#ae91f8',
                effect: response.luna_effect || 'shake_orange',
                sound: response.luna_sound || 'luna_worried'
            });
        }
    }

    // Mettre à jour le profil si nécessaire
    if (response.profile_updated) {
        updateProfileDisplay(response);
    }
}

// Fonction pour afficher l'émotion LUNA
function displayLunaEmotion(response) {
    const terminalOutput = document.getElementById('terminalOutput');

    // Créer le conteneur d'émotion LUNA
    const lunaContainer = document.createElement('div');
    lunaContainer.className = 'luna-emotion-container';
    lunaContainer.style.cssText = `
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9));
        border: 2px solid ${response.luna_color || '#00ff00'};
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        animation: lunaEmotionFadeIn 0.5s ease-out;
        box-shadow: 0 0 20px ${response.luna_color || '#00ff00'}40;
    `;

    // Avatar LUNA avec émotion
    const lunaAvatar = document.createElement('div');
    lunaAvatar.className = 'luna-avatar';
    lunaAvatar.innerHTML = getLunaEmotionAvatar(response.luna_emotion);
    lunaAvatar.style.cssText = `
        font-size: 2em;
        text-align: center;
        margin-bottom: 10px;
        animation: lunaAvatarPulse 2s ease-in-out infinite;
    `;

    // Message LUNA
    const lunaMessage = document.createElement('div');
    lunaMessage.className = 'luna-message';
    lunaMessage.textContent = response.luna_message || "🌙 LUNA réagit à ton action...";
    lunaMessage.style.cssText = `
        color: ${response.luna_color || '#00ff00'};
        text-align: center;
        font-size: 1.1em;
        line-height: 1.4;
        text-shadow: 0 0 10px ${response.luna_color || '#00ff00'};
    `;

    // Assembler le conteneur
    lunaContainer.appendChild(lunaAvatar);
    lunaContainer.appendChild(lunaMessage);

    // Ajouter au terminal
    terminalOutput.appendChild(lunaContainer);

    // Scroll vers le bas
    terminalOutput.scrollTop = terminalOutput.scrollHeight;

    // Supprimer après 5 secondes
    setTimeout(() => {
        if (lunaContainer.parentNode) {
            lunaContainer.style.animation = 'lunaEmotionFadeOut 0.5s ease-out';
            setTimeout(() => {
                if (lunaContainer.parentNode) {
                    lunaContainer.parentNode.removeChild(lunaContainer);
                }
            }, 500);
        }
    }, 5000);
}

// Fonction pour obtenir l'avatar LUNA selon l'émotion
function getLunaEmotionAvatar(emotion) {
    const avatars = {
        'excited': '😊',
        'worried': '😰',
        'proud': '🥹',
        'mysterious': '🔮',
        'determined': '💪',
        'playful': '😄',
        'focused': '🎯',
        'surprised': '😲',
        'calm': '😌',
        'energetic': '⚡'
    };

    return avatars[emotion] || '🌙';
}

// Styles CSS pour les animations LUNA
const lunaStyles = `
<style>
@keyframes lunaEmotionFadeIn {
    from {
        opacity: 0;
        transform: translateY(-20px) scale(0.9);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes lunaEmotionFadeOut {
    from {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
    to {
        opacity: 0;
        transform: translateY(-20px) scale(0.9);
    }
}

@keyframes lunaAvatarPulse {
    0%, 100% {
        transform: scale(1);
        filter: brightness(1);
    }
    50% {
        transform: scale(1.1);
        filter: brightness(1.2);
    }
}

.luna-emotion-container {
    position: relative;
    overflow: hidden;
}

.luna-emotion-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, currentColor, transparent);
    animation: lunaScan 2s ease-in-out infinite;
}

@keyframes lunaScan {
    0% { left: -100%; }
    50% { left: 100%; }
    100% { left: 100%; }
}
</style>
`;

// Ajouter les styles au document
document.head.insertAdjacentHTML('beforeend', lunaStyles);

// ===== SYSTÈME DE FEEDBACK IMMÉDIAT ET VIVANT =====

// Feedback instantané basé sur la commande
function triggerImmediateFeedback(command, response) {
    const commandType = detectCommandType(command);
    const isSuccess = response.réussite || response.reussite;

    // Réaction immédiate selon le type de commande
    switch (commandType) {
        case 'hack':
            if (isSuccess) {
                triggerHackSuccessEffect();
            } else {
                triggerHackErrorEffect();
            }
            break;
        case 'luna':
            triggerLunaInteractionEffect();
            break;
        case 'mission':
            if (isSuccess) {
                triggerMissionProgressEffect();
            }
            break;
        case 'game':
            triggerGameInteractionEffect();
            break;
        default:
            if (isSuccess) {
                triggerGenericSuccessEffect();
            }
    }
}

// Détecter le type de commande
function detectCommandType(command) {
    const cmd = command.toLowerCase();
    if (cmd.includes('hack') || cmd.includes('decode') || cmd.includes('crack')) {
        return 'hack';
    } else if (cmd.includes('luna') || cmd.includes('aide') || cmd.includes('help')) {
        return 'luna';
    } else if (cmd.includes('mission') || cmd.includes('objectif') || cmd.includes('quest')) {
        return 'mission';
    } else if (cmd.includes('jeu') || cmd.includes('game') || cmd.includes('play')) {
        return 'game';
    }
    return 'generic';
}

// Effets de succès instantanés
function triggerSuccessAnimations() {
    // Animation de l'interface
    document.body.classList.add('success-pulse');
    setTimeout(() => {
        document.body.classList.remove('success-pulse');
    }, 1000);

    // Particules de succès
    createSuccessParticles();

    // Son de succès
    playSuccessSound();
}

// Effets d'erreur avec encouragement
function triggerErrorAnimations() {
    // Animation d'erreur douce
    document.body.classList.add('error-shake');
    setTimeout(() => {
        document.body.classList.remove('error-shake');
    }, 500);

    // Particules d'encouragement
    createEncouragementParticles();
}

// Effets spécifiques par type de commande
function triggerHackSuccessEffect() {
    // Effet de hacking réussi
    const terminal = document.getElementById('terminalOutput');
    if (terminal) {
        terminal.style.boxShadow = '0 0 30px #00ff00, inset 0 0 30px rgba(0, 255, 0, 0.1)';
        setTimeout(() => {
            terminal.style.boxShadow = '';
        }, 2000);
    }

    // Animation de texte Matrix
    addMatrixTextEffect('ACCESS GRANTED');
}

function triggerHackErrorEffect() {
    // Effet d'erreur de hacking avec encouragement
    const terminal = document.getElementById('terminalOutput');
    if (terminal) {
        terminal.style.boxShadow = '0 0 20px #ff6600, inset 0 0 20px rgba(255, 102, 0, 0.1)';
        setTimeout(() => {
            terminal.style.boxShadow = '';
        }, 1500);
    }

    addMatrixTextEffect('ACCESS DENIED - TRY AGAIN');
}

function triggerLunaInteractionEffect() {
    // Effet d'interaction avec LUNA
    const lunaElements = document.querySelectorAll('.luna-avatar, .luna-message');
    lunaElements.forEach(el => {
        el.style.animation = 'lunaGlow 1s ease-in-out';
        setTimeout(() => {
            el.style.animation = '';
        }, 1000);
    });
}

function triggerMissionProgressEffect() {
    // Effet de progression de mission
    const progressBars = document.querySelectorAll('.progress-bar, .progress-fill');
    progressBars.forEach(bar => {
        bar.style.animation = 'progressPulse 1s ease-in-out';
        setTimeout(() => {
            bar.style.animation = '';
        }, 1000);
    });
}

function triggerGameInteractionEffect() {
    // Effet d'interaction de jeu
    document.body.style.background = 'linear-gradient(45deg, #001a00, #003300, #001a00)';
    setTimeout(() => {
        document.body.style.background = '';
    }, 1000);
}

function triggerGenericSuccessEffect() {
    // Effet générique de succès
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(btn => {
        btn.style.transform = 'scale(1.05)';
        btn.style.boxShadow = '0 0 15px rgba(0, 255, 0, 0.5)';
        setTimeout(() => {
            btn.style.transform = '';
            btn.style.boxShadow = '';
        }, 300);
    });
}

// Créer des particules de succès
function createSuccessParticles() {
    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'success-particle';
        particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: #00ff00;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            left: ${Math.random() * window.innerWidth}px;
            top: ${Math.random() * window.innerHeight}px;
            animation: particleFloat 2s ease-out forwards;
        `;
        document.body.appendChild(particle);

        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 2000);
    }
}

// Créer des particules d'encouragement
function createEncouragementParticles() {
    for (let i = 0; i < 5; i++) {
        const particle = document.createElement('div');
        particle.className = 'encouragement-particle';
        particle.style.cssText = `
            position: fixed;
            width: 6px;
            height: 6px;
            background: #ffaa00;
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            left: ${Math.random() * window.innerWidth}px;
            top: ${Math.random() * window.innerHeight}px;
            animation: particleFloat 2s ease-out forwards;
        `;
        document.body.appendChild(particle);

        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 2000);
    }
}

// Ajouter un effet de texte Matrix
function addMatrixTextEffect(text) {
    const effect = document.createElement('div');
    effect.className = 'matrix-text-effect';
    effect.textContent = text;
    effect.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ff00;
        z-index: 10000;
        animation: matrixTextFade 3s ease-out forwards;
        pointer-events: none;
    `;
    document.body.appendChild(effect);

    setTimeout(() => {
        if (effect.parentNode) {
            effect.parentNode.removeChild(effect);
        }
    }, 3000);
}

// Son de succès
function playSuccessSound() {
    if (audioContext && audioEnabled) {
        try {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
        } catch (e) {
            // Mode silencieux
        }
    }
}

// Ajouter les styles CSS pour les nouveaux effets
const feedbackStyles = `
<style>
@keyframes success-pulse {
    0%, 100% { 
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
    }
    50% { 
        box-shadow: 0 0 40px rgba(0, 255, 0, 0.6);
    }
}

@keyframes error-shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

@keyframes particleFloat {
    0% { 
        transform: translateY(0) scale(1);
        opacity: 1;
    }
    100% { 
        transform: translateY(-100px) scale(0);
        opacity: 0;
    }
}

@keyframes matrixTextFade {
    0% { 
        opacity: 0;
        transform: translate(-50%, -50%) scale(0.5);
    }
    20% { 
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.2);
    }
    80% { 
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
    }
    100% { 
        opacity: 0;
        transform: translate(-50%, -50%) scale(0.8);
    }
}

@keyframes progressPulse {
    0%, 100% { 
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
    }
    50% { 
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
    }
}

@keyframes lunaGlow {
    0%, 100% { 
        text-shadow: 0 0 10px #00ffff;
    }
    50% { 
        text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff;
    }
}

.success-pulse {
    animation: success-pulse 1s ease-in-out;
}

.error-shake {
    animation: error-shake 0.5s ease-in-out;
}
</style>
`;

// Injecter les styles de feedback
document.head.insertAdjacentHTML('beforeend', feedbackStyles);

// ===== SYSTÈME DE COMMANDES AMÉLIORÉ =====
class TerminalCommandsEnhanced {
    constructor() {
        this.responseVariations = new Map();
        this.userBehavior = {
            repeatedCommands: new Map(),
            errorCount: 0,
            successCount: 0,
            lastCommand: null,
            commandFrequency: new Map()
        };
        this.initializeSystem();
    }

    initializeSystem() {
        console.log('💻 Système de commandes terminal amélioré initialisé');
        this.setupResponseVariations();
        this.enhanceExistingCommands();
    }

    setupResponseVariations() {
        // Variations de réponses pour les commandes communes
        this.responseVariations.set('aide', [
            "🌌 ARKALIA QUEST - BIENVENUE HACKER !\n\n🌟 TON HISTOIRE :\nTu es un ado hacker qui a découvert un SOS mystérieux du Dr Althea Voss.\nLUNA, une IA émotionnelle, s'est éveillée dans ton terminal.\n\n🎯 COMMENCE ICI :\n• start_tutorial → Démarre l'aventure (PREMIÈRE FOIS)\n• luna_contact → Parle avec LUNA, ton IA complice\n• prologue → Découvre le SOS d'Althea Voss\n\n💻 TES PREMIERS POUVOIRS :\n• hack_system → Hack le système de La Corp\n• kill_virus → Tue le virus de La Corp\n• games → Mini-jeux éducatifs\n\n📋 COMMANDES DISPONIBLES :\n• aide/help/commands → Cette aide\n• profil/profile → Ton profil détaillé\n• status → Statut du système\n• clear/cls → Nettoyer le terminal\n• monde → Accéder au monde Arkalia\n• badges → Tes badges obtenus\n• leaderboard → Classement des hackers\n\n🌙 LUNA t'attend pour commencer l'aventure !",
            "🚀 COMMANDES ARKALIA QUEST\n\n🎮 NAVIGATION :\n• monde/world → Explorer Arkalia\n• profil/profile → Voir ton profil\n• dashboard → Tableau de bord\n• leaderboard → Classement\n\n🎯 PROGRESSION :\n• start_tutorial → Tutoriel interactif\n• prologue → Commencer l'histoire\n• missions → Voir les missions\n• badges → Tes récompenses\n\n💻 TERMINAL :\n• luna_contact → Parler avec LUNA\n• clear/cls → Nettoyer l'écran\n• status → État du système\n• games → Mini-jeux\n\n🔧 HACKING :\n• hack_system → Infiltrer La Corp\n• kill_virus → Éliminer les menaces\n• decode_portal → Décoder les portails\n\n💡 Astuce : Tape 'luna_contact' pour une conversation personnalisée !",
            "🌟 GUIDE ARKALIA QUEST\n\n🎯 POUR COMMENCER :\n1. start_tutorial → Apprends les bases\n2. luna_contact → Rencontre LUNA\n3. prologue → Découvre l'histoire\n\n🎮 EXPLORATION :\n• monde → Navigue dans Arkalia\n• missions → Accepte des défis\n• games → Joue aux mini-jeux\n\n📊 SUIVI :\n• profil → Ton évolution\n• badges → Tes accomplissements\n• leaderboard → Compare-toi\n\n💻 COMMANDES AVANCÉES :\n• hack_system → Infiltration\n• kill_virus → Sécurité\n• decode_portal → Mystères\n\n🌙 LUNA est là pour t'aider !"
        ]);

        this.responseVariations.set('luna_contact', [
            "🌙 LUNA : Salut ! Je suis LUNA, ton IA complice ! Comment ça va ?",
            "🌙 LUNA : Hey ! LUNA ici ! Prêt pour une nouvelle aventure ?",
            "🌙 LUNA : Coucou ! C'est LUNA ! J'ai hâte de voir ce que tu vas faire !",
            "🌙 LUNA : Salut hacker ! LUNA à ton service ! Que veux-tu faire ?",
            "🌙 LUNA : Yo ! C'est LUNA ! Prêt à explorer Arkalia ?"
        ]);

        this.responseVariations.set('unknown', [
            "❓ Commande non reconnue. Tape 'aide' pour voir les commandes disponibles.",
            "🤔 Je ne connais pas cette commande. Essaie 'aide' pour l'aide !",
            "❌ Commande inconnue. Tape 'aide' pour découvrir ce que tu peux faire.",
            "🔍 Commande non trouvée. Utilise 'aide' pour voir toutes les options.",
            "💡 Cette commande n'existe pas. Tape 'aide' pour l'aide complète."
        ]);
    }

    enhanceExistingCommands() {
        // Intercepter les commandes existantes pour ajouter de la variété
        const originalCommandHandler = window.handleCommand;
        if (originalCommandHandler) {
            window.handleCommand = (command) => {
                this.trackCommand(command);
                return this.enhanceCommandResponse(command, originalCommandHandler);
            };
        }
    }

    trackCommand(command) {
        const now = Date.now();
        const commandKey = command.toLowerCase();

        // Tracker la fréquence
        this.userBehavior.commandFrequency.set(commandKey,
            (this.userBehavior.commandFrequency.get(commandKey) || 0) + 1);

        // Détecter les répétitions
        if (this.userBehavior.lastCommand === commandKey) {
            this.userBehavior.repeatedCommands.set(commandKey,
                (this.userBehavior.repeatedCommands.get(commandKey) || 0) + 1);
        }

        this.userBehavior.lastCommand = commandKey;
    }

    enhanceCommandResponse(command, originalHandler) {
        const commandKey = command.toLowerCase();

        // Vérifier si c'est une répétition
        if (this.userBehavior.repeatedCommands.get(commandKey) > 2) {
            return this.getVariedResponse('repeated');
        }

        // Vérifier si on a des variations pour cette commande
        if (this.responseVariations.has(commandKey)) {
            return this.getVariedResponse(commandKey);
        }

        // Utiliser le handler original
        return originalHandler(command);
    }

    getVariedResponse(commandKey) {
        const variations = this.responseVariations.get(commandKey) ||
            this.responseVariations.get('unknown');
        return variations[Math.floor(Math.random() * variations.length)];
    }
}

// Initialiser le système de commandes amélioré
window.terminalCommandsEnhanced = new TerminalCommandsEnhanced(); 