import os
import os.path
from tempfile import mkdtemp
from shutil import rmtree
from evaluation_constants import MODEL_SUMMARIES_PATTERN, SYSTEM_SUMMARIES_PATTERN
from pyrouge import Rouge155

""" Class that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
"""

ROUGE_PATH = os.path.join(os.getcwd(), 'ROUGE-RELEASE-1.5.5')
ROUGE_DATA_PATH = os.path.join(ROUGE_PATH, 'data')
SYSTEM_DIR = "system"
MODEL_DIR = "model"
CONFIG_FILENAME = "config.xml"


# Rouge options as used in the DUC2007 competition:
# http://www-nlpir.nist.gov/projects/duc/duc2007/tasks.html#main
ROUGE_OPTIONS = [
    '-e', ROUGE_DATA_PATH,  # Specify ROUGE_EVAL_HOME directory where the ROUGE data files can be found.
    '-n', '2',              # Compute ROUGE-1 and ROUGE-2.
    '-x',                   # Do not calculate ROUGE-L.
    '-m',                   # Apply Porter stemmer on both models and peers.
    '-2', '4',              # Compute skip bigram (ROGUE-S) co-occurrence with a maximum skip distance of 4,
    '-u',                   # Include unigram in Skip Bigram (ROUGE-S).
    '-c', '95',             # Specify CF\% (0 <= CF <= 100) confidence interval to compute.
    '-r', '1000',           # Specify the number of sampling point in bootstrap resampling (default is 1000).
    '-f', 'A',              # Scores are averaged over multiple models.
    '-p', '0.5',            # Compute F-measure with alpha = 0.5.
    '-t', '0',              # Use model unit as the counting unit.
    '-a'                    # Evaluate all systems.
    '-l', '100'             # Only use the first 100 words.
]


def create_temporary_directories():
    tempdir = mkdtemp()

    # Creates the temp directories to hold the rouge files.
    new_system_dir = os.path.join(tempdir, SYSTEM_DIR)
    os.mkdir(new_system_dir)
    new_model_dir = os.path.join(tempdir, MODEL_DIR)
    os.mkdir(new_model_dir)

    return tempdir


def evaluate_summary(model_directory, system_directory):
    tempdir = create_temporary_directories()

    rouge_instance = Rouge155(ROUGE_PATH, verbose=True, rouge_args=' '.join(ROUGE_OPTIONS))

    # Converts the gold references files to rouge format.
    model_input_dir = model_directory
    model_output_dir = os.path.join(tempdir, MODEL_DIR)
    rouge_instance.convert_summaries_to_rouge_format(model_input_dir, model_output_dir)

    # Converts the summary file to rouge format.
    system_output_dir = os.path.join(tempdir, SYSTEM_DIR)
    rouge_instance.convert_summaries_to_rouge_format(system_directory, system_output_dir)

    # Writes the configuration file.
    config_filename = os.path.join(tempdir, CONFIG_FILENAME)
    rouge_instance.write_config_static(system_output_dir, SYSTEM_SUMMARIES_PATTERN,
                                       model_output_dir, MODEL_SUMMARIES_PATTERN,
                                       config_filename, 1)

    # Runs ROUGE comparing the gold reference summaries with the recently generated.
    output = rouge_instance.evaluate_static(ROUGE_PATH, config_filename, ROUGE_OPTIONS)

    # Removes the temporal directories.
    rmtree(tempdir)

    print "ROUGE output:", output

    return rouge_instance.output_to_dict(output)
