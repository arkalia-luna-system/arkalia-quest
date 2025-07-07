#!/bin/bash
export VIRTUAL_ENV="/Volumes/T7/devstation/arkalia-quest/.venv-quest"
export PATH="/Volumes/T7/devstation/arkalia-quest/.venv-quest/bin:$PATH"
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --port=5001 