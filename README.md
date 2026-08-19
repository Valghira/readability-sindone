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
└── reports/                 # Report generati (esclusi da git)
```

Il registro degli indici in `src/core.py` separa le formule (`INDEX_REGISTRY`) dalle lingue supportate (`INDEX_LANGS`). Per aggiungere un nuovo indice è sufficiente implementare la funzione in `src/indices.py` e aggiungere una voce a ciascuno dei due dizionari, senza modificare altro codice.

---

## Requisiti

- **Python ≥ 3.10**
- Dipendenze (installate via `pip`):

| Pacchetto | Uso |
|---|---|
| `pyphen` | Sillabazione italiana tramite dizionario integrato (`it_IT`) |
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
| `lang` | `str`, `list[str]` o `"all"` | Lingua o lingue del corpus. Esempi: `"it"`, `["it","en"]`, `"all"` (tutte le lingue presenti nel corpus e supportate da almeno un indice) |
| `process_all_categories` | `bool` | Se `True`, elabora tutte le categorie ignorando i due parametri seguenti |
| `category` | `str` | Gruppo di primo livello ricavato dalla struttura del JSON |
| `sub_category` | `str` | Sottocategoria di secondo livello ricavata dalla struttura del JSON |

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
2. **Configurazione** — selezione degli indici da calcolare, della lingua e del formato di output (`CSV`, `Excel` o entrambi). La sezione Lingua mostra un checkbox per ogni lingua rilevata nel corpus e supportata da almeno un indice, costruito dinamicamente al caricamento del JSON; bottoni "Seleziona tutti" / "Deseleziona tutti" per selezione rapida. Le lingue presenti nel corpus ma non supportate da alcun indice non compaiono tra le checkbox e vengono segnalate nel log.
3. **Categorie** — scelta tra tutte le categorie disponibili nel corpus o una specifica combinazione gruppo/sottocategoria, con i valori popolati dinamicamente in base al file caricato.
4. **Esegui** — avvia l'analisi; il pannello di log in basso mostra i percorsi dei file generati al termine dell'elaborazione. Il log usa tre livelli visivi: messaggi normali nel colore predefinito del tema; **AVVISO** in arancione (situazioni da segnalare che non bloccano l'esecuzione, es. lingua rilevata nel corpus ma non supportata); **ATTENZIONE** ed **ERRORE** in rosso (problemi che impediscono o interrompono l'esecuzione).

---

## Limiti e sviluppi futuri

**Lingue supportate** — La GUI rileva dinamicamente le lingue presenti nel JSON e mostra come selezionabili solo quelle supportate da almeno un indice (criterio definito in `INDEX_LANGS` in `src/core.py`). Aggiungere una nuova lingua richiede di estendere: le formule in `src/indices.py` e `INDEX_LANGS` per la compatibilità indice-lingua, e la sillabazione in `src/utils.py`. L'infrastruttura di selezione e pipeline supporta già N lingue senza modifiche alla GUI. Le funzioni di calcolo in `src/utils.py` (`average_syllables_per_word`, `count_complex_words`) e in `src/indices.py` (`flesch_index`) gestiscono esplicitamente soltanto `"it"` e `"en"`: una lingua non riconosciuta passata direttamente a queste funzioni solleva un `ValueError` con messaggio esplicito invece di ricadere silenziosamente sul comportamento inglese. Il parametro `lang="en"` nelle firme è mantenuto per retrocompatibilità. Il flusso normale della pipeline è già protetto a monte dal guard `INDEX_LANGS` in `_collect_results`.

**Flesch italiano (Franchina-Vacca)** — La formula originale prevede il conteggio delle sillabe su un campione di 100 parole consecutive. Poiché la grande maggioranza dei testi del corpus ha meno di 100 parole, l'implementazione attuale usa la media delle sillabe per parola in luogo del campione, rappresentando un'approssimazione rispetto alla specifica originale. *(Fonte: [Wikipedia — Formula di Flesch](https://it.wikipedia.org/wiki/Formula_di_Flesch))*

**Gunning Fog** — La specifica originale esclude dal conteggio delle "parole complesse" quattro categorie: nomi propri, parole composte, verbi coniugati con ≥3 sillabe e avverbi in "-mente". L'implementazione attuale applica solo la prima esclusione, tramite un'euristica posizionale (parola maiuscola non a inizio frase). Le restanti tre richiederebbero un'analisi morfologica — distinguere una parola composta da una semplice, o un avverbio in "-mente" dalla radice corrispondente, non è possibile contando solo le sillabe o con espressioni regolari, senza ricorrere a un dizionario grammaticale o a una libreria NLP. Questa è una limitazione nota dell'implementazione attuale. *(Fonti: [Wikipedia — Indice Gunning Fog](https://it.wikipedia.org/wiki/Indice_Gunning_fog); Gunning, R., 1952, *The Technique of Clear Writing*, McGraw-Hill)*

**Sviluppi futuri** — Tra le estensioni possibili: la scelta della cartella di destinazione dei report dalla GUI (attualmente fissa a `./reports/`).
