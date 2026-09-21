<?php
/**
 * Scheda del singolo veicolo.
 *
 * Il contenuto viene costruito dentro il tema (filtro the_content): cosi'
 * funziona sia con i temi classici sia con quelli a blocchi, senza dover
 * modificare il tema del cliente.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cauto_scheda( $content ) {
	if ( ! is_singular( 'auto' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}

	$post_id  = get_the_ID();
	$immagini = cauto_immagini( $post_id );
	$wa       = cauto_link_whatsapp( $post_id );
	$telefono = cauto_impostazione( 'telefono' );

	// Riga per riga: le voci vuote non devono lasciare buchi nella tabella.
	$dati = array_filter(
		array(
			'Immatricolazione'  => cauto_immatricolazione( $post_id ),
			'Chilometri'        => cauto_km( $post_id ),
			'Alimentazione'     => cauto_campo( $post_id, 'alimentazione' ),
			'Cambio'            => cauto_campo( $post_id, 'cambio' ),
			'Carrozzeria'       => cauto_campo( $post_id, 'carrozzeria' ),
			'Potenza'           => cauto_campo( $post_id, 'potenza' ) ? cauto_campo( $post_id, 'potenza' ) . ' CV' : '',
			'Cilindrata'        => cauto_campo( $post_id, 'cilindrata' ) ? number_format( (int) cauto_campo( $post_id, 'cilindrata' ), 0, ',', '.' ) . ' cc' : '',
			'Porte'             => cauto_campo( $post_id, 'porte' ),
			'Posti'             => cauto_campo( $post_id, 'posti' ),
			'Colore'            => cauto_campo( $post_id, 'colore' ),
			'Classe ambientale' => cauto_campo( $post_id, 'classe' ),
			'Garanzia'          => cauto_campo( $post_id, 'garanzia' ) ? cauto_campo( $post_id, 'garanzia' ) . ' mesi' : '',
		)
	);

	$optional = array_filter( array_map( 'trim', explode( "\n", (string) cauto_campo( $post_id, 'optional' ) ) ) );

	ob_start();
	?>
	<div class="scheda">
		<div class="scheda__main">
			<?php if ( $immagini ) : ?>
				<div class="gallery" data-gallery>
					<div class="gallery__main">
						<img src="<?php echo esc_url( wp_get_attachment_image_url( $immagini[0], 'large' ) ); ?>"
							alt="<?php echo esc_attr( get_the_title( $post_id ) ); ?>" data-gallery-main>
						<?php if ( count( $immagini ) > 1 ) : ?>
							<button type="button" class="gallery__nav gallery__nav--prev" data-gallery-prev aria-label="Foto precedente">&#8249;</button>
							<button type="button" class="gallery__nav gallery__nav--next" data-gallery-next aria-label="Foto successiva">&#8250;</button>
						<?php endif; ?>
					</div>
					<?php if ( count( $immagini ) > 1 ) : ?>
						<div class="gallery__thumbs">
							<?php foreach ( $immagini as $id ) : ?>
								<button type="button" data-gallery-thumb data-full="<?php echo esc_url( wp_get_attachment_image_url( $id, 'large' ) ); ?>">
									<img src="<?php echo esc_url( wp_get_attachment_image_url( $id, 'medium' ) ); ?>" alt="" loading="lazy">
								</button>
							<?php endforeach; ?>
						</div>
					<?php endif; ?>
				</div>
			<?php endif; ?>

			<div class="scheda__title">
				<h1><?php echo esc_html( get_the_title( $post_id ) ); ?></h1>
				<p><?php echo esc_html( trim( cauto_marca_nome( $post_id ) . ' ' . cauto_campo( $post_id, 'allestimento' ) ) ); ?></p>
			</div>

			<?php if ( $dati ) : ?>
				<dl class="data-grid">
					<?php foreach ( $dati as $etichetta => $valore ) : ?>
						<div>
							<dt><?php echo esc_html( $etichetta ); ?></dt>
							<dd><?php echo esc_html( $valore ); ?></dd>
						</div>
					<?php endforeach; ?>
				</dl>
			<?php endif; ?>

			<?php if ( trim( wp_strip_all_tags( $content ) ) ) : ?>
				<h2>Descrizione</h2>
				<?php echo $content; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- contenuto gia' filtrato da WordPress. ?>
			<?php endif; ?>

			<?php if ( $optional ) : ?>
				<h2>Dotazioni</h2>
				<ul class="optionals">
					<?php foreach ( $optional as $voce ) : ?>
						<li><?php echo esc_html( $voce ); ?></li>
					<?php endforeach; ?>
				</ul>
			<?php endif; ?>
		</div>

		<aside class="aside-card">
			<p class="price">
				<?php echo esc_html( cauto_prezzo( $post_id ) ); ?>
				<small><?php echo esc_html( cauto_campo( $post_id, 'stato', 'disponibile' ) === 'venduta' ? 'Auto già venduta' : 'Prezzo chiavi in mano, trattabile' ); ?></small>
			</p>

			<div class="aside-card__actions">
				<?php if ( $wa ) : ?>
					<a class="btn btn--wa btn--block" href="<?php echo esc_url( $wa ); ?>" target="_blank" rel="noopener">Scrivi su WhatsApp</a>
				<?php endif; ?>
				<?php if ( $telefono ) : ?>
					<a class="btn btn--dark btn--block" href="tel:<?php echo esc_attr( preg_replace( '/\s+/', '', $telefono ) ); ?>">Chiama <?php echo esc_html( $telefono ); ?></a>
				<?php endif; ?>
			</div>
			<p class="aside-card__note">Possibilità di permuta del tuo usato e finanziamento personalizzato.</p>

			<?php echo cauto_form_richiesta( $post_id ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
		</aside>
	</div>

	<div class="lightbox" data-lightbox>
		<button type="button" class="lightbox__close" data-lightbox-close aria-label="Chiudi">&times;</button>
		<?php if ( count( $immagini ) > 1 ) : ?>
			<button type="button" class="lightbox__nav lightbox__nav--prev" data-lightbox-prev aria-label="Foto precedente">&#8249;</button>
			<button type="button" class="lightbox__nav lightbox__nav--next" data-lightbox-next aria-label="Foto successiva">&#8250;</button>
		<?php endif; ?>
		<img src="" alt="">
	</div>
	<?php
	return ob_get_clean();
}
add_filter( 'the_content', 'cauto_scheda' );
