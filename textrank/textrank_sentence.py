from pagerank_weighted import pagerank_weighted as pagerank, PAGERANK_MANUAL
from pagerank_weighted import pagerank_weighted_scipy as pagerank_scipy, PAGERANK_SCIPY
from textcleaner import clean_text_by_sentences
from commons import get_graph, remove_unreacheable_nodes
from math import fabs, log10
from gexf_export import write_gexf
from gensim import corpora, similarities, models

DEBUG = False


def textrank_by_sentence(text, method=PAGERANK_MANUAL, summary_length=0.2):
    # Gets a list of processed sentences.
    sentences = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = get_graph([sentence.token for sentence in sentences])
    set_graph_edge_weights(graph, sentences)

    # Remove all nodes with all edges weights equal to zero.
    remove_unreacheable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of sentence -> score
    scores = pagerank(graph) if method == PAGERANK_MANUAL else pagerank_scipy(graph)

    # Adds the textrank scores to the sentence objects.
    add_scores_to_sentences(sentences, scores)

    # Extracts the most important sentences.
    extracted_sentences = extract_most_important_sentences(sentences, summary_length)

    # Sorts the extracted sentences by apparition order in the original text.
    extracted_sentences.sort(key=lambda s: s.index)

    #write_gexf(graph, scores, path="sentences.gexf")

    return "\n".join([sentence.text for sentence in extracted_sentences])


def add_scores_to_sentences(sentences, scores):
    for sentence in sentences:
        # Adds the score to the object if it has one.
        if sentence.token in scores:
            sentence.score = scores[sentence.token]
        else:
            sentence.score = 0


def extract_most_important_sentences(sentences, summary_length):
    sentences.sort(key=lambda s: s.score, reverse=True)
    length = len(sentences) * summary_length

    return sentences[:int(length)]


def set_graph_edge_weights(graph, sentences):
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





def get_test_graph(path):
    """Method to run test on the interpreter """
    # TODO: delete this method when no longer needed
    with open(path) as file:
        text = file.read()

    # Gets a list of processed sentences.
    sentences = clean_text_by_sentences(text)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = get_graph([sentence.token for sentence in sentences])
    set_graph_edge_weights(graph, sentences)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    return get_graph([sentence.token for sentence in sentences])
