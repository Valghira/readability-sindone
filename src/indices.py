from src import utils

# ----------------------------
# Readability indexes
# ----------------------------

def gulpease_index(text):
    """
    Calculate the Gulpease index for a given text.
    Formula: 89 + (300 * sentences - 10 * letters) / words
    Returns None if the text contains no words.
    """
    n_sentences = utils.sentence_count(text)
    n_letters = utils.letter_count(text)
    n_words = utils.word_count(text)

    if n_words == 0:
        return None

    sentence_score = 300 * n_sentences
    letter_penalty = 10 * n_letters

    result = 89 + ((sentence_score - letter_penalty) / n_words)
    return result

def flesch_index(text, lang="en"):
    """
    Compute the Flesch readability index based on the language of the text.

    Parameters:
    -----------
    text : str
        Input text to analyze.
    lang : str
        'it' for Italian, 'en' for English.

    Returns:
    --------
    float
        Readability index according to Flesch formula.
    """
    words = utils.word_count(text)
    sentences = utils.sentence_count(text)
    if sentences == 0 or words == 0:
        return None  # Avoid division by zero
    
    avg_words_per_sentence = words / sentences

    # Count syllables for each word depending on language
    if lang == "it":
        syllables = sum(utils.count_syllables_it(w) for w in text.split())
        avg_syllables_per_word = syllables / words
        flesch_score = 206 - (0.65 * avg_words_per_sentence) - (0.75 * avg_syllables_per_word)
    else:  # English
        syllables = sum(utils.count_syllables_en(w) for w in text.split())
        avg_syllables_per_word = syllables / words
        flesch_score = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word

    return flesch_score

def gunning_fog_index(text, lang="en"):
    """
    Compute the Gunning Fog index.
    Formula: 0.4 * [(words/sentences) + 100 * (complex_words/words)]
    Complex words are words with 3 or more syllables.
    Returns None if text has no words or sentences.
    """
    words = utils.word_count(text)
    sentences = utils.sentence_count(text)
    if words == 0 or sentences == 0:
        return None
    complex_words = utils.count_complex_words(text, lang)
    score = 0.4 * ((words / sentences) + 100 * (complex_words / words))
    return score
