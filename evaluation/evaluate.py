import argparse
from rouge_calculator import RougeCalculator
from rouge_results_writer import export_results

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--text_numbers", metavar='N', type=int, nargs='+',
                    help="specify dataset text numbers to summarize.")
parser.add_argument("-d", "--dataset", help="specify which dataset to use.")
args = parser.parse_args()

# Calculate all rouge scores if no argument is provided.
if args.text_numbers:
    text_numbers = [int(x) for x in args.text_numbers]
else:
    text_numbers = xrange(1, 25)

# Use elhadad dataset by default.
if args.dataset:
    dataset = args.dataset
else:
    dataset = 'elhadad'


calculator = RougeCalculator(dataset, text_numbers)
results = calculator.get_rouge_scores()
export_results(dataset, results)
