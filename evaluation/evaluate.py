import argparse
import sys
import os
from rouge_calculator import RougeCalculator
from rouge_results_writer import export_results

from baseline import baseline

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textrank import textrank


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--text_numbers", metavar='N', type=int, nargs='+',
                    help="specify dataset text numbers to summarize.")
parser.add_argument("-d", "--dataset", help="specify which dataset to use.")
parser.add_argument("-b", "--baseline", action="store_true", help="calculates the baselines scores.")
args = parser.parse_args()

# Use elhadad dataset by default.
if args.dataset:
    dataset = args.dataset
else:
    dataset = 'elhadad'

dataset_path = os.path.join('datasets', dataset)

# Calculate all rouge scores by default.
if args.text_numbers:
    text_numbers = [int(n) for n in args.text_numbers]
else:
    text_numbers = sorted(int(n) for n in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, n)))

# Don't calculate baseline method by default.
if args.baseline:
    method = baseline
else:
    method = textrank

calculator = RougeCalculator(dataset, text_numbers, method)
results = calculator.get_rouge_scores()
export_results(dataset, results, 'baseline' if args.baseline else 'textrank')
