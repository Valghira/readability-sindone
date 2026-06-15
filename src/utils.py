import re
import pyphen
import cmudict
from pathlib import Path
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

# pyphen dictionaries

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ITALIAN_HYPHEN_DICT_PATH = PROJECT_ROOT / "dictionaries" / "hyph_it_IT.dic"

if ITALIAN_HYPHEN_DICT_PATH.exists():
    dic_it = pyphen.Pyphen(filename=str(ITALIAN_HYPHEN_DICT_PATH))
else:
    dic_it = pyphen.Pyphen(lang="it_IT")

def count_syllables_it(word):
    """Count syllables for Italian using custom LibreOffice dictionary"""
    syllables = dic_it.inserted(word).split("-")
    return max(len(syllables), 1)

cmu_dict = cmudict.dict()

def count_syllables_en(word):

    """Count syllables for English using CMUdict"""

    word_lower = word.lower()

    if word_lower in cmu_dict:

        # Count vowels in the first pronunciation variant

        return len([ph for ph in cmu_dict[word_lower][0] if ph[-1].isdigit()])

    else:

        # fallback: count vowel groups as approximate syllables

        vowels = "aeiouy"

        count = 0

        prev_vowel = False

        for char in word_lower:

            if char in vowels:

                if not prev_vowel:

                    count += 1

                prev_vowel = True

            else:

                prev_vowel = False

        return max(count, 1)
    
## DEBUG
if __name__ == "__main__":
    print(count_syllables_en("syllable"))  # Should return 3
    print(count_syllables_it("parallelepipedo")) # Should return 7
## DEBUG
# ----------------------------
# Readability indexes
# ----------------------------

def gulpease_index(text):
    """
    Calculate the Gulpease index for a given text.
    Formula: 89 + (300 * sentences - 10 * letters) / words
    Returns None if the text contains no words.
    """
    n_sentences = sentence_count(text)
    n_letters = letter_count(text)
    n_words = word_count(text)

    if n_words == 0:
        return None

    sentence_score = 300 * n_sentences
    letter_penalty = 10 * n_letters

    result = 89 + ((sentence_score - letter_penalty) / n_words)
    return result

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
