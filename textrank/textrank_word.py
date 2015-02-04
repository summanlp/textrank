
from pygraph.classes.graph import graph as pygraph
from pagerank_weighted import pagerank_weighted as pagerank, PAGERANK_MANUAL
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy, PAGERANK_SCIPY
from textcleaner import clean_text_by_word, tokenize_by_word
from itertools import combinations
from Queue import Queue
#TODO sacar en archivo aparte
from textrank_sentence import remove_unreacheable_nodes

import pdb

pygraph.DEFAULT_WEIGHT = 0
WINDOW_SIZE = 2
DEBUG = True


def textrank_by_word(text, method=PAGERANK_SCIPY, summary_length=0.2):
    # Gets a dict of word -> lemma
    tokens = clean_text_by_word(text)
    split_text = list(tokenize_by_word(text))

    # Creates the graph and adds the edges
    graph = get_graph(tokens.values())
    set_graph_edges(graph, tokens, split_text)

    remove_unreacheable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of lemma -> score
    scores = pagerank(graph) if method == PAGERANK_MANUAL else pagerank_scipy(graph)

    extracted_lemmas = extract_tokens(graph.nodes(), scores, summary_length)

    keywords = get_keywords(extracted_lemmas, lemmas_to_words(tokens))

    combined_keywords = get_combined_keywords(keywords, split_text)

    return "\n".join(combined_keywords)


def get_graph(lemmas):
    graph = pygraph()
    for lemma in lemmas:
        if not graph.has_node(lemma):
            graph.add_node(lemma)
    return graph


def set_graph_edges(graph, tokens, split_text):
    process_first_window(graph, tokens, split_text)
    process_text(graph, tokens, split_text)


def process_first_window(graph, tokens, split_text):
    first_window = get_first_window(split_text)
    for word_a, word_b in combinations(first_window, 2):
        set_graph_edge(graph, tokens, word_a, word_b)


def get_first_window(split_text):
    return split_text[:WINDOW_SIZE]


def set_graph_edge(graph, tokens, word_a, word_b):
    if word_a in tokens and word_b in tokens:
        lemma_a = tokens[word_a]
        lemma_b = tokens[word_b]
        edge = (lemma_a, lemma_b)

        if not graph.has_edge(edge):
            graph.add_edge(edge)


def process_text(graph, tokens, split_text):
    queue = init_queue(split_text)
    for i in xrange(WINDOW_SIZE, len(split_text)):
        word = split_text[i]
        process_word(graph, tokens, queue, word)
        update_queue(queue, word)


def init_queue(split_text):
    queue = Queue()
    first_window = get_first_window(split_text)
    for word in first_window[1:]:
        queue.put(word)
    return queue


def process_word(graph, tokens, queue, word):
    for word_to_compare in queue_iterator(queue):
        set_graph_edge(graph, tokens, word, word_to_compare)


def queue_iterator(queue):
    iterations = queue.qsize()
    for i in xrange(iterations):
        var = queue.get()
        yield var
        queue.put(var)


def update_queue(queue, word):
    queue.get()
    queue.put(word)
    assert queue.qsize() == (WINDOW_SIZE - 1)


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
        keyword = lemma_to_word[lemma][0]
        if DEBUG:
            keyword = "({0:.4f}) : {1}".format(score, lemma_to_word[lemma])
        keywords.append(keyword)
    return keywords



def get_combined_keywords(keywords, split_text):
    if DEBUG:
        print "WARN: Can't combine keywords in DEBUG mode"
        return keywords
    keywords_indexes = get_keywords_index(keywords, split_text)
    return combine_keywords(keywords, keywords_indexes)


def combine_keywords(keywords, keywords_indexes):
    INVALID_INDEX = -2
    result = []
    for keyword in keywords:
        keyword_index = keywords_indexes.get(keyword, INVALID_INDEX)
        if keyword_index == INVALID_INDEX: continue

        word_appended = False
        for other_keyword in keywords:
            other_keyword_index = keywords_indexes.get(other_keyword, INVALID_INDEX)
            if other_keyword_index == INVALID_INDEX: continue
            if keyword_index - 1 == other_keyword_index or keyword_index + 1 == other_keyword_index:
                if other_keyword_index == keyword_index + 1:
                    result.append(keyword + " " + other_keyword)
                elif other_keyword_index + 1 == keyword_index:
                    result.append(other_keyword + " " + keyword)
                keywords_indexes[other_keyword] = INVALID_INDEX
                word_appended = True

        if not word_appended:
            result.append(keyword)

    return result


def get_keywords_index(keywords, split_text):
    indexes = {}
    for keyword in keywords:
        try:
            index = split_text.index(keyword)
            indexes[keyword] = index
        except ValueError:
            continue
    return indexes



def get_test_graph(path):
    """Method to run test on the interpreter """
    # TODO: delete this method when no longer needed
    with open(path) as file:
        text = file.read()

    tokens = clean_text_by_word(text)
    split_text = list(tokenize_by_word(text))

    # Creates the graph and adds the edges
    graph = get_graph(tokens.values())
    set_graph_edges(graph, tokens, split_text)

    return graph