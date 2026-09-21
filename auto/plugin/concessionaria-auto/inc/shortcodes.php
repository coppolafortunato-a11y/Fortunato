<?php
/**
 * Shortcode da inserire nelle pagine: catalogo con filtri, auto in evidenza,
 * barra di ricerca rapida.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Marche effettivamente presenti a catalogo (niente voci vuote nel filtro).
 */
function cauto_lista_marche() {
	$termini = get_terms( array( 'taxonomy' => 'marca_auto', 'hide_empty' => true ) );
	return is_wp_error( $termini ) ? array() : $termini;
}

/**
 * Barra dei filtri. In pagina catalogo filtra le card gia' caricate;
 * altrove (es. home) manda al catalogo con i filtri nell'indirizzo.
 */
function cauto_form_filtri( $completo = true, $action = '' ) {
	$valore = static function ( $chiave ) {
		return isset( $_GET[ $chiave ] ) ? sanitize_text_field( wp_unslash( $_GET[ $chiave ] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Recommended
	};

	ob_start();
	?>
	<form class="filters<?php echo $completo ? '' : ' filters--float'; ?>"
		<?php echo $completo ? 'data-auto-filtri' : ''; ?>
		method="get"
		action="<?php echo esc_url( $action ? $action : get_post_type_archive_link( 'auto' ) ); ?>">
		<div class="filters__grid">
			<div class="field">
				<label for="cauto-q">Marca o modello</label>
				<input type="search" id="cauto-q" name="q" value="<?php echo esc_attr( $valore( 'q' ) ); ?>" placeholder="Es. Panda, Golf, Audi">
			</div>
			<div class="field">
				<label for="cauto-marca">Marca</label>
				<select id="cauto-marca" name="marca">
					<option value="">Tutte</option>
					<?php foreach ( cauto_lista_marche() as $marca ) : ?>
						<option value="<?php echo esc_attr( $marca->name ); ?>" <?php selected( $valore( 'marca' ), $marca->name ); ?>>
							<?php echo esc_html( $marca->name ); ?>
						</option>
					<?php endforeach; ?>
				</select>
			</div>
			<div class="field">
				<label for="cauto-prezzo">Prezzo massimo</label>
				<select id="cauto-prezzo" name="prezzo_max">
					<option value="">Qualsiasi</option>
					<?php foreach ( array( 5000, 8000, 10000, 15000, 20000, 30000, 50000 ) as $soglia ) : ?>
						<option value="<?php echo esc_attr( $soglia ); ?>" <?php selected( $valore( 'prezzo_max' ), (string) $soglia ); ?>>
							fino a <?php echo esc_html( number_format( $soglia, 0, ',', '.' ) ); ?> €
						</option>
					<?php endforeach; ?>
				</select>
			</div>
			<div class="field">
				<label for="cauto-alimentazione">Alimentazione</label>
				<select id="cauto-alimentazione" name="alimentazione">
					<option value="">Tutte</option>
					<?php foreach ( cauto_opzioni( 'alimentazione' ) as $voce ) : ?>
						<option value="<?php echo esc_attr( $voce ); ?>" <?php selected( $valore( 'alimentazione' ), $voce ); ?>><?php echo esc_html( $voce ); ?></option>
					<?php endforeach; ?>
				</select>
			</div>
			<?php if ( $completo ) : ?>
				<div class="field">
					<label for="cauto-cambio">Cambio</label>
					<select id="cauto-cambio" name="cambio">
						<option value="">Tutti</option>
						<?php foreach ( cauto_opzioni( 'cambio' ) as $voce ) : ?>
							<option value="<?php echo esc_attr( $voce ); ?>" <?php selected( $valore( 'cambio' ), $voce ); ?>><?php echo esc_html( $voce ); ?></option>
						<?php endforeach; ?>
					</select>
				</div>
				<div class="field">
					<label for="cauto-km">Km massimi</label>
					<select id="cauto-km" name="km_max">
						<option value="">Qualsiasi</option>
						<?php foreach ( array( 30000, 60000, 100000, 150000, 200000 ) as $soglia ) : ?>
							<option value="<?php echo esc_attr( $soglia ); ?>" <?php selected( $valore( 'km_max' ), (string) $soglia ); ?>>
								fino a <?php echo esc_html( number_format( $soglia, 0, ',', '.' ) ); ?> km
							</option>
						<?php endforeach; ?>
					</select>
				</div>
				<div class="field">
					<label for="cauto-anno">Dall'anno</label>
					<select id="cauto-anno" name="anno_min">
						<option value="">Qualsiasi</option>
						<?php
						$anno_corrente = (int) gmdate( 'Y' );
						for ( $anno = $anno_corrente; $anno >= $anno_corrente - 20; $anno -- ) :
							?>
							<option value="<?php echo esc_attr( $anno ); ?>" <?php selected( $valore( 'anno_min' ), (string) $anno ); ?>><?php echo esc_html( $anno ); ?></option>
						<?php endfor; ?>
					</select>
				</div>
				<div class="field">
					<label for="cauto-ordina">Ordina per</label>
					<select id="cauto-ordina" name="ordina">
						<option value="">Più recenti</option>
						<option value="prezzo_asc" <?php selected( $valore( 'ordina' ), 'prezzo_asc' ); ?>>Prezzo crescente</option>
						<option value="prezzo_desc" <?php selected( $valore( 'ordina' ), 'prezzo_desc' ); ?>>Prezzo decrescente</option>
						<option value="km_asc" <?php selected( $valore( 'ordina' ), 'km_asc' ); ?>>Meno chilometri</option>
						<option value="anno_desc" <?php selected( $valore( 'ordina' ), 'anno_desc' ); ?>>Immatricolazione recente</option>
					</select>
				</div>
			<?php endif; ?>
		</div>
		<div class="filters__actions">
			<?php if ( $completo ) : ?>
				<p class="filters__count" data-auto-count></p>
				<button type="reset" class="btn btn--ghost btn--sm">Azzera i filtri</button>
			<?php else : ?>
				<span class="filters__count">Cerca tra le auto disponibili</span>
				<button type="submit" class="btn btn--primary">Vedi le auto</button>
			<?php endif; ?>
		</div>
	</form>
	<?php
	return ob_get_clean();
}

/**
 * [auto_catalogo] — filtri + tutte le auto pubblicate.
 */
function cauto_shortcode_catalogo( $atts ) {
	$atts = shortcode_atts(
		array(
			'limite'  => 60,
			'vendute' => 'si', // "no" per nascondere le auto gia' vendute
		),
		$atts,
		'auto_catalogo'
	);

	$args = array(
		'post_type'      => 'auto',
		'posts_per_page' => (int) $atts['limite'],
		'meta_key'       => '_auto_stato',
		'orderby'        => array( 'meta_value' => 'ASC', 'date' => 'DESC' ),
	);

	if ( 'no' === $atts['vendute'] ) {
		$args['meta_query'] = array(
			array(
				'key'     => '_auto_stato',
				'value'   => 'venduta',
				'compare' => '!=',
			),
		);
	}

	$auto = new WP_Query( $args );

	ob_start();
	// Markup generato da noi, gia' filtrato campo per campo: wp_kses_post()
	// qui toglierebbe il <form> e gli attributi data- su cui lavorano i filtri.
	echo cauto_form_filtri( true ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped

	if ( $auto->have_posts() ) {
		echo '<div class="auto-grid" data-auto-grid style="margin-top:28px">';
		while ( $auto->have_posts() ) {
			$auto->the_post();
			echo cauto_card( get_the_ID() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		}
		echo '</div>';
		echo '<p class="empty-state" data-auto-empty hidden style="margin-top:28px">Nessuna auto corrisponde ai filtri scelti. Prova ad allargare la ricerca.</p>';
	} else {
		echo '<p class="empty-state" style="margin-top:28px">Il catalogo è in aggiornamento: contattaci, abbiamo altre auto in arrivo.</p>';
	}

	wp_reset_postdata();
	return ob_get_clean();
}
add_shortcode( 'auto_catalogo', 'cauto_shortcode_catalogo' );

/**
 * [auto_evidenza limite="3"] — le auto segnate "in evidenza".
 */
function cauto_shortcode_evidenza( $atts ) {
	$atts = shortcode_atts( array( 'limite' => 3 ), $atts, 'auto_evidenza' );

	$auto = new WP_Query(
		array(
			'post_type'      => 'auto',
			'posts_per_page' => (int) $atts['limite'],
			'meta_query'     => array(
				array( 'key' => '_auto_evidenza', 'value' => '1' ),
				array( 'key' => '_auto_stato', 'value' => 'venduta', 'compare' => '!=' ),
			),
		)
	);

	// Se nessuna auto e' stata messa in evidenza mostriamo comunque le ultime inserite.
	if ( ! $auto->have_posts() ) {
		$auto = new WP_Query(
			array(
				'post_type'      => 'auto',
				'posts_per_page' => (int) $atts['limite'],
			)
		);
	}

	ob_start();
	if ( $auto->have_posts() ) {
		echo '<div class="auto-grid">';
		while ( $auto->have_posts() ) {
			$auto->the_post();
			echo cauto_card( get_the_ID() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		}
		echo '</div>';
	}
	wp_reset_postdata();
	return ob_get_clean();
}
add_shortcode( 'auto_evidenza', 'cauto_shortcode_evidenza' );

/**
 * [auto_ricerca] — barra di ricerca rapida da mettere in home.
 */
function cauto_shortcode_ricerca( $atts ) {
	$atts = shortcode_atts( array( 'destinazione' => '' ), $atts, 'auto_ricerca' );
	return cauto_form_filtri( false, $atts['destinazione'] );
}
add_shortcode( 'auto_ricerca', 'cauto_shortcode_ricerca' );
