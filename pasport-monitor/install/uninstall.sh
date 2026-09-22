#!/usr/bin/env bash
# Rimuove il servizio persistente (non tocca log e stato).
set -euo pipefail
case "$(uname -s)" in
  Linux)
    systemctl --user disable --now pasport-monitor.service 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/pasport-monitor.service"
    systemctl --user daemon-reload
    echo "Servizio systemd rimosso." ;;
  Darwin)
    PLIST="$HOME/Library/LaunchAgents/com.fortunato.pasport-monitor.plist"
    launchctl unload -w "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "LaunchAgent rimosso." ;;
esac
