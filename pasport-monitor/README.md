# Monitor appuntamenti — Паспортний сервіс ДП Документ

Controlla ogni 15 minuti, per 10 giorni, se compare un appuntamento per il servizio
**«Закордонний паспорт та (або) ID-картка»** in 5 centri, e avvisa su Telegram appena
trova qualcosa di **nuovo**.

Centri monitorati di serie: **Cracovia, Varsavia, Wrocław, Danzica**.
Milano/Rozzano è configurato ma disattivato — si riattiva con una riga in `.env`.

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

## Installazione — doppio clic

Sul computer che resterà acceso, scarica ed esegui il file adatto:

- **Windows** → [`AVVIA-MONITOR-WINDOWS.bat`](https://raw.githubusercontent.com/coppolafortunato-a11y/Fortunato/claude/brave-wozniak-p0mqp3/pasport-monitor/install/AVVIA-MONITOR-WINDOWS.bat)
- **Mac** → [`AVVIA-MONITOR-MAC.command`](https://raw.githubusercontent.com/coppolafortunato-a11y/Fortunato/claude/brave-wozniak-p0mqp3/pasport-monitor/install/AVVIA-MONITOR-MAC.command)

Scarica, doppio clic, e fa tutto da solo: scarica il progetto, installa i
componenti e lancia la configurazione guidata. L'unico prerequisito è
**Node.js** ([nodejs.org](https://nodejs.org), pulsante **LTS**) — se manca,
il file te lo dice e si ferma.

Su Mac, se al primo doppio clic compare «impossibile aprire perché proviene da
uno sviluppatore non identificato»: clic destro sul file → **Apri** → **Apri**.

### Oppure da terminale

```bash
npm install
npm run setup
```

`npm run setup` fa tutto da solo e ti guida passo passo:

1. controlla Node.js e scarica il browser Chromium;
2. **verifica subito che i siti rispondano da questa connessione** (se c'è una VPN attiva te lo dice);
3. ti fa creare il bot Telegram e trova da solo il tuo `chat_id`, poi ti manda un messaggio di prova;
4. esegue il primo controllo reale dei 5 centri e ti mostra la situazione attuale;
5. installa il monitor come servizio permanente (systemd / launchd / Task Scheduler);
6. stampa dove sono i log e quando il monitor si fermerà.

Serve Node.js 18 o superiore — se non ce l'hai, scaricalo da [nodejs.org](https://nodejs.org) (versione **LTS**).

Il primo controllo viene fatto **senza notifiche**: registra gli appuntamenti già
noti (Danzica 22/10, Milano 15/10) così non ti arriva un avviso per qualcosa che
sai già. Da lì in poi ricevi solo le novità.

---

## Comandi

| Comando | Cosa fa |
|---|---|
| `npm run setup` | Installazione guidata completa (da fare una volta) |
| `npm run check` | Un controllo sui 5 centri, con notifiche |
| `npm run baseline` | Un controllo **senza** notifiche (per fissare lo stato iniziale) |
| `npm run inspect <centro>` | Stampa la struttura del form + screenshot + HTML |
| `npm start` | Avvia il monitor in primo piano (15 min × 10 giorni) |
| `npm run install-service` | Installa il servizio persistente (systemd / launchd) |
| `npm test` | Test automatici della logica (usa un sito di prova locale) |
| `npm run chat-id` | Mostra il chat_id Telegram |
| `npm run test-notifiche` | Invia una prova su tutti i canali (Telegram, email, WhatsApp) |
| `npm run whatsapp-verifica` | Controlla che WhatsApp sia pronto, senza inviare nulla |
| `npm run chrome-collegabile` | Crea il collegamento "Chrome collegabile" (Windows) |
| `npm run whatsapp-login` | Collega la finestra separata col QR (modalità `profilo`) |

Centri validi per `inspect`: `krakow`, `warszawa`, `wroclaw`, `gdansk`, `milan`.

---

## Chi viene avvisato

Tre canali, configurabili indipendentemente:

| Canale | Chi | Come |
|---|---|---|
| **Telegram** | te | bot personale |
| **Email** | te + chi vuoi | SMTP (con Gmail serve una "password per le app") |
| **WhatsApp** | chi vuoi | WhatsApp Web già collegato su questo computer |

WhatsApp può funzionare in due modi, scelti con `WHATSAPP_MODE` in `.env`:

**`chrome` (predefinito)** — usa il Chrome che hai già aperto e già collegato a
WhatsApp Web. Nessun QR, nessun dispositivo in più. In cambio Chrome va avviato
dal collegamento **"Chrome collegabile"** (`npm run chrome-collegabile` lo crea
sul Desktop) e lasciato aperto, con una scheda su `web.whatsapp.com`.
Verifica che sia tutto a posto con `npm run whatsapp-verifica`.

**`profilo`** — finestra separata con memoria propria, da collegare col QR una
volta sola (`npm run whatsapp-login`). Non dipende dal tuo Chrome e funziona
anche a Chrome chiuso, ma occupa uno dei 4 dispositivi collegabili. La sessione
resta in `data/whatsapp-profile/`, cartella **esclusa da git** perché contiene
un accesso al tuo account.

La porta di debug ascolta solo su `127.0.0.1`: raggiungibile da quel computer,
non dalla rete.

L'email contiene anche la spiegazione di cosa fare, per chi non segue i dettagli
tecnici. Telegram e WhatsApp ricevono la versione corta, leggibile dalla notifica.

## Quante richieste fa al sito

Il sito **blocca chi lo interroga troppo** (verificato il 22/09/2026: dopo due
centri controllati di fila ha iniziato a rispondere 403). Il monitor quindi:

- controlla **un solo centro per ciclo**, a rotazione — con 5 centri e un ciclo
  ogni 15 minuti, ogni centro viene visto ogni ~75 minuti;
- aggiunge una **variazione casuale** all'attesa, per non avere un ritmo regolare;
- quando un sito risponde 403, mette quel centro **a riposo per 2, 4, 8, 16 cicli**,
  raddoppiando a ogni blocco.

Di serie controlla i **quattro centri in Polonia** (Cracovia, Varsavia, Wrocław,
Danzica): con un ciclo ogni 15 minuti, ognuno viene visto **ogni ora**.
Per aggiungere Milano: `ONLY_CENTERS=krakow,warszawa,wroclaw,gdansk,milan` in `.env`.

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

**Nessuna notifica** — `npm run test-notifiche`. Se fallisce, controlla di aver scritto
`/start` al bot e che `TELEGRAM_CHAT_ID` sia il numero restituito da `npm run chat-id`.

**Vedere cosa fa il browser** — metti `HEADLESS=false` in `.env` e lancia `npm run check`.
