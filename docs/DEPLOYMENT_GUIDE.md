# Guide de Deploiement — LUNA Hors Connexion

Mise a jour: **26 avril 2026**

## Prerequis

- Python 3.9+
- `pip`
- Acces ecriture au dossier `data/`

## Deploiement local (reference)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Application disponible sur `http://localhost:5001`.

## Deploiement Gunicorn

```bash
pip install -r requirements.txt
gunicorn -c gunicorn.conf.py app:app
```

## Deploiement Docker

```bash
docker build -t luna-hors-connexion .
docker run -p 5001:5001 luna-hors-connexion
```

## Variables utiles

- `SECRET_KEY` (obligatoire en production)
- `PORT` (selon plateforme)
- `FLASK_ENV=production`

## Checklist avant mise en prod

- `python -m pytest -q` OK
- `ruff check .` OK
- `README.md` et `docs/` a jour
- branche `develop` validee puis fusion vers branches cibles
