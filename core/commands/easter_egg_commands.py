"""
Easter eggs Arkalia Quest
Commandes secrètes et easter eggs
"""

from typing import Dict, Any


class EasterEggCommands:
    """Gestionnaire des easter eggs"""

    def __init__(self):
        self.commands = {
            "easter_egg_1337": self.handle_easter_egg_1337,
            "boss_final": self.handle_boss_final,
            "meme_war": self.handle_meme_war,
            "nuke_world": self.handle_nuke_world,
            "assistant_pirate": self.handle_assistant_pirate,
            "generer_meme": self.handle_generer_meme,
            "decoder_message": self.handle_decoder_message,
            "invoquer_dragon": self.handle_invoquer_dragon,
        }

    def handle_easter_egg_1337(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère l'easter egg 1337"""
        profile["score"] += 1337
        if "Easter Egg 1337" not in profile["badges"]:
            profile["badges"].append("Easter Egg 1337")

        return {
            "réussite": True,
            "ascii_art": "🎯",
            "message": """🎯 EASTER EGG 1337 TROUVÉ !

LEET HACKER DÉTECTÉ ! Tu as trouvé le secret 1337 !

💡 Astuce : Les vrais hackers trouvent les secrets !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 1337,
            "badge": "Easter Egg 1337",
            "profile_updated": True,
        }

    def handle_boss_final(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère le boss final"""
        profile["score"] += 500
        if "Boss Slayer" not in profile["badges"]:
            profile["badges"].append("Boss Slayer")

        return {
            "réussite": True,
            "ascii_art": "👹",
            "message": """👹 BOSS FINAL ÉPIQUE !

Affronte le boss final d'Arkalia Quest !

💡 Astuce : Le boss final est le plus difficile !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 500,
            "badge": "Boss Slayer",
            "profile_updated": True,
        }

    def handle_meme_war(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la guerre des memes"""
        profile["score"] += 50
        if "Guerre des Memes" not in profile["badges"]:
            profile["badges"].append("Guerre des Memes")

        return {
            "réussite": True,
            "ascii_art": "😂",
            "message": """😂 GUERRE DES MEMES !

La guerre des memes fait rage dans Arkalia Quest !

💡 Astuce : Les memes sont une arme puissante !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 50,
            "badge": "Guerre des Memes",
            "profile_updated": True,
        }

    def handle_nuke_world(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la destruction du monde"""
        profile["score"] += 100
        if "Détruit" not in profile["badges"]:
            profile["badges"].append("Détruit")

        return {
            "réussite": True,
            "ascii_art": "💥",
            "message": """💥 MONDE NUKE !

Tu as détruit le monde ! (Mais pas vraiment)

💡 Astuce : La destruction peut être créative !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 100,
            "badge": "Détruit",
            "profile_updated": True,
        }

    def handle_assistant_pirate(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère l'assistant pirate"""
        profile["score"] += 75
        if "Pirate visuel" not in profile["badges"]:
            profile["badges"].append("Pirate visuel")

        return {
            "réussite": True,
            "ascii_art": "🏴‍☠️",
            "message": """🏴‍☠️ ASSISTANT PIRATE ACTIVÉ !

🎯 SYSTÈME PIRATE OPÉRATIONNEL :
• Interface pirate personnalisée
• Outils de hacking avancés
• Bypass de sécurité automatique
• Mode furtif activé

🔧 CAPACITÉS DÉBLOQUÉES :
• Infiltration silencieuse
• Détection d'alarmes
• Contournement de pare-feu
• Extraction de données
• Effacement de traces

💡 Astuce : Les pirates ont leur propre code d'honneur ! Utilise tes pouvoirs avec sagesse !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 75,
            "badge": "Pirate visuel",
            "profile_updated": True,
        }

    def handle_generer_meme(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la génération de memes"""
        return {
            "réussite": True,
            "ascii_art": "🎨",
            "message": """🎨 GÉNÉRATEUR DE MEMES ARKALIA QUEST

🎯 SYSTÈME DE CRÉATION :
• Générateur IA de memes
• Templates personnalisables
• Styles multiples disponibles
• Export haute qualité

🎭 CATÉGORIES DE MEMES :
• Hacker Life - La vie de hacker
• LUNA Memes - Humour IA
• Corp Fails - Échecs de La Corp
• Mission Accomplished - Succès
• Easter Eggs - Secrets cachés

💡 Astuce : Les memes personnalisés sont les meilleurs ! Crée tes propres memes pour immortaliser tes exploits !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "profile_updated": False,
        }

    def handle_decoder_message(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère le décodage de messages"""
        profile["score"] += 40
        if "Espion confirmé" not in profile["badges"]:
            profile["badges"].append("Espion confirmé")

        return {
            "réussite": True,
            "ascii_art": "🔐",
            "message": """🔐 MESSAGE SECRET DÉCODÉ !

🎯 DÉCRYPTAGE RÉUSSI :
• Chiffrement AES-256 cassé
• Message intercepté décodé
• Informations sensibles récupérées
• Traçabilité effacée

📋 CONTENU DU MESSAGE :
• Coordonnées d'un serveur caché
• Plans d'une mission secrète
• Codes d'accès temporaires
• Instructions d'infiltration

💡 Astuce : Les messages secrets contiennent des indices précieux ! Utilise-les pour progresser dans tes missions !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 40,
            "badge": "Espion confirmé",
            "profile_updated": True,
        }

    def handle_invoquer_dragon(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Gère l'invocation de dragon"""
        profile["score"] += 80
        if "Maître du feu" not in profile["badges"]:
            profile["badges"].append("Maître du feu")

        return {
            "réussite": True,
            "ascii_art": "🐉",
            "message": """🐉 DRAGON CYBERNIQUE INVOCUÉ !

🎯 INVOCATION RÉUSSIE :
• Dragon de données matérialisé
• Pouvoirs de feu numérique activés
• Protection système renforcée
• Capacités destructrices débloquées

🔥 POUVOIRS DU DRAGON :
• Attaque par feu de données
• Protection contre les virus
• Destruction de pare-feu
• Incinération de malwares
• Régénération automatique

💡 Astuce : Les dragons cyberniques sont des alliés puissants ! Utilise leur feu pour purifier les systèmes corrompus !

🎮 Continue à explorer Arkalia Quest pour débloquer tous les secrets !""",
            "score_gagne": 80,
            "badge": "Maître du feu",
            "profile_updated": True,
        }
