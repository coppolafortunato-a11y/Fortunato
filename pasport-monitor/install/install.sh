#!/usr/bin/env bash
# Installa il monitor come servizio persistente: systemd (Linux) o launchd (macOS).
# Il monitor continua a girare anche chiudendo il terminale.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NODE="$(command -v node)"
[ -n "$NODE" ] || { echo "Node.js non trovato nel PATH."; exit 1; }
[ -f "$DIR/.env" ] || { echo "Manca $DIR/.env — copialo da .env.example e inserisci il token Telegram."; exit 1; }

case "$(uname -s)" in
  Linux)
    UNIT="$HOME/.config/systemd/user/pasport-monitor.service"
    mkdir -p "$(dirname "$UNIT")"
    cat > "$UNIT" <<EOF
[Unit]
Description=Monitor appuntamenti Pasportny servis
After=network-online.target

[Service]
Type=simple
WorkingDirectory=$DIR
ExecStart=$NODE $DIR/src/monitor.js
Restart=on-failure
RestartSec=60
StandardOutput=append:$DIR/logs/service.log
StandardError=append:$DIR/logs/service.log

[Install]
WantedBy=default.target
EOF
    systemctl --user daemon-reload
    systemctl --user enable --now pasport-monitor.service
    # Il servizio sopravvive al logout solo con il lingering attivo.
    loginctl enable-linger "$USER" 2>/dev/null || echo "Nota: 'loginctl enable-linger $USER' richiede sudo; senza, il servizio si ferma al logout."
    echo
    echo "Servizio systemd installato e avviato."
    echo "  Stato : systemctl --user status pasport-monitor"
    echo "  Log   : tail -f $DIR/logs/monitor.log"
    echo "  Stop  : systemctl --user stop pasport-monitor"
    ;;
  Darwin)
    PLIST="$HOME/Library/LaunchAgents/com.fortunato.pasport-monitor.plist"
    mkdir -p "$(dirname "$PLIST")"
    cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.fortunato.pasport-monitor</string>
  <key>ProgramArguments</key>
  <array><string>$NODE</string><string>$DIR/src/monitor.js</string></array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key>
  <dict><key>SuccessfulExit</key><false/></dict>
  <key>StandardOutPath</key><string>$DIR/logs/service.log</string>
  <key>StandardErrorPath</key><string>$DIR/logs/service.log</string>
</dict>
</plist>
EOF
    launchctl unload "$PLIST" 2>/dev/null || true
    launchctl load -w "$PLIST"
    echo
    echo "LaunchAgent installato e avviato."
    echo "  Stato : launchctl list | grep pasport-monitor"
    echo "  Log   : tail -f $DIR/logs/monitor.log"
    echo "  Stop  : launchctl unload -w $PLIST"
    ;;
  *)
    echo "Sistema non gestito da questo script. Su Windows usa: install\\install-windows.ps1"
    exit 1
    ;;
esac
