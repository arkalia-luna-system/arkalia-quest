#!/usr/bin/env bash
# Lancement unifié des tests — Arkalia Quest
# Usage: ./run_tests.sh [options pytest...]   ex: ./run_tests.sh -q   ou   ./run_tests.sh tests/core/

set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate 2>/dev/null || true

echo "🧪 Tests Arkalia Quest..."
python -m pytest tests/ "$@" --tb=short -q
echo "✅ Terminé."
