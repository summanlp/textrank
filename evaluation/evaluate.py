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

# Rouge directories:
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

rouge_instance = Rouge155(ROUGE_PATH, ' '.join(ROUGE_OPTIONS))

# pyrouge needs the model summaries to be stored in a directory without subdirectories.
if not os.path.exists('temp'):
    os.makedirs('temp')

# Makes a summary of the provided file and stores it in the temp folder.
with open('datasets/elhadad/06/text.txt') as fp:
    text = fp.read()
summary = textrank(text)
with open('temp/temp.txt', 'w') as fp:
    fp.write(summary)

# Runs ROUGE comparing the gold reference summaries with the recently generated.
rouge_instance.system_dir = 'datasets/elhadad/06'
rouge_instance.system_filename_pattern = 'summ(\d+).txt'
rouge_instance.model_dir = 'temp'
rouge_instance.model_filename_pattern = 'temp.txt'

output = rouge_instance.convert_and_evaluate()

pp = PrettyPrinter(indent=4)
pp.pprint(rouge_instance.output_to_dict(output))
