# Sito ideamkt.it — kit di pubblicazione homepage

Materiale e automazioni per pubblicare la nuova homepage su **ideamkt.it**
(WordPress, tema Twenty Twenty-Five) ed aggiungere barra contatti + bottone WhatsApp.

Titolare: Idea Marketing di Coppola Fortunato — Reggio Calabria.

> **Nota importante.** La pubblicazione tocca il sito **live** e richiede
> credenziali segrete che, per sicurezza, **non stanno in questo repository**.
> Gli script qui sotto vanno lanciati da te (o da chi ha le credenziali) dopo
> aver creato un file `.env` locale. Il repo contiene i sorgenti e l'automazione,
> non i segreti.

## Contenuto del repository

| File | A cosa serve |
|------|--------------|
| `home-wordpress.html` | Sorgente della nuova homepage (pagina ID 7). |
| `mu-plugins/ideamkt-extras.php` | Mu-plugin: barra contatti in alto + bottone WhatsApp fisso. |
| `scripts/deploy-home.sh` | Obiettivo 1 — backup, prepara e pubblica la home sulla pagina 7. |
| `scripts/upload-mu-plugin.sh` | Obiettivo 2 — carica il mu-plugin via FTP. |
| `scripts/check-permalinks.sh` | Obiettivo 3.4 — elenca gli slug reali per verificare gli href. |
| `.env.example` | Modello di configurazione da copiare in `.env`. |

## 1. Prerequisiti — credenziali

Crea una **Password applicazione** dedicata (non usare la password di login):

WordPress → Utenti → Profilo → in fondo *"Password applicazione"* → nome
`claude-code` → **Aggiungi**. Copia subito la stringa (`abcd EFGH ijkl …`),
non si rivede più.

Poi:

```bash
cp .env.example .env
# apri .env e incolla WP_USER, WP_APP_PASSWORD, WP_BASE (e FTP_* se li hai)
```

Il file `.env` è già in `.gitignore`: non finirà mai su git.

Verifica che l'autenticazione funzioni:

```bash
set -a; source .env; set +a
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE/wp-json/wp/v2/users/me?context=edit" | head -c 300
```

Deve rispondere con l'utente e le sue capability. Se risponde
`rest_not_logged_in`, l'hosting sta togliendo l'header `Authorization`:
aggiungi in `.htaccess` alla radice del sito la riga

```
SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
```

e riprova.

## 2. Obiettivo 1 — pubblicare la homepage (pagina ID 7)

```bash
./scripts/deploy-home.sh
```

Lo script, in un colpo solo:

1. verifica l'autenticazione;
2. fa il **backup** del contenuto attuale in `backup-home-AAAAMMGG-HHMM.json`
   (si ferma se il backup è più corto di 1000 byte);
3. prepara il payload — avvolge tutto nel blocco `<!-- wp:html -->` di Gutenberg
   e aggiunge il fix a larghezza piena alla regola `#ik-home{…}`;
4. pubblica sulla pagina 7;
5. verifica che `ik-home` sia presente nel contenuto salvato.

Opzioni:

```bash
./scripts/deploy-home.sh --dry-run   # prepara payload.json senza inviare nulla
FULLWIDTH=0 ./scripts/deploy-home.sh # se il tema gestisce già la larghezza piena
```

Poi apri `https://ideamkt.it` in incognito e controlla l'hero navy con il titolo
*"Diamo forma alla tua immagine"*.

## 3. Obiettivo 2 — barra contatti e bottone WhatsApp

Il file `mu-plugins/ideamkt-extras.php` va in `public_html/wp-content/mu-plugins/`.
I mu-plugin si attivano da soli.

Con FTP configurato in `.env`:

```bash
./scripts/upload-mu-plugin.sh
```

Senza FTP: carica `mu-plugins/ideamkt-extras.php` a mano da cPanel → Gestione file
nella cartella `public_html/wp-content/mu-plugins/`.

Verifica: barra navy in alto col numero **320 611 6711** e tondo verde WhatsApp
in basso a destra su ogni pagina.

## 4. Obiettivo 3 — pulizie (manuali, dal pannello WordPress)

Queste vanno fatte a mano perché toccano tema, menu e footer:

1. **Titolo pagina Home** — nel tema a blocchi il titolo "Home" compare sopra
   l'hero. Toglilo: Aspetto → Editor → Modelli → Pagina, rimuovi il blocco
   *Titolo articolo* (o crea un modello senza titolo da assegnare alla Home).
2. **Menu** — rimuovi le voci "Sample Page" e la "Home" duplicata, poi cestina
   la pagina Sample Page.
3. **Footer** — sostituisci "My WordPress Blog" con i dati veri:
   Idea Marketing di Coppola Fortunato, Via Campoli 34, 89134 Reggio Calabria,
   tel 320 611 6711, P.IVA 02520960804 — sfondo `#0f1d3f`.
4. **Permalink** — verifica gli slug reali:

   ```bash
   ./scripts/check-permalinks.sh
   ```

   Se `/contatti/`, `/servizi/`, `/ledwall-digital-signage/`,
   `/preventivi-ledwall/` non combaciano, correggi gli href in
   `home-wordpress.html` e rilancia `deploy-home.sh`.

## Vincoli (dal briefing)

- Non toccare pagine diverse dalla ID 7 senza chiedere.
- Fare sempre il backup prima di sovrascrivere (lo script lo fa).
- Non committare `.env`, `payload.json` o i backup (già in `.gitignore`).
- La password applicazione si revoca da Utenti → Profilo a lavoro finito.

## Palette e font

Navy `#1E2235` · oro `#C9A961` · carta `#f8f7f4` · separatori `#e0ddd6` ·
footer `#0f1d3f`. Titoli in Instrument Serif, testo in Manrope.
