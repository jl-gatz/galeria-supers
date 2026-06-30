#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:8000}"
PROFILE_DIR="/tmp/galeria-kiosk-profile"

rm -rf "$PROFILE_DIR"

if command -v chromium-browser >/dev/null 2>&1; then
  BROWSER="chromium-browser"
elif command -v chromium >/dev/null 2>&1; then
  BROWSER="chromium"
elif command -v google-chrome >/dev/null 2>&1; then
  BROWSER="google-chrome"
else
  echo "Nenhum Chromium/Chrome encontrado."
  exit 1
fi

"$BROWSER" \
  --kiosk \
  --user-data-dir="$PROFILE_DIR" \
  --no-first-run \
  --no-default-browser-check \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  "$URL"