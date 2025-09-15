# Configuration Gunicorn pour Arkalia Quest V3.2.0
# Serveur WSGI optimisé pour la production

import multiprocessing
import os

# Configuration de base
bind = f"0.0.0.0:{os.getenv('PORT', '5001')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000

# Gestion des requêtes
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Performance
preload_app = True
worker_tmp_dir = "/dev/shm"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Sécurité
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuration spécifique Arkalia Quest
raw_env = [
    "FLASK_ENV=production",
    "PYTHONPATH=/app",
]

# Optimisations pour les jeux éducatifs
worker_class = "sync"
worker_connections = 1000


# Configuration des processus
def when_ready(server):
    server.log.info("🌌 Arkalia Quest V3.2.0 - Serveur prêt")


def worker_int(worker):
    worker.log.info("⚡ Worker %s initialisé", worker.pid)


def pre_fork(server, worker):
    server.log.info("🚀 Worker %s en cours de démarrage", worker.pid)


def post_fork(server, worker):
    server.log.info("✅ Worker %s démarré", worker.pid)


def worker_abort(worker):
    worker.log.info("⚠️ Worker %s interrompu", worker.pid)
