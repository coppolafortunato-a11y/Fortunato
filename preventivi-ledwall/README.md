# Calcolo preventivi LEDwall

Piccolo modulo Python che calcola, per un LEDwall del listino:

- il **prezzo pieno** (da mostrare **barrato** sul preventivo);
- il **prezzo scontato di fine anno**, se la data cade nel periodo della promo;
- le **rate**: per ogni piano di pagamento, numero di rate e importo della rata
  (rate a interessi zero e canoni di noleggio Grenke).

Tutti gli importi sono **IVA esclusa**, come sul calcolatore del sito.

> Il PDF del preventivo lo genera il gestionale **app.ideamkt.it**: qui c'è solo
> il calcolo dei numeri da riportare nel gestionale.

## Requisiti

Python 3.11 o successivo. Nessuna libreria da installare.

## Uso rapido

Dalla cartella `preventivi-ledwall/`:

```bash
# Elenco dei prodotti in listino
python3 -m preventivi_ledwall --elenco

# Outdoor P6 da 200 × 100 cm, preventivo fatto oggi
python3 -m preventivi_ledwall outdoor_p6 200 100

# Stesso calcolo a una data precisa (utile per verificare la promo)
python3 -m preventivi_ledwall outdoor_p6 200 100 --data 2026-12-01

# Prodotti a prezzo fisso: le misure non servono
python3 -m preventivi_ledwall totem

# Risultato in JSON (per copiarlo o passarlo ad altri strumenti)
python3 -m preventivi_ledwall outdoor_p6 200 100 --json
```

Esempio di risultato:

```
Prodotto:        Outdoor P6
Misure:          200 × 100 cm (2,00 m²)
Prezzo pieno:    1.500,00 €  (barrato)
Sconto fine anno: -15%  (risparmi 225,00 €)
Prezzo scontato: 1.275,00 €
  3 rate senza interessi     3 × 425,00 €  (totale 1.275,00 €)
  6 rate senza interessi     6 × 212,50 €  (totale 1.275,00 €)
  12 rate senza interessi    12 × 106,25 €  (totale 1.275,00 €)
  Noleggio Grenke 36 mesi    36 × 43,00 €  (totale 1.548,00 €)
  Noleggio Grenke 48 mesi    48 × 35,00 €  (totale 1.680,00 €)
  Noleggio Grenke 60 mesi    60 × 30,00 €  (totale 1.800,00 €)
Importi IVA esclusa.
```

## Uso da Python

```python
import datetime as dt
from preventivi_ledwall import carica_configurazione, calcola_preventivo

config = carica_configurazione()                 # legge config.toml
p = calcola_preventivo(config, "outdoor_p6", 200, 100, data=dt.date(2026, 12, 1))

p.prezzo_pieno       # Decimal('1500.00')  -> da barrare
p.prezzo_scontato    # Decimal('1275.00')
for r in p.rate:
    print(r.nome, r.numero_rate, r.importo_rata)
```

## Configurazione (`config.toml`)

Tutti i parametri stanno in [`config.toml`](config.toml): per cambiare prezzi,
sconto o rate si modifica solo quel file. Si può usare un file diverso con
`--config percorso/altro.toml`.

| Sezione | Cosa contiene |
|---------|---------------|
| `[listino]` | `arrotondamento` del prezzo pieno: `"euro"` o `"centesimi"`. |
| `[listino.prodotti.<codice>]` | `nome` e **uno** tra `prezzo_mq` (€/m²) e `prezzo_fisso` (€ a pezzo). |
| `[sconto_fine_anno]` | `percentuale`, `valido_dal`, `valido_al` (date AAAA-MM-GG senza virgolette, estremi inclusi), `arrotondamento`. |
| `[[rate]]` | Un blocco per piano: `codice`, `nome`, `numero_rate` e, solo per il noleggio, `coefficiente`. |

I prezzi al m² e i coefficienti Grenke di partenza sono quelli del calcolatore
pubblicato su ideamkt.it (`wp-pages/preventivi-ledwall.html`). Lo sconto del 15%
dal 1° novembre al 31 dicembre 2026 e i piani a 3, 6 e 12 rate sono valori di
esempio: **controllali e correggili** prima di usarli con i clienti.

Se il file contiene un errore (prezzo mancante, date invertite, percentuale
fuori range…) il programma si ferma e dice quale riga sistemare.

## Come vengono fatti i conti

1. **Superficie** = larghezza × altezza in cm ÷ 10.000 (m²).
2. **Prezzo pieno** = superficie × prezzo al m² (oppure il prezzo fisso),
   arrotondato all'euro.
3. **Prezzo scontato** = prezzo pieno − percentuale di sconto, arrotondato
   all'euro. Fuori dal periodo della promo è uguale al prezzo pieno e
   l'importo non va barrato.
4. **Rate senza interessi**: rata = prezzo scontato ÷ numero rate, al centesimo.
   L'ultima rata assorbe gli eventuali centesimi di differenza (es. 1.000 € in
   3 rate = 333,33 + 333,33 + 333,34), così il totale torna sempre.
5. **Noleggio Grenke**: canone = prezzo scontato × coefficiente, arrotondato
   all'euro **per eccesso**, come fa il calcolatore del sito.

## Test

```bash
cd preventivi-ledwall
python3 -m unittest discover -s tests -v
```
