# Tests — Arkalia Quest

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
python -m pytest tests/core/ -q              # uniquement core
python -m pytest tests/ -k "luna" -q          # tests dont le nom contient "luna"
python -m pytest tests/api/ tests/core/ -q    # api + core
```

## Scripts de lancement

| Script | Rôle |
|--------|------|
| **./run_tests.sh** (racine) | Lance pytest sur tests/ (script unifié) |
| **python -m pytest tests/** | Commande directe recommandée |
| **tests/run_critical_tests.py** | Sous-ensemble de tests critiques (Luna, gamification, etc.) |
| **tests/run_all_tests.py** | Lance pytest sur tests/ |
| **tests/run_validation_tests.py** | Tests de validation |
| **tests/run_all_tests_stable.py** | Suite stable |
| **scripts/utilitaires/run_tests.sh** | Script bash (unitaires, intégration, perf, couverture) |

**Recommandation :** `python -m pytest tests/` ou `./run_tests.sh` depuis la racine.
