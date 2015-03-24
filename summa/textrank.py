
import sys, getopt
from textrank_sentence import textrank_by_sentence
from textrank_word import textrank_by_word

TEST_FILE = "samples/textrank_example.txt"
# Types of summarization
SENTENCE = 0
WORD = 1


def get_arguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:l:h", ["text=", "summary=", "length=", "help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    path = TEST_FILE
    summarize_by = SENTENCE
    length = 0.2
    for o, a in opts:
        if o in ("-t", "--text"):
            path = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--summary"):
            summarize_by = int(a)
        elif o in ("-l", "--length"):
            length = float(a)
        else:
            assert False, "unhandled option"

    return path, summarize_by, length


help_text = """Usage: python summa.py
-s UNIT, --summary=UNIT:
\tType of unit to summarize: sentence or word. Default value: 0
\t0: Sentence. 1: Word
-t PATH, --text=PATH:
\tPATH to text to summarize. Default value: samples/textrank_example.txt
-l LENGTH, --length=LENGTH:
\tFloat number (0,1] that defines the length of the summary. It's a proportion of the original text. Default value: 0.2
-h, --help:
\tprints this help
"""
def usage():
    print help_text


def textrank(text, summarize_by=SENTENCE, summary_length=0.2):
    if summarize_by == SENTENCE:
        return textrank_by_sentence(text, summary_length)
    else:
        return textrank_by_word(text, summary_length)


def main():
    path, summarize_by, length = get_arguments()

    with open(path) as test_file:
        text = test_file.read()

    print textrank(text, summarize_by, length)


if __name__ == "__main__":
    main()
