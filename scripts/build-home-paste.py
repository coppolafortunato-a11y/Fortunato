#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigenera home-da-incollare.html a partire da home-wordpress.html.

Applica la stessa trasformazione di scripts/deploy-home.sh (fix larghezza
piena sulla prima regola #ik-home{...} + blocco <!-- wp:html --> di
Gutenberg), cosi' la versione "da incollare a mano" nell'editor WordPress
resta sempre allineata al sorgente della home.

Uso:  python3 scripts/build-home-paste.py          (con fix larghezza)
      FULLWIDTH=0 python3 scripts/build-home-paste.py
Non contatta il sito: scrive solo il file locale.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "home-wordpress.html")
DST = os.path.join(ROOT, "home-da-incollare.html")

body = open(SRC, encoding="utf-8").read()

if os.environ.get("FULLWIDTH", "1") == "1":
    fix = ";width:100vw;max-width:100vw;margin-left:calc(50% - 50vw);overflow-x:hidden"
    body, n = re.subn(r"(#ik-home\{[^}]*?)\}", r"\1" + fix + "}", body, count=1)
    if n == 0:
        raise SystemExit("ERRORE: regola #ik-home{...} non trovata.")

open(DST, "w", encoding="utf-8").write("<!-- wp:html -->\n" + body.rstrip("\n") + "\n\n<!-- /wp:html -->\n")
print("OK — %s (%d byte)" % (os.path.relpath(DST, ROOT), os.path.getsize(DST)))
