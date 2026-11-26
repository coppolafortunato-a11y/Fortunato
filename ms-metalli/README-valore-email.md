# Email "Nuovo contatto MS Metalli": correzione del valore

L'email automatica che arriva per ogni nuovo contatto Meta mostrava valori assurdi,
per esempio con "Kg: 50 - 200 kg":

    Valore per noi: fino a 476.900 € se è rame 1 (9,50 €/kg, sopra 500 kg)

Lo script leggeva "50 - 200" come 50200 kg. In più usava ancora il listino di Marco del 31/10
e sceglieva il prezzo coi kg (500 kg) invece che col valore (1.500 €).

Con `avviso-email-valore.gs` la stessa email diventa:

    Valore al prezzo di Marco: fino a 1.740 € se è rame 1 (200 kg x 8,70 €/kg, listino sopra 1.500 €)
    Prezzo massimo al cliente: 7,70 €/kg (margine Fortunato 1,00 €/kg, circa 200 €)

## Come aggiornare lo script (a mano, 2 minuti)

1. Apri il foglio "MS Metalli - Contatti da Meta" > Estensioni > Apps Script > `Codice.gs`.
2. Seleziona dalla riga `// Listino di Marco Russo a noi (31/10)` fino alla `}` che chiude
   `function stimaValore` (subito prima di `function avvisa`) e cancellala.
3. Al suo posto incolla tutto il contenuto di `avviso-email-valore.gs`.
4. In `function avvisa` cambia `'Valore per noi: '` in `'Valore al prezzo di Marco: '`.
5. Salva (icona del dischetto). Non serve rifare "installa": il trigger resta quello.
6. Per provare: scegli la funzione `prova` e premi Esegui, arriva un'email con l'ultimo contatto.

Quando Marco cambia listino basta aggiornare i numeri nella tabella `LISTINO`
(prezzo fino a 1.500 €, prezzo sopra 1.500 €, margine di Fortunato).
