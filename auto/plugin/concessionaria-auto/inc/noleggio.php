<?php
/**
 * Veicoli a noleggio e auto per cerimonie.
 *
 * Sono un tipo di contenuto a parte rispetto alle auto in vendita: prezzi
 * a giornata invece che di listino e nessun dato da usato (km, targa...).
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cauto_registra_noleggio() {
	register_post_type(
		'noleggio',
		array(
			'labels'        => array(
				'name'          => 'Noleggio',
				'singular_name' => 'Veicolo a noleggio',
				'add_new'       => 'Aggiungi veicolo',
				'add_new_item'  => 'Aggiungi un veicolo a noleggio',
				'edit_item'     => 'Modifica veicolo',
				'all_items'     => 'Tutti i veicoli',
				'not_found'     => 'Nessun veicolo a noleggio',
				'menu_name'     => 'Noleggio',
			),
			'public'        => true,
			'has_archive'   => 'noleggio',
			'menu_icon'     => 'dashicons-calendar-alt',
			'menu_position' => 6,
			'supports'      => array( 'title', 'editor', 'thumbnail', 'excerpt' ),
			'rewrite'       => array( 'slug' => 'noleggio', 'with_front' => false ),
			'show_in_rest'  => true,
		)
	);
}
add_action( 'init', 'cauto_registra_noleggio' );

function cauto_campi_noleggio() {
	return array(
		'categoria'   => array(
			'label'   => 'Tipo di noleggio',
			'type'    => 'select',
			'options' => array(
				'breve'     => 'Noleggio giornaliero / auto sostitutiva',
				'cerimonie' => 'Cerimonie e matrimoni',
				'furgoni'   => 'Furgoni e trasporto',
			),
			'default' => 'breve',
		),
		'prezzo'      => array( 'label' => 'Prezzo (€)', 'type' => 'number', 'help' => 'Al giorno, oppure a cerimonia per i matrimoni' ),
		'prezzo_nota' => array( 'label' => 'Unità di prezzo', 'type' => 'text', 'help' => 'Es. al giorno, a cerimonia, a weekend', 'default' => 'al giorno' ),
		'posti'       => array( 'label' => 'Posti', 'type' => 'number' ),
		'porte'       => array( 'label' => 'Porte', 'type' => 'number' ),
		'cambio'      => array( 'label' => 'Cambio', 'type' => 'select', 'options' => 'cambio' ),
		'alimentazione' => array( 'label' => 'Alimentazione', 'type' => 'select', 'options' => 'alimentazione' ),
		'bagagli'     => array( 'label' => 'Bagagli', 'type' => 'text', 'help' => 'Es. 2 valigie grandi' ),
		'eta_minima'  => array( 'label' => 'Età minima del conducente', 'type' => 'number' ),
		'autista'     => array( 'label' => 'Disponibile con autista', 'type' => 'checkbox' ),
		'km_inclusi'  => array( 'label' => 'Km inclusi al giorno', 'type' => 'number' ),
		'incluso'     => array( 'label' => 'Cosa è incluso', 'type' => 'textarea', 'help' => 'Una voce per riga: assicurazione, addobbi, secondo guidatore…' ),
		'evidenza'    => array( 'label' => 'Metti in evidenza in home', 'type' => 'checkbox' ),
		'non_disponibile' => array( 'label' => 'Temporaneamente non disponibile', 'type' => 'checkbox' ),
	);
}

function cauto_opzioni_noleggio( $campo ) {
	$campi = cauto_campi_noleggio();
	if ( ! isset( $campi[ $campo ]['options'] ) ) {
		return array();
	}
	$opzioni = $campi[ $campo ]['options'];
	return is_array( $opzioni ) ? $opzioni : cauto_opzioni( $opzioni );
}

function cauto_campo_noleggio( $post_id, $chiave, $default = '' ) {
	$valore = get_post_meta( $post_id, '_noleggio_' . $chiave, true );
	if ( '' === $valore || null === $valore ) {
		$campi = cauto_campi_noleggio();
		return isset( $campi[ $chiave ]['default'] ) ? $campi[ $chiave ]['default'] : $default;
	}
	return $valore;
}

function cauto_prezzo_noleggio( $post_id ) {
	$prezzo = (int) cauto_campo_noleggio( $post_id, 'prezzo', 0 );
	if ( $prezzo <= 0 ) {
		return 'Preventivo su misura';
	}
	return number_format( $prezzo, 0, ',', '.' ) . ' €';
}

/**
 * Pannello dei dati e salvataggio: stessa logica delle auto in vendita,
 * con il prefisso _noleggio_.
 */
function cauto_meta_box_noleggio() {
	add_meta_box( 'cauto-noleggio', 'Dati del noleggio', 'cauto_meta_box_noleggio_html', 'noleggio', 'normal', 'high' );
	add_meta_box( 'cauto-noleggio-galleria', 'Galleria foto', 'cauto_galleria_html', 'noleggio', 'side', 'low' );
}
add_action( 'add_meta_boxes', 'cauto_meta_box_noleggio' );

function cauto_meta_box_noleggio_html( $post ) {
	wp_nonce_field( 'cauto_salva_noleggio_' . $post->ID, 'cauto_nonce_noleggio' );
	echo '<div class="cauto-campi">';

	foreach ( cauto_campi_noleggio() as $chiave => $campo ) {
		$valore = cauto_campo_noleggio( $post->ID, $chiave );
		$id     = 'noleggio_' . $chiave;
		$name   = 'noleggio[' . $chiave . ']';
		$classe = ( 'textarea' === $campo['type'] || 'checkbox' === $campo['type'] ) ? 'cauto-campo cauto-campo--largo' : 'cauto-campo';

		echo '<p class="' . esc_attr( $classe ) . '">';

		if ( 'checkbox' === $campo['type'] ) {
			printf(
				'<label for="%1$s"><input type="checkbox" id="%1$s" name="%2$s" value="1" %3$s> %4$s</label>',
				esc_attr( $id ),
				esc_attr( $name ),
				checked( $valore, '1', false ),
				esc_html( $campo['label'] )
			);
		} else {
			printf( '<label for="%s"><strong>%s</strong></label>', esc_attr( $id ), esc_html( $campo['label'] ) );

			if ( 'select' === $campo['type'] ) {
				echo '<select id="' . esc_attr( $id ) . '" name="' . esc_attr( $name ) . '">';
				echo '<option value="">— seleziona —</option>';
				foreach ( cauto_opzioni_noleggio( $chiave ) as $ov => $ol ) {
					$ov = is_int( $ov ) ? $ol : $ov;
					printf( '<option value="%s" %s>%s</option>', esc_attr( $ov ), selected( $valore, $ov, false ), esc_html( $ol ) );
				}
				echo '</select>';
			} elseif ( 'textarea' === $campo['type'] ) {
				printf( '<textarea id="%s" name="%s" rows="5">%s</textarea>', esc_attr( $id ), esc_attr( $name ), esc_textarea( $valore ) );
			} else {
				printf(
					'<input type="%s" id="%s" name="%s" value="%s">',
					esc_attr( $campo['type'] ),
					esc_attr( $id ),
					esc_attr( $name ),
					esc_attr( $valore )
				);
			}

			if ( ! empty( $campo['help'] ) ) {
				echo '<span class="cauto-help">' . esc_html( $campo['help'] ) . '</span>';
			}
		}

		echo '</p>';
	}

	echo '</div>';
}

function cauto_salva_noleggio( $post_id ) {
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! isset( $_POST['cauto_nonce_noleggio'] ) || ! wp_verify_nonce( sanitize_key( $_POST['cauto_nonce_noleggio'] ), 'cauto_salva_noleggio_' . $post_id ) ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	$inviati = isset( $_POST['noleggio'] ) && is_array( $_POST['noleggio'] ) ? wp_unslash( $_POST['noleggio'] ) : array();

	foreach ( cauto_campi_noleggio() as $chiave => $campo ) {
		$valore = isset( $inviati[ $chiave ] ) ? $inviati[ $chiave ] : '';

		switch ( $campo['type'] ) {
			case 'checkbox':
				$valore = $valore ? '1' : '';
				break;
			case 'number':
				$valore = ( '' === $valore ) ? '' : (string) absint( $valore );
				break;
			case 'select':
				$ammessi = cauto_opzioni_noleggio( $chiave );
				$chiavi  = array_keys( $ammessi );
				$ammessi = is_int( reset( $chiavi ) ) ? array_values( $ammessi ) : $chiavi;
				$valore  = in_array( $valore, $ammessi, true ) ? $valore : '';
				break;
			case 'textarea':
				$valore = sanitize_textarea_field( $valore );
				break;
			default:
				$valore = sanitize_text_field( $valore );
		}

		if ( '' === $valore ) {
			delete_post_meta( $post_id, '_noleggio_' . $chiave );
		} else {
			update_post_meta( $post_id, '_noleggio_' . $chiave, $valore );
		}
	}

	// La galleria usa lo stesso riquadro delle auto in vendita.
	$ids = isset( $_POST['cauto']['galleria'] )
		? array_filter( array_map( 'absint', explode( ',', (string) wp_unslash( $_POST['cauto']['galleria'] ) ) ) )
		: array();
	if ( $ids ) {
		update_post_meta( $post_id, '_auto_galleria', implode( ',', $ids ) );
	} else {
		delete_post_meta( $post_id, '_auto_galleria' );
	}
}
add_action( 'save_post_noleggio', 'cauto_salva_noleggio' );

/**
 * Card del veicolo a noleggio.
 */
function cauto_card_noleggio( $post_id ) {
	$immagini  = cauto_immagini( $post_id );
	$img       = $immagini ? wp_get_attachment_image( $immagini[0], 'medium_large', false, array( 'alt' => get_the_title( $post_id ), 'loading' => 'lazy' ) ) : '';
	$categorie = cauto_opzioni_noleggio( 'categoria' );
	$categoria = cauto_campo_noleggio( $post_id, 'categoria', 'breve' );

	$specs = array_filter(
		array(
			cauto_campo_noleggio( $post_id, 'posti' ) ? cauto_campo_noleggio( $post_id, 'posti' ) . ' posti' : '',
			cauto_campo_noleggio( $post_id, 'cambio' ),
			cauto_campo_noleggio( $post_id, 'alimentazione' ),
			cauto_campo_noleggio( $post_id, 'bagagli' ),
		)
	);

	ob_start();
	?>
	<article class="auto-card" data-noleggio data-categoria="<?php echo esc_attr( $categoria ); ?>">
		<div class="auto-card__media">
			<a href="<?php echo esc_url( get_permalink( $post_id ) ); ?>">
				<?php echo $img ? wp_kses_post( $img ) : '<span class="sr-only">Foto non disponibile</span>'; ?>
			</a>
			<div class="auto-card__badges">
				<?php if ( cauto_campo_noleggio( $post_id, 'autista' ) ) : ?>
					<span class="badge badge--accent">Con autista</span>
				<?php endif; ?>
				<?php if ( cauto_campo_noleggio( $post_id, 'non_disponibile' ) ) : ?>
					<span class="badge badge--muted">Non disponibile</span>
				<?php endif; ?>
			</div>
		</div>
		<div class="auto-card__body">
			<h3 class="auto-card__title">
				<a href="<?php echo esc_url( get_permalink( $post_id ) ); ?>"><?php echo esc_html( get_the_title( $post_id ) ); ?></a>
			</h3>
			<p class="auto-card__sub"><?php echo esc_html( isset( $categorie[ $categoria ] ) ? $categorie[ $categoria ] : '' ); ?></p>
			<ul class="specs">
				<?php foreach ( $specs as $spec ) : ?>
					<li><?php echo esc_html( $spec ); ?></li>
				<?php endforeach; ?>
			</ul>
			<div class="auto-card__foot">
				<p class="price">
					<?php echo esc_html( cauto_prezzo_noleggio( $post_id ) ); ?>
					<small><?php echo esc_html( cauto_campo_noleggio( $post_id, 'prezzo_nota' ) ); ?></small>
				</p>
				<a class="btn btn--dark btn--sm" href="<?php echo esc_url( get_permalink( $post_id ) ); ?>">Dettagli</a>
			</div>
		</div>
	</article>
	<?php
	return ob_get_clean();
}

/**
 * [noleggio_catalogo categoria="cerimonie"] — elenco dei veicoli a noleggio.
 */
function cauto_shortcode_noleggio( $atts ) {
	$atts = shortcode_atts( array( 'categoria' => '', 'limite' => 30 ), $atts, 'noleggio_catalogo' );

	$args = array(
		'post_type'      => 'noleggio',
		'posts_per_page' => (int) $atts['limite'],
	);

	if ( $atts['categoria'] ) {
		$args['meta_query'] = array(
			array( 'key' => '_noleggio_categoria', 'value' => sanitize_text_field( $atts['categoria'] ) ),
		);
	}

	$veicoli = new WP_Query( $args );

	ob_start();
	if ( $veicoli->have_posts() ) {
		echo '<div class="auto-grid">';
		while ( $veicoli->have_posts() ) {
			$veicoli->the_post();
			echo cauto_card_noleggio( get_the_ID() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		}
		echo '</div>';
	} else {
		echo '<p class="empty-state">Stiamo aggiornando la flotta: scrivici e ti diciamo cosa è disponibile.</p>';
	}
	wp_reset_postdata();
	return ob_get_clean();
}
add_shortcode( 'noleggio_catalogo', 'cauto_shortcode_noleggio' );

/**
 * Scheda del veicolo a noleggio, costruita dentro il tema come quella delle auto.
 */
function cauto_scheda_noleggio( $content ) {
	if ( ! is_singular( 'noleggio' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}

	$post_id   = get_the_ID();
	$immagini  = cauto_immagini( $post_id );
	$categorie = cauto_opzioni_noleggio( 'categoria' );
	$categoria = cauto_campo_noleggio( $post_id, 'categoria', 'breve' );
	$telefono  = cauto_impostazione( 'telefono' );
	$wa        = cauto_link_whatsapp(
		$post_id,
		sprintf( 'Salve, vorrei informazioni sul noleggio di: %s.', get_the_title( $post_id ) )
	);

	$dati = array_filter(
		array(
			'Tipo di noleggio' => isset( $categorie[ $categoria ] ) ? $categorie[ $categoria ] : '',
			'Posti'            => cauto_campo_noleggio( $post_id, 'posti' ),
			'Porte'            => cauto_campo_noleggio( $post_id, 'porte' ),
			'Cambio'           => cauto_campo_noleggio( $post_id, 'cambio' ),
			'Alimentazione'    => cauto_campo_noleggio( $post_id, 'alimentazione' ),
			'Bagagli'          => cauto_campo_noleggio( $post_id, 'bagagli' ),
			'Km inclusi'       => cauto_campo_noleggio( $post_id, 'km_inclusi' ) ? cauto_campo_noleggio( $post_id, 'km_inclusi' ) . ' km al giorno' : '',
			'Età minima'       => cauto_campo_noleggio( $post_id, 'eta_minima' ) ? cauto_campo_noleggio( $post_id, 'eta_minima' ) . ' anni' : '',
		)
	);

	$incluso = array_filter( array_map( 'trim', explode( "\n", (string) cauto_campo_noleggio( $post_id, 'incluso' ) ) ) );

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
				<p><?php echo esc_html( isset( $categorie[ $categoria ] ) ? $categorie[ $categoria ] : '' ); ?></p>
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
				<?php echo $content; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
			<?php endif; ?>

			<?php if ( $incluso ) : ?>
				<h2>Incluso nel noleggio</h2>
				<ul class="optionals">
					<?php foreach ( $incluso as $voce ) : ?>
						<li><?php echo esc_html( $voce ); ?></li>
					<?php endforeach; ?>
				</ul>
			<?php endif; ?>
		</div>

		<aside class="aside-card">
			<p class="price">
				<?php echo esc_html( cauto_prezzo_noleggio( $post_id ) ); ?>
				<small><?php echo esc_html( cauto_campo_noleggio( $post_id, 'prezzo_nota' ) ); ?></small>
			</p>
			<div class="aside-card__actions">
				<?php if ( $wa ) : ?>
					<a class="btn btn--wa btn--block" href="<?php echo esc_url( $wa ); ?>" target="_blank" rel="noopener">Verifica disponibilità</a>
				<?php endif; ?>
				<?php if ( $telefono ) : ?>
					<a class="btn btn--dark btn--block" href="tel:<?php echo esc_attr( preg_replace( '/\s+/', '', $telefono ) ); ?>">Chiama <?php echo esc_html( $telefono ); ?></a>
				<?php endif; ?>
			</div>
			<p class="aside-card__note">Prezzi indicativi: variano con i giorni di noleggio e il periodo. Ti confermiamo il preventivo in giornata.</p>
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
add_filter( 'the_content', 'cauto_scheda_noleggio' );

/**
 * Colonne dell'elenco noleggio in bacheca.
 */
function cauto_colonne_noleggio( $colonne ) {
	$nuove = array();
	foreach ( $colonne as $chiave => $etichetta ) {
		$nuove[ $chiave ] = $etichetta;
		if ( 'title' === $chiave ) {
			$nuove['noleggio_categoria'] = 'Tipo';
			$nuove['noleggio_prezzo']    = 'Prezzo';
		}
	}
	return $nuove;
}
add_filter( 'manage_noleggio_posts_columns', 'cauto_colonne_noleggio' );

function cauto_colonna_noleggio( $colonna, $post_id ) {
	if ( 'noleggio_categoria' === $colonna ) {
		$categorie = cauto_opzioni_noleggio( 'categoria' );
		$categoria = cauto_campo_noleggio( $post_id, 'categoria', 'breve' );
		echo esc_html( isset( $categorie[ $categoria ] ) ? $categorie[ $categoria ] : '—' );
	}
	if ( 'noleggio_prezzo' === $colonna ) {
		echo esc_html( cauto_prezzo_noleggio( $post_id ) . ' ' . cauto_campo_noleggio( $post_id, 'prezzo_nota' ) );
	}
}
add_action( 'manage_noleggio_posts_custom_column', 'cauto_colonna_noleggio', 10, 2 );
