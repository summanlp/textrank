import sys, getopt, os

from .summarizer import summarize
from .keywords import keywords

# Types of summarization
SENTENCE = 0
WORD = 1


def exit_with_error(err):
    print("Error: " + str(err))
    usage()
    sys.exit(2)

def get_arguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:r:w:a:h", ["text=", "summary=", "ratio=", "words=", "additional_stopwords=", "help"])
    except getopt.GetoptError as err:
        exit_with_error(err)

    path = None
    summarize_by = SENTENCE
    ratio = 0.2
    words = None
    additional_stopwords = None
    for o, a in opts:
        if o in ("-t", "--text"):
            path = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--summary"):
            summarize_by = int(a)
        elif o in ("-w", "--words"):
            words = int(a)
        elif o in ("-r", "--ratio"):
            ratio = float(a)
        elif o in ("-a", "--additional_stopwords"):
            additional_stopwords = a
        else:
            assert False, "unhandled option"

    if path is None:
        exit_with_error("-t option is required.")

    return path, summarize_by, ratio, words, additional_stopwords


help_text = """Usage: textrank -t FILE
-s UNIT, --summary=UNIT:
\tType of unit to summarize: sentence (0) or word (1). Default value: 0
\t0: Sentence. 1: Word
-t FILE, --text=FILE:
\tPATH to text to summarize
-r RATIO, --ratio=RATIO:
\tFloat number (0,1] that defines the length of the summary. It's a proportion of the original text. Default value: 0.2.
-w WORDS, --words=WORDS:
\tNumber to limit the length of the summary. The length option is ignored if the word limit is set.
-a, --additional_stopwords
\tEither a string of comma separated stopwords or a path to a file which has comma separated stopwords in every line
-h, --help:
\tprints this help
"""
def usage():
    print(help_text)


def textrank(text, summarize_by=SENTENCE, ratio=0.2, words=None, additional_stopwords=None):
    if summarize_by == SENTENCE:
        return summarize(text, ratio, words, additional_stopwords=additional_stopwords)
    else:
        return keywords(text, ratio, words, additional_stopwords=additional_stopwords)


def main():
    path, summarize_by, ratio, words, additional_stopwords = get_arguments()

    with open(path) as file:
        text = file.read()

    if additional_stopwords:
        if os.path.exists(additional_stopwords):
            with open(additional_stopwords) as f:
                additional_stopwords = { s for l in f for s in l.strip().split(",") }
        else:
            additional_stopwords = additional_stopwords.split(",")

    print(textrank(text, summarize_by, ratio, words, additional_stopwords))


if __name__ == "__main__":
    main()
