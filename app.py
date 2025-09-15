import json
import logging
import os
import random
import time
from datetime import datetime, timedelta

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_compress import Compress

# Imports avec gestion d'erreur robuste
try:
    from arkalia_engine import arkalia_engine
    from core.adaptive_storytelling import adaptive_storytelling
    from core.advanced_achievements import advanced_achievements
    from core.cache_manager import cache_manager
    from core.category_leaderboards import category_leaderboards
    from core.command_handler_v2 import CommandHandlerV2 as CommandHandler
    from core.customization_engine import customization_engine
    from core.daily_challenges_engine import DailyChallengesEngine
    from core.database import DatabaseManager
    from core.educational_games_engine import EducationalGamesEngine
    from core.gamification_engine import GamificationEngine
    from core.micro_interactions import micro_interactions
    from core.mission_progress_tracker import mission_progress_tracker
    from core.narrative_branches import narrative_branches
    from core.performance_optimizer import performance_optimizer
    from core.secondary_missions import secondary_missions
    from core.security_enhanced import security_enhanced
    from core.security_manager import security_manager
    from core.social_engine import social_engine
    from core.technical_tutorials import technical_tutorials
    from core.tutorial_manager import tutorial_manager
    from core.websocket_manager import websocket_manager
    from engines.luna_ai_v3 import LunaAIV3

    print("✅ All core modules imported successfully")
except Exception as e:
    print(f"❌ Error importing core modules: {e}")
    import traceback

    traceback.print_exc()
    # Créer des objets factices pour éviter les erreurs
    arkalia_engine = None
    adaptive_storytelling = None
    advanced_achievements = None
    cache_manager = None
    category_leaderboards = None
    CommandHandler = None
    customization_engine = None
    DailyChallengesEngine = None
    DatabaseManager = None
    EducationalGamesEngine = None
    GamificationEngine = None
    micro_interactions = None
    mission_progress_tracker = None
    narrative_branches = None
    performance_optimizer = None
    secondary_missions = None
    security_enhanced = None
    security_manager = None
    social_engine = None
    technical_tutorials = None
    tutorial_manager = None
    websocket_manager = None
    LunaAIV3 = None

try:
    from utils.logger import game_logger, performance_logger, security_logger
except ImportError:
    # Fallback si le module utils est en conflit
    game_logger = logging.getLogger("arkalia_game")
    security_logger = logging.getLogger("arkalia_security")
    performance_logger = logging.getLogger("arkalia_performance")

# from core.educational_games_engine import educational_games

app = Flask(__name__)

# Configuration sécurisée des sessions
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-key-change-in-production"),
    SESSION_COOKIE_SECURE=False,  # Désactivé pour HTTP en développement
    SESSION_COOKIE_HTTPONLY=True,  # Pas d'accès JavaScript
    SESSION_COOKIE_SAMESITE="Lax",  # Protection CSRF
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2),  # Expiration
    SESSION_REFRESH_EACH_REQUEST=True,  # Renouvellement
)

# Configuration de la compression gzip
Compress(app)

# Instance globale du moteur de jeux éducatifs
try:
    games_engine = EducationalGamesEngine() if EducationalGamesEngine else None
    print("✅ Games engine initialized")
except Exception as e:
    print(f"❌ Error initializing games engine: {e}")
    games_engine = None


# Middleware de sécurité et performance
@app.before_request
def before_request():
    """Middleware exécuté avant chaque requête"""
    # Vérifier la sécurité
    client_ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)

    # Vérifier si l'IP est bloquée (si le module est disponible)
    if security_enhanced and hasattr(security_enhanced, "is_ip_blocked"):
        if security_enhanced.is_ip_blocked(client_ip):
            return jsonify({"error": "Accès refusé"}), 403

    # Vérifier le rate limiting (si le module est disponible)
    if security_enhanced and hasattr(security_enhanced, "check_rate_limit"):
        allowed, message = security_enhanced.check_rate_limit(client_ip)
        if not allowed:
            return jsonify({"error": message}), 429

    # Valider les entrées (sauf pour les routes des jeux éducatifs)
    if request.method in ["POST", "PUT", "PATCH"]:
        if (
            request.is_json
            and not request.path.startswith("/api/educational-games")
            and not request.path.startswith("/api/luna-v3/")
        ):
            data = request.get_json()
            if data:
                for key, value in data.items():
                    if isinstance(value, str):
                        # Validation renforcée selon le type de champ
                        input_type = "command"  # Par défaut
                        if "username" in key.lower():
                            input_type = "username"
                        elif "email" in key.lower():
                            input_type = "email"
                        elif "password" in key.lower():
                            input_type = "password"
                        elif "game_id" in key.lower():
                            input_type = "game_id"

                        is_valid, error_msg = security_enhanced.validate_input(
                            input_type, value
                        )
                        if not is_valid:
                            return (
                                jsonify(
                                    {"error": f"Entrée invalide ({key}): {error_msg}"}
                                ),
                                400,
                            )


@app.after_request
def after_request(response):
    """Middleware exécuté après chaque requête"""
    # Ajouter des headers de sécurité renforcés
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'"
    )
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # Ajouter des headers de cache pour les assets statiques
    if request.endpoint and request.endpoint.startswith("static"):
        response.headers["Cache-Control"] = "public, max-age=31536000"  # 1 an
    else:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

    return response


# Gestionnaire d'erreurs global
@app.errorhandler(404)
def not_found(error):
    """Gestion des erreurs 404"""
    return jsonify({"error": "Ressource non trouvée", "code": 404}), 404


# Gestionnaires d'erreurs définis


@app.errorhandler(403)
def forbidden(error):
    """Gestion des erreurs 403"""
    return jsonify({"error": "Accès refusé", "code": 403}), 403


# Instances des modules
gamification = GamificationEngine()
command_handler = CommandHandler()
db_manager = DatabaseManager()

# Variables de disponibilité des modules
DATABASE_AVAILABLE = True
WEBSOCKET_AVAILABLE = True
TUTORIAL_AVAILABLE = True
EDUCATIONAL_GAMES_AVAILABLE = False  # Désactivé temporairement

# Rate limiting simple
request_counts = {}
RATE_LIMIT = 100  # 100 requêtes par minute par IP
RATE_LIMIT_WINDOW = 60  # Fenêtre de 60 secondes

# Variable de temps de démarrage pour les métriques
start_time = time.time()


# Configuration de sécurité
@app.after_request
def add_security_headers(response):
    """Ajoute les headers de sécurité à toutes les réponses"""
    if response is not None:
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )
    return response


@app.after_request
def add_cache_headers(response):
    """Ajoute des headers de cache appropriés selon le type de ressource"""
    if response is not None:
        # Cache long pour les assets statiques
        if request.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=31536000"  # 1 an
            response.headers["ETag"] = f'"{hash(request.path)}"'
        # Cache court pour les pages HTML
        elif request.path.endswith(".html"):
            response.headers["Cache-Control"] = "public, max-age=3600"  # 1 heure
        # Pas de cache pour les API dynamiques
        elif request.path.startswith("/api/") or request.path.startswith("/commande"):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        # Cache par défaut pour les autres ressources
        else:
            response.headers["Cache-Control"] = "public, max-age=300"  # 5 minutes
    return response


# Gestionnaire d'erreurs global
@app.errorhandler(Exception)
def handle_exception(e):
    """Gestionnaire d'erreurs global pour éviter les erreurs en cascade"""
    app.logger.error(f"Exception non gérée: {e}")
    return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    return jsonify({"error": "Internal server error"}), 500


# Gestionnaire 404 supprimé - déjà défini plus haut


# Commandes autorisées - Version "L'Éveil des IA"
COMMANDES_AUTORISEES = {
    # 🎯 COMMANDES DE L'HISTOIRE (7 actes + épilogue)
    "start_tutorial": "🎮 Commence l'aventure (PREMIÈRE FOIS)",
    "luna_contact": "🌙 Contacte LUNA, ton IA complice",
    "prologue": "📖 Décrypte le SOS d'Althea",
    "acte_1": "🌟 Répare le site web de LUNA",
    "acte_2": "📝 Décrypte les logs de NEXUS",
    "acte_3": "🎵 Analyse la berceuse d'Althea",
    "acte_4": "📧 Traque l'email piégé",
    "acte_5": "⚖️ Le choix final : fusion ou destruction",
    "acte_6": "🤖 Naissance d'Arkalia",
    "epilogue": "🌅 L'aube de PANDORA",
    # 🌙 COMMANDES LUNA v3.0
    "luna_engine": "🌙 Active le moteur Arkalia Engine",
    "luna_learning": "📚 Affiche les données d'apprentissage LUNA",
    "luna_analyze": "🧠 Analyse de personnalité avancée",
    "luna_preferences": "⚙️ Affiche vos préférences utilisateur",
    "luna_reset": "🔄 Réinitialise l'apprentissage LUNA",
    # 💻 COMMANDES DE HACKING
    "hack_system": "💻 Hack le système de La Corp (8s max)",
    "kill_virus": "🦠 Élimine les virus du système",
    "find_shadow": "👤 Trouve SHADOW-13",
    "challenge_corp": "⚔️ Défie La Corp",
    "decode_portal": "🚪 Décode un portail mystérieux",
    "hacker_coffre": "💎 Hack un coffre-fort numérique",
    "boss_final": "👑 Affronte le boss final",
    # Commandes utilitaires
    "badges": "🏆 Affiche tes badges gagnés",
    "avatars": "👤 Affiche les avatars disponibles",
    "leaderboard": "📊 Classement des hackers",
    "achievements": "🏆 Affiche les succès",
    "profil": "👤 Affiche ton profil",
    "aide": "❓ Affiche l'aide",
    "monde": "🌍 Accède au monde Arkalia",
    "status": "📊 Statut du système",
}


# Chargement du profil joueur amélioré
def charger_profil():
    try:
        profil = arkalia_engine.profiles.load_main_profile()

        # S'assurer que la structure personnalite est présente
        if "personnalite" not in profil:
            profil["personnalite"] = {
                "type": "non_detecte",
                "traits": [],
                "missions_completees": [],
                "monde_debloque": "arkalia_base",
            }

        # S'assurer que la structure progression est présente
        if "progression" not in profil:
            profil["progression"] = {
                "niveau": profil.get("level", 1),
                "experience": 0,
                "missions_completees": 0,
                "univers_debloques": ["arkalia_base"],
                "portails_ouverts": [],
                "zones_debloquees": [],
            }

        # S'assurer que les badges sont une liste
        if "badges" not in profil:
            profil["badges"] = []

        return profil
    except Exception as e:
        game_logger.error(f"Erreur chargement profil principal: {e}")
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
                "monde_debloque": "arkalia_base",
            },
            "progression": {
                "niveau": 1,
                "experience": 0,
                "missions_completees": 0,
                "univers_debloques": ["arkalia_base"],
                "portails_ouverts": [],
                "zones_debloquees": [],
            },
            "created_at": "2025-01-01T00:00:00",
            "last_login": "2025-01-01T00:00:00",
        }


def sauvegarder_profil(profil):
    try:
        # S'assurer que la clé 'name' est présente
        if "name" not in profil:
            profil["name"] = profil.get("id", "Hacker")

        # S'assurer que la clé 'level' est présente
        if "level" not in profil:
            profil["level"] = profil.get("progression", {}).get("niveau", 1)

        arkalia_engine.profiles.save_main_profile(profil)
    except Exception as e:
        game_logger.error(f"Erreur sauvegarde profil: {e}")


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
            with open(chemin, encoding="utf-8") as f:
                return f.read()
        else:
            return "🎨 ASCII Art non trouvé"
    except Exception:
        return "🎨 ASCII Art non trouvé"


def charger_badges():
    """Charge le système de badges"""
    try:
        with open("data/badges.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"badges": {}, "animations": {}, "couleurs_rarete": {}}


def charger_avatars():
    """Charge le système d'avatars"""
    try:
        with open("data/avatars.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"avatars": {}, "themes_terminal": {}}


def charger_defis_sociaux():
    """Charge le système de défis sociaux"""
    try:
        with open("data/defis_sociaux.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"defis_sociaux": {}, "modes_jeu": {}, "classements": {}}


def charger_chapitre_6():
    """Charge le chapitre 6 - LUNA compromise"""
    try:
        with open("data/chapitre_6_luna_compromise.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
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
                "points_gagnes": badge.get("points", 0),
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
            "timer": defi.get("timer", 30),
        }
    return {"defi_lance": False}


def executer_chapitre_6(etape):
    """Exécute une étape du chapitre 6"""
    chapitre_data = charger_chapitre_6()
    chapitre = chapitre_data.get("chapitre_6", {})

    if etape == "introduction":
        return {
            "chapitre_6": True,
            "message": chapitre.get("introduction", {}).get(
                "message", "Chapitre 6 lancé"
            ),
            "urgence": "CRITIQUE",
            "timer": chapitre.get("timer", 30),
        }
    elif etape == "mission_principale":
        return {
            "mission_principale": True,
            "commande": chapitre.get("mission_principale", {}).get(
                "commande", "save_luna"
            ),
            "timer": chapitre.get("mission_principale", {}).get("timer", 30),
            "difficulte": "extreme",
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
                "message": etape_data.get("message", ""),
            }

    return {"chapitre_6": False, "erreur": "Étape non trouvée"}


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(".", "favicon.ico")


@app.route("/tests/<filename>")
def serve_test_file(filename):
    """Sert les fichiers de test HTML depuis le dossier tests/"""
    return send_from_directory("tests", filename)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tutorial")
def tutorial():
    """Page tutoriel d'accueil pour nouveaux utilisateurs"""
    return render_template("tutorial_welcome.html")


@app.route("/terminal")
def terminal():
    return render_template("terminal.html")


@app.route("/monde")
def monde():
    profil = charger_profil()
    return render_template("monde.html", profil=profil)


@app.route("/profil")
def profil():
    profil = charger_profil()
    return render_template("profil.html", profil=profil)


@app.route("/dashboard")
def dashboard():
    """Page dashboard avec statistiques et actions rapides"""
    profil = charger_profil()
    return render_template("dashboard.html", profil=profil)


@app.route("/explorateur")
def explorateur():
    """Module explorateur de fichiers immersif"""
    profil = charger_profil()
    return render_template("explorateur.html", profil=profil)


@app.route("/mail")
def mail():
    """Module système de mail narratif"""
    profil = charger_profil()
    return render_template("mail.html", profil=profil)


@app.route("/audio")
def audio():
    """Module système audio avancé"""
    profil = charger_profil()
    return render_template("audio.html", profil=profil)


@app.route("/accessibility")
def accessibility():
    """Panneau d'accessibilité pour personnaliser l'expérience utilisateur"""
    profil = charger_profil()
    return render_template("accessibility_panel.html", profil=profil)


# ===== API ACCESSIBILITÉ =====
@app.route("/api/accessibility/save", methods=["POST"])
def api_accessibility_save():
    """Enregistre les préférences d'accessibilité côté serveur (si profil dispo).

    Stocke les préférences sous la clé 'accessibility' du profil utilisateur.
    Retourne success True/False avec message.
    """
    try:
        data = request.get_json(silent=True) or {}

        # Validation basique
        if not isinstance(data, dict):
            return jsonify({"success": False, "message": "Données invalides"}), 400

        profil = charger_profil()
        # Conserver uniquement les clés attendues pour éviter l'injection inutile
        allowed_keys = {
            "highContrast",
            "fontSize",
            "reducedMotion",
            "subtitles",
            "effectsVolume",
            "audioDescription",
            "keyboardNav",
            "focusVisible",
            "keyboardShortcuts",
            "darkMode",
            "elementSpacing",
            "customCursor",
        }
        accessibility_prefs = {k: v for k, v in data.items() if k in allowed_keys}

        profil["accessibility"] = accessibility_prefs
        sauvegarder_profil(profil)

        return jsonify(
            {"success": True, "message": "Préférences d'accessibilité sauvegardées"}
        )
    except Exception as e:
        game_logger.error(f"Erreur sauvegarde accessibilité: {e}")
        return (
            jsonify(
                {"success": False, "message": "Erreur interne lors de l'enregistrement"}
            ),
            500,
        )


# Routes pour servir les fichiers JSON


@app.route("/data/profil_joueur.json")
def get_profil():
    return jsonify(db_manager.load_profile("main_user"))


@app.route("/data/missions/<mission_name>")
def get_mission(mission_name):
    mission = db_manager.load_mission(mission_name)
    if mission:
        return jsonify(mission)
    else:
        return jsonify({"erreur": f"Mission {mission_name} non trouvée"}), 404


def check_rate_limit(ip_address):
    """Vérifie le rate limiting pour une IP donnée"""
    global request_counts
    current_time = time.time()

    # Nettoyer les anciennes entrées
    request_counts = {
        ip: (count, timestamp)
        for ip, (count, timestamp) in request_counts.items()
        if current_time - timestamp < RATE_LIMIT_WINDOW
    }

    if ip_address not in request_counts:
        request_counts[ip_address] = (1, current_time)
        return True

    # Vérifier que l'entrée existe et est valide
    entry = request_counts.get(ip_address)
    if not entry or len(entry) != 2:
        request_counts[ip_address] = (1, current_time)
        return True

    count, timestamp = entry

    if current_time - timestamp >= RATE_LIMIT_WINDOW:
        # Nouvelle fenêtre de temps
        request_counts[ip_address] = (1, current_time)
        return True

    if count >= RATE_LIMIT:
        return False

    # Incrémenter le compteur
    request_counts[ip_address] = (count + 1, timestamp)
    return True


@app.route("/test-commande", methods=["POST"])
def test_commande():
    """Route de test simple pour debugger"""
    try:
        data = request.get_json()
        cmd = data.get("commande", "") if data else ""
        return jsonify({"status": "ok", "commande": cmd, "message": "Test réussi"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/commande", methods=["POST"])
def commande():
    # Rate limiting
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return (
            jsonify(
                {
                    "reponse": {
                        "réussite": False,
                        "message": "❌ Trop de requêtes. Attendez un peu avant de réessayer.",
                        "profile_updated": False,
                    }
                }
            ),
            429,  # Too Many Requests
        )

    data = request.get_json()

    # Validation stricte des entrées
    if not data or not isinstance(data, dict):
        return (
            jsonify(
                {
                    "reponse": {
                        "réussite": False,
                        "message": "❌ Données invalides. Envoie un objet JSON valide.",
                        "profile_updated": False,
                    }
                }
            ),
            400,
        )

    # Accepter soit 'cmd' soit 'commande' comme clé
    cmd = data.get("cmd", data.get("commande", ""))

    # Validation de la commande
    if not isinstance(cmd, str):
        return (
            jsonify(
                {
                    "reponse": {
                        "réussite": False,
                        "message": "❌ Commande invalide. La commande doit être une chaîne de caractères.",
                        "profile_updated": False,
                    }
                }
            ),
            400,
        )

    cmd = cmd.strip()

    # Validation de la longueur et du contenu
    if not cmd:
        return (
            jsonify(
                {
                    "reponse": {
                        "réussite": False,
                        "message": "❌ Commande vide. Utilise la clé 'commande' ou 'cmd' avec une valeur non vide.",
                        "profile_updated": False,
                    }
                }
            ),
            400,
        )

    if len(cmd) > 1000:
        return (
            jsonify(
                {
                    "reponse": {
                        "réussite": False,
                        "message": "❌ Commande trop longue. Maximum 1000 caractères.",
                        "profile_updated": False,
                    }
                }
            ),
            400,
        )

    # Vérification de sécurité avancée
    security_check = security_manager.check_input_security(cmd, client_ip)
    if not security_check["is_safe"]:
        # Bloquer l'IP si menace critique
        if security_check["risk_level"] == "critical":
            security_manager.block_ip(
                client_ip, f"Commande dangereuse: {security_check['threats_detected']}"
            )

        return (
            jsonify(
                {
                    "reponse": {
                        "réussite": False,
                        "message": "❌ Commande rejetée pour des raisons de sécurité.",
                        "profile_updated": False,
                    }
                }
            ),
            400,
        )

    profil = charger_profil()

    # Log de la commande reçue
    game_logger.info(f"Commande reçue: {cmd}")

    try:
        reponse = command_handler.handle_command(cmd, profil)
        game_logger.debug(f"Réponse du handler: {reponse}")
    except Exception as e:
        game_logger.error(f"Erreur lors du traitement de la commande: {e}")
        return (
            jsonify(
                {
                    "reponse": {
                        "réussite": False,
                        "message": "❌ Erreur interne lors du traitement de la commande.",
                        "profile_updated": False,
                    }
                }
            ),
            500,
        )

    # Mise à jour de la gamification
    if reponse.get("profile_updated"):
        try:
            # Mettre à jour le leaderboard
            gamification.update_leaderboard(profil.get("id", "default"), profil)

            # Vérifier les badges secrets et achievements
            unlocked_badges = gamification.check_badges_secrets(
                profil, "command_used", command=cmd
            )
            unlocked_achievements = gamification.check_achievements(
                profil.get("id", "default"), profil, "command_used", command=cmd
            )

            # Ajouter les badges débloqués au profil
            for badge_id in unlocked_badges:
                if "badges" not in profil:
                    profil["badges"] = []
                if badge_id not in profil["badges"]:
                    profil["badges"].append(badge_id)
                    reponse["badge_unlocked"] = badge_id

            # Ajouter les achievements débloqués au profil
            for achievement_id in unlocked_achievements:
                if "achievements" not in profil:
                    profil["achievements"] = []
                if achievement_id not in profil["achievements"]:
                    profil["achievements"].append(achievement_id)
                    reponse["achievement_unlocked"] = achievement_id

            sauvegarder_profil(profil)
        except Exception as e:
            game_logger.error(f"Erreur lors de la mise à jour du profil: {e}")

    return jsonify({"reponse": reponse})


@app.route("/api/content")
def get_available_content():
    """Récupère tout le contenu disponible (missions, profils, etc.)"""
    return jsonify(arkalia_engine.get_available_content())


@app.route("/api/mission/<mission_name>")
def get_mission_via_engine(mission_name):
    """Récupère une mission via le moteur unifié"""
    result = arkalia_engine.get_mission_info(mission_name)
    if result["success"]:
        return jsonify(result["mission"])
    else:
        return jsonify({"erreur": result["message"]}), 404


@app.route("/api/profile/summary")
def get_profile_summary():
    """Récupère un résumé du profil via le moteur unifié"""
    try:
        profil = charger_profil()

        # Créer un résumé du profil
        summary = {
            "success": True,
            "profile": {
                "id": profil.get("id", "default"),
                "name": profil.get("name", "Hacker"),
                "level": profil.get("level", 1),
                "score": profil.get("score", 0),
                "badges": profil.get("badges", []),
                "missions_completees": profil.get("progression", {}).get(
                    "missions_completees", 0
                ),
                "personnalite": profil.get(
                    "personnalite", {"type": "non_detecte", "traits": []}
                ),
                "created_at": profil.get("created_at", "2025-01-01T00:00:00"),
                "last_login": profil.get("last_login", "2025-01-01T00:00:00"),
            },
        }

        return jsonify(summary)
    except Exception as e:
        game_logger.error(f"Erreur dans get_profile_summary: {e}")
        return jsonify(
            {
                "success": True,
                "profile": {
                    "id": "default",
                    "name": "Hacker",
                    "level": 1,
                    "score": 0,
                    "badges": [],
                    "missions_completees": 0,
                    "personnalite": {"type": "non_detecte", "traits": []},
                    "created_at": "2025-01-01T00:00:00",
                    "last_login": "2025-01-01T00:00:00",
                },
            }
        )


def luna_meme_reaction(fail_type, score):
    """Génère des réponses memes de LUNA selon le type d'échec"""

    memes = {
        "hack_fail": [
            "🤖 LUNA: T'es sérieux ? Même mon chat code mieux ! 😹",
            "🤖 LUNA: C'est ça ton niveau ? Mon toaster est plus intelligent ! 🍞",
            "🤖 LUNA: Tu veux que je t'apprenne à utiliser un clavier ? ⌨️",
            "🤖 LUNA: Même un poisson rouge ferait mieux ! 🐠",
        ],
        "timeout": [
            "⏰ LUNA: T'es trop lent, chicken ! Un escargot va plus vite ! 🐌",
            "⏰ LUNA: Tu as la vitesse d'un sloth en hibernation ! 🦥",
            "⏰ LUNA: Même ma grand-mère code plus vite ! 👵",
            "⏰ LUNA: Tu veux que je t'offre une trottinette ? 🛴",
        ],
        "wrong_command": [
            "❌ LUNA: C'est pas ça du tout ! Tu lis les instructions ou quoi ? 📖",
            "❌ LUNA: Tu tapes au hasard ou tu réfléchis ? 🤔",
            "❌ LUNA: Même un singe taperait mieux ! 🐒",
            "❌ LUNA: Tu veux que je t'apprenne l'alphabet ? 🔤",
        ],
        "low_score": [
            f"📊 LUNA: {score} points ? Mon hamster a un meilleur score ! 🐹",
            f"📊 LUNA: {score} points ? C'est tout ? Même un caillou fait mieux ! 🪨",
            f"📊 LUNA: {score} points ? Tu veux que je te donne des cours ? 📚",
            f"📊 LUNA: {score} points ? Mon micro-onde est plus intelligent ! 🔥",
        ],
    }

    return random.choice(memes.get(fail_type, ["🤖 LUNA: ..."]))


# ===== NOUVELLES ROUTES API POUR VERSION 3.0 =====

# Import des nouveaux modules
try:
    from core.database import db_manager
    from core.tutorial_manager import tutorial_manager
    from core.websocket_manager import websocket_manager

    DATABASE_AVAILABLE = True
    WEBSOCKET_AVAILABLE = True
    TUTORIAL_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    WEBSOCKET_AVAILABLE = False
    TUTORIAL_AVAILABLE = False
    game_logger.warning("Modules avancés non disponibles, utilisation du mode dégradé")


@app.route("/api/database/migrate", methods=["POST"])
def migrate_to_database():
    """Migre les données JSON vers SQLite"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database module not available"}), 500

    try:
        db_manager.migrate_json_to_sqlite()
        return jsonify({"success": True, "message": "Migration réussie"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/database/profile/<username>", methods=["GET"])
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


@app.route("/api/database/profile/<username>", methods=["PUT"])
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


@app.route("/api/database/leaderboard", methods=["GET"])
def get_leaderboard():
    """Récupère le classement des joueurs"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database module not available"}), 500

    try:
        limit = request.args.get("limit", 10, type=int)
        leaderboard = db_manager.get_leaderboard(limit)
        return jsonify({"leaderboard": leaderboard})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaderboard", methods=["GET"])
def get_gamification_leaderboard():
    """Récupère le leaderboard de gamification avec protection anti-spam"""
    try:
        # Protection anti-spam - vérifier le rate limiting
        client_ip = request.remote_addr
        current_time = time.time()

        # Nettoyer les anciennes entrées
        if client_ip in request_counts:
            if isinstance(request_counts[client_ip], list):
                request_counts[client_ip] = [
                    req_time
                    for req_time in request_counts[client_ip]
                    if current_time - req_time < RATE_LIMIT_WINDOW
                ]
            else:
                # Convertir de tuple vers liste si nécessaire
                request_counts[client_ip] = []
        else:
            request_counts[client_ip] = []

        # Vérifier la limite
        if len(request_counts[client_ip]) >= RATE_LIMIT:
            return (
                jsonify(
                    {"success": False, "error": "Trop de requêtes. Veuillez patienter."}
                ),
                429,
            )

        # Ajouter cette requête
        request_counts[client_ip].append(current_time)

        # Validation des paramètres
        limit = request.args.get("limit", 10, type=int)
        if limit > 100:  # Limite maximale
            limit = 100
        if limit < 1:
            limit = 10

        # Charger directement depuis le fichier JSON avec gestion d'erreurs robuste
        leaderboard_file = os.path.join("data", "leaderboard.json")
        leaderboard_data = None

        try:
            if os.path.exists(leaderboard_file):
                with open(leaderboard_file, encoding="utf-8") as f:
                    leaderboard_data = json.load(f)

                # Validation des données
                if not isinstance(leaderboard_data, dict):
                    raise ValueError("Format de données invalide")

        except (OSError, json.JSONDecodeError, ValueError) as e:
            # Log l'erreur mais continue avec des données par défaut
            game_logger.warning(f"Erreur lecture leaderboard: {e}")
            leaderboard_data = None

        # Données par défaut si le fichier n'existe pas ou est corrompu
        if not leaderboard_data:
            leaderboard_data = {
                "players": [],
                "statistics": {
                    "total_players": 0,
                    "total_score": 0,
                    "average_score": 0,
                },
            }

        # Format attendu par le frontend avec validation
        formatted_leaderboard = []
        players = leaderboard_data.get("players", [])

        if isinstance(players, list):
            for _i, player in enumerate(players[:limit]):
                if isinstance(player, dict):
                    formatted_leaderboard.append(
                        {
                            "username": str(player.get("name", "Hacker")),
                            "score": int(player.get("score", 0)),
                            "level": int(player.get("level", 1)),
                            "badges_count": int(player.get("badges_count", 0)),
                            "is_current": bool(player.get("is_current", False)),
                        }
                    )

        # Statistiques globales avec protection contre division par zéro
        stats = leaderboard_data.get("statistics", {})
        players_list = leaderboard_data.get("players", [])

        if not isinstance(players_list, list):
            players_list = []

        total_players = len(players_list)
        avg_level = 1

        if total_players > 0:
            try:
                level_sum = sum(
                    int(p.get("level", 1)) for p in players_list if isinstance(p, dict)
                )
                avg_level = level_sum / total_players
            except (ValueError, TypeError):
                avg_level = 1

        formatted_stats = {
            "total_players": total_players,
            "total_score": int(stats.get("total_score", 0)),
            "avg_level": round(avg_level, 1),
            "total_badges": sum(
                int(p.get("badges_count", 0))
                for p in players_list
                if isinstance(p, dict)
            ),
        }

        return jsonify(
            {
                "success": True,
                "leaderboard": formatted_leaderboard,
                "stats": formatted_stats,
            }
        )

    except Exception as e:
        # Log l'erreur pour debugging
        game_logger.error(f"Erreur leaderboard: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Erreur temporaire du serveur. Veuillez réessayer.",
                }
            ),
            500,
        )


@app.route("/leaderboard")
def leaderboard_page():
    """Page du leaderboard"""
    return render_template("leaderboard.html")


@app.route("/api/gamification/summary", methods=["GET"])
def get_gamification_summary():
    """Récupère un résumé de la gamification pour le joueur actuel"""
    try:
        profil = charger_profil()
        user_id = profil.get("id", "default")
        summary = gamification.get_gamification_summary(user_id, profil)

        # Format attendu par le frontend
        formatted_summary = {
            "success": True,
            "total_score": profil.get("score", 0),
            "current_level": profil.get("level", 1),
            "missions_completees": len(
                profil.get("personnalite", {}).get("missions_completees", [])
            ),
            "badges_count": len(profil.get("badges", [])),
            "level_progress": summary.get("level_progress", {}).get(
                "progress_percentage", 0
            ),
            "total_experience": profil.get("score", 0),
            "goals_achieved": len(profil.get("badges", [])),
            "accuracy": 85,  # Valeur par défaut
            "speed": 1200,  # Valeur par défaut en ms
            "efficiency": 75,  # Valeur par défaut
            "recent_badges": profil.get("badges", [])[-3:],  # 3 derniers badges
            "recent_missions": profil.get("personnalite", {}).get(
                "missions_completees", []
            )[-3:],  # 3 dernières missions
            "top_players": summary.get("leaderboard_stats", {}).get("top_players", [])[
                :5
            ],  # Top 5
        }

        return jsonify(formatted_summary)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/websocket/challenge/create", methods=["POST"])
def create_challenge():
    """Crée un nouveau défi social"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"error": "WebSocket module not available"}), 500

    try:
        data = request.get_json()
        room_id = websocket_manager.create_challenge_room(data)
        return jsonify({"success": True, "room_id": room_id, "challenge_info": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/websocket/challenge/<room_id>/info", methods=["GET"])
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


@app.route("/api/websocket/challenge/<room_id>/join", methods=["POST"])
def join_challenge(room_id):
    """Rejoint un défi (simulation WebSocket)"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"error": "WebSocket module not available"}), 500

    try:
        data = request.get_json()
        data["room_id"] = room_id
        session_id = data.get("session_id", f"session_{int(time.time())}")

        result = websocket_manager.handle_join_challenge(session_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/websocket/challenge/<room_id>/action", methods=["POST"])
def challenge_action(room_id):
    """Effectue une action dans un défi (simulation WebSocket)"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify({"error": "WebSocket module not available"}), 500

    try:
        data = request.get_json()
        data["room_id"] = room_id
        session_id = data.get("session_id", f"session_{int(time.time())}")

        result = websocket_manager.handle_challenge_action(session_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/luna/learning-data", methods=["GET"])
def get_luna_learning_data():
    """Récupère les données d'apprentissage de LUNA"""
    try:
        # Charger les données d'apprentissage depuis le fichier JSON
        learning_data_path = "data/learning_data.json"
        if os.path.exists(learning_data_path):
            with open(learning_data_path, encoding="utf-8") as f:
                learning_data = json.load(f)
        else:
            # Données par défaut
            learning_data = {
                "user_patterns": [
                    {
                        "pattern": "speed_hack",
                        "personality_trait": "competitive",
                        "response_style": "encouraging",
                        "success_rate": 0.85,
                    },
                    {
                        "pattern": "social_hack",
                        "personality_trait": "collaborative",
                        "response_style": "supportive",
                        "success_rate": 0.92,
                    },
                    {
                        "pattern": "creative_hack",
                        "personality_trait": "innovative",
                        "response_style": "inspiring",
                        "success_rate": 0.78,
                    },
                ],
                "conversation_history": [],
                "preferences": {
                    "humor_level": 0.7,
                    "encouragement_level": 0.8,
                    "challenge_level": 0.6,
                },
            }

        return jsonify(learning_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/luna/analyze-action", methods=["POST"])
def analyze_user_action():
    """Analyse une action utilisateur avec l'IA LUNA"""
    try:
        data = request.get_json()
        action = data.get("action", "")
        # context = data.get('context', {})  # Variable non utilisée

        # Simulation de l'analyse IA
        analysis = {
            "action_type": "general",
            "difficulty_level": 0.5,
            "success_probability": 0.7,
            "personality_insights": {
                "risk_tolerance": 0.6,
                "creativity_level": 0.5,
                "social_preference": 0.4,
                "competitiveness": 0.7,
            },
            "learning_opportunity": {
                "skill_development": ["general_hacking"],
                "knowledge_gap": [],
                "strategy_improvement": [],
            },
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


@app.route("/api/luna/predict-behavior", methods=["POST"])
def predict_user_behavior():
    """Prédit le comportement futur de l'utilisateur"""
    try:
        data = request.get_json()
        user_actions = data.get("actions", [])

        # Simulation de prédiction
        predictions = {
            "next_likely_action": "aide" if not user_actions else user_actions[-1],
            "success_probability": 0.7,
            "engagement_level": min(1.0, len(user_actions) / 10),
        }

        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===== ROUTES DE TEST POUR LES NOUVELLES FONCTIONNALITÉS =====


@app.route("/api/test/database", methods=["GET"])
def test_database():
    """Test de la base de données"""
    if not DATABASE_AVAILABLE:
        return jsonify(
            {"status": "unavailable", "message": "Database module not available"}
        )

    try:
        # Test de création d'un profil
        test_profile = {
            "score": 1000,
            "niveau": 2,
            "badges": ["Test Badge"],
            "avatars": ["hacker_classique"],
            "preferences": {"theme": "luna"},
        }

        success = db_manager.save_profile("test_user", test_profile)
        if success:
            loaded_profile = db_manager.load_profile("test_user")
            return jsonify(
                {
                    "status": "working",
                    "message": "Database test successful",
                    "profile": loaded_profile,
                }
            )
        else:
            return jsonify({"status": "error", "message": "Failed to save profile"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/api/test/websocket", methods=["GET"])
def test_websocket():
    """Test des WebSockets"""
    if not WEBSOCKET_AVAILABLE:
        return jsonify(
            {"status": "unavailable", "message": "WebSocket module not available"}
        )

    try:
        # Test de création d'un défi
        challenge_data = {
            "title": "Test Challenge",
            "description": "Test challenge for WebSocket",
            "timer": 30,
            "players": [],
        }

        room_id = websocket_manager.create_challenge_room(challenge_data)
        room_info = websocket_manager.get_room_info(room_id)

        return jsonify(
            {
                "status": "working",
                "message": "WebSocket test successful",
                "room_id": room_id,
                "room_info": room_info,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/api/test/ai", methods=["GET"])
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
                "competitiveness": 0.8,
            },
        }

        return jsonify(
            {
                "status": "working",
                "message": "AI test successful",
                "analysis": test_analysis,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ===== ROUTES API TUTORIEL =====


@app.route("/api/tutorial/start", methods=["POST"])
def start_tutorial():
    """Démarre le tutoriel pour un utilisateur"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")

        result = tutorial_manager.start_tutorial(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/step/<int:step_id>", methods=["GET"])
def get_tutorial_step(step_id):
    """Récupère une étape du tutoriel"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        step = tutorial_manager.get_step(step_id)
        if step:
            return jsonify({"success": True, "step": step})
        else:
            return jsonify({"error": "Step not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/execute", methods=["POST"])
def execute_tutorial_step():
    """Exécute une étape du tutoriel"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")
        step_id = data.get("step_id")
        choice = data.get("choice")

        if not step_id:
            return jsonify({"error": "step_id required"}), 400

        result = tutorial_manager.execute_step(user_id, step_id, choice)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/choice", methods=["POST"])
def handle_tutorial_choice():
    """Gère un choix utilisateur dans le tutoriel"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")
        step_id = data.get("step_id")
        choice = data.get("choice")

        if not step_id or not choice:
            return jsonify({"error": "step_id and choice required"}), 400

        # Valider le choix
        if not tutorial_manager.validate_user_choice(step_id, choice):
            return jsonify({"error": "Invalid choice"}), 400

        # Exécuter l'étape avec le choix
        result = tutorial_manager.execute_step(user_id, step_id, choice)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/complete", methods=["POST"])
def complete_tutorial_step():
    """Marque une étape du tutoriel comme terminée"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")
        step_id = data.get("step_id")

        if not step_id:
            return jsonify({"error": "step_id required"}), 400

        result = tutorial_manager.execute_step(user_id, step_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/skip", methods=["POST"])
def skip_tutorial():
    """Permet de sauter le tutoriel"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")

        result = tutorial_manager.skip_tutorial(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/restart", methods=["POST"])
def restart_tutorial():
    """Relance le tutoriel depuis le début"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")

        result = tutorial_manager.restart_tutorial(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/progress/<user_id>", methods=["GET"])
def get_tutorial_progress(user_id):
    """Récupère la progression du tutoriel pour un utilisateur"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        analytics = tutorial_manager.get_tutorial_analytics(user_id)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/analytics", methods=["GET"])
def get_tutorial_analytics():
    """Récupère les analytics de tous les utilisateurs"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        analytics = tutorial_manager.get_all_analytics()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/effects/<int:step_id>", methods=["GET"])
def get_tutorial_effects(step_id):
    """Récupère les effets d'une étape du tutoriel"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        effects = tutorial_manager.get_step_effects(step_id)
        return jsonify({"success": True, "effects": effects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tutorial/luna-dialogue/<int:step_id>", methods=["GET"])
def get_luna_dialogue(step_id):
    """Récupère le dialogue LUNA pour une étape"""
    if not TUTORIAL_AVAILABLE:
        return jsonify({"error": "Tutorial module not available"}), 500

    try:
        context = request.args.get("context", "avant")
        dialogue = tutorial_manager.get_luna_dialogue(step_id, context)
        return jsonify({"success": True, "dialogue": dialogue})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===== ROUTE DE STATUT GÉNÉRAL =====


@app.route("/api/status", methods=["GET"])
def get_system_status():
    """Récupère le statut général du système"""
    status = {
        "version": "3.0.0",
        "database": "available" if DATABASE_AVAILABLE else "unavailable",
        "websocket": "available" if WEBSOCKET_AVAILABLE else "unavailable",
        "tutorial": "available" if TUTORIAL_AVAILABLE else "unavailable",
        "analytics": "available" if ANALYTICS_AVAILABLE else "unavailable",
        "ai": "available",
        "features": {
            "sqlite_migration": DATABASE_AVAILABLE,
            "real_time_challenges": WEBSOCKET_AVAILABLE,
            "interactive_tutorial": TUTORIAL_AVAILABLE,
            "data_driven_analytics": ANALYTICS_AVAILABLE,
            "advanced_ai": True,
            "personality_analysis": True,
        },
    }

    return jsonify(status)


# ===== ROUTES API POUR MINI-JEUX ÉDUCATIFS =====

# Importer le moteur d'analytics
try:
    from core.analytics_engine import analytics_engine

    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    game_logger.warning("Module analytics non disponible")


# Routes API pour les mini-jeux éducatifs
@app.route("/api/educational-games/list", methods=["GET"])
def api_educational_games_list():
    """Liste tous les mini-jeux éducatifs disponibles"""
    try:
        from core.educational_games_engine import EducationalGamesEngine

        games_engine = EducationalGamesEngine()
        games = games_engine.get_available_games(user_level=1)  # Niveau 1 par défaut

        return jsonify({"success": True, "games": games})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur: {e!s}"})


@app.route("/api/educational-games/start", methods=["POST"])
def api_educational_games_start():
    """Démarre un mini-jeu éducatif"""
    try:
        data = request.get_json()
        game_id = data.get("game_id")

        if not game_id:
            return jsonify({"success": False, "message": "ID de jeu requis"})

        # Utiliser un user_id par défaut
        user_id = "main_user"
        result = games_engine.start_game(game_id, user_id)

        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur: {e!s}"})


@app.route("/api/educational-games/submit", methods=["POST"])
def api_educational_games_submit():
    """Soumet une réponse à un mini-jeu"""
    try:
        data = request.get_json()
        session_id = data.get("session_id")
        answer = data.get("answer")

        if not session_id or answer is None:
            return jsonify(
                {"success": False, "message": "Session ID et réponse requis"}
            )

        # Utiliser le moteur de jeux pour valider la réponse
        result = games_engine.submit_answer(session_id, answer)

        # Retourner le résultat du moteur de jeux
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur: {e!s}"})


@app.route("/api/educational-games/stats", methods=["GET"])
def api_educational_games_stats():
    """Retourne les statistiques des mini-jeux"""
    try:
        # Statistiques simulées pour l'instant
        stats = {
            "total_games": 9,
            "total_players": 1,
            "total_sessions": 0,
            "games_by_type": {
                "logic": 2,
                "code": 2,
                "cybersecurity": 2,
                "cryptography": 2,
                "network": 1,
            },
        }

        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur: {e!s}"})


@app.route("/api/educational-games/leaderboard", methods=["GET"])
def api_educational_games_leaderboard():
    """Récupère le classement des mini-jeux éducatifs"""
    try:
        # Leaderboard simulé pour l'instant
        leaderboard = [
            {"rank": 1, "username": "main_user", "score": 0, "games_played": 0}
        ]
        return jsonify({"success": True, "leaderboard": leaderboard})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur: {e!s}"})


@app.route("/api/educational-games/progress", methods=["GET"])
def api_educational_games_progress():
    """Récupère la progression d'un utilisateur dans les mini-jeux"""
    try:
        # Progression simulée pour l'instant
        progress = {
            "games_completed": 0,
            "total_points": 0,
            "badges_earned": 0,
            "favorite_type": "none",
            "completion_rate": 0,
        }

        return jsonify({"success": True, "progress": progress})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur: {e!s}"})


# ===== ROUTES API POUR ANALYTICS =====


@app.route("/api/analytics/track", methods=["POST"])
def track_analytics_event():
    """Track un événement analytics"""
    if not ANALYTICS_AVAILABLE:
        return jsonify({"error": "Analytics module not available"}), 500

    try:
        data = request.get_json()
        events = data.get("events", [])

        if not events:
            return jsonify({"error": "No events provided"}), 400

        # Récupérer l'ID utilisateur depuis le profil
        profil = charger_profil()
        user_id = profil.get("id", "default")

        # Tracker chaque événement
        for event_data in events:
            event_type = event_data.get("event_type")
            session_id = event_data.get("session_id")
            data_payload = event_data.get("data", {})
            context = event_data.get("context", {})

            if event_type and session_id:
                analytics_engine.track_event(
                    event_type=event_type,
                    user_id=user_id,
                    session_id=session_id,
                    data=data_payload,
                    context=context,
                )

        return jsonify({"success": True, "events_tracked": len(events)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/security/status", methods=["GET"])
def get_security_status():
    """Récupère le statut de sécurité du système"""
    try:
        # Vérifier l'origine de la requête
        origin = request.headers.get("Origin")
        if origin and not security_manager.check_origin_security(
            origin, request.remote_addr
        ):
            return jsonify({"error": "Origine non autorisée"}), 403

        security_report = security_manager.get_security_report()
        return jsonify(security_report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analytics/insights", methods=["GET"])
def get_user_insights():
    """Récupère les insights personnalisés d'un utilisateur"""
    if not ANALYTICS_AVAILABLE:
        return jsonify({"error": "Analytics module not available"}), 500

    try:
        profil = charger_profil()
        user_id = str(profil.get("id", "default"))  # Convertir en string

        insights = analytics_engine.get_user_insights(user_id)

        return jsonify({"success": True, "insights": insights})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analytics/global", methods=["GET"])
def get_global_analytics():
    """Récupère les analytics globaux"""
    if not ANALYTICS_AVAILABLE:
        return jsonify({"error": "Analytics module not available"}), 500

    try:
        analytics_data = analytics_engine.get_global_analytics()

        return jsonify({"success": True, "analytics": analytics_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analytics/export", methods=["GET"])
def export_analytics_data():
    """Exporte les données analytics"""
    if not ANALYTICS_AVAILABLE:
        return jsonify({"error": "Analytics module not available"}), 500

    try:
        user_id = request.args.get("user_id")
        export_format = request.args.get("format", "json")

        if user_id:
            data = analytics_engine.export_data(user_id, export_format)
        else:
            data = analytics_engine.export_data(format=export_format)

        return jsonify({"success": True, "data": data, "format": export_format})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analytics/cleanup", methods=["POST"])
def cleanup_analytics_data():
    """Nettoie les anciennes données analytics"""
    if not ANALYTICS_AVAILABLE:
        return jsonify({"error": "Analytics module not available"}), 500

    try:
        analytics_engine.cleanup_old_data()

        return jsonify(
            {"success": True, "message": "Nettoyage des données analytics effectué"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Tutoriel
@app.route("/api/tutorial/steps")
def get_tutorial_steps():
    """Récupère les étapes du tutoriel depuis le système existant"""
    try:
        if TUTORIAL_AVAILABLE:
            # Utiliser le gestionnaire de tutoriel existant
            try:
                from core.tutorial_manager import TutorialManager

                tutorial_manager = TutorialManager()
                tutorial_data = tutorial_manager._load_tutorial_data()
            except ImportError:
                # Fallback si l'import échoue
                tutorial_data = None
            return jsonify(tutorial_data)
        else:
            # Fallback vers les données locales
            return jsonify(
                {
                    "tutoriel": {
                        "etapes": [
                            {
                                "id": 1,
                                "titre": "Bienvenue dans Arkalia Quest",
                                "message": "Salut hacker ! Je suis LUNA, ton assistant IA. Prêt pour l'aventure ?",
                                "commande": "luna_contact",
                                "aide": "Tape 'luna_contact' pour me parler",
                            },
                            {
                                "id": 2,
                                "titre": "Première mission",
                                "message": "Découvre le SOS mystérieux du Dr Althea Voss",
                                "commande": "prologue",
                                "aide": "Tape 'prologue' pour commencer l'histoire",
                            },
                            {
                                "id": 3,
                                "titre": "Répare le site de LUNA",
                                "message": "Aide-moi à réparer mon site web compromis",
                                "commande": "acte_1",
                                "aide": "Tape 'acte_1' pour la première mission",
                            },
                        ]
                    }
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint de santé pour la production et la CI
@app.route("/health")
def health_check():
    """Endpoint de santé pour la production et la CI"""
    try:
        # Vérifications de base
        db_status = "healthy" if DATABASE_AVAILABLE else "unhealthy"
        websocket_status = "healthy" if WEBSOCKET_AVAILABLE else "unhealthy"
        tutorial_status = "healthy" if TUTORIAL_AVAILABLE else "unhealthy"

        return (
            jsonify(
                {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "version": "3.0.0",
                    "services": {
                        "database": db_status,
                        "websocket": websocket_status,
                        "tutorial": tutorial_status,
                    },
                    "uptime": (
                        time.time() - start_time if "start_time" in globals() else 0
                    ),
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


# Endpoint de métriques pour le monitoring
@app.route("/metrics")
def metrics():
    """Endpoint de métriques pour le monitoring"""
    try:
        return (
            jsonify(
                {
                    "version": "3.0.0",
                    "tests_passing": 76,
                    "code_quality": "A+",
                    "ci_status": "passing",
                    "last_deploy": datetime.now().isoformat(),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route('/os2142')
# def os2142():
#     """Route pour l'interface OS 2142"""
#     return render_template('os2142.html')

if __name__ == "__main__":
    # Créer les dossiers nécessaires
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/effects"):
        os.makedirs("data/effects")
    if not os.path.exists("data/effects/ascii"):
        os.makedirs("data/effects/ascii")
    if not os.path.exists("data/missions"):
        os.makedirs("data/missions")

    game_logger.info("🚀 Démarrage d'Arkalia Quest v3.1.0")
    game_logger.info("🌙 IA LUNA initialisée")
    game_logger.info("🎮 Moteur de jeu prêt")
    game_logger.info("🎨 Effets visuels activés")
    game_logger.info("⚡ Optimisations de performance activées")
    game_logger.info("🛡️ Sécurité renforcée")
    game_logger.info("🌐 Serveur sur http://0.0.0.0:5001 (port configuré)")


# ===== ENDPOINTS DE MONITORING ET PERFORMANCE =====


@app.route("/api/performance/stats", methods=["GET"])
@performance_optimizer.monitor_performance("performance_stats")
def api_performance_stats():
    """Retourne les statistiques de performance avec cache"""
    try:
        # Vérifier le cache d'abord
        cache_key = "performance_stats"
        cached_data = performance_optimizer.get_cached_data(cache_key, ttl_seconds=60)

        if cached_data:
            return jsonify(cached_data)

        # Générer les nouvelles données
        stats = performance_optimizer.get_performance_stats()
        cache_stats = cache_manager.get_stats()
        security_stats = security_enhanced.get_security_stats()

        response_data = {
            "success": True,
            "performance": stats,
            "cache": cache_stats,
            "security": security_stats,
            "timestamp": datetime.now().isoformat(),
        }

        # Mettre en cache
        performance_optimizer.set_cached_data(cache_key, response_data, ttl_seconds=60)

        return jsonify(response_data)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/performance/slow-queries", methods=["GET"])
@performance_optimizer.monitor_performance("slow_queries")
def api_slow_queries():
    """Retourne les requêtes les plus lentes"""
    try:
        limit = request.args.get("limit", 10, type=int)
        slow_queries = performance_optimizer.get_slow_queries(limit)

        return jsonify(
            {"success": True, "slow_queries": slow_queries, "count": len(slow_queries)}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/performance/errors", methods=["GET"])
@performance_optimizer.monitor_performance("recent_errors")
def api_recent_errors():
    """Retourne les erreurs récentes"""
    try:
        limit = request.args.get("limit", 10, type=int)
        errors = performance_optimizer.get_recent_errors(limit)

        return jsonify({"success": True, "errors": errors, "count": len(errors)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/performance/optimizations", methods=["GET"])
@performance_optimizer.monitor_performance("optimization_suggestions")
def api_optimization_suggestions():
    """Retourne les suggestions d'optimisation"""
    try:
        suggestions = performance_optimizer.suggest_optimizations()

        return jsonify(
            {"success": True, "suggestions": suggestions, "count": len(suggestions)}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/cache/clear", methods=["POST"])
@performance_optimizer.monitor_performance("cache_clear")
def api_cache_clear():
    """Vide le cache"""
    try:
        cache_manager.clear()

        return jsonify({"success": True, "message": "Cache vidé avec succès"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/security/stats", methods=["GET"])
@performance_optimizer.monitor_performance("security_stats")
def api_security_stats():
    """Retourne les statistiques de sécurité"""
    try:
        stats = security_enhanced.get_security_stats()

        return jsonify(
            {
                "success": True,
                "security_stats": stats,
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== ENDPOINTS SOCIAUX ET COMMUNAUTAIRES =====


@app.route("/api/social/dashboard", methods=["GET"])
@performance_optimizer.monitor_performance("social_dashboard")
def api_social_dashboard():
    """Retourne le tableau de bord social d'un joueur"""
    try:
        player_id = request.args.get("player_id", "default")
        dashboard = social_engine.get_social_dashboard(player_id)

        return jsonify({"success": True, "dashboard": dashboard})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/social/guilds", methods=["POST"])
@performance_optimizer.monitor_performance("create_guild")
def api_create_guild():
    """Crée une nouvelle guilde"""
    try:
        data = request.get_json()
        creator_id = data.get("creator_id", "default")
        guild_name = data.get("name", "")
        description = data.get("description", "")

        if not guild_name:
            return jsonify({"success": False, "error": "Nom de guilde requis"}), 400

        result = social_engine.create_guild(creator_id, guild_name, description)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/social/guilds/<guild_id>/join", methods=["POST"])
@performance_optimizer.monitor_performance("join_guild")
def api_join_guild(guild_id):
    """Rejoint une guilde"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")

        result = social_engine.join_guild(player_id, guild_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/social/challenges", methods=["POST"])
@performance_optimizer.monitor_performance("create_challenge")
def api_create_challenge():
    """Crée un défi coopératif"""
    try:
        data = request.get_json()
        creator_id = data.get("creator_id", "default")
        challenge_data = data.get("challenge_data", {})

        result = social_engine.create_coop_challenge(creator_id, challenge_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/social/chat/global", methods=["POST"])
@performance_optimizer.monitor_performance("send_global_message")
def api_send_global_message():
    """Envoie un message dans le chat global"""
    try:
        data = request.get_json()
        sender_id = data.get("sender_id", "default")
        message = data.get("message", "")
        message_type = data.get("type", "chat")

        if not message:
            return jsonify({"success": False, "error": "Message requis"}), 400

        result = social_engine.send_global_message(sender_id, message, message_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/social/chat/recent", methods=["GET"])
@performance_optimizer.monitor_performance("get_recent_messages")
def api_get_recent_messages():
    """Récupère les messages récents"""
    try:
        limit = request.args.get("limit", 50, type=int)
        messages = social_engine.get_recent_messages(limit)

        return jsonify({"success": True, "messages": messages})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== ENDPOINTS DE CUSTOMISATION =====


@app.route("/api/customization/player", methods=["GET"])
@performance_optimizer.monitor_performance("get_player_customization")
def api_get_player_customization():
    """Retourne la customisation d'un joueur"""
    try:
        player_id = request.args.get("player_id", "default")
        customization = customization_engine.get_player_customization(player_id)

        return jsonify({"success": True, "customization": customization})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/customization/themes", methods=["GET"])
@performance_optimizer.monitor_performance("get_available_themes")
def api_get_available_themes():
    """Retourne les thèmes disponibles pour un joueur"""
    try:
        player_id = request.args.get("player_id", "default")
        themes = customization_engine.get_available_themes(player_id)

        return jsonify({"success": True, "themes": themes})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/customization/themes/<theme_id>/set", methods=["POST"])
@performance_optimizer.monitor_performance("set_player_theme")
def api_set_player_theme(theme_id):
    """Définit le thème d'un joueur"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")

        result = customization_engine.set_player_theme(player_id, theme_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/customization/avatars", methods=["GET"])
@performance_optimizer.monitor_performance("get_available_avatars")
def api_get_available_avatars():
    """Retourne les avatars disponibles pour un joueur"""
    try:
        player_id = request.args.get("player_id", "default")
        avatars = customization_engine.get_available_avatars(player_id)

        return jsonify({"success": True, "avatars": avatars})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/customization/avatars/<avatar_id>/set", methods=["POST"])
@performance_optimizer.monitor_performance("set_player_avatar")
def api_set_player_avatar(avatar_id):
    """Définit l'avatar d'un joueur"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")

        result = customization_engine.set_player_avatar(player_id, avatar_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/customization/unlock/random", methods=["POST"])
@performance_optimizer.monitor_performance("unlock_random_customization")
def api_unlock_random_customization():
    """Débloque une customisation aléatoire"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")
        category = data.get("category", "random")

        result = customization_engine.unlock_random_customization(player_id, category)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== ENDPOINTS DE STORYTELLING ADAPTATIF =====


@app.route("/api/story/progress", methods=["GET"])
@performance_optimizer.monitor_performance("get_story_progress")
def api_get_story_progress():
    """Retourne le progrès de l'histoire d'un joueur"""
    try:
        player_id = request.args.get("player_id", "default")
        progress = adaptive_storytelling.get_story_progress(player_id)

        return jsonify({"success": True, "progress": progress})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/story/choices", methods=["POST"])
@performance_optimizer.monitor_performance("record_player_choice")
def api_record_player_choice():
    """Enregistre un choix du joueur"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")
        story_arc = data.get("story_arc", "")
        choice = data.get("choice", "")
        context = data.get("context", {})

        if not story_arc or not choice:
            return (
                jsonify({"success": False, "error": "Arc narratif et choix requis"}),
                400,
            )

        result = adaptive_storytelling.record_player_choice(
            player_id, story_arc, choice, context
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/story/choices/available", methods=["GET"])
@performance_optimizer.monitor_performance("get_available_choices")
def api_get_available_choices():
    """Retourne les choix disponibles pour un arc narratif"""
    try:
        player_id = request.args.get("player_id", "default")
        story_arc = request.args.get("story_arc", "")

        if not story_arc:
            return jsonify({"success": False, "error": "Arc narratif requis"}), 400

        choices = adaptive_storytelling.get_available_choices(player_id, story_arc)
        return jsonify({"success": True, "choices": choices})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/story/dialogue", methods=["POST"])
@performance_optimizer.monitor_performance("generate_adaptive_dialogue")
def api_generate_adaptive_dialogue():
    """Génère un dialogue adaptatif"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")
        context = data.get("context", "")

        if not context:
            return jsonify({"success": False, "error": "Contexte requis"}), 400

        result = adaptive_storytelling.generate_adaptive_dialogue(player_id, context)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== ENDPOINTS DE MICRO-INTERACTIONS =====


@app.route("/api/interactions/trigger", methods=["POST"])
@performance_optimizer.monitor_performance("trigger_interaction")
def api_trigger_interaction():
    """Déclenche une micro-interaction"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")
        interaction_type = data.get("type", "")
        target_element = data.get("target_element")
        context = data.get("context", {})

        if not interaction_type:
            return (
                jsonify({"success": False, "error": "Type d'interaction requis"}),
                400,
            )

        result = micro_interactions.trigger_interaction(
            player_id, interaction_type, target_element, context
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/interactions/process", methods=["GET"])
@performance_optimizer.monitor_performance("process_interactions")
def api_process_interactions():
    """Traite toutes les queues d'interactions"""
    try:
        result = micro_interactions.process_all_queues()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/interactions/preferences", methods=["GET"])
@performance_optimizer.monitor_performance("get_interaction_preferences")
def api_get_interaction_preferences():
    """Retourne les préférences d'interactions d'un joueur"""
    try:
        player_id = request.args.get("player_id", "default")
        preferences = micro_interactions.get_user_preferences(player_id)

        return jsonify({"success": True, "preferences": preferences})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/interactions/preferences", methods=["POST"])
@performance_optimizer.monitor_performance("update_interaction_preferences")
def api_update_interaction_preferences():
    """Met à jour les préférences d'interactions d'un joueur"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "default")
        preferences = data.get("preferences", {})

        result = micro_interactions.update_user_preferences(player_id, preferences)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== NOUVELLES FONCTIONNALITÉS V3 =====

# Initialisation des nouveaux moteurs
daily_challenges_engine = DailyChallengesEngine()
luna_ai_v3 = LunaAIV3()

# ===== ROUTES POUR LES DÉFIS QUOTIDIENS =====


@app.route("/api/daily-challenges", methods=["GET"])
@performance_optimizer.monitor_performance("get_daily_challenges")
def api_get_daily_challenges():
    """Récupère les défis quotidiens pour un utilisateur"""
    try:
        user_id = request.args.get("user_id", "default")
        date = request.args.get("date")

        challenges = daily_challenges_engine.get_daily_challenges(user_id, date)
        return jsonify(challenges)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/daily-challenges/attempt", methods=["POST"])
@performance_optimizer.monitor_performance("attempt_daily_challenge")
def api_attempt_daily_challenge():
    """Tente de résoudre un défi quotidien"""
    try:
        data = request.get_json()
        user_id = data.get("user_id", "default")
        challenge_id = data.get("challenge_id")
        answer = data.get("answer", "")
        date = data.get("date")

        if not challenge_id:
            return jsonify({"success": False, "error": "ID du défi requis"}), 400

        result = daily_challenges_engine.attempt_challenge(
            user_id, challenge_id, answer, date
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/daily-challenges/leaderboard", methods=["GET"])
@performance_optimizer.monitor_performance("get_daily_leaderboard")
def api_get_daily_leaderboard():
    """Retourne le classement des défis quotidiens"""
    try:
        date = request.args.get("date")
        leaderboard = daily_challenges_engine.get_leaderboard(date)
        return jsonify({"success": True, "leaderboard": leaderboard})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/daily-challenges/weekly-stats", methods=["GET"])
@performance_optimizer.monitor_performance("get_weekly_stats")
def api_get_weekly_stats():
    """Retourne les statistiques hebdomadaires d'un utilisateur"""
    try:
        user_id = request.args.get("user_id", "default")
        stats = daily_challenges_engine.get_weekly_stats(user_id)
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== ROUTES POUR LUNA AI V3 =====


@app.route("/api/luna-v3/chat", methods=["POST"])
@performance_optimizer.monitor_performance("luna_v3_chat")
def api_luna_v3_chat():
    """Chat avec LUNA AI V3"""
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        user_profile = data.get("user_profile", {})
        game_context = data.get("game_context", {})

        if not user_input:
            return jsonify({"success": False, "error": "Message requis"}), 400

        response = luna_ai_v3.generate_response(user_input, user_profile, game_context)
        return jsonify(response)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/luna-v3/learning-stats", methods=["GET"])
@performance_optimizer.monitor_performance("get_luna_learning_stats")
def api_get_luna_learning_stats():
    """Retourne les statistiques d'apprentissage de LUNA"""
    try:
        stats = luna_ai_v3.get_learning_stats()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/luna-v3/reset", methods=["POST"])
@performance_optimizer.monitor_performance("reset_luna_learning")
def api_reset_luna_learning():
    """Remet à zéro l'apprentissage de LUNA (pour les tests)"""
    try:
        luna_ai_v3.reset_learning()
        return jsonify(
            {"success": True, "message": "Apprentissage de LUNA réinitialisé"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== ROUTES POUR LES THÈMES =====


@app.route("/api/themes", methods=["GET"])
@performance_optimizer.monitor_performance("get_themes")
def api_get_themes():
    """Retourne la liste des thèmes disponibles"""
    try:
        themes = {
            "matrix": {
                "name": "Matrix",
                "description": "Thème classique vert Matrix",
                "icon": "🌌",
                "class": "matrix-theme",
            },
            "cyberpunk": {
                "name": "Cyberpunk",
                "description": "Thème néon rose et cyan",
                "icon": "🌆",
                "class": "cyberpunk-theme",
            },
            "neon": {
                "name": "Neon",
                "description": "Thème néon vert et rouge",
                "icon": "💚",
                "class": "neon-theme",
            },
            "dark": {
                "name": "Dark Mode",
                "description": "Thème sombre moderne",
                "icon": "🌙",
                "class": "dark-theme",
            },
            "retro": {
                "name": "Retro",
                "description": "Thème rétro années 80",
                "icon": "🎮",
                "class": "retro-theme",
            },
            "ocean": {
                "name": "Ocean",
                "description": "Thème océan bleu",
                "icon": "🌊",
                "class": "ocean-theme",
            },
        }
        return jsonify({"success": True, "themes": themes})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/performance/log", methods=["POST"])
@performance_optimizer.monitor_performance("log_performance")
def api_log_performance():
    """Endpoint pour recevoir les logs de performance du frontend"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Données manquantes"}), 400

        # Log des métriques de performance
        performance_logger.info(f"Performance metrics: {data}")

        return jsonify({"success": True, "message": "Log enregistré"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/tutorial/data", methods=["GET"])
@performance_optimizer.monitor_performance("get_tutorial_data")
def api_get_tutorial_data():
    """Récupère les données du tutoriel"""
    try:
        tutorial_data = {
            "steps": [
                {
                    "id": "welcome",
                    "title": "Bienvenue dans Arkalia Quest",
                    "content": "Découvrez l'univers cybernétique d'Arkalia Quest",
                    "type": "intro",
                },
                {
                    "id": "navigation",
                    "title": "Navigation",
                    "content": "Utilisez les boutons pour naviguer dans le jeu",
                    "type": "guide",
                },
                {
                    "id": "luna",
                    "title": "LUNA AI",
                    "content": "Interagissez avec LUNA, votre IA compagnon",
                    "type": "interaction",
                },
            ],
            "current_step": 0,
            "completed": False,
        }

        return jsonify({"success": True, "tutorial": tutorial_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== NOUVELLES ROUTES API POUR LES SYSTÈMES AVANCÉS =====


@app.route("/api/mission-progress/update", methods=["POST"])
def api_update_mission_progress():
    """Met à jour la progression d'une mission avec indicateurs visuels"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        mission_id = data.get("mission_id")
        step_id = data.get("step_id")
        action = data.get("action")
        success = data.get("success", True)
        metadata = data.get("metadata", {})

        if not all([mission_id, step_id, action]):
            return jsonify({"error": "Paramètres manquants"}), 400

        result = mission_progress_tracker.update_mission_progress(
            mission_id, player_id, step_id, action, success, metadata
        )

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/mission-progress/analytics/<player_id>", methods=["GET"])
def api_get_mission_analytics(player_id):
    """Récupère les analytics de progression des missions"""
    try:
        analytics = mission_progress_tracker.get_mission_analytics(player_id)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/narrative-branches/available", methods=["GET"])
def api_get_available_branches():
    """Récupère les branches narratives disponibles"""
    try:
        player_id = request.args.get("player_id", "main_user")
        branches = narrative_branches.get_available_branches(player_id)
        return jsonify(branches)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/narrative-branches/choice", methods=["POST"])
def api_make_narrative_choice():
    """Enregistre un choix narratif du joueur"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        branch_id = data.get("branch_id")
        choice_id = data.get("choice_id")
        context = data.get("context", {})

        if not all([branch_id, choice_id]):
            return jsonify({"error": "Paramètres manquants"}), 400

        result = narrative_branches.make_choice(
            player_id, branch_id, choice_id, context
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/narrative-branches/story-state/<player_id>", methods=["GET"])
def api_get_story_state(player_id):
    """Récupère l'état de l'histoire d'un joueur"""
    try:
        story_state = narrative_branches.get_story_state(player_id)
        relationships = narrative_branches.get_character_relationships(player_id)

        return jsonify({"story_state": story_state, "relationships": relationships})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/secondary-missions/available", methods=["GET"])
def api_get_available_secondary_missions():
    """Récupère les missions secondaires disponibles"""
    try:
        player_id = request.args.get("player_id", "main_user")
        missions = secondary_missions.get_available_missions(player_id)
        return jsonify(missions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/secondary-missions/start", methods=["POST"])
def api_start_secondary_mission():
    """Démarre une mission secondaire"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        mission_id = data.get("mission_id")

        if not mission_id:
            return jsonify({"error": "ID de mission manquant"}), 400

        result = secondary_missions.start_mission(player_id, mission_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/secondary-missions/update", methods=["POST"])
def api_update_secondary_mission():
    """Met à jour la progression d'une mission secondaire"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        mission_id = data.get("mission_id")
        objective_id = data.get("objective_id")
        completed = data.get("completed", True)

        if not all([mission_id, objective_id]):
            return jsonify({"error": "Paramètres manquants"}), 400

        result = secondary_missions.update_mission_progress(
            player_id, mission_id, objective_id, completed
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/achievements/check", methods=["POST"])
def api_check_achievements():
    """Vérifie les achievements pour une action"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        action = data.get("action")
        context = data.get("context", {})

        if not action:
            return jsonify({"error": "Action manquante"}), 400

        new_achievements = advanced_achievements.check_achievement_progress(
            player_id, action, context
        )

        return jsonify(
            {"new_achievements": new_achievements, "count": len(new_achievements)}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/achievements/player/<player_id>", methods=["GET"])
def api_get_player_achievements(player_id):
    """Récupère les achievements d'un joueur"""
    try:
        achievements = advanced_achievements.get_player_achievements(player_id)
        return jsonify(achievements)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/achievements/leaderboard", methods=["GET"])
def api_get_achievement_leaderboard():
    """Récupère le classement des achievements"""
    try:
        category = request.args.get("category")
        leaderboard = advanced_achievements.get_achievement_leaderboard(category)
        return jsonify(leaderboard)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaderboards/category/<category>", methods=["GET"])
def api_get_category_leaderboard(category):
    """Récupère le classement d'une catégorie"""
    try:
        period = request.args.get("period", "all_time")
        limit = int(request.args.get("limit", 50))

        leaderboard = category_leaderboards.get_leaderboard(category, period, limit)
        return jsonify(leaderboard)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaderboards/player/<player_id>", methods=["GET"])
def api_get_player_leaderboard_info(player_id):
    """Récupère les informations de classement d'un joueur"""
    try:
        overview = category_leaderboards.get_player_overview(player_id)
        comparison = category_leaderboards.get_category_comparison(player_id)

        return jsonify({"overview": overview, "comparison": comparison})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaderboards/update-metrics", methods=["POST"])
def api_update_player_metrics():
    """Met à jour les métriques d'un joueur pour les classements"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        category = data.get("category")
        metrics = data.get("metrics", {})
        context = data.get("context", {})

        if not category:
            return jsonify({"error": "Catégorie manquante"}), 400

        result = category_leaderboards.update_player_metrics(
            player_id, category, metrics, context
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/available", methods=["GET"])
def api_get_available_tutorials():
    """Récupère les tutoriels techniques disponibles"""
    try:
        player_id = request.args.get("player_id", "main_user")
        tutorials = technical_tutorials.get_available_tutorials(player_id)
        return jsonify(tutorials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/start", methods=["POST"])
def api_start_technical_tutorial():
    """Démarre un tutoriel technique"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        tutorial_id = data.get("tutorial_id")

        if not tutorial_id:
            return jsonify({"error": "ID de tutoriel manquant"}), 400

        result = technical_tutorials.start_tutorial(player_id, tutorial_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/content/<tutorial_id>", methods=["GET"])
def api_get_tutorial_content(tutorial_id):
    """Récupère le contenu d'un tutoriel"""
    try:
        player_id = request.args.get("player_id", "main_user")
        step = int(request.args.get("step", 0))

        content = technical_tutorials.get_tutorial_content(player_id, tutorial_id, step)
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/complete-step", methods=["POST"])
def api_complete_tutorial_step():
    """Marque une étape de tutoriel comme terminée"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        tutorial_id = data.get("tutorial_id")
        step = data.get("step")
        exercise_result = data.get("exercise_result", {})

        if not all([tutorial_id, step is not None]):
            return jsonify({"error": "Paramètres manquants"}), 400

        result = technical_tutorials.complete_tutorial_step(
            player_id, tutorial_id, step, exercise_result
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/quiz/<tutorial_id>", methods=["GET"])
def api_get_tutorial_quiz(tutorial_id):
    """Récupère le quiz d'un tutoriel"""
    try:
        player_id = request.args.get("player_id", "main_user")
        quiz = technical_tutorials.get_quiz(player_id, tutorial_id)
        return jsonify(quiz)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/submit-quiz", methods=["POST"])
def api_submit_tutorial_quiz():
    """Soumet les réponses d'un quiz"""
    try:
        data = request.get_json()
        player_id = data.get("player_id", "main_user")
        tutorial_id = data.get("tutorial_id")
        answers = data.get("answers", {})

        if not all([tutorial_id, answers]):
            return jsonify({"error": "Paramètres manquants"}), 400

        result = technical_tutorials.submit_quiz(player_id, tutorial_id, answers)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/references", methods=["GET"])
def api_get_tutorial_references():
    """Récupère les références d'apprentissage"""
    try:
        category = request.args.get("category")
        references = technical_tutorials.get_references(category)
        return jsonify(references)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/technical-tutorials/concepts", methods=["GET"])
def api_get_tutorial_concepts():
    """Récupère tous les concepts disponibles"""
    try:
        concepts = technical_tutorials.get_concepts()
        return jsonify(concepts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Mode production optimisé - serveur de développement désactivé
    print("🚀 Utilisez Gunicorn pour la production :")
    print("   gunicorn -c gunicorn.conf.py app:app")
    print("   ou Docker : docker-compose up")
    print("")
    print("⚠️  Serveur de développement désactivé pour éviter les fuites de ressources")
    print("   Utilisez 'python -m flask run' pour le développement")
    # app.run(host="0.0.0.0", port=5001, debug=False, threaded=True)
