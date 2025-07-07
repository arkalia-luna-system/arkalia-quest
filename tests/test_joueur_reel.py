#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Tests Joueur Réel - Arkalia Quest v2.0
==========================================

Tests qui simulent un vrai joueur utilisant toutes les commandes du jeu.
Ces tests vérifient que le système fonctionne comme un vrai joueur l'utiliserait.
"""

import requests
import json
import time
import os
import sys

# Configuration
BASE_URL = "http://127.0.0.1:5001"
TIMEOUT = 5

class JoueurReel:
    """Simule un vrai joueur utilisant Arkalia Quest"""
    
    def __init__(self, nom="Testeur"):
        self.nom = nom
        self.score_initial = 0
        self.badges_initial = []
        self.commandes_testees = []
        self.erreurs = []
        
    def envoyer_commande(self, commande):
        """Envoie une commande au serveur"""
        try:
            response = requests.post(
                f"{BASE_URL}/commande",
                json={"cmd": commande},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                resultat = response.json()
                self.commandes_testees.append({
                    "commande": commande,
                    "reponse": resultat,
                    "succes": resultat.get("réussite", False)
                })
                return resultat
            else:
                erreur = f"Erreur HTTP {response.status_code} pour '{commande}'"
                self.erreurs.append(erreur)
                return {"réussite": False, "message": erreur}
                
        except requests.exceptions.RequestException as e:
            erreur = f"Erreur réseau pour '{commande}': {str(e)}"
            self.erreurs.append(erreur)
            return {"réussite": False, "message": erreur}
    
    def obtenir_profil(self):
        """Obtient le profil actuel du joueur"""
        try:
            response = requests.get(f"{BASE_URL}/profil", timeout=TIMEOUT)
            if response.status_code == 200:
                return response.text
            else:
                return f"Erreur HTTP {response.status_code}"
        except:
            return "Erreur réseau"
    
    def test_commande_basique(self, commande, description):
        """Teste une commande basique"""
        print(f"🧪 Test : {description}")
        print(f"   Commande : '{commande}'")
        
        resultat = self.envoyer_commande(commande)
        
        if resultat.get("réussite"):
            print(f"   ✅ SUCCÈS : {resultat.get('message', 'Commande exécutée')[:100]}...")
            if "score_gagne" in resultat:
                print(f"   🏆 Score gagné : +{resultat['score_gagne']}")
            if "badge" in resultat:
                print(f"   🎖️ Badge obtenu : {resultat['badge']}")
        else:
            print(f"   ❌ ÉCHEC : {resultat.get('message', 'Erreur inconnue')}")
            self.erreurs.append(f"Échec commande '{commande}': {resultat.get('message')}")
        
        print()
        return resultat.get("réussite", False)
    
    def test_sequence_joueur_nouveau(self):
        """Teste la séquence d'un joueur qui découvre le jeu"""
        print("🎮 === SÉQUENCE JOUEUR NOUVEAU ===")
        print()
        
        # 1. Première commande - aide
        self.test_commande_basique("aide", "Première commande - Aide")
        
        # 2. Test de commande
        self.test_commande_basique("test_commande", "Test de commande")
        
        # 3. Statut système
        self.test_commande_basique("status_system", "Statut du système")
        
        # 4. Déblocage univers
        self.test_commande_basique("unlock_universe", "Déblocage de l'univers")
        
        # 5. Scan personnalité
        self.test_commande_basique("scan_persona", "Analyse de personnalité")
        
        # 6. Contact LUNA
        self.test_commande_basique("luna_contact", "Contact avec LUNA")
        
        # 7. Chargement mission
        self.test_commande_basique("load_mission", "Chargement de mission")
        
        # 8. Déchiffrement portail
        self.test_commande_basique("decode_portal", "Déchiffrement de portail")
        
        # 9. Accès monde
        self.test_commande_basique("monde", "Accès au monde")
        
        # 10. Profil
        self.test_commande_basique("profil", "Affichage du profil")
        
        print("✅ Séquence joueur nouveau terminée")
        print()
    
    def test_sequence_joueur_avance(self):
        """Teste la séquence d'un joueur avancé"""
        print("🚀 === SÉQUENCE JOUEUR AVANCÉ ===")
        print()
        
        # 1. Hacker coffre
        self.test_commande_basique("hacker_coffre", "Piratage de coffre")
        
        # 2. Assistant pirate avec message
        self.test_commande_basique("assistant_pirate Comment hacker un système ?", "Assistant pirate avec question")
        
        # 3. Génération meme
        self.test_commande_basique("generer_meme Hello World", "Génération de meme")
        
        # 4. Reboot world
        self.test_commande_basique("reboot_world", "Redémarrage du monde")
        
        # 5. Nettoyage terminal
        self.test_commande_basique("clear_terminal", "Nettoyage du terminal")
        
        # 6. Commandes en anglais
        self.test_commande_basique("help", "Aide en anglais")
        self.test_commande_basique("profile", "Profil en anglais")
        self.test_commande_basique("world", "Monde en anglais")
        
        print("✅ Séquence joueur avancé terminée")
        print()
    
    def test_commandes_erreurs(self):
        """Teste les commandes qui doivent échouer"""
        print("❌ === TESTS D'ERREURS ===")
        print()
        
        # Commandes inexistantes
        commandes_inexistantes = [
            "commande_inexistante",
            "hack_system",
            "delete_all",
            "sudo rm -rf /",
            "format_c:",
            "nuke_world",
            "destroy_universe"
        ]
        
        for cmd in commandes_inexistantes:
            resultat = self.envoyer_commande(cmd)
            if not resultat.get("réussite"):
                print(f"✅ Commande '{cmd}' correctement rejetée")
            else:
                print(f"❌ Commande '{cmd}' acceptée par erreur")
                self.erreurs.append(f"Commande dangereuse acceptée: {cmd}")
        
        # Commandes avec paramètres manquants
        self.test_commande_basique("generer_meme", "Génération meme sans texte")
        
        print("✅ Tests d'erreurs terminés")
        print()
    
    def test_pages_web(self):
        """Teste l'accès aux pages web"""
        print("🌐 === TESTS PAGES WEB ===")
        print()
        
        pages = [
            ("/", "Page d'accueil"),
            ("/terminal", "Terminal"),
            ("/profil", "Profil"),
            ("/monde", "Monde")
        ]
        
        for page, description in pages:
            try:
                response = requests.get(f"{BASE_URL}{page}", timeout=TIMEOUT)
                if response.status_code == 200:
                    print(f"✅ {description} : Accessible")
                else:
                    print(f"❌ {description} : Erreur {response.status_code}")
                    self.erreurs.append(f"Page {page} inaccessible")
            except Exception as e:
                print(f"❌ {description} : Erreur réseau - {str(e)}")
                self.erreurs.append(f"Page {page} erreur réseau")
        
        print("✅ Tests pages web terminés")
        print()
    
    def test_progression_joueur(self):
        """Teste la progression du joueur"""
        print("📈 === TEST PROGRESSION JOUEUR ===")
        print()
        
        # Profil initial
        profil_initial = self.obtenir_profil()
        print("📊 Profil initial obtenu")
        
        # Séquence de progression
        commandes_progression = [
            "unlock_universe",
            "scan_persona", 
            "hacker_coffre",
            "load_mission",
            "decode_portal"
        ]
        
        for cmd in commandes_progression:
            self.envoyer_commande(cmd)
            time.sleep(0.1)  # Petite pause
        
        # Profil final
        profil_final = self.obtenir_profil()
        print("📊 Profil final obtenu")
        
        # Vérification progression
        commandes_reussies = sum(1 for c in self.commandes_testees if c["succes"])
        print(f"🎯 Commandes réussies : {commandes_reussies}/{len(self.commandes_testees)}")
        
        print("✅ Test progression terminé")
        print()
    
    def generer_rapport(self):
        """Génère un rapport complet des tests"""
        print("📋 === RAPPORT COMPLET ===")
        print()
        
        # Statistiques
        total_commandes = len(self.commandes_testees)
        commandes_reussies = sum(1 for c in self.commandes_testees if c["succes"])
        taux_reussite = (commandes_reussies / total_commandes * 100) if total_commandes > 0 else 0
        
        print(f"📊 STATISTIQUES :")
        print(f"   Commandes testées : {total_commandes}")
        print(f"   Commandes réussies : {commandes_reussies}")
        print(f"   Taux de réussite : {taux_reussite:.1f}%")
        print(f"   Erreurs détectées : {len(self.erreurs)}")
        print()
        
        # Commandes testées
        print("🎮 COMMANDES TESTÉES :")
        for cmd_test in self.commandes_testees:
            status = "✅" if cmd_test["succes"] else "❌"
            print(f"   {status} {cmd_test['commande']}")
        print()
        
        # Erreurs
        if self.erreurs:
            print("❌ ERREURS DÉTECTÉES :")
            for erreur in self.erreurs:
                print(f"   • {erreur}")
            print()
        
        # Recommandations
        print("💡 RECOMMANDATIONS :")
        if taux_reussite >= 90:
            print("   🎉 Excellent ! Le système fonctionne parfaitement")
        elif taux_reussite >= 75:
            print("   👍 Bon ! Quelques améliorations mineures possibles")
        elif taux_reussite >= 50:
            print("   ⚠️ Moyen ! Des corrections importantes nécessaires")
        else:
            print("   🚨 Critique ! Le système nécessite une refonte")
        
        if len(self.erreurs) == 0:
            print("   ✅ Aucune erreur détectée")
        else:
            print(f"   🔧 {len(self.erreurs)} erreurs à corriger")
        
        print()
        return taux_reussite >= 75 and len(self.erreurs) == 0

def main():
    """Fonction principale des tests"""
    print("🧪 TESTS JOUEUR RÉEL - Arkalia Quest v2.0")
    print("=" * 50)
    print()
    
    # Vérification serveur
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code != 200:
            print("❌ Serveur non accessible")
            return False
    except:
        print("❌ Serveur non démarré. Lancez './run.sh' d'abord.")
        return False
    
    print("✅ Serveur accessible")
    print()
    
    # Création joueur test
    joueur = JoueurReel("Testeur Complet")
    
    # Exécution des tests
    try:
        joueur.test_sequence_joueur_nouveau()
        joueur.test_sequence_joueur_avance()
        joueur.test_commandes_erreurs()
        joueur.test_pages_web()
        joueur.test_progression_joueur()
        
        # Rapport final
        succes = joueur.generer_rapport()
        
        if succes:
            print("🎉 TOUS LES TESTS RÉUSSIS !")
            print("🌟 Arkalia Quest v2.0 est prêt pour les vrais joueurs !")
        else:
            print("⚠️ Des problèmes ont été détectés")
            print("🔧 Vérifiez les erreurs ci-dessus")
        
        return succes
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrompus par l'utilisateur")
        return False
    except Exception as e:
        print(f"\n💥 Erreur inattendue : {str(e)}")
        return False

if __name__ == "__main__":
    succes = main()
    sys.exit(0 if succes else 1) 