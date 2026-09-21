#!/usr/bin/env bash
# Crea lo zip del plugin pronto da caricare su WordPress.
set -euo pipefail

RADICE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DESTINAZIONE="${1:-$RADICE/concessionaria-auto.zip}"

rm -f "$DESTINAZIONE"
cd "$RADICE/plugin"
zip -r -q "$DESTINAZIONE" concessionaria-auto -x "*.DS_Store"
echo "Plugin pronto: $DESTINAZIONE"
