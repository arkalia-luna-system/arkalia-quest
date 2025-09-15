# Arkalia Quest Documentation

Bienvenue dans la documentation complète d'**Arkalia Quest**, le jeu cybernétique immersif développé par l'équipe Arkalia Luna System.

## 🎮 À propos du jeu

Arkalia Quest est une expérience de jeu unique qui combine :
- **Interface terminal immersive** avec LUNA, votre IA guide
- **Système de progression** avec badges, niveaux et défis
- **Thèmes visuels** adaptatifs (Matrix, Neon, Cyberpunk, Ocean, Earth, Dopamine)
- **Accessibilité complète** avec support des lecteurs d'écran
- **Architecture modulaire** pour une extensibilité maximale

## 🚀 Démarrage rapide

### Installation locale
```bash
git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Avec Docker
```bash
docker build -t arkalia-quest .
docker run -p 5000:10000 arkalia-quest
```

## 📚 Documentation

### Pour les développeurs
- [Architecture technique](docs/ARCHITECTURE_TECHNIQUE.md) - Vue d'ensemble de l'architecture
- [Guide technique développeur](docs/GUIDE_TECHNIQUE_DEVELOPPEUR.md) - Guide complet pour les développeurs
- [Guide de développement](docs/GUIDE_DEVELOPPEMENT.md) - Processus de développement

### Pour le déploiement
- [Guide de déploiement](docs/GUIDE_DEPLOIEMENT.md) - Instructions de déploiement
- [Docker](docs/DOCKER_AUTH.md) - Configuration Docker

### Pour les tests
- [Guide test utilisateur](docs/GUIDE_TEST_UTILISATEUR.md) - Tests utilisateur
- [Test plan utilisateur](docs/TEST_PLAN_UTILISATEUR.md) - Plan de tests
- [Checklists test](docs/CHECKLISTS_TEST_UTILISATEUR.md) - Checklists de validation

## 🛠️ Technologies utilisées

- **Backend**: Python 3.10+, Flask, SQLite
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Docker**: Containerisation et déploiement
- **CI/CD**: GitHub Actions
- **Documentation**: MkDocs Material

## 🤝 Contribution

Nous accueillons les contributions ! Consultez notre [guide de contribution](docs/CONTRIBUTING.md) pour commencer.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🔗 Liens utiles

- [Repository GitHub](https://github.com/arkalia-luna-system/arkalia-quest)
- [Issues](https://github.com/arkalia-luna-system/arkalia-quest/issues)
- [Discussions](https://github.com/arkalia-luna-system/arkalia-quest/discussions)

---

*Développé avec ❤️ par l'équipe Arkalia Luna System*
