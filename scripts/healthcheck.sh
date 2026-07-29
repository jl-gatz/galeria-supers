#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8000}"

echo "Testando aplicação..."
curl -I "$BASE_URL"

echo
echo "Testando logo..."
curl -I "$BASE_URL/images/logos/logo-detic-4x.png"

echo
echo "Testando foto sem grayscale..."
curl -I "$BASE_URL/images/supers/01-prof-alfredo.png" || true

echo
echo "Testando foto com grayscale..."
curl -I "$BASE_URL/images/supers/grayscale/01-prof-alfredo.png" || true