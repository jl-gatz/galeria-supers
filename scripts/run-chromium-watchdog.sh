#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:8000}"
PROFILE_DIR="$HOME/.config/galeria-kiosk/chromium-profile"

mkdir -p "$PROFILE_DIR"

while true; do
  chromium-browser \
    --kiosk \
    --user-data-dir="$PROFILE_DIR" \
    --no-first-run \
    --no-default-browser-check \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --disable-background-networking \
    --disable-sync \
    --disable-translate \
    --disable-component-update \
    --disable-domain-reliability \
    --disable-features=MediaRouter,OptimizationHints,AutofillServerCommunication \
    --metrics-recording-only \
    --safebrowsing-disable-auto-update \
    --password-store=basic \
    --use-mock-keychain \
    "$URL"

  echo "Chromium saiu. Reiniciando em 5 segundos..."
  sleep 5
done