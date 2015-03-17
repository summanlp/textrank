
from pagerank_weighted import PAGERANK_MANUAL
from pagerank_weighted import build_adjacency_matrix
from pagerank_weighted import build_probability_matrix
from textcleaner import clean_text_by_sentences
from commons import get_graph, remove_unreacheable_nodes
from math import log10
from scipy.linalg import svd
from math import fabs
from gexf_export import write_gexf

DEBUG = False


def textrank_by_sentence(text, method=PAGERANK_MANUAL, summary_length=0.2):
    # Gets a list of processed sentences.
    sentences = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = get_graph([sentence.token for sentence in sentences])
    set_graph_edge_weights(graph)

    # Remove all nodes with all edges weights equal to zero.
    remove_unreacheable_nodes(graph)

    # Ranks the tokens using the HITS algorithm. Returns dict of sentence -> score
    scores = hits(graph)

    # Adds the textrank scores to the sentence objects.
    add_scores_to_sentences(sentences, scores)

    # Extracts the most important sentences.
    extracted_sentences = extract_most_important_sentences(sentences, summary_length)

    # Sorts the extracted sentences by apparition order in the original text.
    extracted_sentences.sort(key=lambda s: s.index)

    write_gexf(graph, scores, path="sentences.gexf")

    #print "\n".join([sentence.text for sentence in extracted_sentences])

    return "\n".join([sentence.text for sentence in extracted_sentences])


def add_scores_to_sentences(sentences, scores):
    for sentence in sentences:
        # Adds the score to the object if it has one.
        if sentence.token in scores:
            sentence.score = scores[sentence.token]
        else:
            sentence.score = 0


def extract_most_important_sentences(sentences, summary_length):
    sentences.sort(key=lambda s: s.score, reverse=True)
    length = len(sentences) * summary_length

    return sentences[:int(length)]


def set_graph_edge_weights(graph):
    for sentence_1 in graph.nodes():
        for sentence_2 in graph.nodes():

            edge = (sentence_1, sentence_2)
            if sentence_1 != sentence_2 and not graph.has_edge(edge):
                similarity = get_similarity(sentence_1, sentence_2)
                if similarity != 0:
                    graph.add_edge(edge, similarity)


def get_similarity(s1, s2):
    words_sentence_one = s1.split()
    words_sentence_two = s2.split()

    common_word_count = count_common_words(words_sentence_one, words_sentence_two)

    log_s1 = log10(len(words_sentence_one))
    log_s2 = log10(len(words_sentence_two))

    if log_s1 + log_s2 == 0:
        return 0

    return common_word_count / (log_s1 + log_s2)


def count_common_words(words_sentence_one, words_sentence_two):
    words_set = set(words_sentence_two)
    return sum(1 for w in words_sentence_one if w in words_set)


def hits(graph):
    adjacency_matrix = build_adjacency_matrix(graph)
    probability_matrix = build_probability_matrix(graph)

    pagerank_matrix = adjacency_matrix.todense() #+ probability_matrix
    u, s, vh = svd(pagerank_matrix, full_matrices=True, compute_uv=True)

    scores = {}
    for i, node in enumerate(graph.nodes()):
        scores[node] = fabs(float(u[0][i]))

    return scores


def get_test_graph(path):
    """Method to run test on the interpreter """
    # TODO: delete this method when no longer needed
    with open(path) as file:
        text = file.read()

    # Gets a dict of processed_sentence -> original_sentences
    tokens = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    sentences = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    return get_graph([sentence.token for sentence in sentences])
