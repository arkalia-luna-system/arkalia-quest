# Release Checklist — v3.1.1

## 1) Validation locale

- [ ] `ruff check .`
- [ ] `black --check .`
- [ ] `python -m pytest tests/ -q`
- [ ] `python -m build` (ou verification CI package si environnement macOS pollue)

## 2) Sécurité et config

- [ ] `SECRET_KEY` forte définie en production
- [ ] Variables rate-limit définies si besoin:
  - [ ] `STORY_RATE_LIMIT_WINDOW_SECONDS`
  - [ ] `STORY_RATE_LIMIT_MAX_POSTS`
- [ ] Endpoint `/health` retourne `200`

## 3) Smoke test fonctionnel

- [ ] Nouveau joueur: accueil -> prénom -> lancement run OK
- [ ] Sauvegarde: reprise de partie OK
- [ ] Journal/profil/classement chargent sans erreur
- [ ] Fin de chapitre -> bouton suite -> transition OK
- [ ] Écran de fin + rejouer + partage OK

## 4) CI/CD

- [ ] Workflow CI vert sur `develop`
- [ ] Workflow CI vert sur `main`
- [ ] Job package vert (build + twine check)
- [ ] Job docker vert (build + smoke test)

## 5) Publication

- [ ] `CHANGELOG` à jour
- [ ] README à jour (section sécurité ops)
- [ ] Tag release créé (ex: `v3.1.1`)
- [ ] Déploiement production déclenché
- [ ] Vérification post-déploiement sur la démo live

## 6) Vérification post-release

- [ ] Logs applicatifs: pas d'erreurs 5xx anormales
- [ ] Aucun pic de `429` inattendu
- [ ] Retour arrière défini (commit/tag précédent identifié)
