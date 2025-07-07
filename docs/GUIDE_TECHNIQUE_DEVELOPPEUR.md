# 🛠️ GUIDE TECHNIQUE DÉVELOPPEUR - ARKALIA QUEST v3.0

> **Documentation technique complète pour contribuer au développement**

## 📋 TABLE DES MATIÈRES

1. [🏗️ Architecture](#-architecture)
2. [🚀 Installation Développement](#-installation-développement)
3. [📁 Structure du Projet](#-structure-du-projet)
4. [🔧 Configuration](#-configuration)
5. [🧪 Tests](#-tests)
6. [🤖 IA LUNA](#-ia-luna)
7. [🗄️ Base de Données](#-base-de-données)
8. [🔌 WebSockets](#-websockets)
9. [🎨 Frontend](#-frontend)
10. [🚀 Déploiement](#-déploiement)
11. [📝 Contribution](#-contribution)

---

## 🏗️ ARCHITECTURE

### 🎯 **VUE D'ENSEMBLE**

```
Arkalia Quest v3.0
├── Backend (Flask)
│   ├── app.py                    # Application principale
│   ├── core/                     # Modules principaux
│   ├── engines/                  # Moteurs spécialisés
│   └── mission_utils/            # Utilitaires de missions
├── Frontend (HTML/CSS/JS)
│   ├── templates/                # Pages web
│   ├── static/                   # Assets
│   └── js/                       # JavaScript
└── Data (JSON/SQLite)
    ├── missions/                 # Missions du jeu
    ├── profiles/                 # Profils utilisateurs
    └── config/                   # Configuration
```

### 🔄 **FLUX DE DONNÉES**

```
Utilisateur → Frontend → Flask API → Core Modules → Database
                ↓           ↓           ↓           ↓
             WebSocket ← LUNA AI ← Game Engine ← SQLite
```

---

## 🚀 INSTALLATION DÉVELOPPEMENT

### 📋 **PRÉREQUIS**

- **Python 3.9+**
- **Git**
- **Node.js** (optionnel, pour les outils frontend)

### 🔧 **INSTALLATION RAPIDE**

```bash
# Cloner le repository
git clone https://github.com/arkalia-luna-system/arkalia-quest.git
cd arkalia-quest

# Créer l'environnement virtuel
python -m venv .venv-quest
source .venv-quest/bin/activate  # macOS/Linux
# ou
.venv-quest\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer en mode développement
python app.py
```

### ⚙️ **VARIABLES D'ENVIRONNEMENT**

Crée un fichier `.env` :

```env
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5001
DATABASE_URL=sqlite:///arkalia.db
SECRET_KEY=your-secret-key-here
```

---

## 📁 STRUCTURE DU PROJET

### 🎯 **MODULES PRINCIPAUX**

#### **`app.py` - Application Flask**
```python
# Configuration principale
app = Flask(__name__)
app.config.from_object('config')

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commande', methods=['POST'])
def commande():
    # Gestion des commandes
    pass
```

#### **`core/` - Modules Principaux**

**`command_handler.py`**
```python
class CommandHandler:
    def __init__(self):
        self.commands = {}
        self.load_commands()
    
    def execute(self, command, user_id):
        # Exécution des commandes
        pass
```

**`game_engine.py`**
```python
class GameEngine:
    def __init__(self):
        self.luna_ai = LunaAI()
        self.profile_manager = ProfileManager()
    
    def process_action(self, action, user_id):
        # Traitement des actions de jeu
        pass
```

**`profile_manager.py`**
```python
class ProfileManager:
    def __init__(self):
        self.db = Database()
    
    def get_profile(self, user_id):
        # Récupération du profil
        pass
    
    def update_profile(self, user_id, data):
        # Mise à jour du profil
        pass
```

**`database.py`**
```python
class Database:
    def __init__(self):
        self.connection = sqlite3.connect('arkalia.db')
    
    def execute_query(self, query, params=None):
        # Exécution de requêtes SQL
        pass
```

**`websocket_manager.py`**
```python
class WebSocketManager:
    def __init__(self):
        self.rooms = {}
    
    def create_room(self, room_id):
        # Création d'une room
        pass
    
    def join_room(self, room_id, user_id):
        # Rejoindre une room
        pass
```

#### **`engines/` - Moteurs Spécialisés**

**`luna_ai.py`**
```python
class LunaAI:
    def __init__(self):
        self.personality_data = self.load_personality()
        self.meme_engine = MemeEngine()
    
    def respond(self, message, user_context):
        # Réponse de LUNA
        pass
    
    def analyze_action(self, action, context):
        # Analyse d'action
        pass
```

**`effects_engine.py`**
```python
class EffectsEngine:
    def __init__(self):
        self.effects = self.load_effects()
    
    def play_effect(self, effect_name):
        # Jouer un effet
        pass
    
    def screen_shake(self):
        # Effet d'écran qui tremble
        pass
```

### 📊 **DONNÉES**

#### **Structure JSON**

**`data/missions/`**
```json
{
  "id": "mission_1",
  "title": "Introduction",
  "description": "Découvre Arkalia Quest",
  "objectives": ["explore", "interact"],
  "rewards": {
    "xp": 50,
    "badges": ["debutant"]
  }
}
```

**`data/profiles/`**
```json
{
  "user_id": "user_123",
  "username": "HackerRebelle",
  "level": 3,
  "xp": 250,
  "badges": ["debutant", "hacker"],
  "missions_completed": ["mission_1", "mission_2"]
}
```

---

## 🔧 CONFIGURATION

### ⚙️ **CONFIGURATION FLASK**

**`config.py`**
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///arkalia.db'
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    PORT = int(os.environ.get('PORT', 5001))
```

### 🗄️ **CONFIGURATION BASE DE DONNÉES**

**`core/database.py`**
```python
def init_db():
    """Initialise la base de données"""
    with app.app_context():
        db.create_all()
        # Création des tables
        create_tables()
```

---

## 🧪 TESTS

### 🎯 **STRUCTURE DES TESTS**

```
tests/
├── test_arkalia.py              # Tests principaux
├── test_integration_complete.py # Tests d'intégration
├── test_multi_profiles.py       # Tests multi-profils
├── test_stress_simulation.py    # Tests de stress
└── test_interface_complete.py   # Tests d'interface
```

### 🚀 **LANCER LES TESTS**

```bash
# Tous les tests
python -m pytest tests/

# Tests spécifiques
python -m pytest tests/test_arkalia.py -v

# Tests avec couverture
python -m pytest --cov=core tests/

# Tests de stress
python tests/test_stress_simulation.py
```

### 📊 **EXEMPLE DE TEST**

```python
def test_luna_response():
    """Test de la réponse de LUNA"""
    luna = LunaAI()
    response = luna.respond("aide", {"user_id": "test"})
    assert "aide" in response.lower()
    assert len(response) > 0
```

---

## 🤖 IA LUNA

### 🧠 **ARCHITECTURE LUNA**

```python
class LunaAI:
    def __init__(self):
        self.personality = PersonalityEngine()
        self.meme_engine = MemeEngine()
        self.learning = LearningEngine()
    
    def respond(self, input_text, context):
        # 1. Analyse du contexte
        context_analysis = self.analyze_context(context)
        
        # 2. Génération de réponse
        response = self.generate_response(input_text, context_analysis)
        
        # 3. Personnalisation
        personalized_response = self.personalize(response, context)
        
        return personalized_response
```

### 🎭 **SYSTÈME DE PERSONNALITÉ**

**`data/personality_data.json`**
```json
{
  "traits": {
    "rebellious": 0.8,
    "humorous": 0.7,
    "helpful": 0.9,
    "sarcastic": 0.6
  },
  "responses": {
    "greeting": ["Salut rebelle !", "Hey hacker !"],
    "error": ["T'es nul ou tu le fais exprès ?", "Erreur 404: cerveau non trouvé"]
  }
}
```

### 🎪 **MOTEUR DE MEMES**

```python
class MemeEngine:
    def __init__(self):
        self.memes = self.load_memes()
    
    def get_meme(self, context, user_level):
        # Sélection de meme basée sur le contexte
        pass
    
    def generate_insult(self, command):
        # Génération d'insulte amicale
        pass
```

---

## 🗄️ BASE DE DONNÉES

### 📊 **SCHÉMA SQLITE**

```sql
-- Table des profils utilisateurs
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    level INTEGER DEFAULT 1,
    xp INTEGER DEFAULT 0,
    badges TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des missions
CREATE TABLE missions (
    id INTEGER PRIMARY KEY,
    mission_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id TEXT,
    completed_at TIMESTAMP
);

-- Table des actions
CREATE TABLE actions (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    action_data TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🔄 **OPÉRATIONS CRUD**

```python
class DatabaseManager:
    def create_profile(self, user_id, username):
        """Créer un nouveau profil"""
        pass
    
    def get_profile(self, user_id):
        """Récupérer un profil"""
        pass
    
    def update_profile(self, user_id, data):
        """Mettre à jour un profil"""
        pass
    
    def delete_profile(self, user_id):
        """Supprimer un profil"""
        pass
```

---

## 🔌 WEBSOCKETS

### 🌐 **ARCHITECTURE WEBSOCKET**

```python
class WebSocketManager:
    def __init__(self):
        self.rooms = {}
        self.connections = {}
    
    def handle_connection(self, websocket, path):
        """Gestion des connexions WebSocket"""
        pass
    
    def handle_message(self, websocket, message):
        """Gestion des messages"""
        pass
    
    def broadcast_to_room(self, room_id, message):
        """Diffusion dans une room"""
        pass
```

### 🎮 **DÉFIS TEMPS RÉEL**

```python
class ChallengeRoom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = []
        self.timer = None
        self.status = "waiting"
    
    def add_player(self, player):
        """Ajouter un joueur"""
        pass
    
    def start_challenge(self):
        """Démarrer le défi"""
        pass
    
    def end_challenge(self):
        """Terminer le défi"""
        pass
```

---

## 🎨 FRONTEND

### 🎯 **STRUCTURE HTML**

**`templates/terminal.html`**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Arkalia Quest - Terminal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="terminal-container">
        <div class="terminal-header">
            <h1>🌙 ARKALIA QUEST TERMINAL</h1>
        </div>
        <div class="terminal-body">
            <div id="output"></div>
            <div class="input-line">
                <span class="prompt">></span>
                <input type="text" id="command-input" autocomplete="off">
            </div>
        </div>
    </div>
    <script src="{{ url_for('static', filename='js/terminal.js') }}"></script>
</body>
</html>
```

### 🎨 **STYLES CSS**

**`static/style.css`**
```css
/* Thème sombre cyberpunk */
:root {
    --bg-color: #0a0a0a;
    --text-color: #00ff00;
    --accent-color: #ff0066;
    --terminal-bg: #000000;
}

.terminal-container {
    background: var(--terminal-bg);
    color: var(--text-color);
    font-family: 'Courier New', monospace;
    padding: 20px;
    border: 2px solid var(--accent-color);
    border-radius: 10px;
}

/* Effets d'animation */
@keyframes screen-shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

.screen-shake {
    animation: screen-shake 0.5s ease-in-out;
}
```

### ⚡ **JAVASCRIPT**

**`static/js/terminal.js`**
```javascript
class Terminal {
    constructor() {
        this.output = document.getElementById('output');
        this.input = document.getElementById('command-input');
        this.init();
    }
    
    init() {
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand(this.input.value);
            }
        });
    }
    
    async executeCommand(command) {
        try {
            const response = await fetch('/commande', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cmd: command })
            });
            
            const result = await response.json();
            this.displayResult(result);
        } catch (error) {
            this.displayError(error);
        }
    }
    
    displayResult(result) {
        const line = document.createElement('div');
        line.className = 'output-line';
        line.innerHTML = result.message;
        this.output.appendChild(line);
        this.scrollToBottom();
    }
}
```

---

## 🚀 DÉPLOIEMENT

### 🌐 **RENDER**

**`render.yaml`**
```yaml
services:
  - type: web
    name: arkalia-quest
    runtime: python
    buildCommand: poetry install
    startCommand: poetry run gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PORT
        value: 5001
```

### 🐳 **DOCKER (OPTIONNEL)**

**`Dockerfile`**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5001"]
```

### 🔧 **GUNICORN**

**`start_gunicorn.sh`**
```bash
#!/bin/bash
gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

---

## 📝 CONTRIBUTION

### 🎯 **GUIDELINES**

1. **Style de code** : Suivre PEP 8
2. **Tests** : Ajouter des tests pour les nouvelles fonctionnalités
3. **Documentation** : Documenter les changements
4. **Commits** : Messages clairs et descriptifs

### 🔄 **WORKFLOW**

```bash
# 1. Fork le repository
# 2. Clone ton fork
git clone https://github.com/ton-username/arkalia-quest.git

# 3. Crée une branche
git checkout -b feature/nouvelle-fonctionnalite

# 4. Développe
# ... code ...

# 5. Tests
python -m pytest tests/

# 6. Commit
git add .
git commit -m "✨ Ajout nouvelle fonctionnalité"

# 7. Push
git push origin feature/nouvelle-fonctionnalite

# 8. Pull Request
```

### 🧪 **TESTS OBLIGATOIRES**

```bash
# Tests unitaires
python -m pytest tests/ -v

# Tests d'intégration
python -m pytest tests/test_integration_complete.py -v

# Tests de performance
python tests/test_stress_simulation.py

# Couverture de code
python -m pytest --cov=core --cov-report=html tests/
```

### 📚 **DOCUMENTATION**

- **README.md** : Mise à jour obligatoire
- **Changelog** : Ajouter les changements
- **API docs** : Documenter les nouvelles routes
- **Guides** : Mettre à jour les guides utilisateur

---

## 🎉 CONCLUSION

**Arkalia Quest** est un projet open-source qui combine :
- **Éducation** : Apprentissage de la cybersécurité
- **Technologie** : IA, WebSockets, base de données
- **Créativité** : Interface unique et personnalité LUNA
- **Communauté** : Défis sociaux et collaboration

### 🚀 **PROCHAINES ÉTAPES**

1. **Améliorer l'IA** : Machine learning avancé
2. **Nouvelles missions** : Contenu additionnel
3. **Mobile app** : Application native
4. **API publique** : Documentation complète

### 🤝 **REJOINS L'AVENTURE**

**Contribue au développement d'Arkalia Quest et aide à créer la prochaine génération de hackers éthiques !**

---

*Guide technique créé avec ❤️ par l'équipe Arkalia Quest*  
*Version 3.0 - 2025* 