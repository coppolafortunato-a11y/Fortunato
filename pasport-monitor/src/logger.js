'use strict';

const fs = require('fs');
const path = require('path');
const config = require('./config');

fs.mkdirSync(config.paths.logDir, { recursive: true });

/** "2026-09-22 14:15" — formato richiesto per il log leggibile. */
function stamp(d = new Date()) {
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

function write(line) {
  const text = `${line}\n`;
  process.stdout.write(text);
  fs.appendFileSync(config.paths.logFile, text);
}

/** Riga informativa generica. */
function info(message) {
  write(`${stamp()} | ${message}`);
}

/**
 * Riga di esito per un centro, nel formato:
 *   2026-09-22 14:16 | Gdansk | 22/10/2026
 */
function result(centerName, summary) {
  write(`${stamp()} | ${centerName} | ${summary}`);
}

/** Record strutturato, una riga JSON per controllo: serve per analisi a posteriori. */
function record(entry) {
  fs.appendFileSync(config.paths.jsonlFile, JSON.stringify({ ts: new Date().toISOString(), ...entry }) + '\n');
}

module.exports = { info, result, record, stamp };
