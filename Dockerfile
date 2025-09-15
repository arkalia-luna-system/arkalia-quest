# Dockerfile pour Arkalia Quest - Configuration spécifique
FROM python:3.10.14-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt d'abord pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances Python avec pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p logs data/database data/uploads

# Exposer le port (Render utilise le port 10000 par défaut)
EXPOSE 10000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=10000

# Healthcheck pour vérifier que l'application est prête
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:10000/ || exit 1

# Commande de démarrage avec Gunicorn
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 2 --timeout 120 --worker-class sync --preload --access-logfile - --error-logfile - --log-level info"]
