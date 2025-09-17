#!/usr/bin/env python3
"""
Script de configuration des labels GitHub pour Arkalia Quest
Configure automatiquement les labels recommandés pour un projet open source
"""

import os
import sys
from typing import Any

import requests


class GitHubLabelsSetup:
    """Configuration des labels GitHub pour Arkalia Quest"""

    def __init__(
        self, token: str = None, repo: str = "arkalia-luna-system/arkalia-quest"
    ):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}/labels"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Arkalia-Quest-Labels-Setup",
        }

        # Labels recommandés pour un projet open source éducatif
        self.labels = [
            # 🎯 Priorité et statut
            {
                "name": "priority: critical",
                "color": "d73a4a",
                "description": "Problème critique nécessitant une attention immédiate",
            },
            {
                "name": "priority: high",
                "color": "f85149",
                "description": "Problème important nécessitant une attention rapide",
            },
            {
                "name": "priority: medium",
                "color": "fbca04",
                "description": "Problème de priorité moyenne",
            },
            {
                "name": "priority: low",
                "color": "0e8a16",
                "description": "Problème de faible priorité",
            },
            # 🏷️ Types d'issues
            {
                "name": "bug",
                "color": "d73a4a",
                "description": "Quelque chose ne fonctionne pas",
            },
            {
                "name": "enhancement",
                "color": "a2eeef",
                "description": "Nouvelle fonctionnalité ou amélioration",
            },
            {
                "name": "documentation",
                "color": "0075ca",
                "description": "Améliorations ou ajouts à la documentation",
            },
            {
                "name": "question",
                "color": "d876e3",
                "description": "Question ou demande d'information",
            },
            {
                "name": "duplicate",
                "color": "cfd3d7",
                "description": "Issue ou PR en doublon",
            },
            {
                "name": "invalid",
                "color": "e4e669",
                "description": "Issue ou PR non valide",
            },
            {
                "name": "wontfix",
                "color": "ffffff",
                "description": "Ne sera pas corrigé",
            },
            # 🤝 Contribution
            {
                "name": "help wanted",
                "color": "008672",
                "description": "Aide de la communauté bienvenue",
            },
            {
                "name": "good first issue",
                "color": "7057ff",
                "description": "Parfait pour les nouveaux contributeurs",
            },
            {
                "name": "needs-triage",
                "color": "f9d0c4",
                "description": "Nécessite une évaluation initiale",
            },
            {
                "name": "needs-review",
                "color": "fbca04",
                "description": "Nécessite une révision",
            },
            {
                "name": "needs-testing",
                "color": "c2e0c6",
                "description": "Nécessite des tests",
            },
            # 🎮 Spécifique au projet
            {
                "name": "luna-ai",
                "color": "9c27b0",
                "description": "Lié au moteur LUNA AI",
            },
            {
                "name": "gamification",
                "color": "ff9800",
                "description": "Système de gamification",
            },
            {"name": "education", "color": "4caf50", "description": "Contenu éducatif"},
            {
                "name": "security",
                "color": "f44336",
                "description": "Sécurité et protection",
            },
            {
                "name": "performance",
                "color": "2196f3",
                "description": "Optimisation des performances",
            },
            {
                "name": "ui/ux",
                "color": "e91e63",
                "description": "Interface utilisateur et expérience",
            },
            {"name": "api", "color": "607d8b", "description": "API et endpoints"},
            {
                "name": "database",
                "color": "795548",
                "description": "Base de données et stockage",
            },
            {"name": "testing", "color": "ffc107", "description": "Tests et qualité"},
            # 🔧 Technique
            {
                "name": "backend",
                "color": "3f51b5",
                "description": "Code backend et logique métier",
            },
            {
                "name": "frontend",
                "color": "e91e63",
                "description": "Interface utilisateur et frontend",
            },
            {
                "name": "devops",
                "color": "009688",
                "description": "Déploiement et infrastructure",
            },
            {
                "name": "ci/cd",
                "color": "ff5722",
                "description": "Intégration continue et déploiement",
            },
            # 📊 Taille et complexité
            {
                "name": "size: xs",
                "color": "c2e0c6",
                "description": "Très petite tâche (< 1h)",
            },
            {
                "name": "size: s",
                "color": "9be9a8",
                "description": "Petite tâche (1-4h)",
            },
            {
                "name": "size: m",
                "color": "40c463",
                "description": "Tâche moyenne (1-2 jours)",
            },
            {
                "name": "size: l",
                "color": "30a14e",
                "description": "Grande tâche (1-2 semaines)",
            },
            {
                "name": "size: xl",
                "color": "216e39",
                "description": "Très grande tâche (> 2 semaines)",
            },
        ]

    def check_auth(self) -> bool:
        """Vérifie l'authentification GitHub"""
        try:
            response = requests.get(
                f"https://api.github.com/repos/{self.repo}",
                headers=self.headers,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erreur d'authentification: {e}")
            return False

    def get_existing_labels(self) -> list[dict[str, Any]]:
        """Récupère les labels existants"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            print(
                f"❌ Erreur lors de la récupération des labels: {response.status_code}"
            )
            return []
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des labels: {e}")
            return []

    def create_label(self, label: dict[str, str]) -> bool:
        """Crée un label"""
        try:
            response = requests.post(self.base_url, headers=self.headers, json=label)
            if response.status_code == 201:
                print(f"✅ Label créé: {label['name']}")
                return True
            if response.status_code == 422:
                print(f"⚠️  Label déjà existant: {label['name']}")
                return True
            print(
                f"❌ Erreur lors de la création du label {label['name']}: {response.status_code}",
            )
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la création du label {label['name']}: {e}")
            return False

    def update_label(self, label_name: str, label: dict[str, str]) -> bool:
        """Met à jour un label existant"""
        try:
            url = f"{self.base_url}/{label_name}"
            response = requests.patch(url, headers=self.headers, json=label)
            if response.status_code == 200:
                print(f"🔄 Label mis à jour: {label['name']}")
                return True
            print(
                f"❌ Erreur lors de la mise à jour du label {label['name']}: {response.status_code}",
            )
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du label {label['name']}: {e}")
            return False

    def setup_labels(self) -> bool:
        """Configure tous les labels"""
        print("🎮 Configuration des labels GitHub pour Arkalia Quest")
        print("=" * 60)

        # Vérification de l'authentification
        if not self.check_auth():
            print("❌ Authentification GitHub échouée")
            print("💡 Assurez-vous que GITHUB_TOKEN est défini et valide")
            return False

        print("✅ Authentification GitHub réussie")

        # Récupération des labels existants
        existing_labels = self.get_existing_labels()
        existing_names = {label["name"] for label in existing_labels}

        print(f"📊 {len(existing_labels)} labels existants trouvés")
        print(f"🎯 {len(self.labels)} labels à configurer")
        print()

        success_count = 0
        total_count = len(self.labels)

        for label in self.labels:
            if label["name"] in existing_names:
                # Mise à jour du label existant
                if self.update_label(label["name"], label):
                    success_count += 1
            # Création d'un nouveau label
            elif self.create_label(label):
                success_count += 1

        print()
        print("=" * 60)
        print(f"📊 Résumé: {success_count}/{total_count} labels configurés avec succès")

        if success_count == total_count:
            print("🎉 Tous les labels ont été configurés avec succès !")
            return True
        print("⚠️  Certains labels n'ont pas pu être configurés")
        return False

    def generate_labels_documentation(self) -> str:
        """Génère la documentation des labels"""
        doc = """# 🏷️ Labels GitHub - Arkalia Quest

## 📋 Vue d'ensemble

Ce document décrit tous les labels utilisés dans le projet Arkalia Quest pour organiser et catégoriser les issues et pull requests.

## 🎯 Labels de Priorité

| Label | Couleur | Description |
|-------|---------|-------------|
| `priority: critical` | 🔴 | Problème critique nécessitant une attention immédiate |
| `priority: high` | 🟠 | Problème important nécessitant une attention rapide |
| `priority: medium` | 🟡 | Problème de priorité moyenne |
| `priority: low` | 🟢 | Problème de faible priorité |

## 🏷️ Types d'Issues

| Label | Couleur | Description |
|-------|---------|-------------|
| `bug` | 🔴 | Quelque chose ne fonctionne pas |
| `enhancement` | 🔵 | Nouvelle fonctionnalité ou amélioration |
| `documentation` | 📘 | Améliorations ou ajouts à la documentation |
| `question` | 🟣 | Question ou demande d'information |
| `duplicate` | ⚪ | Issue ou PR en doublon |
| `invalid` | 🟡 | Issue ou PR non valide |
| `wontfix` | ⚪ | Ne sera pas corrigé |

## 🤝 Contribution

| Label | Couleur | Description |
|-------|---------|-------------|
| `help wanted` | 🟢 | Aide de la communauté bienvenue |
| `good first issue` | 🟣 | Parfait pour les nouveaux contributeurs |
| `needs-triage` | 🟠 | Nécessite une évaluation initiale |
| `needs-review` | 🟡 | Nécessite une révision |
| `needs-testing` | 🟢 | Nécessite des tests |

## 🎮 Spécifique au Projet

| Label | Couleur | Description |
|-------|---------|-------------|
| `luna-ai` | 🟣 | Lié au moteur LUNA AI |
| `gamification` | 🟠 | Système de gamification |
| `education` | 🟢 | Contenu éducatif |
| `security` | 🔴 | Sécurité et protection |
| `performance` | 🔵 | Optimisation des performances |
| `ui/ux` | 🟣 | Interface utilisateur et expérience |
| `api` | 🔵 | API et endpoints |
| `database` | 🟤 | Base de données et stockage |
| `testing` | 🟡 | Tests et qualité |

## 🔧 Technique

| Label | Couleur | Description |
|-------|---------|-------------|
| `backend` | 🔵 | Code backend et logique métier |
| `frontend` | 🟣 | Interface utilisateur et frontend |
| `devops` | 🟢 | Déploiement et infrastructure |
| `ci/cd` | 🟠 | Intégration continue et déploiement |

## 📊 Taille et Complexité

| Label | Couleur | Description |
|-------|---------|-------------|
| `size: xs` | 🟢 | Très petite tâche (< 1h) |
| `size: s` | 🟢 | Petite tâche (1-4h) |
| `size: m` | 🟡 | Tâche moyenne (1-2 jours) |
| `size: l` | 🟠 | Grande tâche (1-2 semaines) |
| `size: xl` | 🔴 | Très grande tâche (> 2 semaines) |

## 🎯 Utilisation Recommandée

### Pour les Issues
1. **Type** : Toujours assigner un type (`bug`, `enhancement`, `documentation`, etc.)
2. **Priorité** : Assigner une priorité si approprié
3. **Spécifique** : Ajouter des labels spécifiques au projet si applicable
4. **Taille** : Estimer la taille pour les tâches de développement

### Pour les Pull Requests
1. **Type** : Même système que les issues
2. **Statut** : Utiliser `needs-review`, `needs-testing` selon l'état
3. **Spécifique** : Labels techniques selon les fichiers modifiés

## 🔄 Maintenance

Les labels sont maintenus automatiquement via le script `scripts/setup_github_labels.py`.

Pour ajouter de nouveaux labels :
1. Modifier le script `setup_github_labels.py`
2. Exécuter le script pour appliquer les changements
3. Mettre à jour cette documentation

---
*Documentation générée automatiquement pour Arkalia Quest*
"""
        return doc


def main():
    """Fonction principale"""
    print("🎮 Configuration des labels GitHub - Arkalia Quest")
    print("=" * 60)

    # Vérification du token GitHub
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN non défini")
        print("💡 Définissez votre token GitHub :")
        print("   export GITHUB_TOKEN=your_token_here")
        print("   ou créez un fichier .env avec GITHUB_TOKEN=your_token_here")
        return False

    # Configuration des labels
    setup = GitHubLabelsSetup(token)
    success = setup.setup_labels()

    if success:
        # Génération de la documentation
        doc = setup.generate_labels_documentation()
        with open("docs/GITHUB_LABELS.md", "w", encoding="utf-8") as f:
            f.write(doc)
        print("📚 Documentation des labels générée: docs/GITHUB_LABELS.md")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
