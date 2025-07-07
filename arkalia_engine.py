#!/usr/bin/env python3
"""
Arkalia Engine - Module unifié pour Arkalia Quest
Fusionne les meilleures fonctionnalités des modules existants :
- IA LUNA (engines/luna_ai.py, utils/luna_ai_v2.py)
- Analyse de personnalité (mission_utils/personality_engine.py)
- Gestion des missions (core/game_engine.py, core/command_handler.py)
- Logger simple (utils/logger.py)
"""

import json
import random
import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from collections import defaultdict, Counter

# ============================================================================
# LOGGER SIMPLE
# ============================================================================

class ArkaliaLogger:
    """Logger simple pour Arkalia Quest"""
    
    def __init__(self, name="arkalia"):
        self.name = name
        self.log_file = "logs/arkalia.log"
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """Crée le dossier logs s'il n'existe pas"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
    
    def info(self, message: str):
        """Log un message d'information"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] INFO [{self.name}] {message}"
        print(f"🌙 {message}")
        self._write_log(log_entry)
    
    def warning(self, message: str):
        """Log un avertissement"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] WARNING [{self.name}] {message}"
        print(f"⚠️ {message}")
        self._write_log(log_entry)
    
    def error(self, message: str):
        """Log une erreur"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] ERROR [{self.name}] {message}"
        print(f"❌ {message}")
        self._write_log(log_entry)
    
    def _write_log(self, entry: str):
        """Écrit dans le fichier de log"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(entry + "\n")
        except Exception as e:
            print(f"Erreur d'écriture du log: {e}")

# ============================================================================
# IA LUNA v3.0 - AVEC APPRENTISSAGE AUTOMATIQUE
# ============================================================================

class LunaAI:
    """IA LUNA v3.0 avec apprentissage automatique des préférences"""
    
    def __init__(self):
        self.logger = ArkaliaLogger("luna")
        self.personality_data = self._load_personality_data()
        self.responses = self._load_responses()
        self.learning_data = self._load_learning_data()
        self.command_patterns = defaultdict(Counter)
        self.response_effectiveness = defaultdict(lambda: {"success": 0, "total": 0})
        self.logger.info("IA LUNA v3.0 initialisée avec apprentissage automatique")
    
    def _load_personality_data(self) -> Dict[str, Any]:
        """Charge les données de personnalité"""
        try:
            with open("data/personality_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "traits": ["curieux", "analytique", "créatif", "social"],
                "types": ["explorateur", "stratège", "artiste", "communicateur"]
            }
    
    def _load_responses(self) -> Dict[str, List[str]]:
        """Charge les réponses de LUNA - VERSION REBELLE"""
        return {
            "greetings": [
                "🌙 Salut rebelle ! LUNA v3.0 en ligne. Prêt à casser du code ?",
                "🌙 Interface LUNA v3.0 activée. Apprentissage en cours...",
                "🌙 Bienvenue dans le système. LUNA v3.0 en ligne avec IA adaptative."
            ],
            "thinking": [
                "🤔 Analyse en cours...",
                "🧠 Traitement des données...",
                "⚡ Calculs en cours...",
                "🔍 Analyse des patterns utilisateur..."
            ],
            "success": [
                "✅ Opération réussie !",
                "🎯 Objectif atteint !",
                "🌟 Excellent travail !",
                "🚀 Performance optimale détectée !"
            ],
            "error": [
                "❌ Erreur détectée.",
                "⚠️ Attention, problème identifié.",
                "🚨 Alerte système.",
                "🔧 Correction automatique en cours..."
            ],
            "learning": [
                "🧠 Apprentissage en cours...",
                "📊 Analyse des préférences...",
                "🎯 Adaptation aux patterns...",
                "⚡ Optimisation des réponses..."
            ],
            # NOUVELLES RÉPONSES REBELLES
            "rebel_success": [
                "🔥 OK t'es un dieu. SHADOW-13 va chier dans son clavier.",
                "💪 Pas mal pour un noob ! Tu progresses bien.",
                "🚀 Allez, t'es pas si nul que ça finalement !",
                "⚡ Wow, même ma grand-mère hacke pas aussi bien !"
            ],
            "rebel_failure": [
                "😅 T'es nul ou tu le fais exprès ? Même un bot fait mieux !",
                "🤦‍♂️ Même ma grand-mère hacke mieux que ça !",
                "😤 Allez, concentre-toi ! Tu peux faire mieux.",
                "🤷‍♂️ Bon, on va dire que c'était un test..."
            ],
            "rebel_challenge": [
                "⏰ 10 secondes ou ton historique meurt ! VITE !",
                "🚨 La Corp te piste ! Tape 'kill_virus' MAINTENANT !",
                "💀 SHADOW-13 a volé tes memes ! Trouve-le en 15s !",
                "🔥 Défi urgent : 'hack_system' en moins de 8 secondes !"
            ],
            "rebel_insult": [
                "😏 T'es un chicken ou tu vas oser ?",
                "🤪 Allez, montre-moi ce que tu sais faire, noob !",
                "😎 Tu vas craquer ou tu vas hacker ?",
                "🤡 Même un script kiddie fait mieux que ça !"
            ]
        }
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Charge les données d'apprentissage"""
        try:
            with open("data/learning_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "command_patterns": {},
                "response_effectiveness": {},
                "user_preferences": {},
                "learning_history": []
            }
    
    def _save_learning_data(self):
        """Sauvegarde les données d'apprentissage"""
        learning_data = {
            "command_patterns": dict(self.command_patterns),
            "response_effectiveness": dict(self.response_effectiveness),
            "user_preferences": self._extract_user_preferences(),
            "learning_history": self.learning_data.get("learning_history", [])
        }
        
        try:
            with open("data/learning_data.json", "w", encoding="utf-8") as f:
                json.dump(learning_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde données d'apprentissage: {e}")
    
    def learn_from_command(self, commande: str, context: str, user_reaction: str = "neutral"):
        """Apprend des commandes utilisateur"""
        # Analyse du pattern de commande
        self.command_patterns[context][commande] += 1
        
        # Analyse de l'efficacité des réponses
        if context in self.response_effectiveness:
            self.response_effectiveness[context]["total"] += 1
            if user_reaction in ["positive", "success", "good"]:
                self.response_effectiveness[context]["success"] += 1
        
        # Sauvegarde périodique
        if random.random() < 0.1:  # 10% de chance de sauvegarder
            self._save_learning_data()
    
    def _extract_user_preferences(self) -> Dict[str, Any]:
        """Extrait les préférences utilisateur des patterns"""
        preferences = {
            "favorite_commands": {},
            "command_frequency": {},
            "context_preferences": {},
            "response_style": "balanced"
        }
        
        # Commandes préférées par contexte
        for context, patterns in self.command_patterns.items():
            if patterns:
                most_common = patterns.most_common(3)
                preferences["favorite_commands"][context] = [cmd for cmd, _ in most_common]
                preferences["command_frequency"][context] = sum(patterns.values())
        
        # Style de réponse préféré
        success_rates = {}
        for context, stats in self.response_effectiveness.items():
            if stats["total"] > 0:
                success_rates[context] = stats["success"] / stats["total"]
        
        if success_rates:
            avg_success = sum(success_rates.values()) / len(success_rates)
            if avg_success > 0.7:
                preferences["response_style"] = "detailed"
            elif avg_success < 0.3:
                preferences["response_style"] = "simple"
        
        return preferences
    
    def generate_response(self, context: str, user_input: str = "", personality_type: str = "explorateur") -> str:
        """Génère une réponse contextuelle adaptative de LUNA v3.0"""
        self.logger.info(f"Génération de réponse adaptative pour: {context}")
        
        # Apprentissage de la commande
        self.learn_from_command(user_input, context)
        
        # Analyse des préférences utilisateur
        preferences = self._extract_user_preferences()
        response_style = preferences.get("response_style", "balanced")
        
        # Réponses contextuelles avec adaptation REBELLE
        if "commande" in context.lower():
            responses = [
                "🌙 Commande reçue et traitée avec optimisation IA.",
                "⚡ Exécution en cours avec analyse des patterns...",
                "🔧 Traitement de la commande avec apprentissage..."
            ]
            if response_style == "detailed":
                responses.extend([
                    "🌙 Commande analysée. Pattern détecté et optimisé.",
                    "⚡ Exécution intelligente basée sur vos préférences..."
                ])
            # Ajouter réponses rebelles
            if random.random() < 0.3:  # 30% de chance d'être rebelle
                responses.extend(self.responses["rebel_challenge"])
        
        elif "mission" in context.lower():
            responses = [
                "🎯 Mission analysée et adaptée à votre profil.",
                "📋 Détails de mission chargés avec personnalisation.",
                "🚀 Préparation de mission optimisée pour votre style..."
            ]
            if response_style == "detailed":
                responses.extend([
                    "🎯 Mission analysée selon vos patterns de jeu.",
                    "📋 Chargement avec recommandations personnalisées..."
                ])
            # Ajouter défis urgents
            if random.random() < 0.4:  # 40% de chance d'urgence
                responses.extend(self.responses["rebel_challenge"])
        
        elif "profil" in context.lower():
            responses = [
                "👤 Profil utilisateur consulté avec analyse IA.",
                "📊 Données de profil affichées avec insights.",
                "🔍 Analyse de profil terminée avec recommandations..."
            ]
            if response_style == "detailed":
                responses.extend([
                    "👤 Profil analysé avec apprentissage automatique.",
                    "📊 Affichage optimisé selon vos préférences..."
                ])
        
        elif "erreur" in context.lower():
            responses = self.responses["error"]
            if response_style == "detailed":
                responses.extend([
                    "🔧 Correction automatique basée sur l'historique...",
                    "🛠️ Solution adaptée à votre style de résolution..."
                ])
            # Ajouter insultes amicales en cas d'erreur
            responses.extend(self.responses["rebel_failure"])
        
        elif "succès" in context.lower():
            responses = self.responses["success"]
            if response_style == "detailed":
                responses.extend([
                    "🚀 Performance optimale selon vos patterns !",
                    "🌟 Excellence détectée dans votre approche !"
                ])
            # Ajouter compliments rebelles
            responses.extend(self.responses["rebel_success"])
        
        elif "apprentissage" in context.lower() or "learning" in context.lower():
            responses = self.responses["learning"]
            if response_style == "detailed":
                responses.extend([
                    "🧠 Analyse approfondie de vos préférences...",
                    "📊 Optimisation continue des réponses IA..."
                ])
        
        else:
            responses = self.responses["greetings"]
            if response_style == "detailed":
                responses.extend([
                    "🌙 LUNA v3.0 prêt avec apprentissage automatique.",
                    "🧠 IA adaptative activée selon vos patterns..."
                ])
            # Ajouter insultes amicales aléatoires
            if random.random() < 0.2:  # 20% de chance
                responses.extend(self.responses["rebel_insult"])
        
        return random.choice(responses)
    
    def analyze_personality(self, profil: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse la personnalité du joueur avec apprentissage"""
        self.logger.info("Analyse de personnalité avancée en cours...")
        
        # Analyse basée sur les commandes utilisées
        commandes_utilisees = profil.get("commandes_utilisees", [])
        
        # Analyse des patterns d'apprentissage
        learning_patterns = self._extract_user_preferences()
        
        # Scores par type de personnalité
        score_creatif = sum(1 for cmd in commandes_utilisees if cmd in ["créer", "inventer", "design", "art"])
        score_analytique = sum(1 for cmd in commandes_utilisees if cmd in ["analyser", "débugger", "tester", "vérifier"])
        score_social = sum(1 for cmd in commandes_utilisees if cmd in ["partager", "aider", "collaborer", "communiquer"])
        score_explorateur = sum(1 for cmd in commandes_utilisees if cmd in ["explorer", "découvrir", "naviguer", "chercher"])
        
        # Bonus basé sur les patterns d'apprentissage
        if learning_patterns.get("response_style") == "detailed":
            score_analytique += 2
        if any("mission" in cmd for cmd in learning_patterns.get("favorite_commands", {}).get("mission", [])):
            score_explorateur += 1
        
        # Détermination du type dominant
        scores = {
            "créatif": score_creatif,
            "analytique": score_analytique,
            "social": score_social,
            "explorateur": score_explorateur
        }
        
        type_dominant = max(scores.items(), key=lambda x: x[1])[0]
        
        # Traits associés
        traits = []
        if score_creatif > 2:
            traits.append("créatif")
        if score_analytique > 2:
            traits.append("analytique")
        if score_social > 2:
            traits.append("social")
        if score_explorateur > 2:
            traits.append("explorateur")
        
        if not traits:
            traits = ["curieux"]
        
        # Insights d'apprentissage
        learning_insights = {
            "patterns_détectés": len(learning_patterns.get("favorite_commands", {})),
            "style_réponse": learning_patterns.get("response_style", "balanced"),
            "fréquence_commandes": sum(learning_patterns.get("command_frequency", {}).values())
        }
        
        return {
            "type": type_dominant,
            "traits": traits,
            "scores": scores,
            "learning_insights": learning_insights,
            "description": f"Joueur de type {type_dominant} avec apprentissage IA avancé",
            "recommandations": self._generate_recommendations(scores, learning_patterns)
        }
    
    def _generate_recommendations(self, scores: Dict[str, int], learning_patterns: Dict[str, Any]) -> List[str]:
        """Génère des recommandations personnalisées"""
        recommendations = []
        
        # Recommandations basées sur les scores
        if scores["créatif"] > 3:
            recommendations.append("🎨 Explorez les missions créatives et artistiques")
        if scores["analytique"] > 3:
            recommendations.append("🔍 Concentrez-vous sur les missions d'analyse et de debug")
        if scores["social"] > 3:
            recommendations.append("🤝 Participez aux missions collaboratives")
        if scores["explorateur"] > 3:
            recommendations.append("🗺️ Découvrez de nouvelles zones et missions")
        
        # Recommandations basées sur l'apprentissage
        if learning_patterns.get("response_style") == "detailed":
            recommendations.append("🧠 Utilisez des commandes complexes pour des réponses détaillées")
        else:
            recommendations.append("⚡ Utilisez des commandes simples pour des réponses rapides")
        
        if not recommendations:
            recommendations.append("🌟 Explorez différents types de missions pour découvrir votre style")
        
        return recommendations

# ============================================================================
# GESTIONNAIRE DE MISSIONS
# ============================================================================

class MissionManager:
    """Gestionnaire de missions unifié"""
    
    def __init__(self):
        self.logger = ArkaliaLogger("missions")
        self.missions_dir = Path("missions")
        self.bonus_missions_dir = Path("data/missions")
        self.logger.info("Gestionnaire de missions initialisé")
    
    def load_mission(self, mission_name: str) -> Optional[Dict[str, Any]]:
        """Charge une mission par son nom"""
        # Cherche d'abord dans les missions actives
        mission_file = self.missions_dir / f"{mission_name}.json"
        if mission_file.exists():
            try:
                with open(mission_file, "r", encoding="utf-8") as f:
                    mission = json.load(f)
                self.logger.info(f"Mission chargée: {mission_name}")
                return mission
            except Exception as e:
                self.logger.error(f"Erreur chargement mission {mission_name}: {e}")
                return None
        
        # Cherche dans les missions bonus
        bonus_mission_file = self.bonus_missions_dir / f"{mission_name}.json"
        if bonus_mission_file.exists():
            try:
                with open(bonus_mission_file, "r", encoding="utf-8") as f:
                    mission = json.load(f)
                self.logger.info(f"Mission bonus chargée: {mission_name}")
                return mission
            except Exception as e:
                self.logger.error(f"Erreur chargement mission bonus {mission_name}: {e}")
                return None
        
        self.logger.warning(f"Mission non trouvée: {mission_name}")
        return None
    
    def list_available_missions(self) -> Dict[str, List[str]]:
        """Liste toutes les missions disponibles"""
        missions: Dict[str, List[str]] = {
            "actives": [],
            "bonus": []
        }
        
        # Missions actives
        if self.missions_dir.exists():
            for file in self.missions_dir.glob("*.json"):
                missions["actives"].append(file.stem)
        
        # Missions bonus
        if self.bonus_missions_dir.exists():
            for file in self.bonus_missions_dir.glob("*.json"):
                missions["bonus"].append(file.stem)
        
        self.logger.info(f"Missions disponibles: {len(missions['actives'])} actives, {len(missions['bonus'])} bonus")
        return missions
    
    def generate_personalized_mission(self, profil: Dict[str, Any]) -> Dict[str, Any]:
        """Génère une mission personnalisée selon le profil"""
        personality = profil.get("personnalite", {})
        type_personnalite = personality.get("type", "explorateur")
        
        # Missions selon le type de personnalité
        mission_templates = {
            "créatif": {
                "titre": "Création Artistique Digitale",
                "description": "Créez une œuvre d'art numérique unique",
                "objectifs": ["Utiliser des outils créatifs", "Créer quelque chose d'original"],
                "difficulté": "moyenne"
            },
            "analytique": {
                "titre": "Analyse de Données",
                "description": "Analysez et interprétez des données complexes",
                "objectifs": ["Analyser des patterns", "Tirer des conclusions"],
                "difficulté": "élevée"
            },
            "social": {
                "titre": "Collaboration en Réseau",
                "description": "Collaborez avec d'autres joueurs",
                "objectifs": ["Partager des informations", "Aider les autres"],
                "difficulté": "facile"
            },
            "explorateur": {
                "titre": "Exploration de Nouveaux Territoires",
                "description": "Découvrez de nouvelles zones du système",
                "objectifs": ["Explorer des zones inconnues", "Découvrir des secrets"],
                "difficulté": "moyenne"
            }
        }
        
        template = mission_templates.get(type_personnalite, mission_templates["explorateur"])
        
        return {
            "id": f"perso_{int(time.time())}",
            "titre": template["titre"],
            "description": template["description"],
            "objectifs": template["objectifs"],
            "difficulté": template["difficulté"],
            "type": "personnalisée",
            "créée_le": datetime.now().isoformat()
        }

# ============================================================================
# GESTIONNAIRE DE PROFILS
# ============================================================================

class ProfileManager:
    """Gestionnaire de profils unifié"""
    
    def __init__(self):
        self.logger = ArkaliaLogger("profiles")
        self.profiles_dir = Path("data/profiles")
        self.main_profile_path = Path("data/profil_joueur.json")
        self.logger.info("Gestionnaire de profils initialisé")
    
    def load_main_profile(self) -> Dict[str, Any]:
        """Charge le profil principal"""
        try:
            if self.main_profile_path.exists():
                with open(self.main_profile_path, "r", encoding="utf-8") as f:
                    profil = json.load(f)
                self.logger.info("Profil principal chargé")
                return profil
            else:
                self.logger.warning("Profil principal non trouvé, création d'un nouveau")
                return self.create_default_profile()
        except Exception as e:
            self.logger.error(f"Erreur chargement profil principal: {e}")
            return self.create_default_profile()
    
    def save_main_profile(self, profil: Dict[str, Any]):
        """Sauvegarde le profil principal"""
        try:
            with open(self.main_profile_path, "w", encoding="utf-8") as f:
                json.dump(profil, f, indent=2, ensure_ascii=False)
            self.logger.info("Profil principal sauvegardé")
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde profil principal: {e}")
    
    def create_default_profile(self) -> Dict[str, Any]:
        """Crée un profil par défaut"""
        return {
            "nom": "Joueur",
            "niveau": 1,
            "score": 0,
            "badges": [],
            "commandes_utilisees": [],
            "missions_completees": [],
            "portails_ouverts": [],
            "personnalite": {
                "type": "explorateur",
                "traits": ["curieux"],
                "scores": {"créatif": 0, "analytique": 0, "social": 0, "explorateur": 0}
            },
            "derniere_connexion": datetime.now().isoformat(),
            "créé_le": datetime.now().isoformat()
        }
    
    def list_backup_profiles(self) -> List[str]:
        """Liste les profils de sauvegarde"""
        if not self.profiles_dir.exists():
            return []
        
        profiles = []
        for file in self.profiles_dir.glob("*.json"):
            profiles.append(file.stem)
        
        self.logger.info(f"Profils de sauvegarde trouvés: {len(profiles)}")
        return profiles
    
    def backup_current_profile(self, profil: Dict[str, Any]):
        """Crée une sauvegarde du profil actuel"""
        if not self.profiles_dir.exists():
            self.profiles_dir.mkdir(parents=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.profiles_dir / f"user_{timestamp}.json"
        
        try:
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(profil, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Sauvegarde créée: {backup_file.name}")
        except Exception as e:
            self.logger.error(f"Erreur création sauvegarde: {e}")

# ============================================================================
# MOTEUR PRINCIPAL ARKALIA
# ============================================================================

class ArkaliaEngine:
    """Moteur principal unifié d'Arkalia Quest"""
    
    def __init__(self):
        self.logger = ArkaliaLogger("engine")
        self.luna = LunaAI()
        self.missions = MissionManager()
        self.profiles = ProfileManager()
        self.logger.info("Moteur Arkalia initialisé")
    
    def process_command(self, commande: str, profil: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une commande et retourne la réponse"""
        self.logger.info(f"Traitement commande: {commande}")
        
        # Ajouter la commande à l'historique
        if "commandes_utilisees" not in profil:
            profil["commandes_utilisees"] = []
        profil["commandes_utilisees"].append(commande)
        
        # Analyser la personnalité si nécessaire
        if len(profil["commandes_utilisees"]) % 5 == 0:  # Tous les 5 commandes
            profil["personnalite"] = self.luna.analyze_personality(profil)
        
        # Traitement des commandes
        commande_lower = commande.lower().strip()
        
        # Nouvelles commandes d'apprentissage LUNA v3.0
        if commande_lower == "luna_learning":
            return {
                "reponse": self.luna.generate_response("apprentissage", commande),
                "type": "info",
                "donnees": {
                    "learning_data": self.luna._extract_user_preferences(),
                    "patterns": dict(self.luna.command_patterns),
                    "effectiveness": dict(self.luna.response_effectiveness)
                }
            }
        
        elif commande_lower == "luna_analyze":
            personality = self.luna.analyze_personality(profil)
            return {
                "reponse": f"🧠 Analyse de personnalité avancée terminée. Type: {personality['type']}",
                "type": "info",
                "donnees": {
                    "personality": personality,
                    "learning_insights": personality.get("learning_insights", {}),
                    "recommandations": personality.get("recommandations", [])
                }
            }
        
        elif commande_lower == "luna_preferences":
            preferences = self.luna._extract_user_preferences()
            return {
                "reponse": f"📊 Préférences utilisateur analysées. Style: {preferences.get('response_style', 'balanced')}",
                "type": "info",
                "donnees": {
                    "preferences": preferences,
                    "favorite_commands": preferences.get("favorite_commands", {}),
                    "command_frequency": preferences.get("command_frequency", {})
                }
            }
        
        elif commande_lower == "luna_reset":
            self.luna.command_patterns.clear()
            self.luna.response_effectiveness.clear()
            self.luna._save_learning_data()
            return {
                "reponse": "🔄 Données d'apprentissage réinitialisées. LUNA v3.0 repart de zéro.",
                "type": "success"
            }
        
        elif commande_lower == "luna_engine":
            return {
                "reponse": self.luna.generate_response("commande", commande),
                "type": "info",
                "donnees": {
                    "version": "LUNA v3.0",
                    "features": [
                        "Apprentissage automatique des préférences",
                        "Analyse des patterns de commandes",
                        "Adaptation des réponses",
                        "Génération de recommandations personnalisées"
                    ],
                    "status": "Actif avec IA adaptative"
                }
            }
        
        # Commandes existantes
        elif commande_lower == "missions_bonus":
            missions = self.missions.list_available_missions()
            return {
                "reponse": f"📋 Missions bonus disponibles: {len(missions['bonus'])}",
                "type": "info",
                "donnees": {
                    "missions_bonus": missions["bonus"],
                    "total_missions": len(missions["actives"]) + len(missions["bonus"])
                }
            }
        
        elif commande_lower == "scan_persona":
            personality = self.luna.analyze_personality(profil)
            return {
                "reponse": f"🔍 Scan de personnalité: {personality['description']}",
                "type": "info",
                "donnees": {
                    "personality": personality,
                    "traits": personality.get("traits", []),
                    "scores": personality.get("scores", {})
                }
            }
        
        elif commande_lower == "help" or commande_lower == "aide":
            return {
                "reponse": "📚 Commandes disponibles:\n" +
                          "• luna_engine - Active le moteur LUNA v3.0\n" +
                          "• luna_learning - Affiche les données d'apprentissage\n" +
                          "• luna_analyze - Analyse de personnalité avancée\n" +
                          "• luna_preferences - Affiche vos préférences\n" +
                          "• luna_reset - Réinitialise l'apprentissage\n" +
                          "• missions_bonus - Liste les missions bonus\n" +
                          "• scan_persona - Analyse votre personnalité",
                "type": "help"
            }
        
        else:
            # Commande non reconnue
            return {
                "reponse": self.luna.generate_response("commande", commande),
                "type": "unknown"
            }
    
    def get_mission_info(self, mission_name: str) -> Dict[str, Any]:
        """Récupère les informations d'une mission"""
        mission = self.missions.load_mission(mission_name)
        if mission:
            return {
                "success": True,
                "mission": mission,
                "message": self.luna.generate_response("mission")
            }
        else:
            return {
                "success": False,
                "message": "Mission non trouvée"
            }
    
    def get_profile_summary(self, profil: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un résumé du profil"""
        personality = profil.get("personnalite", {})
        type_personnalite = personality.get("type", "explorateur")
        
        return {
            "nom": profil.get("nom", "Joueur"),
            "niveau": profil.get("niveau", 1),
            "score": profil.get("score", 0),
            "badges": profil.get("badges", []),
            "type_personnalite": type_personnalite,
            "traits": personality.get("traits", []),
            "missions_completees": len(profil.get("missions_completees", [])),
            "portails_ouverts": len(profil.get("portails_ouverts", [])),
            "message": self.luna.generate_response("profil")
        }
    
    def get_available_content(self) -> Dict[str, Any]:
        """Récupère tout le contenu disponible"""
        missions = self.missions.list_available_missions()
        backup_profiles = self.profiles.list_backup_profiles()
        
        return {
            "missions_actives": missions["actives"],
            "missions_bonus": missions["bonus"],
            "profils_sauvegarde": backup_profiles,
            "message": "Contenu disponible récupéré"
        }

# Instance globale
arkalia_engine = ArkaliaEngine() 