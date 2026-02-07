/**
 * Audio Manager - Gestionnaire audio unifié pour Arkalia Quest
 * Résout le problème des boutons non fonctionnels en centralisant les fonctions audio
 */

class AudioManager {
    constructor() {
        this.audioContext = null;
        this.audioUnlocked = false;
        this.volume = 0.3;
        this.init();
    }

    init() {
        // Initialiser le contexte audio
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            // AudioManager initialisé
        } catch (e) {
            console.warn('⚠️ AudioContext non supporté:', e);
        }
    }

    /**
     * Fonction principale pour jouer des sons
     * @param {string} soundId - ID du son à jouer
     */
    playSound(soundId) {
        // Tentative de lecture son

        // Débloquer l'audio au premier clic
        if (!this.audioUnlocked) {
            this.audioUnlocked = true;
            // Audio débloqué
        }

        // Sons différents selon le type
        switch (soundId) {
            case 'buttonSound':
                this.createSoundEffect(800, 0.15, 'square');
                break;
            case 'ambientSound':
                this.createSoundEffect(400, 0.5, 'sine');
                break;
            case 'easterSound':
                this.createSoundEffect(1200, 0.3, 'sawtooth');
                break;
            case 'success':
                this.createSoundEffect(1000, 0.2, 'sine');
                break;
            case 'error':
                this.createSoundEffect(300, 0.3, 'square');
                break;
            case 'typing':
                this.createSoundEffect(600, 0.05, 'sine');
                break;
            case 'hack':
                this.createSoundEffect(900, 0.1, 'triangle');
                break;
            default:
                this.createSoundEffect(600, 0.2, 'sine');
        }
    }

    /**
     * Crée un effet sonore
     * @param {number} frequency - Fréquence en Hz
     * @param {number} duration - Durée en secondes
     * @param {string} type - Type d'onde (sine, square, triangle, sawtooth)
     */
    createSoundEffect(frequency = 800, duration = 0.2, type = 'sine') {
        if (!this.audioContext) {
            console.warn('⚠️ AudioContext non disponible');
            return;
        }

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
            oscillator.type = type;

            gainNode.gain.setValueAtTime(this.volume, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + duration);

            // Son joué
        } catch (e) {
            console.warn('⚠️ Erreur création son:', e);
        }
    }

    /**
     * Définit le volume
     * @param {number} volume - Volume entre 0 et 1
     */
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        // Volume défini
    }

    /**
     * Active/désactive le son
     * @param {boolean} enabled - Activer ou non
     */
    setEnabled(enabled) {
        this.audioUnlocked = enabled;
        // Audio état modifié
    }

    /**
     * Joue un effet de frappe
     */
    playTypingSound() {
        this.playSound('typing');
    }

    /**
     * Joue un effet de succès
     */
    playSuccessSound() {
        this.playSound('success');
    }

    /**
     * Joue un effet d'erreur
     */
    playErrorSound() {
        this.playSound('error');
    }

    /**
     * Joue un effet de hacking
     */
    playHackSound() {
        this.playSound('hack');
    }
}

// Instance globale
window.audioManager = new AudioManager();

// Fonction globale pour compatibilité
window.playSound = function (soundId) {
    window.audioManager.playSound(soundId);
};

// Fonction globale pour compatibilité avec l'ancien code
window.createSoundEffect = function (frequency = 800, duration = 0.2) {
    window.audioManager.createSoundEffect(frequency, duration, 'sine');
};

// Initialisation automatique
document.addEventListener('DOMContentLoaded', function () {
    // AudioManager chargé et prêt

    // Débloquer l'audio au premier clic
    document.addEventListener('click', function () {
        if (!window.audioManager.audioUnlocked) {
            window.audioManager.audioUnlocked = true;
            // Audio débloqué au premier clic
        }
    }, { once: true });
});

// AudioManager.js chargé 