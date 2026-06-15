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

def flesch_kincaid_index(text):
    """
    Calculate the Flesch-Kincaid index for a given text.
    Formula: 206.835 - (1.015 * average_words_per_sentence) - (84.6 * average_syllables_per_word)
    Returns None if the text contains no words or sentences.
    """
    avg_words_per_sentence = utils.average_words_per_sentence(text)
    avg_syllables_per_word = utils.average_syllables_per_word(text)

    if avg_words_per_sentence is None or avg_syllables_per_word is None:
        return None

    result = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
    return result
    
