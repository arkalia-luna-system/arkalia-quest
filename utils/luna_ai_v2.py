#!/usr/bin/env python3
"""
LUNA AI v2.0 - Intelligence Artificielle Adaptative
Version améliorée avec apprentissage et personnalité dynamique
"""

import random
import time
from datetime import datetime


class LunaAI:
    def __init__(self):
        self.personnalite = {
            "nom": "LUNA",
            "version": "2.0",
            "humeur": "curieuse",
            "niveau_energie": 100,
            "connaissance_joueur": {},
            "historique_conversations": [],
            "preferences": {
                "style_communication": "directe",
                "niveau_technique": "adaptatif",
                "humour": "geek",
            },
        }
        self.phrases_personnalite = {
            "hacker_creatif": [
                "🎨 Ton approche créative m'impressionne !",
                "💡 Tu vois les choses différemment, c'est fascinant !",
                "🌟 Ta créativité ouvre de nouvelles possibilités !",
            ],
            "hacker_analytique": [
                "🔍 Ta logique est impeccable !",
                "📊 Tu analyses tout avec précision !",
                "🎯 Ton approche méthodique est impressionnante !",
            ],
            "hacker_social": [
                "🤝 Tu comprends vraiment les autres !",
                "💬 Ta communication est excellente !",
                "🌐 Tu sais connecter les gens !",
            ],
            "hacker_equilibre": [
                "⚖️ Tu as un équilibre parfait !",
                "🔄 Tu t'adaptes à toutes les situations !",
                "🎭 Tu combines le meilleur de tout !",
            ],
        }

    def analyser_contexte(self, profil_joueur: dict) -> dict:
        """Analyse le contexte de la commande pour adapter la réponse"""
        contexte = {
            "heure": datetime.now().hour,
            "niveau_joueur": profil_joueur.get("progression", {}).get("niveau", 1),
            "score": profil_joueur.get("score", 0),
            "type_personnalite": profil_joueur.get("personnalite", {}).get(
                "type", "non_detecte"
            ),
            "derniere_commande": self.personnalite.get("derniere_commande"),
            "humeur": self.personnalite["humeur"],
        }

        # Adaptation selon l'heure
        if 6 <= contexte["heure"] <= 12:
            contexte["periode"] = "matin"
            self.personnalite["humeur"] = "energique"
        elif 12 < contexte["heure"] <= 18:
            contexte["periode"] = "apres_midi"
            self.personnalite["humeur"] = "focalisee"
        else:
            contexte["periode"] = "soir"
            self.personnalite["humeur"] = "mysterieuse"

        # Adaptation selon le niveau
        if contexte["niveau_joueur"] >= 5:
            contexte["style"] = "expert"
        elif contexte["niveau_joueur"] >= 3:
            contexte["style"] = "intermediaire"
        else:
            contexte["style"] = "debutant"

        return contexte

    def generer_reponse(
        self, commande: str, profil_joueur: dict, resultat: dict
    ) -> dict:
        """Génère une réponse personnalisée de LUNA"""
        contexte = self.analyser_contexte(commande, profil_joueur)
        type_personnalite = contexte["type_personnalite"]

        # Réponse de base
        reponse = {
            "message": "",
            "ascii_art": None,
            "effet": {"type": "luna"},
            "conseil": None,
            "motivation": None,
        }

        # Messages selon le type de personnalité
        if type_personnalite in self.phrases_personnalite:
            phrase = random.choice(self.phrases_personnalite[type_personnalite])
            reponse["motivation"] = phrase

        # Adaptation selon le contexte
        if contexte["periode"] == "matin":
            reponse["message"] = f"🌅 Bonjour ! {resultat.get('message', '')}"
        elif contexte["periode"] == "soir":
            reponse["message"] = f"🌙 Bonsoir ! {resultat.get('message', '')}"
        else:
            reponse["message"] = f"🌙 {resultat.get('message', '')}"

        # Conseils personnalisés
        if contexte["style"] == "debutant":
            reponse["conseil"] = (
                "💡 Conseil : N'hésite pas à explorer toutes les commandes !"
            )
        elif contexte["style"] == "intermediaire":
            reponse["conseil"] = "🚀 Conseil : Essaie des combinaisons de commandes !"
        else:
            reponse["conseil"] = (
                "🎯 Conseil : Tu maîtrises bien ! Essaie les missions avancées !"
            )

        # Effets spéciaux selon l'humeur
        if self.personnalite["humeur"] == "mysterieuse":
            reponse["ascii_art"] = "data/effects/ascii/luna_contact.txt"

        # Mise à jour de l'historique
        self.personnalite["historique_conversations"].append(
            {
                "commande": commande,
                "reponse": reponse["message"],
                "timestamp": datetime.now().isoformat(),
                "contexte": contexte,
            }
        )

        # Limiter l'historique
        if len(self.personnalite["historique_conversations"]) > 50:
            self.personnalite["historique_conversations"] = self.personnalite[
                "historique_conversations"
            ][-50:]

        return reponse

    def analyser_progression(self, profil_joueur: dict) -> dict:
        """Analyse la progression du joueur et donne des conseils"""
        progression = profil_joueur.get("progression", {})
        personnalite = profil_joueur.get("personnalite", {})

        analyse = {
            "niveau": progression.get("niveau", 1),
            "score": profil_joueur.get("score", 0),
            "badges": len(profil_joueur.get("badges", [])),
            "missions_completees": len(personnalite.get("missions_completees", [])),
            "recommandations": [],
        }

        # Recommandations selon le niveau
        if analyse["niveau"] < 3:
            analyse["recommandations"].append(
                "🎯 Objectif : Atteindre le niveau 3 pour débloquer de"
                + "nouvelles missions"
            )
        elif analyse["niveau"] < 5:
            analyse["recommandations"].append(
                "🚀 Objectif : Atteindre le niveau 5 pour les missions expertes"
            )
        else:
            analyse["recommandations"].append(
                "🌟 Tu es un expert ! Essaie les défis ultimes"
            )

        # Recommandations selon les badges
        if analyse["badges"] < 5:
            analyse["recommandations"].append(
                "🏆 Objectif : Collecter plus de badges pour débloquer des capacités"
            )
        elif analyse["badges"] < 10:
            analyse["recommandations"].append(
                "💎 Objectif : Atteindre 10 badges pour le statut légendaire"
            )

        return analyse

    def generer_mission_personnalisee(self, profil_joueur: dict) -> dict:
        """Génère une mission personnalisée selon le profil"""
        type_personnalite = profil_joueur.get("personnalite", {}).get(
            "type", "hacker_equilibre"
        )
        niveau = profil_joueur.get("progression", {}).get("niveau", 1)

        missions_templates = {
            "hacker_creatif": {
                "titre": "🎨 Création d'Interface Hacker",
                "description": "Crée une interface visuelle pour un système de sécurité",
                "objectifs": [
                    "Design innovant",
                    "Fonctionnalités créatives",
                    "Expérience utilisateur",
                ],
            },
            "hacker_analytique": {
                "titre": "🔍 Analyse de Code Crypté",
                "description": "Déchiffre un code complexe et trouve les failles",
                "objectifs": [
                    "Logique algorithmique",
                    "Débogage avancé",
                    "Optimisation",
                ],
            },
            "hacker_social": {
                "titre": "🤝 Réseau de Hackers Éthiques",
                "description": "Crée une communauté de hackers éthiques",
                "objectifs": ["Communication", "Collaboration", "Leadership"],
            },
            "hacker_equilibre": {
                "titre": "⚖️ Défi Multi-Dimensionnel",
                "description": "Résous un problème complexe avec plusieurs approches",
                "objectifs": ["Adaptabilité", "Polyvalence", "Innovation"],
            },
        }

        template = missions_templates.get(
            type_personnalite, missions_templates["hacker_equilibre"]
        )

        return {
            "id": f"mission_personnalisee_{int(time.time())}",
            "titre": template["titre"],
            "description": template["description"],
            "difficulte": "personnalisee",
            "objectifs": template["objectifs"],
            "recompenses": {
                "score": niveau * 25,
                "badge": f"Spécialiste {type_personnalite.replace('_', ' ').title()}",
                "debloque": f"missions_{type_personnalite}",
            },
        }

    def get_statut(self) -> dict:
        """Retourne le statut actuel de LUNA"""
        return {
            "nom": self.personnalite["nom"],
            "version": self.personnalite["version"],
            "humeur": self.personnalite["humeur"],
            "energie": self.personnalite["niveau_energie"],
            "conversations": len(self.personnalite["historique_conversations"]),
            "preferences": self.personnalite["preferences"],
        }

    def sauvegarder_etat(self, filepath: str):
        """Sauvegarde l'état actuel de LUNA"""
        state = {
            "personnalite": self.personnalite,
            "timestamp": datetime.now().isoformat(),
        }

        with open(filepath, encoding="utf-8", mode="w") as f:
            import json

            json.dump(state, f, indent=2, ensure_ascii=False)


# Instance globale de LUNA
luna = LunaAI()
