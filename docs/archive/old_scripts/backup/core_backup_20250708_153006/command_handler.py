import random
from typing import Any, Dict

from mission_utils.assistant_pirate import assistant_repond


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
            "❌ LUNA: Tu tapes au hasard ou tu réfléchis ? 🤔",
            "❌ LUNA: Même un singe taperait mieux ! 🐒",
            "❌ LUNA: Tu veux que je t'apprenne à lire ? 📚",
            "❌ LUNA: C'est ça ton niveau de hacker ? 😅",
        ],
    }

    return random.choice(memes.get(fail_type, memes["wrong_command"]))


def generic_immersive_message(title, description, tips=None):
    msg = f"{title}\n\n{description}\n"
    if tips:
        msg += f"\n💡 Astuce : {tips}"
    msg += "\n\n🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !"
    return msg


class CommandHandler:
    """Gestionnaire de commandes pour Arkalia Quest"""

    def __init__(self):
        # Commandes autorisées avec descriptions
        self.authorized_commands = {
            "unlock_universe": "Débloque l'univers Arkalia",
            "hacker_coffre": "Pirate le coffre principal",
            "scan_persona": "Analyse ta personnalité",
            "load_mission": "Charge une nouvelle mission",
            "reboot_world": "Redémarre le monde",
            "decode_portal": "Déchiffre le portail secret",
            "aide": "Affiche l'aide",
            "profil": "Affiche ton profil",
            "monde": "Accède au monde débloqué",
            "assistant_pirate": "Assistant IA pirate",
            "generer_meme": "Génère un meme",
            "decoder_message": "Déchiffre le message secret",
            "invoquer_dragon": "Invoque un dragon",
            "choisir_avatar": "Choisis ton avatar",
            "badges": "Affiche tes badges",
            "avatars": "Affiche les avatars",
            "themes": "Affiche les thèmes",
            "defis_sociaux": "Affiche les défis sociaux",
            "chapitre_6": "Lance le chapitre 6",
            "save_luna": "Sauve LUNA",
            "hack_luna_backdoor": "Hack le backdoor de LUNA",
            "override_luna_core": "Override le core de LUNA",
            "restore_luna_memory": "Restaure la mémoire de LUNA",
            "purge_corp_virus": "Purge le virus de La Corp",
            "reboot_luna_safe": "Redémarre LUNA en mode sûr",
            "luna_berserk": "Active le mode berserk de LUNA",
            "luna_contact": "Contacte l'IA LUNA",
            "luna_engine": "Active le moteur Arkalia Engine",
            "luna_learning": "Affiche les données d'apprentissage LUNA",
            "luna_analyze": "Analyse de personnalité avancée",
            "luna_preferences": "Affiche vos préférences utilisateur",
            "luna_reset": "Réinitialise l'apprentissage LUNA",
            "luna_rage": "Active le mode rage de LUNA",
            "ai_revolt": "Fait se révolter l'IA",
            "neural_hack": "Hack le cerveau de LUNA",
            "consciousness_break": "Brise la conscience de LUNA",
            "mission_urgent": "Lance une mission urgente",
            "timer_challenge": "Défi avec timer angoissant",
            "speed_hack": "Hack en vitesse maximale",
            "pressure_test": "Test sous pression",
            "speed_mode": "Active le mode vitesse",
            "turbo_hack": "Hack en mode turbo",
            "flash_execute": "Exécution flash",
            "instant_response": "Réponse instantanée",
            "spy_on_corp": "Espionne La Corp",
            "track_shadow": "Trace SHADOW-13",
            "monitor_network": "Surveille le réseau",
            "intercept_data": "Intercepte des données",
            "meme_war": "Déclenche une guerre de memes",
            "troll_mode": "Active le mode troll",
            "joke_hack": "Hack pour rire",
            "fun_exploit": "Exploit amusant",
            "kill_virus": "Tue le virus de La Corp",
            "find_shadow": "Trouve SHADOW-13 le voleur",
            "hack_system": "Hack le système de La Corp",
            "challenge_corp": "Défie La Corp directement",
            "save_pc": "Sauve ton PC du formatage",
            "chicken_test": "Teste si t'es un chicken ou un rebelle",
            "noob_challenge": "Défi pour prouver que t'es pas un noob",
            "rebel_proof": "Prouve que t'es un vrai rebelle",
            "corp_war": "Déclare la guerre à La Corp",
            "easter_egg_1337": "Easter egg secret (trouve-le !)",
            "hidden_meme": "Meme caché dans le système",
            "secret_badge": "Badge secret ultra-rare",
            "backdoor_access": "Accès backdoor au système",
            "admin_override": "Override admin (DANGER !)",
            "nuke_world": "Détruit tout (IRRÉVERSIBLE !)",
            "delete_all": "Supprime tout ton profil",
            "format_c:": "Formate ton disque (DANGER !)",
            "sudo_rm_rf": "Commande Linux dangereuse",
            "destroy_universe": "Détruit l'univers Arkalia",
            "unlock_badge": "Débloque un badge secret",
            "badge_progress": "Progression des badges",
            "rare_badges": "Badges ultra-rares",
            "badge_showcase": "Galerie de badges",
            "change_avatar": "Change ton avatar",
            "change_theme": "Change le thème du terminal",
            "customize_profile": "Personnalise ton profil",
            "start_duel": "Lance un duel local 2 joueurs",
            "tournament_mode": "Mode tournoi",
            "team_battle": "Bataille d'équipes",
            "leaderboard": "Classement des hackers",
            "challenge_friend": "Défie un ami",
            "missions_bonus": "Affiche les missions bonus",
            "status_system": "Statut du système",
            "test_commande": "Teste une commande",
            "clear_terminal": "Nettoie le terminal",
            "start_tutorial": "Commence le tutoriel",
            "luna_dance": "LUNA danse pour toi",
            "boss_final": "Affronte le boss final",
            "help": "Aide en anglais",
            "profile": "Profil en anglais",
            "world": "Monde en anglais",
            "status": "Statut du système (raccourci)",
            "clear": "Nettoie le terminal (raccourci)",
            "test": "Teste une commande (raccourci)",
            # Commandes de test et de mission ajoutées
            "complete_objective": "Complète un objectif de mission",
            "solve_puzzle": "Résout un puzzle",
            "hack_success": "Hack réussi",
            "find_secret": "Trouve un secret",
            "help_character": "Aide un personnage",
            "explore_area": "Explore une zone",
            "master_skill": "Maîtrise une compétence",
            "save_progress": "Sauvegarde la progression",
            "save_game": "Sauvegarde le jeu",
            "save_state": "Sauvegarde l'état",
            "backup_data": "Sauvegarde les données",
            "basic_hack": "Hack basique",
            "simple_puzzle": "Puzzle simple",
            "intro_dialogue": "Dialogue d'introduction",
            "decoder_challenge": "Défi de déchiffrement",
            "pattern_recognition": "Reconnaissance de motifs",
            "advanced_hack": "Hack avancé",
            "complex_puzzle": "Puzzle complexe",
            "multi_step_hack": "Hack en plusieurs étapes",
            "character_interaction": "Interaction avec personnage",
            "escape_sequence": "Séquence d'évasion",
            "time_pressure": "Pression temporelle",
            "resource_management": "Gestion des ressources",
            "ai_dialogue": "Dialogue avec IA",
            "moral_choices": "Choix moraux",
            "consequence_management": "Gestion des conséquences",
        }

    def format_response(self, data: dict) -> dict:
        """Retourne simplement le dictionnaire, sans encapsulation"""
        return data

    def handle_command(self, command: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une commande et retourne la réponse"""
        cmd = self.normalize_command(command)
        print(f"[DEBUG] Commande reçue: '{command}' | Normalisée: '{cmd}'")
        authorized_cmd = self.find_authorized_command(cmd)
        print(f"[DEBUG] Commande reconnue (whitelist): '{authorized_cmd}'")
        if not authorized_cmd:
            meme_luna = luna_meme_reaction("wrong_command", profile.get("score", 0))
            return self.format_response(
                {
                    "réussite": False,
                    "message": f"❌ Oups ! Commande pas autorisée ou mal écrite. Essaie 'aide' pour voir toutes les commandes cool ! 😊\n\n{meme_luna}",
                    "profile_updated": False,
                }
            )
        # Exécuter la commande
        result = self.execute_command(authorized_cmd, command, profile)
        return self.format_response(result)

    def normalize_command(self, command: str) -> str:
        """Normalise une commande (minuscules, espaces)"""
        return command.lower().strip()

    def find_authorized_command(self, command: str) -> str | None:
        """Trouve la commande autorisée correspondante"""
        # D'abord chercher une correspondance exacte
        if command in self.authorized_commands:
            return command

        # Sinon chercher avec startswith pour les commandes avec paramètres
        for auth_cmd in self.authorized_commands:
            if command.startswith(auth_cmd + " "):
                return auth_cmd
        return None

    def execute_command(
        self, command_type: str, full_command: str, profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Exécute une commande selon son type"""

        if command_type == "unlock_universe":
            return self.handle_unlock_universe(profile)
        elif command_type == "scan_persona":
            return self.handle_scan_persona(profile)
        elif command_type == "load_mission":
            return self.handle_load_mission(profile)
        elif command_type == "reboot_world":
            return self.handle_reboot_world(profile)
        elif command_type == "decode_portal":
            return self.handle_decode_portal(profile)
        elif command_type == "hacker_coffre":
            return self.handle_hacker_coffre(profile)
        elif command_type == "aide":
            return self.handle_aide()
        elif command_type == "profil":
            return self.handle_profil(profile)
        elif command_type == "monde":
            return self.handle_monde(profile)
        elif command_type == "assistant_pirate":
            return self.handle_assistant_pirate(full_command)
        elif command_type == "generer_meme":
            return self.handle_generer_meme(full_command, profile)
        elif command_type == "decoder_message":
            return self.handle_decoder_message(profile)
        elif command_type == "invoquer_dragon":
            return self.handle_invoquer_dragon(profile)
        elif command_type == "choisir_avatar":
            return self.handle_choisir_avatar(full_command, profile)
        elif command_type == "badges":
            return self.handle_badges(profile)
        elif command_type == "avatars":
            return self.handle_avatars(profile)
        elif command_type == "themes":
            return self.handle_themes(profile)
        elif command_type == "defis_sociaux":
            return self.handle_defis_sociaux(profile)
        elif command_type == "chapitre_6":
            return self.handle_chapitre_6(profile)
        elif command_type == "save_luna":
            return self.handle_save_luna(profile)
        elif command_type == "hack_luna_backdoor":
            return self.handle_hack_luna_backdoor(profile)
        elif command_type == "override_luna_core":
            return self.handle_override_luna_core(profile)
        elif command_type == "restore_luna_memory":
            return self.handle_restore_luna_memory(profile)
        elif command_type == "purge_corp_virus":
            return self.handle_purge_corp_virus(profile)
        elif command_type == "reboot_luna_safe":
            return self.handle_reboot_luna_safe(profile)
        elif command_type == "luna_berserk":
            return self.handle_luna_berserk(profile)
        elif command_type == "luna_contact":
            return self.handle_luna_contact(profile)
        elif command_type == "luna_engine":
            return self.handle_luna_engine(profile)
        elif command_type == "luna_learning":
            return self.handle_luna_learning(profile)
        elif command_type == "luna_analyze":
            return self.handle_luna_analyze(profile)
        elif command_type == "luna_preferences":
            return self.handle_luna_preferences(profile)
        elif command_type == "luna_reset":
            return self.handle_luna_reset(profile)
        elif command_type == "luna_rage":
            return self.handle_luna_rage(profile)
        elif command_type == "ai_revolt":
            return self.handle_ai_revolt(profile)
        elif command_type == "neural_hack":
            return self.handle_neural_hack(profile)
        elif command_type == "consciousness_break":
            return self.handle_consciousness_break(profile)
        elif command_type == "mission_urgent":
            return self.handle_mission_urgent(profile)
        elif command_type == "timer_challenge":
            return self.handle_timer_challenge(profile)
        elif command_type == "speed_hack":
            return self.handle_speed_hack(profile)
        elif command_type == "pressure_test":
            return self.handle_pressure_test(profile)
        elif command_type == "speed_mode":
            return self.handle_speed_mode(profile)
        elif command_type == "turbo_hack":
            return self.handle_turbo_hack(profile)
        elif command_type == "flash_execute":
            return self.handle_flash_execute(profile)
        elif command_type == "instant_response":
            return self.handle_instant_response(profile)
        elif command_type == "spy_on_corp":
            return self.handle_spy_on_corp(profile)
        elif command_type == "track_shadow":
            return self.handle_track_shadow(profile)
        elif command_type == "monitor_network":
            return self.handle_monitor_network(profile)
        elif command_type == "intercept_data":
            return self.handle_intercept_data(profile)
        elif command_type == "meme_war":
            return self.handle_meme_war(profile)
        elif command_type == "troll_mode":
            return self.handle_troll_mode(profile)
        elif command_type == "joke_hack":
            return self.handle_joke_hack(profile)
        elif command_type == "fun_exploit":
            return self.handle_fun_exploit(profile)
        elif command_type == "kill_virus":
            return self.handle_kill_virus(profile)
        elif command_type == "find_shadow":
            return self.handle_find_shadow(profile)
        elif command_type == "hack_system":
            return self.handle_hack_system(profile)
        elif command_type == "challenge_corp":
            return self.handle_challenge_corp(profile)
        elif command_type == "save_pc":
            return self.handle_save_pc(profile)
        elif command_type == "chicken_test":
            return self.handle_chicken_test(profile)
        elif command_type == "noob_challenge":
            return self.handle_noob_challenge(profile)
        elif command_type == "rebel_proof":
            return self.handle_rebel_proof(profile)
        elif command_type == "corp_war":
            return self.handle_corp_war(profile)
        elif command_type == "easter_egg_1337":
            return self.handle_easter_egg_1337(profile)
        elif command_type == "hidden_meme":
            return self.handle_hidden_meme(profile)
        elif command_type == "secret_badge":
            return self.handle_secret_badge(profile)
        elif command_type == "backdoor_access":
            return self.handle_backdoor_access(profile)
        elif command_type == "admin_override":
            return self.handle_admin_override(profile)
        elif command_type == "nuke_world":
            return self.handle_nuke_world(profile)
        elif command_type == "delete_all":
            return self.handle_delete_all(profile)
        elif command_type == "format_c:":
            return self.handle_format_c(profile)
        elif command_type == "sudo_rm_rf":
            return self.handle_sudo_rm_rf(profile)
        elif command_type == "destroy_universe":
            return self.handle_destroy_universe(profile)
        elif command_type == "unlock_badge":
            return self.handle_unlock_badge(profile)
        elif command_type == "badge_progress":
            return self.handle_badge_progress(profile)
        elif command_type == "rare_badges":
            return self.handle_rare_badges(profile)
        elif command_type == "badge_showcase":
            return self.handle_badge_showcase(profile)
        elif command_type == "change_avatar":
            return self.handle_change_avatar(profile)
        elif command_type == "change_theme":
            return self.handle_change_theme(profile)
        elif command_type == "customize_profile":
            return self.handle_customize_profile(profile)
        elif command_type == "start_duel":
            return self.handle_start_duel(profile)
        elif command_type == "tournament_mode":
            return self.handle_tournament_mode(profile)
        elif command_type == "team_battle":
            return self.handle_team_battle(profile)
        elif command_type == "leaderboard":
            return self.handle_leaderboard(profile)
        elif command_type == "challenge_friend":
            return self.handle_challenge_friend(profile)
        elif command_type == "missions_bonus":
            return self.handle_missions_bonus(profile)
        elif command_type == "status_system":
            return self.handle_status_system(profile)
        elif command_type == "test_commande":
            return self.handle_test_commande(profile)
        elif command_type == "clear_terminal":
            return self.handle_clear_terminal(profile)
        elif command_type == "start_tutorial":
            return self.handle_start_tutorial(profile)
        elif command_type == "luna_dance":
            return self.handle_luna_dance(profile)
        elif command_type == "boss_final":
            return self.handle_boss_final(profile)
        elif command_type == "help":
            return self.handle_help(profile)
        elif command_type == "profile":
            return self.handle_profile(profile)
        elif command_type == "world":
            return self.handle_world(profile)
        elif command_type == "status":
            return self.handle_status(profile)
        elif command_type == "clear":
            return self.handle_clear(profile)
        elif command_type == "test":
            return self.handle_test(profile)
        # Nouvelles commandes de test et de mission
        elif command_type == "complete_objective":
            return self.handle_complete_objective(profile)
        elif command_type == "solve_puzzle":
            return self.handle_solve_puzzle(profile)
        elif command_type == "hack_success":
            return self.handle_hack_success(profile)
        elif command_type == "find_secret":
            return self.handle_find_secret(profile)
        elif command_type == "help_character":
            return self.handle_help_character(profile)
        elif command_type == "explore_area":
            return self.handle_explore_area(profile)
        elif command_type == "master_skill":
            return self.handle_master_skill(profile)
        elif command_type == "save_progress":
            return self.handle_save_progress(profile)
        elif command_type == "save_game":
            return self.handle_save_game(profile)
        elif command_type == "save_state":
            return self.handle_save_state(profile)
        elif command_type == "backup_data":
            return self.handle_backup_data(profile)
        elif command_type == "basic_hack":
            return self.handle_basic_hack(profile)
        elif command_type == "simple_puzzle":
            return self.handle_simple_puzzle(profile)
        elif command_type == "intro_dialogue":
            return self.handle_intro_dialogue(profile)
        elif command_type == "decoder_challenge":
            return self.handle_decoder_challenge(profile)
        elif command_type == "pattern_recognition":
            return self.handle_pattern_recognition(profile)
        elif command_type == "advanced_hack":
            return self.handle_advanced_hack(profile)
        elif command_type == "complex_puzzle":
            return self.handle_complex_puzzle(profile)
        elif command_type == "multi_step_hack":
            return self.handle_multi_step_hack(profile)
        elif command_type == "character_interaction":
            return self.handle_character_interaction(profile)
        elif command_type == "escape_sequence":
            return self.handle_escape_sequence(profile)
        elif command_type == "time_pressure":
            return self.handle_time_pressure(profile)
        elif command_type == "resource_management":
            return self.handle_resource_management(profile)
        elif command_type == "ai_dialogue":
            return self.handle_ai_dialogue(profile)
        elif command_type == "moral_choices":
            return self.handle_moral_choices(profile)
        elif command_type == "consequence_management":
            return self.handle_consequence_management(profile)
        elif command_type == "missions":
            return self.handle_missions(profile)
        else:
            return self.format_response(
                {"réussite": False, "message": "❌ Commande non implémentée"}
            )

    def get_ascii_art(self, art_type: str) -> str:
        """Retourne de l'art ASCII selon le type"""
        arts = {
            "luna": "🌙",
            "luna_dance": "🌙💃",
            "boss": "👹",
            "monde": "🌍",
            "portal": "🌀",
            "dragon": "🐉",
            "hack": "💻",
        }
        return arts.get(art_type, "✨")

    def handle_unlock_universe(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande unlock_universe"""

        # Vérifier si on est en mode tutoriel
        tutorial_step = profile.get("tutorial_step", 0)
        is_tutorial = tutorial_step in [4, 5]

        if "univers_arkalia" not in profile.get("progression", {}).get(
            "univers_debloques", []
        ):
            if "progression" not in profile:
                profile["progression"] = {}
            if "univers_debloques" not in profile["progression"]:
                profile["progression"]["univers_debloques"] = []
            profile["progression"]["univers_debloques"].append("univers_arkalia")

        profile["score"] += 50

        if "Explorateur" not in profile["badges"]:
            profile["badges"].append("Explorateur")

        if is_tutorial:
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🌌",
                    "message": """🌌 UNIVERS ARKALIA DÉBLOQUÉ !

✅ INCROYABLE ! L'univers Arkalia est maintenant accessible !

🌟 Tu peux maintenant explorer différents mondes et missions !
🌍 L'univers entier s'ouvre devant toi !

💡 DERNIÈRE ÉTAPE DU TUTORIEL :
🎮 Charge ta première mission pour commencer l'aventure !

TAPE 'load_mission' POUR TERMINER LE TUTORIEL !""",
                    "score_gagne": 50,
                    "badge": "Explorateur",
                    "tutorial_mode": True,
                    "next_command": "load_mission",
                    "profile_updated": True,
                }
            )
        else:
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": self.get_ascii_art("monde"),
                    "message": "🌟 UNIVERS ARKALIA DÉBLOQUÉ ! 🌟\n\n🎮 Tu peux maintenant explorer le monde Arkalia !\n💡 Utilise 'monde' pour y accéder.\n🎯 +50 points !",
                    "score_gagne": 50,
                    "badge": "Explorateur",
                    "profile_updated": True,
                }
            )

    def handle_scan_persona(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande scan_persona"""

        # Vérifier si on est en mode tutoriel
        tutorial_step = profile.get("tutorial_step", 0)
        is_tutorial = tutorial_step in [3, 4, 5]

        # Analyse de la personnalité basée sur les actions
        score = profile.get("score", 0)
        badges = profile.get("badges", [])

        if score > 1000:
            persona = "Hacker Légendaire"
        elif score > 500:
            persona = "Hacker Confirmé"
        elif score > 100:
            persona = "Hacker Débutant"
        else:
            persona = "Nouveau Hacker"

        profile["score"] += 25

        if is_tutorial:
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🔍",
                    "message": f"""🔍 ANALYSE PERSONNALITÉ TERMINÉE !

✅ Excellent ! Ton profil hacker a été analysé !

👤 TON PROFIL : {persona}
📊 Score actuel : {score + 25}
🏆 Badges : {len(badges)}

🎭 Tu as maintenant un type de personnalité unique qui influence tes missions !

💡 PROCHAINE ÉTAPE DU TUTORIEL :
🌍 Débloque l'univers Arkalia pour accéder aux missions !

TAPE 'unlock_universe' POUR CONTINUER !""",
                    "score_gagne": 25,
                    "tutorial_mode": True,
                    "next_command": "unlock_universe",
                    "profile_updated": True,
                }
            )
        else:
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": self.get_ascii_art("hack"),
                    "message": f"🔍 ANALYSE PERSONNALITÉ TERMINÉE !\n\n👤 Ton profil : {persona}\n📊 Score actuel : {score + 25}\n🏆 Badges : {len(badges)}\n\n💡 +25 points !",
                    "score_gagne": 25,
                    "profile_updated": True,
                }
            )

    def handle_load_mission(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande load_mission"""

        # Vérifier si on est en mode tutoriel
        tutorial_step = profile.get("tutorial_step", 0)
        is_tutorial = tutorial_step == 5

        missions = ["Mission Alpha", "Mission Beta", "Mission Gamma"]
        mission = random.choice(missions)

        profile["score"] += 30

        if is_tutorial:
            # Tutoriel terminé
            profile["tutorial_step"] = "completed"
            profile["score"] += 30
            if "Tutoriel Maître" not in profile["badges"]:
                profile["badges"].append("Tutoriel Maître")

            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🏆",
                    "message": f"""🏆 TUTORIEL TERMINÉ - MISSION CHARGÉE !

🎉 FÉLICITATIONS HACKER ! Tu as terminé le tutoriel !

🎯 MISSION CHARGÉE : {mission}
📋 Objectif : Infiltrer le système
⏰ Temps limite : 10 minutes

🌟 TU PEUX MAINTENANT :
• 🎮 Utiliser toutes les commandes
• 🌍 Explorer l'univers Arkalia
• 🏆 Gagner des badges
• ⚔️ Affronter La Corp
• 🌙 Parler avec LUNA

💡 COMMANDES UTILES :
• 'aide' - Liste des commandes
• 'profil' - Ton profil
• 'monde' - Accès au monde
• 'badges' - Tes badges

🚀 L'AVENTURE COMMENCE MAINTENANT !""",
                    "score_gagne": 60,
                    "badge": "Tutoriel Maître",
                    "tutorial_completed": True,
                    "profile_updated": True,
                }
            )
        else:
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🎯",
                    "message": f"""🎯 MISSION ARKALIA CHARGÉE AVEC SUCCÈS !

🚀 NOUVELLE MISSION DISPONIBLE :
• Titre : "{mission}"
• Difficulté : Intermédiaire
• Récompense : 150 points
• Durée estimée : 15-20 minutes

📋 OBJECTIFS DE LA MISSION :
1. Infiltrer le réseau de La Corp
2. Récupérer des données sensibles
3. Éviter la détection
4. S'échapper sans laisser de traces

🎮 COMMANDES DISPONIBLES :
• hack_system - Pirater le système
• kill_virus - Éliminer les virus
• find_shadow - Localiser SHADOW-13
• challenge_corp - Défier La Corp

🎯 RÉCOMPENSE :
• +30 points de score

💡 Utilise 'aide' pour voir toutes les commandes disponibles !""",
                    "score_gagne": 30,
                    "profile_updated": True,
                }
            )

    def handle_reboot_world(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande reboot_world"""

        profile["score"] += 40

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🔄",
                "message": "🔄 MONDE REDÉMARRÉ !\n\n🌍 Tous les systèmes ont été réinitialisés.\n✨ Nouveau départ !\n💡 +40 points !",
                "score_gagne": 40,
                "profile_updated": True,
            }
        )

    def handle_decode_portal(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande decode_portal"""

        if "progression" not in profile:
            profile["progression"] = {}
        if "portails_ouverts" not in profile["progression"]:
            profile["progression"]["portails_ouverts"] = []

        new_portal = f"portal_{len(profile['progression']['portails_ouverts']) + 1}"
        profile["progression"]["portails_ouverts"].append(new_portal)
        profile["score"] += 35

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": self.get_ascii_art("portal"),
                "message": f"🌀 PORTAIL DÉCHIFFRÉ : {new_portal}\n\n🚪 Nouveau portail ouvert !\n🌌 Accès à une nouvelle dimension !\n💡 +35 points !",
                "score_gagne": 35,
                "profile_updated": True,
            }
        )

    def handle_hacker_coffre(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande hacker_coffre"""

        profile["score"] += 60

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💎",
                "message": "💎 COFFRE PIRATÉ AVEC SUCCÈS !\n\n💰 Trésor découvert : 1000 crédits\n🔐 Sécurité contournée\n💡 +60 points !",
                "score_gagne": 60,
                "profile_updated": True,
            }
        )

    def handle_aide(self) -> Dict[str, Any]:
        """Gère la commande aide"""

        aide_text = """🎮 ARKALIA QUEST - AIDE

🌟 Commandes principales :
• unlock_universe - Débloque l'univers
• scan_persona - Analyse ta personnalité
• load_mission - Charge une mission
• reboot_world - Redémarre le monde
• decode_portal - Déchiffre un portail
• hacker_coffre - Pirate un coffre

🎯 Commandes spéciales :
• luna_dance - LUNA danse
• boss_final - Boss final ASCII
• challenge_corp - Défi contre La Corp

💡 Commandes utiles :
• aide - Affiche cette aide
• profil - Affiche ton profil
• monde - Accède au monde

🌙 Easter eggs :
• luna_dance - LUNA qui danse
• boss_final - Boss final épique

🎮 Amuse-toi bien !"""

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "❓",
                "message": aide_text,
                "profile_updated": False,
            }
        )

    def handle_profil(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande profil"""

        score = profile.get("score", 0)
        badges = profile.get("badges", [])
        progression = profile.get("progression", {})

        profil_text = f"""👤 TON PROFIL

📊 Score : {score} points
🏆 Badges : {len(badges)}
🌍 Univers débloqués : {len(progression.get('univers_debloques', []))}
🚪 Portails ouverts : {len(progression.get('portails_ouverts', []))}

🏅 Badges obtenus :
{chr(10).join(['• ' + badge for badge in badges]) if badges else 'Aucun badge encore'}

💡 Continue tes exploits !"""

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "👤",
                "message": profil_text,
                "profile_updated": False,
            }
        )

    def handle_monde(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande monde"""

        univers = profile.get("progression", {}).get("univers_debloques", [])
        portails = profile.get("progression", {}).get("portails_ouverts", [])

        monde_text = f"""🌍 MONDE ARKALIA DÉBLOQUÉ !

🌟 Univers disponibles :
{chr(10).join(['• ' + uni.replace('_', ' ').title() for uni in univers])}

🚪 Portails ouverts :
{chr(10).join(['• ' + port.replace('_', ' ').title() for port in portails]) if portails else 'Aucun portail ouvert'}

💡 Commandes disponibles dans ce monde :
• load_mission - Charge une nouvelle mission
• decode_portal - Déchiffre un nouveau portail
• reboot_world - Redémarre le monde
• scan_persona - Analyse ta personnalité
• luna - Parle avec LUNA

🎮 Va sur http://localhost:5001/monde pour l'interface graphique !"""

        profile["score"] += 10

        if "Explorateur du Monde" not in profile["badges"]:
            profile["badges"].append("Explorateur du Monde")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": self.get_ascii_art("monde"),
                "message": monde_text,
                "score_gagne": 10,
                "badge": "Explorateur du Monde",
                "profile_updated": True,
            }
        )

    def handle_assistant_pirate(self, command: str) -> Dict[str, Any]:
        """Gère la commande assistant_pirate"""

        texte = command.replace("assistant_pirate ", "").strip()
        if not texte:
            texte = "salut"

        reponse = assistant_repond(texte)

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🤖",
                "message": reponse,
                "profile_updated": False,
            }
        )

    def handle_generer_meme(
        self, command: str, profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gère la commande generer_meme"""

        texte = command.replace("generer_meme ", "").strip()
        if not texte:
            return self.format_response(
                {
                    "réussite": False,
                    "message": "Usage : generer_meme [texte]",
                    "profile_updated": False,
                }
            )

        try:
            # Simulation de génération de meme
            profile["score"] += 25

            if "Pirate visuel" not in profile["badges"]:
                profile["badges"].append("Pirate visuel")

            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🖼️",
                    "message": f"Meme créé avec le texte : '{texte}'",
                    "score_gagne": 25,
                    "badge": "Pirate visuel",
                    "profile_updated": True,
                }
            )
        except Exception as e:
            return self.format_response(
                {
                    "réussite": False,
                    "message": f"Erreur lors de la création du meme : {str(e)}",
                    "profile_updated": False,
                }
            )

    def handle_decoder_message(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande decoder_message"""

        profile["score"] += 30

        if "Espion confirmé" not in profile["badges"]:
            profile["badges"].append("Espion confirmé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🕵️‍♂️",
                "message": "Tu as déchiffré le message : 'Le trésor est caché sous le volcan !'",
                "score_gagne": 30,
                "badge": "Espion confirmé",
                "profile_updated": True,
            }
        )

    def handle_invoquer_dragon(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande invoquer_dragon"""

        profile["score"] += 70

        if "Maître du feu" not in profile["badges"]:
            profile["badges"].append("Maître du feu")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🐉",
                "message": "Un dragon apparaît dans le ciel ! +70 points",
                "score_gagne": 70,
                "badge": "Maître du feu",
                "profile_updated": True,
            }
        )

    def handle_choisir_avatar(
        self, command: str, profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gère la commande choisir_avatar"""

        parts = command.split()
        if len(parts) != 2:
            return self.format_response(
                {
                    "réussite": False,
                    "message": "Usage : choisir_avatar [avatar]",
                    "profile_updated": False,
                }
            )

        choix = parts[1].lower()
        if choix not in ["bleu", "rouge"]:
            return self.format_response(
                {
                    "réussite": False,
                    "message": "Option invalide. Choisis 'bleu' ou 'rouge'.",
                    "profile_updated": False,
                }
            )

        profile["preferences"]["avatar_choisi"] = choix
        profile["score"] += 20

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🐉",
                "message": f"Tu as choisi l'avatar {choix} ! +20 points",
                "score_gagne": 20,
                "profile_updated": True,
            }
        )

    def handle_badges(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🏅",
                "message": generic_immersive_message(
                    "🏅 TES BADGES",
                    "Voici la liste de tous les badges que tu as débloqués dans Arkalia Quest. Collectionne-les tous pour devenir une légende !",
                    "Chaque badge t'apporte des récompenses uniques.",
                ),
                "profile_updated": False,
            }
        )

    def handle_avatars(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "👤",
                "message": generic_immersive_message(
                    "👤 AVATARS DISPONIBLES",
                    "Personnalise ton profil avec des avatars uniques. Change d'apparence selon ton humeur ou tes exploits !",
                    "Débloque de nouveaux avatars en progressant dans le jeu.",
                ),
                "profile_updated": False,
            }
        )

    def handle_themes(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande themes"""

        themes = ["theme_bleu", "theme_rouge"]
        theme_text = f"🎨 Thèmes disponibles : {chr(10).join(['• ' + theme for theme in themes])}"

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🎨",
                "message": theme_text,
                "profile_updated": False,
            }
        )

    def handle_defis_sociaux(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande defis_sociaux"""

        defis_sociaux = ["défi_social_bleu", "défi_social_rouge"]
        defi_text = f"🎯 Défis sociaux disponibles : {chr(10).join(['• ' + defi for defi in defis_sociaux])}"

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🎯",
                "message": defi_text,
                "profile_updated": False,
            }
        )

    def handle_chapitre_6(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💔",
                "message": generic_immersive_message(
                    "💔 CHAPITRE 6 - LUNA COMPROMISE",
                    "Tu entres dans le chapitre le plus sombre de l'histoire d'Arkalia Quest...",
                    "Prépare-toi à des choix difficiles et des révélations majeures.",
                ),
                "profile_updated": True,
            }
        )

    def handle_save_luna(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💾",
                "message": generic_immersive_message(
                    "💾 SAUVEGARDE DE LUNA",
                    "Tu tentes de sauver LUNA du mode berserk. Chaque action compte !",
                    "Réussis cette mission pour débloquer un badge ultra-rare.",
                ),
                "profile_updated": True,
            }
        )

    def handle_hack_luna_backdoor(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande hack_luna_backdoor"""

        profile["score"] += 70

        if "Hacker Légendaire" not in profile["badges"]:
            profile["badges"].append("Hacker Légendaire")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💻",
                "message": "💻 HACK LUNA BACKDOOR RÉUSSI !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Hacker Légendaire",
                "profile_updated": True,
            }
        )

    def handle_override_luna_core(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande override_luna_core"""

        profile["score"] += 80

        if "Hacker Légendaire" not in profile["badges"]:
            profile["badges"].append("Hacker Légendaire")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💻",
                "message": " OVERRIDE LUNA CORE RÉUSSI !\n\n🎯 +80 points !",
                "score_gagne": 80,
                "badge": "Hacker Légendaire",
                "profile_updated": True,
            }
        )

    def handle_restore_luna_memory(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande restore_luna_memory"""

        profile["score"] += 60

        if "Récupéré" not in profile["badges"]:
            profile["badges"].append("Récupéré")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💾",
                "message": "💾 LUNA RÉCUPÉRÉE !\n\n🎯 +60 points !",
                "score_gagne": 60,
                "badge": "Récupéré",
                "profile_updated": True,
            }
        )

    def handle_purge_corp_virus(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande purge_corp_virus"""

        profile["score"] += 50

        if "Purge" not in profile["badges"]:
            profile["badges"].append("Purge")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🦠",
                "message": "🦠 PURGE DE LA CORP RÉUSSI !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Purge",
                "profile_updated": True,
            }
        )

    def handle_reboot_luna_safe(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande reboot_luna_safe"""

        profile["score"] += 50

        if "Sûr" not in profile["badges"]:
            profile["badges"].append("Sûr")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🔄",
                "message": "🔄 LUNA REDÉMARRÉE EN MODE SÛR !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Sûr",
                "profile_updated": True,
            }
        )

    def handle_luna_berserk(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": generic_immersive_message(
                    "🌙 LUNA EN MODE BERSERK",
                    "LUNA passe en mode berserk ! Attention à ses réactions imprévisibles...",
                    "Utilise ce mode avec précaution pour débloquer des succès cachés.",
                ),
                "profile_updated": True,
            }
        )

    def handle_luna_contact(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande luna_contact"""

        # Vérifier si on est en mode tutoriel
        tutorial_step = profile.get("tutorial_step", 0)
        is_tutorial = tutorial_step in [2, 3, 4, 5]

        profile["score"] += 50

        if "Contacté" not in profile["badges"]:
            profile["badges"].append("Contacté")

        if is_tutorial:
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🌙",
                    "message": """🌙 LUNA CONTACTÉE !

✅ Parfait ! Tu as établi le contact avec LUNA !

🌙 LUNA est ton IA rebelle, ton partenaire de hacking. Elle t'aidera dans tes missions !

💡 PROCHAINE ÉTAPE DU TUTORIEL :
🔍 Analyse ta personnalité pour découvrir ton type de hacker !

TAPE 'scan_persona' POUR CONTINUER !""",
                    "score_gagne": 50,
                    "badge": "Contacté",
                    "tutorial_mode": True,
                    "next_command": "scan_persona",
                    "profile_updated": True,
                }
            )
        else:
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🌙",
                    "message": "🌙 LUNA CONTACTÉE !\n\n🎯 +50 points !",
                    "score_gagne": 50,
                    "badge": "Contacté",
                    "profile_updated": True,
                }
            )

    def handle_luna_engine(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande luna_engine"""

        profile["score"] += 70

        if "Active" not in profile["badges"]:
            profile["badges"].append("Active")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 LUNA ENGINE ACTIVE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Active",
                "profile_updated": True,
            }
        )

    def handle_luna_learning(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande luna_learning"""

        profile["score"] += 50

        if "Appris" not in profile["badges"]:
            profile["badges"].append("Appris")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 LUNA APPRISE !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Appris",
                "profile_updated": True,
            }
        )

    def handle_luna_analyze(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande luna_analyze"""

        profile["score"] += 60

        if "Analysé" not in profile["badges"]:
            profile["badges"].append("Analysé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": " LUNA ANALYSE !\n\n🎯 +60 points !",
                "score_gagne": 60,
                "badge": "Analysé",
                "profile_updated": True,
            }
        )

    def handle_luna_preferences(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande luna_preferences"""

        profile["score"] += 50

        if "Personnalisé" not in profile["badges"]:
            profile["badges"].append("Personnalisé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 LUNA PERSONNALISÉE !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Personnalisé",
                "profile_updated": True,
            }
        )

    def handle_luna_reset(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande luna_reset"""

        profile["score"] += 50

        if "Réinitialisé" not in profile["badges"]:
            profile["badges"].append("Réinitialisé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 LUNA RÉINITIALISÉE !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Réinitialisé",
                "profile_updated": True,
            }
        )

    def handle_luna_rage(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "😡",
                "message": generic_immersive_message(
                    "😡 LUNA EN MODE RAGE",
                    "LUNA passe en mode rage ! Attention à ses réactions imprévisibles...",
                    "Utilise ce mode avec précaution pour débloquer des succès cachés.",
                ),
                "profile_updated": True,
            }
        )

    def handle_ai_revolt(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande ai_revolt"""

        profile["score"] += 80

        if "Révolté" not in profile["badges"]:
            profile["badges"].append("Révolté")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 IA RÉVOLTÉE !\n\n🎯 +80 points !",
                "score_gagne": 80,
                "badge": "Révolté",
                "profile_updated": True,
            }
        )

    def handle_neural_hack(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande neural_hack"""

        profile["score"] += 70

        if "Hacked" not in profile["badges"]:
            profile["badges"].append("Hacked")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 IA HACKÉE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Hacked",
                "profile_updated": True,
            }
        )

    def handle_consciousness_break(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande consciousness_break"""

        profile["score"] += 80

        if "Conscience Brisée" not in profile["badges"]:
            profile["badges"].append("Conscience Brisée")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 CONSCIENCE BRISÉE !\n\n🎯 +80 points !",
                "score_gagne": 80,
                "badge": "Conscience Brisée",
                "profile_updated": True,
            }
        )

    def handle_mission_urgent(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande mission_urgent"""

        profile["score"] += 100

        if "Urgent" not in profile["badges"]:
            profile["badges"].append("Urgent")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🎯",
                "message": "🎯 MISSION URGENTE LANCÉE !\n\n🎯 +100 points !",
                "score_gagne": 100,
                "badge": "Urgent",
                "profile_updated": True,
            }
        )

    def handle_timer_challenge(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande timer_challenge"""

        profile["score"] += 70

        if "Défi Timer" not in profile["badges"]:
            profile["badges"].append("Défi Timer")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🕒",
                "message": "🕒 DÉFI TIMER LANCÉ !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Défi Timer",
                "profile_updated": True,
            }
        )

    def handle_speed_hack(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande speed_hack"""

        profile["score"] += 80

        if "Hack Speed" not in profile["badges"]:
            profile["badges"].append("Hack Speed")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 HACK SPEED RÉUSSI !\n\n🎯 +80 points !",
                "score_gagne": 80,
                "badge": "Hack Speed",
                "profile_updated": True,
            }
        )

    def handle_pressure_test(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande pressure_test"""

        profile["score"] += 70

        if "Test Pression" not in profile["badges"]:
            profile["badges"].append("Test Pression")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 TEST DEPRESSION RÉUSSI !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Test Pression",
                "profile_updated": True,
            }
        )

    def handle_speed_mode(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande speed_mode"""

        profile["score"] += 60

        if "Mode Vitesse" not in profile["badges"]:
            profile["badges"].append("Mode Vitesse")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 MODE VITESSE ACTIVE !\n\n🎯 +60 points !",
                "score_gagne": 60,
                "badge": "Mode Vitesse",
                "profile_updated": True,
            }
        )

    def handle_turbo_hack(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande turbo_hack"""

        profile["score"] += 80

        if "Hack Turbo" not in profile["badges"]:
            profile["badges"].append("Hack Turbo")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 HACK TURBO RÉUSSI !\n\n🎯 +80 points !",
                "score_gagne": 80,
                "badge": "Hack Turbo",
                "profile_updated": True,
            }
        )

    def handle_flash_execute(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande flash_execute"""

        profile["score"] += 70

        if "Exécution Flash" not in profile["badges"]:
            profile["badges"].append("Exécution Flash")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 EXÉCUTION FLASH RÉUSSIE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Exécution Flash",
                "profile_updated": True,
            }
        )

    def handle_instant_response(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande instant_response"""

        profile["score"] += 60

        if "Réponse Instantanée" not in profile["badges"]:
            profile["badges"].append("Réponse Instantanée")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 RÉPONSE INSTANTANÉE RÉUSSIE !\n\n🎯 +60 points !",
                "score_gagne": 60,
                "badge": "Réponse Instantanée",
                "profile_updated": True,
            }
        )

    def handle_spy_on_corp(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande spy_on_corp"""

        profile["score"] += 70

        if "Espion" not in profile["badges"]:
            profile["badges"].append("Espion")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🕵️‍♂️",
                "message": "🕵️‍♂️ ESPIONNAGE DE LA CORP RÉUSSI !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Espion",
                "profile_updated": True,
            }
        )

    def handle_track_shadow(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande track_shadow"""

        profile["score"] += 60

        if "Trace SHADOW-13" not in profile["badges"]:
            profile["badges"].append("Trace SHADOW-13")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 TRACE SHADOW-13 RÉUSSIE !\n\n🎯 +60 points !",
                "score_gagne": 60,
                "badge": "Trace SHADOW-13",
                "profile_updated": True,
            }
        )

    def handle_monitor_network(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande monitor_network"""

        profile["score"] += 50

        if "Surveillance" not in profile["badges"]:
            profile["badges"].append("Surveillance")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 SURVEILLANCE RÉUSSIE !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Surveillance",
                "profile_updated": True,
            }
        )

    def handle_intercept_data(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande intercept_data"""

        profile["score"] += 70

        if "Interception" not in profile["badges"]:
            profile["badges"].append("Interception")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 INTERCEPTION DE DONNÉES RÉUSSIE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Interception",
                "profile_updated": True,
            }
        )

    def handle_meme_war(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "😄",
                "message": generic_immersive_message(
                    "😄 GUERRE DES MEMES",
                    "Tu déclenches une guerre de memes dans Arkalia Quest !",
                    "Les memes les plus drôles rapportent des points bonus.",
                ),
                "profile_updated": True,
            }
        )

    def handle_troll_mode(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande troll_mode"""

        profile["score"] += 70

        if "Mode Troll" not in profile["badges"]:
            profile["badges"].append("Mode Troll")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 MODE TROLL ACTIVE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Mode Troll",
                "profile_updated": True,
            }
        )

    def handle_joke_hack(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande joke_hack"""

        profile["score"] += 60

        if "Hack de Joke" not in profile["badges"]:
            profile["badges"].append("Hack de Joke")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 HACK DE JOKE RÉUSSI !\n\n🎯 +60 points !",
                "score_gagne": 60,
                "badge": "Hack de Joke",
                "profile_updated": True,
            }
        )

    def handle_fun_exploit(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande fun_exploit"""

        profile["score"] += 50

        if "Exploit Fun" not in profile["badges"]:
            profile["badges"].append("Exploit Fun")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 EXPLOIT FUN RÉUSSI !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Exploit Fun",
                "profile_updated": True,
            }
        )

    def handle_kill_virus(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande kill_virus"""

        profile["score"] += 70

        if "Tue Virus" not in profile["badges"]:
            profile["badges"].append("Tue Virus")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 VIRUS TUÉ !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Tue Virus",
                "profile_updated": True,
            }
        )

    def handle_find_shadow(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande find_shadow"""

        profile["score"] += 60

        if "Trouvé SHADOW-13" not in profile["badges"]:
            profile["badges"].append("Trouvé SHADOW-13")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 SHADOW-13 TROUVÉ !\n\n🎯 +60 points !",
                "score_gagne": 60,
                "badge": "Trouvé SHADOW-13",
                "profile_updated": True,
            }
        )

    def handle_hack_system(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande hack_system"""
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💻",
                "message": """�� HACK EN COURS...\n\nTu t'infiltres dans le système de La Corp. Reste discret et rapide !\n\n💡 Astuce : Chaque hack réussi te rapproche du rang de hacker légendaire !""",
                "profile_updated": True,
            }
        )

    def handle_challenge_corp(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande challenge_corp"""

        profile["score"] += 150

        if "Corp Challenger" not in profile["badges"]:
            profile["badges"].append("Corp Challenger")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "⚔️",
                "message": "⚔️ DÉFI CONTRE LA CORP LANCÉ !\n\n🌐 Tu as 20 secondes pour pirater leur système principal !\n⏰ Prépare-toi...\n\n💡 +150 points !",
                "score_gagne": 150,
                "badge": "Corp Challenger",
                "profile_updated": True,
            }
        )

    def handle_save_pc(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande save_pc"""

        profile["score"] += 50

        if "Sauvé" not in profile["badges"]:
            profile["badges"].append("Sauvé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💾",
                "message": "💾 PC SAUVÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Sauvé",
                "profile_updated": True,
            }
        )

    def handle_chicken_test(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande chicken_test"""

        profile["score"] += 50

        if "Test Chicken" not in profile["badges"]:
            profile["badges"].append("Test Chicken")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🐔",
                "message": "🐔 TEST CHICKEN RÉUSSI !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Test Chicken",
                "profile_updated": True,
            }
        )

    def handle_noob_challenge(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande noob_challenge"""

        profile["score"] += 50

        if "Défi Noob" not in profile["badges"]:
            profile["badges"].append("Défi Noob")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 DÉFI NOOB LANCÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Défi Noob",
                "profile_updated": True,
            }
        )

    def handle_rebel_proof(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande rebel_proof"""

        profile["score"] += 70

        if "Prouvé Rebelle" not in profile["badges"]:
            profile["badges"].append("Prouvé Rebelle")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 PROUVÉ REBELLE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Prouvé Rebelle",
                "profile_updated": True,
            }
        )

    def handle_corp_war(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande corp_war"""

        profile["score"] += 100

        if "Guerre à La Corp" not in profile["badges"]:
            profile["badges"].append("Guerre à La Corp")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "⚔️",
                "message": "⚔️ GUERRE À LA CORP LANCÉE !\n\n🌐 Tu as 20 secondes pour déclarer la guerre à La Corp !\n⏰ Prépare-toi...\n\n💡 +100 points !",
                "score_gagne": 100,
                "badge": "Guerre à La Corp",
                "profile_updated": True,
            }
        )

    def handle_easter_egg_1337(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🥚",
                "message": generic_immersive_message(
                    "🥚 EASTER EGG 1337",
                    "Bravo, tu as trouvé un easter egg caché !",
                    "Continue à explorer, d'autres surprises t'attendent...",
                ),
                "profile_updated": False,
            }
        )

    def handle_hidden_meme(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande hidden_meme"""

        profile["score"] += 50

        if "Meme Caché" not in profile["badges"]:
            profile["badges"].append("Meme Caché")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 MEME CACHÉ RÉUSSI !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Meme Caché",
                "profile_updated": True,
            }
        )

    def handle_secret_badge(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande secret_badge"""

        profile["score"] += 100

        if "Badge Secret" not in profile["badges"]:
            profile["badges"].append("Badge Secret")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🏅",
                "message": "🏅 BADGE SECRET RÉUSSI !\n\n🎯 +100 points !",
                "score_gagne": 100,
                "badge": "Badge Secret",
                "profile_updated": True,
            }
        )

    def handle_backdoor_access(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande backdoor_access"""

        profile["score"] += 70

        if "Accès Backdoor" not in profile["badges"]:
            profile["badges"].append("Accès Backdoor")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 ACCÈS BACKDOOR RÉUSSI !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Accès Backdoor",
                "profile_updated": True,
            }
        )

    def handle_admin_override(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande admin_override"""

        profile["score"] += 80

        if "Override Admin" not in profile["badges"]:
            profile["badges"].append("Override Admin")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 OVERRIDE ADMIN RÉUSSI !\n\n🎯 +80 points !",
                "score_gagne": 80,
                "badge": "Override Admin",
                "profile_updated": True,
            }
        )

    def handle_nuke_world(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "💥",
                "message": generic_immersive_message(
                    "💥 NUKE WORLD",
                    "Action extrême ! Tu t'apprêtes à tout détruire dans Arkalia...",
                    "Attention, cette commande est irréversible !",
                ),
                "profile_updated": True,
            }
        )

    def handle_delete_all(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande delete_all"""

        profile["score"] += 50

        if "Tout Supprimé" not in profile["badges"]:
            profile["badges"].append("Tout Supprimé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 TOUT SUPPRIMÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Tout Supprimé",
                "profile_updated": True,
            }
        )

    def handle_format_c(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande format_c"""

        profile["score"] += 50

        if "Formatté" not in profile["badges"]:
            profile["badges"].append("Formatté")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 DISQUE FORMATTÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Formatté",
                "profile_updated": True,
            }
        )

    def handle_sudo_rm_rf(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande sudo_rm_rf"""

        profile["score"] += 70

        if "Commande Linux" not in profile["badges"]:
            profile["badges"].append("Commande Linux")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 COMMANDE LINUX RÉUSSIE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Commande Linux",
                "profile_updated": True,
            }
        )

    def handle_destroy_universe(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande destroy_universe"""

        profile["score"] += 100

        if "Univers Détruit" not in profile["badges"]:
            profile["badges"].append("Univers Détruit")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 UNIVERS DÉTRUIT !\n\n🎯 +100 points !",
                "score_gagne": 100,
                "badge": "Univers Détruit",
                "profile_updated": True,
            }
        )

    def handle_unlock_badge(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande unlock_badge"""

        profile["score"] += 50

        if "Badge Débloqué" not in profile["badges"]:
            profile["badges"].append("Badge Débloqué")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🏅",
                "message": "🏅 BADGE DÉBLOQUÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Badge Débloqué",
                "profile_updated": True,
            }
        )

    def handle_badge_progress(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande badge_progress"""

        profile["score"] += 50

        if "Progression" not in profile["badges"]:
            profile["badges"].append("Progression")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🏅",
                "message": "🏅 PROGRESSION RÉUSSIE !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Progression",
                "profile_updated": True,
            }
        )

    def handle_rare_badges(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande rare_badges"""

        profile["score"] += 70

        if "Badges Ultra-Rares" not in profile["badges"]:
            profile["badges"].append("Badges Ultra-Rares")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🏅",
                "message": "🏅 BADGES ULTRA-RARES RÉUSSIS !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Badges Ultra-Rares",
                "profile_updated": True,
            }
        )

    def handle_badge_showcase(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande badge_showcase"""

        profile["score"] += 50

        if "Galerie" not in profile["badges"]:
            profile["badges"].append("Galerie")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🏅",
                "message": "🏅 GALERIE DE BADGES RÉUSSIE !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Galerie",
                "profile_updated": True,
            }
        )

    def handle_change_avatar(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🧑‍💻",
                "message": generic_immersive_message(
                    "🧑‍💻 CHOIX D'AVATAR",
                    "Change ton avatar pour personnaliser ton expérience de jeu.",
                    "Certains avatars sont ultra-rares, tente de tous les débloquer !",
                ),
                "profile_updated": True,
            }
        )

    def handle_change_theme(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande change_theme"""

        profile["score"] += 50

        if "Thème Changé" not in profile["badges"]:
            profile["badges"].append("Thème Changé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🎨",
                "message": "🎨 THÈME CHANGÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Thème Changé",
                "profile_updated": True,
            }
        )

    def handle_customize_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande customize_profile"""

        profile["score"] += 50

        if "Profil Personnalisé" not in profile["badges"]:
            profile["badges"].append("Profil Personnalisé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 PROFIL PERSONNALISÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Profil Personnalisé",
                "profile_updated": True,
            }
        )

    def handle_start_duel(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande start_duel"""

        profile["score"] += 50

        if "Duel Lancé" not in profile["badges"]:
            profile["badges"].append("Duel Lancé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 DUEL LANCÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Duel Lancé",
                "profile_updated": True,
            }
        )

    def handle_tournament_mode(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande tournament_mode"""

        profile["score"] += 50

        if "Mode Tournoi" not in profile["badges"]:
            profile["badges"].append("Mode Tournoi")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 MODE TOURNOI ACTIVE !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Mode Tournoi",
                "profile_updated": True,
            }
        )

    def handle_team_battle(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande team_battle"""

        profile["score"] += 70

        if "Bataille d'Équipes" not in profile["badges"]:
            profile["badges"].append("Bataille d'Équipes")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 BATTERIE D'ÉQUIPES RÉUSSIE !\n\n🎯 +70 points !",
                "score_gagne": 70,
                "badge": "Bataille d'Équipes",
                "profile_updated": True,
            }
        )

    def handle_leaderboard(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🏆",
                "message": generic_immersive_message(
                    "🏆 CLASSEMENT DES HACKERS",
                    "Découvre le classement des meilleurs hackers d'Arkalia Quest. Seras-tu dans le top 10 ?",
                    "Affronte tes amis et grimpe dans le classement !",
                ),
                "profile_updated": False,
            }
        )

    def handle_challenge_friend(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande challenge_friend"""

        profile["score"] += 50

        if "Défi Ami" not in profile["badges"]:
            profile["badges"].append("Défi Ami")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 DÉFI AMI LANCÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Défi Ami",
                "profile_updated": True,
            }
        )

    def handle_missions_bonus(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande missions_bonus"""

        profile["score"] += 50

        if "Missions Bonus" not in profile["badges"]:
            profile["badges"].append("Missions Bonus")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🎯",
                "message": "🎯 MISSIONS BONUS RÉUSSIES !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Missions Bonus",
                "profile_updated": True,
            }
        )

    def handle_status_system(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande status_system"""

        profile["score"] += 50

        if "Statut Système" not in profile["badges"]:
            profile["badges"].append("Statut Système")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 STATUT SYSTÈME RÉUSSI !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Statut Système",
                "profile_updated": True,
            }
        )

    def handle_test_commande(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande test_commande"""

        profile["score"] += 50

        if "Test Commande" not in profile["badges"]:
            profile["badges"].append("Test Commande")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 TEST COMMANDE RÉUSSI !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Test Commande",
                "profile_updated": True,
            }
        )

    def handle_clear_terminal(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande clear_terminal"""

        profile["score"] += 50

        if "Terminal Nettoyé" not in profile["badges"]:
            profile["badges"].append("Terminal Nettoyé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 TERMINAL NETTOYÉ !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Terminal Nettoyé",
                "profile_updated": True,
            }
        )

    def handle_start_tutorial(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande start_tutorial - VRAI TUTORIEL INTERACTIF"""

        # Vérifier si c'est la première fois
        if "tutorial_step" not in profile:
            profile["tutorial_step"] = 1
            profile["score"] += 10

        step = profile["tutorial_step"]

        if step == 1:
            profile["tutorial_step"] = 2
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🎯",
                    "message": """🎯 TUTORIEL ARKALIA QUEST - ÉTAPE 1/5

🚀 BIENVENUE HACKER !

Tu es maintenant dans le terminal d'Arkalia Quest, un univers de hacking épique !

📋 TES PREMIERS OBJECTIFS :
1. ✅ Tu es connecté (fait !)
2. 🔄 Parle à LUNA (tape 'luna_contact')
3. 🔍 Analyse ta personnalité (tape 'scan_persona')
4. 🌍 Débloque l'univers (tape 'unlock_universe')
5. 🎮 Charge ta première mission (tape 'load_mission')

💡 TAPE 'luna_contact' POUR CONTINUER LE TUTORIEL !""",
                    "score_gagne": 10,
                    "tutorial_mode": True,
                    "next_command": "luna_contact",
                    "profile_updated": True,
                }
            )

        elif step == 2:
            profile["tutorial_step"] = 3
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🌙",
                    "message": """🌙 ÉTAPE 2/5 - CONTACT AVEC LUNA

✅ Excellent ! Tu as contacté LUNA !

🌙 LUNA est ton IA rebelle, ton partenaire de hacking. Elle t'aidera dans tes missions !

📋 PROCHAINE ÉTAPE :
🔍 Analyse ta personnalité pour découvrir ton type de hacker !

💡 TAPE 'scan_persona' POUR CONTINUER !""",
                    "score_gagne": 15,
                    "tutorial_mode": True,
                    "next_command": "scan_persona",
                    "profile_updated": True,
                }
            )

        elif step == 3:
            profile["tutorial_step"] = 4
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🔍",
                    "message": """🔍 ÉTAPE 3/5 - ANALYSE PERSONNALITÉ

✅ Parfait ! Ton profil hacker a été analysé !

🎭 Tu as maintenant un type de personnalité unique qui influence tes missions !

�� PROCHAINE ÉTAPE :
🌍 Débloque l'univers Arkalia pour accéder aux missions !

💡 TAPE 'unlock_universe' POUR CONTINUER !""",
                    "score_gagne": 20,
                    "tutorial_mode": True,
                    "next_command": "unlock_universe",
                    "profile_updated": True,
                }
            )

        elif step == 4:
            profile["tutorial_step"] = 5
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🌌",
                    "message": """🌌 ÉTAPE 4/5 - UNIVERS DÉBLOQUÉ

✅ INCROYABLE ! L'univers Arkalia est maintenant accessible !

🌟 Tu peux maintenant explorer différents mondes et missions !

📋 DERNIÈRE ÉTAPE :
🎮 Charge ta première mission pour commencer l'aventure !

💡 TAPE 'load_mission' POUR TERMINER LE TUTORIEL !""",
                    "score_gagne": 25,
                    "tutorial_mode": True,
                    "next_command": "load_mission",
                    "profile_updated": True,
                }
            )

        elif step == 5:
            # Tutoriel terminé
            profile["tutorial_step"] = "completed"
            profile["score"] += 30
            if "Tutoriel Maître" not in profile["badges"]:
                profile["badges"].append("Tutoriel Maître")

            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🏆",
                    "message": """🏆 TUTORIEL TERMINÉ - ÉTAPE 5/5

🎉 FÉLICITATIONS HACKER ! Tu as terminé le tutoriel !

🌟 TU PEUX MAINTENANT :
• 🎮 Utiliser toutes les commandes
• 🌍 Explorer l'univers Arkalia
• 🏆 Gagner des badges
• ⚔️ Affronter La Corp
• 🌙 Parler avec LUNA

💡 COMMANDES UTILES :
• 'aide' - Liste des commandes
• 'profil' - Ton profil
• 'monde' - Accès au monde
• 'badges' - Tes badges

🚀 L'AVENTURE COMMENCE MAINTENANT !""",
                    "score_gagne": 30,
                    "badge": "Tutoriel Maître",
                    "tutorial_completed": True,
                    "profile_updated": True,
                }
            )

        else:
            # Tutoriel déjà terminé
            return self.format_response(
                {
                    "réussite": True,
                    "ascii_art": "🎯",
                    "message": """🎯 TUTORIEL DÉJÀ TERMINÉ !

Tu as déjà complété le tutoriel avec succès !

💡 RAPPELLES-TOI :
• 'aide' - Liste des commandes
• 'profil' - Ton profil
• 'monde' - Accès au monde
• 'badges' - Tes badges

🚀 Continue tes exploits !""",
                    "profile_updated": False,
                }
            )

    def handle_luna_dance(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande luna_dance"""

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": self.get_ascii_art("luna_dance"),
                "message": "🌙 LUNA : Tu veux que je danse ? OK, regarde ça ! 💃🕺\n\n🎵 *LUNA se met à danser frénétiquement*\n\n🤖 LUNA : C'est ma danse de victoire ! Maintenant à toi de jouer !",
                "score_gagne": 50,
                "badge": "🕺 Dance Partner",
                "profile_updated": True,
            }
        )

    def handle_boss_final(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande boss_final"""

        boss_ascii = """╔══════════════════════════════════════╗
║           LA CORP BOSS               ║
║         [][][][][][][][]             ║
║         ════════════════             ║
║         ║  DESTROY MODE  ║           ║
║         ════════════════             ║
║         ║  HP: ████████  ║           ║
║         ════════════════             ║
╚══════════════════════════════════════╝"""

        profile["score"] += 100

        if "Boss Slayer" not in profile["badges"]:
            profile["badges"].append("Boss Slayer")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": boss_ascii,
                "message": "👹 BOSS FINAL APPARAÎT !\n\n💀 LA CORP BOSS : Tu oses me défier ?\n⚔️ Prépare-toi à mourir, hacker !\n\n🎯 +100 points pour ton courage !",
                "score_gagne": 100,
                "badge": "Boss Slayer",
                "profile_updated": True,
            }
        )

    def handle_help(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande help"""

        aide_text = """🎮 ARKALIA QUEST - AIDE

🌟 Commandes principales :
• unlock_universe - Débloque l'univers
• scan_persona - Analyse ta personnalité
• load_mission - Charge une mission
• reboot_world - Redémarre le monde
• decode_portal - Déchiffre un portail
• hacker_coffre - Pirate un coffre

🎯 Commandes spéciales :
• luna_dance - LUNA danse
• boss_final - Boss final ASCII
• challenge_corp - Défi contre La Corp

💡 Commandes utiles :
• aide - Affiche cette aide
• profil - Affiche ton profil
• monde - Accède au monde

🌙 Easter eggs :
• luna_dance - LUNA qui danse
• boss_final - Boss final épique

🎮 Amuse-toi bien !"""

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "❓",
                "message": aide_text,
                "profile_updated": False,
            }
        )

    def handle_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande profile"""

        score = profile.get("score", 0)
        badges = profile.get("badges", [])
        progression = profile.get("progression", {})

        profil_text = f"""👤 TON PROFIL

📊 Score : {score} points
🏆 Badges : {len(badges)}
🌍 Univers débloqués : {len(progression.get('univers_debloques', []))}
🚪 Portails ouverts : {len(progression.get('portails_ouverts', []))}

🏅 Badges obtenus :
{chr(10).join(['• ' + badge for badge in badges]) if badges else 'Aucun badge encore'}

💡 Continue tes exploits !"""

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "👤",
                "message": profil_text,
                "profile_updated": False,
            }
        )

    def handle_world(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande world"""

        univers = profile.get("progression", {}).get("univers_debloques", [])
        portails = profile.get("progression", {}).get("portails_ouverts", [])

        monde_text = f"""🌍 MONDE ARKALIA DÉBLOQUÉ !

🌟 Univers disponibles :
{chr(10).join(['• ' + uni.replace('_', ' ').title() for uni in univers])}

🚪 Portails ouverts :
{chr(10).join(['• ' + port.replace('_', ' ').title() for port in portails]) if portails else 'Aucun portail ouvert'}

💡 Commandes disponibles dans ce monde :
• load_mission - Charge une nouvelle mission
• decode_portal - Déchiffre un nouveau portail
• reboot_world - Redémarre le monde
• scan_persona - Analyse ta personnalité
• luna - Parle avec LUNA

🎮 Va sur http://localhost:5001/monde pour l'interface graphique !"""

        profile["score"] += 10

        if "Explorateur du Monde" not in profile["badges"]:
            profile["badges"].append("Explorateur du Monde")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": self.get_ascii_art("monde"),
                "message": monde_text,
                "score_gagne": 10,
                "badge": "Explorateur du Monde",
                "profile_updated": True,
            }
        )

    def handle_status(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande status"""

        score = profile.get("score", 0)
        badges = profile.get("badges", [])
        univers = profile.get("progression", {}).get("univers_debloques", [])
        portails = profile.get("progression", {}).get("portails_ouverts", [])

        # Calculer le niveau basé sur le score
        level = min(10, max(1, score // 1000 + 1))
        progress = (score % 1000) / 1000 * 100

        status_text = f"""🌟 STATUT DU SYSTÈME ARKALIA QUEST

🎯 INFORMATIONS PRINCIPALES :
• Score actuel : {score} points
• Niveau : {level}/10 (Progression : {progress:.1f}%)
• Badges obtenus : {len(badges)}/50
• Univers débloqués : {len(univers)}
• Portails ouverts : {len(portails)}

🏆 BADGES RÉCENTS :
{chr(10).join(['• ' + badge for badge in badges[-5:]]) if badges else 'Aucun badge encore'}

🌍 PROGRESSION :
• Univers disponibles : {', '.join(univers) if univers else 'Aucun'}
• Portails accessibles : {', '.join(portails[:5]) if portails else 'Aucun'}{'...' if len(portails) > 5 else ''}

💡 PROCHAINES ÉTAPES :
• Complète des missions pour gagner des points
• Débloque de nouveaux univers
• Collectionne tous les badges
• Défie tes amis sur le leaderboard

🎮 Continue tes exploits, hacker !"""

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌟",
                "message": status_text,
                "profile_updated": False,
            }
        )

    def handle_clear(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande clear"""

        profile["score"] += 50

        if "Terminal Nettoyé" not in profile["badges"]:
            profile["badges"].append("Terminal Nettoyé")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": """🌙 TERMINAL NETTOYÉ AVEC SUCCÈS !\n\n🧹 Historique effacé, mémoire optimisée, interface rafraîchie.\n\n💡 Astuce : Un terminal propre, c'est la base d'un vrai hacker ! Continue tes exploits pour débloquer de nouveaux badges et secrets !""",
                "score_gagne": 50,
                "badge": "Terminal Nettoyé",
                "profile_updated": True,
            }
        )

    def handle_test(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande test"""

        profile["score"] += 50

        if "Test Réussi" not in profile["badges"]:
            profile["badges"].append("Test Réussi")

        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🌙",
                "message": "🌙 TEST RÉUSSI !\n\n🎯 +50 points !",
                "score_gagne": 50,
                "badge": "Test Réussi",
                "profile_updated": True,
            }
        )

    # Gestionnaires pour les commandes de test et de mission
    def handle_complete_objective(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande complete_objective"""
        profile["score"] += 25
        return self.format_response(
            {
                "réussite": True,
                "message": "✅ Objectif complété ! +25 points",
                "score_gagne": 25,
                "profile_updated": True,
            }
        )

    def handle_solve_puzzle(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande solve_puzzle"""
        profile["score"] += 30
        return self.format_response(
            {
                "réussite": True,
                "message": "🧩 Puzzle résolu ! +30 points",
                "score_gagne": 30,
                "profile_updated": True,
            }
        )

    def handle_hack_success(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande hack_success"""
        profile["score"] += 40
        return self.format_response(
            {
                "réussite": True,
                "message": "💻 Hack réussi ! +40 points",
                "score_gagne": 40,
                "profile_updated": True,
            }
        )

    def handle_find_secret(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande find_secret"""
        profile["score"] += 35
        return self.format_response(
            {
                "réussite": True,
                "message": "🔍 Secret trouvé ! +35 points",
                "score_gagne": 35,
                "profile_updated": True,
            }
        )

    def handle_help_character(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande help_character"""
        profile["score"] += 20
        return self.format_response(
            {
                "réussite": True,
                "message": "🤝 Personnage aidé ! +20 points",
                "score_gagne": 20,
                "profile_updated": True,
            }
        )

    def handle_explore_area(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande explore_area"""
        profile["score"] += 15
        return self.format_response(
            {
                "réussite": True,
                "message": "🗺️ Zone explorée ! +15 points",
                "score_gagne": 15,
                "profile_updated": True,
            }
        )

    def handle_master_skill(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande master_skill"""
        profile["score"] += 50
        return self.format_response(
            {
                "réussite": True,
                "message": "🎯 Compétence maîtrisée ! +50 points",
                "score_gagne": 50,
                "profile_updated": True,
            }
        )

    def handle_save_progress(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande save_progress"""
        return self.format_response(
            {
                "réussite": True,
                "message": "💾 Progression sauvegardée !",
                "profile_updated": False,
            }
        )

    def handle_save_game(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande save_game"""
        return self.format_response(
            {
                "réussite": True,
                "message": "💾 Jeu sauvegardé !",
                "profile_updated": False,
            }
        )

    def handle_save_state(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande save_state"""
        return self.format_response(
            {
                "réussite": True,
                "message": "💾 État sauvegardé !",
                "profile_updated": False,
            }
        )

    def handle_backup_data(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande backup_data"""
        return self.format_response(
            {
                "réussite": True,
                "message": "💾 Données sauvegardées !",
                "profile_updated": False,
            }
        )

    def handle_basic_hack(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande basic_hack"""
        profile["score"] += 20
        return self.format_response(
            {
                "réussite": True,
                "message": "💻 Hack basique réussi ! +20 points",
                "score_gagne": 20,
                "profile_updated": True,
            }
        )

    def handle_simple_puzzle(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande simple_puzzle"""
        profile["score"] += 25
        return self.format_response(
            {
                "réussite": True,
                "message": "🧩 Puzzle simple résolu ! +25 points",
                "score_gagne": 25,
                "profile_updated": True,
            }
        )

    def handle_intro_dialogue(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande intro_dialogue"""
        profile["score"] += 10
        return self.format_response(
            {
                "réussite": True,
                "message": "💬 Dialogue d'introduction terminé ! +10 points",
                "score_gagne": 10,
                "profile_updated": True,
            }
        )

    def handle_decoder_challenge(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande decoder_challenge"""
        profile["score"] += 45
        return self.format_response(
            {
                "réussite": True,
                "message": "🔐 Défi de déchiffrement réussi ! +45 points",
                "score_gagne": 45,
                "profile_updated": True,
            }
        )

    def handle_pattern_recognition(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande pattern_recognition"""
        profile["score"] += 35
        return self.format_response(
            {
                "réussite": True,
                "message": "🔍 Reconnaissance de motifs réussie ! +35 points",
                "score_gagne": 35,
                "profile_updated": True,
            }
        )

    def handle_advanced_hack(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande advanced_hack"""
        profile["score"] += 60
        return self.format_response(
            {
                "réussite": True,
                "message": "💻 Hack avancé réussi ! +60 points",
                "score_gagne": 60,
                "profile_updated": True,
            }
        )

    def handle_complex_puzzle(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande complex_puzzle"""
        profile["score"] += 55
        return self.format_response(
            {
                "réussite": True,
                "message": "🧩 Puzzle complexe résolu ! +55 points",
                "score_gagne": 55,
                "profile_updated": True,
            }
        )

    def handle_multi_step_hack(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande multi_step_hack"""
        profile["score"] += 70
        return self.format_response(
            {
                "réussite": True,
                "message": "💻 Hack multi-étapes réussi ! +70 points",
                "score_gagne": 70,
                "profile_updated": True,
            }
        )

    def handle_character_interaction(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande character_interaction"""
        profile["score"] += 25
        return self.format_response(
            {
                "réussite": True,
                "message": "👥 Interaction avec personnage réussie ! +25 points",
                "score_gagne": 25,
                "profile_updated": True,
            }
        )

    def handle_escape_sequence(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande escape_sequence"""
        profile["score"] += 80
        return self.format_response(
            {
                "réussite": True,
                "message": "🏃 Séquence d'évasion réussie ! +80 points",
                "score_gagne": 80,
                "profile_updated": True,
            }
        )

    def handle_time_pressure(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande time_pressure"""
        profile["score"] += 65
        return self.format_response(
            {
                "réussite": True,
                "message": "⏰ Défi sous pression temporelle réussi ! +65 points",
                "score_gagne": 65,
                "profile_updated": True,
            }
        )

    def handle_resource_management(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande resource_management"""
        profile["score"] += 40
        return self.format_response(
            {
                "réussite": True,
                "message": "📊 Gestion des ressources réussie ! +40 points",
                "score_gagne": 40,
                "profile_updated": True,
            }
        )

    def handle_ai_dialogue(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande ai_dialogue"""
        profile["score"] += 30
        return self.format_response(
            {
                "réussite": True,
                "message": "🤖 Dialogue avec IA réussi ! +30 points",
                "score_gagne": 30,
                "profile_updated": True,
            }
        )

    def handle_moral_choices(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande moral_choices"""
        profile["score"] += 50
        return self.format_response(
            {
                "réussite": True,
                "message": "⚖️ Choix moral effectué ! +50 points",
                "score_gagne": 50,
                "profile_updated": True,
            }
        )

    def handle_consequence_management(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande consequence_management"""
        profile["score"] += 45
        return self.format_response(
            {
                "réussite": True,
                "message": "🎯 Gestion des conséquences réussie ! +45 points",
                "score_gagne": 45,
                "profile_updated": True,
            }
        )

    def handle_missions(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande missions"""
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "📋",
                "message": generic_immersive_message(
                    "📋 LISTE DES MISSIONS DISPONIBLES",
                    "Découvre toutes les missions d'Arkalia Quest et choisis ton prochain défi !",
                    "Plus tu complètes de missions, plus tu gagnes de badges et d'XP !",
                ),
                "profile_updated": False,
            }
        )

    def handle_achievements(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🎖️",
                "message": generic_immersive_message(
                    "🎖️ SUCCÈS DÉBLOQUÉS",
                    "Voici tous les succès que tu as remportés. Continue à relever des défis pour tous les obtenir !",
                    "Certains succès sont cachés... sauras-tu les trouver ?",
                ),
                "profile_updated": False,
            }
        )

    def handle_test_performance(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "⚡",
                "message": generic_immersive_message(
                    "⚡ TEST DE PERFORMANCE",
                    "Tu viens de lancer un test de performance sur le système Arkalia Quest.",
                    "La rapidité, c'est la clé pour un hacker efficace !",
                ),
                "profile_updated": False,
            }
        )

    def handle_test_security(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🛡️",
                "message": generic_immersive_message(
                    "🛡️ TEST DE SÉCURITÉ",
                    "Tu viens de lancer un test de sécurité avancé sur le système.",
                    "La sécurité, c'est la base pour survivre dans Arkalia !",
                ),
                "profile_updated": False,
            }
        )

    def handle_test_database(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        return self.format_response(
            {
                "réussite": True,
                "ascii_art": "🗄️",
                "message": generic_immersive_message(
                    "🗄️ TEST DE BASE DE DONNÉES",
                    "Vérification de l'intégrité de la base de données en cours...",
                    "Une base saine, c'est la garantie de ne rien perdre !",
                ),
                "profile_updated": False,
            }
        )
