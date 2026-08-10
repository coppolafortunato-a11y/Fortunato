# -*- coding: utf-8 -*-
import json, urllib.parse, re

hdr = json.load(open("/tmp/hdr.json"))["content"]["raw"]

# 1) rimuovi la vecchia iniezione wp:html (topbar + whatsapp), tieni il resto (header con logo)
end = hdr.find("<!-- /wp:html -->")
header_group = hdr[end + len("<!-- /wp:html -->"):].lstrip("\n") if end != -1 else hdr

# pulizia: rimuovi eventuali CTA già inseriti (evita duplicati fra un run e l'altro)
header_group = re.sub(r'\s*<!-- wp:html --><a class="ik-cta-btn".*?</a><!-- /wp:html -->', '', header_group)

# 2) inserisci il CTA dopo il blocco navigation, dentro il gruppo a destra
nav_marker = 'wp:navigation'
i = header_group.find(nav_marker)
cta_block = '\n<!-- wp:html --><a class="ik-cta-btn" href="/contatti/">Richiedi un preventivo</a><!-- /wp:html -->\n'
if i != -1:
    j = header_group.find('/-->', i)
    if j != -1:
        j += len('/-->')
        header_group = header_group[:j] + cta_block + header_group[j:]

wa = "https://wa.me/393206116711?text=" + urllib.parse.quote("Ciao Idea Marketing, vorrei informazioni su ")

CSS = r'''<style id="ideamkt-extras">
:root{--ik-navy:#1E2235;--ik-gold:#C9A961;}
.ik-topbar{background:var(--ik-navy);color:#fff;font-size:14px;line-height:1;letter-spacing:.02em}
.ik-topbar__inner{max-width:1200px;margin:0 auto;padding:10px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.ik-topbar__left{display:flex;align-items:center;gap:24px;flex-wrap:wrap}
.ik-topbar a{color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:8px;transition:color .2s}
.ik-topbar a:hover{color:var(--ik-gold)}
.ik-topbar svg{width:15px;height:15px;flex:none;fill:var(--ik-gold)}
.ik-topbar__tel{font-weight:600}
.ik-topbar__place{opacity:.6;font-size:13px}
@media (max-width:780px){.ik-topbar__inner{justify-content:center;padding:9px 16px;gap:18px}.ik-topbar__email,.ik-topbar__place{display:none}}
.ik-cta-btn{display:inline-flex;align-items:center;background:var(--ik-gold);color:#1E2235!important;font-weight:600;font-size:14px;padding:9px 18px;border-radius:3px;text-decoration:none;white-space:nowrap;margin-left:6px;font-family:'Inter',sans-serif}
.ik-cta-btn:hover{background:#d8ba73}
@media (max-width:600px){.ik-cta-btn{display:none}}
.ik-fab{position:fixed;right:24px;bottom:24px;z-index:9999}
.ik-fab input{position:absolute;opacity:0;width:0;height:0}
.ik-fab__items{position:absolute;right:4px;bottom:70px;display:flex;flex-direction:column;gap:12px;align-items:center;opacity:0;transform:translateY(10px);pointer-events:none;transition:opacity .2s ease,transform .2s ease}
.ik-fab input:checked ~ .ik-fab__items{opacity:1;transform:none;pointer-events:auto}
.ik-fab__toggle{position:relative;width:58px;height:58px;border-radius:50%;background:var(--ik-gold);display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 6px 22px rgba(0,0,0,.24);transition:transform .2s}
.ik-fab__toggle:hover{transform:translateY(-2px)}
.ik-fab__toggle svg{width:28px;height:28px;fill:#1E2235;transition:transform .3s}
.ik-fab input:checked ~ .ik-fab__toggle svg{transform:rotate(90deg)}
.ik-fab__items a{width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(0,0,0,.22);transition:transform .2s}
.ik-fab__items a:hover{transform:scale(1.08)}
.ik-fab__items a svg{width:24px;height:24px}
.ik-fab__items .wa{background:#25D366}.ik-fab__items .wa svg{fill:#fff}
.ik-fab__items .tel{background:#1E2235}.ik-fab__items .tel svg{fill:var(--ik-gold)}
.ik-fab__items .mail{background:#fff;border:1px solid #e0ddd6}.ik-fab__items .mail svg{fill:#1E2235}
.ik-bottombar{display:none}
@media (max-width:780px){
.ik-fab{display:none}
.ik-bottombar{display:grid;grid-template-columns:1fr 1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:9998;background:#fff;border-top:1px solid #e0ddd6;box-shadow:0 -4px 16px rgba(0,0,0,.10)}
.ik-bottombar a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:9px 4px;font-size:11px;font-weight:700;color:#1E2235;text-decoration:none;border-left:1px solid #f0eee9;min-height:56px}
.ik-bottombar a:first-child{border-left:none}
.ik-bottombar svg{width:20px;height:20px;fill:#1E2235}
.ik-bottombar .wa{background:#25D366;color:#fff}.ik-bottombar .wa svg{fill:#fff}
.ik-bottombar .quote{background:var(--ik-gold);color:#1E2235}.ik-bottombar .quote svg{fill:#1E2235}
body{padding-bottom:58px}
}
@media (prefers-reduced-motion:reduce){.ik-fab *{transition:none}}
</style>'''

TEL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.7 21 3 13.3 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2z"/></svg>'
MAIL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.2-8 5-8-5V6l8 5 8-5v2.2z"/></svg>'
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.7 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5 0-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.3 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.2-.6-.4zM12 2.1c5.5 0 9.9 4.4 9.9 9.9 0 5.5-4.4 9.9-9.9 9.9-1.7 0-3.4-.5-4.9-1.3L2.1 22l1.5-4.8A9.8 9.8 0 0 1 2.1 12c0-5.5 4.4-9.9 9.9-9.9z"/></svg>'
CHAT_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zM7 9h10v2H7V9zm0 4h7v2H7v-2z"/></svg>'
DOC_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm0 2 4 4h-4V4zM8 13h8v2H8v-2zm0 4h8v2H8v-2z"/></svg>'

topbar = ('<div class="ik-topbar"><div class="ik-topbar__inner">'
  '<div class="ik-topbar__left">'
  '<a class="ik-topbar__tel" href="tel:+393206116711">' + TEL_SVG + '320 611 6711</a>'
  '<a class="ik-topbar__email" href="mailto:coppola.fortunato@gmail.com">' + MAIL_SVG + 'coppola.fortunato@gmail.com</a>'
  '</div><span class="ik-topbar__place">Reggio Calabria — Via Campoli 34</span>'
  '</div></div>')

fab = ('<div class="ik-fab">'
  '<input type="checkbox" id="ikfab" aria-hidden="true">'
  '<div class="ik-fab__items">'
  '<a class="wa" data-ik-wa href="' + wa + '" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">' + WA_SVG + '</a>'
  '<a class="tel" href="tel:+393206116711" aria-label="Chiamaci">' + TEL_SVG + '</a>'
  '<a class="mail" href="mailto:coppola.fortunato@gmail.com" aria-label="Scrivici una mail">' + MAIL_SVG + '</a>'
  '</div>'
  '<label class="ik-fab__toggle" for="ikfab" aria-label="Contattaci">' + CHAT_SVG + '</label>'
  '</div>')

bottombar = ('<div class="ik-bottombar">'
  '<a class="call" href="tel:+393206116711" aria-label="Chiama">' + TEL_SVG + '<span>Chiama</span></a>'
  '<a class="wa" data-ik-wa href="' + wa + '" target="_blank" rel="noopener" aria-label="WhatsApp">' + WA_SVG + '<span>WhatsApp</span></a>'
  '<a class="quote" href="/contatti/" aria-label="Richiedi un preventivo">' + DOC_SVG + '<span>Preventivo</span></a>'
  '</div>')

script = ("<script>(function(){"
  "var p=(location.pathname||'').toLowerCase();"
  "var m='Ciao Idea Marketing, vorrei informazioni per un progetto.';"
  "if(p.indexOf('ledwall')>-1){m='Ciao Idea Marketing, vorrei informazioni per un LEDwall.';}"
  "else if(p.indexOf('insegn')>-1){m=\"Ciao Idea Marketing, vorrei un preventivo per un'insegna.\";}"
  "else if(p.indexOf('stampa')>-1){m='Ciao Idea Marketing, vorrei un preventivo di stampa.';}"
  "else if(p.indexOf('sit')>-1||p.indexOf('web')>-1){m='Ciao Idea Marketing, vorrei informazioni per un sito web.';}"
  "else if(p.indexOf('social')>-1){m='Ciao Idea Marketing, vorrei informazioni per i social.';}"
  "var b='https://wa.me/393206116711?text='+encodeURIComponent(m);"
  "document.querySelectorAll('[data-ik-wa]').forEach(function(a){a.setAttribute('href',b);});"
  "})();</script>")

block = "<!-- wp:html -->\n" + CSS + "\n" + topbar + "\n" + fab + "\n" + bottombar + "\n" + script + "\n<!-- /wp:html -->\n\n"
new_header = block + header_group
json.dump({"content": new_header}, open("/tmp/hdr-new.json", "w"), ensure_ascii=False)
print("nuovo header pronto (%d byte) | CTA inserito: %s" % (len(new_header), "ik-cta-btn" in new_header))
