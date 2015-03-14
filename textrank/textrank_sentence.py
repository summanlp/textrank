
from pagerank_weighted import pagerank_weighted as pagerank, PAGERANK_MANUAL
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy, PAGERANK_SCIPY
from textcleaner import clean_text_by_sentences
from commons import get_graph, remove_unreacheable_nodes
from math import log10
from gexf_export import write_gexf
from textrank_word import textrank_by_word

DEBUG = False


def textrank_by_sentence(text, method=PAGERANK_MANUAL, summary_length=0.2):
    # Gets a list of processed sentences.
    sentences = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = get_graph([sentence.token for sentence in sentences])
    keywords = textrank_by_word(text)
    set_graph_edge_weights(graph, frozenset(keywords))

    # Remove all nodes with all edges weights equal to zero.
    remove_unreacheable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of sentence -> score
    scores = pagerank(graph) if method == PAGERANK_MANUAL else pagerank_scipy(graph)

    # Adds the textrank scores to the sentence objects.
    add_scores_to_sentences(sentences, scores)

    # Extracts the most important sentences.
    extracted_sentences = extract_most_important_sentences(sentences, summary_length)

    # Sorts the extracted sentences by apparition order in the original text.
    extracted_sentences.sort(key=lambda s: s.index)

    #write_gexf(graph, scores, path="sentences.gexf")

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


def set_graph_edge_weights(graph, keywords):
    for sentence_1 in graph.nodes():
        for sentence_2 in graph.nodes():

            edge = (sentence_1, sentence_2)
            if sentence_1 != sentence_2 and not graph.has_edge(edge):
                similarity = get_similarity(sentence_1, sentence_2, keywords)
                if similarity != 0:
                    graph.add_edge(edge, similarity)


def get_similarity(s1, s2, keywords):
    words_sentence_one = s1.split()
    words_sentence_two = s2.split()

    common_word_count = count_common_words(words_sentence_one, words_sentence_two)
    extra_points_for_keywords = count_common_keywords(words_sentence_one, words_sentence_two, keywords)

    log_s1 = log10(len(words_sentence_one))
    log_s2 = log10(len(words_sentence_two))

    if log_s1 + log_s2 == 0:
        return 0

    return (common_word_count + extra_points_for_keywords) / (log_s1 + log_s2)


def count_common_keywords(words_sentence_one, words_sentence_two, keywords):
    words_set = set(words_sentence_two)
    factor = 2
    return sum(factor for w in words_sentence_one if w in words_set and w in keywords)


def count_common_words(words_sentence_one, words_sentence_two):
    words_set = set(words_sentence_two)
    return sum(1 for w in words_sentence_one if w in words_set)


def get_test_graph(path):
    """Method to run test on the interpreter """
    # TODO: delete this method when no longer needed
    with open(path) as file:
        text = file.read()

    # Gets a list of processed sentences.
    sentences = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    return get_graph([sentence.token for sentence in sentences])
