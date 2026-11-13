# Sito ideamkt.it — sorgenti e kit di pubblicazione

Sorgenti, builder e script per il sito **ideamkt.it** (WordPress, tema
Twenty Twenty-Five) di Idea Marketing di Coppola Fortunato — Reggio Calabria.

Il repository contiene i **sorgenti** delle pagine e l'automazione, non i
segreti. Lo storico di cosa è stato pubblicato e quando è in
[`DEPLOY-LOG.md`](DEPLOY-LOG.md); i dati aziendali in [`azienda.md`](azienda.md);
le informazioni ancora da ricevere da Fortunato in [`DA-FORNIRE.md`](DA-FORNIRE.md).

> **Regola d'oro.** Tutto ciò che sta qui tocca il sito **live** solo quando
> uno script viene lanciato con le credenziali in `.env`. Nessuna modifica al
> sito va fatta senza l'ok esplicito di Fortunato, e sempre con backup prima.

## Mappa del sito

| Pagina | Slug | ID WP | Sorgente nel repo | Builder |
|--------|------|-------|-------------------|---------|
| Home | `/` | 7 | `home-wordpress.html` | a mano (+ `deploy-home.sh`) |
| Servizi | `/servizi/` | 10 | `wp-pages/servizi.html` | `scripts/build-pages.py` |
| LEDWALL & Digital Signage | `/ledwall/` | 12 | `wp-pages/ledwall.html` | `scripts/build-pages.py` |
| Chi Siamo | `/chi-siamo/` | 14 | `wp-pages/chi-siamo.html` | `scripts/build-pages.py` |
| Contatti (form) | `/contatti/` | 16 | `wp-pages/contatti.html` | `scripts/build-pages.py` |
| Preventivi LEDWALL (calcolatore + configuratore) | `/preventivi-ledwall/` | 27 | `wp-pages/preventivi-ledwall.html` | `scripts/build-pages.py` |
| I nostri lavori (portfolio) | `/lavori/` | 92 | `wp-pages/lavori.html` | `scripts/build-lavori-gallery.py` |
| Grafica & Branding | `/grafica-branding/` | — | `wp-pages/grafica-branding.html` | `scripts/build-pages.py` |
| Stampa digitale | `/stampa-digitale-reggio-calabria/` | — | `wp-pages/stampa-digitale-reggio-calabria.html` | `scripts/build-pages.py` |
| Insegne | `/insegne-reggio-calabria/` | — | `wp-pages/insegne-reggio-calabria.html` | `scripts/build-pages.py` |
| Siti web | `/siti-web-reggio-calabria/` | — | `wp-pages/siti-web-reggio-calabria.html` | `scripts/build-pages.py` |
| Social media | `/social-media-reggio-calabria/` | — | `wp-pages/social-media-reggio-calabria.html` | `scripts/build-pages.py` |
| Abbigliamento e gadget | `/abbigliamento-personalizzato/` | — | `wp-pages/abbigliamento-personalizzato.html` | `scripts/build-pages.py` |
| Privacy Policy | `/privacy-policy/` | — | *non nel repo* | creata dal pannello |
| Cookie Policy | `/cookie-policy/` | — | *non nel repo* | creata dal pannello |

Parti comuni del tema (template part):

| Parte | Sorgente | Note |
|-------|----------|------|
| Header (topbar, logo, menu, CTA solo su LEDWALL, WhatsApp) | `scripts/build-header.py` | lavora su un JSON scaricato dal sito (`/tmp/hdr.json`) |
| Footer a colonne + JSON-LD LocalBusiness | `wp-pages/footer.html` | sfondo `#0f1d3f`, link Privacy/Cookie |
| Alternativa via FTP a topbar + WhatsApp | `mu-plugins/ideamkt-extras.php` | **non attivo**: oggi topbar e WhatsApp vivono nell'header |

Gli ID delle 6 pagine servizio e delle pagine legali non sono stati
registrati: si leggono con `./scripts/check-permalinks.sh`.

## Contenuto del repository

| Percorso | A cosa serve |
|----------|--------------|
| `home-wordpress.html` | Sorgente della homepage (pagina ID 7). |
| `home-da-incollare.html` | Stessa home già avvolta nel blocco `wp:html` con fix larghezza, da incollare a mano nell'editor. **Generato**: `python3 scripts/build-home-paste.py`. |
| `wp-pages/*.html` | Sorgenti generati delle pagine interne e del footer. |
| `wp-pages/lavori-*.json` | Dati del portfolio: progetti, manifest immagini, mappa id Media Library. |
| `assets/` | Logo, favicon, foto hero; `assets/lavori/` foto reali ottimizzate del portfolio. |
| `mu-plugins/ideamkt-extras.php` | Mu-plugin alternativo (topbar + WhatsApp). |
| `scripts/deploy-home.sh` | Backup + pubblicazione della home sulla pagina 7. |
| `scripts/build-pages.py` | Genera le pagine interne e le 6 pagine servizio. |
| `scripts/build-header.py` | Ricostruisce l'header del tema (topbar, CTA, WhatsApp). |
| `scripts/build-lavori-gallery.py` | Genera `/lavori/` con gallerie sfogliabili (versione attuale). |
| `scripts/build-lavori-final.py`, `build-lavori-preview.py` | Versioni precedenti del builder portfolio / anteprima locale. |
| `scripts/optimize-*.py` | Ottimizzano le foto (max 1400px, qualità 82). |
| `scripts/upload-media.sh` | Carica le foto nella Media Library con title/alt SEO. |
| `scripts/upload-mu-plugin.sh` | Carica il mu-plugin via FTP. |
| `scripts/check-permalinks.sh` | Elenca slug e ID reali per verificare i link. |
| `.env.example` | Modello di configurazione da copiare in `.env`. |

> Nota: `build-pages.py`, `build-header.py` e i builder `build-lavori-*.py` leggono e scrivono file di
> lavoro in percorsi temporanei della sessione in cui sono stati usati
> (es. `/tmp/hdr.json`, `page-27.html`, `lavori_projects.json` nello scratchpad). Prima di rilanciarli, scaricare dal
> sito il contenuto attuale corrispondente e adattare i percorsi.

## Stile

Palette: navy `#1E2235` · oro `#C9A961` · carta `#f8f7f4` · separatori `#e0ddd6`
· footer `#0f1d3f` · WhatsApp `#25D366`.
Font: titoli **Archivo**, testo **Inter** (Google Fonts). Nessun corsivo
(regola globale su `#ik-home` / `#ik-page`), nessuna emoji.

Contenuti: solo dati e lavori reali. Niente foto stock spacciate per lavori,
niente recensioni o numeri inventati (vedi `azienda.md`).

## 1. Prerequisiti — credenziali

Crea una **Password applicazione** dedicata (non usare la password di login):

WordPress → Utenti → Profilo → in fondo *"Password applicazione"* → nome
`claude-code` → **Aggiungi**. Copia subito la stringa, non si rivede più.

```bash
cp .env.example .env
# apri .env e incolla WP_USER, WP_APP_PASSWORD, WP_BASE (e FTP_* se li hai)
set -a; source .env; set +a
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE/wp-json/wp/v2/users/me?context=edit" | head -c 300
```

Se risponde `rest_not_logged_in`, l'hosting toglie l'header `Authorization`:
aggiungi in `.htaccess` alla radice del sito
`SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1` e riprova.

## 2. Pubblicare la homepage (pagina ID 7)

```bash
./scripts/deploy-home.sh             # backup, payload, pubblicazione, verifica
./scripts/deploy-home.sh --dry-run   # prepara payload.json senza inviare nulla
FULLWIDTH=0 ./scripts/deploy-home.sh # se il tema gestisce già la larghezza piena
```

Dopo ogni modifica a `home-wordpress.html`, rigenera anche la copia da
incollare: `python3 scripts/build-home-paste.py`.

## 3. Pubblicare le altre pagine

Le pagine interne si pubblicano con un POST su `/wp-json/wp/v2/pages/<ID>`
con il contenuto del file in `wp-pages/` (già avvolto in `wp:html`), **sempre
dopo aver salvato il backup** del contenuto attuale
(`GET /wp-json/wp/v2/pages/<ID>?context=edit` → `backup-<pagina>-AAAAMMGG.json`).
Header e footer sono template part del tema (`/wp-json/wp/v2/template-parts`).

## 4. Rollback

POST sullo stesso endpoint con il `content` del backup corrispondente. I
backup non sono versionati (vedi `.gitignore`): conservarli in locale.

## Vincoli

- Nessuna modifica al sito live senza l'ok esplicito di Fortunato, una
  modifica alla volta.
- Backup sempre prima di sovrascrivere.
- Non committare `.env`, `payload.json` o i backup (già in `.gitignore`).
- La password applicazione si revoca da Utenti → Profilo a lavoro finito.
