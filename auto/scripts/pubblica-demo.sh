#!/usr/bin/env bash
#
# Carica la demo su uno spazio web via FTP, per mostrarla al cliente da un
# indirizzo vero (telefono compreso) invece che con lo zip.
#
# Serve un .env nella radice del repository con FTP_HOST, FTP_USER, FTP_PASS
# (gli stessi usati dagli altri script). Le credenziali restano sul tuo
# computer: non stanno nel repository e non devono starci.
#
# Uso:
#   bash auto/scripts/pubblica-demo.sh                      # ideamkt.it/demo/new-elettrocar/
#   bash auto/scripts/pubblica-demo.sh public_html/demo/prova
#   bash auto/scripts/pubblica-demo.sh public_html "https://demo.ideamkt.it"   # sottodominio
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ROOT_DIR="$(cd "$AUTO_DIR/.." && pwd)"

CARTELLA_REMOTA="${1:-public_html/demo/new-elettrocar}"
INDIRIZZO="${2:-https://ideamkt.it/${CARTELLA_REMOTA#public_html/}}"

if [ ! -f "$ROOT_DIR/.env" ]; then
	echo "ERRORE: manca $ROOT_DIR/.env (copia .env.example e compila FTP_HOST/FTP_USER/FTP_PASS)." >&2
	exit 1
fi
set -a; source "$ROOT_DIR/.env"; set +a

if [ -z "${FTP_HOST:-}" ] || [ -z "${FTP_USER:-}" ] || [ -z "${FTP_PASS:-}" ]; then
	echo "ERRORE: FTP_HOST, FTP_USER o FTP_PASS non impostati in .env." >&2
	echo "In alternativa carica a mano la cartella auto/demo da cPanel -> Gestione file." >&2
	exit 1
fi

# La demo viene rigenerata prima di partire: si carica sempre l'ultima versione.
python3 "$AUTO_DIR/scripts/build-demo.py"

cd "$AUTO_DIR/demo"
TOTALE=$(find . -type f ! -name 'auto.json' ! -name 'crediti.json' ! -name 'rifiutate.json' | wc -l | tr -d ' ')
echo "==> Carico $TOTALE file su ftp://$FTP_HOST/$CARTELLA_REMOTA/"

CARICATI=0
while IFS= read -r file; do
	relativo="${file#./}"
	curl --silent --show-error --ftp-create-dirs -T "$file" \
		"ftp://$FTP_HOST/$CARTELLA_REMOTA/$relativo" \
		--user "$FTP_USER:$FTP_PASS"
	CARICATI=$((CARICATI + 1))
	printf '\r    %d/%d' "$CARICATI" "$TOTALE"
done < <(find . -type f ! -name 'auto.json' ! -name 'crediti.json' ! -name 'rifiutate.json')

printf '\n==> Fatto. La demo è online qui:\n    %s/\n' "$INDIRIZZO"
echo
echo "Nota: le pagine hanno il meta noindex, quindi Google non le indicizza."
echo "Quando la demo non serve più, cancella la cartella $CARTELLA_REMOTA da cPanel."
