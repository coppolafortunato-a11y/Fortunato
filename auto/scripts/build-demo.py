#!/usr/bin/env python3
"""Genera la demo statica del sito auto a partire da demo/auto.json.

La demo usa gli stessi CSS/JS del plugin WordPress: quello che si vede qui
e' quello che si vedra' sul sito vero, con le foto e i dati reali al posto
dei segnaposto.

Uso:  python3 scripts/build-demo.py
"""

import html
import json
import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
DEMO = RADICE / "demo"
IMG = DEMO / "img"
SCHEDE = DEMO / "auto"
DATI = json.loads((DEMO / "auto.json").read_text(encoding="utf-8"))

AZIENDA = DATI["concessionaria"]
AUTO = DATI["auto"]
SERVIZI = DATI.get("servizi", [])
NOLEGGIO = DATI.get("noleggio", [])

CATEGORIE_NOLEGGIO = {
    "breve": "Noleggio giornaliero",
    "furgoni": "Furgoni e 9 posti",
    "cerimonie": "Cerimonie e matrimoni",
}

STATI = {
    "disponibile": ("Disponibile", "badge--ok"),
    "prenotata": ("Prenotata", "badge--muted"),
    "venduta": ("Venduta", "badge--muted"),
    "in-arrivo": ("In arrivo", "badge--muted"),
}

# Tinte dei segnaposto: al loro posto andranno le foto reali dei veicoli.
TINTE = ["#1f2a37", "#2b3a4a", "#3a2f2f", "#26343a", "#332b3d", "#2f3b2f",
         "#3b3326", "#243043", "#3a2a33"]

VISTE = ["Vista esterna", "Interni", "Posteriore"]

PREFISSO_IMG = ""


def e(testo):
    return html.escape(str(testo), quote=True)


def euro(valore):
    return f"{valore:,}".replace(",", ".") + " €"


def km(valore):
    return f"{valore:,}".replace(",", ".") + " km"


def immatricolazione(auto):
    anno, mese = auto["immatricolazione"].split("-")
    return f"{mese}/{anno}"


def anno(auto):
    return auto["immatricolazione"].split("-")[0]


def wa_link(testo):
    from urllib.parse import quote
    return f"https://wa.me/{AZIENDA['whatsapp']}?text={quote(testo)}"


# --------------------------------------------------------------------------
# Segnaposto foto
# --------------------------------------------------------------------------

def scrivi_segnaposto():
    IMG.mkdir(parents=True, exist_ok=True)
    sagoma = (
        "M60,150 L76,104 Q81,94 96,91 L176,85 Q196,83 216,95 L256,119 L306,127 "
        "Q326,131 326,150 L326,166 Q326,173 317,173 L296,173 A28,28 0 0,0 240,173 "
        "L150,173 A28,28 0 0,0 94,173 L69,173 Q60,173 60,166 Z"
    )
    for i, auto in enumerate(AUTO + NOLEGGIO):
        tinta = TINTE[i % len(TINTE)]
        viste = VISTE if auto in AUTO else VISTE[:2]
        for n, vista in enumerate(viste, start=1):
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="800" height="600" role="img" aria-label="{e(auto['titolo'])} — segnaposto">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{tinta}"/>
      <stop offset="1" stop-color="#0f1216"/>
    </linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#g)"/>
  <g transform="translate(6,34) scale(0.94)" opacity="0.5">
    <path d="{sagoma}" fill="#ffffff" opacity="0.14"/>
    <circle cx="122" cy="173" r="27" fill="none" stroke="#ffffff" stroke-opacity="0.35" stroke-width="5"/>
    <circle cx="268" cy="173" r="27" fill="none" stroke="#ffffff" stroke-opacity="0.35" stroke-width="5"/>
    <path d="M104,104 L170,99 L170,82 Q150,83 135,88 Z" fill="#ffffff" opacity="0.12"/>
  </g>
  <text x="24" y="250" fill="#ffffff" font-family="Archivo, Inter, sans-serif" font-size="18" font-weight="700">{e(auto['titolo'])}</text>
  <text x="24" y="272" fill="#ffffff" fill-opacity="0.6" font-family="Inter, sans-serif" font-size="12">{e(vista)} · foto di esempio, qui andranno quelle reali</text>
</svg>
"""
            (IMG / f"{auto['slug']}-{n}.svg").write_text(svg, encoding="utf-8")


# --------------------------------------------------------------------------
# Pezzi di pagina
# --------------------------------------------------------------------------

def foto(slug, n, prefix=""):
    """Percorso dell'immagine n del veicolo: foto scaricata se c'è, sennò segnaposto."""
    if (IMG / f"{slug}-{n}.jpg").exists():
        return f"{prefix}img/{slug}-{n}.jpg"
    return f"{prefix}img/{slug}-{n}.svg"


def quante_foto(slug, massimo=3):
    return [n for n in range(1, massimo + 1)
            if (IMG / f"{slug}-{n}.jpg").exists() or (IMG / f"{slug}-{n}.svg").exists()]


def telefono_link(numero):
    return "tel:+39" + numero.replace(" ", "")


def recapiti_footer():
    """Telefono, cellulare ed e-mail, saltando quelli che non abbiamo."""
    righe = [f'<a href="{telefono_link(AZIENDA["telefono"])}">{e(AZIENDA["telefono"])}</a>']
    if AZIENDA.get("cellulare"):
        righe.append(f'<a href="{telefono_link(AZIENDA["cellulare"])}">{e(AZIENDA["cellulare"])}</a>')
    if AZIENDA.get("email"):
        righe.append(f'<a href="mailto:{e(AZIENDA["email"])}">{e(AZIENDA["email"])}</a>')
    return "<br>\n        ".join(righe)


def iniziali():
    """Logo provvisorio: le iniziali del nome, finché non arriva quello vero."""
    parole = [p for p in AZIENDA["nome"].split() if p[:1].isalpha()]
    return "".join(p[0] for p in parole[:2]).upper()


def testa(titolo, descrizione, css_prefix, attiva):
    voci = [("Home", "index.html"), ("Auto usate", "catalogo.html"),
            ("Noleggio", "noleggio.html"), ("Servizi", "servizi.html"),
            ("Contatti", "index.html#contatti")]
    righe_nav = []
    for etichetta, href in voci:
        corrente = ' aria-current="page"' if etichetta == attiva else ''
        righe_nav.append(f'      <a href="{css_prefix}{href}"{corrente}>{etichetta}</a>')
    nav = "\n".join(righe_nav)
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titolo)}</title>
<meta name="description" content="{e(descrizione)}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_prefix}assets/auto.css">
<style>
  .demo-note{{background:#fff8e1;border-bottom:1px solid #f0e0a8;color:#6b5a11;font-size:.85rem;text-align:center;padding:8px 16px}}
  .demo-note b{{color:#4a3d06}}
</style>
</head>
<body class="auto-site">
<p class="demo-note"><b>Anteprima dimostrativa</b> — foto e dati di esempio. Nel sito vero li inserisce la concessionaria dalla propria bacheca.</p>
<div class="topbar">
  <div class="wrap">
    <span>📍 {e(AZIENDA['indirizzo'])}</span>
    <span>🕘 {e(AZIENDA['orari'])}</span>
    <span>📞 <a href="tel:+39{AZIENDA['telefono'].replace(' ', '')}">{e(AZIENDA['telefono'])}</a></span>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{css_prefix}index.html">
      <span class="brand__mark">{iniziali()}</span>
      <span>{e(AZIENDA['nome'])}</span>
    </a>
    <button class="nav-toggle" data-nav-toggle aria-controls="nav-principale" aria-expanded="false">☰ Menu</button>
    <nav class="nav" id="nav-principale">
{nav}
      <a class="btn btn--primary btn--sm" href="{wa_link('Salve, vorrei informazioni sulle auto disponibili.')}" target="_blank" rel="noopener">WhatsApp</a>
    </nav>
  </div>
</header>
"""


def coda(css_prefix):
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <h4>{e(AZIENDA['nome'])}</h4>
        <p>Vendita auto usate, officina meccanica, elettrauto, noleggio e auto per cerimonie a {e(AZIENDA['citta'])}.</p>
      </div>
      <div>
        <h4>Contatti</h4>
        <p>{e(AZIENDA['indirizzo'])}<br>
        {recapiti_footer()}</p>
      </div>
      <div>
        <h4>Orari</h4>
        <p>{e(AZIENDA['orari'])}</p>
      </div>
      <div>
        <h4>Pagine</h4>
        <p><a href="{css_prefix}catalogo.html">Auto usate</a><br>
        <a href="{css_prefix}noleggio.html">Noleggio</a><br>
        <a href="{css_prefix}servizi.html">Officina ed elettrauto</a><br>
        <a href="{css_prefix}index.html#contatti">Contatti</a><br>
        <a href="{css_prefix}crediti-foto.html">Crediti foto</a></p>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>{("P.IVA " + e(AZIENDA["piva"])) if AZIENDA.get("piva") else ""}</span>
      <span>Sito realizzato da Idea Marketing</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa_link('Salve, vorrei informazioni sulle auto disponibili.')}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">✆</a>
<script src="{css_prefix}assets/auto.js"></script>
</body>
</html>
"""


def card(auto, prefix=""):
    etichetta, classe = STATI[auto["stato"]]
    badges = "" if auto["stato"] == "disponibile" else f'<span class="badge {classe}">{etichetta}</span>'
    if auto.get("neopatentati"):
        badges += '<span class="badge">Neopatentati</span>'

    specs = [km(auto["km"]), immatricolazione(auto), auto["alimentazione"], auto["cambio"]]
    voci = "".join(f"<li>{e(s)}</li>" for s in specs)
    venduta = " auto-card--venduta" if auto["stato"] == "venduta" else ""
    href = f"{prefix}auto/{auto['slug']}.html"

    return f"""      <article class="auto-card{venduta}" data-auto
        data-nome="{e(auto['titolo'])}" data-marca="{e(auto['marca'])}"
        data-allestimento="{e(auto['allestimento'])}" data-prezzo="{auto['prezzo']}"
        data-km="{auto['km']}" data-anno="{anno(auto)}"
        data-alimentazione="{e(auto['alimentazione'])}" data-cambio="{e(auto['cambio'])}"
        data-stato="{auto['stato']}">
        <div class="auto-card__media">
          <a href="{href}"><img src="{foto(auto['slug'], 1, prefix)}" alt="{e(auto['titolo'])}" loading="lazy"></a>
          <div class="auto-card__badges">{badges}</div>
        </div>
        <div class="auto-card__body">
          <h3 class="auto-card__title"><a href="{href}">{e(auto['titolo'])}</a></h3>
          <p class="auto-card__sub">{e(auto['allestimento'])}</p>
          <ul class="specs">{voci}</ul>
          <div class="auto-card__foot">
            <p class="price">{euro(auto['prezzo'])}</p>
            <a class="btn btn--dark btn--sm" href="{href}">Dettagli</a>
          </div>
        </div>
      </article>"""


def filtri(completo, prefix=""):
    marche = sorted({a["marca"] for a in AUTO})
    opzioni_marca = "".join(f'<option value="{e(m)}">{e(m)}</option>' for m in marche)
    prezzi = "".join(f'<option value="{s}">fino a {euro(s)}</option>' for s in (5000, 8000, 10000, 15000, 20000, 30000))
    alimentazioni = "".join(f'<option value="{e(a)}">{e(a)}</option>' for a in
                            ["Benzina", "Diesel", "GPL", "Metano", "Ibrida", "Elettrica"])

    if not completo:
        return f"""    <form class="filters filters--float" method="get" action="{prefix}catalogo.html">
      <div class="filters__grid">
        <div class="field"><label for="q">Marca o modello</label>
          <input type="search" id="q" name="q" placeholder="Es. Panda, Golf, Audi"></div>
        <div class="field"><label for="marca">Marca</label>
          <select id="marca" name="marca"><option value="">Tutte</option>{opzioni_marca}</select></div>
        <div class="field"><label for="prezzo_max">Prezzo massimo</label>
          <select id="prezzo_max" name="prezzo_max"><option value="">Qualsiasi</option>{prezzi}</select></div>
        <div class="field"><label for="alimentazione">Alimentazione</label>
          <select id="alimentazione" name="alimentazione"><option value="">Tutte</option>{alimentazioni}</select></div>
      </div>
      <div class="filters__actions">
        <span class="filters__count">Cerca tra le auto disponibili</span>
        <button type="submit" class="btn btn--primary">Vedi le auto</button>
      </div>
    </form>"""

    km_opzioni = "".join(f'<option value="{s}">fino a {km(s)}</option>' for s in (30000, 60000, 100000, 150000, 200000))
    anni = "".join(f'<option value="{a}">{a}</option>' for a in range(2026, 2005, -1))
    cambi = "".join(f'<option value="{c}">{c}</option>' for c in ["Manuale", "Automatico", "Semiautomatico"])

    return f"""    <form class="filters" data-auto-filtri method="get" action="catalogo.html">
      <div class="filters__grid">
        <div class="field"><label for="q">Marca o modello</label>
          <input type="search" id="q" name="q" placeholder="Es. Panda, Golf, Audi"></div>
        <div class="field"><label for="marca">Marca</label>
          <select id="marca" name="marca"><option value="">Tutte</option>{opzioni_marca}</select></div>
        <div class="field"><label for="prezzo_max">Prezzo massimo</label>
          <select id="prezzo_max" name="prezzo_max"><option value="">Qualsiasi</option>{prezzi}</select></div>
        <div class="field"><label for="alimentazione">Alimentazione</label>
          <select id="alimentazione" name="alimentazione"><option value="">Tutte</option>{alimentazioni}</select></div>
        <div class="field"><label for="cambio">Cambio</label>
          <select id="cambio" name="cambio"><option value="">Tutti</option>{cambi}</select></div>
        <div class="field"><label for="km_max">Km massimi</label>
          <select id="km_max" name="km_max"><option value="">Qualsiasi</option>{km_opzioni}</select></div>
        <div class="field"><label for="anno_min">Dall'anno</label>
          <select id="anno_min" name="anno_min"><option value="">Qualsiasi</option>{anni}</select></div>
        <div class="field"><label for="ordina">Ordina per</label>
          <select id="ordina" name="ordina">
            <option value="">Più recenti</option>
            <option value="prezzo_asc">Prezzo crescente</option>
            <option value="prezzo_desc">Prezzo decrescente</option>
            <option value="km_asc">Meno chilometri</option>
            <option value="anno_desc">Immatricolazione recente</option>
          </select></div>
      </div>
      <div class="filters__actions">
        <p class="filters__count" data-auto-count></p>
        <button type="reset" class="btn btn--ghost btn--sm">Azzera i filtri</button>
      </div>
    </form>"""


# --------------------------------------------------------------------------
# Pagine
# --------------------------------------------------------------------------

def pagina_home():
    evidenza = [a for a in AUTO if a.get("evidenza")][:3]
    cards = "\n".join(card(a) for a in evidenza)
    disponibili = len([a for a in AUTO if a["stato"] != "venduta"])

    destinazione = {"vendita": "catalogo.html", "noleggio": "noleggio.html",
                    "matrimoni": "noleggio.html#cerimonie"}
    blocchi = "\n".join(
        f"""      <a class="card" href="{destinazione.get(s['slug'], 'servizi.html#' + s['slug'])}" style="text-decoration:none">
        <div class="card__icon">{s['icona']}</div>
        <h3>{e(s['titolo'])}</h3>
        <p>{e(s['sommario'])}</p>
      </a>""" for s in SERVIZI
    )
    cerimonie = [n for n in NOLEGGIO if n["categoria"] == "cerimonie"][:2]
    card_cerimonie = "\n".join(card_noleggio(n) for n in cerimonie)

    return testa(
        f"{AZIENDA['nome']} — auto usate, officina, elettrauto e noleggio a {AZIENDA['citta']}",
        f"Vendita auto usate garantite, officina meccanica, elettrauto, noleggio e auto per matrimoni a {AZIENDA['citta']}.",
        "", "Home",
    ) + f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Vendita · Officina · Elettrauto · Noleggio · Cerimonie</p>
    <h1>La tua auto, dall'acquisto al tagliando.</h1>
    <p>Vendiamo auto usate garantite e le teniamo in forma nella nostra officina. E quando ti serve un'auto per qualche giorno — o per il giorno del matrimonio — ce l'abbiamo pronta.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="catalogo.html">Vedi le {disponibili} auto in vendita</a>
      <a class="btn btn--ghost-chiaro" href="servizi.html">Officina ed elettrauto</a>
      <a class="btn btn--wa" href="{wa_link('Salve, vorrei informazioni.')}" target="_blank" rel="noopener">Scrivici su WhatsApp</a>
    </div>
    <div class="hero__stats">
      <div><b>{disponibili}</b><span>auto pronte in salone</span></div>
      <div><b>12 mesi</b><span>di garanzia sulle auto vendute</span></div>
      <div><b>da 29 €</b><span>al giorno per il noleggio</span></div>
    </div>
  </div>
</section>

<div class="wrap">
{filtri(False)}
</div>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">In evidenza</p>
        <h2>Le occasioni della settimana</h2>
        <p>Le auto che il salone mette in primo piano. Cambiano con un clic dalla bacheca.</p>
      </div>
      <a class="btn btn--ghost" href="catalogo.html">Tutte le auto</a>
    </div>
    <div class="auto-grid">
{cards}
    </div>
  </div>
</section>

<section class="section section--surface" id="servizi">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">Servizi</p>
        <h2>Tutto quello che facciamo</h2>
        <p>Officina, elettrauto, vendita, noleggio e cerimonie: un interlocutore unico per la tua auto.</p>
      </div>
      <a class="btn btn--ghost" href="servizi.html">Tutti i servizi</a>
    </div>
    <div class="cards">
{blocchi}
    </div>
  </div>
</section>

<section class="section" id="cerimonie">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">Matrimoni e cerimonie</p>
        <h2>L'auto giusta per il giorno più importante</h2>
        <p>Berline eleganti e auto d'epoca, con autista e addobbo floreale incluso.</p>
      </div>
      <a class="btn btn--ghost" href="noleggio.html#cerimonie">Vedi le auto per cerimonie</a>
    </div>
    <div class="auto-grid">
{card_cerimonie}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Vuoi vendere la tua auto?</h2>
        <p>Mandaci una foto e i chilometri su WhatsApp: ti diamo una valutazione entro 24 ore.</p>
      </div>
      <a class="btn btn--wa" href="{wa_link('Salve, vorrei una valutazione per la mia auto usata.')}" target="_blank" rel="noopener">Chiedi la valutazione</a>
    </div>
  </div>
</section>

<section class="section section--surface" id="contatti">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">Contatti</p>
        <h2>Vieni a trovarci in salone</h2>
        <p>Ti aspettiamo per una prova su strada, senza impegno.</p>
      </div>
    </div>
    <div class="cards">
      <div class="card">
        <div class="card__icon">📍</div>
        <h3>Dove siamo</h3>
        <p>{e(AZIENDA['indirizzo'])}</p>
      </div>
      <div class="card">
        <div class="card__icon">🕘</div>
        <h3>Orari</h3>
        <p>{e(AZIENDA['orari'])}</p>
      </div>
      <div class="card">
        <div class="card__icon">📞</div>
        <h3>Parla con noi</h3>
        <p>{recapiti_footer()}</p>
      </div>
    </div>
  </div>
</section>
""" + coda("")


def pagina_catalogo():
    cards = "\n".join(card(a) for a in AUTO)
    return testa(
        f"Auto usate a {AZIENDA['citta']} — {AZIENDA['nome']}",
        "Tutte le auto usate disponibili: filtra per marca, prezzo, chilometri, alimentazione e cambio.",
        "", "Auto usate",
    ) + f"""
<div class="wrap">
  <p class="breadcrumb"><a href="index.html">Home</a> › Auto usate</p>
  <h1>Auto usate disponibili</h1>
  <p style="color:var(--muted);max-width:60ch;margin-top:-.4em">Filtra e trova l'auto adatta a te. I filtri lavorano subito, senza ricaricare la pagina.</p>
</div>

<div class="wrap" style="margin-top:22px">
{filtri(True)}
</div>

<section class="section" style="padding-top:28px">
  <div class="wrap">
    <div class="auto-grid" data-auto-grid>
{cards}
    </div>
    <p class="empty-state" data-auto-empty hidden style="margin-top:28px">Nessuna auto corrisponde ai filtri scelti. Prova ad allargare la ricerca o scrivici: cerchiamo noi l'auto che ti serve.</p>
  </div>
</section>
""" + coda("")


def pagina_scheda(auto):
    etichetta, classe = STATI[auto["stato"]]
    thumbs = "\n".join(
        f"""          <button type="button" data-gallery-thumb data-full="{foto(auto['slug'], n, '../')}">
            <img src="{foto(auto['slug'], n, '../')}" alt="" loading="lazy">
          </button>""" for n in quante_foto(auto['slug'])
    )

    dati = [
        ("Immatricolazione", immatricolazione(auto)),
        ("Chilometri", km(auto["km"])),
        ("Alimentazione", auto["alimentazione"]),
        ("Cambio", auto["cambio"]),
        ("Carrozzeria", auto["carrozzeria"]),
        ("Potenza", f"{auto['potenza']} CV"),
        ("Cilindrata", f"{auto['cilindrata']:,} cc".replace(",", ".") if auto["cilindrata"] else ""),
        ("Porte", auto["porte"]),
        ("Posti", auto["posti"]),
        ("Colore", auto["colore"]),
        ("Classe ambientale", auto["classe"]),
        ("Garanzia", f"{auto['garanzia']} mesi"),
    ]
    righe = "\n".join(
        f"          <div><dt>{e(et)}</dt><dd>{e(val)}</dd></div>" for et, val in dati if val
    )
    dotazioni = "\n".join(f"          <li>{e(o)}</li>" for o in auto["optional"])
    stato_nota = "Auto già venduta" if auto["stato"] == "venduta" else "Prezzo chiavi in mano, trattabile"
    messaggio_wa = f"Salve, sono interessato a: {auto['titolo']} ({euro(auto['prezzo'])}). È ancora disponibile?"

    return testa(
        f"{auto['titolo']} — {euro(auto['prezzo'])} | {AZIENDA['nome']}",
        f"{auto['titolo']}, {immatricolazione(auto)}, {km(auto['km'])}, {auto['alimentazione']}. {auto['descrizione']}",
        "../", "Auto usate",
    ) + f"""
<div class="wrap">
  <p class="breadcrumb"><a href="../index.html">Home</a> › <a href="../catalogo.html">Auto usate</a> › {e(auto['titolo'])}</p>

  <div class="scheda">
    <div class="scheda__main">
      <div class="gallery" data-gallery>
        <div class="gallery__main">
          <img src="{foto(auto['slug'], 1, '../')}" alt="{e(auto['titolo'])}" data-gallery-main>
          <button type="button" class="gallery__nav gallery__nav--prev" data-gallery-prev aria-label="Foto precedente">‹</button>
          <button type="button" class="gallery__nav gallery__nav--next" data-gallery-next aria-label="Foto successiva">›</button>
        </div>
        <div class="gallery__thumbs">
{thumbs}
        </div>
      </div>

      <div class="scheda__title">
        <h1>{e(auto['titolo'])}</h1>
        <p>{e(auto['marca'])} · {e(auto['allestimento'])}</p>
      </div>

      <dl class="data-grid">
{righe}
      </dl>

      <h2>Descrizione</h2>
      <p>{e(auto['descrizione'])}</p>

      <h2>Dotazioni</h2>
      <ul class="optionals">
{dotazioni}
      </ul>
    </div>

    <aside class="aside-card">
      <p class="price">{euro(auto['prezzo'])}<small>{e(stato_nota)}</small></p>
      {'<p><span class="badge %s">%s</span></p>' % (classe, etichetta) if auto["stato"] != "disponibile" else ''}
      <div class="aside-card__actions">
        <a class="btn btn--wa btn--block" href="{wa_link(messaggio_wa)}" target="_blank" rel="noopener">Scrivi su WhatsApp</a>
        <a class="btn btn--dark btn--block" href="tel:+39{AZIENDA['telefono'].replace(' ', '')}">Chiama {e(AZIENDA['telefono'])}</a>
      </div>
      <p class="aside-card__note">Possibilità di permuta del tuo usato e finanziamento personalizzato.</p>

      <form class="contact-form" data-demo-form>
        <strong>Richiedi informazioni</strong>
        <input type="text" name="nome" placeholder="Nome e cognome" required>
        <input type="tel" name="telefono" placeholder="Telefono" required>
        <input type="email" name="email" placeholder="E-mail (facoltativa)">
        <textarea name="messaggio" placeholder="Vorrei sapere se è ancora disponibile e se posso fare una prova su strada."></textarea>
        <label class="privacy"><input type="checkbox" required>
          <span>Ho letto l'informativa e acconsento al trattamento dei dati per essere ricontattato.</span></label>
        <button type="submit" class="btn btn--primary btn--block">Invia la richiesta</button>
        <p class="aside-card__note" data-demo-esito hidden>Nella demo il modulo non invia nulla: nel sito vero la richiesta arriva per e-mail alla concessionaria.</p>
      </form>
    </aside>
  </div>
</div>

<div class="lightbox" data-lightbox>
  <button type="button" class="lightbox__close" data-lightbox-close aria-label="Chiudi">×</button>
  <button type="button" class="lightbox__nav lightbox__nav--prev" data-lightbox-prev aria-label="Foto precedente">‹</button>
  <button type="button" class="lightbox__nav lightbox__nav--next" data-lightbox-next aria-label="Foto successiva">›</button>
  <img src="" alt="">
</div>

<script>
  document.querySelectorAll('[data-demo-form]').forEach(function (form) {{
    form.addEventListener('submit', function (e) {{
      e.preventDefault();
      form.querySelector('[data-demo-esito]').hidden = false;
    }});
  }});
</script>
""" + coda("../")


def card_noleggio(veicolo):
    """Card di un veicolo a noleggio: il prezzo è a giornata o a cerimonia."""
    badge = '<span class="badge badge--accent">Con autista</span>' if veicolo.get("autista") else ""
    specs = [f"{veicolo['posti']} posti", veicolo["cambio"], veicolo["alimentazione"]]
    if veicolo.get("bagagli") and veicolo["bagagli"] != "—":
        specs.append(veicolo["bagagli"])
    voci = "".join(f"<li>{e(s)}</li>" for s in specs)
    messaggio = f"Salve, vorrei informazioni sul noleggio di: {veicolo['titolo']}."

    return f"""      <article class="auto-card" data-noleggio data-categoria="{veicolo['categoria']}">
        <div class="auto-card__media">
          <img src="{foto(veicolo['slug'], 1, PREFISSO_IMG)}" alt="{e(veicolo['titolo'])}" loading="lazy">
          <div class="auto-card__badges">{badge}</div>
        </div>
        <div class="auto-card__body">
          <h3 class="auto-card__title">{e(veicolo['titolo'])}</h3>
          <p class="auto-card__sub">{e(CATEGORIE_NOLEGGIO.get(veicolo['categoria'], ''))}</p>
          <ul class="specs">{voci}</ul>
          <div class="auto-card__foot">
            <p class="price">{euro(veicolo['prezzo'])}<small>{e(veicolo['prezzo_nota'])}</small></p>
            <a class="btn btn--wa btn--sm" href="{wa_link(messaggio)}" target="_blank" rel="noopener">Disponibilità</a>
          </div>
        </div>
      </article>"""


def pagina_servizi():
    sezioni = []
    for i, s in enumerate(SERVIZI):
        punti = "\n".join(f"          <li>{e(v)}</li>" for v in s["punti"])
        sfondo = ' section--surface' if i % 2 else ''
        sezioni.append(f"""<section class="section{sfondo}" id="{s['slug']}">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">{s['icona']} Servizio</p>
        <h2>{e(s['titolo'])}</h2>
        <p>{e(s['sommario'])}</p>
      </div>
      <a class="btn btn--wa" href="{wa_link(s['cta'])}" target="_blank" rel="noopener">Scrivici su WhatsApp</a>
    </div>
    <ul class="optionals">
{punti}
    </ul>
  </div>
</section>""")

    elenco = "\n".join(sezioni)
    indice = "\n".join(
        f'      <a class="btn btn--ghost-chiaro btn--sm" href="#{s["slug"]}">{s["icona"]} {e(s["titolo"])}</a>'
        for s in SERVIZI
    )

    return testa(
        f"Servizi — officina, elettrauto, noleggio | {AZIENDA['nome']}",
        "Officina meccanica, elettrauto, vendita auto usate, noleggio e auto per matrimoni: tutti i servizi in un'unica officina.",
        "", "Servizi",
    ) + f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">I nostri servizi</p>
    <h1>Un'officina sola, per tutto quello che serve alla tua auto.</h1>
    <p>Meccanica, elettrauto, vendita, noleggio e cerimonie: stesso interlocutore, stessa officina, nessun rimpallo.</p>
    <div class="hero__actions">
{indice}
    </div>
  </div>
</section>

{elenco}

<section class="section">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Prenota un intervento</h2>
        <p>Dicci di che si tratta e ti diamo giorno, ora e preventivo. Se serve, ti diamo l'auto sostitutiva.</p>
      </div>
      <a class="btn btn--wa" href="{wa_link('Salve, vorrei prenotare un intervento in officina.')}" target="_blank" rel="noopener">Scrivici su WhatsApp</a>
    </div>
  </div>
</section>
""" + coda("")


def pagina_noleggio():
    brevi = [n for n in NOLEGGIO if n["categoria"] in ("breve", "furgoni")]
    cerimonie = [n for n in NOLEGGIO if n["categoria"] == "cerimonie"]
    griglia_brevi = "\n".join(card_noleggio(n) for n in brevi)
    griglia_cerimonie = "\n".join(card_noleggio(n) for n in cerimonie)

    incluso_cerimonie = next((n["incluso"] for n in cerimonie), [])
    voci_incluse = "\n".join(f"          <li>{e(v)}</li>" for v in incluso_cerimonie)

    passi = [
        ("1", "Dicci le date", "Scrivici su WhatsApp giorni e tipo di auto che ti serve."),
        ("2", "Ti confermiamo", "Verifichiamo la disponibilità e ti mandiamo il preventivo chiaro, tutto incluso."),
        ("3", "Ritiri l'auto", "Patente, documento e carta: l'auto è pronta, pulita e con il pieno concordato."),
    ]
    blocchi_passi = "\n".join(
        f"""      <div class="card">
        <div class="card__icon">{n}</div>
        <h3>{e(titolo)}</h3>
        <p>{e(testo)}</p>
      </div>""" for n, titolo, testo in passi
    )

    return testa(
        f"Noleggio auto, furgoni e auto per matrimoni | {AZIENDA['nome']}",
        f"Noleggio auto a giornata, furgoni 9 posti e auto con autista per matrimoni e cerimonie a {AZIENDA['citta']}.",
        "", "Noleggio",
    ) + f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Noleggio</p>
    <h1>Un'auto quando ti serve, anche solo per un giorno.</h1>
    <p>Utilitarie, SUV e furgoni da 9 posti a tariffa giornaliera, auto sostitutiva mentre la tua è in officina, e auto con autista per matrimoni e cerimonie.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="#flotta">Vedi la flotta</a>
      <a class="btn btn--ghost-chiaro" href="#cerimonie">Auto per matrimoni</a>
    </div>
  </div>
</section>

<section class="section" id="flotta">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">Flotta</p>
        <h2>Auto e furgoni a noleggio</h2>
        <p>Prezzi indicativi al giorno, assicurazione inclusa. Per più giorni la tariffa scende.</p>
      </div>
    </div>
    <div class="auto-grid">
{griglia_brevi}
    </div>
  </div>
</section>

<section class="section section--surface">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">Come funziona</p>
        <h2>Tre passaggi, nessuna sorpresa</h2>
      </div>
    </div>
    <div class="cards">
{blocchi_passi}
    </div>
    <p style="color:var(--muted);margin-top:22px">Servono patente in corso di validità da almeno un anno, documento d'identità e carta di credito o debito intestata al conducente.</p>
  </div>
</section>

<section class="section" id="cerimonie">
  <div class="wrap">
    <div class="section__head">
      <div>
        <p class="eyebrow">Matrimoni e cerimonie</p>
        <h2>Auto con autista per il giorno del sì</h2>
        <p>Auto lucidata, addobbo floreale e autista in abito scuro. Sopralluogo del percorso prima del giorno.</p>
      </div>
      <a class="btn btn--wa" href="{wa_link('Salve, vorrei informazioni sull auto per il matrimonio.')}" target="_blank" rel="noopener">Chiedi la disponibilità</a>
    </div>
    <div class="auto-grid">
{griglia_cerimonie}
    </div>
    <h3 style="margin-top:34px">Nel servizio è compreso</h3>
    <ul class="optionals">
{voci_incluse}
    </ul>
  </div>
</section>

<section class="section section--surface">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Hai già la data?</h2>
        <p>Le auto per cerimonia si prenotano con anticipo: mandaci la data e te la blocchiamo.</p>
      </div>
      <a class="btn btn--wa" href="{wa_link('Salve, vorrei bloccare la data per l auto della cerimonia.')}" target="_blank" rel="noopener">Blocca la data</a>
    </div>
  </div>
</section>
""" + coda("")


def copia_assets():
    """I fogli di stile restano uno solo: qui vengono copiati dal plugin."""
    origine = RADICE / "plugin" / "concessionaria-auto" / "assets"
    destinazione = DEMO / "assets"
    destinazione.mkdir(parents=True, exist_ok=True)
    for nome in ("auto.css", "auto.js"):
        (destinazione / nome).write_text((origine / nome).read_text(encoding="utf-8"), encoding="utf-8")


def pagina_crediti():
    percorso = IMG / "crediti.json"
    crediti = json.loads(percorso.read_text(encoding="utf-8")) if percorso.exists() else {}
    righe = "\n".join(
        f"""        <tr><td>{e(nome)}</td><td>{e(dato['titolo'])}</td>"""
        f"""<td>{e(dato['autore'])}</td><td>{e(dato['licenza'].upper())}</td>"""
        f"""<td><a href="{e(dato['origine'])}" target="_blank" rel="noopener">originale</a></td></tr>"""
        for nome, dato in sorted(crediti.items())
    )

    return testa(
        f"Crediti fotografici | {AZIENDA['nome']}",
        "Autori e licenze delle foto usate nell'anteprima dimostrativa.",
        "", "",
    ) + f"""
<section class="section">
  <div class="wrap">
    <p class="eyebrow">Anteprima</p>
    <h1>Crediti fotografici</h1>
    <p style="max-width:70ch;color:var(--muted)">Le foto di questa anteprima vengono da archivi con licenza libera
    (Openverse) e servono solo a far vedere l'effetto del sito. Nel sito definitivo vanno sostituite con le foto
    dei veicoli realmente in salone: a quel punto questa pagina non serve più.</p>
    <div style="overflow-x:auto;margin-top:26px">
      <table style="width:100%;border-collapse:collapse;font-size:.92rem">
        <thead><tr style="text-align:left;border-bottom:2px solid var(--line)">
          <th style="padding:10px 12px">File</th><th style="padding:10px 12px">Titolo</th>
          <th style="padding:10px 12px">Autore</th><th style="padding:10px 12px">Licenza</th>
          <th style="padding:10px 12px">Fonte</th>
        </tr></thead>
        <tbody>
{righe}
        </tbody>
      </table>
    </div>
  </div>
</section>
""".replace("<td>", '<td style="padding:9px 12px;border-bottom:1px solid var(--line)">') + coda("")


def main():
    copia_assets()
    scrivi_segnaposto()
    SCHEDE.mkdir(parents=True, exist_ok=True)
    (DEMO / "index.html").write_text(pagina_home(), encoding="utf-8")
    (DEMO / "catalogo.html").write_text(pagina_catalogo(), encoding="utf-8")
    (DEMO / "servizi.html").write_text(pagina_servizi(), encoding="utf-8")
    (DEMO / "noleggio.html").write_text(pagina_noleggio(), encoding="utf-8")
    (DEMO / "crediti-foto.html").write_text(pagina_crediti(), encoding="utf-8")
    for auto in AUTO:
        (SCHEDE / f"{auto['slug']}.html").write_text(pagina_scheda(auto), encoding="utf-8")
    print(f"Demo generata: {len(AUTO)} schede auto, {len(NOLEGGIO)} veicoli a noleggio, "
          f"{len(SERVIZI)} servizi — home, catalogo, servizi, noleggio in {DEMO}")


if __name__ == "__main__":
    main()
