import argparse
import sys
import os
from method_evaluator import MethodEvaluator
from rouge_results_writer import export_results

from baseline import baseline

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textrank import textrank


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--documents", metavar='N', type=str, nargs='+',
                    help="specify dataset text numbers to summarize.")
parser.add_argument("-d", "--dataset", help="specify which dataset to use.")
parser.add_argument("-b", "--baseline", action="store_true", help="calculates the baselines scores.")
args = parser.parse_args()

# Use elhadad dataset by default.
if args.dataset:
    dataset = args.dataset
else:
    dataset = 'elhadad'

# Calculate all rouge scores by default.
if args.documents:
    documents = [document for document in args.documents]
else:
    documents = None

# Don't calculate baseline method by default.
if args.baseline:
    method = baseline
else:
    method = textrank

evaluator = MethodEvaluator(dataset, method, documents)
results = evaluator.get_rouge_scores()
export_results(dataset, results, 'baseline' if args.baseline else 'textrank')
