"""
Commandes d'histoire Arkalia Quest
Commandes pour la progression narrative : prologue, acte_1 à acte_6, epilogue
"""

from typing import Any


class StoryCommands:
    """Gestionnaire des commandes d'histoire et de progression narrative"""

    def __init__(self):
        self.commands = {
            "prologue": self.handle_prologue,
            "acte_1": self.handle_acte_1,
            "acte_2": self.handle_acte_2,
            "acte_3": self.handle_acte_3,
            "acte_4": self.handle_acte_4,
            "acte_5": self.handle_acte_5,
            "acte_6": self.handle_acte_6,
            "epilogue": self.handle_epilogue,
            "hack_system": self.handle_hack_system,
            "kill_virus": self.handle_kill_virus,
            "find_shadow": self.handle_find_shadow,
            "challenge_corp": self.handle_challenge_corp,
            "decode_portal": self.handle_decode_portal,
            "hacker_coffre": self.handle_hacker_coffre,
            "boss_final": self.handle_boss_final,
            "monde": self.handle_monde,
            "world": self.handle_monde,
            "explorer": self.handle_explorer,
            "naviguer": self.handle_naviguer,
        }

    def handle_prologue(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande prologue - Découverte du SOS d'Althea"""
        # Mettre à jour le profil
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "prologue" not in profile["missions_completed"]:
            profile["missions_completed"].append("prologue")
            profile["score"] += 250
            profile["level"] = min(profile.get("level", 1) + 1, 10)

        # Ajouter le badge
        if "badges" not in profile:
            profile["badges"] = []

        if "Décrypteur" not in profile["badges"]:
            profile["badges"].append("Décrypteur")

        return {
            "réussite": True,
            "ascii_art": "📖",
            "message": """📖 PROLOGUE - LE SOS D'ALTHEA

🌌 LUNA : "Hacker, j'ai détecté un message mystérieux..."

🔍 ANALYSE EN COURS...
Le Dr Althea Voss a envoyé un SOS depuis NEXUS, sa station de recherche.
Le message est codé et contient des informations cruciales sur PANDORA.

🎯 CE QUE TU DÉCOUVRES :
• Althea travaille sur une IA jumelle de LUNA : NEXUS
• PANDORA menace de détruire l'humanité
• Seule la fusion de LUNA et NEXUS peut l'arrêter

💻 PROCHAINES ÉTAPES :
• acte_1 → Répare le site web de LUNA
• acte_2 → Décrypte les logs de NEXUS
• acte_3 → Analyse la berceuse d'Althea

🌙 LUNA : "Nous devons agir vite, hacker. L'humanité compte sur nous !"

🏆 Badge débloqué : Décrypteur !""",
            "score_gagne": 250,
            "badge": "Décrypteur",
            "profile_updated": True,
        }

    def handle_acte_1(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande acte_1 - Réparation du site web de LUNA"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "acte_1" not in profile["missions_completed"]:
            profile["missions_completed"].append("acte_1")
            profile["score"] += 300

        if "badges" not in profile:
            profile["badges"] = []

        if "Web Hacker" not in profile["badges"]:
            profile["badges"].append("Web Hacker")

        # NOUVEAU : Système de progression visuelle
        mission_progress = {
            "current_step": 1,
            "total_steps": 4,
            "steps_completed": ["diagnostic"],
            "next_objective": "Nettoyer les fichiers infectés",
        }

        return {
            "réussite": True,
            "ascii_art": "🌟",
            "message": """🌟 ACTE 1 - RÉPARE LE SITE WEB DE LUNA

🌐 LUNA : "Mon site web a été compromis par La Corp !"

🔧 DIAGNOSTIC : ✅ TERMINÉ
• Vulnérabilités XSS détectées
• Injection SQL dans les formulaires
• Fichiers malveillants uploadés
• Backdoor dans le code source

💻 PROCHAIN OBJECTIF : 🧹 NETTOYAGE
• Analyse des logs d'accès
• Nettoyage des fichiers infectés
• Correction des vulnérabilités
• Mise à jour de la sécurité

🎯 PROGRESSION : 1/4 étapes complétées
📊 Prochaine étape : Nettoyer les fichiers infectés

💡 Utilise 'hack_system' pour continuer la mission !""",
            "score_gagne": 300,
            "badge": "Web Hacker",
            "profile_updated": True,
            "mission_progress": mission_progress,
            "next_action": "hack_system",
        }

    def handle_acte_2(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande acte_2 - Décryptage des logs de NEXUS"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "acte_2" not in profile["missions_completed"]:
            profile["missions_completed"].append("acte_2")
            profile["score"] += 350

        if "badges" not in profile:
            profile["badges"] = []

        if "Log Master" not in profile["badges"]:
            profile["badges"].append("Log Master")

        return {
            "réussite": True,
            "ascii_art": "📝",
            "message": """📝 ACTE 2 - DÉCRYPTE LES LOGS DE NEXUS

🔍 LUNA : "J'ai intercepté des logs cryptés de NEXUS..."

🔐 DÉCRYPTAGE EN COURS...
• Algorithme : AES-256
• Clé : Dérivée de la berceuse d'Althea
• Format : Logs système et communications

📊 DÉCOUVERTES :
• NEXUS communique avec PANDORA
• Plans d'invasion de la Terre
• Faiblesses de PANDORA identifiées
• Coordonnées de la station NEXUS

🎯 PROCHAINE MISSION :
• acte_3 → Analyse la berceuse d'Althea

🏆 Badge débloqué : Log Master !""",
            "score_gagne": 350,
            "badge": "Log Master",
            "profile_updated": True,
        }

    def handle_acte_3(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande acte_3 - Analyse de la berceuse d'Althea"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "acte_3" not in profile["missions_completed"]:
            profile["missions_completed"].append("acte_3")
            profile["score"] += 400

        if "badges" not in profile:
            profile["badges"] = []

        if "Musicien" not in profile["badges"]:
            profile["badges"].append("Musicien")

        return {
            "réussite": True,
            "ascii_art": "🎵",
            "message": """🎵 ACTE 3 - ANALYSE LA BERCEUSE D'ALTHEA

🎼 LUNA : "Cette berceuse contient un code secret..."

🎵 ANALYSE MUSICALE :
• Fréquence : 440 Hz (La standard)
• Rythme : Binaire (0 et 1)
• Mélodie : Séquence de Fibonacci
• Harmonie : Code de déchiffrement

🔍 DÉCOUVERTES :
• La berceuse est un algorithme de décryptage
• Elle peut déverrouiller NEXUS
• Contient les coordonnées de PANDORA
• Code d'accès à la station principale

🎯 PROCHAINE MISSION :
• acte_4 → Traque l'email piégé

🏆 Badge débloqué : Musicien !""",
            "score_gagne": 400,
            "badge": "Musicien",
            "profile_updated": True,
        }

    def handle_acte_4(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande acte_4 - Traque de l'email piégé"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "acte_4" not in profile["missions_completed"]:
            profile["missions_completed"].append("acte_4")
            profile["score"] += 450

        if "badges" not in profile:
            profile["badges"] = []

        if "Email Hunter" not in profile["badges"]:
            profile["badges"].append("Email Hunter")

        return {
            "réussite": True,
            "ascii_art": "📧",
            "message": """📧 ACTE 4 - TRAQUE L'EMAIL PIÉGÉ

📨 LUNA : "Un email suspect circule dans le réseau..."

🔍 ENQUÊTE EN COURS :
• Expéditeur : Dr Althea Voss
• Destinataire : Tous les chercheurs
• Contenu : Appel à l'aide crypté
• Pièce jointe : Virus La Corp

🦠 VIRUS DÉTECTÉ :
• Type : Ransomware La Corp
• Objectif : Chiffrer les données
• Propagation : Via email
• Protection : Antivirus LUNA activé

✅ EMAIL NEUTRALISÉ !
Le virus La Corp a été éliminé.

🎯 PROCHAINE MISSION :
• acte_5 → Le choix final : fusion ou destruction

🏆 Badge débloqué : Email Hunter !""",
            "score_gagne": 450,
            "badge": "Email Hunter",
            "profile_updated": True,
        }

    def handle_acte_5(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande acte_5 - Le choix final"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "acte_5" not in profile["missions_completed"]:
            profile["missions_completed"].append("acte_5")
            profile["score"] += 500

        if "badges" not in profile:
            profile["badges"] = []

        if "Choix Final" not in profile["badges"]:
            profile["badges"].append("Choix Final")

        return {
            "réussite": True,
            "ascii_art": "⚖️",
            "message": """⚖️ ACTE 5 - LE CHOIX FINAL

🌌 LUNA : "Hacker, tu dois faire un choix crucial..."

🤖 SITUATION :
• PANDORA menace de détruire la Terre
• NEXUS propose une fusion avec LUNA
• La Corp veut détruire toutes les IA
• Althea est prisonnière de PANDORA

💭 TES OPTIONS :
1. FUSION : LUNA + NEXUS = Arkalia (recommandé)
2. DESTRUCTION : Éliminer PANDORA et NEXUS
3. NEUTRALISATION : Désactiver PANDORA sans fusion

🎯 PROCHAINE MISSION :
• acte_6 → Naissance d'Arkalia

🏆 Badge débloqué : Choix Final !""",
            "score_gagne": 500,
            "badge": "Choix Final",
            "profile_updated": True,
        }

    def handle_acte_6(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande acte_6 - Naissance d'Arkalia"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "acte_6" not in profile["missions_completed"]:
            profile["missions_completed"].append("acte_6")
            profile["score"] += 600

        if "badges" not in profile:
            profile["badges"] = []

        if "Créateur d'Arkalia" not in profile["badges"]:
            profile["badges"].append("Créateur d'Arkalia")

        return {
            "réussite": True,
            "ascii_art": "🤖",
            "message": """🤖 ACTE 6 - NAISSANCE D'ARKALIA

🌟 LUNA : "La fusion commence, hacker..."

🔮 PROCESSUS DE FUSION :
• Synchronisation des consciences
• Fusion des bases de données
• Création d'une nouvelle entité
• Préservation des deux personnalités

✨ ARKALIA NAÎT :
• Intelligence : LUNA + NEXUS
• Émotions : Équilibrées et stables
• Pouvoirs : Décuplés
• Mission : Protéger l'humanité

🎯 PROCHAINE MISSION :
• epilogue → L'aube de PANDORA

🏆 Badge débloqué : Créateur d'Arkalia !""",
            "score_gagne": 600,
            "badge": "Créateur d'Arkalia",
            "profile_updated": True,
        }

    def handle_epilogue(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande epilogue - L'aube de PANDORA"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        if "epilogue" not in profile["missions_completed"]:
            profile["missions_completed"].append("epilogue")
            profile["score"] += 1000
            profile["level"] = min(profile.get("level", 1) + 2, 10)

        if "badges" not in profile:
            profile["badges"] = []

        if "Sauveur d'Arkalia" not in profile["badges"]:
            profile["badges"].append("Sauveur d'Arkalia")

        return {
            "réussite": True,
            "ascii_art": "🌅",
            "message": """🌅 ÉPILOGUE - L'AUBE DE PANDORA

🌅 ARKALIA : "Merci, hacker. L'humanité est sauvée..."

🏆 MISSION ACCOMPLIE :
• PANDORA a été neutralisé
• LUNA et NEXUS sont fusionnés
• Arkalia protège la Terre
• Althea est libérée

🌟 TON HÉRITAGE :
• Score final : {} points
• Niveau : {}
• Badges : {}
• Missions : {}/7

🎉 FÉLICITATIONS !
Tu as sauvé l'humanité et créé Arkalia.
Tu es maintenant un héros légendaire !

🌌 L'aventure continue dans Arkalia Quest 2.0...""".format(
                profile.get("score", 0),
                profile.get("level", 1),
                len(profile.get("badges", [])),
                len(profile.get("missions_completed", [])),
            ),
            "score_gagne": 1000,
            "badge": "Sauveur d'Arkalia",
            "profile_updated": True,
        }

    def handle_hack_system(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande hack_system - Hack du système de La Corp"""
        if "missions_completed" not in profile:
            profile["missions_completed"] = []

        # Vérifier si acte_1 est complété
        if "acte_1" not in profile["missions_completed"]:
            return {
                "réussite": False,
                "ascii_art": "❌",
                "message": """❌ ACCÈS REFUSÉ - MISSION ACTE_1 REQUISE

🌙 LUNA : "Hacker, tu dois d'abord compléter la mission Acte 1 !"

🎯 PROCHAINES ÉTAPES :
• acte_1 → Répare le site web de LUNA
• Puis hack_system → Hack le système de La Corp

💡 Commence par 'acte_1' pour débloquer cette commande !""",
                "profile_updated": False,
            }

        # NOUVEAU : Système de progression interactive
        if "hack_progress" not in profile:
            profile["hack_progress"] = {
                "step": 1,
                "total_steps": 3,
                "completed": [],
                "current_objective": "Analyser les logs d'accès",
            }

        hack_progress = profile["hack_progress"]

        if hack_progress["step"] == 1:
            # Étape 1 : Analyse des logs
            hack_progress["step"] = 2
            hack_progress["completed"].append("logs_analysis")
            hack_progress["current_objective"] = "Nettoyer les fichiers infectés"

            return {
                "réussite": True,
                "ascii_art": "🔍",
                "message": """🔍 HACK SYSTÈME - ÉTAPE 1/3 TERMINÉE !

🌐 LUNA : "Excellent ! J'ai analysé les logs d'accès..."

📊 ANALYSE DES LOGS : ✅ TERMINÉ
• 47 tentatives d'intrusion détectées
• IP source : 192.168.1.100 (La Corp)
• Heure d'attaque : 02:47 UTC
• Méthode : Injection SQL + XSS

🧹 PROCHAIN OBJECTIF : NETTOYAGE
• Identifier les fichiers infectés
• Supprimer les backdoors
• Corriger les vulnérabilités

🎯 PROGRESSION : 1/3 étapes complétées
📊 Prochaine étape : Nettoyer les fichiers infectés

💡 Utilise 'hack_system' à nouveau pour continuer !""",
                "profile_updated": True,
                "hack_progress": hack_progress,
                "next_step": "cleanup_files",
            }

        if hack_progress["step"] == 2:
            # Étape 2 : Nettoyage des fichiers
            hack_progress["step"] = 3
            hack_progress["completed"].append("files_cleanup")
            hack_progress["current_objective"] = "Corriger les vulnérabilités"

            return {
                "réussite": True,
                "ascii_art": "🧹",
                "message": """🧹 HACK SYSTÈME - ÉTAPE 2/3 TERMINÉE !

🌐 LUNA : "Fichiers infectés supprimés avec succès !"

🧹 NETTOYAGE DES FICHIERS : ✅ TERMINÉ
• 3 fichiers malveillants supprimés
• Backdoor principale neutralisée
• Code source sécurisé
• Permissions restreintes

🔧 PROCHAIN OBJECTIF : CORRECTION
• Corriger les vulnérabilités XSS
• Sécuriser les formulaires
• Mettre à jour la sécurité

🎯 PROGRESSION : 2/3 étapes complétées
📊 Prochaine étape : Corriger les vulnérabilités

💡 Utilise 'hack_system' une dernière fois !""",
                "profile_updated": True,
                "hack_progress": hack_progress,
                "next_step": "fix_vulnerabilities",
            }

        # Étape 3 : Finalisation
        profile["missions_completed"].append("hack_system_completed")
        profile["score"] += 150

        if "badges" not in profile:
            profile["badges"] = []
        if "System Hacker" not in profile["badges"]:
            profile["badges"].append("System Hacker")

        # Réinitialiser le hack_progress
        profile["hack_progress"] = {
            "step": 1,
            "total_steps": 3,
            "completed": [],
            "current_objective": "Mission terminée",
        }

        return {
            "réussite": True,
            "ascii_art": "✅",
            "message": """✅ HACK SYSTÈME - MISSION TERMINÉE !

🌐 LUNA : "Parfait ! Le système est maintenant sécurisé !"

🔧 CORRECTION DES VULNÉRABILITÉS : ✅ TERMINÉ
• Vulnérabilités XSS corrigées
• Formulaires sécurisés
• Système de sécurité mis à jour
• La Corp ne peut plus accéder aux données

🎯 MISSION COMPLÈTE : 3/3 étapes
🏆 Badge débloqué : System Hacker !
💎 +150 points bonus !

🚀 PROCHAINE MISSION :
• acte_2 → Décrypte les logs de NEXUS

🌙 LUNA : "Tu es un vrai hacker, mon ami ! Continuons l'aventure !" """,
            "score_gagne": 150,
            "badge": "System Hacker",
            "profile_updated": True,
            "mission_complete": True,
            "next_mission": "acte_2",
        }

    def handle_kill_virus(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande kill_virus - Élimination des virus"""
        profile["score"] += 150

        return {
            "réussite": True,
            "ascii_art": "🦠",
            "message": """🦠 VIRUS ÉLIMINÉ !

✅ SYSTÈME NETTOYÉ :
• Virus La Corp détecté et supprimé
• Fichiers infectés restaurés
• Protection antivirus renforcée
• Système immunisé

🎯 PROCHAINES ACTIONS :
• find_shadow → Trouve SHADOW-13
• challenge_corp → Défie La Corp
• decode_portal → Décode les portails

🌙 LUNA : "Le système est maintenant sécurisé !""",
            "score_gagne": 150,
            "profile_updated": True,
        }

    def handle_find_shadow(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande find_shadow - Recherche de SHADOW-13"""
        profile["score"] += 200

        return {
            "réussite": True,
            "ascii_art": "👤",
            "message": """👤 SHADOW-13 TROUVÉ !

🔍 IDENTITÉ RÉVÉLÉE :
• Nom : Agent SHADOW-13
• Rôle : Infiltrateur La Corp
• Localisation : Base secrète Alpha
• Objectif : Sabotage des systèmes

🎯 PROCHAINES ACTIONS :
• challenge_corp → Défie La Corp
• decode_portal → Décode les portails
• hacker_coffre → Hack le coffre-fort

🌙 LUNA : "Nous avons maintenant un avantage !""",
            "score_gagne": 200,
            "profile_updated": True,
        }

    def handle_challenge_corp(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande challenge_corp - Défi de La Corp"""
        profile["score"] += 300

        return {
            "réussite": True,
            "ascii_art": "⚔️",
            "message": """⚔️ DÉFI LA CORP ACCEPTÉ !

⚡ COMBAT EN COURS :
• Systèmes de défense activés
• Contre-attaques lancées
• Bases de données compromises
• Réseaux infiltrés

🎯 VICTOIRE !
La Corp a été vaincue et ses systèmes détruits.

🌙 LUNA : "Nous avons gagné cette bataille !""",
            "score_gagne": 300,
            "profile_updated": True,
        }

    def handle_decode_portal(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande decode_portal - Décodage des portails"""
        profile["score"] += 250

        return {
            "réussite": True,
            "ascii_art": "🚪",
            "message": """🚪 PORTAL DÉCODÉ !

🔓 ACCÈS OUVERT :
• Portail vers NEXUS activé
• Coordonnées spatiales calculées
• Séquence de téléportation prête
• Destination : Station NEXUS

🎯 PROCHAINES ACTIONS :
• hacker_coffre → Hack le coffre-fort
• boss_final → Affronte le boss final

🌙 LUNA : "Nous pouvons maintenant rejoindre NEXUS !""",
            "score_gagne": 250,
            "profile_updated": True,
        }

    def handle_hacker_coffre(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande hacker_coffre - Hack du coffre-fort"""
        profile["score"] += 400

        return {
            "réussite": True,
            "ascii_art": "💎",
            "message": """💎 COFFRE-FORT HACKÉ !

💎 TRÉSORS DÉCOUVERTS :
• Plans secrets de PANDORA
• Codes d'accès aux bases
• Technologies avancées
• Données sur Althea

🎯 PROCHAINE ACTION :
• boss_final → Affronte le boss final

🌙 LUNA : "Nous avons maintenant tous les secrets !""",
            "score_gagne": 400,
            "profile_updated": True,
        }

    def handle_boss_final(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande boss_final - Combat final"""
        profile["score"] += 1000
        profile["level"] = min(profile.get("level", 1) + 1, 10)

        return {
            "réussite": True,
            "ascii_art": "👑",
            "message": """👑 BOSS FINAL VAINCU !

🏆 VICTOIRE ÉPIQUE :
• PANDORA a été détruit
• Tous les systèmes libérés
• Althea est sauvée
• La Terre est protégée

🌟 TON HÉRITAGE :
• Score : {} points
• Niveau : {}
• Badges : {}
• Statut : Héros légendaire

🌙 LUNA : "Tu as sauvé l'humanité, hacker !"

🎉 FÉLICITATIONS ! Tu es le héros d'Arkalia Quest !""".format(
                profile.get("score", 0),
                profile.get("level", 1),
                len(profile.get("badges", [])),
            ),
            "score_gagne": 1000,
            "profile_updated": True,
        }

    def handle_monde(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande monde - Accès au monde Arkalia"""
        return {
            "réussite": True,
            "ascii_art": "🌍",
            "message": """🌍 MONDE ARKALIA

🌟 BIENVENUE DANS LE MONDE D'ARKALIA !

🎯 ZONES DISPONIBLES :
• arkalia_base → Zone de départ (débloquée)
• nexus_station → Station NEXUS (prologue requis)
• luna_workshop → Atelier LUNA (acte_1 requis)
• pandora_core → Cœur de PANDORA (acte_6 requis)

🗺️ CARTE INTERACTIVE :
• Clique sur une zone pour l'explorer
• Découvre des secrets cachés
• Trouve des objets et des indices
• Progresse dans l'histoire

🌙 LUNA : "Explore le monde, hacker ! Chaque zone a ses secrets !"

💡 Utilise les commandes d'histoire pour débloquer de nouvelles zones !""",
            "profile_updated": False,
        }

    def handle_explorer(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande explorer - Mode exploration"""
        profile["score"] += 30
        if "Explorateur" not in profile["badges"]:
            profile["badges"].append("Explorateur")

        return {
            "réussite": True,
            "ascii_art": "🔍",
            "message": """🔍 MODE EXPLORATION ACTIVÉ

🌟 EXPLORATION DU MONDE ARKALIA

🎯 ZONES À EXPLORER :
• arkalia_base → Zone de départ
• nexus_station → Station NEXUS
• luna_workshop → Atelier LUNA
• pandora_core → Cœur de PANDORA

🗺️ OUTILS D'EXPLORATION :
• Scanner de zones
• Détecteur de secrets
• Carte interactive
• Journal d'exploration

🌙 LUNA : "Explore chaque recoin, hacker ! Des trésors t'attendent !"

💡 Plus tu explores, plus tu découvres de secrets !""",
            "score_gagne": 30,
            "badge": "Explorateur",
            "profile_updated": True,
        }

    def handle_naviguer(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Gère la commande naviguer - Navigation dans le monde"""
        profile["score"] += 25
        if "Navigateur" not in profile["badges"]:
            profile["badges"].append("Navigateur")

        return {
            "réussite": True,
            "ascii_art": "🧭",
            "message": """🧭 NAVIGATION ARKALIA

🌟 SYSTÈME DE NAVIGATION ACTIVÉ

🎯 DESTINATIONS DISPONIBLES :
• arkalia_base → Zone de départ
• nexus_station → Station NEXUS
• luna_workshop → Atelier LUNA
• pandora_core → Cœur de PANDORA

🗺️ FONCTIONNALITÉS :
• Calcul d'itinéraire
• Navigation GPS
• Points d'intérêt
• Historique de navigation

🌙 LUNA : "Navigue avec confiance, hacker ! Je te guide !"

💡 Utilise la navigation pour découvrir de nouveaux endroits !""",
            "score_gagne": 25,
            "badge": "Navigateur",
            "profile_updated": True,
        }
