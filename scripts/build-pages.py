# -*- coding: utf-8 -*-
import re, json, os

D = os.path.dirname(os.path.abspath(__file__)) + "/pages"

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF←-⇿⬀-⯿️‍]",
    flags=re.UNICODE)
def de(s):
    s = EMOJI.sub("", s)
    return re.sub(r"[ \t]{2,}", " ", s).replace(" ,", ",").strip()

HEAD = ('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700'
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
#ik-page .hero h1{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:clamp(34px,5vw,58px);line-height:1.08;letter-spacing:-.02em;color:#fff;margin:0 0 18px;max-width:22ch}
#ik-page .hero h1 em{font-style:normal;color:var(--gold)}
#ik-page .hero .lead{font-size:18px;color:rgba(255,255,255,.7);max-width:58ch;line-height:1.6}
#ik-page .hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
#ik-page .hero-img{border-radius:8px;overflow:hidden;border:1px solid rgba(255,255,255,.14);aspect-ratio:4/3;box-shadow:0 20px 50px rgba(0,0,0,.3)}
#ik-page .hero-img img{width:100%;height:100%;object-fit:cover;display:block}
#ik-page .map-embed{display:block;width:100%;height:380px;border:0;filter:grayscale(.2)}
#ik-page .imgband{display:block;width:100%;height:clamp(220px,30vw,360px);object-fit:cover}
#ik-page .cards2{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}
#ik-page .step{background:#fff;border:1px solid var(--rule);border-radius:4px;padding:26px}
#ik-page .step .n{font-family:'Space Grotesk',sans-serif;font-size:34px;color:var(--gold);line-height:1;margin-bottom:10px}
#ik-page .step h3{font-size:17px;font-weight:600;margin:0 0 6px}
#ik-page .step p{color:var(--muted);font-size:14px}
@media (max-width:820px){#ik-page .cards2{grid-template-columns:1fr}}
#ik-page section{padding:64px 0}
#ik-page .alt{background:var(--paper)}
#ik-page .navy{background:var(--navy);color:#fff}
#ik-page h2{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:clamp(26px,3.4vw,40px);line-height:1.15;letter-spacing:-.02em;margin:0 0 12px}
#ik-page h2 em{font-style:normal;color:var(--gold)}
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
#ik-page .stats .n{font-family:'Space Grotesk',sans-serif;font-size:clamp(38px,5vw,52px);color:var(--gold);line-height:1;margin-bottom:8px}
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
#ik-page .founder-grid{display:grid;grid-template-columns:320px 1fr;gap:48px;align-items:center}
#ik-page .founder-photo{aspect-ratio:4/5;border-radius:6px;overflow:hidden;border:1px solid var(--rule)}
#ik-page .founder-photo img{width:100%;height:100%;object-fit:cover;display:block}
#ik-page .founder-photo .ph{width:100%;height:100%;background:repeating-linear-gradient(135deg,#eceae4,#eceae4 10px,#e4e1d9 10px,#e4e1d9 20px);display:flex;align-items:center;justify-content:center;color:#9a978d;font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:600;text-align:center;padding:14px}
#ik-page .sign{font-family:'Space Grotesk',sans-serif;font-size:22px;color:var(--navy);margin-top:18px}
#ik-page .founder-block{max-width:780px;border-left:3px solid var(--gold);padding-left:30px}
#ik-page .founder-block .eyebrow{margin-bottom:12px}
#ik-page .contact-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:44px;align-items:start}
#ik-page .info-row{padding:14px 0;border-bottom:1px solid var(--rule)}
#ik-page .info-row .k{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:4px}
#ik-page .info-row a{font-weight:600}
#ik-page form.ik-form{display:flex;flex-direction:column;gap:14px;max-width:520px}
#ik-page form.ik-form input,#ik-page form.ik-form textarea{padding:.85rem 1rem;border:1px solid var(--rule);border-radius:4px;font-size:15px;font-family:inherit;width:100%;background:#fff}
#ik-page form.ik-form input:focus,#ik-page form.ik-form textarea:focus{outline:2px solid var(--gold);outline-offset:1px;border-color:var(--gold)}
#ik-page form.ik-form button{align-self:flex-start}
@media (max-width:820px){#ik-page .grid2,#ik-page .cards3,#ik-page .contact-grid,#ik-page .founder-grid,#ik-page .hero-grid{grid-template-columns:1fr}#ik-page .stats{grid-template-columns:repeat(2,1fr)}#ik-page .founder-photo{max-width:280px}#ik-page .hero-img{display:none}}
</style>
"""

def wrap(inner):
    return "<!-- wp:html -->\n" + HEAD + CSS + '<div id="ik-page">\n' + inner + "\n</div>\n<!-- /wp:html -->"

def hero(eyebrow, title_html, lead, img=None):
    if img:
        return (f'<section class="hero"><div class="wrap"><div class="hero-grid">'
                f'<div><p class="eyebrow">{eyebrow}</p><h1>{title_html}</h1><p class="lead">{lead}</p></div>'
                f'<div class="hero-img"><img src="{img}" alt="" loading="lazy"></div>'
                f'</div></div></section>')
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
             "Idea Marketing è un'agenzia di comunicazione full-service a Reggio Calabria: dalla strategia alla posa in opera, con un solo interlocutore.",
             img="https://ideamkt.it/wp-content/uploads/2026/08/ik-servizi-2.jpg")
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
usecases = [
 ("Negozi e vetrine","Promozioni e novità sempre aggiornate, anche a serranda abbassata."),
 ("Concessionarie","Mostra modelli, allestimenti e offerte direttamente in showroom."),
 ("Bar e ristoranti","Menu digitali, piatti del giorno e serate in evidenza."),
 ("Palestre e centri","Corsi, orari e promozioni all'ingresso, aggiornati in un attimo."),
 ("Eventi e fiere","Palchi e stand che catturano l'attenzione, anche a noleggio."),
 ("Piazze e spazi pubblici","Comunicazioni e affissioni dinamiche per comuni e attività."),
]
steps = [
 ("01","Sopralluogo e progetto","Veniamo da te, prendiamo le misure e progettiamo la soluzione giusta."),
 ("02","Fornitura e installazione","Consegna, montaggio e configurazione Novastar a regola d'arte."),
 ("03","Assistenza e contenuti","Ti seguiamo con supporto tecnico e aggiornamento dei contenuti."),
]
def stepset(items):
    return "".join('<div class="step"><p class="n">%s</p><h3>%s</h3><p>%s</p></div>' % (n,t,d) for n,t,d in items)
def cardset(items, kd=None):
    out=""
    for i,(t,d) in enumerate(items):
        k = f'<p class="k">{kd}</p>' if kd else ''
        out += f'<div class="card">{k}<h3>{t}</h3><p>{d}</p></div>'
    return out
pills = "".join(f'<span class="pill">{p}</span>' for p in
        ["Pixel pitch P2.5 – P10","Indoor e outdoor","Controllo Novastar","Noleggio Grenke","Installazione e assistenza"])
body = (hero("LEDWALL &amp; Digital Signage","Schermi led che si vedono <em>da lontano</em>.",
             "Schermi LED professionali per negozi, aziende, eventi e spazi pubblici. Disponibili in vendita e in noleggio operativo Grenke.",
             img="https://ideamkt.it/wp-content/uploads/2026/08/ik-ledwall-hero.jpg")
        + f'<section><div class="wrap"><h2>Perché scegliere un LEDWALL?</h2><p class="sec-lead">Uno strumento che lavora per te ogni giorno.</p><div class="cards3">{cardset(why)}</div><div class="pills">{pills}</div></div></section>'
        + f'<section class="alt"><div class="wrap"><h2>I nostri prodotti</h2><p class="sec-lead">La soluzione giusta per ogni ambiente.</p><div class="cards3">{cardset(prod)}</div></div></section>'
        + '<section style="padding:0"><img class="imgband" src="https://ideamkt.it/wp-content/uploads/2026/08/ik-ledwall-tile.jpg" alt="Schermo led installato" loading="lazy"></section>'
        + f'<section><div class="wrap"><h2>Dove si usano</h2><p class="sec-lead">Un LEDWALL lavora ovunque ci sia qualcosa da comunicare.</p><div class="cards3">{cardset(usecases)}</div></div></section>'
        + f'<section class="alt"><div class="wrap"><h2>Come funziona il <em>noleggio</em></h2><p class="sec-lead">Dal primo contatto allo schermo acceso, ti seguiamo noi in ogni passo.</p><div class="cards3">{stepset(steps)}</div></div></section>'
        + f'<section class="navy"><div class="wrap"><h2>Noleggio operativo <em>Grenke</em></h2><p class="sec-lead">Hai il tuo LEDWALL con un canone mensile fisso, senza immobilizzare capitali.</p><div class="cards3">{cardset(grenke)}</div></div></section>'
        + cta("Calcola il tuo <em>ledwall</em>.","Stima il costo e il canone mensile, poi ti diamo un preventivo definitivo.",
              '<a class="btn" href="/preventivi-ledwall/">Calcola il preventivo</a> <a class="btn btn--ghost" href="/contatti/">Contattaci</a>'))
pages[12] = wrap(body)

# ---------------- CHI SIAMO (14) ----------------
distintivo = [
 ("Un unico partner","Grafica, stampa, digitale, social, web e comunicazione visiva coordinati attraverso un unico interlocutore."),
 ("Soluzioni su misura","Ogni attività è diversa: costruiamo la soluzione sulle reali esigenze del cliente, senza pacchetti standard."),
 ("Esperienza e innovazione","Esperienza sul territorio e ricerca continua di nuove tecnologie, strumenti e soluzioni di comunicazione."),
 ("Rapporto diretto","Seguiamo il cliente prima, durante e dopo la realizzazione del progetto, con un contatto semplice e diretto."),
]
dist_html = "".join('<div class="card"><h3>%s</h3><p>%s</p></div>' % (t,d) for t,d in distintivo)
stats = [("15+","anni di esperienza"),("200+","clienti che ci hanno scelto"),("500+","progetti realizzati"),("1","un solo partner per la tua comunicazione")]
stat_html = "".join(f'<div><p class="n">{n}</p><p class="l">{l}</p></div>' for n,l in stats)
body = (hero("Chi siamo","Idee e soluzioni che fanno crescere la tua <em>attività</em>.",
             "Idea Marketing è un'agenzia di comunicazione con sede a Reggio Calabria, fondata e guidata da Fortunato Coppola. Da oltre 15 anni trasformiamo idee ed esigenze in progetti concreti.",
             img="https://ideamkt.it/wp-content/uploads/2026/08/ik-chisiamo-2.jpg")
        + '<section><div class="wrap" style="max-width:820px"><h2>Il nostro modo di lavorare</h2>'
          '<p class="lead-p">Non ci interessa semplicemente realizzare qualcosa di bello.</p>'
          "<p class=\"body-p\">Prima ascoltiamo il cliente, capiamo cosa vuole ottenere e poi troviamo la soluzione più adatta per comunicarlo nel modo giusto. Uniamo creatività, esperienza, tecnologia e produzione, seguendo il progetto dall'idea iniziale fino alla realizzazione finale.</p>"
          '<p class="body-p">Dalla grafica alla stampa, dalla comunicazione digitale ai social, dai siti web ai LEDwall e alla pubblicità visiva: un unico punto di riferimento per tutta la tua comunicazione.</p></div></section>'
        + '<section class="alt"><div class="wrap founder-block">'
          '<p class="eyebrow">Il fondatore</p><h2>Fortunato Coppola</h2>'
          '<p class="lead-p">Ho fondato Idea Marketing partendo da un principio semplice: un imprenditore dovrebbe poter trovare in un unico partner tutto ciò che serve per comunicare e promuovere bene la propria attività.</p>'
          '<p class="body-p">Per questo negli anni abbiamo ampliato continuamente servizi, competenze e tecnologie. Seguo personalmente i progetti e il rapporto con i clienti, dalla prima idea alla realizzazione. Credo nel rapporto diretto, nella disponibilità e soprattutto nel mantenere gli impegni presi. Ogni cliente per noi non è un numero, ma un progetto da far crescere.</p>'
          '<p class="sign">Fortunato Coppola</p>'
          '</div></section>'
        + f'<section><div class="wrap"><h2>Cosa ci distingue</h2><p class="sec-lead">Quattro cose su cui non transigiamo.</p><div class="cards2">{dist_html}</div></div></section>'
        + f'<section class="navy"><div class="wrap"><h2>I numeri di <em>Idea Marketing</em></h2><div class="stats" style="margin-top:26px">{stat_html}</div></div></section>'
        + cta("Hai un progetto in <em>mente</em>?", "Rinnovare l'immagine, una campagna o partire da zero: raccontaci cosa vuoi realizzare e troviamo insieme la soluzione.",
              '<a class="btn" href="/contatti/">Richiedi un preventivo</a>'))
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
          f'<div><h2>Dove siamo</h2><div style="margin-top:8px">{info}</div></div></div></div></section>'
        + '<section style="padding:0"><iframe class="map-embed" title="Idea Marketing — Via Campoli 34, Reggio Calabria" '
          'src="https://www.google.com/maps?q=Via+Campoli+34,+89134+Reggio+Calabria&output=embed" '
          'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>')
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
