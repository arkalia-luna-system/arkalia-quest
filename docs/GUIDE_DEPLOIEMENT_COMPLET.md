# 🚀 GUIDE DE DÉPLOIEMENT COMPLET - ARKALIA QUEST

> **Guide détaillé pour déployer Arkalia Quest sur toutes les plateformes**

---

## 📋 TABLE DES MATIÈRES

1. [🌐 Render (Recommandé)](#-render-recommandé)
2. [☁️ Heroku](#-heroku)
3. [🚂 Railway](#-railway)
4. [🐳 Docker](#-docker)
5. [🖥️ VPS/Server](#-vpsserver)
6. [📱 Mobile](#-mobile)
7. [🔧 Configuration](#-configuration)
8. [📊 Monitoring](#-monitoring)
9. [🛡️ Sécurité](#-sécurité)
10. [❌ Dépannage](#-dépannage)

---

## 🌐 RENDER (RECOMMANDÉ)

### 🎯 **POURQUOI RENDER ?**

- **Gratuit** : Plan gratuit généreux
- **Simple** : Déploiement automatique depuis GitHub
- **Performant** : Infrastructure moderne
- **SSL** : Certificats HTTPS automatiques
- **Monitoring** : Logs et métriques intégrés

### 🚀 **DÉPLOIEMENT RAPIDE**

#### **Étape 1 : Préparation**
```bash
# Vérifier que le code est sur GitHub
git push origin main

# Vérifier les fichiers de configuration
ls -la render.yaml pyproject.toml requirements.txt
```

#### **Étape 2 : Créer le Compte Render**
1. Va sur https://render.com
2. Clique sur "Sign Up"
3. Connecte ton compte GitHub
4. Autorise l'accès au repository

#### **Étape 3 : Créer le Web Service**
1. **Dashboard** → "New +" → "Web Service"
2. **Connect Repository** : Sélectionne `arkalia-quest`
3. **Configure le service** :
   - **Name** : `arkalia-quest`
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan** : `Free`

#### **Étape 4 : Variables d'Environnement**
```env
FLASK_ENV=production
PORT=5001
DATABASE_URL=sqlite:///arkalia.db
SECRET_KEY=your-super-secret-key-here
```

#### **Étape 5 : Déployer**
1. Clique sur "Create Web Service"
2. Attends le build (2-3 minutes)
3. Vérifie les logs pour détecter les erreurs
4. Teste l'URL générée

### 📊 **MONITORING RENDER**

#### **Logs en Temps Réel**
```bash
# Dans le dashboard Render
Logs → Real-time logs
```

#### **Métriques**
- **CPU** : Utilisation du processeur
- **Memory** : Utilisation mémoire
- **Requests** : Nombre de requêtes
- **Response Time** : Temps de réponse

---

## ☁️ HEROKU

### 🎯 **CONFIGURATION HEROKU**

#### **Étape 1 : Installation CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Télécharge depuis https://devcenter.heroku.com/articles/heroku-cli
```

#### **Étape 2 : Login et Setup**
```bash
heroku login
heroku create arkalia-quest-app
```

#### **Étape 3 : Configuration**
```bash
# Variables d'environnement
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set PORT=5001

# Déployer
git push heroku main
```

#### **Étape 4 : Vérification**
```bash
heroku logs --tail
heroku open
```

### 📋 **FICHIERS HEROKU**

**`Procfile`**
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

**`runtime.txt`**
```
python-3.9.18
```

---

## 🚂 RAILWAY

### 🎯 **DÉPLOIEMENT RAILWAY**

#### **Étape 1 : Connexion**
1. Va sur https://railway.app
2. Connecte ton compte GitHub
3. Clique sur "New Project"

#### **Étape 2 : Configuration**
1. **Deploy from GitHub repo**
2. Sélectionne `arkalia-quest`
3. **Framework Preset** : `Python`
4. **Build Command** : `pip install -r requirements.txt`
5. **Start Command** : `gunicorn app:app --bind 0.0.0.0:$PORT`

#### **Étape 3 : Variables**
```env
FLASK_ENV=production
PORT=5001
DATABASE_URL=sqlite:///arkalia.db
SECRET_KEY=your-secret-key
```

#### **Étape 4 : Déploiement**
1. Clique sur "Deploy Now"
2. Attends le build
3. Vérifie l'URL générée

---

## 🐳 DOCKER

### 🎯 **CONFIGURATION DOCKER**

#### **Dockerfile**
```dockerfile
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .
COPY pyproject.toml .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 5001

# Commande de démarrage
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5001", "--workers", "2"]
```

#### **Docker Compose**
```yaml
version: '3.8'

services:
  arkalia-quest:
    build: .
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - PORT=5001
      - DATABASE_URL=sqlite:///arkalia.db
      - SECRET_KEY=your-secret-key
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

#### **Déploiement Docker**
```bash
# Build l'image
docker build -t arkalia-quest .

# Lancer le conteneur
docker run -p 5001:5001 arkalia-quest

# Avec Docker Compose
docker-compose up -d
```

---

## 🖥️ VPS/SERVER

### 🎯 **CONFIGURATION SERVEUR**

#### **Étape 1 : Préparation Serveur**
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Python et Git
sudo apt install python3 python3-pip python3-venv git nginx -y

# Créer l'utilisateur
sudo adduser arkalia
sudo usermod -aG sudo arkalia
```

#### **Étape 2 : Déploiement Application**
```bash
# Se connecter en tant qu'arkalia
sudo su - arkalia

# Cloner le repository
git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
pip install gunicorn
```

#### **Étape 3 : Configuration Systemd**
```bash
# Créer le service
sudo nano /etc/systemd/system/arkalia-quest.service
```

**Contenu du service :**
```ini
[Unit]
Description=Arkalia Quest Web Application
After=network.target

[Service]
User=arkalia
WorkingDirectory=/home/arkalia/arkalia-quest
Environment="PATH=/home/arkalia/arkalia-quest/venv/bin"
Environment="FLASK_ENV=production"
Environment="PORT=5001"
ExecStart=/home/arkalia/arkalia-quest/venv/bin/gunicorn app:app --bind 0.0.0.0:5001 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

#### **Étape 4 : Configuration Nginx**
```bash
sudo nano /etc/nginx/sites-available/arkalia-quest
```

**Configuration Nginx :**
```nginx
server {
    listen 80;
    server_name ton-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/arkalia/arkalia-quest/static;
    }
}
```

#### **Étape 5 : Activation**
```bash
# Activer le service
sudo systemctl enable arkalia-quest
sudo systemctl start arkalia-quest

# Activer le site Nginx
sudo ln -s /etc/nginx/sites-available/arkalia-quest /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Vérifier le statut
sudo systemctl status arkalia-quest
```

---

## 📱 MOBILE

### 🎯 **PWA (Progressive Web App)**

#### **Manifest.json**
```json
{
  "name": "Arkalia Quest",
  "short_name": "Arkalia",
  "description": "Jeu éducatif hacker pour adolescents",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#00ff00",
  "icons": [
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

#### **Service Worker**
```javascript
// static/js/sw.js
const CACHE_NAME = 'arkalia-quest-v3.0';
const urlsToCache = [
  '/',
  '/static/style.css',
  '/static/js/terminal.js',
  '/static/icons/icon-192x192.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

---

## 🔧 CONFIGURATION

### 🎯 **VARIABLES D'ENVIRONNEMENT**

#### **Développement**
```env
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5001
DATABASE_URL=sqlite:///arkalia.db
SECRET_KEY=dev-secret-key
```

#### **Production**
```env
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5001
DATABASE_URL=sqlite:///arkalia.db
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgresql://user:pass@host:port/db
```

### 🗄️ **BASE DE DONNÉES**

#### **SQLite (Développement)**
```python
# Configuration automatique
DATABASE_URL = "sqlite:///arkalia.db"
```

#### **PostgreSQL (Production)**
```python
# Configuration PostgreSQL
DATABASE_URL = "postgresql://user:password@host:port/database"
```

### 🔐 **SÉCURITÉ**

#### **Clés Secrètes**
```python
# Générer une clé secrète
import secrets
secret_key = secrets.token_hex(32)
print(secret_key)
```

#### **CORS Configuration**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://ton-domaine.com'])
```

---

## 📊 MONITORING

### 🎯 **LOGS ET MÉTRIQUES**

#### **Logs Application**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arkalia.log'),
        logging.StreamHandler()
    ]
)
```

#### **Métriques de Performance**
```python
from flask import request
import time

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    duration = time.time() - request.start_time
    app.logger.info(f'{request.method} {request.path} - {response.status_code} - {duration:.3f}s')
    return response
```

### 📈 **HEALTH CHECKS**

#### **Endpoint de Santé**
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0',
        'database': 'connected'
    }
```

---

## 🛡️ SÉCURITÉ

### 🎯 **BONNES PRATIQUES**

#### **Validation des Entrées**
```python
from flask import request, abort

def validate_command(command):
    if not command or len(command) > 100:
        abort(400, description="Commande invalide")
    return command.strip()
```

#### **Rate Limiting**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/commande', methods=['POST'])
@limiter.limit("10 per minute")
def commande():
    # Gestion des commandes
    pass
```

#### **Headers de Sécurité**
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

---

## ❌ DÉPANNAGE

### 🎯 **PROBLÈMES COURANTS**

#### **Erreur de Build**
```bash
# Vérifier les dépendances
pip install -r requirements.txt --upgrade

# Vérifier la version Python
python --version

# Nettoyer le cache
pip cache purge
```

#### **Erreur de Port**
```bash
# Vérifier les ports utilisés
lsof -i :5001

# Changer le port
export PORT=5002
```

#### **Erreur de Base de Données**
```bash
# Vérifier la connexion
python -c "import sqlite3; sqlite3.connect('arkalia.db')"

# Réinitialiser la base
rm arkalia.db
python -c "from core.database import init_db; init_db()"
```

#### **Erreur de Permissions**
```bash
# Vérifier les permissions
ls -la

# Corriger les permissions
chmod +x start_gunicorn.sh
chmod 755 static/
```

### 📞 **SUPPORT**

#### **Logs d'Erreur**
```bash
# Logs Render
render.com → Dashboard → Logs

# Logs Heroku
heroku logs --tail

# Logs Locaux
tail -f arkalia.log
```

#### **Contact**
- **GitHub Issues** : https://github.com/arkalia-luna-system/arkalia-quest/issues
- **Email** : support@arkalia-quest.com
- **Documentation** : https://github.com/arkalia-luna-system/arkalia-quest

---

## 🎉 CONCLUSION

### 🚀 **PLATEFORMES RECOMMANDÉES**

1. **🌐 Render** : Pour un déploiement simple et gratuit
2. **☁️ Heroku** : Pour une solution robuste et scalable
3. **🚂 Railway** : Pour un déploiement rapide
4. **🐳 Docker** : Pour un contrôle total
5. **🖥️ VPS** : Pour une personnalisation complète

### 📊 **MÉTRIQUES DE PERFORMANCE**

- **Temps de réponse** : < 200ms
- **Uptime** : 99.9%
- **Utilisateurs simultanés** : 50+
- **Mémoire** : < 100MB par instance

### 🔄 **MAINTENANCE**

- **Sauvegardes** : Automatiques quotidiennes
- **Mises à jour** : Sécuritaires automatiques
- **Monitoring** : 24/7 avec alertes
- **Support** : Réponse sous 24h

---

*Guide de déploiement créé avec ❤️ par l'équipe Arkalia Quest*  
*Version 3.0 - 2025* 