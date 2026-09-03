import re
import string
import unicodedata
import pyphen
import cmudict
# ----------------------------
# Utility functions for readability metrics
# ----------------------------

def word_count(text):
    """Return the number of words in the text."""
    return len(text.split())

def sentence_count(text):
    """
    Refined sentence counting function for readability indices (e.g., Gulpease).
    
    This function counts the number of sentences in a text with more accuracy
    than a naive approach. It follows these rules:
    
    1. Only '.', '!', and '?' count as valid sentence-ending punctuation.
    2. Consecutive sentence-ending punctuation marks are treated as a single sentence.
       Example: 'Cosa?!' counts as 1 sentence.
    3. Common abbreviations (Sig., Dott., Prof., Dr., Avv., Ing., Cav.) are not counted 
       as sentence endings.
    4. Ellipses '...' are treated as a single sentence-ending marker.
    5. Texts without punctuation but with words are counted as 1 sentence.
    
    Parameters:
    -----------
    text : str
        The input text to analyze.

    Returns:
    --------
    int
        The number of sentences detected in the text.
    """

    # List of common Italian abbreviations to ignore
    abbreviations = [
        r'\bSig\.', r'\bDott\.', r'\bProf\.', r'\bDr\.', r'\bAvv\.', r'\bIng\.', r'\bCav\.'
    ]
    
    # Temporarily remove abbreviations to avoid counting their dots as sentence-ending
    temp_text = text
    for abbr in abbreviations:
        temp_text = re.sub(abbr, '', temp_text, flags=re.IGNORECASE)

    # Replace ellipses '...' with a single marker to count as one sentence
    temp_text = re.sub(r'\.\.\.', '.', temp_text)

    # Match sequences of sentence-ending punctuation marks (., !, ?)
    sentence_endings = re.findall(r'[.!?]+', temp_text)

    # If no punctuation but there are words, consider it as one sentence
    if len(sentence_endings) == 0 and len(temp_text.split()) > 0:
        return 1

    return len(sentence_endings)

def letter_count(text):
    """Return the number of alphabetic characters (letters) in the text."""
    return sum(1 for char in text if char.isalpha())

dic_it = pyphen.Pyphen(lang="it_IT", left=1)
dic_fr = pyphen.Pyphen(lang="fr", left=1, right=1)
dic_es = pyphen.Pyphen(lang="es", left=1)

_VOWELS_BASE = set("aeiouy")
_FR_ELISION_CHARS = frozenset("’‘'")  # U+2019 RIGHT SINGLE QUOTATION MARK (corpus fr), ASCII apostrophe

def count_syllables_it(word):
    """Count syllables for Italian using Pyphen's built-in it_IT dictionary with left=1."""
    clean_word = word.strip(string.punctuation + "“”‘’")
    if not clean_word:
        return 1
    syllables = dic_it.inserted(clean_word).split("-")
    return max(len(syllables), 1)

cmu_dict = cmudict.dict()

def count_syllables_en(word):
    """Count syllables for English using CMUdict"""
    clean_word = word.strip(string.punctuation + "“”‘’")
    if not clean_word:
        return 1
    word_lower = clean_word.lower()
    if word_lower in cmu_dict:
        # Count vowels in the first pronunciation variant
        return len([ph for ph in cmu_dict[word_lower][0] if ph[-1].isdigit()])
    else:
        # Hyphenated compounds: sum syllables of each component
        if '-' in word_lower:
            parts = [p for p in word_lower.split('-') if p]
            if parts:
                return sum(count_syllables_en(p) for p in parts)
        # Fallback: vowel-group counting with Unicode NFD for accented vowels
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

def _vowel_groups_mute_e_fr(word):
    """Count pronounced vowel nuclei in a French word, excluding mute final unaccented 'e'."""
    clean = word.lower()
    mute_idx = None
    if len(clean) >= 2 and clean[-1] == 'e':
        if unicodedata.normalize("NFD", clean[-2])[0] not in _VOWELS_BASE:
            mute_idx = len(clean) - 1
    count, prev_v = 0, False
    for i, c in enumerate(clean):
        if i == mute_idx:
            prev_v = False
            continue
        b = unicodedata.normalize("NFD", c)[0]
        is_v = b in _VOWELS_BASE
        if is_v and not prev_v:
            count += 1
        prev_v = is_v
    return count

def count_syllables_fr(word):
    """Count syllables for French using Pyphen fr + two corrections.

    Correction 1 — Elision (U+2019): clitic tokens like l’avocat use
    the typographic apostrophe at position 1-2.  Count syllables of the
    remainder since the clitic merges phonologically with the following word.
    Tokens with the apostrophe further in (aujourd’hui, jusqu’en)
    are left intact.

    Correction 2 — Isolated open initial syllable (V+C+V pattern): Pyphen fr
    has no position-1 break points, undercounting ‘ami’ (2), ‘etude’ (2),
    ‘animal’ (3).  One syllable is added only when the pattern is V+C+V (open
    initial syllable), not V+C+C (closed syllable like ‘ob’ in ‘observation’,
    which Pyphen already counts correctly).  Nasal prefixes (‘en-’, ‘an-’) are
    excluded automatically because their third character is a consonant.
    """
    clean_word = word.strip(string.punctuation + "“”‘’")
    if not clean_word:
        return 1
    # Correction 1: French elision — strip clitic at position 1-2 and recurse
    for i, c in enumerate(clean_word):
        if c in _FR_ELISION_CHARS and 0 < i <= 2 and i < len(clean_word) - 1:
            remainder = clean_word[i + 1:]
            return count_syllables_fr(remainder) if remainder else 1
    count = max(len(dic_fr.inserted(clean_word).split("-")), 1)
    if len(clean_word) < 3:
        return count
    positions = dic_fr.positions(clean_word)
    first_break = positions[0] if positions else len(clean_word)
    c0 = unicodedata.normalize("NFD", clean_word[0].lower())[0]
    c1 = unicodedata.normalize("NFD", clean_word[1].lower())[0]
    c2 = unicodedata.normalize("NFD", clean_word[2].lower())[0]
    # Correction 2a: V+C+V open-syllable — Pyphen fr lacks position-1 breaks
    vcv = (c0 in _VOWELS_BASE and c1 not in _VOWELS_BASE
           and c2 in _VOWELS_BASE and first_break >= 2)
    # Correction 2b: V+C+C when Pyphen returns exactly 1 (no break found at all)
    # Covers clusters like V+pr, V+cr, V+vr, V+th, V+ll where the initial vowel
    # is an isolated syllable but the consonant cluster blocks Pyphen's lookup.
    # Nasal prefix guard (V+n/m+C) prevents overcounting for words like 'anges'.
    nasal = c1 in {"n", "m"} and c2 not in _VOWELS_BASE
    vcc1 = (c0 in _VOWELS_BASE and c1 not in _VOWELS_BASE
            and c2 not in _VOWELS_BASE and count == 1 and not nasal)
    if (vcv or vcc1) and _vowel_groups_mute_e_fr(clean_word) >= 2:
        count += 1
    return count

def count_syllables_es(word):
    """Count syllables for Spanish using Pyphen es with left=1."""
    clean_word = word.strip(string.punctuation + "“”‘’")
    if not clean_word:
        return 1
    return max(len(dic_es.inserted(clean_word).split("-")), 1)

_SYLLABLE_COUNTERS = {
    "it": count_syllables_it,
    "en": count_syllables_en,
    "fr": count_syllables_fr,
    "es": count_syllables_es,
}


def average_words_per_sentence(text):
    """
    Calculate the average number of words per sentence in the given text.

    Uses the existing word_count and sentence_count functions.
    Returns None if there are no sentences to avoid division by zero.
    """
    n_words = word_count(text)
    n_sentences = sentence_count(text)
    if n_sentences == 0:
        return None
    return n_words / n_sentences

def average_syllables_per_word(text, lang="en"):
    """
    Calculate the average number of syllables per word in the given text.

    Uses the existing word_count function and counts syllables for each word,
    using the syllable counter appropriate for the given language.
    Returns None if there are no words to avoid division by zero.
    """
    words = text.split()
    n_words = word_count(text)
    if n_words == 0:
        return None
    counter = _SYLLABLE_COUNTERS.get(lang)
    if counter is None:
        raise ValueError(
            f"Language '{lang}' is not supported for syllable counting. "
            f"Supported languages: {sorted(_SYLLABLE_COUNTERS)}."
        )
    total_syllables = sum(counter(word) for word in words)
    return total_syllables / n_words

def count_complex_words(text, lang="en"):
    """
    Return the count of words with 3 or more syllables, excluding proper nouns.

    A word is treated as a proper noun (and excluded from the count) if it
    starts with a capital letter and is not the first word of its sentence,
    per the Gunning Fog "complex word" definition.
    """
    syllable_counter = _SYLLABLE_COUNTERS.get(lang)
    if syllable_counter is None:
        raise ValueError(
            f"Language '{lang}' is not supported for complex word counting. "
            f"Supported languages: {sorted(_SYLLABLE_COUNTERS)}."
        )
    complex_count = 0
    for sentence in re.split(r'[.!?]+', text):
        for i, word in enumerate(sentence.split()):
            stripped = word.strip(string.punctuation + "“”‘’")
            if not stripped:
                continue
            if i > 0 and stripped[0].isupper():
                continue  # treat as proper noun
            if syllable_counter(word) >= 3:
                complex_count += 1
    return complex_count

# ----------------------------
# JSON utility
# ----------------------------

def extract_sentences(obj):
    """
    Recursively extract all strings (sentences) from a nested JSON-like structure.
    Returns a flat list of strings.
    """
    sentences = []
    if isinstance(obj, dict):
        for value in obj.values():
            sentences.extend(extract_sentences(value))
    elif isinstance(obj, list):
        for item in obj:
            sentences.extend(extract_sentences(item))
    elif isinstance(obj, str):
        sentences.append(obj)
    return sentences

def extract_works(obj, current_title=None):
    """
    Recursively walk a nested JSON-like structure and group sentences by
    the nearest enclosing dict key (the artifact/"opera" title).
    Returns a list of (title, [sentences]) tuples.
    """
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
