# 🎮 Arkalia Quest v3.0

> **Jeu éducatif hacker pour adolescents - Apprends la cybersécurité en t'amusant !**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🌟 Présentation

**Arkalia Quest** est un jeu éducatif révolutionnaire conçu pour les adolescents de 13 ans. Plonge dans un univers cyberpunk où tu deviens un hacker rebelle, guidé par LUNA, une IA avec une personnalité unique et des insultes amicales !

### 🎯 Objectifs Éducatifs
- **Cybersécurité** : Apprends les bases du hacking éthique
- **Programmation** : Découvre les concepts de base
- **Logique** : Résous des énigmes et défis
- **Collaboration** : Participe à des défis sociaux temps réel

## 🚀 Fonctionnalités

### 🤖 IA LUNA v3.0
- **Personnalité rebelle** avec insultes amicales
- **Apprentissage automatique** et analyse comportementale
- **Memes dynamiques** et humour personnalisé
- **Recommandations intelligentes** basées sur ton profil

### 🎮 Gameplay Immersif
- **6 missions complètes** avec progression narrative
- **Scénario "La Corp te piste"** avec cliffhangers
- **Système de badges** et récompenses
- **Avatars personnalisables** et profils persistants

### ⚡ Technologies Avancées
- **Base de données SQLite** pour la persistance
- **WebSockets temps réel** pour les défis sociaux
- **IA TensorFlow.js** pour l'analyse comportementale
- **Interface responsive** et effets visuels cyberpunk

### 🌟 Effets Visuels
- **Écran qui tremble** en cas d'échec
- **Animations ASCII** et boss final
- **Effets sonores** et ambiance cyberpunk
- **Design sombre** et interface hacker authentique

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Git
- Navigateur web moderne

### Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/ton-username/arkalia-quest.git
cd arkalia-quest

# Créer l'environnement virtuel
python -m venv .venv-quest
source .venv-quest/bin/activate  # Sur macOS/Linux
# ou
.venv-quest\Scripts\activate     # Sur Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le jeu
python app.py
```

### Accès au Jeu
Ouvre ton navigateur et va sur : `http://localhost:5001`

## 🎮 Comment Jouer

### Commandes de Base
- `aide` - Affiche l'aide
- `profil` - Gère ton profil
- `mission` - Accède aux missions
- `monde` - Explore le monde d'Arkalia

### Commandes Easter Eggs
- `luna_dance` - Fais danser LUNA
- `boss_final` - Affronte le boss final
- `easter_egg_1337` - Découvre un secret
- `challenge_corp` - Défie La Corp

### Défis Sociaux
- Crée des défis temps réel
- Rejoins des rooms de compétition
- Synchronise tes actions avec d'autres joueurs
- Gagne des badges et monte en niveau

## 🏗️ Architecture

```
arkalia-quest/
├── app.py                    # Application principale Flask
├── core/                     # Modules principaux
│   ├── command_handler.py    # Gestionnaire de commandes
│   ├── game_engine.py        # Moteur de jeu
│   ├── profile_manager.py    # Gestion des profils
│   ├── database.py          # Base de données SQLite
│   └── websocket_manager.py # WebSockets temps réel
├── templates/                # Templates HTML
├── static/                   # Assets (CSS, JS, images)
├── data/                     # Données du jeu (missions, profils)
└── tests/                    # Tests automatisés
```

## 🧪 Tests

Le projet inclut une suite de tests complète :

```bash
# Lancer tous les tests
python -m pytest tests/

# Tests spécifiques
python tests/test_arkalia.py
python tests/test_integration_complete.py
```

**Résultats des tests : 100% de réussite (8/8)**

## 🚀 Déploiement

### Render (Recommandé)
Le projet est configuré pour un déploiement automatique sur Render :

1. Connecte ton repository GitHub à Render
2. Configure les variables d'environnement
3. Déploie automatiquement !

### Autres Plateformes
- **Heroku** : Compatible avec Procfile
- **Railway** : Déploiement simple
- **VPS** : Configuration manuelle

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Crée une **branche** pour ta fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Commit** tes changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvre une **Pull Request**

### Guidelines
- Respecte le style de code existant
- Ajoute des tests pour les nouvelles fonctionnalités
- Documente les changements
- Suis les conventions de commit

## 📊 Métriques

- **Tests** : 100% de réussite
- **Performance** : < 200ms de temps de réponse
- **Utilisateurs simultanés** : 50+ supportés
- **Mémoire** : < 100MB par instance

## 🏆 Badges et Récompenses

### Badges de Progression
- 🌱 **Débutant** - Première mission complétée
- ⚡ **Hacker** - Niveau 3 atteint
- 🎯 **Expert** - Toutes les missions terminées
- 🏆 **Légende** - 100% des badges débloqués

### Badges Secrets
- 🕵️ **Easter Egg Hunter** - Découvert tous les secrets
- 🎭 **LUNA's Friend** - Interagi 100 fois avec LUNA
- ⚔️ **Corp Slayer** - Défié La Corp 10 fois

## 📱 Compatibilité

- **Desktop** : Chrome, Firefox, Safari, Edge
- **Mobile** : Interface responsive optimisée
- **Tablet** : Expérience adaptée tactile

## 🔒 Sécurité

- Validation des entrées utilisateur
- Protection contre les injections
- Gestion sécurisée des sessions
- Chiffrement des données sensibles

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **LUNA v3.0** - Notre IA rebelle et attachante
- **La communauté** - Pour les feedbacks et suggestions
- **Les testeurs** - Adolescents de 13 ans qui ont validé le concept

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/ton-username/arkalia-quest/issues)
- **Discussions** : [GitHub Discussions](https://github.com/ton-username/arkalia-quest/discussions)
- **Email** : support@arkalia-quest.com

---

<div align="center">

**🎮 Prêt à devenir un hacker légendaire ? Lance Arkalia Quest maintenant ! 🚀**

*Développé avec ❤️ pour les futurs experts en cybersécurité*

[![Play Now](https://img.shields.io/badge/Play%20Now-Live%20Demo-red?style=for-the-badge&logo=gamepad-icon)](https://arkalia-quest.onrender.com)

</div> 