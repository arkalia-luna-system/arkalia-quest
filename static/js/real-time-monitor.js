/**
 * Système de monitoring en temps réel pour Arkalia Quest
 */

class RealTimeMonitor {
    constructor() {
        this.metrics = {
            performance: {},
            security: {},
            cache: {},
            database: {}
        };

        this.updateInterval = 5000; // 5 secondes
        this.isMonitoring = false;
        this.charts = {};

        this.init();
    }

    init() {
        this.createDashboard();
        this.startMonitoring();
        this.setupEventListeners();
    }

    createDashboard() {
        // Créer le dashboard de monitoring (masqué par défaut)
        const dashboard = document.createElement('div');
        dashboard.id = 'real-time-monitor';
        dashboard.className = 'monitor-dashboard hidden';
        dashboard.innerHTML = `
            <div class="monitor-header">
                <h3>🚀 Monitoring Temps Réel</h3>
                <button id="toggle-monitor" class="btn btn-sm">Afficher</button>
            </div>
            <div class="monitor-content">
                <div class="metrics-grid">
                    <div class="metric-card performance">
                        <h4>⚡ Performance</h4>
                        <div class="metric-value" id="response-time">-</div>
                        <div class="metric-label">Temps de réponse (ms)</div>
                        <div class="metric-trend" id="response-trend"></div>
                    </div>
                    <div class="metric-card security">
                        <h4>🛡️ Sécurité</h4>
                        <div class="metric-value" id="blocked-ips">-</div>
                        <div class="metric-label">IPs bloquées</div>
                        <div class="metric-trend" id="security-trend"></div>
                    </div>
                    <div class="metric-card cache">
                        <h4>💾 Cache</h4>
                        <div class="metric-value" id="cache-hit-rate">-</div>
                        <div class="metric-label">Taux de cache (%)</div>
                        <div class="metric-trend" id="cache-trend"></div>
                    </div>
                    <div class="metric-card database">
                        <h4>🗄️ Base de données</h4>
                        <div class="metric-value" id="db-queries">-</div>
                        <div class="metric-label">Requêtes/seconde</div>
                        <div class="metric-trend" id="db-trend"></div>
                    </div>
                </div>
                <div class="charts-container">
                    <div class="chart-container">
                        <canvas id="performance-chart"></canvas>
                    </div>
                    <div class="chart-container">
                        <canvas id="security-chart"></canvas>
                    </div>
                </div>
            </div>
        `;

        // Ajouter les styles
        const styles = document.createElement('style');
        styles.textContent = `
            .monitor-dashboard {
                position: fixed;
                top: 20px;
                right: 20px;
                width: 350px;
                background: rgba(0, 0, 0, 0.95);
                border: 2px solid #00ff00;
                border-radius: 10px;
                color: #00ff00;
                font-family: 'Hack', monospace;
                z-index: 10000;
                max-height: 70vh;
                overflow-y: auto;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
                backdrop-filter: blur(10px);
            }
            
            .monitor-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                border-bottom: 1px solid #00ff00;
            }
            
            .monitor-content {
                padding: 15px;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 20px;
            }
            
            .metric-card {
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                text-align: center;
            }
            
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                margin: 5px 0;
            }
            
            .metric-label {
                font-size: 12px;
                opacity: 0.8;
            }
            
            .metric-trend {
                font-size: 10px;
                margin-top: 5px;
            }
            
            .trend-up { color: #ff6b6b; }
            .trend-down { color: #4ecdc4; }
            .trend-stable { color: #00ff00; }
            
            .charts-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            
            .chart-container {
                height: 150px;
                background: rgba(0, 255, 0, 0.05);
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 5px;
            }
            
            .monitor-dashboard.hidden {
                display: none;
            }
            
            .btn {
                background: #00ff00;
                color: #000;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                cursor: pointer;
                font-family: 'Hack', monospace;
            }
            
            .btn:hover {
                background: #00cc00;
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(dashboard);

        // Ajouter un bouton discret pour activer le monitoring
        this.createMonitorToggle();
    }

    createMonitorToggle() {
        // Créer un bouton discret pour activer le monitoring
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'monitor-toggle-btn';
        toggleBtn.className = 'monitor-toggle-btn';
        toggleBtn.innerHTML = '📊';
        toggleBtn.title = 'Monitoring système (Ctrl+M)';

        // Styles pour le bouton toggle
        const toggleStyles = document.createElement('style');
        toggleStyles.textContent = `
            .monitor-toggle-btn {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 50px;
                height: 50px;
                background: rgba(0, 255, 0, 0.2);
                border: 2px solid #00ff00;
                border-radius: 50%;
                color: #00ff00;
                font-size: 20px;
                cursor: pointer;
                z-index: 9999;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
            }
            
            .monitor-toggle-btn:hover {
                background: rgba(0, 255, 0, 0.4);
                transform: scale(1.1);
                box-shadow: 0 0 25px rgba(0, 255, 0, 0.5);
            }
            
            .monitor-toggle-btn:active {
                transform: scale(0.95);
            }
            
            .monitor-toggle-btn.active {
                background: rgba(0, 255, 0, 0.6);
                box-shadow: 0 0 30px rgba(0, 255, 0, 0.7);
            }
        `;

        document.head.appendChild(toggleStyles);
        document.body.appendChild(toggleBtn);

        // Event listener pour le bouton toggle
        toggleBtn.addEventListener('click', () => {
            const dashboard = document.getElementById('real-time-monitor');
            const isHidden = dashboard.classList.contains('hidden');

            if (isHidden) {
                dashboard.classList.remove('hidden');
                toggleBtn.classList.add('active');
                toggleBtn.innerHTML = '📊';
                toggleBtn.title = 'Masquer le monitoring (Ctrl+M)';

                // Message de LUNA pour expliquer le monitoring
                if (window.lunaVision) {
                    window.lunaVision.showLunaMessage("Monitoring système activé. Je surveille les performances en temps réel pour toi, hacker !", 3000);
                }
            } else {
                dashboard.classList.add('hidden');
                toggleBtn.classList.remove('active');
                toggleBtn.innerHTML = '📊';
                toggleBtn.title = 'Afficher le monitoring (Ctrl+M)';

                // Message de LUNA
                if (window.lunaVision) {
                    window.lunaVision.showLunaMessage("Monitoring masqué. Concentre-toi sur ta mission, hacker !", 2000);
                }
            }
        });

        // Raccourci clavier Ctrl+M
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'm') {
                e.preventDefault();
                toggleBtn.click();
            }
        });
    }

    setupEventListeners() {
        // Toggle du dashboard
        document.getElementById('toggle-monitor').addEventListener('click', () => {
            const dashboard = document.getElementById('real-time-monitor');
            const button = document.getElementById('toggle-monitor');

            if (dashboard.classList.contains('hidden')) {
                dashboard.classList.remove('hidden');
                button.textContent = 'Masquer';
            } else {
                dashboard.classList.add('hidden');
                button.textContent = 'Afficher';
            }
        });
    }

    startMonitoring() {
        if (this.isMonitoring) return;

        this.isMonitoring = true;
        this.updateMetrics();

        // Mettre à jour toutes les 5 secondes
        setInterval(() => {
            if (this.isMonitoring) {
                this.updateMetrics();
            }
        }, this.updateInterval);
    }

    stopMonitoring() {
        this.isMonitoring = false;
    }

    async updateMetrics() {
        try {
            // Récupérer les métriques de performance
            const performanceResponse = await fetch('/api/performance/stats');
            if (performanceResponse.ok) {
                const data = await performanceResponse.json();
                this.metrics.performance = data.performance;
                this.metrics.cache = data.cache;
                this.metrics.security = data.security;
                this.updatePerformanceDisplay();
            }

            // Récupérer les métriques de sécurité
            const securityResponse = await fetch('/api/security/stats');
            if (securityResponse.ok) {
                const data = await securityResponse.json();
                this.metrics.security = data.security_stats;
                this.updateSecurityDisplay();
            }

        } catch (error) {
            console.error('Erreur récupération métriques:', error);
        }
    }

    updatePerformanceDisplay() {
        const perf = this.metrics.performance;

        // Temps de réponse
        const responseTime = perf.average_response_time || 0;
        document.getElementById('response-time').textContent = responseTime.toFixed(1);
        this.updateTrend('response-trend', responseTime, 'ms');

        // Cache hit rate
        const cacheHitRate = this.metrics.cache.hit_rate || 0;
        document.getElementById('cache-hit-rate').textContent = cacheHitRate.toFixed(1);
        this.updateTrend('cache-trend', cacheHitRate, '%');

        // Requêtes par seconde
        const queriesPerSecond = perf.calls_per_second || 0;
        document.getElementById('db-queries').textContent = queriesPerSecond.toFixed(1);
        this.updateTrend('db-trend', queriesPerSecond, '/s');
    }

    updateSecurityDisplay() {
        const security = this.metrics.security;

        // IPs bloquées
        const blockedIPs = security.blocked_ips || 0;
        document.getElementById('blocked-ips').textContent = blockedIPs;
        this.updateTrend('security-trend', blockedIPs, '');
    }

    updateTrend(elementId, currentValue, unit) {
        const trendElement = document.getElementById(elementId);
        if (!trendElement) return;

        // Simuler une tendance (en réalité, on comparerait avec la valeur précédente)
        const trend = Math.random() - 0.5; // -0.5 à 0.5

        let trendClass, trendText;
        if (trend > 0.1) {
            trendClass = 'trend-up';
            trendText = '↗';
        } else if (trend < -0.1) {
            trendClass = 'trend-down';
            trendText = '↘';
        } else {
            trendClass = 'trend-stable';
            trendText = '→';
        }

        trendElement.className = `metric-trend ${trendClass}`;
        trendElement.textContent = `${trendText} ${trend.toFixed(2)}${unit}`;
    }

    createChart(canvasId, data, label, color = '#00ff00') {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const width = canvas.width = canvas.offsetWidth;
        const height = canvas.height = canvas.offsetHeight;

        // Effacer le canvas
        ctx.clearRect(0, 0, width, height);

        // Dessiner le graphique
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();

        const maxValue = Math.max(...data);
        const minValue = Math.min(...data);
        const range = maxValue - minValue || 1;

        data.forEach((value, index) => {
            const x = (index / (data.length - 1)) * width;
            const y = height - ((value - minValue) / range) * height;

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();

        // Ajouter des points
        ctx.fillStyle = color;
        data.forEach((value, index) => {
            const x = (index / (data.length - 1)) * width;
            const y = height - ((value - minValue) / range) * height;
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
        });

        // Ajouter le label
        ctx.fillStyle = color;
        ctx.font = '12px Hack';
        ctx.fillText(label, 10, 20);
    }

    updateCharts() {
        // Données simulées pour les graphiques
        const performanceData = Array.from({ length: 20 }, () => Math.random() * 100 + 50);
        const securityData = Array.from({ length: 20 }, () => Math.random() * 10);

        this.createChart('performance-chart', performanceData, 'Performance (ms)');
        this.createChart('security-chart', securityData, 'Sécurité (incidents)');
    }

    showAlert(message, type = 'info') {
        const alert = document.createElement('div');
        alert.className = `monitor-alert ${type}`;
        alert.textContent = message;

        const styles = `
            .monitor-alert {
                position: fixed;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                padding: 10px 20px;
                border-radius: 5px;
                color: #000;
                font-family: 'Hack', monospace;
                z-index: 10001;
                animation: slideDown 0.3s ease;
            }
            
            .monitor-alert.info { background: #00ff00; }
            .monitor-alert.warning { background: #ffaa00; }
            .monitor-alert.error { background: #ff0000; color: #fff; }
            
            @keyframes slideDown {
                from { transform: translateX(-50%) translateY(-100%); }
                to { transform: translateX(-50%) translateY(0); }
            }
        `;

        if (!document.getElementById('monitor-alert-styles')) {
            const styleElement = document.createElement('style');
            styleElement.id = 'monitor-alert-styles';
            styleElement.textContent = styles;
            document.head.appendChild(styleElement);
        }

        document.body.appendChild(alert);

        // Supprimer l'alerte après 3 secondes
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 3000);
    }

    getMetrics() {
        return this.metrics;
    }

    exportMetrics() {
        const data = {
            timestamp: new Date().toISOString(),
            metrics: this.metrics
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `arkalia-metrics-${Date.now()}.json`;
        a.click();

        URL.revokeObjectURL(url);
    }
}

// Initialiser le monitoring en temps réel
document.addEventListener('DOMContentLoaded', () => {
    window.realTimeMonitor = new RealTimeMonitor();

    // Mettre à jour les graphiques toutes les 10 secondes
    setInterval(() => {
        if (window.realTimeMonitor) {
            window.realTimeMonitor.updateCharts();
        }
    }, 10000);
});

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RealTimeMonitor;
}
