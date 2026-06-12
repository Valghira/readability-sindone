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

## 4. Evoluzione degli script

### 4.1 Prima versione: testo come stringa diretta (versione originale)

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

### 4.2 Versione intermedia con lettura da JSON (versione originale)

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

### 4.3 Problemi riscontrati con il conteggio delle frasi e introduzione della funzione `refined_sentence_count`

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

### 4.4 Nuova versione aggiornata con `refined_sentence_count` e report CSV (versione evoluta)

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

### 4.5 Commenti generali sulle versioni e l'evoluzione

- Le funzioni sono modulari e facilmente estendibili.
- La logica attuale considera una frase come sequenza terminata da `.`, `!`, `?`, ma la nuova funzione `refined_sentence_count` migliora questa definizione con regole più accurate.
- Il sistema può essere facilmente adattato per limitare il numero di frasi analizzate, utile in vista di una futura interfaccia GUI.
- È pronto per estendere l'analisi anche ad altri indici di leggibilità come Flesch o Gunning Fog.
- La conservazione delle versioni precedenti nel documento permette di tracciare l'evoluzione metodologica e di giustificare le scelte tecniche nel lavoro di tesi.
