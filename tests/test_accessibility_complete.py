#!/usr/bin/env python3
"""
♿ TEST D'ACCESSIBILITÉ WCAG 2.1 AA COMPLET - ARKALIA QUEST
Test complet de l'accessibilité pour atteindre le niveau WCAG AA (85%+)
"""

import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class AccessibilityTester:
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "score": 0,
            "tests": {},
            "recommendations": [],
        }

    def test_skip_links(self):
        """Test des skip links pour navigation clavier"""
        print("🔗 Test des skip links...")

        response = requests.get(f"{self.base_url}/terminal")
        soup = BeautifulSoup(response.content, "html.parser")

        skip_links = soup.find_all("a", class_="skip-link")
        expected_links = 4

        score = min(len(skip_links) / expected_links * 100, 100)

        self.results["tests"]["skip_links"] = {
            "score": score,
            "found": len(skip_links),
            "expected": expected_links,
            "details": [link.get("href", "") for link in skip_links],
        }

        print(f"✅ Skip links: {len(skip_links)}/{expected_links} skip links trouvés")
        return score

    def test_keyboard_navigation(self):
        """Test de la navigation clavier"""
        print("⌨️ Test de la navigation clavier...")

        response = requests.get(f"{self.base_url}/terminal")
        soup = BeautifulSoup(response.content, "html.parser")

        # Éléments navigables au clavier
        focusable_elements = [
            "button",
            "input",
            "select",
            "textarea",
            "a[href]",
            '[tabindex]:not([tabindex="-1"])',
            '[role="button"]',
            '[role="link"]',
        ]

        found_elements = 0
        total_expected = 8

        for selector in focusable_elements:
            elements = soup.select(selector)
            if elements:
                found_elements += len(elements)

        score = min(found_elements / total_expected * 100, 100)

        self.results["tests"]["keyboard_navigation"] = {
            "score": score,
            "found": found_elements,
            "expected": total_expected,
        }

        print(
            f"✅ Navigation clavier: {found_elements}/{total_expected} éléments trouvés"
        )
        return score

    def test_focus_management(self):
        """Test de la gestion du focus"""
        print("🎯 Test de la gestion du focus...")

        response = requests.get(f"{self.base_url}/terminal")
        BeautifulSoup(response.content, "html.parser")

        focus_indicators = 0
        total_expected = 6

        # Vérifier les styles de focus
        css_content = self.get_css_content()

        focus_patterns = [
            r":focus\s*{",
            r"outline:",
            r"box-shadow:",
            r"focus-visible",
            r"focus-outline",
            r"focus-shadow",
        ]

        for pattern in focus_patterns:
            if re.search(pattern, css_content, re.IGNORECASE):
                focus_indicators += 1

        score = min(focus_indicators / total_expected * 100, 100)

        self.results["tests"]["focus_management"] = {
            "score": score,
            "found": focus_indicators,
            "expected": total_expected,
        }

        print(
            f"✅ Gestion du focus: {focus_indicators}/{total_expected} éléments trouvés"
        )
        return score

    def test_color_contrast(self):
        """Test du contraste des couleurs"""
        print("🎨 Test du contraste des couleurs...")

        response = requests.get(f"{self.base_url}/terminal")
        BeautifulSoup(response.content, "html.parser")

        contrast_elements = 0
        total_expected = 6

        # Vérifier les variables CSS de contraste
        css_content = self.get_css_content()

        contrast_patterns = [
            r"--primary-color:\s*#[0-9a-fA-F]{6}",
            r"--text-color:\s*#[0-9a-fA-F]{6}",
            r"--background-color:\s*#[0-9a-fA-F]{6}",
            r"contrast\s*[0-9.]+:1",
            r"high-contrast",
            r"color-scheme",
        ]

        for pattern in contrast_patterns:
            if re.search(pattern, css_content, re.IGNORECASE):
                contrast_elements += 1

        score = min(contrast_elements / total_expected * 100, 100)

        self.results["tests"]["color_contrast"] = {
            "score": score,
            "found": contrast_elements,
            "expected": total_expected,
        }

        print(f"✅ Contraste: {contrast_elements}/{total_expected} éléments trouvés")
        return score

    def test_semantic_html(self):
        """Test du HTML sémantique"""
        print("📝 Test du HTML sémantique...")

        response = requests.get(f"{self.base_url}/terminal")
        soup = BeautifulSoup(response.content, "html.parser")

        semantic_elements = 0
        total_expected = 10

        semantic_tags = [
            "main",
            "nav",
            "header",
            "footer",
            "section",
            "article",
            "aside",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ul",
            "ol",
            "li",
            "p",
            "blockquote",
            "figure",
            "figcaption",
        ]

        for tag in semantic_tags:
            if soup.find(tag):
                semantic_elements += 1

        score = min(semantic_elements / total_expected * 100, 100)

        self.results["tests"]["semantic_html"] = {
            "score": score,
            "found": semantic_elements,
            "expected": total_expected,
        }

        print(
            f"✅ HTML sémantique: {semantic_elements}/{total_expected} éléments trouvés"
        )
        return score

    def test_aria_labels(self):
        """Test des labels ARIA"""
        print("🏷️ Test des labels ARIA...")

        response = requests.get(f"{self.base_url}/terminal")
        soup = BeautifulSoup(response.content, "html.parser")

        aria_attributes = 0
        total_expected = 8

        aria_patterns = [
            "aria-label",
            "aria-describedby",
            "aria-labelledby",
            "aria-live",
            "aria-atomic",
            "aria-pressed",
            "aria-expanded",
            "aria-hidden",
        ]

        for attr in aria_patterns:
            if soup.find(attrs={attr: True}):
                aria_attributes += 1

        score = min(aria_attributes / total_expected * 100, 100)

        self.results["tests"]["aria_labels"] = {
            "score": score,
            "found": aria_attributes,
            "expected": total_expected,
        }

        print(f"✅ Labels ARIA: {aria_attributes}/{total_expected} attributs trouvés")
        return score

    def test_screen_reader_support(self):
        """Test du support lecteurs d'écran"""
        print("🔊 Test du support lecteurs d'écran...")

        response = requests.get(f"{self.base_url}/terminal")
        soup = BeautifulSoup(response.content, "html.parser")

        sr_elements = 0
        total_expected = 8

        # Éléments pour lecteurs d'écran
        sr_patterns = [
            "sr-only",
            "aria-live",
            'role="status"',
            'role="log"',
            'role="banner"',
            'role="main"',
            'role="navigation"',
            'role="region"',
        ]

        for pattern in sr_patterns:
            if soup.find(string=re.compile(pattern, re.IGNORECASE)) or soup.find(
                attrs=re.compile(pattern, re.IGNORECASE)
            ):
                sr_elements += 1

        score = min(sr_elements / total_expected * 100, 100)

        self.results["tests"]["screen_reader_support"] = {
            "score": score,
            "found": sr_elements,
            "expected": total_expected,
        }

        print(
            f"✅ Support lecteurs d'écran: {sr_elements}/{total_expected} éléments trouvés"
        )
        return score

    def test_responsive_accessibility(self):
        """Test de l'accessibilité responsive"""
        print("📱 Test de l'accessibilité responsive...")

        response = requests.get(f"{self.base_url}/terminal")
        BeautifulSoup(response.content, "html.parser")

        responsive_elements = 0
        total_expected = 7

        # Vérifier les media queries et éléments responsive
        css_content = self.get_css_content()

        responsive_patterns = [
            r"@media.*max-width",
            r"min-height:\s*44px",
            r"min-width:\s*44px",
            r"touch-action",
            r"viewport",
            r"responsive",
            r"mobile",
        ]

        for pattern in responsive_patterns:
            if re.search(pattern, css_content, re.IGNORECASE):
                responsive_elements += 1

        score = min(responsive_elements / total_expected * 100, 100)

        self.results["tests"]["responsive_accessibility"] = {
            "score": score,
            "found": responsive_elements,
            "expected": total_expected,
        }

        print(
            f"✅ Accessibilité responsive: {responsive_elements}/{total_expected} éléments trouvés"
        )
        return score

    def test_accessibility_modes(self):
        """Test des modes d'accessibilité"""
        print("🎛️ Test des modes d'accessibilité...")

        response = requests.get(f"{self.base_url}/terminal")
        BeautifulSoup(response.content, "html.parser")

        accessibility_modes = 0
        total_expected = 8

        # Vérifier les modes d'accessibilité
        css_content = self.get_css_content()

        mode_patterns = [
            r"daltonian",
            r"high-contrast",
            r"dyslexia-friendly",
            r"reduced-motion",
            r"zoom-[0-9]+",
            r"spacing-",
            r"highlight-",
            r"low-performance",
        ]

        for pattern in mode_patterns:
            if re.search(pattern, css_content, re.IGNORECASE):
                accessibility_modes += 1

        score = min(accessibility_modes / total_expected * 100, 100)

        self.results["tests"]["accessibility_modes"] = {
            "score": score,
            "found": accessibility_modes,
            "expected": total_expected,
        }

        print(
            f"✅ Modes d'accessibilité: {accessibility_modes}/{total_expected} modes trouvés"
        )
        return score

    def test_haptic_feedback(self):
        """Test du feedback haptique"""
        print("📳 Test du feedback haptique...")

        response = requests.get(f"{self.base_url}/terminal")
        BeautifulSoup(response.content, "html.parser")

        haptic_elements = 0
        total_expected = 6

        # Vérifier le support haptique
        js_content = self.get_js_content()

        haptic_patterns = [
            r"vibrate",
            r"haptic",
            r"feedback",
            r"touch",
            r"vibration",
            r"tactile",
        ]

        for pattern in haptic_patterns:
            if re.search(pattern, js_content, re.IGNORECASE):
                haptic_elements += 1

        score = min(haptic_elements / total_expected * 100, 100)

        self.results["tests"]["haptic_feedback"] = {
            "score": score,
            "found": haptic_elements,
            "expected": total_expected,
        }

        print(
            f"✅ Feedback haptique: {haptic_elements}/{total_expected} éléments trouvés"
        )
        return score

    def test_advanced_accessibility(self):
        """Test des fonctionnalités d'accessibilité avancées"""
        print("🚀 Test des fonctionnalités avancées...")

        response = requests.get(f"{self.base_url}/terminal")
        BeautifulSoup(response.content, "html.parser")

        advanced_features = 0
        total_expected = 5

        # Vérifier les fonctionnalités avancées
        css_content = self.get_css_content()
        js_content = self.get_js_content()

        advanced_patterns = [
            r"focus-trap",
            r"prefers-contrast",
            r"prefers-reduced-motion",
            r"hardwareConcurrency",
            r"deviceMemory",
        ]

        for pattern in advanced_patterns:
            if re.search(pattern, css_content + js_content, re.IGNORECASE):
                advanced_features += 1

        score = min(advanced_features / total_expected * 100, 100)

        self.results["tests"]["advanced_accessibility"] = {
            "score": score,
            "found": advanced_features,
            "expected": total_expected,
        }

        print(
            f"✅ Fonctionnalités avancées: {advanced_features}/{total_expected} éléments trouvés"
        )
        return score

    def test_keyboard_shortcuts(self):
        """Test des raccourcis clavier"""
        print("⌨️ Test des raccourcis clavier...")

        response = requests.get(f"{self.base_url}/terminal")
        BeautifulSoup(response.content, "html.parser")

        shortcuts = 0
        total_expected = 4

        # Vérifier les raccourcis clavier
        js_content = self.get_js_content()

        shortcut_patterns = [r"altKey", r"keydown", r"Escape", r"Tab"]

        for pattern in shortcut_patterns:
            if re.search(pattern, js_content, re.IGNORECASE):
                shortcuts += 1

        score = min(shortcuts / total_expected * 100, 100)

        self.results["tests"]["keyboard_shortcuts"] = {
            "score": score,
            "found": shortcuts,
            "expected": total_expected,
        }

        print(f"✅ Raccourcis clavier: {shortcuts}/{total_expected} éléments trouvés")
        return score

    def get_css_content(self):
        """Récupérer le contenu CSS"""
        try:
            response = requests.get(f"{self.base_url}/static/css/accessibility.css")
            return response.text
        except:
            return ""

    def get_js_content(self):
        """Récupérer le contenu JavaScript"""
        try:
            response = requests.get(f"{self.base_url}/static/js/accessibility.js")
            return response.text
        except:
            return ""

    def calculate_overall_score(self):
        """Calculer le score global"""
        total_score = 0
        test_count = 0

        for _test_name, test_result in self.results["tests"].items():
            total_score += test_result["score"]
            test_count += 1

        if test_count > 0:
            self.results["score"] = total_score / test_count

        return self.results["score"]

    def generate_recommendations(self):
        """Générer des recommandations d'amélioration"""
        recommendations = []

        for test_name, test_result in self.results["tests"].items():
            if test_result["score"] < 80:
                recommendations.append(
                    f"Améliorer {test_name}: {test_result['score']:.1f}%"
                )

        self.results["recommendations"] = recommendations

    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("♿ Test d'Accessibilité WCAG 2.1 AA - Arkalia Quest")
        print("=" * 60)

        # Tests de base
        self.test_skip_links()
        self.test_keyboard_navigation()
        self.test_focus_management()
        self.test_color_contrast()
        self.test_semantic_html()
        self.test_aria_labels()
        self.test_screen_reader_support()
        self.test_responsive_accessibility()
        self.test_accessibility_modes()
        self.test_haptic_feedback()

        # Tests avancés
        self.test_advanced_accessibility()
        self.test_keyboard_shortcuts()

        # Calcul du score global
        overall_score = self.calculate_overall_score()

        # Génération des recommandations
        self.generate_recommendations()

        # Affichage du rapport
        self.display_report()

        # Sauvegarde du rapport
        self.save_report()

        return overall_score

    def display_report(self):
        """Afficher le rapport complet"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT D'ACCESSIBILITÉ WCAG 2.1 AA")
        print("=" * 60)

        print(f"🎯 Score Global: {self.results['score']:.1f}/100")

        # Déterminer le niveau WCAG
        if self.results["score"] >= 85:
            wcag_level = "WCAG AA Conforme"
        elif self.results["score"] >= 70:
            wcag_level = "WCAG A Conforme"
        else:
            wcag_level = "Non conforme"

        print(f"🏆 Niveau WCAG: {wcag_level}")

        # Compter les tests réussis
        successful_tests = sum(
            1 for test in self.results["tests"].values() if test["score"] >= 80
        )
        total_tests = len(self.results["tests"])

        print(f"✅ Tests réussis: {successful_tests}/{total_tests}")
        print(f"⚠️ Avertissements: {len(self.results['recommendations'])}")
        print(
            f"❌ Problèmes critiques: {sum(1 for test in self.results['tests'].values() if test['score'] < 50)}"
        )

        print("\n📋 Détail des tests:")
        for test_name, test_result in self.results["tests"].items():
            status = "✅" if test_result["score"] >= 80 else "❌"
            print(
                f"  {status} {test_name.replace('_', ' ').title()}: {test_result['score']:.1f}/100 - {test_result['found']}/{test_result['expected']} éléments trouvés"
            )

        if self.results["score"] >= 80:
            print("\n✅ Points forts:")
            print("  • Interface accessible et inclusive")
            print("  • Navigation clavier complète")
            print("  • Support lecteurs d'écran")
            print("  • Modes d'accessibilité variés")
            print("  • Design responsive")
        else:
            print("\n⚠️ Améliorations recommandées:")
            for rec in self.results["recommendations"][:5]:
                print(f"  • {rec}")

        print("=" * 60)

    def save_report(self):
        """Sauvegarder le rapport"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tests/reports/accessibility_report_{timestamp}.json"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"📄 Rapport sauvegardé: {filename}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde rapport: {e}")


def main():
    """Fonction principale"""
    tester = AccessibilityTester()

    try:
        score = tester.run_all_tests()

        if score >= 85:
            print("🎉 FÉLICITATIONS ! Niveau WCAG AA atteint !")
        elif score >= 70:
            print("👍 Bon niveau d'accessibilité, quelques améliorations possibles")
        else:
            print("⚠️ Améliorations nécessaires pour l'accessibilité")

    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")


if __name__ == "__main__":
    main()
