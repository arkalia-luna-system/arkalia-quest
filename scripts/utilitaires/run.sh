#!/bin/bash
export VIRTUAL_ENV="$(pwd)/.venv-quest"
export PATH="$(pwd)/.venv-quest/bin:$PATH"
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --port=5001 