'use strict';

const fs = require('fs');
const path = require('path');
const config = require('./config');
const { randomDelay } = require('./browser');
const { normalizeText, parseDate, parseTime, parseSlots } = require('./text');

const SERVICE_FIELD_LABELS = ['послуга', 'оберіть послугу', 'виберіть послугу'];
const DAY_FIELD_LABELS = ['обрати день', 'оберіть день', 'виберіть день', 'дата'];
const TIME_FIELD_LABELS = ['обрати час', 'оберіть час', 'виберіть час', 'час'];

/**
 * Esegue un controllo completo su un centro.
 * Ritorna { status, dates, times, error, screenshot }.
 * status: 'AVAILABLE' | 'FULL' | 'ERROR'
 *
 * Il programma legge soltanto: non compila dati personali, non clicca
 * "Продовжити", non avvia alcuna procedura di firma o prenotazione.
 */
async function checkCenter(context, center, { screenshotOnFind = true } = {}) {
  const page = await context.newPage();
  const out = { status: 'ERROR', dates: [], times: {}, error: null, screenshot: null, blocked: false };

  try {
    const response = await page.goto(center.url, { waitUntil: 'domcontentloaded' });
    if (response && response.status() >= 400) {
      const err = new Error(`HTTP ${response.status()} dalla pagina`);
      // 403 e 429 sono il sito che ci dice di rallentare, non un guasto.
      err.blocked = response.status() === 403 || response.status() === 429;
      throw err;
    }

    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    await detectBlocking(page);

    const selectedService = await selectService(page);
    if (!selectedService) {
      throw new Error(`Servizio "${config.SERVICE_LABEL}" non trovato nel form`);
    }

    // Il sito ricarica le date via JS dopo la scelta del servizio.
    await randomDelay(config.afterServiceSelectMs);
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

    if (await isFull(page)) {
      out.status = 'FULL';
      return out;
    }

    const dates = await readDates(page);
    if (dates.length === 0) {
      // Nessuna data e nessun messaggio di "tutto pieno": trattiamo come pieno,
      // ma salviamo uno screenshot perché potrebbe essere un cambio di struttura.
      out.status = 'FULL';
      out.screenshot = await capture(page, center, 'no-dates');
      return out;
    }

    out.status = 'AVAILABLE';
    out.dates = dates.map((d) => d.iso);

    for (const date of dates) {
      const times = await readTimesForDate(page, date);
      if (times.length) out.times[date.iso] = times;
    }

    if (screenshotOnFind) out.screenshot = await capture(page, center, 'available');
    return out;
  } catch (err) {
    out.error = err.message;
    out.blocked = Boolean(err.blocked);
    out.screenshot = await capture(page, center, 'error').catch(() => null);
    return out;
  } finally {
    await page.close().catch(() => {});
  }
}

/** Riconosce blocchi anti-bot / CAPTCHA: vanno registrati, mai aggirati. */
async function detectBlocking(page) {
  const text = normalizeText(await page.evaluate(() => document.body?.innerText || ''));
  const title = normalizeText(await page.title());
  const markers = [
    'blocked for security reasons',
    'attention required',
    'checking your browser',
    'verify you are human',
    'доступ заборонено',
  ];
  const hit = markers.find((m) => text.includes(m) || title.includes(m));
  if (hit) {
    const err = new Error(`Bloccato da protezione anti-bot ("${hit}") — nessun tentativo di aggiramento`);
    err.blocked = true;
    throw err;
  }

  const hasCaptcha = await page
    .locator('iframe[src*="recaptcha"], iframe[src*="hcaptcha"], iframe[src*="turnstile"], .g-recaptcha')
    .count();
  if (hasCaptcha > 0) {
    const err = new Error('CAPTCHA presente in pagina — controllo interrotto');
    err.blocked = true;
    throw err;
  }
}

/**
 * Seleziona il servizio. Prova prima i <select> nativi, poi i dropdown custom
 * (div/ul cliccabili), perché il sito può usare entrambe le implementazioni.
 */
async function selectService(page) {
  if (await selectNativeOption(page, SERVICE_FIELD_LABELS, isServiceOption)) return true;
  if (await selectCustomOption(page, SERVICE_FIELD_LABELS, isServiceOption)) return true;
  return false;
}

function isServiceOption(label) {
  const n = normalizeText(label);
  if (n === normalizeText(config.SERVICE_LABEL)) return true;
  return config.SERVICE_MATCH_TOKENS.every((tok) => n.includes(tok));
}

/** Cerca un <select> il cui contenuto corrisponde e ne sceglie l'opzione. */
async function selectNativeOption(page, fieldLabels, matcher) {
  const selects = await page.locator('select').all();
  for (const select of selects) {
    const options = await select.locator('option').all();
    for (let i = 0; i < options.length; i++) {
      const label = (await options[i].textContent()) || '';
      if (!matcher(label)) continue;
      const value = await options[i].getAttribute('value');
      await select.selectOption(value ? { value } : { label: label.trim() });
      await select.dispatchEvent('change').catch(() => {});
      return true;
    }
  }
  return false;
}

/**
 * Dropdown custom: individua il contenitore del campo tramite la sua etichetta,
 * lo apre e clicca l'opzione corrispondente.
 */
async function selectCustomOption(page, fieldLabels, matcher) {
  const trigger = await findFieldTrigger(page, fieldLabels);
  if (!trigger) return false;

  await trigger.click({ timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(1200);

  const candidates = page.locator(
    '[role="option"], li, .select2-results__option, .chosen-results li, .dropdown-item, .option'
  );
  const count = Math.min(await candidates.count(), 400);
  for (let i = 0; i < count; i++) {
    const item = candidates.nth(i);
    const label = (await item.textContent().catch(() => '')) || '';
    if (!matcher(label)) continue;
    if (!(await item.isVisible().catch(() => false))) continue;
    await item.click({ timeout: 8000 });
    return true;
  }
  await page.keyboard.press('Escape').catch(() => {});
  return false;
}

/**
 * Trova l'elemento cliccabile di un campo a partire dall'etichetta visibile
 * ("Послуга", "Обрати день", "Обрати час").
 */
async function findFieldTrigger(page, fieldLabels) {
  const handle = await page.evaluateHandle((labels) => {
    const norm = (s) =>
      String(s || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
    const nodes = Array.from(document.querySelectorAll('label, legend, span, div, p, h1,h2,h3,h4,h5,h6'));
    for (const node of nodes) {
      const text = norm(node.textContent);
      if (text.length > 80) continue;
      if (!labels.some((l) => text === l || text.startsWith(l))) continue;

      // L'elemento interattivo è il campo stesso, un fratello o un discendente.
      const scope = node.closest('.form-group, .field, .input-group, .form-item, form') || node.parentElement || node;
      const control = scope.querySelector(
        'select, input, [role="combobox"], [role="listbox"], .select2, .chosen-container, .dropdown-toggle, button'
      );
      if (control) return control;
      return node;
    }
    return null;
  }, fieldLabels);

  const element = handle.asElement();
  return element || null;
}

/** true se il sito dichiara esplicitamente che non ci sono posti. */
async function isFull(page) {
  const text = normalizeText(await page.evaluate(() => document.body?.innerText || ''));
  return config.FULL_MESSAGES.some((msg) => text.includes(msg));
}

/**
 * Legge le date reali dal campo "Обрати день".
 * Scarta i placeholder ("Оберіть день") e le voci disabilitate.
 */
async function readDates(page) {
  const raw = await page.evaluate((labels) => {
    const norm = (s) =>
      String(s || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();

    // 1) <select> nativo il cui campo corrisponde a "Обрати день".
    for (const select of Array.from(document.querySelectorAll('select'))) {
      const scope = select.closest('.form-group, .field, .input-group, .form-item') || select.parentElement;
      const context = norm(scope ? scope.textContent : '') + ' ' + norm(select.getAttribute('name')) +
        ' ' + norm(select.id);
      if (!labels.some((l) => context.includes(l)) && !/day|date|дн|дат/.test(context)) continue;
      const opts = Array.from(select.options)
        .filter((o) => !o.disabled && o.value !== '')
        .map((o) => ({ label: o.textContent, value: o.value }));
      if (opts.length) return { kind: 'select', items: opts };
    }

    // 2) Calendario / lista custom: celle di giorno non disabilitate.
    const cells = Array.from(
      document.querySelectorAll(
        '[role="option"], .day:not(.disabled):not(.off), td.day:not(.disabled), ' +
        '.datepicker-days td:not(.disabled):not(.old):not(.new), .available-date, .date-item'
      )
    ).filter((el) => {
      const cls = el.className || '';
      if (/disabled|off\b|unavailable|empty/.test(cls)) return false;
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    });
    if (cells.length) {
      return {
        kind: 'custom',
        items: cells.map((el) => ({
          label: el.getAttribute('data-date') || el.getAttribute('aria-label') || el.textContent,
          value: el.getAttribute('data-date') || '',
        })),
      };
    }
    return { kind: 'none', items: [] };
  }, DAY_FIELD_LABELS);

  const year = new Date().getFullYear();
  const seen = new Set();
  const dates = [];
  for (const item of raw.items) {
    const iso = parseDate(item.value, year) || parseDate(item.label, year);
    if (!iso || seen.has(iso)) continue;
    seen.add(iso);
    dates.push({ iso, label: String(item.label || '').trim(), value: item.value, kind: raw.kind });
  }
  return dates.sort((a, b) => a.iso.localeCompare(b.iso));
}

/**
 * Seleziona una data e legge gli orari del campo "Обрати час".
 * In caso di problemi restituisce [] — la data resta comunque segnalata.
 */
async function readTimesForDate(page, date) {
  try {
    if (date.kind === 'select') {
      const ok = await selectNativeOption(page, DAY_FIELD_LABELS, (label) => {
        const iso = parseDate(label, new Date().getFullYear());
        return iso === date.iso;
      });
      if (!ok) return [];
    } else {
      const cell = page.locator(`[data-date="${date.value}"]`).first();
      if ((await cell.count()) === 0) return [];
      await cell.click({ timeout: 8000 });
    }

    await randomDelay([1500, 3000]);
    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});

    const labels = await page.evaluate((fieldLabels) => {
      const norm = (s) =>
        String(s || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();

      for (const select of Array.from(document.querySelectorAll('select'))) {
        const scope = select.closest('.form-group, .field, .input-group, .form-item') || select.parentElement;
        const context = norm(scope ? scope.textContent : '') + ' ' + norm(select.getAttribute('name')) +
          ' ' + norm(select.id);
        if (!fieldLabels.some((l) => context.includes(l)) && !/time|hour|час/.test(context)) continue;
        const opts = Array.from(select.options).filter((o) => !o.disabled && o.value !== '');
        if (opts.length) return opts.map((o) => o.textContent);
      }

      const slots = Array.from(
        document.querySelectorAll('.time-slot:not(.disabled), .time:not(.disabled), [data-time]')
      ).filter((el) => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      });
      return slots.map((el) => el.getAttribute('data-time') || el.textContent);
    }, TIME_FIELD_LABELS);

    const seen = new Set();
    const times = [];
    for (const label of labels) {
      const hhmm = parseTime(label);
      if (!hhmm || seen.has(hhmm)) continue;
      seen.add(hhmm);
      const slots = parseSlots(label);
      times.push(slots ? `${hhmm} (${slots} posti)` : hhmm);
    }
    return times;
  } catch {
    return [];
  }
}

/** Screenshot completo della pagina, nominato per centro e motivo. */
async function capture(page, center, reason) {
  fs.mkdirSync(config.paths.screenshotDir, { recursive: true });
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const file = path.join(config.paths.screenshotDir, `${center.id}-${reason}-${ts}.png`);
  await page.screenshot({ path: file, fullPage: true });
  return file;
}

module.exports = { checkCenter };
