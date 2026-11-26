// ============================================================
// MS Metalli - stima del valore nell'email "Nuovo contatto MS Metalli"
//
// Questo blocco SOSTITUISCE, nello script collegato al foglio
// "MS Metalli - Contatti da Meta" (Estensioni > Apps Script, file Codice.gs),
// tutto il pezzo che va da "// Listino di Marco Russo a noi (31/10)"
// fino alla fine della funzione stimaValore (la "}" prima di "function avvisa").
// Il resto dello script resta com'è.
//
// Cosa corregge:
//  - i kg scritti come intervallo ("50 - 200 kg") prima diventavano 50200 kg:
//    ora si prende il MASSIMO dell'intervallo (200 kg);
//  - prezzi aggiornati alle locandine di Marco del 24/11/2026;
//  - la fascia si sceglie col valore del materiale (soglia 1.500 €),
//    non più coi kg (500 kg);
//  - oltre al valore al prezzo di Marco, mostra anche il prezzo massimo
//    da offrire al cliente (prezzo Marco meno il margine di Fortunato).
// ============================================================

// Listino Marco Russo a noi (locandine 24/11/2026), in €/kg:
// [parole cercate, nome, fino a 1.500 €, sopra 1.500 €, margine Fortunato]
// L'ordine conta: le voci più specifiche vanno prima (es. "cavi" prima di "rame").
const LISTINO = [
  [/cav[io]|fil[io]\s*elettric/i, 'cavi', 2.00, 2.30, 0.50],
  [/cordin/i, 'cordina', 2.50, 3.00, 0.50],
  [/caldai/i, 'caldaiette', 7.60, 7.80, 1.00],
  [/radiator|termosifon|calorifer/i, 'radiatori rame/alluminio (non ghisa)', 2.50, 2.70, 0.50],
  [/rame\s*(3|iii|terz)/i, 'rame 3', 8.00, 8.20, 1.00],
  [/rame\s*(2|ii|second)/i, 'rame 2', 8.30, 8.50, 1.00],
  [/stagnat/i, 'rame stagnato', 8.20, 8.40, 1.00],
  [/rame|eame/i, 'rame 1', 8.50, 8.70, 1.00],
  [/campagnolo/i, 'ottone Campagnolo', 4.40, 4.60, 0.50],
  [/ottone/i, 'ottone giallo', 4.60, 4.80, 0.50],
  [/bronzo/i, 'bronzo', 4.80, 5.00, 1.00],
  [/widia/i, 'widia', 25.00, 30.00, 1.00],
  [/piombo/i, 'piombo', 0.70, 0.70, 0.40],
];

// Soglia delle due locandine di Marco: valore del materiale fino a / sopra 1.500 €.
const SOGLIA_LISTINO_EURO = 1500;

// "50 - 200 kg" -> 200, "200-500" -> 500, "<50" -> 50, "1.500" -> 1500,
// "circa 80" -> 80, "1,5 t" -> 1500. Se ci sono più numeri si prende il più alto.
function leggiKg(kg) {
  const t = String(kg || '').toLowerCase();
  const numeri = (t.match(/\d+(?:[.,]\d+)*/g) || []).map(function (s) {
    if (/^\d{1,3}([.,]\d{3})+$/.test(s)) return Number(s.replace(/[.,]/g, '')); // 1.500
    return Number(s.replace(',', '.'));                                        // 1,5
  }).filter(function (n) { return !isNaN(n) && n > 0; });
  if (!numeri.length) return 0;
  let n = Math.max.apply(null, numeri);
  if (/\bt\b|ton/.test(t)) n = n * 1000;
  else if (/quintal|\bq\b/.test(t)) n = n * 100;
  return n;
}

// 1800 -> "1.800"
function euroIt(n) {
  return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function prezzoIt(p) {
  return p.toFixed(2).replace('.', ',');
}

// Stima indicativa: kg scritti dal cliente (il massimo, se è un intervallo)
// x prezzo che Marco paga a noi. La fascia (fino a / sopra 1.500 €) si sceglie
// col valore del materiale.
function stimaValore(metalli, kg) {
  const n = leggiKg(kg);
  const voce = LISTINO.find(function (v) { return v[0].test(metalli); });
  if (!n || !voce) return '';
  const sopra = n * voce[2] > SOGLIA_LISTINO_EURO;
  const prezzoMarco = sopra ? voce[3] : voce[2];
  const prezzoCliente = prezzoMarco - voce[4];
  const fascia = sopra ? 'listino sopra 1.500 €' : 'listino fino a 1.500 €';
  return 'fino a ' + euroIt(n * prezzoMarco) + ' € se è ' + voce[1]
    + ' (' + euroIt(n) + ' kg x ' + prezzoIt(prezzoMarco) + ' €/kg, ' + fascia + ')'
    + '\nPrezzo massimo al cliente: ' + prezzoIt(prezzoCliente) + ' €/kg'
    + ' (margine Fortunato ' + prezzoIt(voce[4]) + ' €/kg, circa ' + euroIt(n * voce[4]) + ' €)';
}

// ------------------------------------------------------------
// Nella funzione avvisa, cambia anche la riga
//     valore ? 'Valore per noi: ' + valore : '',
// in
//     valore ? 'Valore al prezzo di Marco: ' + valore : '',
// ------------------------------------------------------------

// Per i test in locale con Node (in Apps Script questa riga non fa nulla).
if (typeof module !== 'undefined') {
  module.exports = { leggiKg: leggiKg, stimaValore: stimaValore };
}
