# Remarketing sui contatti già in archivio — piano operativo

Idea Marketing di Coppola Fortunato — Reggio Calabria
Preparato per: riattivazione clienti e lead già acquisiti.

> **Numeri di partenza** (dagli archivi già contati per il sito): oltre **1.000 clienti**
> e **1.300 lavori** fatti, ~1.150 clienti distinti. Questo è l'asset più importante:
> costa molto meno riattivare chi ti conosce già che comprare traffico nuovo.

---

## 1. In breve — cosa consiglio di fare

Nell'ordine, senza saltare passaggi:

1. **Prima il foglio, poi le campagne.** Oggi i contatti sono sparsi tra rubrica,
   WhatsApp, Drive e fatture. Finché non stanno in un unico file con nome, telefono,
   email, ultimo lavoro e data, qualsiasi campagna è cieca. È il lavoro di mezza
   giornata che vale di più di tutto il resto.
2. **Parti da WhatsApp e telefono, non dalla pubblicità.** Hai già il canale che
   converte di più e ti costa zero: 1-a-1, con il tuo numero che loro conoscono.
   Meta e Google vengono dopo, per coprire chi non risponde.
3. **Un motivo per farsi risentire, non un "ciao come va".** Il messaggio che
   funziona è legato al lavoro che gli hai già fatto ("l'insegna che ti abbiamo
   montato nel 2023...") e propone una cosa sola, concreta, con una scadenza.
4. **Una campagna per segmento, non una uguale per tutti.** Chi ha comprato
   un'insegna non ha bisogno di un'altra insegna: ha bisogno di manutenzione,
   di un LEDwall o del sito. Vedi §3.
5. **Retargeting a pagamento solo dopo aver messo il pixel.** Senza tracciamento
   sul sito, i soldi delle campagne sono buttati e non sai cosa ha funzionato. Vedi §6.

Budget minimo per partire: **0 € la prima settimana** (solo lavoro tuo su lista e
WhatsApp), poi **150-300 €/mese** per il retargeting a pagamento.

---

## 2. Passo 0 — costruire la lista (prima di tutto)

Usa il modello `marketing/lista-contatti-template.csv`. Fonti da svuotare dentro:

| Fonte | Cosa tirare fuori |
|-------|-------------------|
| Archivio lavori su Drive | nome cliente, tipo di lavoro, anno |
| Fatture / registro IVA | ragione sociale, P.IVA, email, importo |
| Rubrica telefono e WhatsApp | numero di cellulare vero |
| Preventivi non chiusi | chi ha chiesto e non ha comprato ← **oro puro** |
| Form contatti del sito | richieste arrivate e mai richiamate |

Regole per non sprecare il lavoro:
- una riga per **contatto**, non per lavoro (se ha fatto 3 lavori, stanno nella colonna note);
- il telefono in formato `+39...` (serve così a Meta per l'abbinamento);
- se non sai la data dell'ultimo lavoro, metti almeno l'anno: serve per i segmenti;
- segna subito chi **non** va contattato (litigi, insoluti, chiusi).

---

## 3. Segmenti e offerta — chi contattare e con cosa

Priorità dall'alto verso il basso. Non partire dal fondo.

| # | Segmento | Come lo riconosci | Cosa gli proponi | Perché funziona |
|---|----------|-------------------|------------------|-----------------|
| 1 | **Preventivi non chiusi** (ultimi 24 mesi) | ha chiesto, non ha comprato | riapri il preventivo con prezzo aggiornato e una scadenza | è già stato a un passo dal sì |
| 2 | **Clienti insegne 2-5 anni fa** | insegna/vetrina installata | **controllo gratuito + passaggio a LED** (consumi più bassi, luce nuova) | l'insegna vecchia si vede, il LED si ripaga |
| 3 | **Ristoranti, bar, negozi** | categoria | **LEDwall a noleggio** (formula Grenke già sul sito) + menu e vetrofanie | canone mensile, niente investimento iniziale |
| 4 | **Clienti stampa ricorrente** | volantini, etichette, packaging | ristampa stagionale programmata + sconto quantità | comprano già a cicli, basta ricordarglielo |
| 5 | **Clienti senza sito o con sito vecchio** | li conosci tu | sito + Google Business Profile | hai già il rapporto di fiducia |
| 6 | **Tutti gli altri / dormienti 5+ anni** | resto della lista | messaggio leggero "siamo ancora qui, ecco cosa facciamo oggi" | riscalda senza bruciare |

**Regola d'oro:** una campagna = un segmento = **una** offerta. Il messaggio che
propone tre cose non ne fa comprare nessuna.

---

## 4. Calendario 6 settimane

| Settimana | Cosa fai | Canale | Sforzo |
|-----------|----------|--------|--------|
| 1 | Costruisci la lista + scrivi i messaggi | — | mezza giornata |
| 1 | Segmento 1 (preventivi non chiusi): messaggio 1-a-1 | WhatsApp, poi telefono a chi non risponde | 2 ore |
| 2 | Segmento 2 (insegne vecchie): offerta controllo + LED | WhatsApp + email | 2 ore |
| 2 | Metti pixel Meta e GA4 sul sito | tecnico (vedi §6) | 1 ora |
| 3 | Segmento 3 (ristoranti/bar): LEDwall a noleggio | WhatsApp + chiamata ai migliori 20 | 3 ore |
| 3 | Carichi la lista su Meta → pubblico personalizzato | Meta Business | 30 min |
| 4 | Segmento 4 (stampa): ristampa stagionale | email + WhatsApp | 2 ore |
| 4 | Accendi retargeting visitatori sito (150 €/mese) | Meta ads | 1 ora |
| 5 | Segmento 5 (siti web) + follow-up di chi non ha risposto | telefono | 3 ore |
| 6 | Tiri le somme, tieni quello che ha funzionato | — | 1 ora |

Non mandare tutto insieme: se rispondono in 200 lo stesso giorno, non riesci a
seguirli e bruci i contatti. **Massimo 30-40 messaggi al giorno**, così rispondi
a tutti entro poche ore.

---

## 5. Come scrivere i messaggi

I testi pronti da copiare stanno in `marketing/messaggi-pronti.md`. Le regole:

- **Nome + riferimento al lavoro fatto** nella prima riga. Senza quello sembra spam.
- **Una sola domanda alla fine**, facile da rispondere ("te lo mando?", "passo io?").
- **Niente listino nel primo messaggio.** Il prezzo dopo che hai capito cosa gli serve.
- **Scadenza vera**, non finta ("fino a fine mese ho lo slot di montaggio libero").
- Scrivi **come parli**. Niente "gentile cliente", niente maiuscole urlate, niente emoji a raffica.
- **Manda dalle 9:30 alle 12:30 o dalle 15:00 alle 18:00**, mai la domenica.

### Vincoli pratici di WhatsApp — leggere prima di partire
- Le **liste broadcast** arrivano **solo a chi ha il tuo numero salvato in rubrica**.
  Su una lista vecchia, metà dei messaggi non arriva mai: per i segmenti 1-3
  (i più importanti) manda **uno per uno**, a mano. È più lento ma arriva davvero.
- Copia-incollare lo stesso testo a centinaia di numeri in poche ore è il modo
  più veloce per **farsi bloccare il numero**. Personalizza almeno il nome e
  spezza l'invio su più giorni.
- Se vuoi fare invii in massa in regola, serve **WhatsApp Business Platform (API)**
  con modelli approvati e opt-in raccolto: ha un costo per conversazione e va
  attivato prima. Per ora non serve: 1.150 contatti si lavorano a mano in 6 settimane.

---

## 6. Retargeting a pagamento — cosa serve e quanto costa

Da fare **dopo** le prime due settimane, non prima.

### 6.1 Tracciamento sul sito (prerequisito)
Senza questi tre pezzi il retargeting non è possibile:

1. **Meta Pixel** sul sito (tutte le pagine).
2. **Google Analytics 4** (o Google Tag) — per capire da dove arrivano le richieste.
3. **Eventi sui click che contano**: click sul bottone WhatsApp, click su
   `tel:`, invio del form contatti. Sono questi i "lead", non le visite.

Il posto giusto dove metterli è `mu-plugins/ideamkt-extras.php` (già carica
header e bottone WhatsApp su tutto il sito). Serve anche un **banner cookie**
con consenso preventivo: pixel e GA4 vanno caricati **solo dopo l'accettazione**.

> Quando hai gli ID (Pixel ID e ID misurazione GA4) posso scrivere io il codice
> nel mu-plugin, con il consenso gestito correttamente.

### 6.2 Pubblici da creare su Meta
| Pubblico | Come si crea | A cosa serve |
|----------|--------------|--------------|
| Lista clienti | caricamento del CSV (telefono + email) | riattivazione, arriva anche a chi non risponde su WhatsApp |
| Visitatori sito 180 gg | dal Pixel | chi ti ha cercato e non ha scritto |
| Chi ha visto `/ledwall/` o `/preventivi-ledwall/` | dal Pixel, per URL | il pubblico più caldo che hai |
| Simile (lookalike) 1% | dalla lista clienti | per acquisire nuovi, **solo dopo** che la riattivazione funziona |

Nota: perché un pubblico da lista sia utilizzabile servono **almeno ~100 contatti
abbinati**; con 1.000+ contatti reali non è un problema. Per Google Ads
(Customer Match) la soglia è più alta e serve un account in regola: parti da Meta.

### 6.3 Budget consigliato
| Voce | Budget | Cosa aspettarsi |
|------|--------|-----------------|
| Retargeting visitatori sito | 5 €/giorno (~150 €/mese) | pochi click ma caldi |
| Campagna su lista clienti | 3-5 €/giorno per 2 settimane | copertura di chi non ha risposto |
| Google Ads brand + "insegne Reggio Calabria" | 200-300 €/mese | **solo dopo**, è acquisizione non remarketing |

Parti con 150 €/mese. Se in 30 giorni non escono richieste, il problema è
l'offerta o la pagina di atterraggio, non il budget: aumentarlo peggiora e basta.

### 6.4 Dove li mandi (pagina di atterraggio)
Le pagine del sito ci sono già e sono quelle giuste:
- insegne → `/insegne-reggio-calabria/`
- LEDwall → `/ledwall/` e il configuratore `/preventivi-ledwall/`
- portfolio (prova sociale, 19 lavori veri) → `/lavori/`
- richiesta → `/contatti/`

Metti sempre i **parametri UTM** nei link che mandi, così sai cosa ha portato la richiesta:

```
https://ideamkt.it/preventivi-ledwall/?utm_source=whatsapp&utm_medium=remarketing&utm_campaign=riattivazione-ledwall
https://ideamkt.it/insegne-reggio-calabria/?utm_source=meta&utm_medium=retargeting&utm_campaign=insegne-led
```

> Manca una pagina dedicata all'offerta "passaggio a insegna LED" (segmento 2).
> È la pagina che farei per prima, se vuoi la preparo nello stile del sito.

---

## 7. Regole da rispettare (GDPR) — in due righe

- **Ai tuoi clienti** puoi scrivere per proporre **servizi simili** a quelli che ti
  hanno già comprato, senza consenso nuovo (è la cosiddetta *soft spam*), **a patto
  che in ogni messaggio ci sia come dire "basta"**. Metti sempre una riga tipo
  *"se non vuoi più ricevere messaggi rispondi STOP"* — e rispettala davvero.
- **A chi non è mai stato cliente** (liste comprate, contatti raccolti da terzi)
  **non scrivere**: serve consenso esplicito. Non ne vale la pena.
- Tieni traccia di chi chiede di essere tolto: colonna `stop` nel CSV, e non lo
  ricontatti più su nessun canale.
- Il CSV con i contatti **non va messo su git**: è in `.gitignore` come i segreti.
  Tienilo su Drive, condiviso solo con chi lavora alla campagna.

---

## 8. Cosa misurare (e cosa ignorare)

Segna ogni settimana su un foglio, bastano 5 numeri:

| Numero | Come si conta | Riferimento realistico |
|--------|---------------|------------------------|
| Messaggi mandati | li conti tu | 30-40 al giorno |
| Risposte ricevute | risposte / mandati | su una lista tua, buono da 15% in su |
| Preventivi fatti | richieste vere | ~1 su 3 delle risposte |
| Lavori chiusi | ordini firmati | ~1 su 4 dei preventivi |
| Incasso generato | € dai lavori chiusi | è l'unico numero che conta |

*(Le percentuali sono ordini di grandezza prudenti su liste di clienti già
acquisiti, non dati misurati sulla tua base: servono come sveglia, non come promessa.
Dalla seconda settimana usa i tuoi numeri veri.)*

**Ignora** like, follower e visualizzazioni: non pagano le fatture.

---

## 9. Da fare questa settimana

- [ ] Riempire `marketing/lista-contatti-template.csv` (anche solo i primi 100 contatti migliori)
- [ ] Marcare il segmento di ogni riga (colonna `segmento`)
- [ ] Copiare i messaggi da `marketing/messaggi-pronti.md` e adattare il tono
- [ ] Mandare i primi 30 messaggi al segmento 1 (preventivi non chiusi)
- [ ] Richiamare al telefono chi non risponde entro 48 ore
- [ ] Recuperare Pixel ID Meta e ID GA4 (o dirmi di crearli) per il tracciamento
