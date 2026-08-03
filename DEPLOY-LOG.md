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
