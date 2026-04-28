#!/usr/bin/env bash
# Lancement unifié des tests — Arkalia Quest
# Usage: ./run_tests.sh [options pytest...]   ex: ./run_tests.sh -q   ou   ./run_tests.sh tests/core/

set -euo pipefail
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d "venv" ]; then
    "$PYTHON_BIN" -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate

echo "🧪 Tests Arkalia Quest..."
python -m pytest tests/ "$@" --tb=short -q
echo "✅ Terminé."
