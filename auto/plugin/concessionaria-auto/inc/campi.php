<?php
/**
 * Pannello "Dati del veicolo" e galleria foto nella schermata di inserimento auto.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cauto_meta_box() {
	add_meta_box( 'cauto-dati', 'Dati del veicolo', 'cauto_meta_box_html', 'auto', 'normal', 'high' );
	add_meta_box( 'cauto-galleria', 'Galleria foto', 'cauto_galleria_html', 'auto', 'side', 'low' );
}
add_action( 'add_meta_boxes', 'cauto_meta_box' );

function cauto_meta_box_html( $post ) {
	wp_nonce_field( 'cauto_salva_' . $post->ID, 'cauto_nonce' );
	$campi = cauto_campi();
	echo '<div class="cauto-campi">';

	foreach ( $campi as $chiave => $campo ) {
		$valore = cauto_campo( $post->ID, $chiave );
		$id     = 'cauto_' . $chiave;
		$name   = 'cauto[' . $chiave . ']';
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
				$opzioni = cauto_opzioni( $campo['options'] );
				echo '<select id="' . esc_attr( $id ) . '" name="' . esc_attr( $name ) . '">';
				echo '<option value="">— seleziona —</option>';
				foreach ( $opzioni as $ov => $ol ) {
					$ov = is_int( $ov ) ? $ol : $ov;
					printf( '<option value="%s" %s>%s</option>', esc_attr( $ov ), selected( $valore, $ov, false ), esc_html( $ol ) );
				}
				echo '</select>';
			} elseif ( 'textarea' === $campo['type'] ) {
				printf(
					'<textarea id="%s" name="%s" rows="5">%s</textarea>',
					esc_attr( $id ),
					esc_attr( $name ),
					esc_textarea( $valore )
				);
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
	echo '<p class="cauto-nota">Il titolo in alto è il nome dell\'auto come appare nel sito, es. <em>Fiat Panda 1.2 Easy</em>. La descrizione libera si scrive nel riquadro del contenuto.</p>';
}

/**
 * Galleria: salviamo gli ID degli allegati scelti con la libreria media di WordPress.
 */
function cauto_galleria_html( $post ) {
	$ids = array_filter( array_map( 'intval', explode( ',', (string) cauto_campo( $post->ID, 'galleria', '' ) ) ) );
	?>
	<div class="cauto-galleria" data-cauto-galleria>
		<input type="hidden" name="cauto[galleria]" value="<?php echo esc_attr( implode( ',', $ids ) ); ?>" data-cauto-galleria-input>
		<ul class="cauto-galleria__lista" data-cauto-galleria-lista>
			<?php foreach ( $ids as $id ) : ?>
				<li data-id="<?php echo esc_attr( $id ); ?>">
					<?php echo wp_kses_post( wp_get_attachment_image( $id, 'thumbnail' ) ); ?>
					<button type="button" class="cauto-galleria__rimuovi" data-cauto-galleria-rimuovi aria-label="Togli questa foto">&times;</button>
				</li>
			<?php endforeach; ?>
		</ul>
		<button type="button" class="button button-primary" data-cauto-galleria-aggiungi>Aggiungi foto</button>
		<p class="cauto-help">La prima foto della scheda è l'<strong>immagine in evidenza</strong>; qui si aggiungono le altre.</p>
	</div>
	<?php
}

/**
 * Salvataggio: controlli di sicurezza, poi ogni campo nel suo formato.
 */
function cauto_salva( $post_id ) {
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! isset( $_POST['cauto_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['cauto_nonce'] ), 'cauto_salva_' . $post_id ) ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	$inviati = isset( $_POST['cauto'] ) && is_array( $_POST['cauto'] ) ? wp_unslash( $_POST['cauto'] ) : array();
	$campi   = cauto_campi();

	foreach ( $campi as $chiave => $campo ) {
		$valore = isset( $inviati[ $chiave ] ) ? $inviati[ $chiave ] : '';

		switch ( $campo['type'] ) {
			case 'checkbox':
				$valore = $valore ? '1' : '';
				break;
			case 'number':
				$valore = ( '' === $valore ) ? '' : (string) absint( $valore );
				break;
			case 'select':
				$ammessi = cauto_opzioni( $campo['options'] );
				$chiavi  = array_keys( $ammessi );
				$ammessi = is_int( reset( $chiavi ) ) ? array_values( $ammessi ) : $chiavi;
				$valore  = in_array( $valore, $ammessi, true ) ? $valore : '';
				break;
			case 'textarea':
				$valore = sanitize_textarea_field( $valore );
				break;
			case 'month':
				$valore = preg_match( '/^\d{4}-\d{2}$/', $valore ) ? $valore : '';
				break;
			default:
				$valore = sanitize_text_field( $valore );
		}

		if ( '' === $valore ) {
			delete_post_meta( $post_id, '_auto_' . $chiave );
		} else {
			update_post_meta( $post_id, '_auto_' . $chiave, $valore );
		}
	}

	$galleria = isset( $inviati['galleria'] ) ? $inviati['galleria'] : '';
	$ids      = array_filter( array_map( 'absint', explode( ',', (string) $galleria ) ) );
	if ( $ids ) {
		update_post_meta( $post_id, '_auto_galleria', implode( ',', $ids ) );
	} else {
		delete_post_meta( $post_id, '_auto_galleria' );
	}
}
add_action( 'save_post_auto', 'cauto_salva' );

/**
 * Stili e script solo nella schermata di inserimento auto.
 */
function cauto_admin_assets( $hook ) {
	$schermata = get_current_screen();
	if ( ! $schermata || ! in_array( $schermata->post_type, array( 'auto', 'noleggio' ), true ) || ! in_array( $hook, array( 'post.php', 'post-new.php' ), true ) ) {
		return;
	}

	wp_enqueue_media();
	wp_enqueue_style( 'cauto-admin', CAUTO_URL . 'assets/admin.css', array(), CAUTO_VERSION );
	wp_enqueue_script( 'cauto-admin', CAUTO_URL . 'assets/admin.js', array( 'jquery' ), CAUTO_VERSION, true );
}
add_action( 'admin_enqueue_scripts', 'cauto_admin_assets' );
