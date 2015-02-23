
from rouge_dataset_results import RougeDatasetResults
import rouge_calculator
from evaluation_constants import DATASET_DIRECTORY_FORMAT
from evaluation_constants import TEXT_FILENAME
from timeout import TimeoutError, timeout
from utils import get_directories_from_path
from tempfile import mkdtemp
from shutil import rmtree
import os
import traceback
import sys

""" Class that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
    Crated to decouple the single summary calculator.
"""

MODEL_FILENAME = 'temp.txt'


class MethodEvaluator(object):

    def __init__(self, dataset, method, documents=None):
        self.dataset = dataset
        self.dataset_directory = DATASET_DIRECTORY_FORMAT.format(dataset=dataset)
        self.method = method

        if documents is not None:
            self.documents = documents
        else:
            # Reads all the files in the directory.
            self.documents = get_directories_from_path(self.dataset_directory)

    @timeout(10)
    def summarize_text(self, text_filename, output_directory):
        # Makes a summary of the provided file and stores it in the temp folder.
        with open(text_filename) as fp:
            text = fp.read()

        print "Summarizing " + text_filename
        summary = self.method(text)

        with open(os.path.join(output_directory, MODEL_FILENAME), 'w') as fp:
            fp.write(summary)

    def get_rouge_scores(self):
        results = RougeDatasetResults()

        for document in self.documents:
            print "Evaluating set {document}.".format(document=document)

            # Gets the summary using the method.
            try:
                model_directory = mkdtemp()
                text_filename = os.path.join(self.dataset_directory, document, TEXT_FILENAME)
                self.summarize_text(text_filename, model_directory)

            except TimeoutError:
                print "Timeout summarizing text {document}.\n".format(document=document)
                results.add_timeout()
                continue

            except Exception as e:
                print "Error summarizing text {document}.\n".format(document=document)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

                results.add_error()
                continue

            system_directory = os.path.join(self.dataset_directory, document)
            result = rouge_calculator.evaluate_summary(system_directory, model_directory, MODEL_FILENAME)

            print "Text", document, "summarized successfully.\n"
            results.add_success(result)

            # Removes the temporal directory and all its files.
            rmtree(model_directory)

        return results
