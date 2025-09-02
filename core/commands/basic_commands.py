"""
Commandes de base Arkalia Quest
Commandes essentielles : aide, profil, status, clear, etc.
"""

from typing import Any, Dict


class BasicCommands:
    """Gestionnaire des commandes de base"""

    def __init__(self):
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
        }

    def handle_aide(self, profile: Dict[str, Any]) -> Dict[str, Any]:
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

🎮 TES MINI-JEUX :
• games → Liste tous les jeux
• play_game logic_1 → Jeu de logique
• play_game code_1 → Jeu de programmation
• play_game cyber_1 → Jeu de cybersécurité

🌙 INTERACTIONS LUNA :
• luna_contact → Parle avec LUNA
• luna_engine → Active le moteur IA
• luna_analyze → Analyse avancée
• luna_dance → LUNA danse pour toi

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

    def handle_profil(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande profil"""
        badges = profile.get("badges", [])
        badges_text = (
            "\n".join(["• " + badge for badge in badges])
            if badges
            else "Aucun badge encore"
        )

        return {
            "réussite": True,
            "ascii_art": "👤",
            "message": f"""👤 TON PROFIL ARKALIA QUEST

📊 INFORMATIONS PRINCIPALES :
• Score : {profile.get("score", 0)} points
• Badges : {len(badges)}
• Univers débloqués : {len(profile.get("progression", {}).get("univers_debloques", []))}
• Portails ouverts : {len(profile.get("progression", {}).get("portails_ouverts", []))}

🏅 BADGES OBTENUS :
{badges_text}

💡 Continue tes exploits pour débloquer plus de badges et de secrets !""",
            "profile_updated": False,
        }

    def handle_status(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la commande status"""
        score = profile.get("score", 0)
        badges = profile.get("badges", [])
        univers = profile.get("progression", {}).get("univers_debloques", [])
        portails = profile.get("progression", {}).get("portails_ouverts", [])

        # Calcul du niveau
        niveau = min(10, score // 1000 + 1)
        progression = (score % 1000) / 10

        return {
            "réussite": True,
            "ascii_art": "🌟",
            "message": f"""🌟 STATUT DU SYSTÈME ARKALIA QUEST

🎯 INFORMATIONS PRINCIPALES :
• Score actuel : {score} points
• Niveau : {niveau}/10 (Progression : {progression:.1f}%)
• Badges obtenus : {len(badges)}/50
• Univers débloqués : {len(univers)}
• Portails ouverts : {len(portails)}

🏆 BADGES RÉCENTS :
{chr(10).join(['• ' + badge for badge in badges[-5:]]) if len(badges) > 5 else
chr(10).join(['• ' + badge for badge in badges])}

🌍 PROGRESSION :
• Univers disponibles : {', '.join(univers) if univers else 'Aucun univers débloqué'}
• Portails accessibles : {', '.join(portails[:5]) + '...' if len(portails) > 5 else ', '.join(portails)}

💡 PROCHAINES ÉTAPES :
• Complète des missions pour gagner des points
• Débloque de nouveaux univers
• Collectionne tous les badges
• Défie tes amis sur le leaderboard

🎮 Continue tes exploits, hacker !""",
            "profile_updated": False,
        }

    def handle_clear(self, profile: Dict[str, Any]) -> Dict[str, Any]:
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

    def handle_start_tutorial(self, profile: Dict[str, Any]) -> Dict[str, Any]:
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
