
import sys
import os
from itertools import combinations
from rouge_calculator import evaluate_summary
from rouge_calculator import MODEL_DIRECTORY
from rouge_calculator import MODEL_FILENAME
from rouge_calculator import TEXT_FILENAME_FORMAT
from rouge_calculator import GOLD_REFERENCES_DIR_FORMAT

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textcleaner import get_sentences

SUMMARY_LENGHT = 0.2
DATASET = 'summa'
OPTIMUM_FILENAME_FORMAT = 'results/opt_{text_number:02d}.txt'


def get_sentences_from_text(text_number):
    text_filename = TEXT_FILENAME_FORMAT.format(dataset=DATASET, text_number=text_number)
    with open(text_filename) as fp:
        text = fp.read()
    return list(get_sentences(text))


def get_score_for_summay(text_number, summary):
    with open(os.path.join(MODEL_DIRECTORY, MODEL_FILENAME), 'w') as fp:
        fp.write(summary)

    gold_references_dir = GOLD_REFERENCES_DIR_FORMAT.format(dataset=DATASET, text_number=text_number)
    return evaluate_summary(gold_references_dir)


def get_optimum_summary(text_number):
    """ Creates the best possible summary of a set length trying
    all posible combinations.
    """

    # Temporary stores the best results so far.
    best_summary = None
    best_score = 0

    sentences = get_sentences_from_text(text_number)
    summary_lenght = int(len(sentences) * SUMMARY_LENGHT)

    # Creates a summary for each combination of sentences.
    for combination in combinations(sentences, summary_lenght):
        summary = "\n".join(combination)
        result = get_score_for_summay(text_number, summary)

        # We consider the average of several scores.
        score = (result['rouge_1_f_score'] + result['rouge_2_f_score'] + result['rouge_su*_f_score']) / 3

        if score > best_score:
            best_score = score
            best_summary = summary

        print "summary with score", score, ". best score so far:", best_score
        print ""
        print ""
        print ""

    # The optimum summary is written to hard disk.
    output_filename = OPTIMUM_FILENAME_FORMAT.format(text_number=text_number)
    with open(output_filename, 'w') as fp:
        fp.write(best_summary)


get_optimum_summary(1)