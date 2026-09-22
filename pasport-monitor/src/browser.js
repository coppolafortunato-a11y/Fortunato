'use strict';

const { chromium } = require('playwright');
const config = require('./config');

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';

/**
 * Avvia Chromium con impostazioni "da utente normale": lingua ucraina, fuso di
 * Kiev, viewport desktop. Nessun tentativo di aggirare protezioni anti-bot:
 * se il sito blocca, il controllo va semplicemente in errore.
 */
async function launch() {
  const browser = await chromium.launch({
    headless: config.headless,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const context = await browser.newContext({
    userAgent: UA,
    locale: 'uk-UA',
    timezoneId: 'Europe/Kyiv',
    viewport: { width: 1366, height: 900 },
  });
  context.setDefaultTimeout(20000);
  context.setDefaultNavigationTimeout(config.navigationTimeoutMs);
  return { browser, context };
}

/** Pausa casuale in un intervallo [min, max] ms. */
function randomDelay([min, max]) {
  const ms = Math.floor(min + Math.random() * (max - min));
  return new Promise((resolve) => setTimeout(resolve, ms));
}

module.exports = { launch, randomDelay };
