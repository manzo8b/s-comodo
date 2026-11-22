# S-COMODO · Identità editoriale e visiva

**Approvazione editore: 22 novembre 2026.**

## Regole visive
- Palette **solo bianco** (#fff), **nero** (#111) e **rosso** (#a51224). I grigi sono riservati a linee e testi secondari, mai a fondi crema o blu.
- Testata tipografica S-COMODO e impaginazione da giornale contemporaneo.
- Gerarchia: un’apertura editoriale, tre articoli, approfondimenti, cinque rubriche.
- Titoli serif ampi, corpo di testo leggibile, bordi netti. Mai contenuti fittizi o numeri di uscita/periodicità inventati.
- Le fotografie sono facoltative, devono provenire da asset approvati e non simulare prove.
- Desktop: indice articoli a destra, fondo nero, testo bianco, accento rosso. Mobile: indice compatto richiudibile prima del contenuto.

## Regole editoriali
- Rubrica = argomento tramite `topic_id` e `rubrica`.
- `formato` = `dossier` (Verifica), `saggio` (Opinione), `contesto` (Analisi).
- Non classificare i vecchi articoli senza revisione; `format` legacy resta invariato.
- Le fonti originali e numerate restano alla fine di ogni articolo, seguite dai blocchi di trasparenza e rettifica.
- I filtri pubblici usano `editorial_status: pubblicato` e `lang` per evitare bozze e mescolanze linguistiche.
- Non imporre cronologie, precedenti storici o calendario settimanale.

## QA
Viewport minimi: 375, 390, 768, 1180 e 1536 px; no overflow orizzontale, indice mai sovrapposto al testo, contrasto alto, link di lingua e fonti funzionanti. Qualunque modifica futura deve passare test desktop e mobile prima del deploy.
