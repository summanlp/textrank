
from pygraph.classes.digraph import digraph as pygraph

def build_graph(sequence):
    graph = pygraph()
    graph.DEFAULT_WEIGHT = 0
    for item in sequence:
        if not graph.has_node(item):
            graph.add_node(item)
    return graph


def remove_unreachable_nodes(graph):
    for node in graph.nodes():
        if sum(graph.edge_weight((node, other)) for other in graph.neighbors(node)) == 0:
            graph.del_node(node)
