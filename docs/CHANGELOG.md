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
- Alignement du formatage Python sur Black 26.3.1 pour corriger le pipeline CI.
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
- Durcissement runtime: parsing robuste des variables d'environnement (`PORT`, limites payload), header HSTS en production.
- Gestion explicite `413` pour `/api/*` avec message JSON clair.
- Durcissement des reponses API: headers anti-cache (`no-store`) et format d'erreurs JSON uniforme (`404`, `500`).
- Audit securite dependances projet via `pip-audit` et mise a niveau de `black`/`pytest` vers versions non vulnerables.
- Nettoyage repository: suppression du doublon `.github/pull_request_template.md`.
- Suppression de `build.sh` legacy (non reference et destructif pour `pyproject.toml`).
- Remise a plat de `mkdocs.yml` avec une navigation alignee sur les documents existants.
- Ajout de `docs/index.md` comme page d'accueil MkDocs.
- Suppression des scripts Docker legacy redondants: `scripts/test-docker.sh` et `scripts/docker-diagnostic.sh`.
- Modernisation de `scripts/deploy.sh` et `scripts/docker-auth.sh` (bash strict, robustesse shell, message de sortie aligne sur l'app).
- Suppression de modules Python dormants non references: `engines/luna_ai_v3.py` et `utils/logger.py`.
- Nettoyage des paquets `engines` et `utils` pour supprimer les imports casses/legacy.
- Rationalisation deployment/config: suppression des descriptors legacy non relies au runtime principal (`config/cloudbuild.yaml`, `config/digitalocean.yaml`, `config/railway.json`, `config/Procfile`, `config/runtime.txt`, `config/app.json`, `config/nginx.conf`, `config/pytest.ini`).
- Suppression des manifests Kubernetes dormants (`k8s/k8s-deployment.yaml`, `k8s/k8s-service.yaml`) et de `config/systemd/arkalia-quest.service`.
- Simplification de `scripts/deploy.sh` pour limiter les cibles aux plateformes maintenues (`local`, `docker`, `docker-build`, `render`).
- Rationalisation des dependances Python: suppression des paquets non utilises (websocket/async/monitoring/scraping/crypto) et alignement `requirements.txt` + `pyproject.toml` sur les usages reels.
- Polish documentation final: guide de deploiement aligne sur les cibles maintenues et corrections wording roadmap.
- Nettoyage final MkDocs: ajout de `docs/assets/README.md` dans la navigation et exclusion des artefacts `._*`.
- Nettoyage final structure: suppression du test legacy 100% skip `tests/api/test_app_routes_basic.py` et de la config Elastic Beanstalk obsolete `config/.ebextensions/01_packages.config`.
- Rationalisation outillage racine: refonte du `Makefile` pour ne garder que des cibles maintenues, alignees avec la stack actuelle (tests/lint/docs/security/build/run/docker).
- Ajout d'une observabilite gameplay locale via `POST /api/story/telemetry` (events anonymises scene/choix/fin/UI).
- Ajout d'un panneau d'accessibilite in-game (contraste renforce, reduction animations, vitesse de texte configurable).
- Renforcement des tests contractuels API (`/api/story/state`) et tests d'acceptation/rejet pour la route telemetry.
- Rework gameplay "fun-first": hook d'ouverture plus agressif (fenetre 4 minutes), nouveau systeme de pression `threat_level` (traque La Corp) expose API+HUD, et feedback immediate des choix risqués.
- Ajout d'une route narrative secrete (Fin D: "Signal Fantome"), compteur de fins et rangs hacker mis a jour pour 4 fins, et nouveaux moments "wow" en progression de chapitre.
- Ajout d'un systeme "secrets detectes" en run (5 secrets caches), avec unlock visuel instantane, compteur `Secrets x/5` en HUD, persistance serveur, et telemetry `secret_detected`.
- Ajout d'une meta-progression secrets sur le profil (`x/5`), badge `Secret Master` a 5/5, support de la Fin D sur la page profil, et recompense cosmetique in-game quand tous les secrets sont trouves.

---

Format inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
