# Changelog — LUNA Hors Connexion

## [Unreleased] — Avril 2026

### Documentation et qualite
- Audit complet de coherence (README + docs principales).
- Mise a jour des documents d'architecture sur l'etat reel du code.
- Mise a jour de la roadmap et de la vision produit.
- Simplification du guide de contribution et de deploiement.

### Qualite code
- Correction des erreurs Ruff (imports et hygiene tests).
- Alignement du formatage Python sur Black 25.1.0 pour corriger le pipeline CI.
- Durcissement securite/API (SECRET_KEY obligatoire en production, erreurs internes masquees cote client).
- Unification de la logique de rang hacker entre jeu et profil via un module partage.
- Nettoyage de `env.example` pour supprimer les variables legacy non utilisees et aligner les variables runtime reelles.
- Lancement `app.py` pilote par variables d'environnement (`HOST`, `PORT`, `FLASK_DEBUG`) au lieu d'un debug force.
- Verification complete de la suite de tests Python.

---

Format inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
