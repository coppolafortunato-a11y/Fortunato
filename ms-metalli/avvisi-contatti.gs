/**
 * MS Metalli — avviso immediato per ogni nuovo contatto arrivato da Meta.
 *
 * Va incollato nell'editor Apps Script COLLEGATO al foglio
 * "MS Metalli - Contatti da Meta" (Estensioni → Apps Script).
 * Istruzioni complete nel README.md di questa cartella.
 *
 * Cosa fa:
 *  - controlla il foglio ogni minuto (e subito a ogni modifica);
 *  - per ogni riga nuova manda un'email con nome, città, tipo cliente,
 *    metallo, kg e una stima del valore calcolata col LISTINO qui sotto;
 *  - nell'email mette il testo pronto per WhatsApp e il link per scrivere
 *    subito al venditore;
 *  - salta il contatto finto di prova che Meta inserisce ("<test lead: ...>").
 */

// ============================================================
// IMPOSTAZIONI — modifica solo questa parte
// ============================================================

/**
 * Listino d'acquisto in €/kg. Le chiavi sono le parole cercate nella
 * risposta "che tipo di metalli?" (maiuscole/minuscole non contano).
 * Metti le parole più specifiche prima (es. "acciaio inox" prima di "acciaio").
 * Le voci diverse da rame e ottone sono indicative: aggiornale coi tuoi prezzi.
 */
const LISTINO = {
  'rame': 9.0,
  'ottone': 4.0,
  'alluminio': 1.2,   // da verificare
  'acciaio inox': 1.0, // da verificare
  'inox': 1.0,        // da verificare
  'piombo': 1.5,      // da verificare
  'zinco': 1.8,       // da verificare
  'ferro': 0.25,      // da verificare
};

/** Altri nomi con cui la gente scrive i metalli → voce del listino. */
const SINONIMI = {
  'alluminium': 'alluminio',
  'allumino': 'alluminio',
  'acciaio': 'acciaio inox',
  // Esempi da attivare se ti servono (togli // all'inizio):
  // 'cavi': 'rame',      // attenzione: i cavi rivestiti valgono meno del rame pulito
  // 'rottami': 'ferro',
};

/**
 * A chi mandare l'avviso. Lascia vuoto per usare l'indirizzo dell'account
 * Google che installa lo script. Più indirizzi: separali con la virgola.
 */
const EMAIL_DESTINATARIO = '';

/** Nome della scheda del foglio dove arrivano i contatti. */
const NOME_SCHEDA = 'Foglio1';

/** Prefisso internazionale usato quando il numero non ce l'ha. */
const PREFISSO_PAESE = '39';

/** Messaggio iniziale proposto per scrivere al venditore su WhatsApp. */
const SALUTO_WHATSAPP =
  'Buongiorno {nome}, sono di MS Metalli. Ci ha scritto per vendere {metallo}{kg}: ' +
  'quando possiamo sentirci per una valutazione?';

// ============================================================
// FINE IMPOSTAZIONI
// ============================================================

const CHIAVE_ULTIMA_RIGA = 'MS_METALLI_ULTIMA_RIGA';

/**
 * Da lanciare UNA volta a mano dall'editor: crea i trigger e segna come
 * "già visti" i contatti presenti adesso, così non arrivano avvisi vecchi.
 */
function installa() {
  const foglio = scheda_();
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'controllaNuoviContatti') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('controllaNuoviContatti').timeBased().everyMinutes(1).create();
  ScriptApp.newTrigger('controllaNuoviContatti')
    .forSpreadsheet(foglio.getParent()).onChange().create();
  PropertiesService.getScriptProperties()
    .setProperty(CHIAVE_ULTIMA_RIGA, String(foglio.getLastRow()));
  Logger.log('Installato. Contatti già presenti ignorati fino alla riga ' + foglio.getLastRow() + '.');
}

/** Toglie i trigger (per spegnere gli avvisi). */
function disinstalla() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'controllaNuoviContatti') ScriptApp.deleteTrigger(t);
  });
  Logger.log('Avvisi spenti.');
}

/** Manda un avviso di prova usando l'ultima riga vera del foglio (o dati finti). */
function provaAvviso() {
  const foglio = scheda_();
  const dati = foglio.getDataRange().getValues();
  const intestazioni = dati[0];
  let contatto = null;
  for (let r = dati.length - 1; r >= 1 && !contatto; r--) {
    const c = leggiContatto_(intestazioni, dati[r]);
    if (!eRigaVuota_(c) && !eContattoDiProva_(c)) contatto = c;
  }
  if (!contatto) {
    contatto = {
      nome: 'Mario Rossi', citta: 'Reggio Calabria', tipo: 'Privato',
      metallo: 'Rame', kg: '150', telefono: '3331234567', email: '', data: new Date(),
    };
  }
  inviaAvviso_(contatto, true);
  Logger.log('Avviso di prova inviato a ' + destinatario_());
}

/** Chiamata dai trigger: manda un avviso per ogni riga nuova. */
function controllaNuoviContatti() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(20000)) return; // un altro controllo è già in corso
  try {
    const props = PropertiesService.getScriptProperties();
    const foglio = scheda_();
    const ultimaRiga = foglio.getLastRow();
    let giaViste = Number(props.getProperty(CHIAVE_ULTIMA_RIGA));
    if (!giaViste && giaViste !== 0) giaViste = ultimaRiga; // mai installato: non spammare
    if (ultimaRiga < giaViste) giaViste = ultimaRiga;       // righe cancellate
    if (ultimaRiga <= giaViste) {
      props.setProperty(CHIAVE_ULTIMA_RIGA, String(giaViste));
      return;
    }

    const colonne = foglio.getLastColumn();
    const intestazioni = foglio.getRange(1, 1, 1, colonne).getValues()[0];
    const righe = foglio.getRange(giaViste + 1, 1, ultimaRiga - giaViste, colonne).getValues();

    for (let i = 0; i < righe.length; i++) {
      const contatto = leggiContatto_(intestazioni, righe[i]);
      if (!eRigaVuota_(contatto) && !eContattoDiProva_(contatto)) inviaAvviso_(contatto, false);
      // avanza riga per riga: se un invio fallisce, le righe già avvisate non si ripetono
      props.setProperty(CHIAVE_ULTIMA_RIGA, String(giaViste + i + 1));
    }
  } finally {
    lock.releaseLock();
  }
}

// ------------------------------------------------------------
// Lettura del foglio
// ------------------------------------------------------------

function scheda_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const s = ss.getSheetByName(NOME_SCHEDA) || ss.getSheets()[0];
  return s;
}

/** Normalizza un'intestazione: minuscole, senza accenti né simboli. */
function pulisci_(testo) {
  return String(testo || '')
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

/**
 * Trova le colonne per nome (non per posizione), così lo script continua a
 * funzionare anche se Meta cambia l'ordine o il testo delle domande.
 */
function leggiContatto_(intestazioni, riga) {
  const h = intestazioni.map(pulisci_);
  function col(test) {
    for (let i = 0; i < h.length; i++) if (test(h[i])) return riga[i];
    return '';
  }
  function testo(v) { return v === null || v === undefined ? '' : String(v).trim(); }
  return {
    nome: testo(col(function (x) { return x.indexOf('nome') >= 0 || x === 'full name'; })),
    citta: testo(col(function (x) { return x.indexOf('citta') >= 0 || x === 'city'; })),
    tipo: testo(col(function (x) { return x.indexOf('impresa') >= 0 || x.indexOf('privato') >= 0; })),
    metallo: testo(col(function (x) { return x.indexOf('metall') >= 0; })),
    kg: testo(col(function (x) { return /\bkg\b/.test(x); })),
    telefono: testo(col(function (x) { return x.indexOf('telefono') >= 0 || x.indexOf('phone') >= 0; }))
      .replace(/^p:/i, ''),
    email: testo(col(function (x) { return x === 'e mail' || x === 'email'; })),
    data: col(function (x) { return x === 'created time'; }),
  };
}

function eRigaVuota_(c) {
  return !c.nome && !c.telefono && !c.metallo && !c.email;
}

/** Il contatto finto che Meta inserisce quando si prova il modulo. */
function eContattoDiProva_(c) {
  const tutto = [c.nome, c.citta, c.tipo, c.metallo, c.kg, c.telefono, c.email].join(' ').toLowerCase();
  return tutto.indexOf('<test lead') >= 0 || tutto.indexOf('dummy data') >= 0 ||
    c.email.toLowerCase() === 'test@meta.com';
}

// ------------------------------------------------------------
// Stima del valore
// ------------------------------------------------------------

/** "200", "circa 200 kg", "1.500", "100-200", "mezza tonnellata"… → numero di kg (o null). */
function interpretaKg_(testo) {
  const t = String(testo || '').toLowerCase().replace(/\s+/g, ' ');
  if (!t) return null;
  const numeri = (t.match(/\d+(?:[.,]\d+)*/g) || []).map(function (n) {
    // "1.500" e "1,500" → 1500; "1,5" → 1.5
    if (/^\d{1,3}([.,]\d{3})+$/.test(n)) return Number(n.replace(/[.,]/g, ''));
    return Number(n.replace(',', '.'));
  }).filter(function (n) { return !isNaN(n); });
  let kg;
  if (numeri.length >= 2 && /\d\s*(-|–|a)\s*\d/.test(t)) kg = (numeri[0] + numeri[1]) / 2; // intervallo
  else if (numeri.length) kg = numeri[0];
  else if (t.indexOf('mezza tonnellata') >= 0) kg = 500;
  else return null;
  if (/\b(t|ton|tonn|tonnellat[ae])\b/.test(t) || t.indexOf('tonnellat') >= 0) kg = kg * 1000;
  else if (/\bq(uintal[ei])?\b/.test(t)) kg = kg * 100;
  return kg;
}

/** Trova nel testo i metalli del listino. Restituisce [{nome, prezzo}]. */
function trovaMetalli_(testo) {
  let t = ' ' + pulisci_(testo) + ' ';
  const trovati = [];
  function aggiungi(voce) {
    if (LISTINO[voce] === undefined) return;
    if (trovati.some(function (m) { return m.nome === voce; })) return;
    trovati.push({ nome: voce, prezzo: LISTINO[voce] });
  }
  Object.keys(LISTINO).forEach(function (voce) {
    const p = ' ' + pulisci_(voce) + ' ';
    if (t.indexOf(p) >= 0) { aggiungi(voce); t = t.split(p).join(' '); }
  });
  Object.keys(SINONIMI).forEach(function (s) {
    if (t.indexOf(' ' + pulisci_(s) + ' ') >= 0) aggiungi(SINONIMI[s]);
  });
  return trovati;
}

function euro_(n) {
  return '€ ' + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

/** Testo della stima, es. "€ 1.800 (200 kg × 9 €/kg rame)". */
function stimaValore_(c) {
  const kg = interpretaKg_(c.kg);
  const metalli = trovaMetalli_(c.metallo);
  if (!metalli.length) return 'non disponibile (metallo non nel listino)';
  if (kg === null) return 'non disponibile (kg non indicati)';
  const kgTxt = String(Math.round(kg * 10) / 10).replace('.', ',') + ' kg';
  if (metalli.length === 1) {
    const m = metalli[0];
    return euro_(kg * m.prezzo) + ' (' + kgTxt + ' × ' + String(m.prezzo).replace('.', ',') + ' €/kg ' + m.nome + ')';
  }
  const prezzi = metalli.map(function (m) { return m.prezzo; });
  const min = Math.min.apply(null, prezzi), max = Math.max.apply(null, prezzi);
  return 'tra ' + euro_(kg * min) + ' e ' + euro_(kg * max) + ' (' + kgTxt + ', metalli misti: ' +
    metalli.map(function (m) { return m.nome; }).join(', ') + ')';
}

// ------------------------------------------------------------
// Avviso
// ------------------------------------------------------------

function destinatario_() {
  return EMAIL_DESTINATARIO || Session.getEffectiveUser().getEmail();
}

function numeroInternazionale_(tel) {
  let n = String(tel || '').replace(/[^\d+]/g, '');
  if (!n) return '';
  if (n.indexOf('+') === 0) return n.slice(1);
  if (n.indexOf('00') === 0) return n.slice(2);
  if (n.indexOf(PREFISSO_PAESE) === 0 && n.length > 10) return n;
  return PREFISSO_PAESE + n;
}

/** Il testo dell'avviso, pronto da copiare su WhatsApp. */
function testoAvviso_(c) {
  return [
    '🔔 NUOVO CONTATTO MS METALLI',
    '👤 ' + (c.nome || '—'),
    '📍 ' + (c.citta || '—'),
    '🏷️ ' + (c.tipo || '—'),
    '🔩 ' + (c.metallo || '—'),
    '⚖️ ' + (c.kg ? c.kg + (/kg/i.test(c.kg) ? '' : ' kg') : '—'),
    '💶 Valore stimato: ' + stimaValore_(c),
    '📞 ' + (c.telefono || '—'),
  ].join('\n');
}

function linkWhatsApp_(c) {
  const numero = numeroInternazionale_(c.telefono);
  if (!numero) return '';
  const msg = SALUTO_WHATSAPP
    .replace('{nome}', (c.nome || '').split(' ')[0])
    .replace('{metallo}', (c.metallo || 'metalli').toLowerCase())
    .replace('{kg}', c.kg ? ' (' + (/circa|incirca/i.test(c.kg) ? '' : 'circa ') + c.kg + (/kg/i.test(c.kg) ? '' : ' kg') + ')' : '');
  return 'https://wa.me/' + numero + '?text=' + encodeURIComponent(msg);
}

function html_(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function inviaAvviso_(c, prova) {
  const testo = testoAvviso_(c);
  const wa = linkWhatsApp_(c);
  const numero = numeroInternazionale_(c.telefono);
  const condividi = 'https://wa.me/?text=' + encodeURIComponent(testo);
  const oggetto = (prova ? '[PROVA] ' : '') + '🔔 MS Metalli: ' + (c.nome || 'nuovo contatto') +
    ' — ' + (c.metallo || 'metallo ?') + (c.kg ? ', ' + c.kg + (/kg/i.test(c.kg) ? '' : ' kg') : '') +
    ' — ' + stimaValore_(c).split(' (')[0];

  const corpoTesto = testo + '\n\n' +
    (wa ? 'Scrivi al venditore su WhatsApp: ' + wa + '\n' : '') +
    (numero ? 'Chiama: +' + numero + '\n' : '') +
    'Inoltra questo avviso su WhatsApp: ' + condividi + '\n';

  const bottone = function (url, etichetta, colore) {
    return '<a href="' + html_(url) + '" style="display:inline-block;margin:4px 8px 4px 0;padding:10px 16px;' +
      'background:' + colore + ';color:#fff;text-decoration:none;border-radius:6px;font-weight:bold">' +
      etichetta + '</a>';
  };
  const corpoHtml =
    '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5">' +
    '<pre style="font-family:inherit;font-size:16px;white-space:pre-wrap;margin:0 0 12px">' + html_(testo) + '</pre>' +
    (wa ? bottone(wa, 'Scrivi su WhatsApp', '#25D366') : '') +
    (numero ? bottone('tel:+' + numero, 'Chiama', '#1a73e8') : '') +
    bottone(condividi, 'Inoltra l\'avviso su WhatsApp', '#555') +
    (c.email ? '<p>Email del contatto: ' + html_(c.email) + '</p>' : '') +
    '<p style="color:#888;font-size:12px">Il testo qui sopra è pronto da copiare e incollare su WhatsApp. ' +
    'La stima usa il listino nello script MS Metalli.</p></div>';

  MailApp.sendEmail({
    to: destinatario_(),
    subject: oggetto,
    body: corpoTesto,
    htmlBody: corpoHtml,
    name: 'Avvisi MS Metalli',
  });
}

// Per i test in locale con Node (in Apps Script questa riga non fa nulla).
if (typeof module !== 'undefined') {
  module.exports = {
    leggiContatto_: leggiContatto_, eContattoDiProva_: eContattoDiProva_, eRigaVuota_: eRigaVuota_,
    interpretaKg_: interpretaKg_, trovaMetalli_: trovaMetalli_, stimaValore_: stimaValore_,
    testoAvviso_: testoAvviso_, linkWhatsApp_: linkWhatsApp_, numeroInternazionale_: numeroInternazionale_,
  };
}
