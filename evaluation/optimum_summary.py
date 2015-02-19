
import sys
import os
import pyrouge
from itertools import combinations
from tempfile import mkdtemp

# TODO: Well, there's definitely room for improvement over here...
from rouge_calculator import MODEL_DIRECTORY
from rouge_calculator import MODEL_FILENAME
from rouge_calculator import TEXT_FILENAME_FORMAT
from rouge_calculator import GOLD_REFERENCES_DIR_FORMAT
from rouge_calculator import GOLD_REFERENCES_PATTERN
from rouge_calculator import ROUGE_PATH
from rouge_calculator import ROUGE_OPTIONS

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textcleaner import get_sentences


SUMMARY_LENGHT = 0.2
DATASET = 'summa'
OPTIMUM_FILENAME_FORMAT = 'results/opt_{text_number:02d}.txt'
TEMPDIR = mkdtemp()
CONFIG_FILENAME = "rouge_conf.xml"
SYSTEM_DIR = "system"
MODEL_DIR = "model"

rouge_instance = pyrouge.Rouge155(ROUGE_PATH, ' '.join(ROUGE_OPTIONS))


def get_sentences_from_text(text_number):
    text_filename = TEXT_FILENAME_FORMAT.format(dataset=DATASET, text_number=text_number)
    with open(text_filename) as fp:
        text = fp.read()
    return list(get_sentences(text))


def create_system_configuration_files(text_number):
    gold_references_dir = GOLD_REFERENCES_DIR_FORMAT.format(dataset=DATASET, text_number=text_number)
    rouge_instance.convert_summaries_to_rouge_format(gold_references_dir, os.path.join(TEMPDIR, SYSTEM_DIR))


def get_score_for_summary(summary):
    with open(os.path.join(MODEL_DIRECTORY, MODEL_FILENAME), 'w') as fp:
        fp.write(summary)

    # Creates the configuration files for the model summaries.
    rouge_instance.convert_summaries_to_rouge_format(MODEL_DIRECTORY, os.path.join(TEMPDIR, MODEL_DIR))

    rouge_instance.write_config_static(os.path.join(TEMPDIR, SYSTEM_DIR), GOLD_REFERENCES_PATTERN,
                                os.path.join(TEMPDIR, MODEL_DIR), MODEL_FILENAME,
                                os.path.join(TEMPDIR, CONFIG_FILENAME), 1)

    output = rouge_instance.evaluate_static(ROUGE_PATH, os.path.join(TEMPDIR, CONFIG_FILENAME), ROUGE_OPTIONS)
    return rouge_instance.output_to_dict(output)


def create_temporary_directories():
    new_system_dir = os.path.join(TEMPDIR, SYSTEM_DIR)
    os.mkdir(new_system_dir)
    new_model_dir = os.path.join(TEMPDIR, MODEL_DIR)
    os.mkdir(new_model_dir)


def get_optimum_summary(text_number):
    """ Creates the best possible summary of a set length trying
    all posible combinations.
    """
    create_temporary_directories()
    create_system_configuration_files(text_number)

    # Temporary stores the best results so far.
    best_summary = None
    best_score = 0

    sentences = get_sentences_from_text(text_number)
    summary_lenght = int(len(sentences) * SUMMARY_LENGHT)

    # Creates a summary for each combination of sentences.
    for combination in combinations(sentences, summary_lenght):
        summary = "\n".join(combination)
        result = get_score_for_summary(summary)

        # We consider the average of several scores.
        score = (result['rouge_1_f_score'] + result['rouge_2_f_score'] + result['rouge_su*_f_score']) / 3

        if score > best_score:
            best_score = score
            best_summary = summary

        print "summary with score", score, ". best score so far:", best_score

    # The optimum summary is written to hard disk.
    output_filename = OPTIMUM_FILENAME_FORMAT.format(text_number=text_number)
    with open(output_filename, 'w') as fp:
        fp.write(best_summary)


get_optimum_summary(1)