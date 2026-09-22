'use strict';

/**
 * Configurazione centrale del monitor "Паспортний сервіс ДП Документ".
 * Tutti i valori sensibili (token Telegram, SMTP) arrivano da .env — mai dal codice.
 */

const path = require('path');

const ROOT = path.resolve(__dirname, '..');

/** Testo esatto del servizio da selezionare nel campo "Послуга". */
const SERVICE_LABEL = 'Закордонний паспорт та (або) ID-картка';

/**
 * Varianti accettate nel confronto: il sito a volte usa spazi non separabili,
 * trattini diversi o aggiunge un prefisso/suffisso all'opzione.
 * Il match avviene su testo normalizzato (vedi normalizeText).
 */
const SERVICE_MATCH_TOKENS = ['закордонний паспорт', 'id-картка'];

/** Messaggio mostrato dal sito quando non ci sono posti. */
const FULL_MESSAGES = [
  'вибачте, на даний момент всі місця зайняті',
  'всі місця зайняті',
  'немає вільних місць',
];

const CENTERS = [
  { id: 'krakow',   name: 'CRACOVIA',       url: 'https://krakow.pasport.org.ua/solutions/e-queue' },
  { id: 'warszawa', name: 'VARSAVIA',       url: 'https://warszawa.pasport.org.ua/solutions/e-queue' },
  { id: 'wroclaw',  name: 'WROCLAW',        url: 'https://wroclaw.pasport.org.ua/solutions/e-queue' },
  { id: 'gdansk',   name: 'GDANSK',         url: 'https://gdansk.pasport.org.ua/solutions/e-queue' },
  { id: 'milan',    name: 'MILANO/ROZZANO', url: 'https://milan.pasport.org.ua/solutions/e-queue' },
];

const config = {
  ROOT,
  SERVICE_LABEL,
  SERVICE_MATCH_TOKENS,
  FULL_MESSAGES,
  CENTERS,

  /** Intervallo fra un ciclo completo e il successivo. */
  intervalMinutes: num(process.env.INTERVAL_MINUTES, 15),

  /** Se valorizzato, controlla solo questi centri (es. "milan,gdansk"). */
  onlyCenters: (process.env.ONLY_CENTERS || '').split(',').map((s) => s.trim()).filter(Boolean),
  /** Durata totale del monitoraggio. */
  durationDays: num(process.env.DURATION_DAYS, 10),

  /**
   * Un solo centro per ciclo, a rotazione. Il sito risponde 403 dopo poche
   * interrogazioni ravvicinate (verificato il 22/09/2026: dopo 2 centri di fila
   * ha smesso di rispondere), quindi non controlliamo mai i 5 siti in sequenza.
   * Con 5 centri e un ciclo ogni 15 minuti, ogni centro viene visto ogni 75.
   */
  rotate: process.env.ROTATE !== 'false',
  centersPerCycle: num(process.env.CENTERS_PER_CYCLE, 1),

  /** Pausa fra un centro e l'altro, quando se ne controlla più d'uno per ciclo. */
  delayBetweenCentersMs: [90000, 150000],

  /**
   * Dopo un blocco il centro viene messo a riposo per un numero crescente di
   * cicli (2, 4, 8, 16), così smettiamo di insistere proprio quando il sito
   * ci sta dicendo di rallentare.
   */
  backoffMaxCycles: num(process.env.BACKOFF_MAX_CYCLES, 16),

  /** Variazione casuale dell'attesa fra i cicli: evita un ritmo perfettamente regolare. */
  jitterMs: [0, 180000],
  /** Attesa dopo la selezione del servizio, perché il sito aggiorni le date. */
  afterServiceSelectMs: [2500, 5000],

  /** Data oltre la quale un appuntamento non è più "prioritario". */
  priorityBefore: process.env.PRIORITY_BEFORE || '2026-10-15',

  /** Errori consecutivi sullo stesso centro prima di mandare un alert tecnico. */
  errorAlertThreshold: num(process.env.ERROR_ALERT_THRESHOLD, 3),

  navigationTimeoutMs: num(process.env.NAV_TIMEOUT_MS, 60000),
  headless: process.env.HEADLESS !== 'false',

  paths: {
    state: path.join(ROOT, 'data', 'state.json'),
    logDir: path.join(ROOT, 'logs'),
    logFile: path.join(ROOT, 'logs', 'monitor.log'),
    jsonlFile: path.join(ROOT, 'logs', 'checks.jsonl'),
    screenshotDir: path.join(ROOT, 'screenshots'),
  },

  telegram: {
    token: process.env.TELEGRAM_BOT_TOKEN || '',
    chatId: process.env.TELEGRAM_CHAT_ID || '',
  },

  email: {
    enabled: process.env.EMAIL_ENABLED === 'true',
    host: process.env.SMTP_HOST || '',
    port: num(process.env.SMTP_PORT, 587),
    user: process.env.SMTP_USER || '',
    pass: process.env.SMTP_PASS || '',
    /** Uno o più destinatari separati da virgola. */
    to: process.env.EMAIL_TO || '',
  },

  /**
   * WhatsApp tramite WhatsApp Web, con la sessione già autenticata sul
   * computer dove gira il monitor (vedi `npm run whatsapp-login`).
   * Formato: Nome:+39xxxxxxxxxx, più destinatari separati da virgola.
   */
  whatsapp: parseWhatsapp(process.env.WHATSAPP_RECIPIENTS),
};

function parseWhatsapp(raw) {
  if (!raw) return [];
  return raw
    .split(',')
    .map((entry) => entry.trim())
    .filter(Boolean)
    .map((entry) => {
      const [name, phone] = entry.split(':').map((p) => (p || '').trim());
      if (!phone || !/^\+?[0-9 ]{8,20}$/.test(phone)) return null;
      return { name: name || phone, phone };
    })
    .filter(Boolean);
}

function num(value, fallback) {
  const n = Number(value);
  return Number.isFinite(n) && n > 0 ? n : fallback;
}

module.exports = config;
