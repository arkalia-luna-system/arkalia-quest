#!/usr/bin/env python3
"""
Démonstration vidéo améliorée d'Arkalia Quest
Avec gestion d'erreurs détaillée et affichage en temps réel
"""

import sys
import time
from datetime import datetime

import requests


class ArkaliaVideoDemo:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.errors = []
        self.successes = []
        self.start_time = datetime.now()

    def log_success(self, message):
        """Enregistre un succès"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"✅ [{timestamp}] {message}")
        self.successes.append(f"[{timestamp}] {message}")

    def log_error(self, message, error=None):
        """Enregistre une erreur"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        error_msg = f"❌ [{timestamp}] {message}"
        if error:
            error_msg += f" - Erreur: {error}"
        print(error_msg)
        self.errors.append(error_msg)

    def log_info(self, message):
        """Enregistre une information"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"i  [{timestamp}] {message}")

    def check_server(self):
        """Vérifie que le serveur fonctionne"""
        self.log_info("🔍 Vérification du serveur...")
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log_success("Serveur accessible et fonctionnel")
                return True
            else:
                self.log_error(f"Serveur répond avec code {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.log_error("Impossible de se connecter au serveur")
            return False
        except Exception as e:
            self.log_error("Erreur de connexion", str(e))
            return False

    def test_page(self, page, description):
        """Teste une page spécifique"""
        try:
            self.log_info(f"Testing: {description}")
            response = self.session.get(f"{self.base_url}{page}", timeout=5)

            if response.status_code == 200:
                self.log_success(f"{description}: Accessible")
                return True
            else:
                self.log_error(f"{description}: Code {response.status_code}")
                return False

        except Exception as e:
            self.log_error(f"{description}: Erreur", str(e))
            return False

    def test_command(self, cmd, description):
        """Teste une commande spécifique"""
        try:
            self.log_info(f"Testing: {cmd} ({description})")

            response = self.session.post(
                f"{self.base_url}/commande", json={"cmd": cmd}, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    message = (
                        data["message"][:100] + "..."
                        if len(data["message"]) > 100
                        else data["message"]
                    )
                    self.log_success(f"{description}: {message}")
                else:
                    self.log_success(f"{description}: Réponse reçue")
                return True
            else:
                self.log_error(f"{description}: Code {response.status_code}")
                return False

        except requests.exceptions.Timeout:
            self.log_error(f"{description}: Timeout")
            return False
        except Exception as e:
            self.log_error(f"{description}: Erreur", str(e))
            return False

    def test_api(self, endpoint, description):
        """Teste un endpoint API"""
        try:
            self.log_info(f"Testing API: {description}")

            response = self.session.get(f"{self.base_url}{endpoint}", timeout=5)

            if response.status_code == 200:
                try:
                    data = response.json()
                    status = data.get("status", "OK")
                    self.log_success(f"{description}: {status}")
                except Exception:
                    self.log_success(f"{description}: Réponse JSON reçue")
                return True
            else:
                self.log_error(f"{description}: Code {response.status_code}")
                return False

        except Exception as e:
            self.log_error(f"{description}: Erreur", str(e))
            return False

    def run_demo_sequence(self):
        """Lance la séquence de démonstration complète"""
        print("🎬 DÉMONSTRATION VIDÉO AMÉLIORÉE ARKALIA QUEST")
        print("=" * 60)
        print(f"🕐 Démarrage: {self.start_time.strftime('%H:%M:%S')}")
        print()

        # 1. Vérification du serveur
        if not self.check_server():
            print("❌ Impossible de continuer sans serveur")
            return False

        # 2. Test des pages principales
        print("\n📄 TEST DES PAGES PRINCIPALES")
        print("-" * 30)
        pages = [
            ("/", "Page d'accueil"),
            ("/terminal", "Page terminal"),
            ("/monde", "Page monde"),
            ("/profil", "Page profil"),
        ]

        page_success = 0
        for page, description in pages:
            if self.test_page(page, description):
                page_success += 1
            time.sleep(0.5)

        # 3. Test des commandes principales
        print("\n🎮 TEST DES COMMANDES PRINCIPALES")
        print("-" * 35)
        commands = [
            ("aide", "Commande d'aide"),
            ("luna_contact", "Contact LUNA"),
            ("start_tutorial", "Tutoriel"),
            ("badges", "Badges"),
            ("profil", "Profil"),
            ("hack_system", "Hack système"),
            ("kill_virus", "Tue virus"),
            ("find_shadow", "Trouve SHADOW"),
            ("challenge_corp", "Défi Corp"),
            ("luna_dance", "LUNA danse"),
            ("boss_final", "Boss final"),
            ("easter_egg_1337", "Easter egg"),
            ("meme_war", "Guerre de memes"),
            ("nuke_world", "Nuke world"),
            ("luna_rage", "LUNA rage"),
        ]

        command_success = 0
        for cmd, description in commands:
            if self.test_command(cmd, description):
                command_success += 1
            time.sleep(0.8)  # Pause plus longue pour la vidéo

        # 4. Test des commandes d'erreur
        print("\n⚠️  TEST DE GESTION D'ERREURS")
        print("-" * 30)
        error_commands = [
            "commande_inexistante_test",
            "truc_bidule_machin",
            "commande_tres_longue_et_invalide_qui_devrait_echouer",
        ]

        error_success = 0
        for cmd in error_commands:
            try:
                self.log_info(f"Testing erreur: {cmd}")
                response = self.session.post(
                    f"{self.base_url}/commande", json={"cmd": cmd}, timeout=5
                )

                if response.status_code == 200:
                    data = response.json()
                    if "message" in data and (
                        "erreur" in data["message"].lower()
                        or "pas autorisée" in data["message"].lower()
                    ):
                        self.log_success(f"Erreur gérée: {data['message'][:50]}...")
                        error_success += 1
                    else:
                        self.log_error("Pas de message d'erreur détecté")
                else:
                    self.log_error(f"Code {response.status_code}")

                time.sleep(0.5)

            except Exception as e:
                self.log_error(f"Erreur: {e}")

        # 5. Test des API avancées
        print("\n🔧 TEST DES API AVANCÉES")
        print("-" * 25)
        apis = [
            ("/api/status", "Statut système"),
            ("/api/test/database", "Test base de données"),
            ("/api/test/websocket", "Test WebSocket"),
            ("/api/test/ai", "Test IA"),
        ]

        api_success = 0
        for api, description in apis:
            if self.test_api(api, description):
                api_success += 1
            time.sleep(0.3)

        # 6. Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DE LA DÉMONSTRATION")
        print("=" * 60)

        total_tests = len(pages) + len(commands) + len(error_commands) + len(apis)
        total_success = page_success + command_success + error_success + api_success

        print(f"📄 Pages testées: {page_success}/{len(pages)} ✅")
        print(f"🎮 Commandes testées: {command_success}/{len(commands)} ✅")
        print(f"⚠️  Erreurs gérées: {error_success}/{len(error_commands)} ✅")
        print(f"🔧 API testées: {api_success}/{len(apis)} ✅")
        print()
        print(
            f"🎯 Score global: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)"
        )

        if total_success == total_tests:
            print("🏆 DÉMONSTRATION PARFAITE !")
        elif total_success >= total_tests * 0.9:
            print("✅ DÉMONSTRATION EXCELLENTE !")
        elif total_success >= total_tests * 0.8:
            print("👍 DÉMONSTRATION BONNE !")
        else:
            print("⚠️  DÉMONSTRATION AVEC PROBLÈMES")

        # 7. Affichage des erreurs si il y en a
        if self.errors:
            print(f"\n❌ ERREURS DÉTECTÉES ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")

        end_time = datetime.now()
        duration = end_time - self.start_time
        print(f"\n⏱️  Durée totale: {duration}")
        print("🎬 DÉMONSTRATION TERMINÉE")

        return total_success == total_tests


def main():
    demo = ArkaliaVideoDemo()
    success = demo.run_demo_sequence()

    if success:
        print("\n🚀 Arkalia Quest est prêt pour la production !")
        sys.exit(0)
    else:
        print("\n⚠️  Des problèmes ont été détectés")
        sys.exit(1)


if __name__ == "__main__":
    main()
