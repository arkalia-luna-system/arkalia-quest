#!/bin/bash
# Délègue au script unifié (mode évaluation + vérification)
cd "$(dirname "$0")"
exec ./start.sh eval
