# Consegna lavoro — Integrazione Meta (Facebook/Instagram)

> Documento per la sessione **Claude che gira sul PC** (quella con accesso al
> browser locale). Qui trovi **tutto** quello che è stato fatto finora e i
> prossimi passi. Lavoriamo per **Idea Marketing** (Coppola Fortunato, Reggio
> Calabria) che gestisce **78 pagine Facebook**.
>
> Branch di lavoro: `claude/facebook-view-publish-qrl8lu`

---

## 1. Cosa è già stato fatto ✅

### App Meta creata e configurata
- **App:** `IdeaMkt`
- **App ID:** `1997968524238070`
- **Caso d'uso attivato:** *"Gestisci tutto sulla tua Pagina"* (PAGES_API)
- **Permessi abilitati nel caso d'uso** (stato "Pronta per il test"):
  `pages_show_list`, `pages_manage_posts`, `pages_read_engagement`,
  `read_insights`, `business_management`
- Pagina impostazioni: https://developers.facebook.com/apps/1997968524238070/settings/basic/
- Esploratore Graph API: https://developers.facebook.com/tools/explorer/

### Codice creato nel repo (branch sopra)
| File | Cosa fa |
|------|---------|
| `scripts/meta.py` | CLI: `pages`, `insights`, `campaigns`, `publish`. Solo stdlib Python. |
| `scripts/meta-setup.md` | Guida per generare il token. |
| `.env.example` | Variabili `META_TOKEN`, `FB_PAGE_ID`, `FB_AD_ACCOUNT`. |

### Verificato funzionante (già testato via API)
- Lettura di tutte le **78 pagine** ✅
- **Statistiche** di *Idea Marketing* (id `280447418753575`): 601 follower,
  81 visualizzazioni/28gg, 0 interazioni, 0 nuovi follower → **pagina ferma**.
- Permesso di **pubblicazione** presente (`pages_manage_posts`) ✅

---

## 2. Problema aperto: il token scade ogni ~1 ora

I token dell'Esploratore durano poco. **Soluzione: token a lunga durata.**
Da fare (la sessione PC può farlo perché ha il browser + il terminale):

### Passo A — recupera i 2 valori
1. **App Secret**: https://developers.facebook.com/apps/1997968524238070/settings/basic/
   → "Mostra" accanto a *Chiave segreta* → copia.
2. **Token breve**: https://developers.facebook.com/tools/explorer/
   → app `IdeaMkt`, permessi presenti → *Generate Access Token* → copia.

### Passo B — scambia con un token utente a lunga durata (~60 giorni)
```bash
APP_ID=1997968524238070
APP_SECRET=<chiave_segreta>
SHORT_TOKEN=<token_breve>

curl -s "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=$APP_ID&client_secret=$APP_SECRET&fb_exchange_token=$SHORT_TOKEN"
# -> restituisce {"access_token":"<LONG_USER_TOKEN>", ...}
```

### Passo C — ottieni il token PAGINA (non scade mai)
```bash
LONG_USER_TOKEN=<dal passo B>

# elenca le pagine con il loro page-token permanente
curl -s "https://graph.facebook.com/v21.0/me/accounts?fields=id,name,access_token&limit=100&access_token=$LONG_USER_TOKEN"
```
Il campo `access_token` di ogni pagina, ottenuto da un token utente a lunga
durata, è un **Page Access Token che NON scade**. Salvalo in `.env` come
`META_TOKEN` (oppure per-pagina).

> `.env` è già in `.gitignore`: il token non finisce mai su git.

---

## 3. Come si usa lo strumento

```bash
# metti il token in .env:  META_TOKEN="<page-o-user-token>"
python3 scripts/meta.py pages       # elenca tutte le pagine
python3 scripts/meta.py insights    # statistiche (imposta FB_PAGE_ID per scegliere)
python3 scripts/meta.py campaigns   # campagne pubblicitarie (serve ads_read, vedi sotto)
python3 scripts/meta.py publish --text "..."                    # post di testo
python3 scripts/meta.py publish --text "..." --link https://ideamkt.it
python3 scripts/meta.py publish --text "..." --photo assets/foto.jpg
```

Per scegliere la pagina: metti `FB_PAGE_ID=<id>` in `.env`.
ID utili: **Idea Marketing** = `280447418753575`.

---

## 4. Prossimo compito: PUBBLICARE su Idea Marketing

La pagina dell'agenzia è ferma. Bozza già pronta e approvata come punto di
partenza (chiedere conferma all'utente prima di pubblicare):

```
🎯 Diamo forma alla tua immagine.

Il nostro nuovo sito è online! Scopri come Idea Marketing aiuta la tua
attività a farsi notare: stampa, insegne, LEDwall, siti web e social,
tutto con un unico interlocutore.

📍 Reggio Calabria — dal 2011 al fianco delle imprese del territorio.
👉 https://ideamkt.it

#IdeaMarketing #ReggioCalabria #Comunicazione #Marketing #Stampa #Insegne
```

Comando:
```bash
FB_PAGE_ID=280447418753575 python3 scripts/meta.py publish \
  --text "🎯 Diamo forma alla tua immagine. ... 👉 https://ideamkt.it #IdeaMarketing #ReggioCalabria"
```
Lo script chiede **conferma** prima di pubblicare (usa `--yes` per saltarla).

---

## 5. Campagne pubblicitarie (più avanti)

Il caso d'uso attuale copre le Pagine, non le inserzioni. Per le **campagne**
(`campaigns`) serve aggiungere all'app il caso d'uso **API Marketing** con i
permessi `ads_read` (e `ads_management` per modificarle), che richiedono la
**verifica dell'attività** (Business Verification). Da fare quando serve.

---

## 6. Situazione Meduuza (indagine sicurezza — CHIUSA, tutto ok lato FB)

Sospetto hack sulla pagina **Meduuza** (id `102378035849675`) e Instagram non
accessibile. Verificato via API:
- **Admin pagina:** solo Fortunato Coppola ✅
- **Business Manager "Meduuza"** (id `467054317065732`): solo Fortunato ADMIN,
  **nessun** invito in sospeso, **nessun** partner sconosciuto ✅
- **Instagram:** NON collegato alla pagina (solo un page-backed IG "ombra").

**Conclusione:** lato Facebook nessun intruso. Il problema è l'account
**Instagram** (login perso), che si recupera SOLO dal lato Instagram:
- https://www.instagram.com/hacked → "account compromesso"
- cercare l'email Meta *"il tuo indirizzo email è stato cambiato"* → link "Annulla"
- una volta recuperato, ricollegarlo alla pagina da Meta Business Suite.

---

## 7. Note di sicurezza
- I token incollati in chat durante il setup vanno considerati **compromessi**:
  rigenerare/revocare dall'app a lavoro finito.
- L'App Secret usala una volta per il token lungo; puoi **resettarla** dopo
  (il page-token già emesso resta valido).
- Non committare mai `.env`.
