# 🤝 GUIDE DE CONTRIBUTION - ARKALIA QUEST

> **Comment contribuer au développement d'Arkalia Quest**

---

## 📋 TABLE DES MATIÈRES

1. [🎯 Introduction](#-introduction)
2. [🚀 Premiers Pas](#-premiers-pas)
3. [📝 Guidelines](#-guidelines)
4. [🔧 Développement](#-développement)
5. [🧪 Tests](#-tests)
6. [📚 Documentation](#-documentation)
7. [🔄 Workflow](#-workflow)
8. [🎨 Style de Code](#-style-de-code)
9. [🐛 Signaler un Bug](#-signaler-un-bug)
10. [💡 Proposer une Fonctionnalité](#-proposer-une-fonctionnalité)

---

## 🎯 INTRODUCTION

**Merci de ton intérêt pour contribuer à Arkalia Quest !** 🎮

Ce guide t'aidera à comprendre comment contribuer efficacement au projet. Que tu sois un développeur expérimenté ou un débutant, tes contributions sont les bienvenues !

### 🌟 **POURQUOI CONTRIBUER ?**

- **🎓 Apprendre** : Découvre les technologies modernes
- **🤝 Collaborer** : Travaille avec une communauté passionnée
- **🎮 Créer** : Aide à améliorer un jeu éducatif unique
- **🏆 Reconnaissance** : Ton nom dans les contributeurs

---

## 🚀 PREMIERS PAS

### 📋 **PRÉREQUIS**

- **Python 3.9+**
- **Git**
- **Compte GitHub**
- **Éditeur de code** (VS Code recommandé)

### 🔧 **INSTALLATION LOCALE**

```bash
# 1. Fork le repository
# Va sur https://github.com/arkalia-luna-system/arkalia-quest
# Clique sur "Fork"

# 2. Clone ton fork
git clone https://github.com/ton-username/arkalia-quest.git
cd arkalia-quest

# 3. Ajoute le repository original
git remote add upstream https://github.com/arkalia-luna-system/arkalia-quest.git

# 4. Crée l'environnement virtuel
python -m venv .venv-quest
source .venv-quest/bin/activate  # macOS/Linux
# ou
.venv-quest\Scripts\activate     # Windows

# 5. Installe les dépendances
pip install -r requirements.txt

# 6. Lance le jeu
python app.py
```

### ✅ **VÉRIFICATION**

```bash
# Teste que tout fonctionne
python -m pytest tests/ -v

# Lance le jeu localement
python app.py
# Va sur http://localhost:5001
```

---

## 📝 GUIDELINES

### 🎯 **PRINCIPES GÉNÉRAUX**

1. **Respect** : Sois respectueux envers tous les contributeurs
2. **Qualité** : Écris du code propre et bien documenté
3. **Tests** : Ajoute des tests pour tes nouvelles fonctionnalités
4. **Documentation** : Documente tes changements
5. **Communication** : Communique clairement tes intentions

### 🚫 **CE QU'IL NE FAUT PAS FAIRE**

- ❌ **Code non testé** : Toujours tester avant de soumettre
- ❌ **Breaking changes** : Sans discussion préalable
- ❌ **Code dupliqué** : Réutilise le code existant
- ❌ **Commits énormes** : Fais des commits petits et fréquents
- ❌ **Ignorer les guidelines** : Respecte les conventions

### ✅ **CE QU'IL FAUT FAIRE**

- ✅ **Tests complets** : Couvre tes nouvelles fonctionnalités
- ✅ **Documentation** : Mets à jour la documentation
- ✅ **Code propre** : Suis les conventions de style
- ✅ **Communication** : Explique tes changements
- ✅ **Feedback** : Accepte et donne du feedback constructif

---

## 🔧 DÉVELOPPEMENT

### 🎯 **STRUCTURE DU PROJET**

```
arkalia-quest/
├── app.py                    # Application principale
├── core/                     # Modules principaux
│   ├── command_handler.py    # Gestionnaire de commandes
│   ├── game_engine.py        # Moteur de jeu
│   ├── profile_manager.py    # Gestion des profils
│   ├── database.py          # Base de données
│   └── websocket_manager.py # WebSockets
├── engines/                  # Moteurs spécialisés
│   ├── luna_ai.py           # IA LUNA
│   └── effects_engine.py    # Effets visuels
├── templates/                # Templates HTML
├── static/                   # Assets (CSS, JS, images)
├── data/                     # Données du jeu
├── tests/                    # Tests automatisés
└── docs/                     # Documentation
```

### 🎮 **AJOUTER UNE NOUVELLE COMMANDE**

#### **1. Ajouter dans `core/command_handler.py`**
```python
def handle_nouvelle_commande(self, user_id, args=None):
    """Gère la nouvelle commande"""
    try:
        # Logique de la commande
        result = self.execute_nouvelle_commande(user_id, args)
        
        # Mise à jour du profil
        self.profile_manager.add_xp(user_id, 10)
        
        return {
            'success': True,
            'message': f'Commande exécutée avec succès !',
            'data': result
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erreur : {str(e)}'
        }
```

#### **2. Ajouter dans `app.py`**
```python
# Dans la liste des commandes
COMMANDS = {
    # ... autres commandes ...
    'nouvelle_commande': 'Nouvelle commande cool',
}
```

#### **3. Ajouter des tests**
```python
def test_nouvelle_commande():
    """Test de la nouvelle commande"""
    handler = CommandHandler()
    result = handler.handle_nouvelle_commande('test_user')
    
    assert result['success'] == True
    assert 'Commande exécutée' in result['message']
```

### 🤖 **AMÉLIORER LUNA**

#### **1. Ajouter une réponse dans `engines/luna_ai.py`**
```python
def respond_to_nouvelle_commande(self, user_context):
    """Réponse de LUNA pour la nouvelle commande"""
    user_level = user_context.get('level', 1)
    
    if user_level >= 3:
        return "Ah, tu deviens un vrai hacker ! 🌟"
    else:
        return "Continue comme ça, tu progresses bien ! 💪"
```

#### **2. Ajouter des memes**
```python
# Dans data/personality_data.json
{
  "responses": {
    "nouvelle_commande": [
      "Wow, tu as découvert un secret ! 🕵️",
      "Pas mal du tout, rebelle ! ⚡",
      "Tu me surprends de plus en plus ! 🌙"
    ]
  }
}
```

---

## 🧪 TESTS

### 🎯 **TYPES DE TESTS**

#### **Tests Unitaires**
```python
def test_command_handler():
    """Test du gestionnaire de commandes"""
    handler = CommandHandler()
    
    # Test commande valide
    result = handler.execute('aide', 'test_user')
    assert result['success'] == True
    
    # Test commande invalide
    result = handler.execute('commande_inexistante', 'test_user')
    assert result['success'] == False
```

#### **Tests d'Intégration**
```python
def test_full_game_flow():
    """Test du flux complet du jeu"""
    # Créer un profil
    profile = create_test_profile('test_user')
    
    # Exécuter une mission
    mission_result = execute_mission('mission_1', 'test_user')
    
    # Vérifier la progression
    updated_profile = get_profile('test_user')
    assert updated_profile['xp'] > profile['xp']
```

#### **Tests de Performance**
```python
def test_stress_multiple_users():
    """Test de stress avec plusieurs utilisateurs"""
    users = [f'user_{i}' for i in range(10)]
    
    for user in users:
        result = execute_command('aide', user)
        assert result['success'] == True
    
    # Vérifier la performance
    assert get_response_time() < 0.5  # Moins de 500ms
```

### 🚀 **LANCER LES TESTS**

```bash
# Tous les tests
python -m pytest tests/ -v

# Tests spécifiques
python -m pytest tests/test_arkalia.py -v

# Tests avec couverture
python -m pytest --cov=core --cov-report=html tests/

# Tests de stress
python tests/test_stress_simulation.py
```

### 📊 **COUVERTURE DE CODE**

**Objectif : 90%+ de couverture**

```bash
# Générer le rapport de couverture
python -m pytest --cov=core --cov-report=html tests/

# Ouvrir le rapport
open htmlcov/index.html
```

---

## 📚 DOCUMENTATION

### 🎯 **DOCUMENTER TON CODE**

#### **Docstrings Python**
```python
def handle_commande_avancee(user_id: str, args: dict = None) -> dict:
    """
    Gère une commande avancée avec des fonctionnalités complexes.
    
    Args:
        user_id (str): ID de l'utilisateur
        args (dict, optional): Arguments de la commande
        
    Returns:
        dict: Résultat de l'exécution avec format:
            {
                'success': bool,
                'message': str,
                'data': dict
            }
            
    Raises:
        ValueError: Si les arguments sont invalides
        DatabaseError: Si erreur de base de données
        
    Example:
        >>> result = handle_commande_avancee('user_123', {'param': 'value'})
        >>> print(result['success'])
        True
    """
    pass
```

#### **Commentaires**
```python
# Configuration de l'IA LUNA
LUNA_CONFIG = {
    'personality_traits': {
        'rebellious': 0.8,    # Niveau de rébellion
        'humorous': 0.7,      # Niveau d'humour
        'helpful': 0.9        # Niveau d'aide
    }
}

# Traitement des commandes utilisateur
def process_user_command(command: str) -> dict:
    # 1. Validation de la commande
    if not is_valid_command(command):
        return {'error': 'Commande invalide'}
    
    # 2. Exécution de la commande
    result = execute_command(command)
    
    # 3. Mise à jour des statistiques
    update_user_stats(command)
    
    return result
```

### 📝 **MISE À JOUR DE LA DOCUMENTATION**

#### **README.md**
- Mettre à jour les fonctionnalités
- Ajouter les nouvelles commandes
- Mettre à jour les exemples

#### **CHANGELOG.md**
```markdown
## [3.1.0] - 2025-01-08

### 🎉 Nouvelles Fonctionnalités
- **Nouvelle commande** : `commande_cool` pour faire des trucs cools
- **Amélioration LUNA** : Nouvelles réponses personnalisées

### 🔧 Améliorations
- **Performance** : Optimisation de la base de données
- **Interface** : Nouveaux effets visuels

### 🐛 Corrections
- **Bug** : Correction du problème de sauvegarde
```

#### **FAQ.md**
- Ajouter les nouvelles questions fréquentes
- Mettre à jour les réponses existantes

---

## 🔄 WORKFLOW

### 🎯 **WORKFLOW GIT**

#### **1. Synchroniser avec Upstream**
```bash
# Récupérer les dernières modifications
git fetch upstream
git checkout main
git merge upstream/main
```

#### **2. Créer une Branche**
```bash
# Créer une branche pour ta fonctionnalité
git checkout -b feature/nouvelle-fonctionnalite

# Ou pour un bug fix
git checkout -b fix/correction-bug
```

#### **3. Développer**
```bash
# Faire tes modifications
# Tester ton code
python -m pytest tests/ -v

# Commiter régulièrement
git add .
git commit -m "✨ Ajout nouvelle fonctionnalité

- Ajout de la commande 'commande_cool'
- Tests unitaires complets
- Documentation mise à jour"
```

#### **4. Pousser et Créer la PR**
```bash
# Pousser ta branche
git push origin feature/nouvelle-fonctionnalite

# Créer la Pull Request sur GitHub
```

### 📋 **TEMPLATE PULL REQUEST**

```markdown
## 🎯 Description
Brève description de ce que fait cette PR

## 🔧 Changements
- [ ] Nouvelle fonctionnalité
- [ ] Correction de bug
- [ ] Amélioration de performance
- [ ] Documentation

## 🧪 Tests
- [ ] Tests unitaires ajoutés
- [ ] Tests d'intégration ajoutés
- [ ] Tests de performance effectués
- [ ] Tous les tests passent

## 📚 Documentation
- [ ] Code documenté
- [ ] README mis à jour
- [ ] CHANGELOG mis à jour
- [ ] FAQ mise à jour si nécessaire

## 🎮 Test Manuel
- [ ] Testé localement
- [ ] Fonctionnalités vérifiées
- [ ] Interface testée
- [ ] Pas de régression

## 📸 Screenshots (si applicable)
Ajouter des captures d'écran si l'interface change
```

---

## 🎨 STYLE DE CODE

### 🐍 **PYTHON (PEP 8)**

#### **Nommage**
```python
# Variables et fonctions : snake_case
user_name = "hacker_rebelle"
def calculate_xp(user_id):
    pass

# Classes : PascalCase
class GameEngine:
    pass

# Constantes : UPPER_CASE
MAX_LEVEL = 100
DEFAULT_XP = 50
```

#### **Formatage**
```python
# Imports organisés
import os
import sys
from typing import Dict, List, Optional

import flask
from flask import request, jsonify

# Espacement
def function_with_params(param1, param2, param3):
    """Fonction avec paramètres bien espacés."""
    result = param1 + param2 + param3
    return result

# Indentation : 4 espaces
if condition:
    do_something()
    if nested_condition:
        do_nested_thing()
```

### 🎨 **CSS**

#### **Organisation**
```css
/* Variables CSS */
:root {
    --primary-color: #00ff00;
    --secondary-color: #ff0066;
    --bg-color: #000000;
}

/* Classes utilitaires */
.text-center { text-align: center; }
.mt-20 { margin-top: 20px; }

/* Composants */
.terminal-container {
    background: var(--bg-color);
    color: var(--primary-color);
    padding: 20px;
    border-radius: 10px;
}
```

### ⚡ **JAVASCRIPT**

#### **ES6+ Standards**
```javascript
// Arrow functions
const executeCommand = async (command) => {
    try {
        const response = await fetch('/commande', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cmd: command })
        });
        return await response.json();
    } catch (error) {
        console.error('Erreur:', error);
        throw error;
    }
};

// Destructuring
const { success, message, data } = result;

// Template literals
const userMessage = `Bienvenue ${username} ! Niveau ${level}`;
```

---

## 🐛 SIGNALER UN BUG

### 🎯 **TEMPLATE BUG REPORT**

```markdown
## 🐛 Description du Bug
Description claire et concise du bug

## 🔄 Étapes pour Reproduire
1. Va sur '...'
2. Clique sur '...'
3. Tape '...'
4. Voir l'erreur

## ✅ Comportement Attendu
Ce qui devrait se passer

## ❌ Comportement Actuel
Ce qui se passe actuellement

## 📸 Screenshots
Ajouter des captures d'écran si applicable

## 💻 Environnement
- **OS** : macOS/Windows/Linux
- **Navigateur** : Chrome/Firefox/Safari
- **Version** : 3.0.0
- **URL** : https://arkalia-quest-1.onrender.com

## 📋 Informations Supplémentaires
Toute information supplémentaire utile
```

### 🔍 **INFORMATIONS UTILES**

#### **Logs d'Erreur**
```bash
# Logs du navigateur (F12 → Console)
# Logs du serveur (si accès)
# Screenshots de l'erreur
```

#### **Contexte**
- **Navigateur** et version
- **OS** et version
- **Actions** effectuées avant le bug
- **Données** utilisées

---

## 💡 PROPOSER UNE FONCTIONNALITÉ

### 🎯 **TEMPLATE FEATURE REQUEST**

```markdown
## 💡 Description de la Fonctionnalité
Description claire de la fonctionnalité souhaitée

## 🎯 Problème Résolu
Quel problème cette fonctionnalité résout-elle ?

## 💭 Solution Proposée
Comment cette fonctionnalité devrait fonctionner ?

## 🔄 Alternatives Considérées
Autres solutions possibles

## 📊 Impact
- **Utilisateurs** : Qui en bénéficie ?
- **Performance** : Impact sur les performances ?
- **Complexité** : Niveau de complexité ?

## 🎮 Exemples d'Usage
Comment les utilisateurs l'utiliseraient ?

## 📋 Checklist
- [ ] Fonctionnalité clairement définie
- [ ] Impact évalué
- [ ] Alternatives considérées
- [ ] Exemples fournis
```

### 🎯 **CRITÈRES D'ACCEPTATION**

#### **Fonctionnalités Prioritaires**
- **Éducatif** : Améliore l'apprentissage
- **Engagement** : Augmente l'engagement des joueurs
- **Performance** : N'impacte pas les performances
- **Maintenabilité** : Code propre et testable

#### **Fonctionnalités Secondaires**
- **Innovation** : Apporte quelque chose de nouveau
- **Communauté** : Bénéficie à la communauté
- **Compatibilité** : Compatible avec l'existant

---

## 🎉 RECONNAISSANCE

### 🌟 **CONTRIBUTEURS**

Tous les contributeurs sont reconnus dans :
- **README.md** : Liste des contributeurs
- **CHANGELOG.md** : Historique des contributions
- **GitHub** : Profils GitHub liés

### 🏆 **BADGES CONTRIBUTEUR**

- **🥇 Gold Contributor** : 10+ PRs mergées
- **🥈 Silver Contributor** : 5+ PRs mergées
- **🥉 Bronze Contributor** : 1+ PR mergée
- **🌟 Special Contributor** : Contributions exceptionnelles

### 📢 **COMMUNICATION**

- **Discussions GitHub** : Questions et idées
- **Issues** : Bugs et fonctionnalités
- **Pull Requests** : Code et améliorations
- **Email** : support@arkalia-quest.com

---

## 🚀 PROCHAINES ÉTAPES

### 🎯 **FONCTIONNALITÉS PRIORITAIRES**

1. **IA Machine Learning** : LUNA encore plus intelligente
2. **WebSockets réels** : Communication temps réel
3. **Nouvelles missions** : Contenu additionnel
4. **Mobile app** : Application native

### 🤝 **COMMENT COMMENCER**

1. **Lis la documentation** : Comprends le projet
2. **Installe localement** : Configure ton environnement
3. **Choisis une tâche** : Issue labellisée "good first issue"
4. **Développe** : Code, teste, documente
5. **Soumet** : Pull Request avec description claire

### 📞 **BESOIN D'AIDE ?**

- **GitHub Discussions** : Questions générales
- **Issues** : Problèmes spécifiques
- **Email** : support@arkalia-quest.com
- **Documentation** : Guides détaillés

---

**Merci de contribuer à Arkalia Quest ! Ensemble, nous créons la prochaine génération de hackers éthiques ! 🎮✨**

---

*Guide de contribution créé avec ❤️ par l'équipe Arkalia Quest*  
*Version 3.0 - 2025* 