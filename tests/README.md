# Tests — LUNA Hors Connexion

## Lancer tous les tests (recommandé)

À la **racine du projet** :

```bash
python -m pytest tests/ -q
```

Avec rapport verbeux :

```bash
python -m pytest tests/ -v
```

Avec couverture :

```bash
python -m pytest tests/ --cov=core --cov-report=term-missing
```

### Lancer un sous-ensemble

```bash
python -m pytest tests/test_story_engine.py -q
python -m pytest tests/test_api_routes.py -q
```

## Scripts de lancement

| Script | Rôle |
|--------|------|
| **./run_tests.sh** (racine) | Lance pytest sur tests/ (script unifié) |
| **python -m pytest tests/** | Commande directe recommandée |

**Recommandation :** `python -m pytest tests/` ou `./run_tests.sh` depuis la racine.
