
import sys, getopt
from textrank_sentence import textrank_by_sentence, PAGERANK_MANUAL
from textrank_word import textrank_by_word

TEST_FILE = "samples/textrank_example.txt"
# Types of summarization
SENTENCE = 0
WORD = 1


def get_arguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:m:s:l:h", ["text=", "method=", "summary=", "length=", "help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    path = TEST_FILE
    method = PAGERANK_MANUAL
    summarize_by = SENTENCE
    length = 0.2
    for o, a in opts:
        if o in ("-t", "--text"):
            path = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--method"):
            method = int(a)
        elif o in ("-s", "--summary"):
            summarize_by = int(a)
        elif o in ("-l", "--length"):
            length = float(a)
        else:
            assert False, "unhandled option"

    return method, path, summarize_by, length


help_text = """Usage: python textrank.py
-t PATH, --text=PATH:
\tPATH to text to summarize. Default value: samples/textrank_example.txt
-m METHOD, --method=METHOD:
\tMETHOD to use: Default value: 0
\t0: PageRank Manual. 1: PageRank using scipy.linalg.eig
-s UNIT, --summary=UNIT:
\tType of unit to summarize: sentence or word. Default value: 0
\t0: Sentence. 1: Word
-l LENGTH, --length=LENGTH:
\tFloat number (0,1] that defines the length of the summary. It's a proportion of the original text. Default value: 0.2
-h, --help:
\tprints this help
"""
def usage():
    print help_text


def textrank(text, summarize_by=SENTENCE, method=PAGERANK_MANUAL, summary_length=0.2):
    if summarize_by == SENTENCE:
        return textrank_by_sentence(text, method, summary_length)
    else:
        return textrank_by_word(text, method, summary_length)


def main():
    method, path, summarize_by, length = get_arguments()

    with open(path) as test_file:
        text = test_file.read()

    print textrank(text, summarize_by, method, length)


if __name__ == "__main__":
    main()
