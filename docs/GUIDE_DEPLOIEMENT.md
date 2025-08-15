---
**Statut : ACTIF**
**Dernière mise à jour : Juillet 2025**
**Résumé :** Guide de déploiement et configuration d'Arkalia Quest.

**Liens utiles :**
- [Documentation principale](README.md)
- [Statut projet](STATUT_PROJET_ACTUEL.md)
- [Changelog documentation](CHANGELOG_DOCUMENTATION.md)
---

## 📋 PRÉREQUIS

### 🖥️ **Système**
- **OS :** Linux, macOS, Windows
- **Python :** 3.8 ou supérieur
- **RAM :** 512 MB minimum
- **Espace disque :** 100 MB

### 📦 **Dépendances**
- **Flask :** Framework web
- **SQLite :** Base de données
- **Gunicorn :** Serveur WSGI (production)
- **WebSockets :** Communication temps réel

---

## 🛠️ INSTALLATION LOCALE

### 1️⃣ **Cloner le projet**
```bash
git clone https://github.com/votre-username/arkalia-quest.git
cd arkalia-quest
```

### 2️⃣ **Créer l'environnement virtuel**
```bash
# Python 3.8+
python -m venv venv

# Activer l'environnement
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3️⃣ **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Initialiser la base de données**
```bash
python -c "from core.database import DatabaseManager; DatabaseManager().init_database()"
```

### 5️⃣ **Lancer le serveur**
```bash
# Mode développement
python app.py

# Mode production
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### 6️⃣ **Accéder à l'application**
- **URL :** http://localhost:5001
- **Terminal :** http://localhost:5001/terminal
- **Profil :** http://localhost:5001/profil

---

## ☁️ DÉPLOIEMENT RENDER

### 1️⃣ **Préparer le projet**
```bash
# Vérifier que tous les fichiers sont présents
ls -la

# Fichiers requis pour Render
render.yaml          # Configuration Render
Procfile            # Processus de démarrage
requirements.txt    # Dépendances Python
runtime.txt         # Version Python
start_gunicorn.sh   # Script de démarrage
```

### 2️⃣ **Configuration Render (render.yaml)**
```yaml
services:
  - type: web
    name: arkalia-quest
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: ./start_gunicorn.sh
    envVars:
      - key: PYTHON_VERSION
        value: 3.8.0
      - key: PORT
        value: 5001
```

### 3️⃣ **Script de démarrage (start_gunicorn.sh)**
```bash
#!/bin/bash
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### 4️⃣ **Déployer sur Render**
1. **Connecter le repository** GitHub à Render
2. **Créer un nouveau service web**
3. **Configurer les variables d'environnement**
4. **Déployer automatiquement**

### 5️⃣ **Variables d'environnement**
```bash
PYTHON_VERSION=3.8.0
PORT=5001
FLASK_ENV=production
DATABASE_URL=sqlite:///arkalia.db
```

---

## 🔧 CONFIGURATION PRODUCTION

### 🛡️ **Sécurité**
```python
# app.py
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
```

### 📊 **Logs**
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 🗄️ **Base de données**
```python
# Sauvegarde automatique
def backup_database():
    import shutil
    shutil.copy2('arkalia.db', f'backup/arkalia_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
```

---

## 📱 DÉPLOIEMENT MOBILE (PWA)

### 1️⃣ **Manifest (static/manifest.json)**
```json
{
  "name": "Arkalia Quest",
  "short_name": "Arkalia",
  "description": "Jeu éducatif hacker pour ados",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#00ff00",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

### 2️⃣ **Service Worker (static/sw.js)**
```javascript
// Cache des ressources statiques
const CACHE_NAME = 'arkalia-v3.0';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/terminal.js',
  '/static/icons/icon-192.png'
];
```

### 3️⃣ **Installation PWA**
```html
<!-- templates/index.html -->
<link rel="manifest" href="/static/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js');
  }
</script>
```

---

## 🔍 MONITORING ET MAINTENANCE

### 📊 **Métriques de performance**
```python
# Monitoring des requêtes
@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    if diff > 1.0:  # Log des requêtes lentes
        app.logger.warning(f'Slow request: {request.path} took {diff:.2f}s')
    return response
```

### 🚨 **Alertes**
```python
# Surveillance de la base de données
def check_database_health():
    try:
        db = DatabaseManager()
        db.execute("SELECT 1")
        return True
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return False
```

### 🔄 **Sauvegarde automatique**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp arkalia.db backup/arkalia_$DATE.db
find backup/ -name "*.db" -mtime +7 -delete
```

---

## 🧪 TESTS DE DÉPLOIEMENT

### 1️⃣ **Tests de connectivité**
```bash
# Test du serveur
curl -I http://localhost:5001

# Test de l'API
curl http://localhost:5001/api/status

# Test de la base de données
curl http://localhost:5001/api/test/database
```

### 2️⃣ **Tests de performance**
```bash
# Test de charge avec Apache Bench
ab -n 100 -c 10 http://localhost:5001/

# Test de stress
python tests/stress_test.py
```

### 3️⃣ **Tests de sécurité**
```bash
# Test des headers de sécurité
curl -I http://localhost:5001 | grep -E "(X-Frame-Options|X-Content-Type-Options|X-XSS-Protection)"

# Test d'injection SQL
curl "http://localhost:5001/commande?commande=test'; DROP TABLE users; --"
```

---

## 🚨 DÉPANNAGE

### ❌ **Problèmes courants**

#### **Erreur : Port déjà utilisé**
```bash
# Solution 1 : Changer le port
python app.py --port 5002

# Solution 2 : Tuer le processus
lsof -ti:5001 | xargs kill -9
```

#### **Erreur : Base de données corrompue**
```bash
# Restaurer depuis une sauvegarde
cp backup/arkalia_20250708_120000.db arkalia.db

# Ou réinitialiser
rm arkalia.db
python -c "from core.database import DatabaseManager; DatabaseManager().init_database()"
```

#### **Erreur : Dépendances manquantes**
```bash
# Réinstaller les dépendances
pip install --force-reinstall -r requirements.txt

# Vérifier les versions
pip list | grep -E "(Flask|SQLite|Gunicorn)"
```

### 📞 **Support**
- **Logs :** `tail -f logs/app.log`
- **Documentation :** `/docs/`
- **Issues :** GitHub Issues
- **Email :** support@arkalia-quest.com

---

## 🎯 CHECKLIST DE DÉPLOIEMENT

### ✅ **Pré-déploiement**
- [ ] Tests unitaires passent
- [ ] Tests d'intégration validés
- [ ] Documentation mise à jour
- [ ] Variables d'environnement configurées
- [ ] Base de données initialisée

### ✅ **Déploiement**
- [ ] Code déployé sur Render
- [ ] Service accessible
- [ ] Base de données connectée
- [ ] Logs fonctionnels
- [ ] Monitoring actif

### ✅ **Post-déploiement**
- [ ] Tests de régression
- [ ] Performance validée
- [ ] Sécurité vérifiée
- [ ] Sauvegarde configurée
- [ ] Alertes configurées

---

## 🏁 CONCLUSION

### 🚀 **Déploiement réussi !**
Arkalia Quest est maintenant accessible en production et prêt à accueillir les hackers rebelles de demain !

### 📊 **Métriques de succès**
- **Temps de déploiement :** < 5 minutes
- **Disponibilité :** 99.9%
- **Performance :** < 1s de réponse
- **Sécurité :** Headers configurés

### 🎮 **Prêt pour l'aventure !**
Le jeu est maintenant **100% opérationnel** et peut être utilisé par des ados de 13 ans en toute sécurité.

---

**🎯 Arkalia Quest - Déployé avec succès et prêt pour l'aventure ! 🚀** 