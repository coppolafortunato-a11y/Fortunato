# Testo da incollare in Claude in Chrome

Da usare nell'estensione **Claude in Chrome**, sul computer che naviga da una
connessione domestica. Serve a leggere la disponibilità senza prenotare nulla.

---

## Controllo dei 5 centri

> Ho aperto 5 schede con i siti dei centri "Паспортний сервіс ДП Документ".
> Per ciascuna scheda, uno alla volta:
>
> 1. Nel campo **"Послуга"** seleziona esattamente:
>    «Закордонний паспорт та (або) ID-картка»
> 2. Aspetta 3-5 secondi: il sito ricarica la disponibilità via JavaScript.
> 3. Guarda il campo **"Обрати день"**.
>    - Se compare «Вибачте, на даний момент всі місця зайняті!» → il centro è PIENO.
>    - Se compaiono delle date → selezionale una per una e leggi anche il campo
>      **"Обрати час"**, annotando tutti gli orari e, se indicato, il numero di posti.
>
> **Non fare nient'altro:** non prenotare, non inserire numeri di telefono o dati
> personali, non cliccare «Продовжити», non avviare Diia.Signature né BankID.
> Devi soltanto leggere.
>
> Alla fine dammi una tabella con: centro, stato (PIENO / DISPONIBILE), date,
> orari. Segnalami in particolare qualsiasi data **prima del 15/10/2026**.

## Se serve capire com'è fatto il form

Utile se il controllo automatico sbaglia a leggere la pagina.

> Nella scheda aperta, dimmi con precisione com'è costruito il form della coda
> elettronica: i campi "Послуга", "Обрати день" e "Обрати час" sono `<select>`
> HTML normali oppure menu a tendina personalizzati? Riportami il testo esatto
> di tutte le opzioni del campo "Послуга", copiato alla lettera.

---

## I 5 indirizzi

| Centro | Indirizzo |
|---|---|
| Cracovia | https://krakow.pasport.org.ua/solutions/e-queue |
| Varsavia | https://warszawa.pasport.org.ua/solutions/e-queue |
| Wrocław | https://wroclaw.pasport.org.ua/solutions/e-queue |
| Danzica | https://gdansk.pasport.org.ua/solutions/e-queue |
| Milano/Rozzano | https://milan.pasport.org.ua/solutions/e-queue |

## Situazione nota al 22/09/2026

| Centro | Stato |
|---|---|
| Cracovia, Varsavia, Wrocław | nessuna disponibilità |
| Danzica | 22/10/2026, più orari |
| Milano/Rozzano | 15/10/2026 come primo posto libero |

Una data diversa da queste è una **novità**.
