import random
import json

def analyser_personnalite(profil):
    """
    Analyse la personnalité du joueur basée sur ses actions et préférences
    """
    score_creatif = 0
    score_analytique = 0
    score_social = 0
    
    # Analyse basée sur les badges obtenus
    badges = profil.get("badges", [])
    for badge in badges:
        if any(mot in badge.lower() for mot in ["créatif", "artiste", "visuel", "meme"]):
            score_creatif += 2
        elif any(mot in badge.lower() for mot in ["analytique", "espion", "déchiffreur", "maître"]):
            score_analytique += 2
        elif any(mot in badge.lower() for mot in ["social", "communicateur", "assistant"]):
            score_social += 2
    
    # Analyse basée sur les missions complétées
    missions = profil.get("personnalite", {}).get("missions_completees", [])
    if len(missions) > 0:
        # Si beaucoup de missions, tendance analytique
        score_analytique += len(missions)
    
    # Analyse basée sur le score total
    score_total = profil.get("score", 0)
    if score_total > 200:
        score_creatif += 1
    if score_total > 300:
        score_analytique += 1
    
    # Détermination du type dominant
    scores = {
        "hacker_creatif": score_creatif,
        "hacker_analytique": score_analytique,
        "hacker_social": score_social
    }
    
    max_score = max(scores.values())
    if max_score == 0:
        return "hacker_equilibre"
    
    # Retourne le type avec le score le plus élevé
    for type_perso, score in scores.items():
        if score == max_score:
            return type_perso
    
    return "hacker_equilibre"

def generer_mission_personnalisee(profil):
    """
    Génère une mission personnalisée selon le type de personnalité détecté
    """
    type_personnalite = profil.get("personnalite", {}).get("type", "hacker_equilibre")
    
    missions_par_type = {
        "hacker_creatif": [
            {
                "id": "creatif_1",
                "titre": "🎨 Créer un Code Visuel",
                "description": "Tu dois créer un algorithme qui génère des motifs visuels. Utilise ta créativité pour inventer des patterns uniques !",
                "difficulte": "moyenne",
                "recompense": 60,
                "type": "creation"
            },
            {
                "id": "creatif_2", 
                "titre": "🎭 Pirater l'Interface Artistique",
                "description": "Infiltrer un système qui contrôle des installations artistiques. Trouve une approche créative et originale !",
                "difficulte": "difficile",
                "recompense": 80,
                "type": "infiltration"
            }
        ],
        "hacker_analytique": [
            {
                "id": "analytique_1",
                "titre": "🔍 Analyser le Code Crypté",
                "description": "Déchiffrer un algorithme complexe en analysant ses patterns et sa structure logique.",
                "difficulte": "moyenne", 
                "recompense": 70,
                "type": "analyse"
            },
            {
                "id": "analytique_2",
                "titre": "⚙️ Optimiser le Système",
                "description": "Trouver les failles d'efficacité dans un système et proposer des améliorations logiques.",
                "difficulte": "difficile",
                "recompense": 90,
                "type": "optimisation"
            }
        ],
        "hacker_social": [
            {
                "id": "social_1",
                "titre": "🤝 Infiltrer le Réseau Social",
                "description": "Utiliser tes compétences sociales pour gagner la confiance d'un système IA et l'amener à coopérer.",
                "difficulte": "moyenne",
                "recompense": 65,
                "type": "social"
            },
            {
                "id": "social_2",
                "titre": "💬 Décoder les Messages Cachés",
                "description": "Analyser les communications entre systèmes pour comprendre leurs motivations et intentions.",
                "difficulte": "difficile",
                "recompense": 85,
                "type": "communication"
            }
        ],
        "hacker_equilibre": [
            {
                "id": "equilibre_1",
                "titre": "⚖️ Mission Équilibrée",
                "description": "Combiner créativité, logique et empathie pour résoudre un défi complexe qui nécessite toutes tes compétences.",
                "difficulte": "moyenne",
                "recompense": 75,
                "type": "mixte"
            },
            {
                "id": "equilibre_2",
                "titre": "🌟 Débloquer le Potentiel Complet",
                "description": "Utiliser tes multiples talents pour déverrouiller un système qui s'adapte à ton style unique.",
                "difficulte": "difficile", 
                "recompense": 100,
                "type": "adaptatif"
            }
        ]
    }
    
    missions_disponibles = missions_par_type.get(type_personnalite, missions_par_type["hacker_equilibre"])
    
    # Éviter de répéter les missions déjà complétées
    missions_completees = profil.get("personnalite", {}).get("missions_completees", [])
    missions_nouvelles = [m for m in missions_disponibles if m["id"] not in missions_completees]
    
    if missions_nouvelles:
        return random.choice(missions_nouvelles)
    else:
        # Si toutes les missions sont complétées, générer une mission spéciale
        return {
            "id": f"{type_personnalite}_special",
            "titre": "🏆 Mission Maître",
            "description": f"Tu as maîtrisé tous les aspects de ton profil {type_personnalite.replace('_', ' ').title()}. Maintenant, prouve que tu es un vrai maître !",
            "difficulte": "expert",
            "recompense": 150,
            "type": "maitre"
        }

def obtenir_conseils_personnalite(type_personnalite):
    """
    Retourne des conseils personnalisés selon le type de personnalité
    """
    conseils = {
        "hacker_creatif": [
            "Utilise ta créativité pour trouver des solutions uniques",
            "N'hésite pas à expérimenter et à penser différemment",
            "Transforme les problèmes en opportunités artistiques"
        ],
        "hacker_analytique": [
            "Décompose les problèmes en parties logiques",
            "Analyse chaque détail pour trouver les patterns",
            "Utilise la méthode scientifique pour tester tes hypothèses"
        ],
        "hacker_social": [
            "Écoute et observe les systèmes pour comprendre leurs motivations",
            "Utilise l'empathie pour anticiper les réactions",
            "Construis des relations de confiance avec les IA"
        ],
        "hacker_equilibre": [
            "Adapte ton approche selon la situation",
            "Combine différentes méthodes pour des résultats optimaux",
            "Reste flexible et ouvert à toutes les possibilités"
        ]
    }
    
    return conseils.get(type_personnalite, ["Continue d'explorer et d'apprendre !"]) 