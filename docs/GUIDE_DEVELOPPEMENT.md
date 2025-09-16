

# 🔧 **GUIDE DE DÉVELOPPEMENT - ARKALIA QUEST**


> **Guide complet pour les développeurs : installation, développement, tests et déploiement**

---


## 📋 **Table des Matières**


1. [🚀 Installation et Configuration](#-installation-et-configuration)
2. [🏗️ Structure du Projet](#️-structure-du-projet)
3. [💻 Workflow de Développement](#-workflow-de-développement)
4. [🧪 Tests et Qualité](#-tests-et-qualité)
5. [🔒 Sécurité](#-sécurité)
6. [⚡ Performance](#-performance)
7. [📚 Documentation](#-documentation)
8. [🚀 Déploiement](#-déploiement)
9. [🤝 Contribution](#-contribution)

---


## 🚀 **Installation et Configuration**



### **Prérequis Système**


| Composant | Version | Description |
|-----------|---------|-------------|
| **Python** | 3.10+ | Langage principal |
| **Git** | 2.30+ | Contrôle de version |
| **pip** | 23.0+ | Gestionnaire de paquets |
| **Virtualenv** | 20.0+ | Environnements virtuels |


### **Installation Rapide**



```bash



# 1. Cloner le projet


git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest


# 2. Créer l'environnement virtuel


python3 -m venv venv


# 3. Activer l'environnement


source venv/bin/activate  # Linux/Mac


# ou


venv\Scripts\activate     # Windows


# 4. Installer les dépendances


pip install -r requirements.txt


# 5. Lancer l'application


python app.py


```text



### **Configuration de l'Environnement**


Créer un fichier `.env` basé sur `env.example` :


```bash



# Copier le fichier d'exemple


cp env.example .env


# Éditer les variables


nano .env


```text


# **Variables d'environnement principales :**


```env



# Application


FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
DEBUG=True


# Base de données


DATABASE_URL=sqlite:///arkalia.db
DATABASE_PATH=data/database/arkalia.db


# Sécurité


SECURITY_LEVEL=high
MAX_FAILED_ATTEMPTS=5
BLOCK_DURATION=3600


# Performance


ENABLE_COMPRESSION=true
ENABLE_CACHING=true
CACHE_TTL=300


# Monitoring


ENABLE_METRICS=true
METRICS_PORT=9090
LOG_LEVEL=INFO


```text


---


## 🏗️ **Structure du Projet**



### **Organisation des Dossiers**



```mermaid


graph TB
    subgraph "📁 Root"
        A[README.md]
        B[app.py]
        C[requirements.txt]
        D[start.sh]
    end

    subgraph "📁 Core Logic"
        E[core/]
        F[engines/]
        G[utils/]
    end

    subgraph "📁 Web Interface"
        H[templates/]
        I[static/]
        J[assets/]
    end

    subgraph "📁 Data & Config"
        K[data/]
        L[config/]
        M[missions/]
    end

    subgraph "📁 Testing"
        N[tests/]
        O[scripts/]
        P[reports/]
    end

    subgraph "📁 Documentation"
        Q[docs/]
        R[reports/]
        S[CHANGELOG.md]
    end

    A --> E
    B --> E
    E --> F
    E --> G
    E --> H
    E --> I
    E --> K
    E --> L
    E --> N
    E --> Q

    style E fill:#e3f2fd
    style N fill:#e8f5e8
    style Q fill:#fff3e0


```text



### **Description des Composants**


| Composant | Description | Responsabilité |
|-----------|-------------|----------------|
| **📁 core/** | Logique métier principale | Moteurs, gestionnaires, handlers |
| **📁 engines/** | Moteurs spécialisés | IA, gamification, effets |
| **📁 utils/** | Utilitaires et helpers | Logging, validation, helpers |
| **📁 templates/** | Templates HTML | Interface utilisateur |
| **📁 static/** | Assets statiques | CSS, JS, images, fonts |
| **📁 tests/** | Tests automatisés | Unit, integration, performance |
| **📁 docs/** | Documentation | Guides, API, architecture |
| **📁 config/** | Configuration | Settings, deployment, tools |

---


## 💻 **Workflow de Développement**



### **Workflow Git Recommandé**



```mermaid


gitgraph
    commit
    branch develop
    checkout develop
    commit
    commit
    branch feature/security-manager
    checkout feature/security-manager
    commit
    commit
    checkout develop
    merge feature/security-manager
    branch hotfix/security-fix
    checkout hotfix/security-fix
    commit
    checkout main
    merge hotfix/security-fix
    checkout develop
    merge hotfix/security-fix


```text



### **Conventions de Nommage**



#### **Fichiers Python**


| Type | Convention | Exemple |
|------|------------|---------|
| **Modules** | `snake_case.py` | `security_manager.py` |
| **Classes** | `PascalCase` | `SecurityManager` |
| **Fonctions** | `snake_case()` | `validate_input()` |
| **Variables** | `snake_case` | `max_attempts` |
| **Constantes** | `UPPER_SNAKE_CASE` | `MAX_LOGIN_ATTEMPTS` |


#### **Fichiers de Configuration**


| Type | Convention | Exemple |
|------|------------|---------|
| **Python** | `snake_case.py` | `settings.py` |
| **JSON** | `kebab-case.json` | `security-config.json` |
| **YAML** | `kebab-case.yaml` | `deployment-config.yaml` |
| **TOML** | `snake_case.toml` | `pyproject.toml` |


### **Structure des Commits**



```bash



# Format recommandé


<type>(<scope>): <description>


# Exemples


feat(security): add rate limiting for login attempts
fix(database): resolve connection pool memory leak
docs(api): update authentication endpoint documentation
test(gamification): add unit tests for badge system
refactor(core): simplify emotion engine logic
style(ui): improve button accessibility
perf(database): optimize user profile queries


```text


# **Types de commits :**

| Type | Description | Exemple |
|------|-------------|---------|
| **feat** | Nouvelle fonctionnalité | `feat(security): add IP blocking` |
| **fix** | Correction de bug | `fix(database): fix connection timeout` |
| **docs** | Documentation | `docs(api): add endpoint examples` |
| **test** | Tests | `test(core): add unit tests` |
| **refactor** | Refactoring | `refactor(engine): simplify logic` |
| **style** | Formatage | `style(code): apply black formatting` |
| **perf** | Performance | `perf(cache): optimize memory usage` |

---


## 🧪 **Tests et Qualité**



### **Architecture des Tests**



```mermaid


graph TB
    subgraph "🧪 Test Types"
        A[Unit Tests]
        B[Integration Tests]
        C[Performance Tests]
        D[Security Tests]
        E[UI Tests]
    end

    subgraph "🔧 Test Tools"
        F[Pytest]
        G[Pytest-cov]
        H[Pytest-benchmark]
        I[Pytest-mock]
        J[Pytest-timeout]
    end

    subgraph "📊 Test Execution"
        K[Local Development]
        L[CI/CD Pipeline]
        M[Staging Environment]
        N[Production Monitoring]
    end

    A --> F
    B --> G
    C --> H
    D --> I
    E --> J

    F --> K
    G --> L
    H --> M
    I --> N
    J --> N

    style F fill:#e8f5e8
    style K fill:#e3f2fd


```text



### **Exécution des Tests**



#### **Tests Complets**



```bash



# Lancer tous les tests


python -m pytest tests/ -v


# Tests avec couverture


python -m pytest --cov=core --cov-report=html


# Tests de performance


python -m pytest tests/performance/ -v


# Tests spécifiques


python -m pytest tests/core/test_security_manager.py -v


```text



#### **Tests par Catégorie**



```bash



# Tests unitaires uniquement


python -m pytest tests/ -m "unit" -v


# Tests d'intégration


python -m pytest tests/ -m "integration" -v


# Tests de sécurité


python -m pytest tests/ -m "security" -v


# Tests de performance


python -m pytest tests/ -m "performance" -v


```text



### **Exemple de Test**



```python



# tests/core/test_security_manager.py


import pytest
from unittest.mock import Mock, patch
from core.security_manager import SecurityManager

class TestSecurityManager:
    """Tests pour le gestionnaire de sécurité"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.security_manager = SecurityManager()
        self.test_ip = "192.168.1.100"

    def test_rate_limiting(self):
        """Test du rate limiting"""
        # Test normal
        for _ in range(100):
            assert self.security_manager.check_rate_limit(self.test_ip) is True

        # Test dépassement
        assert self.security_manager.check_rate_limit(self.test_ip) is False

    def test_ip_blocking(self):
        """Test du blocage d'IP"""
        # Blocage d'IP
        self.security_manager.block_ip(self.test_ip, "Test blocking", 3600)
        assert self.test_ip in self.security_manager.blocked_ips

        # Vérification du blocage
        assert self.security_manager.is_ip_blocked(self.test_ip) is True

    @patch('core.security_manager.logging')
    def test_security_logging(self, mock_logging):
        """Test de la journalisation de sécurité"""
        self.security_manager.log_security_event(
            "test_event",
            {"test": "data"},
            self.test_ip,
            "info"
        )

        mock_logging.getLogger.return_value.info.assert_called_once()


```text



### **Configuration des Tests**


# **`pyproject.toml` :**


```toml


[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=core",
    "--cov=engines",
    "--cov=utils",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=10",
]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "performance: marks tests as performance tests",
    "ui: marks tests as UI tests",
    "security: marks tests as security tests",
]


```text


---


## 🔒 **Sécurité**



### **Bonnes Pratiques de Sécurité**



#### **1. Validation des Entrées**



```python



# ❌ MAUVAIS - Pas de validation


def process_user_input(user_input):
    return f"Hello {user_input}"


# ✅ BON - Validation complète


def process_user_input(user_input: str) -> str:
    if not user_input:
        raise ValueError("Input cannot be empty")

    # Validation de la longueur
    if len(user_input) > 100:
        raise ValueError("Input too long")

    # Validation des caractères dangereux
    dangerous_chars = ['<', '>', '"', "'", '&', 'script', 'javascript']
    for char in dangerous_chars:
        if char in user_input.lower():
            raise ValueError("Input contains dangerous characters")

    # Échappement des caractères spéciaux
    safe_input = html.escape(user_input)
    return f"Hello {safe_input}"


```text



#### **2. Gestion des Sessions**



```python



# Configuration sécurisée des sessions


app.config.update(
    SESSION_COOKIE_SECURE=True,      # HTTPS uniquement
    SESSION_COOKIE_HTTPONLY=True,    # Pas d'accès JavaScript
    SESSION_COOKIE_SAMESITE='Lax',   # Protection CSRF
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2),  # Expiration
    SESSION_REFRESH_EACH_REQUEST=True  # Renouvellement
)


# Gestion sécurisée des sessions


@app.before_request
def before_request():
    if 'user_id' in session:
        # Vérifier l'expiration
        if 'last_activity' in session:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if datetime.now() - last_activity > timedelta(hours=2):
                session.clear()
                return redirect(url_for('login'))

        # Mettre à jour l'activité
        session['last_activity'] = datetime.now().isoformat()


```text



#### **3. Protection CSRF**



```python


from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)


# Dans les templates


<form method="POST">
    {{ csrf_token() }}
    <input type="text" name="username">
    <button type="submit">Submit</button>
</form>


# Dans les routes


@app.route('/login', methods=['POST'])
def login():
    if not csrf.validate():
        abort(400, "CSRF token invalid")

    # Traitement de la connexion
    username = request.form.get('username')
    password = request.form.get('password')
    # ... validation et authentification


```text



### **Tests de Sécurité**



```python



# tests/security/test_security_manager.py


import pytest
from core.security_manager import SecurityManager

class TestSecurityManager:
    """Tests de sécurité pour le gestionnaire de sécurité"""

    def setup_method(self):
        self.security_manager = SecurityManager()

    def test_sql_injection_prevention(self):
        """Test de prévention des injections SQL"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "'; EXEC xp_cmdshell('dir'); --"
        ]

        for malicious_input in malicious_inputs:
            assert self.security_manager.validate_input(malicious_input) is False

    def test_xss_prevention(self):
        """Test de prévention des attaques XSS"""
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "onload=alert('xss')"
        ]

        for malicious_input in malicious_inputs:
            assert self.security_manager.validate_input(malicious_input) is False

    def test_rate_limiting(self):
        """Test du rate limiting"""
        test_ip = "192.168.1.100"

        # Test normal
        for _ in range(100):
            assert self.security_manager.check_rate_limit(test_ip) is True

        # Test dépassement
        assert self.security_manager.check_rate_limit(test_ip) is False

        # Test reset après délai
        with patch('time.time') as mock_time:
            mock_time.return_value = time.time() + 3600  # +1 heure
            assert self.security_manager.check_rate_limit(test_ip) is True


```text


---


## ⚡ **Performance**



### **Optimisations de Performance**



#### **1. Mise en Cache**



```python



# Cache en mémoire avec TTL


from functools import wraps
import time

def cache_with_ttl(ttl_seconds=300):
    """Décorateur de cache avec TTL"""
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Créer une clé unique
            key = str(args) + str(sorted(kwargs.items()))

            # Vérifier le cache
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl_seconds:
                    return result

            # Exécuter la fonction
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())

            return result
        return wrapper
    return decorator


# Utilisation


@cache_with_ttl(ttl_seconds=600)  # 10 minutes
def get_user_profile(user_id: int):
    """Récupère le profil utilisateur avec cache"""
    # Simulation d'une requête coûteuse
    time.sleep(0.1)
    return {"user_id": user_id, "name": f"User {user_id}"}


```text



#### **2. Optimisation des Requêtes Base de Données**



```python



# Optimisation avec index et requêtes préparées


class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect('arkalia.db')
        self._create_indexes()

    def _create_indexes(self):
        """Création des index pour optimiser les performances"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_missions_difficulty ON missions(difficulty)",
            "CREATE INDEX IF NOT EXISTS idx_user_missions_status ON user_missions(status)"
        ]

        for index_sql in indexes:
            self.connection.execute(index_sql)
        self.connection.commit()

    def get_user_with_profile(self, user_id: int):
        """Récupération optimisée d'un utilisateur avec son profil"""
        query = """
        SELECT u.*, p.*
        FROM users u
        LEFT JOIN profiles p ON u.user_id = p.user_id
        WHERE u.user_id = ?
        """

        cursor = self.connection.execute(query, (user_id,))
        return cursor.fetchone()


```text



#### **3. Compression et Optimisation HTTP**



```python



# Configuration de compression


from flask_compress import Compress

compress = Compress()
compress.init_app(app)


# Headers de cache optimisés


@app.after_request
def add_cache_headers(response):
    """Ajoute des headers de cache optimisés"""
    if request.endpoint == 'static':
        # Assets statiques : cache long
        response.cache_control.max_age = 31536000  # 1 an
        response.cache_control.public = True
    elif request.endpoint in ['home', 'about']:
        # Pages statiques : cache moyen
        response.cache_control.max_age = 3600  # 1 heure
        response.cache_control.public = True
    else:
        # Pages dynamiques : pas de cache
        response.cache_control.no_cache = True
        response.cache_control.no_store = True

    return response


```text



### **Tests de Performance**



```python



# tests/performance/test_performance.py


import pytest
import time
from core.database import DatabaseManager

class TestDatabasePerformance:
    """Tests de performance de la base de données"""

    def setup_method(self):
        self.db = DatabaseManager()

    def test_query_performance(self):
        """Test de performance des requêtes"""
        start_time = time.time()

        # Exécuter une requête
        result = self.db.get_user_with_profile(1)

        execution_time = time.time() - start_time

        # Vérifier que la requête est rapide
        assert execution_time < 0.1  # Moins de 100ms
        assert result is not None

    def test_cache_performance(self):
        """Test de performance du cache"""
        # Premier appel (sans cache)
        start_time = time.time()
        result1 = self.db.get_user_with_profile(1)
        first_call_time = time.time() - start_time

        # Deuxième appel (avec cache)
        start_time = time.time()
        result2 = self.db.get_user_with_profile(1)
        second_call_time = time.time() - start_time

        # Le cache doit être plus rapide
        assert second_call_time < first_call_time
        assert result1 == result2

    @pytest.mark.benchmark
    def test_benchmark_user_queries(self, benchmark):
        """Benchmark des requêtes utilisateur"""
        def query_function():
            return self.db.get_user_with_profile(1)

        result = benchmark(query_function)
        assert result is not None


```text


---


## 📚 **Documentation**



### **UX Unifiée V4 - Systèmes Intégrés**


Depuis la V4, Arkalia Quest utilise des systèmes UX unifiés pour une expérience cohérente :


#### **Notifications Universelles**
- **Fichier** : `static/js/universal-notifications.js`
- **API** : `window.universalNotifications.show({ type, content, ... })`
- **Types** : `success`, `error`, `info`, `warning`, `celebration`
- **Intégration** : Gère tous les feedbacks utilisateur (LUNA, progression, erreurs)


#### **Système de Récompenses**
- **Fichier** : `static/js/reward-feedback-system.js`
- **API** : `window.rewardFeedbackSystem.showLevelUpReward({ level })`
- **Fonctionnalités** : Animations, sons, confettis, progression visuelle


#### **États Vides Intelligents**
- **Fichier** : `static/js/smart-empty-states.js`
- **API** : `window.smartEmptyStates.handleEmptyState(container, type)`
- **Types** : `missions`, `badges`, `leaderboard`, `profil`


#### **Performance UX**
- **Fichier** : `static/js/performance-ux-optimizer.js`
- **Fonctionnalités** : Lazy loading, animations optimisées, cache intelligent


#### **Modules Legacy (Dépréciés)**
- `adaptive-guidance.js` → Délègue vers `universal-notifications.js`
- `visual-guidance.js` → Délègue vers `universal-notifications.js`
- `reward-system.js` → Délègue vers `reward-feedback-system.js`
- `universal-feedback.js` → Délègue vers `universal-notifications.js`


### **Standards de Documentation**



#### **1. Docstrings Python**



```python


class SecurityManager:
    """
    Gestionnaire de sécurité professionnel pour Arkalia Quest.

    Ce gestionnaire fournit une protection multi-niveaux contre les menaces
    de sécurité, incluant le rate limiting, la validation des entrées,
    et le monitoring en temps réel.

    Attributes:
        security_events (List[Dict]): Liste des événements de sécurité
        blocked_ips (Set[str]): Ensemble des IPs bloquées
        suspicious_activities (List[Dict]): Activités suspectes détectées
        security_config (Dict): Configuration de sécurité

    Example:
        >>> security_manager = SecurityManager()
        >>> security_manager.check_rate_limit("192.168.1.100")
        True
        >>> security_manager.block_ip("192.168.1.100", "Test")
        >>> security_manager.is_ip_blocked("192.168.1.100")
        True
    """

    def __init__(self):
        """
        Initialise le gestionnaire de sécurité.

        Configure les paramètres de sécurité par défaut et charge
        la configuration depuis le fichier de config si disponible.
        """
        self.security_events = []
        self.blocked_ips = set()
        self.suspicious_activities = []
        self.security_config = self._load_default_config()
        self._load_security_config()

    def check_rate_limit(self, ip_address: str) -> bool:
        """
        Vérifie si une IP respecte les limites de taux.

        Args:
            ip_address (str): L'adresse IP à vérifier

        Returns:
            bool: True si l'IP respecte les limites, False sinon

        Raises:
            ValueError: Si l'adresse IP est invalide

        Example:
            >>> security_manager.check_rate_limit("192.168.1.100")
            True
        """
        if not self._is_valid_ip(ip_address):
            raise ValueError(f"Invalid IP address: {ip_address}")

        # Logique de vérification du rate limiting
        return self._check_ip_rate_limit(ip_address)


```text



#### **2. Documentation des API**



```python



# Documentation des endpoints avec docstrings


@app.route('/api/security/status', methods=['GET'])
def get_security_status():
    """
    Récupère le statut de sécurité actuel.

    ---
    tags:
      - Security
    summary: Statut de sécurité
    description: Retourne un aperçu complet du statut de sécurité
    responses:
      200:
        description: Statut de sécurité récupéré avec succès
        content:
          application/json:
            schema:
              type: object
              properties:
                total_events:
                  type: integer
                  description: Nombre total d'événements de sécurité
                blocked_ips:
                  type: integer
                  description: Nombre d'IPs bloquées
                threat_level:
                  type: string
                  enum: [low, medium, high, critical]
                  description: Niveau de menace actuel
                recent_events:
                  type: array
                  items:
                    type: object
                    properties:
                      timestamp:
                        type: string
                        format: date-time
                      event_type:
                        type: string
                      severity:
                        type: string
                        enum: [info, warning, error, critical]
      401:
        description: Non autorisé
      500:
        description: Erreur interne du serveur
    """
    try:
        security_status = security_manager.get_security_status()
        return jsonify(security_status), 200
    except Exception as e:
        app.logger.error(f"Error getting security status: {e}")
        return jsonify({"error": "Internal server error"}), 500


```text



### **Génération de Documentation**



```bash



# Génération de la documentation avec Sphinx


pip install sphinx sphinx-rtd-theme


# Initialisation du projet Sphinx


sphinx-quickstart docs/sphinx


# Génération de la documentation


cd docs/sphinx
make html


# Documentation disponible dans docs/sphinx/_build/html/



```text


---


## 🚀 **Déploiement**



### **Environnements de Déploiement**



```mermaid


graph TB
    subgraph "👨‍💻 Development"
        A[Local Development]
        B[Feature Branches]
        C[Code Review]
        D[Local Testing]
    end

    subgraph "🧪 Testing"
        E[Automated Tests]
        F[Integration Tests]
        G[Performance Tests]
        H[Security Tests]
    end

    subgraph "🚀 Staging"
        I[Staging Environment]
        J[User Acceptance]
        K[Performance Validation]
        L[Security Validation]
    end

    subgraph "🌐 Production"
        M[Production Deployment]
        N[Load Balancing]
        O[Monitoring]
        P[Backup & Recovery]
    end

    A --> B
    B --> C
    C --> D

    D --> E
    E --> F
    F --> G
    G --> H

    H --> I
    I --> J
    J --> K
    K --> L

    L --> M
    M --> N
    N --> O
    O --> P

    style A fill:#e8f5e8
    style E fill:#e3f2fd
    style I fill:#fff3e0
    style M fill:#ffebee


```text



### **Scripts de Déploiement**



#### **Script de Déploiement Automatique**



```bash


#!/bin/bash


# scripts/deploy.sh


set -e  # Arrêter en cas d'erreur

echo "🚀 Démarrage du déploiement..."


# Variables d'environnement


ENVIRONMENT=${1:-staging}
BRANCH=${2:-develop}

echo "📍 Environnement: $ENVIRONMENT"
echo "🌿 Branche: $BRANCH"


# 1. Vérification de l'état du code


echo "🔍 Vérification de l'état du code..."
git status --porcelain
if [ $? -ne 0 ]; then
    echo "❌ Erreur: Code non commité détecté"
    exit 1
fi


# 2. Tests automatisés


echo "🧪 Exécution des tests..."
python -m pytest tests/ -v --tb=no
if [ $? -ne 0 ]; then
    echo "❌ Erreur: Tests échoués"
    exit 1
fi


# 3. Vérification de la qualité du code


echo "🔧 Vérification de la qualité du code..."
black . --check
ruff check .
if [ $? -ne 0 ]; then
    echo "❌ Erreur: Problèmes de qualité détectés"
    exit 1
fi


# 4. Déploiement selon l'environnement


case $ENVIRONMENT in
    "staging")
        echo "🚀 Déploiement en staging..."
        # Logique de déploiement staging
        ;;
    "production")
        echo "🚀 Déploiement en production..."
        # Logique de déploiement production
        ;;
    *)
        echo "❌ Environnement non reconnu: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "✅ Déploiement terminé avec succès!"


```text



#### **Configuration Docker**



```dockerfile



# Dockerfile


FROM python:3.10-slim


# Définir le répertoire de travail


WORKDIR /app


# Installer les dépendances système


RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# Copier les fichiers de dépendances


COPY requirements.txt .


# Installer les dépendances Python


RUN pip install --no-cache-dir -r requirements.txt


# Copier le code source


COPY . .


# Créer les répertoires nécessaires


RUN mkdir -p logs data/database


# Exposer le port


EXPOSE 5000


# Variables d'environnement


ENV FLASK_ENV=production
ENV PYTHONPATH=/app


# Commande de démarrage


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]


```text



#### **Docker Compose**



```yaml



# docker-compose.yml


version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///data/database/arkalia.db
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


## 🤝 **Contribution**



### **Processus de Contribution**



```mermaid


flowchart TD
    A[🔍 Identifier un problème] --> B[📝 Créer une issue]
    B --> C[🌿 Créer une branche feature]
    C --> D[🔧 Développer la solution]
    D --> E[🧪 Écrire les tests]
    E --> F[📚 Mettre à jour la documentation]
    F --> G[🔍 Code review]
    G --> H{Review OK?}
    H -->|❌ Non| I[📝 Corrections]
    I --> G
    H -->|✅ Oui| J[🚀 Merge en develop]
    J --> K[🧪 Tests d'intégration]
    K --> L{Tests OK?}
    L -->|❌ Non| M[🔧 Corrections]
    M --> K
    L -->|✅ Oui| N[🚀 Merge en main]


```text



### **Checklist de Contribution**



#### **Avant de Soumettre**



- [ ] **🧪 Tests** : Tous les tests passent



- [ ] **🔧 Qualité** : Code formaté avec Black et Ruff



- [ ] **📚 Documentation** : Docstrings et README mis à jour



- [ ] **🔒 Sécurité** : Aucune vulnérabilité introduite



- [ ] **⚡ Performance** : Aucune régression de performance



- [ ] **📝 Commit** : Message de commit descriptif



#### **Format de Pull Request**



```markdown



## 🎯 Description


Description claire et concise des changements apportés.


## 🔍 Type de Changement



- [ ] Bug fix



- [ ] Nouvelle fonctionnalité



- [ ] Amélioration de performance



- [ ] Documentation



- [ ] Refactoring



## 🧪 Tests



- [ ] Tests unitaires ajoutés/mis à jour



- [ ] Tests d'intégration ajoutés/mis à jour



- [ ] Tests de performance ajoutés/mis à jour



- [ ] Tous les tests passent



## 📚 Documentation



- [ ] Docstrings mises à jour



- [ ] README mis à jour si nécessaire



- [ ] Changelog mis à jour



## 🔒 Sécurité



- [ ] Aucune vulnérabilité introduite



- [ ] Tests de sécurité ajoutés si nécessaire



## 📊 Impact


**Avant :** Description de l'état précédent
**Après :** Description du nouvel état


## 🔗 Liens


Fixes #123
Relates to #456


```text


---


## 📊 **Monitoring et Debugging**



### **Logging Structuré**



```python


import logging
import json
from datetime import datetime

class StructuredLogger:
    """Logger structuré pour Arkalia Quest"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Handler pour fichier
        file_handler = logging.FileHandler(f'logs/{name}.log')
        file_handler.setLevel(logging.INFO)

        # Formatter structuré
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_event(self, event_type: str, details: dict, level: str = "info"):
        """Log un événement structuré"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "level": level
        }

        log_message = json.dumps(log_data, ensure_ascii=False)

        if level == "error":
            self.logger.error(log_message)
        elif level == "warning":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)


# Utilisation


logger = StructuredLogger("security")
logger.log_event("login_attempt", {
    "user_id": 123,
    "ip_address": "192.168.1.100",
    "success": True
}, "info")


```text



### **Debugging Avancé**



```python


import pdb
import traceback
from functools import wraps

def debug_on_error(func):
    """Décorateur pour activer le debugger en cas d'erreur"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Erreur dans {func.__name__}: {e}")
            print("🔍 Traceback:")
            traceback.print_exc()

            # Activer le debugger en mode développement
            if app.config.get('DEBUG'):
                print("🐛 Démarrage du debugger...")
                pdb.set_trace()

            raise
    return wrapper


# Utilisation


@debug_on_error
def risky_function():
    """Fonction qui peut échouer"""
    result = 1 / 0  # Division par zéro
    return result


```text


---


## 🎯 **Conclusion**


Ce guide de développement fournit toutes les informations nécessaires pour contribuer efficacement au projet Arkalia Quest. En suivant ces bonnes pratiques, vous contribuerez à maintenir la qualité, la sécurité et les performances du projet.


### **Points Clés à Retenir**



- **🧪 Tests** : Écrivez des tests pour chaque nouvelle fonctionnalité



- **🔒 Sécurité** : Validez toujours les entrées et suivez les bonnes pratiques



- **⚡ Performance** : Optimisez le code et surveillez les métriques



- **📚 Documentation** : Documentez votre code et mettez à jour la documentation



- **🔧 Qualité** : Utilisez Black et Ruff pour maintenir la qualité du code



- **🚀 Déploiement** : Testez toujours en staging avant la production



### **Ressources Supplémentaires**



- [Architecture Technique](ARCHITECTURE_TECHNIQUE.md)



- [Guide de Déploiement](DEPLOYMENT_GUIDE.md)



- [API Reference](API_REFERENCE.md)



- [Troubleshooting](TROUBLESHOOTING.md)


---

# **🌟 Guide conçu avec ❤️ par l'équipe Arkalia Luna 🌟**

**Bonne contribution !** 🚀✨
