# Cartella marketing

Materiale per le campagne, non per il sito.

| File | A cosa serve |
|------|--------------|
| `remarketing-lead.md` | Il piano: segmenti, calendario 6 settimane, budget, tracciamento, GDPR. **Parti da qui.** |
| `messaggi-pronti.md` | Testi da copiare per WhatsApp, email, telefonate e inserzioni Meta. |
| `lista-contatti-template.csv` | Modello del foglio contatti, con una riga di esempio da cancellare. |

## Come si usa il CSV

Copialo fuori dal repository (es. su Drive) prima di riempirlo: **i contatti reali
non vanno su git**, la regola in `.gitignore` blocca i file `marketing/lista-contatti*.csv`
tranne il modello.

| Colonna | Cosa ci metti |
|---------|---------------|
| `telefono` | formato internazionale `+39...` — serve così per i pubblici Meta |
| `ultimo_lavoro` / `anno_ultimo_lavoro` | il gancio del messaggio: senza questi il testo non è personalizzabile |
| `segmento` | 1-6, secondo la tabella in `remarketing-lead.md` §3 |
| `stato` | `da_contattare` · `contattato` · `risposto` · `preventivo` · `cliente` · `perso` |
| `esito` | cosa ha detto, in due parole |
| `stop` | `si` se ha chiesto di non essere più contattato → **non lo ricontatti su nessun canale** |
