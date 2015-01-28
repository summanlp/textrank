
from pygraph.classes.graph import graph as pygraph
from pagerank_weighted import pagerank_weighted as pagerank, PAGERANK_MANUAL
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy, PAGERANK_SCIPY
from textcleaner import clean_text_by_word, tokenize_by_word
from itertools import combinations

WINDOW_SIZE = 5
DEBUG = True

def textrank_by_word(text, method=PAGERANK_SCIPY, summary_length=0.2):
    # Gets a dict of word -> lemma
    tokens = clean_text_by_word(text)
    split_text = list(tokenize_by_word(text))

    # Creates the graph and adds the edges
    graph = get_graph(tokens.values())
    set_graph_edges(graph, tokens, split_text)

    # Ranks the tokens using the PageRank algorithm. Returns dict of lemma -> score
    scores = pagerank(graph) if method == PAGERANK_MANUAL else pagerank_scipy(graph)

    extracted_lemmas = extract_tokens(graph.nodes(), scores, summary_length)

    keywords = get_keywords(extracted_lemmas, lemmas_to_words(tokens))

    return "\n".join(keywords)

def get_graph(lemmas):
    graph = pygraph()
    for lemma in lemmas:
        if not graph.has_node(lemma):
            graph.add_node(lemma)
    return graph


def set_graph_edges(graph, tokens, split_text):
    #TODO: cambiar la sliding window por una cola, asi cuando la ventana se mueve uno a la derecha, no compara
    #TODO:     nuevamente los primeros n - 1 elementos de la ventana
    windows = get_windows(split_text)
    for window in windows:
        set_edges_from_window(graph, tokens, window)


def set_edges_from_window(graph, tokens, window):
    for word_a, word_b in combinations(window, 2):
        if word_a in tokens and word_b in tokens:
            lemma_a = tokens[word_a]
            lemma_b = tokens[word_b]
            if not graph.has_edge((lemma_a,lemma_b)):
                graph.add_edge((lemma_a,lemma_b))


def get_windows(split_text):
    """return a sliding window generator"""
    #TODO: Aca se puede cambiar, para que la ventana se "calcule" respecto de las palabras ya lemmatizadas
    return sliding_windows(split_text, WINDOW_SIZE)

def sliding_windows(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ..."""
    iterations = len(seq) - n + 1
    for i in xrange(iterations):
        yield seq[i:i+n]


def extract_tokens(lemmas, scores, summary_length):
    lemmas.sort(key=lambda s: scores[s], reverse=True)
    length = len(lemmas) * summary_length
    return [(scores[lemmas[i]], lemmas[i],) for i in range(int(length))]


def lemmas_to_words(tokens):
    lemma_to_word = {}
    for key, value in tokens.iteritems():
        words = lemma_to_word.get(value, None)
        if not words:
            lemma_to_word[value] = [key]
        else:
            words.append(key)
    return lemma_to_word



def get_keywords(extracted_lemmas, lemma_to_word):
    keywords = []
    for score, lemma in extracted_lemmas:
        keyword = lemma_to_word[lemma]
        if DEBUG:
            keyword = "({0:.4f}) : {1}".format(score, keyword)
        keywords.append(keyword)
    return keywords