#!/bin/bash
# Délègue au script unifié (mode production / Gunicorn)
cd "$(dirname "$0")"
exec ./start.sh prod
