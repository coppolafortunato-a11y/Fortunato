"""Lettura e validazione del file di configurazione (TOML)."""

from __future__ import annotations

import datetime as dt
import tomllib
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

CONFIG_PREDEFINITA = Path(__file__).resolve().parent.parent / "config.toml"
ARROTONDAMENTI = ("euro", "centesimi")


class ErroreConfigurazione(ValueError):
    """Il file di configurazione manca di un dato o contiene un valore non valido."""


@dataclass(frozen=True)
class Prodotto:
    codice: str
    nome: str
    prezzo_mq: Decimal | None = None
    prezzo_fisso: Decimal | None = None


@dataclass(frozen=True)
class ScontoFineAnno:
    percentuale: Decimal
    valido_dal: dt.date
    valido_al: dt.date
    arrotondamento: str

    def attivo(self, data: dt.date) -> bool:
        return self.valido_dal <= data <= self.valido_al


@dataclass(frozen=True)
class RegolaRate:
    codice: str
    nome: str
    numero_rate: int
    coefficiente: Decimal | None = None


@dataclass(frozen=True)
class Configurazione:
    prodotti: dict[str, Prodotto]
    arrotondamento_listino: str
    sconto: ScontoFineAnno
    rate: tuple[RegolaRate, ...]


def _decimale(valore, dove: str) -> Decimal:
    if isinstance(valore, bool) or not isinstance(valore, (int, float, str)):
        raise ErroreConfigurazione(f"{dove}: atteso un numero, trovato {valore!r}")
    try:
        # str() evita le imprecisioni dei float (0.0335 resta 0.0335).
        return Decimal(str(valore))
    except Exception as exc:  # decimal.InvalidOperation
        raise ErroreConfigurazione(f"{dove}: numero non valido {valore!r}") from exc


def _arrotondamento(valore, dove: str) -> str:
    if valore not in ARROTONDAMENTI:
        raise ErroreConfigurazione(f"{dove}: usa 'euro' o 'centesimi', trovato {valore!r}")
    return valore


def _richiesto(sezione: dict, chiave: str, dove: str):
    if chiave not in sezione:
        raise ErroreConfigurazione(f"{dove}: manca '{chiave}'")
    return sezione[chiave]


def carica_configurazione(percorso: str | Path | None = None) -> Configurazione:
    """Legge il file TOML (di default ``config.toml`` accanto al pacchetto)."""
    percorso = Path(percorso) if percorso else CONFIG_PREDEFINITA
    with open(percorso, "rb") as f:
        dati = tomllib.load(f)
    return configurazione_da_dict(dati)


def configurazione_da_dict(dati: dict) -> Configurazione:
    listino = _richiesto(dati, "listino", "configurazione")
    prodotti_raw = _richiesto(listino, "prodotti", "[listino]")
    if not prodotti_raw:
        raise ErroreConfigurazione("[listino.prodotti]: nessun prodotto definito")

    prodotti: dict[str, Prodotto] = {}
    for codice, p in prodotti_raw.items():
        dove = f"[listino.prodotti.{codice}]"
        ha_mq, ha_fisso = "prezzo_mq" in p, "prezzo_fisso" in p
        if ha_mq == ha_fisso:
            raise ErroreConfigurazione(f"{dove}: indica 'prezzo_mq' oppure 'prezzo_fisso' (uno solo)")
        prezzo = _decimale(p["prezzo_mq"] if ha_mq else p["prezzo_fisso"], dove)
        if prezzo <= 0:
            raise ErroreConfigurazione(f"{dove}: il prezzo deve essere maggiore di zero")
        prodotti[codice] = Prodotto(
            codice=codice,
            nome=str(p.get("nome", codice)),
            prezzo_mq=prezzo if ha_mq else None,
            prezzo_fisso=prezzo if ha_fisso else None,
        )

    s = _richiesto(dati, "sconto_fine_anno", "configurazione")
    dove = "[sconto_fine_anno]"
    percentuale = _decimale(_richiesto(s, "percentuale", dove), dove + " percentuale")
    if not Decimal(0) <= percentuale < Decimal(100):
        raise ErroreConfigurazione(f"{dove}: la percentuale deve essere tra 0 e 100 (escluso)")
    dal, al = _richiesto(s, "valido_dal", dove), _richiesto(s, "valido_al", dove)
    for nome, d in (("valido_dal", dal), ("valido_al", al)):
        if not isinstance(d, dt.date) or isinstance(d, dt.datetime):
            raise ErroreConfigurazione(f"{dove}: '{nome}' deve essere una data AAAA-MM-GG senza virgolette")
    if dal > al:
        raise ErroreConfigurazione(f"{dove}: 'valido_dal' è dopo 'valido_al'")
    sconto = ScontoFineAnno(
        percentuale=percentuale,
        valido_dal=dal,
        valido_al=al,
        arrotondamento=_arrotondamento(s.get("arrotondamento", "euro"), dove),
    )

    regole: list[RegolaRate] = []
    codici_visti: set[str] = set()
    for i, r in enumerate(dati.get("rate", []), start=1):
        dove = f"[[rate]] n.{i}"
        codice = str(_richiesto(r, "codice", dove))
        if codice in codici_visti:
            raise ErroreConfigurazione(f"{dove}: codice '{codice}' ripetuto")
        codici_visti.add(codice)
        numero = _richiesto(r, "numero_rate", dove)
        if isinstance(numero, bool) or not isinstance(numero, int) or numero < 1:
            raise ErroreConfigurazione(f"{dove}: 'numero_rate' deve essere un intero maggiore di zero")
        coeff = None
        if "coefficiente" in r:
            coeff = _decimale(r["coefficiente"], dove + " coefficiente")
            if coeff <= 0:
                raise ErroreConfigurazione(f"{dove}: il coefficiente deve essere maggiore di zero")
        regole.append(RegolaRate(codice=codice, nome=str(r.get("nome", codice)), numero_rate=numero, coefficiente=coeff))

    return Configurazione(
        prodotti=prodotti,
        arrotondamento_listino=_arrotondamento(listino.get("arrotondamento", "euro"), "[listino]"),
        sconto=sconto,
        rate=tuple(regole),
    )
