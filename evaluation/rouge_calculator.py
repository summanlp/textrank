import os
import os.path
import sys
import traceback
from timeout import TimeoutError, timeout
from rouge_dataset_results import RougeDatasetResults
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

    def __init__(self, dataset, text_numbers, method):
        self.dataset = dataset
        self.text_numbers = text_numbers
        self.method = method

    def get_rouge_evaluation_for_text(self, text_number):
        text_filename = TEXT_FILENAME_FORMAT.format(dataset=self.dataset, text_number=text_number)
        gold_references_dir = GOLD_REFERENCES_DIR_FORMAT.format(dataset=self.dataset, text_number=text_number)
        self.summarize_text(text_filename)
        return evaluate_summary(gold_references_dir)

    @timeout(10)
    def summarize_text(self, filename):
        # pyrouge needs the model summaries to be stored in a directory without subdirectories.
        if not os.path.exists(MODEL_DIRECTORY):
            os.makedirs(MODEL_DIRECTORY)

        # Makes a summary of the provided file and stores it in the temp folder.
        with open(filename) as fp:
            text = fp.read()

        print "Summarizing " + filename
        summary = self.method(text)

        with open(os.path.join(MODEL_DIRECTORY, MODEL_FILENAME), 'w') as fp:
            fp.write(summary)

    def get_rouge_scores(self):
        results = RougeDatasetResults()

        for i in self.text_numbers:
            print "Evaluating set #" + str(i)

            try:
                result = self.get_rouge_evaluation_for_text(i)

            except TimeoutError:
                print "Timeout summarizing text #%d\n" % i
                results.add_timeout()
                continue

            except Exception as e:
                print "Error summarizing text #%d\n" % i
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

                results.add_error()
                continue

            print "Text #%d summarized successfully\n" % i
            results.add_success(result)

        return results


def evaluate_summary(gold_references_dir):
    rouge_instance = Rouge155(ROUGE_PATH, ' '.join(ROUGE_OPTIONS))

    # Runs ROUGE comparing the gold reference summaries with the recently generated.
    rouge_instance.system_dir = gold_references_dir
    rouge_instance.system_filename_pattern = GOLD_REFERENCES_PATTERN
    rouge_instance.model_dir = MODEL_DIRECTORY
    rouge_instance.model_filename_pattern = MODEL_FILENAME

    output = rouge_instance.convert_and_evaluate()

    return rouge_instance.output_to_dict(output)


