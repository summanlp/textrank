
CONVERGENCE_THRESHOLD = 0.0001


def pagerank_weighted(graph, damping=0.85):
    scores = dict.fromkeys(graph.nodes(), 1.0 / len(graph.nodes()))

    for iteration_number in range(100):
        for i in graph.nodes():
            rank = 1 - damping
            for j in graph.incidents(i):
                neighbors_sum = sum(graph.edge_weight((j, k)) for k in graph.neighbors(j))

                if neighbors_sum == 0:
                    neighbors_sum = 1

                rank += damping * scores[j] * graph.edge_weight((j, i)) / neighbors_sum

            scores[i] = rank

    return scores
