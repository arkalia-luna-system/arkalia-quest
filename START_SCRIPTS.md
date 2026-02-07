# Scripts de démarrage et tests — Arkalia Quest

## Démarrage unifié (racine)

| Commande | Usage |
|----------|--------|
| `./start.sh` ou `./start.sh dev` | Développement : venv + `python app.py` — port 5001 |
| `./start.sh prod` | Production : Gunicorn si dispo, sinon Flask (arrête processus existants) |
| `./start.sh eval` | Évaluation : lance l’app, vérifie http://localhost:5001, affiche les guides |

**Alias :**  
- `./start_optimized.sh` → `./start.sh prod`  
- `./start_evaluation.sh` → `./start.sh eval`

## Tests

| Commande | Usage |
|----------|--------|
| `./run_tests.sh` | Lance pytest sur `tests/` (mode court) |
| `./run_tests.sh -v` | Mode verbeux |
| `./run_tests.sh tests/core/` | Sous-ensemble de tests |

Voir aussi : `scripts/utilitaires/run_tests.sh` (tests unitaires / intégration / couverture).

## Autres

- **scripts/deploiement/start_gunicorn.sh** — Déploiement serveur (Gunicorn)
- **scripts/utilitaires/start_arkalia.sh** — Utilitaire interne

**Recommandation :** pour le dev quotidien, utiliser `./start.sh` à la racine.
