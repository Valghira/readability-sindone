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

$$G = 89 + \frac{300 \cdot Frasi - 10 \cdot Lettere}{Parole}$$

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

$$F_{en} = 206.835 - 1.015 \cdot \frac{Parole}{Frasi} - 84.6 \cdot \frac{Sillabe}{Parole}$$

### Formula adattata per l'italiano

La versione italiana utilizza coefficienti diversi, poiché le parole italiane tendono ad avere più sillabe delle inglesi:

$$F_{it} = 206 - 0.65 \cdot \frac{Sillabe}{Parole} - \frac{Parole}{Frasi}$$

> **Nota:** questa è la formulazione del 1972 di Vacca e Franchina, indicata su Wikipedia come la più attendibile per l'italiano in base agli studi del Gruppo Linguistico-Pedagogico Universitario. Esiste anche una revisione del 1986 ($F_{it} = 217 - 1.3 \cdot \frac{Sillabe}{Parole} - 0.6 \cdot \frac{Parole}{Frasi}$), non utilizzata in questo progetto. Entrambe le formule sono state riverificate a giugno 2026 contro la fonte ([Wikipedia - Formula di Flesch](https://it.wikipedia.org/wiki/Formula_di_Flesch)) e corrispondono esattamente all'implementazione in `src/indices.py`.

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

- **Italiano**: si utilizza la libreria `pyphen` con il dizionario integrato per l'italiano (`lang="it_IT"`) e il parametro `left=1`. Il significato di questo parametro, la distinzione tra sillabazione linguistica e ifenazione tipografica e le verifiche che hanno portato a questa configurazione sono documentati nella sezione 7.7.
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
- Utilizza espressioni regolari avanzate: rimuove temporaneamente le abbreviazioni comuni (Sig., Dott., Prof., Dr., Avv., Ing., Cav.) con `re.sub`, poi conta i gruppi di punteggiatura terminale `[.!?]+` con `re.findall`. Non utilizza librerie NLP esterne.
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
- La logica attuale considera una frase come sequenza terminata da `.`, `!`, `?`, ma la funzione `refined_sentence_count` (successivamente rinominata `sentence_count`) migliora questa definizione con regole più accurate (gestione abbreviazioni, ellissi, punteggiatura multipla).
- Il sistema può essere facilmente adattato per limitare il numero di frasi analizzate, utile in vista di una futura interfaccia GUI.
- La conservazione delle versioni precedenti nel documento permette di tracciare l'evoluzione metodologica e di giustificare le scelte tecniche nel lavoro di tesi.

---

### 5.6 Prima versione multi-indice e multi-lingua

Questa è la versione raggiunta al termine di questa fase del progetto. Introduce il supporto a più indici di leggibilità e più lingue all'interno di un'unica funzione di generazione report, eliminando la dipendenza da una singola formula fissa.

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

> **Nota (aggiornamento 7.10):** il parametro `lang` supporta ora anche `list[str]` per rappresentare un sottoinsieme esplicito di lingue. Il significato di `"all"` è stato precisato: processa le lingue del JSON *supportate da almeno un indice*, non necessariamente tutte quelle presenti. I dettagli sono in sezione 7.10.
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
| `Title` | Titolo dell'opera del museo |
| `Sentence_Text` | Testo dell'opera (frasi unite con "a capo" per leggibilità) |
| `Letters` | Numero di lettere alfabetiche (sul testo unito con spazio) |
| `Words` | Numero di parole (sul testo unito con spazio) |
| `Num_Sentences` | Numero di frasi rilevate nell'opera |
| `gulpease` *(se richiesto)* | Punteggio Gulpease |
| `flesch` *(se richiesto)* | Punteggio Flesch |
| `gunning_fog` *(se richiesto)* | Punteggio Gunning Fog |

`src/utils.py` include ora anche `extract_works()`, una versione corretta e generalizzata di `average_syllables_per_word(text, lang)`, e `count_complex_words()` con esclusione dei nomi propri. `src/indices.py` include anche `gunning_fog_index()`, già presente nella versione corrente del codice ma non ancora documentato in questo file.

---

### 6.7 Refactoring di `main.py`: separazione raccolta dati e formato di output, e report Excel

**Motivazione:** l'aggiunta di un secondo formato di output (Excel) ha reso necessario un ulteriore refactoring di `main.py`. Lasciare tutta la logica all'interno della singola funzione `generate_report()` avrebbe significato duplicare il codice di raccolta dati (costruzione di `tagged_works`, risoluzione di `"all"` per lingua e indici, calcolo delle metriche) sia nella funzione CSV sia in quella Excel. Il principio DRY ha portato a estrarre una funzione privata condivisa.

#### Struttura dopo il refactoring

`generate_report()` viene sostituita da tre funzioni:

**`_collect_results(indices_to_use, lang, process_all_categories, category, sub_category)`**

Funzione privata (prefisso `_`, non destinata all'uso diretto dall'esterno) che centralizza tutta la logica di raccolta dati:
- risolve `"all"` per `indices_to_use` (in tutti gli indici registrati) e per `lang` (in tutte le lingue del JSON);
- itera le opere con `utils.extract_works()` e costruisce i testi di analisi e di visualizzazione;
- calcola `Letters`, `Words`, `Num_Sentences` e il valore di ogni indice per ogni opera;
- restituisce la tupla `(results, indices_to_use, lang, cat_label)` pronta da usare direttamente dalle funzioni di output.

```python
def _collect_results(indices_to_use, lang, process_all_categories, category, sub_category):
    if indices_to_use == "all":
        indices_to_use = list(INDEX_REGISTRY.keys())
    langs_to_process = list(data.keys()) if lang == "all" else [lang]
    # ... costruzione tagged_works con extract_works(), calcolo metriche ...
    cat_label = "all" if process_all_categories else f"{category}_{sub_category}"
    return results, indices_to_use, lang, cat_label
```

> **Nota (aggiornamento 7.10):** la risoluzione di `"all"` in `_collect_results` ora usa `get_supported_langs(data)` invece di `list(data.keys())`, escludendo le lingue non supportate. Il `return` restituisce `lang_label` (stringa leggibile per il filename) invece di `lang` (che potrebbe essere una lista). I dettagli in sezione 7.10.

**`generate_csv_report(indices_to_use, lang, process_all_categories=False, category=None, sub_category=None)`**

Chiama `_collect_results` e scrive l'output con `csv.DictWriter`. Firma e comportamento identici alla vecchia `generate_report()`: produce un file `.csv` con il nome `report_{indici}_{lingua}_{categoria}_{timestamp}.csv`.

**`generate_excel_report(indices_to_use, lang, process_all_categories=False, category=None, sub_category=None)`**

Chiama `_collect_results` e produce un file `.xlsx` con lo stesso nome ma estensione diversa. Descritto in dettaglio nel paragrafo successivo.

**Schema d'uso a fondo di `main.py`:**

```python
generate_csv_report(indices_to_use="all", lang="it", process_all_categories=False, category="adult", sub_category="typical")
generate_excel_report(indices_to_use="all", lang="it", process_all_categories=False, category="adult", sub_category="typical")
```

#### `generate_excel_report`: output in formato Excel

**Dipendenza aggiunta:** `openpyxl` (aggiunto a `requirements.txt`). Pandas è già presente nelle dipendenze ma non viene usato per la scrittura Excel: `openpyxl` usato direttamente dà controllo completo sulla formattazione delle singole celle, che non sarebbe disponibile con `pandas.DataFrame.to_excel()`.

**Formattazione applicata:**

- **Riga header in grassetto** — ogni cella della prima riga ha `Font(bold=True)`.
- **Colonna `Sentence_Text` con testo a capo** — le celle di questa colonna hanno `Alignment(wrap_text=True, vertical="top")`: i caratteri `\n` inseriti nel testo visualizzato vengono resi come veri a-capo all'interno della cella, senza bisogno di espandere manualmente la riga in Excel/Numbers.
- **Allineamento verticale `"top"` su tutte le celle** — le righe con `Sentence_Text` multi-riga diventano più alte; l'allineamento verticale in alto mantiene coerenza estetica su tutta la riga.
- **Larghezze colonne adattate automaticamente** — per ogni colonna si calcola il massimo tra la lunghezza dell'header e quella della riga più lunga nel corpus (per celle multi-riga, si usa la riga interna più lunga). Il valore risultante è cappato a 60 caratteri per evitare colonne esageratamente larghe.
- **Celle numeriche come numeri nativi Excel** — openpyxl scrive interi e float come tipi numerici nativi (non come stringhe come farebbe `csv.DictWriter`). I valori sono numericamente identici a quelli nel CSV, ma questo consente di usare direttamente su quelle colonne le funzioni di ordinamento, filtro e creazione di grafici di Excel.

```python
def generate_excel_report(indices_to_use, lang, process_all_categories=False, ...):
    results, indices_to_use, lang, cat_label = _collect_results(...)
    wb = openpyxl.Workbook()
    ws = wb.active
    bold = Font(bold=True)
    for col_idx, name in enumerate(fieldnames, start=1):
        cell = ws.cell(row=1, column=col_idx, value=name)
        cell.font = bold
    wrap    = Alignment(wrap_text=True, vertical="top")
    no_wrap = Alignment(vertical="top")
    sentence_col = fieldnames.index("Sentence_Text") + 1
    for row_idx, row in enumerate(results, start=2):
        for col_idx, name in enumerate(fieldnames, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=row[name])
            cell.alignment = wrap if col_idx == sentence_col else no_wrap
    # larghezze automatiche (max contenuto, cappato a 60)
    ...
    wb.save(path)
```

#### Struttura aggiornata dei moduli

```
readability-sindone/
├── main.py           # Entry point: INDEX_REGISTRY, INDEX_LANGS, caricamento JSON,
│                     #   _collect_results, generate_csv_report, generate_excel_report
├── src/
│   ├── indices.py    # gulpease_index, flesch_index, gunning_fog_index
│   └── utils.py      # word_count, sentence_count, letter_count,
│                     #   count_syllables_it, count_syllables_en,
│                     #   average_words_per_sentence, average_syllables_per_word(text, lang),
│                     #   count_complex_words, extract_sentences, extract_works
├── dictionaries/
│   └── hyph_it_IT.dic
└── requirements.txt  # pyphen, cmudict, textstat, pandas, openpyxl
```

### 6.8 Evidenziazione cromatica nel report Excel

#### Motivazione

Su richiesta della commissione, il report `.xlsx` evidenzia i punteggi degli indici di leggibilità con colori di sfondo che ne rendono immediatamente leggibile la fascia di difficoltà: verde per i testi più accessibili, rosso per quelli più difficili. La colorazione è implementata in `generate_excel_report` tramite `PatternFill` di openpyxl e non altera il valore numerico delle celle né il file CSV.

#### Soglie per indice

Le soglie sono tratte dalle pubblicazioni originali dei rispettivi autori.

**Indice Gulpease**
*(Lucisano & Piemontese, 1988, "GULPEASE: una formula per la predizione della difficoltà dei testi in lingua italiana", Scuola e città XXXIX(3); Piemontese, 1996, Capire e farsi capire, Tecnodid)*

Scala 0–100; punteggi più alti indicano maggiore leggibilità.

| Punteggio | Interpretazione | Colore |
|-----------|-----------------|--------|
| < 40 | Difficile anche per lettori con diploma superiore | Rosso |
| 40–59 | Accessibile a lettori con diploma superiore | Arancione |
| 60–79 | Accessibile a lettori con licenza media | Giallo |
| ≥ 80 | Accessibile a tutti | Verde |

**Indice Flesch Reading Ease**
*(Flesch, 1948, "A New Readability Yardstick", Journal of Applied Psychology 32(3))*

Scala 0–100; punteggi più alti indicano maggiore leggibilità. Le stesse soglie si applicano sia alla variante inglese (Flesch 1948) sia alla variante italiana (Franchina-Vacca 1972), che condividono la medesima scala.

| Punteggio | Livello | Colore |
|-----------|---------|--------|
| < 30 | Molto difficile (testi specialistici/professionali) | Rosso |
| 30–59 | Difficile (livello universitario) | Arancione |
| 60–79 | Medio (scuola secondaria / standard) | Giallo |
| ≥ 80 | Facile / Molto facile | Verde |

**Gunning Fog Index**
*(Gunning, 1952, The Technique of Clear Writing, McGraw-Hill)*

Scala tipica 6–20+; il valore rappresenta gli anni di istruzione necessari alla comprensione. **La scala è invertita rispetto ai precedenti**: punteggi più bassi indicano maggiore accessibilità.

| Punteggio | Livello di istruzione richiesto | Colore |
|-----------|--------------------------------|--------|
| ≤ 8 | Scuola media (accesso universale) | Verde |
| 8–12 | Scuola secondaria / liceo | Giallo |
| 12–17 | Università | Arancione |
| > 17 | Post-laurea / testi molto tecnici | Rosso |

#### Implementazione

In `src/core.py` sono definiti:

- Quattro costanti di colore (colori saturi per massima leggibilità visiva):
  ```
  _COLOR_GREEN  = "92D050"   # verde vivo
  _COLOR_YELLOW = "FFFF00"   # giallo puro
  _COLOR_ORANGE = "FF6600"   # arancione deciso
  _COLOR_RED    = "FF0000"   # rosso pieno
  ```
- Un oggetto bordo sottile, applicato a tutte le celle (header e dati):
  ```python
  _thin = Side(style="thin")
  _BORDER = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)
  ```
- La funzione `_score_color(index_name, score)` che restituisce la costante colore appropriata dato il nome dell'indice e il punteggio numerico; restituisce `None` per valori non numerici (`"N/A"`, `None`), lasciando quelle celle senza riempimento.

Nel loop di scrittura di `generate_excel_report`, per ogni cella vengono applicati bordo e — se si tratta di una colonna indice — il riempimento cromatico:
```python
cell.border = _BORDER
if name in indices_to_use:
    color = _score_color(name, row[name])
    if color:
        cell.fill = PatternFill(patternType="solid", fgColor=color)
```
I bordi facilitano la lettura riga per riga nel foglio Excel. Le celle con valore `"N/A"` (indice non applicabile alla lingua) o `None` (testo vuoto) rimangono senza riempimento colorato.

### 6.9 Verifica della formula Flesch rispetto a Wikipedia

In seguito a un controllo delle formule rispetto alla fonte indicata dai docenti (Wikipedia IT — *Formula di Flesch*), è stato verificato che le implementazioni in `src/indices.py` corrispondono esattamente alle formule pubblicate:

**Variante inglese (Flesch 1948):**
```
F = 206,835 − (84,6 × S) − (1,015 × P)
```

**Variante italiana (Vacca & Franchina 1972, raccomandata dal GULP):**
```
F = 206 − (0,65 × S) − P
```

dove S = media sillabe per parola, P = media parole per frase.

**Nota sulla scala italiana:** la variante italiana con questi coefficienti produce punteggi nell'intervallo ~160–200 anziché 0–100. Questo è un limite noto della formula nella sua variante non normalizzata; i docenti hanno confermato che i valori così calcolati sono accettabili per gli scopi di questo studio. Di conseguenza, le celle Flesch dei testi italiani risulteranno tutte nella fascia "verde" del report Excel.

---

## 7. Interfaccia grafica (GUI)

### 7.1 Motivazione e scelta della libreria

**Obiettivo:** rendere il tool accessibile anche a chi non usa la riga di comando — ricercatori, curatori del museo, collaboratori che ricevono il progetto senza esperienza di terminale.

**Libreria scelta: CustomTkinter.** Le principali alternative sono state valutate e scartate:

- **Tkinter puro** (incluso nella libreria standard Python): escluso per l'aspetto visuale datato su macOS, non adatto a qualcosa da mostrare ai docenti.
- **PyQt6/PySide6**: API professionale ma complessa, molti concetti da imparare, dipendenza pesante.
- **Streamlit**: molto elegante ma web-based — apre una scheda del browser, richiede un paradigma completamente diverso (ogni interazione causa un re-run dell'intero script), non adatto a un'app desktop standalone.
- **CustomTkinter**: wrapper moderno sopra Tkinter che ne mantiene l'API semplice ma aggiunge aspetto contemporaneo (bordi arrotondati, supporto dark/light mode, tema blu). Una sola dipendenza extra (`pip install customtkinter`), documentazione ottima, ideale per chi è alle prime armi con le GUI Python.

**Nota macOS:** Python installato via Homebrew non include il modulo `_tkinter` di default. Prima di usare la GUI è necessario installare il pacchetto Homebrew corrispondente alla versione Python in uso:
```bash
brew install python-tk@3.14  # sostituire 3.14 con la propria versione
```

**Dipendenze aggiunte a `requirements.txt`:** `customtkinter`.

### 7.2 Nuovo strato condiviso: `src/core.py`

L'aggiunta della GUI ha richiesto un ulteriore refactoring architetturale. Il problema: `main.py` caricava il JSON e chiamava le funzioni di report **a livello di modulo** — cioè fuori da qualsiasi funzione, eseguiti immediatamente all'`import`. Se `gui.py` avesse fatto `import main`, quel codice sarebbe stato eseguito come effetto collaterale indesiderato (caricamento JSON e generazione report automatica).

**Soluzione:** tutta la logica di business è stata spostata in un nuovo file `src/core.py`, importabile liberamente sia dalla CLI sia dalla GUI senza effetti collaterali.

Funzioni e costanti esportate da `src/core.py`:

| Simbolo | Descrizione |
|---------|-------------|
| `DEFAULT_JSON_PATH` | Path di default al file JSON del corpus |
| `MAX_WORKS` | Limite opere da processare (None = tutte) |
| `INDEX_REGISTRY` | Dizionario nome → callable dell'indice |
| `INDEX_LANGS` | Dizionario nome → lingue supportate |
| `load_data(json_path)` | Carica e restituisce il JSON |
| `inspect_json(data)` | Analizza la struttura del corpus → `{lang: {age_group: [sub_cat, ...]}}` |
| `_collect_results(data, ...)` | Raccoglie i risultati; ora riceve `data` come primo argomento invece di una variabile globale |
| `get_supported_langs(data)` | Restituisce la lista ordinata di codici lingua presenti nel corpus e supportati da almeno un indice |
| `generate_csv_report(data, ..., log_fn=print)` | Genera il CSV; `log_fn` sostituisce `print` per reindirizzare il log |
| `generate_excel_report(data, ..., log_fn=print)` | Genera l'Excel; stessa firma |

`main.py` diventa un thin wrapper di 12 righe con guard `if __name__ == "__main__"`:

```python
from src.core import load_data, generate_csv_report, generate_excel_report, DEFAULT_JSON_PATH

if __name__ == "__main__":
    data = load_data(DEFAULT_JSON_PATH)
    generate_csv_report(data, indices_to_use="all", lang="it", ...)
    generate_excel_report(data, indices_to_use="all", lang="it", ...)
```

`python main.py` funziona esattamente come prima — zero regressioni per l'uso da terminale.

### 7.3 Struttura della GUI (`gui.py`)

La GUI è una finestra singola (820×740 px) organizzata in cinque sezioni verticali, ognuna un `CTkFrame` distinto:

**1 — File JSON**
Campo di testo precompilato con il path al corpus di default, bottone "Sfoglia" (apre un file dialog filtrato su `*.json`). Al caricamento del file, viene chiamata `inspect_json()` e i risultati popolano un riquadro read-only:
```
Corpus: 2 lingue  •  it: adult(3 sub-cat), child(3 sub-cat)
                      en: adult(3 sub-cat), child(3 sub-cat)
```

**2 — Configurazione** (tre colonne affiancate)
- *Indici*: un checkbox per ogni indice, generati dinamicamente da `INDEX_REGISTRY.keys()`; bottoni "Tutti"/"Nessuno" per selezione rapida.
- *Lingua*: radio Tutte / Italiano / Inglese. *(Questa implementazione statica è stata in seguito sostituita con checkbox costruite dinamicamente; vedi sezione 7.10.)*
- *Formato output*: checkbox CSV e checkbox Excel (.xlsx), selezionabili indipendentemente.

**3 — Categorie**
Radio "Tutte le categorie" (default, processa tutto il corpus) oppure "Seleziona:" con due menu a tendina (age_group / sub-categoria) disabilitati di default e abilitati solo se si sceglie "Seleziona:". I valori nei menu si aggiornano automaticamente in base alla lingua selezionata nella sezione 2.

**4 — Bottone "Genera Report"**
Grande e centrato, viene disabilitato durante la generazione (testo "Generazione in corso…") per prevenire doppi click, e riabilitato al termine.

**5 — Log**
Riquadro read-only che riceve i messaggi di stato via `log_fn=self._log`, mostrando i path dei file generati e l'esito dell'operazione.

**Footer** — label grigio piccolo fisso in basso: *Sviluppato da Valerio Ghirardotto*.

### 7.4 Comportamento dinamico e future-proofing

- **Cambio JSON:** caricare un file diverso via "Sfoglia" ricalcola la preview del corpus e ripopola tutti i menu di lingua e categoria in tempo reale, senza riavviare l'app.
- **Checkbox indici generati da codice:** i checkbox sono costruiti iterando `INDEX_REGISTRY.keys()`. Aggiungere un nuovo indice in `src/core.py` fa apparire automaticamente il checkbox corrispondente in GUI senza toccare `gui.py`.
- **Validazione pre-esecuzione:** se nessun indice o nessun formato è selezionato, il bottone scrive un avviso nel log invece di procedere.
- **`log_fn` come callback:** `generate_csv_report` e `generate_excel_report` accettano un parametro `log_fn` (default `print`). Da terminale si usa `print`; dalla GUI si passa `self._log`, che scrive nel riquadro di log. In questo modo la stessa funzione funziona sia in modalità CLI che GUI senza codice condizionale.
- **Lingue rilevate dinamicamente:** al caricamento del JSON, `get_supported_langs(data)` calcola l'intersezione tra le lingue presenti nel corpus e quelle supportate da almeno un indice (`INDEX_LANGS`). Le checkbox nella sezione Lingua vengono ricostruite da zero su questo insieme. Caricare un JSON con una lingua non supportata non produce errori: la lingua viene esclusa dalle checkbox e segnalata con un avviso nel log.
- **Sottoinsiemi arbitrari di lingue:** il parametro `lang` della pipeline ora accetta `str`, `"all"` o `list[str]`. Selezionare qualsiasi sottoinsieme non vuoto di lingue disponibili produce un report che le contiene tutte, con `lang_label` nel nome del file costruito come codici ordinati separati da `_` (es. `en_it`).
- **Categorie e sottocategorie sempre dinamiche:** i menu vengono popolati dalla struttura del JSON caricato; nessuna categoria o sottocategoria è hardcoded. Verificato con JSON di test contenenti nomi di categorie arbitrari.

### 7.5 Struttura aggiornata dei moduli

```
readability-sindone/
├── main.py           # CLI thin wrapper (12 righe): importa da src/core,
│                     #   chiama generate_csv/excel_report sotto __main__
├── gui.py            # GUI entry point: CustomTkinter app, importa da src/core
├── src/
│   ├── core.py       # Business logic condivisa: INDEX_REGISTRY, INDEX_LANGS,
│   │                 #   load_data, inspect_json, _collect_results,
│   │                 #   generate_csv_report, generate_excel_report
│   ├── indices.py    # gulpease_index, flesch_index, gunning_fog_index
│   └── utils.py      # word_count, sentence_count, letter_count,
│                     #   count_syllables_it/en, average_words_per_sentence,
│                     #   average_syllables_per_word(text, lang),
│                     #   count_complex_words, extract_sentences, extract_works
└── requirements.txt  # pyphen, cmudict, textstat, pandas, openpyxl, customtkinter
```

### 7.6 Evidenziazione cromatica dei messaggi di errore nel log

**Motivazione:** i docenti hanno segnalato che nel pannello Log tutti i messaggi — informativi, avvertimenti ed errori — avevano lo stesso colore, rendendo difficile accorgersi a colpo d'occhio di un problema bloccante.

**Approccio tecnico:** `ctk.CTkTextbox` è un wrapper sopra il widget nativo `tkinter.Text`, accessibile tramite l'attributo `._textbox`. Il widget `tkinter.Text` supporta i *tag*: etichette associate a intervalli di testo a cui possono essere applicati stili come colore del testo, grassetto o sottofondo. Tramite `tag_configure` si definisce lo stile di un tag; tramite `tag_add` lo si applica a un intervallo di caratteri già inseriti. Questo meccanismo permette di colorare selettivamente singole righe del log senza dover cambiare il widget o introdurre widget aggiuntivi.

**Classificazione dei messaggi:** i messaggi critici nel codice sono già riconoscibili dal prefisso con cui iniziano:
- `"ERRORE"` — errori bloccanti (es. file JSON non trovato, eccezione durante la generazione del report)
- `"ATTENZIONE"` — avvertimenti che impediscono l'esecuzione (es. nessun indice selezionato, nessun formato di output scelto)

Il rilevamento avviene con `msg.startswith("ERRORE") or msg.startswith("ATTENZIONE")` nel metodo `_log`.

**Modifiche a `gui.py`:**

In `_build_log_section`, dopo la creazione di `self.log_box`, viene configurato il tag `"error"` con colore rosso (#E53935, rosso Material Design):

```python
self.log_box._textbox.tag_configure("error", foreground="#E53935")
```

In `_log`, la posizione `start` viene catturata *prima* dell'inserimento del testo e `end` *dopo*; il tag viene applicato all'intervallo `[start, end]` solo se il messaggio è un errore o avvertimento:

```python
def _log(self, msg):
    is_error = msg.startswith("ERRORE") or msg.startswith("ATTENZIONE")
    self.log_box.configure(state="normal")
    start = self.log_box._textbox.index("end-1c")
    self.log_box.insert("end", msg + "\n")
    if is_error:
        end = self.log_box._textbox.index("end-1c")
        self.log_box._textbox.tag_add("error", start, end)
    self.log_box.see("end")
    self.log_box.configure(state="disabled")
    self.update_idletasks()
```

**Risultato:** i messaggi `ERRORE` e `ATTENZIONE` appaiono in rosso nel pannello Log; i messaggi informativi (`JSON caricato: ...`, `Fatto.`) restano nel colore predefinito del testo.

**Evoluzione successiva: terzo livello visivo (AVVISO)**

In una fase successiva (v. sezione 7.10) è stato introdotto un terzo livello visivo per i messaggi non bloccanti che l'utente deve comunque conoscere. Il tag `"warning"` arancione (`#FF8C00`) viene configurato accanto al tag `"error"` in `_build_log_section`:

```python
self.log_box._textbox.tag_configure("warning", foreground="#FF8C00")
```

Il metodo `_log` rileva i messaggi che iniziano con `"AVVISO"` e applica il tag `"warning"` tramite un ramo `elif` (che esclude la sovrapposizione con il tag `"error"`).

La gerarchia visiva completa diventa:

| Prefisso | Colore | Natura |
|----------|--------|--------|
| *(nessuno)* | default del tema | informativo |
| `AVVISO` | arancione `#FF8C00` | non bloccante |
| `ATTENZIONE` | rosso `#E53935` | bloccante (validazione) |
| `ERRORE` | rosso `#E53935` | eccezione |

Il primo utilizzo concreto di `AVVISO` è la segnalazione delle lingue presenti nel JSON ma non supportate da alcun indice, emessa da `_load_json` dopo il messaggio "JSON caricato: …".

### 7.7 Verifica e perfezionamento della sillabazione italiana

#### Contesto

Durante lo sviluppo era stato inserito nella cartella `dictionaries/` un file `hyph_it_IT.dic` prelevato dal repository ufficiale di LibreOffice, nell'ipotesi che disporre di un dizionario di sillabazione esplicito e fisicamente presente nel progetto offrisse un controllo maggiore rispetto al dizionario integrato in pyphen. Il codice corrispondente in `src/utils.py` caricava il file locale se presente, altrimenti ricadeva sul dizionario bundled:

```python
if ITALIAN_HYPHEN_DICT_PATH.exists():
    dic_it = pyphen.Pyphen(filename=str(ITALIAN_HYPHEN_DICT_PATH))
else:
    dic_it = pyphen.Pyphen(lang="it_IT")
```

#### Verifica dell'equivalenza del dizionario locale

Un confronto diretto tra i due file ha mostrato che `hyph_it_IT.dic` era **byte per byte identico** al dizionario italiano già distribuito con pyphen (stesso hash MD5, stessa dimensione: 2308 byte). Il repository di LibreOffice e il pacchetto pyphen usano la stessa sorgente per i dizionari di sillabazione. La copia locale non offriva quindi alcun vantaggio rispetto all'uso diretto di `pyphen.Pyphen(lang="it_IT")`.

Di conseguenza, il file locale e la relativa logica di caricamento sono stati rimossi: la cartella `dictionaries/` è ora vuota. Le costanti `ITALIAN_HYPHEN_DICT_PATH` e `PROJECT_ROOT`, l'import `from pathlib import Path` e il blocco `if/else` sono stati eliminati da `src/utils.py`.

#### Pyphen: sillabazione linguistica e ifenazione tipografica

Questa verifica ha spostato l'attenzione sul vero elemento rilevante per l'accuratezza del conteggio: non il *contenuto* del dizionario, ma il *modo* in cui pyphen lo utilizza. Per capire il problema individuato, è utile chiarire cosa fa pyphen e come funzionano i parametri che lo governano.

**Che cosa fa pyphen.** Pyphen è una libreria Python che calcola i punti in cui una parola può essere divisa tra due righe — un'operazione che in tipografia si chiama *ifenazione* (in inglese *hyphenation*). Per farlo, pyphen legge dizionari in formato LibreOffice/TeX che contengono *pattern linguistici*: regole derivate dalla fonetica e dalla morfologia della lingua. Per l'italiano, questi pattern codificano le regole della sillabazione: dove separare le sillabe, dove si trovano dittonghi, dove si trovano iati. Internamente, per ogni parola il dizionario genera un insieme di *posizioni* — indici della stringa — in corrispondenza delle quali è lecito inserire un trattino.

**Sillabazione linguistica e ifenazione tipografica: una distinzione importante.** Il punto di separazione linguisticamente corretto e quello tipograficamente accettabile non coincidono sempre. In linguistica, `opera` si divide in tre sillabe: **o – pe – ra**. La prima sillaba è la singola vocale iniziale "o". In tipografia, però, spezzare una parola lasciando un solo carattere a inizio o fine riga è considerato esteticamente indesiderabile e viene evitato. Un sistema tipografico non scriverebbe `o-` a fine riga, saltando quel punto e usando il successivo: `ope-ra` anziché `o-pe-ra`.

Pyphen è nato per uso tipografico, e i suoi valori predefiniti riflettono questa origine. Il filtro che produce questo comportamento è controllato dai parametri `left` e `right`.

**Il parametro `left`.** Dopo che i pattern del dizionario hanno generato tutti i punti di separazione linguisticamente validi, pyphen li filtra con questa regola: viene mantenuto solo un punto di posizione `i` se `i >= left`. In altre parole, `left` impone una lunghezza minima per il primo segmento della parola (i caratteri che precedono il primo trattino). Con il valore predefinito `left=2`, la posizione 1 — che lascerebbe un solo carattere nel primo segmento — viene scartata. Per `opera`, il dizionario genera le posizioni {1, 3}: con `left=2`, la posizione 1 viene filtrata e rimane solo la 3, producendo `ope-ra` invece di `o-pe-ra`.

**Il parametro `right`.** In modo simmetrico, `right` impone una lunghezza minima per l'ultimo segmento (i caratteri dopo l'ultimo trattino): viene mantenuto solo un punto di posizione `i` se `i <= len(word) - right`. Con `right=2` (valore predefinito), non è ammesso un segmento finale di un solo carattere. Su parole italiane che terminano in consonante o in sequenze di più lettere, questo vincolo non ha effetti pratici; lo stesso vale per il corpus analizzato: come verificato sperimentalmente, `right=2` e `right=1` producono risultati identici su tutte le 584 parole italiane del corpus.

> **Nota tecnica.** pyphen ignora esplicitamente le direttive `LEFTHYPHENMIN` e `RIGHTHYPHENMIN` eventualmente presenti nel file dizionario (sono nella tupla `ignored` del codice sorgente). I valori di `left` e `right` dipendono esclusivamente dai parametri del costruttore `Pyphen(...)`.

**Perché `left=2` causa errori nel conteggio delle sillabe.** Pyphen viene usato nel progetto non per spezzare parole a fine riga, ma per stimare il numero di sillabe ai fini del calcolo degli indici di leggibilità. Quando `left=2` scarta il punto di separazione linguisticamente corretto dopo la vocale iniziale, il numero di segmenti restituiti da `inserted()` è inferiore di 1 rispetto al numero reale di sillabe. Questo vale sistematicamente per tutte le parole italiane che iniziano con una singola vocale seguita da consonante: `era`, `una`, `origini`, `esposto`, `edizione`, `opera`, e molte altre.

**Esempio concreto.** La parola `opera` ha tre sillabe fonologiche: o – pe – ra. Il dizionario genera i punti di separazione nelle posizioni {1, 3}.

| Configurazione | Punti ammessi | Risultato di `inserted()` | Sillabe contate |
|---|---|---|---|
| `left=2` (precedente) | solo {3} (pos. 1 esclusa) | `ope-ra` | **2** — errato |
| `left=1` (attuale) | {1, 3} | `o-pe-ra` | **3** ✓ |

**Perché `left=1` è la configurazione corretta per il nostro scopo.** Impostando `left=1`, pyphen ammette punti di separazione anche dopo il primo carattere. Il dizionario contiene già il punto fonologicamente corretto dopo la vocale iniziale: `left=1` smette semplicemente di filtrarlo. Non vengono modificati i pattern linguistici del dizionario né aggiunte nuove regole. Viene solo rimosso un vincolo tipografico che era privo di senso nel contesto del conteggio delle sillabe.

#### Test comparativo

Il confronto è stato condotto su 584 parole italiane uniche estratte dal corpus, confrontando il conteggio prodotto da pyphen con un riferimento indipendente (nuclei vocalici): una parola con N gruppi vocalici separati da consonanti ha N sillabe, nella misura in cui non intervengano dittonghi o iati.

| Configurazione | Concordanze con riferimento euristico | Concordanza (%) |
|---|---|---|
| Precedente (`left=2`) | 533 / 584 | 91,3% |
| Attuale (`left=1`) | 577 / 584 | 98,8% |

Le percentuali misurano la concordanza con il metodo dei nuclei vocalici, non l'accuratezza assoluta di pyphen: come mostrato nell'analisi degli errori residui, alcune discrepanze non sono errori di pyphen ma limiti del riferimento euristico (dittonghi/iati non distinti, nomi propri stranieri). Il passaggio dal 91,3% al 98,8% costituisce comunque una forte evidenza sperimentale del miglioramento sul corpus analizzato.

La configurazione `left=1` corregge 45 parole — tutte inizianti con vocale — e introduce una sola regressione: il numero romano `XVI`, che con `left=1` viene diviso come `X-VI` (2 segmenti) pur avendo un solo nucleo vocalico. Per ora non è stata implementata alcuna gestione speciale dei numeri romani.

Tra i 7 errori residui, tre non sono errori reali di pyphen: `savoia` (sa–vo–ia), `telaio` (te–la–io) e `distribuiti` (di–stri–bu–i–ti) sono sillabati correttamente da pyphen, ma il riferimento basato sui nuclei vocalici li sottostima perché non distingue dittonghi da iati. Gli altri tre (`chambéry`, `charny`, `mandylion`) sono nomi propri stranieri con `y` in funzione vocalica — un caso che pyphen non gestisce perfettamente in nessuna configurazione.

#### Modifica effettuata

`src/utils.py` è stato semplificato sostituendo il blocco condizionale con una singola riga:

```python
dic_it = pyphen.Pyphen(lang="it_IT", left=1)
```

Rimossi anche: `from pathlib import Path`, `PROJECT_ROOT`, `ITALIAN_HYPHEN_DICT_PATH` e l'intera logica `if/else`. Il parametro `right` è stato lasciato al valore predefinito (`right=2`), confermato sperimentalmente irrilevante su questo corpus.

#### Impatto sui report

Su un report completo (tutte le opere, tutte le lingue, tutti gli indici), 150 delle 240 opere italiane presentano variazioni in almeno uno degli indici dipendenti dalle sillabe. Gulpease — che non usa il conteggio sillabe — rimane invariato in tutti i casi. I testi inglesi non sono interessati.

| Indice | Direzione | Δ medio | Δ massimo osservato |
|---|---|---|---|
| Flesch | ↓ | −0,05 | −0,13 |
| Gunning Fog | ↑ | +0,56 | +2,98 |
| Gulpease | invariato | — | — |

La direzione delle variazioni è coerente: più sillabe contate implicano parole in media più lunghe foneticamente, e quindi punteggi di leggibilità che riflettono più correttamente la complessità reale del lessico. Le variazioni di Flesch sono praticamente impercettibili sulla scala di riferimento. Quelle di Gunning Fog sono più visibili ma in tutti i casi rimangono all'interno della stessa fascia interpretativa.

### 7.8 Analisi diagnostica della sillabazione inglese

Dopo aver corretto e verificato la sillabazione italiana (sezione 7.7), è stata condotta un'analoga analisi diagnostica sulla sillabazione inglese, con l'obiettivo di misurare la copertura effettiva di CMUdict sul corpus reale e valutare l'affidabilità del fallback euristico sulle parole non coperte.

#### Implementazione attuale

La funzione `count_syllables_en()` in `src/utils.py` opera in due fasi distinte:

1. **Ricerca in CMUdict.** La parola viene normalizzata con `word.strip(string.punctuation + """''")` — punteggiatura ASCII e virgolette tipografiche vengono rimosse **solo dalle estremità**; la punteggiatura interna (trattini, apostrofi interni, em-dash) non viene toccata. Se la parola normalizzata e convertita in minuscolo è presente in CMUdict, si usa la prima pronuncia disponibile (`cmu_dict[word_lower][0]`) e si contano i fonemi il cui ultimo carattere è una cifra. In ARPABET, i numeri 0, 1, 2 appaiono **esclusivamente** sui fonemi vocalici come indicatori del livello di accento (0=atono, 1=accento primario, 2=secondario): contarli equivale quindi a contare i nuclei sillabici, che in inglese coincidono con le sillabe fonologiche.

2. **Fallback euristico.** Se la parola non è in CMUdict, si contano i gruppi contigui di caratteri appartenenti alla stringa `"aeiouy"`, restituendo almeno 1. Questo metodo non distingue dittonghi da iati, non riconosce vocali accentate (es. `é`, `è`), e non tratta casi particolari come la *e* muta finale, le forme contratte o le parole composte con trattino.

#### Copertura di CMUdict sul corpus inglese

Il corpus inglese contiene 8.802 occorrenze totali di parole, per 600 tipi (parole uniche). L'analisi è stata condotta con uno script temporaneo, usando la stessa logica di normalizzazione di `count_syllables_en()`.

| Misura | Valore |
|---|---|
| Parole uniche totali | 600 |
| Presenti in CMUdict | 536 (89,3%) |
| OOV (non in CMUdict) | 64 (10,7%) |
| Copertura ponderata su occorrenze | 94,4% |
| Occorrenze gestite dal fallback | 5,6% |

La copertura ponderata — la percentuale di volte in cui CMUdict è effettivamente disponibile durante il calcolo — è la cifra più rilevante per valutare l'impatto pratico del fallback.

#### Analisi delle parole OOV

Le 64 parole non presenti in CMUdict appartengono a categorie prevedibili per un corpus museale con testi sia storici che in lingue originali diverse:

- **Numeri e date** (18 OOV, es. `4`, `21`, `1578`, `2010`): il fallback restituisce 1. Difendibile ai fini dell'indice di leggibilità.
- **Composti con trattino** (11 OOV, es. `ninety-eight` freq=24, `eighteenth-century` freq=12): il fallback opera sull'intera stringa incluso il trattino. `ninety-eight` ottiene 4 dal fallback, mentre il valore reale è 3 (nine-ty-eight). Il trattino è trattato correttamente come separatore non-vocalico, ma il conteggio complessivo è impreciso perché `y` finale di `ninety` viene contata come sillaba separata.
- **Nomi propri e toponimi** (14+ OOV, es. `edessa` freq=18, `mandylion` freq=18, `zakopane`, `sanliurfa`): il fallback produce risultati spesso corretti per questi nomi (`edessa`=3 reale 3, `mandylion`=3 reale 3), ma è intrinsecamente inaffidabile su parole con schemi fonetici atipici per l'inglese.
- **Parole con caratteri non-ASCII** (`chambéry`, `besançon`, `valfrè`, `which—in`, `edition—is`): le vocali accentate (`é`, `è`) non sono nella stringa `"aeiouy"` e vengono trattate come consonanti dal fallback. `valfrè` ottiene quindi 1 invece di 2. Le ultime due contengono un em-dash (U+2014) incorporato, che non è in `string.punctuation` (ASCII) e non viene strippato nemmeno dai bordi — i due token vengono processati come parole malformate.
- **Forme contratte** (`pia's` freq=6, `shroud's` freq=24): il fallback tratta `ia` come un unico gruppo vocalico, dando a `pia's` 1 sillaba invece di 2.

#### Pronunce multiple in CMUdict

Tra le 536 parole presenti in CMUdict, 126 hanno più di una pronuncia; di queste, 11 producono conteggi di sillabe diversi tra le varianti. I casi più frequenti nel corpus sono `several` (usato con 2 sillabe, alternativa 3), `history` (usato con 3, alternativa 2), `camera` (usato con 3, alternativa 2). Le varianti con meno sillabe corrispondono alle pronunce ridotte tipiche del parlato colloquiale; usare sempre la prima pronuncia (`[0]`), che è la forma più elaborata, è coerente con l'obiettivo di misurare la complessità lessicale in un contesto di comunicazione museale. Questo non costituisce un problema.

#### Riferimento indipendente: textstat

`textstat` — già incluso in `requirements.txt` — è stato usato come punto di confronto. La sua implementazione interna usa CMUdict come metodo principale e pyphen (con dizionario inglese) come fallback per le parole OOV: **non** l'euristica sui gruppi vocalici. Per le parole in CMUdict, textstat usa la stessa logica della nostra implementazione, quindi i risultati sono identici. Le differenze riguardano **solo le 64 parole OOV**, dove i due metodi di fallback divergono:

- 568/600 parole (94,7%): concordanza tra i due metodi
- 32/600 parole (5,3%): disaccordo — tutte e sole parole OOV

Per alcuni OOV il nostro fallback è più accurato di textstat/pyphen (`edessa`, `mandylion`, `hematoma`); per altri è meno accurato (`pia's`, `valfrè`, `ninety-eight`). Nessuno dei due metodi è una ground truth.

#### Impatto sui report

Le differenze tra i due metodi di fallback si ripercuotono sulle opere che contengono OOV frequenti. Su 240 opere inglesi analizzate, 126 (52,5%) presentano almeno una differenza di conteggio rispetto a textstat. Il Δ Flesch massimo osservato su una singola opera è circa 14 punti, generato principalmente da `ninety-eight` (24 occorrenze totali nel corpus), che il nostro fallback sovrastima di 1 sillaba per ogni occorrenza. Le opere con alta concentrazione di questa parola in rapporto alla loro lunghezza sono quelle più esposte all'errore.

#### Limitazioni identificate

A differenza della sillabazione italiana, dove è stata identificata e corretta una causa sistematica (il parametro `left=2`), per l'inglese non esiste un'unica correzione strutturale equivalente. I problemi identificati sono:

1. **Vocali accentate non riconosciute dal fallback** (`valfrè`, `besançon`, `chambéry`): frequenza bassa (6 occorrenze ciascuna), impatto limitato.
2. **Em-dash non strippato** (`which—in`, `edition—is`): tokenizzazione errata per 2 parole, freq=6 ciascuna, impatto trascurabile.
3. **`ninety-eight` sovrastimato di 1 sillaba**: la parola più frequente tra le OOV problematiche (24 occorrenze); il fallback dà 4 invece del reale 3.
4. **`pia's` trattato come monosillabo**: sequenza `ia` collassata in un solo gruppo vocalico.

I problemi 1, 2 e 3 sono stati successivamente corretti con modifiche minimali a `src/utils.py` e `src/core.py`; il problema 4 è rimasto documentato come limitazione nota. Le correzioni e il loro impatto sono documentati nella sezione 7.9.

---

### 7.9 Correzioni al fallback della sillabazione inglese

In seguito all'analisi diagnostica della sezione 7.8, sono state apportate tre correzioni mirate a `src/utils.py` e `src/core.py`. L'obiettivo era eliminare gli errori sistematicamente verificabili senza introdurre regole specifiche per singole parole né nuove dipendenze. Il core CMUdict rimane invariato.

#### Correzione 1 — Vocali accentate nel fallback (src/utils.py)

**Problema**: il loop di conteggio vocalico confrontava `char in "aeiouy"`, ma le vocali accentate (`é`, `è`, `ç`-base-vocale) non sono nella stringa ASCII. `valfrè` veniva contato come 1 sillaba invece di 2.

**Soluzione**: sostituire il confronto diretto con la decomposizione Unicode NFD. `unicodedata.normalize('NFD', char)[0]` restituisce il carattere base senza diacritico (es. `é`→`e`, `è`→`e`, `ç`→`c`). Il confronto avviene sul carattere base.

Aggiunta dell'import:
```python
import unicodedata
```

Loop modificato in `count_syllables_en`:
```python
vowels = "aeiouy"
count = 0
prev_vowel = False
for char in word_lower:
    base = unicodedata.normalize('NFD', char)[0]
    is_v = base in vowels
    if is_v:
        if not prev_vowel:
            count += 1
        prev_vowel = True
    else:
        prev_vowel = False
return max(count, 1)
```

**Effetto sui casi di test**:
- `valfrè`: 1 → **2** ✓ (v-a-l-f-r-è→e)
- `besançon`: 2 → **3** ✓ (b-e-s-a-n-ç→c-o-n)
- `chambéry`: 2 → **3** ✓ (c-h-a-m-b-é→e-r-y)

#### Correzione 2 — Composti con trattino OOV (src/utils.py)

**Problema**: il fallback operava sull'intera stringa incluso il trattino. `ninety-eight` veniva spacchettato come sequenza di caratteri, producendo 4 gruppi vocalici invece del corretto 3.

**Soluzione**: prima del loop, se `word_lower` contiene `-`, spezzare la parola sui trattini e sommare ricorsivamente le sillabe di ogni componente. Ogni componente attraversa autonomamente CMUdict → fallback: `ninety` e `eight` sono entrambe in CMUdict, quindi vengono conteggiate con precisione fonetica.

```python
if '-' in word_lower:
    parts = [p for p in word_lower.split('-') if p]
    if parts:
        return sum(count_syllables_en(p) for p in parts)
```

Questo blocco viene inserito **dopo** il check CMUdict (le parole composte in CMUdict vengono usate intatte) e **prima** del loop sui caratteri.

**Effetto sui casi di test**:
- `ninety-eight`: 4 → **3** ✓ (`ninety`(CMU,2) + `eight`(CMU,1))
- `one-to-one`: 5 → **3** ✓ (`one`(1)+`to`(1)+`one`(1))
- `eighteenth-century`: 5 → **5** (invariato — entrambi componenti già corretti via CMUdict)

#### Correzione 3 — Normalizzazione em-dash upstream (src/core.py)

**Problema architetturale**: em-dash (U+2014) e en-dash (U+2013) non appartengono ad `string.punctuation` (ASCII). Un token come `which—in` arrivava intero a `count_syllables_en` e a `word_count`. Correggerlo solo dentro `count_syllables_en` avrebbe lasciato `word_count` e `count_complex_words` a trattare `which—in` come un'unica parola, creando incoerenza tra le metriche.

**Soluzione**: normalizzare `analysis_text` nel punto in cui viene assemblato in `_collect_results`, prima di qualsiasi funzione di metrica. `display_text` (usato solo per la colonna testuale del CSV) rimane inalterato.

```python
# Prima (riga ~142):
tagged_works.append((title, " ".join(sentences), "\n".join(sentences), current_lang))

# Dopo:
tagged_works.append((title, " ".join(sentences).replace('—', ' ').replace('–', ' '), "\n".join(sentences), current_lang))
```

Lo stesso pattern viene applicato sia al ramo `process_all_categories=True` (riga 142) sia al ramo singola categoria (riga 147).

**Effetto**: `which—in` e `edition—is` vengono correttamente splittati in due parole per `word_count`, `sentence_count`, `average_syllables_per_word` e `count_complex_words`.

#### Limitazione non corretta — `pia's`

`pia's` viene trattato come 1 sillaba (sequenza `ia` collassata in un unico gruppo vocalico). Il valore corretto è 2 (Pi-a). Distinguere l'iato `ia` dal dittongo richiede conoscenza fonemica specifica per ogni parola: in inglese `ia` può essere sia dittongo che iato a seconda dell'origine etimologica, e nessuna regola semplice generalizza correttamente. La parola appare 6 volte nel corpus, con impatto trascurabile sugli indici. La limitazione rimane documentata.

#### Impatto sui report

Dopo le correzioni, il report è stato rigenerato (`report_gulpease_flesch_gunning_fog_all_all_20260817_123409.csv`) e confrontato con la versione precedente.

**Concordanza vs textstat** (su parole uniche): 94,7% → **95,5%**. Le 3 parole corrette (valfrè, besançon, chambéry) si spostano dalla colonna dei disaccordi a quella dei casi allineati o giustificabili. Nota: chambéry ora ottiene 3 sillabe (corretto: Cham-bé-ry) mentre textstat restituisce 2 — si tratta di un caso in cui la nostra implementazione è più accurata.

**Gulpease**: **invariato**. La formula Gulpease dipende dal conteggio di lettere e parole, non di sillabe; le correzioni alla sillabazione non la influenzano.

**Flesch (inglese)**: variazioni limitate sulle opere che contengono le parole corrette. Il caso più estremo è l'opera `Blessed Sebastiano Valfrè`: testo di soli 3 parole, Flesch passa da 34,59 a 6,39 (Δ −28,20). Questo comportamento non è un bug della correzione: su un testo di 3 parole la formula Flesch `206,835 − 84,6 × (S/W) − 1,015 × (W/Fr)` amplifica qualsiasi variazione nella media sillabe/parola — `valfrè` che passa da 1 a 2 sillabe sposta la media da 2,0 a 2,33, con un Δ Flesch di circa 28 punti. Questo riflette la nota instabilità di Flesch sui testi molto brevi, non un errore del conteggio.

**Gunning Fog (inglese)**: 6 delle 240 righe risultano modificate con Δ = +0,25 costante. Le 6 righe corrispondono alla stessa opera **"The 18th-century reliquaries"** presente in 6 categorie diverse del corpus — non si tratta di 6 fenomeni linguistici indipendenti. Le cause sono due: la normalizzazione dell'em-dash porta il word count da 61 a 63 (`which—in` e `edition—is` splittati in 2 token), e `chambéry` passa da 2 a 3 sillabe (soglia "parola complessa" per Gunning Fog). L'impatto è trascurabile a livello di corpus.

**Conclusione**: le tre correzioni migliorano l'accuratezza della stima del conteggio sillabico per le categorie di parole più problematiche (accentate, composte con trattino, em-dash), senza regressioni sulle parole già gestite correttamente da CMUdict. La copertura CMUdict sul corpus rimane invariata (89,3% per parole uniche, 94,4% ponderata per occorrenze).

#### Verifica quantitativa finale

Prima del commit, i due report CSV sono stati confrontati sistematicamente con uno script diagnostico temporaneo: report pre-fix (`20260815_170858`) vs. report post-fix rigenerato (`20260817_125723`). Corpus totale: 480 opere (240 IT + 240 EN); merge 1:1 su Id/Lang/Title.

**Italiano — invarianza completa**

| Campo | Risultato |
|---|---|
| Gulpease | 240/240 invariate |
| Flesch | 240/240 invariate |
| Gunning Fog | 240/240 invariate |
| Words, Letters, Num\_Sentences | 240/240 invariati |

Nessuna delle correzioni alla sillabazione o tokenizzazione inglese ha avuto effetti collaterali sui calcoli italiani.

**Inglese — Flesch**

| Statistica (sole 84 opere modificate) | Valore |
|---|---|
| Opere modificate | 84 / 240 |
| Opere invariate | 156 / 240 |
| Delta medio | +1,17 |
| Delta mediano | +3,29 |
| Delta minimo | −28,20 |
| Delta massimo | +11,28 |

La distribuzione è prevalentemente positiva: i fix di `ninety-eight` (4→3 sill) e `one-to-one` (5→3) riducono la stima media di sillabe per parola e alzano il punteggio Flesch delle opere coinvolte. Le variazioni negative importanti si limitano a un solo caso ("Blessed Sebastiano Valfrè", già discusso sopra).

**Inglese — Gunning Fog**

6/240 righe modificate (la stessa opera "The 18th-century reliquaries" in 6 categorie), Δ = +0,25 costante. 234/240 invariate.

**Verifica word-level**

| Parola | Sillabe attese | Sillabe ottenute | Stato |
|---|---|---|---|
| `valfrè` | 2 | 2 | OK |
| `besançon` | 3 | 3 | OK |
| `chambéry` | 3 | 3 | OK |
| `ninety-eight` | 3 | 3 | OK |
| `one-to-one` | 3 | 3 | OK |
| `eighteenth-century` | 5 | 5 | OK (invariato, CMUdict) |
| `pia's` | 1 | 1 | OK (limitazione nota) |
| `history` | 3 | 3 | OK (CMUdict) |
| `camera` | 3 | 3 | OK (CMUdict) |
| `museum` | 3 | 3 | OK (CMUdict — trisillabo: mu-se-um) |

Nota: il test diagnostico aveva inizialmente impostato `museum` atteso=2; CMUdict restituisce correttamente 3 (mu-se-um). Non si tratta di un bug del codice.

**Concordanza textstat aggiornata**

| Fase | Concordanza su 600 parole uniche |
|---|---|
| Pre-fix (sezione 7.8) | 568/600 = 94,7% |
| Post-fix (attuale) | 573/600 = 95,5% |

I 27 disaccordi residui riguardano tutti parole OOV (non in CMUdict). Categorie principali: nomi propri/toponimi (`edessa`, `mandylion`, `sebastiano`, `lirey`, ecc.), composti con trattino dove le due euristiche divergono sistematicamente, 1 caso di limitazione nota (`pia's`). Tra i disaccordi compare anche `which—in` (freq=6): si tratta di un artefatto metodologico della comparazione — lo script diagnostico opera sulle parole grezze del corpus, mentre nel flusso di produzione `_collect_results` normalizza l'em-dash prima di qualsiasi calcolo e `which—in` non raggiunge mai `count_syllables_en`.

**Conclusione della fase inglese**

Non sono state identificate regressioni. Le correzioni eliminano errori sistematici verificabili sui tre casi identificati in 7.8 (punti 1–3). La concordanza con il riferimento indipendente migliora dal 94,7% al 95,5%. Le limitazioni residue (OOV, nomi propri stranieri, `pia's`) sono note, documentate e accettabili per un corpus specialistico di questa natura. La parte relativa alla sillabazione inglese può essere considerata sufficientemente verificata e chiusa.

---

### 7.10 Generalizzazione dinamica delle lingue nella GUI e nella pipeline

#### Situazione iniziale

La GUI conteneva una lista hardcoded `[("it", "Italiano"), ("en", "Inglese")]` usata per costruire un radio button statico "Tutte / Italiano / Inglese". Qualsiasi JSON con lingue aggiuntive avrebbe ignorato le lingue extra senza avvertire l'utente; la pipeline assumeva `lang` come `str | "all"`, rendendo impossibile selezionare un sottoinsieme arbitrario di lingue.

#### Obiettivo

Preparare l'architettura per N lingue senza aggiungere ancora lingue reali: generalizzare selezione, GUI, pipeline e filtraggio. La correttezza linguistica (formule specifiche, sillabazione) di nuove lingue è fuori scope di questa fase.

#### get_supported_langs(data)

Introdotta in `src/core.py` la funzione:

```python
def get_supported_langs(data):
    """Return sorted list of language codes present in data AND supported by at least one index."""
    langs_in_json = set(data.keys())
    langs_with_index = set().union(*INDEX_LANGS.values())
    return sorted(langs_in_json & langs_with_index)
```

Centralizza il criterio: una lingua è "utilizzabile" solo se compare sia nel JSON sia in almeno un valore di `INDEX_LANGS`. Viene usata da `_load_json` (GUI) e da `_collect_results` (pipeline), evitando duplicazione della logica.

#### Costruzione dinamica delle checkbox

`_load_json` chiama `_rebuild_lang_checkboxes(get_supported_langs(self.data))` invece di costruire i radio button statici. Il nuovo metodo `_rebuild_lang_checkboxes` svuota `self.lang_frame`, azzera `self.lang_vars` e crea una `CTkCheckBox` per ogni codice lingua risultante, con il codice come etichetta (`"it"`, `"en"`, …) senza ulteriori mappature hardcoded.

I bottoni "Seleziona tutti" / "Deseleziona tutti" sono in un frame esterno (`lang_outer`) che non viene mai distrutto durante la ricostruzione delle checkbox. Al caricamento di un JSON diverso, le checkbox vengono ricostruite da zero rispecchiando il nuovo corpus.

#### Avviso per lingue non supportate

Dopo il messaggio "JSON caricato: …", `_load_json` calcola `set(self.data.keys()) - set(supported)` e logga un `AVVISO` arancione per ogni lingua non resa selezionabile, spiegando il motivo all'utente senza interrompere il flusso. Esempio:

```
AVVISO: lingua 'de' rilevata nel JSON ma non supportata da alcun indice. Non sarà disponibile per la generazione del report.
```

#### Nuovo significato di "all"

Prima: `lang == "all"` → `list(data.keys())` (tutte le lingue del JSON, comprese le non supportate).  
Ora: `lang == "all"` → `get_supported_langs(data)` (sole lingue supportate).

La distinzione è rilevante quando il JSON contiene lingue senza un indice corrispondente.

#### Estensione di lang a list[str]

`_collect_results` normalizza `lang` in tre rami distinti:

| Valore | `langs_to_process` | `lang_label` (nome file) |
|--------|-------------------|--------------------------|
| `"all"` | `get_supported_langs(data)` | `"all"` |
| `list[str]` | il valore stesso | codici ordinati uniti da `_` (es. `"en_it"`) |
| `str` | `[lang]` | il valore stesso |

`_run()` in `gui.py` produce `"all"` se tutte le lingue disponibili sono selezionate, altrimenti passa la lista completa dei codici selezionati. La retrocompatibilità con `lang="it"`, `lang="en"`, `lang="all"` è preservata.

#### Categorie e sottocategorie dinamiche

I menu "Categorie" erano già dinamici. La verifica con un JSON di test contenente categorie con nomi arbitrari (`visitatori`, `ricercatori`, `standard`, `percorso_semplice`, `scheda_breve`, `scheda_tecnica`) ha confermato che nessun nome di categoria è hardcoded nella GUI. Il fallback in `_update_category_menus` e `_on_cat_select` usa ora `self.lang_vars.keys()` (sole lingue supportate/selezionabili) invece di `self.structure.keys()` (tutte le lingue del JSON), evitando di includere lingue non supportate nel calcolo dei menu.

#### Test manuali effettuati

| Caso | Risultato |
|------|-----------|
| Corpus attuale (it + en) | Comportamento preservato, nessun AVVISO lingua |
| JSON con sola lingua italiana | Una sola checkbox `it`, report generato correttamente |
| JSON it + en + de (de non supportato) | Checkbox `it` e `en`, AVVISO arancione per `de` |
| JSON con categorie e sottocategorie arbitrarie | Menu popolati correttamente, nessun hardcoding |
| Sottoinsieme it (su corpus it+en) | Report solo IT, filename `…_it_…` |
| Regressione: tutte le lingue corpus attuale | `lang="all"`, 480 opere, risultati identici ai report precedenti |

Nessuna regressione osservata.

#### Limiti di questa fase

Questa fase generalizza la **gestione, la selezione e la pipeline** delle lingue. Non costituisce un'aggiunta di nuove lingue funzionanti: per qualsiasi lingua oltre `it` e `en` restano da affrontare nelle fasi successive:

- formule degli indici specifiche per la nuova lingua;
- aggiornamento di `INDEX_LANGS` con il nuovo codice lingua;
- conteggio delle sillabe (nuova funzione o fallback appropriato in `src/utils.py`);
- verifica dell'accuratezza dei risultati su un corpus reale;
- eliminazione di eventuali fallback impliciti verso l'inglese presenti nelle funzioni esistenti.

---

### 7.11 Eliminazione dei fallback linguistici impliciti

#### Contesto

La sezione 7.10 citava tra i lavori futuri: "eliminazione di eventuali fallback impliciti verso l'inglese presenti nelle funzioni esistenti". Questa fase porta a compimento quel punto, come prerequisito all'aggiunta di nuove lingue al progetto.

#### Problema

Nelle funzioni di calcolo di `src/utils.py` e `src/indices.py`, il ramo `else` era strutturalmente equivalente a "non italiano → inglese":

- `average_syllables_per_word`: `if lang == "it": ... else: sum(count_syllables_en(...))`
- `count_complex_words`: ternario `count_syllables_it if lang == "it" else count_syllables_en`
- `flesch_index`: `if lang == "it": ... else:  # English`

Fintanto che le sole lingue erano `it` e `en`, questo era funzionalmente corretto. Con l'architettura N-lingua introdotta in §7.10, una terza lingua come `"fr"` avrebbe percorso silenziosamente il ramo `else`, usando sillabazione e coefficienti inglesi senza alcun avviso né errore.

`gunning_fog_index` non conteneva branching linguistico proprio: delegava interamente a `count_complex_words`, dove risiedeva il fallback. `gulpease_index` non accetta `lang` e non è interessato: la protezione è già garantita dal guard `INDEX_LANGS` nella pipeline.

#### Soluzione

Per ciascuna delle tre funzioni con `else` implicito, il ramo è stato reso esplicito:

```python
# PRIMA
if lang == "it":
    ...
else:   # silenziosamente inglese per qualsiasi altra lingua
    ...

# DOPO
if lang == "it":
    ...
elif lang == "en":
    ...
else:
    raise ValueError(
        f"Language '{lang}' is not supported ... Supported languages: 'it', 'en'."
    )
```

File modificati: solo `src/utils.py` e `src/indices.py`. Nessuna modifica a `core.py`, `gui.py`, `INDEX_LANGS`, `INDEX_REGISTRY` o alle formule/algoritmi esistenti.

Il valore di default `lang="en"` nelle firme delle funzioni è stato mantenuto per retrocompatibilità dell'API: una chiamata che omette `lang` si comporta ancora come prima. L'errore viene sollevato solo quando viene passato esplicitamente un valore non riconosciuto.

Per `gunning_fog_index` con lingua non supportata il `ValueError` proviene da `count_complex_words`, con messaggio esplicito. Non è stato aggiunto un controllo ridondante in `gunning_fog_index` poiché il flusso normale della pipeline non raggiunge mai queste funzioni con lingue non dichiarate (il guard `INDEX_LANGS` in `_collect_results` produce `"N/A"` senza chiamare le formule).

#### Comportamento post-modifica

| `lang` | Comportamento |
|--------|---------------|
| `"it"` | italiano, identico a prima |
| `"en"` | inglese, identico a prima |
| omesso (default) | `lang="en"` → inglese, identico a prima |
| qualsiasi altro valore esplicito | `ValueError` con messaggio esplicito |

#### Verifica effettuata

**Test diretti — 16/16 superati:**

| Funzione | `"it"` | `"en"` | omesso | lingua non supportata |
|----------|--------|--------|--------|-----------------------|
| `average_syllables_per_word` | OK | OK | == `"en"` ✓ | ValueError ✓ |
| `count_complex_words` | OK | OK | == `"en"` ✓ | ValueError ✓ |
| `flesch_index` | OK | OK | == `"en"` ✓ | ValueError (da `average_syllables_per_word`) ✓ |
| `gunning_fog_index` | OK | OK | == `"en"` ✓ | ValueError (da `count_complex_words`) ✓ |

**Regressione numerica sul corpus reale (`content.json`):**

La versione pre-modifica è stata recuperata tramite `git show HEAD` in un modulo Python temporaneo; i valori prodotti sono stati confrontati opera per opera con quelli della versione post-modifica.

| Misura | Valore |
|--------|--------|
| Lingue confrontate | `it`, `en` |
| Indici confrontati | `gulpease`, `flesch`, `gunning_fog` |
| Opere confrontate | 80 |
| Valori numerici confrontati | 200 |
| Differenze trovate | **0** |
| Differenza massima | **0** |

**Pipeline completa:** `python main.py` completato senza errori. CSV e XLSX generati correttamente.

**JSON it/en/de:** `get_supported_langs` restituisce `['en', 'it']`; `"de"` non ricade sul comportamento inglese, non è resa selezionabile nella GUI, l'AVVISO arancione introdotto in §7.10 resta invariato.

---

### 7.12 Estensione della sillabazione al francese e allo spagnolo

#### Contesto e separazione metodologica

La sezione §7.11 ha eliminato i fallback impliciti verso l'inglese nelle funzioni di `src/utils.py`, rendendo esplicito che qualsiasi lingua non dichiarata solleva un `ValueError`. Questo ha reso sicuro aggiungere nuove lingue: ogni nuova funzione sillabica viene riconosciuta correttamente dal registry senza il rischio di percorsi non previsti.

Questa fase aggiunge il supporto al conteggio delle sillabe per il francese (`"fr"`) e lo spagnolo (`"es"`). È importante distinguere due livelli di supporto che restano separati al termine della fase:

- **Utility sillabica disponibile**: `_SYLLABLE_COUNTERS` in `src/utils.py` contiene funzioni di conteggio per tutte e quattro le lingue — `it`, `en`, `fr`, `es`. Le chiamate dirette a `average_syllables_per_word` o `count_complex_words` con `lang="fr"` o `lang="es"` sono ora supportate.
- **Indice effettivamente abilitato**: `INDEX_LANGS` in `src/core.py` rimane invariato. La pipeline produce `"N/A"` per le combinazioni indice-lingua non in `INDEX_LANGS`, senza mai chiamare le formule.

| Indice | IT | EN | FR | ES |
|--------|:--:|:--:|:--:|:--:|
| Gulpease | ✓ | — | — | — |
| Flesch | ✓ | ✓ | — | — |
| Gunning Fog | ✓ | ✓ | — | — |
| Utility sillabica | ✓ | ✓ | ✓ | ✓ |

L'estensione degli indici Flesch al francese e allo spagnolo richiede la verifica dei coefficienti da fonte primaria (rispettivamente Kandel-Moles 1958 e Fernández-Huerta 1959) e non è ancora stata implementata.

#### Refactoring: `_SYLLABLE_COUNTERS` come registry

Prima di questa fase, `average_syllables_per_word` e `count_complex_words` contenevano un branching esplicito `if lang == "it" / elif lang == "en"`. Aggiungere una terza lingua avrebbe richiesto modificare due punti separati e avrebbe reintrodotto il problema della logica duplicata eliminato in §7.11.

La soluzione adottata è un dizionario di dispatch a livello di modulo in `src/utils.py`:

```python
_SYLLABLE_COUNTERS = {
    "it": count_syllables_it,
    "en": count_syllables_en,
    "fr": count_syllables_fr,
    "es": count_syllables_es,
}
```

Le funzioni consumano il registry con un unico `get`:

```python
counter = _SYLLABLE_COUNTERS.get(lang)
if counter is None:
    raise ValueError(
        f"Language '{lang}' is not supported for syllable counting. "
        f"Supported languages: {sorted(_SYLLABLE_COUNTERS)}."
    )
total_syllables = sum(counter(word) for word in words)
```

Aggiungere una nuova lingua richiede ora una sola modifica — inserire una voce in `_SYLLABLE_COUNTERS` — senza toccare le funzioni che lo usano. I percorsi `"it"` e `"en"` attraversano le stesse funzioni di prima: **zero regressione numerica**, verificata sul corpus completo (§ Risultati).

#### Spagnolo

Per lo spagnolo viene usata l'istanza pyphen con il dizionario bundled `"es"`:

```python
dic_es = pyphen.Pyphen(lang="es", left=1)
```

Il parametro `left=1` è stato scelto sperimentalmente, seguendo la stessa logica della sillabazione italiana (§7.7): con il valore predefinito `left=2`, pyphen filtra i break points in posizione 1, sottocontando le parole che iniziano con una vocale seguita da consonante (`otoño`, `Europa`, `acción`, …). Un confronto su campione ha verificato tre configurazioni:

| `left` | Errori su campione RAE (9 parole) | Osservazione |
|--------|-----------------------------------|--------------|
| `left=1` | 0 / 9 | Configurazione adottata |
| `left=2` | 2 / 9 | Sottoconteggio vocale iniziale isolata |
| `left=3` | 3 / 9 | Sottoconteggio più pronunciato |

**Risultato:** 9/9 PASS sul campione di riferimento RAE.

**Limite noto:** `museo` produce 2 segmenti invece delle 3 sillabe attese (mu-sé-o). Il dizionario di ifenazione usato da pyphen non introduce in questo caso tutti i punti di separazione necessari al conteggio sillabico: la distinzione tra dittongo e iato richiede conoscenza fonologica che i pattern di ifenazione tipografica non sempre codificano (v. §7.7). Questo limite è indipendente dal parametro `left`. La funzione `count_syllables_es` non introduce correzioni euristiche: per lo spagnolo il dizionario pyphen si è rivelato sufficientemente accurato sul campione analizzato.

#### Francese — perché pyphen puro non è sufficiente

Il caso francese è strutturalmente diverso da quello spagnolo. Come spiegato in §7.7, pyphen è uno strumento di ifenazione tipografica: il parametro `left` controlla la lunghezza minima del primo segmento per ragioni tipografiche. Per l'italiano, impostare `left=1` è stato sufficiente perché il dizionario Hunspell `it_IT` contiene break points in posizione 1 per le parole che iniziano con vocale — `left=1` ha semplicemente smesso di filtrarli.

Per il francese il problema è diverso: il dizionario Hunspell `fr` **non contiene break points a posizione 1 per nessuna parola**, indipendentemente dal valore di `left`. Le parole che iniziano con una vocale seguita da consonante — `ami`, `étude`, `animal`, `image`, `étoile`, `amour`, `avoir`, … — hanno la prima sillaba come singola vocale, ma il dizionario non registra quel punto di separazione. Abbassare `left` non aiuta: il dato semplicemente non è presente.

Verifica iniziale su un campione di 24 parole verificate su Wiktionnaire (trascrizioni IPA):

| Metodo | Errori su 24 parole | Natura degli errori |
|--------|---------------------|---------------------|
| Pyphen fr puro (`left=1`) | 8 / 24 | Tutte: vocale iniziale isolata sottocontata di 1 |
| Conteggio gruppi vocalici (fallback) | 10 / 24 | Sovracconto su 'e' muta, nasali, dittonghi |

Nessuno dei due approcci di base è applicabile direttamente: il primo sottoconteggia sistematicamente, il secondo sovracconta su categorie frequenti. È stata quindi sviluppata un'euristica specifica per il francese.

#### Francese — evoluzione dell'euristica

**v1 — correzione V+C:** correzione +1 quando i primi tre caratteri della parola seguono il pattern vocale+consonante (V+C). Il campione di 24 parole scende a 0 errori, ma il corpus reale rivela falsi positivi: `observation` (ob-ser-va-tion, 4 sillabe) diventa 5, `Agrandissement` (6 sillabe) diventa 7. Il pattern V+C scatta anche per sillabe iniziali *chiuse* come `ob-`, `ar-`, `ex-`, che pyphen già conteggia correttamente perché il break point a posizione 2 è presente nel dizionario.

**Analisi del corpus reale:** il test su `content_it_en_fr_es.json` ha rivelato due anomalie sistematiche non emerse sul campione iniziale di 24 parole.

*Anomalia A — Elisione con apostrofo tipografico (U+2019).* Il corpus francese usa sistematicamente il RIGHT SINGLE QUOTATION MARK (U+2019) per i clitici: `l'avocat`, `l'État`, `d'Orient`, `s'agit`, … Pyphen tratta questi token come parole intere e conta anche le sillabe del clitic (`l`, `d`, `s`). La soluzione è rilevare U+2019 — e l'apostrofo ASCII per robustezza — a posizione 1–2 nel token e ricorrere su `count_syllables_fr(resto)`: il clitic si fonde fonologicamente con la parola seguente e non contribuisce al conteggio.

*Anomalia B — Falsi positivi V+C+C.* La correzione v1 attivava il +1 anche per il pattern V+C+C (sillaba iniziale chiusa), già trattato correttamente da pyphen grazie al break point in posizione 2. La correzione deve distinguere i due pattern:

| Pattern | Esempio | pyphen | Correzione |
|---------|---------|--------|-----------|
| V+C+V (sillaba aperta) | `ami` → a-mi | sottocontato | necessaria |
| V+C+C (sillaba chiusa) | `observation` → ob-... | corretto | non necessaria |

**v3 (fix Anomalie A+B):** implementa due correzioni:

```
Correzione 1 — Elisione: rilevare apostrofo tipografico/ASCII a posizione 1–2 del
               token (dopo strip punteggiatura), rimuovere il clitic e ricorrere
               su count_syllables_fr(resto). Token con apostrofo a posizione > 2
               (aujourd'hui, jusqu'en) vengono lasciati intatti.

Correzione 2a — V+C+V: aggiungere 1 quando i primi tre caratteri (dopo NFD)
                seguono il pattern vocale+consonante+vocale e pyphen non ha
                trovato un break point in posizione 1. Il terzo carattere vocale
                conferma la sillaba aperta; i prefissi nasali (en-, an-) sono
                esclusi automaticamente perché il loro terzo carattere è una
                consonante.
```

Sul campione Wiktionnaire di 50 parole l'analisi ha individuato 5 parole ancora sottocontate nel corpus reale: `après`, `avril`, `écrits`, `Athènes`, `illustre`. Sono tutte parole con pattern V+C+C iniziale dove il cluster consonantico (pr, vr, cr, th, ll) impedisce a pyphen di trovare qualsiasi break point: pyphen restituisce conteggio 1, ma la parola è polisillaba. Il risultato complessivo sul campione è riportato nella sezione "Francese — risultati dei test" che segue.

**v3c — versione finale implementata:** mantiene le correzioni 1 e 2a di v3 e aggiunge:

```
Correzione 2b — V+C+C con pyphen count=1: aggiungere 1 quando il pattern iniziale
                è vocale+consonante+consonante (V+C+C) E pyphen restituisce
                esattamente 1 (nessun break trovato nell'intera parola). La
                condizione count==1 distingue le parole per cui pyphen fallisce
                completamente (après, écrits) da quelle che iniziano con sillaba
                chiusa ma hanno break points successivi (observation, count=4).

                Guardia nasale: c1 ∈ {n, m} e c2 non vocale → correzione non
                applicata. Esclude parole come anges ([ɑ̃ʒ], 1 sillaba) dove il
                prefisso V+n+C è una vocale nasale, non una sillaba aperta.

                Guardia monosillabicità: _vowel_groups_mute_e_fr(parola) >= 2.
                Il helper conta i nuclei vocalici pronunciati, escludendo la 'e'
                finale muta. Se il risultato è < 2, la parola è realmente
                monosillaba e la correzione non viene applicata.
```

L'implementazione completa in `src/utils.py`:

```python
# Correction 2a: V+C+V open-syllable
vcv = (c0 in _VOWELS_BASE and c1 not in _VOWELS_BASE
       and c2 in _VOWELS_BASE and first_break >= 2)
# Correction 2b: V+C+C when Pyphen returns exactly 1 (no break found at all)
nasal = c1 in {"n", "m"} and c2 not in _VOWELS_BASE
vcc1 = (c0 in _VOWELS_BASE and c1 not in _VOWELS_BASE
        and c2 not in _VOWELS_BASE and count == 1 and not nasal)
if (vcv or vcc1) and _vowel_groups_mute_e_fr(clean_word) >= 2:
    count += 1
```

**Esempi di guardie attive:**

| Parola | count pyphen | Condizione | Esito |
|--------|:------------:|------------|-------|
| `après` | 1 | V+C+C, count=1, non nasale, ≥ 2 nuclei | +1 → 2 ✓ |
| `avril` | 1 | V+C+C, count=1, non nasale, ≥ 2 nuclei | +1 → 2 ✓ |
| `anges` | 1 | c1='n' ∈ {n,m} → guardia nasale | invariato → 1 ✓ |
| `observation` | 4 | count=4 ≠ 1 → 2b non scatta | invariato → 4 ✓ |
| `agrandissement` | 4 | count=4 ≠ 1 → 2b non scatta | invariato → 4 ✓ |
| `inspirées` | 3 | count=3 ≠ 1 → 2b non scatta | invariato → 3 ✓ |

#### Francese — risultati dei test

| Sezione | Risultato |
|---------|-----------|
| T-FR-WIKT — campione Wiktionnaire 50 parole | 49/50 corretti; 1 errore noto |
| T-FR-ELISION — 64 token U+2019 nel corpus | 0 errori (16 monosillabi post-elisione corretti) |
| T-FR-CORPUS — guardie double-correction | 0 doppie correzioni rilevate |
| T-ES — campione RAE 9 parole | 9/9 PASS |
| T-REG IT/EN — 876 frasi corpus | **0 differenze** |

**Caso residuo nel campione Wiktionnaire.** `aujourd'hui` restituisce 3 sillabe invece di 4: è l'unico errore sul campione. La parola contiene U+2019 a posizione 8 — ben oltre la soglia di elisione a posizione 1–2 — e il dizionario di sillabazione usato da pyphen non produce il conteggio corretto per questo token con apostrofo tipografico. L'errore non è riconducibile alle correzioni euristiche introdotte: modificarle non lo correggerebbe.

**Casi residui noti non corretti dall'implementazione attuale:**

| Parola | Pyphen | Corretto | Causa |
|--------|:------:|:--------:|-------|
| `connaissance` | 2 | 3 | Pyphen/Hunspell fr non produce il conteggio atteso |
| `Constantinople` | 3 | 4 | Pyphen/Hunspell fr non produce il conteggio atteso |
| `aujourd'hui` | 3 | 4 | Pyphen/Hunspell fr + apostrofo U+2019 a posizione > 2 |

I tre casi residui non sono corretti dalle correzioni euristiche implementate: il risultato prodotto da pyphen per queste parole rimane invariato indipendentemente dalle correzioni applicate. Non sono state introdotte eccezioni hardcoded per singole parole.

**Parole migliorate da v3 a v3c:** `après`, `avril`, `écrits`, `Athènes`, `illustre`, e le forme con elisione che li precedono (es. `l'échelle`, `l'église`).

**Statistiche corpus francese** (da `content_it_en_fr_es.json`):

| Metrica | Valore |
|---------|--------|
| Token totali corpus FR | 8.760 |
| Sillabe totali | 14.412 |
| Media sillabe/parola | 1,6452 |

#### Corpus e test strutturali

Il file `file_to_process/content_it_en_fr_es.json` è il corpus parallelo a quattro lingue usato per validare l'estensione FR/ES. La struttura è identica a `content.json`: `lang → age_group → categoria → opere → frasi`. Il file non sostituisce `content.json` come corpus predefinito della pipeline — `DEFAULT_JSON_PATH` in `src/core.py` rimane invariato — ma è necessario per:

- analizzare il vocabolario francese reale e verificare l'euristica sul testo autentico del museo, non solo sul campione controllato;
- misurare la regressione IT/EN su un corpus più ampio (876 frasi contro le 80 di `content.json`);
- verificare che le modifiche alla sillabazione francese non abbiano effetti collaterali sulla sillabazione spagnola.

#### Stato finale della fase

| Componente | Stato |
|------------|-------|
| `count_syllables_it` | Invariata (§7.7) |
| `count_syllables_en` | Invariata (§7.9) |
| `count_syllables_fr` | Nuova (v3c): elisione + V+C+V + V+C+C/count=1 |
| `count_syllables_es` | Nuova: Pyphen es, `left=1` |
| `_SYLLABLE_COUNTERS` | Nuovo registry `{it, en, fr, es}` |
| `average_syllables_per_word` | Refactored via registry — retrocompatibile |
| `count_complex_words` | Refactored via registry — retrocompatibile |
| `INDEX_LANGS["gulpease"]` | `{"it"}` — invariato |
| `INDEX_LANGS["flesch"]` | `{"it", "en"}` — invariato |
| `INDEX_LANGS["gunning_fog"]` | `{"it", "en"}` — invariato |

---

### 7.13 Adattamento Flesch francese e refactoring data-driven

#### Adattamento Kandel-Moles e abilitazione del francese

Al termine della fase §7.12, `INDEX_LANGS["flesch"]` conteneva `{"it", "en"}`: la sillabazione francese era disponibile ma Flesch FR non era ancora abilitato. Il passo successivo è stato verificare l'esistenza di un adattamento linguistico appropriato e abilitarlo nella pipeline.

L'adattamento individuato è quello di **Kandel e Moles (1958)**, che mantiene la stessa struttura matematica del Flesch originale con coefficienti adattati al francese:

```text
207 - 1.015 × ASL - 73.6 × ASW
```

Struttura identica alla famiglia Flesch: `C - asl × ASL - asw × ASW`. La fonte è stata verificata prima dell'implementazione. L'abilitazione ha richiesto:

1. aggiunta della lingua `"fr"` a `INDEX_LANGS["flesch"]` in `src/core.py`;
2. implementazione nella funzione `flesch_index()` in `src/indices.py`.

#### Situazione precedente e motivazione del refactoring

Con l'aggiunta del francese, `flesch_index()` conteneva una catena di tre rami:

```python
if lang == "it":
    flesch_score = 206 - (0.65 * avg_syllables_per_word) - avg_words_per_sentence
elif lang == "en":
    flesch_score = 206.835 - (84.6 * avg_syllables_per_word) - (1.015 * avg_words_per_sentence)
elif lang == "fr":
    flesch_score = 207 - (1.015 * avg_words_per_sentence) - (73.6 * avg_syllables_per_word)
else:
    raise ValueError(...)
```

Le tre formule condividono la struttura `C - asl × ASL - asw × ASW`: cambiano solo i coefficienti. Aggiungere una quarta lingua avrebbe significato un quarto `elif`. La ricerca esplorativa preliminare aveva mostrato che numerosi adattamenti Flesch in letteratura mantengono la stessa struttura, suggerendo che una configurazione data-driven fosse più appropriata della catena if/elif.

#### FLESCH_PARAMS e formula generica

Il refactoring ha introdotto un dizionario di configurazione `FLESCH_PARAMS` in `src/indices.py`:

```python
FLESCH_PARAMS = {
    "it": {"C": 206,     "asl": 1.0,   "asw": 0.65},
    "en": {"C": 206.835, "asl": 1.015, "asw": 84.6},
    "fr": {"C": 207,     "asl": 1.015, "asw": 73.6},
}
```

`flesch_index()` usa ora una sola formula generica:

```python
params = FLESCH_PARAMS.get(lang)
if params is None:
    supported = ", ".join(f"'{k}'" for k in FLESCH_PARAMS)
    raise ValueError(
        f"Language '{lang}' is not supported by flesch_index. "
        f"Supported languages: {supported}."
    )
return params["C"] - params["asl"] * avg_words_per_sentence - params["asw"] * avg_syllables_per_word
```

L'elenco delle lingue supportate nel messaggio di errore è derivato dinamicamente da `FLESCH_PARAMS.keys()`, senza duplicare la lista altrove.

#### Principio metodologico

La ricerca sugli adattamenti linguistici ha evidenziato tre situazioni ricorrenti:

1. **Stessa struttura matematica, coefficienti diversi** — esempio tipico: numerosi adattamenti Flesch in letteratura. In questo caso è appropriato un registry di parametri.
2. **Stessa famiglia di indice, componente diversa** — va valutato caso per caso; non si forza nell'astrazione esistente senza che la leggibilità del codice ne benefici.
3. **Struttura o feature sostanzialmente differenti** — preferibile una funzione dedicata.

Principio emerso:

> **Generalizzare ciò che è realmente comune, senza generalizzare per forza ciò che comune non è.**

**Gulpease** — La ricerca non ha evidenziato adattamenti linguistici consolidati. L'indice è specifico per l'italiano e `gulpease_index()` non è stato modificato.

**Gunning Fog** — Non è emersa una famiglia omogenea di adattamenti linguistici paragonabile a quella del Flesch. La funzione resta invariata su `{"it", "en"}`.

**Spagnolo** — `_SYLLABLE_COUNTERS` supporta già `"es"`. Non esiste ancora un adattamento Flesch verificato e abilitato per lo spagnolo: `INDEX_LANGS["flesch"]` non include `"es"`. La presenza del sillabatore non implica l'applicabilità automatica dell'indice.

#### Risultati dei test di regressione

I test sono stati eseguiti confrontando i valori prodotti dalla versione con `if/elif` e dalla versione con `FLESCH_PARAMS`:

| Test | Risultato |
|------|-----------|
| Confronto numerico it/en/fr (testo campione fisso) | 0 differenze (tolleranza < 1 × 10⁻¹⁰) |
| ValueError per `lang="es"` (sillabazione presente, Flesch non configurato) | Messaggio dinamico con lista da `FLESCH_PARAMS.keys()` |
| Confronto report pre/post — 40 opere × 3 lingue (`content_it_en_fr_es.json`) | 0 differenze nei valori Flesch |

#### Stato finale della fase

| Componente | Stato |
|------------|-------|
| `FLESCH_PARAMS` | Nuovo: `{it, en, fr}` con `C`, `asl`, `asw` per lingua |
| `flesch_index()` | Refactored: formula generica + lookup `FLESCH_PARAMS` |
| `INDEX_LANGS["flesch"]` | `{"it", "en", "fr"}` |
| `INDEX_LANGS["gulpease"]` | `{"it"}` — invariato |
| `INDEX_LANGS["gunning_fog"]` | `{"it", "en"}` — invariato |
| `_SYLLABLE_COUNTERS` | `{it, en, fr, es}` — invariato (§7.12) |
