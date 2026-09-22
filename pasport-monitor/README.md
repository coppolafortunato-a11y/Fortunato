# Monitor appuntamenti — Паспортний сервіс ДП Документ

Controlla ogni 15 minuti, per 10 giorni, se compare un appuntamento per il servizio
**«Закордонний паспорт та (або) ID-картка»** in 5 centri, e avvisa su Telegram appena
trova qualcosa di **nuovo**.

Centri monitorati: Cracovia, Varsavia, Wrocław, Danzica, Milano/Rozzano.

Il programma **legge soltanto**: non prenota, non inserisce numeri di telefono, non
clicca «Продовжити», non avvia Diia.Signature né BankID. Se un sito mostra un CAPTCHA
o blocca l'automazione, il controllo viene registrato come errore — nessun tentativo
di aggiramento.

---

## ⚠️ Dove va eseguito

I siti `*.pasport.org.ua` sono dietro Cloudflare e **rifiutano le connessioni dagli
indirizzi IP dei datacenter** (403 «Blocked for security reasons» prima di qualsiasi
contenuto). Vale per i server cloud, e quindi anche per GitHub Actions o una VPS.

**Va eseguito dal tuo computer di casa**, sulla tua connessione normale. È anche la
scelta giusta nel merito: dallo stesso IP da cui poi prenoterai.

---

## Installazione (una volta sola)

```bash
cd pasport-monitor
npm install
npx playwright install chromium     # scarica il browser (~150 MB)
```

Serve Node.js 18 o superiore (`node --version`).

### Telegram

1. Su Telegram apri **@BotFather** → `/newbot` → scegli un nome → ricevi il **token**.
2. Apri il tuo nuovo bot e scrivigli `/start`.
3. Configura:

```bash
cp .env.example .env
# incolla il token in TELEGRAM_BOT_TOKEN, poi:
npm run chat-id          # stampa il tuo chat_id -> incollalo in TELEGRAM_CHAT_ID
npm run test-telegram    # deve arrivarti un messaggio di prova
```

---

## Primo avvio

```bash
npm run inspect krakow   # 1. verifica che il form venga letto correttamente
npm run baseline         # 2. primo controllo SENZA notifiche: registra la situazione attuale
npm run check            # 3. controllo normale: da qui in poi notifica le novità
npm run install-service  # 4. avvia il monitor in modo persistente
```

Su Windows, al posto dell'ultimo comando:

```powershell
.\install\install-windows.ps1
```

`npm run baseline` è importante: memorizza gli orari già presenti su Danzica e Milano,
così il primo controllo vero non ti manda una notifica per appuntamenti che conosci già.

---

## Comandi

| Comando | Cosa fa |
|---|---|
| `npm run check` | Un controllo sui 5 centri, con notifiche |
| `npm run baseline` | Un controllo **senza** notifiche (per fissare lo stato iniziale) |
| `npm run inspect <centro>` | Stampa la struttura del form + screenshot + HTML |
| `npm start` | Avvia il monitor in primo piano (15 min × 10 giorni) |
| `npm run install-service` | Installa il servizio persistente (systemd / launchd) |
| `npm test` | Test automatici della logica (usa un sito di prova locale) |
| `npm run chat-id` | Mostra il chat_id Telegram |
| `npm run test-telegram` | Invia una notifica di prova |

Centri validi per `inspect`: `krakow`, `warszawa`, `wroclaw`, `gdansk`, `milan`.

---

## Quando arriva una notifica

Solo quando c'è una **novità** rispetto al controllo precedente:

- compare una data mai vista;
- compare un orario nuovo su una data già nota;
- un centro prima pieno torna ad avere posti.

Se la situazione non cambia, non ricevi nulla. Le date prima del **15/10/2026** sono
marcate `⭐ PRIORITARIO`.

Notifica tecnica separata (`⚠️`) dopo **3 controlli falliti di fila** sullo stesso centro.

---

## File

```
data/state.json        ultimo stato conosciuto (memoria anti-doppione)
logs/monitor.log       log leggibile:  2026-09-22 14:16 | Gdansk | 22/10/2026
logs/checks.jsonl      un record JSON per controllo (per analisi)
screenshots/           screenshot automatici: disponibilità trovata ed errori
.env                   token e impostazioni — non finisce mai su git
```

---

## Gestione

**Linux**
```bash
systemctl --user status pasport-monitor
systemctl --user stop pasport-monitor
tail -f logs/monitor.log
```

**macOS**
```bash
launchctl list | grep pasport-monitor
launchctl unload -w ~/Library/LaunchAgents/com.fortunato.pasport-monitor.plist
tail -f logs/monitor.log
```

**Windows**
```powershell
Get-ScheduledTask -TaskName PasportMonitor
Stop-ScheduledTask -TaskName PasportMonitor
Get-Content -Wait logs\monitor.log
```

Il monitor si ferma **da solo dopo 10 giorni** e manda un messaggio finale.
Per cambiare durata o intervallo, modifica `DURATION_DAYS` e `INTERVAL_MINUTES` in `.env`.

---

## Se qualcosa non funziona

**«Servizio non trovato nel form»** — il sito ha cambiato struttura. Lancia
`npm run inspect krakow`: stampa le opzioni reali del menu. Se il testo del servizio è
cambiato, aggiorna `SERVICE_LABEL` in `src/config.js`.

**«Bloccato da protezione anti-bot»** — stai uscendo da un IP che Cloudflare non
gradisce (VPN, datacenter). Disattiva la VPN e usa la connessione di casa.

**Nessuna notifica** — `npm run test-telegram`. Se fallisce, controlla di aver scritto
`/start` al bot e che `TELEGRAM_CHAT_ID` sia il numero restituito da `npm run chat-id`.

**Vedere cosa fa il browser** — metti `HEADLESS=false` in `.env` e lancia `npm run check`.
