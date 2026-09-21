<?php
/**
 * Pagina "Impostazioni" sotto il menu Auto: recapiti usati dai pulsanti
 * WhatsApp/telefono e indirizzo e-mail a cui arrivano le richieste.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cauto_campi_impostazioni() {
	return array(
		'nome'      => array( 'Nome della concessionaria', 'text' ),
		'telefono'  => array( 'Telefono', 'text' ),
		'whatsapp'  => array( 'Numero WhatsApp', 'text', 'Con prefisso internazionale, es. 393206116711' ),
		'email'     => array( 'E-mail per le richieste', 'email', 'Qui arrivano i messaggi inviati dal sito' ),
		'indirizzo' => array( 'Indirizzo', 'text' ),
		'orari'     => array( 'Orari di apertura', 'text' ),
		'piva'      => array( 'Partita IVA', 'text' ),
	);
}

function cauto_menu_impostazioni() {
	add_submenu_page(
		'edit.php?post_type=auto',
		'Impostazioni concessionaria',
		'Impostazioni',
		'manage_options',
		'cauto-impostazioni',
		'cauto_pagina_impostazioni'
	);
}
add_action( 'admin_menu', 'cauto_menu_impostazioni' );

function cauto_registra_impostazioni() {
	register_setting(
		'cauto_impostazioni_gruppo',
		'cauto_impostazioni',
		array( 'sanitize_callback' => 'cauto_sanifica_impostazioni' )
	);
}
add_action( 'admin_init', 'cauto_registra_impostazioni' );

function cauto_sanifica_impostazioni( $valori ) {
	$puliti = array();
	foreach ( cauto_campi_impostazioni() as $chiave => $campo ) {
		$valore = isset( $valori[ $chiave ] ) ? $valori[ $chiave ] : '';
		$puliti[ $chiave ] = ( 'email' === $campo[1] ) ? sanitize_email( $valore ) : sanitize_text_field( $valore );
	}
	return $puliti;
}

function cauto_pagina_impostazioni() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	?>
	<div class="wrap">
		<h1>Impostazioni concessionaria</h1>
		<p>Questi dati compaiono nei pulsanti di contatto delle schede auto.</p>
		<form method="post" action="options.php">
			<?php settings_fields( 'cauto_impostazioni_gruppo' ); ?>
			<table class="form-table" role="presentation">
				<?php foreach ( cauto_campi_impostazioni() as $chiave => $campo ) : ?>
					<tr>
						<th scope="row"><label for="cauto_<?php echo esc_attr( $chiave ); ?>"><?php echo esc_html( $campo[0] ); ?></label></th>
						<td>
							<input type="<?php echo esc_attr( $campo[1] ); ?>"
								id="cauto_<?php echo esc_attr( $chiave ); ?>"
								name="cauto_impostazioni[<?php echo esc_attr( $chiave ); ?>]"
								value="<?php echo esc_attr( cauto_impostazione( $chiave ) ); ?>"
								class="regular-text">
							<?php if ( isset( $campo[2] ) ) : ?>
								<p class="description"><?php echo esc_html( $campo[2] ); ?></p>
							<?php endif; ?>
						</td>
					</tr>
				<?php endforeach; ?>
			</table>
			<?php submit_button( 'Salva' ); ?>
		</form>

		<h2>Come si usa il catalogo</h2>
		<p>Inserisci questi shortcode nelle pagine del sito:</p>
		<ul>
			<li><code>[auto_catalogo]</code> — catalogo completo con i filtri di ricerca.</li>
			<li><code>[auto_evidenza limite="3"]</code> — le auto segnate come «in evidenza», per la home.</li>
			<li><code>[auto_ricerca]</code> — solo la barra di ricerca rapida (rimanda al catalogo).</li>
		</ul>
	</div>
	<?php
}
