// ===== TERMINAL ARKALIA QUEST v2.0 - VERSION CORRIGÉE =====

// Variables globales
let audioEnabled = true;
let messageHistory = [];
let commandHistory = [];
let historyIndex = -1;
let hackingEffects = null;
let isLowPerformanceDevice = false;

// Détection des appareils faibles
function detectDevicePerformance() {
    const userAgent = navigator.userAgent.toLowerCase();
    const isMobile = /mobile|android|iphone|ipad/.test(userAgent);
    const isOldBrowser = /msie|trident/.test(userAgent);
    const hasLowMemory = navigator.deviceMemory && navigator.deviceMemory < 4;
    
    isLowPerformanceDevice = isMobile || isOldBrowser || hasLowMemory;
    
    if (isLowPerformanceDevice) {
        console.log('🔧 Mode performance réduite activé');
        disableHeavyEffects();
    }
}

// Désactiver les effets lourds
function disableHeavyEffects() {
    const style = document.createElement('style');
    style.textContent = `
        body::before, body::after { display: none !important; }
        .matrix-particles { display: none !important; }
        .hack-effect::before { display: none !important; }
    `;
    document.head.appendChild(style);
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    detectDevicePerformance();
    initTerminal();
    initHackingEffects();
    updateTime();
    // Gestion du bouton audio
    const audioToggle = document.getElementById('audioToggle');
    if (audioToggle) {
        // Charger l'état depuis localStorage
        audioEnabled = localStorage.getItem('arkalia_audio') !== 'off';
        updateAudioToggle(audioEnabled);
        audioToggle.addEventListener('click', function() {
            audioEnabled = !audioEnabled;
            localStorage.setItem('arkalia_audio', audioEnabled ? 'on' : 'off');
            updateAudioToggle(audioEnabled);
            if (window.ArkaliaEffects) {
                try {
                    window.ArkaliaEffects.getInstance().audioManager.muted = !audioEnabled;
                } catch (e) {}
            }
        });
    }
    
    // Démarrer l'ambiance sonore (avec fallback)
    setTimeout(() => {
        if (window.ArkaliaEffects && !isLowPerformanceDevice) {
            try {
                window.ArkaliaEffects.getInstance()?.audioManager.playAmbiance('matrix');
            } catch (error) {
                console.log('🔇 Audio non supporté, mode silencieux activé');
                audioEnabled = false;
            }
        }
    }, 1000);
});

// Initialisation des effets de hacking
function initHackingEffects() {
    try {
        if (window.HackingEffects) {
            hackingEffects = new window.HackingEffects();
            console.log('🎮 Effets de hacking initialisés');
        }
    } catch (error) {
        console.log('⚠️ Effets de hacking non disponibles');
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
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            executeCommand();
        }
    });
    
    // Gestion de l'historique avec flèches
    input.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            navigateHistory('up');
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            navigateHistory('down');
        }
    });
    
    // Effet de frappe (avec fallback)
    input.addEventListener('input', function() {
        if (audioEnabled && window.ArkaliaEffects && !isLowPerformanceDevice) {
            try {
                window.ArkaliaEffects.getInstance()?.audioManager.play('typing');
            } catch (error) {
                // Mode silencieux
            }
        }
    });
    
    // Feedback visuel des boutons
    setupButtonFeedback();
}

// Configuration du feedback des boutons
function setupButtonFeedback() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
        
        button.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 0 10px rgba(0, 255, 0, 0.5)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
}

// Fonction unifiée pour les commandes rapides
function executeQuickCommand(command, event) {
    console.log('🚀 Commande rapide exécutée:', command);
    // Effet visuel du bouton
    if (event && event.target) {
        const button = event.target;
        button.classList.add('button-clicked');
        setTimeout(() => button.classList.remove('button-clicked'), 200);
    }
    // Jouer le son de clic
    if (window.ArkaliaEffects) {
        try {
            window.ArkaliaEffects.getInstance()?.audioManager.playTypingSound();
        } catch (e) {}
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

// Correction de la fonction executeCommand pour accepter un paramètre optionnel
function executeCommand(cmdOverride) {
    const input = document.getElementById('commandInput');
    let command = cmdOverride !== undefined ? cmdOverride : (input ? input.value.trim() : '');
    if (!command) return;
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
            addErrorMessage('Erreur système : commande non reconnue.');
            return;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;
        // Mettre à jour le header si le backend renvoie les infos
        if (data.profil) {
            updatePlayerHeader({
                niveau: data.profil.progression ? data.profil.progression.niveau : undefined,
                score: data.profil.score,
                badges: data.profil.badges
            });
        }
        if (data.réussite || data.reussite) {
            playSuccessEffect();
            addSuccessMessage(data.message || 'Succès !');
            if (data.badge) celebrate('badge', data.badge);
            if (data.niveau_gagne) celebrate('level', data.niveau_gagne);
            if (data.urgent) showUrgentProgressBar(data.urgent);
        } else {
            playErrorEffect();
            addErrorMessage(data.message || 'Erreur inconnue.');
        }
        if (data.badge) {
            addSuccessMessage('🏆 Badge : ' + data.badge);
        }
        if (data.ascii_art) {
            addAsciiArt(data.ascii_art);
        }
    })
    .catch(err => {
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
    if (audioEnabled && window.ArkaliaEffects && !isLowPerformanceDevice) {
        try {
            window.ArkaliaEffects.getInstance()?.playSuccess();
        } catch (error) {
            // Mode silencieux
        }
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
    if (audioEnabled && window.ArkaliaEffects && !isLowPerformanceDevice) {
        try {
            window.ArkaliaEffects.getInstance()?.playError();
        } catch (error) {
            // Mode silencieux
        }
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
    if (window.ArkaliaEffects) {
        window.ArkaliaEffects.getInstance()?.playHack();
    }
}

// Fonction de scroll automatique
function scrollToBottom() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

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
window.addEventListener('error', function(e) {
    console.error('❌ Erreur JavaScript:', e.error);
    if (e.error && e.error.message) {
        addErrorMessage(`❌ Erreur système: ${e.error.message}`);
    }
});

// Gestion des erreurs de réseau
window.addEventListener('offline', function() {
    addErrorMessage('❌ Connexion internet perdue ! Vérifie ta connexion.');
});

window.addEventListener('online', function() {
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
        if (window.ArkaliaEffects) {
            try { window.ArkaliaEffects.getInstance().audioManager.playLevelUpSound(); } catch (e) {}
        }
    }
    if (type === 'level') {
        addSuccessMessage('🌟 Niveau supérieur : ' + value + ' !');
        if (window.ArkaliaEffects) {
            try { window.ArkaliaEffects.getInstance().audioManager.playLevelUpSound(); } catch (e) {}
        }
    }
} 