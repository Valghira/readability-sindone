import re

# ----------------------------
# Utility functions for readability metrics
# ----------------------------

def word_count(text):
    """Return the number of words in the text."""
    return len(text.split())

import re

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