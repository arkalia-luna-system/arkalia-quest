/**
 * Interface Analytics pour Arkalia Quest
 * Collecte et envoie les données d'engagement utilisateur
 */

class AnalyticsInterface {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.userId = null;
        this.sessionStartTime = Date.now();
        this.eventQueue = [];
        this.isEnabled = true;
        this.flushInterval = 30000; // 30 secondes
        this.maxQueueSize = 50;
        
        // Démarrer le flush automatique
        this.startAutoFlush();
        
        // Écouter les événements du terminal
        this.setupEventListeners();
        
        console.log('🔍 Analytics Interface initialisée');
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    setUserId(userId) {
        this.userId = userId;
        this.trackEvent('session_start', {
            session_id: this.sessionId,
            user_id: userId
        });
    }
    
    trackEvent(eventType, data = {}, context = {}) {
        if (!this.isEnabled || !this.userId) return;
        
        const event = {
            event_type: eventType,
            user_id: this.userId,
            session_id: this.sessionId,
            timestamp: Date.now(),
            data: data,
            context: {
                ...context,
                user_agent: navigator.userAgent,
                screen_resolution: `${screen.width}x${screen.height}`,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
            }
        };
        
        this.eventQueue.push(event);
        
        // Flush si la queue est pleine
        if (this.eventQueue.length >= this.maxQueueSize) {
            this.flushEvents();
        }
    }
    
    async flushEvents() {
        if (this.eventQueue.length === 0) return;
        
        const events = [...this.eventQueue];
        this.eventQueue = [];
        
        try {
            const response = await fetch('/api/analytics/track', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    events: events
                })
            });
            
            if (!response.ok) {
                console.warn('⚠️ Erreur lors de l\'envoi des événements analytics');
                // Remettre les événements dans la queue en cas d'échec
                this.eventQueue.unshift(...events);
            }
        } catch (error) {
            console.error('❌ Erreur analytics:', error);
            // Remettre les événements dans la queue en cas d'échec
            this.eventQueue.unshift(...events);
        }
    }
    
    startAutoFlush() {
        setInterval(() => {
            this.flushEvents();
        }, this.flushInterval);
    }
    
    setupEventListeners() {
        // Écouter les événements du terminal
        document.addEventListener('arkalia:command_executed', (e) => {
            this.trackEvent('command_executed', {
                command: e.detail.command,
                success: e.detail.success,
                execution_time: e.detail.executionTime
            });
        });
        
        // Écouter les événements de mission
        document.addEventListener('arkalia:mission_start', (e) => {
            this.trackEvent('mission_start', {
                mission_id: e.detail.missionId,
                mission_name: e.detail.missionName,
                difficulty: e.detail.difficulty
            });
        });
        
        document.addEventListener('arkalia:mission_complete', (e) => {
            this.trackEvent('mission_complete', {
                mission_id: e.detail.missionId,
                completion_time: e.detail.completionTime,
                score: e.detail.score,
                hints_used: e.detail.hintsUsed
            });
        });
        
        document.addEventListener('arkalia:mission_fail', (e) => {
            this.trackEvent('mission_fail', {
                mission_id: e.detail.missionId,
                failure_reason: e.detail.reason,
                attempts: e.detail.attempts
            });
        });
        
        // Écouter les événements de jeu éducatif
        document.addEventListener('arkalia:game_start', (e) => {
            this.trackEvent('game_start', {
                game_type: e.detail.gameType,
                game_id: e.detail.gameId,
                difficulty: e.detail.difficulty
            });
        });
        
        document.addEventListener('arkalia:game_complete', (e) => {
            this.trackEvent('game_complete', {
                game_type: e.detail.gameType,
                game_id: e.detail.gameId,
                score: e.detail.score,
                completion_time: e.detail.completionTime,
                perfect_score: e.detail.perfectScore
            });
        });
        
        document.addEventListener('arkalia:game_fail', (e) => {
            this.trackEvent('game_fail', {
                game_type: e.detail.gameType,
                game_id: e.detail.gameId,
                failure_reason: e.detail.reason,
                attempts: e.detail.attempts
            });
        });
        
        // Écouter les événements de tutoriel
        document.addEventListener('arkalia:tutorial_start', (e) => {
            this.trackEvent('tutorial_start', {
                tutorial_id: e.detail.tutorialId,
                tutorial_name: e.detail.tutorialName
            });
        });
        
        document.addEventListener('arkalia:tutorial_complete', (e) => {
            this.trackEvent('tutorial_complete', {
                tutorial_id: e.detail.tutorialId,
                completion_time: e.detail.completionTime
            });
        });
        
        // Écouter les événements de badge
        document.addEventListener('arkalia:badge_earned', (e) => {
            this.trackEvent('badge_earned', {
                badge_id: e.detail.badgeId,
                badge_name: e.detail.badgeName,
                badge_category: e.detail.badgeCategory
            });
        });
        
        // Écouter les événements d'émotion
        document.addEventListener('arkalia:emotion_triggered', (e) => {
            this.trackEvent('emotion_triggered', {
                emotion: e.detail.emotion,
                intensity: e.detail.intensity,
                trigger: e.detail.trigger
            });
        });
        
        // Écouter les événements d'aide
        document.addEventListener('arkalia:help_requested', (e) => {
            this.trackEvent('help_requested', {
                help_type: e.detail.helpType,
                context: e.detail.context
            });
        });
        
        document.addEventListener('arkalia:hint_used', (e) => {
            this.trackEvent('hint_used', {
                hint_id: e.detail.hintId,
                hint_type: e.detail.hintType,
                mission_id: e.detail.missionId
            });
        });
        
        // Écouter les erreurs
        document.addEventListener('arkalia:error_occurred', (e) => {
            this.trackEvent('error_occurred', {
                error_type: e.detail.errorType,
                error_message: e.detail.errorMessage,
                context: e.detail.context
            });
        });
        
        // Écouter les interactions
        document.addEventListener('arkalia:interaction', (e) => {
            this.trackEvent('interaction', {
                interaction_type: e.detail.interactionType,
                element: e.detail.element,
                value: e.detail.value
            });
        });
        
        // Écouter les événements de temps passé
        document.addEventListener('arkalia:time_spent', (e) => {
            this.trackEvent('time_spent', {
                activity: e.detail.activity,
                duration: e.detail.duration,
                session_duration: Date.now() - this.sessionStartTime
            });
        });
    }
    
    // Méthodes utilitaires pour tracker des événements spécifiques
    trackCommand(command, success = true, executionTime = 0) {
        this.trackEvent('command_executed', {
            command: command,
            success: success,
            execution_time: executionTime
        });
    }
    
    trackMissionStart(missionId, missionName, difficulty) {
        this.trackEvent('mission_start', {
            mission_id: missionId,
            mission_name: missionName,
            difficulty: difficulty
        });
    }
    
    trackMissionComplete(missionId, completionTime, score, hintsUsed = 0) {
        this.trackEvent('mission_complete', {
            mission_id: missionId,
            completion_time: completionTime,
            score: score,
            hints_used: hintsUsed
        });
    }
    
    trackGameStart(gameType, gameId, difficulty) {
        this.trackEvent('game_start', {
            game_type: gameType,
            game_id: gameId,
            difficulty: difficulty
        });
    }
    
    trackGameComplete(gameType, gameId, score, completionTime, perfectScore = false) {
        this.trackEvent('game_complete', {
            game_type: gameType,
            game_id: gameId,
            score: score,
            completion_time: completionTime,
            perfect_score: perfectScore
        });
    }
    
    trackBadgeEarned(badgeId, badgeName, badgeCategory) {
        this.trackEvent('badge_earned', {
            badge_id: badgeId,
            badge_name: badgeName,
            badge_category: badgeCategory
        });
    }
    
    trackEmotion(emotion, intensity, trigger) {
        this.trackEvent('emotion_triggered', {
            emotion: emotion,
            intensity: intensity,
            trigger: trigger
        });
    }
    
    trackError(errorType, errorMessage, context = {}) {
        this.trackEvent('error_occurred', {
            error_type: errorType,
            error_message: errorMessage,
            context: context
        });
    }
    
    trackInteraction(interactionType, element, value = null) {
        this.trackEvent('interaction', {
            interaction_type: interactionType,
            element: element,
            value: value
        });
    }
    
    trackTimeSpent(activity, duration) {
        this.trackEvent('time_spent', {
            activity: activity,
            duration: duration,
            session_duration: Date.now() - this.sessionStartTime
        });
    }
    
    // Méthodes pour obtenir des insights
    async getUserInsights() {
        try {
            const response = await fetch('/api/analytics/insights');
            if (response.ok) {
                return await response.json();
            }
            return null;
        } catch (error) {
            console.error('❌ Erreur lors de la récupération des insights:', error);
            return null;
        }
    }
    
    async getGlobalAnalytics() {
        try {
            const response = await fetch('/api/analytics/global');
            if (response.ok) {
                return await response.json();
            }
            return null;
        } catch (error) {
            console.error('❌ Erreur lors de la récupération des analytics globaux:', error);
            return null;
        }
    }
    
    // Méthodes de contrôle
    enable() {
        this.isEnabled = true;
        console.log('🔍 Analytics activé');
    }
    
    disable() {
        this.isEnabled = false;
        console.log('🔍 Analytics désactivé');
    }
    
    // Nettoyer à la fin de session
    endSession() {
        this.trackEvent('session_end', {
            session_id: this.sessionId,
            session_duration: Date.now() - this.sessionStartTime
        });
        
        // Flush final
        this.flushEvents();
        
        console.log('🔍 Session analytics terminée');
    }
}

// Classe pour afficher les insights dans le terminal
class AnalyticsDisplay {
    constructor(analyticsInterface) {
        this.analytics = analyticsInterface;
        this.terminal = window.terminal;
    }
    
    async showUserInsights() {
        const insights = await this.analytics.getUserInsights();
        if (!insights) {
            this.terminal.print('❌ Impossible de récupérer vos insights analytics', 'error');
            return;
        }
        
        this.terminal.print('\n📊 VOS INSIGHTS PERSONNALISÉS', 'info');
        this.terminal.print('=' * 50, 'info');
        
        // Statistiques générales
        this.terminal.print(`🎮 Sessions totales: ${insights.total_sessions}`, 'success');
        this.terminal.print(`⏱️ Temps de jeu total: ${insights.total_playtime_hours}h`, 'success');
        this.terminal.print(`📈 Taux d'engagement: ${insights.engagement_rate}%`, 'success');
        this.terminal.print(`🏆 Niveau actuel: ${insights.current_level}`, 'success');
        
        // Missions et jeux
        this.terminal.print(`🎯 Missions complétées: ${insights.missions_completed}`, 'info');
        this.terminal.print(`🎲 Jeux complétés: ${insights.games_completed}`, 'info');
        this.terminal.print(`🏅 Badges gagnés: ${insights.badges_earned}`, 'info');
        
        // Style d'apprentissage
        this.terminal.print(`🧠 Style d'apprentissage: ${this.formatLearningStyle(insights.learning_style)}`, 'warning');
        
        // Jeux préférés
        if (insights.preferred_games && insights.preferred_games.length > 0) {
            this.terminal.print(`🎮 Jeux préférés: ${insights.preferred_games.join(', ')}`, 'info');
        }
        
        // Dernière activité
        this.terminal.print(`🕐 Dernière activité: il y a ${insights.last_active_days} jours`, 'info');
        
        // Recommandations
        if (insights.recommendations && insights.recommendations.length > 0) {
            this.terminal.print('\n💡 RECOMMANDATIONS PERSONNALISÉES:', 'warning');
            insights.recommendations.forEach((rec, index) => {
                this.terminal.print(`${index + 1}. ${rec}`, 'info');
            });
        }
        
        this.terminal.print('=' * 50, 'info');
    }
    
    async showGlobalAnalytics() {
        const analytics = await this.analytics.getGlobalAnalytics();
        if (!analytics) {
            this.terminal.print('❌ Impossible de récupérer les analytics globaux', 'error');
            return;
        }
        
        this.terminal.print('\n🌍 ANALYTICS GLOBAUX ARKALIA QUEST', 'info');
        this.terminal.print('=' * 50, 'info');
        
        // Statistiques générales
        this.terminal.print(`👥 Utilisateurs totaux: ${analytics.total_users}`, 'success');
        this.terminal.print(`🎮 Sessions totales: ${analytics.total_sessions}`, 'success');
        this.terminal.print(`⏱️ Temps de jeu total: ${analytics.total_playtime_hours}h`, 'success');
        this.terminal.print(`📊 Temps moyen par utilisateur: ${analytics.avg_playtime_per_user}h`, 'success');
        
        // Sessions récentes
        this.terminal.print(`📈 Sessions (7 derniers jours): ${analytics.recent_sessions_7_days}`, 'info');
        
        // Métriques d'engagement
        if (analytics.engagement_metrics) {
            this.terminal.print('\n📊 MÉTRIQUES D\'ENGAGEMENT:', 'warning');
            this.terminal.print(`🔄 Taux de rétention (7j): ${analytics.engagement_metrics.retention_rate_7_days}%`, 'info');
            this.terminal.print(`✅ Taux de complétion missions: ${analytics.engagement_metrics.mission_completion_rate}%`, 'info');
            this.terminal.print(`⭐ Score d'engagement moyen: ${analytics.engagement_metrics.avg_engagement_score}/100`, 'info');
        }
        
        // Événements populaires
        if (analytics.popular_events) {
            this.terminal.print('\n🔥 ÉVÉNEMENTS POPULAIRES:', 'warning');
            Object.entries(analytics.popular_events).slice(0, 5).forEach(([event, count]) => {
                this.terminal.print(`• ${this.formatEventName(event)}: ${count}`, 'info');
            });
        }
        
        this.terminal.print('=' * 50, 'info');
    }
    
    formatLearningStyle(style) {
        const styles = {
            'guided_learner': 'Apprenant guidé (préfère les tutoriels)',
            'hands_on_learner': 'Apprenant pratique (préfère l\'expérimentation)',
            'support_seeker': 'Demandeur d\'aide (utilise indices et support)',
            'balanced_learner': 'Apprenant équilibré',
            'unknown': 'Non déterminé'
        };
        return styles[style] || style;
    }
    
    formatEventName(event) {
        const names = {
            'command_executed': 'Commandes exécutées',
            'mission_start': 'Missions démarrées',
            'mission_complete': 'Missions complétées',
            'game_start': 'Jeux démarrés',
            'game_complete': 'Jeux complétés',
            'tutorial_start': 'Tutoriels démarrés',
            'badge_earned': 'Badges gagnés',
            'session_start': 'Sessions démarrées'
        };
        return names[event] || event;
    }
}

// Initialisation globale
window.analyticsInterface = new AnalyticsInterface();
window.analyticsDisplay = new AnalyticsDisplay(window.analyticsInterface);

// Exposer les méthodes pour le terminal
window.analytics = {
    track: (eventType, data, context) => window.analyticsInterface.trackEvent(eventType, data, context),
    insights: () => window.analyticsDisplay.showUserInsights(),
    global: () => window.analyticsDisplay.showGlobalAnalytics(),
    enable: () => window.analyticsInterface.enable(),
    disable: () => window.analyticsInterface.disable()
};

console.log('🔍 Analytics Interface chargée et prête'); 