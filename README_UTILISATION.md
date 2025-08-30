# 🚀 Guide d'Utilisation - Arkalia Quest

## 🌟 Démarrage Rapide

### 1. **Démarrage Automatique (Recommandé)**
```bash
./start.sh
```
Ce script :
- ✅ Crée l'environnement virtuel si nécessaire
- ✅ Installe les dépendances automatiquement
- ✅ Lance l'application Flask
- ✅ Crée les dossiers nécessaires (logs, etc.)

### 2. **Démarrage Manuel**
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# L'activer
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

---

## 🎯 **Fonctionnalités Principales**

### 🔒 **Sécurité Avancée**
- **Rate Limiting** : 100 requêtes/minute par IP
- **Validation des entrées** : Protection contre les injections
- **Headers de sécurité** : CSP, HSTS, XSS Protection
- **Monitoring** : Logs de sécurité en temps réel

### ⚡ **Performance Optimisée**
- **Compression gzip** : Réduction automatique de la taille
- **Cache HTTP intelligent** : Headers de cache appropriés
- **Base de données optimisée** : Index et cache mémoire
- **Tests de charge** : Validation de la scalabilité

---

## 🧪 **Tests et Qualité**

### **Lancer tous les tests :**
```bash
python -m pytest tests/ -v
```

### **Tests de charge :**
```bash
python tests/performance/test_load_testing.py
```

### **Formatage du code :**
```bash
black . --line-length 88
```

### **Linting et corrections :**
```bash
ruff check . --fix
```

---

## 📁 **Structure du Projet**

```
arkalia-quest/
├── app.py                 # Application Flask principale
├── core/                  # Logique métier
│   ├── security_manager.py    # Gestionnaire de sécurité
│   ├── database.py            # Gestion de la base de données
│   └── ...
├── config/               # Configuration
│   ├── security.json         # Paramètres de sécurité
│   └── ...
├── tests/                # Tests automatisés
├── static/               # Assets statiques
├── templates/            # Templates HTML
└── start.sh             # Script de démarrage
```

---

## 🔧 **Configuration**

### **Sécurité (`config/security.json`)**
```json
{
  "max_failed_attempts": 5,
  "block_duration": 3600,
  "security_level": "high",
  "enable_logging": true
}
```

### **Variables d'environnement**
```bash
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///arkalia.db
```

---

## 📊 **Monitoring et Logs**

### **Logs de sécurité :**
```bash
tail -f logs/security.log
```

### **Statut de sécurité :**
```bash
curl http://localhost:5000/api/security/status
```

### **Métriques de performance :**
```bash
curl http://localhost:5000/api/performance/metrics
```

---

## 🚨 **Dépannage**

### **Problème de dépendances :**
```bash
pip install --upgrade -r requirements.txt
```

### **Problème de base de données :**
```bash
rm arkalia.db  # Supprimer la base corrompue
python -c "from core.database import init_database; init_database()"
```

### **Problème de permissions :**
```bash
chmod +x start.sh
chmod -R 755 logs/
```

---

## 🌐 **Déploiement**

### **Heroku :**
```bash
git push heroku main
```

### **Docker :**
```bash
docker build -t arkalia-quest .
docker run -p 5000:5000 arkalia-quest
```

---

## 📞 **Support**

- **Documentation** : Voir `docs/` pour plus de détails
- **Issues** : Utiliser GitHub Issues pour les bugs
- **Tests** : Vérifier que tous les tests passent avant de signaler un problème

---

## 🎉 **Félicitations !**

Vous utilisez maintenant **Arkalia Quest**, un projet de jeu éducatif avec une architecture professionnelle, une sécurité avancée et des performances optimisées !

**Bon jeu !** 🎮✨
