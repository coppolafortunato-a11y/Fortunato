import datetime as dt
import io
import tomllib
import unittest
from contextlib import redirect_stdout
from decimal import Decimal as D

from preventivi_ledwall import ErroreConfigurazione, calcola_preventivo, carica_configurazione
from preventivi_ledwall.__main__ import euro, main
from preventivi_ledwall.config import CONFIG_PREDEFINITA, configurazione_da_dict

IN_PROMO = dt.date(2026, 12, 1)
FUORI_PROMO = dt.date(2027, 1, 15)


def dati_base():
    with open(CONFIG_PREDEFINITA, "rb") as f:
        return tomllib.load(f)


class TestPrezzi(unittest.TestCase):
    def setUp(self):
        self.config = carica_configurazione()

    def test_prezzo_pieno_a_mq(self):
        # 200x100 cm = 2 m² x 750 €/m² (stesso risultato del calcolatore sul sito)
        p = calcola_preventivo(self.config, "outdoor_p6", 200, 100, IN_PROMO)
        self.assertEqual(p.superficie_mq, D("2.00"))
        self.assertEqual(p.prezzo_pieno, D("1500.00"))

    def test_prezzo_pieno_arrotondato_all_euro(self):
        # 155x95 cm = 1,4725 m² x 1800 = 2650,50 -> 2651
        p = calcola_preventivo(self.config, "indoor_p25", 155, 95, IN_PROMO)
        self.assertEqual(p.prezzo_pieno, D("2651.00"))

    def test_sconto_fine_anno_attivo(self):
        p = calcola_preventivo(self.config, "outdoor_p6", 200, 100, IN_PROMO)
        self.assertTrue(p.sconto_attivo)
        self.assertEqual(p.sconto_percentuale, D("15"))
        self.assertEqual(p.prezzo_scontato, D("1275.00"))
        self.assertEqual(p.risparmio, D("225.00"))

    def test_sconto_estremi_inclusi(self):
        for giorno in (dt.date(2026, 11, 1), dt.date(2026, 12, 31)):
            self.assertTrue(calcola_preventivo(self.config, "totem", data=giorno).sconto_attivo)
        self.assertFalse(calcola_preventivo(self.config, "totem", data=dt.date(2026, 10, 31)).sconto_attivo)

    def test_fuori_periodo_nessuno_sconto(self):
        p = calcola_preventivo(self.config, "outdoor_p6", 200, 100, FUORI_PROMO)
        self.assertFalse(p.sconto_attivo)
        self.assertEqual(p.prezzo_scontato, p.prezzo_pieno)
        self.assertEqual(p.risparmio, D("0"))
        self.assertEqual(p.sconto_percentuale, D("0"))

    def test_prezzo_fisso_ignora_misure(self):
        p = calcola_preventivo(self.config, "totem", data=IN_PROMO)
        self.assertEqual(p.prezzo_pieno, D("2800.00"))
        self.assertEqual(p.prezzo_scontato, D("2380.00"))
        self.assertIsNone(p.superficie_mq)

    def test_errori_di_input(self):
        with self.assertRaises(ValueError):
            calcola_preventivo(self.config, "inesistente", 100, 100)
        with self.assertRaises(ValueError):
            calcola_preventivo(self.config, "outdoor_p6")
        with self.assertRaises(ValueError):
            calcola_preventivo(self.config, "outdoor_p6", 0, 100)


class TestRate(unittest.TestCase):
    def setUp(self):
        self.config = carica_configurazione()

    def rate(self, prev):
        return {r.codice: r for r in prev.rate}

    def test_rate_senza_interessi_sommano_al_prezzo(self):
        prev = calcola_preventivo(self.config, "outdoor_p6", 200, 100, IN_PROMO)  # 1275
        r = self.rate(prev)
        self.assertEqual((r["rate3"].numero_rate, r["rate3"].importo_rata), (3, D("425.00")))
        # 1275 / 12 = 106,25 esatto
        self.assertEqual(r["rate12"].importo_rata, D("106.25"))
        for piano in prev.rate:
            if not piano.noleggio:
                totale = piano.importo_rata * (piano.numero_rate - 1) + piano.importo_ultima_rata
                self.assertEqual(totale, prev.prezzo_scontato)
                self.assertEqual(piano.totale, prev.prezzo_scontato)

    def test_ultima_rata_assorbe_i_centesimi(self):
        # 1000 / 3 = 333,33 + 333,33 + 333,34
        dati = dati_base()
        dati["listino"]["prodotti"] = {"x": {"nome": "X", "prezzo_fisso": 1000}}
        dati["sconto_fine_anno"]["percentuale"] = 0
        prev = calcola_preventivo(configurazione_da_dict(dati), "x", data=IN_PROMO)
        r = self.rate(prev)["rate3"]
        self.assertEqual(r.importo_rata, D("333.33"))
        self.assertEqual(r.importo_ultima_rata, D("333.34"))

    def test_canone_grenke_come_sul_sito(self):
        # Sul sito: Math.ceil(base * coeff). 1275 x 0,0335 = 42,7125 -> 43
        prev = calcola_preventivo(self.config, "outdoor_p6", 200, 100, IN_PROMO)
        g = self.rate(prev)["grenke36"]
        self.assertTrue(g.noleggio)
        self.assertEqual((g.numero_rate, g.importo_rata, g.totale), (36, D("43.00"), D("1548.00")))
        self.assertEqual(self.rate(prev)["grenke60"].importo_rata, D("30.00"))  # 29,07 -> 30

    def test_rate_calcolate_sul_prezzo_pieno_fuori_promo(self):
        prev = calcola_preventivo(self.config, "outdoor_p6", 200, 100, FUORI_PROMO)  # 1500
        self.assertEqual(self.rate(prev)["rate3"].importo_rata, D("500.00"))


class TestConfigurazione(unittest.TestCase):
    def test_config_predefinita_valida(self):
        c = carica_configurazione()
        self.assertIn("outdoor_p6", c.prodotti)
        self.assertEqual(c.rate[3].coefficiente, D("0.0335"))

    def test_prodotto_con_due_prezzi(self):
        dati = dati_base()
        dati["listino"]["prodotti"]["totem"]["prezzo_mq"] = 10
        with self.assertRaises(ErroreConfigurazione):
            configurazione_da_dict(dati)

    def test_percentuale_fuori_range(self):
        dati = dati_base()
        dati["sconto_fine_anno"]["percentuale"] = 100
        with self.assertRaises(ErroreConfigurazione):
            configurazione_da_dict(dati)

    def test_date_invertite(self):
        dati = dati_base()
        dati["sconto_fine_anno"]["valido_dal"] = dt.date(2027, 1, 1)
        with self.assertRaises(ErroreConfigurazione):
            configurazione_da_dict(dati)

    def test_numero_rate_non_valido(self):
        dati = dati_base()
        dati["rate"][0]["numero_rate"] = 0
        with self.assertRaises(ErroreConfigurazione):
            configurazione_da_dict(dati)

    def test_arrotondamento_centesimi(self):
        dati = dati_base()
        dati["listino"]["arrotondamento"] = "centesimi"
        dati["sconto_fine_anno"]["arrotondamento"] = "centesimi"
        prev = calcola_preventivo(configurazione_da_dict(dati), "indoor_p25", 155, 95, IN_PROMO)
        self.assertEqual(prev.prezzo_pieno, D("2650.50"))
        self.assertEqual(prev.prezzo_scontato, D("2252.93"))  # 2252,925 -> 2252,93


class TestRigaDiComando(unittest.TestCase):
    def test_formato_euro(self):
        self.assertEqual(euro(D("1234.5")), "1.234,50 €")

    def test_output(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            codice = main(["outdoor_p6", "200", "100", "--data", "2026-12-01"])
        self.assertEqual(codice, 0)
        testo = buf.getvalue()
        self.assertIn("1.500,00 €  (barrato)", testo)
        self.assertIn("1.275,00 €", testo)
        self.assertIn("36 × 43,00 €", testo)


if __name__ == "__main__":
    unittest.main()
