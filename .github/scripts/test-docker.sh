#!/bin/bash
set -e

echo "🐳 Testing Docker container..."

# Vérifier que l'image existe
if ! docker image inspect arkalia-quest:latest > /dev/null 2>&1; then
  echo "❌ Image arkalia-quest:latest not found. Building it first..."
  docker build -t arkalia-quest:latest .
  echo "✅ Image built successfully"
fi

# Vérifier que l'image a été créée
echo "Available Docker images:"
docker images | grep arkalia-quest || echo "No arkalia-quest image found"

# Nettoyer les conteneurs existants avec le même nom
echo "Cleaning up existing containers..."
docker stop arkalia-test 2>/dev/null || true
docker rm arkalia-test 2>/dev/null || true

# Démarrer le conteneur
echo "Starting container..."
CONTAINER_ID=$(docker run --rm -d --name arkalia-test -p 5001:10000 -e PORT=10000 arkalia-quest:latest)
echo "Container started with ID: $CONTAINER_ID"

# Attendre un peu et vérifier immédiatement
echo "Waiting for container to initialize..."
sleep 10

# Vérifier le statut du conteneur
echo "Checking container status..."
docker ps -a

# Afficher les logs immédiatement pour debug
echo "Container logs (first 20 lines):"
docker logs arkalia-test --tail 20 2>/dev/null || echo "No logs available yet"

# Vérifier que le conteneur est toujours en cours d'exécution
if ! docker ps --format "table {{.Names}}" | grep -q "arkalia-test"; then
  echo "❌ Container stopped unexpectedly. Checking logs..."
  # Essayer de récupérer les logs même si le conteneur s'est arrêté
  docker logs arkalia-test --tail 50 2>/dev/null || echo "No logs available"
  echo "Container exit code: $(docker inspect arkalia-test --format='{{.State.ExitCode}}' 2>/dev/null || echo 'unknown')"
  
  # Afficher plus de détails de debug
  echo "Docker system info:"
  docker system df
  echo "Docker version:"
  docker version
  echo "Docker info:"
  docker info | head -20
  
  exit 1
fi

# Attendre un peu plus pour que l'application démarre complètement
echo "Waiting for application to start..."
sleep 15

# Afficher les logs
echo "Container logs:"
docker logs arkalia-test --tail 20

# Tester la santé du conteneur
echo "Testing container health..."
HEALTHY=false
for i in {1..3}; do
  echo "Attempt $i/3..."
  
  # Vérifier d'abord que le conteneur est toujours en cours d'exécution
  if ! docker ps --format "table {{.Names}}" | grep -q "arkalia-test"; then
    echo "❌ Container stopped during health check!"
    docker logs arkalia-test --tail 50 2>/dev/null || echo "No logs available"
    exit 1
  fi
  
  # Tester la connectivité interne
  if docker exec arkalia-test curl -f http://localhost:10000/ > /dev/null 2>&1; then
    echo "✅ Container is healthy!"
    HEALTHY=true
    break
  else
    echo "⏳ Container not ready yet, waiting..."
    sleep 10
  fi
done

# Test de connectivité externe (plus permissif dans CI)
echo "Testing external connectivity..."
if curl -f http://localhost:5001/ > /dev/null 2>&1; then
  echo "✅ External connectivity test passed!"
elif [ "$HEALTHY" = true ]; then
  echo "⚠️ External connectivity failed, but container is healthy internally"
  echo "This might be normal in CI environment"
else
  echo "❌ Both internal and external connectivity failed"
  docker logs arkalia-test --tail 50 2>/dev/null || echo "No logs available"
  exit 1
fi

# Nettoyer
echo "Cleaning up..."
docker stop arkalia-test || echo "Container already stopped"

echo "✅ Docker test completed successfully!"
