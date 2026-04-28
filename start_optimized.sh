#!/usr/bin/env bash
# Délègue au script unifié (mode production / Gunicorn)
set -euo pipefail
cd "$(dirname "$0")"
exec ./start.sh prod
