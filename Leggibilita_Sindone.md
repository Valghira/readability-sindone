# Analisi della leggibilità dei testi del Museo della Sindone

## 1. Obiettivo del progetto
L'obiettivo di questo lavoro è sviluppare un sistema di analisi della leggibilità dei testi utilizzati all'interno del Museo della Sindone.  
Lo scopo è misurare in modo oggettivo la facilità di lettura dei testi sia per adulti che per bambini, calcolando indici di leggibilità come il Gulpease.

Questo permette di confrontare i testi originali con eventuali versioni adattate o semplificate, fornendo supporto scientifico nella valutazione dell'efficacia comunicativa dei testi destinati ai visitatori del museo.

## 2. Introduzione agli indici di leggibilità
Gli indici di leggibilità sono strumenti quantitativi che permettono di valutare quanto un testo sia facile o difficile da leggere.  
Essi si basano tipicamente su parametri come:
- lunghezza media delle parole
- lunghezza media delle frasi
- numero di sillabe

Tra gli indici più diffusi troviamo:
- **Flesch Reading Ease**: originariamente sviluppato per l'inglese, valuta la leggibilità sulla base di parole, frasi e sillabe.
- **Gunning Fog Index**: calcola il livello di istruzione necessario per comprendere un testo.
- **Indice Gulpease**: sviluppato specificamente per la lingua italiana, tiene conto del numero di lettere, parole e frasi.

Fonti:
- [Wikipedia - Indice di leggibilità](https://it.wikipedia.org/wiki/Indice_di_leggibilit%C3%A0)
- [Wikipedia - Formula di Flesch](https://it.wikipedia.org/wiki/Formula_di_Flesch)

## 3. L'indice Gulpease
L'indice Gulpease è stato sviluppato dall'Università di Roma "La Sapienza" ed è ottimizzato per la lingua italiana.  
Si calcola con la formula:

\[ G = 89 + \frac{300 \cdot Frasi - 10 \cdot Lettere}{Parole} \]

Dove:
- **Frasi** = numero di frasi nel testo (identificate tramite punteggiatura: ., !, ?)
- **Lettere** = numero di caratteri alfabetici
- **Parole** = numero di parole

Interpretazione dei valori:
- 0–40: testo difficile
- 40–60: testo medio
- 60–80: testo facile
- 80–100: testo molto facile

Fonti:
- [Wikipedia - Indice Gulpease](https://it.wikipedia.org/wiki/Indice_Gulpease)

## 4. L'indice Flesch

L'indice Flesch (o Flesch Reading Ease) è uno degli indici di leggibilità più diffusi al mondo. È stato originariamente sviluppato da Rudolf Flesch nel 1948 per la lingua inglese e successivamente adattato ad altre lingue, tra cui l'italiano.

A differenza dell'indice Gulpease — che usa lettere, parole e frasi — il Flesch si basa sul numero medio di **sillabe per parola** e sul numero medio di **parole per frase**.

### Formula per l'inglese

\[ F_{en} = 206.835 - 1.015 \cdot \frac{Parole}{Frasi} - 84.6 \cdot \frac{Sillabe}{Parole} \]

### Formula adattata per l'italiano

La versione italiana utilizza coefficienti diversi, poiché le parole italiane tendono ad avere più sillabe delle inglesi:

\[ F_{it} = 206 - 0.65 \cdot \frac{Sillabe}{Parole} - \frac{Parole}{Frasi} \]

> **Nota:** questa è la formulazione del 1972 di Vacca e Franchina, indicata su Wikipedia come la più attendibile per l'italiano in base agli studi del Gruppo Linguistico-Pedagogico Universitario. Esiste anche una revisione del 1986 (\( F_{it} = 217 - 1.3 \cdot \frac{Sillabe}{Parole} - 0.6 \cdot \frac{Parole}{Frasi} \)), non utilizzata in questo progetto. Entrambe le formule sono state riverificate a giugno 2026 contro la fonte ([Wikipedia - Formula di Flesch](https://it.wikipedia.org/wiki/Formula_di_Flesch)) e corrispondono esattamente all'implementazione in `src/indices.py`.

### Interpretazione dei valori

| Punteggio | Livello di leggibilità |
|-----------|----------------------|
| 90–100 | Molto facile |
| 70–90 | Facile |
| 50–70 | Abbastanza difficile |
| 30–50 | Difficile |
| 0–30 | Molto difficile |

### Conteggio delle sillabe

Per il conteggio delle sillabe vengono usati due approcci distinti in base alla lingua:

- **Italiano**: si utilizza il dizionario di sillabazione **LibreOffice** (`hyph_it_IT.dic`) tramite la libreria `pyphen`. Se il dizionario personalizzato è presente nella cartella `dictionaries/`, viene usato quello; altrimenti si utilizza il dizionario predefinito di pyphen per l'italiano.
- **Inglese**: si utilizza il **CMUdict** (Carnegie Mellon University Pronouncing Dictionary), che fornisce le trascrizioni fonetiche delle parole e permette di contare le sillabe contando i fonemi vocalici. Per le parole non presenti nel dizionario è previsto un fallback basato sul conteggio dei gruppi vocalici.

Fonti:
- [Wikipedia - Formula di Flesch](https://it.wikipedia.org/wiki/Formula_di_Flesch)
- [Wikipedia - Flesch–Kincaid readability tests](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)

---

## 5. Evoluzione degli script

### 5.1 Prima versione: testo come stringa diretta (versione originale)

In questa prima versione, il testo viene passato direttamente come stringa e si utilizzano funzioni base per calcolare l'indice Gulpease e i conteggi di parole, frasi e lettere.

```python
from utils import gulpease_index, word_count, sentence_count, letter_count

# Testo passato direttamente come stringa
text = "La statua è stata realizzata nel 1998 dallo scultore Luigi Mattei."
score = gulpease_index(text)

print(f"Testo: {text}")
print(f"Gulpease: {score:.2f}")
print(f"Parole: {word_count(text)} | Frasi: {sentence_count(text)} | Lettere: {letter_count(text)}")
```

**Spiegazione delle funzioni di utils (versione originale):**
- `word_count(text)` → conta il numero di parole nel testo.
- `sentence_count(text)` → conta il numero di frasi basandosi su ., !, ?; se il testo non ha punteggiatura ma contiene parole, conta almeno 1 frase.
- `letter_count(text)` → conta il numero di lettere alfabetiche.
- `gulpease_index(text)` → calcola l'indice Gulpease usando le funzioni precedenti.

---

### 5.2 Versione intermedia con lettura da JSON (versione originale)

In questa versione si introduce la lettura da un file JSON e l'estrazione ricorsiva delle frasi, mantenendo l'uso della funzione `sentence_count` originale.

```python
import json
from utils import extract_sentences, gulpease_index, word_count, refined_sentence_count, letter_count

# Caricamento del file JSON
with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Estrazione ricorsiva delle frasi dal JSON
sentences = extract_sentences(data["it"]["adult"]["typical"])

# Elaborazione di ciascuna frase
for idx, sentence in enumerate(sentences, start=1):
    score = gulpease_index(sentence)
    print(f"Sentence {idx}: {sentence}")
    print(f"Gulpease: {score:.2f} | Words: {word_count(sentence)} | Sentences: {sentence_count(sentence)} | Letters: {letter_count(sentence)}")
    print("-" * 50)
```

**Nota:** Qui viene mostrato l'uso della funzione `sentence_count` originale per il conteggio delle frasi.

---

### 5.3 Problemi riscontrati con il conteggio delle frasi e introduzione della funzione `refined_sentence_count`

Il conteggio delle frasi è un aspetto cruciale per il calcolo dell'indice Gulpease, tuttavia risulta spesso non banale a causa di alcune difficoltà intrinseche nel testo.

**Problemi con la funzione `sentence_count` originale:**
- Conta le frasi semplicemente individuando i caratteri di punteggiatura terminale come `.`, `!`, `?`.
- Questo approccio può essere inaccurato in presenza di abbreviazioni, numeri decimali, o frasi che contengono punti interni (es. "Dr.", "p.es.", "3.14").
- Inoltre, testi senza punteggiatura vengono comunque conteggiati come almeno una frase, il che può non riflettere la reale struttura del testo.

**Soluzione con la nuova funzione `refined_sentence_count`:**
- Implementa una logica più sofisticata per distinguere tra punti che terminano effettivamente una frase e quelli che fanno parte di abbreviazioni o numeri.
- Utilizza espressioni regolari avanzate o librerie di NLP per migliorare la segmentazione.
- Garantisce un conteggio più affidabile e aderente alla realtà del testo, migliorando così la precisione del calcolo dell'indice Gulpease.

---

### 5.4 Nuova versione aggiornata con `refined_sentence_count` e report CSV (versione evoluta)

Questa versione utilizza la nuova funzione `refined_sentence_count` per un conteggio più accurato delle frasi e introduce la generazione di un report in formato CSV con colonne sia per i valori grezzi che per quelli normalizzati dell'indice Gulpease.

```python
import csv
from utils import extract_sentences, gulpease_index, word_count, refined_sentence_count, letter_count

def generate_report(data, output_file):
    sentences = extract_sentences(data)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Sentence', 'Gulpease_raw', 'Gulpease_normalized']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sentence in sentences:
            raw_score = gulpease_index(sentence)
            # Normalizzazione esempio: scala 0-100 divisa per 100 (esempio ipotetico)
            normalized_score = round(raw_score / 100, 2)
            writer.writerow({
                'Sentence': sentence,
                'Gulpease_raw': round(raw_score, 2),
                'Gulpease_normalized': normalized_score
            })
```

**Caratteristiche principali della nuova implementazione:**

- **Funzione di generazione report:**  
  Elabora i testi, calcola gli indici di leggibilità con la funzione `gulpease_index` e compila un report tabellare esportato in CSV.

- **Colonne aggiunte:**  
  Oltre alla colonna con il valore grezzo dell'indice Gulpease, è stata aggiunta una colonna con il valore normalizzato, che consente un confronto più immediato e standardizzato tra testi di diversa lunghezza o complessità.

- **Arrotondamento:**  
  I valori degli indici sono arrotondati a due cifre decimali per migliorare la leggibilità e la presentazione dei dati.

- **Uso della funzione `refined_sentence_count`:**  
  Per il conteggio delle frasi si utilizza la funzione avanzata `refined_sentence_count`, che migliora la precisione della segmentazione rispetto alla funzione precedente `sentence_count`.

- **Formato CSV:**  
  L'output è esportato in un file CSV, facilitando l'analisi successiva con strumenti di data analysis o fogli di calcolo.

---

### 5.5 Commenti generali sulle versioni e l'evoluzione

- Le funzioni sono modulari e facilmente estendibili.
- La logica attuale considera una frase come sequenza terminata da `.`, `!`, `?`, ma la funzione `sentence_count` migliora questa definizione con regole più accurate (gestione abbreviazioni, ellissi, punteggiatura multipla).
- Il sistema può essere facilmente adattato per limitare il numero di frasi analizzate, utile in vista di una futura interfaccia GUI.
- La conservazione delle versioni precedenti nel documento permette di tracciare l'evoluzione metodologica e di giustificare le scelte tecniche nel lavoro di tesi.

---

### 5.6 Versione attuale: architettura multi-indice e multi-lingua

Questa è la versione corrente del sistema. Introduce il supporto a più indici di leggibilità e più lingue all'interno di un'unica funzione di generazione report, eliminando la dipendenza da una singola formula fissa.

#### Architettura: registro degli indici

Il cuore della nuova architettura è un **registro degli indici** (`INDEX_REGISTRY`) che mappa il nome di ogni indice alla funzione che lo calcola. Affiancato da un dizionario delle **lingue supportate** (`INDEX_LANGS`), permette di sapere quali indici applicare a quale lingua senza logica condizionale sparsa nel codice.

```python
# Maps index name → callable(text, lang) → score
INDEX_REGISTRY = {
    "gulpease": lambda text, lang: indices.gulpease_index(text),
    "flesch":   lambda text, lang: indices.flesch_index(text, lang),
}

# Maps index name → set of languages it supports
INDEX_LANGS = {
    "gulpease": {"it"},
    "flesch":   {"it", "en"},
}
```

Aggiungere un nuovo indice richiede solo di aggiungere una voce in entrambi i dizionari, senza modificare la logica della funzione principale.

#### La funzione `generate_report`

```python
def generate_report(indices_to_use, lang, process_all_categories=False, category=None, sub_category=None):
```

**Parametri:**

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `indices_to_use` | `list[str]` oppure `"all"` | Indici da calcolare. `"all"` include tutti quelli registrati. |
| `lang` | `str` oppure `"all"` | Lingua dei testi (`"it"`, `"en"`, …). `"all"` processa tutte le lingue presenti nel JSON. |
| `process_all_categories` | `bool` | Se `True`, elabora tutte le categorie del JSON; altrimenti filtra su `category` e `sub_category`. |
| `category` | `str \| None` | Gruppo (es. `"adult"`, `"children"`). Obbligatorio se `process_all_categories=False`. |
| `sub_category` | `str \| None` | Sottocategoria (es. `"typical"`). Obbligatorio se `process_all_categories=False`. |

**Comportamento:**

1. Se `lang="all"`, vengono iterate tutte le lingue presenti nel file JSON; i testi vengono raccolti come coppie `(frase, lingua)`.
2. Per ogni frase viene calcolato solo il sottoinsieme degli indici richiesti che sono compatibili con la lingua di quella frase. Le celle per gli indici non compatibili (es. Gulpease su testi inglesi) vengono lasciate a `N/A`.
3. Il CSV prodotto contiene sempre una colonna `Lang` che indica la lingua di ogni riga, utile quando si processano più lingue contemporaneamente.
4. Le colonne degli indici nel CSV sono generate dinamicamente in base agli indici richiesti.

**Esempi d'uso:**

```python
# Solo Gulpease, testi italiani, singola categoria
generate_report(
    indices_to_use=["gulpease"],
    lang="it",
    process_all_categories=False,
    category="adult",
    sub_category="typical"
)

# Solo Flesch, testi inglesi, tutte le categorie
generate_report(
    indices_to_use=["flesch"],
    lang="en",
    process_all_categories=True
)

# Tutti gli indici, tutte le lingue, tutte le categorie
generate_report(
    indices_to_use="all",
    lang="all",
    process_all_categories=True
)
```

#### Struttura del CSV prodotto

Le colonne del file CSV di output sono:

| Colonna | Descrizione |
|---------|-------------|
| `Id` | Numero progressivo della frase |
| `Lang` | Lingua del testo (`it`, `en`, …) |
| `Sentence_Text` | Testo della frase analizzata |
| `Letters` | Numero di lettere alfabetiche |
| `Words` | Numero di parole |
| `Num_Sentences` | Numero di frasi rilevate |
| `gulpease` *(se richiesto)* | Punteggio Gulpease (arrotondato a 2 decimali; `N/A` se lingua incompatibile) |
| `flesch` *(se richiesto)* | Punteggio Flesch (arrotondato a 2 decimali; `N/A` se lingua incompatibile) |

Il nome del file viene generato automaticamente con il formato:  
`report_{indici}_{lingua}_{categoria}_{timestamp}.csv`

#### Struttura dei moduli

```
readability-sindone/
├── main.py           # Entry point: registro degli indici, caricamento JSON, generate_report
├── src/
│   ├── indices.py    # Funzioni di calcolo: gulpease_index, flesch_index
│   └── utils.py      # Funzioni di supporto: word_count, sentence_count, letter_count,
│                     #   count_syllables_it, count_syllables_en,
│                     #   average_words_per_sentence, average_syllables_per_word,
│                     #   extract_sentences
└── dictionaries/
    └── hyph_it_IT.dic  # Dizionario LibreOffice per sillabazione italiana
```

#### `indices.py`: le funzioni di calcolo

- **`gulpease_index(text)`**: calcola l'indice Gulpease. Non richiede il parametro lingua poiché è definito solo per l'italiano.
- **`flesch_index(text, lang)`**: calcola l'indice Flesch con la formula appropriata alla lingua. Per `lang="it"` usa i coefficienti adattati all'italiano; per `lang="en"` usa la formula originale di Flesch. Restituisce `None` se il testo non contiene parole o frasi.

---

## 6. Evoluzione recente: raggruppamento per opera e correzioni di accuratezza

Questa sezione documenta un secondo ciclo di modifiche, successivo alla versione descritta al punto 5.6, motivato da un feedback dei docenti sull'unità di analisi del report e da una verifica sistematica delle formule contro le fonti ufficiali da loro indicate. Viene riportato in dettaglio anche per motivare, nella tesi, le scelte fatte e i limiti rimasti.

### 6.1 Raggruppamento per opera (`extract_works`)

**Motivazione:** i docenti hanno richiesto che gli indici di leggibilità non vengano più calcolati frase per frase, ma su tutte le frasi che compongono la descrizione di una stessa opera del museo, considerate come un unico testo.

Nel file JSON, ogni categoria (es. `data["it"]["adult"]["typical"]`) è una lista di dizionari, dove ogni dizionario ha come chiavi i titoli delle opere e come valori la lista delle frasi che le descrivono:

```json
"Macchina fotografica di Secondo Pia": [
    "In questa nicchia è esposta la macchina fotografica...",
    "Si tratta di un apparecchio appositamente costruito..."
]
```

La funzione `extract_sentences()` esistente appiattisce ricorsivamente tutta la struttura in una lista di frasi sciolte, perdendo questo raggruppamento. È stata quindi introdotta una nuova funzione in `src/utils.py`:

```python
def extract_works(obj, current_title=None):
    works = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            works.extend(extract_works(value, current_title=key))
    elif isinstance(obj, list):
        if obj and all(isinstance(item, str) for item in obj):
            works.append((current_title, list(obj)))
        else:
            for item in obj:
                works.extend(extract_works(item, current_title=current_title))
    return works
```

A differenza di `extract_sentences()`, questa funzione si ferma non appena trova una lista composta interamente da stringhe (cioè le frasi di un'opera) e la etichetta con la chiave del dizionario più vicina che la contiene (il titolo dell'opera).

In `generate_report()` (`main.py`), per ogni opera le frasi vengono unite in due modi distinti:
- con uno **spazio singolo**, per il testo usato nel calcolo degli indici (`Letters`, `Words`, `Num_Sentences`, Gulpease, Flesch, Gunning Fog) — uno spazio non altera i conteggi basati su punteggiatura;
- con un **"a capo" (`\n`)**, solo per il valore mostrato nella colonna `Sentence_Text` del CSV, per leggibilità estetica (ogni frase originale su una riga propria all'interno della cella).

È stata aggiunta una colonna `Titolo` al CSV, e la variabile `MAX_SENTENCES` è stata rinominata `MAX_WORKS`, poiché ora limita il numero di opere processate e non più di frasi singole.

**Conflitto rilevato con un'altra parte della tesi:** la prima parte del progetto usa un modello text-to-speech per generare, dallo stesso `content.json`, i file audio riprodotti dal robot Sanbot al museo — un file audio per ogni singola frase, esattamente come funzionava la vecchia unità di analisi "per frase". Con il raggruppamento per opera, gli indici di leggibilità del report non corrispondono più alla granularità realmente percepita dal visitatore tramite Sanbot. Per questo motivo `extract_sentences()` non è stata rimossa: coesiste con `extract_works()` nel codice, così da poter tornare al comportamento per-frase modificando solo `generate_report()`, senza dover recuperare nulla dalla cronologia Git, qualora i docenti richiedano di mantenere (anche) la granularità per-frase.

### 6.2 Verifica delle formule rispetto alle fonti ufficiali

Su richiesta dei docenti, le tre formule implementate sono state confrontate punto per punto con le rispettive pagine di Wikipedia:

- [Indice Gulpease](https://it.wikipedia.org/wiki/Indice_Gulpease)
- [Formula di Flesch](https://it.wikipedia.org/wiki/Formula_di_Flesch)
- [Indice Gunning Fog](https://it.wikipedia.org/wiki/Indice_Gunning_fog)

**Gulpease**: la formula implementata in `gulpease_index()` (`89 + (300·Frasi − 10·Lettere) / Parole`) corrisponde esattamente alla fonte. Nessuna modifica necessaria.

**Flesch**: la formula implementata in `flesch_index()` per l'italiano corrisponde esattamente alla formulazione 1972 di Vacca-Franchina (`206 − 0.65·Sillabe/Parole − Parole/Frasi`), quella indicata dalla fonte come più attendibile. Il *codice* era già corretto; era la documentazione di questo stesso file (sezione 4) a contenere un errore di trascrizione, corretto al punto A in apertura di questa revisione.

**Gunning Fog**: la parte numerica della formula (`0.4·[(Parole/Frasi) + 100·(Parole_complesse/Parole)]`, implementata in `gunning_fog_index()`) corrisponde alla fonte. Mancava invece l'esatta definizione di "parola complessa" — vedi punto 6.3.

### 6.3 Bug: il Gunning Fog non escludeva i nomi propri dal conteggio delle "parole complesse"

**Problema:** secondo la fonte, una "parola complessa" (≥3 sillabe) per il calcolo del Gunning Fog **esclude**:
- i nomi propri;
- le parole composte da due parole brevi (1-2 sillabe ciascuna);
- i verbi di due sillabe che diventano di 3+ sillabe quando coniugati;
- gli avverbi in "-mente" derivati da una radice di due sillabe.

La funzione `count_complex_words()` in `src/utils.py` contava invece semplicemente ogni parola con ≥3 sillabe, senza alcuna eccezione.

**Perché è un problema rilevante per questo corpus:** i testi del Museo della Sindone contengono moltissimi nomi propri (titoli di opere, personaggi storici, toponimi: "Sìndone", "Secondo Pia", "Torino", "Sebastiano Valfrè"...). Molti di questi hanno 3 o più sillabe, e venivano quindi erroneamente contati come parole complesse, gonfiando artificialmente il punteggio Gunning Fog (un punteggio più alto indica un testo più difficile da leggere).

**Soluzione adottata:** implementare solo l'esclusione dei nomi propri, tramite un'euristica posizionale: una parola che inizia con lettera maiuscola e **non è la prima parola della sua frase** viene trattata come nome proprio ed esclusa dal conteggio.

```python
def count_complex_words(text, lang="en"):
    syllable_counter = count_syllables_it if lang == "it" else count_syllables_en
    complex_count = 0
    for sentence in re.split(r'[.!?]+', text):
        for i, word in enumerate(sentence.split()):
            stripped = word.strip(string.punctuation + "“”‘’")
            if not stripped:
                continue
            if i > 0 and stripped[0].isupper():
                continue  # trattata come nome proprio
            if syllable_counter(word) >= 3:
                complex_count += 1
    return complex_count
```

Le altre tre esclusioni (parole composte, verbi coniugati, avverbi in "-mente") non sono state implementate: richiederebbero un'analisi morfologica/NLP che, con euristiche semplici basate solo su regex o conteggio sillabe, rischierebbe di introdurre più falsi positivi/negativi di quanti ne risolva. Questa è una **limitazione nota e documentata** dell'implementazione attuale.

**Verifica:** sul testo di esempio "Macchina fotografica di Secondo Pia", le parole "Secondo" e "Sìndone" non vengono più contate come complesse; il punteggio Gunning Fog scende da 22.71 a 21.17. Sull'intero report (480 righe, tutte le lingue/categorie), il punteggio Gunning Fog è sceso o rimasto invariato in tutti i casi tranne uno, risultato anomalo poi spiegato e risolto al punto 6.4.

### 6.4 Bug: la punteggiatura finale rompeva il conteggio delle sillabe in inglese

**Come è stato scoperto:** investigando l'unico caso in cui, dopo la modifica del punto 6.3, il punteggio Gunning Fog era **aumentato** invece di diminuire (cosa logicamente impossibile se si escludono solo parole, mai se ne aggiungono), è stato individuato un bug preesistente e indipendente.

**Problema:** `count_syllables_en()` cerca la parola nel dizionario CMU (CMUdict) con un confronto esatto. Se alla parola è attaccata la punteggiatura di fine frase (es. `"period."` invece di `"period"`), la chiave non viene trovata nel dizionario, e la funzione ricade su un fallback approssimato (conteggio dei gruppi di vocali), meno preciso:

```
count_syllables_en("period")   -> 3  (corretto, da CMUdict)
count_syllables_en("period.")  -> 2  (fallback impreciso, "period." non è una chiave del dizionario)
```

Questo riguardava **l'ultima parola di ogni frase inglese**, in tutto il progetto, da prima di questa sessione. L'italiano non ne era affetto: la sillabazione tramite `pyphen` (basata su pattern ortografici, non su lookup esatto in un dizionario) gestisce correttamente la punteggiatura finale (`count_syllables_it("formato")` e `count_syllables_it("formato.")` danno entrambe 3).

**Perché l'effetto era piccolo ma non trascurabile:** su un testo lungo, un solo conteggio errato su una parola (l'ultima di ogni frase) ha un peso minimo sulla media. Ma su testi/titoli molto brevi l'effetto si amplifica: il titolo "Saint Francis de Sales." (4 parole, 1 frase) passava da un punteggio Flesch di 75.88 a 97.03 dopo la correzione, perché un solo errore di sillabazione su 4 parole pesa per un quarto della media.

**Soluzione:** `count_syllables_it()` e `count_syllables_en()` ora rimuovono la punteggiatura dalla parola prima di contare le sillabe, centralizzando la correzione così che tutte le funzioni che le usano (`average_syllables_per_word()`, `count_complex_words()`, e quindi `flesch_index()` e `gunning_fog_index()`) ne beneficino automaticamente.

### 6.5 Refactor: eliminazione di logica duplicata in `indices.py`

**Problema:** `flesch_index()` e `gunning_fog_index()` calcolavano manualmente il rapporto `parole/frasi` (e `flesch_index()` anche `sillabe/parole`) invece di richiamare le utility già esistenti `utils.average_words_per_sentence()` e `utils.average_syllables_per_word()`, pensate esattamente per questo scopo.

**Soluzione:** entrambe le funzioni indice ora richiamano le utility condivise. Questo refactor ha anche fatto emergere e corretto un bug latente in `average_syllables_per_word()`: la funzione ignorava il parametro lingua e usava sempre il conteggio sillabe inglese — un bug che non si era mai manifestato perché, prima di questo refactor, la funzione non era richiamata da nessuna parte del codice. Ora accetta un parametro `lang` e seleziona il contatore di sillabe corretto.

**Verifica:** confrontando il report generato prima e dopo questo refactor, riga per riga su tutte le 480 righe, i valori numerici sono risultati identici (il refactor ha eliminato duplicazione senza alterare alcun risultato).

### 6.6 Stato aggiornato della struttura del CSV e dei moduli

Rispetto alla tabella di sezione 5.6, le colonne del CSV prodotto sono ora:

| Colonna | Descrizione |
|---------|-------------|
| `Id` | Numero progressivo dell'opera |
| `Lang` | Lingua del testo (`it`, `en`, …) |
| `Titolo` | Titolo dell'opera del museo |
| `Sentence_Text` | Testo dell'opera (frasi unite con "a capo" per leggibilità) |
| `Letters` | Numero di lettere alfabetiche (sul testo unito con spazio) |
| `Words` | Numero di parole (sul testo unito con spazio) |
| `Num_Sentences` | Numero di frasi rilevate nell'opera |
| `gulpease` *(se richiesto)* | Punteggio Gulpease |
| `flesch` *(se richiesto)* | Punteggio Flesch |
| `gunning_fog` *(se richiesto)* | Punteggio Gunning Fog |

`src/utils.py` include ora anche `extract_works()`, una versione corretta e generalizzata di `average_syllables_per_word(text, lang)`, e `count_complex_words()` con esclusione dei nomi propri. `src/indices.py` include anche `gunning_fog_index()`, già presente nella versione corrente del codice ma non ancora documentato in questo file.
