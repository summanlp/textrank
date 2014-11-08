
from nltk.tokenize import sent_tokenize
import nltk.data
from sentence_splitter import split_into_sentences
import textcleaner as tc
import os
import os.path

SAMPLES_DIRECTORY = "samples"
DEBUG = True


def compare_sentences(output_list_1, output_list_2):
    total_sentences = len(output_list_1)
    sentences_hit = 0

    for line in output_list_1:
        if line in output_list_2:
            sentences_hit += 1
        else:
            if DEBUG:
                print "Line not found on source #2:", line

    return float(sentences_hit) / float(total_sentences)


def compare(sample_text_file_name):
    """
    Given the filename of a sample text, extracts its sentences using two
    different methods.
    Returns the proportion between the mathes of both methods and the number of
    sentences of the first.
    """
    output_1 = nltk_tokenize(sample_text_file_name)
    output_2 = my_tokenize(sample_text_file_name)

    return compare_sentences(output_1, output_2)


def nltk_tokenize(file):
    sample_text = nltk.data.load(file)
    output_1 = sent_tokenize(sample_text)
    return [sentence.encode('utf8') for sentence in output_1]


def my_tokenize(file):
    with open(file) as text_fp:
        sample_text = text_fp.read()

    return split_into_sentences(sample_text)


def tokenize2(file):
    with open(file) as text_fp:
        sample_text = text_fp.read()

    return tc.get_tokenized_sentences(sample_text)


def compare2(sample_text_file_name):
    output_1 = nltk_tokenize(sample_text_file_name)
    output_2 = tokenize2(sample_text_file_name)

    return compare_sentences(output_1, output_2)


def run_tests():
    """ Tests the sentence_splitter function by comparing a sample result
    with the output of the sentence_tokenize function in NLTK.
    """
    for filename in os.listdir(SAMPLES_DIRECTORY):
        filepath = os.path.join(SAMPLES_DIRECTORY, filename)
        accuracy = compare(filepath)
        print "Accuracy for simple method: '{filename}': {acc}".format(filename=filename, acc=accuracy)
        accuracy2 = compare2(filepath)
        print "Accuracy for improved method: '{filename}': {acc}".format(filename=filename, acc=accuracy2)
        print


run_tests()