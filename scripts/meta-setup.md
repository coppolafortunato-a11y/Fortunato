# Collegare Meta (Facebook/Instagram) — guida passo-passo

L'automazione (`scripts/meta.py`) ha bisogno di **un token di accesso Meta**.
Il token lo generi **tu**, dal tuo browser già loggato su Facebook: è l'unico
passo che richiede il tuo login. Nessuna password viene mai condivisa.

Tempo richiesto: ~5–10 minuti la prima volta.

---

## Passo 1 — Crea un'app Meta (una volta sola)

1. Vai su **https://developers.facebook.com/apps** (accedi col tuo Facebook).
2. **Crea app** → tipo **"Business"** → dai un nome (es. `IdeaMkt Automazioni`).
3. Collega la tua **Business Manager** se te lo chiede.

## Passo 2 — Genera il token con i permessi giusti

1. Apri lo **Strumento Esploratore Graph API**:
   **https://developers.facebook.com/tools/explorer**
2. In alto a destra seleziona la tua **app**.
3. Menu **"User or Page"** → scegli **"Get Page Access Token"** (o User Token).
4. Clicca **"Add permissions"** e spunta questi permessi:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`   ← per pubblicare
   - `read_insights`        ← per le statistiche pagina
   - `ads_read`             ← per vedere le campagne
   - `ads_management`       ← (solo se vuoi anche modificare le campagne)
5. Clicca **"Generate Access Token"** e **autorizza** le finestre che si aprono.
6. Copia la stringa lunga del token.

> I permessi `ads_*` e la pubblicazione, per l'uso pubblico continuativo,
> richiedono la **verifica dell'attività** (Business Verification) e la
> revisione dell'app da parte di Meta. Per **provare subito** funziona già
> ora, perché tu sei admin dell'app.

## Passo 3 — (Consigliato) Rendi il token a lunga durata

Il token dell'Esploratore dura ~1–2 ore. Per uno che dura ~60 giorni,
scambialo così (mettendo i tuoi valori):

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=TOKEN_BREVE
```

`APP_ID` e `APP_SECRET` sono in **Impostazioni → Di base** dell'app.

## Passo 4 — Mettilo in `.env`

Nel file `.env` (mai committato) aggiungi:

```bash
META_TOKEN="il-token-lungo-che-hai-copiato"
# facoltativi (l'app li ricava da sola se hai una sola pagina/account):
FB_PAGE_ID=
FB_AD_ACCOUNT=act_XXXXXXXXXX
```

---

## Passo 5 — Prova che funziona

```bash
python3 scripts/meta.py pages       # elenca le tue pagine e conferma il token
python3 scripts/meta.py insights    # statistiche della pagina
python3 scripts/meta.py campaigns   # campagne pubblicitarie e risultati
```

Per pubblicare un post:

```bash
python3 scripts/meta.py publish --text "Il nostro nuovo sito è online! https://ideamkt.it"
python3 scripts/meta.py publish --text "Nuovo lavoro" --photo assets/lavori/foto.jpg
```

---

## Sicurezza

- Il token vive **solo** nel tuo `.env` locale, già escluso da git.
- Se lo esponi per errore, **revocalo** da developers.facebook.com → la tua app,
  oppure cambia l'App Secret: tutti i token vecchi smettono di funzionare.
- A lavoro finito puoi ridurre i permessi o rigenerare il token.
