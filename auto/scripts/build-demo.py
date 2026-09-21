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
    for i, auto in enumerate(AUTO):
        tinta = TINTE[i % len(TINTE)]
        for n, vista in enumerate(VISTE, start=1):
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

def testa(titolo, descrizione, css_prefix, attiva):
    voci = [("Home", "index.html"), ("Auto usate", "catalogo.html"),
            ("Servizi", "index.html#servizi"), ("Contatti", "index.html#contatti")]
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_prefix}../plugin/concessionaria-auto/assets/auto.css">
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
      <span class="brand__mark">AU</span>
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
        <p>Vendita auto usate garantite a {e(AZIENDA['citta'])}. Permute, finanziamenti e assistenza dopo la vendita.</p>
      </div>
      <div>
        <h4>Contatti</h4>
        <p>{e(AZIENDA['indirizzo'])}<br>
        <a href="tel:+39{AZIENDA['telefono'].replace(' ', '')}">{e(AZIENDA['telefono'])}</a><br>
        <a href="mailto:{e(AZIENDA['email'])}">{e(AZIENDA['email'])}</a></p>
      </div>
      <div>
        <h4>Orari</h4>
        <p>{e(AZIENDA['orari'])}</p>
      </div>
      <div>
        <h4>Pagine</h4>
        <p><a href="{css_prefix}catalogo.html">Auto usate</a><br>
        <a href="{css_prefix}index.html#servizi">Servizi</a><br>
        <a href="{css_prefix}index.html#contatti">Contatti</a></p>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>P.IVA {e(AZIENDA['piva'])}</span>
      <span>Sito realizzato da Idea Marketing</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa_link('Salve, vorrei informazioni sulle auto disponibili.')}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">✆</a>
<script src="{css_prefix}../plugin/concessionaria-auto/assets/auto.js"></script>
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
          <a href="{href}"><img src="{prefix}img/{auto['slug']}-1.svg" alt="{e(auto['titolo'])}" loading="lazy"></a>
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

    servizi = [
        ("🔧", "Garanzia 12 mesi", "Ogni auto è controllata in officina e consegnata con garanzia e tagliando fatto."),
        ("🔁", "Ritiro e permuta", "Valutiamo la tua auto usata e la scaliamo dal prezzo di quella nuova."),
        ("💳", "Finanziamento su misura", "Rate personalizzate con pratica approvata in giornata, anche senza anticipo."),
        ("📄", "Passaggio di proprietà", "Ci occupiamo noi di tutte le pratiche: tu ritiri l'auto già intestata."),
    ]
    blocchi = "\n".join(
        f"""      <div class="card">
        <div class="card__icon">{icona}</div>
        <h3>{e(titolo)}</h3>
        <p>{e(testo)}</p>
      </div>""" for icona, titolo, testo in servizi
    )

    return testa(
        f"{AZIENDA['nome']} — auto usate garantite a {AZIENDA['citta']}",
        f"Auto usate selezionate e garantite a {AZIENDA['citta']}: permute, finanziamenti e passaggio di proprietà inclusi.",
        "", "Home",
    ) + f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Auto usate garantite · {e(AZIENDA['citta'])}</p>
    <h1>L'auto giusta, controllata e pronta da guidare.</h1>
    <p>Ogni veicolo passa da un controllo di 60 punti prima di entrare in salone. Permuta il tuo usato, scegli la rata e ritira l'auto già intestata.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="catalogo.html">Vedi le {disponibili} auto disponibili</a>
      <a class="btn btn--wa" href="{wa_link('Salve, vorrei informazioni sulle auto disponibili.')}" target="_blank" rel="noopener">Scrivici su WhatsApp</a>
    </div>
    <div class="hero__stats">
      <div><b>{disponibili}</b><span>auto pronte in salone</span></div>
      <div><b>12 mesi</b><span>di garanzia inclusa</span></div>
      <div><b>24h</b><span>per la risposta al finanziamento</span></div>
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
        <h2>Non vendiamo solo l'auto</h2>
        <p>Dalla valutazione dell'usato al passaggio di proprietà: un interlocutore unico.</p>
      </div>
    </div>
    <div class="cards">
{blocchi}
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
        <p><a href="tel:+39{AZIENDA['telefono'].replace(' ', '')}">{e(AZIENDA['telefono'])}</a><br>
        <a href="mailto:{e(AZIENDA['email'])}">{e(AZIENDA['email'])}</a></p>
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
        f"""          <button type="button" data-gallery-thumb data-full="../img/{auto['slug']}-{n}.svg">
            <img src="../img/{auto['slug']}-{n}.svg" alt="" loading="lazy">
          </button>""" for n in (1, 2, 3)
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
          <img src="../img/{auto['slug']}-1.svg" alt="{e(auto['titolo'])}" data-gallery-main>
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


def main():
    scrivi_segnaposto()
    SCHEDE.mkdir(parents=True, exist_ok=True)
    (DEMO / "index.html").write_text(pagina_home(), encoding="utf-8")
    (DEMO / "catalogo.html").write_text(pagina_catalogo(), encoding="utf-8")
    for auto in AUTO:
        (SCHEDE / f"{auto['slug']}.html").write_text(pagina_scheda(auto), encoding="utf-8")
    print(f"Demo generata: {len(AUTO)} schede + home + catalogo in {DEMO}")


if __name__ == "__main__":
    main()
