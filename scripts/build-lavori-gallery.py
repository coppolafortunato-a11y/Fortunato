# -*- coding: utf-8 -*-
# Builder v2: ogni lavoro puo' avere PIU' foto -> lightbox a galleria (avanti/indietro, contatore, swipe).
# Legge projects.json: [{category,client,title,photos:[url,...]}]
import json, sys
SC = "/tmp/claude-0/-home-user-Fortunato/caa1bb9f-37fa-587f-bedd-c11b09576fba/scratchpad/"
projects = json.load(open(SC + "lavori_projects.json"))

ORDER = ["LEDwall", "Insegne", "Menu", "Etichette", "Stampa"]
LABEL = {"LEDwall": "LEDwall", "Insegne": "Insegne &amp; Vetrine", "Menu": "Menu",
         "Etichette": "Etichette &amp; Packaging", "Stampa": "Stampa &amp; Allestimenti"}
by_cat = {c: [] for c in ORDER}
for p in projects:
    by_cat.setdefault(p["category"], []).append(p)

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
#ik-lavori figure.card{margin:0;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;box-shadow:0 8px 24px rgba(20,24,40,.06);transition:.18s;cursor:pointer;position:relative}
#ik-lavori figure.card:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(20,24,40,.12)}
#ik-lavori .card .im{aspect-ratio:4/3;overflow:hidden;background:#f0eee9;position:relative}
#ik-lavori .card .im img{width:100%;height:100%;object-fit:cover;display:block}
#ik-lavori .card .im::after{content:"";position:absolute;inset:0;background:rgba(30,34,53,0);transition:.18s}
#ik-lavori .card:hover .im::after{background:rgba(30,34,53,.14)}
#ik-lavori .card .badge{position:absolute;left:10px;bottom:10px;background:rgba(30,34,53,.82);color:#fff;font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px;display:inline-flex;align-items:center;gap:6px;z-index:2}
#ik-lavori .card .badge svg{width:13px;height:13px;fill:var(--gold)}
#ik-lavori .card .zoom{position:absolute;top:10px;right:10px;width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.9);transition:.18s;z-index:2;box-shadow:0 3px 10px rgba(0,0,0,.18)}
#ik-lavori .card:hover .zoom{opacity:1;transform:none}
#ik-lavori .card .zoom svg{width:18px;height:18px;fill:#1E2235}
#ik-lavori .card figcaption{padding:14px 16px}
#ik-lavori .card figcaption strong{display:block;font-family:'Archivo','Inter',sans-serif;font-size:16px;color:var(--navy)}
#ik-lavori .card figcaption span{display:block;color:#8a8676;font-size:13px;margin-top:2px}
#ik-lavori .cta{background:var(--navy);color:#fff;text-align:center;padding:54px 24px 58px}
#ik-lavori .cta h2{font-size:30px;margin:0 0 10px}
#ik-lavori .cta p{color:#c7cbd8;margin:0 0 24px;font-size:16px}
#ik-lavori .cta a{display:inline-flex;align-items:center;gap:9px;background:var(--gold);color:#1E2235;font-weight:600;text-decoration:none;padding:15px 30px;border-radius:5px;font-size:16px}
#ik-lavori .cta a:hover{background:#d8ba73}
/* lightbox galleria */
#ik-lb{position:fixed;inset:0;z-index:99999;background:rgba(15,20,34,.94);display:none;flex-direction:column;align-items:center;justify-content:center;padding:20px 12px}
#ik-lb.open{display:flex}
#ik-lb .stage{flex:1;display:flex;align-items:center;justify-content:center;width:100%;max-width:1180px;overflow:auto;-webkit-overflow-scrolling:touch}
#ik-lb .stage img{max-width:100%;max-height:100%;height:auto;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.5);background:#fff}
#ik-lb .cap{color:#fff;font-family:'Archivo','Inter',sans-serif;margin:14px 0 2px;font-size:19px;font-weight:700;text-align:center}
#ik-lb .cap small{display:block;color:var(--gold);font-family:'Inter',sans-serif;font-weight:500;font-size:14px;margin-top:3px}
#ik-lb .count{color:#aeb4c6;font-size:13px;margin-top:8px;letter-spacing:.03em}
#ik-lb .nav{position:fixed;top:50%;transform:translateY(-50%);width:52px;height:52px;border:0;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font-size:26px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.15s;z-index:2}
#ik-lb .nav:hover{background:var(--gold);color:#1E2235}
#ik-lb .prev{left:16px}#ik-lb .next{right:16px}
#ik-lb .nav.hidden{display:none}
#ik-lb .close{position:fixed;top:16px;right:18px;width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.14);border:0;color:#fff;font-size:26px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.15s;z-index:3}
#ik-lb .close:hover{background:var(--gold);color:#1E2235}
__RULES__
@media(max-width:820px){#ik-lavori .grid{grid-template-columns:repeat(2,1fr)}#ik-lavori .hero h1{font-size:32px}#ik-lb .nav{width:44px;height:44px;font-size:22px}}
@media(max-width:520px){#ik-lavori .grid{grid-template-columns:1fr}#ik-lb .prev{left:6px}#ik-lb .next{right:6px}}
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
    if not by_cat[c]:
        continue
    tabs += '<label for="cat-%s" class="tab tab-%s">%s <span class="n">%d</span></label>' % (
        c.lower(), c.lower(), LABEL[c], len(by_cat[c]))
tabs += '</div>'

CAM = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3 7.2 5H4a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-3.2L15 3H9zm3 15a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-2a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>')
LENTE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 5 1.49-1.5-5-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14z"/></svg>')

panels = '<div class="panels wrap">'
for c in ORDER:
    if not by_cat[c]:
        continue
    panels += '<section class="panel panel-%s"><div class="grid">' % c.lower()
    for p in by_cat[c]:
        photos = p["photos"]
        cover = photos[0]
        data = esc(json.dumps(photos))
        badge = ''
        if len(photos) > 1:
            badge = '<span class="badge">%s%d foto</span>' % (CAM, len(photos))
        panels += ('<figure class="card" role="button" tabindex="0" aria-label="Apri %s" '
                   'data-photos="%s" data-cli="%s" data-sub="%s">'
                   '<div class="im"><span class="zoom">%s</span>%s'
                   '<img loading="lazy" src="%s" alt="%s" width="1400" height="1050"></div>'
                   '<figcaption><strong>%s</strong><span>%s</span></figcaption></figure>') % (
            esc(p["client"]), data, esc(p["client"]), esc(p["title"]),
            LENTE, badge, cover, esc(p["client"] + " - " + p["title"]),
            esc(p["client"]), esc(p["title"]))
    panels += '</div></section>'
panels += '</div>'

cta = ('<div class="cta"><h2>Ti piace quello che facciamo?</h2>'
       '<p>Raccontaci la tua idea: ti diamo un preventivo senza impegno.</p>'
       '<a href="/contatti/">Richiedi un preventivo</a></div>')

hero = ('<section class="hero"><div class="wrap">'
        '<p class="eyebrow">Portfolio</p><h1>I nostri lavori</h1>'
        '<p>Una selezione di progetti realizzati per le attivit&agrave; del territorio: '
        'insegne, LEDwall, menu, etichette e stampa. Scegli una categoria e apri un lavoro per sfogliare le foto.</p>'
        '</div></section>')

lightbox = ('<div id="ik-lb" role="dialog" aria-modal="true">'
            '<button class="close" type="button" aria-label="Chiudi">&times;</button>'
            '<button class="nav prev" type="button" aria-label="Precedente">&#10094;</button>'
            '<div class="stage"><img src="" alt=""></div>'
            '<button class="nav next" type="button" aria-label="Successiva">&#10095;</button>'
            '<div class="cap"></div><div class="count"></div></div>')

script = ("<script>(function(){"
  "var lb=document.getElementById('ik-lb');if(!lb)return;"
  "var img=lb.querySelector('.stage img'),cap=lb.querySelector('.cap'),cnt=lb.querySelector('.count');"
  "var prev=lb.querySelector('.prev'),next=lb.querySelector('.next');"
  "var pics=[],idx=0;"
  "function show(){img.src=pics[idx];cnt.textContent=pics.length>1?(idx+1)+' / '+pics.length:'';"
  "var h=pics.length<2;prev.classList.toggle('hidden',h);next.classList.toggle('hidden',h);lb.querySelector('.stage').scrollTop=0;}"
  "function open(c){try{pics=JSON.parse(c.getAttribute('data-photos'));}catch(e){pics=[];}if(!pics.length)return;idx=0;"
  "cap.innerHTML=(c.getAttribute('data-cli')||'')+'<small>'+(c.getAttribute('data-sub')||'')+'</small>';"
  "show();lb.classList.add('open');document.body.style.overflow='hidden';}"
  "function close(){lb.classList.remove('open');img.src='';document.body.style.overflow='';}"
  "function go(d){idx=(idx+d+pics.length)%pics.length;show();}"
  "document.querySelectorAll('#ik-lavori .card').forEach(function(c){"
  "c.addEventListener('click',function(){open(c);});"
  "c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(c);}});});"
  "prev.addEventListener('click',function(e){e.stopPropagation();go(-1);});"
  "next.addEventListener('click',function(e){e.stopPropagation();go(1);});"
  "lb.querySelector('.close').addEventListener('click',close);"
  "lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('stage'))close();});"
  "document.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;"
  "if(e.key==='Escape')close();else if(e.key==='ArrowLeft')go(-1);else if(e.key==='ArrowRight')go(1);});"
  "var sx=0;lb.addEventListener('touchstart',function(e){sx=e.changedTouches[0].clientX;},{passive:true});"
  "lb.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50&&pics.length>1)go(dx<0?1:-1);},{passive:true});"
  "})();</script>")

content = ('<!-- wp:html -->\n<div id="ik-lavori">' + CSS + hero + radios + tabs + panels + cta +
           lightbox + '</div>' + script + '\n<!-- /wp:html -->')

json.dump({"content": content}, open(SC + "lavori_page_payload.json", "w"), ensure_ascii=False)
tot_photos = sum(len(p["photos"]) for p in projects)
print("payload:", len(content), "byte |", len(projects), "lavori |", tot_photos, "foto totali")
for c in ORDER:
    if by_cat[c]:
        print("  %-9s %d lavori" % (c, len(by_cat[c])))
