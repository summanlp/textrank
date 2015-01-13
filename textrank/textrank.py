
from pygraph.classes.digraph import digraph as pydigraph
from pagerank_weighted import pagerank_weighted as pagerank
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy
from textcleaner import tokenize_by_sentences
from math import log10


SUMMARY_LENGTH = 0.2
TEST_FILE = "samples/textrank_example.txt"
DEBUG = False
PAGERANK_MANUAL = 0
PAGERANK_SCIPY = 1


def textrank(text, method=PAGERANK_MANUAL):
    # Gets a dict of processed_sentence -> original_sentences
    tokens = tokenize_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = get_graph(tokens.keys())
    set_graph_edge_weights(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of sentence -> score
    scores = pagerank(graph) if method == PAGERANK_MANUAL else pagerank_scipy(graph)

    # Extracts the most important tokens.
    extracted_tokens = extract_tokens(graph.nodes(), scores)

    # Sorts the extracted sentences by apparition order in the original text.
    summary = sort_by_apparition(extracted_tokens, tokens, text)
    
    return "\n".join(summary)


def sort_by_apparition(extracted_tokens, tokens, text):
    summary = []

    for extracted in extracted_tokens:
        original_sentence = tokens[extracted]
        try:
            index = text.index(original_sentence)
            if DEBUG:
                summary.append((original_sentence, index, extracted_tokens[extracted]))
            else:
                summary.append((original_sentence, index))

        except ValueError:
            print "ERROR: sentence not found: " + original_sentence

    summary.sort(key=lambda t: t[1])
    if DEBUG:
        debug_info = lambda item: "({0:.4f}) : {1}".format(item[2], item[0])
        return [debug_info(item) for item in summary]
    return [item[0] for item in summary]


def extract_tokens(sentences, scores):
    sentences.sort(key=lambda s: scores[s], reverse=True)
    length = len(sentences) * SUMMARY_LENGTH
    return {sentences[i]: scores[sentences[i]] for i in range(int(length))}


def get_graph(sentences):
    graph = pydigraph()

    # Creates the graph.
    for sentence in sentences:
        graph.add_node(sentence)

    return graph


def set_graph_edge_weights(graph):
    for sentence_1 in graph.nodes():
        for sentence_2 in graph.nodes():
            if sentence_1 == sentence_2:
                continue

            edge_1 = (sentence_1, sentence_2)
            edge_2 = (sentence_2, sentence_1)

            if graph.has_edge(edge_1) or graph.has_edge(edge_2):
                continue

            similarity = get_similarity(sentence_1, sentence_2)

            graph.add_edge(edge_1, similarity)
            graph.add_edge(edge_2, similarity)


def get_similarity(s1, s2):

    words_sentence_one = s1.split()
    words_sentence_two = s2.split()

    common_word_count = get_common_word_count(words_sentence_one, words_sentence_two)

    log_s1 = log10(len(words_sentence_one))
    log_s2 = log10(len(words_sentence_two))

    if log_s1 + log_s2 == 0:
        return 0

    return common_word_count / (log_s1 + log_s2)


def get_common_word_count(words_sentence_one, words_sentence_two):
    words_set = set(words_sentence_two)
    return sum(1 for w in words_sentence_one if w in words_set)


def get_arguments():
    import sys, getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:m:h", ["text=", "method=", "help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    path = None
    method = None
    for o, a in opts:
        if o in ("-t", "--text"):
            path = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--method"):
            method = int(a)
        else:
            assert False, "unhandled option"
    if not path:
        path = TEST_FILE
    if not method:
        method = PAGERANK_MANUAL
    return method, path


def main():
    method, path = get_arguments()

    with open(path) as test_file:
        text = test_file.read()

    print textrank(text, method)


def usage():
    print "Usage: python textrank.py -t path/to/text -m [0,1]"
    print "-t: text to summarize. Default value: samples/textrank_example.txt"
    print "-m: method to use: Default value: 0"
    print "\t0: PageRank Manual. 1: PageRank using scipy.linalg.eig"


if __name__ == "__main__":
    main()





def get_test_graph(path):
    """Method to run test on the interpreter """
    # TODO: delete this method when no longer needed
    with open(path) as file:
        text = file.read()

    # Gets a dict of processed_sentence -> original_sentences
    tokens = tokenize_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = get_graph(tokens.keys())
    set_graph_edge_weights(graph)

    return graph
    # Ranks the tokens using the PageRank algorithm.
    # return pagerank_scipy(graph)