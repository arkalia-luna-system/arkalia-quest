#!/usr/bin/env python3
"""
Script de test pour vérifier l'optimisation du système de sécurité
"""

import os
import sys
import time

# Ajouter le chemin du projet
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Changer le répertoire de travail
os.chdir(project_root)

# Import après configuration du path
from core.security_manager import SecurityManager  # noqa: E402


def test_security_deduplication():
    """Test la déduplication des alertes de sécurité"""
    print(r"🔒 Test du système de sécurité optimisé...")

    security_manager = SecurityManager()

    # Test 1: Première tentative XSS
    print(r"\n1️⃣ Première tentative XSS...")
    result1 = security_manager.check_input_security(
        "<script>alert(1)</script>", "1.2.3.4"
    )
    print(f"   Résultat: {result1}")

    # Test 2: Même tentative XSS (devrait être dédupliquée)
    print(r"\n2️⃣ Même tentative XSS (déduplication)...")
    result2 = security_manager.check_input_security(
        "<script>alert(1)</script>", "1.2.3.4"
    )
    print(f"   Résultat: {result2}")
    print(f"   Duplicate détecté: {result2.get('duplicate_detected', False)}")

    # Test 3: Tentative différente
    print(r"\n3️⃣ Tentative XSS différente...")
    result3 = security_manager.check_input_security(
        "<script>alert(2)</script>", "1.2.3.4"
    )
    print(f"   Résultat: {result3}")

    # Test 4: Même IP, input différent
    print(r"\n4️⃣ Même IP, input différent...")
    result4 = security_manager.check_input_security("javascript:void(0)", "1.2.3.4")
    print(f"   Résultat: {result4}")

    # Test 5: IP différente, même input
    print(r"\n5️⃣ IP différente, même input...")
    result5 = security_manager.check_input_security(
        "<script>alert(1)</script>", "5.6.7.8"
    )
    print(f"   Résultat: {result5}")

    # Attendre et retester (déduplication expirée)
    print(r"\n6️⃣ Test après expiration de la déduplication...")
    print(r"   Attente de 2 secondes...")
    time.sleep(2)

    # Modifier le seuil de déduplication pour le test
    security_manager.duplicate_threshold = 1  # 1 seconde pour le test

    result6 = security_manager.check_input_security(
        "<script>alert(1)</script>", "1.2.3.4"
    )
    print(f"   Résultat: {result6}")

    print(
        f"\n📊 Nombre d'événements de sécurité: {len(security_manager.security_events)}"
    )
    print(f"📊 Événements en cache: {len(security_manager.recent_events)}")

    print(r"\n✅ Test terminé!")


if __name__ == "__main__":
    test_security_deduplication()
