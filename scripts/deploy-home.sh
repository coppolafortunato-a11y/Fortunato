#!/usr/bin/env bash
#
# Obiettivo 1 del briefing — pubblica home-wordpress.html sulla pagina ID 7 di ideamkt.it
#
# Esegue in sequenza:
#   1. verifica autenticazione (application password)
#   2. backup del contenuto attuale della pagina 7
#   3. prepara il payload (wrap blocco wp:html + fix larghezza piena)
#   4. POST alla pagina 7
#   5. verifica che 'ik-home' sia presente nel contenuto salvato
#
# Uso:
#   ./scripts/deploy-home.sh              # deploy completo
#   FULLWIDTH=0 ./scripts/deploy-home.sh  # senza il fix larghezza piena
#   ./scripts/deploy-home.sh --dry-run    # prepara payload.json senza inviare nulla
#
set -euo pipefail

# --- posizionamento nella root del progetto -------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

PAGE_ID=7
SRC="home-wordpress.html"
FULLWIDTH="${FULLWIDTH:-1}"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

# --- caricamento .env ------------------------------------------------------
if [ ! -f .env ]; then
	echo "ERRORE: manca il file .env. Copia .env.example in .env e compilalo." >&2
	exit 1
fi
set -a; source .env; set +a

: "${WP_USER:?WP_USER non impostato in .env}"
: "${WP_APP_PASSWORD:?WP_APP_PASSWORD non impostato in .env}"
: "${WP_BASE:?WP_BASE non impostato in .env}"

if [ ! -f "$SRC" ]; then
	echo "ERRORE: $SRC non trovato." >&2
	exit 1
fi

AUTH="$WP_USER:$WP_APP_PASSWORD"

# --- passo 1: verifica autenticazione -------------------------------------
echo "==> [1/5] Verifica autenticazione..."
ME="$(curl -s -u "$AUTH" "$WP_BASE/wp-json/wp/v2/users/me?context=edit")"
if echo "$ME" | grep -q '"rest_not_logged_in"\|"rest_cannot_access"'; then
	echo "ERRORE: autenticazione fallita. Risposta:" >&2
	echo "$ME" | head -c 400 >&2; echo >&2
	echo "Se vedi rest_not_logged_in, l'hosting rimuove l'header Authorization." >&2
	echo "Aggiungi in .htaccess (radice del sito):" >&2
	echo '  SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1' >&2
	exit 1
fi
echo "    OK — autenticato."

# --- passo 2: backup -------------------------------------------------------
echo "==> [2/5] Backup della pagina $PAGE_ID..."
STAMP="$(date +%Y%m%d-%H%M)"
BACKUP="backup-home-$STAMP.json"
curl -s -u "$AUTH" \
	"$WP_BASE/wp-json/wp/v2/pages/$PAGE_ID?context=edit&_fields=id,title,content" \
	> "$BACKUP"

BSIZE="$(wc -c < "$BACKUP" | tr -d ' ')"
if [ "$BSIZE" -lt 1000 ]; then
	echo "ERRORE: backup vuoto o troppo corto ($BSIZE byte). Non procedo." >&2
	echo "Contenuto ricevuto:" >&2; head -c 400 "$BACKUP" >&2; echo >&2
	exit 1
fi
echo "    OK — salvato $BACKUP ($BSIZE byte)."

# --- passo 3: preparazione payload ----------------------------------------
echo "==> [3/5] Preparazione payload (fullwidth=$FULLWIDTH)..."
FULLWIDTH="$FULLWIDTH" SRC="$SRC" python3 - <<'PY'
import json, os, re

src = os.environ['SRC']
fullwidth = os.environ.get('FULLWIDTH', '1') == '1'

body = open(src, encoding='utf-8').read()

# Modifica 2: sfonda il contenitore a larghezza limitata del tema.
if fullwidth:
    fix = ';width:100vw;max-width:100vw;margin-left:calc(50% - 50vw);overflow-x:hidden'
    # inserisce in coda alla prima regola #ik-home{...}, prima della graffa di chiusura
    new_body, n = re.subn(r'(#ik-home\{[^}]*?)\}', r'\1' + fix + '}', body, count=1)
    if n == 0:
        raise SystemExit('ERRORE: regola #ik-home{...} non trovata, impossibile applicare il fix larghezza.')
    if fix not in new_body:  # idempotenza / sanity
        raise SystemExit('ERRORE: fix larghezza non applicato.')
    body = new_body

# Modifica 1: avvolgi tutto nel blocco HTML di Gutenberg
content = '<!-- wp:html -->\n' + body + '\n<!-- /wp:html -->'

json.dump({'content': content, 'status': 'publish'},
          open('payload.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('    OK — payload.json creato (%d byte).' % os.path.getsize('payload.json'))
PY

if [ "$DRY_RUN" -eq 1 ]; then
	echo "==> --dry-run: payload.json pronto, nessun invio effettuato."
	exit 0
fi

# --- passo 4: invio --------------------------------------------------------
echo "==> [4/5] Invio alla pagina $PAGE_ID..."
RESP="$(curl -s -u "$AUTH" \
	-X POST "$WP_BASE/wp-json/wp/v2/pages/$PAGE_ID" \
	-H "Content-Type: application/json; charset=utf-8" \
	--data-binary @payload.json)"

if ! echo "$RESP" | python3 -c 'import sys,json; d=json.load(sys.stdin); sys.exit(0 if d.get("id") else 1)' 2>/dev/null; then
	echo "ERRORE: risposta inattesa dal server:" >&2
	echo "$RESP" | head -c 600 >&2; echo >&2
	exit 1
fi
echo "    OK — pagina aggiornata."

# --- passo 5: verifica -----------------------------------------------------
echo "==> [5/5] Verifica..."
COUNT="$(curl -s -u "$AUTH" \
	"$WP_BASE/wp-json/wp/v2/pages/$PAGE_ID?context=edit&_fields=content" \
	| grep -c 'ik-home' || true)"

if [ "$COUNT" -ge 1 ]; then
	echo "    OK — 'ik-home' presente nel contenuto salvato."
	echo
	echo "Fatto. Apri $WP_BASE in incognito e controlla l'hero navy"
	echo "con il titolo \"Diamo forma alla tua immagine\"."
else
	echo "ATTENZIONE: 'ik-home' non trovato nella verifica. Controlla manualmente." >&2
	exit 1
fi
