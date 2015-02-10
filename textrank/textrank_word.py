
from pygraph.classes.graph import graph as pygraph
from pagerank_weighted import pagerank_weighted as pagerank, PAGERANK_MANUAL
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy, PAGERANK_SCIPY
from textcleaner import clean_text_by_word, tokenize_by_word
from itertools import combinations
from Queue import Queue
from commons import get_graph, remove_unreacheable_nodes

import pdb

PAGERANK_INITIAL_VALUE = 1
WINDOW_SIZE = 2
DEBUG = False


def textrank_by_word(text, method=PAGERANK_SCIPY, summary_length=0.2):
    # Gets a dict of word -> lemma
    tokens = clean_text_by_word(text)
    split_text = list(tokenize_by_word(text))

    # Creates the graph and adds the edges
    graph = get_graph(tokens.values())
    set_graph_edges(graph, tokens, split_text)

    remove_unreacheable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of lemma -> score
    scores = pagerank(graph, PAGERANK_INITIAL_VALUE) if method == PAGERANK_MANUAL else pagerank_scipy(graph)

    extracted_lemmas = extract_tokens(graph.nodes(), scores, summary_length)

    keywords = get_keywords_with_score(extracted_lemmas, lemmas_to_words(tokens))

    combined_keywords = get_combined_keywords(keywords, split_text)

    return format_results(keywords, combined_keywords)



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


def get_keywords_with_score(extracted_lemmas, lemma_to_word):
    """
    :param extracted_lemmas:list of tuples
    :param lemma_to_word: dict of {lemma:list of words}
    :return: dict of {keyword:score}
    """
    keywords = {}
    for score, lemma in extracted_lemmas:
        keyword_list = lemma_to_word[lemma]
        for keyword in keyword_list:
            keywords[keyword] = score
    return keywords
    # return {keyword:score for score, lemma in extracted_lemmas for keyword in lemma_to_word[lemma]}
    # if you dare


def get_combined_keywords(keywords, split_text):
    """
    :param keywords:dict of keywords:scores
    :param split_text: list of strings
    :return: combined_keywords:list
    """
    result = []
    keywords = keywords.copy()
    len_text = len(split_text)
    for i in xrange(len_text):
        word = split_text[i]
        if word in keywords:
            combined_word = [word]
            if i + 1 == len_text: result.append(word) # appends last word if keyword and doesn't iterate
            for j in xrange(i + 1, len_text):
                other_word = split_text[j]
                if other_word in keywords:
                    combined_word.append(other_word)
                else:
                    for keyword in combined_word: keywords.pop(keyword)
                    result.append(" ".join(combined_word))
                    break
    return result


def format_results(keywords, combined_keywords):
    combined_keywords.sort(key=lambda w: keywords[w.split()[0]], reverse=True)
    if DEBUG:
        combined_keywords = ["({0:.4f}) : {1}".format(keywords[word.split()[0]], word) for word in combined_keywords]

    return "\n".join(combined_keywords)


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