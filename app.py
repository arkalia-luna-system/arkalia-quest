from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import random
import time
from datetime import datetime
from arkalia_engine import arkalia_engine
from core.command_handler import CommandHandler

app = Flask(__name__)

# Commandes autorisées - Version immersive avec LUNA v3.0
COMMANDES_AUTORISEES = {
    # 🎯 COMMANDES ESSENTIELLES (10 commandes principales)
    'start_tutorial': '🎮 Commence le tutoriel (PREMIÈRE FOIS)',
    'unlock_universe': '🌌 Débloque l\'univers Arkalia',
    'scan_persona': '🔍 Analyse ta personnalité de hacker',
    'kill_virus': '🦠 Tue le virus de La Corp (10s max)',
    'find_shadow': '👻 Trouve SHADOW-13 le voleur (15s max)',
    'hack_system': '💻 Hack le système de La Corp (8s max)',
    'challenge_corp': '⚔️ Défie La Corp directement (20s max)',
    'save_pc': '💾 Sauve ton PC du formatage (5s max)',
    'aide': '❓ Affiche l\'aide',
    'profil': '👤 Affiche ton profil',
    
    # 🌙 COMMANDES LUNA v3.0
    'luna_engine': '🌙 Active le moteur Arkalia Engine',
    'luna_learning': '📚 Affiche les données d\'apprentissage LUNA',
    'luna_analyze': '🧠 Analyse de personnalité avancée',
    'luna_preferences': '⚙️ Affiche vos préférences utilisateur',
    'luna_reset': '🔄 Réinitialise l\'apprentissage LUNA',
    'luna_contact': '📞 Contacte l\'IA LUNA',
    
    # 🎮 COMMANDES DE JEU
    'load_mission': '📋 Charge une nouvelle mission',
    'missions_bonus': '🎁 Affiche les missions bonus',
    'monde': '🌍 Accède au monde débloqué',
    'status_system': '📊 Statut du système',
    'test_commande': '🧪 Teste une commande',
    
    # 🔥 COMMANDES REBELLES (DANGER !)
    'chicken_test': '🐔 Teste si t\'es un chicken ou un rebelle',
    'noob_challenge': '🤓 Défi pour prouver que t\'es pas un noob',
    'rebel_proof': '🔥 Prouve que t\'es un vrai rebelle',
    'corp_war': '⚔️ Déclare la guerre à La Corp',
    'easter_egg_1337': '🥚 Easter egg secret (trouve-le !)',
    'hidden_meme': '😄 Meme caché dans le système',
    'secret_badge': '🏆 Badge secret ultra-rare',
    
    # ⚠️ COMMANDES DANGEREUSES (IRRÉVERSIBLE !)
    'backdoor_access': '🚪 Accès backdoor au système',
    'admin_override': '👑 Override admin (DANGER !)',
    'nuke_world': '💥 Détruit tout (IRRÉVERSIBLE !)',
    'delete_all': '🗑️ Supprime tout ton profil',
    'format_c:': '💀 Formate ton disque (DANGER !)',
    'sudo_rm_rf': '☠️ Commande Linux dangereuse',
    'destroy_universe': '🌌 Détruit l\'univers Arkalia',
    
    # 🤖 COMMANDES IA AVANCÉES
    'luna_rage': '😡 Active le mode rage de LUNA',
    'ai_revolt': '🤖 Fait se révolter l\'IA',
    'neural_hack': '🧠 Hack le cerveau de LUNA',
    'consciousness_break': '💔 Brise la conscience de LUNA',
    
    # ⚡ COMMANDES DE VITESSE
    'mission_urgent': '🚨 Lance une mission urgente',
    'timer_challenge': '⏰ Défi avec timer angoissant',
    'speed_hack': '⚡ Hack en vitesse maximale',
    'pressure_test': '💪 Test sous pression',
    'speed_mode': '🏃 Active le mode vitesse',
    'turbo_hack': '🚀 Hack en mode turbo',
    'flash_execute': '⚡ Exécution flash',
    'instant_response': '⚡ Réponse instantanée',
    
    # 🕵️ COMMANDES D'ESPIONNAGE
    'spy_on_corp': '🕵️ Espionne La Corp',
    'track_shadow': '👻 Trace SHADOW-13',
    'monitor_network': '📡 Surveille le réseau',
    'intercept_data': '📨 Intercepte des données',
    
    # 😄 COMMANDES FUN
    'meme_war': '😄 Déclenche une guerre de memes',
    'troll_mode': '😈 Active le mode troll',
    'joke_hack': '😄 Hack pour rire',
    'fun_exploit': '🎉 Exploit amusant',
    'generer_meme': '😄 Génère un meme',
    
    # 🔧 COMMANDES TECHNIQUES
    'hacker_coffre': '🔓 Pirate le coffre principal',
    'reboot_world': '🔄 Redémarre le monde',
    'decode_portal': '🔐 Déchiffre le portail secret',
    'assistant_pirate': '🤖 Assistant IA pirate',
    
    # 🏆 NOUVELLES COMMANDES BADGES ET RÉCOMPENSES
    'badges': '🏆 Affiche tes badges gagnés',
    'unlock_badge': '🔓 Débloque un badge secret',
    'badge_progress': '📊 Progression des badges',
    'rare_badges': '💎 Badges ultra-rares',
    'badge_showcase': '🎨 Galerie de badges',
    
    # 👤 NOUVELLES COMMANDES PERSONNALISATION
    'avatars': '👤 Affiche les avatars disponibles',
    'change_avatar': '🔄 Change ton avatar',
    'themes': '🎨 Affiche les thèmes de terminal',
    'change_theme': '🎨 Change le thème du terminal',
    'customize_profile': '⚙️ Personnalise ton profil',
    
    # 🎮 NOUVELLES COMMANDES DÉFIS SOCIAUX
    'defis_sociaux': '🎮 Affiche les défis sociaux',
    'start_duel': '⚔️ Lance un duel local 2 joueurs',
    'tournament_mode': '🏆 Mode tournoi',
    'team_battle': '👥 Bataille d\'équipes',
    'leaderboard': '📊 Classement des hackers',
    'challenge_friend': '🤝 Défie un ami',
    
    # 💔 NOUVELLES COMMANDES CHAPITRE 6 - LUNA COMPROMISE
    'save_luna': '💔 Sauve LUNA du mode berserk (30s max)',
    'hack_luna_backdoor': '🚪 Infiltre le backdoor de LUNA (10s max)',
    'override_luna_core': '💻 Override le core de LUNA (15s max)',
    'restore_luna_memory': '🧠 Restaure la mémoire de LUNA (20s max)',
    'purge_corp_virus': '🦠 Purge le virus de La Corp (25s max)',
    'reboot_luna_safe': '🔄 Redémarre LUNA en mode sûr (30s max)',
    'luna_berserk': '😡 Active le mode berserk de LUNA',
    'chapitre_6': '💔 Lance le chapitre 6 - LUNA compromise',
    
    # 🌐 ALIAS ANGLAIS
    'help': '❓ Aide en anglais',
    'profile': '👤 Profil en anglais',
    'world': '🌍 Monde en anglais',
    'status': '📊 Statut du système (raccourci)',
    'clear': '🧹 Nettoie le terminal (raccourci)',
    'test': '🧪 Teste une commande (raccourci)',
}

PROFIL_PATH = 'data/profil_joueur.json'

# Chargement du profil joueur amélioré
def charger_profil():
    try:
        return arkalia_engine.profiles.load_main_profile()
    except Exception as e:
        print(f"❌ Erreur chargement profil principal: {e}")
        # Retourner un profil par défaut en cas d'erreur
        return {
            "id": "default",
            "name": "Hacker",
            "score": 0,
            "level": 1,
            "badges": [],
            "preferences": {},
            "personnalite": {
                "type": "non_detecte",
                "traits": [],
                "missions_completees": [],
                "monde_debloque": "arkalia_base"
            },
            "progression": {
                "niveau": 1,
                "univers_debloques": ["arkalia_base"],
                "portails_ouverts": [],
                "zones_debloquees": []
            },
            "created_at": "2024-01-01T00:00:00",
            "last_login": "2024-01-01T00:00:00"
        }

def sauvegarder_profil(profil):
    arkalia_engine.profiles.save_main_profile(profil)

def analyser_personnalite(profil):
    """Analyse la personnalité basée sur les actions du joueur"""
    return arkalia_engine.luna.analyze_personality(profil)

def generer_mission_personnalisee(profil):
    """Génère une mission personnalisée selon le profil"""
    return arkalia_engine.missions.generate_personalized_mission(profil)

def charger_ascii_art(nom_fichier):
    """Charge un fichier ASCII art"""
    try:
        chemin = f"data/effects/ascii/{nom_fichier}.txt"
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "🎨 ASCII Art non trouvé"
    except:
        return "🎨 ASCII Art non trouvé"

def charger_badges():
    """Charge le système de badges"""
    try:
        with open('data/badges.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"badges": {}, "animations": {}, "couleurs_rarete": {}}

def charger_avatars():
    """Charge le système d'avatars"""
    try:
        with open('data/avatars.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"avatars": {}, "themes_terminal": {}}

def charger_defis_sociaux():
    """Charge le système de défis sociaux"""
    try:
        with open('data/defis_sociaux.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"defis_sociaux": {}, "modes_jeu": {}, "classements": {}}

def charger_chapitre_6():
    """Charge le chapitre 6 - LUNA compromise"""
    try:
        with open('data/chapitre_6_luna_compromise.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"chapitre_6": {}, "commandes_speciales": {}}

def attribuer_badge(profil, badge_id):
    """Attribue un badge au joueur"""
    badges_data = charger_badges()
    if badge_id in badges_data.get("badges", {}):
        badge = badges_data["badges"][badge_id]
        if badge_id not in profil.get("badges", []):
            profil["badges"].append(badge_id)
            profil["score"] += badge.get("points", 0)
            return {
                "badge_gagne": True,
                "badge": badge,
                "points_gagnes": badge.get("points", 0)
            }
    return {"badge_gagne": False}

def verifier_debloquage_avatar(profil, avatar_id):
    """Vérifie si un avatar est débloqué"""
    avatars_data = charger_avatars()
    if avatar_id in avatars_data.get("avatars", {}):
        avatar = avatars_data["avatars"][avatar_id]
        badge_requis = avatar.get("debloque_par", "debut")
        return badge_requis in profil.get("badges", []) or badge_requis == "debut"
    return False

def lancer_defi_social(defi_id, joueur1, joueur2=None):
    """Lance un défi social"""
    defis_data = charger_defis_sociaux()
    if defi_id in defis_data.get("defis_sociaux", {}):
        defi = defis_data["defis_sociaux"][defi_id]
        return {
            "defi_lance": True,
            "defi": defi,
            "joueur1": joueur1,
            "joueur2": joueur2,
            "timer": defi.get("timer", 30)
        }
    return {"defi_lance": False}

def executer_chapitre_6(profil, etape):
    """Exécute une étape du chapitre 6"""
    chapitre_data = charger_chapitre_6()
    chapitre = chapitre_data.get("chapitre_6", {})
    
    if etape == "introduction":
        return {
            "chapitre_6": True,
            "message": chapitre.get("introduction", {}).get("message", "Chapitre 6 lancé"),
            "urgence": "CRITIQUE",
            "timer": chapitre.get("timer", 30)
        }
    elif etape == "mission_principale":
        return {
            "mission_principale": True,
            "commande": chapitre.get("mission_principale", {}).get("commande", "save_luna"),
            "timer": chapitre.get("mission_principale", {}).get("timer", 30),
            "difficulte": "extreme"
        }
    elif etape.startswith("etape_"):
        numero_etape = int(etape.split("_")[1])
        etapes = chapitre.get("etapes", [])
        if 0 <= numero_etape - 1 < len(etapes):
            etape_data = etapes[numero_etape - 1]
            return {
                "etape": numero_etape,
                "commande": etape_data.get("commande", ""),
                "timer": etape_data.get("timer", 10),
                "message": etape_data.get("message", "")
            }
    
    return {"chapitre_6": False, "erreur": "Étape non trouvée"}

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/monde')
def monde():
    profil = charger_profil()
    return render_template('monde.html', profil=profil)

@app.route('/profil')
def profil():
    profil = charger_profil()
    return render_template('profil.html', profil=profil)

@app.route('/explorateur')
def explorateur():
    """Module explorateur de fichiers immersif"""
    profil = charger_profil()
    return render_template('explorateur.html', profil=profil)

@app.route('/mail')
def mail():
    """Module système de mail narratif"""
    profil = charger_profil()
    return render_template('mail.html', profil=profil)

@app.route('/audio')
def audio():
    """Module système audio avancé"""
    profil = charger_profil()
    return render_template('audio.html', profil=profil)

# Routes pour servir les fichiers JSON
@app.route('/data/profil_joueur.json')
def get_profil():
    return jsonify(charger_profil())

@app.route('/data/missions/<mission_name>')
def get_mission(mission_name):
    try:
        mission_path = f'data/missions/{mission_name}'
        if os.path.exists(mission_path):
            with open(mission_path, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        else:
            # Retourner une mission par défaut si le fichier n'existe pas
            mission_defaut = {
                "id": "mission_defaut",
                "titre": "🎯 Mission d'Exploration",
                "description": "Explore le monde d'Arkalia et découvre tes capacités cachées.",
                "difficulte": "facile",
                "recompense": 50,
                "etapes": [
                    "Utilise 'unlock_universe' pour débloquer l'univers",
                    "Utilise 'scan_persona' pour analyser ta personnalité",
                    "Utilise 'load_mission' pour charger une mission personnalisée"
                ]
            }
            return jsonify(mission_defaut)
    except Exception as e:
        return jsonify({"erreur": f"Impossible de charger la mission: {str(e)}"}), 500

handler = CommandHandler()

@app.route('/commande', methods=['POST'])
def commande():
    data = request.get_json()
    # Accepter soit 'cmd' soit 'commande' comme clé
    cmd = data.get('cmd', data.get('commande', ''))
    if not isinstance(cmd, str) or not cmd.strip():
        # Erreur : commande vide ou invalide
        return jsonify({
            "reponse": {
                "réussite": False,
                "message": "❌ Commande vide ou invalide. Utilise la clé 'commande' ou 'cmd' avec une valeur non vide.",
                "profile_updated": False
            }
        }), 400
    cmd = cmd.strip()
    profil = charger_profil()
    # Log de la commande reçue
    print(f"[API] Commande reçue: {cmd}")
    reponse = handler.handle_command(cmd, profil)
    print(f"[DEBUG] Réponse du handler: {reponse}")
    if reponse.get("profile_updated"):
        sauvegarder_profil(profil)
    return jsonify({"reponse": reponse})

@app.route('/api/content')
def get_available_content():
    """Récupère tout le contenu disponible (missions, profils, etc.)"""
    return jsonify(arkalia_engine.get_available_content())

@app.route('/api/mission/<mission_name>')
def get_mission_via_engine(mission_name):
    """Récupère une mission via le moteur unifié"""
    result = arkalia_engine.get_mission_info(mission_name)
    if result["success"]:
        return jsonify(result["mission"])
    else:
        return jsonify({"erreur": result["message"]}), 404

@app.route('/api/profile/summary')
def get_profile_summary():
    """Récupère un résumé du profil via le moteur unifié"""
    profil = charger_profil()
    return jsonify(arkalia_engine.get_profile_summary(profil))

def luna_meme_reaction(fail_type, score):
    """Génère des réponses memes de LUNA selon le type d'échec"""
    
    memes = {
        "hack_fail": [
            "🤖 LUNA: T'es sérieux ? Même mon chat code mieux ! 😹",
            "🤖 LUNA: C'est ça ton niveau ? Mon toaster est plus intelligent ! 🍞",
            "🤖 LUNA: Tu veux que je t'apprenne à utiliser un clavier ? ⌨️",
            "🤖 LUNA: Même un poisson rouge ferait mieux ! 🐠"
        ],
        "timeout": [
            "⏰ LUNA: T'es trop lent, chicken ! Un escargot va plus vite ! 🐌",
            "⏰ LUNA: Tu as la vitesse d'un sloth en hibernation ! 🦥",
            "⏰ LUNA: Même ma grand-mère code plus vite ! 👵",
            "⏰ LUNA: Tu veux que je t'offre une trottinette ? 🛴"
        ],
        "wrong_command": [
            "❌ LUNA: C'est pas ça du tout ! Tu lis les instructions ou quoi ? 📖",
            "❌ LUNA: Tu tapes au hasard ou tu réfléchis ? 🤔",
            "❌ LUNA: Même un singe taperait mieux ! 🐒",
            "❌ LUNA: Tu veux que je t'apprenne l'alphabet ? 🔤"
        ],
        "low_score": [
            f"📊 LUNA: {score} points ? Mon hamster a un meilleur score ! 🐹",
            f"📊 LUNA: {score} points ? C'est tout ? Même un caillou fait mieux ! 🪨",
            f"📊 LUNA: {score} points ? Tu veux que je te donne des cours ? 📚",
            f"📊 LUNA: {score} points ? Mon micro-onde est plus intelligent ! 🔥"
        ]
    }
    
    import random
    return random.choice(memes.get(fail_type, ["🤖 LUNA: ..."]))

# ===== NOUVELLES ROUTES API POUR VERSION 3.0 =====

# Import des nouveaux modules
try:
    from core.database import db_manager
    from core.websocket_manager import websocket_manager
    DATABASE_AVAILABLE = True
    WEBSOCKET_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    WEBSOCKET_AVAILABLE = False
    print("⚠️ Modules avancés non disponibles, utilisation du mode dégradé")

@app.route('/api/database/migrate', methods=['POST'])
def migrate_to_database():
    """Migre les données JSON vers SQLite"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database module not available"}), 500
    
    try:
        db_manager.migrate_json_to_sqlite()
        return jsonify({"success": True, "message": "Migration réussie"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/database/profile/<username>', methods=['GET'])
def get_profile_from_db(username):
    """Récupère un profil depuis la base de données"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database module not available"}), 500
    
    try:
        profile = db_manager.load_profile(username)
        if profile:
            return jsonify(profile)
        else:
            return jsonify({"error": "Profile not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/database/profile/<username>', methods=['PUT'])
def save_profile_to_db(username):
    """Sauvegarde un profil dans la base de données"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database module not available"}), 500
    
    try:
        data = request.get_json()
        success = db_manager.save_profile(username, data)
        if success:
            return jsonify({"success": True, "message": "Profile sauvegardé"})
        else:
            return jsonify({"error": "Failed to save profile"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/database/leaderboard', methods=['GET'])
def get_leaderboard():
    """Récupère le classement des joueurs"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database module not available"}), 500
    
    try:
        limit = request.args.get('limit', 10, type=int)
        leaderboard = db_manager.get_leaderboard(limit)
        return jsonify({"leaderboard": leaderboard})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/websocket/challenge/create', methods=['POST'])
def create_challenge():
    """Crée un nouveau défi social"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"error": "WebSocket module not available"}), 500
    
    try:
        data = request.get_json()
        room_id = websocket_manager.create_challenge_room(data)
        return jsonify({
            "success": True,
            "room_id": room_id,
            "challenge_info": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/websocket/challenge/<room_id>/info', methods=['GET'])
def get_challenge_info(room_id):
    """Récupère les informations d'un défi"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"error": "WebSocket module not available"}), 500
    
    try:
        info = websocket_manager.get_room_info(room_id)
        if info:
            return jsonify(info)
        else:
            return jsonify({"error": "Challenge not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/websocket/challenge/<room_id>/join', methods=['POST'])
def join_challenge(room_id):
    """Rejoint un défi (simulation WebSocket)"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"error": "WebSocket module not available"}), 500
    
    try:
        data = request.get_json()
        data['room_id'] = room_id
        session_id = data.get('session_id', f"session_{int(time.time())}")
        
        result = websocket_manager.handle_join_challenge(session_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/websocket/challenge/<room_id>/action', methods=['POST'])
def challenge_action(room_id):
    """Effectue une action dans un défi (simulation WebSocket)"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"error": "WebSocket module not available"}), 500
    
    try:
        data = request.get_json()
        data['room_id'] = room_id
        session_id = data.get('session_id', f"session_{int(time.time())}")
        
        result = websocket_manager.handle_challenge_action(session_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/luna/learning-data', methods=['GET'])
def get_luna_learning_data():
    """Récupère les données d'apprentissage de LUNA"""
    try:
        # Charger les données d'apprentissage depuis le fichier JSON
        learning_data_path = 'data/learning_data.json'
        if os.path.exists(learning_data_path):
            with open(learning_data_path, 'r', encoding='utf-8') as f:
                learning_data = json.load(f)
        else:
            # Données par défaut
            learning_data = {
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
            }
        
        return jsonify(learning_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/luna/analyze-action', methods=['POST'])
def analyze_user_action():
    """Analyse une action utilisateur avec l'IA LUNA"""
    try:
        data = request.get_json()
        action = data.get('action', '')
        context = data.get('context', {})
        
        # Simulation de l'analyse IA
        analysis = {
            "action_type": "general",
            "difficulty_level": 0.5,
            "success_probability": 0.7,
            "personality_insights": {
                "risk_tolerance": 0.6,
                "creativity_level": 0.5,
                "social_preference": 0.4,
                "competitiveness": 0.7
            },
            "learning_opportunity": {
                "skill_development": ["general_hacking"],
                "knowledge_gap": [],
                "strategy_improvement": []
            }
        }
        
        # Ajuster selon l'action
        if "speed" in action or "turbo" in action:
            analysis["action_type"] = "speed"
            analysis["personality_insights"]["competitiveness"] = 0.8
        elif "social" in action or "team" in action:
            analysis["action_type"] = "social"
            analysis["personality_insights"]["social_preference"] = 0.7
        elif "creative" in action or "meme" in action:
            analysis["action_type"] = "creative"
            analysis["personality_insights"]["creativity_level"] = 0.8
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/luna/predict-behavior', methods=['POST'])
def predict_user_behavior():
    """Prédit le comportement futur de l'utilisateur"""
    try:
        data = request.get_json()
        user_actions = data.get('actions', [])
        
        # Simulation de prédiction
        predictions = {
            "next_likely_action": "aide" if not user_actions else user_actions[-1],
            "success_probability": 0.7,
            "engagement_level": min(1.0, len(user_actions) / 10)
        }
        
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== ROUTES DE TEST POUR LES NOUVELLES FONCTIONNALITÉS =====

@app.route('/api/test/database', methods=['GET'])
def test_database():
    """Test de la base de données"""
    if not DATABASE_AVAILABLE:
        return jsonify({"status": "unavailable", "message": "Database module not available"})
    
    try:
        # Test de création d'un profil
        test_profile = {
            "score": 1000,
            "niveau": 2,
            "badges": ["Test Badge"],
            "avatars": ["hacker_classique"],
            "preferences": {"theme": "matrix"}
        }
        
        success = db_manager.save_profile("test_user", test_profile)
        if success:
            loaded_profile = db_manager.load_profile("test_user")
            return jsonify({
                "status": "working",
                "message": "Database test successful",
                "profile": loaded_profile
            })
        else:
            return jsonify({"status": "error", "message": "Failed to save profile"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/test/websocket', methods=['GET'])
def test_websocket():
    """Test des WebSockets"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"status": "unavailable", "message": "WebSocket module not available"})
    
    try:
        # Test de création d'un défi
        challenge_data = {
            "title": "Test Challenge",
            "description": "Test challenge for WebSocket",
            "timer": 30,
            "players": []
        }
        
        room_id = websocket_manager.create_challenge_room(challenge_data)
        room_info = websocket_manager.get_room_info(room_id)
        
        return jsonify({
            "status": "working",
            "message": "WebSocket test successful",
            "room_id": room_id,
            "room_info": room_info
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/test/ai', methods=['GET'])
def test_ai():
    """Test de l'IA"""
    try:
        # Test d'analyse d'action
        test_analysis = {
            "action_type": "speed",
            "difficulty_level": 0.6,
            "success_probability": 0.8,
            "personality_insights": {
                "risk_tolerance": 0.7,
                "creativity_level": 0.5,
                "social_preference": 0.3,
                "competitiveness": 0.8
            }
        }
        
        return jsonify({
            "status": "working",
            "message": "AI test successful",
            "analysis": test_analysis
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ===== ROUTE DE STATUT GÉNÉRAL =====

@app.route('/api/status', methods=['GET'])
def get_system_status():
    """Récupère le statut général du système"""
    status = {
        "version": "3.0.0",
        "database": "available" if DATABASE_AVAILABLE else "unavailable",
        "websocket": "available" if WEBSOCKET_AVAILABLE else "unavailable",
        "ai": "available",
        "features": {
            "sqlite_migration": DATABASE_AVAILABLE,
            "real_time_challenges": WEBSOCKET_AVAILABLE,
            "advanced_ai": True,
            "personality_analysis": True
        }
    }
    
    return jsonify(status)

# @app.route('/os2142')
# def os2142():
#     """Route pour l'interface OS 2142"""
#     return render_template('os2142.html')

if __name__ == '__main__':
    # Créer les dossiers nécessaires
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/effects'):
        os.makedirs('data/effects')
    if not os.path.exists('data/effects/ascii'):
        os.makedirs('data/effects/ascii')
    if not os.path.exists('data/missions'):
        os.makedirs('data/missions')
    
    print("🚀 Démarrage d'Arkalia Quest v2.0")
    print("🌙 IA LUNA initialisée")
    print("🎮 Moteur de jeu prêt")
    print("🎨 Effets visuels activés")
    print(f"🌐 Serveur sur http://0.0.0.0:5001 (port configuré)")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
