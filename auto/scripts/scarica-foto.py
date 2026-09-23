#!/usr/bin/env python3
"""Scarica foto dimostrative con licenza libera (Openverse) per la demo.

Sono immagini di esempio per far vedere l'effetto al cliente: nel sito vero
vanno sostituite con le foto dei veicoli davvero in salone.
Autori e licenze finiscono in demo/img/crediti.json e nella pagina crediti.

Uso:  python3 scripts/scarica-foto.py
"""

import json
import pathlib
import subprocess
import time
import re
import unicodedata
import urllib.parse

RADICE = pathlib.Path(__file__).resolve().parent.parent
DEMO = RADICE / "demo"
IMG = DEMO / "img"
DATI = json.loads((DEMO / "auto.json").read_text(encoding="utf-8"))

API = "https://api.openverse.org/v1/images/"
LICENZE = "cc0,pdm,by"
MAX_BYTE = 2_000_000
AGENTE = "NewElettrocarDemo/1.0 (sito dimostrativo)"

USATE = set()  # url gia' presi, per non ripetere la stessa foto su due veicoli


def rifiutate():
    """Foto gia' scartate a mano: non vanno riscaricate."""
    percorso = pathlib.Path(__file__).resolve().parent.parent / "demo" / "img" / "rifiutate.json"
    if not percorso.exists():
        return set()
    return set(json.loads(percorso.read_text(encoding="utf-8")))


def interroga(parametri):
    risposta = subprocess.run(
        ["curl", "-s", "--max-time", "30", "-A", AGENTE, f"{API}?{urllib.parse.urlencode(parametri)}"],
        capture_output=True, text=True, check=False,
    ).stdout
    try:
        return json.loads(risposta).get("results", [])
    except json.JSONDecodeError:
        return []


def normalizza(testo):
    testo = unicodedata.normalize("NFD", str(testo or "").lower())
    return "".join(c for c in testo if unicodedata.category(c) != "Mn")


# Titoli da scartare: l'archivio libero e' pieno di modellini, auto da corsa,
# disegni e foto che con un annuncio di vendita non c'entrano niente.
ESCLUSI = (
    "lego", "toy", "model kit", "diecast", "die-cast", "miniature", "scale model",
    "rally", "race", "racing", "drift", "wrc", "crash", "wreck", "junk", "scrap",
    "rusty", "abandoned", "cutaway", "diagram", "drawing", "illustration", "poster",
    "sketch", "logo", "badge", "emblem", "vr", "virtual reality", "simulator",
    "museum", "engine", "gearbox", "tuning", "modified", "camper", "motorhome",
    "ambulance", "police", "taxi", "postal", "usps", "fire", "army",
    "advert", "advertisement", "brochure", "magazine", "catalogue", "leaflet",
    "welly", "crane", "space", "sexy", "cabrio", "convertible", "show car",
)

GENERICHE = {"car", "auto", "classic", "benz"}


def punteggio(risultato, query):
    """Quanto un risultato somiglia davvero al veicolo cercato."""
    titolo = normalizza(risultato.get("title"))
    if not titolo:
        return -1
    # parole intere: "toy" non deve far scartare "Toyota"
    if any(re.search(r"\b" + re.escape(parola) + r"\b", titolo) for parola in ESCLUSI):
        return -1

    chiavi = [normalizza(p) for p in query.split() if normalizza(p) not in GENERICHE]
    trovate = sum(1 for k in chiavi if k in titolo)
    if trovate < len(chiavi):
        return -1  # deve contenere marca e modello, non uno solo

    larghezza = risultato.get("width") or 0
    altezza = risultato.get("height") or 0
    punti = 10
    if larghezza and altezza:
        rapporto = larghezza / altezza
        if 1.2 <= rapporto <= 2.0:  # foto orizzontale, come le vuole il catalogo
            punti += 5
        if larghezza >= 800:
            punti += 2
    return punti


def cerca(query, quante):
    # senza chiave l'archivio accetta al massimo 20 risultati per pagina
    base = {
        "license": LICENZE,
        "license_type": "commercial",
        "page_size": 20,
        "mature": "false",
    }
    candidati = []
    for parametri in (
        dict(base, q=query, aspect_ratio="wide"),
        dict(base, q=query, aspect_ratio="wide", page=2),
        dict(base, q=query),
    ):
        candidati.extend(interroga(parametri))
        if len(candidati) >= 40:
            break
        time.sleep(0.5)

    valutati = [(punteggio(c, query), c) for c in candidati]
    validi = [c for punti, c in sorted(valutati, key=lambda x: -x[0]) if punti > 0]

    # niente doppioni fra un veicolo e l'altro
    scarti = rifiutate()
    unici, visti = [], set()
    for c in validi:
        if c.get("url") and c["url"] not in USATE and c["url"] not in visti and c["url"] not in scarti:
            visti.add(c["url"])
            unici.append(c)
    return unici


def scarica(url, destinazione):
    esito = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "45", "-A", AGENTE, "-o", str(destinazione), url],
        check=False,
    )
    if esito.returncode != 0 or not destinazione.exists():
        return False
    peso = destinazione.stat().st_size
    if peso < 8_000 or peso > MAX_BYTE:  # pagina di errore o file troppo pesante
        destinazione.unlink(missing_ok=True)
        return False
    return True


def veicoli():
    """Ogni veicolo con quante foto servono e con cosa cercarle."""
    for auto in DATI["auto"]:
        yield auto["slug"], auto.get("foto_query", auto["titolo"]), 3
    for noleggio in DATI.get("noleggio", []):
        yield noleggio["slug"], noleggio.get("foto_query", noleggio["titolo"]), 2


def foto_presenti(slug, quante):
    return [n for n in range(1, quante + 1) if (IMG / f"{slug}-{n}.jpg").exists()]


def prendi(slug, query, quante):
    """Completa le foto mancanti di un veicolo. Restituisce quante ne ha ora."""
    gia = foto_presenti(slug, quante)
    if len(gia) >= quante:
        return len(gia), {}

    crediti = {}
    presi = len(gia)
    for risultato in cerca(query, quante):
        if presi >= quante:
            break
        url = risultato.get("url")
        if not url or not url.lower().split("?")[0].endswith((".jpg", ".jpeg", ".png")):
            continue

        destinazione = IMG / f"{slug}-{presi + 1}.jpg"
        if not scarica(url, destinazione):
            continue

        USATE.add(url)
        crediti[destinazione.name] = {
            "url": url,
            "titolo": risultato.get("title", ""),
            "autore": risultato.get("creator", ""),
            "licenza": (risultato.get("license", "") + " " + str(risultato.get("license_version", ""))).strip(),
            "origine": risultato.get("foreign_landing_url", ""),
        }
        presi += 1
        time.sleep(0.4)

    return presi, crediti


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    percorso_crediti = IMG / "crediti.json"
    crediti = json.loads(percorso_crediti.read_text(encoding="utf-8")) if percorso_crediti.exists() else {}
    for dato in crediti.values():
        pass

    da_fare = list(veicoli())

    # L'archivio limita le richieste ravvicinate: chi resta a mani vuote
    # viene ritentato in un secondo giro, non scartato.
    for giro in range(1, 4):
        rimasti = []
        for slug, query, quante in da_fare:
            presi, nuovi = prendi(slug, query, quante)
            crediti.update(nuovi)
            print(f"{'  ' if giro > 1 else ''}{slug}: {presi}/{quante} foto  ({query})")
            if presi < quante:
                rimasti.append((slug, query, quante))
            time.sleep(1.2)

        if not rimasti:
            break
        da_fare = rimasti
        if giro < 3:
            print(f"\nRitento {len(rimasti)} veicoli rimasti indietro...")
            time.sleep(5)

    percorso_crediti.write_text(json.dumps(crediti, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFoto disponibili: {len(crediti)}. Crediti in demo/img/crediti.json")


if __name__ == "__main__":
    main()
