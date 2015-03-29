
from math import log10 as _log10
from pagerank_weighted import pagerank_weighted_scipy as _pagerank
from preprocessing.textcleaner import clean_text_by_sentences as _clean_text_by_sentences
from commons import build_graph as _build_graph
from commons import remove_unreachable_nodes as _remove_unreachable_nodes
from gensim import corpora, similarities, models

def _set_graph_edge_weights(graph, sentences):
    dictionary, corpus = build_dictionary_and_corpus(sentences)
    tfidf = models.TfidfModel(corpus)
    similarityMatrix = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.token2id))
    for sentence_1 in sentences:
        for sentence_2 in sentences:
            if sentence_1.index == sentence_2.index: continue

            token_1 = sentence_1.token
            token_2 = sentence_2.token

            edge = (token_1, token_2)
            if not graph.has_edge(edge):
                similarity = get_similarity(sentence_1, sentence_2, similarityMatrix, corpus, tfidf)
                if similarity != 0:
                    graph.add_edge(edge, similarity)


def build_dictionary_and_corpus(sentences):
    split_tokens = [sentence.token.split() for sentence in sentences]
    dictionary = corpora.Dictionary(split_tokens)
    corpus = [dictionary.doc2bow(token) for token in split_tokens]
    return dictionary, corpus


def get_similarity(s1, s2, similarityMatrix, corpus, tfidf):
    similarity = similarityMatrix[tfidf[corpus[s1.index]]]
    return list(similarity)[s2.index]


def _format_results(extracted_sentences, split, score):
    if score:
        return [(sentence.text, sentence.score) for sentence in extracted_sentences]
    if split:
        return [sentence.text for sentence in extracted_sentences]
    return "\n".join([sentence.text for sentence in extracted_sentences])


def _add_scores_to_sentences(sentences, scores):
    for sentence in sentences:
        # Adds the score to the object if it has one.
        if sentence.token in scores:
            sentence.score = scores[sentence.token]
        else:
            sentence.score = 0


def _get_sentences_with_word_count(sentences, words):
    """ Given a list of sentences, returns a list of sentences with a
    total word count similar to the word count provided.
    """
    word_count = 0
    selected_sentences = []
    # Loops until the word count is reached.
    for sentence in sentences:
        words_in_sentence = len(sentence.text.split())

        # Checks if the inclusion of the sentence gives a better approximation
        # to the word parameter.
        if abs(words - word_count - words_in_sentence) > abs(words - word_count):
            return selected_sentences

        selected_sentences.append(sentence)
        word_count += words_in_sentence

    return selected_sentences


def _extract_most_important_sentences(sentences, ratio, words):
    sentences.sort(key=lambda s: s.score, reverse=True)

    # If no "words" option is selected, the number of sentences is
    # reduced by the provided ratio.
    if words is None:
        length = len(sentences) * ratio
        return sentences[:int(length)]

    # Else, the ratio is ignored.
    else:
        return _get_sentences_with_word_count(sentences, words)


def summarize(text, ratio=0.2, words=None, language="EN", split=False, scores=False):
    # Gets a list of processed sentences.
    sentences = _clean_text_by_sentences(text, language)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = _build_graph([sentence.token for sentence in sentences])
    _set_graph_edge_weights(graph, sentences)

    # Remove all nodes with all edges weights equal to zero.
    _remove_unreachable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of sentence -> score
    pagerank_scores = _pagerank(graph)

    # Adds the summa scores to the sentence objects.
    _add_scores_to_sentences(sentences, pagerank_scores)

    # Extracts the most important sentences with the selected criterion.
    extracted_sentences = _extract_most_important_sentences(sentences, ratio, words)

    # Sorts the extracted sentences by apparition order in the original text.
    extracted_sentences.sort(key=lambda s: s.index)

    return _format_results(extracted_sentences, split, scores)


def get_graph(text, language="EN"):
    sentences = _clean_text_by_sentences(text, language)

    graph = _build_graph([sentence.token for sentence in sentences])
    _set_graph_edge_weights(graph)

    return graph
