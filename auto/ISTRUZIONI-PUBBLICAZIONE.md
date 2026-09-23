# Pubblicare la demo su ideamkt.it/demo/new-elettrocar

Testo da incollare nella sessione Claude collegata al computer (quella che
apre il browser con le password salvate), oppure da seguire a mano.

---

## Testo da incollare nell'altra sessione

> Devi pubblicare una demo di sito su ideamkt.it, all'indirizzo
> **https://ideamkt.it/demo/new-elettrocar/**
>
> I file stanno nel repository `coppolafortunato-a11y/Fortunato`, branch
> **`claude/vigilant-thompson-noka4z`**, cartella `auto/demo`.
>
> Passaggi:
> 1. `git fetch origin claude/vigilant-thompson-noka4z && git checkout claude/vigilant-thompson-noka4z && git pull`
> 2. Genera lo zip: `bash auto/scripts/crea-zip-demo.sh`
>    (produce `auto/demo-new-elettrocar.zip`, circa 7 MB, 95 file)
> 3. Carica il contenuto **della cartella `demo`** in
>    `public_html/demo/new-elettrocar/` sull'hosting di ideamkt.it.
>    Nel pannello dell'hosting la password è già salvata nel browser:
>    cPanel → Gestione file → `public_html` → crea la cartella `demo`, poi
>    dentro `new-elettrocar` → carica lo zip → Estrai → se l'estrazione crea
>    una sottocartella `demo`, sposta il contenuto un livello sopra.
>    In alternativa, se in `.env` ci sono FTP_HOST/FTP_USER/FTP_PASS:
>    `bash auto/scripts/pubblica-demo.sh`
> 4. Verifica aprendo `https://ideamkt.it/demo/new-elettrocar/`: devono
>    funzionare home, **Auto usate** (con i filtri), **Noleggio**, **Servizi**
>    e una scheda auto, con le foto visibili.
>
> Struttura attesa sul server:
> ```
> public_html/demo/new-elettrocar/index.html
> public_html/demo/new-elettrocar/catalogo.html
> public_html/demo/new-elettrocar/noleggio.html
> public_html/demo/new-elettrocar/servizi.html
> public_html/demo/new-elettrocar/crediti-foto.html
> public_html/demo/new-elettrocar/assets/   (auto.css, auto.js)
> public_html/demo/new-elettrocar/img/      (foto)
> public_html/demo/new-elettrocar/auto/     (schede dei singoli veicoli)
> ```
>
> Note: è una demo, le pagine hanno già il meta `noindex` e non vanno
> collegate dal menu di ideamkt.it. Non toccare nient'altro del sito.

---

## Se preferisci farlo a mano (2 minuti)

1. Scarica lo zip della demo (te l'ho mandato in chat, oppure generalo con
   `bash auto/scripts/crea-zip-demo.sh`).
2. cPanel → **Gestione file** → entra in `public_html`.
3. **+ Cartella** → `demo` → entraci → **+ Cartella** → `new-elettrocar`.
4. **Carica** → scegli lo zip → attendi il 100%.
5. Torna in `new-elettrocar`, tasto destro sullo zip → **Estrai**.
6. Se è comparsa una cartella `demo` dentro `new-elettrocar`, apri quella,
   seleziona tutto e **Sposta** in `public_html/demo/new-elettrocar`.
7. Cancella lo zip e apri https://ideamkt.it/demo/new-elettrocar/

Per toglierla, quando non serve più: cancella la cartella `demo`.
