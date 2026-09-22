'use strict';

/**
 * Invio messaggi tramite WhatsApp Web, usando la sessione già autenticata
 * sul computer dove gira il monitor.
 *
 * La sessione vive in un profilo Chromium dedicato (data/whatsapp-profile):
 * va autenticata UNA volta con `npm run whatsapp-login`, inquadrando il QR
 * col telefono. Da lì in poi resta valida per mesi.
 *
 * Nota: è la stessa cosa che farebbe una persona davanti allo schermo, ma
 * automatizzata. WhatsApp non lo incoraggia: usalo per pochi messaggi a
 * familiari, non per invii massivi.
 */

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
const config = require('./config');

const PROFILE_DIR = path.join(config.ROOT, 'data', 'whatsapp-profile');
const WA = 'https://web.whatsapp.com';

/** Apre il profilo persistente: headless per l'invio, visibile per il login. */
async function openContext({ headless }) {
  fs.mkdirSync(PROFILE_DIR, { recursive: true });
  return chromium.launchPersistentContext(PROFILE_DIR, {
    headless,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
    viewport: { width: 1280, height: 860 },
    locale: 'it-IT',
  });
}

/**
 * Distingue i tre stati possibili della pagina:
 * 'ready' (sessione valida), 'login' (chiede il QR), 'unknown' (in caricamento).
 */
async function pageState(page) {
  return page.evaluate(() => {
    const body = document.body ? document.body.innerText : '';
    const qr =
      document.querySelector('canvas[aria-label*="scan" i], canvas[aria-label*="QR" i], [data-ref]') ||
      /scansiona il codice QR|scan the qr code|per accedere/i.test(body);
    if (qr) return 'login';
    const chatList =
      document.querySelector('#pane-side') ||
      document.querySelector('[data-testid="chat-list"]') ||
      document.querySelector('div[role="textbox"][contenteditable="true"]');
    if (chatList) return 'ready';
    return 'unknown';
  });
}

/** Attende che la pagina raggiunga 'ready' o 'login'. */
async function waitForState(page, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  let state = 'unknown';
  while (Date.now() < deadline) {
    state = await pageState(page).catch(() => 'unknown');
    if (state !== 'unknown') return state;
    await page.waitForTimeout(1000);
  }
  return state;
}

/** Login interattivo: apre il browser, mostra il QR, attende la scansione. */
async function login() {
  const context = await openContext({ headless: false });
  const page = context.pages()[0] || (await context.newPage());
  try {
    await page.goto(WA, { waitUntil: 'domcontentloaded', timeout: 60000 });
    console.log('\n  Si è aperta una finestra con WhatsApp Web.');
    console.log('  Sul telefono: WhatsApp → Impostazioni → Dispositivi collegati');
    console.log('  → Collega un dispositivo → inquadra il QR nella finestra.\n');
    console.log('  Attendo (fino a 3 minuti)…');

    const state = await waitForState(page, 180000);
    if (state !== 'ready') {
      throw new Error('Login non completato: il QR non è stato scansionato in tempo.');
    }
    // Un attimo perché la sessione venga scritta su disco prima di chiudere.
    await page.waitForTimeout(5000);
    console.log('\n  ✅ WhatsApp Web collegato. La sessione resta salvata in:');
    console.log(`     ${PROFILE_DIR}\n`);
  } finally {
    await context.close().catch(() => {});
  }
}

/**
 * Invia lo stesso testo a più destinatari riusando una sola finestra.
 * Restituisce un esito per destinatario: un fallimento non blocca gli altri.
 */
async function sendToAll(recipients, text) {
  if (recipients.length === 0) return [];
  const context = await openContext({ headless: config.headless });
  const page = context.pages()[0] || (await context.newPage());
  const results = [];

  try {
    await page.goto(WA, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const state = await waitForState(page, 60000);
    if (state === 'login') {
      throw new Error('WhatsApp Web non è collegato: esegui `npm run whatsapp-login`.');
    }
    if (state !== 'ready') {
      throw new Error('WhatsApp Web non si è caricato in tempo.');
    }

    for (const person of recipients) {
      try {
        await sendOne(page, person, text);
        results.push({ ok: true, channel: `whatsapp:${person.name}` });
      } catch (err) {
        results.push({ ok: false, channel: `whatsapp:${person.name}`, error: err.message });
      }
    }
  } catch (err) {
    // Errore che riguarda l'intera sessione: vale per tutti i destinatari.
    for (const person of recipients) {
      if (!results.some((r) => r.channel === `whatsapp:${person.name}`)) {
        results.push({ ok: false, channel: `whatsapp:${person.name}`, error: err.message });
      }
    }
  } finally {
    await context.close().catch(() => {});
  }
  return results;
}

/** Apre la chat del numero indicato, scrive il testo e invia. */
async function sendOne(page, person, text) {
  const digits = person.phone.replace(/[^0-9]/g, '');
  const url = `${WA}/send?phone=${digits}&text=${encodeURIComponent(text)}&app_absent=0`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

  // Numero non valido o non su WhatsApp: il sito lo dice in un riquadro.
  const invalid = page.locator('text=/numero di telefono.*non.*valido|phone number.*invalid|non è su WhatsApp|isn\'t on WhatsApp/i');
  const box = page.locator('div[role="textbox"][contenteditable="true"]').last();

  const deadline = Date.now() + 60000;
  for (;;) {
    if (await invalid.count().catch(() => 0)) {
      throw new Error(`Il numero ${person.phone} non risulta valido su WhatsApp.`);
    }
    if (await box.count().catch(() => 0)) break;
    if (Date.now() > deadline) throw new Error('La chat non si è aperta in tempo.');
    await page.waitForTimeout(1000);
  }

  await box.click();
  // Il testo passato nell'URL a volte non arriva nel campo: lo scriviamo noi.
  const current = (await box.innerText().catch(() => '')).trim();
  if (!current) {
    for (const line of text.split('\n')) {
      await page.keyboard.type(line);
      await page.keyboard.press('Shift+Enter'); // a capo senza inviare
    }
  }
  await page.keyboard.press('Enter');

  // Conferma: il campo si svuota quando il messaggio parte.
  await page.waitForTimeout(2500);
  const after = (await box.innerText().catch(() => '')).trim();
  if (after && after === current && current) {
    throw new Error('Il messaggio sembra non essere partito (campo ancora pieno).');
  }
  await page.waitForTimeout(1500); // respiro fra un destinatario e l'altro
}

module.exports = { login, sendToAll, pageState, PROFILE_DIR };
