#!/usr/bin/env bash
# Délègue au script unifié (mode évaluation + vérification)
set -euo pipefail
cd "$(dirname "$0")"
exec ./start.sh eval
