'use strict';

/**
 * Verifica che il monitor riconosca lo stato di WhatsApp Web: sessione valida,
 * oppure schermata di login col QR. Sbagliare qui significa credere di aver
 * mandato un messaggio che non è mai partito.
 */
const assert = require('assert');
const http = require('http');
const { chromium } = require('playwright');
const { pageState } = require('../src/whatsapp-web');

const PAGES = {
  // Schermata QR: com'è quando la sessione è scaduta.
  '/login': `<!doctype html><html lang="it"><body>
      <h1>Usa WhatsApp sul tuo computer</h1>
      <p>Scansiona il codice QR per accedere</p>
      <canvas aria-label="Scan me!" width="264" height="264"></canvas>
    </body></html>`,
  // Interfaccia normale: lista chat a sinistra, campo di scrittura.
  '/ready': `<!doctype html><html lang="it"><body>
      <div id="pane-side"><div>Daria</div><div>Ulina</div></div>
      <div role="textbox" contenteditable="true"></div>
    </body></html>`,
  // Pagina ancora in caricamento: non dobbiamo dare per buono nulla.
  '/loading': `<!doctype html><html lang="it"><body><div>Caricamento…</div></body></html>`,
};

(async () => {
  const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(PAGES[req.url] || PAGES['/loading']);
  });
  await new Promise((r) => server.listen(8733, '127.0.0.1', r));

  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  let fails = 0;

  const check = async (nome, percorso, atteso) => {
    await page.goto(`http://127.0.0.1:8733${percorso}`, { waitUntil: 'domcontentloaded' });
    const stato = await pageState(page);
    try {
      assert.strictEqual(stato, atteso);
      console.log(`  ✓ ${nome} → "${stato}"`);
    } catch {
      fails++;
      console.log(`  ✗ ${nome} → atteso "${atteso}", ottenuto "${stato}"`);
    }
  };

  console.log('\n[Stato di WhatsApp Web]');
  await check('schermata QR = da ricollegare', '/login', 'login');
  await check('interfaccia chat = pronto', '/ready', 'ready');
  await check('pagina in caricamento = incerto', '/loading', 'unknown');

  await browser.close();
  server.close();
  console.log(fails === 0 ? '\n✅ TUTTI I TEST SUPERATI\n' : `\n❌ ${fails} test falliti\n`);
  process.exit(fails === 0 ? 0 : 1);
})();
