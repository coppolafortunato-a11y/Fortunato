'use strict';

const fs = require('fs');
const path = require('path');
const config = require('./config');

/**
 * Stato persistente: per ogni centro, le date note e gli orari noti per data.
 * Formato:
 *   { centers: { krakow: { dates: [], times: { "2026-10-22": ["10:30"] },
 *                          lastStatus: "FULL", errorStreak: 0 } } }
 */
function emptyCenter() {
  return { dates: [], times: {}, lastStatus: null, errorStreak: 0, lastCheck: null };
}

function load() {
  try {
    const raw = fs.readFileSync(config.paths.state, 'utf8');
    const parsed = JSON.parse(raw);
    if (parsed && parsed.centers) return normalize(parsed);
  } catch (err) {
    if (err.code !== 'ENOENT') {
      console.error(`Stato illeggibile (${err.message}), riparto da uno stato vuoto.`);
    }
  }
  return normalize({ centers: {} });
}

function normalize(state) {
  state.centers = state.centers || {};
  for (const c of config.CENTERS) {
    state.centers[c.id] = Object.assign(emptyCenter(), state.centers[c.id]);
  }
  return state;
}

function save(state) {
  fs.mkdirSync(path.dirname(config.paths.state), { recursive: true });
  const tmp = `${config.paths.state}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(state, null, 2));
  fs.renameSync(tmp, config.paths.state); // scrittura atomica: niente stato corrotto
}

/**
 * Confronta il risultato di un controllo con lo stato memorizzato.
 * Restituisce { newDates, newTimes, reopened } — vuoto se non c'è nulla di nuovo.
 *
 * Notifichiamo quando: compare una data mai vista, compare un orario nuovo su una
 * data già nota, oppure un centro prima pieno torna ad avere disponibilità.
 */
function diff(previous, current) {
  const knownDates = new Set(previous.dates || []);
  const newDates = current.dates.filter((d) => !knownDates.has(d));

  const newTimes = {};
  for (const [date, times] of Object.entries(current.times || {})) {
    const known = new Set((previous.times && previous.times[date]) || []);
    const fresh = times.filter((t) => !known.has(t));
    if (fresh.length) newTimes[date] = fresh;
  }

  const reopened =
    previous.lastStatus === 'FULL' && current.dates.length > 0 && newDates.length === 0;

  const hasNews = newDates.length > 0 || Object.keys(newTimes).length > 0 || reopened;
  return { newDates, newTimes, reopened, hasNews };
}

/** Fonde il risultato corrente nello stato (le date scomparse vengono rimosse). */
function merge(state, centerId, current) {
  const entry = state.centers[centerId] || emptyCenter();
  entry.dates = current.dates.slice().sort();
  const times = {};
  for (const d of entry.dates) {
    const fresh = (current.times && current.times[d]) || [];
    const old = entry.times[d] || [];
    times[d] = Array.from(new Set([...old, ...fresh])).sort();
  }
  entry.times = times;
  entry.lastStatus = current.status;
  entry.lastCheck = new Date().toISOString();
  entry.errorStreak = current.status === 'ERROR' ? (entry.errorStreak || 0) + 1 : 0;
  state.centers[centerId] = entry;
  return entry;
}

module.exports = { load, save, diff, merge, emptyCenter };
