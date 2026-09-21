<?php
/**
 * Dati strutturati della scheda auto (schema.org/Car).
 * Servono a Google per capire prezzo, chilometri e disponibilita' del veicolo.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cauto_dati_strutturati() {
	if ( ! is_singular( 'auto' ) ) {
		return;
	}

	$post_id  = get_queried_object_id();
	$stato    = cauto_campo( $post_id, 'stato', 'disponibile' );
	$immagini = cauto_immagini( $post_id );

	$dati = array(
		'@context'    => 'https://schema.org',
		'@type'       => 'Car',
		'name'        => get_the_title( $post_id ),
		'url'         => get_permalink( $post_id ),
		'description' => wp_strip_all_tags( get_the_excerpt( $post_id ) ),
	);

	if ( $immagini ) {
		$dati['image'] = array_values(
			array_filter(
				array_map(
					static function ( $id ) {
						return wp_get_attachment_image_url( $id, 'large' );
					},
					$immagini
				)
			)
		);
	}

	$marca = cauto_marca_nome( $post_id );
	if ( $marca ) {
		$dati['brand'] = array( '@type' => 'Brand', 'name' => $marca );
	}

	$km = cauto_campo( $post_id, 'km' );
	if ( $km ) {
		$dati['mileageFromOdometer'] = array( '@type' => 'QuantitativeValue', 'value' => (int) $km, 'unitCode' => 'KMT' );
	}

	$anno = cauto_immatricolazione( $post_id, true );
	if ( $anno ) {
		$dati['productionDate'] = $anno;
	}

	$alimentazione = cauto_campo( $post_id, 'alimentazione' );
	if ( $alimentazione ) {
		$dati['fuelType'] = $alimentazione;
	}

	$cambio = cauto_campo( $post_id, 'cambio' );
	if ( $cambio ) {
		$dati['vehicleTransmission'] = $cambio;
	}

	$prezzo = (int) cauto_campo( $post_id, 'prezzo', 0 );
	if ( $prezzo > 0 && ! cauto_campo( $post_id, 'trattativa' ) ) {
		$dati['offers'] = array(
			'@type'         => 'Offer',
			'price'         => $prezzo,
			'priceCurrency' => 'EUR',
			'availability'  => 'venduta' === $stato ? 'https://schema.org/SoldOut' : 'https://schema.org/InStock',
			'url'           => get_permalink( $post_id ),
		);

		$venditore = cauto_impostazione( 'nome' );
		if ( $venditore ) {
			$dati['offers']['seller'] = array( '@type' => 'AutoDealer', 'name' => $venditore );
		}
	}

	printf(
		'<script type="application/ld+json">%s</script>' . "\n",
		wp_json_encode( $dati, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
	);
}
add_action( 'wp_head', 'cauto_dati_strutturati' );
