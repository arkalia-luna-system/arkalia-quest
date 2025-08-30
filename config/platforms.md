# 🚀 Guide de Déploiement - Arkalia Quest

Ce guide couvre le déploiement d'Arkalia Quest sur différentes plateformes cloud et d'hébergement.

## 📋 **Plateformes Supportées**

- [Heroku](#heroku)
- [Render](#render)
- [Railway](#railway)
- [DigitalOcean App Platform](#digitalocean)
- [AWS Elastic Beanstalk](#aws)
- [Google Cloud Run](#gcp)
- [Docker](#docker)

---

## 🎯 **Heroku**

### **Déploiement Rapide**
```bash
# Installation de Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Création de l'app
heroku create arkalia-quest-demo

# Configuration des variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Déploiement
git push heroku main

# Ouverture
heroku open
```

### **Configuration Heroku**
- **Buildpack** : `heroku/python`
- **Port** : `$PORT` (automatique)
- **Workers** : 2-4 selon le plan

---

## 🌐 **Render**

### **Déploiement via Git**
1. **Connectez** votre repo GitHub
2. **Créez** un nouveau Web Service
3. **Configuration** :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`

### **Variables d'Environnement**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
PYTHON_VERSION=3.11.13
```

---

## 🚂 **Railway**

### **Déploiement Automatique**
```bash
# Installation Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialisation
railway init

# Déploiement
railway up
```

### **Configuration**
- **Runtime** : Python 3.11
- **Start Command** : `gunicorn app:app --bind 0.0.0.0:$PORT`

---

## 🌊 **DigitalOcean App Platform**

### **Déploiement via Dashboard**
1. **Créez** une nouvelle app
2. **Connectez** votre repo GitHub
3. **Configuration** :
   - **Source** : GitHub
   - **Branch** : main
   - **Build Command** : `pip install -r requirements.txt`
   - **Run Command** : `gunicorn app:app --bind 0.0.0.0:$PORT`

---

## ☁️ **AWS Elastic Beanstalk**

### **Déploiement via CLI**
```bash
# Installation EB CLI
pip install awsebcli

# Initialisation
eb init -p python-3.11 arkalia-quest

# Création de l'environnement
eb create production

# Déploiement
eb deploy
```

### **Configuration EB**
```yaml
# .ebextensions/01_packages.config
packages:
  yum:
    gcc: []
    gcc-c++: []

# .ebextensions/02_requirements.config
container_commands:
  01_install_requirements:
    command: "pip install -r requirements.txt"
```

---

## 🐳 **Google Cloud Run**

### **Déploiement via gcloud**
```bash
# Installation gcloud CLI
curl https://sdk.cloud.google.com | bash

# Configuration
gcloud config set project YOUR_PROJECT_ID

# Build et déploiement
gcloud run deploy arkalia-quest \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🐳 **Docker**

### **Construction Locale**
```bash
# Build de l'image
docker build -f config/Dockerfile -t arkalia-quest .

# Lancement
docker run -p 5001:5001 arkalia-quest

# Avec docker-compose
cd config
docker-compose up --build
```

### **Déploiement sur Serveur**
```bash
# Sur votre serveur
git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest

# Construction et lancement
docker build -f config/Dockerfile -t arkalia-quest .
docker run -d -p 80:5001 --name arkalia-quest arkalia-quest

# Avec Nginx (reverse proxy)
docker run -d -p 80:80 nginx:alpine
```

---

## 🔧 **Configuration Commune**

### **Variables d'Environnement**
```bash
# Production
FLASK_ENV=production
DEBUG=false
SECRET_KEY=your-secure-secret-key

# Base de données
DATABASE_URL=sqlite:///arkalia.db

# Performance
WORKERS=2
TIMEOUT=120
MAX_REQUESTS=1000
```

### **Gunicorn Configuration**
```python
# gunicorn.conf.py
bind = "0.0.0.0:5001"
workers = 2
timeout = 120
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

---

## 📊 **Monitoring et Logs**

### **Logs d'Application**
```python
import logging
from logging.handlers import RotatingFileHandler

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        RotatingFileHandler('logs/arkalia.log', maxBytes=10240000, backupCount=10),
        logging.StreamHandler()
    ]
)
```

### **Métriques de Performance**
```python
# Endpoint de santé
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0'
    }

# Endpoint de métriques
@app.route('/metrics')
def metrics():
    return {
        'uptime': time.time() - start_time,
        'requests_total': request_count,
        'memory_usage': psutil.virtual_memory().percent
    }
```

---

## 🚨 **Sécurité en Production**

### **Headers de Sécurité**
```python
from flask_talisman import Talisman

# Configuration Talisman
Talisman(app, 
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
)
```

### **Rate Limiting**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## 🔄 **CI/CD Automatisé**

### **GitHub Actions**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "arkalia-quest-demo"
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

---

## 📞 **Support et Dépannage**

### **Logs et Debugging**
```bash
# Heroku
heroku logs --tail

# Docker
docker logs arkalia-quest

# Local
tail -f logs/arkalia.log
```

### **Problèmes Courants**
- **Port binding** : Vérifiez la variable `$PORT`
- **Dépendances** : Vérifiez `requirements.txt`
- **Permissions** : Vérifiez les droits d'écriture
- **Mémoire** : Ajustez le nombre de workers

---

## 🌟 **Bonnes Pratiques**

1. **Variables d'environnement** : Jamais de secrets en dur
2. **Logs structurés** : Format JSON pour la production
3. **Health checks** : Endpoints de vérification
4. **Monitoring** : Métriques et alertes
5. **Backup** : Sauvegarde régulière des données
6. **SSL/TLS** : Certificats valides en production
7. **Updates** : Mise à jour régulière des dépendances

---

*Ce guide est maintenu par l'équipe Arkalia Quest.*
