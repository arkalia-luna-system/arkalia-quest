# Déploiement

## Local (smoke rapide)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Production (Gunicorn)

```bash
gunicorn -c gunicorn.conf.py app:app
```

## Docker (option)

```bash
docker build -t luna-hors-connexion .
docker run -p 5001:5001 luna-hors-connexion
```

## Variables critiques

- `SECRET_KEY` (prod obligatoire)
- `APP_ENV=production`
- `FLASK_DEBUG=0`

## Gate avant déploiement

- `python -m pytest -q`
- `ruff check .`
- `black --check .`
