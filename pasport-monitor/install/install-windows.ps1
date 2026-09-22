# Installa il monitor come attivita persistente di Windows (Task Scheduler).
# Esegui da PowerShell nella cartella del progetto:  .\install\install-windows.ps1
$ErrorActionPreference = 'Stop'

$dir  = Split-Path -Parent $PSScriptRoot
$node = (Get-Command node -ErrorAction SilentlyContinue).Source
if (-not $node) { Write-Error "Node.js non trovato nel PATH."; exit 1 }
if (-not (Test-Path "$dir\.env")) { Write-Error "Manca $dir\.env - copialo da .env.example e inserisci il token Telegram."; exit 1 }

$taskName = 'PasportMonitor'
$action   = New-ScheduledTaskAction -Execute $node -Argument "$dir\src\monitor.js" -WorkingDirectory $dir
# All'avvio del PC e subito; il monitor gestisce da se il ciclo ogni 15 minuti.
$trigger  = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
              -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5) `
              -ExecutionTimeLimit (New-TimeSpan -Days 11)

Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings `
  -Description 'Monitor disponibilita appuntamenti Pasportny servis DP Dokument' | Out-Null
Start-ScheduledTask -TaskName $taskName

Write-Host ""
Write-Host "Attivita '$taskName' registrata e avviata."
Write-Host "  Stato : Get-ScheduledTask -TaskName $taskName"
Write-Host "  Log   : Get-Content -Wait $dir\logs\monitor.log"
Write-Host "  Stop  : Stop-ScheduledTask -TaskName $taskName"
