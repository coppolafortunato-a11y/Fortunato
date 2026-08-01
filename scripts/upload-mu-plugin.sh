#!/usr/bin/env bash
#
# Obiettivo 2 del briefing — carica ideamkt-extras.php nei mu-plugins via FTP.
# I mu-plugin si attivano da soli, senza passare dal pannello plugin.
#
# Richiede FTP_HOST, FTP_USER, FTP_PASS in .env.
# Se non li hai, carica mu-plugins/ideamkt-extras.php a mano da cPanel -> Gestione file
# nella cartella  public_html/wp-content/mu-plugins/
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

SRC="mu-plugins/ideamkt-extras.php"

if [ ! -f .env ]; then
	echo "ERRORE: manca .env. Copia .env.example in .env e compilalo." >&2
	exit 1
fi
set -a; source .env; set +a

if [ -z "${FTP_HOST:-}" ] || [ -z "${FTP_USER:-}" ] || [ -z "${FTP_PASS:-}" ]; then
	echo "FTP non configurato in .env (FTP_HOST/FTP_USER/FTP_PASS)." >&2
	echo "Carica a mano $SRC in  public_html/wp-content/mu-plugins/  da cPanel." >&2
	exit 1
fi

if [ ! -f "$SRC" ]; then
	echo "ERRORE: $SRC non trovato." >&2
	exit 1
fi

echo "==> Upload di $SRC su ftp://$FTP_HOST/public_html/wp-content/mu-plugins/"
curl --ftp-create-dirs -T "$SRC" \
	"ftp://$FTP_HOST/public_html/wp-content/mu-plugins/ideamkt-extras.php" \
	--user "$FTP_USER:$FTP_PASS"

echo "==> Fatto. Apri il sito e verifica:"
echo "    - barra navy in alto con il numero 320 611 6711"
echo "    - tondo verde WhatsApp in basso a destra"
