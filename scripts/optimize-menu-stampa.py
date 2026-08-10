# -*- coding: utf-8 -*-
import os, json
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
SC = "/tmp/claude-0/-home-user-Fortunato/caa1bb9f-37fa-587f-bedd-c11b09576fba/scratchpad/"
SRC = SC + "menu_stampa/"
OUT = SC + "menu_stampa_web/"
os.makedirs(OUT, exist_ok=True)

# menu galleries: client -> ordered source basenames
menus = {
    "Windy Hill": ["menu_windy-hill_%02d.jpg" % i for i in range(1, 9)],
    "Bad Bull":   ["menu_bad-bull_01.jpg"] + ["menu_bad-bull_%02d.jpg" % i for i in [3,4,5,6,7,8,9,10]],
    "Kairos":     ["menu_kairos_02.png", "menu_kairos_03.png", "menu_kairos_05.png"],
}
# stampa new works: (basename, client, title, slug)
stampa = [
    ("stampa_peppe-plutino.png", "Plugin Gin", "Roll-up espositore", "stampa-plugin-gin"),
    ("stampa_pinacoteca.png",    "Pinacoteca", "Insegna", "stampa-pinacoteca"),
    ("stampa_gf-barber-shop.png","GF Barber Shop", "Espositore da terra", "stampa-gf-barber"),
]

MAXW = 1400
def opt(src, slug):
    im = ImageOps.exif_transpose(Image.open(SRC + src)).convert("RGB")
    w, h = im.size
    if w > MAXW:
        im = im.resize((MAXW, int(h * MAXW / w)), Image.LANCZOS)
    p = OUT + slug + ".jpg"
    im.save(p, "JPEG", quality=82, optimize=True, progressive=True)
    return {"slug": slug, "file": p, "kb": os.path.getsize(p)//1024}

out_menus = []
SLUGM = {"Windy Hill": "windy-hill", "Bad Bull": "bad-bull", "Kairos": "kairos"}
for cli, files in menus.items():
    ph = []
    for i, fn in enumerate(files, 1):
        if not os.path.exists(SRC + fn):
            print("MISS", fn); continue
        ph.append(opt(fn, "menu-%s-%02d" % (SLUGM[cli], i)))
    out_menus.append({"client": cli, "photos": ph})
    print("menu %-12s %d pagine" % (cli, len(ph)))

out_stampa = []
for fn, cli, title, slug in stampa:
    if not os.path.exists(SRC + fn):
        print("MISS", fn); continue
    o = opt(fn, slug); o.update({"client": cli, "title": title})
    out_stampa.append(o)
    print("stampa %-14s ok" % cli)

json.dump({"menus": out_menus, "stampa": out_stampa},
          open(SC + "menu_stampa_src.json", "w"), ensure_ascii=False, indent=1)
print("tot foto:", sum(len(m["photos"]) for m in out_menus) + len(out_stampa))
