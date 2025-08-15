---
**Statut : ACTIF**
**Dernière mise à jour : Juillet 2025**
**Résumé :** Guide de contribution pour participer au développement d'Arkalia Quest.

**Liens utiles :**
- [Documentation principale](README.md)
- [Statut projet](STATUT_PROJET_ACTUEL.md)
- [Changelog documentation](CHANGELOG_DOCUMENTATION.md)
---

## 🎯 BIENVENUE CONTRIBUTEURS !

Merci de votre intérêt pour contribuer à **Arkalia Quest** ! Ce guide vous aidera à comprendre comment participer au développement de ce jeu éducatif pour ados.

### 🌟 **Pourquoi contribuer ?**
- **Éducation** : Aider les ados à apprendre la programmation
- **Innovation** : Créer des expériences de jeu uniques
- **Communauté** : Rejoindre une équipe passionnée
- **Impact** : Faire une différence dans l'éducation numérique

---

## 📋 PRÉREQUIS

### 🛠️ **Compétences techniques**
- **Python** : Connaissance de base (Flask, SQLite)
- **JavaScript** : HTML, CSS, ES6+
- **Git** : Gestion de versions
- **Tests** : Notions de tests automatisés

### 🎮 **Connaissance du projet**
- **Lire la documentation** : `/docs/`
- **Tester le jeu** : Comprendre l'expérience utilisateur
- **Connaître l'architecture** : Structure du code
- **Comprendre le public** : Ados de 13 ans

---

## 🚀 PREMIERS PAS

### 1️⃣ **Fork et Clone**
```bash
# Fork le projet sur GitHub
# Puis cloner votre fork
git clone https://github.com/votre-username/arkalia-quest.git
cd arkalia-quest

# Ajouter le repository original
git remote add upstream https://github.com/original/arkalia-quest.git
```

### 2️⃣ **Installation locale**
```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python -c "from core.database import DatabaseManager; DatabaseManager().init_database()"
```

### 3️⃣ **Lancer le projet**
```bash
python app.py
# Accéder à http://localhost:5001
```

---

## 🎯 TYPES DE CONTRIBUTIONS

### 🐛 **Correction de bugs**
- **Rapporter un bug** : Issue détaillée
- **Corriger un bug** : Pull Request avec tests
- **Améliorer la robustesse** : Gestion d'erreurs

### ✨ **Nouvelles fonctionnalités**
- **Commandes** : Nouvelles commandes de jeu
- **Missions** : Scénarios additionnels
- **Badges** : Système de récompenses
- **Interface** : Améliorations UX/UI

### 📚 **Documentation**
- **Guides** : Tutoriels et explications
- **API** : Documentation technique
- **Traductions** : Support multi-langues
- **Exemples** : Code d'exemple

### 🧪 **Tests**
- **Tests unitaires** : Couverture de code
- **Tests d'intégration** : Fonctionnalités
- **Tests de performance** : Optimisations
- **Tests de sécurité** : Vulnérabilités

---

## 🔧 PROCESSUS DE DÉVELOPPEMENT

### 1️⃣ **Créer une branche**
```bash
# Synchroniser avec upstream
git fetch upstream
git checkout main
git merge upstream/main

# Créer une branche pour votre contribution
git checkout -b feature/nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

### 2️⃣ **Développer**
```bash
# Faire vos modifications
# Tester localement
python app.py

# Vérifier les tests
python -m pytest tests/

# Vérifier le style de code
flake8 .
black .
```

### 3️⃣ **Commiter**
```bash
# Ajouter vos fichiers
git add .

# Commiter avec un message descriptif
git commit -m "feat: ajouter nouvelle commande hack_advanced

- Implémente la commande hack_advanced
- Ajoute des effets visuels Matrix
- Inclut des tests unitaires
- Met à jour la documentation"
```

### 4️⃣ **Pousser et créer une Pull Request**
```bash
git push origin feature/nouvelle-fonctionnalite
# Créer une Pull Request sur GitHub
```

---

## 📝 STANDARDS DE CODE

### 🐍 **Python (PEP 8)**
```python
# ✅ Bon
def calculate_score(points, multiplier=1.0):
    """Calcule le score final du joueur."""
    return points * multiplier

# ❌ Mauvais
def calculateScore(points,multiplier=1.0):
    return points*multiplier
```

### 🟨 **JavaScript (ES6+)**
```javascript
// ✅ Bon
const calculateScore = (points, multiplier = 1.0) => {
    return points * multiplier;
};

// ❌ Mauvais
function calculateScore(points,multiplier){
    return points*multiplier;
}
```

### 🎨 **CSS (BEM)**
```css
/* ✅ Bon */
.terminal__input {
    background-color: #000;
}

.terminal__input--error {
    border-color: #ff0000;
}

/* ❌ Mauvais */
.terminalInput {
    background-color: #000;
}
```

---

## 🧪 TESTS

### 📊 **Tests unitaires**
```python
# tests/test_commands.py
import pytest
from app import app

def test_hack_command():
    """Test de la commande hack_system."""
    with app.test_client() as client:
        response = client.get('/commande?commande=hack_system')
        assert response.status_code == 200
        assert 'HACK RÉUSSI' in response.get_json()['message']
```

### 🔄 **Tests d'intégration**
```python
# tests/test_integration.py
def test_complete_game_flow():
    """Test du flux complet du jeu."""
    # Test tutoriel → mission → badge
    pass
```

### ⚡ **Tests de performance**
```python
# tests/test_performance.py
def test_response_time():
    """Test du temps de réponse."""
    start_time = time.time()
    # Faire une requête
    response_time = time.time() - start_time
    assert response_time < 1.0  # Moins d'1 seconde
```

---

## 📋 CHECKLIST PULL REQUEST

### ✅ **Avant de soumettre**
- [ ] **Code fonctionne** : Tests locaux passent
- [ ] **Tests ajoutés** : Couverture appropriée
- [ ] **Documentation mise à jour** : README, docstrings
- [ ] **Style de code** : PEP 8, ESLint respecté
- [ ] **Commit message** : Conventionnel et descriptif

### ✅ **Description de la PR**
```markdown
## 🎯 Description
Ajoute une nouvelle commande `hack_advanced` avec effets visuels.

## 🔧 Changements
- Nouvelle commande dans `app.py`
- Effets CSS dans `static/css/style.css`
- Tests dans `tests/test_commands.py`
- Documentation dans `README.md`

## 🧪 Tests
- [x] Tests unitaires passent
- [x] Tests d'intégration validés
- [x] Performance vérifiée

## 📸 Screenshots
[Si applicable]

## 🔗 Issues liées
Closes #123
```

---

## 🎮 GUIDELINES SPÉCIFIQUES

### 👦 **Public cible : Ados de 13 ans**
- **Langage adapté** : Vocabulaire gaming, insultes amicales
- **Interface intuitive** : Navigation simple et claire
- **Feedback immédiat** : Réponses rapides et visuelles
- **Gamification** : Badges, points, progression

### 🎯 **Commandes de jeu**
```python
# ✅ Bon - Style rebelle pour ados
def hack_advanced():
    return {
        "message": "BOOM ! Hack avancé réussi ! La Corp va chier dans son clavier !",
        "points": 150,
        "badge": "advanced_hacker"
    }

# ❌ Mauvais - Trop technique
def execute_advanced_hacking_protocol():
    return {
        "message": "Advanced hacking protocol executed successfully.",
        "points": 150,
        "badge": "advanced_hacker"
    }
```

### 🎨 **Interface utilisateur**
- **Design cyberpunk** : Couleurs sombres, effets Matrix
- **Responsive** : Mobile-first design
- **Accessibilité** : Support clavier, navigation
- **Performance** : Animations fluides 60 FPS

---

## 🚨 RÈGLES IMPORTANTES

### ✅ **À faire**
- **Respecter le public** : Ados de 13 ans
- **Tester localement** : Avant chaque commit
- **Documenter** : Code et fonctionnalités
- **Communiquer** : Issues, discussions, feedback

### ❌ **À éviter**
- **Contenu inapproprié** : Violence, langage offensant
- **Bugs de sécurité** : Injections, XSS
- **Performance dégradée** : Temps de réponse > 1s
- **Breaking changes** : Sans migration guide

---

## 🏆 RECONNAISSANCE

### 🌟 **Contributeurs**
- **Badge GitHub** : Apparaître dans les contributeurs
- **Mention README** : Crédits dans la documentation
- **Badge in-game** : Badge spécial "Contributeur"
- **Accès prioritaire** : Nouvelles fonctionnalités

### 🎯 **Niveaux de contribution**
- **Bronze** : 1-5 contributions
- **Argent** : 6-15 contributions
- **Or** : 16-30 contributions
- **Platine** : 30+ contributions

---

## 📞 SUPPORT ET COMMUNICATION

### 💬 **Canaux de communication**
- **GitHub Issues** : Bugs et suggestions
- **GitHub Discussions** : Questions et idées
- **Discord** : Chat en temps réel
- **Email** : contact@arkalia-quest.com

### 🆘 **Besoin d'aide ?**
1. **Vérifier la documentation** : `/docs/`
2. **Chercher dans les issues** : GitHub Issues
3. **Poser une question** : GitHub Discussions
4. **Contacter l'équipe** : Discord ou email

---

## 🎉 MERCI !

### 🌟 **Votre contribution compte !**
Chaque ligne de code, chaque test, chaque documentation aide à créer une meilleure expérience pour les ados qui apprennent la programmation.

### 🚀 **Prêt à contribuer ?**
1. **Fork le projet**
2. **Créez une branche**
3. **Développez votre fonctionnalité**
4. **Soumettez une Pull Request**

### 🎮 **Ensemble, créons le meilleur jeu éducatif !**

---

**🤝 Merci de contribuer à Arkalia Quest ! 🚀** 