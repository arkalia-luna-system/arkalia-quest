# Dockerfile pour Arkalia Quest - Force l'utilisation de pip
FROM python:3.10.14-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements.txt d'abord pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances avec pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port (Render utilise le port 10000 par défaut)
EXPOSE 10000

# Commande de démarrage
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 2 --timeout 120 --preload"]
