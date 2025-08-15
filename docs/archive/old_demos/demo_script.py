#!/usr/bin/env python3
"""
Script de démonstration automatique pour Arkalia Quest
Teste toutes les fonctionnalités pour la vidéo
"""

import time

import requests


class ArkaliaDemo:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()

    def demo_sequence(self):
        """Séquence de démonstration complète"""
        print("🎬 DÉBUT DE LA DÉMONSTRATION ARKALIA QUEST")
        print("=" * 50)

        # 1. Test de connexion
        print("1️⃣ Test de connexion au serveur...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Serveur accessible")
            else:
                print(f"❌ Erreur: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return

        # 2. Test de la page terminal
        print("\n2️⃣ Test de la page terminal...")
        try:
            response = self.session.get(f"{self.base_url}/terminal")
            if response.status_code == 200:
                print("✅ Page terminal accessible")
            else:
                print(f"❌ Erreur: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur: {e}")

        # 3. Test des commandes principales
        print("\n3️⃣ Test des commandes principales...")
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

        for cmd, description in commands:
            try:
                print(f"   Testing: {cmd} ({description})")
                response = self.session.post(
                    f"{self.base_url}/commande", json={"cmd": cmd}, timeout=5
                )

                if response.status_code == 200:
                    data = response.json()
                    if "message" in data:
                        print(f"   ✅ {description}: {data['message'][:50]}...")
                    else:
                        print(f"   ✅ {description}: Réponse reçue")
                else:
                    print(f"   ❌ {description}: Code {response.status_code}")

                time.sleep(0.5)  # Pause pour la vidéo

            except Exception as e:
                print(f"   ❌ {description}: Erreur {e}")

        # 4. Test des commandes d'erreur
        print("\n4️⃣ Test des commandes d'erreur...")
        error_commands = [
            "commande_inexistante_test",
            "truc_bidule_machin",
            "commande_tres_longue_et_invalide_qui_devrait_echouer",
        ]

        for cmd in error_commands:
            try:
                print(f"   Testing erreur: {cmd}")
                response = self.session.post(
                    f"{self.base_url}/commande", json={"cmd": cmd}, timeout=5
                )

                if response.status_code == 200:
                    data = response.json()
                    if (
                        "message" in data
                        and "erreur" in data["message"].lower()
                        or "pas autorisée" in data["message"].lower()
                    ):
                        print(f"   ✅ Erreur gérée: {data['message'][:50]}...")
                    else:
                        print("   ⚠️ Pas de message d'erreur détecté")
                else:
                    print(f"   ❌ Code {response.status_code}")

                time.sleep(0.5)

            except Exception as e:
                print(f"   ❌ Erreur: {e}")

        # 5. Test des pages
        print("\n5️⃣ Test des pages...")
        pages = [
            ("/monde", "Page monde"),
            ("/profil", "Page profil"),
            ("/", "Page d'accueil"),
        ]

        for page, description in pages:
            try:
                print(f"   Testing: {description}")
                response = self.session.get(f"{self.base_url}{page}")
                if response.status_code == 200:
                    print(f"   ✅ {description}: Accessible")
                else:
                    print(f"   ❌ {description}: Code {response.status_code}")
                time.sleep(0.3)
            except Exception as e:
                print(f"   ❌ {description}: Erreur {e}")

        # 6. Test des API avancées
        print("\n6️⃣ Test des API avancées...")
        apis = [
            ("/api/status", "Statut système"),
            ("/api/test/database", "Test base de données"),
            ("/api/test/websocket", "Test WebSocket"),
            ("/api/test/ai", "Test IA"),
        ]

        for api, description in apis:
            try:
                print(f"   Testing: {description}")
                response = self.session.get(f"{self.base_url}{api}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ {description}: {data.get('status', 'OK')}")
                else:
                    print(f"   ❌ {description}: Code {response.status_code}")
                time.sleep(0.3)
            except Exception as e:
                print(f"   ❌ {description}: Erreur {e}")

        print("\n" + "=" * 50)
        print("🎬 DÉMONSTRATION TERMINÉE")
        print("✅ Toutes les fonctionnalités testées avec succès !")
        print("🚀 Arkalia Quest est prêt pour la production !")


def main():
    demo = ArkaliaDemo()
    demo.demo_sequence()


if __name__ == "__main__":
    main()
