import sys
import os
from copy import deepcopy

# TODO: fix imports.
sys.path.append(os.pardir)
from textrank.textcleaner import get_sentences
from textrank.impl import get_graph, set_graph_edge_weights, remove_unreacheable_nodes
from textrank.pagerank_weighted import pagerank_weighted, pagerank_weighted_scipy

"""Performs a comparison between the iterative version and the
   scipy design."""

# Uses the summa database texts.
TEXT_FILENAME_FORMAT = '../evaluation/datasets/summa/{text_number:02d}/text.txt'
TEXT_FILE_PATHS = [TEXT_FILENAME_FORMAT.format(text_number=i) for i in xrange(1, 11)]


def get_graph_for_text(text_filename):
    # Reads the file.
    with open(text_filename) as fp:
        text = fp.read()

    # Splits the text into sentences.
    sentences = get_sentences(text)

    # Creates the graph.
    graph = get_graph(sentences)
    set_graph_edge_weights(graph)
    remove_unreacheable_nodes(graph)

    return graph


def get_scores(graph):
    # Keeps a copy of the graphs for applying the second method.
    graph_copy = deepcopy(graph)

    # Runs the algorithms.
    pagerank_weighted_score = pagerank_weighted(graph)
    pagerank_weighted_scipy_score = pagerank_weighted_scipy(graph_copy)

    return pagerank_weighted_score, pagerank_weighted_scipy_score


def get_highest_scoring_sentences(score):
    """From a dict with the sentences as keys and the scores as values,
    returns a list of tuples with the top scoring sentences."""

    # Sorts the sentences by score.
    sentences = score.items()
    sentences.sort(key=lambda x: x[1], reverse=True)

    # Keeps the top scoring.
    number_sentences = int(len(sentences) * 0.2)
    return [sentence[0] for sentence in sentences[:number_sentences]]


def compare_scores(score_1, score_2):
    """Returns a final score based on how many sentences the scores have in common."""
    sentences_1 = get_highest_scoring_sentences(score_1)
    sentences_2 = get_highest_scoring_sentences(score_2)

    score = 0.0
    for sentence in sentences_1:
        if sentence in sentences_2:
            score += 1

    return score / len(sentences_1)


def compare_texts():
    number_texts = len(TEXT_FILE_PATHS)
    total_score = 0.0

    for text_filename in TEXT_FILE_PATHS:
        print "Processing file", text_filename
        graph = get_graph_for_text(text_filename)
        score_1, score_2 = get_scores(graph)
        text_score = compare_scores(score_1, score_2)
        total_score += text_score
        print "Text score is", str(text_score)

    print "Total score is:", str(total_score / number_texts)


compare_texts()