# S-COMODO — Sistema copertine fotografiche
Ultimo aggiornamento: 22 novembre 2026 · Responsabilità editoriale S-COMODO

## Regola approvata
Ogni articolo pubblicato deve avere una propria copertina originale in formato orizzontale 16:9, senza headline, sottotitoli o altri testi incorporati nella fotografia. La card presenta, nell'ordine: fotografia, rubrica e genere editoriale, titolo autentico, introduzione breve, data.

Palette della cornice editoriale: bianco #ffffff, nero #111111, rosso #a51224. La fotografia può usare colori naturali sobri purché non introduca un'altra palette grafica. Niente poster tipografici, ripetizione del titolo, stock generico, miniature social o elementi ornamentali non giustificati.

La copertina è un contenuto **illustrativo**, non una prova. Per eventi pubblici e persone storiche non creare falsi fotogrammi documentari: una scena simulata è sempre identificata come ricostruzione IA. Alt descrive cosa si vede, la didascalia ne specifica la natura. I dati statistici restano nelle fonti e nei grafici verificati, non sono inventati dentro la fotografia.

Produzione: immagine esclusiva per storia; dimensioni target 1440×810 o 1280×720; WebP, compressione visivamente senza perdita grave; verifica 16:9, focus mobile, assenza di scritte, assenza di volti attribuiti falsamente; aggiornamento frontmatter `image`, `image_alt`, `image_caption`. Le traduzioni della stessa storia possono condividere la fotografia.

## Copertine fotografiche già integrate
- SC-PATRIMONIALE-2026 (IT, ES) — dossier eredità — fotografia di documenti e proprietà.
- SC-GENTILE-2026 — ritratto editoriale sintetico dichiarato non autentico.
- SC-REPORT-UOVA-2026 — uova e documenti per verifica.
- SC-SPAGNA-2026 — urna e istituzioni, scena simbolica.
- SC021 — memoria, album e ambiente di cura: pubblicata come fotografia IA, non paziente reale.
- SC016 — già dotato di una copertina fotografica sintetica: controllare eventuale duplicazione e coerenza alle prossime revisioni.

## Coda di produzione, priorità decrescente
| Storia / riferimento | Direzione fotografica originale | Nota |
|---|---|---|
| SC020 · Ozempic | Scrivania medica luminosa, appunti, strumenti di consultazione; nessun packaging o marchio inventato | Evitare suggerimenti clinici nell'immagine |
| SC019 · Midterm USA | Seggio e schede elettorali generiche, architettura istituzionale non identificata | Non fingere foto di eventi reali |
| SC018 · ueno bank audit (IT/ES/EN) | Documenti bancari, calcolatrice, fogli di verifica e lente, senza loghi né dati fittizi leggibili | Distinta da SC017 |
| SC017 · Crisi bancaria Paraguay (IT/ES/EN) | Architettura bancaria generica con documenti economici in primo piano | Non insinuare prove con una foto |
| SC015 · Il cervello non basta | Libro aperto, scacchiera incompleta e appunti critici, luce di studio | Nessun testo in copertina |
| SC014 · Paraguay, la storia troppo grande | Paesaggio fluviale e città, profondità di campo, fotografia evocativa | Sostituire immagine con titolo integrato |
| SC013 · Cuba, prezzo della rivoluzione | Scorcio urbano quotidiano dell'Avana reso come scena concettuale | Non presentare come luogo/data documentata |
| SC012 · Le parole prima dei fatti | Edizioni di quotidiani con testi volutamente illeggibili e matita rossa | Evitare statistiche fittizie |
| SC011 · Brasile 2026 | Seggio elettorale generico e immagine istituzionale astratta | Nessun candidato reale o verdetto suggerito |
| SC010 · Infanzia in Paraguay (IT/ES) | Strada di quartiere, giochi e luce pomeridiana, senza persone identificabili | Rappresentazione dichiarata |
| SC009 · El Chavo del 8 (ES) | Cortile di vicinato latinoamericano immaginario | Nessuna ricostruzione riconoscibile della serie |
| SC007 / SC008 · Dissenso e parole (IT/ES) | Due microfoni e sedie vuote in una sala per dibattiti | Considerare due declinazioni, non doppioni meccanici |
| SC006 · Data center Paraguay | Infrastruttura elettrica e sala server generiche, nessun logo | Distinguere fotografia concettuale e impianto reale |
| SC005 · The Lost Art of Belonging (EN) | Tavolo comune in un quartiere, tazze e sedie, luce naturale | Nessuna scritta |
| SC004 · Il Paraguay plurilingue | Quaderni e scena di mercato/società, nessun testo in lingue inventato | Evitare folklore superficiale |
| SC003 · Diritti e partiti | Documenti civici, matite, sedie di assemblea senza loghi | Neutrale e non partigiana |
| SC002 · La città dietro il compensato | Vetrina di negozio protetta da tavole, strada urbana realistica | Non attribuire a un luogo reale |
| SC001 · Democrazia e dissenso | Podio vuoto, microfoni e sala civica | Non simulare manifestazioni accadute |

## QA obbligatorio
1. Nessuna fotografia contiene il titolo dell'articolo.
2. Foto pertinente alla storia e diversa dalle altre copertine.
3. Formato 16:9, buona nitidezza su telefono e desktop.
4. Fotografia accessibile mediante testo alternativo specifico.
5. Didascalia sulle immagini generate con IA, senza attribuzioni documentarie false.
6. Nessuna modifica alle fonti o alle conclusioni dell'articolo in occasione della sostituzione.
7. Controllo della homepage, dell'archivio e del singolo articolo su desktop/mobile.
8. Il deploy GitHub Pages deve essere completato prima di dichiarare la pubblicazione.

Questo registro è operativo, non un calendario: la pubblicazione di nuovi articoli non ha cadenza obbligatoria.


## Verifica tecnica automatizzabile — aggiornamento 22 novembre 2026

Da questa revisione è disponibile `scripts/check_covers.py`, eseguibile dal checkout del repository con:

```bash
python3 scripts/check_covers.py
python3 scripts/check_covers.py --json
```

Il controllo **non inventa fotografie e non verifica visivamente il contenuto delle immagini**; segnala:
- copertina o file locale mancanti;
- testo alternativo e didascalia assenti;
- possibili copertine tipografiche con il titolo all'interno;
- SVG legacy da ricontrollare prima di assegnare lo stato «fotografica approvata».

Stato produzione successivo: è stata preparata una nuova fotografia editoriale 16:9 per **SC020 · Ozempic** (consultazione medica simbolica, nessun marchio, nessuna funzione clinica attribuibile al dispositivo). Fino al caricamento effettivo del WebP nel repository e all'aggiornamento del front matter, la copertina pubblicata resta quella precedente. Gli output non fotografici per SC017/SC018/SC013/SC015 sono stati scartati; non vanno usati come copertine.

Non modificare mai `image` puntando a una risorsa inesistente. Mantenere invariati i testi, i link, le fonti e le traduzioni durante la migrazione delle fotografie.
