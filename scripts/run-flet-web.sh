#!/usr/bin/env bash
set -euo pipefail

FLET_FORCE_WEB_SERVER=true \
FLET_SERVER_IP=127.0.0.1 \
FLET_SERVER_PORT=8000 \
poetry run python -m galeria.main