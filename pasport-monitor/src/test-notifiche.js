'use strict';

require('./env');
const config = require('./config');
const { notify } = require('./notifier');

/**
 * Manda un messaggio di prova su TUTTI i canali configurati e riporta
 * esattamente quale ha funzionato e quale no.
 *   node src/test-notifiche.js
 *   node src/test-notifiche.js --chat-id   (mostra il chat_id Telegram)
 */
async function main() {
  if (process.argv.includes('--chat-id')) return mostraChatId();

  console.log('\nCanali configurati:');
  console.log(`  Telegram : ${config.telegram.token && config.telegram.chatId ? 'sì' : 'NO'}`);
  console.log(`  Email    : ${config.email.enabled && config.email.to ? config.email.to : 'NO'}`);
  console.log(`  WhatsApp : ${config.whatsapp.length ? config.whatsapp.map((p) => `${p.name} (${p.phone})`).join(', ') : 'NO'}`);
  console.log('\nInvio in corso… (WhatsApp richiede una ventina di secondi)\n');

  const results = await notify({
    short:
      '✅ Monitor appuntamenti ATTIVO\n\n' +
      'Questo è un messaggio di prova.\n' +
      'Riceverai un avviso come questo appena si libera un posto per la ID-card.',
    full:
      '✅ Monitor appuntamenti ATTIVO\n\n' +
      'Questo è solo un messaggio di prova: non c\'è nessun appuntamento da prenotare adesso.\n\n' +
      'Da ora un programma controlla automaticamente i centri "Паспортний сервіс ДП Документ"\n' +
      'di Cracovia, Varsavia, Wrocław, Danzica e Milano/Rozzano.\n\n' +
      'Appena si libera un posto per «Закордонний паспорт та (або) ID-картка»\n' +
      'riceverai un messaggio con la data, l\'ora e il link per prenotare subito.\n\n' +
      'Non devi fare nulla: ti scriviamo noi.',
  }, { subject: '✅ Monitor appuntamenti attivo (messaggio di prova)' });

  console.log('Esito:');
  for (const r of results) {
    console.log(`  ${r.ok ? '✅' : '❌'} ${r.channel}${r.error ? ' — ' + r.error : ''}`);
  }
  const ok = results.filter((r) => r.ok).length;
  console.log(`\n${ok} canale/i su ${results.length} hanno funzionato.`);
  process.exit(ok > 0 ? 0 : 1);
}

async function mostraChatId() {
  if (!config.telegram.token) {
    console.error('TELEGRAM_BOT_TOKEN mancante in .env');
    process.exit(1);
  }
  const res = await fetch(`https://api.telegram.org/bot${config.telegram.token}/getUpdates`);
  const data = await res.json();
  const chats = new Map();
  for (const u of data.result || []) {
    const chat = (u.message || u.channel_post || {}).chat;
    if (chat) chats.set(chat.id, chat.title || `${chat.first_name || ''} ${chat.last_name || ''}`.trim());
  }
  if (chats.size === 0) {
    console.log('Nessuna chat trovata. Scrivi /start al tuo bot su Telegram, poi rilancia.');
  } else {
    console.log('Chat trovate (metti il numero in TELEGRAM_CHAT_ID):');
    for (const [id, name] of chats) console.log(`  ${id}  →  ${name}`);
  }
}

main().catch((err) => { console.error(`ERRORE: ${err.message}`); process.exit(1); });
