#!/usr/bin/env python3
"""Toglie dalla demo le foto scaricate che non vanno bene e rinumera le altre.

L'archivio libero restituisce anche modellini, disegni tecnici e foto fuori
tema: questo passaggio è la selezione a occhio, fatta una volta.

Uso:  python3 scripts/scarta-foto.py file1.jpg file2.jpg ...
"""

import json
import pathlib
import re
import sys

IMG = pathlib.Path(__file__).resolve().parent.parent / "demo" / "img"
CREDITI = IMG / "crediti.json"
RIFIUTATE = IMG / "rifiutate.json"


def main(scartate):
    crediti = json.loads(CREDITI.read_text(encoding="utf-8")) if CREDITI.exists() else {}

    scarti = set(json.loads(RIFIUTATE.read_text(encoding="utf-8"))) if RIFIUTATE.exists() else set()

    for nome in scartate:
        (IMG / nome).unlink(missing_ok=True)
        dato = crediti.pop(nome, None)
        if dato and dato.get("url"):
            scarti.add(dato["url"])

    RIFIUTATE.write_text(json.dumps(sorted(scarti), ensure_ascii=False, indent=2), encoding="utf-8")

    # Rinumera: se resta un buco (2 cancellata su 1,2,3) le foto successive
    # scalano, altrimenti la galleria si ferma al primo numero mancante.
    per_veicolo = {}
    for percorso in sorted(IMG.glob("*.jpg")):
        slug = re.sub(r"-\d+$", "", percorso.stem)
        per_veicolo.setdefault(slug, []).append(percorso)

    for slug, percorsi in per_veicolo.items():
        percorsi.sort(key=lambda p: int(p.stem.rsplit("-", 1)[1]))
        for nuovo, percorso in enumerate(percorsi, start=1):
            atteso = IMG / f"{slug}-{nuovo}.jpg"
            if percorso != atteso:
                dato = crediti.pop(percorso.name, None)
                percorso.rename(atteso)
                if dato:
                    crediti[atteso.name] = dato

    CREDITI.write_text(json.dumps(crediti, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scartate {len(scartate)} foto, ne restano {len(list(IMG.glob('*.jpg')))}.")


if __name__ == "__main__":
    main(sys.argv[1:])
