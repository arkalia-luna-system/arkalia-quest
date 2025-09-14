# 🎮 Configuration de Contribution GitHub - Arkalia Quest

## 🎯 Vue d'Ensemble

Ce guide explique comment configurer et utiliser les outils de contribution GitHub pour Arkalia Quest. Ces outils facilitent la collaboration et améliorent l'expérience des contributeurs.

## 🚀 Configuration Rapide

### 1. Prérequis

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier que tout est prêt
python scripts/setup_github_contribution.py
```

### 2. Configuration avec Token GitHub (Optionnel)

```bash
# Définir le token GitHub
export GITHUB_TOKEN=your_github_token_here

# Exécuter la configuration complète
python scripts/setup_github_contribution.py
```

## 📋 Éléments Configurés

### ✅ Templates d'Issues

#### 🐛 Bug Report (`bug_report.yml`)
- Description structurée du bug
- Étapes de reproduction
- Comportement attendu vs actuel
- Informations sur l'environnement
- Logs d'erreur

#### ✨ Feature Request (`feature_request.yml`)
- Description de la fonctionnalité
- Problème résolu
- Solution proposée
- Priorité et complexité
- Cas d'usage

#### 🤝 Help Wanted (`help_wanted.yml`)
- Tâches pour les contributeurs
- Critères d'acceptation
- Niveau de difficulté
- Compétences nécessaires
- Guide de démarrage

#### ⚙️ Configuration (`config.yml`)
- Liens vers les ressources
- Redirections vers les templates
- Désactivation des issues vides

### ✅ Template de Pull Request

#### 📝 Template Complet (`pull_request_template.md`)
- Description des changements
- Type de changement
- Tests effectués
- Documentation mise à jour
- Checklist de contribution
- Impact et liens

### ✅ Scripts de Configuration

#### 🏷️ Labels GitHub (`setup_github_labels.py`)
- 30+ labels organisés par catégories
- Priorité, types, contribution, technique
- Spécifique au projet (luna-ai, gamification)
- Taille et complexité

#### 💬 Discussions GitHub (`setup_github_discussions.py`)
- 10 catégories de discussions
- Templates pour questions et idées
- Guide d'utilisation complet

#### 🎮 Configuration Complète (`setup_github_contribution.py`)
- Vérification de l'environnement
- Tests de qualité du code
- Configuration de tous les éléments
- Génération de documentation

## 🛠️ Utilisation

### Configuration Manuelle (Sans Token)

```bash
# Vérifier l'environnement
source venv/bin/activate

# Tester la configuration
python scripts/setup_github_contribution.py
```

### Configuration Automatique (Avec Token)

```bash
# Définir le token
export GITHUB_TOKEN=your_token_here

# Configuration complète
python scripts/setup_github_contribution.py

# Ou configuration individuelle
python scripts/setup_github_labels.py
python scripts/setup_github_discussions.py
```

### Activation Manuelle Requise

1. **Discussions GitHub** :
   - Aller dans Settings → Features → Discussions
   - Activer les discussions
   - Créer les catégories recommandées

2. **Labels GitHub** :
   - Vérifier que les labels sont créés
   - Ajuster les couleurs si nécessaire

## 📚 Documentation Générée

### 📋 Fichiers Créés

- `.github/ISSUE_TEMPLATE/` - Templates d'issues
- `.github/pull_request_template.md` - Template de PR
- `docs/GITHUB_LABELS.md` - Documentation des labels
- `docs/GITHUB_DISCUSSIONS_GUIDE.md` - Guide des discussions
- `docs/CONTRIBUTION_SETUP_SUMMARY.md` - Résumé de configuration

### 🎯 Utilisation des Templates

#### Pour les Issues
1. Aller sur GitHub → Issues → New Issue
2. Choisir le template approprié
3. Remplir les sections requises
4. Assigner les labels appropriés

#### Pour les Pull Requests
1. Créer une nouvelle PR
2. Le template s'affiche automatiquement
3. Remplir les sections pertinentes
4. Cocher les éléments de la checklist

## 🔧 Maintenance

### Mise à Jour des Templates

```bash
# Modifier les fichiers dans .github/ISSUE_TEMPLATE/
# Les changements sont immédiatement visibles sur GitHub
```

### Ajout de Nouveaux Labels

```bash
# Modifier scripts/setup_github_labels.py
# Ajouter le nouveau label dans la liste self.labels
python scripts/setup_github_labels.py
```

### Mise à Jour de la Documentation

```bash
# Les scripts génèrent automatiquement la documentation
# Vérifier les fichiers dans docs/
```

## 🎯 Bonnes Pratiques

### Pour les Contributeurs

1. **Utiliser les templates** : Toujours utiliser les templates appropriés
2. **Labels appropriés** : Assigner les bons labels aux issues/PR
3. **Description claire** : Remplir toutes les sections requises
4. **Tests** : Vérifier que les tests passent avant de soumettre

### Pour les Mainteneurs

1. **Révision des templates** : Vérifier régulièrement les templates
2. **Labels cohérents** : Maintenir la cohérence des labels
3. **Documentation** : Mettre à jour la documentation
4. **Feedback** : Collecter les retours des contributeurs

## 🚨 Dépannage

### Problèmes Courants

#### Token GitHub Non Valide
```bash
# Vérifier le token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

#### Permissions Insuffisantes
- Vérifier que le token a les bonnes permissions
- Repository : Contents, Issues, Pull Requests, Discussions

#### Templates Non Visibles
- Vérifier que les fichiers sont dans `.github/ISSUE_TEMPLATE/`
- S'assurer que les fichiers ont l'extension `.yml`

### Logs et Debug

```bash
# Exécuter avec debug
python -u scripts/setup_github_contribution.py

# Vérifier les fichiers générés
ls -la .github/
ls -la docs/GITHUB_*
```

## 🎉 Résultat

Avec cette configuration, votre projet Arkalia Quest dispose de :

- ✅ **Templates professionnels** pour issues et PR
- ✅ **Labels organisés** pour la classification
- ✅ **Discussions structurées** pour la collaboration
- ✅ **Documentation complète** pour les contributeurs
- ✅ **Scripts automatisés** pour la maintenance

## 📞 Support

Pour des questions ou problèmes :
- Consulter ce guide
- Vérifier les logs d'erreur
- Ouvrir une issue avec le template approprié
- Utiliser les discussions GitHub

---

*Configuration optimisée pour Arkalia Quest - Projet éducatif innovant* 🎮✨
