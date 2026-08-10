# -*- coding: utf-8 -*-
import json
SC = "/tmp/claude-0/-home-user-Fortunato/caa1bb9f-37fa-587f-bedd-c11b09576fba/scratchpad/"
media = json.load(open(SC + "lavori_media_map.json"))

ORDER = ["LEDwall", "Insegne", "Menu", "Etichette", "Stampa"]
LABEL = {"LEDwall": "LEDwall", "Insegne": "Insegne &amp; Vetrine", "Menu": "Menu",
         "Etichette": "Etichette &amp; Packaging", "Stampa": "Stampa &amp; Allestimenti"}
by_cat = {c: [] for c in ORDER}
for m in media:
    by_cat.setdefault(m["category"], []).append(m)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

CSS = """<style id="ik-lavori-css">
#ik-lavori{--navy:#1E2235;--gold:#C9A961;--paper:#f8f7f4;--ink:#20232f;--line:#e7e3da;font-family:'Inter',system-ui,-apple-system,sans-serif;color:var(--ink);background:var(--paper)}
#ik-lavori *{box-sizing:border-box}
#ik-lavori h1,#ik-lavori h2{font-family:'Archivo','Inter',sans-serif;font-style:normal;font-weight:700}
#ik-lavori em,#ik-lavori i,#ik-lavori cite{font-style:normal}
#ik-lavori .wrap{max-width:1180px;margin:0 auto;padding:0 24px}
#ik-lavori .hero{background:var(--navy);color:#fff;padding:66px 0 60px;text-align:center}
#ik-lavori .hero .eyebrow{color:var(--gold);font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:13px;margin:0 0 14px}
#ik-lavori .hero h1{font-size:44px;line-height:1.08;margin:0 0 16px}
#ik-lavori .hero p{max-width:640px;margin:0 auto;color:#c7cbd8;font-size:17px;line-height:1.6}
#ik-lavori .tabradio{position:absolute;opacity:0;pointer-events:none;width:0;height:0}
#ik-lavori .tabs{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:-28px auto 34px;position:relative;z-index:2}
#ik-lavori .tab{cursor:pointer;background:#fff;border:1px solid var(--line);border-radius:40px;padding:11px 20px;font-weight:600;font-size:15px;color:var(--ink);box-shadow:0 6px 18px rgba(20,24,40,.06);transition:.15s;display:inline-flex;align-items:center;gap:8px}
#ik-lavori .tab:hover{border-color:var(--gold)}
#ik-lavori .tab .n{background:var(--paper);color:#8a8676;font-size:12px;font-weight:700;border-radius:20px;padding:2px 8px}
#ik-lavori .panel{display:none;padding-bottom:46px}
#ik-lavori .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
#ik-lavori figure.card{margin:0;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;box-shadow:0 8px 24px rgba(20,24,40,.06);transition:.18s}
#ik-lavori figure.card:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(20,24,40,.12)}
#ik-lavori .card .im{aspect-ratio:4/3;overflow:hidden;background:#f0eee9}
#ik-lavori .card .im img{width:100%;height:100%;object-fit:cover;display:block}
#ik-lavori .card figcaption{padding:14px 16px}
#ik-lavori .card figcaption strong{display:block;font-family:'Archivo','Inter',sans-serif;font-size:16px;color:var(--navy)}
#ik-lavori .card figcaption span{display:block;color:#8a8676;font-size:13px;margin-top:2px}
#ik-lavori .cta{background:var(--navy);color:#fff;text-align:center;padding:54px 24px 58px}
#ik-lavori .cta h2{font-size:30px;margin:0 0 10px}
#ik-lavori .cta p{color:#c7cbd8;margin:0 0 24px;font-size:16px}
#ik-lavori .cta a{display:inline-flex;align-items:center;gap:9px;background:var(--gold);color:#1E2235;font-weight:600;text-decoration:none;padding:15px 30px;border-radius:5px;font-size:16px}
#ik-lavori .cta a:hover{background:#d8ba73}
__RULES__
@media(max-width:820px){#ik-lavori .grid{grid-template-columns:repeat(2,1fr)}#ik-lavori .hero h1{font-size:32px}}
@media(max-width:520px){#ik-lavori .grid{grid-template-columns:1fr}}
</style>"""

rules = ""
for c in ORDER:
    lc = c.lower()
    rules += "#ik-lavori #cat-%s:checked~.tabs .tab-%s{background:var(--navy);color:#fff;border-color:var(--navy)}\n" % (lc, lc)
    rules += "#ik-lavori #cat-%s:checked~.panels .panel-%s{display:block}\n" % (lc, lc)
CSS = CSS.replace("__RULES__", rules)

radios = ""
for i, c in enumerate(ORDER):
    chk = " checked" if i == 0 else ""
    radios += '<input type="radio" name="ikcat" id="cat-%s" class="tabradio"%s>' % (c.lower(), chk)

tabs = '<div class="tabs">'
for c in ORDER:
    tabs += '<label for="cat-%s" class="tab tab-%s">%s <span class="n">%d</span></label>' % (
        c.lower(), c.lower(), LABEL[c], len(by_cat[c]))
tabs += '</div>'

panels = '<div class="panels wrap">'
for c in ORDER:
    panels += '<section class="panel panel-%s"><div class="grid">' % c.lower()
    for m in by_cat[c]:
        panels += ('<figure class="card"><div class="im"><img loading="lazy" src="%s" alt="%s" width="%d" height="%d"></div>'
                   '<figcaption><strong>%s</strong><span>%s</span></figcaption></figure>') % (
            m["url"], esc(m["client"] + " - " + m["title"]),
            1400, 1050, esc(m["client"]), esc(m["title"]))
    panels += '</div></section>'
panels += '</div>'

wa = "https://wa.me/393206116711?text=Ciao%20Idea%20Marketing%2C%20ho%20visto%20i%20vostri%20lavori%20e%20vorrei%20un%20preventivo."
cta = ('<div class="cta"><h2>Ti piace quello che facciamo?</h2>'
       '<p>Raccontaci la tua idea: ti diamo un preventivo senza impegno.</p>'
       '<a href="/contatti/">Richiedi un preventivo</a></div>')

hero = ('<section class="hero"><div class="wrap">'
        '<p class="eyebrow">Portfolio</p>'
        '<h1>I nostri lavori</h1>'
        '<p>Una selezione di progetti realizzati per le attivit&agrave; del territorio: '
        'insegne, LEDwall, menu, etichette e stampa. Scegli una categoria.</p>'
        '</div></section>')

content = ('<!-- wp:html -->\n<div id="ik-lavori">' + CSS + hero + radios + tabs + panels + cta +
           '</div>\n<!-- /wp:html -->')

json.dump({"content": content}, open(SC + "lavori_page_payload.json", "w"), ensure_ascii=False)
print("payload pronto:", len(content), "byte,", len(media), "immagini")
