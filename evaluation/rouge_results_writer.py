import os
import os.path
import csv

RESULTS_DIRECTORY_FORMAT = 'results_{dataset}'


def export_results(dataset, results):
    successes = float(results.successes)

    print "Successful tests: " + str(results.successes)
    print "Failed tests: " + str(results.errors)
    print "Timed out tests: " + str(results.timeouts)

    if successes == 0:
        return

    results_directory = RESULTS_DIRECTORY_FORMAT.format(dataset=dataset)

    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    avg_rouge1_fscore = sum(result['rouge_1_f_score'] for result in results.reports) / successes
    print "Average F-score for ROUGE-1 metric: " + str(avg_rouge1_fscore)
    avg_rouge2_fscore = sum(result['rouge_2_f_score'] for result in results.reports) / successes
    print "Average F-score for ROUGE-2 metric: " + str(avg_rouge2_fscore)
    avg_su_fscore = sum(result['rouge_su*_f_score'] for result in results.reports) / successes
    print "Average F-score for ROUGE-SU metric: " + str(avg_su_fscore)

    # Export ROUGE measures on successes.
    with open(os.path.join(results_directory, 'avg_rouge1_fscore.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AVG ROUGE-1 F-measure'])
        csv_writer.writerow([str(avg_rouge1_fscore)])

    with open(os.path.join(results_directory, 'avg_rouge2_fscore.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AVG ROUGE-2 F-measure'])
        csv_writer.writerow([str(avg_rouge2_fscore)])

    with open(os.path.join(results_directory, 'avg_su_fscore.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AVG ROUGE-SU F-measure'])
        csv_writer.writerow([str(avg_su_fscore)])

    # Exports overall results.
    with open(os.path.join(results_directory, 'textrank_successes.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Successes'])
        csv_writer.writerow([str(results.successes)])

    with open(os.path.join(results_directory, 'textrank_failures.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Failures'])
        csv_writer.writerow([str(results.errors)])

    with open(os.path.join(results_directory, 'textrank_timeouts.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timeouts'])
        csv_writer.writerow([str(results.timeouts)])
