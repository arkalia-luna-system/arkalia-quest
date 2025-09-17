#!/usr/bin/env python3
"""
Script de nettoyage des logs pour Arkalia Quest
Supprime les logs anciens et optimise les fichiers de log
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def cleanup_logs():
    """Nettoie les logs anciens et optimise les fichiers"""
    logs_dir = Path("logs")

    if not logs_dir.exists():
        print("❌ Dossier logs introuvable")
        return

    print("🧹 Nettoyage des logs en cours...")

    # Sauvegarder les logs actuels
    backup_dir = logs_dir / "backup"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Fichiers de log à nettoyer
    log_files = ["arkalia.log", "error.log", "security.log"]

    for log_file in log_files:
        log_path = logs_dir / log_file
        if log_path.exists():
            # Sauvegarder
            backup_path = backup_dir / f"{log_file}.{timestamp}"
            shutil.copy2(log_path, backup_path)
            print(f"📁 Sauvegardé: {log_file} -> {backup_path}")

            # Nettoyer le fichier (garder seulement les 1000 dernières lignes)
            try:
                with open(log_path, encoding="utf-8") as f:
                    lines = f.readlines()

                if len(lines) > 1000:
                    # Garder les 1000 dernières lignes
                    with open(log_path, "w", encoding="utf-8") as f:
                        f.writelines(lines[-1000:])
                    print(f"✂️  Tronqué: {log_file} (gardé 1000 dernières lignes)")
                else:
                    print(f"✅ OK: {log_file} (taille acceptable)")

            except Exception as e:
                print(f"❌ Erreur lors du nettoyage de {log_file}: {e}")

    # Nettoyer les anciennes sauvegardes (plus de 7 jours)
    cutoff_date = datetime.now() - timedelta(days=7)
    for backup_file in backup_dir.glob("*.log.*"):
        try:
            file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            if file_time < cutoff_date:
                backup_file.unlink()
                print(f"🗑️  Supprimé ancienne sauvegarde: {backup_file.name}")
        except Exception as e:
            print(f"❌ Erreur suppression {backup_file}: {e}")

    print("✅ Nettoyage terminé!")


if __name__ == "__main__":
    cleanup_logs()
