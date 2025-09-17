#!/usr/bin/env python3
"""
Script principal de configuration de la contribution GitHub pour Arkalia Quest
Configure automatiquement tous les éléments nécessaires pour une contribution optimale
"""

import os
import subprocess
import sys
from pathlib import Path


class GitHubContributionSetup:
    """Configuration complète de la contribution GitHub pour Arkalia Quest"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"

    def print_header(self, title: str):
        """Affiche un en-tête stylisé"""
        print("\n" + "=" * 60)
        game_logger.info(f"🎮 {title}")
        print("=" * 60)

    def check_environment(self) -> bool:
        """Vérifie l'environnement de développement"""
        self.print_header("Vérification de l'environnement")

        # Vérification du venv
        if not os.environ.get("VIRTUAL_ENV"):
            game_logger.info(r"❌ Environnement virtuel non activé")
            game_logger.info(r"💡 Activez le venv : source venv/bin/activate")
            return False

        game_logger.info(r"✅ Environnement virtuel activé")

        # Vérification de Python
        try:
            result = subprocess.run(
                ["python", "--version"], check=False, capture_output=True, text=True
            )
            game_logger.info(f"✅ Python: {result.stdout.strip()}")
        except Exception as e:
            game_logger.info(f"❌ Erreur Python: {e}")
            return False

        # Vérification de Git
        try:
            result = subprocess.run(
                ["git", "--version"], check=False, capture_output=True, text=True
            )
            game_logger.info(f"✅ Git: {result.stdout.strip()}")
        except Exception as e:
            game_logger.info(f"❌ Erreur Git: {e}")
            return False

        # Vérification du token GitHub
        if not os.environ.get("GITHUB_TOKEN"):
            game_logger.info(r"⚠️  GITHUB_TOKEN non défini")
            game_logger.info(r"💡 Définissez votre token GitHub :")
            game_logger.info(r"   export GITHUB_TOKEN=your_token_here")
            game_logger.info(
                r"   ou créez un fichier .env avec GITHUB_TOKEN=your_token_here"
            )
            return False

        game_logger.info(r"✅ GITHUB_TOKEN défini")
        return True

    def run_code_quality_checks(self) -> bool:
        """Exécute les vérifications de qualité du code"""
        self.print_header("Vérification de la qualité du code")

        try:
            # Black
            game_logger.info(r"🎨 Vérification Black...")
            result = subprocess.run(
                ["black", "--check", "."], check=False, capture_output=True, text=True
            )
            if result.returncode != 0:
                game_logger.info(r"❌ Black a trouvé des problèmes de formatage")
                game_logger.info(r"💡 Exécutez: black .")
                return False
            game_logger.info(r"✅ Black: Code bien formaté")

            # Ruff
            game_logger.info(r"🔍 Vérification Ruff...")
            result = subprocess.run(
                ["ruff", "check", "."], check=False, capture_output=True, text=True
            )
            if result.returncode != 0:
                game_logger.info(r"❌ Ruff a trouvé des problèmes de linting")
                game_logger.info(r"💡 Exécutez: ruff check . --fix")
                return False
            game_logger.info(r"✅ Ruff: Code conforme")

            # Tests
            game_logger.info(r"🧪 Exécution des tests...")
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "--tb=no", "-q"],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                game_logger.info(r"❌ Certains tests ont échoué")
                game_logger.info(r"💡 Vérifiez les tests avant de continuer")
                return False
            game_logger.info(r"✅ Tests: Tous passent")

            return True

        except Exception as e:
            game_logger.info(f"❌ Erreur lors des vérifications: {e}")
            return False

    def setup_issue_templates(self) -> bool:
        """Configure les templates d'issues"""
        self.print_header("Configuration des templates d'issues")

        templates_dir = self.project_root / ".github" / "ISSUE_TEMPLATE"

        if not templates_dir.exists():
            print("❌ Répertoire des templates d'issues non trouvé")
            return False

        templates = list(templates_dir.glob("*.yml"))
        print(f"✅ {len(templates)} templates d'issues trouvés:")
        for template in templates:
            game_logger.info(f"   📋 {template.name}")

        return True

    def setup_pull_request_template(self) -> bool:
        """Configure le template de pull request"""
        self.print_header("Configuration du template de pull request")

        pr_template = self.project_root / ".github" / "pull_request_template.md"

        if not pr_template.exists():
            game_logger.info(r"❌ Template de pull request non trouvé")
            return False

        game_logger.info(r"✅ Template de pull request configuré")
        return True

    def setup_github_labels(self) -> bool:
        """Configure les labels GitHub"""
        self.print_header("Configuration des labels GitHub")

        labels_script = self.scripts_dir / "setup_github_labels.py"

        if not labels_script.exists():
            game_logger.info(r"❌ Script de configuration des labels non trouvé")
            return False

        try:
            game_logger.info(r"🏷️  Exécution du script de configuration des labels...")
            result = subprocess.run(
                ["python", str(labels_script)],
                check=False,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                game_logger.info(r"✅ Labels GitHub configurés avec succès")
                return True
            game_logger.info(r"❌ Erreur lors de la configuration des labels")
            game_logger.info(f"Erreur: {result.stderr}")
            return False

        except Exception as e:
            print(f"❌ Erreur lors de l'exécution du script: {e}")
            return False

    def setup_github_discussions(self) -> bool:
        """Configure les discussions GitHub"""
        self.print_header("Configuration des discussions GitHub")

        discussions_script = self.scripts_dir / "setup_github_discussions.py"

        if not discussions_script.exists():
            game_logger.info(r"❌ Script de configuration des discussions non trouvé")
            return False

        try:
            game_logger.info(
                r"💬 Exécution du script de configuration des discussions..."
            )
            result = subprocess.run(
                ["python", str(discussions_script)],
                check=False,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                game_logger.info(r"✅ Discussions GitHub configurées avec succès")
                return True
            game_logger.info(r"❌ Erreur lors de la configuration des discussions")
            game_logger.info(f"Erreur: {result.stderr}")
            return False

        except Exception as e:
            print(f"❌ Erreur lors de l'exécution du script: {e}")
            return False

    def create_contribution_summary(self) -> str:
        """Crée un résumé de la configuration de contribution"""
        summary = """# 🎮 Configuration de Contribution - Arkalia Quest

## ✅ Éléments Configurés

### 📋 Templates d'Issues
- **Bug Report** : Template structuré pour signaler les bugs
- **Feature Request** : Template pour proposer des fonctionnalités
- **Help Wanted** : Template pour les tâches de contribution
- **Configuration** : Liens et redirections vers les templates

### 🚀 Template de Pull Request
- Template complet avec checklist de contribution
- Sections pour tests, documentation, sécurité
- Format standardisé pour les PR

### 🏷️ Labels GitHub
- **Priorité** : critical, high, medium, low
- **Types** : bug, enhancement, documentation, question
- **Contribution** : help wanted, good first issue, needs-triage
- **Spécifique** : luna-ai, gamification, education, security
- **Technique** : backend, frontend, devops, ci/cd
- **Taille** : xs, s, m, l, xl

### 💬 Discussions GitHub
- **Catégories** : General, Q&A, Ideas, Gameplay, Development
- **Templates** : Question, Idée, Show and Tell
- **Guide** : Documentation complète d'utilisation

## 🎯 Prochaines Étapes

### 1. Activation Manuelle (Requis)
- [ ] Activer les Discussions dans les paramètres GitHub
- [ ] Vérifier que les labels sont bien créés
- [ ] Tester les templates d'issues

### 2. Création d'Issues "Help Wanted"
- [ ] Identifier 3-5 tâches parfaites pour les nouveaux contributeurs
- [ ] Créer des issues avec le label "help wanted"
- [ ] Marquer avec "good first issue" si approprié

### 3. Documentation
- [ ] Mettre à jour le README avec les nouveaux liens
- [ ] Créer un guide de contribution pour les nouveaux arrivants
- [ ] Documenter le processus de contribution

## 🚀 Commandes Utiles

### Vérification de la qualité
```bash
# Formatage
black .

# Linting
ruff check . --fix

# Tests
python -m pytest tests/
```

### Configuration GitHub
```bash
# Labels
python scripts/setup_github_labels.py

# Discussions
python scripts/setup_github_discussions.py

# Configuration complète
python scripts/setup_github_contribution.py
```

## 📚 Ressources

- [Guide de Contribution](docs/CONTRIBUTING.md)
- [Labels GitHub](docs/GITHUB_LABELS.md)
- [Guide des Discussions](docs/GITHUB_DISCUSSIONS_GUIDE.md)
- [Templates d'Issues](.github/ISSUE_TEMPLATE/)
- [Template de PR](.github/pull_request_template.md)

## 🎉 Résultat

Votre projet Arkalia Quest est maintenant parfaitement configuré pour accueillir les contributeurs externes !

---
*Configuration générée automatiquement pour Arkalia Quest*
"""
        return summary

    def run_complete_setup(self) -> bool:
        """Exécute la configuration complète"""
        game_logger.info(
            r"🎮 Configuration Complète de la Contribution - Arkalia Quest"
        )
        print("=" * 70)

        # Vérification de l'environnement
        if not self.check_environment():
            return False

        # Vérification de la qualité du code
        if not self.run_code_quality_checks():
            game_logger.info(r"❌ Qualité du code insuffisante - correction requise")
            return False

        # Configuration des templates d'issues
        if not self.setup_issue_templates():
            return False

        # Configuration du template de PR
        if not self.setup_pull_request_template():
            return False

        # Configuration des labels (si token disponible)
        if os.environ.get("GITHUB_TOKEN"):
            self.setup_github_labels()
            self.setup_github_discussions()
        else:
            game_logger.info(
                r"⚠️  GITHUB_TOKEN non défini - configuration des labels et discussions ignorée"
            )

        # Génération du résumé
        summary = self.create_contribution_summary()
        summary_file = self.project_root / "docs" / "CONTRIBUTION_SETUP_SUMMARY.md"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)

        print("\n" + "=" * 70)
        game_logger.info(r"🎉 Configuration terminée avec succès !")
        game_logger.info(r"📚 Résumé généré: docs/CONTRIBUTION_SETUP_SUMMARY.md")
        print("=" * 70)

        return True


def main():
    """Fonction principale"""
    setup = GitHubContributionSetup()
    success = setup.run_complete_setup()

    if success:
        game_logger.info(r"\n✅ Configuration de contribution terminée avec succès !")
        game_logger.info(
            r"🚀 Votre projet est prêt pour accueillir les contributeurs !"
        )
    else:
        game_logger.info(r"\n❌ Configuration échouée - vérifiez les erreurs ci-dessus")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
