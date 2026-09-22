'use strict';

/**
 * Installazione guidata: esegue sul computer dell'utente tutti i passaggi che
 * non possono essere fatti da remoto — browser, Telegram, primo controllo reale,
 * servizio persistente. Un comando solo: npm run setup
 */
require('./env');
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');
const { execFileSync, execSync } = require('child_process');
const config = require('./config');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
let stdinClosed = false;
rl.on('close', () => { stdinClosed = true; });
/** Domanda all'utente. Se stdin è chiuso (esecuzione non interattiva)
 *  restituisce stringa vuota, così la procedura termina senza errori. */
const ask = (q) =>
  stdinClosed
    ? Promise.resolve('')
    : new Promise((resolve) => {
        try {
          rl.question(q, (a) => resolve(a.trim()));
        } catch {
          stdinClosed = true;
          resolve('');
        }
      });

const ok = (m) => console.log(`  ✅ ${m}`);
const bad = (m) => console.log(`  ❌ ${m}`);
const warn = (m) => console.log(`  ⚠️  ${m}`);

function step(n, title) {
  console.log(`\n${'─'.repeat(62)}\n  PASSO ${n} — ${title}\n${'─'.repeat(62)}`);
}

async function main() {
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║   MONITOR APPUNTAMENTI — Паспортний сервіс ДП Документ       ║
║   Installazione guidata                                      ║
╚══════════════════════════════════════════════════════════════╝`);

  const env = readEnv();

  // ── 1. Node ──────────────────────────────────────────────────────────
  step(1, 'Verifica del sistema');
  const major = Number(process.versions.node.split('.')[0]);
  if (major < 18) {
    bad(`Node.js ${process.versions.node} è troppo vecchio: serve la versione 18 o superiore.`);
    console.log('     Scaricalo da https://nodejs.org (scegli "LTS") e rilancia questo comando.');
    process.exit(1);
  }
  ok(`Node.js ${process.versions.node}`);
  ok(`Sistema: ${os.type()} ${os.release()} (${os.arch()})`);

  // ── 2. Chromium ──────────────────────────────────────────────────────
  step(2, 'Browser Chromium');
  try {
    const { chromium } = require('playwright');
    const exe = chromium.executablePath();
    if (fs.existsSync(exe)) {
      ok('Chromium già installato.');
    } else {
      console.log('  Scarico Chromium (~150 MB, un paio di minuti)…');
      execSync('npx playwright install chromium', { stdio: 'inherit' });
      ok('Chromium installato.');
    }
  } catch (err) {
    bad(`Problema con Chromium: ${err.message}`);
    console.log('     Prova a mano:  npx playwright install chromium');
    process.exit(1);
  }

  // ── 3. Raggiungibilità dei siti ──────────────────────────────────────
  step(3, 'Controllo che i siti siano raggiungibili da questa connessione');
  console.log('  (i siti bloccano VPN e IP di datacenter: verifichiamo subito)\n');
  const reach = await testReachability();
  if (reach.status !== 'ok') {
    if (reach.status === 'blocked') {
      bad('Il sito rifiuta le connessioni da questo computer (blocco anti-bot).');
      console.log('\n     Cosa fare:');
      console.log('       • se hai una VPN o un proxy attivo, disattivalo e rilancia;');
      console.log('       • se sei su una rete aziendale o su un server, usa la connessione di casa.');
    } else {
      bad(`Non riesco a raggiungere il sito: ${reach.detail}`);
      console.log('\n     Cosa fare:');
      console.log('       • controlla che il computer sia connesso a Internet;');
      console.log('       • se usi una VPN, un proxy o un antivirus che ispeziona il traffico,');
      console.log('         disattivalo e rilancia.');
    }
    const go = await ask('\n  Vuoi continuare comunque la configurazione? [s/N] ');
    if (!/^s/i.test(go)) { rl.close(); process.exit(1); }
  } else {
    ok('I siti rispondono correttamente da questa connessione.');
  }

  // ── 4. Telegram ──────────────────────────────────────────────────────
  step(4, 'Notifiche Telegram');
  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
    ok('Telegram risulta già configurato.');
    const again = await ask('  Vuoi riconfigurarlo? [s/N] ');
    if (!/^s/i.test(again)) { console.log('  Lascio la configurazione attuale.'); }
    else await configureTelegram(env);
  } else {
    console.log(`
  Ti servono 30 secondi su Telegram:
    1. cerca il contatto  @BotFather
    2. scrivigli          /newbot
    3. scegli un nome (es. "Appuntamenti ID card")
    4. ti risponde con un TOKEN, tipo 123456789:AAH...xyz
`);
    await configureTelegram(env);
  }

  // ── 4b. Email ────────────────────────────────────────────────────────
  step('4b', 'Notifiche via email (facoltative)');
  const vuoleEmail = await ask('  Vuoi ricevere gli avvisi anche per email? [s/N] ');
  if (/^s/i.test(vuoleEmail)) {
    console.log(`
  Con Gmail serve una "password per le app", non quella normale:
  Account Google → Sicurezza → Verifica in due passaggi → Password per le app
`);
    env.SMTP_HOST = (await ask(`  Server SMTP [${env.SMTP_HOST || 'smtp.gmail.com'}]: `)) || env.SMTP_HOST || 'smtp.gmail.com';
    env.SMTP_PORT = (await ask(`  Porta [${env.SMTP_PORT || '587'}]: `)) || env.SMTP_PORT || '587';
    env.SMTP_USER = (await ask('  Tuo indirizzo email (mittente): ')) || env.SMTP_USER || '';
    env.SMTP_PASS = (await ask('  Password per le app: ')) || env.SMTP_PASS || '';
    env.EMAIL_TO = (await ask('  Destinatari, separati da virgola: ')) || env.EMAIL_TO || '';
    env.EMAIL_ENABLED = env.SMTP_USER && env.EMAIL_TO ? 'true' : 'false';
    writeEnv(env);
    ok(env.EMAIL_ENABLED === 'true' ? `Email attive → ${env.EMAIL_TO}` : 'Email non configurate.');
  } else {
    env.EMAIL_ENABLED = env.EMAIL_ENABLED || 'false';
  }

  // ── 4c. WhatsApp ─────────────────────────────────────────────────────
  step('4c', 'Notifiche via WhatsApp (facoltative)');
  const vuoleWa = await ask('  Vuoi avvisare qualcuno su WhatsApp? [s/N] ');
  if (/^s/i.test(vuoleWa)) {
    console.log(`
  Serve WhatsApp Web collegato a questo computer: si apre una finestra
  con un QR da inquadrare col telefono (una volta sola).
`);
    const dest = await ask('  Destinatari, formato Nome:+39numero, separati da virgola:\n  ');
    if (dest) {
      env.WHATSAPP_RECIPIENTS = dest;
      writeEnv(env);
      process.env.WHATSAPP_RECIPIENTS = dest;
      const collega = await ask('  Apro ora la finestra per collegare WhatsApp Web? [S/n] ');
      if (!/^n/i.test(collega)) {
        try {
          execFileSync(process.execPath, [path.join(__dirname, 'whatsapp-login.js')], {
            stdio: 'inherit', cwd: config.ROOT,
          });
          ok('WhatsApp Web collegato.');
        } catch {
          warn('Collegamento non riuscito. Riprova più tardi con: npm run whatsapp-login');
        }
      }
    }
  }

  // ── 5. Impostazioni ──────────────────────────────────────────────────
  step(5, 'Impostazioni del monitoraggio');
  env.INTERVAL_MINUTES = env.INTERVAL_MINUTES || '15';
  env.DURATION_DAYS = env.DURATION_DAYS || '10';
  env.PRIORITY_BEFORE = env.PRIORITY_BEFORE || '2026-10-15';
  env.ERROR_ALERT_THRESHOLD = env.ERROR_ALERT_THRESHOLD || '3';
  env.HEADLESS = env.HEADLESS || 'true';
  env.ROTATE = env.ROTATE || 'true';
  env.CENTERS_PER_CYCLE = env.CENTERS_PER_CYCLE || '1';
  writeEnv(env);
  ok(`Controllo ogni ${env.INTERVAL_MINUTES} minuti, per ${env.DURATION_DAYS} giorni.`);
  ok('Un centro per ciclo a rotazione: ogni centro viene visto ogni ~75 minuti.');
  console.log('     (il sito blocca chi lo interroga troppo spesso, quindi si va piano)');
  ok(`Impostazioni salvate in ${path.join(config.ROOT, '.env')}`);

  // ── 6. Primo controllo reale ─────────────────────────────────────────
  step(6, 'Primo controllo dei 5 centri (senza notifiche)');
  console.log('  Serve a registrare la situazione attuale, così non ricevi');
  console.log('  una notifica per appuntamenti che già conosci. Circa 1-2 minuti…\n');
  try {
    execFileSync(process.execPath, [path.join(__dirname, 'check.js'), '--no-notify'], {
      stdio: 'inherit', cwd: config.ROOT,
    });
  } catch {
    warn('Il primo controllo ha incontrato problemi: guarda i messaggi qui sopra.');
    warn('Puoi indagare con:  npm run inspect krakow');
  }

  // ── 7. Servizio persistente ──────────────────────────────────────────
  step(7, 'Avvio permanente');
  const install = await ask('  Avvio il monitor in modo che continui anche chiudendo il terminale? [S/n] ');
  if (/^n/i.test(install)) {
    console.log('\n  Va bene. Per avviarlo a mano:  npm start');
  } else {
    try {
      if (process.platform === 'win32') {
        execSync('powershell -ExecutionPolicy Bypass -File install\\install-windows.ps1', { stdio: 'inherit', cwd: config.ROOT });
      } else {
        execSync('bash install/install.sh', { stdio: 'inherit', cwd: config.ROOT });
      }
      ok('Monitor avviato.');
    } catch (err) {
      bad(`Installazione del servizio non riuscita: ${err.message}`);
      console.log('     In alternativa avvialo a mano con:  npm start');
    }
  }

  // ── Riepilogo ────────────────────────────────────────────────────────
  const stop = new Date(Date.now() + Number(env.DURATION_DAYS) * 86400000);
  console.log(`
${'═'.repeat(62)}
  FATTO
${'═'.repeat(62)}
  Log             : ${config.paths.logFile}
  Stato salvato   : ${config.paths.state}
  Screenshot      : ${config.paths.screenshotDir}
  Notifiche       : ${[
    env.TELEGRAM_CHAT_ID ? 'Telegram' : null,
    env.EMAIL_ENABLED === 'true' ? `email (${env.EMAIL_TO})` : null,
    env.WHATSAPP_RECIPIENTS ? `WhatsApp (${env.WHATSAPP_RECIPIENTS})` : null,
  ].filter(Boolean).join(', ') || 'nessuna'}
  Frequenza       : ogni ${env.INTERVAL_MINUTES} minuti
  Arresto previsto: ${stop.toLocaleString('it-IT')}

  Per vedere cosa sta facendo:
${process.platform === 'win32'
  ? '    Get-Content -Wait logs\\monitor.log'
  : '    tail -f logs/monitor.log'}

  Per fermarlo:
${process.platform === 'win32'
  ? '    Stop-ScheduledTask -TaskName PasportMonitor'
  : process.platform === 'darwin'
    ? '    launchctl unload -w ~/Library/LaunchAgents/com.fortunato.pasport-monitor.plist'
    : '    systemctl --user stop pasport-monitor'}
${'═'.repeat(62)}
`);
  rl.close();
}

/**
 * Prova ad aprire un sito col browser e distingue i due casi che contano:
 * il sito ci blocca ('blocked') oppure non lo raggiungiamo affatto ('unreachable').
 */
async function testReachability() {
  const { launch } = require('./browser');
  const { browser, context } = await launch();
  try {
    const page = await context.newPage();
    const res = await page.goto(config.CENTERS[0].url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    const status = res ? res.status() : 0;
    const text = (await page.evaluate(() => document.body?.innerText || '')).slice(0, 200);
    console.log(`  ${config.CENTERS[0].name}: HTTP ${status}`);
    if (status === 403 || /blocked for security|attention required/i.test(text)) {
      console.log(`  Risposta del sito: "${text.trim().slice(0, 80)}"`);
      return { status: 'blocked' };
    }
    if (status > 0 && status < 400) return { status: 'ok' };
    return { status: 'unreachable', detail: `HTTP ${status}` };
  } catch (err) {
    const detail = err.message.split('\n')[0];
    console.log(`  Errore: ${detail}`);
    return { status: 'unreachable', detail };
  } finally {
    await browser.close().catch(() => {});
  }
}

/** Chiede il token, trova il chat_id e manda un messaggio di prova. */
async function configureTelegram(env) {
  for (;;) {
    const token = await ask('  Incolla qui il TOKEN del bot: ');
    if (!token) { console.log('  (vuoto — riprova)'); continue; }

    let me;
    try {
      const res = await fetch(`https://api.telegram.org/bot${token}/getMe`);
      me = await res.json();
    } catch (err) {
      bad(`Non riesco a contattare Telegram: ${err.message}`);
      continue;
    }
    if (!me.ok) { bad('Token non valido. Ricontrolla e reincollalo.'); continue; }
    ok(`Bot riconosciuto: @${me.result.username}`);

    console.log(`\n  Ora apri Telegram, cerca  @${me.result.username}  e scrivigli:  /start`);
    await ask('  Quando l\'hai fatto, premi INVIO qui… ');

    let chatId = null;
    for (let attempt = 1; attempt <= 6 && !chatId; attempt++) {
      const res = await fetch(`https://api.telegram.org/bot${token}/getUpdates`);
      const data = await res.json();
      for (const u of (data.result || []).reverse()) {
        const chat = (u.message || u.channel_post || {}).chat;
        if (chat) { chatId = chat.id; break; }
      }
      if (!chatId) {
        console.log(`  Non vedo ancora il messaggio… riprovo (${attempt}/6)`);
        await new Promise((r) => setTimeout(r, 3000));
      }
    }
    if (!chatId) {
      bad('Non ho ricevuto nessun messaggio dal bot.');
      const retry = await ask('  Riprovo da capo? [S/n] ');
      if (/^n/i.test(retry)) return;
      continue;
    }
    ok(`Chat trovata: ${chatId}`);

    env.TELEGRAM_BOT_TOKEN = token;
    env.TELEGRAM_CHAT_ID = String(chatId);
    writeEnv(env);
    process.env.TELEGRAM_BOT_TOKEN = token;
    process.env.TELEGRAM_CHAT_ID = String(chatId);
    config.telegram.token = token;
    config.telegram.chatId = String(chatId);

    const { notify } = require('./notifier');
    const results = await notify(
      '✅ Monitor appuntamenti attivo\n\nRiceverai un messaggio come questo appena compare un posto libero per la ID-card.'
    );
    if (results.some((r) => r && r.ok)) { ok('Messaggio di prova inviato — controlla Telegram.'); return; }
    bad('Invio non riuscito. Riproviamo.');
  }
}

function readEnv() {
  const file = path.join(config.ROOT, '.env');
  const env = {};
  if (fs.existsSync(file)) {
    for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
      const t = line.trim();
      if (!t || t.startsWith('#')) continue;
      const i = t.indexOf('=');
      if (i > 0) env[t.slice(0, i).trim()] = t.slice(i + 1).trim();
    }
  }
  return env;
}

function writeEnv(env) {
  const file = path.join(config.ROOT, '.env');
  const body = Object.entries(env).map(([k, v]) => `${k}=${v}`).join('\n') + '\n';
  fs.writeFileSync(file, body, { mode: 0o600 }); // il token resta leggibile solo dall'utente
}

main().catch((err) => {
  console.error(`\nERRORE: ${err.stack || err.message}`);
  rl.close();
  process.exit(1);
});
