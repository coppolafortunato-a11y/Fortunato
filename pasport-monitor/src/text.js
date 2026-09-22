'use strict';

/** Normalizza per il confronto: minuscole, spazi unificati, apostrofi/trattini uniformi. */
function normalizeText(s) {
  return String(s || '')
    .replace(/ /g, ' ')
    .replace(/[‘’ʼ′]/g, "'")
    .replace(/[‐-―−]/g, '-')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

const UA_MONTHS = {
  'січня': 1, 'січень': 1, 'лютого': 2, 'лютий': 2, 'березня': 3, 'березень': 3,
  'квітня': 4, 'квітень': 4, 'травня': 5, 'травень': 5, 'червня': 6, 'червень': 6,
  'липня': 7, 'липень': 7, 'серпня': 8, 'серпень': 8, 'вересня': 9, 'вересень': 9,
  'жовтня': 10, 'жовтень': 10, 'листопада': 11, 'листопад': 11, 'грудня': 12, 'грудень': 12,
};

/**
 * Estrae una data ISO (YYYY-MM-DD) da un'etichetta del menu "Обрати день".
 * Gestisce dd.mm.yyyy, dd/mm/yyyy, yyyy-mm-dd e "22 жовтня 2026".
 * Restituisce null se la stringa non contiene una data reale (es. un placeholder).
 */
function parseDate(raw, fallbackYear) {
  const s = normalizeText(raw);
  if (!s) return null;

  let m = s.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (m) return iso(+m[1], +m[2], +m[3]);

  m = s.match(/(\d{1,2})[.\/-](\d{1,2})[.\/-](\d{4})/);
  if (m) return iso(+m[3], +m[2], +m[1]);

  m = s.match(/(\d{1,2})\s+([а-яіїєґ']+)\s*(\d{4})?/);
  if (m && UA_MONTHS[m[2]]) {
    const year = m[3] ? +m[3] : (fallbackYear || new Date().getFullYear());
    return iso(year, UA_MONTHS[m[2]], +m[1]);
  }

  // dd.mm senza anno: deduciamo l'anno più vicino nel futuro.
  m = s.match(/\b(\d{1,2})[.\/](\d{1,2})\b/);
  if (m) {
    const now = new Date();
    let year = fallbackYear || now.getFullYear();
    const candidate = iso(year, +m[2], +m[1]);
    if (candidate && new Date(candidate) < now) year += 1;
    return iso(year, +m[2], +m[1]);
  }

  return null;
}

function iso(y, mo, d) {
  if (!(y >= 2000 && y <= 2100) || !(mo >= 1 && mo <= 12) || !(d >= 1 && d <= 31)) return null;
  return `${y}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

/** Estrae un orario HH:MM da un'etichetta del menu "Обрати час". */
function parseTime(raw) {
  const m = String(raw || '').match(/\b(\d{1,2})[:.](\d{2})\b/);
  if (!m) return null;
  const h = +m[1], min = +m[2];
  if (h > 23 || min > 59) return null;
  return `${String(h).padStart(2, '0')}:${String(min).padStart(2, '0')}`;
}

/** Numero di posti, se il sito lo indica accanto all'orario (es. "10:30 (3)"). */
function parseSlots(raw) {
  const m = String(raw || '').match(/\((\d+)\)|(\d+)\s*(?:місц|вільн)/i);
  if (!m) return null;
  return Number(m[1] || m[2]);
}

/** Converte YYYY-MM-DD in DD/MM/YYYY per le notifiche. */
function formatDateIt(isoDate) {
  const m = String(isoDate).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  return m ? `${m[3]}/${m[2]}/${m[1]}` : String(isoDate);
}

module.exports = { normalizeText, parseDate, parseTime, parseSlots, formatDateIt };
