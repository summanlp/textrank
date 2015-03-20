
from rouge_dataset_results import RougeDatasetResults
import rouge_calculator
from evaluation_constants import *
from timeout import TimeoutError, timeout
from utils import get_directories_from_path
from tempfile import mkdtemp
from shutil import rmtree
from shutil import copyfile
import os
import traceback
import sys
import re

""" Class that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
    Crated to decouple the single summary calculator.
"""


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
    def summarize_text(self, document, output_directory):
        input_filename = os.path.join(self.dataset_directory, document, TEXT_FILENAME)

        # Makes a summary of the provided file and stores it in the temp folder.
        with open(input_filename) as fp:
            text = fp.read()

        print "Summarizing " + document
        summary = self.method(text)

        output_filename = SYSTEM_SUMMARIES_FORMAT.format(text_id=document)
        with open(os.path.join(output_directory, output_filename), 'w') as fp:
            fp.write(summary)

    def prepare_model_summaries(self, document, model_directory):
        """ Copies all files that matches the model regex into the selected directory.
        """
        model_source = os.path.join(self.dataset_directory, document)

        summaries_filename_pattern = re.compile(SUMMARIES_FILE_PATTERN)
        summary_id = 0
        for file in os.listdir(model_source):
            if not summaries_filename_pattern.match(file):
                continue

            dest_filename = MODEL_SUMMARIES_FORMAT.format(model_id=document,
                                                          text_id=chr(65 + summary_id))
            file_dest_path = os.path.join(model_directory, dest_filename)
            file_source_path = os.path.join(model_source, file)

            if summaries_filename_pattern.match(file):
                copyfile(file_source_path, file_dest_path)

            summary_id += 1

    def get_rouge_scores(self):
        results = RougeDatasetResults()

        for document in self.documents:
            print "Evaluating set {document}.".format(document=document)

            system_directory = mkdtemp()
            model_directory = mkdtemp()

            try:
                # Gets the summary using the method.
                self.summarize_text(document, system_directory)

                # And prepares the model files.
                self.prepare_model_summaries(document, model_directory)

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

            result = rouge_calculator.evaluate_summary(model_directory, system_directory)

            print "Text", document, "summarized successfully.\n"
            results.add_success(result)

            # Removes the temporal directory and all its files.
            rmtree(system_directory)
            rmtree(model_directory)

        return results
