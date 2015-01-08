import os
import os.path
import sys
from pprint import PrettyPrinter
from pyrouge import Rouge155

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textrank import textrank


""" Script that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
"""

TEMP_DIRECTORY = 'temp'
TEMP_FILENAME = 'temp.txt'
ROUGE_PATH = os.path.join(os.getcwd(), 'ROUGE-RELEASE-1.5.5')
ROUGE_DATA_PATH = os.path.join(ROUGE_PATH, 'data')

ROUGE_OPTIONS = [
    '-e', ROUGE_DATA_PATH,  # Specify ROUGE_EVAL_HOME directory where the ROUGE data files can be found.
    '-c', '95',             # Specify CF\% (0 <= CF <= 100) confidence interval to compute.
    '-2',                   # Compute skip bigram (ROGUE-S) co-occurrence,
    '-1',
    '-U',                   # Compute skip bigram as -2 but include unigram.
    '-r', '1000',           # Specify the number of sampling point in bootstrap resampling (default is 1000).
    '-n', '2',              # Compute ROUGE-N up to max-ngram length will be computed.
    '-a',                   # Evaluate all systems specified in the ROUGE-eval-config-file.
    '-x'                    # Do not calculate ROUGE-L.
]


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


def evaluate_summary(gold_references_dir, gold_references_pattern):
    rouge_instance = Rouge155(ROUGE_PATH, ' '.join(ROUGE_OPTIONS))

    # Runs ROUGE comparing the gold reference summaries with the recently generated.
    rouge_instance.system_dir = gold_references_dir
    rouge_instance.system_filename_pattern = gold_references_pattern
    rouge_instance.model_dir = TEMP_DIRECTORY
    rouge_instance.model_filename_pattern = TEMP_FILENAME

    output = rouge_instance.convert_and_evaluate()

    pp = PrettyPrinter(indent=4)
    pp.pprint(rouge_instance.output_to_dict(output))


summarize_text('datasets/elhadad/06/text.txt')
evaluate_summary('datasets/elhadad/06', 'summ(\d+).txt')