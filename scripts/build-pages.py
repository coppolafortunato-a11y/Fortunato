# -*- coding: utf-8 -*-
import re, json, os

D = os.path.dirname(os.path.abspath(__file__)) + "/pages"

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF←-⇿⬀-⯿️‍]",
    flags=re.UNICODE)
def de(s):
    s = EMOJI.sub("", s)
    return re.sub(r"[ \t]{2,}", " ", s).replace(" ,", ",").strip()

HEAD = ('<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
        '&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">\n')

CSS = """<style>
#ik-page{--navy:#1E2235;--gold:#C9A961;--paper:#f8f7f4;--rule:#e0ddd6;--muted:#6b6b73;font-family:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1E2235;line-height:1.6;width:100vw;max-width:100vw;margin-left:calc(50% - 50vw);overflow-x:hidden}
#ik-page *{box-sizing:border-box}
#ik-page p{margin:0}
#ik-page a{color:inherit;text-decoration:none}
#ik-page .wrap{max-width:1100px;margin:0 auto;padding:0 24px}
#ik-page .hero{background:var(--navy);color:#fff;position:relative;overflow:hidden}
#ik-page .hero::after{content:'';position:absolute;right:-140px;top:-140px;width:420px;height:420px;border:1px solid rgba(201,169,97,.16);border-radius:50%}
#ik-page .hero .wrap{padding:74px 24px;position:relative;z-index:1}
#ik-page .eyebrow{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:18px}
#ik-page .hero h1{font-family:'Instrument Serif',serif;font-weight:400;font-size:clamp(34px,5vw,58px);line-height:1.08;letter-spacing:-.02em;color:#fff;margin:0 0 18px;max-width:22ch}
#ik-page .hero h1 em{font-style:italic;color:var(--gold)}
#ik-page .hero .lead{font-size:18px;color:rgba(255,255,255,.7);max-width:58ch;line-height:1.6}
#ik-page section{padding:64px 0}
#ik-page .alt{background:var(--paper)}
#ik-page .navy{background:var(--navy);color:#fff}
#ik-page h2{font-family:'Instrument Serif',serif;font-weight:400;font-size:clamp(26px,3.4vw,40px);line-height:1.15;letter-spacing:-.02em;margin:0 0 12px}
#ik-page h2 em{font-style:italic;color:var(--gold)}
#ik-page .navy h2{color:#fff}
#ik-page .sec-lead{color:var(--muted);font-size:16px;max-width:62ch;margin-bottom:38px}
#ik-page .navy .sec-lead{color:rgba(255,255,255,.7)}
#ik-page .grid2{display:grid;grid-template-columns:repeat(2,1fr);border-top:1px solid var(--rule);border-left:1px solid var(--rule)}
#ik-page .svc{border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:30px 28px;background:#fff;transition:background .2s}
#ik-page .svc:hover{background:var(--paper)}
#ik-page .svc .num{font-size:13px;font-weight:700;letter-spacing:.1em;color:var(--gold);margin-bottom:16px}
#ik-page .svc h3{font-size:18px;font-weight:600;margin:0 0 8px;letter-spacing:-.01em}
#ik-page .svc>p{color:var(--muted);font-size:14px;margin-bottom:12px}
#ik-page .svc ul{margin:0;padding-left:18px;color:var(--muted);font-size:14px;line-height:1.75}
#ik-page .cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
#ik-page .card{background:#fff;border:1px solid var(--rule);border-radius:4px;padding:28px}
#ik-page .navy .card{background:#262b42;border-color:rgba(255,255,255,.12)}
#ik-page .card .k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:10px}
#ik-page .card h3{font-size:18px;font-weight:600;margin:0 0 8px}
#ik-page .navy .card h3{color:#fff}
#ik-page .card p{color:var(--muted);font-size:14px}
#ik-page .navy .card p{color:rgba(255,255,255,.68)}
#ik-page .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
#ik-page .stats .n{font-family:'Instrument Serif',serif;font-size:clamp(38px,5vw,52px);color:var(--gold);line-height:1;margin-bottom:8px}
#ik-page .stats .l{font-size:14px;color:var(--muted);font-weight:600}
#ik-page .btn{display:inline-flex;align-items:center;gap:9px;font-size:14px;font-weight:600;padding:13px 24px;border-radius:3px;background:var(--gold);color:#33270a;transition:transform .18s,background .2s;border:none;cursor:pointer}
#ik-page .btn:hover{background:#d8ba73;transform:translateY(-2px)}
#ik-page .btn--ghost{background:transparent;border:1px solid rgba(255,255,255,.45);color:#fff}
#ik-page .btn--ghost:hover{background:rgba(255,255,255,.08)}
#ik-page .pills{display:flex;flex-wrap:wrap;gap:9px;margin-top:24px}
#ik-page .pill{border:1px solid rgba(201,169,97,.42);color:var(--gold);font-size:12.5px;font-weight:600;padding:7px 14px;border-radius:100px}
#ik-page .navy .pill{color:var(--gold)}
#ik-page .actions{display:flex;gap:14px;flex-wrap:wrap;margin-top:30px}
#ik-page .lead-p{font-size:18px;color:#3a3d4d;max-width:64ch;margin-bottom:16px}
#ik-page .body-p{color:var(--muted);max-width:64ch;margin-bottom:14px}
#ik-page .contact-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:44px;align-items:start}
#ik-page .info-row{padding:14px 0;border-bottom:1px solid var(--rule)}
#ik-page .info-row .k{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:4px}
#ik-page .info-row a{font-weight:600}
#ik-page form.ik-form{display:flex;flex-direction:column;gap:14px;max-width:520px}
#ik-page form.ik-form input,#ik-page form.ik-form textarea{padding:.85rem 1rem;border:1px solid var(--rule);border-radius:4px;font-size:15px;font-family:inherit;width:100%;background:#fff}
#ik-page form.ik-form input:focus,#ik-page form.ik-form textarea:focus{outline:2px solid var(--gold);outline-offset:1px;border-color:var(--gold)}
#ik-page form.ik-form button{align-self:flex-start}
@media (max-width:820px){#ik-page .grid2,#ik-page .cards3,#ik-page .contact-grid{grid-template-columns:1fr}#ik-page .stats{grid-template-columns:repeat(2,1fr)}}
</style>
"""

def wrap(inner):
    return "<!-- wp:html -->\n" + HEAD + CSS + '<div id="ik-page">\n' + inner + "\n</div>\n<!-- /wp:html -->"

def hero(eyebrow, title_html, lead):
    return (f'<section class="hero"><div class="wrap">'
            f'<p class="eyebrow">{eyebrow}</p><h1>{title_html}</h1>'
            f'<p class="lead">{lead}</p></div></section>')

def cta(title_html, sub, btns):
    return (f'<section class="navy cta"><div class="wrap" style="text-align:center">'
            f'<h2>{title_html}</h2><p class="sec-lead" style="margin:12px auto 26px">{sub}</p>'
            f'<div class="actions" style="justify-content:center">{btns}</div></div></section>')

pages = {}

# ---------------- SERVIZI (10) ----------------
svc = [
 ("01","Marketing Strategico","Analisi del mercato, posizionamento, pianificazione e misurazione dei risultati.",
  ["Analisi di mercato e competitor","Target e buyer personas","Piano marketing annuale","KPI e misurazione","Consulenza continuativa"]),
 ("02","Digital Marketing","La tua presenza online a 360°: social, campagne, SEO e lead generation.",
  ["Social media (Facebook, Instagram, LinkedIn, TikTok)","Google Ads e Meta Ads","SEO e ottimizzazione","Email marketing e newsletter","Lead generation e funnel"]),
 ("03","Web &amp; E-commerce","Siti, e-commerce e landing page ad alta conversione, ottimizzati per mobile.",
  ["Siti web aziendali e portfolio","E-commerce WooCommerce e Shopify","Landing page e funnel di vendita","Ottimizzazione velocità e UX","Manutenzione e aggiornamento"]),
 ("04","Branding &amp; Identità Visiva","Costruiamo la tua identità di marca da zero o rinnoviamo quella esistente.",
  ["Naming e brand positioning","Logo design e declinazioni","Brand guidelines","Palette colori e tipografia","Restyling e rebranding"]),
 ("05","Grafica &amp; Stampa","Dalla progettazione grafica alla stampa professionale.",
  ["Biglietti da visita e carta intestata","Brochure, flyer e locandine","Roll-up, totem e striscioni","Packaging ed etichette","Gadget personalizzati"]),
 ("06","Fotografia &amp; Video","Contenuti visivi professionali per il tuo brand.",
  ["Shooting aziendali e di prodotto","Video istituzionali e presentazioni","Reel e video per social","Riprese con drone"]),
 ("07","LEDWALL &amp; Segnaletica","Soluzioni di digital signage per negozi, eventi, aziende e spazi pubblici.",
  ["Schermi LED indoor e outdoor","Totem digitali","Noleggio operativo Grenke","Installazione e assistenza"]),
]
cards = ""
for n,t,d,items in svc:
    li = "".join(f"<li>{i}</li>" for i in items)
    cards += f'<div class="svc"><p class="num">{n}</p><h3>{t}</h3><p>{d}</p><ul>{li}</ul></div>'
body = (hero("Servizi","Tutto quello che serve alla tua <em>comunicazione</em>.",
             "Idea Marketing è un'agenzia di comunicazione full-service a Reggio Calabria: dalla strategia alla posa in opera, con un solo interlocutore.")
        + f'<section class="alt"><div class="wrap"><div class="grid2">{cards}</div></div></section>'
        + cta("Raccontaci il progetto, ti diamo <em>un prezzo</em>.","Preventivo gratuito, di solito entro 24 ore.",
              '<a class="btn" href="/contatti/">Richiedi un preventivo</a>'))
pages[10] = wrap(body)

# ---------------- LEDWALL (12) ----------------
why = [
 ("Massima visibilità","Attira l'attenzione di clienti e passanti con immagini e video di alta qualità, giorno e notte."),
 ("Contenuti dinamici","Aggiorni in tempo reale: promozioni, eventi, orari e messaggi personalizzati."),
 ("100% deducibile","Con il noleggio operativo Grenke, canone mensile fisso completamente deducibile."),
]
prod = [
 ("LED Indoor · P2.5–P4","Alta risoluzione per negozi, showroom, reception e ambienti interni. Colori brillanti e dettagli nitidi."),
 ("LED Outdoor · P4–P10","Resistenti alle intemperie, alta luminosità per visibilità anche sotto il sole diretto."),
 ("Totem Digitali","Display verticali autoportanti per centri commerciali, hotel, ristoranti e punti vendita."),
]
grenke = [
 ("Nessun anticipo","Paghi solo il canone mensile, senza immobilizzare capitali."),
 ("100% deducibile","Costo aziendale completamente deducibile."),
 ("Assistenza inclusa","Installazione, configurazione e supporto tecnico."),
]
def cardset(items, kd=None):
    out=""
    for i,(t,d) in enumerate(items):
        k = f'<p class="k">{kd}</p>' if kd else ''
        out += f'<div class="card">{k}<h3>{t}</h3><p>{d}</p></div>'
    return out
pills = "".join(f'<span class="pill">{p}</span>' for p in
        ["Pixel pitch P2.5 – P10","Indoor e outdoor","Controllo Novastar","Noleggio Grenke","Installazione e assistenza"])
body = (hero("LEDWALL &amp; Digital Signage","Schermi led che si vedono <em>da lontano</em>.",
             "Schermi LED professionali per negozi, aziende, eventi e spazi pubblici. Disponibili in vendita e in noleggio operativo Grenke.")
        + f'<section><div class="wrap"><h2>Perché scegliere un LEDWALL?</h2><p class="sec-lead">Uno strumento che lavora per te ogni giorno.</p><div class="cards3">{cardset(why)}</div><div class="pills">{pills}</div></div></section>'
        + f'<section class="alt"><div class="wrap"><h2>I nostri prodotti</h2><p class="sec-lead">La soluzione giusta per ogni ambiente.</p><div class="cards3">{cardset(prod)}</div></div></section>'
        + f'<section class="navy"><div class="wrap"><h2>Noleggio operativo <em>Grenke</em></h2><p class="sec-lead">Hai il tuo LEDWALL con un canone mensile fisso, senza immobilizzare capitali.</p><div class="cards3">{cardset(grenke)}</div></div></section>'
        + cta("Calcola il tuo <em>ledwall</em>.","Stima il costo e il canone mensile, poi ti diamo un preventivo definitivo.",
              '<a class="btn" href="/preventivi-ledwall/">Calcola il preventivo</a> <a class="btn btn--ghost" href="/contatti/">Contattaci</a>'))
pages[12] = wrap(body)

# ---------------- CHI SIAMO (14) ----------------
valori = [
 ("Risultati concreti","Ogni progetto è misurato sui risultati. Non ci accontentiamo del “bello”: vogliamo che funzioni."),
 ("Partnership vera","Non siamo un fornitore, siamo un partner. Il tuo successo è il nostro successo."),
 ("Innovazione continua","Investiamo costantemente nella formazione e nelle tecnologie più recenti."),
]
stats = [("15+","Anni di esperienza"),("200+","Clienti soddisfatti"),("500+","Progetti completati"),("8","Aree di servizio")]
stat_html = "".join(f'<div><p class="n">{n}</p><p class="l">{l}</p></div>' for n,l in stats)
body = (hero("Chi siamo","Un partner per la tua <em>crescita</em>.",
             "Idea Marketing è un'agenzia di comunicazione full-service con sede a Reggio Calabria, fondata e guidata da Fortunato Coppola.")
        + '<section><div class="wrap" style="max-width:820px"><h2>La nostra missione</h2>'
          '<p class="lead-p">Crediamo che ogni azienda meriti una comunicazione professionale ed efficace.</p>'
          '<p class="body-p">La nostra missione è rendere accessibile il marketing strategico alle imprese del Sud Italia, aiutandole a crescere, competere e affermarsi sul mercato. Affianchiamo imprenditori, professionisti e aziende del territorio calabrese e non solo, con soluzioni integrate di marketing, comunicazione e digital transformation.</p></div></section>'
        + f'<section class="alt"><div class="wrap"><h2>I nostri valori</h2><p class="sec-lead">Come lavoriamo, ogni giorno.</p><div class="cards3">{cardset(valori)}</div></div></section>'
        + f'<section class="navy"><div class="wrap"><h2>I numeri di <em>Idea Marketing</em></h2><div class="stats" style="margin-top:26px">{stat_html}</div></div></section>'
        + cta("Vuoi lavorare con <em>noi</em>?","Raccontaci il tuo progetto: ti rispondiamo di solito entro 24 ore.",
              '<a class="btn" href="/contatti/">Lavora con noi</a>'))
pages[14] = wrap(body)

# ---------------- CONTATTI (16) ----------------
form = ('<form class="ik-form" action="mailto:coppola.fortunato@gmail.com" method="post" enctype="text/plain">'
        '<input type="text" name="nome" placeholder="Il tuo nome *" required>'
        '<input type="email" name="email" placeholder="La tua email *" required>'
        '<input type="tel" name="telefono" placeholder="Telefono">'
        '<input type="text" name="oggetto" placeholder="Oggetto">'
        '<textarea name="messaggio" placeholder="Il tuo messaggio *" rows="5" required></textarea>'
        '<button type="submit" class="btn">Invia messaggio</button></form>')
info = (
 '<div class="info-row"><p class="k">Indirizzo</p><p>Via Campoli 34<br>89134 Reggio Calabria (RC)</p></div>'
 '<div class="info-row"><p class="k">Telefono</p><p><a href="tel:+393206116711">320 611 6711</a></p></div>'
 '<div class="info-row"><p class="k">Email</p><p><a href="mailto:coppola.fortunato@gmail.com">coppola.fortunato@gmail.com</a></p></div>'
 '<div class="info-row"><p class="k">PEC</p><p><a href="mailto:coppola.fortunato@pec.it">coppola.fortunato@pec.it</a></p></div>'
 '<div class="info-row"><p class="k">Orari</p><p>Lunedì – Venerdì: 9:00 – 18:00<br>Sabato: 9:00 – 13:00</p></div>'
 '<div class="info-row" style="border-bottom:none"><p class="k">Dati aziendali</p><p>Idea Marketing di Coppola Fortunato<br>P.IVA 02520960804 · C.F. CPPFTN88L05H224S · SDI SU9YNJA</p></div>'
)
body = (hero("Contatti","Parliamo del tuo <em>progetto</em>.",
             "Hai un'idea o vuoi un preventivo? Scrivici o chiamaci: rispondiamo di solito entro 24 ore.")
        + f'<section><div class="wrap"><div class="contact-grid"><div><h2>Scrivici</h2><p class="sec-lead">Compila il modulo, ti ricontattiamo noi.</p>{form}</div>'
          f'<div><h2>Dove siamo</h2><div style="margin-top:8px">{info}</div></div></div></div></section>')
pages[16] = wrap(body)

# ---------------- PREVENTIVI LEDWALL (27) — preserva calcolatore ----------------
raw27 = open(f"{D}/page-27.html", encoding="utf-8").read()
m = re.search(r"<!-- wp:html -->(.*?)<!-- /wp:html -->", raw27, flags=re.S)
calc = de(m.group(1).strip())  # calcolatore (style+html+js) senza emoji
body = (hero("Preventivi LEDWALL","Calcola il tuo <em>ledwall</em> in un minuto.",
             "Stima subito il costo del tuo LEDWALL e il canone mensile con noleggio operativo Grenke. Poi ti diamo un preventivo definitivo.")
        + f'<section class="alt"><div class="wrap">{calc}</div></section>')
pages[27] = wrap(body)

# ---- scrivi payload e report ----
for pid, content in pages.items():
    content = de(content) if pid != 27 else content  # 27 già de-emojizzata sul calc; de-emojizza hero
    if pid == 27:
        content = EMOJI.sub("", content)
    json.dump({"content": content}, open(f"{D}/new-{pid}.json","w"), ensure_ascii=False)
    has_emoji = bool(EMOJI.search(content))
    print(f"pagina {pid}: {len(content)} byte | emoji residue: {has_emoji}")
