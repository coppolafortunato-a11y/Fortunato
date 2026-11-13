# Log pubblicazione ideamkt.it — 2026-08-03

Tutto pubblicato in diretta via API REST di WordPress (utente `fortunato`,
Password applicazione dedicata). Sito verificato online dopo ogni passo.

## Fatto e verificato live

| # | Obiettivo | Come | Esito |
|---|-----------|------|-------|
| 1 | Homepage nuova (pagina ID 7) | POST `/wp/v2/pages/7` con blocco `wp:html` + fix larghezza piena | ✓ online |
| 2 | Barra contatti + WhatsApp su tutto il sito | blocco `wp:html` in cima al template part `header` (versione statica di `mu-plugins/ideamkt-extras.php`) | ✓ su home e pagine |
| 3.1 | Via il titolo "Home" sopra l'hero | pagina 7 → template `page-no-title` | ✓ tolto |
| 3.2 | Menu senza "Sample Page" e "Home" | menu esplicito su `navigation` ID 4 (Servizi, LEDWALL, Chi Siamo, Contatti); Sample Page (ID 2) → cestino | ✓ pulito |
| 3.3 | Footer con dati reali, sfondo #0f1d3f | sostituito template part `footer` | ✓ aggiornato |
| 3.4 | Permalink | verificati vs slug reali; corretto `/ledwall-digital-signage/` → `/ledwall/` (era 404) | ✓ corretti |

## Aggiornamento — restyle di tutte le pagine interne

Tutte le pagine ridisegnate con lo stile della home (navy/oro, Instrument
Serif + Manrope, niente emoji), contenuti reali mantenuti:

| Pagina | ID | Preservato |
|--------|----|-----------|
| Servizi | 10 | 7 aree di servizio con elenchi |
| LEDWALL & Digital Signage | 12 | prodotti, Grenke, CTA calcolatore |
| Chi Siamo | 14 | missione, valori, numeri |
| Contatti | 16 | **form email funzionante**, orari, dati fiscali |
| Preventivi LEDWALL | 27 | **calcolatore JS intatto** (prezzi, coeff. Grenke) |

Sorgenti generati in `wp-pages/*.html`, builder in `scripts/build-pages.py`.
Backup pre-restyle in `backup-*.json` / scratchpad di sessione.

## Aggiornamento — logo, favicon, motto, correzioni

- **Logo** (da ideamarketing.me) caricato in media (#56) e messo nell'header
  al posto del titolo testuale, su tutte le pagine. Copia in `assets/`.
- **Favicon** ricavata dal monogramma del logo (512x512), impostata come
  site_icon (#58). Copia in `assets/`.
- **Motto sito** corretto: era ancora "My WordPress Blog" → ora
  "Agenzia di comunicazione a Reggio Calabria — stampa, insegne, ledwall, siti web".
- **Corsivi** (Instrument Serif italico) rimossi da tutto il sito.
- **Chi Siamo**: aggiunta sezione "Il fondatore" (bio + spazio foto).

Nota: le altre immagini su ideamarketing.me (1/2/3/4-1/5) sono foto STOCK
generiche (codice, laptop), non lavori reali: NON usate come portfolio per
non ingannare. Servono foto vere dei lavori dal cliente.

## Contenuti reali usati (fonte: ideamarketing.me)
- Clienti in "Ci hanno scelto" e "Risultati recenti": Torrefazione Due Zero,
  Mamas, Pilone by Rare, Barber Srl (con i loro risultati reali).
- Nessuna recensione inventata: la sezione è diventata "Perché sceglierci"
  con punti di forza veri.

## Rollback (se serve tornare indietro)
I backup pre-modifica sono stati salvati in questa sessione (file `backup-*.json`,
non versionati per scelta del briefing):
- `backup-home-*.json` → contenuto precedente pagina 7
- `backup-menu-*.json` → menu precedente (era `<!-- wp:page-list /-->`)
- `backup-part-header-*.json`, `backup-part-footer-*.json` → header/footer originali

Per ripristinare un elemento: POST dello stesso endpoint con il `content`
del backup corrispondente.

## Note / migliorie future
- La barra contatti e il WhatsApp ora vivono nel template `header` del tema.
  Se in futuro attivi l'FTP, puoi spostarli nel mu-plugin
  `mu-plugins/ideamkt-extras.php` (più pulito e indipendente dal tema) e
  togliere il blocco `wp:html` dall'header.
- Da aggiungere quando disponibili: loghi immagine dei clienti, foto reali
  dei lavori, recensioni Google vere, orari e link social.

## Aggiornamento — pagina "I nostri lavori" (portfolio) — 2026-08-10

Portfolio reale costruito **solo con lavori estratti dagli archivi Google Drive**
del cliente (nessuno stock, nessun contenuto inventato). Pubblicato sulla pagina
`/lavori/` (ID 92), template `page-no-title`. Home invariata.

**Struttura:** tab per tipologia cliccabili (CSS-only, radio hack), LEDwall in cima:
LEDwall (4) · Insegne & Vetrine (6) · Menu (3) · Etichette & Packaging (4) · Stampa & Allestimenti (2) = **19 lavori**.

**Immagini:** ottimizzate a max 1400px / qualità 82 (`scripts/optimize-lavori.py`),
caricate nella Media Library WP con title/alt SEO (`scripts/upload-media.sh`, id 134–152),
mappa in `wp-pages/lavori-media-map.json`. Sorgenti in `assets/lavori/`.

**Design:** coerente col sito (navy #1E2235 / oro #C9A961 / Archivo+Inter), card con hover,
griglia responsive (3→2→1 col), CTA "Richiedi un preventivo" a fondo pagina.

**Scartati** (qualità/coerenza): "Vetrina-1/3" (erano foto stock), loghi su bianco
(CVS, Kairos, Petroil), slide di testo deboli (Fortunato Romeo/Posta Express),
etichette poco leggibili (Fragomani).

**In sospeso:** 4 foto reali di LEDwall installati (Sagra della Cipolla, Hotel La Bussola,
Il Trenino, Bagno Mareservice) non scaricabili via API (file 8–12 MB, oltre il limite del
tool). Da aggiungere in cima ai LEDwall appena disponibili in versione più leggera.

Builder pagina: `scripts/build-lavori-final.py` → `wp-pages/lavori.html`.
Anteprima: `scripts/build-lavori-preview.py`. Backup pre-modifica salvato prima del POST.

## Riepilogo modifiche 2026-08-07 → 2026-08-10 (ricostruito dallo storico git)

Queste modifiche risultano pubblicate nelle sessioni del 7 e del 10 agosto
ma non erano ancora riportate in questo log.

| Data | Area | Cosa |
|------|------|------|
| 08-07 | Home | Hero commerciale "Tutto quello che serve per far vedere la tua azienda", 7 servizi con CTA, barra azioni mobile (Chiama / WhatsApp / Preventivo), messaggio WhatsApp contestuale per pagina |
| 08-07 | Menu | Home, Servizi (a tendina con 7 voci), LEDWALL, I nostri lavori, Chi Siamo, Contatti |
| 08-07 | SEO | 6 pagine servizio dedicate con FAQ + schema FAQPage: `/grafica-branding/`, `/stampa-digitale-reggio-calabria/`, `/insegne-reggio-calabria/`, `/siti-web-reggio-calabria/`, `/social-media-reggio-calabria/`, `/abbigliamento-personalizzato/` |
| 08-07 | Footer | Footer a colonne su `#0f1d3f`, JSON-LD LocalBusiness, link a Privacy e Cookie |
| 08-07 | Legale | Pagine Privacy Policy e Cookie Policy create come **base da far verificare** (sorgente non salvato nel repo) |
| 08-07 | Contatti | Form con campo "Di cosa hai bisogno?" e azienda facoltativa |
| 08-07 | LEDWALL | Configuratore guidato (dove / misure / formula) → preventivo su WhatsApp |
| 08-10 | Font | Passaggio a Archivo (titoli) + Inter (testo) su tutto il sito, corsivi eliminati |
| 08-10 | Header | Topbar con sede "Via Ravagnese Superiore 200" (**da confermare**); CTA "Richiedi un preventivo" in header solo su LEDWALL |
| 08-10 | Numeri | Home e Chi Siamo: 1.000+ clienti, 1.300+ lavori (contati dagli archivi Drive Lavori + Fabio, ~1.150 clienti distinti) |
| 08-10 | Home | Tolto il pulsante "Richiedi un preventivo" dall'hero, resta WhatsApp |
| 08-10 | Lavori | Gallerie sfogliabili per cliente: 21 lavori, 53 foto. LEDwall: Officina Gastronomica (8), Belle Gomme (8), Il Trenino del Capo (1). Menu multi-pagina: Windy Hill (8), Bad Bull (9), Kairos (4). Stampa: 5 lavori |

## Allineamento repository — 2026-11-13

Nessuna modifica al sito live. Solo documentazione e sorgenti nel repo:

- `README.md` riscritto: mappa completa delle pagine, builder, font attuali
  (Archivo + Inter al posto di Instrument Serif + Manrope).
- `home-da-incollare.html` rigenerato da `home-wordpress.html` (era fermo alla
  versione del 3 agosto: font vecchi e numeri 200+/500+). Nuovo script
  `scripts/build-home-paste.py` per tenerlo allineato.
- `azienda.md` aggiornato con sede operativa e stato attuale.
- Nuovo `DA-FORNIRE.md`: informazioni che solo Fortunato può dare.
