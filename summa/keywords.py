from itertools import combinations as _combinations
from Queue import Queue as _Queue

from pagerank_weighted import pagerank_weighted_scipy as _pagerank
from preprocessing.textcleaner import clean_text_by_word as _clean_text_by_word
from preprocessing.textcleaner import tokenize_by_word as _tokenize_by_word
from commons import build_graph as _build_graph
from commons import remove_unreacheable_nodes as _remove_unreacheable_nodes


WINDOW_SIZE = 2
DEBUG = False


def keywords(text, summary_length=0.2, language="EN"):
    # Gets a dict of word -> lemma
    tokens = _clean_text_by_word(text, language)
    split_text = list(_tokenize_by_word(text))

    # Creates the graph and adds the edges
    graph = _build_graph(_get_words_for_graph(tokens))
    _set_graph_edges(graph, tokens, split_text)
    del split_text # It's no longer used

    _remove_unreacheable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of lemma -> score
    scores = _pagerank(graph)

    extracted_lemmas = _extract_tokens(graph.nodes(), scores, summary_length)

    lemmas_to_word = _lemmas_to_words(tokens)
    keywords = _get_keywords_with_score(extracted_lemmas, lemmas_to_word)

    # text.split() to keep numbers and punctuation marks, so separeted concepts are not combined
    combined_keywords = _get_combined_keywords(keywords, text.split())

    return _format_results(keywords, combined_keywords)


def _get_words_for_graph(tokens):
    include_filters, exclude_filters = _get_pos_filters()
    if include_filters and exclude_filters:
        raise ValueError("Can't use both include and exclude filters, should use only one")

    result = []
    for word, unit in tokens.iteritems():
        if exclude_filters and unit.tag in exclude_filters:
            continue
        if (include_filters and unit.tag in include_filters) or not include_filters or not unit.tag:
            result.append(unit.token)
    return result


def _get_pos_filters():
    """Check tags in http://www.clips.ua.ac.be/pages/mbsp-tags and use only first two letters
    Example: filter for nouns and adjectives:
    including = ['NN', 'JJ']
    """
    including = ['NN', 'JJ']
    excluding = []
    return frozenset(including), frozenset(excluding)


def _set_graph_edges(graph, tokens, split_text):
    _process_first_window(graph, tokens, split_text)
    _process_text(graph, tokens, split_text)


def _process_first_window(graph, tokens, split_text):
    first_window = _get_first_window(split_text)
    for word_a, word_b in _combinations(first_window, 2):
        _set_graph_edge(graph, tokens, word_a, word_b)


def _get_first_window(split_text):
    return split_text[:WINDOW_SIZE]


def _set_graph_edge(graph, tokens, word_a, word_b):
    if word_a in tokens and word_b in tokens:
        lemma_a = tokens[word_a].token
        lemma_b = tokens[word_b].token
        edge = (lemma_a, lemma_b)

        if graph.has_node(lemma_a) and graph.has_node(lemma_b) and not graph.has_edge(edge):
            graph.add_edge(edge)


def _process_text(graph, tokens, split_text):
    queue = _init_queue(split_text)
    for i in xrange(WINDOW_SIZE, len(split_text)):
        word = split_text[i]
        _process_word(graph, tokens, queue, word)
        _update_queue(queue, word)


def _init_queue(split_text):
    queue = _Queue()
    first_window = _get_first_window(split_text)
    for word in first_window[1:]:
        queue.put(word)
    return queue


def _process_word(graph, tokens, queue, word):
    for word_to_compare in _queue_iterator(queue):
        _set_graph_edge(graph, tokens, word, word_to_compare)


def _queue_iterator(queue):
    iterations = queue.qsize()
    for i in xrange(iterations):
        var = queue.get()
        yield var
        queue.put(var)


def _update_queue(queue, word):
    queue.get()
    queue.put(word)
    assert queue.qsize() == (WINDOW_SIZE - 1)


def _extract_tokens(lemmas, scores, summary_length):
    lemmas.sort(key=lambda s: scores[s], reverse=True)
    length = len(lemmas) * summary_length
    return [(scores[lemmas[i]], lemmas[i],) for i in range(int(length))]


def _lemmas_to_words(tokens):
    lemma_to_word = {}
    for word, unit in tokens.iteritems():
        lemma = unit.token
        if lemma in lemma_to_word:
            lemma_to_word[lemma].append(word)
        else:
            lemma_to_word[lemma] = [word]
    return lemma_to_word


def _get_keywords_with_score(extracted_lemmas, lemma_to_word):
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


def _get_combined_keywords(keywords, split_text):
    """
    :param keywords:dict of keywords:scores
    :param split_text: list of strings
    :return: combined_keywords:list
    """
    result = []
    keywords = keywords.copy()
    len_text = len(split_text)
    for i in xrange(len_text):
        word = _strip_word(split_text[i])
        if word in keywords:
            combined_word = [word]
            if i + 1 == len_text: result.append(word)   # appends last word if keyword and doesn't iterate
            for j in xrange(i + 1, len_text):
                other_word = _strip_word(split_text[j])
                if other_word in keywords and other_word == split_text[j].decode("utf-8"):
                    combined_word.append(other_word)
                else:
                    for keyword in combined_word: keywords.pop(keyword)
                    result.append(" ".join(combined_word))
                    break
    return result


def _strip_word(word):
    stripped_word_list = list(_tokenize_by_word(word))
    return stripped_word_list[0] if stripped_word_list else ""


def _format_results(keywords, combined_keywords):
    combined_keywords.sort(key=lambda w: keywords[w.split()[0]], reverse=True)
    if DEBUG:
        combined_keywords = ["({0:.4f}) : {1}".format(keywords[word.split()[0]], word) for word in combined_keywords]

    return "\n".join(combined_keywords)


def get_graph(text, language="EN"):
    tokens = _clean_text_by_word(text, language)
    split_text = list(_tokenize_by_word(text))

    graph = _build_graph(tokens.values())
    _set_graph_edges(graph, tokens, split_text)

    return graph