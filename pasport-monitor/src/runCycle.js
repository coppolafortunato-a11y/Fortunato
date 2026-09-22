'use strict';

const config = require('./config');
const log = require('./logger');
const state = require('./state');
const { launch, randomDelay } = require('./browser');
const { checkCenter } = require('./checker');
const { notify, buildAvailabilityMessage, buildErrorMessage } = require('./notifier');
const { formatDateIt } = require('./text');

/**
 * Esegue un ciclo completo sui 5 centri: controlla, confronta con lo stato
 * precedente, notifica solo le novità, aggiorna lo stato e scrive il log.
 */
async function runCycle({ notifications = true } = {}) {
  const current = state.load();
  const { browser, context } = await launch();
  const summary = [];

  try {
    for (let i = 0; i < config.CENTERS.length; i++) {
      const center = config.CENTERS[i];
      const previous = { ...current.centers[center.id] };
      const result = await checkCenter(context, center);

      const line = describe(result);
      log.result(center.name, line);
      log.record({
        center: center.id,
        status: result.status,
        dates: result.dates,
        times: result.times,
        error: result.error,
        screenshot: result.screenshot,
      });

      const entry = state.merge(current, center.id, result);
      summary.push({ center, result, entry });

      if (result.status === 'ERROR') {
        if (notifications && entry.errorStreak >= config.errorAlertThreshold) {
          await notify(buildErrorMessage(center, entry.errorStreak, result.error), {
            screenshot: result.screenshot,
          });
        }
      } else {
        const changes = state.diff(previous, result);
        if (changes.hasNews) {
          log.info(`NOVITÀ su ${center.name}: ${JSON.stringify({ newDates: changes.newDates, newTimes: changes.newTimes, reopened: changes.reopened })}`);
          if (notifications) {
            await notify(buildAvailabilityMessage(center, changes, entry), {
              screenshot: result.screenshot,
            });
          }
        }
      }

      state.save(current);

      if (i < config.CENTERS.length - 1) await randomDelay(config.delayBetweenCentersMs);
    }
  } finally {
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
  }

  return summary;
}

/** Riga di log leggibile: "FULL", "ERRORE: ...", oppure l'elenco delle date. */
function describe(result) {
  if (result.status === 'ERROR') return `ERRORE: ${result.error}`;
  if (result.status === 'FULL' || result.dates.length === 0) return 'FULL';
  return result.dates
    .map((d) => {
      const times = result.times[d];
      return times && times.length ? `${formatDateIt(d)} [${times.join(', ')}]` : formatDateIt(d);
    })
    .join(' | ');
}

module.exports = { runCycle, describe };
