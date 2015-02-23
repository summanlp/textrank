import os
import os.path
from tempfile import mkdtemp
from shutil import rmtree
from evaluation_constants import GOLD_REFERENCES_PATTERN
from pyrouge import Rouge155

""" Class that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
"""

ROUGE_PATH = os.path.join(os.getcwd(), 'ROUGE-RELEASE-1.5.5')
ROUGE_DATA_PATH = os.path.join(ROUGE_PATH, 'data')
SYSTEM_DIR = "system"
MODEL_DIR = "model"
CONFIG_FILENAME = "config.xml"

ROUGE_OPTIONS = [
    '-e', ROUGE_DATA_PATH, # Specify ROUGE_EVAL_HOME directory where the ROUGE data files can be found.
    '-c', '95', # Specify CF\% (0 <= CF <= 100) confidence interval to compute.
    '-2', # Compute skip bigram (ROGUE-S) co-occurrence,
    '-1',
    '-U', # Compute skip bigram as -2 but include unigram.
    '-r', '1000', # Specify the number of sampling point in bootstrap resampling (default is 1000).
    '-n', '2', # Compute ROUGE-N up to max-ngram length will be computed.
    '-a', # Evaluate all systems specified in the ROUGE-eval-config-file.
    '-x' # Do not calculate ROUGE-L.
]


def create_temporary_directories():
    tempdir = mkdtemp()

    # Creates the temp directories to hold the rouge files.
    new_system_dir = os.path.join(tempdir, SYSTEM_DIR)
    os.mkdir(new_system_dir)
    new_model_dir = os.path.join(tempdir, MODEL_DIR)
    os.mkdir(new_model_dir)

    return tempdir


def evaluate_summary(system_directory, model_directory, model_filename):
    tempdir = create_temporary_directories()

    rouge_instance = Rouge155(ROUGE_PATH, verbose=False, rouge_args=' '.join(ROUGE_OPTIONS))

    # Converts the gold references files to rouge format.
    gold_references_input_dir = system_directory
    gold_references_output_dir = os.path.join(tempdir, SYSTEM_DIR)
    rouge_instance.convert_summaries_to_rouge_format(gold_references_input_dir, gold_references_output_dir)

    # Converts the summary file to rouge format.
    model_directory_output_dir = os.path.join(tempdir, MODEL_DIR)
    rouge_instance.convert_summaries_to_rouge_format(model_directory, model_directory_output_dir)

    # Writes the configuration file.
    config_filename = os.path.join(tempdir, CONFIG_FILENAME)
    rouge_instance.write_config_static(gold_references_output_dir, GOLD_REFERENCES_PATTERN,
                                       model_directory_output_dir, model_filename,
                                       config_filename, 1)

    # Runs ROUGE comparing the gold reference summaries with the recently generated.
    output = rouge_instance.evaluate_static(ROUGE_PATH, config_filename, ROUGE_OPTIONS)

    # Removes the temporal directories.
    rmtree(tempdir)

    return rouge_instance.output_to_dict(output)
