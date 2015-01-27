import sys
import os
from pygraph.classes.digraph import digraph as pydigraph

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


