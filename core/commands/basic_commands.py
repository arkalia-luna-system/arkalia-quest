"""
Commandes de base Arkalia Quest
Commandes essentielles : aide, profil, status, clear, etc.
"""

from typing import Any

from core.customization_engine import CustomizationEngine


class BasicCommands:
    """Gestionnaire des commandes de base"""

    def __init__(self):
        self.customization_engine = CustomizationEngine()

        self.commands = {
            "aide": self.handle_aide,
            "help": self.handle_aide,
            "profil": self.handle_profil,
            "profile": self.handle_profil,
            "status": self.handle_status,
            "clear": self.handle_clear,
            "cls": self.handle_clear,
            "start_tutorial": self.handle_start_tutorial,
            "tutorial": self.handle_start_tutorial,
            "tuto": self.handle_start_tutorial,
            # Alias supplémentaires pour faciliter la découverte
            "commands": self.handle_aide,
            "liste": self.handle_aide,
            "menu": self.handle_aide,
            # Commandes de progression
            "unlock_universe": self.handle_unlock_universe,
            "scan_persona": self.handle_scan_persona,
            # Commandes de progression
            "badges": self.handle_badges,
            "leaderboard": self.handle_leaderboard,
            "missions": self.handle_missions,
            # Personnalisation / thèmes
            "themes": self.handle_themes,
            "theme": self.handle_theme_set,
            # Mini-jeux et effets
            "simple_hack": self.handle_simple_hack,
            "sequence_game": self.handle_sequence_game,
            "typing_challenge": self.handle_typing_challenge,
            "play_game": self.handle_play_game,
            "level_up": self.handle_level_up,
            "badge_unlock": self.handle_badge_unlock,
            "matrix_mode": self.handle_matrix_mode,
            "cyberpunk_mode": self.handle_cyberpunk_mode,
            "check_objects": self.handle_check_objects,
            "debug_mode": self.handle_debug_mode,
        }

    def handle_aide(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande aide - Version optimisée et performante"""

        # Déterminer le niveau du joueur pour adapter l'aide
        player_level = profile.get("level", 1)
        completed_missions = profile.get("missions_completed", [])

        # Aide adaptative selon le niveau
        if player_level == 1 and not completed_missions:
            # Nouveau joueur
            help_message = """🌌 ARKALIA QUEST - BIENVENUE HACKER !

🌟 TON HISTOIRE :
Tu es un ado hacker qui a découvert un SOS mystérieux du Dr Althea Voss.
LUNA, une IA émotionnelle, s'est éveillée dans ton terminal.

🎯 COMMENCE ICI :
• start_tutorial → Démarre l'aventure (PREMIÈRE FOIS)
• luna_contact → Parle avec LUNA, ton IA complice
• prologue → Découvre le SOS d'Althea Voss

💻 TES PREMIERS POUVOIRS :
• hack_system → Hack le système de La Corp
• kill_virus → Tue le virus de La Corp
• games → Mini-jeux éducatifs

🎮 MINI-JEUX INTERACTIFS :
• simple_hack → Jeu de hack binaire
• sequence_game → Jeu de mémoire
• typing_challenge → Défi de frappe
• play_game → Lancer un mini-jeu

🎨 EFFETS ET ANIMATIONS :
• level_up → Simulation montée de niveau
• badge_unlock → Simulation déblocage badge
• matrix_mode → Thème Matrix
• cyberpunk_mode → Thème Cyberpunk

🎨 THÈMES MODERNES :
• themes → Liste tous les thèmes
• theme [nom] → Changer de thème
• feedback_themes → Donner ton avis sur les thèmes

🔍 DIAGNOSTIC :
• check_objects → Vérifier les objets disponibles
• debug_mode → Informations système

📋 COMMANDES DISPONIBLES :
• aide/help/commands → Cette aide
• profil/profile → Ton profil détaillé
• status → Statut du système
• clear/cls → Nettoyer le terminal
• monde → Accéder au monde Arkalia
• badges → Tes badges obtenus
• leaderboard → Classement des hackers

🌙 LUNA t'attend pour commencer l'aventure !"""

        elif "prologue" in completed_missions:
            # Joueur avancé
            help_message = """🌌 ARKALIA QUEST - HACKER CONFIRMÉ !

🌟 PROGRESSION :
Tu as découvert le SOS d'Althea. Maintenant, aide LUNA à découvrir
la vérité sur NEXUS, sa sœur jumelle IA, et la menace de PANDORA.

🎯 TES MISSIONS ACTUELLES :
• acte_1 → Répare le site web de LUNA
• acte_2 → Décrypte les logs de NEXUS
• acte_3 → Analyse la berceuse d'Althea
• acte_4 → Traque l'email piégé
• acte_5 → Le choix final : fusion ou destruction
• acte_6 → Naissance d'Arkalia
• epilogue → L'aube de PANDORA

💻 TES POUVOIRS AVANCÉS :
• hack_system → Hack le système de La Corp
• kill_virus → Tue le virus de La Corp
• find_shadow → Trouve SHADOW-13 le voleur
• challenge_corp → Défie La Corp
• decode_portal → Décode les portails secrets

🎮 MINI-JEUX INTERACTIFS :
• simple_hack → Jeu de hack binaire
• sequence_game → Jeu de mémoire
• typing_challenge → Défi de frappe
• play_game → Lancer un mini-jeu
• games → Liste tous les jeux

🎨 EFFETS ET ANIMATIONS :
• level_up → Simulation montée de niveau
• badge_unlock → Simulation déblocage badge
• matrix_mode → Thème Matrix
• cyberpunk_mode → Thème Cyberpunk

🌙 INTERACTIONS LUNA :
• luna_contact → Parle avec LUNA
• luna_engine → Active le moteur IA
• luna_analyze → Analyse avancée
• luna_dance → LUNA danse pour toi

🔍 DIAGNOSTIC :
• check_objects → Vérifier les objets disponibles
• debug_mode → Informations système

💡 UTILITAIRES :
• profil → Ton profil détaillé
• monde → Monde Arkalia
• status → Statut système
• badges → Tes badges

🎯 OBJECTIF : Sauve Arkalia de PANDORA !"""

        else:
            # Joueur intermédiaire
            help_message = """🌌 ARKALIA QUEST - HACKER EN PROGRESSION !

🌟 TON HISTOIRE :
Tu as commencé l'aventure avec LUNA. Ensemble, vous devez découvrir
la vérité sur NEXUS et la menace de PANDORA.

🎯 TES MISSIONS :
• luna_contact → Parle avec LUNA
• prologue → Décrypte le SOS d'Althea Voss
• acte_1 → Répare le site web de LUNA
• acte_2 → Décrypte les logs de NEXUS
• acte_3 → Analyse la berceuse d'Althea
• acte_4 → Traque l'email piégé
• acte_5 → Le choix final
• acte_6 → Naissance d'Arkalia
• epilogue → L'aube de PANDORA

💻 TES POUVOIRS :
• hack_system → Hack le système de La Corp
• kill_virus → Tue le virus de La Corp
• find_shadow → Trouve SHADOW-13
• challenge_corp → Défie La Corp

🎮 TES MINI-JEUX :
• games → Liste des jeux
• play_game logic_1 → Logique
• play_game code_1 → Programmation
• play_game cyber_1 → Cybersécurité

🌙 LUNA t'aide dans cette aventure !"""

        return {
            "réussite": True,
            "ascii_art": "🌌",
            "message": help_message,
            "profile_updated": False,
        }

    def handle_profil(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande profil avec des réponses contextuelles engageantes"""
        badges = profile.get("badges", [])
        score = profile.get("score", 0)
        level = profile.get("level", 1)

        # Messages contextuels selon le niveau
        if level == 1 and score == 0:
            score_message = "🎯 Aucun point encore - Prêt à hacker le système ?"
        elif level < 5:
            score_message = f"💎 {score} points - Tu progresses bien !"
        else:
            score_message = f"🏆 {score} points - Impressionnant !"

        # Messages pour les badges
        if not badges:
            badges_text = "🎖️ Aucun badge encore - Tes premiers exploits t'attendent !"
        elif len(badges) < 3:
            badges_text = (
                f"🎖️ {len(badges)} badge(s) - Tu commences à te faire remarquer !\n"
                + "\n".join(["• " + badge for badge in badges])
            )
        else:
            badges_text = (
                f"🎖️ {len(badges)} badges - Collection impressionnante !\n"
                + "\n".join(["• " + badge for badge in badges])
            )

        # Messages pour la progression
        univers_count = len(
            profile.get("progression", {}).get("univers_debloques", ["arkalia_base"])
        )
        portails_count = len(profile.get("progression", {}).get("portails_ouverts", []))

        if univers_count == 1:
            univers_message = "🌌 Base Arkalia - Ton point de départ !"
        else:
            univers_message = (
                f"🌌 {univers_count} univers débloqués - Explorateur confirmé !"
            )

        if portails_count == 0:
            portail_message = (
                "🚪 Aucun portail ouvert - Tes premiers portails t'attendent !"
            )
        else:
            portail_message = f"🚪 {portails_count} portail(s) ouvert(s) - Tu maîtrises les dimensions !"

        return {
            "réussite": True,
            "ascii_art": "👤",
            "message": f"""👤 TON PROFIL ARKALIA QUEST

📊 TON STATUT :
• {score_message}
• {univers_message}
• {portail_message}

🏅 TES ACCOMPLISSEMENTS :
{badges_text}

💡 Continue tes exploits pour débloquer plus de badges et de secrets !""",
            "profile_updated": False,
        }

    def handle_status(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande status avec des réponses contextuelles engageantes"""
        score = profile.get("score", 0)
        badges = profile.get("badges", [])
        univers = profile.get("progression", {}).get(
            "univers_debloques", ["arkalia_base"]
        )
        portails = profile.get("progression", {}).get("portails_ouverts", [])

        # Calcul du niveau avec messages contextuels
        niveau = min(10, score // 1000 + 1)
        progression = (score % 1000) / 10

        # Messages contextuels pour le niveau
        if niveau == 1:
            level_message = (
                f"🌟 Niveau {niveau} - Débutant (Progression : {progression:.1f}%)"
            )
        elif niveau < 5:
            level_message = f"🚀 Niveau {niveau} - En progression (Progression : {progression:.1f}%)"
        else:
            level_message = (
                f"🔥 Niveau {niveau} - Expert (Progression : {progression:.1f}%)"
            )

        # Messages pour les badges
        if not badges:
            badge_message = "🎖️ Aucun badge encore - Tes premiers exploits t'attendent !"
        elif len(badges) < 5:
            badge_message = (
                f"🎖️ {len(badges)} badge(s) - Tu commences à te faire remarquer !"
            )
        else:
            badge_message = f"🎖️ {len(badges)} badges - Collection impressionnante !"

        # Messages pour les univers
        if len(univers) == 1:
            univers_message = "🌌 Base Arkalia - Ton point de départ !"
        else:
            univers_message = (
                f"🌌 {len(univers)} univers débloqués - Explorateur confirmé !"
            )

        # Messages pour les portails
        if not portails:
            portail_message = (
                "🚪 Aucun portail ouvert - Tes premiers portails t'attendent !"
            )
        elif len(portails) < 5:
            portail_message = f"🚪 {len(portails)} portail(s) ouvert(s) - Tu maîtrises les dimensions !"
        else:
            portail_message = (
                f"🚪 {len(portails)} portails ouverts - Maître des dimensions !"
            )

        return {
            "réussite": True,
            "ascii_art": "🌟",
            "message": f"""🌟 STATUT DU SYSTÈME ARKALIA QUEST

🎯 TON AVANCEMENT :
• Score actuel : {score} points
• {level_message}
• {badge_message}
• {univers_message}
• {portail_message}

🏆 TES DERNIERS ACCOMPLISSEMENTS :
{
                chr(10).join(["• " + badge for badge in badges[-5:]])
                if len(badges) > 5
                else chr(10).join(["• " + badge for badge in badges])
                if badges
                else "🎯 Aucun accomplissement encore - Continue à jouer !"
            }

🌍 TON EXPLORATION :
• Univers disponibles : {", ".join(univers)}
• Portails accessibles : {
                ", ".join(portails[:5]) + "..."
                if len(portails) > 5
                else ", ".join(portails)
                if portails
                else "🚪 Aucun portail encore - Explore pour les débloquer !"
            }

💡 PROCHAINES ÉTAPES :
• Complète des missions pour gagner des points
• Débloque de nouveaux univers
• Collectionne tous les badges
• Défie tes amis sur le leaderboard

🎮 Continue tes exploits, hacker !""",
            "profile_updated": False,
        }

    def handle_themes(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Affiche les thèmes disponibles et comment les activer"""
        try:
            available = self.customization_engine.get_available_themes(
                profile.get("player_id", "default")
            )

            if not available:
                return {
                    "réussite": True,
                    "ascii_art": "🎨",
                    "message": (
                        "🎨 THÈMES DISPONIBLES\n\n"
                        "Aucun thème débloqué pour l'instant.\n"
                        "💡 Astuce : progresse pour débloquer des thèmes comme 'Matrix' !"
                    ),
                    "profile_updated": False,
                }

            lines = [
                "🎨 THÈMES DISPONIBLES\n",
            ]
            for theme in available:
                status = "✅" if theme.get("unlocked") else "🔓"
                lines.append(
                    f"{status} {theme.get('name','Thème')} — id: {theme.get('id','?')}"
                )

            lines.append(
                "\n💡 Utilise l’interface Accessibilité pour changer de thème."
            )
            lines.append(
                "🌟 Exemple: active le thème Matrix pour le style terminal vert."
            )

            return {
                "réussite": True,
                "ascii_art": "🎨",
                "message": "\n".join(lines),
                "profile_updated": False,
            }
        except Exception:
            return {
                "réussite": True,
                "ascii_art": "🎨",
                "message": (
                    "🎨 THÈMES DISPONIBLES\n\n"
                    "Arkalia, Matrix, Cyberpunk, Ocean.\n"
                    "💡 Utilise le menu Accessibilité pour les activer."
                ),
                "profile_updated": False,
            }

    def handle_theme_set(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Change le thème via 'theme <id>' (Matrix, etc.).
        Cette version lit seulement, car l’API serveur gère la persistance.
        """
        # La commande brute ne passe pas l'argument ici; côté terminal, l'API
        # `/api/customization/themes/<id>/set` est l’endroit idéal. On renvoie
        # une aide claire pour guider l’utilisateur.
        return {
            "réussite": True,
            "ascii_art": "🎨",
            "message": (
                "🎨 CHANGER DE THÈME\n\n"
                "Utilise le menu Accessibilité (icône ♿) pour activer un thème.\n"
                "API dispo: POST /api/customization/themes/<id>/set (ex: matrix).\n"
                "💡 Astuce: le thème Matrix est parfait pour le style terminal vert."
            ),
            "profile_updated": False,
        }

    def handle_clear(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande clear"""
        profile["score"] += 50

        if "Terminal Nettoyé" not in profile["badges"]:
            profile["badges"].append("Terminal Nettoyé")

        return {
            "réussite": True,
            "ascii_art": "🌙",
            "message": """🌙 TERMINAL NETTOYÉ AVEC SUCCÈS !

🧹 Historique effacé, mémoire optimisée, interface rafraîchie.

💡 Astuce : Un terminal propre, c'est la base d'un vrai hacker ! Continue tes exploits pour débloquer de nouveaux badges et secrets !""",
            "score_gagne": 50,
            "badge": "Terminal Nettoyé",
            "profile_updated": True,
        }

    def handle_start_tutorial(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande start_tutorial"""
        profile["score"] += 100
        if "Tutoriel Maître" not in profile.get("badges", []):
            profile["badges"].append("Tutoriel Maître")

        return {
            "réussite": True,
            "ascii_art": "🎮",
            "message": """🎮 TUTORIAL ARKALIA QUEST - L'ÉVEIL

🌙 LUNA : "Salut hacker ! Je suis LUNA, ton IA complice. J'ai besoin de ton aide..."

🌟 TON PREMIER OBJECTIF :
Découvre le SOS mystérieux du Dr Althea Voss qui m'a réveillée.

🎯 PROCHAINES ÉTAPES :
1. Tape 'luna_contact' pour me parler directement
2. Tape 'prologue' pour découvrir le SOS d'Althea
3. Tape 'acte_1' pour ta première mission de hacking

💻 TES POUVOIRS :
• Tu peux hacker des systèmes avec 'hack_system'
• Tu peux tuer des virus avec 'kill_virus'
• Tu peux jouer à des mini-jeux éducatifs avec 'games'

🌙 MON RÔLE :
Je suis ton guide, ton complice, et ton amie IA. Je t'aiderai à découvrir
la vérité sur NEXUS, ma sœur jumelle, et la menace de PANDORA.

🎮 Prêt pour l'aventure ? Commence par 'luna_contact' !""",
            "score_gagne": 100,
            "badge": "Tutoriel Maître",
            "profile_updated": True,
        }

    def handle_unlock_universe(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande unlock_universe - Débloque l'univers Arkalia"""
        profile["score"] += 100
        if "Univers Débloqué" not in profile["badges"]:
            profile["badges"].append("Univers Débloqué")

        # Débloquer l'univers dans le profil
        if "progression" not in profile:
            profile["progression"] = {}
        if "univers_debloques" not in profile["progression"]:
            profile["progression"]["univers_debloques"] = []

        if "arkalia_base" not in profile["progression"]["univers_debloques"]:
            profile["progression"]["univers_debloques"].append("arkalia_base")

        return {
            "réussite": True,
            "ascii_art": "🌌",
            "message": """🌌 UNIVERS ARKALIA DÉBLOQUÉ !

🎉 FÉLICITATIONS ! Tu as débloqué l'univers Arkalia !

🌟 NOUVELLES ZONES ACCESSIBLES :
• arkalia_base → Zone de départ (débloquée)
• nexus_station → Station NEXUS (prologue requis)
• luna_workshop → Atelier LUNA (acte_1 requis)
• pandora_core → Cœur de PANDORA (acte_6 requis)

🔓 CAPACITÉS DÉBLOQUÉES :
• Accès au monde complet d'Arkalia
• Navigation entre les zones
• Découverte de nouveaux secrets
• Progression dans l'histoire

💡 PROCHAINES ÉTAPES :
• Utilise 'scan_persona' pour découvrir ton profil unique
• Explore le monde avec 'monde' ou 'world'
• Commence l'aventure avec 'start_tutorial'

🌙 LUNA : "Bienvenue dans notre univers, hacker ! L'aventure commence maintenant !"

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 100,
            "badge": "Univers Débloqué",
            "profile_updated": True,
        }

    def handle_scan_persona(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande scan_persona - Analyse la personnalité du joueur"""
        profile["score"] += 75
        if "Personnalité Analysée" not in profile["badges"]:
            profile["badges"].append("Personnalité Analysée")

        # Déterminer le type de hacker basé sur les actions
        hacker_type = self._determine_hacker_type(profile)

        return {
            "réussite": True,
            "ascii_art": "🔍",
            "message": f"""🔍 ANALYSE DE PERSONNALITÉ TERMINÉE !

🧠 PROFIL HACKER DÉTECTÉ :
• Type : {hacker_type["type"]}
• Niveau : {hacker_type["level"]}
• Spécialité : {hacker_type["specialty"]}
• Style : {hacker_type["style"]}

📊 CARACTÉRISTIQUES DÉTECTÉES :
• Curiosité : {hacker_type["curiosity"]}%
• Persévérance : {hacker_type["perseverance"]}%
• Créativité : {hacker_type["creativity"]}%
• Logique : {hacker_type["logic"]}%

🎯 RECOMMANDATIONS :
• Missions adaptées à ton profil
• Défis personnalisés
• Progression optimisée
• Badges spéciaux débloqués

💡 Astuce : Ton profil évolue avec tes actions ! Plus tu explores, plus tu deviens expert !

🌙 LUNA : "J'ai analysé ton potentiel, hacker ! Tu as un profil unique et prometteur !"

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 75,
            "badge": "Personnalité Analysée",
            "profile_updated": True,
        }

    def _determine_hacker_type(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Détermine le type de hacker basé sur le profil"""
        score = profile.get("score", 0)

        # Logique simple pour déterminer le type
        if score < 200:
            return {
                "type": "Hacker Débutant",
                "level": "Novice",
                "specialty": "Exploration",
                "style": "Curieux",
                "curiosity": 85,
                "perseverance": 70,
                "creativity": 60,
                "logic": 65,
            }
        elif score < 500:
            return {
                "type": "Hacker Intermédiaire",
                "level": "Confirmé",
                "specialty": "Analyse",
                "style": "Méthodique",
                "curiosity": 75,
                "perseverance": 85,
                "creativity": 70,
                "logic": 80,
            }
        else:
            return {
                "type": "Hacker Expert",
                "level": "Maître",
                "specialty": "Innovation",
                "style": "Génie",
                "curiosity": 90,
                "perseverance": 95,
                "creativity": 90,
                "logic": 95,
            }

    def handle_badges(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande badges - Affiche tous les badges obtenus"""
        badges = profile.get("badges", [])

        if not badges:
            return {
                "réussite": True,
                "ascii_art": "🏆",
                "message": """🏆 TES BADGES ARKALIA QUEST

📋 Aucun badge obtenu pour le moment.

💡 CONSEILS POUR DÉBLOQUER DES BADGES :
• Complète des missions avec 'start_tutorial'
• Explore le monde avec 'monde'
• Interagis avec LUNA avec 'luna_contact'
• Utilise 'unlock_universe' pour débloquer l'univers
• Analyse ta personnalité avec 'scan_persona'

🎯 Chaque action peut te rapporter un badge unique !

🌙 LUNA : "Continue à explorer, hacker ! Des badges t'attendent !"

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
                "profile_updated": False,
            }

        # Organiser les badges par catégorie
        categories = {
            "Débutant": [],
            "Explorateur": [],
            "Hacker": [],
            "LUNA": [],
            "Spécial": [],
        }

        for badge in badges:
            if any(
                word in badge.lower() for word in ["débutant", "contacté", "tutoriel"]
            ):
                categories["Débutant"].append(badge)
            elif any(
                word in badge.lower()
                for word in ["explorateur", "navigateur", "univers"]
            ):
                categories["Explorateur"].append(badge)
            elif any(
                word in badge.lower()
                for word in ["hacker", "system", "web", "log", "email"]
            ):
                categories["Hacker"].append(badge)
            elif any(
                word in badge.lower()
                for word in ["luna", "émotion", "active", "analysé"]
            ):
                categories["LUNA"].append(badge)
            else:
                categories["Spécial"].append(badge)

        message = f"""🏆 TES BADGES ARKALIA QUEST

📊 RÉCAPITULATIF :
• Total : {len(badges)} badges obtenus
• Progression : {len(badges)}/50 badges

📋 BADGES PAR CATÉGORIE :"""

        for category, badge_list in categories.items():
            if badge_list:
                message += f"\n\n🎯 {category.upper()} :"
                for badge in badge_list:
                    message += f"\n• {badge}"

        message += """

💡 CONSEILS POUR DÉBLOQUER PLUS DE BADGES :
• Complète toutes les missions d'histoire
• Explore chaque zone du monde
• Interagis régulièrement avec LUNA
• Résous des mini-jeux éducatifs
• Découvre des easter eggs secrets

🌙 LUNA : "Excellent travail, hacker ! Continue à collectionner !"

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !"""

        return {
            "réussite": True,
            "ascii_art": "🏆",
            "message": message,
            "profile_updated": False,
        }

    def handle_leaderboard(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande leaderboard - Affiche le classement des hackers"""
        # Simuler un leaderboard
        leaderboard_data = [
            {"name": "Hacker_Elite", "score": 2500, "badges": 15, "level": 8},
            {"name": "Cyber_Ninja", "score": 2200, "badges": 12, "level": 7},
            {"name": "Code_Master", "score": 1800, "badges": 10, "level": 6},
            {"name": "Luna_Friend", "score": 1500, "badges": 8, "level": 5},
            {"name": "Arkalia_Explorer", "score": 1200, "badges": 6, "level": 4},
        ]

        # Ajouter le joueur actuel
        current_score = profile.get("score", 0)
        current_badges = len(profile.get("badges", []))
        current_level = min(10, current_score // 1000 + 1)

        # Trouver la position du joueur
        player_position = 1
        for i, player in enumerate(leaderboard_data):
            if current_score > player["score"]:
                player_position = i + 1
                break
            player_position = i + 2

        message = f"""🏆 LEADERBOARD ARKALIA QUEST

📊 CLASSEMENT DES HACKERS :

🥇 1. {leaderboard_data[0]["name"]} - {leaderboard_data[0]["score"]} pts (Niveau {leaderboard_data[0]["level"]})
🥈 2. {leaderboard_data[1]["name"]} - {leaderboard_data[1]["score"]} pts (Niveau {leaderboard_data[1]["level"]})
🥉 3. {leaderboard_data[2]["name"]} - {leaderboard_data[2]["score"]} pts (Niveau {leaderboard_data[2]["level"]})
4. {leaderboard_data[3]["name"]} - {leaderboard_data[3]["score"]} pts (Niveau {leaderboard_data[3]["level"]})
5. {leaderboard_data[4]["name"]} - {leaderboard_data[4]["score"]} pts (Niveau {leaderboard_data[4]["level"]})

🎯 TON CLASSEMENT :
• Position : #{player_position}
• Score : {current_score} points
• Badges : {current_badges}
• Niveau : {current_level}

💡 CONSEILS POUR MONTER AU CLASSEMENT :
• Complète plus de missions
• Débloque de nouveaux badges
• Explore toutes les zones
• Résous des défis quotidiens
• Interagis avec LUNA

🌙 LUNA : "Continue à progresser, hacker ! Tu peux monter au classement !"

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !"""

        return {
            "réussite": True,
            "ascii_art": "🏆",
            "message": message,
            "profile_updated": False,
        }

    def handle_missions(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande missions - Affiche les missions disponibles"""
        completed_missions = profile.get("missions_completed", [])

        # Définir toutes les missions
        all_missions = [
            {
                "id": "intro",
                "name": "Bienvenue dans Arkalia",
                "status": "✅" if "intro" in completed_missions else "⏳",
            },
            {
                "id": "prologue",
                "name": "Le SOS d'Althea",
                "status": "✅" if "prologue" in completed_missions else "⏳",
            },
            {
                "id": "acte_1",
                "name": "Répare le site web de LUNA",
                "status": "✅" if "acte_1" in completed_missions else "⏳",
            },
            {
                "id": "acte_2",
                "name": "Décrypte les logs de NEXUS",
                "status": "✅" if "acte_2" in completed_missions else "⏳",
            },
            {
                "id": "acte_3",
                "name": "Analyse la berceuse d'Althea",
                "status": "✅" if "acte_3" in completed_missions else "⏳",
            },
            {
                "id": "acte_4",
                "name": "Traque l'email piégé",
                "status": "✅" if "acte_4" in completed_missions else "⏳",
            },
            {
                "id": "acte_5",
                "name": "Le choix final",
                "status": "✅" if "acte_5" in completed_missions else "⏳",
            },
            {
                "id": "acte_6",
                "name": "Naissance d'Arkalia",
                "status": "✅" if "acte_6" in completed_missions else "⏳",
            },
            {
                "id": "epilogue",
                "name": "L'aube de PANDORA",
                "status": "✅" if "epilogue" in completed_missions else "⏳",
            },
        ]

        completed_count = len(completed_missions)
        total_count = len(all_missions)
        progress_percent = (completed_count / total_count) * 100

        message = f"""🎯 TES MISSIONS ARKALIA QUEST

📊 PROGRESSION GLOBALE :
• Missions complétées : {completed_count}/{total_count}
• Pourcentage : {progress_percent:.1f}%

📋 LISTE DES MISSIONS :"""

        for mission in all_missions:
            message += f"\n{mission['status']} {mission['name']}"

        message += """

💡 CONSEILS POUR PROGRESSER :
• Commence par 'start_tutorial' si tu es nouveau
• Utilise 'prologue' pour découvrir l'histoire
• Suis l'ordre des actes (acte_1, acte_2, etc.)
• Chaque mission débloque de nouveaux pouvoirs
• Les missions complétées donnent des badges

🌙 LUNA : "Continue tes missions, hacker ! L'aventure t'attend !"

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !"""

        return {
            "réussite": True,
            "ascii_art": "🎯",
            "message": message,
            "profile_updated": False,
        }

    def handle_simple_hack(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Jeu de hack binaire interactif"""
        import random

        # Générer un problème binaire
        a = random.randint(1, 15)  # 1 à 15 en décimal
        b = random.randint(1, 15)
        correct_answer = a + b

        # Convertir en binaire
        a_binary = bin(a)[2:]  # Enlever le '0b'
        b_binary = bin(b)[2:]
        correct_binary = bin(correct_answer)[2:]

        # Simuler la réussite (80% de chance)
        if random.random() < 0.8:
            message = f"""🔐 HACK BINAIRE RÉUSSI !

🎯 PROBLÈME : {a_binary} + {b_binary} = ?
✅ RÉPONSE : {correct_binary} (décimal: {correct_answer})

🎉 VICTOIRE ! Vous avez cracké le code !
🏆 +100 points pour cette réussite !
💡 Mini-jeu ajouté à votre collection !"""

            return {
                "réussite": True,
                "ascii_art": "🔐",
                "message": message,
                "score_gagne": 100,
                "profile_updated": True,
            }
        else:
            message = f"""🔐 HACK BINAIRE ÉCHOUÉ !

🎯 PROBLÈME : {a_binary} + {b_binary} = ?
❌ RÉPONSE : {bin(random.randint(1, 30))[2:]} (incorrecte)
✅ BONNE RÉPONSE : {correct_binary} (décimal: {correct_answer})

😔 ÉCHEC ! Mais ne vous découragez pas !
💡 Réessayez ! La pratique rend parfait !
Utilisez 'simple_hack' pour réessayer."""

            return {
                "réussite": False,
                "ascii_art": "🔐",
                "message": message,
                "score_gagne": 0,
                "profile_updated": False,
            }

    def handle_sequence_game(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Jeu de mémoire de séquences"""
        profile["score"] += 30

        return {
            "réussite": True,
            "ascii_art": "🧠",
            "message": """🧠 JEU DE MÉMOIRE DE SÉQUENCES

🎯 OBJECTIF : Mémoriser et reproduire la séquence
📊 DIFFICULTÉ : Moyen
⏱️ TEMPS : 45 secondes

🎮 SÉQUENCE À MÉMORISER :
🔴 → 🟡 → 🔵 → 🟢 → 🔴

💡 Clique sur les couleurs dans l'ordre !
🎯 Score basé sur la vitesse et la précision

🌟 +30 points pour avoir testé ta mémoire !""",
            "score_gagne": 30,
            "profile_updated": True,
        }

    def handle_typing_challenge(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Défi de frappe rapide"""
        profile["score"] += 20

        return {
            "réussite": True,
            "ascii_art": "⌨️",
            "message": """⌨️ DÉFI DE FRAPPE RAPIDE

🎯 OBJECTIF : Taper le plus vite possible
📊 DIFFICULTÉ : Variable
⏱️ TEMPS : 60 secondes

📝 TEXTE À TAPER :
"Arkalia Quest est un jeu d'aventure cyberpunk où tu incarnes un hacker qui découvre LUNA, une IA émotionnelle."

💡 Tape exactement le texte affiché !
🎯 Score basé sur les mots par minute (WPM)

🌟 +20 points pour avoir testé ta vitesse !""",
            "score_gagne": 20,
            "profile_updated": True,
        }

    def handle_play_game(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Lancer un mini-jeu"""
        profile["score"] += 15

        return {
            "réussite": True,
            "ascii_art": "🎮",
            "message": """🎮 LANCEMENT DE MINI-JEU

🎯 JEUX DISPONIBLES :
• simple_hack → Jeu de hack binaire
• sequence_game → Jeu de mémoire
• typing_challenge → Défi de frappe

💡 UTILISATION :
Tape le nom du jeu directement :
• simple_hack
• sequence_game
• typing_challenge

🌟 +15 points pour avoir exploré les jeux !""",
            "score_gagne": 15,
            "profile_updated": True,
        }

    def handle_level_up(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Simulation de montée de niveau"""
        current_level = profile.get("level", 1)
        new_level = current_level + 1
        profile["level"] = new_level
        profile["score"] += 100

        if "Level Up Master" not in profile.get("badges", []):
            profile["badges"].append("Level Up Master")

        return {
            "réussite": True,
            "ascii_art": "🌟",
            "message": f"""🌟 SIMULATION DE MONTÉE DE NIVEAU

🎉 FÉLICITATIONS !
⭐ Niveau {current_level} → Niveau {new_level}

🎯 RÉCOMPENSES :
• +100 points de score
• Nouveau badge : "Level Up Master"
• Capacités débloquées

💪 PROGRESSION :
Tu deviens plus fort à chaque niveau !
Continue à explorer pour monter encore plus haut !

🌟 +100 points pour cette montée de niveau !""",
            "score_gagne": 100,
            "badge": "Level Up Master",
            "niveau_gagne": new_level,
            "profile_updated": True,
        }

    def handle_badge_unlock(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Simulation de déblocage de badge"""
        profile["score"] += 50

        badge_name = "Badge Hunter"
        if badge_name not in profile.get("badges", []):
            profile["badges"].append(badge_name)

        return {
            "réussite": True,
            "ascii_art": "🏆",
            "message": f"""🏆 SIMULATION DE DÉBLOCAGE DE BADGE

🎉 NOUVEAU BADGE DÉBLOQUÉ !
🏆 "{badge_name}"

✨ DESCRIPTION :
Tu as découvert comment débloquer des badges !

🎯 RÉCOMPENSES :
• +50 points de score
• Badge ajouté à ta collection
• Progression dans les accomplissements

💡 ASTUCE :
Continue à explorer et accomplir des actions
pour débloquer plus de badges secrets !

🌟 +50 points pour ce badge !""",
            "score_gagne": 50,
            "badge": badge_name,
            "instant_rewards": {"badge": badge_name, "xp": 50},
            "profile_updated": True,
        }

    def handle_matrix_mode(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Active le thème Matrix"""
        profile["score"] += 10

        return {
            "réussite": True,
            "ascii_art": "🔮",
            "message": """🔮 MODE MATRIX ACTIVÉ

🌌 THÈME MATRIX APPLIQUÉ
💚 Code vert partout
⚡ Effets visuels Matrix
🎵 Ambiance cyberpunk

💡 UTILISATION :
Le thème Matrix est maintenant actif !
• Couleurs : Vert sur noir
• Police : Monospace
• Effets : Particules vertes

🌟 +10 points pour avoir activé Matrix !""",
            "score_gagne": 10,
            "profile_updated": True,
        }

    def handle_cyberpunk_mode(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Active le thème Cyberpunk"""
        profile["score"] += 10

        return {
            "réussite": True,
            "ascii_art": "🌃",
            "message": """🌃 MODE CYBERPUNK ACTIVÉ

🌆 THÈME CYBERPUNK APPLIQUÉ
💜 Néo-Tokyo vibes
⚡ Effets néon
🎵 Ambiance futuriste

💡 UTILISATION :
Le thème Cyberpunk est maintenant actif !
• Couleurs : Rose/Cyan sur noir
• Police : Futuriste
• Effets : Néons clignotants

🌟 +10 points pour avoir activé Cyberpunk !""",
            "score_gagne": 10,
            "profile_updated": True,
        }

    def handle_check_objects(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Vérifier les objets disponibles"""
        profile["score"] += 5

        return {
            "réussite": True,
            "ascii_art": "🔍",
            "message": """🔍 VÉRIFICATION DES OBJETS

📦 OBJETS DISPONIBLES :
• Terminal Arkalia ✅
• Interface LUNA ✅
• Système de badges ✅
• Mini-jeux éducatifs ✅
• Thèmes personnalisés ✅
• Système de progression ✅

🎯 STATUT :
Tous les systèmes sont opérationnels !

💡 ASTUCE :
Utilise 'aide' pour voir toutes les commandes disponibles.

🌟 +5 points pour cette vérification !""",
            "score_gagne": 5,
            "profile_updated": True,
        }

    def handle_debug_mode(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Informations système de debug"""
        profile["score"] += 5

        return {
            "réussite": True,
            "ascii_art": "🐛",
            "message": """🐛 MODE DEBUG ACTIVÉ

🔍 INFORMATIONS SYSTÈME :
• Version : Arkalia Quest v3.3.0
• LUNA : v2.1.0
• Terminal : v3.0.0
• Mini-jeux : v1.5.0

📊 STATISTIQUES :
• Score actuel : {score}
• Niveau : {level}
• Badges : {badges_count}

💡 MODE DÉVELOPPEUR :
Toutes les fonctionnalités sont disponibles !

🌟 +5 points pour cette analyse !""".format(
                score=profile.get("score", 0),
                level=profile.get("level", 1),
                badges_count=len(profile.get("badges", [])),
            ),
            "score_gagne": 5,
            "profile_updated": True,
        }
