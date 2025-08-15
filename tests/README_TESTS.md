---
**Statut : ACTIF**
**Dernière mise à jour : Juillet 2025**
**Résumé :** Guide des tests automatisés et manuels pour Arkalia Quest.

**Liens utiles :**
- [Documentation principale](../docs/README.md)
- [Statut projet](../docs/STATUT_PROJET_ACTUEL.md)
---

## Sommaire
- [Introduction](#introduction)
- [Structure des tests](#structure-des-tests)
- [Lancer les tests](#lancer-les-tests)
- [Bonnes pratiques](#bonnes-pratiques)
- [FAQ](#faq)

# 🧪 GUIDE COMPLET DES TESTS - ARKALIA QUEST

## 📁 Structure des Tests

```
tests/
├── README_TESTS.md                 # Ce guide
├── run_all_tests.py               # Script de lancement unifié
├── test_manager.py                # Gestionnaire centralisé des tests
├── results/                       # Résultats individuels des tests
│   ├── test_boutons_rapide_*.json
│   ├── test_tutoriel_*.json
│   └── ...
├── reports/                       # Rapports globaux et historiques
│   ├── complete_test_report_*.json
│   ├── global_test_report_*.json
│   └── ...
├── scripts/                       # Tests de scripts individuels
│   ├── test_boutons_rapide.py
│   ├── test_tutoriel.py
│   ├── test_interface_complete.py
│   ├── test_os2142_complete.py
│   └── test_phase1_complete.py
├── test_ui_boutons_actions_experience.py
├── test_ui_navigation_experience.py
├── test_ui_terminal_experience.py
├── test_ui_pwa_mobile_experience.py
├── test_ui_tutoriel_experience.py
├── test_stable_version_complete.py
├── test_security_complete.py
├── test_performance_stress.py
├── test_gamification_complete.py
└── test_complet_arkalia.py
```

## 🚀 Lancement des Tests

### Option 1: Tous les tests (Recommandé)
```bash
cd tests
python run_all_tests.py
```

### Option 2: Tests individuels
```bash
# Test rapide des boutons
python scripts/test_boutons_rapide.py

# Test du tutoriel
python scripts/test_tutoriel.py

# Test d'expérience utilisateur
python test_ui_boutons_actions_experience.py
```

### Option 3: Tests par catégorie
```bash
# Tests d'expérience utilisateur
python run_all_experience_tests.py

# Tests de stabilité
python run_all_tests_stable.py
```

## 📊 Types de Tests

### 🎮 Tests d'Expérience Utilisateur
- **test_ui_boutons_actions_experience.py**: Test des boutons et actions
- **test_ui_navigation_experience.py**: Test de la navigation
- **test_ui_terminal_experience.py**: Test de l'expérience terminal
- **test_ui_pwa_mobile_experience.py**: Test mobile et PWA
- **test_ui_tutoriel_experience.py**: Test du tutoriel interactif

### 🔧 Tests de Stabilité
- **test_stable_version_complete.py**: Test de version stable
- **test_security_complete.py**: Tests de sécurité
- **test_performance_stress.py**: Tests de performance
- **test_gamification_complete.py**: Tests de gamification
- **test_complet_arkalia.py**: Test complet du jeu

### 📜 Tests de Scripts
- **test_boutons_rapide.py**: Test rapide des boutons
- **test_tutoriel.py**: Test du tutoriel
- **test_interface_complete.py**: Test complet de l'interface
- **test_os2142_complete.py**: Test OS2142
- **test_phase1_complete.py**: Test de la phase 1

## 📋 Gestion des Résultats

### Sauvegarde Automatique
- **Résultats individuels**: `tests/results/`
- **Rapports globaux**: `tests/reports/`
- **Format**: JSON avec timestamp et session ID

### Structure des Résultats
```json
{
  "test_name": "nom_du_test",
  "session_id": "20250709_133500",
  "timestamp": "2025-07-09T13:35:00.123456",
  "success": true,
  "duration": 12.34,
  "result": {
    // Résultats spécifiques au test
  }
}
```

## 🔧 Configuration

### Prérequis
1. Serveur Arkalia Quest démarré (`python app.py`)
2. Port 5001 accessible
3. Dépendances installées (`pip install -r requirements.txt`)

### Variables d'Environnement
- `ARKALIA_TEST_URL`: URL du serveur (défaut: http://localhost:5001)
- `ARKALIA_TEST_TIMEOUT`: Timeout des tests (défaut: 300s)

## 📈 Analyse des Résultats

### Rapports Automatiques
- **Rapport global**: Résumé de tous les tests
- **Rapport par catégorie**: Détails par type de test
- **Historique**: Conservation des résultats précédents

### Métriques Clés
- **Taux de réussite**: Pourcentage de tests réussis
- **Durée moyenne**: Temps d'exécution des tests
- **Tests critiques**: Tests de sécurité et stabilité
- **Tests UX**: Tests d'expérience utilisateur

## 🐛 Dépannage

### Problèmes Courants

#### Serveur non accessible
```bash
# Vérifier que le serveur tourne
python app.py

# Vérifier le port
lsof -i :5001
```

#### Tests qui échouent
1. Vérifier les logs du serveur
2. Consulter les rapports d'erreur dans `tests/results/`
3. Relancer les tests individuels

#### Timeout des tests
- Augmenter le timeout dans `run_all_tests.py`
- Vérifier la performance du serveur
- Réduire le nombre de tests simultanés

### Logs et Debug
- **Logs serveur**: Console où `python app.py` est lancé
- **Logs tests**: Sortie des scripts de test
- **Rapports détaillés**: Fichiers JSON dans `tests/reports/`

## 🔄 Maintenance

### Nettoyage des Anciens Résultats
```bash
# Supprimer les résultats de plus de 30 jours
find tests/results -name "*.json" -mtime +30 -delete
find tests/reports -name "*.json" -mtime +30 -delete
```

### Ajout de Nouveaux Tests
1. Créer le fichier de test dans le bon dossier
2. Ajouter le test au script `run_all_tests.py`
3. Documenter le test dans ce README
4. Tester et valider

### Mise à Jour de la Documentation
- Maintenir ce README à jour
- Documenter les nouveaux types de tests
- Mettre à jour les exemples

## 📞 Support

Pour toute question sur les tests :
1. Consulter les rapports d'erreur
2. Vérifier la documentation
3. Tester manuellement les fonctionnalités
4. Consulter les logs du serveur

---

**Dernière mise à jour**: 9 juillet 2025
**Version**: 2.0 - Structure organisée et centralisée 