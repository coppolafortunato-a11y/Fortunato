'use strict';

/**
 * Prova d'insieme: esegue un ciclo completo del monitor sui 5 centri, con il
 * sito di prova al posto di quelli reali. Verifica log, stato e notifiche.
 * Scenari: 3 centri pieni, 2 con disponibilità (come il baseline noto).
 */
const fs = require('fs');
const { start } = require('./mock-site');
const os = require('os');
const path = require('path');
const config = require('../src/config');

// Sostituiamo gli URL reali con quelli del server di prova.
const SCENARIOS = { krakow: 'full', warszawa: 'full', wroclaw: 'full', gdansk: 'available', milan: 'available' };
for (const c of config.CENTERS) c.url = `http://127.0.0.1:8732/${SCENARIOS[c.id]}`;
config.delayBetweenCentersMs = [200, 400];
config.rotate = false;   // in questo test vogliamo tutti e 5 i centri in un ciclo
config.paths.state = path.join(os.tmpdir(), 'pasport-monitor-test-state.json');

const notifier = require('../src/notifier');
const sent = [];
notifier.notify = async (text) => { sent.push(text); return [{ ok: true, channel: 'mock' }]; };

const { runCycle } = require('../src/runCycle');

(async () => {
  const server = await start(8732);
  try {
    fs.writeFileSync(config.paths.state, JSON.stringify({
      centers: {
        krakow: { dates: [], times: {}, lastStatus: 'FULL', errorStreak: 0 },
        warszawa: { dates: [], times: {}, lastStatus: 'FULL', errorStreak: 0 },
        wroclaw: { dates: [], times: {}, lastStatus: 'FULL', errorStreak: 0 },
        gdansk: { dates: ['2026-10-22'], times: { '2026-10-22': ['09:15'] }, lastStatus: 'AVAILABLE', errorStreak: 0 },
        milan: { dates: ['2026-10-15'], times: {}, lastStatus: 'AVAILABLE', errorStreak: 0 },
      },
    }, null, 2));

    console.log('\n===== CICLO 1 (baseline: Gdansk 22/10 già noto) =====');
    await runCycle({ notifications: true });
    console.log(`\nNotifiche inviate nel ciclo 1: ${sent.length}`);
    sent.forEach((m) => console.log('\n---\n' + m));

    const before = sent.length;
    console.log('\n===== CICLO 2 (stessa situazione: non deve notificare nulla) =====');
    await runCycle({ notifications: true });
    console.log(`\nNotifiche inviate nel ciclo 2: ${sent.length - before} (atteso: 0)`);

    console.log('\n===== STATO SALVATO =====');
    console.log(fs.readFileSync(config.paths.state, 'utf8'));
    process.exit(sent.length - before === 0 ? 0 : 1);
  } finally {
    server.close();
  }
})();
