<?php
/**
 * Tipo di contenuto "Auto" e tassonomia "Marca".
 * E' quello che fa comparire la voce Auto nel menu della bacheca.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cauto_register_post_type() {
	register_post_type(
		'auto',
		array(
			'labels'        => array(
				'name'               => 'Auto',
				'singular_name'      => 'Auto',
				'add_new'            => 'Aggiungi auto',
				'add_new_item'       => 'Aggiungi una nuova auto',
				'edit_item'          => 'Modifica auto',
				'new_item'           => 'Nuova auto',
				'view_item'          => 'Vedi la scheda',
				'search_items'       => 'Cerca tra le auto',
				'not_found'          => 'Nessuna auto inserita',
				'not_found_in_trash' => 'Nessuna auto nel cestino',
				'all_items'          => 'Tutte le auto',
				'menu_name'          => 'Auto',
			),
			'public'        => true,
			'has_archive'   => 'auto-usate',
			'menu_icon'     => 'dashicons-dashboard',
			'menu_position' => 5,
			'supports'      => array( 'title', 'editor', 'thumbnail', 'excerpt' ),
			'rewrite'       => array( 'slug' => 'auto', 'with_front' => false ),
			'show_in_rest'  => true,
		)
	);

	register_taxonomy(
		'marca_auto',
		'auto',
		array(
			'labels'            => array(
				'name'          => 'Marche',
				'singular_name' => 'Marca',
				'add_new_item'  => 'Aggiungi una marca',
				'menu_name'     => 'Marche',
			),
			'public'            => true,
			'hierarchical'      => true, // elenco con le spunte: il cliente sceglie, non riscrive
			'show_admin_column' => true,
			'show_in_rest'      => true,
			'rewrite'           => array( 'slug' => 'marca' ),
		)
	);
}
add_action( 'init', 'cauto_register_post_type' );

/**
 * Nell'archivio e nelle pagine marca: prima le disponibili, poi le vendute.
 */
function cauto_ordina_archivio( $query ) {
	if ( is_admin() || ! $query->is_main_query() ) {
		return;
	}
	if ( $query->is_post_type_archive( 'auto' ) || $query->is_tax( 'marca_auto' ) ) {
		$query->set( 'posts_per_page', 24 );
		$query->set( 'meta_key', '_auto_stato' );
		$query->set( 'orderby', array( 'meta_value' => 'ASC', 'date' => 'DESC' ) );
	}
}
add_action( 'pre_get_posts', 'cauto_ordina_archivio' );

/**
 * Colonne dell'elenco auto in bacheca: foto, prezzo, km, anno e stato a colpo d'occhio.
 */
function cauto_colonne( $colonne ) {
	$nuove = array();
	foreach ( $colonne as $chiave => $etichetta ) {
		if ( 'title' === $chiave ) {
			$nuove['cauto_foto'] = 'Foto';
		}
		$nuove[ $chiave ] = $etichetta;
		if ( 'title' === $chiave ) {
			$nuove['cauto_prezzo'] = 'Prezzo';
			$nuove['cauto_km']     = 'Km';
			$nuove['cauto_anno']   = 'Immatr.';
			$nuove['cauto_stato']  = 'Stato';
		}
	}
	return $nuove;
}
add_filter( 'manage_auto_posts_columns', 'cauto_colonne' );

function cauto_colonna_contenuto( $colonna, $post_id ) {
	switch ( $colonna ) {
		case 'cauto_foto':
			$immagini = cauto_immagini( $post_id );
			echo $immagini
				? wp_kses_post( wp_get_attachment_image( $immagini[0], array( 70, 52 ), false, array( 'style' => 'border-radius:6px;object-fit:cover;' ) ) )
				: '—';
			break;
		case 'cauto_prezzo':
			echo esc_html( cauto_prezzo( $post_id ) );
			break;
		case 'cauto_km':
			echo esc_html( cauto_km( $post_id ) ?: '—' );
			break;
		case 'cauto_anno':
			echo esc_html( cauto_immatricolazione( $post_id ) ?: '—' );
			break;
		case 'cauto_stato':
			$stato     = cauto_campo( $post_id, 'stato', 'disponibile' );
			$etichette = cauto_opzioni( 'stato' );
			echo esc_html( isset( $etichette[ $stato ] ) ? $etichette[ $stato ] : $stato );
			break;
	}
}
add_action( 'manage_auto_posts_custom_column', 'cauto_colonna_contenuto', 10, 2 );
