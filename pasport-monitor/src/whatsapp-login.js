'use strict';

require('./env');
const { login, PROFILE_DIR } = require('./whatsapp-web');

/**
 * Collega WhatsApp Web al monitor. Da eseguire una volta sola, sul computer
 * dove gira il monitor, con il telefono a portata di mano.
 */
login()
  .then(() => {
    console.log('Fatto. Ora puoi provare l\'invio con:  npm run test-notifiche');
  })
  .catch((err) => {
    console.error(`\n  ❌ ${err.message}`);
    console.error(`     Profilo: ${PROFILE_DIR}`);
    process.exit(1);
  });
