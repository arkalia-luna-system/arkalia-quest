#!/usr/bin/env python3
"""
📚 TECHNICAL TUTORIALS - ARKALIA QUEST
======================================

Système de tutoriels techniques pour la cybersécurité
avec concepts éducatifs et références d'apprentissage.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
import random
from datetime import datetime, timedelta
from typing import Any, Optional

logger = logging.getLogger(__name__)


class TechnicalTutorials:
    """Gestionnaire des tutoriels techniques de cybersécurité"""

    def __init__(self):
        self.tutorials = {}
        self.concepts = {}
        self.references = {}
        self.player_progress = {}
        self.quizzes = {}

        # Charger les données
        self.load_tutorial_data()

    def load_tutorial_data(self) -> None:
        """Charge les données de tutoriels"""
        try:
            with open("data/technical_tutorials.json", encoding="utf-8") as f:
                data = json.load(f)
                self.tutorials = data.get("tutorials", {})
                self.concepts = data.get("concepts", {})
                self.references = data.get("references", {})
                self.player_progress = data.get("player_progress", {})
                self.quizzes = data.get("quizzes", {})
        except FileNotFoundError:
            logger.info("Fichier de tutoriels non trouvé, création des données par défaut")
            self._create_default_tutorials()
        except Exception as e:
            logger.error(f"Erreur chargement tutoriels: {e}")
            self._create_default_tutorials()

    def _create_default_tutorials(self) -> None:
        """Crée les tutoriels techniques par défaut"""
        self.concepts = {
            "cryptography": {
                "name": "Cryptographie",
                "description": "Art et science de la protection de l'information",
                "difficulty": "intermediate",
                "category": "security",
                "icon": "🔐",
                "color": "#00ff00",
            },
            "network_security": {
                "name": "Sécurité Réseau",
                "description": "Protection des infrastructures réseau",
                "difficulty": "advanced",
                "category": "security",
                "icon": "🌐",
                "color": "#00ffff",
            },
            "ethical_hacking": {
                "name": "Hacking Éthique",
                "description": "Techniques de test de pénétration légales",
                "difficulty": "expert",
                "category": "hacking",
                "icon": "🥷",
                "color": "#ff4444",
            },
            "malware_analysis": {
                "name": "Analyse de Malware",
                "description": "Identification et analyse des logiciels malveillants",
                "difficulty": "expert",
                "category": "security",
                "icon": "🦠",
                "color": "#ffaa00",
            },
            "incident_response": {
                "name": "Réponse aux Incidents",
                "description": "Gestion des incidents de sécurité",
                "difficulty": "advanced",
                "category": "security",
                "icon": "🚨",
                "color": "#ff00ff",
            },
        }

        self.tutorials = {
            "crypto_basics": {
                "id": "crypto_basics",
                "title": "Introduction à la Cryptographie",
                "description": "Apprends les bases de la cryptographie moderne",
                "concept": "cryptography",
                "difficulty": "beginner",
                "duration_minutes": 15,
                "prerequisites": [],
                "learning_objectives": [
                    "Comprendre les concepts de base de la cryptographie",
                    "Différencier entre chiffrement symétrique et asymétrique",
                    "Utiliser des outils de chiffrement simples",
                ],
                "content": [
                    {
                        "type": "text",
                        "title": "Qu'est-ce que la Cryptographie ?",
                        "content": "La cryptographie est l'art et la science de protéger l'information en la transformant en une forme illisible pour les non-autorisés. Elle est utilisée partout : dans les communications, les transactions bancaires, et la protection des données.",
                    },
                    {
                        "type": "interactive",
                        "title": "Chiffrement César",
                        "content": "Le chiffrement de César est l'une des méthodes de chiffrement les plus anciennes. Il consiste à décaler chaque lettre d'un nombre fixe dans l'alphabet.",
                        "exercise": {
                            "type": "caesar_cipher",
                            "instruction": "Chiffre le message 'HELLO' avec un décalage de 3",
                            "expected": "KHOOR",
                        },
                    },
                    {
                        "type": "visual",
                        "title": "Types de Chiffrement",
                        "content": "Il existe deux types principaux de chiffrement : symétrique (même clé pour chiffrer et déchiffrer) et asymétrique (clés différentes).",
                        "diagram": "encryption_types_diagram",
                    },
                ],
                "quiz": {
                    "questions": [
                        {
                            "id": "q1",
                            "question": "Qu'est-ce que le chiffrement de César ?",
                            "options": [
                                "Un algorithme de chiffrement moderne",
                                "Une méthode de chiffrement par décalage",
                                "Un type de chiffrement asymétrique",
                                "Un protocole de sécurité réseau",
                            ],
                            "correct": 1,
                            "explanation": "Le chiffrement de César utilise un décalage fixe dans l'alphabet pour chiffrer les messages.",
                        }
                    ]
                },
                "references": [
                    {
                        "title": "Introduction à la Cryptographie",
                        "url": "https://fr.wikipedia.org/wiki/Cryptographie",
                        "type": "wikipedia",
                    },
                    {
                        "title": "Cours de Cryptographie",
                        "url": "https://www.coursera.org/learn/cryptography",
                        "type": "course",
                    },
                ],
            },
            "network_security_basics": {
                "id": "network_security_basics",
                "title": "Sécurité des Réseaux",
                "description": "Protège les réseaux contre les menaces",
                "concept": "network_security",
                "difficulty": "intermediate",
                "duration_minutes": 25,
                "prerequisites": ["crypto_basics"],
                "learning_objectives": [
                    "Identifier les vulnérabilités réseau communes",
                    "Configurer un pare-feu basique",
                    "Comprendre les protocoles de sécurité",
                ],
                "content": [
                    {
                        "type": "text",
                        "title": "Vulnérabilités Réseau",
                        "content": "Les réseaux sont vulnérables à de nombreuses attaques : déni de service, interception de données, usurpation d'identité. Il est crucial de comprendre ces menaces pour les contrer.",
                    },
                    {
                        "type": "interactive",
                        "title": "Configuration de Pare-feu",
                        "content": "Un pare-feu filtre le trafic réseau entrant et sortant. Configure les règles pour bloquer les connexions suspectes.",
                        "exercise": {
                            "type": "firewall_config",
                            "instruction": "Bloque le port 23 (Telnet) et autorise le port 80 (HTTP)",
                            "rules": [
                                {"port": 23, "action": "deny", "protocol": "tcp"},
                                {"port": 80, "action": "allow", "protocol": "tcp"},
                            ],
                        },
                    },
                    {
                        "type": "simulation",
                        "title": "Attaque DDoS",
                        "content": "Simule une attaque par déni de service distribué et apprends à la détecter et la contrer.",
                        "scenario": "ddos_attack_simulation",
                    },
                ],
                "quiz": {
                    "questions": [
                        {
                            "id": "q1",
                            "question": "Qu'est-ce qu'une attaque DDoS ?",
                            "options": [
                                "Une attaque de déni de service distribué",
                                "Une attaque de chiffrement",
                                "Une attaque de pare-feu",
                                "Une attaque de malware",
                            ],
                            "correct": 0,
                            "explanation": "DDoS signifie Distributed Denial of Service - une attaque qui surcharge un serveur avec du trafic.",
                        }
                    ]
                },
                "references": [
                    {
                        "title": "Sécurité Réseau - OWASP",
                        "url": "https://owasp.org/www-project-top-ten/",
                        "type": "documentation",
                    }
                ],
            },
            "ethical_hacking_intro": {
                "id": "ethical_hacking_intro",
                "title": "Introduction au Hacking Éthique",
                "description": "Apprends les techniques de test de pénétration légales",
                "concept": "ethical_hacking",
                "difficulty": "advanced",
                "duration_minutes": 30,
                "prerequisites": ["network_security_basics"],
                "learning_objectives": [
                    "Comprendre l'éthique du hacking",
                    "Utiliser des outils de test de pénétration",
                    "Effectuer des tests de vulnérabilité",
                ],
                "content": [
                    {
                        "type": "text",
                        "title": "Éthique du Hacking",
                        "content": "Le hacking éthique consiste à utiliser les mêmes techniques que les pirates, mais de manière légale et éthique pour améliorer la sécurité. Toujours obtenir une autorisation écrite avant de tester un système.",
                    },
                    {
                        "type": "interactive",
                        "title": "Scan de Ports",
                        "content": "Utilise Nmap pour scanner les ports ouverts d'un système cible (simulation).",
                        "exercise": {
                            "type": "port_scan",
                            "target": "192.168.1.1",
                            "ports": "1-1000",
                            "instruction": "Identifie les ports ouverts et leurs services",
                        },
                    },
                    {
                        "type": "simulation",
                        "title": "Test de Pénétration",
                        "content": "Effectue un test de pénétration complet sur un système de test.",
                        "scenario": "penetration_test_simulation",
                    },
                ],
                "quiz": {
                    "questions": [
                        {
                            "id": "q1",
                            "question": "Qu'est-ce qu'un test de pénétration ?",
                            "options": [
                                "Une attaque malveillante",
                                "Un test de sécurité autorisé",
                                "Une installation de malware",
                                "Un scan de virus",
                            ],
                            "correct": 1,
                            "explanation": "Un test de pénétration est un test de sécurité autorisé pour identifier les vulnérabilités.",
                        }
                    ]
                },
                "references": [
                    {
                        "title": "Certified Ethical Hacker (CEH)",
                        "url": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/",
                        "type": "certification",
                    }
                ],
            },
        }

        self.references = {
            "books": [
                {
                    "title": "The Web Application Hacker's Handbook",
                    "author": "Dafydd Stuttard, Marcus Pinto",
                    "isbn": "978-1118026472",
                    "description": "Guide complet sur les vulnérabilités web",
                    "level": "intermediate",
                },
                {
                    "title": "Hacking: The Art of Exploitation",
                    "author": "Jon Erickson",
                    "isbn": "978-1593271442",
                    "description": "Introduction technique au hacking",
                    "level": "advanced",
                },
            ],
            "courses": [
                {
                    "title": "Cybersecurity Fundamentals",
                    "provider": "Coursera",
                    "url": "https://www.coursera.org/learn/cybersecurity-fundamentals",
                    "description": "Cours d'introduction à la cybersécurité",
                    "level": "beginner",
                },
                {
                    "title": "Ethical Hacking",
                    "provider": "edX",
                    "url": "https://www.edx.org/course/ethical-hacking",
                    "description": "Cours sur le hacking éthique",
                    "level": "intermediate",
                },
            ],
            "tools": [
                {
                    "name": "Nmap",
                    "description": "Scanner de ports et de vulnérabilités",
                    "url": "https://nmap.org/",
                    "type": "network_scanner",
                },
                {
                    "name": "Wireshark",
                    "description": "Analyseur de protocoles réseau",
                    "url": "https://www.wireshark.org/",
                    "type": "network_analyzer",
                },
            ],
            "standards": [
                {
                    "name": "ISO 27001",
                    "description": "Système de management de la sécurité de l'information",
                    "url": "https://www.iso.org/isoiec-27001-information-security.html",
                    "type": "standard",
                },
                {
                    "name": "NIST Cybersecurity Framework",
                    "description": "Cadre de cybersécurité du NIST",
                    "url": "https://www.nist.gov/cyberframework",
                    "type": "framework",
                },
            ],
        }

    def get_available_tutorials(self, player_id: str) -> list[dict[str, Any]]:
        """Retourne les tutoriels disponibles pour un joueur"""
        available = []

        for _tutorial_id, tutorial in self.tutorials.items():
            if self._check_tutorial_availability(player_id, tutorial):
                available.append(self._format_tutorial(tutorial, player_id))

        return available

    def _check_tutorial_availability(self, player_id: str, tutorial: dict[str, Any]) -> bool:
        """Vérifie si un tutoriel est disponible pour un joueur"""
        prerequisites = tutorial.get("prerequisites", [])

        for prereq in prerequisites:
            if not self._check_prerequisite(player_id, prereq):
                return False

        return True

    def _check_prerequisite(self, player_id: str, prereq: str) -> bool:
        """Vérifie un prérequis"""
        if player_id not in self.player_progress:
            return False

        completed_tutorials = self.player_progress[player_id].get("completed_tutorials", [])
        return prereq in completed_tutorials

    def _format_tutorial(self, tutorial: dict[str, Any], player_id: str) -> dict[str, Any]:
        """Formate un tutoriel pour l'affichage"""
        concept = self.concepts.get(tutorial.get("concept", ""), {})

        return {
            "id": tutorial["id"],
            "title": tutorial["title"],
            "description": tutorial["description"],
            "concept": concept,
            "difficulty": tutorial["difficulty"],
            "duration_minutes": tutorial["duration_minutes"],
            "learning_objectives": tutorial.get("learning_objectives", []),
            "progress": self._calculate_tutorial_progress(player_id, tutorial["id"]),
        }

    def _calculate_tutorial_progress(self, player_id: str, tutorial_id: str) -> dict[str, Any]:
        """Calcule la progression d'un tutoriel"""
        if player_id not in self.player_progress:
            return {"percentage": 0, "completed": False, "current_step": 0}

        tutorial_progress = (
            self.player_progress[player_id].get("tutorials", {}).get(tutorial_id, {})
        )

        if tutorial_progress.get("completed", False):
            return {"percentage": 100, "completed": True, "current_step": -1}

        current_step = tutorial_progress.get("current_step", 0)
        total_steps = len(self.tutorials[tutorial_id].get("content", []))

        percentage = (current_step / total_steps) * 100 if total_steps > 0 else 0

        return {
            "percentage": percentage,
            "completed": False,
            "current_step": current_step,
            "total_steps": total_steps,
        }

    def start_tutorial(self, player_id: str, tutorial_id: str) -> dict[str, Any]:
        """Démarre un tutoriel pour un joueur"""
        if tutorial_id not in self.tutorials:
            return {"error": "Tutoriel introuvable"}

        tutorial = self.tutorials[tutorial_id]

        if not self._check_tutorial_availability(player_id, tutorial):
            return {"error": "Tutoriel non disponible"}

        # Initialiser la progression
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {
                "tutorials": {},
                "completed_tutorials": [],
                "quiz_scores": {},
            }

        if tutorial_id not in self.player_progress[player_id]["tutorials"]:
            self.player_progress[player_id]["tutorials"][tutorial_id] = {
                "started_at": datetime.now().isoformat(),
                "current_step": 0,
                "completed": False,
                "quiz_completed": False,
                "quiz_score": 0,
            }

        return {
            "success": True,
            "tutorial": self._format_tutorial(tutorial, player_id),
            "message": f"Tutoriel '{tutorial['title']}' démarré !",
        }

    def get_tutorial_content(
        self, player_id: str, tutorial_id: str, step: int = 0
    ) -> dict[str, Any]:
        """Retourne le contenu d'un tutoriel à une étape donnée"""
        if tutorial_id not in self.tutorials:
            return {"error": "Tutoriel introuvable"}

        tutorial = self.tutorials[tutorial_id]
        content = tutorial.get("content", [])

        if step >= len(content):
            return {"error": "Étape invalide"}

        step_content = content[step]

        # Vérifier si l'étape est débloquée
        if not self._check_step_availability(player_id, tutorial_id, step):
            return {"error": "Étape non débloquée"}

        return {
            "tutorial_id": tutorial_id,
            "step": step,
            "total_steps": len(content),
            "content": step_content,
            "progress": self._calculate_tutorial_progress(player_id, tutorial_id),
        }

    def _check_step_availability(self, player_id: str, tutorial_id: str, step: int) -> bool:
        """Vérifie si une étape est débloquée"""
        if player_id not in self.player_progress:
            return False

        tutorial_progress = (
            self.player_progress[player_id].get("tutorials", {}).get(tutorial_id, {})
        )
        current_step = tutorial_progress.get("current_step", 0)

        return step <= current_step

    def complete_tutorial_step(
        self,
        player_id: str,
        tutorial_id: str,
        step: int,
        exercise_result: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Marque une étape de tutoriel comme terminée"""
        if player_id not in self.player_progress:
            return {"error": "Joueur non trouvé"}

        if tutorial_id not in self.player_progress[player_id]["tutorials"]:
            return {"error": "Tutoriel non démarré"}

        tutorial_progress = self.player_progress[player_id]["tutorials"][tutorial_id]
        current_step = tutorial_progress.get("current_step", 0)

        if step != current_step:
            return {"error": "Étape invalide"}

        # Marquer l'étape comme terminée
        tutorial_progress["current_step"] = step + 1

        # Vérifier si le tutoriel est terminé
        tutorial = self.tutorials[tutorial_id]
        total_steps = len(tutorial.get("content", []))

        if step + 1 >= total_steps:
            tutorial_progress["completed"] = True
            self.player_progress[player_id]["completed_tutorials"].append(tutorial_id)

            return {
                "success": True,
                "tutorial_completed": True,
                "message": "Tutoriel terminé ! Félicitations !",
                "rewards": self._calculate_tutorial_rewards(tutorial),
            }
        else:
            return {
                "success": True,
                "tutorial_completed": False,
                "message": "Étape terminée ! Continue !",
                "next_step": step + 1,
            }

    def _calculate_tutorial_rewards(self, tutorial: dict[str, Any]) -> dict[str, Any]:
        """Calcule les récompenses d'un tutoriel"""
        return {
            "xp": 200,
            "badges": ["tutorial_completed"],
            "unlock": tutorial.get("concept", ""),
        }

    def get_quiz(self, player_id: str, tutorial_id: str) -> dict[str, Any]:
        """Retourne le quiz d'un tutoriel"""
        if tutorial_id not in self.tutorials:
            return {"error": "Tutoriel introuvable"}

        tutorial = self.tutorials[tutorial_id]
        quiz = tutorial.get("quiz", {})

        if not quiz:
            return {"error": "Aucun quiz disponible pour ce tutoriel"}

        return {
            "tutorial_id": tutorial_id,
            "questions": quiz.get("questions", []),
            "time_limit": quiz.get("time_limit", 300),  # 5 minutes par défaut
        }

    def submit_quiz(
        self, player_id: str, tutorial_id: str, answers: dict[str, int]
    ) -> dict[str, Any]:
        """Soumet les réponses d'un quiz"""
        if tutorial_id not in self.tutorials:
            return {"error": "Tutoriel introuvable"}

        tutorial = self.tutorials[tutorial_id]
        quiz = tutorial.get("quiz", {})
        questions = quiz.get("questions", [])

        if not questions:
            return {"error": "Aucun quiz disponible"}

        # Calculer le score
        correct_answers = 0
        total_questions = len(questions)

        for question in questions:
            question_id = question["id"]
            if question_id in answers:
                if answers[question_id] == question["correct"]:
                    correct_answers += 1

        score = (correct_answers / total_questions) * 100

        # Sauvegarder le score
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {
                "tutorials": {},
                "completed_tutorials": [],
                "quiz_scores": {},
            }

        self.player_progress[player_id]["quiz_scores"][tutorial_id] = score

        # Marquer le quiz comme terminé
        if tutorial_id in self.player_progress[player_id]["tutorials"]:
            self.player_progress[player_id]["tutorials"][tutorial_id]["quiz_completed"] = True
            self.player_progress[player_id]["tutorials"][tutorial_id]["quiz_score"] = score

        return {
            "success": True,
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "passed": score >= 70,  # 70% pour réussir
            "message": "Quiz terminé !" if score >= 70 else "Quiz échoué, réessaie !",
        }

    def get_references(self, category: Optional[str] = None) -> dict[str, Any]:
        """Retourne les références d'apprentissage"""
        if category:
            return {category: self.references.get(category, [])}
        else:
            return self.references

    def get_concepts(self) -> dict[str, Any]:
        """Retourne tous les concepts disponibles"""
        return self.concepts

    def get_player_progress(self, player_id: str) -> dict[str, Any]:
        """Retourne la progression d'un joueur"""
        if player_id not in self.player_progress:
            return {"tutorials": {}, "completed_tutorials": [], "quiz_scores": {}}

        return self.player_progress[player_id]

    def save_tutorial_data(self) -> bool:
        """Sauvegarde les données de tutoriels"""
        try:
            data = {
                "tutorials": self.tutorials,
                "concepts": self.concepts,
                "references": self.references,
                "player_progress": self.player_progress,
                "quizzes": self.quizzes,
            }

            with open("data/technical_tutorials.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde tutoriels: {e}")
            return False


# Instance globale
technical_tutorials = TechnicalTutorials()
