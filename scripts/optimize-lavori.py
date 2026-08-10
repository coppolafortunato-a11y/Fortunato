# -*- coding: utf-8 -*-
import os, json
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None

SC = "/tmp/claude-0/-home-user-Fortunato/caa1bb9f-37fa-587f-bedd-c11b09576fba/scratchpad/"
P2 = SC + "portfolio2/"
LW = SC + "ledwall/"
OUT = SC + "lavori_web/"
os.makedirs(OUT, exist_ok=True)

# (src, category, client, title, slug)
items = [
    # LEDwall (prima)
    (LW+"06_passion-pizza.jpg",      "LEDwall", "Passion Pizza", "LEDwall pubblicitario",       "ledwall-passion-pizza"),
    (LW+"09_ideamarketing-generico.png","LEDwall","Idea Marketing","LEDwall a noleggio",          "ledwall-noleggio"),
    (LW+"07_promozioni-clienti-evento-28-ago.jpg","LEDwall","Evento cliente","Schermo installato","ledwall-evento"),
    (LW+"11_fusiion.jpg",            "LEDwall", "Fusion Restaurant", "Grafica per LEDwall",        "ledwall-fusion"),
    # Insegne
    (P2+"06_la-frutteria-insegne.jpg","Insegne","La Frutteria","Insegna esterna",                "insegna-la-frutteria"),
    (P2+"08_terra-mia-insegne.jpg",  "Insegne", "Terra Mia", "Insegna ristorante-pizzeria",       "insegna-terra-mia"),
    (P2+"03_stilo-infissi-insegne.png","Insegne","Stilo Infissi","Insegna e brand",               "insegna-stilo-infissi"),
    (P2+"07_insegna-luminosa-da-esterno-cassa-in-alluminio-70x100.jpg","Insegne","House of Kipp","Insegna luminosa","insegna-house-of-kipp"),
    (P2+"05_zio-sam-insegne.jpg",    "Insegne", "Zio Sam", "Insegna decorata",                    "insegna-zio-sam"),
    (P2+"12_centro-riparo-vetrine.jpg","Insegne","Centro Riparo","Punto vendita (foto reale)",    "insegna-centro-riparo"),
    # Menu & Ristorazione
    (P2+"19_windy-hill-menu.jpg",    "Menu", "Windy Hill", "Menu pizzeria",                        "menu-windy-hill"),
    (P2+"20_bad-bull-menu.jpg",      "Menu", "Bad Bull", "Menu burger",                            "menu-bad-bull"),
    (P2+"21_kairos-menu.png",        "Menu", "Kairos", "Menu gelateria",                           "menu-kairos"),
    # Etichette & Packaging
    (P2+"24_calabrian-sauce-etichette.png","Etichette","Calabrian Sauce","Etichetta conserve",    "etichetta-calabrian-sauce"),
    (P2+"25_creazzo-luigia-etichette.jpg","Etichette","Creazzo Luigia","Etichetta gastronomia",   "etichetta-creazzo-luigia"),
    (P2+"23_ideafrutta-etichette.jpg","Etichette","Ideafrutta","Marchio e etichetta",             "etichetta-ideafrutta"),
    (P2+"17_lustro-mockup.png",      "Etichette", "Lustro", "Etichetta vino",                      "etichetta-lustro"),
    # Stampa & Allestimenti
    (P2+"13_air-and-fire-vetrine.png","Stampa","Air & Fire","Espositore roll-up",                 "stampa-air-and-fire"),
    (P2+"18_mockup-2.jpg",           "Stampa", "NG Citrus", "Merchandising e packaging",           "stampa-ng-citrus"),
]

MAXW = 1400
manifest = []
for src, cat, cli, title, slug in items:
    if not os.path.exists(src):
        print("MISSING", src); continue
    im = Image.open(src)
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    if w > MAXW:
        im = im.resize((MAXW, int(h * MAXW / w)), Image.LANCZOS)
    out = OUT + slug + ".jpg"
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    kb = os.path.getsize(out) // 1024
    manifest.append({"category": cat, "client": cli, "title": title, "slug": slug,
                     "file": out, "w": im.width, "h": im.height, "kb": kb})
    print("%-9s %-18s %5dx%-4d %4dKB  %s" % (cat, cli, im.width, im.height, kb, slug))

json.dump(manifest, open(SC+"lavori_manifest.json", "w"), ensure_ascii=False, indent=1)
cats = {}
for m in manifest:
    cats[m["category"]] = cats.get(m["category"], 0) + 1
print("\nTotale:", len(manifest), "| per categoria:", cats)
