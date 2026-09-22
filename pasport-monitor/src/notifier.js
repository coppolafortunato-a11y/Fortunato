'use strict';

const fs = require('fs');
const config = require('./config');
const { formatDateIt } = require('./text');

/**
 * Invia una notifica su tutti i canali configurati: Telegram, email, WhatsApp.
 * Un canale che fallisce non blocca gli altri né il monitor: meglio una
 * notifica su due che nessuna.
 *
 * `messages` può essere una stringa (stesso testo ovunque) oppure
 * { short, full } — `short` per Telegram e WhatsApp, `full` per l'email.
 */
async function notify(messages, { screenshot = null, subject = null } = {}) {
  const short = typeof messages === 'string' ? messages : messages.short;
  const full = typeof messages === 'string' ? messages : (messages.full || messages.short);
  const tasks = [];

  if (config.telegram.token && config.telegram.chatId) {
    tasks.push(wrap('telegram', sendTelegram(short, screenshot)));
  }
  if (config.email.enabled && config.email.host && config.email.to) {
    tasks.push(wrap('email', sendEmail(full, subject || firstLine(short))));
  }
  if (tasks.length === 0 && config.whatsapp.length === 0) {
    console.warn('ATTENZIONE: nessun canale di notifica configurato — vedi .env');
    return [];
  }

  const results = await Promise.all(tasks);

  // WhatsApp Web riusa una sola finestra per tutti i destinatari, quindi
  // viene dopo gli altri canali: è il più lento, non deve ritardarli.
  if (config.whatsapp.length) {
    const { sendToAll } = require('./whatsapp-web');
    try {
      results.push(...(await sendToAll(config.whatsapp, short)));
    } catch (err) {
      console.error(`Notifica WhatsApp non riuscita: ${err.message}`);
      results.push({ ok: false, channel: 'whatsapp', error: err.message });
    }
  }
  return results;
}

/** Non lascia mai fallire l'intero invio per colpa di un singolo canale. */
async function wrap(channel, promise) {
  try {
    await promise;
    return { ok: true, channel };
  } catch (err) {
    console.error(`Notifica ${channel} non riuscita: ${err.message}`);
    return { ok: false, channel, error: err.message };
  }
}

async function sendTelegram(text, screenshot) {
  const base = `https://api.telegram.org/bot${config.telegram.token}`;

  if (screenshot && fs.existsSync(screenshot)) {
    const form = new FormData();
    form.append('chat_id', config.telegram.chatId);
    form.append('caption', truncate(text, 1024));
    form.append('photo', new Blob([fs.readFileSync(screenshot)]), 'screenshot.png');
    const res = await fetch(`${base}/sendPhoto`, { method: 'POST', body: form });
    if (res.ok) return;
    // Se la foto non passa, ripieghiamo sul solo testo.
  }

  const res = await fetch(`${base}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: config.telegram.chatId, text: truncate(text, 4096) }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${truncate(await res.text(), 200)}`);
}

async function sendEmail(text, subject) {
  const nodemailer = require('nodemailer');
  const transport = nodemailer.createTransport({
    host: config.email.host,
    port: config.email.port,
    secure: config.email.port === 465,
    auth: config.email.user ? { user: config.email.user, pass: config.email.pass } : undefined,
  });
  await transport.sendMail({
    from: config.email.user || `monitor@${config.email.host}`,
    to: config.email.to,
    subject: truncate(subject, 120),
    text,
  });
}

function truncate(s, n) {
  const str = String(s);
  return str.length > n ? str.slice(0, n - 1) + '…' : str;
}

function firstLine(s) {
  return String(s).split('\n')[0];
}

/**
 * Messaggio di disponibilità.
 * `short` va su Telegram e WhatsApp: deve stare in una notifica sul telefono.
 * `full` va per email: contiene la spiegazione per chi non segue i dettagli.
 */
function buildAvailabilityMessage(center, changes, current) {
  const dates = changes.newDates.length ? changes.newDates : Object.keys(changes.newTimes);
  const righe = [];

  for (const date of dates) {
    const times = (current.times && current.times[date]) || [];
    const priority = date < config.priorityBefore ? '  ⭐ PRIORITARIO' : '';
    righe.push(`Data: ${formatDateIt(date)}${priority}`);
    righe.push(times.length ? `Orari: ${times.join(', ')}` : 'Orari: (controlla sul sito)');
  }

  if (changes.reopened && dates.length === 0) {
    righe.push('Stato: disponibilità RIAPERTA dopo un periodo senza posti');
    righe.push(`Date attuali: ${current.dates.map(formatDateIt).join(', ') || '—'}`);
  }

  const short = [
    '🚨 APPUNTAMENTO TROVATO',
    '',
    `Centro: ${center.name}`,
    ...righe,
    '',
    'Servizio: Passaporto e/o ID-card',
    '',
    'PRENOTA SUBITO:',
    center.url,
  ].join('\n');

  const full = [
    '🚨 APPUNTAMENTO DISPONIBILE — PRENOTA SUBITO',
    '',
    `Centro:    ${center.name}`,
    ...righe.map((r) => '  ' + r),
    '  Servizio:  Закордонний паспорт та (або) ID-картка',
    '             (passaporto estero e/o carta d\'identità)',
    '',
    'PRENOTA QUI:',
    center.url,
    '',
    '─'.repeat(58),
    'COSA FARE, IN BREVE',
    '',
    '1. Apri subito il link qui sopra: i posti spariscono in pochi minuti.',
    '2. Nel campo "Послуга" scegli «Закордонний паспорт та (або) ID-картка».',
    '3. Scegli la data e l\'ora indicate sopra.',
    '4. Inserisci i dati richiesti e conferma la prenotazione.',
    '',
    'Serve: nome e cognome come sul documento, data di nascita,',
    'e un numero di telefono per la conferma.',
    '',
    '─'.repeat(58),
    'Questo messaggio arriva da un programma che controlla automaticamente',
    'i centri "Паспортний сервіс ДП Документ" e avvisa appena si libera un',
    'posto. Ti scrive solo quando c\'è una novità vera, mai due volte per la',
    'stessa disponibilità.',
  ].join('\n');

  return { short, full, subject: `🚨 Appuntamento disponibile — ${center.name}` };
}

/** Alert tecnico dopo N errori consecutivi sullo stesso centro. */
function buildErrorMessage(center, streak, error) {
  const short = [
    '⚠️ PROBLEMA TECNICO MONITOR',
    '',
    `Centro: ${center.name}`,
    `Controlli falliti consecutivi: ${streak}`,
    `Errore: ${error}`,
    '',
    'Il monitor continua a provare.',
    center.url,
  ].join('\n');
  return { short, full: short, subject: `⚠️ Monitor appuntamenti — problema su ${center.name}` };
}

module.exports = { notify, buildAvailabilityMessage, buildErrorMessage };
