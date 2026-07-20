# Analisi di Leggibilità — Museo della Sindone

Strumento per il calcolo automatico degli indici di leggibilità (Gulpease, Flesch Reading Ease, Gunning Fog) su testi del Museo della Sindone di Torino. Legge un corpus JSON strutturato per lingua e categoria, e produce report in formato CSV ed Excel con evidenziazione in base ai punteggi.

---

## Architettura

```
readability-sindone/
├── main.py                  # Entry point CLI: configura e avvia la generazione dei report
├── gui.py                   # Interfaccia grafica (CustomTkinter)
├── src/
│   ├── core.py              # INDEX_REGISTRY, caricamento dati, generate_csv/excel_report
│   ├── indices.py           # Formule: gulpease_index, flesch_index, gunning_fog_index
│   └── utils.py             # Metriche di testo: parole, frasi, lettere, sillabe
├── file_to_process/
│   └── content.json         # Corpus: lang → age_group → categoria → opere → frasi
├── dictionaries/
│   └── hyph_it_IT.dic       # Dizionario LibreOffice per la sillabazione italiana
└── reports/                 # Report generati (esclusi da git)
```

Il registro degli indici in `src/core.py` separa le formule (`INDEX_REGISTRY`) dalle lingue supportate (`INDEX_LANGS`). Per aggiungere un nuovo indice è sufficiente implementare la funzione in `src/indices.py` e aggiungere una voce a ciascuno dei due dizionari, senza modificare altro codice.

---

## Requisiti

- **Python ≥ 3.10**
- Dipendenze (installate via `pip`):

| Pacchetto | Uso |
|---|---|
| `pyphen` | Sillabazione italiana tramite dizionario LibreOffice |
| `cmudict` | Sillabazione inglese tramite CMU Pronouncing Dictionary |
| `textstat` | Utilità di supporto per metriche testuali |
| `pandas` | Manipolazione dati tabellari |
| `openpyxl` | Generazione report Excel con formattazione |
| `customtkinter` | Interfaccia grafica (necessaria solo per la GUI) |

---

## Installazione

```bash
# Creare e attivare un ambiente virtuale
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Installare le dipendenze
pip install -r requirements.txt
```

---

## Utilizzo

### Modalità CLI

Aprire `main.py` e modificare le chiamate nella sezione finale in base all'analisi desiderata, poi eseguire:

```bash
python main.py
```

I parametri disponibili per `generate_csv_report` e `generate_excel_report` sono:

| Parametro | Tipo | Descrizione |
|---|---|---|
| `indices_to_use` | `list` o `"all"` | Indici da calcolare (`"gulpease"`, `"flesch"`, `"gunning_fog"`) |
| `lang` | `str` o `"all"` | Lingua del corpus (`"it"`, `"en"`, o `"all"`) |
| `process_all_categories` | `bool` | Se `True`, elabora tutte le categorie ignorando i due parametri seguenti |
| `category` | `str` | Gruppo di età (`"adult"`, `"children"`) |
| `sub_category` | `str` | Sottocategoria (es. `"typical"`, `"blind"`, `"deaf"`) |

I report vengono salvati in `./reports/` con nome nel formato:

```
report_{indici}_{lang}_{categoria}_{timestamp}.csv
report_{indici}_{lang}_{categoria}_{timestamp}.xlsx
```

**Esempio:** calcolare tutti gli indici sui testi italiani per adulti tipici:

```python
generate_csv_report(data, indices_to_use="all", lang="it",
                    process_all_categories=False,
                    category="adult", sub_category="typical")
generate_excel_report(data, indices_to_use="all", lang="it",
                      process_all_categories=False,
                      category="adult", sub_category="typical")
```

---

### Modalità GUI

```bash
python gui.py
```

L'interfaccia è organizzata in quattro pannelli:

1. **File JSON** — percorso del corpus da analizzare (precaricato con il file predefinito); il pulsante *Sfoglia* permette di selezionare un file diverso.
2. **Configurazione** — selezione degli indici da calcolare, della lingua (`Tutte`, `Italiano`, `Inglese`) e del formato di output (`CSV`, `Excel` o entrambi).
3. **Categorie** — scelta tra tutte le categorie disponibili nel corpus o una specifica combinazione gruppo/sottocategoria, con i valori popolati dinamicamente in base al file caricato.
4. **Esegui** — avvia l'analisi; il pannello di log in basso mostra i percorsi dei file generati al termine dell'elaborazione.
