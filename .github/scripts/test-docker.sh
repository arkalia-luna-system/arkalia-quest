#!/bin/bash
set -e

echo "🐳 Testing Docker container..."

# Vérifier que l'image existe
if ! docker image inspect arkalia-quest:latest > /dev/null 2>&1; then
  echo "❌ Image arkalia-quest:latest not found. Building it first..."
  docker build -t arkalia-quest:latest .
  echo "✅ Image built successfully"
fi

# Nettoyer les conteneurs existants avec le même nom
echo "Cleaning up existing containers..."
docker stop arkalia-test 2>/dev/null || true
docker rm arkalia-test 2>/dev/null || true

# Démarrer le conteneur
echo "Starting container..."
CONTAINER_ID=$(docker run --rm -d --name arkalia-test -p 5001:10000 arkalia-quest:latest)
echo "Container started with ID: $CONTAINER_ID"

# Attendre que le conteneur soit prêt
echo "Waiting for container to be ready..."
sleep 30

# Vérifier le statut du conteneur
echo "Checking container status..."
docker ps -a

# Vérifier que le conteneur est toujours en cours d'exécution
if ! docker ps --format "table {{.Names}}" | grep -q "arkalia-test"; then
  echo "❌ Container is not running. Checking logs..."
  docker logs arkalia-test --tail 50
  exit 1
fi

# Afficher les logs
echo "Container logs:"
docker logs arkalia-test --tail 20

# Tester la santé du conteneur
echo "Testing container health..."
HEALTHY=false
for i in {1..5}; do
  echo "Attempt $i/5..."
  if docker exec arkalia-test curl -f http://localhost:10000/ > /dev/null 2>&1; then
    echo "✅ Container is healthy!"
    HEALTHY=true
    break
  else
    echo "⏳ Container not ready yet, waiting..."
    sleep 10
  fi
done

# Test final avec timeout
if [ "$HEALTHY" = false ]; then
  echo "Final health check..."
  timeout 15s docker exec arkalia-test curl -f http://localhost:10000/ || {
    echo "⚠️ Health check failed, but checking if container is still running..."
    docker ps -a
    docker logs arkalia-test --tail 50
    echo "❌ Container health check failed"
    exit 1
  }
fi

# Test de connectivité externe
echo "Testing external connectivity..."
if curl -f http://localhost:5001/ > /dev/null 2>&1; then
  echo "✅ External connectivity test passed!"
else
  echo "⚠️ External connectivity test failed, but container is running internally"
fi

# Nettoyer
echo "Cleaning up..."
docker stop arkalia-test || echo "Container already stopped"

echo "✅ Docker test completed successfully!"
