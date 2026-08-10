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
#ik-lavori figure.card{cursor:pointer;position:relative}
#ik-lavori .card .im{position:relative}
#ik-lavori .card .im::after{content:"";position:absolute;inset:0;background:rgba(30,34,53,0);transition:background .18s;display:flex}
#ik-lavori .card:hover .im::after{background:rgba(30,34,53,.14)}
#ik-lavori .card .zoom{position:absolute;top:10px;right:10px;width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.9);transition:.18s;z-index:2;box-shadow:0 3px 10px rgba(0,0,0,.18)}
#ik-lavori .card:hover .zoom{opacity:1;transform:none}
#ik-lavori .card .zoom svg{width:18px;height:18px;fill:#1E2235}
#ik-lb{position:fixed;inset:0;z-index:99999;background:rgba(15,20,34,.92);display:none;align-items:flex-start;justify-content:center;padding:28px 16px;overflow:auto;-webkit-overflow-scrolling:touch}
#ik-lb.open{display:flex}
#ik-lb .box{max-width:1100px;width:100%;margin:auto;text-align:center}
#ik-lb img{max-width:100%;height:auto;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.5);background:#fff}
#ik-lb .cap{color:#fff;font-family:'Archivo','Inter',sans-serif;margin:16px 0 4px;font-size:19px;font-weight:700}
#ik-lb .cap small{display:block;color:var(--gold);font-family:'Inter',sans-serif;font-weight:500;font-size:14px;margin-top:3px}
#ik-lb .close{position:fixed;top:16px;right:18px;width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.14);border:0;color:#fff;font-size:26px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.15s}
#ik-lb .close:hover{background:var(--gold);color:#1E2235}
#ik-lb .hint{color:#aeb4c6;font-size:12px;margin-top:12px}
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
        zoom = ('<span class="zoom"><svg viewBox="0 0 24 24" aria-hidden="true">'
                '<path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 5 1.49-1.5-5-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14zM9 7h1v2h2v1h-2v2H9v-2H7V9h2z"/>'
                '</svg></span>')
        panels += ('<figure class="card" role="button" tabindex="0" aria-label="Ingrandisci %s" '
                   'data-full="%s" data-cli="%s" data-sub="%s">'
                   '<div class="im">%s<img loading="lazy" src="%s" alt="%s" width="%d" height="%d"></div>'
                   '<figcaption><strong>%s</strong><span>%s</span></figcaption></figure>') % (
            esc(m["client"]), m["url"], esc(m["client"]), esc(m["title"]),
            zoom, m["url"], esc(m["client"] + " - " + m["title"]),
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

lightbox = ('<div id="ik-lb" role="dialog" aria-modal="true">'
            '<button class="close" type="button" aria-label="Chiudi">&times;</button>'
            '<div class="box"><img src="" alt=""><div class="cap"></div>'
            '<div class="hint">Tocca fuori o premi ESC per chiudere</div></div></div>')

script = ("<script>(function(){"
  "var lb=document.getElementById('ik-lb');if(!lb)return;"
  "var img=lb.querySelector('img'),cap=lb.querySelector('.cap');"
  "function open(c){var f=c.getAttribute('data-full');if(!f)return;"
  "img.setAttribute('src',f);img.setAttribute('alt',(c.getAttribute('data-cli')||'')+' '+(c.getAttribute('data-sub')||''));"
  "cap.innerHTML=(c.getAttribute('data-cli')||'')+'<small>'+(c.getAttribute('data-sub')||'')+'</small>';"
  "lb.classList.add('open');lb.scrollTop=0;document.body.style.overflow='hidden';}"
  "function close(){lb.classList.remove('open');img.setAttribute('src','');document.body.style.overflow='';}"
  "document.querySelectorAll('#ik-lavori .card').forEach(function(c){"
  "c.addEventListener('click',function(){open(c);});"
  "c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(c);}});});"
  "lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('close')||e.target.classList.contains('box'))close();});"
  "lb.querySelector('.close').addEventListener('click',close);"
  "document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('open'))close();});"
  "})();</script>")

content = ('<!-- wp:html -->\n<div id="ik-lavori">' + CSS + hero + radios + tabs + panels + cta +
           lightbox + '</div>' + script + '\n<!-- /wp:html -->')

json.dump({"content": content}, open(SC + "lavori_page_payload.json", "w"), ensure_ascii=False)
print("payload pronto:", len(content), "byte,", len(media), "immagini")
