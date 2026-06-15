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


