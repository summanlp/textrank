import os.path
import sys
import csv
import rouge_calculator
import traceback
from timeout import TimeoutError, timeout

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textrank import textrank

TEMP_DIRECTORY = rouge_calculator.MODEL_DIRECTORY
TEMP_FILENAME = rouge_calculator.MODEL_FILENAME
RESULTS_DIRECTORY = 'results'


@timeout(10)
def summarize_text(filename):
    # pyrouge needs the model summaries to be stored in a directory without subdirectories.
    if not os.path.exists(TEMP_DIRECTORY):
        os.makedirs(TEMP_DIRECTORY)

    # Makes a summary of the provided file and stores it in the temp folder.
    with open(filename) as fp:
        text = fp.read()

    print "Summarizing " + filename
    summary = textrank(text)

    with open(os.path.join(TEMP_DIRECTORY, TEMP_FILENAME), 'w') as fp:
        fp.write(summary)


def get_rouge_summary_for_text(text_number):
    text_filename = 'datasets/elhadad/{text_number:02d}/text.txt'.format(text_number=text_number)
    gold_references_dir = 'datasets/elhadad/{text_number:02d}'.format(text_number=text_number)
    summarize_text(text_filename)
    return rouge_calculator.evaluate_summary(gold_references_dir, 'summ(\d+).txt')


def get_rouge_scores(dataset_numbers):
    results = {'runs': 0, 'successes': 0, 'timeouts': 0, 'errors': 0, 'reports': []}

    for i in dataset_numbers:
        print "Evaluating set #" + str(i)

        results['runs'] += 1
        try:
            result = get_rouge_summary_for_text(i)
        except TimeoutError:
            print "Timeout summarizing text #%d\n" % i
            results['timeouts'] += 1
            continue
        except Exception as e:
            print "Error summarizing text #%d\n" % i
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            results['errors'] += 1
            continue

        print "Text #%d summarized successfully\n" % i
        results['successes'] += 1
        results['reports'].append(result)

    return results


def export_results(results):
    successes = float(results['successes'])

    print "Successful tests: " + str(results['successes'])
    print "Failed tests: " + str(results['errors'])
    print "Timed out tests: " + str(results['timeouts'])

    if successes == 0:
        return

    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    avg_rouge1_fscore = sum(result['rouge_1_f_score'] for result in results['reports']) / successes
    print "Average F-score for ROUGE-1 metric: " + str(avg_rouge1_fscore)
    avg_rouge2_fscore = sum(result['rouge_2_f_score'] for result in results['reports']) / successes
    print "Average F-score for ROUGE-2 metric: " + str(avg_rouge2_fscore)
    avg_su_fscore = sum(result['rouge_su*_f_score'] for result in results['reports']) / successes
    print "Average F-score for ROUGE-SU metric: " + str(avg_su_fscore)

    # Export ROUGE measures on successes.
    with open(os.path.join(RESULTS_DIRECTORY, 'avg_rouge1_fscore.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AVG ROUGE-1 F-measure'])
        csv_writer.writerow([str(avg_rouge1_fscore)])

    with open(os.path.join(RESULTS_DIRECTORY, 'avg_rouge2_fscore.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AVG ROUGE-2 F-measure'])
        csv_writer.writerow([str(avg_rouge2_fscore)])

    with open(os.path.join(RESULTS_DIRECTORY, 'avg_su_fscore.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AVG ROUGE-SU F-measure'])
        csv_writer.writerow([str(avg_su_fscore)])

    # Exports overall results.
    with open(os.path.join(RESULTS_DIRECTORY, 'textrank_successes.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Successes'])
        csv_writer.writerow([str(results['successes'])])

    with open(os.path.join(RESULTS_DIRECTORY, 'textrank_failures.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Failures'])
        csv_writer.writerow([str(results['errors'])])

    with open(os.path.join(RESULTS_DIRECTORY, 'textrank_timeouts.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timeouts'])
        csv_writer.writerow([str(results['timeouts'])])


if __name__ == '__main__':
    # Calculate all rouge scores if no argument is provided.
    if len(sys.argv) == 1:
        results = get_rouge_scores(xrange(1, 25))

    # Else calculate rouge scores for the specified datasets.
    else:
        results = get_rouge_scores([int(x) for x in sys.argv[1:]])

    export_results(results)
