# Sito auto — vendita, officina, elettrauto, noleggio e cerimonie

Kit completo per un'attività che vende auto usate **e** fa assistenza: officina
meccanica, elettrauto, noleggio auto e furgoni, auto con autista per matrimoni.
Il cliente inserisce e aggiorna veicoli e flotta dalla **bacheca WordPress**; il
sito mostra catalogo con filtri, schede veicolo, pagine servizi e contatti
diretti (WhatsApp, telefono, modulo).

Due parti:

| Cartella | Cosa contiene |
|----------|---------------|
| `plugin/concessionaria-auto/` | Il plugin WordPress: è il prodotto vero. |
| `demo/` | Anteprima statica (HTML) da mostrare al cliente **senza installare niente**. |
| `scripts/build-demo.py` | Rigenera la demo dai dati di `demo/auto.json`. |
| `scripts/scarica-foto.py` | Scarica foto dimostrative con licenza libera (Openverse). |
| `scripts/scarta-foto.py` | Toglie le foto sbagliate e rinumera le altre. |

Demo e sito vero usano **gli stessi CSS e JS** (`plugin/concessionaria-auto/assets/`):
quello che il cliente approva nella demo è quello che vedrà online.

---

## 1. Mostrare la demo al cliente

Apri `demo/index.html` con un doppio clic (funziona anche offline, senza server).
Pagine disponibili: home, catalogo con filtri, 9 schede veicolo di esempio.

Per cambiare i dati della demo (nome concessionaria, auto, prezzi):

```bash
# modifica demo/auto.json, poi
python3 scripts/build-demo.py
```

Le foto dell'anteprima sono immagini con licenza libera scaricate da Openverse
(`python3 scripts/scarica-foto.py`): servono solo a far vedere l'effetto, e autori
e licenze sono elencati nella pagina *Crediti foto* della demo. **Vanno sostituite
con le foto dei veicoli realmente in salone prima di andare online.**

Per mettere le foto vere basta salvarle in `demo/img/` con il nome
`<slug>-1.jpg`, `<slug>-2.jpg`… : il generatore usa il `.jpg` se c'è, altrimenti
disegna il segnaposto. Se una foto scaricata non va bene:

```bash
python3 scripts/scarta-foto.py nome-file.jpg      # la toglie e la ricorda
python3 scripts/scarica-foto.py                   # ne cerca un'altra al suo posto
```

---

## 2. Installare il plugin su WordPress

1. Crea lo zip del plugin:

   ```bash
   bash scripts/crea-zip.sh
   # produce concessionaria-auto.zip
   ```

2. WordPress → **Plugin → Aggiungi nuovo → Carica plugin** → scegli lo zip → **Installa** → **Attiva**.
3. WordPress → **Impostazioni → Permalink** → **Salva** (serve a far funzionare gli indirizzi delle schede auto).
4. Menu **Auto → Impostazioni**: inserisci nome concessionaria, telefono, numero
   WhatsApp (con prefisso, es. `393201234567`) ed e-mail a cui far arrivare le richieste.

### Pagine da creare

| Pagina | Cosa inserire |
|--------|---------------|
| Auto usate | `[auto_catalogo]` — catalogo completo con i filtri |
| Home | `[auto_ricerca]` (barra di ricerca) e `[auto_evidenza limite="3"]` (le occasioni) |
| Noleggio | `[noleggio_catalogo]` — tutta la flotta |
| Matrimoni e cerimonie | `[noleggio_catalogo categoria="cerimonie"]` |
| Servizi (officina, elettrauto) | testo e foto normali: sono pagine WordPress, senza shortcode |

Attributi utili:

- `[auto_catalogo vendute="no"]` nasconde le auto già vendute;
- `[auto_catalogo limite="100"]` alza il numero massimo di auto caricate;
- `[auto_evidenza limite="6"]`.

Le schede dei singoli veicoli si creano da sole: l'indirizzo è `tuosito.it/auto/nome-auto`,
l'elenco generale `tuosito.it/auto-usate`, quello per marca `tuosito.it/marca/fiat`.

---

## 3. Cosa fa il plugin

- Due sezioni in bacheca: **Auto** (vendita) e **Noleggio** (flotta e cerimonie).
- Tipo di contenuto **Auto** con campi: prezzo, chilometri, immatricolazione,
  alimentazione, cambio, carrozzeria, potenza, cilindrata, porte, posti, colore,
  classe ambientale, garanzia, neopatentati, allestimento, dotazioni, stato.
- **Marche** come categorie: il cliente sceglie con una spunta, niente refusi.
- **Galleria foto** per veicolo, presa dalla libreria media di WordPress.
- **Stato del veicolo**: disponibile / prenotata / venduta / in arrivo.
  Le vendute restano online in fondo all'elenco, in bianco e nero, con l'etichetta.
- **Catalogo con filtri** immediati (senza ricaricare la pagina) e ordinamento.
  I filtri finiscono nell'indirizzo della pagina: una ricerca si può inviare su WhatsApp.
- **Scheda veicolo**: galleria con lightbox, tabella dati, dotazioni, prezzo,
  pulsanti WhatsApp e telefono, modulo "richiedi informazioni" (e-mail alla concessionaria).
- **Dati strutturati schema.org/Car**: Google legge prezzo, km e disponibilità.
- **Noleggio**: veicoli con prezzo al giorno o a cerimonia, posti, cambio,
  bagagli, km inclusi, età minima, «con autista» e cosa è incluso. Tre categorie:
  noleggio giornaliero, furgoni e 9 posti, cerimonie e matrimoni.
- Le richieste dal modulo hanno nonce e campo trappola anti-spam.
- La demo in `demo/` è autonoma (CSS e JS copiati dentro): si può zippare e
  inviare al cliente, o caricare su un indirizzo di prova.

---

## 4. Cosa serve prima di andare online

- [ ] Nome, logo, colori e recapiti veri della concessionaria
- [ ] Dominio e hosting (basta un hosting WordPress economico)
- [ ] Foto reali dei veicoli (consigliato: 6–10 per auto, stesso sfondo)
- [ ] Pagina privacy e cookie banner (i moduli raccolgono dati personali)
- [ ] Profilo Google Business collegato, per farsi trovare su Maps

---

## 5. Da sapere

- Il catalogo filtra lato browser: perfetto fino a qualche centinaio di veicoli.
  Oltre, conviene passare a filtri lato server (si aggiunge senza rifare il sito).
- Il modulo usa `wp_mail()`: su molti hosting le e-mail finiscono in spam.
  Consigliato collegare un servizio SMTP (es. plugin WP Mail SMTP) in fase di pubblicazione.
- Il plugin non tocca il tema: funziona sia con i temi classici sia con quelli a blocchi.
