# MS Metalli — avvisi immediati per i nuovi contatti

Quando nel foglio **"MS Metalli - Contatti da Meta"** arriva un nuovo contatto
dal modulo Meta (Facebook/Instagram), lo script `avvisi-contatti.gs` ti manda
subito un'email con:

- nome, città, tipo cliente (impresa o privato), metallo e kg;
- **valore stimato** calcolato col listino (es. 200 kg di rame × 9 €/kg = € 1.800);
- il testo dell'avviso **pronto per WhatsApp** e tre bottoni:
  *Scrivi su WhatsApp* (apre la chat col venditore con un messaggio già scritto),
  *Chiama* e *Inoltra l'avviso su WhatsApp*.

L'oggetto dell'email riassume già tutto, così basta la notifica sul telefono:

```
🔔 MS Metalli: Mario Rossi — Rame, 200 kg — € 1.800
```

Il contatto finto di prova di Meta (quello con `<test lead: dummy data …>` e
`test@meta.com`) viene ignorato.

## Installazione (una volta sola, 5 minuti)

1. Apri il foglio **MS Metalli - Contatti da Meta** con il tuo account Google.
2. Menu **Estensioni → Apps Script**. Si apre l'editor.
3. Cancella il contenuto di `Codice.gs` e incolla tutto il file
   [`avvisi-contatti.gs`](avvisi-contatti.gs). Premi **Salva** (icona dischetto).
4. Controlla la parte **IMPOSTAZIONI** in alto (vedi sotto): listino,
   destinatario dell'email, nome della scheda (di solito `Foglio1`).
5. In alto, nel menu a tendina delle funzioni, scegli **`installa`** e premi
   **Esegui**.
6. Google chiede le autorizzazioni: **Rivedi autorizzazioni** → scegli il tuo
   account → se compare "Google non ha verificato questa app" premi
   **Avanzate → Vai a … (non sicuro)** → **Consenti**. È normale: lo script è
   tuo e non è pubblicato.
7. Scegli **`provaAvviso`** e premi **Esegui**: ti arriva un'email
   `[PROVA]` con l'ultimo contatto vero del foglio. Se arriva, è tutto pronto.

`installa` crea due trigger (li vedi nell'icona **⏰ Trigger** a sinistra):

| Trigger | Quando scatta | Perché |
|---|---|---|
| `controllaNuoviContatti` — a tempo, **ogni minuto** | sempre | Meta scrive nel foglio da fuori: questo garantisce l'avviso entro ~1 minuto |
| `controllaNuoviContatti` — **alla modifica** del foglio | a ogni cambiamento | quando Google lo fa scattare, l'avviso è istantaneo |

I contatti già presenti al momento dell'installazione **non** generano avvisi:
partono solo quelli nuovi. Lo script ricorda l'ultima riga avvisata, quindi
non manda mai lo stesso avviso due volte.

## Impostazioni

Tutto quello che si cambia sta in cima al file, nella sezione **IMPOSTAZIONI**.

**Listino (€/kg)** — modifica i numeri, aggiungi o togli metalli:

```js
const LISTINO = {
  'rame': 9.0,
  'ottone': 4.0,
  'alluminio': 1.2,   // da verificare
  ...
};
```

Rame e ottone sono i prezzi che ci hai dato; gli altri sono **indicativi**,
aggiornali coi tuoi. Lo script cerca queste parole nella risposta "che tipo di
metalli?". Se il venditore scrive più metalli (es. "rame e ottone") l'avviso
mostra una forbice ("tra € 6.000 e € 13.500"). Se il metallo non è nel listino
o mancano i kg, scrive "stima non disponibile" ma l'avviso parte comunque.

**`SINONIMI`** — altri modi in cui la gente scrive un metallo (es. "allumino"
→ alluminio).

**`EMAIL_DESTINATARIO`** — vuoto = l'account che ha installato lo script.
Puoi mettere più indirizzi separati da virgola, ad esempio per avvisare anche
un collega.

**`SALUTO_WHATSAPP`** — il messaggio già scritto che si apre quando premi
*Scrivi su WhatsApp*. `{nome}`, `{metallo}` e `{kg}` vengono sostituiti.

Dopo ogni modifica premi **Salva**: non serve rifare `installa`.

## Avere l'avviso anche come notifica WhatsApp

L'email contiene già il testo pronto e il bottone per inoltrarlo. Per avere
la notifica in tempo reale sul telefono:

- attiva le notifiche di Gmail sul telefono (o crea un filtro Gmail su
  "MS Metalli" con etichetta e notifica prioritaria);
- se in futuro vuoi il messaggio **direttamente su WhatsApp** senza passare
  dall'email, serve un servizio esterno (WhatsApp Business API, Twilio o
  simili): la funzione `testoAvviso_` produce già il testo da mandare.

## Comandi utili

| Funzione | A cosa serve |
|---|---|
| `installa` | Attiva gli avvisi (o li reimposta). |
| `provaAvviso` | Manda un'email di prova. |
| `disinstalla` | Spegne gli avvisi. |
| `controllaNuoviContatti` | Il controllo vero e proprio (lo lanciano i trigger). |

## Problemi frequenti

- **Non arriva niente:** guarda **Esecuzioni** (icona ☰ a sinistra
  nell'editor) per vedere errori. Controlla che `NOME_SCHEDA` corrisponda al
  nome della scheda in basso nel foglio.
- **Arrivano avvisi di righe vecchie:** rilancia `installa`, che riparte
  dall'ultima riga attuale.
- **Meta cambia le domande del modulo:** lo script trova le colonne per nome
  (parole come "metalli", "kg", "nome", "telefono", "città"), quindi di solito
  continua a funzionare. Se cambi molto le domande, tieni quelle parole nel
  testo.
- **Limiti Google:** un account Gmail gratuito può mandare circa 100 email al
  giorno da script, più che sufficienti per gli avvisi.
