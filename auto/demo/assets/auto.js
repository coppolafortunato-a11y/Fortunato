/* Catalogo Auto — comportamenti front-end (demo statica + plugin WordPress)
   Tutto client-side: i filtri lavorano sulle card gia' presenti nella pagina. */
(function () {
  'use strict';

  /* ---------- menu mobile ---------- */
  document.querySelectorAll('[data-nav-toggle]').forEach(function (btn) {
    var nav = document.getElementById(btn.getAttribute('aria-controls'));
    if (!nav) return;
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ---------- utilita' ---------- */
  function num(value) {
    var n = parseInt(String(value == null ? '' : value).replace(/[^\d-]/g, ''), 10);
    return isNaN(n) ? null : n;
  }

  function normalize(text) {
    return String(text || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '');
  }

  /* ---------- filtri catalogo ---------- */
  var form = document.querySelector('[data-auto-filtri]');
  var grid = document.querySelector('[data-auto-grid]');

  if (form && grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-auto]'));
    var counter = document.querySelector('[data-auto-count]');
    var empty = document.querySelector('[data-auto-empty]');
    var sort = form.querySelector('[name="ordina"]');

    // i valori arrivati via querystring (es. ricerca rapida in home) pre-compilano il form
    var params = new URLSearchParams(window.location.search);
    params.forEach(function (value, key) {
      var input = form.elements[key];
      if (input && value) input.value = value;
    });

    function matches(card) {
      var d = card.dataset;
      var get = function (name) {
        var el = form.elements[name];
        return el ? el.value.trim() : '';
      };

      var q = normalize(get('q'));
      if (q && normalize(d.nome + ' ' + (d.allestimento || '')).indexOf(q) === -1) return false;

      var marca = get('marca');
      if (marca && d.marca !== marca) return false;

      var alim = get('alimentazione');
      if (alim && d.alimentazione !== alim) return false;

      var cambio = get('cambio');
      if (cambio && d.cambio !== cambio) return false;

      var prezzoMax = num(get('prezzo_max'));
      if (prezzoMax !== null && (num(d.prezzo) === null || num(d.prezzo) > prezzoMax)) return false;

      var kmMax = num(get('km_max'));
      if (kmMax !== null && (num(d.km) === null || num(d.km) > kmMax)) return false;

      var annoMin = num(get('anno_min'));
      if (annoMin !== null && (num(d.anno) === null || num(d.anno) < annoMin)) return false;

      return true;
    }

    function order(list) {
      var mode = sort ? sort.value : '';
      if (!mode) return list;
      var by = {
        prezzo_asc: function (a, b) { return (num(a.dataset.prezzo) || 0) - (num(b.dataset.prezzo) || 0); },
        prezzo_desc: function (a, b) { return (num(b.dataset.prezzo) || 0) - (num(a.dataset.prezzo) || 0); },
        km_asc: function (a, b) { return (num(a.dataset.km) || 0) - (num(b.dataset.km) || 0); },
        anno_desc: function (a, b) { return (num(b.dataset.anno) || 0) - (num(a.dataset.anno) || 0); }
      }[mode];
      return by ? list.slice().sort(by) : list;
    }

    function apply() {
      var visible = cards.filter(function (card) {
        var ok = matches(card);
        card.hidden = !ok;
        return ok;
      });

      order(visible).forEach(function (card) { grid.appendChild(card); });

      if (counter) counter.innerHTML = '<b>' + visible.length + '</b> ' + (visible.length === 1 ? 'auto trovata' : 'auto trovate');
      if (empty) empty.hidden = visible.length > 0;

      // la ricerca resta condivisibile: i filtri finiscono nell'indirizzo della pagina
      var qs = new URLSearchParams();
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.value.trim()) qs.set(el.name, el.value.trim());
      });
      var url = window.location.pathname + (qs.toString() ? '?' + qs.toString() : '');
      window.history.replaceState(null, '', url);
    }

    form.addEventListener('input', apply);
    form.addEventListener('change', apply);
    form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    form.addEventListener('reset', function () { window.setTimeout(apply, 0); });
    apply();
  }

  /* ---------- galleria scheda auto + lightbox ---------- */
  var gallery = document.querySelector('[data-gallery]');
  if (gallery) {
    var main = gallery.querySelector('[data-gallery-main]');
    var thumbs = Array.prototype.slice.call(gallery.querySelectorAll('[data-gallery-thumb]'));
    var sources = thumbs.map(function (t) { return t.dataset.full || t.querySelector('img').src; });
    var index = 0;

    function show(i) {
      if (!sources.length) return;
      index = (i + sources.length) % sources.length;
      if (main) main.src = sources[index];
      thumbs.forEach(function (t, n) { t.setAttribute('aria-current', n === index ? 'true' : 'false'); });
      var box = document.querySelector('[data-lightbox] img');
      if (box) box.src = sources[index];
    }

    thumbs.forEach(function (t, n) { t.addEventListener('click', function () { show(n); }); });
    gallery.querySelectorAll('[data-gallery-prev]').forEach(function (b) {
      b.addEventListener('click', function () { show(index - 1); });
    });
    gallery.querySelectorAll('[data-gallery-next]').forEach(function (b) {
      b.addEventListener('click', function () { show(index + 1); });
    });

    var lightbox = document.querySelector('[data-lightbox]');
    if (lightbox && main) {
      var open = function () { lightbox.classList.add('is-open'); show(index); };
      var close = function () { lightbox.classList.remove('is-open'); };
      main.addEventListener('click', open);
      lightbox.querySelectorAll('[data-lightbox-close]').forEach(function (b) { b.addEventListener('click', close); });
      lightbox.querySelectorAll('[data-lightbox-prev]').forEach(function (b) {
        b.addEventListener('click', function (e) { e.stopPropagation(); show(index - 1); });
      });
      lightbox.querySelectorAll('[data-lightbox-next]').forEach(function (b) {
        b.addEventListener('click', function (e) { e.stopPropagation(); show(index + 1); });
      });
      lightbox.addEventListener('click', function (e) { if (e.target === lightbox) close(); });
      document.addEventListener('keydown', function (e) {
        if (!lightbox.classList.contains('is-open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') show(index - 1);
        if (e.key === 'ArrowRight') show(index + 1);
      });
    }

    show(0);
  }
})();
