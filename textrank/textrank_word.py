
from pygraph.classes.graph import graph as pygraph
from pagerank_weighted import pagerank_weighted as pagerank, PAGERANK_MANUAL
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy, PAGERANK_SCIPY
from textcleaner import tokenize_by_word

WINDOW_SIZE = 5

def textrank_by_word(text, method=PAGERANK_MANUAL, summary_length=0.2):
    # Gets a dict of word -> lemma
    tokens = tokenize_by_word(text)

    # Creates the graph and adds the edges
    graph = get_graph(tokens.values())
    set_graph_edges(graph, tokens)


def get_graph(lemmas):
    graph = pygraph()
    graph.add_nodes(lemmas)
    return graph


def set_graph_edges(graph, tokens):
    windows = get_windows(tokens)


def get_windows(tokens):
    """return a window generator"""
    # aca puedo cambiar si quiero que la ventana sea en base a las words o a los lemmas
    return window(tokens.keys(), WINDOW_SIZE)

def window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ..."""
    iterations = len(seq) - n + 1
    for i in xrange(iterations):
        yield seq[i:i+n]
