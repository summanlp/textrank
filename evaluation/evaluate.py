import os.path
import sys
from pprint import PrettyPrinter
import rouge_calculator
from timeout import TimeoutError, timeout

# Imports files from a parent directory.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'textrank'))
from textrank import textrank

TEMP_DIRECTORY = rouge_calculator.MODEL_DIRECTORY
TEMP_FILENAME = rouge_calculator.MODEL_FILENAME

RESULTS = {'runs': 0, 'successes': 0, 'timeouts': 0, 'errors': 0, 'reports': []}

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


for i in range(1, 25):
    print "Evaluating set #" + str(i)

    RESULTS['runs'] += 1

    text_filename = 'datasets/elhadad/{text_number:02d}/text.txt'.format(text_number=i)
    gold_references_dir = 'datasets/elhadad/{text_number:02d}'.format(text_number=i)

    try:
        summarize_text(text_filename)
    except TimeoutError:
        print "Timeout summarizing text #" + str(i)
        RESULTS['timeouts'] += 1
        continue
    except:
        print "Error summarizing text #" + str(i)
        RESULTS['errors'] += 1
        continue

    print "Text #%d summarized successfully" % i
    RESULTS['successes'] += 1

    result = rouge_calculator.evaluate_summary(gold_references_dir, 'summ(\d+).txt')
    RESULTS['reports'].append(result)

successes = float(RESULTS['successes'])

avg_rouge1_fscore = sum(result['rouge_1_f_score'] for result in RESULTS['reports']) / successes
print "Average F-score for ROUGE-1 metric: " + str(avg_rouge1_fscore)

avg_rouge2_fscore = sum(result['rouge_2_f_score'] for result in RESULTS['reports']) / successes
print "Average F-score for ROUGE-2 metric: " + str(avg_rouge2_fscore)

avg_su_fscore = sum(result['rouge_su*_f_score'] for result in RESULTS['reports']) / successes
print "Average F-score for ROUGE-SU metric: " + str(avg_su_fscore)
