

from sentence_splitter import sentence_split

SAMPLE_TEXT_1 = "samples/1.txt"
NLTK_OUTPUT_1 = "samples/1_split.txt"
SAMPLE_TEXT_2 = "samples/2.txt"
NLTK_OUTPUT_2 = "samples/2_split.txt"

''' Tests the sentence_splitter function by comparing a sample result
    with the output of the sentence_tokenize function in NLTK.
'''


def compare_sentences_lists(output_list, nltk_list):
    total_sentences = len(nltk_list)
    sentences_hit = 0
    for line in nltk_list:
        if line in output_list:
            sentences_hit += 1

    return float(sentences_hit) / float(total_sentences)


def compare(sample_text_file_name, nltk_output_file_name):
    with open(sample_text_file_name) as text_fp:
        sample_text = text_fp.read()

    output = sentence_split(sample_text)

    with open(nltk_output_file_name) as nltk_output_fp:
        return compare_sentences_lists(output, nltk_output_fp.readlines())


def run_tests():
    rush_acc = compare(SAMPLE_TEXT_1, NLTK_OUTPUT_1)
    print "Sample text Rush: {acc}".format(acc=rush_acc)

    argentina_acc = compare(SAMPLE_TEXT_2, NLTK_OUTPUT_2)
    print "Sample text Argentina: {acc}".format(acc=argentina_acc)


run_tests()