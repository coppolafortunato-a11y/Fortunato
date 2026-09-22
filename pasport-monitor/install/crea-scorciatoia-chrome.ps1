# Crea sul Desktop un collegamento "Chrome collegabile".
# E' il Chrome di sempre, con gli stessi accessi e le stesse schede, ma avviato
# in modo che il monitor possa usarlo per mandare i messaggi WhatsApp.

$ErrorActionPreference = 'Stop'

$porta = 9222
$chrome = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $chrome) {
  Write-Host '  [X] Non trovo Google Chrome su questo computer.' -ForegroundColor Red
  Write-Host '      Se usi un altro browser, in .env imposta WHATSAPP_MODE=profilo'
  exit 1
}

$desktop = [Environment]::GetFolderPath('Desktop')
$lnk = Join-Path $desktop 'Chrome collegabile.lnk'

$shell = New-Object -ComObject WScript.Shell
$s = $shell.CreateShortcut($lnk)
$s.TargetPath = $chrome
# --remote-debugging-address resta implicito su 127.0.0.1: raggiungibile solo
# da questo computer, non dalla rete.
$s.Arguments = "--remote-debugging-port=$porta"
$s.WorkingDirectory = Split-Path $chrome
$s.Description = 'Chrome avviato in modo che il monitor appuntamenti possa inviare i messaggi WhatsApp'
$s.Save()

Write-Host ''
Write-Host '  [OK] Creato sul Desktop: "Chrome collegabile"' -ForegroundColor Green
Write-Host ''
Write-Host '  DA ORA IN POI apri Chrome da quel collegamento.'
Write-Host '  E'' il tuo Chrome normale: stesse schede, stessi accessi, stesso WhatsApp Web.'
Write-Host ''
Write-Host '  Perche'' funzioni, WhatsApp Web deve restare aperto in una scheda'
Write-Host '  e Chrome non deve essere chiuso.'
Write-Host ''
