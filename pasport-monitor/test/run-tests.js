'use strict';

/** Test end-to-end del checker contro il sito di prova locale. */
const assert = require('assert');
const { start } = require('./mock-site');
const { launch } = require('../src/browser');
const { checkCenter } = require('../src/checker');
const state = require('../src/state');

(async () => {
  const server = await start(8731);
  const { browser, context } = await launch();
  let failures = 0;
  const check = (name, fn) => {
    try { fn(); console.log(`  ✓ ${name}`); }
    catch (e) { failures++; console.log(`  ✗ ${name}\n      ${e.message}`); }
  };

  try {
    console.log('\n[1] Centro SENZA disponibilità (messaggio "всі місця зайняті")');
    const full = await checkCenter(context, { id: 'mock-full', name: 'MOCK FULL', url: 'http://127.0.0.1:8731/full' }, { screenshotOnFind: false });
    console.log('    →', JSON.stringify({ status: full.status, dates: full.dates, error: full.error }));
    check('status = FULL', () => assert.strictEqual(full.status, 'FULL'));
    check('nessuna data', () => assert.strictEqual(full.dates.length, 0));
    check('nessun errore', () => assert.strictEqual(full.error, null));

    console.log('\n[2] Centro CON disponibilità (date + orari caricati via JS)');
    const avail = await checkCenter(context, { id: 'mock-avail', name: 'MOCK AVAIL', url: 'http://127.0.0.1:8731/available' }, { screenshotOnFind: false });
    console.log('    →', JSON.stringify({ status: avail.status, dates: avail.dates, times: avail.times, error: avail.error }));
    check('status = AVAILABLE', () => assert.strictEqual(avail.status, 'AVAILABLE'));
    check('date corrette (ISO, ordinate)', () => assert.deepStrictEqual(avail.dates, ['2026-10-03', '2026-10-22']));
    check('orari del 03/10 con numero posti', () => assert.deepStrictEqual(avail.times['2026-10-03'], ['10:30 (3 posti)', '11:00']));
    check('orari del 22/10', () => assert.deepStrictEqual(avail.times['2026-10-22'], ['09:15']));

    console.log('\n[3] Logica di notifica (solo le novità)');
    const seeded = { dates: ['2026-10-22'], times: { '2026-10-22': ['09:15'] }, lastStatus: 'AVAILABLE' };
    const d1 = state.diff(seeded, avail);
    console.log('    → con baseline Gdansk-like:', JSON.stringify({ newDates: d1.newDates, newTimes: d1.newTimes }));
    check('segnala solo la data nuova', () => assert.deepStrictEqual(d1.newDates, ['2026-10-03']));
    const d2 = state.diff({ dates: avail.dates, times: avail.times, lastStatus: 'AVAILABLE' }, avail);
    check('secondo controllo identico = nessuna notifica', () => assert.strictEqual(d2.hasNews, false));
    const d3 = state.diff({ dates: [], times: {}, lastStatus: 'FULL' }, avail);
    check('da FULL a disponibile = notifica', () => assert.strictEqual(d3.hasNews, true));

    console.log('\n[4] Errore di rete (host irraggiungibile)');
    const err = await checkCenter(context, { id: 'mock-err', name: 'MOCK ERR', url: 'http://127.0.0.1:9/x' }, { screenshotOnFind: false });
    console.log('    →', JSON.stringify({ status: err.status, error: (err.error || '').slice(0, 60) }));
    check('status = ERROR', () => assert.strictEqual(err.status, 'ERROR'));
    check('errore registrato', () => assert.ok(err.error));
  } finally {
    await browser.close().catch(() => {});
    server.close();
  }

  console.log(failures === 0 ? '\n✅ TUTTI I TEST SUPERATI\n' : `\n❌ ${failures} test falliti\n`);
  process.exit(failures === 0 ? 0 : 1);
})();
