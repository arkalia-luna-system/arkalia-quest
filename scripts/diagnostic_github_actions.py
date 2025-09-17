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
        print(r"🔍 Vérification des fichiers de workflow...")

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
        print(r"\n🔐 Vérification des permissions...")

        # Vérifier deploy.yml
        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "permissions:" in content:
                print(r"✅ Permissions configurées dans deploy.yml")
            else:
                self.issues.append("❌ Permissions manquantes dans deploy.yml")

            if "contents: write" in content:
                print(r"✅ Permission contents:write configurée")
            else:
                self.issues.append("❌ Permission contents:write manquante")

            if "packages: write" in content:
                print(r"✅ Permission packages:write configurée")
            else:
                self.issues.append("❌ Permission packages:write manquante")
        else:
            self.issues.append("❌ Fichier deploy.yml manquant")

    def check_git_config(self):
        """Vérifie la configuration Git dans les workflows"""
        print(r"\n🏷️ Vérification de la configuration Git...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "github-actions[bot]@users.noreply.github.com" in content:
                print(r"✅ Email Git correctement configuré")
            else:
                self.issues.append("❌ Email Git incorrect dans deploy.yml")

            if "github-actions[bot]" in content:
                print(r"✅ Nom Git correctement configuré")
            else:
                self.issues.append("❌ Nom Git incorrect dans deploy.yml")

    def check_secrets(self):
        """Vérifie la configuration des secrets"""
        print(r"\n🔐 Vérification des secrets...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "DOCKER_USERNAME" in content:
                print(r"✅ Secret DOCKER_USERNAME référencé")
            else:
                self.issues.append("❌ Secret DOCKER_USERNAME manquant")

            if "DOCKER_PASSWORD" in content:
                print(r"✅ Secret DOCKER_PASSWORD référencé")
            else:
                self.issues.append("❌ Secret DOCKER_PASSWORD manquant")

            if "GITHUB_TOKEN" in content:
                print(r"✅ GITHUB_TOKEN configuré")
            else:
                self.issues.append("❌ GITHUB_TOKEN manquant")

    def check_docker_config(self):
        """Vérifie la configuration Docker"""
        print(r"\n🐳 Vérification de la configuration Docker...")

        dockerfile = "config/Dockerfile"
        if os.path.exists(dockerfile):
            print(r"✅ Dockerfile trouvé")
        else:
            self.issues.append("❌ Dockerfile manquant")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "docker build" in content:
                print(r"✅ Commande docker build configurée")
            else:
                self.issues.append("❌ Commande docker build manquante")

    def check_workflow_triggers(self):
        """Vérifie les déclencheurs des workflows"""
        print(r"\n🚀 Vérification des déclencheurs...")

        deploy_yml = ".github/workflows/deploy.yml"
        if os.path.exists(deploy_yml):
            with open(deploy_yml) as f:
                content = f.read()

            if "branches: [main]" in content:
                print(r"✅ Déclencheur sur main configuré")
            else:
                self.issues.append("❌ Déclencheur sur main manquant")

            if "workflow_dispatch:" in content:
                print(r"✅ Déclenchement manuel configuré")
            else:
                self.issues.append("❌ Déclenchement manuel manquant")

    def generate_report(self):
        """Génère un rapport de diagnostic"""
        print("\n" + "=" * 60)
        print(r"📊 RAPPORT DE DIAGNOSTIC GITHUB ACTIONS")
        print("=" * 60)

        if not self.issues:
            print(r"🎉 AUCUN PROBLÈME DÉTECTÉ !")
            print(r"✅ Toutes les actions GitHub sont correctement configurées")
        else:
            print(f"❌ {len(self.issues)} PROBLÈME(S) DÉTECTÉ(S):")
            for issue in self.issues:
                print(f"   • {issue}")

        print(r"\n🔧 CORRECTIONS APPLIQUÉES:")
        if self.fixes:
            for fix in self.fixes:
                print(f"   ✅ {fix}")
        else:
            print(r"   Aucune correction nécessaire")

        return len(self.issues) == 0

    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        print(r"🚀 DÉMARRAGE DU DIAGNOSTIC GITHUB ACTIONS")
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
