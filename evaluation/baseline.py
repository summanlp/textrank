import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
import textcleaner  # Uses textrank's method for extracting sentences.

BASELINE_WORD_COUNT = 100


def baseline(text):
    """ Creates a baseline summary to be used as reference.
    The baseline is set to an extract of the first 100 words.
    """
    sentences = list(textcleaner.get_sentences(text))

    baseline_summary = ""
    word_count = 0
    for sentence in sentences:
        for word in sentence.split():
            baseline_summary += word + " "
            word_count += 1

            if word_count == BASELINE_WORD_COUNT:
                return baseline_summary

        baseline_summary += "\n"

    return baseline_summary