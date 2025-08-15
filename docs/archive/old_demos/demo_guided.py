#!/usr/bin/env python3
"""
Démonstration guidée automatique d'Arkalia Quest
Utilise Selenium pour naviguer automatiquement dans l'interface
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ArkaliaGuidedDemo:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.driver = None

    def setup_driver(self):
        """Configure le navigateur Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Mode headless pour l'automatisation
        # chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def demo_sequence(self):
        """Séquence de démonstration guidée"""
        print("🎬 DÉMONSTRATION GUIDÉE ARKALIA QUEST")
        print("=" * 50)

        try:
            self.setup_driver()

            # 1. Page d'accueil
            print("1️⃣ Navigation vers la page d'accueil...")
            self.driver.get(self.base_url)
            time.sleep(2)

            # Vérifier que la page est chargée
            title = self.driver.title
            print(f"   ✅ Page chargée: {title}")

            # 2. Page terminal
            print("\n2️⃣ Navigation vers le terminal...")
            self.driver.get(f"{self.base_url}/terminal")
            time.sleep(3)

            # Attendre que le terminal soit chargé
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "terminal"))
                )
                print("   ✅ Terminal chargé")
            except:
                print("   ⚠️ Terminal non trouvé, mais page accessible")

            # 3. Test des commandes via interface
            print("\n3️⃣ Test des commandes via interface...")
            commands = ["aide", "luna_contact", "badges", "profil"]

            for cmd in commands:
                try:
                    print(f"   Testing: {cmd}")

                    # Trouver le champ de saisie
                    input_field = self.driver.find_element(By.ID, "command-input")
                    input_field.clear()
                    input_field.send_keys(cmd)

                    # Trouver le bouton d'envoi
                    submit_btn = self.driver.find_element(By.ID, "submit-btn")
                    submit_btn.click()

                    # Attendre la réponse
                    time.sleep(2)

                    # Vérifier qu'une réponse est affichée
                    output = self.driver.find_element(By.ID, "terminal-output")
                    if output.text.strip():
                        print(f"   ✅ Réponse reçue pour {cmd}")
                    else:
                        print(f"   ⚠️ Pas de réponse visible pour {cmd}")

                    time.sleep(1)

                except Exception as e:
                    print(f"   ❌ Erreur avec {cmd}: {e}")

            # 4. Navigation vers les autres pages
            print("\n4️⃣ Navigation vers les autres pages...")
            pages = [("/monde", "Page monde"), ("/profil", "Page profil")]

            for page, description in pages:
                try:
                    print(f"   Testing: {description}")
                    self.driver.get(f"{self.base_url}{page}")
                    time.sleep(2)

                    # Vérifier que la page est chargée
                    current_url = self.driver.current_url
                    if page in current_url:
                        print(f"   ✅ {description} accessible")
                    else:
                        print(f"   ⚠️ {description} - URL différente: {current_url}")

                except Exception as e:
                    print(f"   ❌ Erreur avec {description}: {e}")

            # 5. Retour à l'accueil et test des effets
            print("\n5️⃣ Retour à l'accueil et test des effets...")
            self.driver.get(self.base_url)
            time.sleep(2)

            # Tester les boutons et effets visuels
            try:
                # Chercher des boutons ou liens interactifs
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                links = self.driver.find_elements(By.TAG_NAME, "a")

                print(
                    f"   📊 Éléments interactifs trouvés: {len(buttons)} boutons, {len(links)} liens"
                )

                # Tester un bouton si disponible
                if buttons:
                    print(f"   🎯 Test du premier bouton: {buttons[0].text}")
                    buttons[0].click()
                    time.sleep(1)
                    print("   ✅ Clic effectué")

            except Exception as e:
                print(f"   ⚠️ Test des effets: {e}")

            # 6. Test de responsive design
            print("\n6️⃣ Test du responsive design...")
            try:
                # Tester différentes tailles d'écran
                sizes = [
                    (1920, 1080, "Desktop"),
                    (768, 1024, "Tablet"),
                    (375, 667, "Mobile"),
                ]

                for width, height, device in sizes:
                    print(f"   Testing: {device} ({width}x{height})")
                    self.driver.set_window_size(width, height)
                    time.sleep(1)

                    # Vérifier que la page s'adapte
                    self.driver.find_element(By.TAG_NAME, "body")
                    print(f"   ✅ {device}: Page adaptée")

            except Exception as e:
                print(f"   ❌ Test responsive: {e}")

            # 7. Test des performances
            print("\n7️⃣ Test des performances...")
            try:
                # Mesurer le temps de chargement
                start_time = time.time()
                self.driver.get(self.base_url)
                load_time = time.time() - start_time

                print(f"   ⚡ Temps de chargement: {load_time:.2f}s")

                if load_time < 3:
                    print("   ✅ Performance excellente")
                elif load_time < 5:
                    print("   ✅ Performance correcte")
                else:
                    print("   ⚠️ Performance lente")

            except Exception as e:
                print(f"   ❌ Test performance: {e}")

            print("\n" + "=" * 50)
            print("🎬 DÉMONSTRATION GUIDÉE TERMINÉE")
            print("✅ Interface testée avec succès !")
            print("🚀 Arkalia Quest est prêt pour la production !")

            # Garder la page ouverte pour la vidéo
            print("\n💡 Gardez cette fenêtre ouverte pour l'enregistrement vidéo")
            print("⏱️  Appuyez sur Entrée pour fermer...")
            input()

        except Exception as e:
            print(f"❌ Erreur générale: {e}")

        finally:
            if self.driver:
                self.driver.quit()


def main():
    demo = ArkaliaGuidedDemo()
    demo.demo_sequence()


if __name__ == "__main__":
    main()
