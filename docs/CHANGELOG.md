# Changelog — LUNA Hors Connexion

## [Unreleased] — Avril 2026

### Documentation et qualite

- Nettoyage massif des tags techniques parasites (test-permissions + tags hash v3.0.0).
- Conservation d'un set de tags releases significatifs: `v3.0.0-complete`, `v3.0.0-professional`, `v3.1.0`.
- Consolidation de la documentation tags dans ce changelog (suppression du dump historique dédié).
- Suppression du doublon `docs/ARCHITECTURE_TECHNIQUE.md` pour garder une seule source d'architecture.
- Simplification du template de pull request pour reduire le bruit de maintenance.
- Suppression des modules `config/*` non utilises (ancienne couche de config non branchee au runtime actuel).
- Suppression du `config/Dockerfile` duplique et alignement des scripts/build sur le `Dockerfile` racine.
- Simplification de `docker-compose.yml` pour reflecter l'execution reelle (service unique app).
- Ajout de l'URL de demo live Render dans le README.
- Re-audit documentaire au 27/04/2026 (README + docs principales).
- Ajout d'un plan de visibilite (demo live + screenshots/GIF) dans le README.
- Ajout d'un axe roadmap sur la rationalisation des tags Git.
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
- Suppression de scripts utilitaires legacy non relies au projet actuel (`scripts/utilitaires/*`).
- Suppression d'un doublon de rapport de tests historique (`tests/tests/reports/...`).
- Suppression de fichiers legacy non references (anciens rapports, assets de tests HTML manuels, config de charge obsoletes, donnees JSON de l'ancien systeme).
- Verification complete de la suite de tests Python.
- Durcissement API supplementaire: validation UUID cookie, rate-limit POST configurable, header `Retry-After` sur 429, et headers de securite HTTP.
- Stabilisation release packaging: exclusion explicite des artefacts macOS (`._*`) et correction de la detection des paquets Python dans `pyproject.toml`.
- Harmonisation wording frontend: `Hackeur` -> `Hacker` sur profil/classement.
- Renforcement robustesse frontend: `escapeHtml` defensif sur le leaderboard.
- Ajout d'une checklist de release `v3.1.1` dans `docs/RELEASE_CHECKLIST_v3.1.1.md`.

---

Format inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
