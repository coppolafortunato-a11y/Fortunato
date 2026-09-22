'use strict';

require('./env');
const fs = require('fs');
const path = require('path');
const config = require('./config');
const { launch } = require('./browser');

/**
 * Diagnostica: apre un centro e stampa la struttura reale del form
 * (select, opzioni, etichette, testo). Serve a confermare che i selettori
 * del checker corrispondano al sito prima di lasciare il monitor in autonomia.
 *
 *   node src/inspect.js krakow
 */
async function main() {
  const id = process.argv[2] || 'krakow';
  const center = config.CENTERS.find((c) => c.id === id);
  if (!center) {
    console.error(`Centro sconosciuto: ${id}. Validi: ${config.CENTERS.map((c) => c.id).join(', ')}`);
    process.exit(1);
  }

  const { browser, context } = await launch();
  const page = await context.newPage();

  try {
    const res = await page.goto(center.url, { waitUntil: 'domcontentloaded' });
    console.log(`URL      : ${center.url}`);
    console.log(`HTTP     : ${res && res.status()}`);
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(4000);
    console.log(`TITOLO   : ${await page.title()}`);

    const dump = await page.evaluate(() => ({
      text: (document.body.innerText || '').slice(0, 3000),
      selects: Array.from(document.querySelectorAll('select')).map((s) => ({
        id: s.id, name: s.name, class: s.className,
        options: Array.from(s.options).map((o) => `${o.textContent.trim()} [value=${o.value}]${o.disabled ? ' DISABLED' : ''}`),
      })),
      labels: Array.from(document.querySelectorAll('label, legend'))
        .map((l) => l.textContent.trim()).filter((t) => t && t.length < 90),
      inputs: Array.from(document.querySelectorAll('input')).map((i) => `${i.type}:${i.name || i.id}:${i.placeholder || ''}`),
      buttons: Array.from(document.querySelectorAll('button, [role="button"]')).map((b) => b.textContent.trim().slice(0, 50)).filter(Boolean),
      combos: Array.from(document.querySelectorAll('[role="combobox"], .select2, .chosen-container, .dropdown-toggle'))
        .map((e) => `${e.tagName}.${e.className}`.slice(0, 80)),
    }));

    console.log('\n--- ETICHETTE ---'); console.log(dump.labels.join('\n'));
    console.log('\n--- SELECT NATIVI ---'); console.log(JSON.stringify(dump.selects, null, 2));
    console.log('\n--- DROPDOWN CUSTOM ---'); console.log(dump.combos.join('\n') || '(nessuno)');
    console.log('\n--- INPUT ---'); console.log(dump.inputs.join('\n'));
    console.log('\n--- BOTTONI ---'); console.log(dump.buttons.join(' | '));
    console.log('\n--- TESTO PAGINA ---'); console.log(dump.text);

    fs.mkdirSync(config.paths.screenshotDir, { recursive: true });
    const shot = path.join(config.paths.screenshotDir, `inspect-${id}.png`);
    const html = path.join(config.paths.screenshotDir, `inspect-${id}.html`);
    await page.screenshot({ path: shot, fullPage: true });
    fs.writeFileSync(html, await page.content());
    console.log(`\nScreenshot: ${shot}\nHTML      : ${html}`);
  } finally {
    await browser.close().catch(() => {});
  }
}

main().catch((err) => { console.error(`ERRORE: ${err.stack || err.message}`); process.exit(1); });
