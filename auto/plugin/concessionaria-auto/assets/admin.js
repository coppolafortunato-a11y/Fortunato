/* Galleria foto dell'auto: apre la libreria media di WordPress e tiene
   aggiornato il campo nascosto con gli ID delle immagini scelte. */
(function ($) {
  'use strict';

  $(function () {
    var box = $('[data-cauto-galleria]');
    if (!box.length) return;

    var input = box.find('[data-cauto-galleria-input]');
    var lista = box.find('[data-cauto-galleria-lista]');
    var frame = null;

    function sincronizza() {
      var ids = lista.children('li').map(function () { return $(this).data('id'); }).get();
      input.val(ids.join(','));
    }

    box.on('click', '[data-cauto-galleria-aggiungi]', function (e) {
      e.preventDefault();

      if (!frame) {
        frame = wp.media({
          title: 'Foto dell\'auto',
          button: { text: 'Usa queste foto' },
          library: { type: 'image' },
          multiple: 'add'
        });

        frame.on('select', function () {
          frame.state().get('selection').each(function (attachment) {
            var a = attachment.toJSON();
            if (lista.find('li[data-id="' + a.id + '"]').length) return;
            var thumb = (a.sizes && a.sizes.thumbnail) ? a.sizes.thumbnail.url : a.url;
            lista.append(
              '<li data-id="' + a.id + '"><img src="' + thumb + '" alt="">' +
              '<button type="button" class="cauto-galleria__rimuovi" data-cauto-galleria-rimuovi aria-label="Togli questa foto">&times;</button></li>'
            );
          });
          sincronizza();
        });
      }

      frame.open();
    });

    box.on('click', '[data-cauto-galleria-rimuovi]', function (e) {
      e.preventDefault();
      $(this).closest('li').remove();
      sincronizza();
    });
  });
})(jQuery);
