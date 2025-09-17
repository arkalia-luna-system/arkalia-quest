// ===== EFFETS DE HACKING ULTRA-ATTRACTIFS =====
// Spécialement conçu pour les ados de 13 ans !

class HackingEffects {
    constructor() {
        this.isActive = false;
        this.audioEnabled = true;
        this.init();
    }

    init() {
        // Effets de hacking initialisés
        this.createAudioContext();
        this.setupEventListeners();
    }

    // Création du contexte audio pour les effets sonores
    createAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            // Audio non supporté sur ce navigateur
            this.audioEnabled = false;
        }
    }

    // Configuration des écouteurs d'événements
    setupEventListeners() {
        // Effet de frappe sur l'input
        const input = document.getElementById('commandInput');
        if (input) {
            input.addEventListener('input', () => this.playTypingSound());
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    this.playHackSound();
                }
            });
        }

        // Effet sur les boutons
        const buttons = document.querySelectorAll('.quick-btn, #sendButton');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => this.playClickSound());
        });
    }

    // === EFFETS SONORES ===
    playTypingSound() {
        if (!this.audioEnabled) return;

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(600, this.audioContext.currentTime + 0.1);

            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.1);
        } catch (e) {
            // Ignore les erreurs audio
        }
    }

    playHackSound() {
        if (!this.audioEnabled) return;

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.setValueAtTime(200, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(800, this.audioContext.currentTime + 0.3);

            gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);
        } catch (e) {
            // Ignore les erreurs audio
        }
    }

    playClickSound() {
        if (!this.audioEnabled) return;

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.setValueAtTime(1000, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(500, this.audioContext.currentTime + 0.1);

            gainNode.gain.setValueAtTime(0.15, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.1);
        } catch (e) {
            // Ignore les erreurs audio
        }
    }

    // === EFFETS VISUELS ===

    // Animation de progression de hacking
    showHackingProgress(duration = 5000, command = 'HACKING') {
        const progressDiv = document.getElementById('hackingProgress');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');

        if (!progressDiv || !progressFill || !progressText) return;

        progressDiv.style.display = 'block';
        progressFill.style.width = '0%';

        const steps = [
            { percent: 25, text: '🔍 CONNEXION AU SYSTÈME...' },
            { percent: 50, text: '⚡ ANALYSE DES FAILLES...' },
            { percent: 75, text: '💻 EXPLOITATION EN COURS...' },
            { percent: 100, text: '🎉 HACK RÉUSSI ! ' + command }
        ];

        let currentStep = 0;
        const interval = setInterval(() => {
            const step = steps[currentStep];
            if (step) {
                progressFill.style.width = step.percent + '%';
                progressText.textContent = step.text;

                // Effet de flash
                progressDiv.style.boxShadow = '0 0 30px rgba(0, 255, 0, 0.8)';
                setTimeout(() => {
                    progressDiv.style.boxShadow = '0 0 15px rgba(0, 255, 0, 0.3)';
                }, 200);
            }

            currentStep++;

            if (currentStep >= steps.length) {
                clearInterval(interval);
                setTimeout(() => {
                    progressDiv.style.display = 'none';
                }, 2000);
            }
        }, duration / steps.length);
    }

    // Effet de glitch sur un élément
    addGlitchEffect(element, duration = 300) {
        if (!element) return;

        element.classList.add('glitch');
        setTimeout(() => {
            element.classList.remove('glitch');
        }, duration);
    }

    // Effet de hacking sur un élément
    addHackEffect(element, duration = 1000) {
        if (!element) return;

        element.classList.add('hack-effect');
        setTimeout(() => {
            element.classList.remove('hack-effect');
        }, duration);
    }

    // Animation de particules Luna
    createLunaParticles() {
        const container = document.querySelector('.terminal-container');
        if (!container) return;

        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                this.createParticle(container);
            }, i * 100);
        }
    }

    createParticle(container) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: #00ff00;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            animation: particleFall 2s linear forwards;
        `;

        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = '-10px';

        container.appendChild(particle);

        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 2000);
    }

    // Animation de texte qui s'écrit tout seul
    typeWriter(element, text, speed = 50) {
        if (!element) return;

        element.textContent = '';
        let i = 0;

        const typeInterval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                this.playTypingSound();
            } else {
                clearInterval(typeInterval);
            }
        }, speed);
    }

    // Effet de succès avec confettis
    showSuccessEffect() {
        this.createLunaParticles();
        this.playHackSound();

        // Flash vert sur tout l'écran
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 255, 0, 0.1);
            pointer-events: none;
            z-index: 9999;
            animation: successFlash 0.5s ease-out;
        `;

        document.body.appendChild(flash);

        setTimeout(() => {
            if (flash.parentNode) {
                flash.parentNode.removeChild(flash);
            }
        }, 500);
    }

    // Effet d'erreur avec tremblement
    showErrorEffect() {
        const container = document.querySelector('.terminal-container');
        if (!container) return;

        container.style.animation = 'errorShake 0.5s ease-in-out';
        setTimeout(() => {
            container.style.animation = '';
        }, 500);
    }

    // Animation de niveau qui monte
    animateLevelUp(newLevel) {
        const levelElement = document.getElementById('playerLevel');
        if (!levelElement) return;

        const oldLevel = parseInt(levelElement.textContent);
        if (newLevel > oldLevel) {
            levelElement.style.animation = 'levelUp 1s ease-in-out';
            levelElement.textContent = newLevel;

            setTimeout(() => {
                levelElement.style.animation = '';
            }, 1000);

            this.showSuccessEffect();
        }
    }

    // Effet de mission complétée
    showMissionComplete(missionName) {
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(45deg, #00ff00, #00ffff);
            color: #000;
            padding: 30px;
            border-radius: 20px;
            font-size: 1.5em;
            font-weight: bold;
            z-index: 10000;
            animation: missionComplete 2s ease-in-out;
            text-align: center;
        `;

        message.innerHTML = `
            🎉 MISSION COMPLÉTÉE ! 🎉<br>
            <span style="font-size: 0.8em;">${missionName}</span>
        `;

        document.body.appendChild(message);

        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 2000);

        this.showSuccessEffect();
    }

    // ===== EFFETS D'ÉCHEC ULTRA-COOL =====

    // Faire trembler l'écran quand on échoue
    triggerFailShake() {
        const body = document.body;
        body.style.animation = 'failShake 0.5s ease-in-out';

        // Ajouter un effet de flash rouge
        body.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';

        setTimeout(() => {
            body.style.animation = '';
            body.style.backgroundColor = '';
        }, 500);
    }

    // Effet d'explosion quand on réussit
    triggerSuccessExplosion() {
        const container = document.querySelector('.terminal-container');
        if (!container) return;

        // Créer des particules d'explosion
        for (let i = 0; i < 30; i++) {
            setTimeout(() => {
                this.createExplosionParticle(container);
            }, i * 50);
        }

        // Flash vert de succès
        document.body.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
        setTimeout(() => {
            document.body.style.backgroundColor = '';
        }, 1000);
    }

    // Créer une particule d'explosion
    createExplosionParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'explosion-particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: #ffaa00;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        `;

        container.appendChild(particle);

        // Animation d'explosion
        const angle = Math.random() * Math.PI * 2;
        const distance = 50 + Math.random() * 100;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;

        particle.style.transition = 'all 0.8s ease-out';
        particle.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
        particle.style.opacity = '0';

        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 800);
    }

    // Effet de glitch sur l'écran
    triggerGlitchEffect() {
        const terminal = document.querySelector('.terminal-container');
        if (!terminal) return;

        terminal.classList.add('glitch-effect');

        // Effet de distorsion
        terminal.style.filter = 'hue-rotate(90deg) contrast(1.5)';

        setTimeout(() => {
            terminal.classList.remove('glitch-effect');
            terminal.style.filter = '';
        }, 1000);
    }

    // Effet de boss final
    triggerBossEffect() {
        const body = document.body;

        // Tremblement intense
        body.style.animation = 'bossShake 0.1s ease-in-out infinite';

        // Flash rouge
        body.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';

        // Son d'alerte (si audio disponible)
        if (window.audioManager) {
            window.audioManager.playSound('error');
        }

        setTimeout(() => {
            body.style.animation = '';
            body.style.backgroundColor = '';
        }, 3000);
    }
}

// Styles CSS pour les animations
const style = document.createElement('style');
style.textContent = `
    @keyframes particleFall {
        0% { transform: translateY(-10px); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
    
    @keyframes successFlash {
        0% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
    
    @keyframes levelUp {
        0% { transform: scale(1); }
        50% { transform: scale(1.5); }
        100% { transform: scale(1); }
    }
    
    @keyframes missionComplete {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
    }
    
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
`;

document.head.appendChild(style);

// Instance globale
window.HackingEffects = new HackingEffects();

// Fonctions globales pour compatibilité
window.showHackingProgress = (duration, command) => {
    window.HackingEffects.showHackingProgress(duration, command);
};

window.addGlitchEffect = (element) => {
    window.HackingEffects.addGlitchEffect(element);
};

window.addHackEffect = (element) => {
    window.HackingEffects.addHackEffect(element);
};

window.showSuccessEffect = () => {
    window.HackingEffects.showSuccessEffect();
};

window.showErrorEffect = () => {
    window.HackingEffects.showErrorEffect();
};

// Effets de hacking chargés avec succès 