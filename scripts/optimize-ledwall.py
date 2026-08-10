# -*- coding: utf-8 -*-
import os, json
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
SC = "/tmp/claude-0/-home-user-Fortunato/caa1bb9f-37fa-587f-bedd-c11b09576fba/scratchpad/"
SRC = SC + "ledwall_real/"
OUT = SC + "ledwall_web/"
os.makedirs(OUT, exist_ok=True)

# project -> ordered list of source filenames (first = cover)
projects = {
    "Officina Gastronomica": {
        "title": "LEDwall pubblicitario",
        "files": ["44_29agosto-11-47-25-3.jpg", "12_promozioni-10-11-39-4.jpg",
                  "13_promozioni-10-11-41-1.jpg", "15_promozioni-10-11-40-3.jpg",
                  "21_promozioni-10-11-39.jpg", "22_promozioni-10-11-40.jpg",
                  "25_29agosto-11-47-25-2.jpg", "17_promozioni-10-11-38.jpg"],
    },
    "Belle Gomme": {
        "title": "LEDwall officina",
        "files": ["14_promozioni-ledwall-promozioni-clien.jpg", "10_promozioni-10-11-39-1.jpg",
                  "18_promozioni-10-11-40-2.jpg", "26_29agosto-11-50-15.jpg",
                  "24_29agosto-11-50-17-4.jpg", "27_29agosto-11-50-15-3.jpg",
                  "30_29agosto-11-50-16-4.jpg", "46_29agosto-11-50-15-1.jpg"],
    },
    "Il Trenino del Capo": {
        "title": "LEDwall evento - Tropea",
        "files": ["07_il-trenino-trenino.png"],
    },
}
SLUG = {"Officina Gastronomica": "officina-gastronomica", "Belle Gomme": "belle-gomme",
        "Il Trenino del Capo": "trenino-del-capo"}

MAXW = 1400
out = []
for proj, info in projects.items():
    ps = []
    for i, fn in enumerate(info["files"], 1):
        src = SRC + fn
        if not os.path.exists(src):
            print("MISSING", src); continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        w, h = im.size
        if w > MAXW:
            im = im.resize((MAXW, int(h * MAXW / w)), Image.LANCZOS)
        slug = "ledwall-%s-%02d" % (SLUG[proj], i)
        p = OUT + slug + ".jpg"
        im.save(p, "JPEG", quality=82, optimize=True, progressive=True)
        ps.append({"slug": slug, "file": p, "kb": os.path.getsize(p)//1024})
    out.append({"project": proj, "title": info["title"], "slug": SLUG[proj], "photos": ps})
    print("%-22s %d foto" % (proj, len(ps)))

json.dump(out, open(SC + "ledwall_projects_src.json", "w"), ensure_ascii=False, indent=1)
print("tot foto:", sum(len(x["photos"]) for x in out))
