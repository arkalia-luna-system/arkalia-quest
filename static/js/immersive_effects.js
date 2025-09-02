/**
 * 🌟 Immersive Effects Engine v4.0 - Effets visuels ultra-avancés
 * Système d'effets immersifs qui réagit aux émotions de LUNA
 */

class ImmersiveEffectsEngine {
    constructor() {
        this.isActive = false;
        this.currentEmotion = 'calm';
        this.emotionIntensity = 0.5;
        this.particleSystems = [];
        this.audioContext = null;
        this.oscillators = {};

        // Initialiser l'engine
        this.init();
    }

    init() {
        // Initialisation du moteur d'effets immersifs

        // Créer le canvas pour les particules
        this.createParticleCanvas();

        // Initialiser l'audio context
        this.initAudioContext();

        // Démarrer le loop d'animation
        this.startAnimationLoop();

        this.isActive = true;
        // Moteur d'effets immersifs initialisé
    }

    createParticleCanvas() {
        // Créer le canvas des particules
        this.particleCanvas = document.createElement('canvas');
        this.particleCanvas.id = 'immersive-particles';
        this.particleCanvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
            opacity: 0.7;
        `;
        document.body.appendChild(this.particleCanvas);

        this.particleCtx = this.particleCanvas.getContext('2d');
        this.resizeCanvas();

        // Gérer le redimensionnement
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    resizeCanvas() {
        this.particleCanvas.width = window.innerWidth;
        this.particleCanvas.height = window.innerHeight;
    }

    initAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            // Audio context initialisé
        } catch (error) {
            console.warn("⚠️ Audio context non supporté:", error);
        }
    }

    // 🌙 SYSTÈME D'ÉMOTIONS LUNA

    updateLunaEmotion(emotionData) {
        const { emotion, intensity, color, effect, sound } = emotionData;

        this.currentEmotion = emotion;
        this.emotionIntensity = intensity;

        // LUNA émotion mise à jour

        // Appliquer les effets visuels
        this.applyEmotionEffects(emotion, intensity, color, effect);

        // Jouer le son d'émotion
        this.playEmotionSound(sound, intensity);

        // Mettre à jour l'interface
        this.updateInterfaceColors(color, intensity);
    }

    applyEmotionEffects(emotion, intensity, color, effect) {
        // Arrêter les effets précédents
        this.stopAllEffects();

        // Appliquer le nouvel effet selon l'émotion
        switch (emotion) {
            case 'excited':
                this.startExcitedEffect(intensity, color);
                break;
            case 'worried':
                this.startWorriedEffect(intensity, color);
                break;
            case 'proud':
                this.startProudEffect(intensity, color);
                break;
            case 'mysterious':
                this.startMysteriousEffect(intensity, color);
                break;
            case 'determined':
                this.startDeterminedEffect(intensity, color);
                break;
            case 'playful':
                this.startPlayfulEffect(intensity, color);
                break;
            case 'focused':
                this.startFocusedEffect(intensity, color);
                break;
            case 'surprised':
                this.startSurprisedEffect(intensity, color);
                break;
            case 'calm':
                this.startCalmEffect(intensity, color);
                break;
            case 'energetic':
                this.startEnergeticEffect(intensity, color);
                break;
        }
    }

    // 🎨 EFFETS PAR ÉMOTION

    startExcitedEffect(intensity, color) {
        // Particules vertes qui explosent
        this.createParticleExplosion(color, 50, intensity);

        // Flash vert sur l'écran
        this.createFlash(color, intensity * 0.5);

        // Animation de pulse sur les boutons
        this.pulseButtons(color, intensity);

        // Son d'excitation
        this.playSound('success', intensity);
    }

    startWorriedEffect(intensity, color) {
        // Tremblement de l'écran
        this.shakeScreen(intensity);

        // Particules orange inquiètes
        this.createWorriedParticles(color, intensity);

        // Son d'inquiétude
        this.playSound('warning', intensity);
    }

    startProudEffect(intensity, color) {
        // Étincelles magiques
        this.createSparkles(color, 30, intensity);

        // Animation de victoire
        this.victoryAnimation(intensity);

        // Son de fierté
        this.playSound('levelup', intensity);
    }

    startMysteriousEffect(intensity, color) {
        // Brouillard mystérieux
        this.createMysteryFog(color, intensity);

        // Effet de fade
        this.fadeEffect(intensity);

        // Son mystérieux
        this.playSound('mystery', intensity);
    }

    startDeterminedEffect(intensity, color) {
        // Rayons de détermination
        this.createDeterminationRays(color, intensity);

        // Glow rouge
        this.glowEffect(color, intensity);

        // Son de détermination
        this.playSound('hack', intensity);
    }

    startPlayfulEffect(intensity, color) {
        // Particules qui rebondissent
        this.createBouncingParticles(color, intensity);

        // Animation de bounce
        this.bounceEffect(intensity);

        // Son joueur
        this.playSound('playful', intensity);
    }

    startFocusedEffect(intensity, color) {
        // Zoom sur l'interface
        this.zoomEffect(intensity);

        // Particules concentrées
        this.createFocusedParticles(color, intensity);

        // Son de concentration
        this.playSound('focus', intensity);
    }

    startSurprisedEffect(intensity, color) {
        // Flash rose surprise
        this.createFlash('#ff00aa', intensity);

        // Particules qui explosent
        this.createParticleExplosion(color, 40, intensity);

        // Son de surprise
        this.playSound('surprise', intensity);
    }

    startCalmEffect(intensity, color) {
        // Particules flottantes calmes
        this.createCalmParticles(color, intensity);

        // Effet de flottement
        this.floatEffect(intensity);

        // Son calme
        this.playSound('calm', intensity);
    }

    startEnergeticEffect(intensity, color) {
        // Vibration de l'écran
        this.vibrateScreen(intensity);

        // Particules énergiques
        this.createEnergeticParticles(color, intensity);

        // Son énergique
        this.playSound('energetic', intensity);
    }

    // 🎭 EFFETS VISUELS SPÉCIFIQUES

    createParticleExplosion(color, count, intensity) {
        const particles = [];
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;

        for (let i = 0; i < count; i++) {
            const angle = (Math.PI * 2 * i) / count;
            const speed = 2 + Math.random() * 3;
            const size = 2 + Math.random() * 4;

            particles.push({
                x: centerX,
                y: centerY,
                vx: Math.cos(angle) * speed * intensity,
                vy: Math.sin(angle) * speed * intensity,
                size: size,
                color: color,
                life: 1.0,
                decay: 0.02 + Math.random() * 0.03
            });
        }

        this.particleSystems.push({
            type: 'explosion',
            particles: particles,
            duration: 60
        });
    }

    createSparkles(color, count, intensity) {
        const sparkles = [];

        for (let i = 0; i < count; i++) {
            sparkles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                size: 1 + Math.random() * 3,
                color: color,
                life: 1.0,
                decay: 0.01,
                twinkle: Math.random() * Math.PI * 2
            });
        }

        this.particleSystems.push({
            type: 'sparkles',
            particles: sparkles,
            duration: 120
        });
    }

    createWorriedParticles(color, intensity) {
        const particles = [];

        for (let i = 0; i < 20; i++) {
            particles.push({
                x: Math.random() * window.innerWidth,
                y: window.innerHeight + 10,
                vx: (Math.random() - 0.5) * 2,
                vy: -1 - Math.random() * 2,
                size: 2 + Math.random() * 3,
                color: color,
                life: 1.0,
                decay: 0.005
            });
        }

        this.particleSystems.push({
            type: 'worried',
            particles: particles,
            duration: 90
        });
    }

    createMysteryFog(color, intensity) {
        const fogParticles = [];

        for (let i = 0; i < 15; i++) {
            fogParticles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                size: 50 + Math.random() * 100,
                color: color,
                opacity: 0.1 + Math.random() * 0.2,
                life: 1.0,
                decay: 0.001
            });
        }

        this.particleSystems.push({
            type: 'fog',
            particles: fogParticles,
            duration: 180
        });
    }

    createDeterminationRays(color, intensity) {
        const rays = [];
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;

        for (let i = 0; i < 8; i++) {
            const angle = (Math.PI * 2 * i) / 8;
            rays.push({
                x: centerX,
                y: centerY,
                angle: angle,
                length: 200 + Math.random() * 100,
                color: color,
                opacity: 0.3 + Math.random() * 0.4,
                life: 1.0,
                decay: 0.01
            });
        }

        this.particleSystems.push({
            type: 'rays',
            particles: rays,
            duration: 60
        });
    }

    createBouncingParticles(color, intensity) {
        const particles = [];

        for (let i = 0; i < 25; i++) {
            particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 4,
                vy: (Math.random() - 0.5) * 4,
                size: 3 + Math.random() * 4,
                color: color,
                life: 1.0,
                decay: 0.005,
                bounce: 0.8
            });
        }

        this.particleSystems.push({
            type: 'bouncing',
            particles: particles,
            duration: 150
        });
    }

    createFocusedParticles(color, intensity) {
        const particles = [];
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;

        for (let i = 0; i < 30; i++) {
            const angle = Math.random() * Math.PI * 2;
            const distance = 50 + Math.random() * 100;

            particles.push({
                x: centerX + Math.cos(angle) * distance,
                y: centerY + Math.sin(angle) * distance,
                targetX: centerX,
                targetY: centerY,
                size: 2 + Math.random() * 3,
                color: color,
                life: 1.0,
                decay: 0.01
            });
        }

        this.particleSystems.push({
            type: 'focused',
            particles: particles,
            duration: 90
        });
    }

    createCalmParticles(color, intensity) {
        const particles = [];

        for (let i = 0; i < 20; i++) {
            particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 0.5,
                vy: -0.5 - Math.random() * 0.5,
                size: 2 + Math.random() * 3,
                color: color,
                life: 1.0,
                decay: 0.002
            });
        }

        this.particleSystems.push({
            type: 'calm',
            particles: particles,
            duration: 200
        });
    }

    createEnergeticParticles(color, intensity) {
        const particles = [];

        for (let i = 0; i < 40; i++) {
            particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 6,
                vy: (Math.random() - 0.5) * 6,
                size: 2 + Math.random() * 4,
                color: color,
                life: 1.0,
                decay: 0.01,
                energy: Math.random()
            });
        }

        this.particleSystems.push({
            type: 'energetic',
            particles: particles,
            duration: 120
        });
    }

    // 🎬 EFFETS D'ÉCRAN

    createFlash(color, intensity) {
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: ${color};
            opacity: ${intensity * 0.3};
            pointer-events: none;
            z-index: 9999;
            transition: opacity 0.3s ease-out;
        `;

        document.body.appendChild(flash);

        setTimeout(() => {
            flash.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(flash);
            }, 300);
        }, 100);
    }

    shakeScreen(intensity) {
        const originalTransform = document.body.style.transform;
        const shakeAmount = intensity * 10;

        let shakeCount = 0;
        const maxShakes = 10;

        const shake = () => {
            if (shakeCount >= maxShakes) {
                document.body.style.transform = originalTransform;
                return;
            }

            const x = (Math.random() - 0.5) * shakeAmount;
            const y = (Math.random() - 0.5) * shakeAmount;

            document.body.style.transform = `translate(${x}px, ${y}px)`;
            shakeCount++;

            setTimeout(shake, 50);
        };

        shake();
    }

    vibrateScreen(intensity) {
        if ('vibrate' in navigator) {
            navigator.vibrate(intensity * 200);
        }

        // Vibration visuelle
        const originalTransform = document.body.style.transform;
        let vibrateCount = 0;
        const maxVibrations = 20;

        const vibrate = () => {
            if (vibrateCount >= maxVibrations) {
                document.body.style.transform = originalTransform;
                return;
            }

            const x = (Math.random() - 0.5) * intensity * 5;
            const y = (Math.random() - 0.5) * intensity * 5;

            document.body.style.transform = `translate(${x}px, ${y}px)`;
            vibrateCount++;

            setTimeout(vibrate, 30);
        };

        vibrate();
    }

    zoomEffect(intensity) {
        const originalTransform = document.body.style.transform;
        const scale = 1 + intensity * 0.1;

        document.body.style.transform = `scale(${scale})`;

        setTimeout(() => {
            document.body.style.transform = originalTransform;
        }, 500);
    }

    fadeEffect(intensity) {
        const fade = document.createElement('div');
        fade.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, ${intensity * 0.3});
            pointer-events: none;
            z-index: 9998;
            transition: opacity 1s ease-in-out;
        `;

        document.body.appendChild(fade);

        setTimeout(() => {
            fade.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(fade);
            }, 1000);
        }, 500);
    }

    glowEffect(color, intensity) {
        const glow = document.createElement('div');
        glow.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, ${color}20, transparent 70%);
            pointer-events: none;
            z-index: 9997;
            opacity: ${intensity};
            transition: opacity 0.5s ease-in-out;
        `;

        document.body.appendChild(glow);

        setTimeout(() => {
            glow.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(glow);
            }, 500);
        }, 1000);
    }

    bounceEffect(intensity) {
        const buttons = document.querySelectorAll('button, .nav-button, .main-action-btn');

        buttons.forEach(button => {
            const originalTransform = button.style.transform;
            const bounceScale = 1 + intensity * 0.2;

            button.style.transform = `scale(${bounceScale})`;

            setTimeout(() => {
                button.style.transform = originalTransform;
            }, 300);
        });
    }

    pulseButtons(color, intensity) {
        const buttons = document.querySelectorAll('button, .nav-button, .main-action-btn');

        buttons.forEach(button => {
            const originalBoxShadow = button.style.boxShadow;
            const pulseShadow = `0 0 ${20 + intensity * 30}px ${color}`;

            button.style.boxShadow = pulseShadow;

            setTimeout(() => {
                button.style.boxShadow = originalBoxShadow;
            }, 1000);
        });
    }

    floatEffect(intensity) {
        const containers = document.querySelectorAll('.portal-container, .terminal-container, .monde-container, .profil-container');

        containers.forEach(container => {
            const originalTransform = container.style.transform;
            const floatAmount = intensity * 5;

            container.style.transform = `translateY(-${floatAmount}px)`;

            setTimeout(() => {
                container.style.transform = originalTransform;
            }, 2000);
        });
    }

    victoryAnimation(intensity) {
        // Confettis
        this.createConfetti(intensity);

        // Animation de victoire sur les badges
        const badges = document.querySelectorAll('.badge');
        badges.forEach((badge, index) => {
            setTimeout(() => {
                badge.style.transform = 'scale(1.2) rotate(360deg)';
                setTimeout(() => {
                    badge.style.transform = 'scale(1) rotate(0deg)';
                }, 500);
            }, index * 100);
        });
    }

    createConfetti(intensity) {
        const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
        const confettiCount = Math.floor(intensity * 50);

        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                top: -10px;
                left: ${Math.random() * window.innerWidth}px;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                pointer-events: none;
                z-index: 10000;
                animation: confettiFall 3s linear forwards;
            `;

            document.body.appendChild(confetti);

            setTimeout(() => {
                document.body.removeChild(confetti);
            }, 3000);
        }
    }

    // 🎵 SYSTÈME AUDIO

    playEmotionSound(soundType, intensity) {
        if (!this.audioContext) return;

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            // Configurer selon le type de son
            switch (soundType) {
                case 'luna_excited':
                    oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
                    oscillator.type = 'sine';
                    break;
                case 'luna_worried':
                    oscillator.frequency.setValueAtTime(400, this.audioContext.currentTime);
                    oscillator.type = 'triangle';
                    break;
                case 'luna_proud':
                    oscillator.frequency.setValueAtTime(1200, this.audioContext.currentTime);
                    oscillator.type = 'sine';
                    break;
                case 'luna_mysterious':
                    oscillator.frequency.setValueAtTime(300, this.audioContext.currentTime);
                    oscillator.type = 'sawtooth';
                    break;
                case 'luna_determined':
                    oscillator.frequency.setValueAtTime(600, this.audioContext.currentTime);
                    oscillator.type = 'square';
                    break;
                default:
                    oscillator.frequency.setValueAtTime(500, this.audioContext.currentTime);
                    oscillator.type = 'sine';
            }

            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(intensity * 0.1, this.audioContext.currentTime + 0.1);
            gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.5);

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.5);

        } catch (error) {
            console.warn("⚠️ Erreur audio:", error);
        }
    }

    playSound(soundType, intensity) {
        // Utiliser le système audio existant si disponible
        if (window.audioManager && window.audioManager.playSound) {
            window.audioManager.playSound(soundType, intensity);
        } else {
            this.playEmotionSound(soundType, intensity);
        }
    }

    // 🎨 MISE À JOUR DE L'INTERFACE

    updateInterfaceColors(color, intensity) {
        // Mettre à jour les couleurs CSS variables
        document.documentElement.style.setProperty('--luna-emotion-color', color);
        document.documentElement.style.setProperty('--luna-emotion-intensity', intensity);

        // Appliquer aux éléments spécifiques
        const lunaElements = document.querySelectorAll('.luna-avatar, .luna-message');
        lunaElements.forEach(element => {
            element.style.color = color;
            element.style.textShadow = `0 0 ${10 + intensity * 20}px ${color}`;
        });
    }

    // 🎬 LOOP D'ANIMATION

    startAnimationLoop() {
        const animate = () => {
            this.updateParticles();
            requestAnimationFrame(animate);
        };
        animate();
    }

    updateParticles() {
        // Effacer le canvas
        this.particleCtx.clearRect(0, 0, this.particleCanvas.width, this.particleCanvas.height);

        // Mettre à jour chaque système de particules
        this.particleSystems = this.particleSystems.filter(system => {
            system.duration--;

            if (system.duration <= 0) {
                return false;
            }

            this.updateParticleSystem(system);
            return true;
        });
    }

    updateParticleSystem(system) {
        const { type, particles } = system;

        particles.forEach(particle => {
            // Mettre à jour la vie
            particle.life -= particle.decay;

            if (particle.life <= 0) return;

            // Mettre à jour la position selon le type
            switch (type) {
                case 'explosion':
                case 'bouncing':
                case 'energetic':
                    particle.x += particle.vx;
                    particle.y += particle.y;
                    break;
                case 'worried':
                case 'calm':
                    particle.y += particle.vy;
                    break;
                case 'focused':
                    const dx = particle.targetX - particle.x;
                    const dy = particle.targetY - particle.y;
                    particle.x += dx * 0.05;
                    particle.y += dy * 0.05;
                    break;
            }

            // Gérer les rebonds
            if (type === 'bouncing') {
                if (particle.x <= 0 || particle.x >= window.innerWidth) {
                    particle.vx *= -particle.bounce;
                }
                if (particle.y <= 0 || particle.y >= window.innerHeight) {
                    particle.vy *= -particle.bounce;
                }
            }

            // Dessiner la particule
            this.drawParticle(particle, type);
        });
    }

    drawParticle(particle, type) {
        this.particleCtx.save();

        const alpha = particle.life;
        this.particleCtx.globalAlpha = alpha;

        switch (type) {
            case 'sparkles':
                this.particleCtx.fillStyle = particle.color;
                this.particleCtx.beginPath();
                this.particleCtx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                this.particleCtx.fill();

                // Effet de scintillement
                const twinkle = Math.sin(particle.twinkle + Date.now() * 0.01) * 0.5 + 0.5;
                this.particleCtx.globalAlpha = alpha * twinkle;
                this.particleCtx.fillStyle = '#ffffff';
                this.particleCtx.beginPath();
                this.particleCtx.arc(particle.x, particle.y, particle.size * 0.5, 0, Math.PI * 2);
                this.particleCtx.fill();
                break;

            case 'fog':
                this.particleCtx.fillStyle = particle.color;
                this.particleCtx.globalAlpha = particle.opacity * alpha;
                this.particleCtx.beginPath();
                this.particleCtx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                this.particleCtx.fill();
                break;

            case 'rays':
                this.particleCtx.strokeStyle = particle.color;
                this.particleCtx.lineWidth = 3;
                this.particleCtx.globalAlpha = particle.opacity * alpha;
                this.particleCtx.beginPath();
                this.particleCtx.moveTo(particle.x, particle.y);
                this.particleCtx.lineTo(
                    particle.x + Math.cos(particle.angle) * particle.length,
                    particle.y + Math.sin(particle.angle) * particle.length
                );
                this.particleCtx.stroke();
                break;

            default:
                this.particleCtx.fillStyle = particle.color;
                this.particleCtx.beginPath();
                this.particleCtx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                this.particleCtx.fill();
        }

        this.particleCtx.restore();
    }

    // 🛑 GESTION DES EFFETS

    stopAllEffects() {
        this.particleSystems = [];
        this.particleCtx.clearRect(0, 0, this.particleCanvas.width, this.particleCanvas.height);
    }

    // 🎮 API PUBLIQUE

    static getInstance() {
        if (!window.immersiveEffects) {
            window.immersiveEffects = new ImmersiveEffectsEngine();
        }
        return window.immersiveEffects;
    }
}

// Styles CSS pour les animations
const immersiveStyles = `
<style>
@keyframes confettiFall {
    to {
        transform: translateY(100vh) rotate(720deg);
    }
}

:root {
    --luna-emotion-color: #00ff00;
    --luna-emotion-intensity: 0.5;
}

.luna-avatar {
    color: var(--luna-emotion-color);
    text-shadow: 0 0 calc(10px + var(--luna-emotion-intensity) * 20px) var(--luna-emotion-color);
    transition: all 0.3s ease;
}

.luna-message {
    color: var(--luna-emotion-color);
    text-shadow: 0 0 calc(5px + var(--luna-emotion-intensity) * 10px) var(--luna-emotion-color);
    transition: all 0.3s ease;
}
</style>
`;

// Ajouter les styles au document
document.head.insertAdjacentHTML('beforeend', immersiveStyles);

// Instance globale
window.immersiveEffectsEngine = ImmersiveEffectsEngine.getInstance();

// Moteur d'effets immersifs chargé et prêt 