<?php
/**
 * Plugin Name:       Concessionaria Auto
 * Description:       Catalogo auto usate: il cliente inserisce i veicoli dalla bacheca WordPress, il sito mostra catalogo con filtri e scheda veicolo.
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            Idea Marketing di Coppola Fortunato
 * Text Domain:       concessionaria-auto
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'CAUTO_VERSION', '1.0.0' );
define( 'CAUTO_FILE', __FILE__ );
define( 'CAUTO_DIR', plugin_dir_path( __FILE__ ) );
define( 'CAUTO_URL', plugin_dir_url( __FILE__ ) );

require_once CAUTO_DIR . 'inc/helpers.php';
require_once CAUTO_DIR . 'inc/post-type.php';
require_once CAUTO_DIR . 'inc/campi.php';
require_once CAUTO_DIR . 'inc/impostazioni.php';
require_once CAUTO_DIR . 'inc/shortcodes.php';
require_once CAUTO_DIR . 'inc/scheda.php';
require_once CAUTO_DIR . 'inc/contatti.php';
require_once CAUTO_DIR . 'inc/seo.php';

/**
 * Fogli di stile e script del front-end.
 * Sono gli stessi file usati dalla demo statica, cosi' il sito vero e la demo
 * restano identici e si correggono in un punto solo.
 */
function cauto_assets() {
	wp_enqueue_style( 'concessionaria-auto', CAUTO_URL . 'assets/auto.css', array(), CAUTO_VERSION );
	wp_enqueue_script( 'concessionaria-auto', CAUTO_URL . 'assets/auto.js', array(), CAUTO_VERSION, true );
}
add_action( 'wp_enqueue_scripts', 'cauto_assets' );

/**
 * La classe sulle pagine serve a limitare gli stili del catalogo al nostro markup.
 */
function cauto_body_class( $classes ) {
	$classes[] = 'auto-site';
	return $classes;
}
add_filter( 'body_class', 'cauto_body_class' );

/**
 * All'attivazione registriamo il tipo di contenuto e riscriviamo i permalink,
 * altrimenti le schede auto darebbero 404 fino al primo salvataggio dei permalink.
 */
function cauto_activate() {
	cauto_register_post_type();
	flush_rewrite_rules();
}
register_activation_hook( __FILE__, 'cauto_activate' );

function cauto_deactivate() {
	flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, 'cauto_deactivate' );
