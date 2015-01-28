
from scipy.sparse import csr_matrix
from scipy.linalg import eig
from math import fabs
# Methods for PageRank
PAGERANK_MANUAL = 0
PAGERANK_SCIPY = 1

CONVERGENCE_THRESHOLD = 0.0001

def pagerank_weighted(graph, damping=0.85):
    scores = dict.fromkeys(graph.nodes(), 1.0 / len(graph.nodes()))

    #iteration_quantity = 0
    for iteration_number in xrange(100):
    #    iteration_quantity += 1
        convergence_achieved = 0
        for i in graph.nodes():
            rank = 1 - damping
            for j in graph.incidents(i):
                neighbors_sum = sum(graph.edge_weight((j, k)) for k in graph.neighbors(j))
                rank += damping * scores[j] * graph.edge_weight((j, i)) / neighbors_sum

            if fabs(scores[i] - rank) <= CONVERGENCE_THRESHOLD:
                convergence_achieved += 1

            scores[i] = rank

        if convergence_achieved == len(graph.nodes()):
            break

        # print "pagerank iteration %d ended. achieved %f convergence " % (iteration_number, convergence_achieved / float(len(graph.nodes())))
    # print "Cantidad de iteraciones:", iteration_quantity
    return scores


def pagerank_weighted_scipy(graph):
    matrix = build_matrix(graph)
    vals, vecs = eig(matrix.todense(), left=True, right=False)
    return process_results(graph, vecs)

def build_matrix(graph):
    row = []
    col = []
    data = []
    nodes = graph.nodes()
    length = len(nodes)

    for i in xrange(length):
        current_node = nodes[i]
        neighbors_sum = sum(graph.edge_weight((current_node, neighbor)) for neighbor in graph.neighbors(current_node))
        for j in xrange(length):
            edge_weight = float(graph.edge_weight((current_node, nodes[j])))
            if i != j and edge_weight != 0:
                row.append(i)
                col.append(j)
                data.append(edge_weight / neighbors_sum)

    return csr_matrix((data,(row,col)), shape=(length,length))

def process_results(graph, vecs):
    scores = {}
    for i, node in enumerate(graph.nodes()):
        scores[node] = fabs(float(vecs[i][0]))

    return scores














