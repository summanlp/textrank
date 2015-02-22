
import networkx as nx
from os import system as shell

NODE_COLOR = {'r': 239, 'g': 10, 'b': 10}

def write_gexf(graph, scores, path="test.gexf"):
    nx_graph = get_nx_graph(graph)
    set_layout(nx_graph, scores)
    nx.write_gexf(nx_graph, path)
    shell("sed -i 's/<ns0/<viz/g' {0}".format(path))
    shell('echo \'<?xml version="1.0" encoding="UTF-8"?>\' | cat - {0} > out.tmp && mv out.tmp {0}'.format(path))
    shell("mv {0} views/{0}".format(path))


def get_nx_graph(graph):
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(graph.nodes())
    for edge in graph.edges():
        weight = graph.edge_weight(edge)
        if weight != 0:
            nx_graph.add_edge(edge[0], edge[1], {'weight':weight})
    return nx_graph


def set_layout(nx_graph, scores):
    positions = nx.graphviz_layout(nx_graph, prog="neato") # prog options: neato, dot, fdp, sfdp, twopi, circo
    for node in nx_graph.nodes():
        nx_graph.node[node]['viz'] = get_viz_data(node, positions, scores)
        nx_graph.node[node]['label'] = " ".join(node.split()[0:2])


def get_viz_data(node, positions, scores):
    viz_data = {}
    viz_data['position'] = {'x':positions[node][0], 'y':positions[node][1]}
    viz_data['size'] = scores[node]
    viz_data['color'] = NODE_COLOR
    return viz_data

