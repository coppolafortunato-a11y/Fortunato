# -*- coding: utf-8 -*-
import json, base64, os

SC = "/tmp/claude-0/-home-user-Fortunato/caa1bb9f-37fa-587f-bedd-c11b09576fba/scratchpad/"
manifest = json.load(open(SC + "lavori_manifest.json"))
faces = open(SC + "fonts/faces2.css").read()

# category order — LEDwall first
ORDER = ["LEDwall", "Insegne", "Menu", "Etichette", "Stampa"]
LABEL = {"LEDwall": "LEDwall", "Insegne": "Insegne & Vetrine", "Menu": "Menu",
         "Etichette": "Etichette & Packaging", "Stampa": "Stampa & Allestimenti"}

by_cat = {c: [] for c in ORDER}
for m in manifest:
    by_cat.setdefault(m["category"], []).append(m)

def b64img(path):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

def build(overview=False):
    # radios
    radios = ""
    for i, c in enumerate(ORDER):
        chk = " checked" if i == 0 else ""
        radios += '<input type="radio" name="ikcat" id="cat-%s" class="ik-tabradio"%s>\n' % (c.lower(), chk)
    # tabs
    tabs = '<div class="ik-tabs">'
    for c in ORDER:
        tabs += '<label for="cat-%s" class="ik-tab">%s <span>%d</span></label>' % (c.lower(), LABEL[c], len(by_cat[c]))
    tabs += '</div>'
    # panels
    panels = '<div class="ik-panels">'
    for c in ORDER:
        panels += '<section class="ik-panel ik-panel-%s">' % c.lower()
        panels += '<div class="ik-grid">'
        for m in by_cat[c]:
            src = b64img(m["file"])
            panels += ('<figure class="ik-card">'
                       '<div class="ik-card__img"><img loading="lazy" src="%s" alt="%s"></div>'
                       '<figcaption><strong>%s</strong><span>%s</span></figcaption>'
                       '</figure>') % (src, m["client"] + " - " + m["title"], m["client"], m["title"])
        panels += '</div></section>'
    panels += '</div>'

    ov_css = ".ik-panel{display:block!important}" if overview else ""

    css_rules = ""
    for c in ORDER:
        css_rules += "#cat-%s:checked~.ik-panels .ik-panel-%s{display:block}\n" % (c.lower(), c.lower())
        css_rules += "#cat-%s:checked~.ik-tabs label[for=cat-%s]{background:var(--navy);color:#fff;border-color:var(--navy)}\n" % (c.lower(), c.lower())

    html = """<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>I nostri lavori - Idea Marketing</title>
<style>
%FACES%
:root{--navy:#1E2235;--gold:#C9A961;--paper:#f8f7f4;--ink:#20232f;--line:#e7e3da}
*{box-sizing:border-box}
body{margin:0;font-family:'Inter',system-ui,sans-serif;color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
.ik-wrap{max-width:1180px;margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:'Archivo',sans-serif;font-style:normal}
em,i,cite{font-style:normal}
.ik-hero{background:var(--navy);color:#fff;padding:64px 0 56px;text-align:center}
.ik-hero .eyebrow{color:var(--gold);font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:13px;margin:0 0 14px}
.ik-hero h1{font-size:44px;line-height:1.08;margin:0 0 16px;font-weight:700}
.ik-hero p{max-width:640px;margin:0 auto;color:#c7cbd8;font-size:17px;line-height:1.6}
.ik-tabradio{position:absolute;opacity:0;pointer-events:none}
.ik-tabs{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:-28px auto 34px;position:relative;z-index:2}
.ik-tab{cursor:pointer;background:#fff;border:1px solid var(--line);border-radius:40px;padding:11px 20px;font-weight:600;font-size:15px;color:var(--ink);box-shadow:0 6px 18px rgba(20,24,40,.06);transition:.15s;display:inline-flex;align-items:center;gap:8px}
.ik-tab:hover{border-color:var(--gold)}
.ik-tab span{background:var(--paper);color:#8a8676;font-size:12px;font-weight:700;border-radius:20px;padding:2px 8px}
%RULES%
.ik-panel{display:none;padding-bottom:40px}
.ik-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.ik-card{margin:0;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;box-shadow:0 8px 24px rgba(20,24,40,.06);transition:.18s}
.ik-card:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(20,24,40,.12)}
.ik-card__img{aspect-ratio:4/3;overflow:hidden;background:#f0eee9;display:flex;align-items:center;justify-content:center}
.ik-card__img img{width:100%;height:100%;object-fit:cover;display:block}
.ik-card figcaption{padding:14px 16px}
.ik-card figcaption strong{display:block;font-family:'Archivo',sans-serif;font-size:16px;color:var(--navy)}
.ik-card figcaption span{display:block;color:#8a8676;font-size:13px;margin-top:2px}
.ik-note{max-width:1180px;margin:8px auto 60px;padding:0 24px;text-align:center;color:#9a9686;font-size:13px}
@media(max-width:820px){.ik-grid{grid-template-columns:repeat(2,1fr)}.ik-hero h1{font-size:32px}}
@media(max-width:520px){.ik-grid{grid-template-columns:1fr}}
%OVCSS%
</style></head><body>
<section class="ik-hero"><div class="ik-wrap">
<p class="eyebrow">Portfolio</p>
<h1>I nostri lavori</h1>
<p>Una selezione di progetti realizzati per le attivita del territorio: insegne, LEDwall, menu, etichette e stampa. Scegli una categoria.</p>
</div></section>
<div class="ik-wrap">
%RADIOS%
%TABS%
%PANELS%
</div>
<p class="ik-note">Anteprima - immagini reali dagli archivi. Da confermare prima della pubblicazione.</p>
</body></html>"""
    html = (html.replace("%FACES%", faces).replace("%RULES%", css_rules)
                .replace("%OVCSS%", ov_css).replace("%RADIOS%", radios)
                .replace("%TABS%", tabs).replace("%PANELS%", panels))
    return html

open(SC + "lavori_preview.html", "w").write(build(overview=False))
open(SC + "lavori_overview.html", "w").write(build(overview=True))
print("scritti lavori_preview.html (interattivo) e lavori_overview.html (tutto visibile)")
print("KB preview:", os.path.getsize(SC+"lavori_preview.html")//1024)
