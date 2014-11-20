import os
import os.path
import sys
from pyrouge import Rouge155

# Needed to import files from a parent folder.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from textrank.textrank import textrank


""" Script that runs ROUGE to compare the output of a custom summarization tool
    comparing it to a 'gold standard' reference summary.
"""

# Initializes ROUGE.
ROUGE_PATH = os.path.join(os.getcwd(), 'ROUGE-RELEASE-1.5.5')
rouge_instance = Rouge155(ROUGE_PATH)

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

print rouge_instance.convert_and_evaluate()
