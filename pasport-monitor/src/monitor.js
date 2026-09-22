'use strict';

require('./env');
const config = require('./config');
const log = require('./logger');
const { runCycle } = require('./runCycle');
const { notify } = require('./notifier');

/**
 * Monitor persistente: un ciclo ogni INTERVAL_MINUTES per DURATION_DAYS giorni,
 * poi si ferma da solo. Un errore in un ciclo non interrompe il monitoraggio.
 */
async function main() {
  const startedAt = new Date();
  const stopAt = new Date(startedAt.getTime() + config.durationDays * 86400000);

  log.info('='.repeat(64));
  log.info(`MONITOR AVVIATO — PID ${process.pid}`);
  log.info(`Intervallo: ${config.intervalMinutes} min | Durata: ${config.durationDays} giorni`);
  log.info(`Arresto previsto: ${stopAt.toISOString()} (${stopAt.toLocaleString('it-IT')})`);
  log.info(`Centri: ${config.CENTERS.map((c) => c.name).join(', ')}`);
  log.info(`Notifiche Telegram: ${config.telegram.token && config.telegram.chatId ? 'ATTIVE' : 'NON configurate'}`);
  log.info('='.repeat(64));

  let running = true;
  for (const sig of ['SIGINT', 'SIGTERM']) {
    process.on(sig, () => {
      log.info(`Ricevuto ${sig}: arresto del monitor.`);
      running = false;
      process.exit(0);
    });
  }

  let cycle = 0;
  while (running && Date.now() < stopAt.getTime()) {
    cycle += 1;
    const cycleStart = Date.now();
    log.info(`--- Ciclo #${cycle} ---`);

    try {
      await runCycle({ notifications: true });
    } catch (err) {
      log.info(`ERRORE DI CICLO: ${err.message}`);
      log.record({ event: 'cycle_error', error: err.message });
    }

    // L'attesa parte dalla fine del ciclo: mai più di un giro ogni 15 minuti.
    const elapsed = Date.now() - cycleStart;
    const wait = Math.max(config.intervalMinutes * 60000 - elapsed, 60000);
    const next = new Date(Date.now() + wait);
    if (next.getTime() >= stopAt.getTime()) break;
    log.info(`Ciclo #${cycle} concluso in ${Math.round(elapsed / 1000)}s. Prossimo: ${next.toLocaleTimeString('it-IT')}`);
    await sleep(wait);
  }

  log.info(`MONITOR TERMINATO dopo ${cycle} cicli (durata prevista raggiunta).`);
  await notify(
    `ℹ️ Monitor appuntamenti TERMINATO\n\nCicli eseguiti: ${cycle}\nAvvio: ${startedAt.toLocaleString('it-IT')}\nFine: ${new Date().toLocaleString('it-IT')}\n\nRiavvialo se ti serve ancora.`
  ).catch(() => {});
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

main().catch((err) => {
  log.info(`ERRORE FATALE: ${err.stack || err.message}`);
  process.exit(1);
});
