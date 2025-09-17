#!/usr/bin/env python3
"""
Script de configuration des Discussions GitHub pour Arkalia Quest
Active et configure les discussions pour faciliter la collaboration communautaire
"""

import os
import sys

import requests


class GitHubDiscussionsSetup:
    """Configuration des Discussions GitHub pour Arkalia Quest"""

    def __init__(self, token: str = None, repo: str = "arkalia-luna-system/arkalia-quest"):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Arkalia-Quest-Discussions-Setup",
        }

        # Catégories de discussions recommandées
        self.categories = [
            {
                "name": "💬 General",
                "description": "Discussions générales sur le projet Arkalia Quest",
                "emoji": "💬",
                "answerable": False,
            },
            {
                "name": "❓ Q&A",
                "description": "Questions et réponses sur l'utilisation d'Arkalia Quest",
                "emoji": "❓",
                "answerable": True,
            },
            {
                "name": "💡 Ideas",
                "description": "Idées et suggestions pour améliorer Arkalia Quest",
                "emoji": "💡",
                "answerable": False,
            },
            {
                "name": "🎮 Gameplay",
                "description": "Discussions sur le gameplay et l'expérience utilisateur",
                "emoji": "🎮",
                "answerable": False,
            },
            {
                "name": "🔧 Development",
                "description": "Discussions techniques sur le développement",
                "emoji": "🔧",
                "answerable": False,
            },
            {
                "name": "📚 Documentation",
                "description": "Discussions sur la documentation et les guides",
                "emoji": "📚",
                "answerable": False,
            },
            {
                "name": "🤝 Contributing",
                "description": "Discussions sur la contribution au projet",
                "emoji": "🤝",
                "answerable": False,
            },
            {
                "name": "🐛 Bug Reports",
                "description": "Signalement et discussion des bugs",
                "emoji": "🐛",
                "answerable": False,
            },
            {
                "name": "✨ Feature Requests",
                "description": "Demandes de nouvelles fonctionnalités",
                "emoji": "✨",
                "answerable": False,
            },
            {
                "name": "🎉 Show and Tell",
                "description": "Partagez vos créations et projets avec Arkalia Quest",
                "emoji": "🎉",
                "answerable": False,
            },
        ]

    def check_auth(self) -> bool:
        """Vérifie l'authentification GitHub"""
        try:
            response = requests.get(f"{self.base_url}", headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erreur d'authentification: {e}")
            return False

    def check_discussions_enabled(self) -> bool:
        """Vérifie si les discussions sont activées"""
        try:
            response = requests.get(f"{self.base_url}/discussions", headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des discussions: {e}")
            return False

    def enable_discussions(self) -> bool:
        """Active les discussions (nécessite des permissions admin)"""
        print("⚠️  L'activation des discussions nécessite des permissions d'administrateur")
        print(
            "💡 Veuillez activer manuellement les discussions dans les paramètres du repository :",
        )
        print(f"   https://github.com/{self.repo}/settings")
        print("   → Features → Discussions → Enable discussions")
        return True

    def create_discussion_categories(self) -> bool:
        """Crée les catégories de discussions"""
        print("📋 Création des catégories de discussions...")

        success_count = 0
        total_count = len(self.categories)

        for category in self.categories:
            try:
                # Note: L'API GitHub ne permet pas de créer des catégories via l'API
                # Les catégories doivent être créées manuellement
                print(f"📝 Catégorie recommandée: {category['name']} - {category['description']}")
                success_count += 1
            except Exception as e:
                print(f"❌ Erreur pour la catégorie {category['name']}: {e}")

        print(f"📊 {success_count}/{total_count} catégories documentées")
        return True

    def create_discussion_templates(self) -> bool:
        """Crée des templates de discussions"""
        print("📝 Création des templates de discussions...")

        # Template pour les questions
        qa_template = """# ❓ Question

## 🎯 Sujet
<!-- Décrivez brièvement votre question -->

## 📝 Détails
<!-- Fournissez plus de détails sur votre question -->

## 🔍 Ce que j'ai essayé
<!-- Décrivez ce que vous avez déjà essayé -->

## 📚 Ressources consultées
<!-- Liens vers la documentation, issues, etc. -->

## 🖥️ Environnement
- OS: [ex: macOS 14.0, Windows 11, Ubuntu 22.04]
- Version Python: [ex: 3.10.14]
- Version Arkalia Quest: [ex: 3.1.0]

## 📎 Informations supplémentaires
<!-- Autres informations utiles -->
"""

        # Template pour les idées
        ideas_template = """# 💡 Idée

## 🎯 Titre de l'idée
<!-- Un titre clair et concis -->

## 📝 Description
<!-- Décrivez votre idée en détail -->

## 🤔 Problème résolu
<!-- Quel problème cette idée résout-elle ? -->

## 💡 Solution proposée
<!-- Comment imaginez-vous cette idée ? -->

## 🎯 Public cible
<!-- Qui bénéficierait de cette idée ? -->

## 📊 Impact estimé
<!-- Quel serait l'impact de cette idée ? -->

## 🔄 Alternatives
<!-- Avez-vous considéré d'autres approches ? -->

## 📎 Informations supplémentaires
<!-- Mockups, exemples, références, etc. -->
"""

        # Template pour le show and tell
        show_template = """# 🎉 Show and Tell

## 🎮 Titre de votre projet
<!-- Un titre accrocheur pour votre création -->

## 📝 Description
<!-- Décrivez ce que vous avez créé avec Arkalia Quest -->

## 🖼️ Images/Vidéos
<!-- Ajoutez des captures d'écran ou vidéos -->

## 🛠️ Technologies utilisées
<!-- Quelles technologies avez-vous utilisées ? -->

## 🎯 Fonctionnalités
<!-- Quelles fonctionnalités d'Arkalia Quest avez-vous utilisées ? -->

## 🔗 Liens
<!-- Liens vers votre projet, code, etc. -->

## 💭 Leçons apprises
<!-- Qu'avez-vous appris en utilisant Arkalia Quest ? -->

## 🤝 Aide recherchée
<!-- Avez-vous besoin d'aide pour quelque chose ? -->
"""

        # Sauvegarde des templates
        templates_dir = ".github/DISCUSSION_TEMPLATE"
        os.makedirs(templates_dir, exist_ok=True)

        templates = {
            "question.md": qa_template,
            "idea.md": ideas_template,
            "show_and_tell.md": show_template,
        }

        for filename, content in templates.items():
            filepath = os.path.join(templates_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Template créé: {filepath}")

        return True

    def generate_discussions_guide(self) -> str:
        """Génère un guide d'utilisation des discussions"""
        guide = """# 💬 Guide des Discussions GitHub - Arkalia Quest

## 🎯 Introduction

Les Discussions GitHub sont un espace de collaboration communautaire pour Arkalia Quest. Elles permettent d'échanger des idées, poser des questions et partager des expériences.

## 📋 Catégories Disponibles

### 💬 General
Discussions générales sur le projet Arkalia Quest, annonces, mises à jour.

### ❓ Q&A
Questions et réponses sur l'utilisation d'Arkalia Quest. Parfait pour obtenir de l'aide !

### 💡 Ideas
Idées et suggestions pour améliorer Arkalia Quest. Partagez vos idées créatives !

### 🎮 Gameplay
Discussions sur le gameplay, l'expérience utilisateur, les missions et le contenu éducatif.

### 🔧 Development
Discussions techniques sur le développement, l'architecture, les bugs et les améliorations.

### 📚 Documentation
Discussions sur la documentation, les guides, les tutoriels et l'aide.

### 🤝 Contributing
Discussions sur la contribution au projet, les bonnes pratiques et l'organisation.

### 🐛 Bug Reports
Signalement et discussion des bugs. Utilisez les issues pour les bugs confirmés.

### ✨ Feature Requests
Demandes de nouvelles fonctionnalités. Utilisez les issues pour les demandes formelles.

### 🎉 Show and Tell
Partagez vos créations, projets et expériences avec Arkalia Quest !

## 🎯 Comment Utiliser les Discussions

### ✅ Bonnes Pratiques

1. **Choisissez la bonne catégorie** : Assurez-vous de poster dans la catégorie appropriée
2. **Titre descriptif** : Utilisez un titre clair et descriptif
3. **Recherchez d'abord** : Vérifiez si votre question a déjà été posée
4. **Soyez respectueux** : Maintenez un ton professionnel et bienveillant
5. **Utilisez les templates** : Les templates vous aident à structurer vos posts

### ❌ À Éviter

- Spam ou contenu non pertinent
- Questions déjà répondues dans la documentation
- Discussions off-topic
- Langage inapproprié ou irrespectueux

## 📝 Templates Disponibles

### Question (❓ Q&A)
Utilisez le template `question.md` pour poser des questions structurées.

### Idée (💡 Ideas)
Utilisez le template `idea.md` pour proposer des idées détaillées.

### Show and Tell (🎉 Show and Tell)
Utilisez le template `show_and_tell.md` pour partager vos créations.

## 🔍 Recherche et Navigation

- **Recherche** : Utilisez la barre de recherche pour trouver des discussions existantes
- **Filtres** : Filtrez par catégorie, statut, auteur, etc.
- **Épinglage** : Les discussions importantes sont épinglées en haut
- **Marquage** : Marquez les discussions comme résolues quand approprié

## 🏷️ Labels et Organisation

Les discussions utilisent des labels pour l'organisation :
- `resolved` : Discussion résolue
- `needs-answer` : Besoin d'une réponse
- `feature-request` : Demande de fonctionnalité
- `bug-report` : Signalement de bug
- `documentation` : Lié à la documentation
- `help-wanted` : Aide recherchée

## 🤝 Modération

Les discussions sont modérées par l'équipe Arkalia Quest :
- Respect des règles de la communauté
- Qualité du contenu
- Organisation et catégorisation
- Résolution des conflits

## 📞 Support

Pour des questions sur l'utilisation des discussions :
- Consultez ce guide
- Posez une question dans la catégorie Q&A
- Contactez l'équipe via les issues

## 🎉 Bienvenue !

Nous sommes ravis de vous accueillir dans la communauté Arkalia Quest !
Partagez, collaborez et contribuez à faire d'Arkalia Quest un projet encore meilleur.

---
*Guide généré automatiquement pour Arkalia Quest*
"""
        return guide

    def setup_discussions(self) -> bool:
        """Configure les discussions GitHub"""
        print("💬 Configuration des Discussions GitHub - Arkalia Quest")
        print("=" * 60)

        # Vérification de l'authentification
        if not self.check_auth():
            print("❌ Authentification GitHub échouée")
            print("💡 Assurez-vous que GITHUB_TOKEN est défini et valide")
            return False

        print("✅ Authentification GitHub réussie")

        # Vérification des discussions
        if self.check_discussions_enabled():
            print("✅ Discussions déjà activées")
        else:
            print("⚠️  Discussions non activées")
            self.enable_discussions()

        # Création des catégories
        self.create_discussion_categories()

        # Création des templates
        self.create_discussion_templates()

        # Génération du guide
        guide = self.generate_discussions_guide()
        with open("docs/GITHUB_DISCUSSIONS_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(guide)
        print("📚 Guide des discussions généré: docs/GITHUB_DISCUSSIONS_GUIDE.md")

        print()
        print("=" * 60)
        print("🎉 Configuration des discussions terminée !")
        print("💡 N'oubliez pas d'activer les discussions manuellement dans les paramètres GitHub")

        return True


def main():
    """Fonction principale"""
    print("💬 Configuration des Discussions GitHub - Arkalia Quest")
    print("=" * 60)

    # Vérification du token GitHub
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN non défini")
        print("💡 Définissez votre token GitHub :")
        print("   export GITHUB_TOKEN=your_token_here")
        print("   ou créez un fichier .env avec GITHUB_TOKEN=your_token_here")
        return False

    # Configuration des discussions
    setup = GitHubDiscussionsSetup(token)
    success = setup.setup_discussions()

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
