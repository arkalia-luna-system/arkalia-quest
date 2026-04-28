#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_BUILD_DIR="$(mktemp -d "/tmp/arkalia-build-XXXXXX")"
TMP_SRC_DIR="${TMP_BUILD_DIR}/src"

cleanup() {
  rm -rf "${TMP_BUILD_DIR}"
}
trap cleanup EXIT

echo "🏗️ Build package depuis espace temporaire propre..."
mkdir -p "${TMP_SRC_DIR}"

rsync -a \
  --exclude ".git" \
  --exclude ".venv" \
  --exclude "venv" \
  --exclude "build" \
  --exclude "dist" \
  --exclude "site" \
  --exclude ".mypy_cache" \
  --exclude ".pytest_cache" \
  --exclude ".ruff_cache" \
  --exclude "__pycache__" \
  --exclude "logs" \
  --exclude "._*" \
  "${ROOT_DIR}/" "${TMP_SRC_DIR}/"

cd "${TMP_SRC_DIR}"

python3 -m pip install --upgrade pip
pip install build twine

python3 - <<'PY'
import os
removed = 0
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith("._")]
    for name in files:
        if name.startswith("._"):
            os.remove(os.path.join(root, name))
            removed += 1
print(f"Removed AppleDouble artifacts before build: {removed}")
PY

python3 -m build
twine check dist/*

mkdir -p "${ROOT_DIR}/dist"
cp -f dist/* "${ROOT_DIR}/dist/"

echo "✅ Build terminé. Artifacts copiés dans dist/"
