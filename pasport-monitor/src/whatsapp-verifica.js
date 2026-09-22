'use strict';

require('./env');
const config = require('./config');

/**
 * Controlla che il canale WhatsApp sia pronto, senza mandare messaggi a nessuno.
 * Dice esattamente cosa manca e come rimediare.
 */
async function main() {
  console.log(`\nModalità: ${config.whatsappMode === 'chrome' ? 'Chrome già aperto' : 'finestra separata'}`);
  console.log(`Destinatari: ${config.whatsapp.map((p) => `${p.name} (${p.phone})`).join(', ') || 'nessuno'}`);

  if (config.whatsapp.length === 0) {
    console.log('\n⚠️  Nessun destinatario: imposta WHATSAPP_RECIPIENTS in .env');
    process.exit(1);
  }

  const { chromium } = require('playwright');
  const { pageState } = require('./whatsapp-web');

  if (config.whatsappMode === 'chrome') {
    const endpoint = `http://127.0.0.1:${config.chromeDebugPort}`;
    let browser;
    try {
      browser = await chromium.connectOverCDP(endpoint, { timeout: 15000 });
    } catch {
      console.log(`\n❌ Chrome non raggiungibile su ${endpoint}.`);
      console.log('\n   Rimedio: chiudi Chrome del tutto, poi riaprilo dal');
      console.log('   collegamento "Chrome collegabile" sul Desktop.');
      console.log('   Se non ce l\'hai:  powershell -ExecutionPolicy Bypass -File install\\crea-scorciatoia-chrome.ps1');
      process.exit(1);
    }
    console.log('\n✅ Chrome raggiungibile.');

    const context = browser.contexts()[0];
    const wa = context && context.pages().find((p) => p.url().includes('web.whatsapp.com'));
    if (!wa) {
      console.log('⚠️  Nessuna scheda con WhatsApp Web aperta.');
      console.log('   Aprine una su https://web.whatsapp.com e lasciala lì.');
      await browser.close().catch(() => {});
      process.exit(1);
    }
    const stato = await pageState(wa).catch(() => 'unknown');
    console.log(
      stato === 'ready' ? '✅ WhatsApp Web è connesso e pronto.'
      : stato === 'login' ? '❌ WhatsApp Web chiede l\'accesso: inquadra il QR nella scheda.'
      : '⚠️  WhatsApp Web sta ancora caricando: riprova fra qualche secondo.'
    );
    await browser.close().catch(() => {});
    process.exit(stato === 'ready' ? 0 : 1);
  }

  const { login } = require('./whatsapp-web');
  console.log('\nModalità finestra separata: verifica il collegamento con  npm run whatsapp-login');
  void login;
  process.exit(0);
}

main().catch((err) => { console.error(`ERRORE: ${err.message}`); process.exit(1); });
