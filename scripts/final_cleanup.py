#!/usr/bin/env python3
"""
Script de nettoyage final pour Arkalia Quest
Supprime tous les fichiers cachés et optimise le projet
"""

import os
import subprocess
import sys


def cleanup_hidden_files():
    """Supprime tous les fichiers cachés macOS"""
    print("🧹 Nettoyage des fichiers cachés...")
    
    # Supprimer les fichiers ._*
    result = subprocess.run(
        "find . -name '._*' -delete",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Fichiers cachés supprimés")
    else:
        print(f"⚠️ Erreur suppression fichiers cachés: {result.stderr}")


def cleanup_pycache():
    """Supprime les dossiers __pycache__"""
    print("🧹 Nettoyage des __pycache__...")
    
    result = subprocess.run(
        "find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true",
        shell=True,
        capture_output=True,
        text=True
    )
    
    print("✅ Dossiers __pycache__ supprimés")


def cleanup_logs():
    """Nettoie les logs anciens"""
    print("🧹 Nettoyage des logs...")
    
    log_files = [
        "logs/arkalia.log",
        "logs/error.log", 
        "logs/security.log"
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            # Garder seulement les 1000 dernières lignes
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                if len(lines) > 1000:
                    with open(log_file, 'w', encoding='utf-8') as f:
                        f.writelines(lines[-1000:])
                    print(f"✅ {log_file} nettoyé ({len(lines)} → 1000 lignes)")
                else:
                    print(f"✅ {log_file} déjà optimisé")
            except Exception as e:
                print(f"⚠️ Erreur nettoyage {log_file}: {e}")


def verify_integration():
    """Vérifie que tous les modules sont intégrés"""
    print("🔍 Vérification de l'intégration...")
    
    try:
        # Tester l'import de l'app
        sys.path.append('.')
        from app import app
        
        # Tester quelques modules clés
        modules_to_test = [
            'database_optimizer',
            'luna_emotions_engine', 
            'mission_handler',
            'profile_manager',
            'effects_engine'
        ]
        
        for module in modules_to_test:
            if hasattr(app, module):
                print(f"✅ {module} intégré")
            else:
                print(f"❌ {module} manquant")
        
        print("✅ Vérification terminée")
        
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")


def main():
    """Fonction principale"""
    print("🚀 NETTOYAGE FINAL ARKALIA QUEST")
    print("=" * 50)
    
    cleanup_hidden_files()
    cleanup_pycache()
    cleanup_logs()
    verify_integration()
    
    print("\n🎉 Nettoyage final terminé!")
    print("✨ Projet optimisé et prêt pour la production")


if __name__ == "__main__":
    main()
