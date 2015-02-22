import os
import os.path
import sys

from pyrouge import Rouge155

""" Class that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
"""

GOLD_REFERENCES_DIR_FORMAT = 'datasets/{dataset}/{text_number:02d}'
TEXT_FILENAME_FORMAT = 'datasets/{dataset}/{text_number:02d}/text.txt'
GOLD_REFERENCES_PATTERN = 'summ(\d+).txt'

MODEL_DIRECTORY = 'temp'
MODEL_FILENAME = 'temp.txt'
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


class RougeCalculator(object):

    def get_rouge_evaluation_for_text(self, text_number):
        text_filename = TEXT_FILENAME_FORMAT.format(dataset=self.dataset, text_number=text_number)
        gold_references_dir = GOLD_REFERENCES_DIR_FORMAT.format(dataset=self.dataset, text_number=text_number)
        self.summarize_text(text_filename)
        return evaluate_summary(gold_references_dir)






def evaluate_summary(gold_references_dir):
    rouge_instance = Rouge155(ROUGE_PATH, ' '.join(ROUGE_OPTIONS))

    # Runs ROUGE comparing the gold reference summaries with the recently generated.
    rouge_instance.system_dir = gold_references_dir
    rouge_instance.system_filename_pattern = GOLD_REFERENCES_PATTERN
    rouge_instance.model_dir = MODEL_DIRECTORY
    rouge_instance.model_filename_pattern = MODEL_FILENAME

    output = rouge_instance.convert_and_evaluate()

    return rouge_instance.output_to_dict(output)


