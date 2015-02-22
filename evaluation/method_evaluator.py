
from rouge_dataset_results import RougeDatasetResults
import rouge_calculator
from evaluation_constants import TEXT_FILENAME_FORMAT
from timeout import TimeoutError, timeout
import os
import traceback
import sys

""" Class that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
    Crated to decouple the single summary calculator.
"""

MODEL_DIRECTORY = 'temp'
MODEL_FILENAME = 'temp.txt'


class MethodEvaluator(object):

    def __init__(self, dataset, text_numbers, method):
        self.dataset = dataset
        self.text_numbers = text_numbers
        self.method = method

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

            # Gets the summary using the method.
            try:
                text_filename = TEXT_FILENAME_FORMAT.format(dataset=self.dataset, text_number=i)
                self.summarize_text(text_filename)

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

            result = rouge_calculator.evaluate_summary(i, self.dataset, MODEL_DIRECTORY, MODEL_FILENAME)

            print "Text #%d summarized successfully\n" % i
            results.add_success(result)

        return results
