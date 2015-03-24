
from pygraph.classes.graph import graph as pygraph
from abc import ABCMeta, abstractmethod


class IGraph:
    """
    Represents the interface or contract that the graph for TextRank should implement
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def nodes(self):
        """
        Return node list.

        @rtype:  list
        @return: Node list.
        """
        pass


    @abstractmethod
    def edges(self):
        """
        Return all edges in the graph.

        @rtype:  list
        @return: List of all edges in the graph.
        """
        pass

    @abstractmethod
    def neighbors(self, node):
        """
        Return all nodes that are directly accessible from given node.

        @type  node: node
        @param node: Node identifier

        @rtype:  list
        @return: List of nodes directly accessible from given node.
        """
        pass


    @abstractmethod
    def has_node(self, node):
        """
        Return whether the requested node exists.

        @type  node: node
        @param node: Node identifier

        @rtype:  boolean
        @return: Truth-value for node existence.
        """
        pass


    @abstractmethod
    def add_node(self, node, attrs=None):
        """
        Add given node to the graph.

        @attention: While nodes can be of any type, it's strongly recommended to use only
        numbers and single-line strings as node identifiers if you intend to use write().

        @type  node: node
        @param node: Node identifier.

        @type  attrs: list
        @param attrs: List of node attributes specified as (attribute, value) tuples.
        """
        pass


    @abstractmethod
    def add_edge(self, edge, wt=1, label='', attrs=[]):
        """
        Add an edge to the graph connecting two nodes.

        An edge, here, is a pair of nodes like C{(n, m)}.

        @type  edge: tuple
        @param edge: Edge.

        @type  wt: number
        @param wt: Edge weight.

        @type  label: string
        @param label: Edge label.

        @type  attrs: list
        @param attrs: List of node attributes specified as (attribute, value) tuples.
        """
        pass


    @abstractmethod
    def has_edge(self, edge):
        """
        Return whether an edge exists.

        @type  edge: tuple
        @param edge: Edge.

        @rtype:  boolean
        @return: Truth-value for edge existence.
        """
        pass


    @abstractmethod
    def edge_weight(self, edge):
        """
        Get the weight of an edge.

        @type  edge: edge
        @param edge: One edge.

        @rtype:  number
        @return: Edge weight.
        """
        pass


    @abstractmethod
    def del_node(self, node):
        """
        Remove a node from the graph.

        @type  node: node
        @param node: Node identifier.
        """
        pass


class PygraphWrapper(IGraph):

    def __init__(self):
        self.graph = pygraph()
        self.graph.DEFAULT_WEIGHT = 0

    def has_edge(self, edge):
        return self.graph.has_edge(edge)

    def edge_weight(self, edge):
        return self.graph.edge_weight(edge)

    def neighbors(self, node):
        return self.graph.neighbors(node)

    def has_node(self, node):
        return self.graph.has_node(node)

    def add_edge(self, edge, wt=1, label='', attrs=[]):
        return self.graph.add_edge(edge, wt, label, attrs)

    def add_node(self, node, attrs=None):
        return self.graph.add_node(node, attrs)

    def nodes(self):
        return self.graph.nodes()

    def edges(self):
        return self.graph.edges()

    def del_node(self, node):
        return self.graph.del_node(node)
