import os
import os.path
from evaluation_constants import GOLD_REFERENCES_DIR_FORMAT
from evaluation_constants import GOLD_REFERENCES_PATTERN
from pyrouge import Rouge155

""" Class that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
"""

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


def evaluate_summary(text_number, dataset, model_directory, model_filename):
    rouge_instance = Rouge155(ROUGE_PATH, ' '.join(ROUGE_OPTIONS))

    gold_references_dir = GOLD_REFERENCES_DIR_FORMAT.format(dataset=dataset, text_number=text_number)

    # Runs ROUGE comparing the gold reference summaries with the recently generated.
    rouge_instance.system_dir = gold_references_dir
    rouge_instance.system_filename_pattern = GOLD_REFERENCES_PATTERN
    rouge_instance.model_dir = model_directory
    rouge_instance.model_filename_pattern = model_filename

    output = rouge_instance.convert_and_evaluate()

    return rouge_instance.output_to_dict(output)
