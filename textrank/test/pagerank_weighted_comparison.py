import sys
import os
from pygraph.classes.digraph import digraph as pydigraph
from copy import deepcopy

sys.path.append(os.pardir)
from textrank import textrank

from textrank.textcleaner import get_sentences
from textrank.impl import get_graph, set_graph_edge_weights
from textrank.pagerank_weighted import pagerank_weighted, pagerank_weighted_scipy

"""Performs a comparison between the iterative version and the
   scipy design."""

# Uses the summa database texts.
TEXT_FILENAME_FORMAT = '../../evaluation/datasets/summa/{text_number:02d}/text.txt'
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

    return graph


def get_comparison(graph):
    # Keeps a copy of the graphs for applying the second method.
    graph_copy = deepcopy(graph)

    # Performs the algorithms.
    pagerank_weighted_score = pagerank_weighted(graph)
    pagerank_weighted_scipy_score = pagerank_weighted_scipy(graph_copy)

    return pagerank_weighted_score, pagerank_weighted_scipy_score




