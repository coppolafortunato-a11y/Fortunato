'use strict';

/**
 * Sito finto che riproduce il form "e-queue": il servizio si sceglie in un
 * <select>, le date compaiono via JS solo dopo la scelta, gli orari solo dopo
 * la scelta della data. Serve a validare il checker senza toccare i siti reali.
 */
const http = require('http');

function page(scenario) {
  const data = {
    full: { dates: [], times: {} },
    available: {
      dates: ['03.10.2026', '22.10.2026'],
      times: { '03.10.2026': ['10:30 (3)', '11:00'], '22.10.2026': ['09:15'] },
    },
  }[scenario] || { dates: [], times: {} };

  return `<!doctype html><html lang="uk"><head><meta charset="utf-8"><title>Електронна черга</title></head>
<body>
<h1>Електронна черга</h1>
<form id="eq">
  <div class="form-group">
    <label for="service">Послуга</label>
    <select id="service" name="service">
      <option value="">Оберіть послугу</option>
      <option value="1">Оформлення довідки</option>
      <option value="2">Закордонний паспорт та (або) ID-картка</option>
      <option value="3">Консультація</option>
    </select>
  </div>
  <div class="form-group" id="dayGroup" style="display:none">
    <label for="day">Обрати день</label>
    <select id="day" name="day"><option value="">Оберіть день</option></select>
  </div>
  <div class="form-group" id="timeGroup" style="display:none">
    <label for="time">Обрати час</label>
    <select id="time" name="time"><option value="">Оберіть час</option></select>
  </div>
  <div id="msg"></div>
  <button type="button">Продовжити</button>
</form>
<script>
const DATA = ${JSON.stringify(data)};
document.getElementById('service').addEventListener('change', function () {
  const msg = document.getElementById('msg');
  const dayGroup = document.getElementById('dayGroup');
  const day = document.getElementById('day');
  msg.textContent = ''; day.innerHTML = '<option value="">Оберіть день</option>';
  document.getElementById('timeGroup').style.display = 'none';
  if (this.value !== '2') { dayGroup.style.display = 'none'; return; }
  setTimeout(function () {                       // il sito reale risponde con un ritardo
    if (DATA.dates.length === 0) {
      msg.textContent = 'Вибачте, на даний момент всі місця зайняті!';
      dayGroup.style.display = 'none';
      return;
    }
    dayGroup.style.display = 'block';
    DATA.dates.forEach(function (d) {
      const o = document.createElement('option'); o.value = d; o.textContent = d; day.appendChild(o);
    });
  }, 1200);
});
document.getElementById('day').addEventListener('change', function () {
  const timeGroup = document.getElementById('timeGroup');
  const time = document.getElementById('time');
  time.innerHTML = '<option value="">Оберіть час</option>';
  if (!this.value) { timeGroup.style.display = 'none'; return; }
  setTimeout(function () {
    timeGroup.style.display = 'block';
    (DATA.times[this.value] || []).forEach(function (t) {
      const o = document.createElement('option'); o.value = t; o.textContent = t; time.appendChild(o);
    });
  }.bind(this), 800);
});
</script></body></html>`;
}

function start(port = 8731) {
  const server = http.createServer((req, res) => {
    const scenario = req.url.includes('available') ? 'available' : 'full';
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(page(scenario));
  });
  return new Promise((resolve) => server.listen(port, '127.0.0.1', () => resolve(server)));
}

module.exports = { start };
