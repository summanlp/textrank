import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
import textcleaner  # Uses textrank's method for extracting sentences.

SUMMARY_LENGHT = 0.2


def baseline(text):
    """ Creates a baseline summary to be used as reference.
    """
    sentences = list(textcleaner.get_sentences(text))
    summary_sentences = int(SUMMARY_LENGHT * len(sentences))
    return " ".join(sentences[:summary_sentences])