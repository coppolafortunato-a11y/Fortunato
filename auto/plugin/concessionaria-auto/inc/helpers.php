<?php
/**
 * Definizione dei campi veicolo, formattazione e pezzi di markup riusati
 * da catalogo e scheda.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Elenco delle voci a tendina. Cambiare qui significa cambiarle ovunque:
 * pannello di inserimento, filtri del catalogo e scheda.
 */
function cauto_opzioni( $campo ) {
	$opzioni = array(
		'alimentazione' => array( 'Benzina', 'Diesel', 'GPL', 'Metano', 'Ibrida', 'Ibrida plug-in', 'Elettrica' ),
		'cambio'        => array( 'Manuale', 'Automatico', 'Semiautomatico' ),
		'carrozzeria'   => array( 'Utilitaria', 'Berlina', 'Station Wagon', 'SUV', 'Coupé', 'Cabrio', 'Monovolume', 'Furgone' ),
		'classe'        => array( 'Euro 6', 'Euro 5', 'Euro 4', 'Euro 3' ),
		'stato'         => array(
			'disponibile' => 'Disponibile',
			'prenotata'   => 'Prenotata',
			'venduta'     => 'Venduta',
			'in-arrivo'   => 'In arrivo',
		),
	);

	return isset( $opzioni[ $campo ] ) ? $opzioni[ $campo ] : array();
}

/**
 * Campi del veicolo: chiave => etichetta, tipo, suffisso mostrato in scheda.
 */
function cauto_campi() {
	return array(
		'prezzo'          => array( 'label' => 'Prezzo (€)', 'type' => 'number', 'help' => 'Solo numeri, es. 12900' ),
		'trattativa'      => array( 'label' => 'Prezzo su richiesta (nascondi il prezzo)', 'type' => 'checkbox' ),
		'km'              => array( 'label' => 'Chilometri', 'type' => 'number' ),
		'immatricolazione'=> array( 'label' => 'Immatricolazione', 'type' => 'month', 'help' => 'Mese e anno' ),
		'alimentazione'   => array( 'label' => 'Alimentazione', 'type' => 'select', 'options' => 'alimentazione' ),
		'cambio'          => array( 'label' => 'Cambio', 'type' => 'select', 'options' => 'cambio' ),
		'carrozzeria'     => array( 'label' => 'Carrozzeria', 'type' => 'select', 'options' => 'carrozzeria' ),
		'potenza'         => array( 'label' => 'Potenza (CV)', 'type' => 'number' ),
		'cilindrata'      => array( 'label' => 'Cilindrata (cc)', 'type' => 'number' ),
		'porte'           => array( 'label' => 'Porte', 'type' => 'number' ),
		'posti'           => array( 'label' => 'Posti', 'type' => 'number' ),
		'colore'          => array( 'label' => 'Colore', 'type' => 'text' ),
		'classe'          => array( 'label' => 'Classe ambientale', 'type' => 'select', 'options' => 'classe' ),
		'garanzia'        => array( 'label' => 'Garanzia (mesi)', 'type' => 'number' ),
		'neopatentati'    => array( 'label' => 'Adatta ai neopatentati', 'type' => 'checkbox' ),
		'allestimento'    => array( 'label' => 'Allestimento / versione', 'type' => 'text', 'help' => 'Es. Business, Sport, S-Line' ),
		'stato'           => array( 'label' => 'Stato', 'type' => 'select', 'options' => 'stato', 'default' => 'disponibile' ),
		'evidenza'        => array( 'label' => 'Metti in evidenza in home', 'type' => 'checkbox' ),
		'optional'        => array( 'label' => 'Dotazioni e optional', 'type' => 'textarea', 'help' => 'Una voce per riga' ),
	);
}

/**
 * Valore di un campo del veicolo.
 */
function cauto_campo( $post_id, $chiave, $default = '' ) {
	$valore = get_post_meta( $post_id, '_auto_' . $chiave, true );
	if ( '' === $valore || null === $valore ) {
		$campi = cauto_campi();
		if ( isset( $campi[ $chiave ]['default'] ) ) {
			return $campi[ $chiave ]['default'];
		}
		return $default;
	}
	return $valore;
}

function cauto_impostazione( $chiave, $default = '' ) {
	$opzioni = get_option( 'cauto_impostazioni', array() );
	return ( isset( $opzioni[ $chiave ] ) && '' !== $opzioni[ $chiave ] ) ? $opzioni[ $chiave ] : $default;
}

/**
 * 12900 => "12.900 €"
 */
function cauto_prezzo( $post_id ) {
	if ( cauto_campo( $post_id, 'trattativa' ) ) {
		return 'Trattativa riservata';
	}
	$prezzo = (int) cauto_campo( $post_id, 'prezzo', 0 );
	if ( $prezzo <= 0 ) {
		return 'Prezzo su richiesta';
	}
	return number_format( $prezzo, 0, ',', '.' ) . ' €';
}

/**
 * 145000 => "145.000 km"
 */
function cauto_km( $post_id ) {
	$km = cauto_campo( $post_id, 'km', '' );
	if ( '' === $km ) {
		return '';
	}
	return number_format( (int) $km, 0, ',', '.' ) . ' km';
}

/**
 * "2019-06" => "06/2019"; l'anno da solo serve ai filtri.
 */
function cauto_immatricolazione( $post_id, $solo_anno = false ) {
	$valore = (string) cauto_campo( $post_id, 'immatricolazione', '' );
	if ( ! preg_match( '/^(\d{4})-(\d{2})/', $valore, $m ) ) {
		return '';
	}
	return $solo_anno ? $m[1] : $m[2] . '/' . $m[1];
}

function cauto_marche( $post_id ) {
	$termini = get_the_terms( $post_id, 'marca_auto' );
	if ( is_wp_error( $termini ) || empty( $termini ) ) {
		return array();
	}
	return $termini;
}

function cauto_marca_nome( $post_id ) {
	$termini = cauto_marche( $post_id );
	return $termini ? $termini[0]->name : '';
}

/**
 * Immagini della scheda: immagine in evidenza + galleria, senza duplicati.
 */
function cauto_immagini( $post_id ) {
	$ids = array();

	$featured = get_post_thumbnail_id( $post_id );
	if ( $featured ) {
		$ids[] = (int) $featured;
	}

	$galleria = cauto_campo( $post_id, 'galleria', '' );
	if ( $galleria ) {
		foreach ( explode( ',', $galleria ) as $id ) {
			$id = (int) trim( $id );
			if ( $id && ! in_array( $id, $ids, true ) ) {
				$ids[] = $id;
			}
		}
	}

	return $ids;
}

/**
 * Link WhatsApp precompilato con l'auto di cui si sta parlando.
 */
function cauto_link_whatsapp( $post_id = 0, $testo = '' ) {
	$numero = preg_replace( '/\D/', '', cauto_impostazione( 'whatsapp' ) );
	if ( ! $numero ) {
		return '';
	}

	if ( ! $testo ) {
		$testo = $post_id
			? sprintf( 'Salve, sono interessato a: %s (%s). È ancora disponibile?', get_the_title( $post_id ), cauto_prezzo( $post_id ) )
			: 'Salve, vorrei informazioni sulle auto disponibili.';
	}

	return 'https://wa.me/' . $numero . '?text=' . rawurlencode( $testo );
}

/**
 * Etichetta colorata sullo stato del veicolo.
 */
function cauto_badge_stato( $post_id ) {
	$stato  = cauto_campo( $post_id, 'stato', 'disponibile' );
	$classi = array(
		'disponibile' => 'badge--ok',
		'prenotata'   => 'badge--muted',
		'venduta'     => 'badge--muted',
		'in-arrivo'   => 'badge--muted',
	);
	$etichette = cauto_opzioni( 'stato' );

	if ( 'disponibile' === $stato || ! isset( $etichette[ $stato ] ) ) {
		return '';
	}

	return sprintf(
		'<span class="badge %s">%s</span>',
		esc_attr( $classi[ $stato ] ),
		esc_html( $etichette[ $stato ] )
	);
}

/**
 * Card del catalogo. Gli attributi data- sono cio' su cui lavorano i filtri.
 */
function cauto_card( $post_id ) {
	$immagini = cauto_immagini( $post_id );
	$img      = $immagini ? wp_get_attachment_image( $immagini[0], 'medium_large', false, array( 'alt' => get_the_title( $post_id ), 'loading' => 'lazy' ) ) : '';
	$stato    = cauto_campo( $post_id, 'stato', 'disponibile' );

	$specs = array_filter( array(
		cauto_km( $post_id ),
		cauto_immatricolazione( $post_id ),
		cauto_campo( $post_id, 'alimentazione' ),
		cauto_campo( $post_id, 'cambio' ),
	) );

	ob_start();
	?>
	<article class="auto-card<?php echo 'venduta' === $stato ? ' auto-card--venduta' : ''; ?>"
		data-auto
		data-nome="<?php echo esc_attr( get_the_title( $post_id ) ); ?>"
		data-marca="<?php echo esc_attr( cauto_marca_nome( $post_id ) ); ?>"
		data-allestimento="<?php echo esc_attr( cauto_campo( $post_id, 'allestimento' ) ); ?>"
		data-prezzo="<?php echo esc_attr( cauto_campo( $post_id, 'prezzo' ) ); ?>"
		data-km="<?php echo esc_attr( cauto_campo( $post_id, 'km' ) ); ?>"
		data-anno="<?php echo esc_attr( cauto_immatricolazione( $post_id, true ) ); ?>"
		data-alimentazione="<?php echo esc_attr( cauto_campo( $post_id, 'alimentazione' ) ); ?>"
		data-cambio="<?php echo esc_attr( cauto_campo( $post_id, 'cambio' ) ); ?>"
		data-stato="<?php echo esc_attr( $stato ); ?>">
		<div class="auto-card__media">
			<a href="<?php echo esc_url( get_permalink( $post_id ) ); ?>">
				<?php echo $img ? wp_kses_post( $img ) : '<span class="sr-only">Foto non disponibile</span>'; ?>
			</a>
			<div class="auto-card__badges">
				<?php
				echo cauto_badge_stato( $post_id ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
				if ( cauto_campo( $post_id, 'neopatentati' ) ) {
					echo '<span class="badge">Neopatentati</span>';
				}
				?>
			</div>
		</div>
		<div class="auto-card__body">
			<h3 class="auto-card__title">
				<a href="<?php echo esc_url( get_permalink( $post_id ) ); ?>"><?php echo esc_html( get_the_title( $post_id ) ); ?></a>
			</h3>
			<p class="auto-card__sub"><?php echo esc_html( cauto_campo( $post_id, 'allestimento' ) ); ?></p>
			<ul class="specs">
				<?php foreach ( $specs as $spec ) : ?>
					<li><?php echo esc_html( $spec ); ?></li>
				<?php endforeach; ?>
			</ul>
			<div class="auto-card__foot">
				<p class="price"><?php echo esc_html( cauto_prezzo( $post_id ) ); ?></p>
				<a class="btn btn--dark btn--sm" href="<?php echo esc_url( get_permalink( $post_id ) ); ?>">Dettagli</a>
			</div>
		</div>
	</article>
	<?php
	return ob_get_clean();
}
