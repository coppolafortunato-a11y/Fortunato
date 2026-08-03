#!/usr/bin/env bash
#
# Obiettivo 3.4 del briefing — verifica gli slug reali delle pagine.
#
# La home punta a /contatti/, /servizi/, /ledwall-digital-signage/, /preventivi-ledwall/.
# Questo script elenca id/slug/titolo di tutte le pagine così puoi confrontarli
# con gli href in home-wordpress.html e correggerli se non combaciano.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

if [ -f .env ]; then set -a; source .env; set +a; fi
: "${WP_BASE:?WP_BASE non impostato: mettilo in .env oppure passalo come variabile}"

echo "==> Slug attuali su $WP_BASE:"
curl -s "$WP_BASE/wp-json/wp/v2/pages?per_page=50&_fields=id,slug,title" \
	| python3 -m json.tool

cat <<'NOTE'

Href usati nella home (verificati contro gli slug reali il 2026-08-03):
  /contatti/             -> contatti (ID 16)            ok
  /servizi/              -> servizi (ID 10)             ok
  /ledwall/              -> ledwall (ID 12)             ok (era /ledwall-digital-signage/, corretto)
  /preventivi-ledwall/   -> preventivi-ledwall (ID 27)  ok
  #ik-servizi            (ancora interna, ok)

Se uno slug non combacia, correggi l'href in home-wordpress.html
e rilancia ./scripts/deploy-home.sh
NOTE
