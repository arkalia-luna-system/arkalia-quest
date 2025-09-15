/**
 * Optimiseur de performances JavaScript pour Arkalia Quest
 */

class PerformanceOptimizer {
    constructor() {
        this.metrics = {
            renderTime: 0,
            memoryUsage: 0,
            frameRate: 0,
            loadTime: 0,
            errorCount: 0
        };

        this.observers = [];
        this.performanceEntries = [];
        this.isMonitoring = false;

        this.init();
    }

    init() {
        // Démarrer le monitoring automatiquement
        this.startMonitoring();

        // Optimiser les performances au chargement
        this.optimizeOnLoad();

        // Configurer les observers de performance
        this.setupPerformanceObservers();
    }

    startMonitoring() {
        if (this.isMonitoring) return;

        this.isMonitoring = true;

        // Monitorer les performances de rendu
        this.monitorRenderPerformance();

        // Monitorer l'utilisation mémoire
        this.monitorMemoryUsage();

        // Monitorer les erreurs
        this.monitorErrors();

        console.log('🚀 Performance monitoring activé');
    }

    stopMonitoring() {
        this.isMonitoring = false;

        // Arrêter tous les observers
        this.observers.forEach(observer => observer.disconnect());
        this.observers = [];

        console.log('⏹️ Performance monitoring arrêté');
    }

    monitorRenderPerformance() {
        let frameCount = 0;
        let lastTime = performance.now();

        const measureFrame = () => {
            frameCount++;
            const currentTime = performance.now();

            if (currentTime - lastTime >= 1000) {
                this.metrics.frameRate = Math.round((frameCount * 1000) / (currentTime - lastTime));
                frameCount = 0;
                lastTime = currentTime;

                // Alerter si le FPS est trop bas
                if (this.metrics.frameRate < 30) {
                    this.optimizeRendering();
                }
            }

            if (this.isMonitoring) {
                requestAnimationFrame(measureFrame);
            }
        };

        requestAnimationFrame(measureFrame);
    }

    monitorMemoryUsage() {
        const checkMemory = () => {
            if (performance.memory) {
                this.metrics.memoryUsage = {
                    used: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024),
                    total: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024),
                    limit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024)
                };

                // Alerter si l'utilisation mémoire est élevée
                if (this.metrics.memoryUsage.used > 100) { // > 100MB
                    this.optimizeMemory();
                }
            }

            if (this.isMonitoring) {
                setTimeout(checkMemory, 5000); // Vérifier toutes les 5 secondes
            }
        };

        checkMemory();
    }

    monitorErrors() {
        window.addEventListener('error', (event) => {
            this.metrics.errorCount++;
            this.logPerformanceEvent('error', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno
            });
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.metrics.errorCount++;
            this.logPerformanceEvent('unhandledrejection', {
                reason: event.reason
            });
        });
    }

    setupPerformanceObservers() {
        // Observer les entrées de performance
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    this.performanceEntries.push({
                        name: entry.name,
                        duration: entry.duration,
                        startTime: entry.startTime,
                        type: entry.entryType
                    });
                }
            });

            observer.observe({ entryTypes: ['measure', 'navigation', 'resource'] });
            this.observers.push(observer);
        }
    }

    optimizeOnLoad() {
        // Optimiser les images
        this.optimizeImages();

        // Optimiser les animations
        this.optimizeAnimations();

        // Optimiser les événements
        this.optimizeEventListeners();

        // Optimiser le DOM
        this.optimizeDOM();
    }

    optimizeImages() {
        // Lazy loading des images
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    optimizeAnimations() {
        // Utiliser will-change pour les éléments animés
        const animatedElements = document.querySelectorAll('.animated, .pulse, .glow');
        animatedElements.forEach(el => {
            el.style.willChange = 'transform, opacity';
        });

        // Optimiser les animations CSS
        const style = document.createElement('style');
        style.textContent = `
            .optimized-animation {
                transform: translateZ(0);
                backface-visibility: hidden;
                perspective: 1000px;
            }
        `;
        document.head.appendChild(style);
    }

    optimizeEventListeners() {
        // Debounce les événements de scroll
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.handleScroll();
            }, 16); // ~60fps
        });

        // Debounce les événements de resize
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        });
    }

    optimizeDOM() {
        // Utiliser DocumentFragment pour les insertions multiples
        this.createDocumentFragment = () => document.createDocumentFragment();

        // Optimiser les sélecteurs
        this.optimizeSelectors();

        // Réduire les reflows
        this.minimizeReflows();
    }

    optimizeSelectors() {
        // Cache des sélecteurs fréquemment utilisés
        this.cachedSelectors = new Map();

        this.querySelector = (selector) => {
            if (!this.cachedSelectors.has(selector)) {
                this.cachedSelectors.set(selector, document.querySelector(selector));
            }
            return this.cachedSelectors.get(selector);
        };

        this.querySelectorAll = (selector) => {
            if (!this.cachedSelectors.has(selector + '_all')) {
                this.cachedSelectors.set(selector + '_all', document.querySelectorAll(selector));
            }
            return this.cachedSelectors.get(selector + '_all');
        };
    }

    minimizeReflows() {
        // Batch les modifications DOM
        this.domBatch = [];
        this.batchDOMUpdates = (callback) => {
            this.domBatch.push(callback);

            if (this.domBatch.length === 1) {
                requestAnimationFrame(() => {
                    this.domBatch.forEach(cb => cb());
                    this.domBatch = [];
                });
            }
        };
    }

    optimizeRendering() {
        console.log('🎨 Optimisation du rendu...');

        // Réduire la qualité des animations si nécessaire
        const animatedElements = document.querySelectorAll('.animated');
        animatedElements.forEach(el => {
            el.style.animationDuration = '0.1s';
        });

        // Désactiver les effets visuels lourds
        document.body.classList.add('performance-mode');
    }

    optimizeMemory() {
        console.log('🧠 Optimisation mémoire...');

        // Nettoyer les caches
        this.clearCaches();

        // Forcer le garbage collection si disponible
        if (window.gc) {
            window.gc();
        }

        // Réduire la taille des données en mémoire
        this.reduceMemoryUsage();
    }

    clearCaches() {
        // Nettoyer le cache des sélecteurs
        this.cachedSelectors?.clear();

        // Nettoyer les entrées de performance anciennes
        const now = performance.now();
        this.performanceEntries = this.performanceEntries.filter(
            entry => now - entry.startTime < 60000 // Garder seulement la dernière minute
        );
    }

    reduceMemoryUsage() {
        // Réduire la taille des images
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (img.naturalWidth > 800) {
                img.style.maxWidth = '800px';
                img.style.height = 'auto';
            }
        });
    }

    handleScroll() {
        // Optimiser le scroll
        const scrollTop = window.pageYOffset;

        // Parallax optimisé
        const parallaxElements = document.querySelectorAll('.parallax');
        parallaxElements.forEach(el => {
            const speed = el.dataset.speed || 0.5;
            const yPos = -(scrollTop * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });
    }

    handleResize() {
        // Optimiser le resize
        this.clearCaches(); // Nettoyer les caches lors du resize

        // Recalculer les dimensions si nécessaire
        const elements = document.querySelectorAll('.responsive');
        elements.forEach(el => {
            el.style.width = 'auto';
        });
    }

    logPerformanceEvent(type, data) {
        const event = {
            type,
            data,
            timestamp: performance.now(),
            memory: this.metrics.memoryUsage
        };

        // Envoyer vers l'API si disponible (avec throttling)
        if (window.fetch && this.shouldLogPerformance()) {
            fetch('/api/performance/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(event)
            }).catch(() => {
                // Ignorer les erreurs de réseau
            });
        }
    }

    shouldLogPerformance() {
        // Throttling : ne logger que toutes les 5 secondes
        const now = Date.now();
        if (!this.lastLogTime || now - this.lastLogTime > 5000) {
            this.lastLogTime = now;
            return true;
        }
        return false;
    }

    getMetrics() {
        return {
            ...this.metrics,
            performanceEntries: this.performanceEntries.length,
            cachedSelectors: this.cachedSelectors?.size || 0
        };
    }

    getPerformanceReport() {
        const metrics = this.getMetrics();
        const report = {
            timestamp: new Date().toISOString(),
            metrics,
            recommendations: this.getRecommendations()
        };

        return report;
    }

    getRecommendations() {
        const recommendations = [];

        if (this.metrics.frameRate < 30) {
            recommendations.push('Réduire la complexité des animations');
        }

        if (this.metrics.memoryUsage.used > 100) {
            recommendations.push('Optimiser l\'utilisation mémoire');
        }

        if (this.metrics.errorCount > 5) {
            recommendations.push('Corriger les erreurs JavaScript');
        }

        return recommendations;
    }
}

// Initialiser l'optimiseur de performances
window.performanceOptimizer = new PerformanceOptimizer();

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceOptimizer;
}