#!/usr/bin/env python3
"""
meta.py — ponte con Meta (Facebook/Instagram) via Graph + Marketing API.

Gestisce, da riga di comando e con un solo token:
  - vedere le pagine e i loro dati              -> `pages`
  - pubblicare un post (testo / link / foto)    -> `publish`
  - controllare le campagne pubblicitarie       -> `campaigns`
  - leggere le statistiche della pagina         -> `insights`

Nessuna dipendenza esterna: usa solo la libreria standard di Python.

Configurazione (in `.env`, mai committato):
  META_TOKEN      token di accesso Meta (utente o pagina). OBBLIGATORIO.
  FB_PAGE_ID      ID della pagina Facebook (facoltativo: se manca lo ricava).
  FB_AD_ACCOUNT   ID account pubblicitario, formato act_1234567890 (facoltativo).

Come si genera il token: vedi scripts/meta-setup.md (guida passo-passo).

Esempi:
  python3 scripts/meta.py pages
  python3 scripts/meta.py insights
  python3 scripts/meta.py campaigns
  python3 scripts/meta.py publish --text "Ciao dal nostro nuovo sito!"
  python3 scripts/meta.py publish --text "Guarda qui" --link https://ideamkt.it
  python3 scripts/meta.py publish --text "Nuovo lavoro" --photo assets/lavori/foto.jpg
  python3 scripts/meta.py publish --text "..." --yes    # salta la conferma
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

GRAPH = "https://graph.facebook.com/v21.0"


# ---------------------------------------------------------------- utilità ---
def load_env(path=".env"):
    """Carica le variabili da .env senza dipendenze (solo KEY=VALUE)."""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                val = val.strip().strip('"').strip("'")
                os.environ.setdefault(key.strip(), val)


def token():
    tok = os.environ.get("META_TOKEN", "").strip()
    if not tok:
        sys.exit("ERRORE: manca META_TOKEN in .env (vedi scripts/meta-setup.md).")
    return tok


def api(path, params=None, data=None, method="GET"):
    """Chiamata Graph API. `data` non-None => POST. Ritorna dict JSON."""
    params = dict(params or {})
    params.setdefault("access_token", token())
    url = f"{GRAPH}/{path.lstrip('/')}"
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
        body = None
    else:
        body = urllib.parse.urlencode({**params, **(data or {})}).encode()
    req = urllib.request.Request(url, data=body, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        try:
            msg = json.loads(detail)["error"]["message"]
        except Exception:
            msg = detail
        sys.exit(f"ERRORE Meta ({e.code}): {msg}")
    except urllib.error.URLError as e:
        sys.exit(f"ERRORE di rete: {e.reason}")


def page_id_and_token():
    """Ricava (page_id, page_access_token) dal token e da FB_PAGE_ID."""
    want = os.environ.get("FB_PAGE_ID", "").strip()
    data = api("me/accounts", {"fields": "id,name,access_token"}).get("data", [])
    if not data:
        sys.exit("Nessuna pagina accessibile con questo token "
                 "(serve il permesso pages_show_list / pages_manage_posts).")
    if want:
        for p in data:
            if p["id"] == want:
                return p["id"], p["access_token"]
        sys.exit(f"FB_PAGE_ID={want} non trovato tra le pagine di questo token.")
    if len(data) > 1:
        names = ", ".join(f'{p["name"]} ({p["id"]})' for p in data)
        sys.exit(f"Più pagine disponibili: {names}\n"
                 f"Imposta FB_PAGE_ID in .env per scegliere.")
    return data[0]["id"], data[0]["access_token"]


# ------------------------------------------------------------- sottocomandi ---
def cmd_pages(_):
    me = api("me", {"fields": "id,name"})
    print(f"Token valido. Utente/entità: {me.get('name','?')} (id {me.get('id','?')})\n")
    data = api("me/accounts",
               {"fields": "id,name,category,fan_count,link,tasks"}).get("data", [])
    if not data:
        print("Nessuna pagina collegata a questo token.")
        return
    print(f"Pagine accessibili ({len(data)}):")
    for p in data:
        tasks = ",".join(p.get("tasks", [])) or "—"
        print(f"  • {p['name']}  (id {p['id']})")
        print(f"      categoria: {p.get('category','?')} · "
              f"follower: {p.get('fan_count','?')} · permessi: {tasks}")
        print(f"      {p.get('link','')}")


def cmd_insights(_):
    pid, ptok = page_id_and_token()
    metrics = "page_impressions,page_post_engagements,page_fans,page_views_total"
    r = api(f"{pid}/insights",
            {"metric": metrics, "period": "days_28", "access_token": ptok})
    print(f"Statistiche pagina {pid} (ultimi 28 giorni):\n")
    for m in r.get("data", []):
        vals = m.get("values", [])
        last = vals[-1]["value"] if vals else "—"
        print(f"  • {m.get('title', m['name'])}: {last}")
    if not r.get("data"):
        print("  (nessun dato: pagina nuova o permesso read_insights mancante)")


def cmd_campaigns(_):
    acct = os.environ.get("FB_AD_ACCOUNT", "").strip()
    if not acct:
        accts = api("me/adaccounts",
                    {"fields": "id,name,account_status"}).get("data", [])
        if not accts:
            sys.exit("Nessun account pubblicitario (serve il permesso ads_read).")
        if len(accts) > 1:
            lst = ", ".join(f'{a["name"]} ({a["id"]})' for a in accts)
            sys.exit(f"Più account ads: {lst}\nImposta FB_AD_ACCOUNT in .env.")
        acct = accts[0]["id"]
    fields = "name,status,objective,daily_budget,lifetime_budget"
    camps = api(f"{acct}/campaigns", {"fields": fields, "limit": 50}).get("data", [])
    if not camps:
        print(f"Account {acct}: nessuna campagna.")
        return
    print(f"Campagne su {acct} ({len(camps)}):\n")
    for c in camps:
        budget = c.get("daily_budget") or c.get("lifetime_budget")
        budget = f"{int(budget)/100:.2f}€" if budget else "—"
        ins = api(f"{c['id']}/insights",
                  {"fields": "impressions,clicks,spend,ctr,cpc",
                   "date_preset": "last_30d"}).get("data", [])
        s = ins[0] if ins else {}
        print(f"  • {c['name']}  [{c.get('status')}]  obiettivo {c.get('objective','?')}")
        print(f"      budget {budget} · spesa {s.get('spend','0')}€ · "
              f"impression {s.get('impressions','0')} · click {s.get('clicks','0')} · "
              f"CTR {s.get('ctr','0')}% · CPC {s.get('cpc','0')}€")


def cmd_publish(args):
    if not args.text and not args.link and not args.photo:
        sys.exit("Serve almeno --text, --link o --photo.")
    pid, ptok = page_id_and_token()

    # anteprima + conferma (a meno di --yes)
    print("Sto per pubblicare su Facebook:")
    print(f"  pagina : {pid}")
    if args.text:
        print(f"  testo  : {args.text}")
    if args.link:
        print(f"  link   : {args.link}")
    if args.photo:
        print(f"  foto   : {args.photo}")
    if not args.yes:
        if input("Confermi la pubblicazione? [s/N] ").strip().lower() not in ("s", "si", "y"):
            sys.exit("Annullato.")

    if args.photo:
        if not os.path.exists(args.photo):
            sys.exit(f"File non trovato: {args.photo}")
        r = _publish_photo(pid, ptok, args.photo, args.text)
    else:
        data = {"access_token": ptok}
        if args.text:
            data["message"] = args.text
        if args.link:
            data["link"] = args.link
        r = api(f"{pid}/feed", data=data, method="POST")
    post_id = r.get("post_id") or r.get("id", "?")
    print(f"✓ Pubblicato. ID post: {post_id}")


def _publish_photo(pid, ptok, path, caption):
    """Upload multipart di una foto sul feed della pagina."""
    import mimetypes
    import uuid
    boundary = uuid.uuid4().hex
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as fh:
        content = fh.read()
    parts = []
    for key, val in (("access_token", ptok), ("caption", caption or "")):
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; "
                     f'name="{key}"\r\n\r\n{val}\r\n'.encode())
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"source\"; "
        f'filename="{os.path.basename(path)}"\r\n'
        f"Content-Type: {mime}\r\n\r\n".encode() + content + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    req = urllib.request.Request(
        f"{GRAPH}/{pid}/photos", data=body, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRORE upload foto ({e.code}): {e.read().decode(errors='replace')}")


# --------------------------------------------------------------------- main ---
def main():
    load_env()
    p = argparse.ArgumentParser(description="Ponte Meta (Facebook/Instagram).")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pages", help="elenca pagine e dati del token")
    sub.add_parser("insights", help="statistiche pagina (28 giorni)")
    sub.add_parser("campaigns", help="campagne pubblicitarie + risultati")
    pub = sub.add_parser("publish", help="pubblica un post sulla pagina")
    pub.add_argument("--text", help="testo del post")
    pub.add_argument("--link", help="URL da allegare")
    pub.add_argument("--photo", help="percorso immagine da caricare")
    pub.add_argument("--yes", action="store_true", help="salta la conferma")
    args = p.parse_args()
    {"pages": cmd_pages, "insights": cmd_insights,
     "campaigns": cmd_campaigns, "publish": cmd_publish}[args.cmd](args)


if __name__ == "__main__":
    main()
