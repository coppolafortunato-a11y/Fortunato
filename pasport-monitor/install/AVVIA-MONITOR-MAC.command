#!/bin/bash
# Avvio con doppio clic su macOS: scarica il progetto, installa e configura.
# Unico prerequisito: Node.js (https://nodejs.org, versione LTS).

echo
echo " ============================================================"
echo "   MONITOR APPUNTAMENTI — Паспортний сервіс ДП Документ"
echo " ============================================================"
echo

if ! command -v node >/dev/null 2>&1; then
  echo " [X] Node.js non risulta installato."
  echo
  echo "     1. apri  https://nodejs.org"
  echo "     2. scarica il pulsante grande \"LTS\""
  echo "     3. installa lasciando tutte le opzioni come sono"
  echo "     4. torna qui e fai di nuovo doppio clic su questo file"
  echo
  read -n 1 -s -r -p " Premi un tasto per chiudere..."
  exit 1
fi
echo " [OK] Node.js $(node --version)"

BASE="$HOME/MonitorAppuntamenti"
PROJ="$BASE/Fortunato-claude-brave-wozniak-p0mqp3/pasport-monitor"

if [ -f "$PROJ/package.json" ]; then
  echo " [OK] Progetto già presente, uso quello."
else
  echo " [..] Scarico il progetto…"
  mkdir -p "$BASE"
  if ! curl -fsSL -o "$BASE/progetto.zip" \
      "https://github.com/coppolafortunato-a11y/Fortunato/archive/refs/heads/claude/brave-wozniak-p0mqp3.zip"; then
    echo " [X] Download non riuscito. Controlla la connessione a Internet."
    read -n 1 -s -r -p " Premi un tasto per chiudere..."
    exit 1
  fi
  unzip -q -o "$BASE/progetto.zip" -d "$BASE"
  rm -f "$BASE/progetto.zip"
  echo " [OK] Progetto scaricato in $BASE"
fi

cd "$PROJ" || { echo " [X] Cartella del progetto non trovata."; read -n 1 -s -r -p " Premi un tasto..."; exit 1; }

echo " [..] Installo i componenti (qualche minuto la prima volta)…"
npm install --no-audit --no-fund || { echo " [X] Installazione non riuscita."; read -n 1 -s -r -p " Premi un tasto..."; exit 1; }

echo
echo " Ora parte la configurazione guidata: tieni pronto il TOKEN del bot Telegram."
echo
npm run setup

echo
echo " ============================================================"
echo "   Cartella del progetto:"
echo "   $PROJ"
echo " ============================================================"
read -n 1 -s -r -p " Premi un tasto per chiudere..."
