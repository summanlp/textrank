
import sys
import os
from itertools import combinations
from rouge_calculator import MODEL_DIRECTORY
from rouge_calculator import MODEL_FILENAME
from rouge_calculator import TEXT_FILENAME_FORMAT
from rouge_calculator import GOLD_REFERENCES_DIR_FORMAT

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textcleaner import get_sentences

SUMMARY_LENGHT = 0.2
DATASET = 'summa'


def get_sentences_from_text(text_number):
    text_filename = TEXT_FILENAME_FORMAT.format(dataset=DATASET, text_number=text_number)
    with open(text_filename) as fp:
        text = fp.read()
    return list(get_sentences(text))


def get_optimum_summary(text_number):
    """ Creates the best possible summary of a set length trying
    all posible combinations.
    """

    # Temporary stores the best results so far.
    best_sentences = None
    best_scores = None

    sentences = get_sentences_from_text(text_number)
    summary_lenght = int(len(sentences) * SUMMARY_LENGHT)
    # Creates a summary for each combination of sentences.
    for combination in combinations(sentences, summary_lenght):
        #print combination
        pass

    # gold_references_dir = GOLD_REFERENCES_DIR_FORMAT.format(dataset=DATASET, text_number=text_number)


get_optimum_summary(1)