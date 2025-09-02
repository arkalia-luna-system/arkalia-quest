/**
 * ARKALIA QUEST - SYSTÈME DE FEEDBACK ULTRA-PRO 2025
 * Animations, effets visuels et micro-interactions professionnelles
 */

class UltraProEffects {
    constructor() {
        this.init();
    }

    init() {
        this.setupButtonEffects();
        this.setupSuccessAnimations();
        this.setupErrorAnimations();
        this.setupLoadingStates();
        this.setupConfettiSystem();
        this.setupParticleEffects();
        this.setupSoundEffects();
        // Système d'effets ultra-pro initialisé
    }

    // ===== EFFETS DE BOUTONS ULTRA-PRO =====

    setupButtonEffects() {
        // Effet de ripple sur tous les boutons
        document.addEventListener('click', (e) => {
            if (e.target.matches('button, .nav-btn, .main-action-btn, .secondary-btn')) {
                this.createRippleEffect(e);
                this.playButtonSound();
            }
        });

        // Effet de hover avancé
        document.addEventListener('mouseover', (e) => {
            if (e.target.matches('button, .nav-btn, .main-action-btn, .secondary-btn')) {
                this.createHoverGlow(e.target);
            }
        });
    }

    createRippleEffect(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            transform: scale(0);
            animation: rippleEffect 0.6s ease-out;
            pointer-events: none;
            z-index: 1000;
        `;

        button.style.position = 'relative';
        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }

    createHoverGlow(element) {
        element.style.boxShadow = `
            0 8px 25px rgba(0, 102, 255, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.3)
        `;

        setTimeout(() => {
            element.style.boxShadow = '';
        }, 300);
    }

    // ===== ANIMATIONS DE SUCCÈS ULTRA-PRO =====

    setupSuccessAnimations() {
        // Observer pour détecter les messages de succès
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.classList && node.classList.contains('message') && node.classList.contains('success')) {
                            this.triggerSuccessAnimation(node);
                        }
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    triggerSuccessAnimation(element) {
        // Animation de succès
        element.style.animation = 'successPulse 0.6s ease-out';

        // Effet de brillance
        this.createSuccessGlow(element);

        // Confettis
        this.createConfetti(element);

        // Son de succès
        this.playSuccessSound();

        // Message de félicitations
        this.showCongratulations(element);
    }

    createSuccessGlow(element) {
        const glow = document.createElement('div');
        glow.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle, rgba(0, 255, 136, 0.2) 0%, transparent 70%);
            border-radius: 8px;
            animation: successGlow 1s ease-out;
            pointer-events: none;
            z-index: -1;
        `;

        element.style.position = 'relative';
        element.appendChild(glow);

        setTimeout(() => glow.remove(), 1000);
    }

    showCongratulations(element) {
        const congrats = document.createElement('div');
        congrats.innerHTML = '🎉 BRAVO ! 🎉';
        congrats.style.cssText = `
            position: absolute;
            top: -30px;
            right: 10px;
            background: linear-gradient(145deg, #00ff88, #00cc6a);
            color: #000;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            animation: congratsFloat 2s ease-out;
            z-index: 1000;
        `;

        element.appendChild(congrats);
        setTimeout(() => congrats.remove(), 2000);
    }

    // ===== ANIMATIONS D'ERREUR ULTRA-PRO =====

    setupErrorAnimations() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.classList && node.classList.contains('message') && node.classList.contains('error')) {
                            this.triggerErrorAnimation(node);
                        }
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    triggerErrorAnimation(element) {
        // Animation d'erreur
        element.style.animation = 'errorShake 0.6s ease-out';

        // Effet de rougeoiement
        this.createErrorGlow(element);

        // Son d'erreur
        this.playErrorSound();

        // Message d'encouragement
        this.showEncouragement(element);
    }

    createErrorGlow(element) {
        const glow = document.createElement('div');
        glow.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle, rgba(255, 0, 68, 0.2) 0%, transparent 70%);
            border-radius: 8px;
            animation: errorGlow 1s ease-out;
            pointer-events: none;
            z-index: -1;
        `;

        element.style.position = 'relative';
        element.appendChild(glow);

        setTimeout(() => glow.remove(), 1000);
    }

    showEncouragement(element) {
        const encouragement = document.createElement('div');
        encouragement.innerHTML = '💪 Essaie encore !';
        encouragement.style.cssText = `
            position: absolute;
            top: -30px;
            right: 10px;
            background: linear-gradient(145deg, #ff6600, #cc5200);
            color: #fff;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            animation: encouragementFloat 2s ease-out;
            z-index: 1000;
        `;

        element.appendChild(encouragement);
        setTimeout(() => encouragement.remove(), 2000);
    }

    // ===== ÉTATS DE CHARGEMENT ULTRA-PRO =====

    setupLoadingStates() {
        // Loading spinner pour les boutons
        document.addEventListener('click', (e) => {
            if (e.target.matches('button[data-loading]')) {
                this.showButtonLoading(e.target);
            }
        });
    }

    showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<span class="loading-spinner"></span> Chargement...';
        button.disabled = true;

        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 2000);
    }

    // ===== SYSTÈME DE CONFETTIS ULTRA-PRO =====

    setupConfettiSystem() {
        this.confettiColors = ['#00ff88', '#0066ff', '#ff6600', '#ff0044', '#00ffff'];
    }

    createConfetti(element) {
        const rect = element.getBoundingClientRect();
        const colors = this.confettiColors;

        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                this.createConfettiPiece(rect, colors[Math.floor(Math.random() * colors.length)]);
            }, i * 50);
        }
    }

    createConfettiPiece(rect, color) {
        const confetti = document.createElement('div');
        const size = Math.random() * 8 + 4;
        const startX = rect.left + Math.random() * rect.width;
        const startY = rect.top;

        confetti.style.cssText = `
            position: fixed;
            width: ${size}px;
            height: ${size}px;
            background: ${color};
            left: ${startX}px;
            top: ${startY}px;
            border-radius: 2px;
            animation: confettiFall 2s ease-out forwards;
            z-index: 10000;
            pointer-events: none;
        `;

        document.body.appendChild(confetti);

        setTimeout(() => confetti.remove(), 2000);
    }

    // ===== EFFETS DE PARTICULES ULTRA-PRO =====

    setupParticleEffects() {
        // Particules de fond
        this.createBackgroundParticles();

        // Particules interactives
        this.setupInteractiveParticles();
    }

    createBackgroundParticles() {
        const particleContainer = document.createElement('div');
        particleContainer.id = 'particle-container';
        particleContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        `;

        document.body.appendChild(particleContainer);

        for (let i = 0; i < 50; i++) {
            this.createParticle(particleContainer);
        }
    }

    createParticle(container) {
        const particle = document.createElement('div');
        const size = Math.random() * 3 + 1;
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;
        const duration = Math.random() * 20 + 10;

        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: rgba(0, 102, 255, 0.3);
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            animation: particleFloat ${duration}s linear infinite;
        `;

        container.appendChild(particle);
    }

    setupInteractiveParticles() {
        document.addEventListener('mousemove', (e) => {
            if (Math.random() < 0.1) {
                this.createMouseParticle(e.clientX, e.clientY);
            }
        });
    }

    createMouseParticle(x, y) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: rgba(0, 255, 136, 0.6);
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            animation: mouseParticle 1s ease-out forwards;
            pointer-events: none;
            z-index: 1000;
        `;

        document.body.appendChild(particle);
        setTimeout(() => particle.remove(), 1000);
    }

    // ===== EFFETS SONORES ULTRA-PRO =====

    setupSoundEffects() {
        this.audioContext = null;
        this.initAudioContext();
    }

    initAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            // Audio context non supporté
        }
    }

    playButtonSound() {
        if (!this.audioContext) return;

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
    }

    playSuccessSound() {
        if (!this.audioContext) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.setValueAtTime(523, this.audioContext.currentTime);
        oscillator.frequency.setValueAtTime(659, this.audioContext.currentTime + 0.1);
        oscillator.frequency.setValueAtTime(784, this.audioContext.currentTime + 0.2);

        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.3);
    }

    playErrorSound() {
        if (!this.audioContext) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.setValueAtTime(200, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(150, this.audioContext.currentTime + 0.2);

        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.2);
    }
}

// ===== CSS ANIMATIONS ULTRA-PRO =====

const ultraProStyles = `
    @keyframes rippleEffect {
        0% { transform: scale(0); opacity: 1; }
        100% { transform: scale(4); opacity: 0; }
    }
    
    @keyframes successGlow {
        0% { opacity: 0; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 0; transform: scale(1.5); }
    }
    
    @keyframes errorGlow {
        0% { opacity: 0; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 0; transform: scale(1.5); }
    }
    
    @keyframes congratsFloat {
        0% { transform: translateY(0) scale(0.8); opacity: 0; }
        50% { transform: translateY(-20px) scale(1.1); opacity: 1; }
        100% { transform: translateY(-40px) scale(1); opacity: 0; }
    }
    
    @keyframes encouragementFloat {
        0% { transform: translateY(0) scale(0.8); opacity: 0; }
        50% { transform: translateY(-20px) scale(1.1); opacity: 1; }
        100% { transform: translateY(-40px) scale(1); opacity: 0; }
    }
    
    @keyframes confettiFall {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    
    @keyframes particleFloat {
        0% { transform: translateY(0) translateX(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) translateX(100px); opacity: 0; }
    }
    
    @keyframes mouseParticle {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0) translateY(-20px); opacity: 0; }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
        margin-right: 8px;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;

// Injection des styles
const styleSheet = document.createElement('style');
styleSheet.textContent = ultraProStyles;
document.head.appendChild(styleSheet);

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    window.ultraProEffects = new UltraProEffects();
}); 