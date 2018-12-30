import os, sys
import argparse


from .summarizer import summarize
from .keywords import keywords

# Types of summarization
SENTENCE = 0
WORD = 1

DEFAULT_RATIO = 0.2


def textrank(text, summarize_by=SENTENCE, ratio=DEFAULT_RATIO, words=None, additional_stopwords=None):
    if summarize_by == SENTENCE:
        return summarize(text, ratio, words, additional_stopwords=additional_stopwords)
    else:
        return keywords(text, ratio, words, additional_stopwords=additional_stopwords)


def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("{} not in range [0.0, 1.0]".format(x))
    return x


def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="textrank", description="Extract the most relevant sentences or keywords of a given text using the TextRank algorithm.")
    parser.add_argument('--text', '-t', type=str, required=True, help="Text to summarize")
    parser.add_argument('--summary', '-s', type=int, default=0, help="Type of unit to summarize: sentence (0) or word (1)")
    parser.add_argument('--ratio', '-r', type=restricted_float, default=DEFAULT_RATIO, help="Float number (0,1] that defines the length of the summary. It's a proportion of the original text")
    parser.add_argument('--words', '-w', type=int, help="Number to limit the length of the summary. The length option is ignored if the word limit is set.")
    parser.add_argument('--additional_stopwords', '-a', help="Either a string of comma separated stopwords or a path to a file which has comma separated stopwords in every line")
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    with open(args.text) as file:
        text = file.read()

    additional_stopwords = None
    if args.additional_stopwords:
        if os.path.exists(args.additional_stopwords):
            with open(args.additional_stopwords) as f:
                additional_stopwords = {s for l in f for s in l.strip().split(",")}
        else:
            additional_stopwords = args.additional_stopwords.split(",")

    print(textrank(text, args.summary, args.ratio, args.words, additional_stopwords))


if __name__ == "__main__":
    main()
