from pagerank_weighted import pagerank_weighted as pagerank, PAGERANK_MANUAL
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy, PAGERANK_SCIPY
from textcleaner import clean_text_by_sentences
from commons import get_graph, remove_unreacheable_nodes
from math import fabs, log10
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
    common_word_group_count = count_common_word_group(words_sentence_one, words_sentence_two)

    log_s1 = log10(len(words_sentence_one))
    log_s2 = log10(len(words_sentence_two))

    if log_s1 + log_s2 == 0:
        return 0

    return (common_word_count + common_word_group_count) / (log_s1 + log_s2)


def count_common_words(words_sentence_one, words_sentence_two):
    words_set = set(words_sentence_two)
    return sum(1 for w in words_sentence_one if w in words_set)


def count_common_word_group(s1_split, s2_split):
    common_concepts = count_common_concepts(s1_split, s2_split)
    factor = 10
    return common_concepts * factor

def count_common_concepts(s1_split, s2_split):
    s2_index = get_index_dict(s2_split)
    concepts = 0
    for i in xrange(len(s1_split) - 1):
        word = s1_split[i]
        if word in s2_index:
            next_word = s1_split[i+1]
            if next_word in s2_index and distance_is_one(s2_index[word], s2_index[next_word]):
                concepts += 1
    return concepts


def distance_is_one(index_word, index_next_word):
    for index in index_word:
        for index_next in index_next_word:
            if index_next - index == 1:
                return True
    return False


def get_index_dict(s2_split):
    index = {}
    for i in xrange(len(s2_split)):
        word = s2_split[i]
        if word in index:
            index[word].append(i)
        else:
            index[word] = [i]
    return index

def get_test_graph(path):
    """Method to run test on the interpreter """
    # TODO: delete this method when no longer needed
    with open(path) as file:
        text = file.read()

    # Gets a list of processed sentences.
    sentences = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = get_graph([sentence.token for sentence in sentences])
    set_graph_edge_weights(graph)

    return graph
    # Ranks the tokens using the PageRank algorithm.
    # return pagerank_scipy(graph)
