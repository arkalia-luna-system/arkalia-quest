# Index de la documentation — Arkalia Quest

Guide de navigation dans la documentation du projet. *Dernière mise à jour : 7 février 2026.*

---

## 🎯 **DOCUMENTATION PRINCIPALE**

### **📖 Fichiers Essentiels**

- **[POINT_PROJET_2026.md](POINT_PROJET_2026.md)** — Faire le point : checklist complète, fait / reste, métriques, références (7 fév. 2026).
- **[README.md](../README.md)** - Documentation principale du projet
- **[CHANGELOG.md](../CHANGELOG.md)** - Historique des versions
- **[README_UTILISATION.md](README_UTILISATION.md)** - Guide utilisateur (docs)
- **[START_SCRIPTS.md](../START_SCRIPTS.md)** - Scripts de démarrage (start.sh, start_optimized.sh, etc.)

### **🏗️ Architecture & Technique**

- **[ARCHITECTURE_TECHNIQUE.md](ARCHITECTURE_TECHNIQUE.md)** - Architecture complète
- **[ROADMAP_STRATEGIQUE.md](ROADMAP_STRATEGIQUE.md)** - Feuille de route
- **[STATUT_PROJET_ACTUEL.md](STATUT_PROJET_ACTUEL.md)** - État actuel du projet

### **👨‍💻 Guides Développeur**

- **[GUIDE_DEVELOPPEMENT.md](GUIDE_DEVELOPPEMENT.md)** - Guide de développement
- **[GUIDE_TECHNIQUE_DEVELOPPEUR.md](GUIDE_TECHNIQUE_DEVELOPPEUR.md)** - Guide technique
- **[GUIDE_DEPLOIEMENT.md](GUIDE_DEPLOIEMENT.md)** - Guide de déploiement (voir aussi [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) et config/platforms.md)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guide de contribution

---

## 📊 **RAPPORTS & ANALYSES**

### **🧪 Tests & Qualité**

- **[../tests/README.md](../tests/README.md)** - Lancer les tests (pytest depuis la racine, scripts disponibles)
- **[CHECKLISTS_TEST_UTILISATEUR.md](CHECKLISTS_TEST_UTILISATEUR.md)** - Checklists de tests
- **[TEST_PLAN_UTILISATEUR.md](TEST_PLAN_UTILISATEUR.md)** - Plan de tests utilisateur
- **[GUIDE_TEST_UTILISATEUR.md](GUIDE_TEST_UTILISATEUR.md)** - Guide de tests

### Rapports et audits

- **[../RAPPORT_AUDIT_COMPLET_PROJET.md](../RAPPORT_AUDIT_COMPLET_PROJET.md)** — Audit complet (racine) : exploitation 100 %, static/config/docs, url_for, LUNA. Voir [rapports/README.md](rapports/README.md).
- **[rapports/RAPPORT_AUDIT_PROJET.md](rapports/RAPPORT_AUDIT_PROJET.md)** — Audit projet (7 fév. 2026)
- **[audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md](audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md)** — Audit UX vs meilleurs jeux 2024–2025, promesse 15 mots, prochaines étapes
- **[AUDIT_ET_REVISION_CONCEPT.md](AUDIT_ET_REVISION_CONCEPT.md)** — Audit complet du projet + révision du concept (abandon du terminal, nouveau concept narratif/exploration)
- **[PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md)** — Guide playtest 15 min pour ados (scénario, grille, indicateurs)
- **[COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md)** — Pourquoi le jeu peut sembler nul vs autres (sources 2024–2025), fun / game feel / onboarding ; tableau « Couverture des pages » (game-feel + focus + reduced-motion sur les 13 pages)
- **[CHEMIN_NULL_VERS_SUPER.md](CHEMIN_NULL_VERS_SUPER.md)** — Ce qui a été fait pour passer de « null » à « super » (choix, fonds, émotions, ambiance, aide unifiée, visuel minimal) et ce qui reste (playtests) ; commandes Git pour push
- **[REPARTIR_SUR_DES_BASES_SANES.md](REPARTIR_SUR_DES_BASES_SANES.md)** — Diagnostic visuel/comportement, plan (visuel minimal), questionnaire ; visuel minimal appliqué partout
- **[REFONTE_VISUELLE_2026.md](REFONTE_VISUELLE_2026.md)** — Ancienne refonte « Nuit émotionnelle » (ambre/cyan) ; désormais **visuel minimal** unifié : [REPARTIR_SUR_DES_BASES_SANES.md](REPARTIR_SUR_DES_BASES_SANES.md) et `static/css/arkalia-minimal.css` sur toutes les pages.
- **[reports/README.md](reports/README.md)** — Rapports d’évaluation
- **[../reports/PLAN_AMELIORATION_TESTS_ADO.md](../reports/PLAN_AMELIORATION_TESTS_ADO.md)** — Plan d'amélioration tests
- **[../reports/RAPPORT_OPTIMISATION_PERFORMANCE.md](../reports/RAPPORT_OPTIMISATION_PERFORMANCE.md)** — Optimisations

---

## 🗂️ **ORGANISATION DES FICHIERS**

### **📁 Autres dossiers clés**

- **static/** : `css/` (41 fichiers), `js/` (62 fichiers), `icons/`, `images/`, `manifest.json` — voir rapport d’audit complet pour détails (orphelins, scripts commentés).
- **config/** : Configuration app (settings.py, config.example.py), déploiement (Procfile, Dockerfile, railway.json, etc.), pytest.ini, platforms.md (guide déploiement multi-plateformes).
- **Regroupement CSS/JS** : [CSS_JS_BUNDLES.md](CSS_JS_BUNDLES.md) — groupes par type de page, bundle `arkalia-bundle-pages.css` disponible.

### **📁 Structure Recommandée**

```
docs/
├── INDEX_DOCUMENTATION.md          # Ce fichier
├── README.md                       # Documentation principale
├── ARCHITECTURE_TECHNIQUE.md       # Architecture
├── ROADMAP_STRATEGIQUE.md          # Roadmap
├── STATUT_PROJET_ACTUEL.md         # Statut actuel
├── GUIDE_DEVELOPPEMENT.md          # Guide dev
├── GUIDE_DEPLOIEMENT.md            # Guide déploiement
├── CONTRIBUTING.md                 # Contribution
├── versions/                       # Versions
│   ├── CHANGELOG.md
│   └── CHANGELOG_v3.0.0.md
├── rapports/                       # Rapports actifs
│   ├── README.md
│   └── RAPPORT_AUDIT_PROJET.md
├── audits/                        # Audits (résumé + lien consolidé)
│   ├── README.md
│   └── RESUME_AUDIT_FINAL.md
└── archive/                       # Archives
    ├── README_ARCHIVE.md
    ├── rapports/                  # Anciens rapports
    └── audits/                    # Audits détaillés
```

### Archives

- Rapports obsolètes dans `docs/archive/` et `docs/archive/rapports/` (voir [README_ARCHIVE.md](archive/README_ARCHIVE.md)).

---

## 🎯 **NOUVELLES FONCTIONNALITÉS V3.2.0**

### **🌙 LUNA AI V3**

- Machine Learning intégré
- Mémoire à long terme
- Personnalité évolutive
- Moteur prédictif

### **🎯 Défis Quotidiens**

- 6 types de défis (Hacking, Programming, Logic, etc.)
- Système de streaks
- Leaderboard hebdomadaire
- Récompenses dynamiques

### **🎨 Thèmes Alternatifs**

- Matrix (classique)
- Cyberpunk
- Neon
- Dark Mode
- Retro
- Ocean

### **⚡ Optimisations Performance**

- Réduction 95% des appels API
- Throttling intelligent
- Chargement optimisé
- Monitoring avancé

---

## 🔧 **MAINTENANCE DE LA DOCUMENTATION**

### **✅ Règles de Mise à Jour**

1. **Version** : Toujours mettre à jour la version dans les badges
2. **Dates** : Utiliser le format YYYY-MM-DD
3. **Statut** : Maintenir le statut à jour
4. **Liens** : Vérifier les liens internes
5. **Cohérence** : Garder le même style et format

### **📝 Template de Mise à Jour**

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Ajouté
- ✨ Nouvelle fonctionnalité

### Amélioré
- 🔧 Amélioration existante

### Corrigé
- ❌ Correction de bug
```

---

## 🗺️ **PAGES & FONCTIONNALITÉS (EXPLOITATION 100 %)**

- **Accueil** `/` — **Aventure** `/histoire` — **Terminal** `/terminal` — **Monde** `/monde` — **Profil** `/profil` — **Classement** `/leaderboard` (avec onglets par catégorie) — **Dashboard** `/dashboard` (défis du jour, accès rapide) — **Compétences** `/skill-tree` — **Tutoriel** `/tutorial` — **Explorateur** `/explorateur` — **Mail** `/mail` — **Audio** `/audio` — **Tutoriels techniques** `/technical-tutorials` — **Accessibilité** `/accessibility`.

---

## 🎮 **ARKALIA QUEST V3.2.0 - STATUT FINAL**

**✅ PRODUCTION READY**

- **Tests** : 225/225 PASS
- **Performance** : 98%
- **Sécurité** : Bandit ✓
- **Documentation** : Complète et à jour

**🚀 Prêt pour la Phase 2** (Multijoueur, Guildes, Boss Fights)

---

*Dernière mise à jour : 7 février 2026*
