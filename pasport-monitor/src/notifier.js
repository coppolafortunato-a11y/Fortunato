'use strict';

const fs = require('fs');
const config = require('./config');
const { formatDateIt } = require('./text');

/**
 * Invia una notifica su tutti i canali configurati.
 * Un canale che fallisce non blocca gli altri né il monitor.
 */
async function notify(text, { screenshot = null } = {}) {
  const results = [];
  if (config.telegram.token && config.telegram.chatId) {
    results.push(await sendTelegram(text, screenshot).catch((e) => ({ ok: false, channel: 'telegram', error: e.message })));
  }
  if (config.email.enabled && config.email.host && config.email.to) {
    results.push(await sendEmail(text).catch((e) => ({ ok: false, channel: 'email', error: e.message })));
  }
  if (results.length === 0) {
    console.warn('ATTENZIONE: nessun canale di notifica configurato — vedi .env');
  }
  return results;
}

async function sendTelegram(text, screenshot) {
  const base = `https://api.telegram.org/bot${config.telegram.token}`;

  if (screenshot && fs.existsSync(screenshot)) {
    const form = new FormData();
    form.append('chat_id', config.telegram.chatId);
    form.append('caption', truncate(text, 1024));
    form.append('photo', new Blob([fs.readFileSync(screenshot)]), 'screenshot.png');
    const res = await fetch(`${base}/sendPhoto`, { method: 'POST', body: form });
    if (res.ok) return { ok: true, channel: 'telegram' };
    // Se l'invio della foto fallisce ripieghiamo sul solo testo.
  }

  const res = await fetch(`${base}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: config.telegram.chatId,
      text: truncate(text, 4096),
      disable_web_page_preview: false,
    }),
  });
  if (!res.ok) throw new Error(`Telegram HTTP ${res.status}: ${truncate(await res.text(), 200)}`);
  return { ok: true, channel: 'telegram' };
}

async function sendEmail(text) {
  let nodemailer;
  try {
    nodemailer = require('nodemailer');
  } catch {
    throw new Error('nodemailer non installato: esegui `npm install nodemailer`');
  }
  const transport = nodemailer.createTransport({
    host: config.email.host,
    port: config.email.port,
    secure: config.email.port === 465,
    auth: config.email.user ? { user: config.email.user, pass: config.email.pass } : undefined,
  });
  await transport.sendMail({
    from: config.email.user || `monitor@${config.email.host}`,
    to: config.email.to,
    subject: text.split('\n')[0].slice(0, 120),
    text,
  });
  return { ok: true, channel: 'email' };
}

function truncate(s, n) {
  const str = String(s);
  return str.length > n ? str.slice(0, n - 1) + '…' : str;
}

/** Messaggio di disponibilità, nel formato richiesto. */
function buildAvailabilityMessage(center, changes, current) {
  const lines = ['🚨 APPUNTAMENTO TROVATO', '', `Centro: ${center.name}`];

  const dates = changes.newDates.length
    ? changes.newDates
    : Object.keys(changes.newTimes);

  for (const date of dates) {
    const times = (current.times && current.times[date]) || [];
    const priority = date < config.priorityBefore ? '  ⭐ PRIORITARIO' : '';
    lines.push(`Data: ${formatDateIt(date)}${priority}`);
    if (times.length) {
      lines.push(`Orari: ${times.join(', ')}`);
    } else {
      lines.push('Orari: (non letti — controlla sul sito)');
    }
  }

  if (changes.reopened && dates.length === 0) {
    lines.push('Stato: disponibilità RIAPERTA dopo un periodo senza posti');
    lines.push(`Date attuali: ${current.dates.map(formatDateIt).join(', ') || '—'}`);
  }

  lines.push('', 'Servizio: Passaporto e/o ID-card', '', 'PRENOTA SUBITO:', center.url);
  return lines.join('\n');
}

/** Alert tecnico dopo N errori consecutivi sullo stesso centro. */
function buildErrorMessage(center, streak, error) {
  return [
    '⚠️ PROBLEMA TECNICO MONITOR',
    '',
    `Centro: ${center.name}`,
    `Controlli falliti consecutivi: ${streak}`,
    `Errore: ${error}`,
    '',
    'Il monitor continua a provare. Se persiste, il sito potrebbe aver',
    'cambiato struttura o bloccato l\'automazione.',
    '',
    center.url,
  ].join('\n');
}

module.exports = { notify, buildAvailabilityMessage, buildErrorMessage };
