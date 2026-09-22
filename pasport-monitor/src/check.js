'use strict';

require('./env');
const config = require('./config');
const log = require('./logger');
const { runCycle, describe } = require('./runCycle');
const { formatDateIt } = require('./text');

/**
 * Un solo ciclo, per test manuale.
 *   node src/check.js            -> controlla e notifica
 *   node src/check.js --no-notify -> controlla senza inviare notifiche
 */
async function main() {
  const notifications = !process.argv.includes('--no-notify');
  log.info(`CONTROLLO SINGOLO (notifiche: ${notifications ? 'sì' : 'no'})`);

  const summary = await runCycle({ notifications });

  console.log('\n' + '='.repeat(60));
  console.log('STATO ATTUALE DEI 5 CENTRI');
  console.log('='.repeat(60));
  for (const { center, result } of summary) {
    const icon = result.status === 'AVAILABLE' ? '🟢' : result.status === 'FULL' ? '🔴' : '⚠️ ';
    console.log(`${icon} ${center.name.padEnd(16)} ${describe(result)}`);
  }
  console.log('='.repeat(60));

  const priority = summary.flatMap(({ center, result }) =>
    result.dates.filter((d) => d < config.priorityBefore).map((d) => `${center.name} → ${formatDateIt(d)}`)
  );
  console.log(
    priority.length
      ? `\n⭐ PRIORITARI (prima del ${formatDateIt(config.priorityBefore)}):\n   ` + priority.join('\n   ')
      : `\nNessuna disponibilità prima del ${formatDateIt(config.priorityBefore)}.`
  );
}

main().catch((err) => {
  console.error(`ERRORE: ${err.stack || err.message}`);
  process.exit(1);
});
