#!/usr/bin/env python3
"""
Script de diagnostic des actions GitHub Actions
Identifie et corrige les problèmes courants
"""

import os
import sys


class GitHubActionsDiagnostic:
    """Diagnostic des actions GitHub Actions"""

    def __init__(self):
        self.issues = []
        self.fixes = []

    def check_workflow_files(self):
        """Vérifie les fichiers de workflow"""
        game_logger.info(r"🔍 Vérification des fichiers de workflow...")

        workflows_dir = ".github/workflows"
        if not os.path.exists(workflows_dir):
            self.issues.append("❌ Répertoire .github/workflows manquant")
            return

        workflow_files = [f for f in os.listdir(workflows_dir) if f.endswith(".yml")]
        game_logger.info(f"✅ {len(workflow_files)} fichiers de workflow trouvés")

        for workflow in workflow_files:
            game_logger.info(f"   📋 {workflow}")

    def check_permissions_config(self):
        """Vérifie la configuration des permissions"""
        game_logger.info(r"\n🔐 Vérification des permissions...")

        # Vérifier deploy.yml
        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "permissions:" in content:
                game_logger.info(r"✅ Permissions configurées dans deploy.yml")
            else:
                self.issues.append("❌ Permissions manquantes dans deploy.yml")

            if "contents: write" in content:
                game_logger.info(r"✅ Permission contents:write configurée")
            else:
                self.issues.append("❌ Permission contents:write manquante")

            if "packages: write" in content:
                game_logger.info(r"✅ Permission packages:write configurée")
            else:
                self.issues.append("❌ Permission packages:write manquante")
        else:
            self.issues.append("❌ Fichier deploy.yml manquant")

    def check_git_config(self):
        """Vérifie la configuration Git dans les workflows"""
        game_logger.info(r"\n🏷️ Vérification de la configuration Git...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "github-actions[bot]@users.noreply.github.com" in content:
                game_logger.info(r"✅ Email Git correctement configuré")
            else:
                self.issues.append("❌ Email Git incorrect dans deploy.yml")

            if "github-actions[bot]" in content:
                game_logger.info(r"✅ Nom Git correctement configuré")
            else:
                self.issues.append("❌ Nom Git incorrect dans deploy.yml")

    def check_secrets(self):
        """Vérifie la configuration des secrets"""
        game_logger.info(r"\n🔐 Vérification des secrets...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "DOCKER_USERNAME" in content:
                game_logger.info(r"✅ Secret DOCKER_USERNAME référencé")
            else:
                self.issues.append("❌ Secret DOCKER_USERNAME manquant")

            if "DOCKER_PASSWORD" in content:
                game_logger.info(r"✅ Secret DOCKER_PASSWORD référencé")
            else:
                self.issues.append("❌ Secret DOCKER_PASSWORD manquant")

            if "GITHUB_TOKEN" in content:
                game_logger.info(r"✅ GITHUB_TOKEN configuré")
            else:
                self.issues.append("❌ GITHUB_TOKEN manquant")

    def check_docker_config(self):
        """Vérifie la configuration Docker"""
        game_logger.info(r"\n🐳 Vérification de la configuration Docker...")

        dockerfile = "config/Dockerfile"
        if os.path.exists(dockerfile):
            game_logger.info(r"✅ Dockerfile trouvé")
        else:
            self.issues.append("❌ Dockerfile manquant")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "docker build" in content:
                game_logger.info(r"✅ Commande docker build configurée")
            else:
                self.issues.append("❌ Commande docker build manquante")

    def check_workflow_triggers(self):
        """Vérifie les déclencheurs des workflows"""
        game_logger.info(r"\n🚀 Vérification des déclencheurs...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "branches: [main]" in content:
                game_logger.info(r"✅ Déclencheur sur main configuré")
            else:
                self.issues.append("❌ Déclencheur sur main manquant")

            if "workflow_dispatch:" in content:
                game_logger.info(r"✅ Déclenchement manuel configuré")
            else:
                self.issues.append("❌ Déclenchement manuel manquant")

    def generate_report(self):
        """Génère un rapport de diagnostic"""
        print("\n" + "=" * 60)
        game_logger.info(r"📊 RAPPORT DE DIAGNOSTIC GITHUB ACTIONS")
        print("=" * 60)

        if not self.issues:
            game_logger.info(r"🎉 AUCUN PROBLÈME DÉTECTÉ !")
            game_logger.info(
                r"✅ Toutes les actions GitHub sont correctement configurées"
            )
        else:
            game_logger.info(f"❌ {len(self.issues)} PROBLÈME(S) DÉTECTÉ(S):")
            for issue in self.issues:
                game_logger.info(f"   • {issue}")

        game_logger.info(r"\n🔧 CORRECTIONS APPLIQUÉES:")
        if self.fixes:
            for fix in self.fixes:
                game_logger.info(f"   ✅ {fix}")
        else:
            game_logger.info(r"   Aucune correction nécessaire")

        return len(self.issues) == 0

    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        game_logger.info(r"🚀 DÉMARRAGE DU DIAGNOSTIC GITHUB ACTIONS")
        print("=" * 60)

        self.check_workflow_files()
        self.check_permissions_config()
        self.check_git_config()
        self.check_secrets()
        self.check_docker_config()
        self.check_workflow_triggers()

        return self.generate_report()


def main():
    """Fonction principale"""
    diagnostic = GitHubActionsDiagnostic()

    try:
        success = diagnostic.run_full_diagnostic()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Diagnostic interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        game_logger.info(f"\n💥 Erreur lors du diagnostic: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
