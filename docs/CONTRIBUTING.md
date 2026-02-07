
# 🤝 Guide de Contribution - Arkalia Quest

Merci de votre intérêt pour contribuer à **Arkalia Quest** ! Ce guide vous aidera à participer au développement de ce projet éducatif innovant.

## 📋 **Table des Matières**

- [🚀 Démarrage Rapide](#-démarrage-rapide)

- [🔧 Configuration de l'Environnement](#-configuration-de-lenvironnement)

- [📝 Standards de Code](#-standards-de-code)

- [🧪 Tests](#-tests)

- [📚 Documentation](#-documentation)

- [🔄 Workflow de Contribution](#-workflow-de-contribution)

- [🏷️ Types de Contributions](#-types-de-contributions)

- [📞 Support et Questions](#-support-et-questions)

---

## 🚀 **Démarrage Rapide**

### **1. Fork et Clone**

```bash



# Fork le projet sur GitHub



# Puis clonez votre fork


git clone https://github.com/VOTRE_USERNAME/arkalia-quest.git
cd arkalia-quest


# Ajoutez le remote upstream


git remote add upstream https://github.com/arkalia-luna-system/arkalia-quest.git


```text



### **2. Installation**



```bash



# Créez l'environnement virtuel


python -m venv venv
source venv/bin/activate  # Linux/Mac


# ou


venv\Scripts\activate     # Windows


# Installez les dépendances


pip install -r requirements.txt


```text



### **3. Lancement**



```bash



# Démarrez l'application


python app.py


# Ouvrez http://localhost:5001



```text


---


## 🔧 **Configuration de l'Environnement**



### **Prérequis**



- **Python** : 3.8+



- **Git** : 2.20+



- **pip** : 20.0+



### **Variables d'Environnement**



```bash



# Copiez le fichier de configuration


cp config/config.example.py config/config.py


# Configurez vos variables


export FLASK_ENV=development
export DEBUG=true
export SECRET_KEY=your-secret-key


```text



### **Outils de Développement**



```bash



# Installation des outils de qualité


pip install black ruff pytest pytest-cov


# Configuration des hooks Git (optionnel)


pre-commit install


```text


---


## 📝 **Standards de Code**



### **Python (PEP 8)**



- **Indentation** : 4 espaces



- **Longueur de ligne** : 88 caractères max



- **Imports** : Triés et groupés



- **Docstrings** : Format Google



### **Formatage Automatique**



```bash



# Formatage avec Black


black .


# Linting avec Ruff


ruff check .
ruff format .


```text



### **Exemple de Code**



```python


def calculate_score(user_id: int, game_type: str) -> float:
    """Calcule le score d'un utilisateur pour un type de jeu.

    Args:
        user_id: Identifiant de l'utilisateur
        game_type: Type de jeu ('math', 'logic', 'science')

    Returns:
        Score calculé (0.0 à 100.0)

    Raises:
        ValueError: Si le type de jeu est invalide
    """
    if game_type not in VALID_GAME_TYPES:
        raise ValueError(f"Type de jeu invalide: {game_type}")

    # Logique de calcul...
    return final_score


```text


---


## 🧪 **Tests**



### **Exécution des Tests**



```bash



# Tous les tests


python -m pytest tests/


# Tests spécifiques


python -m pytest tests/test_game_engine.py


# Avec couverture


python -m pytest tests/ --cov=core --cov-report=html


# Tests en parallèle


python -m pytest tests/ -n auto


```text



### **Écriture de Tests**



```python


import pytest
from core.game_engine import GameEngine

class TestGameEngine:
    """Tests pour le moteur de jeu."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.engine = GameEngine()

    def test_new_game_creation(self):
        """Test de création d'une nouvelle partie."""
        game = self.engine.create_game("math", user_id=1)
        assert game is not None
        assert game.type == "math"
        assert game.user_id == 1

    def test_invalid_game_type(self):
        """Test avec un type de jeu invalide."""
        with pytest.raises(ValueError):
            self.engine.create_game("invalid", user_id=1)


```text



### **Standards des Tests**



- **Nommage** : `test_<fonctionnalité>_<scénario>`



- **Structure** : Arrange-Act-Assert



- **Couverture** : Minimum 80%



- **Mocking** : Utilisez `pytest-mock`


---


## 📚 **Documentation**



### **Docstrings**



```python


def process_user_input(input_data: dict) -> dict:
    """Traite les données d'entrée utilisateur.

    Cette fonction valide et traite les données soumises
    par l'utilisateur via l'interface web.

    Args:
        input_data: Dictionnaire contenant les données utilisateur

    Returns:
        Dictionnaire avec les données traitées et validées

    Raises:
        ValidationError: Si les données sont invalides
        ProcessingError: Si le traitement échoue

    Example:
        >>> data = {"name": "John", "age": 25}
        >>> result = process_user_input(data)
        >>> print(result["status"])
        'validated'
    """


```text



### **README et Documentation**



- **README.md** : Présentation du projet



- **docs/** : Documentation technique



- **API** : Documentation des endpoints



- **Architecture** : Schémas et diagrammes


---


## 🔄 **Workflow de Contribution**



### **1. Préparation**



```bash



# Synchronisez avec upstream


git fetch upstream
git checkout main
git merge upstream/main


# Créez une branche feature


git checkout -b feature/nouvelle-fonctionnalite


```text



### **2. Développement**



```bash



# Faites vos modifications



# Testez localement


python -m pytest tests/
black .
ruff check .


# Committez régulièrement


git add .
git commit -m "feat: ajoute nouvelle fonctionnalité X"


```text



### **3. Soumission**



```bash



# Poussez votre branche


git push origin feature/nouvelle-fonctionnalite


# Créez une Pull Request sur GitHub



# Remplissez le template de PR



```text



### **4. Revue et Merge**



- **Code Review** : Au moins 1 approbation



- **Tests** : Tous les tests doivent passer



- **CI/CD** : GitHub Actions doit réussir



- **Merge** : Squash et merge recommandé


---


## 🏷️ **Types de Contributions**



### **🐛 Corrections de Bugs**



- **Issue** : Décrivez le bug clairement



- **Reproduction** : Étapes pour reproduire



- **Fix** : Solution proposée



- **Tests** : Tests pour éviter la régression



### **✨ Nouvelles Fonctionnalités**



- **Discussion** : Ouvrez une issue pour discuter



- **Spécification** : Décrivez la fonctionnalité



- **Implémentation** : Code + tests + docs



- **Documentation** : Mise à jour des guides



### **📚 Documentation**



- **README** : Amélioration de la présentation



- **API Docs** : Documentation des endpoints



- **Guides** : Tutoriels et exemples



- **Traduction** : Support multilingue



### **🧪 Tests**



- **Couverture** : Augmentation de la couverture



- **Nouveaux tests** : Tests pour nouvelles fonctionnalités



- **Performance** : Tests de charge et stress



- **Intégration** : Tests end-to-end


---


## 📞 **Support et Questions**



### **Ressources**



- **Issues GitHub** : [Bugs et demandes](https://github.com/arkalia-luna-system/arkalia-quest/issues)



- **Discussions** : [Forum communautaire](https://github.com/arkalia-luna-system/arkalia-quest/discussions)



- **Wiki** : [Documentation détaillée](https://github.com/arkalia-luna-system/arkalia-quest/wiki)



### **Contact**



- **Mainteneurs** : [@arkalia-luna-system](https://github.com/arkalia-luna-system)



- **Email** : arkalia.luna.system@gmail.com



- **Discord** : [Serveur communautaire](https://discord.gg/arkalia)


---


## 🎯 **Conventions de Commit**



### **Format**



```text


<type>(<scope>): <description>

[body optionnel]

[footer optionnel]


```text



### **Types**



- **feat** : Nouvelle fonctionnalité



- **fix** : Correction de bug



- **docs** : Documentation



- **style** : Formatage, point-virgules, etc.



- **refactor** : Refactoring du code



- **test** : Ajout de tests



- **chore** : Tâches de maintenance



### **Exemples**



```bash


git commit -m "feat(game): ajoute système de niveaux progressifs"
git commit -m "fix(ui): corrige l'affichage sur mobile"
git commit -m "docs(api): met à jour la documentation des endpoints"


```text


---


## 🌟 **Reconnaissance**


Toutes les contributions sont appréciées ! Les contributeurs seront mentionnés dans :


- **README.md** : Section contributeurs



- **CHANGELOG.md** : Historique des versions



- **Releases GitHub** : Notes de version


---

# **Merci de contribuer à Arkalia Quest ! 🎮✨**

## *Ensemble, créons l'éducation de demain !*
