<?php
/**
 * Modulo "richiedi informazioni" presente in ogni scheda auto.
 * Il messaggio arriva per e-mail all'indirizzo indicato nelle impostazioni.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function cauto_form_richiesta( $post_id ) {
	$inviato = isset( $_GET['richiesta'] ) ? sanitize_key( wp_unslash( $_GET['richiesta'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Recommended

	ob_start();

	if ( 'ok' === $inviato ) {
		echo '<p class="form-msg form-msg--ok">Richiesta inviata. Ti rispondiamo al più presto.</p>';
	} elseif ( 'ko' === $inviato ) {
		echo '<p class="form-msg form-msg--ko">Non siamo riusciti a inviare la richiesta. Riprova o scrivici su WhatsApp.</p>';
	}
	?>
	<form class="contact-form" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
		<input type="hidden" name="action" value="cauto_richiesta">
		<input type="hidden" name="auto_id" value="<?php echo esc_attr( $post_id ); ?>">
		<?php wp_nonce_field( 'cauto_richiesta', 'cauto_richiesta_nonce' ); ?>

		<p class="hp">
			<label for="cauto-sito">Non compilare questo campo</label>
			<input type="text" id="cauto-sito" name="sito" tabindex="-1" autocomplete="off">
		</p>

		<strong>Richiedi informazioni</strong>
		<label class="sr-only" for="cauto-nome">Nome</label>
		<input type="text" id="cauto-nome" name="nome" placeholder="Nome e cognome" required>

		<label class="sr-only" for="cauto-telefono">Telefono</label>
		<input type="tel" id="cauto-telefono" name="telefono" placeholder="Telefono" required>

		<label class="sr-only" for="cauto-email">E-mail</label>
		<input type="email" id="cauto-email" name="email" placeholder="E-mail (facoltativa)">

		<label class="sr-only" for="cauto-messaggio">Messaggio</label>
		<textarea id="cauto-messaggio" name="messaggio" placeholder="Vorrei sapere se è ancora disponibile e se è possibile una prova su strada."></textarea>

		<label class="privacy">
			<input type="checkbox" name="privacy" value="1" required>
			<span>Ho letto l'informativa e acconsento al trattamento dei dati per essere ricontattato.</span>
		</label>

		<button type="submit" class="btn btn--primary btn--block">Invia la richiesta</button>
	</form>
	<?php
	return ob_get_clean();
}

function cauto_gestisci_richiesta() {
	$auto_id  = isset( $_POST['auto_id'] ) ? absint( $_POST['auto_id'] ) : 0;
	$ritorno  = $auto_id ? get_permalink( $auto_id ) : home_url( '/' );
	$fallisci = static function () use ( $ritorno ) {
		wp_safe_redirect( add_query_arg( 'richiesta', 'ko', $ritorno ) . '#cauto-nome' );
		exit;
	};

	if ( ! isset( $_POST['cauto_richiesta_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['cauto_richiesta_nonce'] ), 'cauto_richiesta' ) ) {
		$fallisci();
	}

	// Campo trappola: lo compilano solo i robot che inviano spam.
	if ( ! empty( $_POST['sito'] ) ) {
		wp_safe_redirect( add_query_arg( 'richiesta', 'ok', $ritorno ) );
		exit;
	}

	$nome      = isset( $_POST['nome'] ) ? sanitize_text_field( wp_unslash( $_POST['nome'] ) ) : '';
	$telefono  = isset( $_POST['telefono'] ) ? sanitize_text_field( wp_unslash( $_POST['telefono'] ) ) : '';
	$email     = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
	$messaggio = isset( $_POST['messaggio'] ) ? sanitize_textarea_field( wp_unslash( $_POST['messaggio'] ) ) : '';

	if ( ! $nome || ! $telefono || empty( $_POST['privacy'] ) ) {
		$fallisci();
	}

	$destinatario = cauto_impostazione( 'email', get_option( 'admin_email' ) );
	$titolo_auto  = $auto_id ? get_the_title( $auto_id ) : 'Richiesta generica';

	$corpo = array( 'Nuova richiesta dal sito.', '', 'Auto: ' . $titolo_auto );
	if ( $auto_id ) {
		$corpo[] = 'Scheda: ' . get_permalink( $auto_id );
	}
	$corpo[] = '';
	$corpo[] = 'Nome: ' . $nome;
	$corpo[] = 'Telefono: ' . $telefono;
	$corpo[] = 'E-mail: ' . ( $email ? $email : '—' );
	$corpo[] = '';
	$corpo[] = 'Messaggio:';
	$corpo[] = $messaggio ? $messaggio : '—';

	$intestazioni = array( 'Content-Type: text/plain; charset=UTF-8' );
	if ( $email ) {
		$intestazioni[] = 'Reply-To: ' . $nome . ' <' . $email . '>';
	}

	$ok = wp_mail(
		$destinatario,
		'Richiesta auto: ' . $titolo_auto,
		implode( "\n", $corpo ),
		$intestazioni
	);

	wp_safe_redirect( add_query_arg( 'richiesta', $ok ? 'ok' : 'ko', $ritorno ) );
	exit;
}
add_action( 'admin_post_cauto_richiesta', 'cauto_gestisci_richiesta' );
add_action( 'admin_post_nopriv_cauto_richiesta', 'cauto_gestisci_richiesta' );
