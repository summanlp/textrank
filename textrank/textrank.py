
from pygraph.classes.digraph import digraph as pydigraph
from pagerank_weighted import pagerank_weighted as pagerank
from textcleaner import tokenize_by_sentences
from math import log10

import pdb

SUMMARY_LENGTH = .2
TEST_FILE = "samples/textrank_example.txt"
DEBUG = False


def textrank(text):
    # Gets a dict of processed_sentence -> original_sentences
    tokens = tokenize_by_sentences(text)

    # Creates the graph and calculates the simmilarity coefficient for every pair of nodes.
    graph = get_graph(tokens.keys())
    set_graph_edge_weights(graph)

    # Ranks the tokens using the PageRank algorithm.
    scores = pagerank(graph)

    # Extracts the most important tokens.
    extracted_tokens = extract_tokens(graph.nodes(), scores)

    # Sorts the extracted sentences by apparition order in the
    # original text.
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
    return { sentences[i]: scores[sentences[i]] for i in range(int(length))}


def get_graph(text):
    graph = pydigraph()

    # Creates the graph.
    for line in text:
        graph.add_node(line)

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

    s1_list = s1.split()
    s2_list = s2.split()

    common_word_count = get_common_word_count(s1_list, s2_list)

    log_s1 = log10(len(s1_list))
    log_s2 = log10(len(s2_list))

    if log_s1 + log_s2 == 0:
        return 0

    return common_word_count / (log_s1 + log_s2)


def get_common_word_count(s1_list, s2_list):
    return sum(1 for w in set(s1_list) if w in set(s2_list))


def main():
    with open(TEST_FILE) as file:
        text = file.read()

    print textrank(text)


if __name__ == "__main__":
    main()