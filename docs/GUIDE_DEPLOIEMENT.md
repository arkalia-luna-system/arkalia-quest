

# 🚀 **GUIDE DE DÉPLOIEMENT - ARKALIA QUEST**


> **Guide complet pour déployer Arkalia Quest en production**

---


## 📋 **Table des Matières**


1. [🎯 Prérequis](#-prérequis)
2. [🔧 Configuration](#-configuration)
3. [🐳 Docker](#-docker)
4. [☁️ Cloud](#️-cloud)
5. [📊 Monitoring](#-monitoring)
6. [🔄 CI/CD](#-cicd)

---


## 🎯 **Prérequis**



### **Système**


| Composant | Version | Description |
|-----------|---------|-------------|
| **Python** | 3.10+ | Runtime principal |
| **SQLite** | 3.x | Base de données |
| **Nginx** | 1.18+ | Serveur web (optionnel) |
| **Gunicorn** | 21.0+ | Serveur WSGI |


### **Sécurité**



- ✅ **HTTPS/TLS** : Certificat SSL valide



- ✅ **Firewall** : Ports 80, 443, 5000



- ✅ **Rate Limiting** : Protection DDoS



- ✅ **Monitoring** : Logs et alertes


---


## 🔧 **Configuration**



### **Variables d'Environnement**



```bash



# .env.production


FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key
DEBUG=False
LOG_LEVEL=WARNING


# Base de données


DATABASE_URL=sqlite:///data/database/arkalia.db
DATABASE_PATH=data/database/arkalia.db


# Sécurité


SECURITY_LEVEL=high
MAX_FAILED_ATTEMPTS=3
BLOCK_DURATION=7200


# Performance


ENABLE_COMPRESSION=true
ENABLE_CACHING=true
CACHE_TTL=600


# Monitoring


ENABLE_METRICS=true
METRICS_PORT=9090


```text



### **Configuration Gunicorn**



```python



# gunicorn.conf.py


bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True


```text


---


## 🐳 **Docker**



### **Dockerfile**



```dockerfile


FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p logs data/database

EXPOSE 5000

ENV FLASK_ENV=production
ENV PYTHONPATH=/app

CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]


```text



### **Docker Compose**



```yaml


version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped


```text


---


## ☁️ **Cloud**



### **Heroku**



```bash



# Procfile


web: gunicorn app:app


# Déploiement


heroku create arkalia-quest
git push heroku main
heroku config:set FLASK_ENV=production
heroku open


```text



### **Railway**



```bash



# railway.json


{
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "gunicorn app:app"
  }
}


# Déploiement


railway login
railway init
railway up


```text



### **DigitalOcean App Platform**



```yaml



# .do/app.yaml


name: arkalia-quest
services:


- name: web


  source_dir: /
  github:
    repo: arkalia-luna-system/arkalia-quest
    branch: main
  run_command: gunicorn app:app
  environment_slug: python
  instance_count: 2
  instance_size_slug: basic-xxs


```text


---


## 📊 **Monitoring**



### **Métriques Clés**


| Métrique | Seuil | Action |
|----------|-------|---------|
| **CPU** | >80% | Scale up |
| **Mémoire** | >80% | Optimisation |
| **Temps réponse** | >200ms | Investigation |
| **Erreurs** | >1% | Debug immédiat |


### **Logs Structurés**



```python



# Configuration des logs


import logging
import json

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )


# Log structuré


def log_event(event_type, details):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }
    logging.info(json.dumps(log_data))


```text


---


## 🔄 **CI/CD**



### **GitHub Actions**



```yaml



# .github/workflows/deploy.yml


name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Logique de déploiement


```text



### **Script de Déploiement**



```bash


#!/bin/bash


# scripts/deploy.sh


set -e

echo "🚀 Déploiement en cours..."


# Tests


python -m pytest tests/ -v
black . --check
ruff check .


# Déploiement


case $1 in
  "staging")
    echo "Deploying to staging..."
    ;;
  "production")
    echo "Deploying to production..."
    ;;
  *)
    echo "Usage: $0 {staging|production}"
    exit 1
    ;;
esac

echo "✅ Déploiement terminé!"


```text


---


## 🎯 **Checklist de Déploiement**



- [ ] **🧪 Tests** : Tous les tests passent



- [ ] **🔧 Qualité** : Code formaté et linté



- [ ] **🔒 Sécurité** : Variables d'environnement sécurisées



- [ ] **📊 Monitoring** : Logs et métriques configurés



- [ ] **🔄 Rollback** : Plan de rollback préparé



- [ ] **📚 Documentation** : Documentation mise à jour


---


## 🚨 **Troubleshooting**



### **Problèmes Courants**


| Problème | Cause | Solution |
|----------|-------|----------|
| **Port déjà utilisé** | Autre service | Changer le port |
| **Permission denied** | Droits insuffisants | `chmod +x start.sh` |
| **Module not found** | Dépendances manquantes | `pip install -r requirements.txt` |
| **Database locked** | Concurrence SQLite | Vérifier les connexions |


### **Commandes de Debug**



```bash



# Vérifier les processus


ps aux | grep python


# Vérifier les ports


netstat -tulpn | grep :5000


# Vérifier les logs


tail -f logs/app.log


# Vérifier la base de données


sqlite3 data/database/arkalia.db ".tables"


```text


---


## 🌟 **Conclusion**


Ce guide couvre les aspects essentiels du déploiement d'Arkalia Quest. Pour plus de détails, consultez la [documentation complète](ARCHITECTURE_TECHNIQUE.md).

**Bon déploiement !** 🚀✨
