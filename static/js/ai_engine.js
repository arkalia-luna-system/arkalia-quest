/**
 * AI Engine - Moteur d'Intelligence Artificielle pour Arkalia Quest
 * Version 3.0 avec apprentissage automatique
 */

class AIEngine {
    constructor() {
        this.model = null;
        this.isInitialized = false;
        this.learningData = [];
        this.personalityModel = null;
        this.responsePatterns = {};
        
        // Initialiser l'IA
        this.init();
    }
    
    async init() {
        try {
            console.log("🤖 Initialisation de l'IA LUNA v3.0...");
            
            // Charger les données d'apprentissage
            await this.loadLearningData();
            
            // Initialiser le modèle de personnalité
            this.initPersonalityModel();
            
            // Charger les patterns de réponse
            this.loadResponsePatterns();
            
            this.isInitialized = true;
            console.log("✅ IA LUNA v3.0 initialisée avec succès");
            
        } catch (error) {
            console.error("❌ Erreur initialisation IA:", error);
            this.isInitialized = false;
        }
    }
    
    async loadLearningData() {
        try {
            // Charger les données d'apprentissage depuis le serveur
            const response = await fetch('/api/luna/learning-data');
            if (response.ok) {
                this.learningData = await response.json();
            } else {
                // Données par défaut si pas de serveur
                this.learningData = this.getDefaultLearningData();
            }
        } catch (error) {
            console.warn("⚠️ Impossible de charger les données d'apprentissage, utilisation des données par défaut");
            this.learningData = this.getDefaultLearningData();
        }
    }
    
    getDefaultLearningData() {
        return {
            "user_patterns": [
                {
                    "pattern": "speed_hack",
                    "personality_trait": "competitive",
                    "response_style": "encouraging",
                    "success_rate": 0.85
                },
                {
                    "pattern": "social_hack",
                    "personality_trait": "collaborative",
                    "response_style": "supportive",
                    "success_rate": 0.92
                },
                {
                    "pattern": "creative_hack",
                    "personality_trait": "innovative",
                    "response_style": "inspiring",
                    "success_rate": 0.78
                }
            ],
            "conversation_history": [],
            "preferences": {
                "humor_level": 0.7,
                "encouragement_level": 0.8,
                "challenge_level": 0.6
            }
        };
    }
    
    initPersonalityModel() {
        // Modèle de personnalité basé sur les actions du joueur
        this.personalityModel = {
            "traits": {
                "competitive": 0.5,
                "collaborative": 0.5,
                "innovative": 0.5,
                "analytical": 0.5,
                "social": 0.5
            },
            "learning_rate": 0.1,
            "adaptation_factor": 0.8
        };
    }
    
    loadResponsePatterns() {
        this.responsePatterns = {
            "success": {
                "competitive": [
                    "🔥 Incroyable ! Tu as battu le record !",
                    "⚡ Vitesse de hacker légendaire !",
                    "🏆 Tu es un vrai champion !"
                ],
                "collaborative": [
                    "🤝 Excellent travail d'équipe !",
                    "🌟 Tu as aidé tout le monde !",
                    "💪 Collaboration parfaite !"
                ],
                "innovative": [
                    "💡 Solution géniale ! Personne n'y avait pensé !",
                    "🎨 Créativité pure !",
                    "🚀 Innovation révolutionnaire !"
                ]
            },
            "failure": {
                "competitive": [
                    "😤 Ne t'inquiète pas, tu vas les écraser la prochaine fois !",
                    "💪 Un échec ? Juste un entraînement pour la victoire !",
                    "🔥 Tu vas revenir plus fort !"
                ],
                "collaborative": [
                    "🤝 On va s'entraider pour réussir !",
                    "🌟 Ensemble on est plus forts !",
                    "💪 L'échec nous rend plus sages !"
                ],
                "innovative": [
                    "💡 Chaque échec est une leçon !",
                    "🎨 L'échec nourrit la créativité !",
                    "🚀 L'innovation naît de l'échec !"
                ]
            },
            "encouragement": {
                "competitive": [
                    "⚡ Montre-leur qui est le boss !",
                    "🔥 Tu vas tout casser !",
                    "🏆 La victoire t'attend !"
                ],
                "collaborative": [
                    "🤝 On va réussir ensemble !",
                    "🌟 Tu as le soutien de toute l'équipe !",
                    "💪 Ensemble on peut tout faire !"
                ],
                "innovative": [
                    "💡 Pense différemment !",
                    "🎨 Utilise ta créativité !",
                    "🚀 Innove et révolutionne !"
                ]
            }
        };
    }
    
    analyzeUserAction(action, context = {}) {
        if (!this.isInitialized) {
            return this.getDefaultResponse();
        }
        
        // Analyser l'action de l'utilisateur
        const analysis = this.analyzeAction(action, context);
        
        // Mettre à jour le modèle de personnalité
        this.updatePersonalityModel(analysis);
        
        // Générer une réponse personnalisée
        return this.generatePersonalizedResponse(analysis);
    }
    
    analyzeAction(action, context) {
        const analysis = {
            "action_type": this.categorizeAction(action),
            "difficulty_level": this.assessDifficulty(action, context),
            "success_probability": this.predictSuccess(action, context),
            "personality_insights": this.extractPersonalityInsights(action),
            "learning_opportunity": this.identifyLearningOpportunity(action)
        };
        
        return analysis;
    }
    
    categorizeAction(action) {
        const actionPatterns = {
            "speed": ["kill_virus", "speed_hack", "turbo_hack", "flash_execute"],
            "social": ["luna_contact", "challenge_friend", "team_battle"],
            "creative": ["generer_meme", "easter_egg_1337", "meme_war"],
            "analytical": ["hack_system", "decode_portal", "analyze_virus"],
            "competitive": ["challenge_corp", "boss_final", "rebel_proof"]
        };
        
        for (const [category, patterns] of Object.entries(actionPatterns)) {
            if (patterns.includes(action)) {
                return category;
            }
        }
        
        return "general";
    }
    
    assessDifficulty(action, context) {
        const difficultyScores = {
            "kill_virus": 0.3,
            "speed_hack": 0.4,
            "hack_system": 0.6,
            "challenge_corp": 0.8,
            "boss_final": 0.9,
            "easter_egg_1337": 0.2
        };
        
        return difficultyScores[action] || 0.5;
    }
    
    predictSuccess(action, context) {
        // Basé sur l'historique et la difficulté
        const baseSuccessRate = 0.7;
        const difficultyFactor = this.assessDifficulty(action, context);
        const userLevel = context.userLevel || 1;
        
        return Math.min(0.95, baseSuccessRate + (userLevel * 0.05) - (difficultyFactor * 0.2));
    }
    
    extractPersonalityInsights(action) {
        const insights = {
            "risk_tolerance": 0.5,
            "creativity_level": 0.5,
            "social_preference": 0.5,
            "competitiveness": 0.5
        };
        
        // Ajuster selon l'action
        switch (this.categorizeAction(action)) {
            case "speed":
                insights.risk_tolerance += 0.2;
                insights.competitiveness += 0.3;
                break;
            case "social":
                insights.social_preference += 0.3;
                insights.risk_tolerance -= 0.1;
                break;
            case "creative":
                insights.creativity_level += 0.3;
                insights.risk_tolerance += 0.1;
                break;
            case "analytical":
                insights.risk_tolerance -= 0.1;
                insights.creativity_level -= 0.1;
                break;
            case "competitive":
                insights.competitiveness += 0.4;
                insights.risk_tolerance += 0.2;
                break;
        }
        
        return insights;
    }
    
    identifyLearningOpportunity(action) {
        const opportunities = {
            "skill_development": [],
            "knowledge_gap": [],
            "strategy_improvement": []
        };
        
        // Identifier les opportunités d'apprentissage
        if (action.includes("hack")) {
            opportunities.skill_development.push("technique_hacking");
        }
        if (action.includes("social")) {
            opportunities.skill_development.push("communication");
        }
        if (action.includes("creative")) {
            opportunities.skill_development.push("innovation");
        }
        
        return opportunities;
    }
    
    updatePersonalityModel(analysis) {
        const insights = analysis.personality_insights;
        const learningRate = this.personalityModel.learning_rate;
        
        // Mettre à jour les traits de personnalité
        this.personalityModel.traits.competitive = this.updateTrait(
            this.personalityModel.traits.competitive,
            insights.competitiveness,
            learningRate
        );
        
        this.personalityModel.traits.collaborative = this.updateTrait(
            this.personalityModel.traits.collaborative,
            insights.social_preference,
            learningRate
        );
        
        this.personalityModel.traits.innovative = this.updateTrait(
            this.personalityModel.traits.innovative,
            insights.creativity_level,
            learningRate
        );
    }
    
    updateTrait(currentValue, newValue, learningRate) {
        return currentValue + (learningRate * (newValue - currentValue));
    }
    
    generatePersonalizedResponse(analysis) {
        const dominantTrait = this.getDominantTrait();
        const responseType = this.determineResponseType(analysis);
        const responsePool = this.responsePatterns[responseType][dominantTrait] || 
                           this.responsePatterns[responseType]["competitive"];
        
        // Sélectionner une réponse aléatoire
        const response = responsePool[Math.floor(Math.random() * responsePool.length)];
        
        return {
            "message": response,
            "personality_trait": dominantTrait,
            "confidence": analysis.success_probability,
            "learning_insights": analysis.learning_opportunity,
            "next_recommendation": this.generateRecommendation(analysis)
        };
    }
    
    getDominantTrait() {
        const traits = this.personalityModel.traits;
        let dominantTrait = "competitive";
        let maxValue = traits.competitive;
        
        for (const [trait, value] of Object.entries(traits)) {
            if (value > maxValue) {
                maxValue = value;
                dominantTrait = trait;
            }
        }
        
        return dominantTrait;
    }
    
    determineResponseType(analysis) {
        if (analysis.success_probability > 0.8) {
            return "success";
        } else if (analysis.success_probability < 0.3) {
            return "failure";
        } else {
            return "encouragement";
        }
    }
    
    generateRecommendation(analysis) {
        const recommendations = {
            "speed": "Essaie une mission plus difficile pour tester tes limites !",
            "social": "Invite un ami pour un défi d'équipe !",
            "creative": "Crée ton propre meme ou easter egg !",
            "analytical": "Analyse les patterns pour optimiser tes stratégies !",
            "competitive": "Défie le boss final pour prouver ta valeur !"
        };
        
        return recommendations[analysis.action_type] || "Continue d'explorer et d'apprendre !";
    }
    
    getDefaultResponse() {
        return {
            "message": "🌙 LUNA : Salut rebelle ! Prêt à casser du code ?",
            "personality_trait": "competitive",
            "confidence": 0.5,
            "learning_insights": {},
            "next_recommendation": "Commence par explorer les commandes de base !"
        };
    }
    
    // Méthodes pour l'apprentissage automatique avancé
    async trainModel(trainingData) {
        console.log("🤖 Entraînement du modèle IA...");
        
        // Simulation d'entraînement
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        console.log("✅ Modèle entraîné avec succès");
        return true;
    }
    
    async predictUserBehavior(userActions) {
        // Prédire le comportement futur de l'utilisateur
        const predictions = {
            "next_likely_action": this.predictNextAction(userActions),
            "success_probability": this.calculateSuccessProbability(userActions),
            "engagement_level": this.assessEngagement(userActions)
        };
        
        return predictions;
    }
    
    predictNextAction(userActions) {
        const actionCounts = {};
        userActions.forEach(action => {
            actionCounts[action] = (actionCounts[action] || 0) + 1;
        });
        
        // Trouver l'action la plus fréquente
        let mostLikelyAction = "aide";
        let maxCount = 0;
        
        for (const [action, count] of Object.entries(actionCounts)) {
            if (count > maxCount) {
                maxCount = count;
                mostLikelyAction = action;
            }
        }
        
        return mostLikelyAction;
    }
    
    calculateSuccessProbability(userActions) {
        // Calculer la probabilité de succès basée sur l'historique
        const recentActions = userActions.slice(-5);
        const successRate = recentActions.filter(action => 
            ["kill_virus", "hack_system", "easter_egg_1337"].includes(action)
        ).length / recentActions.length;
        
        return Math.max(0.1, Math.min(0.9, successRate));
    }
    
    assessEngagement(userActions) {
        // Évaluer le niveau d'engagement de l'utilisateur
        const uniqueActions = new Set(userActions).size;
        const totalActions = userActions.length;
        
        if (totalActions === 0) return 0.5;
        
        const diversityScore = uniqueActions / totalActions;
        const frequencyScore = Math.min(1, totalActions / 10);
        
        return (diversityScore + frequencyScore) / 2;
    }
}

// Instance globale
window.aiEngine = new AIEngine();

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIEngine;
} 