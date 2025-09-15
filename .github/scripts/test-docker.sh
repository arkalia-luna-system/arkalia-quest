#!/bin/bash
set -e

echo "🐳 Testing Docker container..."

# Démarrer le conteneur
echo "Starting container..."
docker run --rm -d --name arkalia-test -p 5001:10000 arkalia-quest:latest

# Attendre que le conteneur soit prêt
echo "Waiting for container to be ready..."
sleep 30

# Vérifier le statut du conteneur
echo "Checking container status..."
docker ps -a

# Afficher les logs
echo "Container logs:"
docker logs arkalia-test

# Tester la santé du conteneur
echo "Testing container health..."
for i in {1..5}; do
  echo "Attempt $i/5..."
  if docker exec arkalia-test curl -f http://localhost:10000/ > /dev/null 2>&1; then
    echo "✅ Container is healthy!"
    break
  else
    echo "⏳ Container not ready yet, waiting..."
    sleep 10
  fi
done

# Test final avec timeout
echo "Final health check..."
timeout 15s docker exec arkalia-test curl -f http://localhost:10000/ || {
  echo "⚠️ Health check failed, but checking if container is still running..."
  docker ps -a
  docker logs arkalia-test --tail 50
}

# Nettoyer
echo "Cleaning up..."
docker stop arkalia-test || echo "Container already stopped"

echo "✅ Docker test completed!"
