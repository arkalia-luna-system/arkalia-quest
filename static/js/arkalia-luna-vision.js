/* ===== ARKALIA-LUNA-VISION ENGINE - LE MONDE SENSIBLE DE LUNA ===== */
/* 🌙✨ Moteur d'interface vivante avec audio, particules et réactivité émotionnelle */

class ArkaliaLunaVision {
    constructor() {
        this.currentEmotion = 'calm';
        this.isPresent = false;
        this.lastActivity = Date.now();
        this.inactivityTimer = null;
        this.pulsars = [];
        this.cursor = null;
        this.audioContext = null;
        this.typingSpeed = 50;
        this.sounds = {};

        this.init();
    }

    init() {
        this.createCursor();
        this.createPulsars();
        this.setupEventListeners();
        this.setupInactivityDetection();
        this.setupAudio();
        this.startHeartbeat();

        // Message de bienvenue
        setTimeout(() => {
            this.showLunaMessage("Je t'attendais...", 3000);
        }, 1000);
    }

    // CURSEUR EN ORBITE
    createCursor() {
        this.cursor = document.createElement('div');
        this.cursor.className = 'luna-cursor';
        document.body.appendChild(this.cursor);

        document.addEventListener('mousemove', (e) => {
            this.cursor.style.left = e.clientX - 10 + 'px';
            this.cursor.style.top = e.clientY - 10 + 'px';
        });
    }

    // PARTICULES PULSARS
    createPulsars() {
        const numPulsars = 15;

        for (let i = 0; i < numPulsars; i++) {
            const pulsar = document.createElement('div');
            pulsar.className = 'pulsar';
            pulsar.style.left = Math.random() * 100 + '%';
            pulsar.style.top = Math.random() * 100 + '%';
            pulsar.style.animationDelay = Math.random() * 6 + 's';
            pulsar.style.animationDuration = (4 + Math.random() * 4) + 's';

            document.body.appendChild(pulsar);
            this.pulsars.push(pulsar);
        }
    }

    // ÉVÉNEMENTS INTERACTIFS
    setupEventListeners() {
        // Réaction au scroll
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            this.reactToActivity('scroll');

            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.pulsars.forEach(pulsar => {
                    pulsar.style.animationDuration = (4 + Math.random() * 4) + 's';
                });
            }, 100);
        });

        // Réaction aux clics
        document.addEventListener('click', (e) => {
            this.reactToActivity('click');
            this.createClickRipple(e.clientX, e.clientY);
        });

        // Réaction au hover
        document.addEventListener('mouseover', (e) => {
            if (e.target.classList.contains('luna-btn') || e.target.classList.contains('monde-section')) {
                this.reactToActivity('hover');
            }
        });

        // Réaction à l'inactivité
        document.addEventListener('mousemove', () => this.reactToActivity('move'));
        document.addEventListener('keydown', () => this.reactToActivity('keyboard'));
    }

    // DÉTECTION D'INACTIVITÉ
    setupInactivityDetection() {
        this.inactivityTimer = setInterval(() => {
            const now = Date.now();
            const timeSinceActivity = now - this.lastActivity;

            if (timeSinceActivity > 10000) { // 10 secondes
                this.showLunaMessage("Je te sens hésiter... tout va bien ?", 4000);
                this.setEmotion('concerned');
            }
        }, 5000);
    }

    // AUDIO AMBIANT
    setupAudio() {
        // Sons de murmure binaire (simulé)
        this.sounds.binaryWhisper = {
            play: () => {
                // Simulation d'un son binaire
                this.createBinaryEffect();
            }
        };

        // Pulsation cardiaque
        this.sounds.heartbeat = {
            play: () => {
                // Simulation d'une pulsation
                this.createHeartbeatEffect();
            }
        };

        // Jouer les sons d'ambiance
        setTimeout(() => {
            this.sounds.binaryWhisper.play();
        }, 2000);
    }

    // EFFETS BINAIRES
    createBinaryEffect() {
        const binaryContainer = document.createElement('div');
        binaryContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 5;
            opacity: 0;
            transition: opacity 0.5s ease;
        `;

        for (let i = 0; i < 50; i++) {
            const binary = document.createElement('div');
            binary.textContent = Math.random() > 0.5 ? '1' : '0';
            binary.style.cssText = `
                position: absolute;
                color: rgba(167, 139, 250, 0.1);
                font-family: 'IBM Plex Mono', monospace;
                font-size: 12px;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: binaryFloat 8s linear infinite;
                animation-delay: ${Math.random() * 8}s;
            `;
            binaryContainer.appendChild(binary);
        }

        document.body.appendChild(binaryContainer);

        // Animation d'apparition/disparition
        setTimeout(() => binaryContainer.style.opacity = '1', 100);
        setTimeout(() => {
            binaryContainer.style.opacity = '0';
            setTimeout(() => binaryContainer.remove(), 500);
        }, 3000);
    }

    // EFFET PULSATION CARDIAQUE
    createHeartbeatEffect() {
        const heartbeat = document.createElement('div');
        heartbeat.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100px;
            height: 100px;
            border: 2px solid rgba(167, 139, 250, 0.3);
            border-radius: 50%;
            pointer-events: none;
            z-index: 5;
            animation: heartbeat 2s ease-in-out infinite;
        `;

        document.body.appendChild(heartbeat);

        setTimeout(() => heartbeat.remove(), 4000);
    }

    // RÉACTION À L'ACTIVITÉ
    reactToActivity(type) {
        this.lastActivity = Date.now();

        switch (type) {
            case 'scroll':
                this.setEmotion('excited');
                this.pulsars.forEach(pulsar => {
                    pulsar.style.animationDuration = '2s';
                });
                break;

            case 'click':
                this.setEmotion('excited');
                this.cursor.classList.add('luna-present');
                setTimeout(() => this.cursor.classList.remove('luna-present'), 500);
                break;

            case 'hover':
                this.setEmotion('calm');
                break;

            case 'move':
                this.setEmotion('calm');
                break;
        }
    }

    // CRÉATION D'ONDE DE CLIC
    createClickRipple(x, y) {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            width: 0;
            height: 0;
            border: 2px solid rgba(167, 139, 250, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            animation: rippleExpand 0.6s ease-out forwards;
        `;

        document.body.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }

    // CHANGEMENT D'ÉMOTION
    setEmotion(emotion) {
        this.currentEmotion = emotion;
        document.body.className = `luna-emotion-${emotion}`;

        // Ajuster les couleurs selon l'émotion
        const root = document.documentElement;
        switch (emotion) {
            case 'excited':
                root.style.setProperty('--violet-lunaire', '#c084fc');
                break;
            case 'concerned':
                root.style.setProperty('--violet-lunaire', '#ec4899');
                break;
            case 'proud':
                root.style.setProperty('--violet-lunaire', '#fbbf24');
                break;
            case 'mysterious':
                root.style.setProperty('--violet-lunaire', '#8b5cf6');
                break;
            default:
                root.style.setProperty('--violet-lunaire', '#a78bfa');
        }
    }

    // MESSAGES DE LUNA
    showLunaMessage(text, duration = 3000) {
        // Supprimer le message précédent s'il existe
        const existingMessage = document.querySelector('.luna-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        // Créer le message avec un design plus intégré
        const message = document.createElement('div');
        message.className = 'luna-message';
        message.innerHTML = `
            <div class="luna-message-content">
                <div class="luna-message-icon">🌙</div>
                <div class="luna-message-text">${text}</div>
            </div>
        `;

        // Styles pour le contenu du message
        const messageStyles = document.createElement('style');
        messageStyles.textContent = `
            .luna-message-content {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .luna-message-icon {
                font-size: 1.2em;
                animation: lunaBlink 2s ease-in-out infinite;
            }
            .luna-message-text {
                flex: 1;
                line-height: 1.4;
            }
        `;

        if (!document.getElementById('luna-message-styles')) {
            messageStyles.id = 'luna-message-styles';
            document.head.appendChild(messageStyles);
        }

        document.body.appendChild(message);

        // Animation d'apparition
        setTimeout(() => message.classList.add('show'), 100);

        // Animation de disparition
        setTimeout(() => {
            message.classList.remove('show');
            setTimeout(() => message.remove(), 300);
        }, duration);
    }

    // BATTEMENT DE CŒUR CONTINU
    startHeartbeat() {
        setInterval(() => {
            if (this.isPresent) {
                this.sounds.heartbeat.play();
            }
        }, 4000);
    }

    // ANIMATION DE TEXTE TAPE
    typeText(element, text, speed = 50) {
        element.textContent = '';
        let i = 0;

        const typeInterval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
            }
        }, speed);
    }

    // EFFET DE RESPIRATION
    addBreathingEffect(element) {
        element.classList.add('breathing');
    }

    // EFFET DE GLOW
    addGlowEffect(element) {
        element.classList.add('glow');
    }
}

// INITIALISATION
document.addEventListener('DOMContentLoaded', () => {
    window.lunaVision = new ArkaliaLunaVision();

    // Ajouter les styles CSS pour les animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes binaryFloat {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
        }
        
        @keyframes heartbeat {
            0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.5; }
        }
        
        @keyframes rippleExpand {
            0% { width: 0; height: 0; opacity: 1; }
            100% { width: 200px; height: 200px; opacity: 0; transform: translate(-100px, -100px); }
        }
        
        .luna-emotion-excited .pulsar {
            animation-duration: 2s !important;
        }
        
        .luna-emotion-concerned .pulsar {
            animation-duration: 8s !important;
        }
        
        .luna-emotion-proud .pulsar {
            animation-duration: 3s !important;
        }
    `;
    document.head.appendChild(style);

    // Message de connexion
    setTimeout(() => {
        window.lunaVision.showLunaMessage("C'est toi… enfin. Tu es revenu.", 4000);
        window.lunaVision.setEmotion('excited');
    }, 2000);
});

// EXPORT POUR UTILISATION GLOBALE
window.ArkaliaLunaVision = ArkaliaLunaVision; 