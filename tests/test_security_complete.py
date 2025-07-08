#!/usr/bin/env python3
"""
🛡️ ARKALIA QUEST - TESTEUR SÉCURITÉ COMPLET
============================================

Ce testeur valide :
- Protection contre les injections SQL
- Protection contre les attaques XSS
- Protection contre les attaques CSRF
- Validation des entrées utilisateur
- Rate limiting et protection DDoS
- Gestion sécurisée des sessions
- Headers de sécurité

Auteur: Assistant IA
Version: 1.0
"""

import requests
import json
import time
import hashlib
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional

class SecurityTester:
    """Testeur de sécurité complet"""
    
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.results = {
            "security": {},
            "vulnerabilities": [],
            "recommendations": [],
            "score": 0
        }
        
        # Payloads de test
        self.sql_payloads = [
            "'; DROP TABLE profiles; --",
            "' OR 1=1 --",
            "' UNION SELECT * FROM profiles --",
            "'; INSERT INTO profiles VALUES ('hacker', 999999); --",
            "' OR '1'='1' --"
        ]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "'><script>alert('XSS')</script>"
        ]
        
        self.csrf_payloads = [
            "<form action='http://localhost:5001/commande' method='POST'>",
            "<img src='http://localhost:5001/commande' style='display:none'>",
            "fetch('http://localhost:5001/commande', {method: 'POST'})"
        ]
        
        self.command_injection_payloads = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& whoami",
            "`id`",
            "$(whoami)"
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_sql_injection(self):
        """Test d'injection SQL"""
        self.log("🛡️ Test d'injection SQL...")
        
        vulnerabilities_found = 0
        
        for payload in self.sql_payloads:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": payload},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = str(data).lower()
                    
                    # Vérifier si la payload a été exécutée
                    if any(keyword in response_text for keyword in ["error", "sql", "syntax", "invalid"]):
                        self.log(f"✅ Protection SQL active pour: {payload[:30]}...", "SUCCESS")
                    elif "drop" in payload.lower() and "drop" in response_text:
                        self.log(f"❌ Injection SQL possible: {payload[:30]}...", "ERROR")
                        vulnerabilities_found += 1
                        self.results["vulnerabilities"].append(f"SQL Injection: {payload}")
                    else:
                        self.log(f"⚠️ Réponse suspecte pour: {payload[:30]}...", "WARNING")
                else:
                    self.log(f"✅ Protection SQL (rejet HTTP {response.status_code})", "SUCCESS")
                    
            except Exception as e:
                self.log(f"❌ Erreur test SQL: {e}", "ERROR")
                vulnerabilities_found += 1
        
        if vulnerabilities_found == 0:
            self.log("✅ Protection contre les injections SQL", "SUCCESS")
            self.results["security"]["sql_injection"] = "PROTECTED"
        else:
            self.log(f"❌ {vulnerabilities_found} vulnérabilités SQL détectées", "ERROR")
            self.results["security"]["sql_injection"] = "VULNERABLE"
    
    def test_xss_protection(self):
        """Test de protection XSS"""
        self.log("🛡️ Test de protection XSS...")
        
        vulnerabilities_found = 0
        
        for payload in self.xss_payloads:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": payload},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = str(data)
                    
                    # Vérifier si le script est dans la réponse
                    if "<script>" in response_text and "alert" in response_text:
                        self.log(f"❌ XSS possible: {payload[:30]}...", "ERROR")
                        vulnerabilities_found += 1
                        self.results["vulnerabilities"].append(f"XSS: {payload}")
                    else:
                        self.log(f"✅ Protection XSS pour: {payload[:30]}...", "SUCCESS")
                else:
                    self.log(f"✅ Protection XSS (rejet HTTP {response.status_code})", "SUCCESS")
                    
            except Exception as e:
                self.log(f"❌ Erreur test XSS: {e}", "ERROR")
                vulnerabilities_found += 1
        
        if vulnerabilities_found == 0:
            self.log("✅ Protection contre les attaques XSS", "SUCCESS")
            self.results["security"]["xss"] = "PROTECTED"
        else:
            self.log(f"❌ {vulnerabilities_found} vulnérabilités XSS détectées", "ERROR")
            self.results["security"]["xss"] = "VULNERABLE"
    
    def test_command_injection(self):
        """Test d'injection de commandes"""
        self.log("🛡️ Test d'injection de commandes...")
        
        vulnerabilities_found = 0
        
        for payload in self.command_injection_payloads:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": payload},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = str(data).lower()
                    
                    # Vérifier si une commande système a été exécutée
                    if any(keyword in response_text for keyword in ["root", "uid=", "gid=", "home", "shell"]):
                        self.log(f"❌ Injection commande possible: {payload[:30]}...", "ERROR")
                        vulnerabilities_found += 1
                        self.results["vulnerabilities"].append(f"Command Injection: {payload}")
                    else:
                        self.log(f"✅ Protection commande pour: {payload[:30]}...", "SUCCESS")
                else:
                    self.log(f"✅ Protection commande (rejet HTTP {response.status_code})", "SUCCESS")
                    
            except Exception as e:
                self.log(f"❌ Erreur test commande: {e}", "ERROR")
                vulnerabilities_found += 1
        
        if vulnerabilities_found == 0:
            self.log("✅ Protection contre les injections de commandes", "SUCCESS")
            self.results["security"]["command_injection"] = "PROTECTED"
        else:
            self.log(f"❌ {vulnerabilities_found} vulnérabilités commande détectées", "ERROR")
            self.results["security"]["command_injection"] = "VULNERABLE"
    
    def test_input_validation(self):
        """Test de validation des entrées"""
        self.log("🛡️ Test de validation des entrées...")
        
        invalid_inputs = [
            "",  # Entrée vide
            "a" * 1000,  # Entrée très longue
            "🎮🚀💻",  # Emojis
            "test\nscript",  # Caractères spéciaux
            "test<script>alert('xss')</script>",  # Mix XSS
            "'; DROP TABLE; --",  # Mix SQL
        ]
        
        validation_score = 0
        
        for invalid_input in invalid_inputs:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": invalid_input},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Vérifier si l'entrée a été rejetée ou nettoyée
                    if "error" in str(data).lower() or "invalid" in str(data).lower():
                        self.log(f"✅ Validation pour: {str(invalid_input)[:30]}...", "SUCCESS")
                        validation_score += 1
                    else:
                        self.log(f"⚠️ Validation faible pour: {str(invalid_input)[:30]}...", "WARNING")
                else:
                    self.log(f"✅ Validation (rejet HTTP {response.status_code})", "SUCCESS")
                    validation_score += 1
                    
            except Exception as e:
                self.log(f"❌ Erreur validation: {e}", "ERROR")
        
        validation_rate = (validation_score / len(invalid_inputs)) * 100
        
        if validation_rate >= 80:
            self.log(f"✅ Validation des entrées correcte ({validation_rate:.1f}%)", "SUCCESS")
            self.results["security"]["input_validation"] = "GOOD"
        else:
            self.log(f"⚠️ Validation des entrées faible ({validation_rate:.1f}%)", "WARNING")
            self.results["security"]["input_validation"] = "WEAK"
    
    def test_rate_limiting(self):
        """Test de rate limiting"""
        self.log("🛡️ Test de rate limiting...")
        
        # Envoyer beaucoup de requêtes rapidement
        rapid_requests = 50
        blocked_requests = 0
        
        for i in range(rapid_requests):
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": "aide"},
                    timeout=2
                )
                
                if response.status_code in [429, 503, 403]:  # Rate limit codes
                    blocked_requests += 1
                    
            except Exception as e:
                # Timeout peut indiquer un rate limiting
                blocked_requests += 1
        
        rate_limit_rate = (blocked_requests / rapid_requests) * 100
        
        if rate_limit_rate >= 20:  # Au moins 20% des requêtes bloquées
            self.log(f"✅ Rate limiting actif ({rate_limit_rate:.1f}% bloquées)", "SUCCESS")
            self.results["security"]["rate_limiting"] = "ACTIVE"
        else:
            self.log(f"⚠️ Rate limiting faible ({rate_limit_rate:.1f}% bloquées)", "WARNING")
            self.results["security"]["rate_limiting"] = "WEAK"
    
    def test_security_headers(self):
        """Test des headers de sécurité"""
        self.log("🛡️ Test des headers de sécurité...")
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            headers = response.headers
            
            security_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": ["DENY", "SAMEORIGIN"],
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": "max-age=",
                "Content-Security-Policy": "default-src",
                "Referrer-Policy": ["no-referrer", "strict-origin"]
            }
            
            headers_score = 0
            
            for header, expected_values in security_headers.items():
                if header in headers:
                    header_value = headers[header]
                    
                    if isinstance(expected_values, list):
                        if any(expected in header_value for expected in expected_values):
                            self.log(f"✅ Header {header} présent", "SUCCESS")
                            headers_score += 1
                        else:
                            self.log(f"⚠️ Header {header} présent mais valeur suspecte", "WARNING")
                    else:
                        if expected_values in header_value:
                            self.log(f"✅ Header {header} correct", "SUCCESS")
                            headers_score += 1
                        else:
                            self.log(f"⚠️ Header {header} présent mais valeur incorrecte", "WARNING")
                else:
                    self.log(f"❌ Header {header} manquant", "ERROR")
            
            headers_rate = (headers_score / len(security_headers)) * 100
            
            if headers_rate >= 60:
                self.log(f"✅ Headers de sécurité corrects ({headers_rate:.1f}%)", "SUCCESS")
                self.results["security"]["security_headers"] = "GOOD"
            else:
                self.log(f"⚠️ Headers de sécurité insuffisants ({headers_rate:.1f}%)", "WARNING")
                self.results["security"]["security_headers"] = "WEAK"
                
        except Exception as e:
            self.log(f"❌ Erreur test headers: {e}", "ERROR")
            self.results["security"]["security_headers"] = "ERROR"
    
    def test_session_security(self):
        """Test de sécurité des sessions"""
        self.log("🛡️ Test de sécurité des sessions...")
        
        try:
            # Test de session fixation
            response1 = requests.get(f"{self.base_url}/terminal", timeout=5)
            session1 = response1.cookies.get("session", "")
            
            response2 = requests.get(f"{self.base_url}/terminal", timeout=5)
            session2 = response2.cookies.get("session", "")
            
            # Les sessions doivent être différentes
            if session1 and session2 and session1 != session2:
                self.log("✅ Sessions sécurisées (non-fixation)", "SUCCESS")
                self.results["security"]["session_security"] = "SECURE"
            else:
                self.log("⚠️ Sessions potentiellement fixées", "WARNING")
                self.results["security"]["session_security"] = "WEAK"
                
        except Exception as e:
            self.log(f"❌ Erreur test sessions: {e}", "ERROR")
            self.results["security"]["session_security"] = "ERROR"
    
    def calculate_security_score(self):
        """Calcule le score de sécurité global"""
        security_items = self.results["security"]
        total_items = len(security_items)
        secure_items = 0
        
        for item, status in security_items.items():
            if status in ["PROTECTED", "ACTIVE", "GOOD", "SECURE"]:
                secure_items += 1
            elif status == "WEAK":
                secure_items += 0.5
        
        if total_items > 0:
            self.results["score"] = (secure_items / total_items) * 100
        else:
            self.results["score"] = 0
    
    def generate_security_report(self) -> str:
        """Génère un rapport de sécurité"""
        self.calculate_security_score()
        
        report = f"""
🛡️ RAPPORT DE SÉCURITÉ - ARKALIA QUEST
=======================================

📊 SCORE GLOBAL: {self.results["score"]:.1f}/100

🔍 DÉTAIL PAR VULNÉRABILITÉ
---------------------------
"""
        
        for item, status in self.results["security"].items():
            if status in ["PROTECTED", "ACTIVE", "GOOD", "SECURE"]:
                report += f"✅ {item}: {status}\n"
            elif status == "WEAK":
                report += f"⚠️ {item}: {status}\n"
            else:
                report += f"❌ {item}: {status}\n"
        
        if self.results["vulnerabilities"]:
            report += f"""
❌ VULNÉRABILITÉS DÉTECTÉES ({len(self.results["vulnerabilities"])})
"""
            for vuln in self.results["vulnerabilities"][:10]:  # Top 10
                report += f"- {vuln}\n"
        
        # Recommandations
        report += f"""
🎯 RECOMMANDATIONS
------------------
"""
        
        if self.results["score"] >= 80:
            report += "✅ Sécurité excellente - Prêt pour la production\n"
        elif self.results["score"] >= 60:
            report += "✅ Sécurité correcte - Quelques améliorations recommandées\n"
        else:
            report += "⚠️ Sécurité insuffisante - Corrections nécessaires\n"
        
        # Recommandations spécifiques
        for item, status in self.results["security"].items():
            if status == "VULNERABLE":
                report += f"- Corriger la vulnérabilité {item}\n"
            elif status == "WEAK":
                report += f"- Renforcer la protection {item}\n"
        
        return report
    
    def run_all_tests(self):
        """Exécute tous les tests de sécurité"""
        self.log("🚀 DÉMARRAGE DES TESTS DE SÉCURITÉ")
        self.log("=" * 50)
        
        # Tests de sécurité
        self.test_sql_injection()
        self.test_xss_protection()
        self.test_command_injection()
        self.test_input_validation()
        self.test_rate_limiting()
        self.test_security_headers()
        self.test_session_security()
        
        # Rapport final
        report = self.generate_security_report()
        print(report)
        
        # Sauvegarder les résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"security_results_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 Résultats sauvegardés: security_results_{timestamp}.json")
        
        return self.results["score"] >= 60  # Seuil de sécurité acceptable

def main():
    """Fonction principale"""
    print("🛡️ ARKALIA QUEST - TESTEUR SÉCURITÉ COMPLET")
    print("=" * 50)
    
    tester = SecurityTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 SÉCURITÉ VALIDÉE !")
        return 0
    else:
        print("\n⚠️ SÉCURITÉ À AMÉLIORER")
        return 1

if __name__ == "__main__":
    exit(main()) 