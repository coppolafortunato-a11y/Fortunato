@echo off
REM Avvio con doppio clic su Windows: scarica il progetto, installa e configura.
REM Unico prerequisito: Node.js (https://nodejs.org, versione LTS).
setlocal
title Monitor appuntamenti - installazione

echo.
echo  ============================================================
echo    MONITOR APPUNTAMENTI - Passaportny servis DP Dokument
echo  ============================================================
echo.

where node >nul 2>&1
if errorlevel 1 (
  echo  [X] Node.js non risulta installato.
  echo.
  echo      1. apri  https://nodejs.org
  echo      2. scarica il pulsante grande "LTS"
  echo      3. installa lasciando tutte le opzioni come sono
  echo      4. torna qui e fai di nuovo doppio clic su questo file
  echo.
  pause
  exit /b 1
)
for /f "delims=" %%v in ('node --version') do echo  [OK] Node.js %%v

set "BASE=%USERPROFILE%\MonitorAppuntamenti"
set "PROJ=%BASE%\Fortunato-claude-brave-wozniak-p0mqp3\pasport-monitor"

if exist "%PROJ%\package.json" (
  echo  [OK] Progetto gia presente, uso quello.
) else (
  echo  [..] Scarico il progetto...
  if not exist "%BASE%" mkdir "%BASE%"
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ErrorActionPreference='Stop'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/coppolafortunato-a11y/Fortunato/archive/refs/heads/claude/brave-wozniak-p0mqp3.zip' -OutFile '%BASE%\progetto.zip'; Expand-Archive -Path '%BASE%\progetto.zip' -DestinationPath '%BASE%' -Force; Remove-Item '%BASE%\progetto.zip'"
  if errorlevel 1 (
    echo  [X] Download non riuscito. Controlla la connessione a Internet.
    pause
    exit /b 1
  )
  echo  [OK] Progetto scaricato in %BASE%
)

cd /d "%PROJ%" || (echo  [X] Cartella del progetto non trovata. & pause & exit /b 1)

echo  [..] Installo i componenti (qualche minuto la prima volta)...
call npm install --no-audit --no-fund
if errorlevel 1 (echo  [X] Installazione non riuscita. & pause & exit /b 1)

echo.
echo  Ora parte la configurazione guidata: tieni pronto il TOKEN del bot Telegram.
echo.
call npm run setup

echo.
echo  ============================================================
echo    Cartella del progetto:
echo    %PROJ%
echo  ============================================================
pause
