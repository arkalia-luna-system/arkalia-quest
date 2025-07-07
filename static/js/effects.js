/**
 * Système d'effets Arkalia Quest - VERSION ULTRA-ATTRACTIVE
 * Sons, animations et feedback immersif pour ados de 13 ans
 */

// ===== SYSTÈME SONORE ULTRA-FONCTIONNEL =====
class AudioManager {
    constructor() {
        this.sounds = {};
        this.ambiances = {};
        this.volume = 0.4;
        this.muted = false;
        this.audioContext = null;
        this.init();
    }

    init() {
        // Créer le contexte audio
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.log('🔇 Audio non supporté, mode silencieux');
            this.muted = true;
        }

        this.setupControls();
    }

    // ===== SONS ULTRA-COOL POUR ADOS =====
    playTypingSound() {
        if (this.muted || !this.audioContext) return;
        
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
            // Mode silencieux
        }
    }

    playHackSound() {
        if (this.muted || !this.audioContext) return;
        
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
            // Mode silencieux
        }
    }

    playSuccessSound() {
        if (this.muted || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(400, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(800, this.audioContext.currentTime + 0.2);
            oscillator.frequency.exponentialRampToValueAtTime(1200, this.audioContext.currentTime + 0.4);
            
            gainNode.gain.setValueAtTime(0.15, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.4);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.4);
        } catch (e) {
            // Mode silencieux
        }
    }

    playErrorSound() {
        if (this.muted || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(400, this.audioContext.currentTime + 0.3);
            
            gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);
        } catch (e) {
            // Mode silencieux
        }
    }

    playLevelUpSound() {
        if (this.muted || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(400, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(600, this.audioContext.currentTime + 0.1);
            oscillator.frequency.exponentialRampToValueAtTime(800, this.audioContext.currentTime + 0.2);
            oscillator.frequency.exponentialRampToValueAtTime(1000, this.audioContext.currentTime + 0.3);
            
            gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);
        } catch (e) {
            // Mode silencieux
        }
    }

    playPortalSound() {
        if (this.muted || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(300, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(600, this.audioContext.currentTime + 0.5);
            oscillator.frequency.exponentialRampToValueAtTime(300, this.audioContext.currentTime + 1.0);
            
            gainNode.gain.setValueAtTime(0.15, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 1.0);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 1.0);
        } catch (e) {
            // Mode silencieux
        }
    }

    playLunaSound() {
        if (this.muted || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(500, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(700, this.audioContext.currentTime + 0.2);
            oscillator.frequency.exponentialRampToValueAtTime(500, this.audioContext.currentTime + 0.4);
            
            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.4);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.4);
        } catch (e) {
            // Mode silencieux
        }
    }

    // ===== AMBIANCE MATRIX ULTRA-COOL =====
    playMatrixAmbiance() {
        if (this.muted || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(100, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(150, this.audioContext.currentTime + 2.0);
            oscillator.frequency.exponentialRampToValueAtTime(100, this.audioContext.currentTime + 4.0);
            
            gainNode.gain.setValueAtTime(0.05, this.audioContext.currentTime);
            
            oscillator.start(this.audioContext.currentTime);
            
            // Arrêter après 4 secondes
            setTimeout(() => {
                oscillator.stop();
            }, 4000);
        } catch (e) {
            // Mode silencieux
        }
    }

    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
    }

    toggleMute() {
        this.muted = !this.muted;
        this.updateMuteButton();
    }

    setupControls() {
        // Créer les contrôles audio ultra-cool
        const audioControls = document.createElement('div');
        audioControls.className = 'audio-controls';
        audioControls.innerHTML = `
            <div class="audio-panel">
                <button id="muteBtn" class="audio-btn" title="Muet/Activer le son">
                    <span class="icon">🔊</span>
                </button>
                <div class="volume-slider">
                    <input type="range" id="volumeSlider" min="0" max="100" value="40" title="Volume">
                </div>
                <div class="audio-presets">
                    <button class="preset-btn active" data-ambiance="matrix">🌐 Matrix</button>
                    <button class="preset-btn" data-ambiance="cyber">⚡ Cyber</button>
                    <button class="preset-btn" data-ambiance="portal">🌀 Portal</button>
                </div>
            </div>
        `;

        document.body.appendChild(audioControls);

        // Événements
        document.getElementById('muteBtn').addEventListener('click', () => this.toggleMute());
        document.getElementById('volumeSlider').addEventListener('input', (e) => {
            this.setVolume(e.target.value / 100);
        });

        // Presets d'ambiance
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const ambiance = btn.dataset.ambiance;
                this.updateActivePreset(btn);
                if (ambiance === 'matrix') {
                    this.playMatrixAmbiance();
                }
            });
        });
    }

    updateMuteButton() {
        const btn = document.getElementById('muteBtn');
        const icon = btn.querySelector('.icon');
        icon.textContent = this.muted ? '🔇' : '🔊';
        btn.classList.toggle('muted', this.muted);
    }

    updateActivePreset(activeBtn) {
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        activeBtn.classList.add('active');
    }
}

// ===== EFFETS VISUELS ULTRA-OPTIMISÉS =====
class VisualEffects {
    constructor() {
        this.audioManager = new AudioManager();
        this.isLowPerformance = this.detectLowPerformance();
        this.init();
    }

    detectLowPerformance() {
        // Détecter les appareils faibles
        const userAgent = navigator.userAgent.toLowerCase();
        const isMobile = /mobile|android|iphone|ipad/.test(userAgent);
        const memory = navigator.deviceMemory || 4;
        const cores = navigator.hardwareConcurrency || 4;
        
        return isMobile || memory < 4 || cores < 4;
    }

    init() {
        if (!this.isLowPerformance) {
            this.setupMatrixRain();
            this.setupParticleSystem();
        }
        this.setupGlitchEffects();
        this.setupTerminalEffects();
    }

    setupMatrixRain() {
        const canvas = document.createElement('canvas');
        canvas.id = 'matrixRain';
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.05;
        `;
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
        const matrixArray = matrix.split("");

        const fontSize = 8;
        const columns = canvas.width / fontSize;
        const drops = [];

        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }

        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }

        setInterval(draw, 50);
    }

    setupParticleSystem() {
        const canvas = document.createElement('canvas');
        canvas.id = 'particleCanvas';
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.3;
        `;
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const particles = [];
        const particleCount = 20;

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.size = Math.random() * 2 + 1;
                this.color = `hsl(${Math.random() * 60 + 120}, 100%, 50%)`;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }

            draw() {
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });

            requestAnimationFrame(animate);
        }

        animate();
    }

    setupGlitchEffects() {
        // Effet de glitch sur les messages
        const style = document.createElement('style');
        style.textContent = `
            @keyframes glitch {
                0% { transform: translate(0); }
                20% { transform: translate(-2px, 2px); }
                40% { transform: translate(-2px, -2px); }
                60% { transform: translate(2px, 2px); }
                80% { transform: translate(2px, -2px); }
                100% { transform: translate(0); }
            }

            @keyframes errorShake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }

            @keyframes successGlow {
                0%, 100% { box-shadow: 0 0 5px #00ff00; }
                50% { box-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; }
            }

            .glitch-effect {
                animation: glitch 0.3s ease-in-out;
            }

            .error-effect {
                animation: errorShake 0.5s ease-in-out;
            }

            .success-effect {
                animation: successGlow 1s ease-in-out;
            }
        `;
        document.head.appendChild(style);
    }

    setupTerminalEffects() {
        // Effet de frappe sur le terminal
        const terminal = document.querySelector('.terminal-output');
        if (terminal) {
            terminal.style.fontFamily = "'Share Tech Mono', monospace";
            terminal.style.letterSpacing = '1px';
        }
    }

    // ===== EFFETS ULTRA-COOL POUR ADOS =====
    playSuccess() {
        this.audioManager.playSuccessSound();
        this.createSuccessParticles();
    }

    playError() {
        this.audioManager.playErrorSound();
        this.createErrorEffect();
    }

    playGlitch() {
        this.audioManager.playTypingSound();
        this.createGlitchEffect();
    }

    playLevelUp() {
        this.audioManager.playLevelUpSound();
        this.createLevelUpEffect();
    }

    playHack() {
        this.audioManager.playHackSound();
        this.createHackEffect();
    }

    playPortal() {
        this.audioManager.playPortalSound();
        this.createPortalEffect();
    }

    playLuna() {
        this.audioManager.playLunaSound();
        this.createLunaEffect();
    }

    // ===== EFFETS VISUELS ULTRA-ATTRACTIFS =====
    createSuccessParticles() {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 1000;
        `;

        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: #00ff00;
                border-radius: 50%;
                animation: particleSuccess 1s ease-out forwards;
            `;

            const angle = (i / 20) * Math.PI * 2;
            const distance = 50 + Math.random() * 50;
            const x = Math.cos(angle) * distance;
            const y = Math.sin(angle) * distance;

            particle.style.setProperty('--x', x + 'px');
            particle.style.setProperty('--y', y + 'px');

            container.appendChild(particle);
        }

        document.body.appendChild(container);

        setTimeout(() => {
            document.body.removeChild(container);
        }, 1000);
    }

    createErrorEffect() {
        const messagesContainer = document.getElementById('messagesContainer');
        if (messagesContainer) {
            messagesContainer.classList.add('error-effect');
            setTimeout(() => {
                messagesContainer.classList.remove('error-effect');
            }, 500);
        }
    }

    createGlitchEffect() {
        const messagesContainer = document.getElementById('messagesContainer');
        if (messagesContainer) {
            messagesContainer.classList.add('glitch-effect');
            setTimeout(() => {
                messagesContainer.classList.remove('glitch-effect');
            }, 300);
        }
    }

    createLevelUpEffect() {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(45deg, #00ff00, #00ffff);
            color: #000;
            padding: 20px 40px;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            z-index: 1000;
            animation: levelUpEffect 2s ease-out forwards;
        `;
        container.textContent = '🎉 NIVEAU SUPÉRIEUR ! 🎉';

        document.body.appendChild(container);

        setTimeout(() => {
            document.body.removeChild(container);
        }, 2000);
    }

    createHackEffect() {
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 255, 0, 0.1);
            z-index: 999;
            animation: hackEffect 0.5s ease-out forwards;
        `;

        document.body.appendChild(overlay);

        setTimeout(() => {
            document.body.removeChild(overlay);
        }, 500);
    }

    createPortalEffect() {
        const portal = document.createElement('div');
        portal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 200px;
            height: 200px;
            border: 3px solid #00ffff;
            border-radius: 50%;
            z-index: 1000;
            animation: portalEffect 2s ease-out forwards;
        `;

        document.body.appendChild(portal);

        setTimeout(() => {
            document.body.removeChild(portal);
        }, 2000);
    }

    createLunaEffect() {
        const luna = document.createElement('div');
        luna.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #00ffff, #ff00ff);
            color: #000;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            z-index: 1000;
            animation: lunaEffect 3s ease-out forwards;
        `;
        luna.textContent = '🌙 LUNA';

        document.body.appendChild(luna);

        setTimeout(() => {
            document.body.removeChild(luna);
        }, 3000);
    }
}

// ===== INITIALISATION ULTRA-COOL =====
let visualEffects;

document.addEventListener('DOMContentLoaded', () => {
    visualEffects = new VisualEffects();
    
    // Démarrer l'ambiance Matrix
    setTimeout(() => {
        visualEffects.audioManager.playMatrixAmbiance();
    }, 1000);

    // Ajouter les styles CSS pour les animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleSuccess {
            0% {
                transform: translate(0, 0);
                opacity: 1;
            }
            100% {
                transform: translate(var(--x), var(--y));
                opacity: 0;
            }
        }

        @keyframes levelUpEffect {
            0% {
                transform: translate(-50%, -50%) scale(0);
                opacity: 0;
            }
            50% {
                transform: translate(-50%, -50%) scale(1.2);
                opacity: 1;
            }
            100% {
                transform: translate(-50%, -50%) scale(1);
                opacity: 0;
            }
        }

        @keyframes hackEffect {
            0% {
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            100% {
                opacity: 0;
            }
        }

        @keyframes portalEffect {
            0% {
                transform: translate(-50%, -50%) scale(0);
                opacity: 1;
            }
            50% {
                transform: translate(-50%, -50%) scale(1.5);
                opacity: 0.8;
            }
            100% {
                transform: translate(-50%, -50%) scale(2);
                opacity: 0;
            }
        }

        @keyframes lunaEffect {
            0% {
                transform: translateX(100%);
                opacity: 0;
            }
            20% {
                transform: translateX(0);
                opacity: 1;
            }
            80% {
                transform: translateX(0);
                opacity: 1;
            }
            100% {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        .audio-controls {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
        }

        .audio-panel {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .audio-btn {
            background: #00ff00;
            color: #000;
            border: none;
            border-radius: 5px;
            padding: 8px 12px;
            cursor: pointer;
            font-weight: bold;
        }

        .audio-btn.muted {
            background: #ff4444;
        }

        .volume-slider input {
            width: 100%;
            height: 5px;
            background: #333;
            outline: none;
            border-radius: 5px;
        }

        .audio-presets {
            display: flex;
            gap: 5px;
        }

        .preset-btn {
            background: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 3px;
            padding: 5px 8px;
            cursor: pointer;
            font-size: 12px;
        }

        .preset-btn.active {
            background: #00ff00;
            color: #000;
        }
    `;
    document.head.appendChild(style);
});

// ===== EXPORT POUR UTILISATION GLOBALE =====
window.ArkaliaEffects = {
    getInstance: () => visualEffects
}; 