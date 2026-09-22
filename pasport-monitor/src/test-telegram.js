'use strict';

require('./env');
const config = require('./config');
const { notify } = require('./notifier');

/**
 * Verifica il canale di notifica.
 *   node src/test-telegram.js            -> invia un messaggio di prova
 *   node src/test-telegram.js --chat-id  -> mostra il chat_id (scrivi prima al bot)
 */
async function main() {
  if (!config.telegram.token) {
    console.error('TELEGRAM_BOT_TOKEN mancante in .env');
    process.exit(1);
  }

  if (process.argv.includes('--chat-id')) {
    const res = await fetch(`https://api.telegram.org/bot${config.telegram.token}/getUpdates`);
    const data = await res.json();
    const chats = new Map();
    for (const u of data.result || []) {
      const chat = (u.message || u.channel_post || {}).chat;
      if (chat) chats.set(chat.id, chat.title || `${chat.first_name || ''} ${chat.last_name || ''}`.trim() || chat.username);
    }
    if (chats.size === 0) {
      console.log('Nessuna chat trovata. Apri Telegram, scrivi /start al tuo bot, poi rilancia questo comando.');
    } else {
      console.log('Chat trovate (metti il numero in TELEGRAM_CHAT_ID):');
      for (const [id, name] of chats) console.log(`  ${id}  →  ${name}`);
    }
    return;
  }

  const results = await notify(
    '✅ Monitor appuntamenti Паспортний сервіс\n\nCanale di notifica configurato correttamente.\nRiceverai un messaggio come questo appena compare un posto libero.'
  );
  console.log(JSON.stringify(results, null, 2));
  if (results.some((r) => r && r.ok)) console.log('\nNotifica inviata.');
  else { console.error('\nNessuna notifica inviata — controlla token e chat_id.'); process.exit(1); }
}

main().catch((err) => { console.error(`ERRORE: ${err.message}`); process.exit(1); });
