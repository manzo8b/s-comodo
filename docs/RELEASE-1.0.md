# S-COMODO — Validazione 1.0
Data: 25 novembre 2026. Stato: **candidato al rilascio**, non certificazione integrale.

## Baseline verificata
Commit pubblico: `dab7a79ff793d9490c244a028eda218b479ce08a`.

| Controllo | Esito |
|---|---|
| Pubblicazione Pages | PASS |
| Contratto SEO: 59 URL, 32 articoli | PASS, zero errori |
| Audit strutturale: 32 articoli | PASS, zero anomalie rilevate |
| Regressione dossier: 11 rotte × 6 viewport | PASS |
| Browser smoke: 35 pagine × 2 viewport | PASS, 70/70 |

Evidenze: [pubblicazione](https://github.com/manzo8b/s-comodo/actions/runs/45603360550), [SEO](https://github.com/manzo8b/s-comodo/actions/runs/45603360557), [browser](https://github.com/manzo8b/s-comodo/actions/runs/45603360876).

## Criteri di accettazione
- Nessun nuovo errore nei controlli SEO, struttura o browser. Pubblicazione solo per contenuti approvati.
- Rapporti axe-core e Lighthouse consultabili come artefatti CI; esaminare tutte le violazioni e i punteggi di laboratorio prima della chiusura.
- Verifica manuale di contrasto, zoom, navigazione da tastiera e screen reader; nessuna dichiarazione di conformità WCAG basata unicamente su test automatici.
- Verifica in Search Console di copertura, sitemap e URL campione; non confondere indicizzabilità con indicizzazione.
- Revisione delle copertine SVG (20 pagine al controllo precedente), compresa la copertina infografica SC012; nuove copertine fotografiche originali senza testi sovrapposti. Non modificare le infografiche documentali.
- Revisione linguistica dei testi ES/EN, incluse didascalie, etichette, fonti e note metodologiche; non attribuire automaticamente lo stesso significato a due articoli diversi.
- Controllo editoriale delle affermazioni, fonti primarie, diritto di replica e data di aggiornamento: distinto dal collaudo tecnico.

## Gestione ordinaria
Ogni nuovo articolo: approvazione editoriale, immagine/ALT/didascalia, descrizione, rubrica, lingua, ID stabile, fonti, trasparenza IA. Consultare i rapporti CI dopo ogni pubblicazione; non modificare globalmente il design per correggere un singolo dossier. Conservare gli originali e usare commit reversibili.
