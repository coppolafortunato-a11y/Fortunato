'use strict';

/** Verifica rotazione dei centri e pausa crescente dopo un blocco del sito. */
const assert = require('assert');
const os = require('os');
const path = require('path');
const config = require('../src/config');
config.paths.state = path.join(os.tmpdir(), 'pasport-rotation-test.json');
require('fs').rmSync(config.paths.state, { force: true });
const state = require('../src/state');

let fails = 0;
const check = (name, fn) => {
  try { fn(); console.log(`  ✓ ${name}`); }
  catch (e) { fails++; console.log(`  ✗ ${name}\n      ${e.message}`); }
};

const centers = config.CENTERS;
const s = state.load();

console.log('\n[1] Rotazione: un centro per ciclo, tutti a turno');
const giro = [];
for (let i = 0; i < 7; i++) {
  s.cycleCount = i + 1;
  const picked = state.pickCenters(s, centers);
  giro.push(picked.map((c) => c.id).join(','));
}
console.log('    →', giro.join(' → '));
check('un solo centro per ciclo', () => assert.ok(giro.every((g) => !g.includes(','))));
check('i 5 centri nei primi 5 cicli', () =>
  assert.deepStrictEqual([...new Set(giro.slice(0, 5))].sort(), centers.map((c) => c.id).sort()));
check('poi riparte dal primo', () => assert.strictEqual(giro[5], giro[0]));

console.log('\n[2] Blocco del sito: pausa che raddoppia');
const attese = [];
for (let n = 1; n <= 5; n++) {
  s.cycleCount = 100;
  state.merge(s, 'milan', { status: 'ERROR', dates: [], times: {}, blocked: true });
  attese.push(s.centers.milan.skipUntilCycle - 100);
}
console.log('    → pause successive (in cicli):', attese.join(', '));
check('raddoppia a ogni blocco', () => assert.deepStrictEqual(attese.slice(0, 4), [2, 4, 8, 16]));
check('si ferma al massimo configurato', () => assert.strictEqual(attese[4], config.backoffMaxCycles));

console.log('\n[3] Un centro in pausa viene saltato');
s.cycleCount = 101;
s.rotationIndex = 0;
const visti = [];
for (let i = 0; i < 4; i++) {
  s.cycleCount = 101 + i;
  visti.push(...state.pickCenters(s, centers).map((c) => c.id));
}
console.log('    → controllati:', visti.join(', '));
check('milan resta fuori mentre è in pausa', () => assert.ok(!visti.includes('milan')));

console.log('\n[4] Dopo un controllo riuscito la pausa si azzera');
s.cycleCount = 200;
state.merge(s, 'milan', { status: 'FULL', dates: [], times: {}, blocked: false });
console.log('    → skipUntilCycle:', s.centers.milan.skipUntilCycle, '| blockStreak:', s.centers.milan.blockStreak);
check('pausa azzerata', () => assert.strictEqual(s.centers.milan.skipUntilCycle, 0));
check('contatore blocchi azzerato', () => assert.strictEqual(s.centers.milan.blockStreak, 0));

console.log('\n[5] Tutti in pausa: il ciclo non controlla nulla');
s.cycleCount = 300;
for (const c of centers) s.centers[c.id].skipUntilCycle = 999;
const vuoto = state.pickCenters(s, centers);
check('nessun centro selezionato', () => assert.strictEqual(vuoto.length, 0));

console.log(fails === 0 ? '\n✅ TUTTI I TEST SUPERATI\n' : `\n❌ ${fails} test falliti\n`);
process.exit(fails === 0 ? 0 : 1);
