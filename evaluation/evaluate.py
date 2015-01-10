import os.path
import sys
from pprint import PrettyPrinter
import rouge_calculator

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textrank import textrank

TEMP_DIRECTORY = rouge_calculator.MODEL_DIRECTORY
TEMP_FILENAME = rouge_calculator.MODEL_FILENAME


def summarize_text(filename):
    # pyrouge needs the model summaries to be stored in a directory without subdirectories.
    if not os.path.exists(TEMP_DIRECTORY):
        os.makedirs(TEMP_DIRECTORY)

    # Makes a summary of the provided file and stores it in the temp folder.
    with open(filename) as fp:
        text = fp.read()
    summary = textrank(text)
    with open(os.path.join(TEMP_DIRECTORY, TEMP_FILENAME), 'w') as fp:
        fp.write(summary)


text_filename = 'datasets/elhadad/{text_number:02d}/text.txt'.format(text_number=6)
gold_references_dir = 'datasets/elhadad/{text_number:02d}'.format(text_number=6)

summarize_text(text_filename)
result = rouge_calculator.evaluate_summary(gold_references_dir, 'summ(\d+).txt')

pp = PrettyPrinter(indent=4)
pp.pprint(result)