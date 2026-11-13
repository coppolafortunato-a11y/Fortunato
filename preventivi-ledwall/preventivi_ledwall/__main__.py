"""Uso da riga di comando:

    python -m preventivi_ledwall outdoor_p6 200 100
    python -m preventivi_ledwall totem --data 2027-01-15
    python -m preventivi_ledwall --elenco
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from decimal import Decimal

from .calcolo import calcola_preventivo
from .config import ErroreConfigurazione, carica_configurazione


def euro(importo: Decimal) -> str:
    """Formato italiano: 1.234,50 €"""
    testo = f"{importo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{testo} €"


def _json(valore):
    if isinstance(valore, Decimal):
        return str(valore)
    raise TypeError(type(valore))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="preventivi_ledwall", description="Prezzi e rate per i preventivi LEDwall (IVA esclusa).")
    parser.add_argument("prodotto", nargs="?", help="codice prodotto, es. outdoor_p6")
    parser.add_argument("larghezza_cm", nargs="?", type=Decimal)
    parser.add_argument("altezza_cm", nargs="?", type=Decimal)
    parser.add_argument("--data", type=dt.date.fromisoformat, help="data del preventivo AAAA-MM-GG (default oggi)")
    parser.add_argument("--config", help="percorso di un config.toml alternativo")
    parser.add_argument("--json", action="store_true", help="stampa il risultato in JSON")
    parser.add_argument("--elenco", action="store_true", help="elenca i prodotti in listino")
    args = parser.parse_args(argv)

    try:
        config = carica_configurazione(args.config)
    except (OSError, ErroreConfigurazione) as exc:
        print(f"Errore nella configurazione: {exc}", file=sys.stderr)
        return 2

    if args.elenco or not args.prodotto:
        for codice, p in config.prodotti.items():
            prezzo = f"{euro(p.prezzo_mq)}/m²" if p.prezzo_mq is not None else euro(p.prezzo_fisso)
            print(f"{codice:<14} {p.nome:<14} {prezzo}")
        return 0

    try:
        prev = calcola_preventivo(config, args.prodotto, args.larghezza_cm, args.altezza_cm, args.data)
    except ValueError as exc:
        print(f"Errore: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(prev.__dict__ | {"rate": [r.__dict__ for r in prev.rate]}, default=_json, ensure_ascii=False, indent=2))
        return 0

    print(f"Prodotto:        {prev.nome_prodotto}")
    if prev.superficie_mq is not None:
        mq = str(prev.superficie_mq).replace(".", ",")
        print(f"Misure:          {prev.larghezza_cm} × {prev.altezza_cm} cm ({mq} m²)")
    if prev.sconto_attivo:
        print(f"Prezzo pieno:    {euro(prev.prezzo_pieno)}  (barrato)")
        print(f"Sconto fine anno: -{prev.sconto_percentuale}%  (risparmi {euro(prev.risparmio)})")
        print(f"Prezzo scontato: {euro(prev.prezzo_scontato)}")
    else:
        print(f"Prezzo:          {euro(prev.prezzo_pieno)}  (sconto fine anno non attivo)")
    for r in prev.rate:
        if r.importo_ultima_rata != r.importo_rata:
            dettaglio = f"{r.numero_rate - 1} × {euro(r.importo_rata)} + 1 × {euro(r.importo_ultima_rata)}"
        else:
            dettaglio = f"{r.numero_rate} × {euro(r.importo_rata)}"
        print(f"  {r.nome:<26} {dettaglio}  (totale {euro(r.totale)})")
    print("Importi IVA esclusa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
