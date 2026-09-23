#!/usr/bin/env bash
# Crea lo zip della demo da inviare o aprire sul computer del cliente.
set -euo pipefail

RADICE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NOME="${1:-demo-new-elettrocar}"
DESTINAZIONE="$RADICE/$NOME.zip"

rm -f "$DESTINAZIONE"
cd "$RADICE"
zip -r -q "$DESTINAZIONE" demo -x "demo/auto.json" "*/.DS_Store" "demo/img/crediti.json" "demo/img/rifiutate.json"
echo "Demo pronta: $DESTINAZIONE"
