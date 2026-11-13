"""Calcolo di prezzo pieno (barrato), prezzo scontato di fine anno e rate."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal

from .config import Configurazione, RegolaRate

EURO = Decimal("1")
CENTESIMO = Decimal("0.01")


def _arrotonda(importo: Decimal, modo: str) -> Decimal:
    passo = EURO if modo == "euro" else CENTESIMO
    return importo.quantize(passo, rounding=ROUND_HALF_UP).quantize(CENTESIMO)


@dataclass(frozen=True)
class PianoRate:
    codice: str
    nome: str
    numero_rate: int
    importo_rata: Decimal
    """Importo di ogni rata (per le rate a interessi zero, tutte tranne l'ultima)."""
    importo_ultima_rata: Decimal
    totale: Decimal
    noleggio: bool


@dataclass(frozen=True)
class Preventivo:
    prodotto: str
    nome_prodotto: str
    larghezza_cm: Decimal | None
    altezza_cm: Decimal | None
    superficie_mq: Decimal | None
    prezzo_pieno: Decimal
    """Prezzo di listino, da mostrare barrato quando lo sconto è attivo."""
    sconto_attivo: bool
    sconto_percentuale: Decimal
    prezzo_scontato: Decimal
    risparmio: Decimal
    rate: tuple[PianoRate, ...]


def _piano(regola: RegolaRate, prezzo: Decimal) -> PianoRate:
    if regola.coefficiente is not None:
        canone = (prezzo * regola.coefficiente).quantize(EURO, rounding=ROUND_CEILING).quantize(CENTESIMO)
        return PianoRate(
            codice=regola.codice,
            nome=regola.nome,
            numero_rate=regola.numero_rate,
            importo_rata=canone,
            importo_ultima_rata=canone,
            totale=canone * regola.numero_rate,
            noleggio=True,
        )
    n = regola.numero_rate
    rata = (prezzo / n).quantize(CENTESIMO, rounding=ROUND_HALF_UP)
    ultima = prezzo - rata * (n - 1)
    return PianoRate(
        codice=regola.codice,
        nome=regola.nome,
        numero_rate=n,
        importo_rata=rata,
        importo_ultima_rata=ultima,
        totale=prezzo,
        noleggio=False,
    )


def calcola_preventivo(
    config: Configurazione,
    prodotto: str,
    larghezza_cm: float | int | str | Decimal | None = None,
    altezza_cm: float | int | str | Decimal | None = None,
    data: dt.date | None = None,
) -> Preventivo:
    """Calcola prezzi e rate per un prodotto del listino.

    Per i prodotti a metro quadro servono larghezza e altezza in centimetri;
    per quelli a prezzo fisso le misure sono facoltative e non cambiano il prezzo.
    ``data`` decide se lo sconto di fine anno è attivo (di default oggi).
    """
    if prodotto not in config.prodotti:
        disponibili = ", ".join(sorted(config.prodotti))
        raise ValueError(f"Prodotto '{prodotto}' non in listino. Disponibili: {disponibili}")
    p = config.prodotti[prodotto]

    larghezza = Decimal(str(larghezza_cm)) if larghezza_cm is not None else None
    altezza = Decimal(str(altezza_cm)) if altezza_cm is not None else None
    superficie = None
    if larghezza is not None and altezza is not None:
        if larghezza <= 0 or altezza <= 0:
            raise ValueError("Larghezza e altezza devono essere maggiori di zero")
        superficie = larghezza * altezza / Decimal(10000)

    if p.prezzo_fisso is not None:
        lordo = p.prezzo_fisso
    else:
        if superficie is None:
            raise ValueError(f"Per '{prodotto}' servono larghezza e altezza in cm")
        lordo = superficie * p.prezzo_mq
    prezzo_pieno = _arrotonda(lordo, config.arrotondamento_listino)

    data = data or dt.date.today()
    sconto = config.sconto
    attivo = sconto.attivo(data) and sconto.percentuale > 0
    if attivo:
        prezzo_scontato = _arrotonda(prezzo_pieno * (100 - sconto.percentuale) / 100, sconto.arrotondamento)
    else:
        prezzo_scontato = prezzo_pieno

    return Preventivo(
        prodotto=prodotto,
        nome_prodotto=p.nome,
        larghezza_cm=larghezza,
        altezza_cm=altezza,
        superficie_mq=superficie.quantize(CENTESIMO, rounding=ROUND_HALF_UP) if superficie is not None else None,
        prezzo_pieno=prezzo_pieno,
        sconto_attivo=attivo,
        sconto_percentuale=sconto.percentuale if attivo else Decimal(0),
        prezzo_scontato=prezzo_scontato,
        risparmio=prezzo_pieno - prezzo_scontato,
        rate=tuple(_piano(r, prezzo_scontato) for r in config.rate),
    )
