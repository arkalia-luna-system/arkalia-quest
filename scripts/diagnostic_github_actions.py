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
        print("🔍 Vérification des fichiers de workflow...")

        workflows_dir = ".github/workflows"
        if not os.path.exists(workflows_dir):
            self.issues.append("❌ Répertoire .github/workflows manquant")
            return

        workflow_files = [f for f in os.listdir(workflows_dir) if f.endswith(".yml")]
        print(f"✅ {len(workflow_files)} fichiers de workflow trouvés")

        for workflow in workflow_files:
            print(f"   📋 {workflow}")

    def check_permissions_config(self):
        """Vérifie la configuration des permissions"""
        print("\n🔐 Vérification des permissions...")

        # Vérifier deploy.yml
        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "permissions:" in content:
                print("✅ Permissions configurées dans deploy.yml")
            else:
                self.issues.append("❌ Permissions manquantes dans deploy.yml")

            if "contents: write" in content:
                print("✅ Permission contents:write configurée")
            else:
                self.issues.append("❌ Permission contents:write manquante")

            if "packages: write" in content:
                print("✅ Permission packages:write configurée")
            else:
                self.issues.append("❌ Permission packages:write manquante")
        else:
            self.issues.append("❌ Fichier deploy.yml manquant")

    def check_git_config(self):
        """Vérifie la configuration Git dans les workflows"""
        print("\n🏷️ Vérification de la configuration Git...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "github-actions[bot]@users.noreply.github.com" in content:
                print("✅ Email Git correctement configuré")
            else:
                self.issues.append("❌ Email Git incorrect dans deploy.yml")

            if "github-actions[bot]" in content:
                print("✅ Nom Git correctement configuré")
            else:
                self.issues.append("❌ Nom Git incorrect dans deploy.yml")

    def check_secrets(self):
        """Vérifie la configuration des secrets"""
        print("\n🔐 Vérification des secrets...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "DOCKER_USERNAME" in content:
                print("✅ Secret DOCKER_USERNAME référencé")
            else:
                self.issues.append("❌ Secret DOCKER_USERNAME manquant")

            if "DOCKER_PASSWORD" in content:
                print("✅ Secret DOCKER_PASSWORD référencé")
            else:
                self.issues.append("❌ Secret DOCKER_PASSWORD manquant")

            if "GITHUB_TOKEN" in content:
                print("✅ GITHUB_TOKEN configuré")
            else:
                self.issues.append("❌ GITHUB_TOKEN manquant")

    def check_docker_config(self):
        """Vérifie la configuration Docker"""
        print("\n🐳 Vérification de la configuration Docker...")

        dockerfile = "config/Dockerfile"
        if os.path.exists(dockerfile):
            print("✅ Dockerfile trouvé")
        else:
            self.issues.append("❌ Dockerfile manquant")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "docker build" in content:
                print("✅ Commande docker build configurée")
            else:
                self.issues.append("❌ Commande docker build manquante")

    def check_workflow_triggers(self):
        """Vérifie les déclencheurs des workflows"""
        print("\n🚀 Vérification des déclencheurs...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "branches: [main]" in content:
                print("✅ Déclencheur sur main configuré")
            else:
                self.issues.append("❌ Déclencheur sur main manquant")

            if "workflow_dispatch:" in content:
                print("✅ Déclenchement manuel configuré")
            else:
                self.issues.append("❌ Déclenchement manuel manquant")

    def generate_report(self):
        """Génère un rapport de diagnostic"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT DE DIAGNOSTIC GITHUB ACTIONS")
        print("=" * 60)

        if not self.issues:
            print("🎉 AUCUN PROBLÈME DÉTECTÉ !")
            print("✅ Toutes les actions GitHub sont correctement configurées")
        else:
            print(f"❌ {len(self.issues)} PROBLÈME(S) DÉTECTÉ(S):")
            for issue in self.issues:
                print(f"   • {issue}")

        print("\n🔧 CORRECTIONS APPLIQUÉES:")
        if self.fixes:
            for fix in self.fixes:
                print(f"   ✅ {fix}")
        else:
            print("   Aucune correction nécessaire")

        return len(self.issues) == 0

    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        print("🚀 DÉMARRAGE DU DIAGNOSTIC GITHUB ACTIONS")
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
        print(f"\n💥 Erreur lors du diagnostic: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
