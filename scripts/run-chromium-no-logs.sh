#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:8000}"
PROFILE_DIR="/tmp/galeria-kiosk-profile"

rm -rf "$PROFILE_DIR"

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