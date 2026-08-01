<?php
/**
 * Plugin Name: Idea Marketing — Extras
 * Description: Barra contatti in alto (telefono ed email cliccabili) e bottone WhatsApp fisso. Indipendente dal tema.
 * Author:      Idea Marketing di Coppola Fortunato
 * Version:     1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Dati aziendali — modifica solo qui.
 */
function ideamkt_data() {
	return array(
		'tel_display' => '320 611 6711',
		'tel_link'    => '+393206116711',
		'whatsapp'    => '393206116711',
		'email'       => 'coppola.fortunato@gmail.com',
		'citta'       => 'Reggio Calabria',
		'wa_msg'      => 'Ciao Idea Marketing, vorrei informazioni su',
	);
}

/**
 * Stili.
 */
add_action( 'wp_head', 'ideamkt_extras_css', 99 );
function ideamkt_extras_css() {
	?>
<style id="ideamkt-extras">
:root{
	--ik-navy:#1E2235;
	--ik-gold:#C9A961;
	--ik-paper:#f8f7f4;
	--ik-footer:#0f1d3f;
	--ik-rule:#e0ddd6;
}

/* ---- Barra contatti ---- */
.ik-topbar{
	background:var(--ik-navy);
	color:#fff;
	font-size:14px;
	line-height:1;
	letter-spacing:.02em;
}
.ik-topbar__inner{
	max-width:1200px;
	margin:0 auto;
	padding:10px 24px;
	display:flex;
	align-items:center;
	justify-content:space-between;
	gap:16px;
	flex-wrap:wrap;
}
.ik-topbar__left{
	display:flex;
	align-items:center;
	gap:24px;
	flex-wrap:wrap;
}
.ik-topbar a{
	color:#fff;
	text-decoration:none;
	display:inline-flex;
	align-items:center;
	gap:8px;
	transition:color .2s ease;
}
.ik-topbar a:hover,
.ik-topbar a:focus-visible{ color:var(--ik-gold); }
.ik-topbar a:focus-visible{ outline:2px solid var(--ik-gold); outline-offset:3px; }
.ik-topbar svg{ width:15px; height:15px; flex:none; fill:var(--ik-gold); }
.ik-topbar__tel{ font-weight:600; }
.ik-topbar__place{ opacity:.6; font-size:13px; }

@media (max-width:780px){
	.ik-topbar__inner{ justify-content:center; padding:9px 16px; gap:18px; }
	.ik-topbar__email,
	.ik-topbar__place{ display:none; }
}

/* ---- Bottone WhatsApp ---- */
.ik-wa{
	position:fixed;
	right:24px;
	bottom:24px;
	z-index:9999;
	width:58px;
	height:58px;
	border-radius:50%;
	background:#25D366;
	display:flex;
	align-items:center;
	justify-content:center;
	box-shadow:0 6px 22px rgba(0,0,0,.22);
	transition:transform .2s ease, box-shadow .2s ease;
}
.ik-wa:hover,
.ik-wa:focus-visible{
	transform:translateY(-3px);
	box-shadow:0 10px 28px rgba(0,0,0,.28);
}
.ik-wa:focus-visible{ outline:3px solid var(--ik-gold); outline-offset:3px; }
.ik-wa svg{ width:31px; height:31px; fill:#fff; }

@media (max-width:780px){
	.ik-wa{ right:16px; bottom:16px; width:52px; height:52px; }
	.ik-wa svg{ width:28px; height:28px; }
}

@media (prefers-reduced-motion:reduce){
	.ik-topbar a,
	.ik-wa{ transition:none; }
	.ik-wa:hover{ transform:none; }
}
</style>
	<?php
}

/**
 * Barra contatti in cima alla pagina.
 */
add_action( 'wp_body_open', 'ideamkt_topbar', 1 );
function ideamkt_topbar() {
	$d = ideamkt_data();
	?>
<div class="ik-topbar">
	<div class="ik-topbar__inner">
		<div class="ik-topbar__left">
			<a class="ik-topbar__tel" href="tel:<?php echo esc_attr( $d['tel_link'] ); ?>">
				<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.7 21 3 13.3 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2z"/></svg>
				<?php echo esc_html( $d['tel_display'] ); ?>
			</a>
			<a class="ik-topbar__email" href="mailto:<?php echo esc_attr( $d['email'] ); ?>">
				<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.2-8 5-8-5V6l8 5 8-5v2.2z"/></svg>
				<?php echo esc_html( $d['email'] ); ?>
			</a>
		</div>
		<span class="ik-topbar__place"><?php echo esc_html( $d['citta'] ); ?> — Via Campoli 34</span>
	</div>
</div>
	<?php
}

/**
 * Bottone WhatsApp fisso.
 */
add_action( 'wp_footer', 'ideamkt_whatsapp' );
function ideamkt_whatsapp() {
	$d   = ideamkt_data();
	$url = 'https://wa.me/' . $d['whatsapp'] . '?text=' . rawurlencode( $d['wa_msg'] . ' ' );
	?>
<a class="ik-wa" href="<?php echo esc_url( $url ); ?>" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">
	<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.7 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5 0-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.3 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.2-.6-.4zM12 2.1c5.5 0 9.9 4.4 9.9 9.9 0 5.5-4.4 9.9-9.9 9.9-1.7 0-3.4-.5-4.9-1.3L2.1 22l1.5-4.8A9.8 9.8 0 0 1 2.1 12c0-5.5 4.4-9.9 9.9-9.9z"/></svg>
</a>
	<?php
}
