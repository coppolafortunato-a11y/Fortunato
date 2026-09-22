# Avvio del monitor appuntamenti su Windows.
# Scarica il progetto, installa i componenti e lancia la configurazione guidata.
# Unico prerequisito: Node.js (https://nodejs.org, pulsante LTS).

$ErrorActionPreference = 'Stop'

function Titolo($testo) {
  Write-Host ''
  Write-Host ('  ' + $testo) -ForegroundColor Cyan
  Write-Host ('  ' + ('-' * 58)) -ForegroundColor DarkGray
}

function Esci($codice) {
  Write-Host ''
  Write-Host '  Premi INVIO per chiudere...' -ForegroundColor DarkGray
  Read-Host | Out-Null
  exit $codice
}

Write-Host ''
Write-Host '  ============================================================' -ForegroundColor Cyan
Write-Host '    MONITOR APPUNTAMENTI - Passaportny servis DP Dokument' -ForegroundColor Cyan
Write-Host '  ============================================================' -ForegroundColor Cyan

# ---- 1. Node.js -----------------------------------------------------------
Titolo '1. Controllo Node.js'
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
  Write-Host '  [X] Node.js non e'' installato.' -ForegroundColor Red
  Write-Host ''
  Write-Host '      1. apri  https://nodejs.org'
  Write-Host '      2. clicca il pulsante grande "LTS"'
  Write-Host '      3. installa lasciando tutte le opzioni come sono'
  Write-Host '      4. CHIUDI questa finestra, riaprine una nuova'
  Write-Host '         e incolla di nuovo gli stessi due comandi'
  Esci 1
}
$versione = (& node --version)
Write-Host ("  [OK] Node.js " + $versione) -ForegroundColor Green

# ---- 2. Download ----------------------------------------------------------
Titolo '2. Scarico il progetto'
$base = Join-Path $env:USERPROFILE 'MonitorAppuntamenti'
$proj = Join-Path $base 'Fortunato-claude-brave-wozniak-p0mqp3\pasport-monitor'
$zipUrl = 'https://github.com/coppolafortunato-a11y/Fortunato/archive/refs/heads/claude/brave-wozniak-p0mqp3.zip'

if (Test-Path (Join-Path $proj 'package.json')) {
  Write-Host '  [OK] Progetto gia'' presente, uso quello.' -ForegroundColor Green
} else {
  if (-not (Test-Path $base)) { New-Item -ItemType Directory -Path $base | Out-Null }
  $zip = Join-Path $base 'progetto.zip'
  try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Write-Host '  [..] Download in corso (circa 15 MB)...'
    Invoke-WebRequest -Uri $zipUrl -OutFile $zip -UseBasicParsing
    Write-Host '  [..] Estrazione...'
    Expand-Archive -Path $zip -DestinationPath $base -Force
    Remove-Item $zip -Force
  } catch {
    Write-Host ('  [X] Download non riuscito: ' + $_.Exception.Message) -ForegroundColor Red
    Write-Host '      Controlla che il computer sia connesso a Internet.'
    Esci 1
  }
  if (-not (Test-Path (Join-Path $proj 'package.json'))) {
    Write-Host '  [X] Il progetto non si trova dove previsto.' -ForegroundColor Red
    Write-Host ('      Cartella attesa: ' + $proj)
    Esci 1
  }
  Write-Host ('  [OK] Scaricato in ' + $base) -ForegroundColor Green
}

Set-Location $proj

# ---- 3. Componenti --------------------------------------------------------
Titolo '3. Installo i componenti'
Write-Host '  (la prima volta richiede qualche minuto)'
Write-Host ''
& npm install --no-audit --no-fund
if ($LASTEXITCODE -ne 0) {
  Write-Host '  [X] Installazione non riuscita.' -ForegroundColor Red
  Esci 1
}
Write-Host '  [OK] Componenti installati.' -ForegroundColor Green

# ---- 4. Configurazione guidata -------------------------------------------
Titolo '4. Configurazione guidata'
Write-Host '  Tieni pronto il TOKEN del bot Telegram.'
Write-Host ''
& npm run setup

Write-Host ''
Write-Host '  ============================================================' -ForegroundColor Cyan
Write-Host ('   Cartella del progetto: ' + $proj)
Write-Host ('   Log del monitor      : ' + (Join-Path $proj 'logs\monitor.log'))
Write-Host '  ============================================================' -ForegroundColor Cyan
Esci 0
